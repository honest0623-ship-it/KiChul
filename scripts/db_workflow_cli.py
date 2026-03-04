from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from math import ceil
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingest_pipeline import (  # pylint: disable=wrong-import-position
    IngestConfig,
    _build_problem_id,
    _extract_unit_hint_from_filename,
    _unit_triplet_from_filename_hint,
    detect_candidate,
    ingest_images,
    list_original_images,
    remove_top_right_footnote_numbers_in_dir,
)


STATE_PATH = ROOT / "scripts" / ".db_workflow_state.json"
PLAN_PATH = ROOT / "scripts" / "DB_WORKFLOW_PLAN.md"
PROFILES_PATH = ROOT / "scripts" / "db_workflow_profiles.json"

STATE_VERSION = 1
SCAN_SUFFIX_RE = re.compile(r"(?:[_\-\s]?scan)$", re.IGNORECASE)
DUPLICATE_OPTIONS = ("ask", "skip", "overwrite")

DEFAULT_PROFILE_NAME = "JE_2025_G2_S1_MID"
DEFAULT_PROFILE: Dict[str, Any] = {
    "school": "JE",
    "year": 2025,
    "grade": 2,
    "semester": 1,
    "exam": "MID",
    "source_label": "user_upload_2026-03-03",
    "subjective_offset": 100,
    "source_dir": "db/original",
    "problems_root": "db/problems",
    "use_ocr": True,
    "ocr_lang": "kor+eng",
    "use_ai_solver": True,
    "ai_provider": "gemini",
    "gemini_api_key": "",
    "gemini_model": "gemini-2.5-flash",
    "groq_api_key": "",
    "groq_model": "llama-3.2-90b-vision-preview",
    "openai_api_key": "",
    "openai_model": "gpt-4.1",
    "allow_ocr_fallback_if_ai_fails": False,
    "move_after_ingest": False,
}
DEFAULT_RUN: Dict[str, Any] = {
    "chunk_size": 2,
    "rpm": 4,
    "on_duplicate": "ask",
}
SOURCE_META_CANDIDATES = (
    "_meta.json",
    "meta.json",
    "ingest_meta.json",
    "db_meta.json",
)
META_KEYS = (
    "school",
    "year",
    "grade",
    "semester",
    "exam",
    "source_label",
    "source",
    "subjective_offset",
    "source_dir",
    "problems_root",
)


@dataclass(frozen=True)
class CandidatePlan:
    filename: str
    source_question_no: Optional[int]
    problem_no: int
    qtype: str
    problem_id: str
    duplicate: bool
    unit_hint: str
    unit_hint_matched: Optional[bool]
    has_scan_companion: bool
    scan_companion_filename: str


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _to_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _to_bool(value: Any, fallback: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        token = value.strip().lower()
        if token in {"1", "true", "yes", "y", "on"}:
            return True
        if token in {"0", "false", "no", "n", "off"}:
            return False
    return fallback


def _resolve_gemini_api_key(raw_value: Any) -> str:
    token = str(raw_value or "").strip()
    if token:
        return token
    return os.environ.get("GEMINI_API_KEY", "").strip()


def _resolve_groq_api_key(raw_value: Any) -> str:
    token = str(raw_value or "").strip()
    if token:
        return token
    return os.environ.get("GROQ_API_KEY", "").strip()


def _resolve_openai_api_key(raw_value: Any) -> str:
    token = str(raw_value or "").strip()
    if token:
        return token
    return os.environ.get("OPENAI_API_KEY", "").strip()


def _resolve_path(path_token: str) -> Path:
    path = Path(path_token)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def _default_source_label() -> str:
    return f"user_upload_{datetime.now().date().isoformat()}"


def _parse_compact_meta(token: str) -> Dict[str, Any]:
    parts = [item.strip() for item in (token or "").split(",")]
    if len(parts) != 5:
        raise ValueError(
            "Invalid --meta format. Expected: school,year,grade,semester,exam "
            "(example: JE,2025,2,1,MID)"
        )

    school, year_raw, grade_raw, semester_raw, exam = parts
    if not school:
        raise ValueError("Invalid --meta: school is empty.")
    if not exam:
        raise ValueError("Invalid --meta: exam is empty.")

    try:
        year = int(year_raw)
        grade = int(grade_raw)
        semester = int(semester_raw)
    except ValueError as exc:
        raise ValueError("Invalid --meta: year/grade/semester must be integers.") from exc

    if year < 1900 or year > 2100:
        raise ValueError("Invalid --meta: year must be between 1900 and 2100.")
    if grade < 1 or grade > 12:
        raise ValueError("Invalid --meta: grade must be between 1 and 12.")
    if semester < 1 or semester > 2:
        raise ValueError("Invalid --meta: semester must be 1 or 2.")

    return {
        "school": school.upper(),
        "year": year,
        "grade": grade,
        "semester": semester,
        "exam": exam.upper(),
    }


def _resolve_meta_path(source_dir: Path, meta_file: Optional[str]) -> Optional[Path]:
    if meta_file:
        token = Path(meta_file)
        if token.is_absolute():
            return token
        return (source_dir / token).resolve()

    for name in SOURCE_META_CANDIDATES:
        path = source_dir / name
        if path.exists() and path.is_file():
            return path.resolve()
    return None


def _load_source_meta(source_dir: Path, meta_file: Optional[str]) -> Tuple[Dict[str, Any], str]:
    path = _resolve_meta_path(source_dir, meta_file)
    if path is None:
        return {}, ""

    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Source meta JSON parse error at {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"Source meta at {path} must be a JSON object.")

    filtered: Dict[str, Any] = {}
    for key in META_KEYS:
        if key in raw:
            filtered[key] = raw[key]
    if "source" in filtered and "source_label" not in filtered:
        filtered["source_label"] = filtered["source"]
    filtered.pop("source", None)

    return filtered, str(path)


def _runtime_profile_with_overrides(profile: Dict[str, Any], args: argparse.Namespace) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    merged = dict(profile)
    explicit_source_label = str(getattr(args, "source_label", "") or "").strip()
    if getattr(args, "source_dir", None):
        merged["source_dir"] = args.source_dir

    compact_meta: Dict[str, Any] = {}
    compact_meta_token = getattr(args, "meta", None)
    if compact_meta_token:
        compact_meta = _parse_compact_meta(str(compact_meta_token))
        merged.update(compact_meta)
        if not explicit_source_label:
            merged["source_label"] = _default_source_label()

    source_dir = _resolve_path(str(merged.get("source_dir", "db/original")))
    source_meta, meta_path = _load_source_meta(source_dir, getattr(args, "meta_file", None))
    merged.update(source_meta)

    cli_overrides: Dict[str, Any] = {}
    for key in ("school", "year", "grade", "semester", "exam", "source_label", "subjective_offset", "source_dir", "problems_root"):
        value = getattr(args, key, None)
        if value is None:
            continue
        cli_overrides[key] = value
    merged.update(compact_meta)
    merged.update(cli_overrides)

    meta_info = {
        "source_meta_path": meta_path,
        "source_meta_overrides": source_meta,
        "compact_meta_overrides": compact_meta,
        "cli_overrides": cli_overrides,
    }
    return merged, meta_info


def _effective_meta(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "school": str(profile.get("school", "JE")),
        "year": _to_int(profile.get("year"), 2025),
        "grade": _to_int(profile.get("grade"), 2),
        "semester": _to_int(profile.get("semester"), 1),
        "exam": str(profile.get("exam", "MID")),
        "source_label": str(profile.get("source_label", "")),
        "subjective_offset": _to_int(profile.get("subjective_offset"), 100),
    }


def _chunked(items: Sequence[str], size: int) -> List[List[str]]:
    if size <= 0:
        size = 1
    return [list(items[idx : idx + size]) for idx in range(0, len(items), size)]


def _scan_key(stem: str) -> str:
    compact = SCAN_SUFFIX_RE.sub("", (stem or "").strip())
    compact = re.sub(r"\s+", "", compact)
    return compact.lower()


def _ensure_profiles_file() -> Dict[str, Any]:
    if PROFILES_PATH.exists():
        try:
            data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("profiles"), dict):
                return data
        except json.JSONDecodeError:
            pass

    bootstrap = {
        "active_profile": DEFAULT_PROFILE_NAME,
        "defaults": DEFAULT_RUN,
        "profiles": {
            DEFAULT_PROFILE_NAME: DEFAULT_PROFILE,
        },
    }
    PROFILES_PATH.write_text(
        json.dumps(bootstrap, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return bootstrap


def _load_profile(profile_name: Optional[str]) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    all_profiles = _ensure_profiles_file()
    profiles = all_profiles.get("profiles", {})
    defaults = all_profiles.get("defaults", {})
    active_name = str(all_profiles.get("active_profile") or DEFAULT_PROFILE_NAME).strip()
    chosen_name = (profile_name or active_name).strip()
    if chosen_name not in profiles:
        available = ", ".join(sorted(profiles.keys())) or "(none)"
        raise ValueError(f"Profile '{chosen_name}' not found. Available: {available}")
    chosen = profiles[chosen_name]
    if not isinstance(chosen, dict):
        raise ValueError(f"Profile '{chosen_name}' is invalid.")
    merged_defaults = dict(DEFAULT_RUN)
    if isinstance(defaults, dict):
        merged_defaults.update(defaults)
    return chosen_name, dict(chosen), merged_defaults


def _collect_candidate_plan(profile: Dict[str, Any]) -> Tuple[List[CandidatePlan], List[str], Path, Path]:
    source_dir = _resolve_path(str(profile.get("source_dir", "db/original")))
    problems_root = _resolve_path(str(profile.get("problems_root", "db/problems")))
    subjective_offset = _to_int(profile.get("subjective_offset"), 100)

    images = list_original_images(source_dir)
    scan_map: Dict[str, str] = {}
    for image in images:
        key = _scan_key(image.stem)
        if SCAN_SUFFIX_RE.search(image.stem):
            scan_map[key] = image.name

    invalid_rows: List[str] = []
    rows: List[CandidatePlan] = []
    for image in images:
        detected = detect_candidate(image, subjective_offset=subjective_offset)
        if not detected.qtype:
            continue
        if detected.detected_problem_no is None:
            invalid_rows.append(image.name)
            continue

        problem_no = int(detected.detected_problem_no)
        problem_id = _build_problem_id(
            school=str(profile.get("school", "JE")),
            year=_to_int(profile.get("year"), 2025),
            grade=_to_int(profile.get("grade"), 2),
            semester=_to_int(profile.get("semester"), 1),
            exam=str(profile.get("exam", "MID")),
            problem_no=problem_no,
        )
        folder = problems_root / problem_id
        unit_hint = _extract_unit_hint_from_filename(image.name)
        matched: Optional[bool] = None
        if unit_hint:
            matched = _unit_triplet_from_filename_hint(image.name) is not None

        rows.append(
            CandidatePlan(
                filename=image.name,
                source_question_no=detected.source_question_no,
                problem_no=problem_no,
                qtype=detected.qtype,
                problem_id=problem_id,
                duplicate=folder.exists(),
                unit_hint=unit_hint,
                unit_hint_matched=matched,
                has_scan_companion=_scan_key(image.stem) in scan_map,
                scan_companion_filename=scan_map.get(_scan_key(image.stem), ""),
            )
        )

    rows.sort(key=lambda item: item.filename)
    return rows, invalid_rows, source_dir, problems_root


def _state_from_preflight(
    profile_name: str,
    profile: Dict[str, Any],
    run_defaults: Dict[str, Any],
    chunk_size: int,
    rpm: int,
    on_duplicate: str,
    meta_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    rows, invalid_rows, source_dir, problems_root = _collect_candidate_plan(profile)
    on_duplicate = on_duplicate if on_duplicate in DUPLICATE_OPTIONS else "ask"
    duplicate_ids = sorted({row.problem_id for row in rows if row.duplicate})
    unmatched_unit = [row.filename for row in rows if row.unit_hint and row.unit_hint_matched is False]

    state: Dict[str, Any] = {
        "version": STATE_VERSION,
        "updated_at": _now_iso(),
        "phase": "planned",
        "profile_name": profile_name,
        "profile": profile,
        "effective_meta": _effective_meta(profile),
        "meta_info": meta_info or {},
        "defaults": run_defaults,
        "source_dir": str(source_dir),
        "problems_root": str(problems_root),
        "chunk_size": max(chunk_size, 1),
        "rpm": max(rpm, 1),
        "on_duplicate": on_duplicate,
        "duplicate_resolution": "",
        "overwrite_problem_md": False,
        "preflight": {
            "candidate_count": len(rows),
            "duplicate_count": len(duplicate_ids),
            "invalid_candidate_count": len(invalid_rows),
            "unit_hint_unmatched_count": len(unmatched_unit),
            "duplicates": duplicate_ids,
            "invalid_candidates": invalid_rows,
            "unit_hint_unmatched": unmatched_unit,
        },
        "candidates": [asdict(row) for row in rows],
        "run_filenames": [],
        "pending_filenames": [],
        "processed_filenames": [],
        "warnings": [],
        "results": [],
        "review_paths": [],
        "created_at": _now_iso(),
    }
    return state


def _write_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = _now_iso()
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        raise FileNotFoundError(f"State file not found: {STATE_PATH}")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _to_results_summary(results: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    summary = {"created": 0, "updated": 0, "skipped": 0}
    for row in results:
        status = str(row.get("status", "")).lower()
        if status in summary:
            summary[status] += 1
    return summary


def _write_plan_markdown(state: Dict[str, Any]) -> None:
    candidates = state.get("candidates", [])
    pending = state.get("pending_filenames", [])
    processed = state.get("processed_filenames", [])
    chunk_size = max(_to_int(state.get("chunk_size"), 2), 1)
    run_filenames = list(state.get("run_filenames", []))
    if not run_filenames and not str(state.get("duplicate_resolution", "")).strip():
        run_filenames = [row.get("filename", "") for row in candidates if row.get("filename")]
    chunks = _chunked(run_filenames, chunk_size)

    done_count = len(processed)
    done_chunks = ceil(done_count / chunk_size) if chunk_size else 0
    preflight = state.get("preflight", {})
    summary = _to_results_summary(state.get("results", []))

    lines: List[str] = []
    lines.append("# DB Workflow Plan")
    lines.append("")
    lines.append(f"- Updated: {state.get('updated_at', '')}")
    lines.append(f"- Phase: {state.get('phase', '')}")
    lines.append(f"- Profile: {state.get('profile_name', '')}")
    lines.append(f"- Source dir: `{state.get('source_dir', '')}`")
    lines.append(f"- Problems root: `{state.get('problems_root', '')}`")
    lines.append(f"- Chunk size: {chunk_size}")
    lines.append(f"- RPM: {state.get('rpm', '')}")
    lines.append(f"- Duplicate policy: {state.get('on_duplicate', '')}")
    lines.append(f"- Duplicate resolution: {state.get('duplicate_resolution', '(pending)')}")
    lines.append("")
    lines.append("## Effective Meta")
    effective_meta = state.get("effective_meta", {})
    lines.append(f"- school: {effective_meta.get('school', '')}")
    lines.append(f"- year: {effective_meta.get('year', '')}")
    lines.append(f"- grade: {effective_meta.get('grade', '')}")
    lines.append(f"- semester: {effective_meta.get('semester', '')}")
    lines.append(f"- exam: {effective_meta.get('exam', '')}")
    lines.append(f"- source: {effective_meta.get('source_label', '')}")
    lines.append(f"- subjective_offset: {effective_meta.get('subjective_offset', '')}")
    meta_info = state.get("meta_info", {})
    if meta_info and meta_info.get("source_meta_path"):
        lines.append(f"- source_meta_path: `{meta_info.get('source_meta_path', '')}`")
    lines.append("")
    lines.append("## Preflight")
    lines.append(f"- Candidates: {preflight.get('candidate_count', 0)}")
    lines.append(f"- Duplicates: {preflight.get('duplicate_count', 0)}")
    lines.append(f"- Invalid candidates: {preflight.get('invalid_candidate_count', 0)}")
    lines.append(f"- Unit hint unmatched: {preflight.get('unit_hint_unmatched_count', 0)}")
    lines.append("")

    duplicates: List[str] = list(preflight.get("duplicates", []))
    if duplicates:
        lines.append("### Duplicate IDs")
        for item in duplicates:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Execution Chunks")
    if not chunks:
        lines.append("- No runnable chunks.")
    else:
        for idx, chunk in enumerate(chunks, start=1):
            checked = "x" if idx <= done_chunks else " "
            files_repr = ", ".join(chunk)
            lines.append(f"- [{checked}] Chunk {idx}: {files_repr}")
    lines.append("")
    lines.append("## Progress")
    lines.append(f"- Processed files: {len(processed)}")
    lines.append(f"- Pending files: {len(pending)}")
    lines.append(f"- Created: {summary['created']}")
    lines.append(f"- Updated: {summary['updated']}")
    lines.append(f"- Skipped: {summary['skipped']}")
    lines.append(f"- Warnings: {len(state.get('warnings', []))}")
    lines.append("")
    lines.append("## Resume")
    lines.append("```powershell")
    lines.append("python scripts/db_workflow_cli.py resume")
    lines.append("```")
    lines.append("")

    review_paths: List[str] = list(state.get("review_paths", []))
    if review_paths:
        lines.append("## Review Paths")
        for path in review_paths:
            lines.append(f"- {path}")
        lines.append("")

    PLAN_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _print_preflight(state: Dict[str, Any]) -> None:
    preflight = state.get("preflight", {})
    meta = state.get("effective_meta", {})
    print(
        "Meta:"
        f" school={meta.get('school', '')},"
        f" year={meta.get('year', '')},"
        f" grade={meta.get('grade', '')},"
        f" semester={meta.get('semester', '')},"
        f" exam={meta.get('exam', '')},"
        f" source={meta.get('source_label', '')},"
        f" subjective_offset={meta.get('subjective_offset', '')}"
    )
    meta_info = state.get("meta_info", {})
    if meta_info and meta_info.get("source_meta_path"):
        print(f"Source meta file: {meta_info.get('source_meta_path')}")
    if meta_info and meta_info.get("compact_meta_overrides"):
        print(f"Compact meta input: {meta_info.get('compact_meta_overrides')}")
    print(
        "Preflight:"
        f" candidates={preflight.get('candidate_count', 0)},"
        f" duplicates={preflight.get('duplicate_count', 0)},"
        f" invalid={preflight.get('invalid_candidate_count', 0)},"
        f" unit_unmatched={preflight.get('unit_hint_unmatched_count', 0)}"
    )
    for row in state.get("candidates", []):
        marker = "DUP" if row.get("duplicate") else "NEW"
        hint = row.get("unit_hint", "")
        hint_info = f" | hint:{hint}" if hint else ""
        scan_info = f" | scan:{row.get('scan_companion_filename')}" if row.get("has_scan_companion") else ""
        print(f"- {row.get('filename')} -> {row.get('problem_id')} [{marker}]{hint_info}{scan_info}")


def _prepare_run_targets(state: Dict[str, Any], decision: Optional[str]) -> Tuple[bool, str]:
    if decision and decision not in {"skip", "overwrite"}:
        return False, "Invalid decision. Use skip or overwrite."

    duplicate_mode = str(state.get("on_duplicate", "ask")).strip().lower()
    if duplicate_mode not in DUPLICATE_OPTIONS:
        duplicate_mode = "ask"
        state["on_duplicate"] = "ask"

    preflight = state.get("preflight", {})
    has_duplicates = int(preflight.get("duplicate_count", 0)) > 0
    candidates = list(state.get("candidates", []))

    effective_mode = duplicate_mode
    if duplicate_mode == "ask":
        if has_duplicates and not decision:
            state["phase"] = "awaiting_duplicate_decision"
            state["run_filenames"] = []
            state["pending_filenames"] = []
            state["duplicate_resolution"] = ""
            return False, "Duplicate folders found. Decision is required."
        if has_duplicates:
            effective_mode = str(decision)
        else:
            effective_mode = "skip"

    run_filenames: List[str] = []
    for row in candidates:
        is_duplicate = bool(row.get("duplicate"))
        if effective_mode == "skip" and is_duplicate:
            continue
        run_filenames.append(str(row.get("filename")))

    state["duplicate_resolution"] = effective_mode
    state["overwrite_problem_md"] = effective_mode == "overwrite"
    state["run_filenames"] = run_filenames
    processed = list(state.get("processed_filenames", []))
    processed_set = set(processed)
    state["pending_filenames"] = [name for name in run_filenames if name not in processed_set]
    return True, ""


def _build_config(state: Dict[str, Any]) -> IngestConfig:
    profile = state.get("profile", {})
    return IngestConfig(
        school=str(profile.get("school", "JE")),
        year=_to_int(profile.get("year"), 2025),
        grade=_to_int(profile.get("grade"), 2),
        semester=_to_int(profile.get("semester"), 1),
        exam=str(profile.get("exam", "MID")),
        source_label=str(profile.get("source_label", "")),
        subjective_offset=_to_int(profile.get("subjective_offset"), 100),
        overwrite_problem_md=_to_bool(state.get("overwrite_problem_md"), False),
        include_original_preview_in_q=False,
        copy_to_scan_png=False,
        use_ocr=_to_bool(profile.get("use_ocr"), True),
        ocr_lang=str(profile.get("ocr_lang", "kor+eng")),
        use_ai_solver=_to_bool(profile.get("use_ai_solver"), False),
        ai_provider=str(profile.get("ai_provider", "gemini")),
        gemini_api_key=_resolve_gemini_api_key(profile.get("gemini_api_key", "")),
        gemini_model=str(profile.get("gemini_model", "gemini-2.5-flash")),
        groq_api_key=_resolve_groq_api_key(profile.get("groq_api_key", "")),
        groq_model=str(profile.get("groq_model", "llama-3.2-90b-vision-preview")),
        openai_api_key=_resolve_openai_api_key(profile.get("openai_api_key", "")),
        openai_model=str(profile.get("openai_model", "gpt-4.1")),
        allow_ocr_fallback_if_ai_fails=_to_bool(profile.get("allow_ocr_fallback_if_ai_fails"), False),
        move_after_ingest=_to_bool(profile.get("move_after_ingest"), False),
    )


def _run_pending(state: Dict[str, Any], review_only: bool = False) -> int:
    pending = list(state.get("pending_filenames", []))
    if not pending:
        state["phase"] = "completed"
        _write_state(state)
        _write_plan_markdown(state)
        _print_completion(state, review_only=review_only)
        return 0

    config = _build_config(state)
    source_dir = Path(state["source_dir"])
    problems_root = Path(state["problems_root"])
    chunk_size = max(_to_int(state.get("chunk_size"), 2), 1)
    rpm = max(_to_int(state.get("rpm"), 4), 1)
    delay_sec = 60.0 / float(rpm)

    state["phase"] = "running"
    _write_state(state)
    _write_plan_markdown(state)

    while pending:
        chunk = pending[:chunk_size]
        print(f"Running chunk: {', '.join(chunk)}")
        results, warnings = ingest_images(
            original_dir=source_dir,
            problems_root=problems_root,
            config=config,
            selected_filenames=chunk,
            overrides={},
        )

        stored_results = list(state.get("results", []))
        for item in results:
            record = {
                "filename": item.filename,
                "problem_id": item.problem_id,
                "status": item.status,
                "message": item.message,
                "problem_md": str(item.problem_md),
                "original_asset": str(item.original_asset),
            }
            stored_results.append(record)
            if item.status in {"created", "updated"}:
                review_paths = list(state.get("review_paths", []))
                if str(item.problem_md) not in review_paths:
                    review_paths.append(str(item.problem_md))
                state["review_paths"] = review_paths
        state["results"] = stored_results

        warn_list = list(state.get("warnings", []))
        warn_list.extend(warnings)
        state["warnings"] = warn_list

        processed = list(state.get("processed_filenames", []))
        processed.extend(chunk)
        state["processed_filenames"] = processed
        pending = pending[chunk_size:]
        state["pending_filenames"] = pending

        _write_state(state)
        _write_plan_markdown(state)

        if pending and delay_sec > 0:
            print(f"Sleeping {delay_sec:.1f}s for rate limit safety...")
            time.sleep(delay_sec)

    state["phase"] = "completed"
    _write_state(state)
    _write_plan_markdown(state)
    _print_completion(state, review_only=review_only)
    return 0


def _print_completion(state: Dict[str, Any], review_only: bool = False) -> None:
    summary = _to_results_summary(state.get("results", []))
    warnings = list(state.get("warnings", []))
    review_paths = list(state.get("review_paths", []))

    if not review_only:
        print(
            "Completed:"
            f" created={summary['created']},"
            f" updated={summary['updated']},"
            f" skipped={summary['skipped']},"
            f" warnings={len(warnings)}"
        )

        if warnings:
            print("[WARNINGS]")
            for item in warnings:
                print(f"- {item}")

    print("[REVIEW_PATHS]")
    if review_paths:
        for path in review_paths:
            print(path)
    else:
        print("(none)")


def _cmd_plan(args: argparse.Namespace) -> int:
    try:
        profile_name, profile, run_defaults = _load_profile(args.profile)
    except ValueError as exc:
        print(str(exc))
        return 1

    try:
        runtime_profile, meta_info = _runtime_profile_with_overrides(profile, args)
    except ValueError as exc:
        print(str(exc))
        return 1

    chunk_size = args.chunk_size if args.chunk_size is not None else _to_int(run_defaults.get("chunk_size"), 2)
    rpm = args.rpm if args.rpm is not None else _to_int(run_defaults.get("rpm"), 4)
    on_duplicate = args.on_duplicate or str(run_defaults.get("on_duplicate", "ask"))
    if on_duplicate not in DUPLICATE_OPTIONS:
        on_duplicate = "ask"

    state = _state_from_preflight(
        profile_name=profile_name,
        profile=runtime_profile,
        run_defaults=run_defaults,
        chunk_size=chunk_size,
        rpm=rpm,
        on_duplicate=on_duplicate,
        meta_info=meta_info,
    )
    _write_state(state)
    _write_plan_markdown(state)
    _print_preflight(state)
    print(f"State file: {STATE_PATH}")
    print(f"Plan file: {PLAN_PATH}")
    return 0


def _cmd_start(args: argparse.Namespace) -> int:
    try:
        _, profile, _ = _load_profile(args.profile)
        runtime_profile, _ = _runtime_profile_with_overrides(profile, args)
    except ValueError as exc:
        print(str(exc))
        return 1

    source_dir = _resolve_path(str(runtime_profile.get("source_dir", "db/original")))
    ocr_lang = str(runtime_profile.get("ocr_lang", "kor+eng")).strip() or "kor+eng"
    changed_files, cleanup_warnings = remove_top_right_footnote_numbers_in_dir(
        source_dir,
        lang=ocr_lang,
    )
    print(f"Pre-clean (footnote number removal): changed={len(changed_files)}")
    if changed_files:
        preview = ", ".join(changed_files[:10])
        print(f"[PRE-CLEAN CHANGED] {preview}")
        if len(changed_files) > 10:
            print(f"[PRE-CLEAN CHANGED] ... and {len(changed_files) - 10} more")
    if cleanup_warnings:
        for warning in cleanup_warnings[:10]:
            print(f"[PRE-CLEAN WARN] {warning}")
        if len(cleanup_warnings) > 10:
            print(f"[PRE-CLEAN WARN] ... and {len(cleanup_warnings) - 10} more")

    exit_code = _cmd_plan(args)
    if exit_code != 0:
        return exit_code
    state = _load_state()

    ok, reason = _prepare_run_targets(state, decision=args.decision)
    _write_state(state)
    _write_plan_markdown(state)

    if not ok:
        print(reason)
        duplicates: List[str] = list(state.get("preflight", {}).get("duplicates", []))
        if duplicates:
            print("[DUPLICATES]")
            for item in duplicates:
                print(item)
        print("Rerun with one of:")
        print("python scripts/db_workflow_cli.py resume --decision skip")
        print("python scripts/db_workflow_cli.py resume --decision overwrite")
        return 2

    return _run_pending(state, review_only=bool(args.review_only))


def _cmd_resume(args: argparse.Namespace) -> int:
    state = _load_state()
    if state.get("phase") == "completed":
        _print_completion(state, review_only=bool(args.review_only))
        return 0

    # Respect latest CLI overrides on resume.
    if args.chunk_size is not None:
        state["chunk_size"] = max(int(args.chunk_size), 1)
    if args.rpm is not None:
        state["rpm"] = max(int(args.rpm), 1)

    if state.get("phase") == "awaiting_duplicate_decision":
        ok, reason = _prepare_run_targets(state, decision=args.decision)
        _write_state(state)
        _write_plan_markdown(state)
        if not ok:
            print(reason)
            duplicates: List[str] = list(state.get("preflight", {}).get("duplicates", []))
            if duplicates:
                print("[DUPLICATES]")
                for item in duplicates:
                    print(item)
            return 2
    elif not state.get("run_filenames"):
        ok, reason = _prepare_run_targets(state, decision=args.decision)
        _write_state(state)
        _write_plan_markdown(state)
        if not ok:
            print(reason)
            return 2

    return _run_pending(state, review_only=bool(args.review_only))


def _cmd_report(args: argparse.Namespace) -> int:
    state = _load_state()
    _print_completion(state, review_only=bool(args.review_only))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "DB workflow helper for VSCode-Agent mode. "
            "Supports preflight, duplicate-aware chunk run, and resume."
        )
    )
    subparsers = parser.add_subparsers(dest="command")

    def add_common(sub: argparse.ArgumentParser) -> None:
        sub.add_argument("--profile", help="Profile name in scripts/db_workflow_profiles.json")
        sub.add_argument(
            "--meta",
            help="Compact meta: school,year,grade,semester,exam (example: JE,2025,2,1,MID)",
        )
        sub.add_argument("--source-dir", help="Override source directory (default from profile)")
        sub.add_argument("--meta-file", help="Meta JSON file name/path under source dir")
        sub.add_argument("--school", help="Override school code")
        sub.add_argument("--year", type=int, help="Override year")
        sub.add_argument("--grade", type=int, help="Override grade")
        sub.add_argument("--semester", type=int, help="Override semester")
        sub.add_argument("--exam", help="Override exam code")
        sub.add_argument("--source-label", help="Override source label")
        sub.add_argument("--subjective-offset", type=int, help="Override subjective offset")
        sub.add_argument("--problems-root", help="Override problems root directory")
        sub.add_argument("--chunk-size", type=int, help="Chunk size per ingest call")
        sub.add_argument("--rpm", type=int, help="Chunk runs per minute (safety throttle)")
        sub.add_argument(
            "--on-duplicate",
            choices=list(DUPLICATE_OPTIONS),
            help="Duplicate handling policy for start/plan",
        )

    plan = subparsers.add_parser("plan", help="Preflight only (no ingest)")
    add_common(plan)
    plan.set_defaults(func=_cmd_plan)

    start = subparsers.add_parser("start", help="Preflight + execute")
    add_common(start)
    start.add_argument(
        "--decision",
        choices=["skip", "overwrite"],
        help="Decision when duplicate mode is ask",
    )
    start.add_argument(
        "--review-only",
        action="store_true",
        help="Print review paths only in completion output",
    )
    start.set_defaults(func=_cmd_start)

    resume = subparsers.add_parser("resume", help="Resume from last state file")
    resume.add_argument("--chunk-size", type=int, help="Override chunk size for resume")
    resume.add_argument("--rpm", type=int, help="Override rpm for resume")
    resume.add_argument(
        "--decision",
        choices=["skip", "overwrite"],
        help="Decision if waiting for duplicate confirmation",
    )
    resume.add_argument(
        "--review-only",
        action="store_true",
        help="Print review paths only in completion output",
    )
    resume.set_defaults(func=_cmd_resume)

    report = subparsers.add_parser("report", help="Print summary from latest state")
    report.add_argument(
        "--review-only",
        action="store_true",
        help="Print review paths only",
    )
    report.set_defaults(func=_cmd_report)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        # Default shortcut: same as `start`.
        args.command = "start"
        args.profile = None
        args.meta = None
        args.source_dir = None
        args.meta_file = None
        args.school = None
        args.year = None
        args.grade = None
        args.semester = None
        args.exam = None
        args.source_label = None
        args.subjective_offset = None
        args.problems_root = None
        args.chunk_size = None
        args.rpm = None
        args.on_duplicate = None
        args.decision = None
        args.review_only = False
        args.func = _cmd_start
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
