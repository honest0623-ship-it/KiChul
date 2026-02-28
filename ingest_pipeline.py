from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Tuple
import re
import shutil
from gemini_solver import solve_problem_with_gemini
from groq_solver import DEFAULT_GROQ_MODEL, DEPRECATED_GROQ_MODELS, solve_problem_with_groq
from unit_level_classifier import classify_unit_and_level

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore[assignment]

try:
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore[assignment]

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:  # pragma: no cover - optional dependency
    RapidOCR = None  # type: ignore[assignment]


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}

SCORE_TOKEN_RE = re.compile(r"\(\s*\d+(?:\.\d+)?\s*점\s*\)")
MULTI_NEWLINE_RE = re.compile(r"\n{3,}")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
SUBJECTIVE_RE = re.compile(r"서답\s*([0-9]{1,3})\s*번?", re.IGNORECASE)
SIMPLE_NUMERIC_RE = re.compile(r"0*([0-9]{1,3})$")
ANY_NUMERIC_TOKEN_RE = re.compile(r"(?<!\d)([0-9]{1,3})(?!\d)")
ANSWER_HINT_RE = re.compile(r"(정답|answer|ans)", re.IGNORECASE)
SOLUTION_HINT_RE = re.compile(r"(해설|solution|sol|풀이)", re.IGNORECASE)
ANSWER_TEXT_RE = re.compile(r"(?:정답|answer|ans)?\s*[:：]?\s*([①②③④⑤1-5])", re.IGNORECASE)
RAPID_OCR_ENGINE: Any = None


def _compact_error(message: str, limit: int = 220) -> str:
    cleaned = re.sub(r"\s+", " ", (message or "")).strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}..."


def _is_auth_error(message: str) -> bool:
    token = (message or "").lower()
    return (
        "401" in token
        or "invalid api key" in token
        or "invalid_api_key" in token
        or "unauthorized" in token
        or "authentication" in token
    )


def _is_model_decommissioned_error(message: str) -> bool:
    token = (message or "").lower()
    return "decommissioned" in token or "no longer supported" in token


@dataclass(frozen=True)
class IngestConfig:
    school: str = "HN"
    year: int = 2025
    grade: int = 1
    semester: int = 1
    exam: str = "MID"
    source_label: str = ""
    subjective_offset: int = 100
    overwrite_problem_md: bool = False
    include_original_preview_in_q: bool = False
    copy_to_scan_png: bool = False
    use_ocr: bool = False
    ocr_lang: str = "kor+eng"
    use_ai_solver: bool = False
    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    groq_api_key: str = ""
    groq_model: str = DEFAULT_GROQ_MODEL
    allow_ocr_fallback_if_ai_fails: bool = False
    move_after_ingest: bool = False


@dataclass(frozen=True)
class ImageCandidate:
    filename: str
    path: Path
    source_question_no: Optional[int]
    detected_problem_no: Optional[int]
    qtype: str
    detection_note: str


@dataclass(frozen=True)
class IngestResult:
    filename: str
    problem_id: str
    status: str
    message: str
    problem_md: Path
    original_asset: Path


CompanionKind = Literal["answer", "solution"]


def _companion_kind(stem: str) -> Optional[CompanionKind]:
    compact = re.sub(r"\s+", "", stem).lower()
    if SOLUTION_HINT_RE.search(compact):
        return "solution"
    if ANSWER_HINT_RE.search(compact):
        return "answer"
    return None


def _extract_problem_no_from_name(stem: str, subjective_offset: int) -> Optional[int]:
    subjective_match = SUBJECTIVE_RE.search(stem)
    if subjective_match:
        return int(subjective_match.group(1)) + subjective_offset

    compact = re.sub(r"\s+", "", stem)
    numeric_match = SIMPLE_NUMERIC_RE.fullmatch(compact)
    if numeric_match:
        return int(numeric_match.group(1))

    token_match = ANY_NUMERIC_TOKEN_RE.search(stem)
    if token_match:
        return int(token_match.group(1))
    return None


def list_original_images(original_dir: Path) -> List[Path]:
    if not original_dir.exists():
        return []
    return sorted(
        [
            item
            for item in original_dir.iterdir()
            if item.is_file() and item.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ],
        key=lambda p: p.name.lower(),
    )


def detect_candidate(path: Path, subjective_offset: int = 100) -> ImageCandidate:
    stem = path.stem.strip()

    if _companion_kind(stem) is not None:
        return ImageCandidate(
            filename=path.name,
            path=path,
            source_question_no=None,
            detected_problem_no=None,
            qtype="",
            detection_note="companion file (answer/solution), not a question image",
        )

    source_no: Optional[int] = None
    problem_no: Optional[int] = None
    qtype = "객관식"
    note = "number not detected"

    subjective_match = SUBJECTIVE_RE.search(stem)
    if subjective_match:
        source_no = int(subjective_match.group(1))
        problem_no = source_no + subjective_offset
        qtype = "단답형" if source_no in {2, 3} else "서술형"
        note = "detected from subjective filename pattern"
    else:
        problem_no = _extract_problem_no_from_name(stem, subjective_offset=subjective_offset)
        if problem_no is not None:
            source_no = problem_no
            qtype = "객관식"
            note = "detected from numeric filename"

    return ImageCandidate(
        filename=path.name,
        path=path,
        source_question_no=source_no,
        detected_problem_no=problem_no,
        qtype=qtype,
        detection_note=note,
    )


def sanitize_question_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = SCORE_TOKEN_RE.sub("", cleaned)
    cleaned = MULTI_SPACE_RE.sub(" ", cleaned)
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = MULTI_NEWLINE_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def _rapidocr_engine() -> Any:
    global RAPID_OCR_ENGINE  # pylint: disable=global-statement
    if RapidOCR is None:
        return None
    if RAPID_OCR_ENGINE is None:
        RAPID_OCR_ENGINE = RapidOCR()
    return RAPID_OCR_ENGINE


def _rapidocr_to_text(raw_result: Any) -> str:
    if not raw_result:
        return ""
    lines: List[str] = []
    for row in raw_result:
        text: Optional[str] = None
        if isinstance(row, dict):
            if isinstance(row.get("text"), str):
                text = row["text"]
        elif isinstance(row, (list, tuple)):
            if len(row) >= 2:
                second = row[1]
                if isinstance(second, str):
                    text = second
                elif isinstance(second, (list, tuple)) and second and isinstance(second[0], str):
                    text = second[0]
            if text is None and row and isinstance(row[-1], str):
                text = row[-1]
        if text:
            stripped = text.strip()
            if stripped:
                lines.append(stripped)
    return "\n".join(lines).strip()


def detect_ocr_ready() -> Tuple[bool, str]:
    engine = _rapidocr_engine()
    if engine is not None:
        return True, "OCR ready (RapidOCR)"

    if pytesseract is None or Image is None:
        return False, "Install rapidocr-onnxruntime or Pillow+pytesseract to enable OCR."
    try:
        _ = pytesseract.get_tesseract_version()
    except Exception as exc:  # pylint: disable=broad-except
        return False, f"Tesseract binary unavailable ({exc})."
    return True, "OCR ready (Tesseract)"


def _run_ocr(image_path: Path, lang: str) -> Tuple[str, Optional[str]]:
    engine = _rapidocr_engine()
    if engine is not None:
        try:
            raw_result, _ = engine(str(image_path))
            return _rapidocr_to_text(raw_result), None
        except Exception as exc:  # pylint: disable=broad-except
            return "", f"RapidOCR failed: {exc}"

    if pytesseract is None or Image is None:
        return "", "OCR dependencies are not installed."
    try:
        with Image.open(image_path) as img:
            extracted = pytesseract.image_to_string(img, lang=lang)
    except Exception as exc:  # pylint: disable=broad-except
        return "", f"OCR failed: {exc}"
    return extracted, None


def _normalize_choice_token(token: str) -> str:
    mapper = {
        "1": "①",
        "2": "②",
        "3": "③",
        "4": "④",
        "5": "⑤",
    }
    return mapper.get(token, token)


def _extract_answer_text(raw: str) -> str:
    cleaned = sanitize_question_text(raw)
    if not cleaned:
        return ""

    match = ANSWER_TEXT_RE.search(cleaned)
    if match:
        return _normalize_choice_token(match.group(1))

    circled = re.search(r"[①②③④⑤]", cleaned)
    if circled:
        return circled.group(0)

    numeric = re.search(r"\b([1-5])\b", cleaned)
    if numeric:
        return _normalize_choice_token(numeric.group(1))
    return ""


def _extract_solution_text(raw: str) -> str:
    cleaned = sanitize_question_text(raw)
    if not cleaned:
        return ""
    return re.sub(r"^(해설|solution|sol)\s*[:：]?\s*", "", cleaned, flags=re.IGNORECASE).strip()


def _companion_indexes(
    original_dir: Path, subjective_offset: int
) -> Tuple[Dict[int, Path], Dict[int, Path]]:
    answer_index: Dict[int, Path] = {}
    solution_index: Dict[int, Path] = {}
    for item in list_original_images(original_dir):
        kind = _companion_kind(item.stem)
        if kind is None:
            continue
        problem_no = _extract_problem_no_from_name(item.stem, subjective_offset=subjective_offset)
        if problem_no is None:
            continue
        if kind == "answer":
            answer_index.setdefault(problem_no, item)
        else:
            solution_index.setdefault(problem_no, item)
    return answer_index, solution_index


def _resolve_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def _build_problem_id(
    school: str,
    year: int,
    grade: int,
    semester: int,
    exam: str,
    problem_no: int,
) -> str:
    return f"{school}-{year}-G{grade}-S{semester}-{exam}-{problem_no:03d}"


def _choices_template(qtype: str) -> str:
    if qtype == "객관식":
        return "\n".join(["①", "②", "③", "④", "⑤"])
    return ""


def _tags(source_no: Optional[int], qtype: str, used_ocr: bool, used_ai: bool) -> List[str]:
    tags = ["자동입력", qtype]
    if source_no is not None:
        tags.append(f"출제번호-{source_no}")
    if used_ocr:
        tags.append("OCR")
    if used_ai:
        tags.append("AI")
    return tags


def _yaml_tags_block(tags: Sequence[str]) -> str:
    if not tags:
        return "[]"
    return "\n".join([f"  - {tag}" for tag in tags])


def _build_problem_markdown(
    problem_id: str,
    config: IngestConfig,
    qtype: str,
    source_question_no: Optional[int],
    problem_no: Optional[int],
    original_asset_filename: str,
    extracted_text: str,
    ocr_warning: Optional[str],
    choices_markdown: str,
    answer_text: str,
    solution_text: str,
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    level: int,
    used_ai_generation: bool,
) -> str:
    source_kind = "objective"
    source_no_text = str(source_question_no) if source_question_no is not None else ""
    tail_text = problem_id.rsplit("-", 1)[-1]
    tail_number = int(tail_text) if tail_text.isdigit() else None
    if tail_number is not None and tail_number >= 100:
        source_kind = "subjective"
    elif qtype != "객관식":
        source_kind = "subjective"

    if not source_no_text and tail_number is not None:
        if source_kind == "subjective" and tail_number >= 100:
            source_no_text = str(tail_number - 100)
        else:
            source_no_text = str(tail_number)

    source_label = f"서답{source_no_text}" if source_no_text and source_kind == "subjective" else source_no_text
    source_record_label = config.source_label or f"web_upload_{datetime.now().strftime('%Y-%m-%d')}"
    source_record_label = source_record_label.replace('"', "'")
    used_ocr = bool(config.use_ocr and extracted_text.strip())
    q_lines: List[str] = []
    if used_ocr:
        q_lines.append(sanitize_question_text(extracted_text))
    else:
        q_lines.append("(OCR 결과가 없어서 문제 텍스트를 자동 입력하지 못했습니다.)")
        q_lines.append("(아래 원본 이미지를 참고해 문제 텍스트를 입력하세요.)")

    if ocr_warning:
        q_lines.append("")
        q_lines.append(f"(OCR 참고: {ocr_warning})")

    if config.include_original_preview_in_q:
        q_lines.append("")
        q_lines.append(f"![원본 이미지](assets/original/{original_asset_filename})")

    used_ai = used_ai_generation
    tags = _tags(source_no=source_question_no, qtype=qtype, used_ocr=used_ocr, used_ai=used_ai)
    tags_block = _yaml_tags_block(tags)
    choices_body = choices_markdown.strip() or _choices_template(qtype)

    return f"""---
id: {problem_id}
school: {config.school}
year: {config.year}
grade: {config.grade}
semester: {config.semester}
exam: {config.exam}
type: {qtype}
source_question_no: {source_no_text if source_no_text else "null"}
source_question_kind: {source_kind}
source_question_label: "{source_label if source_label else ""}"
difficulty: {level}
level: {level}
unit: "{' > '.join([item for item in [unit_l1.strip(), unit_l2.strip(), unit_l3.strip()] if item])}"
unit_l1: "{unit_l1}"
unit_l2: "{unit_l2}"
unit_l3: "{unit_l3}"
source: "{source_record_label}"
tags:
{tags_block}
assets:
  # Inline figure image path (use when Q/Choices references this file).
  - assets/scan.png
  # Raw source image archive.
  - assets/original/
  - assets/original/{original_asset_filename}
---

## Q
{chr(10).join(q_lines).strip()}

## Choices
{choices_body}

## Answer
{answer_text}

## Solution
{solution_text}
"""


def build_candidates(
    original_dir: Path, subjective_offset: int = 100
) -> List[ImageCandidate]:
    candidates = [detect_candidate(path=item, subjective_offset=subjective_offset) for item in list_original_images(original_dir)]
    return [item for item in candidates if item.qtype]


def ingest_images(
    original_dir: Path,
    problems_root: Path,
    config: IngestConfig,
    selected_filenames: Optional[Iterable[str]] = None,
    overrides: Optional[Dict[str, int]] = None,
) -> Tuple[List[IngestResult], List[str]]:
    overrides = overrides or {}
    warnings: List[str] = []
    results: List[IngestResult] = []

    all_candidates = build_candidates(original_dir=original_dir, subjective_offset=config.subjective_offset)
    if selected_filenames is None:
        candidates = all_candidates
    else:
        selected = set(selected_filenames)
        candidates = [item for item in all_candidates if item.filename in selected]

    answer_index, solution_index = _companion_indexes(
        original_dir=original_dir, subjective_offset=config.subjective_offset
    )

    ai_provider = (config.ai_provider or "gemini").strip().lower()
    if ai_provider not in {"gemini", "groq"}:
        ai_provider = "gemini"
    selected_groq_model = (
        DEFAULT_GROQ_MODEL if config.groq_model in DEPRECATED_GROQ_MODELS else config.groq_model
    )

    ocr_ready, ocr_message = detect_ocr_ready()
    if config.use_ai_solver:
        selected_key = (
            config.gemini_api_key if ai_provider == "gemini" else config.groq_api_key
        )
    else:
        selected_key = ""

    if config.use_ai_solver and not selected_key.strip():
        provider_name = "Gemini" if ai_provider == "gemini" else "Groq"
        warnings.append(
            f"AI 자동 풀이가 체크되었지만 {provider_name} API 키가 비어 있어 DB 생성을 중단했습니다."
        )
        for item in candidates:
            problem_no = overrides.get(item.filename, item.detected_problem_no)
            fallback_problem_id = (
                _build_problem_id(
                    school=config.school,
                    year=config.year,
                    grade=config.grade,
                    semester=config.semester,
                    exam=config.exam,
                    problem_no=problem_no,
                )
                if problem_no is not None
                else "(unknown)"
            )
            results.append(
                IngestResult(
                    filename=item.filename,
                    problem_id=fallback_problem_id,
                    status="skipped",
                    message="AI enabled but API key is empty.",
                    problem_md=(problems_root / fallback_problem_id / "problem.md"),
                    original_asset=item.path,
                )
            )
        return results, warnings

    if config.use_ocr and not ocr_ready and not config.use_ai_solver:
        warnings.append(
            "OCR을 실행할 수 없어 DB 생성을 중단했습니다. "
            f"OCR 상태: {ocr_message}"
        )
        for item in candidates:
            problem_no = overrides.get(item.filename, item.detected_problem_no)
            fallback_problem_id = (
                _build_problem_id(
                    school=config.school,
                    year=config.year,
                    grade=config.grade,
                    semester=config.semester,
                    exam=config.exam,
                    problem_no=problem_no,
                )
                if problem_no is not None
                else "(unknown)"
            )
            results.append(
                IngestResult(
                    filename=item.filename,
                    problem_id=fallback_problem_id,
                    status="skipped",
                    message=f"OCR unavailable: {ocr_message}",
                    problem_md=(problems_root / fallback_problem_id / "problem.md"),
                    original_asset=item.path,
                )
            )
        return results, warnings

    ai_auth_failed = False
    auth_failure_message = ""
    ai_model_unavailable = False
    model_unavailable_message = ""
    for item in candidates:
        override_problem_no = overrides.get(item.filename)
        problem_no = override_problem_no if override_problem_no is not None else item.detected_problem_no
        if problem_no is None:
            warnings.append(f"{item.filename}: problem number not detected. Skipped.")
            continue

        problem_id = _build_problem_id(
            school=config.school,
            year=config.year,
            grade=config.grade,
            semester=config.semester,
            exam=config.exam,
            problem_no=problem_no,
        )

        folder = problems_root / problem_id
        assets = folder / "assets"
        original_assets = assets / "original"
        original_assets.mkdir(parents=True, exist_ok=True)

        source_file = item.path
        dest_file = _resolve_unique_path(original_assets / source_file.name)
        shutil.copy2(source_file, dest_file)

        if config.copy_to_scan_png:
            shutil.copy2(dest_file, assets / "scan.png")

        extracted_text = ""
        ocr_warning: Optional[str] = None
        choices_markdown = ""
        answer_text = ""
        solution_text = ""
        effective_qtype = item.qtype
        ai_result: Optional[Any] = None
        ai_error: Optional[str] = None
        used_ocr_flow = False

        if config.use_ai_solver:
            if ai_auth_failed:
                ai_error = auth_failure_message or "AI authentication failed."
            elif ai_model_unavailable:
                ai_error = model_unavailable_message or "Selected AI model is unavailable."
            else:
                ocr_hint = ""
                if config.use_ocr and ocr_ready:
                    ocr_hint, hint_warning = _run_ocr(dest_file, lang=config.ocr_lang)
                    if hint_warning:
                        warnings.append(f"{problem_id}: OCR hint warning ({hint_warning})")

                try:
                    if ai_provider == "groq":
                        ai_result = solve_problem_with_groq(
                            api_key=config.groq_api_key,
                            model=selected_groq_model,
                            image_path=dest_file,
                            ocr_hint=ocr_hint,
                        )
                    else:
                        ai_result = solve_problem_with_gemini(
                            api_key=config.gemini_api_key,
                            model=config.gemini_model,
                            image_path=dest_file,
                            ocr_hint=ocr_hint,
                        )
                except Exception as exc:  # pylint: disable=broad-except
                    ai_error = str(exc)
                    provider_name = "Groq" if ai_provider == "groq" else "Gemini"
                    if _is_auth_error(ai_error):
                        ai_auth_failed = True
                        auth_failure_message = (
                            f"{provider_name} authentication failed (invalid API key)."
                        )
                        ai_error = auth_failure_message
                        warnings.append(
                            f"{problem_id}: {provider_name} auth failed. "
                            "Remaining items will skip AI in this run."
                        )
                    elif _is_model_decommissioned_error(ai_error):
                        ai_model_unavailable = True
                        model_unavailable_message = (
                            f"{provider_name} model unavailable (decommissioned). "
                            "Refresh model list and select another model."
                        )
                        ai_error = model_unavailable_message
                        warnings.append(
                            f"{problem_id}: {provider_name} model is unavailable. "
                            "Remaining items will skip AI in this run."
                        )
                    else:
                        warnings.append(
                            f"{problem_id}: {provider_name} solve failed ({_compact_error(ai_error)})"
                        )

            if ai_result is not None:
                if ai_result.qtype:
                    effective_qtype = ai_result.qtype
                extracted_text = ai_result.question_markdown
                choices_markdown = ai_result.choices_markdown
                answer_text = ai_result.answer_text or "(AI 정답 추출 실패)"
                solution_text = ai_result.solution_markdown or "(AI 해설 추출 실패)"

        # OCR fallback flow: used when AI is disabled or when AI failed.
        should_use_ocr_fallback = (
            config.use_ai_solver
            and ai_result is None
            and config.allow_ocr_fallback_if_ai_fails
        )

        if (not config.use_ai_solver or should_use_ocr_fallback) and config.use_ocr and ocr_ready:
            used_ocr_flow = True
            extracted_text, ocr_warning = _run_ocr(dest_file, lang=config.ocr_lang)
            if ocr_warning:
                warnings.append(f"{problem_id}: question OCR warning ({ocr_warning})")

            answer_source = answer_index.get(problem_no)
            if answer_source is not None:
                copied_answer = _resolve_unique_path(original_assets / answer_source.name)
                shutil.copy2(answer_source, copied_answer)
                answer_raw, answer_warn = _run_ocr(copied_answer, lang=config.ocr_lang)
                if answer_warn:
                    warnings.append(f"{problem_id}: answer OCR warning ({answer_warn})")
                answer_text = _extract_answer_text(answer_raw)
            elif ANSWER_HINT_RE.search(extracted_text):
                answer_text = _extract_answer_text(extracted_text)

            solution_source = solution_index.get(problem_no)
            if solution_source is not None:
                copied_solution = _resolve_unique_path(original_assets / solution_source.name)
                shutil.copy2(solution_source, copied_solution)
                solution_raw, solution_warn = _run_ocr(copied_solution, lang=config.ocr_lang)
                if solution_warn:
                    warnings.append(f"{problem_id}: solution OCR warning ({solution_warn})")
                solution_text = _extract_solution_text(solution_raw)
            elif SOLUTION_HINT_RE.search(extracted_text):
                solution_text = _extract_solution_text(extracted_text)

            if not answer_text:
                answer_text = "(정답 OCR 추출 실패)"
            if not solution_text:
                solution_text = "(해설 OCR 추출 실패)"

        if config.use_ai_solver and ai_result is None and not used_ocr_flow:
            compact_ai_error = _compact_error(ai_error or "unknown error")
            results.append(
                IngestResult(
                    filename=item.filename,
                    problem_id=problem_id,
                    status="skipped",
                    message=f"AI solve failed with no fallback ({compact_ai_error}).",
                    problem_md=(folder / "problem.md"),
                    original_asset=dest_file,
                )
            )
            if config.move_after_ingest:
                try:
                    source_file.unlink()
                except FileNotFoundError:
                    pass
                except OSError as exc:
                    warnings.append(f"{item.filename}: failed to delete source file ({exc}).")
            continue

        problem_md_path = folder / "problem.md"
        existed_before = problem_md_path.exists()
        if existed_before and not config.overwrite_problem_md:
            results.append(
                IngestResult(
                    filename=item.filename,
                    problem_id=problem_id,
                    status="skipped",
                    message="problem.md exists (overwrite disabled). Image archived only.",
                    problem_md=problem_md_path,
                    original_asset=dest_file,
                )
            )
        else:
            classification = classify_unit_and_level(
                question_text=extracted_text,
                choices_text=choices_markdown,
                answer_text=answer_text,
                solution_text=solution_text,
                qtype=effective_qtype,
                grade=config.grade,
                problem_no=problem_no,
            )
            content = _build_problem_markdown(
                problem_id=problem_id,
                config=config,
                qtype=effective_qtype,
                source_question_no=item.source_question_no,
                problem_no=problem_no,
                original_asset_filename=dest_file.name,
                extracted_text=extracted_text,
                ocr_warning=ocr_warning,
                choices_markdown=choices_markdown,
                answer_text=answer_text,
                solution_text=solution_text,
                unit_l1=classification.unit_l1,
                unit_l2=classification.unit_l2,
                unit_l3=classification.unit_l3,
                level=classification.level,
                used_ai_generation=(ai_result is not None),
            )
            problem_md_path.write_text(content, encoding="utf-8")
            status = "updated" if existed_before else "created"
            detail = "problem.md written."
            if ai_result is not None:
                detail = (
                    "problem.md written (AI: "
                    f"Q={'ok' if extracted_text.strip() else 'empty'}, "
                    f"A={'ok' if answer_text and '실패' not in answer_text else 'fail'}, "
                    f"S={'ok' if solution_text and '실패' not in solution_text else 'fail'})."
                )
            elif used_ocr_flow:
                detail = (
                    "problem.md written (OCR: "
                    f"Q={'ok' if extracted_text.strip() else 'empty'}, "
                    f"A={'ok' if answer_text and '실패' not in answer_text else 'fail'}, "
                    f"S={'ok' if solution_text and '실패' not in solution_text else 'fail'})."
                )
                if config.use_ai_solver and ai_result is None:
                    detail = f"{detail} (AI failed -> OCR fallback)"
            results.append(
                IngestResult(
                    filename=item.filename,
                    problem_id=problem_id,
                    status=status,
                    message=detail,
                    problem_md=problem_md_path,
                    original_asset=dest_file,
                )
            )

        if config.move_after_ingest:
            try:
                source_file.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                warnings.append(f"{item.filename}: failed to delete source file ({exc}).")

    return results, warnings
