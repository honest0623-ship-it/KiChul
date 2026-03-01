from __future__ import annotations

from dataclasses import asdict
import fnmatch
from hashlib import sha1
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Dict, List

from flask import Flask, flash, redirect, render_template, request, session, url_for

from ingest_pipeline import (
    IngestConfig,
    build_candidates,
    detect_ocr_ready,
    ingest_images,
)
from gemini_solver import list_gemini_models, ranked_gemini_models
from groq_solver import (
    DEFAULT_GROQ_MODEL,
    DEPRECATED_GROQ_MODELS,
    list_groq_models,
    ranked_groq_models,
)
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
DB_ORIGINAL_DIR = BASE_DIR / "db" / "original"
DB_PROBLEMS_DIR = BASE_DIR / "db" / "problems"
OUTPUT_DIR = BASE_DIR / "output"
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
PROBLEM_ID_RE = re.compile(
    r"^(?P<school>[^-]+)-(?P<year>\d{4})-G(?P<grade>\d+)-S(?P<semester>\d+)-(?P<exam>[^-]+)-(?P<number>\d{3})$"
)
SOURCE_NO_TAG_RE = re.compile(r"출제번호-(\d+)")
DEFAULT_OBJECTIVE_SOURCE_NUMBERS = [str(num) for num in range(1, 21)]
DEFAULT_SUBJECTIVE_SOURCE_NUMBERS = [f"서답{num}" for num in range(1, 7)]
DEFAULT_SOURCE_LABELS = [*DEFAULT_OBJECTIVE_SOURCE_NUMBERS, *DEFAULT_SUBJECTIVE_SOURCE_NUMBERS]

DEFAULTS = {
    "school": "HN",
    "year": "2025",
    "grade": "1",
    "semester": "1",
    "exam": "MID",
    "subjective_offset": "100",
    "ocr_lang": "kor+eng",
    "ai_provider": "gemini",
    "gemini_model": "gemini-2.5-flash",
    "groq_model": DEFAULT_GROQ_MODEL,
    "use_ai_solver": "1",
    "use_ocr": "1",
    "allow_ocr_fallback_if_ai_fails": "0",
    "overwrite_problem_md": "0",
    "include_original_preview_in_q": "0",
    "copy_to_scan_png": "0",
    "move_after_ingest": "1",
}

app = Flask(__name__)
app.secret_key = "math_kichul_local_admin"


def _file_key(filename: str) -> str:
    return sha1(filename.encode("utf-8")).hexdigest()[:12]


def _safe_uploaded_name(raw_name: str) -> str:
    name = Path(raw_name or "").name.strip()
    return name.replace("\\", "_").replace("/", "_")


def _resolve_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def _resolve_unique_pdf_path(path: Path) -> Path:
    if not path.exists():
        return path
    index = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{index:03d}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


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
    qtype = str(front_matter.get("type", "")).strip()

    # Legacy fallback for subjective numbering (e.g. 101 -> source no 1).
    if 100 <= number < 200 and "객관식" not in qtype:
        return str(number - 100)
    return str(number)


def _extract_source_kind(front_matter: Dict[str, Any], folder_number: str) -> str:
    raw_kind = str(front_matter.get("source_question_kind", "")).strip().lower()
    if raw_kind in {"objective", "객관식"}:
        return "objective"
    if raw_kind in {"subjective", "서답형", "단답형", "서술형"}:
        return "subjective"

    qtype = str(front_matter.get("type", "")).strip()
    if "객관" in qtype:
        return "objective"
    if any(token in qtype for token in ("서답", "단답", "서술")):
        return "subjective"

    if folder_number.isdigit() and int(folder_number) >= 100:
        return "subjective"
    return "objective"


def _build_source_label(source_no: str, source_kind: str) -> str:
    token = source_no.strip()
    if not token:
        return ""
    if source_kind == "subjective":
        return f"서답{token}"
    return token


def _sort_source_labels(values: List[str]) -> List[str]:
    def key(item: str) -> tuple[int, int, str]:
        label = item.strip()
        subjective = label.startswith("서답")
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
        level = _extract_level_from_front_matter(front_matter)

        rows.append(
            {
                "id": folder.name,
                "school": matched.group("school").upper(),
                "year": matched.group("year"),
                "grade": matched.group("grade"),
                "semester": matched.group("semester"),
                "exam": matched.group("exam").upper(),
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
    priority = {"MID": 0, "FINAL": 1}

    def key(item: str) -> tuple[int, str]:
        token = item.strip().upper()
        return (priority.get(token, 2), token)

    return sorted(values, key=key)


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
        "question_count": request.args.get("question_count", "0"),
        "show_source_info": request.args.get("show_source_info", "1") != "0",
        "teacher_view": request.args.get("teacher_view", "0") == "1",
        "title": request.args.get(
            "title",
            f"{defaults['school']} {defaults['year']} G{defaults['grade']} S{defaults['semester']} {defaults['exam']}",
        ),
    }


def _resolve_gemini_api_key(raw_value: str) -> str:
    typed = (raw_value or "").strip()
    if typed:
        return typed
    return os.environ.get("GEMINI_API_KEY", "").strip()


def _resolve_groq_api_key(raw_value: str) -> str:
    typed = (raw_value or "").strip()
    if typed:
        return typed
    return os.environ.get("GROQ_API_KEY", "").strip()


@app.get("/")
def index():
    defaults = _current_defaults()
    ai_provider = (defaults.get("ai_provider", "gemini").strip().lower() or "gemini")
    if ai_provider not in {"gemini", "groq"}:
        ai_provider = "gemini"

    gemini_models = session.get("gemini_models")
    if not isinstance(gemini_models, list) or not gemini_models:
        gemini_models = ranked_gemini_models()
    selected_gemini_model = (
        defaults.get("gemini_model", "gemini-2.5-flash").strip() or "gemini-2.5-flash"
    )
    if selected_gemini_model not in gemini_models:
        gemini_models = [selected_gemini_model, *[item for item in gemini_models if item != selected_gemini_model]]

    groq_models = session.get("groq_models")
    if not isinstance(groq_models, list) or not groq_models:
        groq_models = ranked_groq_models()
    selected_groq_model = (
        defaults.get("groq_model", DEFAULT_GROQ_MODEL).strip()
        or DEFAULT_GROQ_MODEL
    )
    if selected_groq_model in DEPRECATED_GROQ_MODELS:
        selected_groq_model = DEFAULT_GROQ_MODEL
    if selected_groq_model not in groq_models:
        groq_models = [selected_groq_model, *[item for item in groq_models if item != selected_groq_model]]

    subjective_offset = _parse_int(defaults.get("subjective_offset", "100"), 100)
    candidates = build_candidates(DB_ORIGINAL_DIR, subjective_offset=subjective_offset)
    candidate_rows = []
    for item in candidates:
        row = asdict(item)
        row["key"] = _file_key(item.filename)
        candidate_rows.append(row)

    problem_meta = _scan_problem_meta()
    pdf_options = _build_pdf_filter_options(problem_meta)
    pdf_selected = _read_pdf_selected(defaults, pdf_options)

    ocr_ready, ocr_message = detect_ocr_ready()
    return render_template(
        "admin.html",
        defaults=defaults,
        ai_provider=ai_provider,
        candidates=candidate_rows,
        gemini_models=gemini_models,
        groq_models=groq_models,
        pdf_options=pdf_options,
        pdf_selected=pdf_selected,
        original_dir=DB_ORIGINAL_DIR,
        problems_dir=DB_PROBLEMS_DIR,
        output_dir=OUTPUT_DIR,
        ocr_ready=ocr_ready,
        ocr_message=ocr_message,
    )


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


@app.post("/upload")
def upload_images():
    DB_ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    files = request.files.getlist("images")
    if not files:
        flash("업로드할 파일이 없습니다.", "error")
        return redirect(url_for("index", **_current_defaults()))

    saved = 0
    skipped = 0
    for item in files:
        filename = _safe_uploaded_name(item.filename)
        if not filename:
            skipped += 1
            continue
        extension = Path(filename).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            skipped += 1
            continue
        destination = _resolve_unique_path(DB_ORIGINAL_DIR / filename)
        item.save(destination)
        saved += 1

    flash(f"업로드 완료: 저장 {saved}개 / 제외 {skipped}개", "success")
    return redirect(url_for("index", **_current_defaults()))


@app.post("/ingest")
def ingest():
    defaults = _current_defaults()
    action = request.form.get("action", "ingest")
    school = request.form.get("school", defaults["school"]).strip().upper()
    year = _parse_int(request.form.get("year", defaults["year"]), 2025)
    grade = _parse_int(request.form.get("grade", defaults["grade"]), 1)
    semester = _parse_int(request.form.get("semester", defaults["semester"]), 1)
    exam = request.form.get("exam", defaults["exam"]).strip().upper() or "MID"
    use_ocr = bool(request.form.get("use_ocr"))
    use_ai_solver = bool(request.form.get("use_ai_solver"))
    allow_ocr_fallback_if_ai_fails = bool(request.form.get("allow_ocr_fallback_if_ai_fails"))
    ai_provider = (request.form.get("ai_provider", defaults.get("ai_provider", "gemini"))).strip().lower() or "gemini"
    if ai_provider not in {"gemini", "groq"}:
        ai_provider = "gemini"
    overwrite_problem_md = bool(request.form.get("overwrite_problem_md"))
    include_original_preview_in_q = bool(request.form.get("include_original_preview_in_q"))
    copy_to_scan_png = bool(request.form.get("copy_to_scan_png"))
    move_after_ingest = bool(request.form.get("move_after_ingest"))
    gemini_api_key = _resolve_gemini_api_key(request.form.get("gemini_api_key", ""))
    groq_api_key = _resolve_groq_api_key(request.form.get("groq_api_key", ""))
    gemini_model = (
        request.form.get("gemini_model", defaults.get("gemini_model", "gemini-2.5-flash")).strip()
        or "gemini-2.5-flash"
    )
    groq_model = (
        request.form.get("groq_model", defaults.get("groq_model", DEFAULT_GROQ_MODEL)).strip()
        or DEFAULT_GROQ_MODEL
    )
    if groq_model in DEPRECATED_GROQ_MODELS:
        groq_model = DEFAULT_GROQ_MODEL
        flash("선택한 Groq 모델은 지원 종료되어 기본 모델로 자동 전환했습니다.", "warning")
    subjective_offset = _parse_int(
        request.form.get("subjective_offset", defaults["subjective_offset"]), 100
    )
    ocr_lang = request.form.get("ocr_lang", defaults["ocr_lang"]).strip() or "kor+eng"

    next_defaults = {
        "school": school,
        "year": str(year),
        "grade": str(grade),
        "semester": str(semester),
        "exam": exam,
        "subjective_offset": str(subjective_offset),
        "ocr_lang": ocr_lang,
        "ai_provider": ai_provider,
        "gemini_model": gemini_model,
        "groq_model": groq_model,
        "use_ai_solver": "1" if use_ai_solver else "0",
        "use_ocr": "1" if use_ocr else "0",
        "allow_ocr_fallback_if_ai_fails": "1" if allow_ocr_fallback_if_ai_fails else "0",
        "overwrite_problem_md": "1" if overwrite_problem_md else "0",
        "include_original_preview_in_q": "1" if include_original_preview_in_q else "0",
        "copy_to_scan_png": "1" if copy_to_scan_png else "0",
        "move_after_ingest": "1" if move_after_ingest else "0",
    }

    if action == "refresh_models":
        if ai_provider == "groq":
            if not groq_api_key:
                flash("Groq API 키를 입력하거나 GROQ_API_KEY 환경변수를 설정한 뒤 다시 시도하세요.", "warning")
                return redirect(url_for("index", **next_defaults))
            models, error = list_groq_models(groq_api_key)
            session_key = "groq_models"
            selected_model = groq_model
            model_key = "groq_model"
            provider_label = "Groq"
        else:
            if not gemini_api_key:
                flash("Gemini API 키를 입력하거나 GEMINI_API_KEY 환경변수를 설정한 뒤 다시 시도하세요.", "warning")
                return redirect(url_for("index", **next_defaults))
            models, error = list_gemini_models(gemini_api_key)
            session_key = "gemini_models"
            selected_model = gemini_model
            model_key = "gemini_model"
            provider_label = "Gemini"

        if error:
            flash(f"모델 목록 갱신 실패: {error}", "warning")
            return redirect(url_for("index", **next_defaults))
        session[session_key] = models
        if selected_model not in models and models:
            next_defaults[model_key] = models[0]
        flash(f"{provider_label} 모델 {len(models)}개를 불러왔습니다.", "success")
        return redirect(url_for("index", **next_defaults))

    selected_filenames = request.form.getlist("selected")
    if action == "delete_selected":
        if not selected_filenames:
            flash("삭제할 항목이 선택되지 않았습니다.", "warning")
            return redirect(url_for("index", **next_defaults))

        deleted = 0
        missing = 0
        for filename in selected_filenames:
            target = DB_ORIGINAL_DIR / Path(filename).name
            if target.exists() and target.is_file():
                try:
                    target.unlink()
                    deleted += 1
                except OSError:
                    missing += 1
            else:
                missing += 1

        flash(f"선택 업로드 파일 삭제: 삭제 {deleted}개, 제외 {missing}개", "success")
        return redirect(url_for("index", **next_defaults))

    if not selected_filenames:
        flash("선택된 이미지가 없습니다. 표에서 최소 1개를 선택하세요.", "warning")
        return redirect(url_for("index", **next_defaults))

    overrides: Dict[str, int] = {}
    for key, value in request.form.items():
        if not key.startswith("num_for_"):
            continue
        digest = key.removeprefix("num_for_")
        filename = request.form.get(f"file_for_{digest}", "").strip()
        if not filename:
            continue
        raw = value.strip()
        if not raw:
            continue
        try:
            overrides[filename] = int(raw)
        except ValueError:
            continue

    config = IngestConfig(
        school=school,
        year=year,
        grade=grade,
        semester=semester,
        exam=exam,
        source_label=request.form.get("source_label", "").strip(),
        subjective_offset=subjective_offset,
        overwrite_problem_md=overwrite_problem_md,
        include_original_preview_in_q=include_original_preview_in_q,
        copy_to_scan_png=copy_to_scan_png,
        use_ocr=use_ocr,
        ocr_lang=ocr_lang,
        use_ai_solver=use_ai_solver,
        ai_provider=ai_provider,
        gemini_api_key=gemini_api_key,
        gemini_model=gemini_model,
        groq_api_key=groq_api_key,
        groq_model=groq_model,
        allow_ocr_fallback_if_ai_fails=allow_ocr_fallback_if_ai_fails,
        move_after_ingest=move_after_ingest,
    )

    results, warnings = ingest_images(
        original_dir=DB_ORIGINAL_DIR,
        problems_root=DB_PROBLEMS_DIR,
        config=config,
        selected_filenames=selected_filenames,
        overrides=overrides,
    )

    created = len([item for item in results if item.status == "created"])
    updated = len([item for item in results if item.status == "updated"])
    skipped = len([item for item in results if item.status == "skipped"])

    flash(
        f"DB 처리 완료: 생성 {created}, 갱신 {updated}, 스킵 {skipped}, 경고 {len(warnings)}",
        "success",
    )

    for warning in warnings[:15]:
        flash(warning, "warning")

    for item in results[:20]:
        flash(
            f"{item.filename} -> {item.problem_id} ({item.status}) | {item.message}",
            "info",
        )

    next_defaults["ocr_lang"] = config.ocr_lang
    next_defaults["ai_provider"] = config.ai_provider
    next_defaults["gemini_model"] = config.gemini_model
    next_defaults["groq_model"] = config.groq_model
    next_defaults["use_ai_solver"] = "1" if config.use_ai_solver else "0"
    next_defaults["use_ocr"] = "1" if config.use_ocr else "0"
    next_defaults["allow_ocr_fallback_if_ai_fails"] = (
        "1" if config.allow_ocr_fallback_if_ai_fails else "0"
    )
    next_defaults["overwrite_problem_md"] = "1" if config.overwrite_problem_md else "0"
    next_defaults["include_original_preview_in_q"] = (
        "1" if config.include_original_preview_in_q else "0"
    )
    next_defaults["copy_to_scan_png"] = "1" if config.copy_to_scan_png else "0"
    next_defaults["move_after_ingest"] = "1" if config.move_after_ingest else "0"
    return redirect(url_for("index", **next_defaults))


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
    pattern = request.form.get("selector_pattern", "").strip()
    question_count = max(_parse_int(request.form.get("question_count", "0"), 0), 0)
    show_source_info = bool(request.form.get("show_source_info"))
    teacher_view = bool(request.form.get("teacher_view"))
    append_answer_sheet = bool(request.form.get("answer_sheet"))
    append_solution_sheet = bool(request.form.get("solution_sheet"))

    problem_meta = _scan_problem_meta()
    available_ids = {item["id"] for item in problem_meta}
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
            "subjective_offset": defaults.get("subjective_offset", "100"),
            "ocr_lang": defaults.get("ocr_lang", "kor+eng"),
            "ai_provider": defaults.get("ai_provider", "gemini"),
            "gemini_model": defaults.get("gemini_model", "gemini-2.5-flash"),
            "groq_model": defaults.get("groq_model", DEFAULT_GROQ_MODEL),
            "use_ai_solver": defaults.get("use_ai_solver", "1"),
            "use_ocr": defaults.get("use_ocr", "1"),
            "allow_ocr_fallback_if_ai_fails": defaults.get("allow_ocr_fallback_if_ai_fails", "0"),
            "overwrite_problem_md": defaults.get("overwrite_problem_md", "0"),
            "include_original_preview_in_q": defaults.get("include_original_preview_in_q", "0"),
            "copy_to_scan_png": defaults.get("copy_to_scan_png", "0"),
            "move_after_ingest": defaults.get("move_after_ingest", "1"),
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "teacher_view": "1" if teacher_view else "0",
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
    if teacher_view:
        cmd.append("--teacher-view")

    if append_answer_sheet:
        answer_name = request.form.get("answer_name", "").strip() or "answer_sheet_web.pdf"
        answer_name = Path(answer_name).name
        if not answer_name.lower().endswith(".pdf"):
            answer_name = f"{answer_name}.pdf"
        answer_path = _resolve_unique_pdf_path(OUTPUT_DIR / answer_name)
        cmd.extend(["--answer-sheet", str(answer_path)])

    if append_solution_sheet:
        solution_name = request.form.get("solution_name", "").strip() or "solution_sheet_web.pdf"
        solution_name = Path(solution_name).name
        if not solution_name.lower().endswith(".pdf"):
            solution_name = f"{solution_name}.pdf"
        solution_path = _resolve_unique_pdf_path(OUTPUT_DIR / solution_name)
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
        flash(f"출제 문항수: {len(selected_problem_ids)}", "info")
        if append_answer_sheet or append_solution_sheet:
            flash("체크된 답안지/해설지가 시험지 뒤에 병합된 단일 PDF로 생성되었습니다.", "info")
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
        "subjective_offset": defaults.get("subjective_offset", "100"),
        "ocr_lang": defaults.get("ocr_lang", "kor+eng"),
        "ai_provider": defaults.get("ai_provider", "gemini"),
        "gemini_model": defaults.get("gemini_model", "gemini-2.5-flash"),
        "groq_model": defaults.get("groq_model", DEFAULT_GROQ_MODEL),
        "use_ai_solver": defaults.get("use_ai_solver", "1"),
        "use_ocr": defaults.get("use_ocr", "1"),
        "allow_ocr_fallback_if_ai_fails": defaults.get("allow_ocr_fallback_if_ai_fails", "0"),
        "overwrite_problem_md": defaults.get("overwrite_problem_md", "0"),
        "include_original_preview_in_q": defaults.get("include_original_preview_in_q", "0"),
        "copy_to_scan_png": defaults.get("copy_to_scan_png", "0"),
        "move_after_ingest": defaults.get("move_after_ingest", "1"),
        "schools": schools,
        "years": years,
        "grades": grades,
        "semesters": semesters,
        "exams": exams,
        "unit_nodes": unit_nodes,
        "levels": levels,
        "source_numbers": source_numbers,
        "selector_pattern": pattern,
        "question_count": str(question_count),
        "show_source_info": "1" if show_source_info else "0",
        "teacher_view": "1" if teacher_view else "0",
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
