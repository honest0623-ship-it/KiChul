from __future__ import annotations

import fnmatch
from html import escape
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
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


BASE_DIR = Path(__file__).resolve().parent
DB_PROBLEMS_DIR = BASE_DIR / "db" / "problems"
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

DEFAULTS = {
    "school": "HN",
    "year": "2025",
    "grade": "1",
    "semester": "1",
    "exam": "MID",
}
SORT_FIELDS = {"default", "unit", "school", "year", "manual"}
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
    problem_folder = _resolve_problem_folder(problem_id)
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


def _scan_problem_meta() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not DB_PROBLEMS_DIR.exists():
        return rows

    for folder in DB_PROBLEMS_DIR.iterdir():
        if not folder.is_dir():
            continue
        matched = PROBLEM_ID_RE.match(folder.name)
        if not matched:
            continue
        front_matter: Dict[str, Any] = {}
        problem_md = folder / "problem.md"
        if problem_md.exists():
            try:
                parsed = parse_problem_file(problem_md)
                if isinstance(parsed.front_matter, dict):
                    front_matter = parsed.front_matter
            except Exception:
                front_matter = {}

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
    return sorted(rows, key=lambda item: item["id"])


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


def _normalize_sort_field(raw: str) -> str:
    token = (raw or "").strip().lower()
    if token in SORT_FIELDS:
        return token
    return "default"


def _normalize_sort_order(raw: str) -> str:
    token = (raw or "").strip().lower()
    if token in SORT_ORDERS:
        return token
    return "asc"


def _sort_selected_problem_ids(
    selected_problem_ids: List[str],
    problem_meta: List[Dict[str, str]],
    sort_field: str,
    sort_order: str,
) -> List[str]:
    sort_field = _normalize_sort_field(sort_field)
    sort_order = _normalize_sort_order(sort_order)
    items = list(selected_problem_ids)

    if len(items) < 2:
        return items

    if sort_field in {"default", "manual"}:
        if sort_order == "desc":
            items.reverse()
        return items

    meta_by_id = {item["id"]: item for item in problem_meta}

    def _as_int(value: str, fallback: int) -> int:
        token = str(value or "").strip()
        return int(token) if token.isdigit() else fallback

    def _key(problem_id: str) -> tuple[Any, ...]:
        row = meta_by_id.get(problem_id, {})
        school = str(row.get("school", "")).strip()
        year = _as_int(str(row.get("year", "")), 9999)
        grade = _as_int(str(row.get("grade", "")), 99)
        semester = _as_int(str(row.get("semester", "")), 99)
        exam = str(row.get("exam", "")).strip()
        subject = str(row.get("subject", "")).strip()
        unit = str(row.get("unit", "")).strip()
        number = _as_int(str(row.get("number", "")), 999)

        if sort_field == "unit":
            return (unit, school, year, grade, semester, exam, subject, number, problem_id)
        if sort_field == "school":
            return (school, year, grade, semester, exam, subject, unit, number, problem_id)
        if sort_field == "year":
            return (year, school, grade, semester, exam, subject, unit, number, problem_id)
        return (problem_id,)

    return sorted(items, key=_key, reverse=(sort_order == "desc"))


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


def _build_pdf_filter_options(problem_meta: List[Dict[str, str]]) -> Dict[str, Any]:
    source_labels = set(_distinct_values(problem_meta, "source_label"))
    source_labels.update(DEFAULT_SOURCE_LABELS)
    return {
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
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{parsed.q.strip()}\n\n"
        f"## Choices\n{parsed.choices.strip()}\n\n"
        f"## Answer\n{parsed.answer.strip()}\n\n"
        f"## Solution\n{parsed.solution.strip()}\n"
    )
    path.write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def _serialize_problem_meta(problem_id: str, front: Dict[str, Any]) -> Dict[str, Any]:
    matched = PROBLEM_ID_RE.match(problem_id)
    from_id = matched.groupdict() if matched else {}
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


def _read_pdf_selected(defaults: Dict[str, str], pdf_options: Dict[str, Any]) -> Dict[str, Any]:
    def pick_all_when_empty(name: str) -> List[str]:
        selected = request.args.getlist(name)
        if selected:
            return selected
        return list(pdf_options.get(name, []))

    selected_unit_nodes = request.args.getlist("unit_nodes")
    if not selected_unit_nodes:
        selected_unit_nodes = default_selected_unit_nodes()

    return {
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
        "sort_field": _normalize_sort_field(request.args.get("sort_field", "default")),
        "sort_order": _normalize_sort_order(request.args.get("sort_order", "asc")),
        "question_count": request.args.get("question_count", "0"),
        "show_source_info": request.args.get("show_source_info", "1") != "0",
        "show_unit_info": request.args.get("show_unit_info", "1") != "0",
        "teacher_view": request.args.get("teacher_view", "0") == "1",
        "exam_sheet": request.args.get("exam_sheet", "1") != "0",
        "title": request.args.get(
            "title",
            f"{defaults['school']} {defaults['year']} G{defaults['grade']} S{defaults['semester']} {defaults['exam']}",
        ),
    }


@app.get("/")
def index():
    defaults = _current_defaults()
    problem_meta = _scan_problem_meta()
    pdf_options = _build_pdf_filter_options(problem_meta)
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
    folder = _resolve_problem_folder(problem_id)
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
    folder = _resolve_problem_folder(problem_id)
    if folder is None:
        return jsonify({"error": "problem-not-found"}), 404

    problem_md = folder / "problem.md"
    if not problem_md.is_file():
        return jsonify({"error": "problem-file-not-found"}), 404

    try:
        parsed = parse_problem_file(problem_md)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

    question_html = _rewrite_preview_img_sources(
        _markdown_to_html_preview(parsed.q),
        problem_id,
    )
    choices_html = _rewrite_preview_img_sources(
        _markdown_to_html_preview(parsed.choices),
        problem_id,
    )
    answer_html = _rewrite_preview_img_sources(
        _markdown_to_html_preview(parsed.answer),
        problem_id,
    )
    solution_html = _rewrite_preview_img_sources(
        _markdown_to_html_preview(parsed.solution),
        problem_id,
    )

    return jsonify(
        {
            "id": parsed.display_id,
            "question_html": question_html,
            "choices_html": choices_html,
            "answer_html": answer_html,
            "solution_html": solution_html,
            "warnings": parsed.warnings,
        }
    )


@app.get("/api/problem-meta")
def problem_meta():
    problem_id = request.args.get("id", "").strip()
    folder = _resolve_problem_folder(problem_id)
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
    folder = _resolve_problem_folder(problem_id)
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
    matched = PROBLEM_ID_RE.match(problem_id)
    from_id = matched.groupdict() if matched else {}

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

    front["id"] = problem_id
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
        shutil.rmtree(folder)
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "delete-failed", "detail": str(exc)}), 500

    return jsonify({"ok": True, "id": problem_id})


@app.get("/open-output")
def open_output_folder():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if hasattr(os, "startfile"):
            os.startfile(str(OUTPUT_DIR))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(OUTPUT_DIR)], cwd=str(BASE_DIR))
        else:
            subprocess.Popen(["xdg-open", str(OUTPUT_DIR)], cwd=str(BASE_DIR))
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

    selector_ids = _extract_ids(request.form.get("selector_ids", ""))
    manual_order_ids = _extract_ids(request.form.get("manual_order_ids", ""))
    manual_selected_supplied = "manual_selected_ids" in request.form
    manual_selected_ids = _extract_ids(request.form.get("manual_selected_ids", ""))
    pattern = request.form.get("selector_pattern", "").strip()
    sort_field = _normalize_sort_field(request.form.get("sort_field", "default"))
    sort_order = _normalize_sort_order(request.form.get("sort_order", "asc"))
    question_count = max(_parse_int(request.form.get("question_count", "0"), 0), 0)
    show_source_info = bool(request.form.get("show_source_info"))
    show_unit_info = bool(request.form.get("show_unit_info"))
    teacher_view = bool(request.form.get("teacher_view"))
    include_exam_sheet = bool(request.form.get("exam_sheet"))
    append_answer_sheet = bool(request.form.get("answer_sheet"))
    append_solution_sheet = bool(request.form.get("solution_sheet"))

    problem_meta = _scan_problem_meta()
    available_ids = {item["id"] for item in problem_meta}
    manual_selected_ids = [item for item in manual_selected_ids if item in available_ids]
    manual_selection_active = manual_selected_supplied and (sort_field == "manual" or bool(manual_order_ids))
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
        selected_problem_ids = [item for item in selected_problem_ids if fnmatch.fnmatch(item, pattern)]

    if manual_selection_active:
        selected_manual_set = set(manual_selected_ids)
        selected_problem_ids = [item for item in selected_problem_ids if item in selected_manual_set]

    if sort_field == "manual":
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
            sort_field=sort_field,
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
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field": sort_field,
            "sort_order": sort_order,
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "teacher_view": "1" if teacher_view else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
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
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field": sort_field,
            "sort_order": sort_order,
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "teacher_view": "1" if teacher_view else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
            "selector_ids": " ".join(selector_ids),
            "title": request.form.get(
                "title",
                f"{_first_or(schools, defaults['school'])} {_first_or(years, defaults['year'])} "
                f"G{_first_or(grades, defaults['grade'])} S{_first_or(semesters, defaults['semester'])} "
                f"{_first_or(exams, defaults['exam'])}",
            ),
        }
        return redirect(url_for("index", **next_defaults))

    out_name = Path(request.form.get("out_name", "").strip() or "exam_from_web.pdf").name
    if not out_name.lower().endswith(".pdf"):
        out_name = f"{out_name}.pdf"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _resolve_unique_pdf_path(OUTPUT_DIR / out_name)

    cmd = [
        sys.executable,
        "build_exam.py",
        "--root",
        "db/problems",
        "--out",
        str(out_path),
        "--paper",
        request.form.get("paper", "A4"),
        "--columns",
        request.form.get("columns", "2"),
        "--title",
        request.form.get(
            "title",
            f"{_first_or(schools, defaults['school'])} {_first_or(years, defaults['year'])} "
            f"G{_first_or(grades, defaults['grade'])} S{_first_or(semesters, defaults['semester'])} "
            f"{_first_or(exams, defaults['exam'])}",
        ),
        "--ids",
        ",".join(selected_problem_ids),
    ]

    if show_source_info:
        cmd.append("--show-source-info")
    if show_unit_info:
        cmd.append("--show-unit-info")
    if teacher_view:
        cmd.append("--teacher-view")
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

    completed = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

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
        "schools": schools,
        "years": years,
        "grades": grades,
        "semesters": semesters,
        "exams": exams,
        "unit_nodes": unit_nodes,
        "levels": levels,
        "source_numbers": source_numbers,
        "selector_pattern": pattern,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "manual_order_ids": " ".join(manual_order_ids),
        "manual_selected_ids": " ".join(manual_selected_ids),
        "question_count": str(question_count),
        "show_source_info": "1" if show_source_info else "0",
        "show_unit_info": "1" if show_unit_info else "0",
        "teacher_view": "1" if teacher_view else "0",
        "exam_sheet": "1" if include_exam_sheet else "0",
        "selector_ids": " ".join(selector_ids),
        "title": request.form.get(
            "title",
            f"{_first_or(schools, defaults['school'])} {_first_or(years, defaults['year'])} "
            f"G{_first_or(grades, defaults['grade'])} S{_first_or(semesters, defaults['semester'])} "
            f"{_first_or(exams, defaults['exam'])}",
        ),
    }
    return redirect(url_for("index", **next_defaults))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
