from __future__ import annotations

from typing import Any, Dict, Optional
import json
import re

import requests


def parse_retry_after_seconds(response: requests.Response) -> Optional[int]:
    raw = (response.headers.get("Retry-After") or "").strip()
    if not raw:
        return None
    try:
        seconds = int(float(raw))
    except ValueError:
        return None
    if seconds <= 0:
        return None
    return seconds


def should_retry_status(status_code: int) -> bool:
    return status_code in {408, 429, 500, 502, 503, 504}


def extract_json_object(raw_text: str) -> Dict[str, Any]:
    direct = raw_text.strip()
    if direct.startswith("```"):
        direct = re.sub(r"^```(?:json)?\s*", "", direct)
        direct = re.sub(r"\s*```$", "", direct)

    for candidate in (direct, raw_text):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            pass
        else:
            if isinstance(parsed, dict):
                return parsed

    decoder = json.JSONDecoder()
    for candidate in (direct, raw_text):
        for idx, char in enumerate(candidate):
            if char != "{":
                continue
            try:
                parsed, _ = decoder.raw_decode(candidate[idx:])
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed

    raise ValueError("AI response does not contain a valid JSON object.")
