from __future__ import annotations

import fnmatch
from datetime import datetime
from difflib import SequenceMatcher
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from threading import Lock
from typing import Any, Dict, List
from urllib.parse import urlparse

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
import markdown
import yaml
from parser import parse_problem_file
from unit_taxonomy import (
    LEAF_PATHS,
    default_selected_unit_nodes,
    expand_unit_nodes_to_leaf_paths,
    normalize_unit_path,
    normalize_unit_triplet,
    unit_tree_for_ui,
)

from services.ai_runtime import (
    AI_PROVIDER_DEFAULT_MODEL,
    AI_PROVIDER_MODEL_CATALOG,
    AI_SUPPORTED_PROVIDERS,
    _build_similar_generation_prompt,
    _call_ai_model_text,
    _is_generation_retryable_error,
    _is_timeout_generation_error,
    _parse_generated_sections,
)


BASE_DIR = Path(__file__).resolve().parent
DB_PROBLEMS_DIR = BASE_DIR / "db" / "problems"
DB_GENERATED_CANDIDATES_DIR = BASE_DIR / "db" / "generated_candidates"
OUTPUT_DIR = BASE_DIR / "output"
VENDOR_DIR = BASE_DIR / "vendor"
PROBLEM_ID_RE = re.compile(
    r"^(?P<school>[^-]+)-(?P<year>\d{4})-G(?P<grade>\d+)-S(?P<semester>\d+)-(?P<exam>[^-]+)(?:-(?P<subject>[^-]+))?-(?P<number>\d{3})$"
)
SOURCE_NO_TAG_RE = re.compile(r"출제번호-(\d+)")
DEFAULT_OBJECTIVE_SOURCE_NUMBERS = [str(num) for num in range(1, 21)]
DEFAULT_SUBJECTIVE_SOURCE_NUMBERS = [f"SUB{num}" for num in range(1, 7)]
DEFAULT_SOURCE_LABELS = [*DEFAULT_OBJECTIVE_SOURCE_NUMBERS, *DEFAULT_SUBJECTIVE_SOURCE_NUMBERS]
IMG_TAG_RE = re.compile(
    r"<img\b(?P<before>[^>]*?)\bsrc=(?P<quote>[\"'])(?P<src>.*?)(?P=quote)(?P<after>[^>]*)>",
    re.IGNORECASE,
)
MATH_PLACEHOLDER_RE = re.compile(r"@@MATH_BLOCK_(\d+)@@")
MATH_SEGMENT_RE = re.compile(
    r"(\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|\$(?:\\.|[^$\\])+\$)",
    re.DOTALL,
)
SIMILAR_BATCH_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
SIMILAR_CANDIDATE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
GENERATED_PROBLEM_UI_ID_RE = re.compile(r"^GEN::(?P<batch>[^:]+)::(?P<candidate>.+)$")
DRAFT_TOKEN = "[DRAFT]"
DATA_SOURCE_VALUES = {"official", "generated"}
AI_RUNTIME_CONFIG = {
    "provider": "openai",
    "model": "gpt-5-mini",
    "api_keys": {"gemini": "", "groq": "", "openai": ""},
    "updated_at": "",
}
AI_CONFIG_LOCK = Lock()
SIMILAR_GENERATION_MAX_ATTEMPTS = 3
SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST = 6
SIMILAR_PROMOTION_ENABLED = False
FRONT_MATTER_CACHE_LOCK = Lock()
FRONT_MATTER_CACHE: Dict[str, tuple[int, int, Dict[str, Any]]] = {}

DEFAULTS = {
    "school": "HN",
    "year": "2025",
    "grade": "1",
    "semester": "1",
    "exam": "MID",
}
DEFAULT_EXAM_TITLE = "내신 기출"
DEFAULT_SORT_FIELD_SLOTS = ("school", "unit", "year")
PRINT_PROBLEMS_PER_PAGE_CHOICES = {4, 6, 8}
SORT_FIELDS = {"default", "unit", "school", "year", "source", "manual"}
SORT_ORDERS = {"asc", "desc"}
SUBJECT_CODE_ALIASES = {
    "COM1": "COM1",
    "COMMON1": "COM1",
    "공통수학1": "COM1",
    "공통수학1(2022개정)": "COM1",
    "COM2": "COM2",
    "COMMON2": "COM2",
    "공통수학2": "COM2",
    "공통수학2(2022개정)": "COM2",
    "ALG": "ALG",
    "대수": "ALG",
    "대수(2022개정)": "ALG",
    "CAL1": "CAL1",
    "CALC1": "CAL1",
    "미적분1": "CAL1",
    "미적분I": "CAL1",
    "미적분Ⅰ": "CAL1",
    "미적분I(2022개정)": "CAL1",
    "미적분Ⅰ(2022개정)": "CAL1",
    "STAT": "STAT",
    "확통": "STAT",
    "확률통계": "STAT",
    "확률과통계": "STAT",
    "확률과 통계": "STAT",
    "확률과 통계(2022개정)": "STAT",
}

app = Flask(__name__)
app.secret_key = "math_kichul_local_admin"


def _open_path_in_file_manager(target: Path) -> None:
    target_path = str(target)
    if hasattr(os, "startfile"):
        os.startfile(target_path)  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", target_path], cwd=str(BASE_DIR))
        return
    subprocess.Popen(["xdg-open", target_path], cwd=str(BASE_DIR))


def _resolve_unique_pdf_path(path: Path) -> Path:
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{index:03d}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def _normalize_subject_token(raw: Any) -> str:
    token = str(raw or "").strip()
    if not token:
        return ""
    token = token.replace("Ⅰ", "I")
    token = re.sub(r"\s+", "", token)
    return token.upper()


def _subject_code_from_unit_l1(unit_l1: str) -> str:
    token = str(unit_l1 or "").strip()
    if not token:
        return ""
    if token.startswith("공통수학1"):
        return "COM1"
    if token.startswith("공통수학2"):
        return "COM2"
    if token.startswith("대수"):
        return "ALG"
    if token.startswith("미적분"):
        return "CAL1"
    if token.startswith("확률과 통계"):
        return "STAT"
    return ""


def _normalize_subject_code(raw: Any, *, unit_l1: str = "", fallback: Any = "") -> str:
    token = _normalize_subject_token(raw)
    if token:
        mapped = SUBJECT_CODE_ALIASES.get(token)
        if mapped:
            return mapped
        if re.fullmatch(r"[A-Z0-9_]+", token):
            return token

    inferred = _subject_code_from_unit_l1(unit_l1)
    if inferred:
        return inferred

    fallback_token = _normalize_subject_token(fallback)
    if fallback_token:
        mapped = SUBJECT_CODE_ALIASES.get(fallback_token)
        if mapped:
            return mapped
        if re.fullmatch(r"[A-Z0-9_]+", fallback_token):
            return fallback_token
    return ""


def _parse_int(raw: str, default: int) -> int:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


def _normalize_problems_per_page(raw: str | None, default: int = 8) -> int:
    value = _parse_int(str(raw or "").strip(), default)
    if value in PRINT_PROBLEMS_PER_PAGE_CHOICES:
        return value
    return default


def _normalize_paper(raw: str | None) -> str:
    token = str(raw or "").strip().upper()
    if token in {"A4", "B4"}:
        return token
    return "A4"


def _normalize_title(raw: str | None, default: str = DEFAULT_EXAM_TITLE) -> str:
    token = str(raw or "").strip()
    return token or default


def _extract_ids(raw: str) -> List[str]:
    if not raw.strip():
        return []
    pieces = re.split(r"[\s,]+", raw.strip())
    return [item for item in pieces if item]


def _current_defaults() -> Dict[str, str]:
    merged = dict(DEFAULTS)
    for key in DEFAULTS:
        value = request.args.get(key)
        if value:
            merged[key] = value
    return merged


def _normalize_values(values: List[str], upper: bool = False) -> List[str]:
    output: List[str] = []
    seen = set()
    for raw in values:
        token = raw.strip()
        if not token:
            continue
        if upper:
            token = token.upper()
        if token in seen:
            continue
        seen.add(token)
        output.append(token)
    return output


def _extract_source_no_from_front_matter(front_matter: Dict[str, Any]) -> str:
    raw = front_matter.get("source_question_no")
    if isinstance(raw, int):
        return str(raw)
    if isinstance(raw, str):
        token = raw.strip()
        if token.isdigit():
            return str(int(token))

    tags = front_matter.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            matched = SOURCE_NO_TAG_RE.search(str(tag))
            if matched:
                return str(int(matched.group(1)))
    return ""


def _fallback_source_no(folder_number: str, front_matter: Dict[str, Any]) -> str:
    if not folder_number.isdigit():
        return ""
    number = int(folder_number)
    qtype = str(front_matter.get("type", "")).strip().lower()

    # Legacy fallback for subjective numbering (e.g. 101 -> source no 1).
    if 100 <= number < 200 and "objective" not in qtype:
        return str(number - 100)
    return str(number)


def _extract_source_kind(front_matter: Dict[str, Any], folder_number: str) -> str:
    raw_kind = str(front_matter.get("source_question_kind", "")).strip().lower()
    if raw_kind in {"objective", "obj", "multiple"}:
        return "objective"
    if raw_kind in {"subjective", "subj", "essay"}:
        return "subjective"

    qtype = str(front_matter.get("type", "")).strip().lower()
    if any(token in qtype for token in ("objective", "multiple", "choice")):
        return "objective"
    if any(token in qtype for token in ("subjective", "essay", "short answer")):
        return "subjective"

    if folder_number.isdigit() and int(folder_number) >= 100:
        return "subjective"
    return "objective"


def _build_source_label(source_no: str, source_kind: str) -> str:
    token = source_no.strip()
    if not token:
        return ""
    if source_kind == "subjective":
        return f"SUB{token}"
    return token


def _sort_source_labels(values: List[str]) -> List[str]:
    def key(item: str) -> tuple[int, int, str]:
        label = item.strip()
        subjective = label.upper().startswith("SUB")
        number_text = re.sub(r"[^0-9]", "", label)
        number = int(number_text) if number_text.isdigit() else 9999
        return (1 if subjective else 0, number, label)

    return sorted(values, key=key)


def _extract_unit_from_front_matter(front_matter: Dict[str, Any]) -> str:
    unit = str(front_matter.get("unit", "")).strip()

    pieces = [
        str(front_matter.get("unit_l1", "")).strip(),
        str(front_matter.get("unit_l2", "")).strip(),
        str(front_matter.get("unit_l3", "")).strip(),
    ]
    grade_value = _parse_int(str(front_matter.get("grade", "")).strip(), 0) or None
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
        pieces[0],
        pieces[1],
        pieces[2],
        unit_path=unit,
        grade=grade_value,
    )
    return normalize_unit_path(f"{unit_l1}>{unit_l2}>{unit_l3}", grade=grade_value)


def _extract_level_from_front_matter(front_matter: Dict[str, Any]) -> str:
    for key in ("level", "difficulty"):
        raw = front_matter.get(key)
        if isinstance(raw, int):
            return str(raw)
        token = str(raw).strip()
        if token.isdigit():
            return str(int(token))
    return ""


def _resolve_problem_folder(problem_id: str) -> Path | None:
    token = (problem_id or "").strip()
    if not PROBLEM_ID_RE.match(token):
        return None
    folder = DB_PROBLEMS_DIR / token
    if not folder.is_dir():
        return None
    return folder


def _build_generated_problem_ui_id(batch_id: str, candidate_id: str) -> str:
    return f"GEN::{batch_id}::{candidate_id}"


def _parse_generated_problem_ui_id(problem_id: str) -> tuple[str, str] | None:
    matched = GENERATED_PROBLEM_UI_ID_RE.match(str(problem_id or "").strip())
    if not matched:
        return None
    batch_id = matched.group("batch")
    candidate_id = matched.group("candidate")
    return (batch_id, candidate_id)


def _list_generated_batch_ids() -> List[str]:
    if not DB_GENERATED_CANDIDATES_DIR.is_dir():
        return []
    rows = set()

    for folder in sorted(DB_GENERATED_CANDIDATES_DIR.iterdir(), key=lambda p: p.name):
        if not folder.is_dir():
            continue

        # Flat layout candidate folder
        if (folder / "problem.md").is_file():
            batch_id = _extract_generation_batch_id(folder)
            if batch_id:
                rows.add(batch_id)
            continue

        # Legacy nested batch folder
        if not SIMILAR_BATCH_ID_RE.match(folder.name):
            continue
        if _scan_similar_candidate_dirs(folder):
            rows.add(folder.name)

    return sorted(rows)


def _normalize_data_sources(raw_values: List[str]) -> List[str]:
    normalized: List[str] = []
    seen = set()
    for value in raw_values:
        token = str(value or "").strip().lower()
        if token not in DATA_SOURCE_VALUES:
            continue
        if token in seen:
            continue
        seen.add(token)
        normalized.append(token)
    if not normalized:
        return ["official"]
    return normalized


def _normalize_data_source(raw_value: Any) -> str:
    token = str(raw_value or "").strip().lower()
    if token in DATA_SOURCE_VALUES:
        return token
    return "official"


def _normalize_generated_batches(raw_values: List[str], available_batches: List[str]) -> List[str]:
    available_set = set(available_batches)
    normalized: List[str] = []
    seen = set()
    for value in raw_values:
        token = str(value or "").strip()
        if not token or token not in available_set:
            continue
        if token in seen:
            continue
        seen.add(token)
        normalized.append(token)
    return normalized


def _resolve_problem_folder_any(problem_id: str) -> Path | None:
    official = _resolve_problem_folder(problem_id)
    if official is not None:
        return official

    parsed = _parse_generated_problem_ui_id(problem_id)
    if parsed is None:
        return None
    batch_id, candidate_id = parsed
    return _resolve_similar_candidate_folder(batch_id, candidate_id)


def _now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def _normalize_for_similarity(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def _count_choice_lines(choices_text: str) -> int:
    lines = [line.strip() for line in (choices_text or "").splitlines() if line.strip()]
    if not lines:
        return 0
    pattern = re.compile(r"^(?:[1-9][\).]|[\u2460-\u2469]|[-*])\s*")
    return sum(1 for line in lines if pattern.match(line))


def _latex_balance_issues(text: str) -> List[str]:
    issues: List[str] = []
    token = text or ""
    dollar_count = len(re.findall(r"(?<!\\)\$", token))
    if dollar_count % 2 != 0:
        issues.append("Unbalanced inline/display `$` delimiters.")
    if token.count("\\(") != token.count("\\)"):
        issues.append("Unbalanced `\\(` and `\\)` delimiters.")
    if token.count("\\[") != token.count("\\]"):
        issues.append("Unbalanced `\\[` and `\\]` delimiters.")
    return issues


def _resolve_similar_batch_folder(batch_id: str) -> Path | None:
    token = (batch_id or "").strip()
    if not SIMILAR_BATCH_ID_RE.match(token):
        return None
    batch_dir = DB_GENERATED_CANDIDATES_DIR / token
    if not batch_dir.is_dir():
        # Flat layout keeps candidate folders directly under generated root.
        if _collect_batch_candidate_dirs(token):
            return DB_GENERATED_CANDIDATES_DIR
        return None
    return batch_dir


def _resolve_similar_candidate_folder(batch_id: str, candidate_id: str) -> Path | None:
    token = (candidate_id or "").strip()
    if not SIMILAR_CANDIDATE_ID_RE.match(token):
        return None
    # 1) Flat layout: db/generated_candidates/<candidate_id>
    flat_candidate = DB_GENERATED_CANDIDATES_DIR / token
    if flat_candidate.is_dir() and (flat_candidate / "problem.md").is_file():
        flat_batch_id = _extract_generation_batch_id(flat_candidate)
        if flat_batch_id == (batch_id or "").strip():
            return flat_candidate
        if not batch_id:
            return flat_candidate

    # 2) Legacy nested layout: db/generated_candidates/<batch_id>/<candidate_id>
    batch_dir = DB_GENERATED_CANDIDATES_DIR / str(batch_id or "").strip()
    nested_candidate = batch_dir / token
    if nested_candidate.is_dir() and (nested_candidate / "problem.md").is_file():
        return nested_candidate
    return None


def _scan_flat_similar_candidate_dirs() -> List[Path]:
    rows: List[Path] = []
    if not DB_GENERATED_CANDIDATES_DIR.is_dir():
        return rows
    for child in sorted(DB_GENERATED_CANDIDATES_DIR.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if (child / "problem.md").is_file():
            rows.append(child)
    return rows


def _read_front_matter_cached(problem_md: Path) -> Dict[str, Any]:
    if not problem_md.is_file():
        return {}
    try:
        stat = problem_md.stat()
    except OSError:
        return {}

    cache_key = str(problem_md.resolve())
    cache_sig = (int(stat.st_mtime_ns), int(stat.st_size))
    with FRONT_MATTER_CACHE_LOCK:
        cached = FRONT_MATTER_CACHE.get(cache_key)
        if cached is not None and cached[0] == cache_sig[0] and cached[1] == cache_sig[1]:
            return dict(cached[2])

    front: Dict[str, Any] = {}
    try:
        parsed = parse_problem_file(problem_md)
        if isinstance(parsed.front_matter, dict):
            front = dict(parsed.front_matter)
    except Exception:
        front = {}

    with FRONT_MATTER_CACHE_LOCK:
        FRONT_MATTER_CACHE[cache_key] = (cache_sig[0], cache_sig[1], dict(front))
    return front


def _invalidate_front_matter_cache_for_file(problem_md: Path) -> None:
    cache_key = str(problem_md.resolve())
    with FRONT_MATTER_CACHE_LOCK:
        FRONT_MATTER_CACHE.pop(cache_key, None)


def _invalidate_front_matter_cache_for_folder(folder: Path) -> None:
    prefix = str(folder.resolve())
    with FRONT_MATTER_CACHE_LOCK:
        stale_keys = [key for key in FRONT_MATTER_CACHE if key.startswith(prefix)]
        for key in stale_keys:
            FRONT_MATTER_CACHE.pop(key, None)


def _read_front_matter_quiet(problem_md: Path) -> Dict[str, Any]:
    return _read_front_matter_cached(problem_md)


def _extract_generation_batch_id(candidate_dir: Path) -> str:
    problem_md = candidate_dir / "problem.md"
    if not problem_md.is_file():
        return ""
    front = _read_front_matter_quiet(problem_md)
    token = str(front.get("generation_batch_id", "")).strip()
    if token and SIMILAR_BATCH_ID_RE.match(token):
        return token
    return ""


def _collect_batch_candidate_dirs(batch_id: str) -> Dict[str, Path]:
    token = str(batch_id or "").strip()
    if not token or not SIMILAR_BATCH_ID_RE.match(token):
        return {}

    rows: Dict[str, Path] = {}

    # Flat layout candidates tagged by generation_batch_id
    for candidate_dir in _scan_flat_similar_candidate_dirs():
        generation_batch_id = _extract_generation_batch_id(candidate_dir)
        if generation_batch_id != token:
            continue
        rows.setdefault(candidate_dir.name, candidate_dir)

    # Legacy nested batch directory support
    legacy_batch_dir = DB_GENERATED_CANDIDATES_DIR / token
    if legacy_batch_dir.is_dir():
        for candidate_dir in _scan_similar_candidate_dirs(legacy_batch_dir):
            rows.setdefault(candidate_dir.name, candidate_dir)

    return rows


def _batch_report_path(batch_id: str, report_kind: str) -> Path:
    safe_batch_id = _sanitize_batch_id(batch_id) or "batch"
    safe_kind = _sanitize_batch_id(report_kind) or "report"
    return DB_GENERATED_CANDIDATES_DIR / f"{safe_kind}_{safe_batch_id}.json"


def _batch_ids_from_report_files() -> set[str]:
    rows: set[str] = set()
    if not DB_GENERATED_CANDIDATES_DIR.is_dir():
        return rows

    prefixes = ("manifest_", "validation_report_", "promotion_report_")
    for json_path in DB_GENERATED_CANDIDATES_DIR.glob("*.json"):
        name = json_path.name
        if not name.endswith(".json"):
            continue
        stem = name[:-5]
        for prefix in prefixes:
            if not stem.startswith(prefix):
                continue
            token = stem[len(prefix) :].strip()
            if token and SIMILAR_BATCH_ID_RE.match(token):
                rows.add(token)
            break
    return rows


def _existing_batch_ids() -> set[str]:
    rows = set(_list_generated_batch_ids())
    rows.update(_batch_ids_from_report_files())
    return rows


def _mask_secret(secret: str) -> str:
    token = str(secret or "").strip()
    if not token:
        return ""
    if len(token) <= 4:
        return "*" * len(token)
    return "*" * (len(token) - 4) + token[-4:]


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


def _ensure_runtime_api_keys_unlocked() -> Dict[str, str]:
    raw = AI_RUNTIME_CONFIG.get("api_keys")
    keys: Dict[str, str]
    if isinstance(raw, dict):
        keys = {str(k).strip().lower(): str(v or "").strip() for k, v in raw.items()}
    else:
        keys = {}
    legacy_gemini_key = str(AI_RUNTIME_CONFIG.get("api_key", "") or "").strip()
    if legacy_gemini_key and not keys.get("gemini"):
        keys["gemini"] = legacy_gemini_key
    for provider in AI_SUPPORTED_PROVIDERS:
        keys.setdefault(provider, "")
    AI_RUNTIME_CONFIG["api_keys"] = keys
    if "api_key" in AI_RUNTIME_CONFIG:
        AI_RUNTIME_CONFIG.pop("api_key", None)
    return keys


def _normalize_runtime_config_unlocked() -> tuple[str, str, Dict[str, str], str]:
    provider = _normalize_ai_provider(AI_RUNTIME_CONFIG.get("provider", "gemini"))
    model = str(AI_RUNTIME_CONFIG.get("model", "") or "").strip() or _default_ai_model(provider)
    updated_at = str(AI_RUNTIME_CONFIG.get("updated_at", "") or "").strip()
    keys = _ensure_runtime_api_keys_unlocked()
    AI_RUNTIME_CONFIG["provider"] = provider
    AI_RUNTIME_CONFIG["model"] = model
    AI_RUNTIME_CONFIG["updated_at"] = updated_at
    return provider, model, keys, updated_at


def _serialize_ai_runtime_config() -> Dict[str, Any]:
    with AI_CONFIG_LOCK:
        provider, model, keys, updated_at = _normalize_runtime_config_unlocked()
        api_key = str(keys.get(provider, "") or "").strip()

    return {
        "provider": provider,
        "model": model,
        "has_api_key": bool(api_key),
        "api_key_masked": _mask_secret(api_key),
        "updated_at": updated_at,
        "providers": list(AI_SUPPORTED_PROVIDERS),
        "models_by_provider": {k: list(v) for k, v in AI_PROVIDER_MODEL_CATALOG.items()},
        "default_models": dict(AI_PROVIDER_DEFAULT_MODEL),
    }


def _current_ai_runtime_secret() -> Dict[str, str]:
    with AI_CONFIG_LOCK:
        provider, model, keys, _ = _normalize_runtime_config_unlocked()
        api_key = str(keys.get(provider, "") or "").strip()
    return {"provider": provider, "model": model, "api_key": api_key}


def _sanitize_batch_id(raw: str) -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "_", str(raw or "").strip())
    return token.strip("_")


def _sanitize_candidate_id(raw: str) -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "-", str(raw or "").strip())
    token = re.sub(r"-{2,}", "-", token)
    return token.strip("-._")


def _unique_batch_id(requested: str) -> str:
    base = _sanitize_batch_id(requested) if requested else datetime.now().strftime("sim_%Y%m%d_%H%M%S")
    if not base:
        base = datetime.now().strftime("sim_%Y%m%d_%H%M%S")
    used_batch_ids = _existing_batch_ids()
    candidate = base
    index = 2
    while candidate in used_batch_ids:
        candidate = f"{base}_{index:03d}"
        index += 1
    return candidate


def _build_similar_candidate_id(
    *,
    seed_id: str,
    variant_index: int,
    variants_per_seed: int,
    batch_dir: Path,
) -> str:
    seed_token = _sanitize_candidate_id(seed_id) or "seed"
    _ = variants_per_seed  # reserved for future policy tuning
    serial = variant_index if variant_index > 0 else 1
    candidate = f"{seed_token}-sim{serial:03d}"
    while (batch_dir / candidate).exists():
        serial += 1
        candidate = f"{seed_token}-sim{serial:03d}"
    return candidate


def _seed_ids_from_payload(payload: Dict[str, Any]) -> List[str]:
    raw_ids = payload.get("seed_ids")
    ids: List[str] = []
    if isinstance(raw_ids, list):
        ids = [str(item or "").strip() for item in raw_ids]
    elif isinstance(raw_ids, str):
        ids = _extract_ids(raw_ids)
    unique: List[str] = []
    seen = set()
    for item in ids:
        if not item or item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def _as_positive_int(raw: Any, default: int, *, min_value: int = 1, max_value: int = 10) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = default
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def _save_source_snapshot(candidate_dir: Path, *, seed_id: str, q: str, choices: str, answer: str, solution: str) -> None:
    snapshot = (
        f"# Source Snapshot: {seed_id}\n\n"
        "## Q\n\n"
        f"{q.strip()}\n\n"
        "## Choices\n\n"
        f"{choices.strip()}\n\n"
        "## Answer\n\n"
        f"{answer.strip()}\n\n"
        "## Solution\n\n"
        f"{solution.strip()}\n"
    )
    (candidate_dir / "source_snapshot.md").write_text(snapshot, encoding="utf-8")


def _rewrite_preview_img_sources_from_folder(
    html_text: str,
    *,
    base_folder: Path,
    endpoint: str,
    endpoint_values: Dict[str, str],
) -> str:
    base = base_folder.resolve()

    def replace(match: re.Match[str]) -> str:
        before = match.group("before")
        quote = match.group("quote")
        src = match.group("src")
        after = match.group("after")

        source = src.strip()
        if not source or _is_external_src(source):
            return match.group(0)

        normalized = source.replace("\\", "/").lstrip("./")
        if not normalized:
            return ""

        candidate = (base_folder / normalized).resolve()
        try:
            candidate.relative_to(base)
        except ValueError:
            return ""
        if not candidate.is_file():
            return ""

        resolved = url_for(endpoint, asset_rel=normalized, **endpoint_values)
        return f"<img{before}src={quote}{resolved}{quote}{after}>"

    return IMG_TAG_RE.sub(replace, html_text)


def _is_external_src(src: str) -> bool:
    parsed = urlparse(src)
    return bool(parsed.scheme) or src.startswith("//")


def _markdown_to_html_preview(md_text: str) -> str:
    source = md_text or ""
    source = re.sub(
        r"(\\\[.*?\\\]|\$\$.*?\$\$)\n{2,}(?=\S)",
        r"\1\n",
        source,
        flags=re.DOTALL,
    )

    saved_math: List[str] = []

    def stash_math(match: re.Match[str]) -> str:
        saved_math.append(match.group(1))
        return f"@@MATH_BLOCK_{len(saved_math) - 1}@@"

    protected = MATH_SEGMENT_RE.sub(stash_math, source)
    converter = markdown.Markdown(extensions=["extra", "sane_lists", "nl2br"])
    html_text = converter.convert(protected)

    def restore_math(match: re.Match[str]) -> str:
        index = int(match.group(1))
        if index < 0 or index >= len(saved_math):
            return match.group(0)
        return escape(saved_math[index], quote=False)

    return MATH_PLACEHOLDER_RE.sub(restore_math, html_text)


def _rewrite_preview_img_sources(html_text: str, problem_id: str) -> str:
    problem_folder = _resolve_problem_folder_any(problem_id)
    if problem_folder is None:
        return html_text

    base = problem_folder.resolve()

    def replace(match: re.Match[str]) -> str:
        before = match.group("before")
        quote = match.group("quote")
        src = match.group("src")
        after = match.group("after")

        source = src.strip()
        if not source or _is_external_src(source):
            return match.group(0)

        normalized = source.replace("\\", "/").lstrip("./")
        if not normalized:
            return ""

        candidate = (problem_folder / normalized).resolve()
        try:
            candidate.relative_to(base)
        except ValueError:
            return ""

        if not candidate.is_file():
            return ""

        resolved = url_for("problem_asset", problem_id=problem_id, asset_rel=normalized)
        return f"<img{before}src={quote}{resolved}{quote}{after}>"

    return IMG_TAG_RE.sub(replace, html_text)


def _resolve_mathjax_bundle_uri() -> str:
    bundle = VENDOR_DIR / "mathjax" / "tex-svg.js"
    if bundle.is_file():
        return url_for("vendor_asset", asset_rel="mathjax/tex-svg.js")
    return ""


def _scan_problem_meta(
    *,
    data_sources: List[str] | None = None,
    generated_batches: List[str] | None = None,
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    selected_sources = _normalize_data_sources(data_sources or ["official"])
    include_official = "official" in selected_sources
    include_generated = "generated" in selected_sources

    if include_official and DB_PROBLEMS_DIR.exists():
        for folder in DB_PROBLEMS_DIR.iterdir():
            if not folder.is_dir():
                continue
            matched = PROBLEM_ID_RE.match(folder.name)
            if not matched:
                continue
            problem_md = folder / "problem.md"
            front_matter = _read_front_matter_quiet(problem_md)

            source_no = _extract_source_no_from_front_matter(front_matter)
            if not source_no:
                source_no = _fallback_source_no(matched.group("number"), front_matter)
            source_kind = _extract_source_kind(front_matter, matched.group("number"))
            source_label = _build_source_label(source_no, source_kind)
            unit = _extract_unit_from_front_matter(front_matter)
            unit_l1_hint = unit.split(">", 1)[0] if unit else ""
            level = _extract_level_from_front_matter(front_matter)
            school = str(front_matter.get("school") or matched.group("school") or "").strip().upper()
            year = str(front_matter.get("year") or matched.group("year") or "").strip()
            grade = str(front_matter.get("grade") or matched.group("grade") or "").strip()
            semester = str(front_matter.get("semester") or matched.group("semester") or "").strip()
            exam = str(front_matter.get("exam") or matched.group("exam") or "").strip().upper()
            subject = _normalize_subject_code(
                front_matter.get("subject"),
                unit_l1=unit_l1_hint,
                fallback=matched.group("subject") or "",
            )

            rows.append(
                {
                    "id": folder.name,
                    "problem_id": folder.name,
                    "display_id": folder.name,
                    "root_kind": "official",
                    "batch_id": "",
                    "folder_path": str(folder),
                    "school": school,
                    "year": year,
                    "grade": grade,
                    "semester": semester,
                    "exam": exam,
                    "subject": subject,
                    "number": matched.group("number"),
                    "source_no": source_no,
                    "source_kind": source_kind,
                    "source_label": source_label,
                    "unit": unit,
                    "level": level,
                }
            )

    if include_generated and DB_GENERATED_CANDIDATES_DIR.exists():
        available_batches = _list_generated_batch_ids()
        selected_batches = (
            _normalize_generated_batches(generated_batches or [], available_batches)
            if generated_batches is not None
            else list(available_batches)
        )
        if not selected_batches:
            selected_batches = list(available_batches)

        for batch_id in selected_batches:
            candidate_dirs = _collect_batch_candidate_dirs(batch_id)
            for folder in candidate_dirs.values():
                problem_md = folder / "problem.md"
                front_matter = _read_front_matter_quiet(problem_md)

                derived_from = str(front_matter.get("derived_from", "")).strip()
                matched = PROBLEM_ID_RE.match(derived_from)
                folder_number = matched.group("number") if matched else "001"
                source_no = _extract_source_no_from_front_matter(front_matter)
                if not source_no and matched:
                    source_no = _fallback_source_no(folder_number, front_matter)
                source_kind = _extract_source_kind(front_matter, folder_number)
                source_label = _build_source_label(source_no, source_kind)
                unit = _extract_unit_from_front_matter(front_matter)
                unit_l1_hint = unit.split(">", 1)[0] if unit else ""
                level = _extract_level_from_front_matter(front_matter)
                school = str(front_matter.get("school") or (matched.group("school") if matched else "") or "").strip().upper()
                year = str(front_matter.get("year") or (matched.group("year") if matched else "") or "").strip()
                grade = str(front_matter.get("grade") or (matched.group("grade") if matched else "") or "").strip()
                semester = str(front_matter.get("semester") or (matched.group("semester") if matched else "") or "").strip()
                exam = str(front_matter.get("exam") or (matched.group("exam") if matched else "") or "").strip().upper()
                subject = _normalize_subject_code(
                    front_matter.get("subject"),
                    unit_l1=unit_l1_hint,
                    fallback=(matched.group("subject") if matched else "") or "",
                )
                candidate_id = folder.name
                ui_id = _build_generated_problem_ui_id(batch_id, candidate_id)

                rows.append(
                    {
                        "id": ui_id,
                        "problem_id": candidate_id,
                        "display_id": candidate_id,
                        "root_kind": "generated",
                        "batch_id": batch_id,
                        "folder_path": str(folder),
                        "school": school,
                        "year": year,
                        "grade": grade,
                        "semester": semester,
                        "exam": exam,
                        "subject": subject,
                        "number": folder_number if matched else "",
                        "source_no": source_no,
                        "source_kind": source_kind,
                        "source_label": source_label,
                        "unit": unit,
                        "level": level,
                    }
                )

    return sorted(rows, key=lambda item: (str(item.get("root_kind", "")), str(item.get("batch_id", "")), str(item["id"])))


def _pattern_candidates_for_row(row: Dict[str, str]) -> List[str]:
    problem_id = str(row.get("id", "")).strip()
    display_id = str(row.get("display_id", "")).strip()
    candidate_id = str(row.get("problem_id", "")).strip()
    root_kind = str(row.get("root_kind", "")).strip()
    batch_id = str(row.get("batch_id", "")).strip()
    school = str(row.get("school", "")).strip()
    year = str(row.get("year", "")).strip()
    grade = str(row.get("grade", "")).strip()
    semester = str(row.get("semester", "")).strip()
    exam = str(row.get("exam", "")).strip()
    subject = str(row.get("subject", "")).strip()
    source_label = str(row.get("source_label", "")).strip()

    exam_token = f"{school}.{year}.G{grade}.S{semester}.{exam}{f'({subject})' if subject else ''}"
    exam_token_dash = f"{school}-{year}-G{grade}-S{semester}-{exam}{f'({subject})' if subject else ''}"
    exam_token_space = f"{school} {year} G{grade} S{semester} {exam}{f'({subject})' if subject else ''}".strip()
    id_no_number = re.sub(r"-\d{3}$", "", problem_id)

    return [
        token
        for token in (
            problem_id,
            display_id,
            candidate_id,
            id_no_number,
            exam_token,
            exam_token_dash,
            exam_token_space,
            source_label,
            root_kind,
            batch_id,
            f"{batch_id}/{candidate_id}" if batch_id and candidate_id else "",
        )
        if token
    ]


def _matches_pattern_for_row(row: Dict[str, str], pattern: str) -> bool:
    token = str(pattern or "").strip()
    if not token:
        return True
    for candidate in _pattern_candidates_for_row(row):
        if fnmatch.fnmatch(candidate, token):
            return True
    return False


def _distinct_values(rows: List[Dict[str, str]], key: str, numeric: bool = False) -> List[str]:
    values = {str(item.get(key, "")).strip() for item in rows if str(item.get(key, "")).strip()}
    if numeric:
        return sorted(values, key=lambda x: (0, int(x)) if x.isdigit() else (1, x))
    return sorted(values)


def _sort_exam_values(values: List[str]) -> List[str]:
    # Keep deterministic UI order when exam variants are mixed.
    priority = {"MID": 0, "MID2": 1, "FINAL": 2, "FINAL2": 3}

    def key(item: str) -> tuple[int, str]:
        token = item.strip().upper()
        return (priority.get(token, 2), token)

    return sorted(values, key=key)


def _normalize_sort_field(raw: str, *, slot_index: int = 1) -> str:
    token = (raw or "").strip().lower()
    if slot_index <= 1:
        if token in SORT_FIELDS:
            return token
        return "default"
    if token in SORT_FIELDS and token != "manual":
        return token
    if token == "none":
        return "none"
    return "none"


def _normalize_sort_field_slots(raw_fields: List[str]) -> List[str]:
    normalized: List[str] = []
    for slot_index in range(1, 4):
        raw = raw_fields[slot_index - 1] if slot_index - 1 < len(raw_fields) else ""
        normalized.append(_normalize_sort_field(raw, slot_index=slot_index))
    return normalized


def _effective_sort_fields(sort_fields: List[str]) -> List[str]:
    ordered: List[str] = []
    for slot_index, token in enumerate(sort_fields, start=1):
        field = _normalize_sort_field(token, slot_index=slot_index)
        if field == "none":
            continue
        if field in ordered:
            continue
        ordered.append(field)
        if field == "manual":
            break
    if not ordered:
        return ["default"]
    return ordered


def _normalize_sort_order(raw: str) -> str:
    token = (raw or "").strip().lower()
    if token in SORT_ORDERS:
        return token
    return "asc"


def _sort_selected_problem_ids(
    selected_problem_ids: List[str],
    problem_meta: List[Dict[str, str]],
    sort_fields: List[str],
    sort_order: str,
) -> List[str]:
    normalized_slots = _normalize_sort_field_slots(sort_fields)
    effective_fields = _effective_sort_fields(normalized_slots)
    sort_order = _normalize_sort_order(sort_order)
    items = list(selected_problem_ids)

    if len(items) < 2:
        return items

    if effective_fields and effective_fields[0] == "manual":
        return items

    if effective_fields == ["default"]:
        if sort_order == "desc":
            items.reverse()
        return items

    meta_by_id = {item["id"]: item for item in problem_meta}

    def _as_int(value: str, fallback: int) -> int:
        token = str(value or "").strip()
        return int(token) if token.isdigit() else fallback

    def _key_for_field(problem_id: str, sort_field: str) -> tuple[Any, ...]:
        row = meta_by_id.get(problem_id, {})
        school = str(row.get("school", "")).strip()
        year = _as_int(str(row.get("year", "")), 9999)
        grade = _as_int(str(row.get("grade", "")), 99)
        semester = _as_int(str(row.get("semester", "")), 99)
        exam = str(row.get("exam", "")).strip()
        subject = str(row.get("subject", "")).strip()
        unit = str(row.get("unit", "")).strip()
        number = _as_int(str(row.get("number", "")), 999)
        source_no = _as_int(str(row.get("source_no", "")), 999)
        source_kind = str(row.get("source_kind", "")).strip().lower()
        source_kind_base_rank = 1 if source_kind == "subjective" else 0
        # Keep objective block before subjective block even when sort_order is desc.
        source_kind_rank = (
            (1 - source_kind_base_rank)
            if sort_field == "source" and sort_order == "desc"
            else source_kind_base_rank
        )

        # For multi-key sorting, each key should include only its own dimension.
        # Tie-breaking is handled by subsequent sort fields and final problem_id.
        if sort_field == "unit":
            return (unit,)
        if sort_field == "school":
            return (school,)
        if sort_field == "year":
            return (year,)
        if sort_field == "source":
            return (source_kind_rank, source_no)
        return (problem_id,)

    def _composite_key(problem_id: str) -> tuple[Any, ...]:
        keys = []
        for field in effective_fields:
            keys.append(_key_for_field(problem_id, field))
        keys.append((problem_id,))
        return tuple(keys)

    return sorted(items, key=_composite_key, reverse=(sort_order == "desc"))


def _apply_manual_order(
    selected_problem_ids: List[str],
    manual_order_ids: List[str],
) -> tuple[List[str], List[str]]:
    selected_set = set(selected_problem_ids)
    ordered: List[str] = []
    seen = set()
    missing: List[str] = []

    for problem_id in manual_order_ids:
        if problem_id in selected_set:
            if problem_id in seen:
                continue
            seen.add(problem_id)
            ordered.append(problem_id)
            continue
        missing.append(problem_id)

    for problem_id in selected_problem_ids:
        if problem_id in seen:
            continue
        ordered.append(problem_id)

    return ordered, missing


def _build_pdf_filter_options(problem_meta: List[Dict[str, str]], *, generated_batches: List[str]) -> Dict[str, Any]:
    source_labels = set(_distinct_values(problem_meta, "source_label"))
    source_labels.update(DEFAULT_SOURCE_LABELS)
    return {
        "data_sources": ["official", "generated"],
        "generated_batches": list(generated_batches),
        "schools": _distinct_values(problem_meta, "school"),
        "years": _distinct_values(problem_meta, "year", numeric=True),
        "grades": _distinct_values(problem_meta, "grade", numeric=True),
        "semesters": _distinct_values(problem_meta, "semester", numeric=True),
        "exams": _sort_exam_values(_distinct_values(problem_meta, "exam")),
        "units": list(LEAF_PATHS),
        "unit_tree": unit_tree_for_ui(),
        "levels": _distinct_values(problem_meta, "level", numeric=True),
        "source_numbers": _sort_source_labels(list(source_labels)),
    }


def _safe_int_token(raw: str, field_name: str) -> int:
    token = str(raw or "").strip()
    if not token.isdigit():
        raise ValueError(f"'{field_name}' must be numeric.")
    return int(token)


def _rewrite_problem_md(path: Path, front: Dict[str, Any], parsed) -> None:
    _rewrite_problem_md_sections(
        path,
        front,
        q=parsed.q,
        choices=parsed.choices,
        answer=parsed.answer,
        solution=parsed.solution,
    )


def _rewrite_problem_md_sections(
    path: Path,
    front: Dict[str, Any],
    *,
    q: str,
    choices: str,
    answer: str,
    solution: str,
) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{str(q or '').strip()}\n\n"
        f"## Choices\n{str(choices or '').strip()}\n\n"
        f"## Answer\n{str(answer or '').strip()}\n\n"
        f"## Solution\n{str(solution or '').strip()}\n"
    )
    path.write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")
    _invalidate_front_matter_cache_for_file(path)


def _id_groups_for_problem_meta(problem_id: str, front: Dict[str, Any]) -> Dict[str, str]:
    candidates: List[str] = [str(problem_id or "").strip()]
    parsed_generated = _parse_generated_problem_ui_id(problem_id)
    if parsed_generated is not None:
        _, candidate_id = parsed_generated
        candidates.extend(
            [
                str(front.get("derived_from", "")).strip(),
                str(front.get("id", "")).strip(),
                str(candidate_id or "").strip(),
            ]
        )
    else:
        candidates.extend(
            [
                str(front.get("id", "")).strip(),
                str(front.get("derived_from", "")).strip(),
            ]
        )

    for token in candidates:
        if not token:
            continue
        matched = PROBLEM_ID_RE.match(token)
        if matched:
            return matched.groupdict()
    return {}


def _serialize_problem_meta(problem_id: str, front: Dict[str, Any]) -> Dict[str, Any]:
    from_id = _id_groups_for_problem_meta(problem_id, front)
    school = str(front.get("school") or from_id.get("school") or "").strip().upper()
    year = str(front.get("year") or from_id.get("year") or "").strip()
    grade = str(front.get("grade") or from_id.get("grade") or "").strip()
    semester = str(front.get("semester") or from_id.get("semester") or "").strip()
    exam = str(front.get("exam") or from_id.get("exam") or "").strip().upper()
    source_no = _extract_source_no_from_front_matter(front)
    if not source_no:
        source_no = _fallback_source_no(str(from_id.get("number", "")), front)
    source_kind = _extract_source_kind(front, str(from_id.get("number", "")))
    source_label = str(front.get("source_question_label", "")).strip()
    if not source_label:
        if source_no:
            if source_kind == "subjective":
                source_label = f"서답{source_no}번"
            else:
                source_label = str(int(source_no))
        else:
            source_label = ""
    level = _extract_level_from_front_matter(front)
    raw_unit = str(front.get("unit", "")).strip()
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
        str(front.get("unit_l1", "")).strip(),
        str(front.get("unit_l2", "")).strip(),
        str(front.get("unit_l3", "")).strip(),
        unit_path=raw_unit,
        grade=_parse_int(grade, 0) or None,
    )
    subject = _normalize_subject_code(
        front.get("subject"),
        unit_l1=unit_l1,
        fallback=from_id.get("subject") or "",
    )
    return {
        "id": problem_id,
        "school": school,
        "year": year,
        "grade": grade,
        "semester": semester,
        "exam": exam,
        "subject": subject,
        "number": str(from_id.get("number", "")),
        "type": str(front.get("type", "")).strip(),
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": source_label,
        "unit_l1": unit_l1,
        "unit_l2": unit_l2,
        "unit_l3": unit_l3,
        "unit": normalize_unit_path(f"{unit_l1}>{unit_l2}>{unit_l3}", grade=_parse_int(grade, 0) or None),
        "level": level,
        "difficulty": str(front.get("difficulty", "")).strip(),
    }


def _refresh_problem_meta_row(problem_id: str) -> Dict[str, Any] | None:
    token = str(problem_id or "").strip()
    if not token:
        return None

    parsed_generated = _parse_generated_problem_ui_id(token)
    if parsed_generated is None:
        folder = _resolve_problem_folder(token)
        if folder is None:
            return None
        matched = PROBLEM_ID_RE.match(token)
        if not matched:
            return None
        problem_md = folder / "problem.md"
        front = _read_front_matter_quiet(problem_md)
        source_no = _extract_source_no_from_front_matter(front) or _fallback_source_no(matched.group("number"), front)
        source_kind = _extract_source_kind(front, matched.group("number"))
        source_label = _build_source_label(source_no, source_kind)
        unit = _extract_unit_from_front_matter(front)
        unit_l1_hint = unit.split(">", 1)[0] if unit else ""
        subject = _normalize_subject_code(
            front.get("subject"),
            unit_l1=unit_l1_hint,
            fallback=matched.group("subject") or "",
        )
        return {
            "id": token,
            "problem_id": token,
            "display_id": token,
            "root_kind": "official",
            "batch_id": "",
            "folder_path": str(folder),
            "school": str(front.get("school") or matched.group("school") or "").strip().upper(),
            "year": str(front.get("year") or matched.group("year") or "").strip(),
            "grade": str(front.get("grade") or matched.group("grade") or "").strip(),
            "semester": str(front.get("semester") or matched.group("semester") or "").strip(),
            "exam": str(front.get("exam") or matched.group("exam") or "").strip().upper(),
            "subject": subject,
            "number": matched.group("number"),
            "source_no": source_no,
            "source_kind": source_kind,
            "source_label": source_label,
            "unit": unit,
            "level": _extract_level_from_front_matter(front),
        }

    batch_id, candidate_id = parsed_generated
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return None
    problem_md = folder / "problem.md"
    front = _read_front_matter_quiet(problem_md)

    derived_from = str(front.get("derived_from", "")).strip()
    matched = PROBLEM_ID_RE.match(derived_from)
    folder_number = matched.group("number") if matched else "001"
    source_no = _extract_source_no_from_front_matter(front)
    if not source_no and matched:
        source_no = _fallback_source_no(folder_number, front)
    source_kind = _extract_source_kind(front, folder_number)
    source_label = _build_source_label(source_no, source_kind)
    unit = _extract_unit_from_front_matter(front)
    unit_l1_hint = unit.split(">", 1)[0] if unit else ""
    subject = _normalize_subject_code(
        front.get("subject"),
        unit_l1=unit_l1_hint,
        fallback=(matched.group("subject") if matched else "") or "",
    )

    return {
        "id": token,
        "problem_id": candidate_id,
        "display_id": candidate_id,
        "root_kind": "generated",
        "batch_id": batch_id,
        "folder_path": str(folder),
        "school": str(front.get("school") or (matched.group("school") if matched else "") or "").strip().upper(),
        "year": str(front.get("year") or (matched.group("year") if matched else "") or "").strip(),
        "grade": str(front.get("grade") or (matched.group("grade") if matched else "") or "").strip(),
        "semester": str(front.get("semester") or (matched.group("semester") if matched else "") or "").strip(),
        "exam": str(front.get("exam") or (matched.group("exam") if matched else "") or "").strip().upper(),
        "subject": subject,
        "number": folder_number if matched else "",
        "source_no": source_no,
        "source_kind": source_kind,
        "source_label": source_label,
        "unit": unit,
        "level": _extract_level_from_front_matter(front),
    }


def _serialize_problem_sections(parsed) -> Dict[str, str]:
    return {
        "q": str(parsed.q or ""),
        "choices": str(parsed.choices or ""),
        "answer": str(parsed.answer or ""),
        "solution": str(parsed.solution or ""),
    }


def _build_preview_payload(problem_id: str, *, q: str, choices: str, answer: str, solution: str) -> Dict[str, Any]:
    return {
        "id": problem_id,
        "question_html": _rewrite_preview_img_sources(_markdown_to_html_preview(q), problem_id),
        "choices_html": _rewrite_preview_img_sources(_markdown_to_html_preview(choices), problem_id),
        "answer_html": _rewrite_preview_img_sources(_markdown_to_html_preview(answer), problem_id),
        "solution_html": _rewrite_preview_img_sources(_markdown_to_html_preview(solution), problem_id),
    }


def _build_similar_preview_payload(
    *,
    batch_id: str,
    candidate_id: str,
    q: str,
    choices: str,
    answer: str,
    solution: str,
) -> Dict[str, Any]:
    candidate_folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if candidate_folder is None:
        question_html = _markdown_to_html_preview(q)
        choices_html = _markdown_to_html_preview(choices)
        answer_html = _markdown_to_html_preview(answer)
        solution_html = _markdown_to_html_preview(solution)
    else:
        endpoint_values = {"batch_id": batch_id, "candidate_id": candidate_id}
        question_html = _rewrite_preview_img_sources_from_folder(
            _markdown_to_html_preview(q),
            base_folder=candidate_folder,
            endpoint="similar_asset",
            endpoint_values=endpoint_values,
        )
        choices_html = _rewrite_preview_img_sources_from_folder(
            _markdown_to_html_preview(choices),
            base_folder=candidate_folder,
            endpoint="similar_asset",
            endpoint_values=endpoint_values,
        )
        answer_html = _rewrite_preview_img_sources_from_folder(
            _markdown_to_html_preview(answer),
            base_folder=candidate_folder,
            endpoint="similar_asset",
            endpoint_values=endpoint_values,
        )
        solution_html = _rewrite_preview_img_sources_from_folder(
            _markdown_to_html_preview(solution),
            base_folder=candidate_folder,
            endpoint="similar_asset",
            endpoint_values=endpoint_values,
        )
    return {
        "id": candidate_id,
        "question_html": question_html,
        "choices_html": choices_html,
        "answer_html": answer_html,
        "solution_html": solution_html,
    }


def _next_problem_id_for_prefix(prefix: str) -> str:
    if not prefix:
        raise ValueError("empty prefix")
    used_numbers: set[int] = set()
    if DB_PROBLEMS_DIR.is_dir():
        for folder in DB_PROBLEMS_DIR.iterdir():
            if not folder.is_dir():
                continue
            matched = PROBLEM_ID_RE.match(folder.name)
            if not matched:
                continue
            row_prefix = folder.name.rsplit("-", 1)[0]
            if row_prefix != prefix:
                continue
            number_token = matched.group("number")
            if number_token.isdigit():
                used_numbers.add(int(number_token))
    candidate = (max(used_numbers) + 1) if used_numbers else 1
    if candidate > 999:
        raise ValueError(f"No available 3-digit number for prefix `{prefix}`.")
    return f"{prefix}-{candidate:03d}"


def _scan_similar_candidate_dirs(batch_dir: Path) -> List[Path]:
    rows: List[Path] = []
    if not batch_dir.is_dir():
        return rows
    for child in sorted(batch_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if not (child / "problem.md").is_file():
            continue
        rows.append(child)
    return rows


def _objective_like_candidate(front: Dict[str, Any], candidate_id: str) -> bool:
    kind = str(front.get("source_question_kind", "")).strip().lower()
    if kind in {"objective", "obj", "multiple"}:
        return True
    if kind in {"subjective", "subj", "essay"}:
        return False
    derived = str(front.get("derived_from", "")).strip()
    matched = PROBLEM_ID_RE.match(derived) or PROBLEM_ID_RE.match(candidate_id)
    if not matched:
        return True
    return int(matched.group("number")) < 100


def _read_pdf_selected(defaults: Dict[str, str], pdf_options: Dict[str, Any]) -> Dict[str, Any]:
    def pick_all_when_empty(name: str) -> List[str]:
        selected = request.args.getlist(name)
        if selected:
            return selected
        return list(pdf_options.get(name, []))

    selected_unit_nodes = request.args.getlist("unit_nodes")
    if not selected_unit_nodes:
        selected_unit_nodes = default_selected_unit_nodes()

    legacy_sort_field = request.args.get("sort_field", "")
    sort_field_slots = _normalize_sort_field_slots(
        [
            request.args.get("sort_field_1", legacy_sort_field or DEFAULT_SORT_FIELD_SLOTS[0]),
            request.args.get("sort_field_2", DEFAULT_SORT_FIELD_SLOTS[1]),
            request.args.get("sort_field_3", DEFAULT_SORT_FIELD_SLOTS[2]),
        ]
    )

    selected_data_source = _normalize_data_source(
        request.args.get("data_source", "") or (request.args.getlist("data_sources")[:1] or ["official"])[0]
    )

    return {
        "data_source": selected_data_source,
        "schools": pick_all_when_empty("schools"),
        "years": pick_all_when_empty("years"),
        "grades": pick_all_when_empty("grades"),
        "semesters": pick_all_when_empty("semesters"),
        "exams": pick_all_when_empty("exams"),
        "units": pick_all_when_empty("units"),
        "unit_nodes": selected_unit_nodes,
        "levels": pick_all_when_empty("levels"),
        "source_numbers": pick_all_when_empty("source_numbers"),
        "pattern": request.args.get("selector_pattern", ""),
        "selector_ids": request.args.get("selector_ids", ""),
        "manual_order_ids": request.args.get("manual_order_ids", ""),
        "manual_selected_ids": request.args.get("manual_selected_ids", ""),
        "sort_field_1": sort_field_slots[0],
        "sort_field_2": sort_field_slots[1],
        "sort_field_3": sort_field_slots[2],
        "sort_order": _normalize_sort_order(request.args.get("sort_order", "asc")),
        "paper": _normalize_paper(request.args.get("paper", "A4")),
        "problems_per_page": _normalize_problems_per_page(request.args.get("problems_per_page", "8")),
        "question_count": request.args.get("question_count", "0"),
        "show_source_info": request.args.get("show_source_info", "1") != "0",
        "show_unit_info": request.args.get("show_unit_info", "1") != "0",
        "show_outer_border": request.args.get("show_outer_border", "1") != "0",
        "show_inner_dividers": request.args.get("show_inner_dividers", "1") != "0",
        "teacher_view": request.args.get("teacher_view", "0") == "1",
        "reset_question_number_by_school": request.args.get("reset_question_number_by_school", "0") == "1",
        "exam_sheet": request.args.get("exam_sheet", "1") != "0",
        "answer_sheet": request.args.get("answer_sheet", "0") == "1",
        "solution_sheet": request.args.get("solution_sheet", "1") != "0",
        "title": _normalize_title(request.args.get("title"), default=DEFAULT_EXAM_TITLE),
    }


@app.get("/")
def index():
    defaults = _current_defaults()
    available_generated_batches = _list_generated_batch_ids()

    problem_meta = _scan_problem_meta(
        data_sources=["official", "generated"],
        generated_batches=available_generated_batches,
    )
    pdf_options = _build_pdf_filter_options(problem_meta, generated_batches=available_generated_batches)
    pdf_selected = _read_pdf_selected(defaults, pdf_options)
    return render_template(
        "admin.html",
        pdf_options=pdf_options,
        pdf_selected=pdf_selected,
        problem_meta=problem_meta,
        output_dir=OUTPUT_DIR,
        mathjax_bundle_uri=_resolve_mathjax_bundle_uri(),
    )


@app.get("/vendor-assets/<path:asset_rel>")
def vendor_asset(asset_rel: str):
    rel_path = (asset_rel or "").replace("\\", "/").strip()
    if not rel_path:
        abort(404)

    target = (VENDOR_DIR / rel_path).resolve()
    try:
        target.relative_to(VENDOR_DIR.resolve())
    except ValueError:
        abort(403)
    if not target.is_file():
        abort(404)

    return send_from_directory(str(VENDOR_DIR), rel_path)


@app.get("/api/problem-asset/<problem_id>/<path:asset_rel>")
def problem_asset(problem_id: str, asset_rel: str):
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        abort(404)

    rel_path = (asset_rel or "").replace("\\", "/").strip()
    if not rel_path:
        abort(404)

    target = (folder / rel_path).resolve()
    try:
        target.relative_to(folder.resolve())
    except ValueError:
        abort(403)

    if not target.is_file():
        abort(404)

    return send_from_directory(str(folder), rel_path)


@app.get("/api/similar-asset/<batch_id>/<candidate_id>/<path:asset_rel>")
def similar_asset(batch_id: str, candidate_id: str, asset_rel: str):
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        abort(404)

    rel_path = (asset_rel or "").replace("\\", "/").strip()
    if not rel_path:
        abort(404)

    target = (folder / rel_path).resolve()
    try:
        target.relative_to(folder.resolve())
    except ValueError:
        abort(403)
    if not target.is_file():
        abort(404)
    return send_from_directory(str(folder), rel_path)


@app.get("/api/problem-preview")
def problem_preview():
    problem_id = request.args.get("id", "").strip()
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    preview = _build_preview_payload(
        problem_id=problem_id,
        q=parsed.q,
        choices=parsed.choices,
        answer=parsed.answer,
        solution=parsed.solution,
    )
    preview["id"] = parsed.display_id
    preview["warnings"] = parsed.warnings
    return jsonify(preview)


@app.get("/api/problem-content")
def problem_content():
    problem_id = request.args.get("id", "").strip()
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    return jsonify(
        {
            "id": parsed.display_id,
            **_serialize_problem_sections(parsed),
            "warnings": parsed.warnings,
        }
    )


@app.post("/api/problem-preview-render")
def problem_preview_render():
    payload = request.get_json(silent=True) or {}
    problem_id = str(payload.get("id", "")).strip()
    if _resolve_problem_folder_any(problem_id) is None:
        return jsonify({"error": "problem-not-found"}), 404

    q = str(payload.get("q", "") or "")
    choices = str(payload.get("choices", "") or "")
    answer = str(payload.get("answer", "") or "")
    solution = str(payload.get("solution", "") or "")

    preview = _build_preview_payload(
        problem_id=problem_id,
        q=q,
        choices=choices,
        answer=answer,
        solution=solution,
    )
    preview["id"] = problem_id
    return jsonify(preview)


@app.post("/api/problem-content")
def update_problem_content():
    payload = request.get_json(silent=True) or {}
    problem_id = str(payload.get("id", "")).strip()
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    front = dict(parsed.front_matter or {})
    parsed_generated = _parse_generated_problem_ui_id(problem_id)
    if parsed_generated is None:
        front["id"] = problem_id
    else:
        _, candidate_id = parsed_generated
        existing_id = str(front.get("id", "")).strip()
        if existing_id:
            front["id"] = existing_id
        elif candidate_id:
            front["id"] = candidate_id

    q = str(payload.get("q", "") or "")
    choices = str(payload.get("choices", "") or "")
    answer = str(payload.get("answer", "") or "")
    solution = str(payload.get("solution", "") or "")

    try:
        _rewrite_problem_md_sections(
            problem_md,
            front,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "write-failed", "detail": str(exc)}), 500

    preview = _build_preview_payload(
        problem_id=problem_id,
        q=q,
        choices=choices,
        answer=answer,
        solution=solution,
    )
    return jsonify(
        {
            "ok": True,
            "id": problem_id,
            "sections": {
                "q": q,
                "choices": choices,
                "answer": answer,
                "solution": solution,
            },
            "preview": preview,
        }
    )


@app.get("/api/problem-meta")
def problem_meta():
    problem_id = request.args.get("id", "").strip()
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
        front = dict(parsed.front_matter or {})
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    payload = _serialize_problem_meta(problem_id, front)
    return jsonify({"id": problem_id, "meta": payload})


@app.post("/api/problem-meta")
def update_problem_meta():
    payload = request.get_json(silent=True) or {}
    problem_id = str(payload.get("id", "")).strip()
    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    front = dict(parsed.front_matter or {})
    from_id = _id_groups_for_problem_meta(problem_id, front)
    parsed_generated = _parse_generated_problem_ui_id(problem_id)

    def _pick(name: str, fallback: str = "") -> str:
        if name not in payload:
            return fallback
        return str(payload.get(name, "")).strip()

    try:
        school = _pick("school", str(front.get("school") or from_id.get("school") or "")).upper().strip()
        year = _pick("year", str(front.get("year") or from_id.get("year") or "").strip())
        grade = _pick("grade", str(front.get("grade") or from_id.get("grade") or "").strip())
        semester = _pick("semester", str(front.get("semester") or from_id.get("semester") or "").strip())
        exam = _pick("exam", str(front.get("exam") or from_id.get("exam") or "").strip()).upper()
        raw_subject = _pick("subject", str(front.get("subject") or from_id.get("subject") or "").strip())
        qtype = _pick("type", str(front.get("type", "")).strip())

        source_no = _pick(
            "source_question_no",
            _extract_source_no_from_front_matter(front) or _fallback_source_no(str(from_id.get("number", "")), front),
        )
        source_kind = _pick(
            "source_question_kind",
            _extract_source_kind(front, str(from_id.get("number", ""))),
        ).lower()
        source_label = _pick("source_question_label", str(front.get("source_question_label", "")).strip())
        level_token = _pick("level", _extract_level_from_front_matter(front))
        difficulty_token = _pick("difficulty", str(front.get("difficulty", "")).strip())

        if not school:
            raise ValueError("'school' is required.")
        year_value = _safe_int_token(year, "year")
        grade_value = _safe_int_token(grade, "grade")
        semester_value = _safe_int_token(semester, "semester")
        source_no_value = _safe_int_token(source_no, "source_question_no")
        if source_kind not in {"objective", "subjective"}:
            raise ValueError("'source_question_kind' must be objective or subjective.")

        if not source_label:
            source_label = f"서답{source_no_value}번" if source_kind == "subjective" else str(source_no_value)

        parsed_level = None
        if level_token:
            parsed_level = _safe_int_token(level_token, "level")
        elif difficulty_token:
            parsed_level = _safe_int_token(difficulty_token, "difficulty")
        if parsed_level is None:
            parsed_level = 3
        parsed_level = max(1, min(5, int(parsed_level)))

        unit_l1_input = _pick("unit_l1", str(front.get("unit_l1", "")).strip())
        unit_l2_input = _pick("unit_l2", str(front.get("unit_l2", "")).strip())
        unit_l3_input = _pick("unit_l3", str(front.get("unit_l3", "")).strip())
        if not unit_l1_input or not unit_l2_input or not unit_l3_input:
            raise ValueError("'unit_l1', 'unit_l2', 'unit_l3' are required.")
        unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
            unit_l1_input,
            unit_l2_input,
            unit_l3_input,
            grade=grade_value,
        )
        subject = _normalize_subject_code(raw_subject, unit_l1=unit_l1, fallback=from_id.get("subject") or "")
    except ValueError as exc:
        return jsonify({"error": "invalid-payload", "detail": str(exc)}), 400

    if parsed_generated is None:
        front["id"] = problem_id
    else:
        _, candidate_id = parsed_generated
        existing_id = str(front.get("id", "")).strip()
        if existing_id:
            front["id"] = existing_id
        elif candidate_id:
            front["id"] = candidate_id
    front["school"] = school
    front["year"] = year_value
    front["grade"] = grade_value
    front["semester"] = semester_value
    front["exam"] = exam
    front["subject"] = subject
    front["type"] = qtype
    front["source_question_no"] = source_no_value
    front["source_question_kind"] = source_kind
    front["source_question_label"] = source_label
    front["difficulty"] = parsed_level
    front["level"] = parsed_level
    front["unit_l1"] = unit_l1
    front["unit_l2"] = unit_l2
    front["unit_l3"] = unit_l3
    front["unit"] = f"{unit_l1}>{unit_l2}>{unit_l3}"

    try:
        _rewrite_problem_md(problem_md, front, parsed)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "write-failed", "detail": str(exc)}), 500

    refreshed = _refresh_problem_meta_row(problem_id)
    if refreshed is None:
        refreshed = _serialize_problem_meta(problem_id, front)
    return jsonify({"ok": True, "id": problem_id, "row": refreshed})


@app.post("/api/problem-delete")
def delete_problem():
    payload = request.get_json(silent=True) or {}
    problem_id = str(payload.get("id", "")).strip()
    if not problem_id:
        return jsonify({"error": "invalid-payload", "detail": "'id' is required."}), 400

    folder = _resolve_problem_folder(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    try:
        _invalidate_front_matter_cache_for_folder(folder)
        shutil.rmtree(folder)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "delete-failed", "detail": str(exc)}), 500

    return jsonify({"ok": True, "id": problem_id})


@app.post("/api/problem-open-folder")
def open_problem_folder():
    payload = request.get_json(silent=True) or {}
    problem_id = str(payload.get("id", "")).strip()
    if not problem_id:
        return jsonify({"error": "invalid-payload", "detail": "'id' is required."}), 400

    folder = _resolve_problem_folder_any(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    try:
        _open_path_in_file_manager(folder)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "open-failed", "detail": str(exc)}), 500

    return jsonify({"ok": True, "id": problem_id, "path": str(folder)})


@app.get("/api/ai-config")
def get_ai_config():
    return jsonify(_serialize_ai_runtime_config())


@app.post("/api/ai-config")
def update_ai_config():
    payload = request.get_json(silent=True) or {}

    provider_input = str(payload.get("provider", "gemini") or "gemini").strip().lower()
    if provider_input and provider_input not in AI_SUPPORTED_PROVIDERS:
        return jsonify({"error": "invalid-payload", "detail": f"Unsupported provider: {provider_input}"}), 400
    provider = _normalize_ai_provider(provider_input)

    model = str(payload.get("model", "") or "").strip() or _default_ai_model(provider)
    if not _model_allowed_for_provider(provider, model):
        return (
            jsonify(
                {
                    "error": "invalid-payload",
                    "detail": f"Unsupported model for provider `{provider}`: {model}",
                }
            ),
            400,
        )
    clear_api_key = bool(payload.get("clear_api_key"))
    api_key_raw = payload.get("api_key", None)

    changed = False
    with AI_CONFIG_LOCK:
        current_provider, _, keys, _ = _normalize_runtime_config_unlocked()
        if current_provider != provider:
            AI_RUNTIME_CONFIG["provider"] = provider
            changed = True

        if str(AI_RUNTIME_CONFIG.get("model", "")).strip() != model:
            AI_RUNTIME_CONFIG["model"] = model
            changed = True

        if clear_api_key:
            if str(keys.get(provider, "")).strip():
                keys[provider] = ""
                changed = True
        elif api_key_raw is not None:
            token = str(api_key_raw or "").strip()
            if token and token != str(keys.get(provider, "")).strip():
                keys[provider] = token
                changed = True

        if changed:
            AI_RUNTIME_CONFIG["updated_at"] = _now_iso()

    summary = _serialize_ai_runtime_config()
    return jsonify({"ok": True, **summary})


@app.post("/api/similar-generate")
def generate_similar_candidates():
    payload = request.get_json(silent=True) or {}
    seed_ids = _seed_ids_from_payload(payload)
    if not seed_ids:
        return jsonify({"error": "invalid-payload", "detail": "seed_ids is required."}), 400
    if len(seed_ids) > SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST:
        return (
            jsonify(
                {
                    "error": "too-many-seeds",
                    "detail": (
                        f"seed_ids can contain up to {SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST} items per request. "
                        "Split into smaller chunks and retry."
                    ),
                }
            ),
            400,
        )

    variants_per_seed = _as_positive_int(payload.get("variants_per_seed"), 1, min_value=1, max_value=5)
    similarity_type = str(payload.get("similarity_type", "parameter_change") or "parameter_change").strip()
    requested_batch_id = str(payload.get("batch_id", "") or "").strip()
    temperature_raw = payload.get("temperature", 0.45)
    try:
        temperature = float(temperature_raw)
    except (TypeError, ValueError):
        temperature = 0.45
    if temperature < 0.0:
        temperature = 0.0
    if temperature > 1.0:
        temperature = 1.0

    ai = _current_ai_runtime_secret()
    provider = _normalize_ai_provider(ai.get("provider", "gemini"))
    if provider not in AI_SUPPORTED_PROVIDERS:
        return jsonify({"error": "provider-not-supported", "detail": f"Unsupported provider: {provider}"}), 400
    api_key = ai.get("api_key", "")
    if not api_key:
        provider_label = _provider_display_name(provider)
        return jsonify({"error": "ai-not-configured", "detail": f"{provider_label} API key is not set."}), 400

    model_from_payload = str(payload.get("model", "") or "").strip()
    model = model_from_payload or ai.get("model", _default_ai_model(provider))
    if not model:
        model = _default_ai_model(provider)
    if not _model_allowed_for_provider(provider, model):
        return (
            jsonify(
                {
                    "error": "invalid-payload",
                    "detail": f"Unsupported model for provider `{provider}`: {model}",
                }
            ),
            400,
        )

    DB_GENERATED_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    batch_id = _unique_batch_id(requested_batch_id)

    created_rows: List[Dict[str, Any]] = []
    failed_rows: List[Dict[str, Any]] = []
    skipped_rows: List[Dict[str, Any]] = []

    for seed_id in seed_ids:
        seed_folder = _resolve_problem_folder(seed_id)
        if seed_folder is None:
            skipped_rows.append({"seed_id": seed_id, "reason": "seed-not-found"})
            continue
        seed_md = seed_folder / "problem.md"
        if not seed_md.is_file():
            skipped_rows.append({"seed_id": seed_id, "reason": "seed-problem-md-not-found"})
            continue

        try:
            seed_parsed = parse_problem_file(seed_md)
        except Exception as exc:  # pylint: disable=broad-except
            skipped_rows.append({"seed_id": seed_id, "reason": f"seed-parse-failed: {exc}"})
            continue

        seed_front = dict(seed_parsed.front_matter or {})
        objective = _objective_like_candidate(seed_front, seed_id)
        grade = str(seed_front.get("grade", "") or "").strip()
        raw_unit = str(seed_front.get("unit", "") or "").strip()
        unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
            str(seed_front.get("unit_l1", "")).strip(),
            str(seed_front.get("unit_l2", "")).strip(),
            str(seed_front.get("unit_l3", "")).strip(),
            unit_path=raw_unit,
            grade=_parse_int(grade, 0) or None,
        )

        for variant_index in range(1, variants_per_seed + 1):
            candidate_id = _build_similar_candidate_id(
                seed_id=seed_id,
                variant_index=variant_index,
                variants_per_seed=variants_per_seed,
                batch_dir=DB_GENERATED_CANDIDATES_DIR,
            )
            candidate_dir = DB_GENERATED_CANDIDATES_DIR / candidate_id
            candidate_dir.mkdir(parents=True, exist_ok=False)

            prompt = _build_similar_generation_prompt(
                seed_id=seed_id,
                seed_q=seed_parsed.q,
                seed_choices=seed_parsed.choices,
                seed_answer=seed_parsed.answer,
                seed_solution=seed_parsed.solution,
                grade=grade or "?",
                unit_l1=unit_l1 or "?",
                unit_l2=unit_l2 or "?",
                unit_l3=unit_l3 or "?",
                similarity_type=similarity_type,
                objective=objective,
                variant_index=variant_index,
            )
            (candidate_dir / "prompt.md").write_text(prompt, encoding="utf-8")
            _save_source_snapshot(
                candidate_dir,
                seed_id=seed_id,
                q=seed_parsed.q,
                choices=seed_parsed.choices,
                answer=seed_parsed.answer,
                solution=seed_parsed.solution,
            )

            front = dict(seed_front)
            front["id"] = candidate_id
            front["derived_from"] = seed_id
            front["similarity_type"] = similarity_type
            front["generation_batch_id"] = batch_id
            front["generation_model"] = f"{provider}:{model}"
            front["review_status"] = "pending"
            front["review_note"] = ""
            front["promoted_to"] = ""
            front["generated_at"] = _now_iso()

            generated_sections: Dict[str, str] | None = None
            last_error = ""
            attempt_prompt = prompt
            active_model = model
            model_used_for_candidate = model
            fallback_downgraded = False
            for attempt in range(1, SIMILAR_GENERATION_MAX_ATTEMPTS + 1):
                try:
                    text = _call_ai_model_text(
                        provider=provider,
                        api_key=api_key,
                        model=active_model,
                        prompt=attempt_prompt,
                        temperature=temperature,
                    )
                    candidate_sections = _parse_generated_sections(text)
                    if objective and _count_choice_lines(candidate_sections.get("choices", "")) < 4:
                        raise ValueError("Generated objective choices are insufficient.")
                    if any(DRAFT_TOKEN in candidate_sections.get(key, "") for key in ("q", "choices", "answer", "solution")):
                        raise ValueError("Generated output still contains draft token.")
                    generated_sections = candidate_sections
                    model_used_for_candidate = active_model
                    break
                except Exception as exc:  # pylint: disable=broad-except
                    last_error = str(exc).strip() or exc.__class__.__name__
                    if provider == "openai" and (not fallback_downgraded) and _is_timeout_generation_error(last_error):
                        fallback_model = _default_ai_model("openai")
                        if fallback_model and fallback_model != active_model:
                            active_model = fallback_model
                            fallback_downgraded = True
                            continue
                    should_retry = (
                        attempt < SIMILAR_GENERATION_MAX_ATTEMPTS
                        and _is_generation_retryable_error(last_error)
                    )
                    if not should_retry:
                        break
                    attempt_prompt = (
                        f"{prompt}\n\n"
                        "직전 출력은 형식 검증에 실패했다. 아래 오류를 반영해 JSON만 다시 출력하라.\n"
                        f"- 오류: {last_error}\n"
                    )
                    continue

            front["generation_model"] = f"{provider}:{model_used_for_candidate}"

            if generated_sections is None:
                failed_rows.append(
                    {
                        "candidate_id": candidate_id,
                        "seed_id": seed_id,
                        "reason": last_error or "unknown-generation-error",
                    }
                )
                generated_sections = {
                    "q": f"{DRAFT_TOKEN} generation failed. seed={seed_id}",
                    "choices": "1) \n2) \n3) \n4) \n5) " if objective else "",
                    "answer": f"{DRAFT_TOKEN} generation failed",
                    "solution": f"{DRAFT_TOKEN} generation failed",
                }
                front["review_note"] = f"auto-generation failed: {last_error}".strip()

            try:
                _rewrite_problem_md_sections(
                    candidate_dir / "problem.md",
                    front,
                    q=generated_sections["q"],
                    choices=generated_sections["choices"],
                    answer=generated_sections["answer"],
                    solution=generated_sections["solution"],
                )
            except Exception as exc:  # pylint: disable=broad-except
                failed_rows.append(
                    {
                        "candidate_id": candidate_id,
                        "seed_id": seed_id,
                        "reason": f"write-failed: {exc}",
                    }
                )
                continue

            created_rows.append(
                {
                    "candidate_id": candidate_id,
                    "seed_id": seed_id,
                    "objective": objective,
                    "status": "generated" if DRAFT_TOKEN not in generated_sections["q"] else "draft-fallback",
                }
            )

    manifest = {
        "batch_id": batch_id,
        "created_at": _now_iso(),
        "provider": provider,
        "model": model,
        "similarity_type": similarity_type,
        "variants_per_seed": variants_per_seed,
        "seed_ids": seed_ids,
        "summary": {
            "requested_seed_count": len(seed_ids),
            "created": len(created_rows),
            "failed": len(failed_rows),
            "skipped": len(skipped_rows),
        },
        "created": created_rows,
        "failed": failed_rows,
        "skipped": skipped_rows,
    }
    manifest_path = _batch_report_path(batch_id, "manifest")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return jsonify(
        {
            "ok": True,
            "batch_id": batch_id,
            "batch_path": str(DB_GENERATED_CANDIDATES_DIR),
            "manifest_path": str(manifest_path),
            "summary": manifest["summary"],
            "created": created_rows,
            "failed": failed_rows,
            "skipped": skipped_rows,
        }
    )


@app.get("/api/similar-batches")
def similar_batches():
    rows: List[Dict[str, Any]] = []
    if not DB_GENERATED_CANDIDATES_DIR.is_dir():
        return jsonify({"batches": rows})

    for batch_id in sorted(_list_generated_batch_ids(), reverse=True):
        candidate_dirs = _collect_batch_candidate_dirs(batch_id)
        if not candidate_dirs:
            continue
        validation_summary = {"total": 0, "ok": 0, "failed": 0}
        report_path = _batch_report_path(batch_id, "validation_report")
        legacy_report_path = DB_GENERATED_CANDIDATES_DIR / batch_id / "validation_report.json"
        if not report_path.is_file() and legacy_report_path.is_file():
            report_path = legacy_report_path

        if report_path.is_file():
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                if isinstance(report, dict):
                    raw_summary = report.get("summary", {})
                    if isinstance(raw_summary, dict):
                        validation_summary = {
                            "total": int(raw_summary.get("total", 0) or 0),
                            "ok": int(raw_summary.get("ok", 0) or 0),
                            "failed": int(raw_summary.get("failed", 0) or 0),
                        }
            except Exception:
                validation_summary = {"total": 0, "ok": 0, "failed": 0}

        latest_mtime = 0.0
        for candidate_dir in candidate_dirs.values():
            try:
                latest_mtime = max(latest_mtime, candidate_dir.stat().st_mtime)
            except Exception:
                continue

        rows.append(
            {
                "batch_id": batch_id,
                "candidate_count": len(candidate_dirs),
                "created_at": datetime.fromtimestamp(latest_mtime).isoformat(timespec="seconds") if latest_mtime else "",
                "validation": validation_summary,
            }
        )
    return jsonify({"batches": rows})


@app.get("/api/similar-candidates")
def similar_candidates():
    batch_id = request.args.get("batch_id", "").strip()
    candidate_dirs = _collect_batch_candidate_dirs(batch_id)
    if not candidate_dirs:
        return jsonify({"error": "batch-not-found"}), 404

    validation_index: Dict[str, Dict[str, Any]] = {}
    report_path = _batch_report_path(batch_id, "validation_report")
    legacy_report_path = DB_GENERATED_CANDIDATES_DIR / batch_id / "validation_report.json"
    if not report_path.is_file() and legacy_report_path.is_file():
        report_path = legacy_report_path
    if report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            for row in report.get("results", []) if isinstance(report, dict) else []:
                candidate_id = str(row.get("candidate_id", "")).strip()
                if candidate_id:
                    validation_index[candidate_id] = row
        except Exception:
            validation_index = {}

    rows: List[Dict[str, Any]] = []
    for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
        candidate_id = cdir.name
        try:
            parsed = parse_problem_file(cdir / "problem.md")
        except Exception as exc:  # pylint: disable=broad-except
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "review_status": "parse-failed",
                    "review_note": str(exc),
                    "derived_from": "",
                }
            )
            continue

        front = dict(parsed.front_matter or {})
        has_draft = any(
            DRAFT_TOKEN in str(section or "")
            for section in (parsed.q, parsed.choices, parsed.answer, parsed.solution)
        )
        review_note = str(front.get("review_note", "")).strip()
        validation = validation_index.get(candidate_id, {})
        rows.append(
            {
                "candidate_id": candidate_id,
                "derived_from": str(front.get("derived_from", "")).strip(),
                "similarity_type": str(front.get("similarity_type", "")).strip(),
                "review_status": str(front.get("review_status", "pending") or "pending").strip().lower(),
                "review_note": review_note,
                "has_draft": has_draft,
                "auto_failed": review_note.lower().startswith("auto-generation failed"),
                "promoted_to": str(front.get("promoted_to", "")).strip(),
                "generation_batch_id": str(front.get("generation_batch_id", "")).strip(),
                "warnings": parsed.warnings,
                "validation": {
                    "ok": bool(validation.get("ok", False)) if validation else None,
                    "error_count": len(validation.get("errors", [])) if isinstance(validation, dict) else 0,
                    "warning_count": len(validation.get("warnings", [])) if isinstance(validation, dict) else 0,
                    "similarity_ratio": validation.get("similarity_ratio") if isinstance(validation, dict) else None,
                },
            }
        )
    return jsonify({"batch_id": batch_id, "candidates": rows})


@app.get("/api/similar-preview")
def similar_preview():
    batch_id = request.args.get("batch_id", "").strip()
    candidate_id = request.args.get("candidate_id", "").strip()
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404
    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    preview = _build_similar_preview_payload(
        batch_id=batch_id,
        candidate_id=candidate_id,
        q=parsed.q,
        choices=parsed.choices,
        answer=parsed.answer,
        solution=parsed.solution,
    )
    preview["batch_id"] = batch_id
    preview["candidate_id"] = candidate_id
    preview["warnings"] = parsed.warnings
    return jsonify(preview)


@app.get("/api/similar-content")
def similar_content():
    batch_id = request.args.get("batch_id", "").strip()
    candidate_id = request.args.get("candidate_id", "").strip()
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404
    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    front = dict(parsed.front_matter or {})
    return jsonify(
        {
            "batch_id": batch_id,
            "candidate_id": candidate_id,
            **_serialize_problem_sections(parsed),
            "review_status": str(front.get("review_status", "pending") or "pending").strip().lower(),
            "review_note": str(front.get("review_note", "")).strip(),
            "derived_from": str(front.get("derived_from", "")).strip(),
            "warnings": parsed.warnings,
        }
    )


@app.post("/api/similar-preview-render")
def render_similar_preview_draft():
    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_id = str(payload.get("candidate_id", "")).strip()
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404

    q = str(payload.get("q", "") or "")
    choices = str(payload.get("choices", "") or "")
    answer = str(payload.get("answer", "") or "")
    solution = str(payload.get("solution", "") or "")

    preview = _build_similar_preview_payload(
        batch_id=batch_id,
        candidate_id=candidate_id,
        q=q,
        choices=choices,
        answer=answer,
        solution=solution,
    )
    return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "preview": preview})


@app.post("/api/similar-content")
def update_similar_content():
    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_id = str(payload.get("candidate_id", "")).strip()
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404
    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    front = dict(parsed.front_matter or {})
    front["id"] = candidate_id
    q = str(payload.get("q", "") or "")
    choices = str(payload.get("choices", "") or "")
    answer = str(payload.get("answer", "") or "")
    solution = str(payload.get("solution", "") or "")

    try:
        _rewrite_problem_md_sections(
            problem_md,
            front,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "write-failed", "detail": str(exc)}), 500

    preview = _build_similar_preview_payload(
        batch_id=batch_id,
        candidate_id=candidate_id,
        q=q,
        choices=choices,
        answer=answer,
        solution=solution,
    )
    return jsonify(
        {
            "ok": True,
            "batch_id": batch_id,
            "candidate_id": candidate_id,
            "sections": {"q": q, "choices": choices, "answer": answer, "solution": solution},
            "preview": preview,
        }
    )


@app.post("/api/similar-review")
def update_similar_review():
    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_id = str(payload.get("candidate_id", "")).strip()
    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404
    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    status = str(payload.get("review_status", "")).strip().lower()
    if status not in {"pending", "approved", "rejected"}:
        return jsonify({"error": "invalid-payload", "detail": "review_status must be pending|approved|rejected"}), 400
    note = str(payload.get("review_note", "") or "").strip()

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    front = dict(parsed.front_matter or {})
    front["id"] = candidate_id
    front["review_status"] = status
    front["review_note"] = note
    front["reviewed_at"] = _now_iso()

    try:
        _rewrite_problem_md_sections(
            problem_md,
            front,
            q=parsed.q,
            choices=parsed.choices,
            answer=parsed.answer,
            solution=parsed.solution,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "write-failed", "detail": str(exc)}), 500

    return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "review_status": status, "review_note": note})


@app.post("/api/similar-delete")
def delete_similar_candidate():
    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_id = str(payload.get("candidate_id", "")).strip()
    if not batch_id or not candidate_id:
        return jsonify({"error": "invalid-payload", "detail": "batch_id and candidate_id are required"}), 400

    folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
    if folder is None:
        return jsonify({"error": "candidate-not-found"}), 404

    try:
        resolved_folder = folder.resolve()
    except Exception:
        resolved_folder = folder

    try:
        resolved_folder.relative_to(DB_GENERATED_CANDIDATES_DIR.resolve())
    except ValueError:
        return jsonify({"error": "candidate-not-found"}), 404

    if not resolved_folder.is_dir():
        return jsonify({"error": "candidate-not-found"}), 404

    try:
        _invalidate_front_matter_cache_for_folder(resolved_folder)
        shutil.rmtree(resolved_folder)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "delete-failed", "detail": str(exc)}), 500

    legacy_batch_dir = DB_GENERATED_CANDIDATES_DIR / batch_id
    if legacy_batch_dir.is_dir():
        try:
            if resolved_folder.parent.resolve() == legacy_batch_dir.resolve() and not any(legacy_batch_dir.iterdir()):
                legacy_batch_dir.rmdir()
        except Exception:
            # Empty legacy batch folder cleanup is best-effort only.
            pass

    return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "deleted_path": str(resolved_folder)})


@app.post("/api/similar-validate")
def validate_similar_batch():
    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_dirs = _collect_batch_candidate_dirs(batch_id)
    if not candidate_dirs:
        return jsonify({"error": "batch-not-found"}), 404

    candidate_ids_raw = str(payload.get("candidate_ids", "") or "").strip()
    selected_ids = set(_extract_ids(candidate_ids_raw))
    max_similarity = payload.get("max_similarity", 0.92)
    try:
        max_similarity_value = float(max_similarity)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid-payload", "detail": "max_similarity must be numeric"}), 400

    results: List[Dict[str, Any]] = []
    for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
        candidate_id = cdir.name
        if selected_ids and candidate_id not in selected_ids:
            continue

        errors: List[str] = []
        warnings: List[str] = []
        similarity_ratio = 0.0
        try:
            parsed = parse_problem_file(cdir / "problem.md")
        except Exception as exc:  # pylint: disable=broad-except
            results.append(
                {
                    "candidate_id": candidate_id,
                    "ok": False,
                    "similarity_ratio": 1.0,
                    "errors": [f"Parse failed: {exc}"],
                    "warnings": [],
                }
            )
            continue

        front = dict(parsed.front_matter or {})
        for section_name in ("q", "choices", "answer", "solution"):
            value = str(getattr(parsed, section_name, "") or "").strip()
            if not value:
                errors.append(f"Section `{section_name}` is empty.")
            if DRAFT_TOKEN in value:
                errors.append(f"Section `{section_name}` still contains draft token.")
            for issue in _latex_balance_issues(value):
                warnings.append(f"{section_name}: {issue}")

        if _objective_like_candidate(front, candidate_id):
            count = _count_choice_lines(parsed.choices)
            if count < 4:
                errors.append(f"Objective question has too few option-like lines ({count}).")

        derived_from = str(front.get("derived_from", "")).strip()
        if derived_from:
            source_md = DB_PROBLEMS_DIR / derived_from / "problem.md"
            if source_md.is_file():
                try:
                    source = parse_problem_file(source_md)
                    similarity_ratio = SequenceMatcher(
                        None,
                        _normalize_for_similarity(source.q),
                        _normalize_for_similarity(parsed.q),
                    ).ratio()
                    if similarity_ratio > max_similarity_value:
                        errors.append(
                            f"Q similarity too high vs source ({similarity_ratio:.3f} > {max_similarity_value:.3f})."
                        )
                    elif similarity_ratio > max_similarity_value - 0.08:
                        warnings.append(f"Q similarity near threshold ({similarity_ratio:.3f}).")
                except Exception as exc:  # pylint: disable=broad-except
                    warnings.append(f"Source parse failed for similarity check: {exc}")
            else:
                warnings.append(f"Source problem not found: {derived_from}")
        else:
            warnings.append("`derived_from` is missing.")

        results.append(
            {
                "candidate_id": candidate_id,
                "ok": len(errors) == 0,
                "similarity_ratio": similarity_ratio,
                "errors": errors,
                "warnings": warnings,
            }
        )

    failed = [row for row in results if not row.get("ok")]
    report = {
        "batch_id": batch_id,
        "validated_at": _now_iso(),
        "max_similarity": max_similarity_value,
        "summary": {"total": len(results), "ok": len(results) - len(failed), "failed": len(failed)},
        "results": results,
    }
    report_path = _batch_report_path(batch_id, "validation_report")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return jsonify({"ok": True, "batch_id": batch_id, "summary": report["summary"], "results": results, "report_path": str(report_path)})


@app.post("/api/similar-promote")
def promote_similar_candidates():
    if not SIMILAR_PROMOTION_ENABLED:
        return jsonify(
            {
                "error": "policy-disabled",
                "detail": "Promotion is disabled by policy. Official DB and generated candidates DB must remain separated.",
            }
        ), 403

    payload = request.get_json(silent=True) or {}
    batch_id = str(payload.get("batch_id", "")).strip()
    candidate_dirs = _collect_batch_candidate_dirs(batch_id)
    if not candidate_dirs:
        return jsonify({"error": "batch-not-found"}), 404

    selected_ids = set(_extract_ids(str(payload.get("candidate_ids", "") or "").strip()))
    force = bool(payload.get("force"))

    promoted: List[Dict[str, str]] = []
    skipped: List[Dict[str, str]] = []

    for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
        candidate_id = cdir.name
        if selected_ids and candidate_id not in selected_ids:
            continue
        try:
            parsed = parse_problem_file(cdir / "problem.md")
        except Exception as exc:  # pylint: disable=broad-except
            skipped.append({"candidate_id": candidate_id, "reason": f"parse-failed: {exc}"})
            continue
        front = dict(parsed.front_matter or {})
        status = str(front.get("review_status", "")).strip().lower()
        if status != "approved" and not force:
            skipped.append({"candidate_id": candidate_id, "reason": f"review_status={status or 'none'}"})
            continue
        if any(DRAFT_TOKEN in str(getattr(parsed, sec, "") or "") for sec in ("q", "choices", "answer", "solution")):
            skipped.append({"candidate_id": candidate_id, "reason": "contains-draft-token"})
            continue

        derived_from = str(front.get("derived_from", "")).strip()
        source_match = PROBLEM_ID_RE.match(derived_from)
        if not source_match:
            skipped.append({"candidate_id": candidate_id, "reason": "invalid-derived_from"})
            continue

        prefix = derived_from.rsplit("-", 1)[0]
        try:
            new_id = _next_problem_id_for_prefix(prefix)
        except ValueError as exc:
            skipped.append({"candidate_id": candidate_id, "reason": str(exc)})
            continue

        target_dir = DB_PROBLEMS_DIR / new_id
        if target_dir.exists():
            skipped.append({"candidate_id": candidate_id, "reason": "target-already-exists"})
            continue

        try:
            shutil.copytree(cdir, target_dir)
            for extra_name in ("prompt.md", "source_snapshot.md", "validation_report.json"):
                extra = target_dir / extra_name
                if extra.exists():
                    if extra.is_dir():
                        shutil.rmtree(extra)
                    else:
                        extra.unlink()

            promoted_front = dict(front)
            promoted_front["id"] = new_id
            promoted_front["promoted_from"] = candidate_id
            promoted_front["promoted_at"] = _now_iso()
            _rewrite_problem_md_sections(
                target_dir / "problem.md",
                promoted_front,
                q=parsed.q,
                choices=parsed.choices,
                answer=parsed.answer,
                solution=parsed.solution,
            )

            front["promoted_to"] = new_id
            front["review_status"] = "promoted"
            front["promoted_at"] = _now_iso()
            _rewrite_problem_md_sections(
                cdir / "problem.md",
                front,
                q=parsed.q,
                choices=parsed.choices,
                answer=parsed.answer,
                solution=parsed.solution,
            )
            promoted.append({"candidate_id": candidate_id, "new_problem_id": new_id})
        except Exception as exc:  # pylint: disable=broad-except
            skipped.append({"candidate_id": candidate_id, "reason": f"promote-failed: {exc}"})

    report = {
        "batch_id": batch_id,
        "promoted_at": _now_iso(),
        "promoted": promoted,
        "skipped": skipped,
    }
    report_path = _batch_report_path(batch_id, "promotion_report")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return jsonify(
        {
            "ok": True,
            "batch_id": batch_id,
            "promoted": promoted,
            "skipped": skipped,
            "report_path": str(report_path),
        }
    )


@app.get("/open-output")
def open_output_folder():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        _open_path_in_file_manager(OUTPUT_DIR)
        flash(f"출력 폴더를 열었습니다: {OUTPUT_DIR}", "success")
    except Exception as exc:  # pylint: disable=broad-except
        flash(f"출력 폴더 열기 실패: {exc}", "warning")
    return redirect(url_for("index", **_current_defaults()))


@app.post("/render")
def render_pdf():
    def _first_or(values: List[str], fallback: str) -> str:
        return values[0] if values else fallback

    defaults = _current_defaults()
    schools = _normalize_values(request.form.getlist("schools"), upper=True)
    years = _normalize_values(request.form.getlist("years"))
    grades = _normalize_values(request.form.getlist("grades"))
    semesters = _normalize_values(request.form.getlist("semesters"))
    exams = _normalize_values(request.form.getlist("exams"), upper=True)
    unit_nodes = _normalize_values(request.form.getlist("unit_nodes"))
    if not unit_nodes:
        unit_nodes = default_selected_unit_nodes()
    units = expand_unit_nodes_to_leaf_paths(unit_nodes)
    levels = _normalize_values(request.form.getlist("levels"))
    source_numbers = _normalize_values(request.form.getlist("source_numbers"))
    selected_data_source = _normalize_data_source(request.form.get("data_source", "official"))

    selector_ids = _extract_ids(request.form.get("selector_ids", ""))
    manual_order_ids = _extract_ids(request.form.get("manual_order_ids", ""))
    manual_selected_supplied = "manual_selected_ids" in request.form
    manual_selected_ids = _extract_ids(request.form.get("manual_selected_ids", ""))
    pattern = request.form.get("selector_pattern", "").strip()
    legacy_sort_field = request.form.get("sort_field", "")
    sort_field_slots = _normalize_sort_field_slots(
        [
            request.form.get("sort_field_1", legacy_sort_field or DEFAULT_SORT_FIELD_SLOTS[0]),
            request.form.get("sort_field_2", DEFAULT_SORT_FIELD_SLOTS[1]),
            request.form.get("sort_field_3", DEFAULT_SORT_FIELD_SLOTS[2]),
        ]
    )
    effective_sort_fields = _effective_sort_fields(sort_field_slots)
    primary_sort_field = sort_field_slots[0]
    sort_order = _normalize_sort_order(request.form.get("sort_order", "asc"))
    paper = _normalize_paper(request.form.get("paper", "A4"))
    problems_per_page = _normalize_problems_per_page(request.form.get("problems_per_page", "8"))
    question_count = max(_parse_int(request.form.get("question_count", "0"), 0), 0)
    show_source_info = bool(request.form.get("show_source_info"))
    show_unit_info = bool(request.form.get("show_unit_info"))
    show_outer_border = bool(request.form.get("show_outer_border"))
    show_inner_dividers = bool(request.form.get("show_inner_dividers"))
    teacher_view = bool(request.form.get("teacher_view"))
    reset_question_number_by_school = bool(request.form.get("reset_question_number_by_school"))
    include_exam_sheet = bool(request.form.get("exam_sheet"))
    append_answer_sheet = bool(request.form.get("answer_sheet"))
    append_solution_sheet = bool(request.form.get("solution_sheet"))
    title = _normalize_title(request.form.get("title"), default=DEFAULT_EXAM_TITLE)

    problem_meta = _scan_problem_meta(
        data_sources=[selected_data_source],
    )
    meta_by_id = {item["id"]: item for item in problem_meta}
    available_ids = {item["id"] for item in problem_meta}
    manual_selected_ids = [item for item in manual_selected_ids if item in available_ids]
    manual_selection_active = manual_selected_supplied and (primary_sort_field == "manual" or bool(manual_order_ids))
    selected_problem_ids: List[str] = []

    if selector_ids:
        selected_problem_ids = [item for item in selector_ids if item in available_ids]
        missing_ids = [item for item in selector_ids if item not in available_ids]
        if missing_ids:
            flash(f"존재하지 않는 ID 제외: {', '.join(missing_ids[:10])}", "warning")
    else:
        for item in problem_meta:
            if schools and item["school"] not in schools:
                continue
            if years and item["year"] not in years:
                continue
            if grades and item["grade"] not in grades:
                continue
            if semesters and item["semester"] not in semesters:
                continue
            if exams and item["exam"] not in exams:
                continue
            if units and item.get("unit", "") not in units:
                continue
            if levels and item.get("level", "") not in levels:
                continue
            if source_numbers and str(item.get("source_label", "")) not in source_numbers:
                continue
            selected_problem_ids.append(item["id"])

    if pattern:
        selected_problem_ids = [
            item
            for item in selected_problem_ids
            if _matches_pattern_for_row(meta_by_id.get(item, {}), pattern)
        ]

    if manual_selection_active:
        selected_manual_set = set(manual_selected_ids)
        selected_problem_ids = [item for item in selected_problem_ids if item in selected_manual_set]

    if primary_sort_field == "manual":
        manual_reference_ids = (
            manual_selected_ids
            if manual_selection_active
            else (manual_order_ids if manual_order_ids else selector_ids)
        )
        selected_problem_ids, missing_manual_ids = _apply_manual_order(
            selected_problem_ids=selected_problem_ids,
            manual_order_ids=manual_reference_ids,
        )
        if not manual_reference_ids and not (manual_selection_active and not manual_selected_ids):
            flash("수동 정렬 기준(ID 목록)이 비어 있어 현재 선택 순서를 유지합니다.", "warning")
        if missing_manual_ids:
            flash(f"수동 정렬 목록에서 제외된 ID: {', '.join(missing_manual_ids[:10])}", "warning")
    else:
        selected_problem_ids = _sort_selected_problem_ids(
            selected_problem_ids=selected_problem_ids,
            problem_meta=problem_meta,
            sort_fields=effective_sort_fields,
            sort_order=sort_order,
        )

    if question_count > 0:
        selected_problem_ids = selected_problem_ids[:question_count]

    if not selected_problem_ids:
        flash("선택 조건에 해당하는 문항이 없습니다.", "warning")
        next_defaults = {
            "school": _first_or(schools, defaults["school"]),
            "year": _first_or(years, defaults["year"]),
            "grade": _first_or(grades, defaults["grade"]),
            "semester": _first_or(semesters, defaults["semester"]),
            "exam": _first_or(exams, defaults["exam"]),
            "data_source": selected_data_source,
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field_1": sort_field_slots[0],
            "sort_field_2": sort_field_slots[1],
            "sort_field_3": sort_field_slots[2],
            "sort_order": sort_order,
            "paper": paper,
            "problems_per_page": str(problems_per_page),
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "show_outer_border": "1" if show_outer_border else "0",
            "show_inner_dividers": "1" if show_inner_dividers else "0",
            "teacher_view": "1" if teacher_view else "0",
            "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
            "answer_sheet": "1" if append_answer_sheet else "0",
            "solution_sheet": "1" if append_solution_sheet else "0",
        }
        return redirect(url_for("index", **next_defaults))

    selected_problem_dirs: List[str] = []
    seen_problem_dirs = set()
    missing_problem_dirs: List[str] = []
    for problem_id in selected_problem_ids:
        row = meta_by_id.get(problem_id)
        folder_path = str(row.get("folder_path", "")).strip() if row else ""
        if not folder_path:
            missing_problem_dirs.append(problem_id)
            continue
        normalized_folder_path = str(Path(folder_path))
        if normalized_folder_path in seen_problem_dirs:
            continue
        seen_problem_dirs.add(normalized_folder_path)
        selected_problem_dirs.append(normalized_folder_path)

    if missing_problem_dirs:
        flash(f"문항 폴더를 찾을 수 없는 ID 제외: {', '.join(missing_problem_dirs[:10])}", "warning")

    if not selected_problem_dirs:
        flash("선택된 문항 폴더를 찾을 수 없습니다.", "warning")
        next_defaults = {
            "school": _first_or(schools, defaults["school"]),
            "year": _first_or(years, defaults["year"]),
            "grade": _first_or(grades, defaults["grade"]),
            "semester": _first_or(semesters, defaults["semester"]),
            "exam": _first_or(exams, defaults["exam"]),
            "data_source": selected_data_source,
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field_1": sort_field_slots[0],
            "sort_field_2": sort_field_slots[1],
            "sort_field_3": sort_field_slots[2],
            "sort_order": sort_order,
            "paper": paper,
            "problems_per_page": str(problems_per_page),
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "show_outer_border": "1" if show_outer_border else "0",
            "show_inner_dividers": "1" if show_inner_dividers else "0",
            "teacher_view": "1" if teacher_view else "0",
            "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
            "answer_sheet": "1" if append_answer_sheet else "0",
            "solution_sheet": "1" if append_solution_sheet else "0",
            "selector_ids": " ".join(selector_ids),
        }
        return redirect(url_for("index", **next_defaults))

    if not include_exam_sheet and not append_answer_sheet and not append_solution_sheet:
        flash("문제지/답안지/해설지 중 하나 이상 선택해 주세요.", "warning")
        next_defaults = {
            "school": _first_or(schools, defaults["school"]),
            "year": _first_or(years, defaults["year"]),
            "grade": _first_or(grades, defaults["grade"]),
            "semester": _first_or(semesters, defaults["semester"]),
            "exam": _first_or(exams, defaults["exam"]),
            "data_source": selected_data_source,
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field_1": sort_field_slots[0],
            "sort_field_2": sort_field_slots[1],
            "sort_field_3": sort_field_slots[2],
            "sort_order": sort_order,
            "paper": paper,
            "problems_per_page": str(problems_per_page),
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "show_outer_border": "1" if show_outer_border else "0",
            "show_inner_dividers": "1" if show_inner_dividers else "0",
            "teacher_view": "1" if teacher_view else "0",
            "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
            "answer_sheet": "1" if append_answer_sheet else "0",
            "solution_sheet": "1" if append_solution_sheet else "0",
            "selector_ids": " ".join(selector_ids),
            "title": title,
        }
        return redirect(url_for("index", **next_defaults))

    out_name = Path(request.form.get("out_name", "").strip() or "exam_from_web.pdf").name
    if not out_name.lower().endswith(".pdf"):
        out_name = f"{out_name}.pdf"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _resolve_unique_pdf_path(OUTPUT_DIR / out_name)

    dirs_manifest = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        prefix="build_exam_dirs_",
        dir=str(OUTPUT_DIR),
        delete=False,
        encoding="utf-8",
        newline="\n",
    )
    dirs_manifest_path = Path(dirs_manifest.name)
    try:
        for problem_dir in selected_problem_dirs:
            dirs_manifest.write(f"{problem_dir}\n")
    finally:
        dirs_manifest.close()

    cmd = [
        sys.executable,
        "build_exam.py",
        "--out",
        str(out_path),
        "--paper",
        paper,
        "--problems-per-page",
        str(problems_per_page),
        "--title",
        title,
        "--dirs-file",
        str(dirs_manifest_path),
    ]

    if show_source_info:
        cmd.append("--show-source-info")
    if show_unit_info:
        cmd.append("--show-unit-info")
    if not show_outer_border:
        cmd.append("--outer-border-off")
    if not show_inner_dividers:
        cmd.append("--inner-dividers-off")
    if teacher_view:
        cmd.append("--teacher-view")
    if reset_question_number_by_school:
        cmd.append("--reset-question-number-by-school")
    if not include_exam_sheet:
        cmd.append("--skip-exam")

    if append_answer_sheet:
        answer_path = _resolve_unique_pdf_path(OUTPUT_DIR / "answer_sheet_web.pdf")
        cmd.extend(["--answer-sheet", str(answer_path)])

    if append_solution_sheet:
        solution_path = _resolve_unique_pdf_path(OUTPUT_DIR / "solution_sheet_web.pdf")
        cmd.extend(["--solution-sheet", str(solution_path)])

    if append_answer_sheet or append_solution_sheet:
        cmd.append("--append-sheets-to-out")

    try:
        completed = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    finally:
        dirs_manifest_path.unlink(missing_ok=True)

    if completed.returncode != 0:
        flash("PDF 생성 실패", "error")
        if completed.stderr.strip():
            for line in completed.stderr.strip().splitlines()[:20]:
                flash(line, "warning")
        if completed.stdout.strip():
            for line in completed.stdout.strip().splitlines()[:20]:
                flash(line, "info")
    else:
        flash(f"PDF 생성 완료: {out_path}", "success")
        flash(f"출제 문항 수: {len(selected_problem_ids)}", "info")
        if append_answer_sheet or append_solution_sheet:
            flash("체크한 답안지/해설지를 본문 PDF에 병합해 단일 파일로 생성했습니다.", "info")
        if completed.stdout.strip():
            for line in completed.stdout.strip().splitlines()[:20]:
                flash(line, "info")
        if completed.stderr.strip():
            for line in completed.stderr.strip().splitlines()[:20]:
                flash(line, "warning")

    next_defaults = {
        "school": _first_or(schools, defaults["school"]),
        "year": _first_or(years, defaults["year"]),
        "grade": _first_or(grades, defaults["grade"]),
        "semester": _first_or(semesters, defaults["semester"]),
        "exam": _first_or(exams, defaults["exam"]),
        "data_source": selected_data_source,
        "schools": schools,
        "years": years,
        "grades": grades,
        "semesters": semesters,
        "exams": exams,
        "unit_nodes": unit_nodes,
        "levels": levels,
        "source_numbers": source_numbers,
        "selector_pattern": pattern,
        "sort_field_1": sort_field_slots[0],
        "sort_field_2": sort_field_slots[1],
        "sort_field_3": sort_field_slots[2],
        "sort_order": sort_order,
        "paper": paper,
        "problems_per_page": str(problems_per_page),
        "manual_order_ids": " ".join(manual_order_ids),
        "manual_selected_ids": " ".join(manual_selected_ids),
        "question_count": str(question_count),
        "show_source_info": "1" if show_source_info else "0",
        "show_unit_info": "1" if show_unit_info else "0",
        "show_outer_border": "1" if show_outer_border else "0",
        "show_inner_dividers": "1" if show_inner_dividers else "0",
        "teacher_view": "1" if teacher_view else "0",
        "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
        "exam_sheet": "1" if include_exam_sheet else "0",
        "answer_sheet": "1" if append_answer_sheet else "0",
        "solution_sheet": "1" if append_solution_sheet else "0",
        "selector_ids": " ".join(selector_ids),
        "title": title,
    }
    return redirect(url_for("index", **next_defaults))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
