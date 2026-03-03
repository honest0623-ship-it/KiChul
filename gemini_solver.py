from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import base64
import re
import time

import requests

from ai_solver_utils import (
    extract_json_object as _extract_json_object,
    parse_retry_after_seconds as _parse_retry_after_seconds,
    should_retry_status as _should_retry_status,
)


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com"
MODEL_LIST_ENDPOINT = f"{GEMINI_BASE_URL}/v1beta/models"

# Curated order: newer + higher-tier first.
DEFAULT_GEMINI_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

SCORE_TOKEN_RE = re.compile(r"\(\s*\d+(?:\.\d+)?\s*점\s*\)")


@dataclass(frozen=True)
class AISolveResult:
    qtype: str
    question_markdown: str
    choices_markdown: str
    answer_text: str
    solution_markdown: str
    raw_response_text: str


def _coerce_model_score(model_id: str) -> Tuple[int, int, int, int, str]:
    token = model_id.lower().strip()
    major = 0
    minor = 0

    matched = re.search(r"gemini-(\d+)(?:\.(\d+))?", token)
    if matched:
        major = int(matched.group(1))
        if matched.group(2):
            minor = int(matched.group(2))

    tier = 10
    if "pro" in token:
        tier = 40
    elif "flash-lite" in token or "lite" in token:
        tier = 20
    elif "flash" in token:
        tier = 30
    elif "8b" in token or "nano" in token:
        tier = 15

    stability = 0
    if "preview" in token or "exp" in token or "experimental" in token:
        stability -= 10

    return (major, minor, tier, stability, model_id)


def ranked_gemini_models(model_ids: Optional[Sequence[str]] = None) -> List[str]:
    merged: List[str] = []
    seen = set()

    incoming = list(model_ids or [])
    for item in [*incoming, *DEFAULT_GEMINI_MODELS]:
        token = item.strip()
        if not token or token in seen:
            continue
        seen.add(token)
        merged.append(token)

    return [
        row[4]
        for row in sorted(
            [_coerce_model_score(item) for item in merged],
            key=lambda x: (x[0], x[1], x[2], x[3], x[4].lower()),
            reverse=True,
        )
    ]


def _extract_model_id(raw_name: str) -> str:
    token = raw_name.strip()
    if token.startswith("models/"):
        return token.split("/", 1)[1]
    return token


def list_gemini_models(api_key: str, timeout_sec: int = 20) -> Tuple[List[str], Optional[str]]:
    if not api_key.strip():
        return [], "API key is empty."

    try:
        response = requests.get(
            MODEL_LIST_ENDPOINT,
            params={"key": api_key.strip()},
            timeout=timeout_sec,
        )
    except requests.RequestException as exc:
        return [], f"Failed to list models ({exc})"

    if response.status_code >= 400:
        snippet = response.text[:300].replace("\n", " ")
        return [], f"Model list request failed ({response.status_code}): {snippet}"

    try:
        payload = response.json()
    except ValueError:
        return [], "Model list response is not valid JSON."

    rows = payload.get("models", [])
    model_ids: List[str] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        raw_name = item.get("name")
        if not isinstance(raw_name, str) or not raw_name.strip():
            continue
        methods = item.get("supportedGenerationMethods", [])
        if isinstance(methods, list) and "generateContent" not in methods:
            continue
        model_id = _extract_model_id(raw_name)
        if model_id.lower().startswith("gemini"):
            model_ids.append(model_id)

    if not model_ids:
        return [], "No Gemini models returned from API."

    return ranked_gemini_models(model_ids), None


def _inline_data_for_image(image_path: Path) -> Tuple[str, str]:
    suffix = image_path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
    }.get(suffix, "image/png")
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return mime, encoded


def _strip_score_tokens(text: str) -> str:
    return SCORE_TOKEN_RE.sub("", text).strip()


def _normalize_qtype(raw: Any) -> str:
    token = str(raw or "").strip().lower()
    if "객관" in token or "multiple" in token or "choice" in token:
        return "객관식"
    if "단답" in token or "short" in token:
        return "단답형"
    if "서술" in token or "essay" in token or "descriptive" in token:
        return "서술형"
    return ""


def _normalize_choice_symbol(token: str) -> str:
    mapper = {"1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤"}
    return mapper.get(token, token)


def _normalize_choices(raw_choices: Any) -> str:
    if raw_choices is None:
        return ""
    lines: List[str] = []

    if isinstance(raw_choices, list):
        source_lines = [str(item).strip() for item in raw_choices if str(item).strip()]
    else:
        text = str(raw_choices).strip()
        source_lines = [line.strip() for line in text.splitlines() if line.strip()]

    for idx, line in enumerate(source_lines, start=1):
        if re.match(r"^[①②③④⑤]\s*", line):
            lines.append(line)
            continue
        if re.match(r"^[1-5][\.\)]\s*", line):
            lines.append(_normalize_choice_symbol(line[0]) + line[2:].strip())
            continue
        if len(source_lines) <= 5:
            lines.append(f"{_normalize_choice_symbol(str(idx))} {line}")
        else:
            lines.append(line)

    return "\n".join(lines).strip()


def _normalize_answer(raw_answer: Any) -> str:
    token = str(raw_answer or "").strip()
    if not token:
        return ""
    if token in {"1", "2", "3", "4", "5"}:
        return _normalize_choice_symbol(token)
    return token


def _extract_text_from_candidates(response_json: Dict[str, Any]) -> str:
    candidates = response_json.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        prompt_feedback = response_json.get("promptFeedback", {})
        if isinstance(prompt_feedback, dict):
            reason = prompt_feedback.get("blockReason")
            if reason:
                raise RuntimeError(f"Gemini blocked the request ({reason}).")
        raise RuntimeError("Gemini response has no candidates field.")

    first = candidates[0] if isinstance(candidates[0], dict) else {}
    content = first.get("content", {}) if isinstance(first, dict) else {}
    parts = content.get("parts", []) if isinstance(content, dict) else []

    texts: List[str] = []
    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunk = part["text"].strip()
                if chunk:
                    texts.append(chunk)

    if not texts:
        raise RuntimeError("Gemini response content is empty.")
    return "\n".join(texts).strip()


def _post_generate_content(
    api_key: str,
    model: str,
    payload: Dict[str, Any],
    timeout_sec: int,
) -> requests.Response:
    endpoint = f"{GEMINI_BASE_URL}/v1beta/models/{model}:generateContent"
    return requests.post(
        endpoint,
        params={"key": api_key.strip()},
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=timeout_sec,
    )


def _post_generate_content_with_retry(
    api_key: str,
    model: str,
    payload: Dict[str, Any],
    timeout_sec: int,
    max_attempts: int = 6,
    base_wait_sec: int = 12,
    max_wait_sec: int = 90,
) -> requests.Response:
    last_network_error: Optional[Exception] = None
    last_response: Optional[requests.Response] = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = _post_generate_content(
                api_key=api_key,
                model=model,
                payload=payload,
                timeout_sec=timeout_sec,
            )
            last_response = response
        except requests.RequestException as exc:
            last_network_error = exc
            if attempt >= max_attempts:
                raise
            wait_sec = min(max_wait_sec, base_wait_sec * attempt)
            time.sleep(wait_sec)
            continue

        if not _should_retry_status(response.status_code):
            return response
        if attempt >= max_attempts:
            return response

        retry_after = _parse_retry_after_seconds(response)
        wait_sec = retry_after if retry_after is not None else min(max_wait_sec, base_wait_sec * attempt)
        time.sleep(wait_sec)

    if last_response is not None:
        return last_response
    if last_network_error is not None:
        raise last_network_error
    raise RuntimeError("Gemini request failed before receiving any response.")


def _repair_json_with_gemini(
    api_key: str,
    model: str,
    raw_text: str,
    timeout_sec: int,
) -> Dict[str, Any]:
    repair_prompt = (
        "아래 텍스트를 다음 JSON 스키마의 엄격한 JSON 객체로만 변환하라. "
        "설명/코드블록/추가 텍스트 금지.\n"
        "{\n"
        '  "qtype": "객관식|단답형|서술형",\n'
        '  "question_markdown": "문제 본문",\n'
        '  "choices": ["선지1", "선지2", "..."],\n'
        '  "answer": "정답",\n'
        '  "solution_markdown": "해설"\n'
        "}\n"
        f"[원본 텍스트]\n{raw_text}"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": repair_prompt}]}],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
        },
    }
    response = _post_generate_content_with_retry(
        api_key=api_key,
        model=model,
        payload=payload,
        timeout_sec=timeout_sec,
    )
    if response.status_code >= 400:
        snippet = response.text[:260].replace("\n", " ")
        raise RuntimeError(
            f"Gemini JSON repair failed after auto-retry ({response.status_code}): {snippet}"
        )
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError("Gemini JSON repair response is not valid JSON.") from exc
    repaired_text = _extract_text_from_candidates(body)
    return _extract_json_object(repaired_text)


def solve_problem_with_gemini(
    api_key: str,
    model: str,
    image_path: Path,
    ocr_hint: str = "",
    timeout_sec: int = 120,
) -> AISolveResult:
    if not api_key.strip():
        raise ValueError("Gemini API key is empty.")
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    model_id = _extract_model_id(model)
    mime_type, image_data = _inline_data_for_image(image_path)

    system_prompt = (
        "너는 수학 고등학교 시험 DB 구축 도우미다. "
        "이미지 문제를 정확히 판독하고 아래 JSON 스키마로만 출력하라. "
        "수식은 markdown/LaTeX 형식으로 보존하라. "
        "문항 배점 표기(예: (4점), (4.2점))는 question에서 반드시 제거하라."
    )

    hint_text = ""
    if ocr_hint.strip():
        hint_text = (
            "\n\n[OCR 힌트 - 오탈자 가능성이 있으니 이미지 기준으로 최종 판단]\n"
            f"{ocr_hint.strip()}"
        )

    user_text = (
        "다음 이미지에서 문제를 추출해 아래 JSON 형식으로만 답하라.\n"
        "{\n"
        '  "qtype": "객관식|단답형|서술형",\n'
        '  "question_markdown": "문제 본문",\n'
        '  "choices": ["선지1", "선지2", "..."],\n'
        '  "answer": "정답",\n'
        '  "solution_markdown": "해설"\n'
        "}\n"
        "규칙:\n"
        "- 객관식이면 choices를 가능한 정확히 5개로 제공.\n"
        "- 단답형/서술형이면 choices는 빈 배열 가능.\n"
        "- answer를 모르더라도 빈 값 대신 최선 추론값을 작성.\n"
        "- solution_markdown에는 계산 근거를 포함.\n"
        "- 문항 번호는 question_markdown에서 제거.\n"
        f"{hint_text}"
    )

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": user_text},
                    {"inline_data": {"mime_type": mime_type, "data": image_data}},
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
        },
    }

    try:
        response = _post_generate_content_with_retry(
            api_key=api_key,
            model=model_id,
            payload=payload,
            timeout_sec=timeout_sec,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Gemini request failed ({exc})") from exc

    # Some models may reject responseMimeType; retry once without it.
    if response.status_code >= 400:
        fallback_payload = dict(payload)
        fallback_config = dict(payload.get("generationConfig", {}))
        fallback_config.pop("responseMimeType", None)
        fallback_payload["generationConfig"] = fallback_config
        try:
            fallback_response = _post_generate_content_with_retry(
                api_key=api_key,
                model=model_id,
                payload=fallback_payload,
                timeout_sec=timeout_sec,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"Gemini request failed ({exc})") from exc

        if fallback_response.status_code < response.status_code:
            response = fallback_response

    if response.status_code >= 400:
        snippet = response.text[:400].replace("\n", " ")
        raise RuntimeError(
            f"Gemini request failed after auto-retry ({response.status_code}): {snippet}"
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError("Gemini response is not valid JSON.") from exc

    content_text = _extract_text_from_candidates(body)
    try:
        parsed = _extract_json_object(content_text)
    except ValueError:
        parsed = _repair_json_with_gemini(
            api_key=api_key,
            model=model_id,
            raw_text=content_text,
            timeout_sec=timeout_sec,
        )

    qtype = _normalize_qtype(parsed.get("qtype"))
    question_md = _strip_score_tokens(str(parsed.get("question_markdown", "")).strip())
    choices_md = _normalize_choices(parsed.get("choices"))
    answer_text = _normalize_answer(parsed.get("answer"))
    solution_md = str(parsed.get("solution_markdown", "")).strip()

    if not question_md:
        raise RuntimeError("AI returned an empty question.")

    return AISolveResult(
        qtype=qtype,
        question_markdown=question_md,
        choices_markdown=choices_md,
        answer_text=answer_text,
        solution_markdown=solution_md,
        raw_response_text=content_text,
    )
