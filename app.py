from __future__ import annotations

import fnmatch
from dataclasses import dataclass
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
    render_template,
    request,
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
from routes.problem_routes import register_problem_routes
from routes.render_routes import register_render_routes
from routes.similar_routes import register_similar_routes
from services.problem_index import ProblemMetaIndex

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
PROBLEM_META_INDEX_LOCK = Lock()
PROBLEM_META_INDEX: ProblemMetaIndex | None = None

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
    return _problem_meta_index().list_generated_batch_ids()


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
    return _problem_meta_index().collect_batch_candidate_dirs(batch_id)


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


def _build_official_problem_meta_row(folder: Path) -> Dict[str, str] | None:
    matched = PROBLEM_ID_RE.match(folder.name)
    if not matched:
        return None

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

    return {
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


def _build_generated_problem_meta_row(batch_id: str, folder: Path) -> Dict[str, str] | None:
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

    return {
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


def _problem_meta_index() -> ProblemMetaIndex:
    global PROBLEM_META_INDEX
    if PROBLEM_META_INDEX is not None:
        return PROBLEM_META_INDEX

    with PROBLEM_META_INDEX_LOCK:
        if PROBLEM_META_INDEX is None:
            PROBLEM_META_INDEX = ProblemMetaIndex(
                official_root=DB_PROBLEMS_DIR,
                generated_root=DB_GENERATED_CANDIDATES_DIR,
                problem_id_re=PROBLEM_ID_RE,
                batch_id_re=SIMILAR_BATCH_ID_RE,
                extract_flat_batch_id=_extract_generation_batch_id,
                build_official_row=_build_official_problem_meta_row,
                build_generated_row=_build_generated_problem_meta_row,
            )
    return PROBLEM_META_INDEX


def _scan_problem_meta(
    *,
    data_sources: List[str] | None = None,
    generated_batches: List[str] | None = None,
) -> List[Dict[str, str]]:
    return _problem_meta_index().scan_problem_meta(
        data_sources=data_sources,
        generated_batches=generated_batches,
    )


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


def _problem_meta_for_bootstrap(problem_meta: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    keys = (
        "id",
        "problem_id",
        "display_id",
        "root_kind",
        "batch_id",
        "school",
        "year",
        "grade",
        "semester",
        "exam",
        "subject",
        "number",
        "source_no",
        "source_kind",
        "source_label",
        "unit",
        "level",
    )
    rows: List[Dict[str, str]] = []
    for row in problem_meta:
        rows.append({key: str(row.get(key, "") or "") for key in keys})
    return rows


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
        "solution_sheet": request.args.get("solution_sheet", "0") == "1",
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
    # Keep initial payload lean; row details are fetched on demand via /api/problem-meta-list.
    bootstrap_problem_meta: List[Dict[str, str]] = []
    pdf_options = _build_pdf_filter_options(problem_meta, generated_batches=available_generated_batches)
    pdf_selected = _read_pdf_selected(defaults, pdf_options)
    return render_template(
        "admin.html",
        pdf_options=pdf_options,
        pdf_selected=pdf_selected,
        problem_meta=bootstrap_problem_meta,
        output_dir=OUTPUT_DIR,
        mathjax_bundle_uri=_resolve_mathjax_bundle_uri(),
    )


@dataclass(frozen=True)
class AppRouteServices:
    problem: Dict[str, Any]
    similar: Dict[str, Any]
    render: Dict[str, Any]


def _build_route_services() -> AppRouteServices:
    problem_deps: Dict[str, Any] = {
        "VENDOR_DIR": VENDOR_DIR,
        "normalize_unit_triplet": normalize_unit_triplet,
        "parse_problem_file": parse_problem_file,
        "shutil": shutil,
        "_build_preview_payload": _build_preview_payload,
        "_extract_level_from_front_matter": _extract_level_from_front_matter,
        "_extract_source_kind": _extract_source_kind,
        "_extract_source_no_from_front_matter": _extract_source_no_from_front_matter,
        "_fallback_source_no": _fallback_source_no,
        "_id_groups_for_problem_meta": _id_groups_for_problem_meta,
        "_invalidate_front_matter_cache_for_folder": _invalidate_front_matter_cache_for_folder,
        "_normalize_subject_code": _normalize_subject_code,
        "_open_path_in_file_manager": _open_path_in_file_manager,
        "_parse_generated_problem_ui_id": _parse_generated_problem_ui_id,
        "_refresh_problem_meta_row": _refresh_problem_meta_row,
        "_resolve_problem_folder": _resolve_problem_folder,
        "_resolve_problem_folder_any": _resolve_problem_folder_any,
        "_resolve_similar_candidate_folder": _resolve_similar_candidate_folder,
        "_rewrite_problem_md": _rewrite_problem_md,
        "_rewrite_problem_md_sections": _rewrite_problem_md_sections,
        "_safe_int_token": _safe_int_token,
        "_scan_problem_meta": _scan_problem_meta,
        "_serialize_problem_meta": _serialize_problem_meta,
        "_serialize_problem_sections": _serialize_problem_sections,
    }

    similar_deps: Dict[str, Any] = {
        "AI_CONFIG_LOCK": AI_CONFIG_LOCK,
        "AI_RUNTIME_CONFIG": AI_RUNTIME_CONFIG,
        "AI_SUPPORTED_PROVIDERS": AI_SUPPORTED_PROVIDERS,
        "DB_GENERATED_CANDIDATES_DIR": DB_GENERATED_CANDIDATES_DIR,
        "DB_PROBLEMS_DIR": DB_PROBLEMS_DIR,
        "DRAFT_TOKEN": DRAFT_TOKEN,
        "PROBLEM_ID_RE": PROBLEM_ID_RE,
        "SIMILAR_GENERATION_MAX_ATTEMPTS": SIMILAR_GENERATION_MAX_ATTEMPTS,
        "SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST": SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST,
        "SIMILAR_PROMOTION_ENABLED": SIMILAR_PROMOTION_ENABLED,
        "SequenceMatcher": SequenceMatcher,
        "datetime": datetime,
        "json": json,
        "normalize_unit_triplet": normalize_unit_triplet,
        "parse_problem_file": parse_problem_file,
        "shutil": shutil,
        "_as_positive_int": _as_positive_int,
        "_batch_report_path": _batch_report_path,
        "_build_similar_candidate_id": _build_similar_candidate_id,
        "_build_similar_generation_prompt": _build_similar_generation_prompt,
        "_build_similar_preview_payload": _build_similar_preview_payload,
        "_call_ai_model_text": _call_ai_model_text,
        "_collect_batch_candidate_dirs": _collect_batch_candidate_dirs,
        "_count_choice_lines": _count_choice_lines,
        "_current_ai_runtime_secret": _current_ai_runtime_secret,
        "_default_ai_model": _default_ai_model,
        "_extract_ids": _extract_ids,
        "_invalidate_front_matter_cache_for_folder": _invalidate_front_matter_cache_for_folder,
        "_is_generation_retryable_error": _is_generation_retryable_error,
        "_is_timeout_generation_error": _is_timeout_generation_error,
        "_latex_balance_issues": _latex_balance_issues,
        "_list_generated_batch_ids": _list_generated_batch_ids,
        "_model_allowed_for_provider": _model_allowed_for_provider,
        "_next_problem_id_for_prefix": _next_problem_id_for_prefix,
        "_normalize_ai_provider": _normalize_ai_provider,
        "_normalize_for_similarity": _normalize_for_similarity,
        "_normalize_runtime_config_unlocked": _normalize_runtime_config_unlocked,
        "_now_iso": _now_iso,
        "_objective_like_candidate": _objective_like_candidate,
        "_parse_generated_sections": _parse_generated_sections,
        "_parse_int": _parse_int,
        "_provider_display_name": _provider_display_name,
        "_resolve_problem_folder": _resolve_problem_folder,
        "_resolve_similar_candidate_folder": _resolve_similar_candidate_folder,
        "_rewrite_problem_md_sections": _rewrite_problem_md_sections,
        "_save_source_snapshot": _save_source_snapshot,
        "_seed_ids_from_payload": _seed_ids_from_payload,
        "_serialize_ai_runtime_config": _serialize_ai_runtime_config,
        "_serialize_problem_sections": _serialize_problem_sections,
        "_unique_batch_id": _unique_batch_id,
    }

    render_deps: Dict[str, Any] = {
        "BASE_DIR": BASE_DIR,
        "DEFAULT_EXAM_TITLE": DEFAULT_EXAM_TITLE,
        "DEFAULT_SORT_FIELD_SLOTS": DEFAULT_SORT_FIELD_SLOTS,
        "OUTPUT_DIR": OUTPUT_DIR,
        "Path": Path,
        "default_selected_unit_nodes": default_selected_unit_nodes,
        "expand_unit_nodes_to_leaf_paths": expand_unit_nodes_to_leaf_paths,
        "subprocess": subprocess,
        "sys": sys,
        "tempfile": tempfile,
        "_apply_manual_order": _apply_manual_order,
        "_current_defaults": _current_defaults,
        "_effective_sort_fields": _effective_sort_fields,
        "_extract_ids": _extract_ids,
        "_matches_pattern_for_row": _matches_pattern_for_row,
        "_normalize_data_source": _normalize_data_source,
        "_normalize_paper": _normalize_paper,
        "_normalize_problems_per_page": _normalize_problems_per_page,
        "_normalize_sort_field_slots": _normalize_sort_field_slots,
        "_normalize_sort_order": _normalize_sort_order,
        "_normalize_title": _normalize_title,
        "_normalize_values": _normalize_values,
        "_open_path_in_file_manager": _open_path_in_file_manager,
        "_parse_int": _parse_int,
        "_resolve_unique_pdf_path": _resolve_unique_pdf_path,
        "_scan_problem_meta": _scan_problem_meta,
        "_sort_selected_problem_ids": _sort_selected_problem_ids,
    }

    return AppRouteServices(
        problem=problem_deps,
        similar=similar_deps,
        render=render_deps,
    )


ROUTE_SERVICES = _build_route_services()

register_problem_routes(app, ROUTE_SERVICES.problem)
register_similar_routes(app, ROUTE_SERVICES.similar)
register_render_routes(app, ROUTE_SERVICES.render)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
