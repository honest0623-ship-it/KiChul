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


OPENAI_BASE_URL = "https://api.openai.com/v1"
MODEL_LIST_ENDPOINT = f"{OPENAI_BASE_URL}/models"
RESPONSES_ENDPOINT = f"{OPENAI_BASE_URL}/responses"
CHAT_COMPLETIONS_ENDPOINT = f"{OPENAI_BASE_URL}/chat/completions"

DEFAULT_OPENAI_MODELS = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4o",
    "gpt-4o-mini",
]

SCORE_TOKEN_RE = re.compile(r"\(\s*\d+(?:\.\d+)?\s*(?:점|pts?|points?)\s*\)", re.IGNORECASE)


@dataclass(frozen=True)
class AISolveResult:
    qtype: str
    question_markdown: str
    choices_markdown: str
    answer_text: str
    solution_markdown: str
    raw_response_text: str


def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }


def _coerce_model_score(model_id: str) -> Tuple[int, int, int, int, str]:
    token = model_id.lower().strip()
    major = 0
    minor = 0
    matched = re.search(r"gpt-(\d+)(?:\.(\d+))?", token)
    if matched:
        major = int(matched.group(1))
        if matched.group(2):
            minor = int(matched.group(2))

    tier = 10
    if "pro" in token:
        tier += 12
    if "mini" in token:
        tier -= 4
    if "nano" in token:
        tier -= 8
    if "preview" in token:
        tier -= 2

    vision_bonus = 0
    if "4o" in token or "4.1" in token:
        vision_bonus = 6

    return (major, minor, tier, vision_bonus, model_id)


def ranked_openai_models(model_ids: Optional[Sequence[str]] = None) -> List[str]:
    merged: List[str] = []
    seen = set()

    incoming = list(model_ids or [])
    for item in [*incoming, *DEFAULT_OPENAI_MODELS]:
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


def _is_supported_model(model_id: str) -> bool:
    token = (model_id or "").strip().lower()
    if not token:
        return False
    if not token.startswith("gpt-"):
        return False
    blocked = ("embedding", "audio", "tts", "whisper", "realtime", "moderation")
    return not any(flag in token for flag in blocked)


def list_openai_models(api_key: str, timeout_sec: int = 20) -> Tuple[List[str], Optional[str]]:
    if not api_key.strip():
        return [], "API key is empty."

    try:
        response = requests.get(
            MODEL_LIST_ENDPOINT,
            headers=_headers(api_key),
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

    rows = payload.get("data", [])
    model_ids: List[str] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        model_id = str(item.get("id", "")).strip()
        if _is_supported_model(model_id):
            model_ids.append(model_id)

    if not model_ids:
        return [], "No OpenAI models returned from API."
    return ranked_openai_models(model_ids), None


def _data_uri_for_image(image_path: Path) -> str:
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
    return f"data:{mime};base64,{encoded}"


def _strip_score_tokens(text: str) -> str:
    return SCORE_TOKEN_RE.sub("", text).strip()


def _normalize_qtype(raw: Any) -> str:
    token = str(raw or "").strip().lower()
    if any(flag in token for flag in ("multiple", "choice", "objective", "객관")):
        return "객관식"
    if any(flag in token for flag in ("short", "단답", "주관")):
        return "단답형"
    if any(flag in token for flag in ("essay", "descriptive", "서술")):
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
        if re.match(r"^[①②③④⑤⑴⑵⑶⑷⑸]\s*", line):
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


def _post_with_retry(
    url: str,
    api_key: str,
    payload: Dict[str, Any],
    timeout_sec: int,
    max_attempts: int = 6,
    base_wait_sec: int = 8,
    max_wait_sec: int = 60,
) -> requests.Response:
    last_network_error: Optional[Exception] = None
    last_response: Optional[requests.Response] = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.post(
                url,
                headers=_headers(api_key),
                json=payload,
                timeout=timeout_sec,
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
    raise RuntimeError("OpenAI request failed before receiving any response.")


def _extract_text_from_response(body: Dict[str, Any]) -> str:
    output_text = body.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    chunks: List[str] = []

    output = body.get("output", [])
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content", [])
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue
                text = part.get("text")
                if isinstance(text, str) and text.strip():
                    chunks.append(text.strip())

    if chunks:
        return "\n".join(chunks).strip()

    choices = body.get("choices", [])
    if isinstance(choices, list) and choices:
        first = choices[0] if isinstance(choices[0], dict) else {}
        message = first.get("message", {}) if isinstance(first, dict) else {}
        content = message.get("content", "")
        if isinstance(content, str) and content.strip():
            return content.strip()

    raise RuntimeError("OpenAI response content is empty.")


def _repair_json_with_openai(
    api_key: str,
    model: str,
    raw_text: str,
    timeout_sec: int,
) -> Dict[str, Any]:
    repair_prompt = (
        "Convert the following text into a strict JSON object with this schema only:\n"
        "{\n"
        '  "qtype": "객관식|단답형|서술형",\n'
        '  "question_markdown": "문제 본문",\n'
        '  "choices": ["선지1", "선지2", "..."],\n'
        '  "answer": "정답",\n'
        '  "solution_markdown": "해설"\n'
        "}\n"
        "No explanation, no markdown fence, JSON only.\n"
        f"[RAW]\n{raw_text}"
    )

    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": repair_prompt}],
            }
        ],
        "temperature": 0,
        "text": {"format": {"type": "json_object"}},
    }
    response = _post_with_retry(
        url=RESPONSES_ENDPOINT,
        api_key=api_key,
        payload=payload,
        timeout_sec=timeout_sec,
    )
    if response.status_code >= 400:
        snippet = response.text[:260].replace("\n", " ")
        raise RuntimeError(
            f"OpenAI JSON repair failed after auto-retry ({response.status_code}): {snippet}"
        )
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError("OpenAI JSON repair response is not valid JSON.") from exc

    repaired_text = _extract_text_from_response(body)
    return _extract_json_object(repaired_text)


def solve_problem_with_openai(
    api_key: str,
    model: str,
    image_path: Path,
    ocr_hint: str = "",
    timeout_sec: int = 120,
) -> AISolveResult:
    if not api_key.strip():
        raise ValueError("OpenAI API key is empty.")
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    model_id = model.strip() or "gpt-4.1"
    image_uri = _data_uri_for_image(image_path)

    system_prompt = (
        "You are an assistant building a Korean high-school math problem DB. "
        "Read the problem image accurately and return JSON only."
    )
    hint_text = f"\n\n[OCR HINT]\n{ocr_hint.strip()}" if ocr_hint.strip() else ""
    user_prompt = (
        "Extract this image into strict JSON with schema:\n"
        "{\n"
        '  "qtype": "객관식|단답형|서술형",\n'
        '  "question_markdown": "문제 본문",\n'
        '  "choices": ["선지1", "선지2", "..."],\n'
        '  "answer": "정답",\n'
        '  "solution_markdown": "해설"\n'
        "}\n"
        "Rules:\n"
        "- Remove score tokens like (4점), (4.2점).\n"
        "- For objective items, output up to 5 choices accurately.\n"
        "- Include concise reasoning in solution_markdown.\n"
        f"{hint_text}"
    )

    responses_payload = {
        "model": model_id,
        "temperature": 0.1,
        "text": {"format": {"type": "json_object"}},
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": image_uri},
                ],
            },
        ],
    }
    chat_payload = {
        "model": model_id,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": image_uri}},
                ],
            },
        ],
    }

    endpoint = RESPONSES_ENDPOINT
    response = _post_with_retry(
        url=endpoint,
        api_key=api_key,
        payload=responses_payload,
        timeout_sec=timeout_sec,
    )

    # Some models may reject strict JSON format in Responses API.
    if response.status_code >= 400:
        fallback_payload = dict(responses_payload)
        fallback_payload.pop("text", None)
        fallback_response = _post_with_retry(
            url=endpoint,
            api_key=api_key,
            payload=fallback_payload,
            timeout_sec=timeout_sec,
        )
        if fallback_response.status_code < response.status_code:
            response = fallback_response

    # Compatibility fallback to Chat Completions endpoint.
    if response.status_code >= 400:
        endpoint = CHAT_COMPLETIONS_ENDPOINT
        response = _post_with_retry(
            url=endpoint,
            api_key=api_key,
            payload=chat_payload,
            timeout_sec=timeout_sec,
        )
        if response.status_code >= 400:
            fallback_chat_payload = dict(chat_payload)
            fallback_chat_payload.pop("response_format", None)
            fallback_chat_response = _post_with_retry(
                url=endpoint,
                api_key=api_key,
                payload=fallback_chat_payload,
                timeout_sec=timeout_sec,
            )
            if fallback_chat_response.status_code < response.status_code:
                response = fallback_chat_response

    if response.status_code >= 400:
        snippet = response.text[:400].replace("\n", " ")
        raise RuntimeError(
            f"OpenAI request failed after auto-retry ({response.status_code}): {snippet}"
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError("OpenAI response is not valid JSON.") from exc

    content_text = _extract_text_from_response(body)
    try:
        parsed = _extract_json_object(content_text)
    except ValueError:
        parsed = _repair_json_with_openai(
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
