from __future__ import annotations

import json
import re
from typing import Any, Dict, List
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

AI_PROVIDER_MODEL_CATALOG: Dict[str, List[str]] = {
    # Updated against official docs (ai.google.dev / console.groq.com / platform.openai.com) on 2026-03-09.
    "gemini": [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-3-pro-preview",
        "gemini-3.1-pro-preview-09-2025",
        "gemini-3.1-flash-preview-09-2025",
        "gemini-3.1-flash-lite-preview-09-2025",
    ],
    "groq": [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3-32b",
        "moonshotai/kimi-k2-instruct-0905",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "groq/compound",
        "groq/compound-mini",
    ],
    "openai": [
        "gpt-5.2",
        "gpt-5.1",
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        "o3",
        "o3-pro",
        "o4-mini",
    ],
}
AI_SUPPORTED_PROVIDERS = tuple(AI_PROVIDER_MODEL_CATALOG.keys())
AI_PROVIDER_DEFAULT_MODEL = {
    "gemini": "gemini-2.5-flash",
    "groq": "openai/gpt-oss-120b",
    "openai": "gpt-5-mini",
}
AI_GENERATE_TIMEOUT_SEC = 120
AI_GENERATE_OPENAI_TIMEOUT_SEC = 45

def _normalize_ai_provider(raw: Any) -> str:
    token = str(raw or "").strip().lower()
    if token in AI_SUPPORTED_PROVIDERS:
        return token
    return "gemini"


def _default_ai_model(provider: str) -> str:
    provider_token = _normalize_ai_provider(provider)
    return AI_PROVIDER_DEFAULT_MODEL.get(provider_token, "gemini-2.5-flash")


def _model_allowed_for_provider(provider: str, model: str) -> bool:
    provider_token = _normalize_ai_provider(provider)
    catalog = AI_PROVIDER_MODEL_CATALOG.get(provider_token, [])
    target = str(model or "").strip()
    if not target:
        return False
    return target in catalog


def _provider_display_name(provider: str) -> str:
    token = _normalize_ai_provider(provider)
    if token == "gemini":
        return "Gemini"
    if token == "groq":
        return "Groq"
    if token == "openai":
        return "OpenAI"
    return token



def _strip_code_fence(text: str) -> str:
    token = str(text or "").strip()
    fenced = re.match(r"^```(?:json|JSON)?\s*([\s\S]*?)\s*```$", token)
    if fenced:
        return fenced.group(1).strip()
    return token


def _extract_json_object_text(text: str) -> str:
    token = _strip_code_fence(text)
    if token.startswith("{") and token.endswith("}"):
        return token
    left = token.find("{")
    right = token.rfind("}")
    if left >= 0 and right > left:
        return token[left : right + 1]
    return token


def _parse_generated_sections(raw_text: str) -> Dict[str, str]:
    token = _extract_json_object_text(raw_text)
    payload = json.loads(token)
    if not isinstance(payload, dict):
        raise ValueError("Model response is not a JSON object.")
    sections = {
        "q": str(payload.get("q", "") or "").strip(),
        "choices": str(payload.get("choices", "") or "").strip(),
        "answer": str(payload.get("answer", "") or "").strip(),
        "solution": str(payload.get("solution", "") or "").strip(),
    }
    for key in ("q", "answer", "solution"):
        if not sections[key]:
            raise ValueError(f"Generated section `{key}` is empty.")
    return sections


def _extract_gemini_text(response_obj: Dict[str, Any]) -> str:
    candidates = response_obj.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Gemini response missing candidates.")
    first = candidates[0] if isinstance(candidates[0], dict) else {}
    content = first.get("content", {}) if isinstance(first, dict) else {}
    parts = content.get("parts", []) if isinstance(content, dict) else []
    texts: List[str] = []
    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, dict):
                text = str(part.get("text", "") or "")
                if text:
                    texts.append(text)
    merged = "\n".join(texts).strip()
    if merged:
        return merged
    if isinstance(first, dict):
        fallback = str(first.get("text", "") or "").strip()
        if fallback:
            return fallback
    raise ValueError("Gemini response contained no text.")


def _call_gemini_json(*, api_key: str, model: str, prompt: str, temperature: float = 0.45) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("Gemini API key is not configured.")
    clean_model = str(model or _default_ai_model("gemini")).strip()
    if not clean_model:
        clean_model = _default_ai_model("gemini")
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib_parse.quote(clean_model, safe='-._')}:generateContent"
    )
    query = urllib_parse.urlencode({"key": api_key})
    url = f"{endpoint}?{query}"

    body = {
        "contents": [{"parts": [{"text": str(prompt or "")}]}],
        "generationConfig": {
            "temperature": float(temperature),
            "responseMimeType": "application/json",
        },
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        },
    )
    try:
        with urllib_request.urlopen(req, timeout=AI_GENERATE_TIMEOUT_SEC) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:  # pylint: disable=broad-except
            detail = ""
        raise ValueError(f"Gemini HTTP {exc.code}: {detail[:400]}") from exc
    except urllib_error.URLError as exc:
        raise ValueError(f"Gemini request failed: {exc}") from exc

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini response is not valid JSON: {raw[:400]}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Gemini response root is not an object.")
    return parsed


def _extract_openai_chat_text(response_obj: Dict[str, Any], *, provider_name: str) -> str:
    choices = response_obj.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError(f"{provider_name} response missing choices.")
    first = choices[0] if isinstance(choices[0], dict) else {}
    message = first.get("message", {}) if isinstance(first, dict) else {}
    content = message.get("content", "") if isinstance(message, dict) else ""
    if isinstance(content, str) and content.strip():
        return content.strip()
    if isinstance(content, list):
        text_parts: List[str] = []
        for part in content:
            if not isinstance(part, dict):
                continue
            text = str(part.get("text", "") or "").strip()
            if text:
                text_parts.append(text)
        merged = "\n".join(text_parts).strip()
        if merged:
            return merged
    raise ValueError(f"{provider_name} response contained no text.")


def _extract_openai_responses_text(response_obj: Dict[str, Any], *, provider_name: str) -> str:
    top = str(response_obj.get("output_text", "") or "").strip()
    if top:
        return top

    output_items = response_obj.get("output")
    texts: List[str] = []
    if isinstance(output_items, list):
        for item in output_items:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict):
                        continue
                    text = str(part.get("text", "") or "").strip()
                    if text:
                        texts.append(text)
            fallback_text = str(item.get("text", "") or "").strip()
            if fallback_text:
                texts.append(fallback_text)

    merged = "\n".join(texts).strip()
    if merged:
        return merged

    # Defensive fallback: sometimes compatibility responses may still carry choices.
    try:
        return _extract_openai_chat_text(response_obj, provider_name=provider_name)
    except Exception:  # pylint: disable=broad-except
        pass

    raise ValueError(f"{provider_name} responses output contained no text.")


def _extract_openai_completions_text(response_obj: Dict[str, Any], *, provider_name: str) -> str:
    choices = response_obj.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError(f"{provider_name} completions response missing choices.")
    first = choices[0] if isinstance(choices[0], dict) else {}
    text = str(first.get("text", "") or "").strip()
    if text:
        return text
    raise ValueError(f"{provider_name} completions response contained no text.")


def _call_openai_endpoint_json(
    *,
    api_key: str,
    endpoint: str,
    body: Dict[str, Any],
    endpoint_name: str,
    timeout_sec: int,
) -> Dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(
        endpoint,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib_request.urlopen(req, timeout=timeout_sec) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:  # pylint: disable=broad-except
            detail = ""
        raise ValueError(f"OpenAI HTTP {exc.code}: {detail[:400]}") from exc
    except urllib_error.URLError as exc:
        raise ValueError(f"OpenAI request failed ({endpoint_name}): {exc}") from exc

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"OpenAI response is not valid JSON ({endpoint_name}): {raw[:400]}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"OpenAI response root is not an object ({endpoint_name}).")
    return parsed


def _call_openai_responses_json(*, api_key: str, model: str, prompt: str) -> Dict[str, Any]:
    clean_model = str(model or _default_ai_model("openai")).strip() or _default_ai_model("openai")
    body = {
        "model": clean_model,
        "input": str(prompt or ""),
    }
    return _call_openai_endpoint_json(
        api_key=api_key,
        endpoint="https://api.openai.com/v1/responses",
        body=body,
        endpoint_name="responses",
        timeout_sec=AI_GENERATE_OPENAI_TIMEOUT_SEC,
    )


def _call_groq_chat_json(*, api_key: str, model: str, prompt: str, temperature: float = 0.45) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("Groq API key is not configured.")
    clean_model = str(model or _default_ai_model("groq")).strip()
    if not clean_model:
        clean_model = _default_ai_model("groq")

    body = {
        "model": clean_model,
        "messages": [{"role": "user", "content": str(prompt or "")}],
        "temperature": float(temperature),
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib_request.urlopen(req, timeout=AI_GENERATE_TIMEOUT_SEC) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:  # pylint: disable=broad-except
            detail = ""
        raise ValueError(f"Groq HTTP {exc.code}: {detail[:400]}") from exc
    except urllib_error.URLError as exc:
        raise ValueError(f"Groq request failed: {exc}") from exc

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Groq response is not valid JSON: {raw[:400]}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Groq response root is not an object.")
    return parsed


def _call_openai_chat_json(*, api_key: str, model: str, prompt: str, temperature: float = 0.45) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("OpenAI API key is not configured.")
    clean_model = str(model or _default_ai_model("openai")).strip()
    if not clean_model:
        clean_model = _default_ai_model("openai")
    _ = temperature  # Some OpenAI models only accept default temperature.

    body = {
        "model": clean_model,
        "messages": [{"role": "user", "content": str(prompt or "")}],
    }
    return _call_openai_endpoint_json(
        api_key=api_key,
        endpoint="https://api.openai.com/v1/chat/completions",
        body=body,
        endpoint_name="chat.completions",
        timeout_sec=AI_GENERATE_OPENAI_TIMEOUT_SEC,
    )


def _call_openai_completions_json(*, api_key: str, model: str, prompt: str, temperature: float = 0.45) -> Dict[str, Any]:
    clean_model = str(model or _default_ai_model("openai")).strip() or _default_ai_model("openai")
    # Keep compatibility for instruction/completions models.
    body = {
        "model": clean_model,
        "prompt": str(prompt or ""),
        "temperature": float(temperature),
    }
    return _call_openai_endpoint_json(
        api_key=api_key,
        endpoint="https://api.openai.com/v1/completions",
        body=body,
        endpoint_name="completions",
        timeout_sec=AI_GENERATE_OPENAI_TIMEOUT_SEC,
    )


def _openai_http_code_from_error(error: Exception) -> int | None:
    message = str(error or "")
    matched = re.search(r"OpenAI HTTP (\d+):", message)
    if not matched:
        return None
    try:
        return int(matched.group(1))
    except ValueError:
        return None


def _openai_error_allows_fallback(error: Exception) -> bool:
    code = _openai_http_code_from_error(error)
    if code in (400, 404, 405, 422):
        return True
    message = str(error or "").lower()
    # Non-HTTP parse/shape errors can still be endpoint-shape mismatch.
    return (
        "missing choices" in message
        or "contained no text" in message
        or "response root is not an object" in message
        or "response is not valid json" in message
    )


def _is_generation_retryable_error(message: str) -> bool:
    token = str(message or "").strip().lower()
    if not token:
        return False

    non_retry_tokens = (
        "http 400",
        "http 401",
        "http 402",
        "http 403",
        "http 404",
        "http 405",
        "http 409",
        "http 410",
        "http 422",
        "http 429",
        "quota",
        "rate limit",
        "access denied",
        "browser_signature_banned",
        "owner_action_required",
        "invalid api key",
        "api key is not configured",
        "unsupported value",
        "unsupported provider",
        "not supported in the v1/chat/completions endpoint",
    )
    if any(item in token for item in non_retry_tokens):
        return False

    retry_tokens = (
        "response is not valid json",
        "response root is not an object",
        "missing choices",
        "contained no text",
        "generated section",
        "objective choices are insufficient",
        "still contains draft token",
        "timed out",
        "timeout",
        "request failed",
        "connection reset",
        "connection aborted",
        "temporarily unavailable",
        "http 500",
        "http 502",
        "http 503",
        "http 504",
    )
    return any(item in token for item in retry_tokens)


def _is_timeout_generation_error(message: str) -> bool:
    token = str(message or "").strip().lower()
    if not token:
        return False
    return "timed out" in token or "timeout" in token


def _call_ai_model_text(*, provider: str, api_key: str, model: str, prompt: str, temperature: float = 0.45) -> str:
    token = _normalize_ai_provider(provider)
    if token == "gemini":
        response_obj = _call_gemini_json(
            api_key=api_key,
            model=model,
            prompt=prompt,
            temperature=temperature,
        )
        return _extract_gemini_text(response_obj)
    if token == "groq":
        response_obj = _call_groq_chat_json(
            api_key=api_key,
            model=model,
            prompt=prompt,
            temperature=temperature,
        )
        return _extract_openai_chat_text(response_obj, provider_name="Groq")
    if token == "openai":
        errors: List[str] = []

        # 1) Prefer /v1/responses first for broad model compatibility.
        try:
            response_obj = _call_openai_responses_json(
                api_key=api_key,
                model=model,
                prompt=prompt,
            )
            return _extract_openai_responses_text(response_obj, provider_name="OpenAI")
        except Exception as exc:  # pylint: disable=broad-except
            errors.append(f"responses={exc}")
            if not _openai_error_allows_fallback(exc):
                raise

        # 2) Fallback: /v1/chat/completions for chat-native models.
        try:
            response_obj = _call_openai_chat_json(
                api_key=api_key,
                model=model,
                prompt=prompt,
                temperature=temperature,
            )
            return _extract_openai_chat_text(response_obj, provider_name="OpenAI")
        except Exception as exc:  # pylint: disable=broad-except
            errors.append(f"chat={exc}")
            if not _openai_error_allows_fallback(exc):
                raise

        # 3) Final fallback: /v1/completions for legacy completion models.
        try:
            response_obj = _call_openai_completions_json(
                api_key=api_key,
                model=model,
                prompt=prompt,
                temperature=temperature,
            )
            return _extract_openai_completions_text(response_obj, provider_name="OpenAI")
        except Exception as exc:  # pylint: disable=broad-except
            errors.append(f"completions={exc}")
            raise ValueError("OpenAI endpoint fallback failed: " + " | ".join(errors)) from exc
    raise ValueError(f"Unsupported provider: {provider}")


def _build_similar_generation_prompt(
    *,
    seed_id: str,
    seed_q: str,
    seed_choices: str,
    seed_answer: str,
    seed_solution: str,
    grade: str,
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    similarity_type: str,
    objective: bool,
    variant_index: int,
) -> str:
    objective_rule = (
        "- 객관식 문항으로 만들고, `choices`에는 5개 선택지(①~⑤)를 줄바꿈으로 제공한다."
        if objective
        else "- 주관식 문항으로 만들고, `choices`는 빈 문자열로 둔다."
    )
    return (
        "당신은 한국 고등학교 수학 문항 제작자다.\n"
        "아래 원문항을 바탕으로 유사하지만 새로운 문항 1개를 생성하라.\n"
        "반드시 대한민국 고등학교 교육과정 기호를 사용하고, 수식은 markdown LaTeX로 작성하라.\n"
        "답과 해설은 문항과 일치해야 한다.\n\n"
        "출력 형식은 반드시 JSON 객체 하나만 출력한다. 다른 텍스트를 절대 붙이지 마라.\n"
        "JSON keys: q, choices, answer, solution\n\n"
        "제약:\n"
        f"- 학년: 고{grade}\n"
        f"- 단원: {unit_l1} > {unit_l2} > {unit_l3}\n"
        f"- 변형유형: {similarity_type}\n"
        f"- 변형번호: {variant_index}\n"
        "- 문제/정답/해설 모두 한국어로 작성.\n"
        "- `solution`은 중간 계산을 간결하게 포함하고 최종 결론을 명확히 제시.\n"
        f"{objective_rule}\n"
        "- 벡터/미적분 등 해당 학년·단원을 벗어나는 풀이 기호는 사용하지 않는다.\n\n"
        f"[원본 ID] {seed_id}\n"
        "[원본 Q]\n"
        f"{seed_q.strip()}\n\n"
        "[원본 Choices]\n"
        f"{seed_choices.strip()}\n\n"
        "[원본 Answer]\n"
        f"{seed_answer.strip()}\n\n"
        "[원본 Solution]\n"
        f"{seed_solution.strip()}\n"
    )


