from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tempfile
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Tuple
import re
import shutil
from gemini_solver import solve_problem_with_gemini
from groq_solver import DEFAULT_GROQ_MODEL, DEPRECATED_GROQ_MODELS, solve_problem_with_groq
from openai_solver import solve_problem_with_openai
from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

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

try:
    import cv2
except ImportError:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore[assignment]

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency
    np = None  # type: ignore[assignment]


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
FOOTNOTE_NUM_TOKEN_RE = re.compile(r"^[\(\[]?\d{1,3}[\)\]]?$")
ANSWER_HINT_RE = re.compile(r"(정답|answer|ans)", re.IGNORECASE)
SOLUTION_HINT_RE = re.compile(r"(해설|solution|sol|풀이)", re.IGNORECASE)
ANSWER_TEXT_RE = re.compile(r"(?:정답|answer|ans)?\s*[:：]?\s*([①②③④⑤1-5])", re.IGNORECASE)
SUBJECTIVE_LABEL_LINE_RE = re.compile(
    r"^\s*\[?\s*서답형(?:\s*\([^)]*\))?\s*\d+\s*번\s*\]?\s*$",
    re.IGNORECASE,
)
QUESTION_SECTION_SKIP_LINE_RE = re.compile(r"^\s*(?:정답|해설|풀이)\s*[:：]?", re.IGNORECASE)
CHOICE_TOKEN_RE = re.compile(r"(①|②|③|④|⑤|⑴|⑵|⑶|⑷|⑸|\([1-5]\)|（[1-5]）|[1-5][\.\)])")
CHOICE_MARKERS = ["①", "②", "③", "④", "⑤"]
SCAN_SUFFIX_RE = re.compile(r"(?:[_\-\s]?scan)$", re.IGNORECASE)
UNIT_HINT_INDEX_PREFIX_RE = re.compile(r"^\d+\s*-\s*\d+\s*\.\s*")
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
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1"
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


def _is_scan_companion(stem: str) -> bool:
    token = (stem or "").strip()
    return bool(token and SCAN_SUFFIX_RE.search(token))


def _strip_scan_suffix(stem: str) -> str:
    token = (stem or "").strip()
    stripped = SCAN_SUFFIX_RE.sub("", token)
    return stripped.strip("_- ").strip()


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


def _natural_sort_key(name: str) -> List[Any]:
    return [int(token) if token.isdigit() else token.lower() for token in re.split(r"(\d+)", name)]


def _normalize_unit_hint_token(text: str) -> str:
    token = (text or "").strip()
    token = UNIT_HINT_INDEX_PREFIX_RE.sub("", token)
    token = re.sub(r"\s+", "", token)
    return token


# File-name unit hint mapping.
# Expected names: "012_나머지정리.png", "서답3번_이차방정식과 이차함수.png", etc.
FILENAME_UNIT_HINT_MAP: Dict[str, Tuple[str, str, str]] = {
    "다항식의 연산": ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산"),
    "나머지정리": ("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리"),
    "인수분해": ("공통수학1(2022개정)", "1. 다항식", "1-3. 인수분해"),
    "복소수와 이차방정식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식"),
    "이차방정식과 이차함수": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수"),
    "여러 가지 방정식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식"),
    "여러 가지 부등식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식"),
    "합의 법칙과 곱의 법칙": ("공통수학1(2022개정)", "3. 경우의 수", "3-1. 합의 법칙과 곱의 법칙"),
    "순열과 조합": ("공통수학1(2022개정)", "3. 경우의 수", "3-2. 순열과 조합"),
    "행렬과 그 연산": ("공통수학1(2022개정)", "4. 행렬", "4-1. 행렬과 그 연산"),
    "지수와 로그": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "지수함수": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "로그함수": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수"),
    "삼각함수": ("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수"),
    "삼각함수의 그래프": ("대수(2022개정)", "2. 삼각함수", "2-2. 삼각함수의 그래프"),
    "삼각함수의 활용": ("대수(2022개정)", "2. 삼각함수", "2-3. 삼각함수의 활용"),
    "등차수열": ("대수(2022개정)", "3. 수열", "3-1. 등차수열"),
    "등비수열": ("대수(2022개정)", "3. 수열", "3-2. 등비수열"),
    "수열의 합": ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    "수학적귀납법": ("대수(2022개정)", "3. 수열", "3-4. 수학적귀납법"),
}


def _extract_unit_hint_from_filename(filename: str) -> str:
    stem = Path(filename).stem.strip()
    if _is_scan_companion(stem):
        stem = _strip_scan_suffix(stem)
    if "_" not in stem:
        return ""
    # Use first underscore as separator: "<번호>_<소단원>".
    _, hint = stem.split("_", 1)
    hint = re.sub(r"\s+", " ", hint).strip()
    return hint


def _unit_triplet_from_filename_hint(filename: str) -> Optional[Tuple[str, str, str]]:
    hint = _extract_unit_hint_from_filename(filename)
    if not hint:
        return None

    # Direct match first.
    matched = FILENAME_UNIT_HINT_MAP.get(hint)
    if matched:
        return matched

    # Compact fallback with index-prefix normalization.
    compact = _normalize_unit_hint_token(hint)
    for key, value in FILENAME_UNIT_HINT_MAP.items():
        if _normalize_unit_hint_token(key) == compact:
            return value
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
        key=lambda p: _natural_sort_key(p.name),
    )


def detect_candidate(path: Path, subjective_offset: int = 100) -> ImageCandidate:
    stem = path.stem.strip()

    if _is_scan_companion(stem):
        return ImageCandidate(
            filename=path.name,
            path=path,
            source_question_no=None,
            detected_problem_no=None,
            qtype="",
            detection_note="companion file (_scan), not a question image",
        )

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


def _clean_question_body(text: str) -> str:
    cleaned = sanitize_question_text(text)
    if not cleaned:
        return ""

    filtered_lines: List[str] = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if not stripped:
            filtered_lines.append("")
            continue
        if SUBJECTIVE_LABEL_LINE_RE.match(stripped):
            continue
        if QUESTION_SECTION_SKIP_LINE_RE.match(stripped):
            continue
        filtered_lines.append(line)

    normalized = "\n".join(filtered_lines)
    normalized = MULTI_NEWLINE_RE.sub("\n\n", normalized)
    return normalized.strip()


def _choice_index_from_token(token: str) -> Optional[int]:
    mapper = {
        "①": 1,
        "②": 2,
        "③": 3,
        "④": 4,
        "⑤": 5,
        "⑴": 1,
        "⑵": 2,
        "⑶": 3,
        "⑷": 4,
        "⑸": 5,
    }
    normalized = token.strip()
    if normalized in mapper:
        return mapper[normalized]
    digit_match = re.search(r"[1-5]", normalized)
    if digit_match:
        return int(digit_match.group(0))
    return None


def _extract_objective_question_and_choices(raw_text: str) -> Tuple[str, str]:
    cleaned = _clean_question_body(raw_text)
    if not cleaned:
        return "", ""

    matches = list(CHOICE_TOKEN_RE.finditer(cleaned))
    if len(matches) < 4:
        return cleaned, ""

    choices: Dict[int, str] = {}
    for idx, match in enumerate(matches):
        choice_idx = _choice_index_from_token(match.group(1))
        if choice_idx is None:
            continue
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        raw_piece = cleaned[start:end]
        normalized_piece = MULTI_SPACE_RE.sub(" ", re.sub(r"\s*\n\s*", " ", raw_piece)).strip(" \t:：-")
        if normalized_piece and choice_idx not in choices:
            choices[choice_idx] = normalized_piece

    if len(choices) < 4:
        return cleaned, ""

    question_body = cleaned[: matches[0].start()].strip()
    if not question_body:
        question_body = cleaned

    choice_lines = [f"{CHOICE_MARKERS[idx - 1]} {choices.get(idx, '')}".rstrip() for idx in range(1, 6)]
    return question_body, "\n".join(choice_lines)


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


def _read_image_cv2(image_path: Path) -> Tuple[Optional[Any], Optional[str]]:
    if cv2 is None:
        return None, "OpenCV is not installed."
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        return None, "Failed to read image."
    return image, None


def _write_image_cv2(image_path: Path, image: Any) -> Optional[str]:
    if cv2 is None:
        return "OpenCV is not installed."
    try:
        ok = cv2.imwrite(str(image_path), image)
    except Exception as exc:  # pylint: disable=broad-except
        return f"Failed to write image ({exc})."
    if not ok:
        return "Failed to write image."
    return None


def _bbox_from_quad(quad: Any) -> Optional[Tuple[int, int, int, int]]:
    if isinstance(quad, (list, tuple)) and len(quad) == 4 and all(
        isinstance(value, (int, float)) for value in quad
    ):
        x1, y1, x2, y2 = [int(round(float(value))) for value in quad]
        if x2 > x1 and y2 > y1:
            return x1, y1, x2, y2
        return None

    if not isinstance(quad, (list, tuple)):
        return None

    xs: List[int] = []
    ys: List[int] = []
    for point in quad:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            continue
        try:
            x_val = int(round(float(point[0])))
            y_val = int(round(float(point[1])))
        except (TypeError, ValueError):
            continue
        xs.append(x_val)
        ys.append(y_val)

    if not xs or not ys:
        return None

    x1 = min(xs)
    y1 = min(ys)
    x2 = max(xs)
    y2 = max(ys)
    if x2 <= x1 or y2 <= y1:
        return None
    return x1, y1, x2, y2


def _rapidocr_word_boxes(image_path: Path) -> Tuple[List[Tuple[str, Tuple[int, int, int, int]]], Optional[str]]:
    engine = _rapidocr_engine()
    if engine is None:
        return [], "RapidOCR unavailable."

    try:
        raw_result, _ = engine(str(image_path))
    except Exception as exc:  # pylint: disable=broad-except
        return [], f"RapidOCR failed: {exc}"

    rows = raw_result or []
    words: List[Tuple[str, Tuple[int, int, int, int]]] = []
    for row in rows:
        text: Optional[str] = None
        quad: Any = None
        if isinstance(row, dict):
            if isinstance(row.get("text"), str):
                text = row.get("text")
            quad = row.get("box") or row.get("points") or row.get("bbox")
        elif isinstance(row, (list, tuple)):
            if row:
                quad = row[0]
            if len(row) >= 2:
                second = row[1]
                if isinstance(second, str):
                    text = second
                elif isinstance(second, (list, tuple)) and second and isinstance(second[0], str):
                    text = second[0]
            if text is None and row and isinstance(row[-1], str):
                text = row[-1]

        if not text:
            continue
        stripped = text.strip()
        if not stripped:
            continue
        bbox = _bbox_from_quad(quad)
        if bbox is None:
            continue
        words.append((stripped, bbox))
    return words, None


def _tesseract_word_boxes(
    image_path: Path, lang: str
) -> Tuple[List[Tuple[str, Tuple[int, int, int, int]]], Optional[str]]:
    if pytesseract is None or Image is None:
        return [], "Tesseract dependencies are not installed."
    if not hasattr(pytesseract, "Output") or not hasattr(pytesseract.Output, "DICT"):
        return [], "Unsupported pytesseract version (Output.DICT missing)."

    try:
        with Image.open(image_path) as img:
            data = pytesseract.image_to_data(
                img,
                lang=lang,
                output_type=pytesseract.Output.DICT,
            )
    except Exception as exc:  # pylint: disable=broad-except
        return [], f"Tesseract failed: {exc}"

    texts = list(data.get("text") or [])
    lefts = list(data.get("left") or [])
    tops = list(data.get("top") or [])
    widths = list(data.get("width") or [])
    heights = list(data.get("height") or [])
    confs = list(data.get("conf") or [])
    if not texts:
        return [], None

    words: List[Tuple[str, Tuple[int, int, int, int]]] = []
    max_len = min(len(texts), len(lefts), len(tops), len(widths), len(heights))
    for idx in range(max_len):
        text = str(texts[idx] or "").strip()
        if not text:
            continue

        conf_raw = str(confs[idx] if idx < len(confs) else "")
        try:
            conf_val = float(conf_raw)
        except ValueError:
            conf_val = 0.0
        if conf_val < 20:
            continue

        try:
            x1 = int(lefts[idx])
            y1 = int(tops[idx])
            width = int(widths[idx])
            height = int(heights[idx])
        except (TypeError, ValueError):
            continue

        if width <= 1 or height <= 1:
            continue
        x2 = x1 + width
        y2 = y1 + height
        words.append((text, (x1, y1, x2, y2)))

    return words, None


def _vertical_overlap_ratio(
    box_a: Tuple[int, int, int, int], box_b: Tuple[int, int, int, int]
) -> float:
    a_h = max(1, box_a[3] - box_a[1])
    b_h = max(1, box_b[3] - box_b[1])
    overlap = max(0, min(box_a[3], box_b[3]) - max(box_a[1], box_b[1]))
    return overlap / float(min(a_h, b_h))


def _remove_top_right_footnote_number(image_path: Path, lang: str) -> Tuple[bool, Optional[str]]:
    if cv2 is None or np is None:
        return False, "Pre-clean skipped (OpenCV/numpy not available)."

    image, read_warning = _read_image_cv2(image_path)
    if image is None:
        return False, read_warning or "Pre-clean skipped (failed to read image)."

    image_height, image_width = image.shape[:2]

    boxes, _ = _rapidocr_word_boxes(image_path)
    warning: Optional[str] = None
    if not boxes:
        tess_boxes, tess_warning = _tesseract_word_boxes(image_path, lang=lang)
        boxes = tess_boxes
        if not boxes:
            warning = _merge_warning("No OCR boxes found.", tess_warning)

    if not boxes:
        return False, warning

    score_token_re = re.compile(r"[\[\(]?\s*\d+(?:\.\d+)?\s*점\s*[\]\)]?")
    score_boxes: List[Tuple[int, int, int, int]] = []
    for text, box in boxes:
        compact = re.sub(r"\s+", "", text)
        if "점" in compact and score_token_re.search(compact):
            score_boxes.append(box)

    top_limit = int(image_height * 0.52)
    right_limit = int(image_width * 0.55)
    candidates: List[Tuple[int, int, int, int]] = []

    for raw_text, box in boxes:
        token = re.sub(r"\s+", "", raw_text or "")
        token = token.replace("（", "(").replace("）", ")").replace("【", "[").replace("】", "]")
        if not FOOTNOTE_NUM_TOKEN_RE.fullmatch(token):
            continue

        x1, y1, x2, y2 = box
        if y2 > top_limit or x1 < right_limit:
            continue

        width = x2 - x1
        height = y2 - y1
        if width <= 0 or height <= 0:
            continue
        if width > int(image_width * 0.2) or height > int(image_height * 0.12):
            continue

        if score_boxes:
            anchored = False
            for score_box in score_boxes:
                if _vertical_overlap_ratio(box, score_box) >= 0.35 and x1 >= score_box[0] - int(image_width * 0.03):
                    anchored = True
                    break
            if not anchored and x2 < int(image_width * 0.92):
                continue

        candidates.append(box)

    if not candidates:
        return False, None

    def _candidate_key(candidate_box: Tuple[int, int, int, int]) -> Tuple[float, int, int]:
        x1, y1, x2, y2 = candidate_box
        overlap_score = 0.0
        if score_boxes:
            overlap_score = max(_vertical_overlap_ratio(candidate_box, score_box) for score_box in score_boxes)
        area = (x2 - x1) * (y2 - y1)
        return overlap_score, x2, -area

    target_box = max(candidates, key=_candidate_key)
    x1, y1, x2, y2 = target_box
    pad_x = max(2, int((x2 - x1) * 0.22))
    pad_y = max(2, int((y2 - y1) * 0.28))
    rx1 = max(0, x1 - pad_x)
    ry1 = max(0, y1 - pad_y)
    rx2 = min(image_width - 1, x2 + pad_x)
    ry2 = min(image_height - 1, y2 + pad_y)
    cv2.rectangle(image, (rx1, ry1), (rx2, ry2), (255, 255, 255), thickness=-1)

    write_warning = _write_image_cv2(image_path, image)
    if write_warning:
        return False, write_warning
    return True, None


def remove_top_right_footnote_numbers_in_dir(
    original_dir: Path, lang: str = "kor+eng"
) -> Tuple[List[str], List[str]]:
    if not original_dir.exists():
        return [], [f"{original_dir} does not exist."]

    if cv2 is None or np is None:
        return [], ["Pre-clean skipped: OpenCV/numpy is not installed."]

    rapid_available = _rapidocr_engine() is not None
    tess_available = pytesseract is not None and Image is not None
    if not rapid_available and not tess_available:
        return [], [
            "Pre-clean skipped: OCR engine unavailable (install rapidocr-onnxruntime or Pillow+pytesseract)."
        ]

    changed_files: List[str] = []
    warnings: List[str] = []
    for path in list_original_images(original_dir):
        candidate = detect_candidate(path)
        if candidate.detected_problem_no is None:
            continue
        changed, warning = _remove_top_right_footnote_number(path, lang=lang)
        if changed:
            changed_files.append(path.name)
        elif warning:
            warnings.append(f"{path.name}: {warning}")

    return changed_files, warnings


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


def _merge_warning(first: Optional[str], second: Optional[str]) -> Optional[str]:
    items = [item.strip() for item in [first, second] if item and item.strip()]
    if not items:
        return None
    if len(items) == 1:
        return items[0]
    return " | ".join(items)


def _prepare_ocr_image(image_path: Path) -> Tuple[Path, bool, Optional[str]]:
    if cv2 is None or np is None:
        return image_path, False, None

    temp_path: Optional[Path] = None
    try:
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            return image_path, False, "OCR pre-processing skipped (failed to read image)."

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        red_mask_1 = cv2.inRange(hsv, np.array([0, 45, 25]), np.array([15, 255, 255]))
        red_mask_2 = cv2.inRange(hsv, np.array([160, 45, 25]), np.array([179, 255, 255]))
        marker_mask = cv2.bitwise_or(red_mask_1, red_mask_2)
        vivid_color_mask = cv2.inRange(hsv, np.array([70, 70, 20]), np.array([179, 255, 255]))
        marker_mask = cv2.bitwise_or(marker_mask, vivid_color_mask)

        kernel = np.ones((3, 3), np.uint8)
        marker_mask = cv2.morphologyEx(marker_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        marker_mask = cv2.dilate(marker_mask, kernel, iterations=1)

        if cv2.countNonZero(marker_mask) > 0:
            image = cv2.inpaint(image, marker_mask, 3, cv2.INPAINT_TELEA)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11,
        )
        binary = cv2.medianBlur(binary, 3)

        temp_file = tempfile.NamedTemporaryFile(prefix="ocr_clean_", suffix=".png", delete=False)
        temp_file.close()
        temp_path = Path(temp_file.name)
        if not cv2.imwrite(str(temp_path), binary):
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)
            return image_path, False, "OCR pre-processing skipped (failed to write temp image)."
        return temp_path, True, None
    except Exception as exc:  # pylint: disable=broad-except
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        return image_path, False, f"OCR pre-processing failed ({exc})."


def _run_ocr(image_path: Path, lang: str) -> Tuple[str, Optional[str]]:
    prepared_path, using_temp, prep_warning = _prepare_ocr_image(image_path)
    cleanup_targets: List[Path] = []
    if using_temp:
        cleanup_targets.append(prepared_path)

    def _cleanup() -> None:
        for temp in cleanup_targets:
            temp.unlink(missing_ok=True)

    def _select_better_text(primary: str, fallback: str) -> str:
        if len(primary.strip()) >= len(fallback.strip()):
            return primary
        return fallback

    engine = _rapidocr_engine()
    if engine is not None:
        try:
            raw_result, _ = engine(str(prepared_path))
            extracted = _rapidocr_to_text(raw_result)

            if using_temp and len(extracted.strip()) < 16:
                fallback_raw, _ = engine(str(image_path))
                fallback_text = _rapidocr_to_text(fallback_raw)
                extracted = _select_better_text(extracted, fallback_text)

            _cleanup()
            return extracted, prep_warning
        except Exception as exc:  # pylint: disable=broad-except
            _cleanup()
            return "", _merge_warning(prep_warning, f"RapidOCR failed: {exc}")

    if pytesseract is None or Image is None:
        _cleanup()
        return "", _merge_warning(prep_warning, "OCR dependencies are not installed.")
    try:
        with Image.open(prepared_path) as img:
            extracted = pytesseract.image_to_string(img, lang=lang)
        if using_temp and len(extracted.strip()) < 16:
            with Image.open(image_path) as img:
                fallback_text = pytesseract.image_to_string(img, lang=lang)
            extracted = _select_better_text(extracted, fallback_text)
    except Exception as exc:  # pylint: disable=broad-except
        _cleanup()
        return "", _merge_warning(prep_warning, f"OCR failed: {exc}")

    _cleanup()
    return extracted, prep_warning


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
    images: Sequence[Path], subjective_offset: int
) -> Tuple[Dict[int, Path], Dict[int, Path], Dict[int, Path]]:
    answer_index: Dict[int, Path] = {}
    solution_index: Dict[int, Path] = {}
    scan_index: Dict[int, Path] = {}
    for item in images:
        if _is_scan_companion(item.stem):
            base_stem = _strip_scan_suffix(item.stem)
            problem_no = _extract_problem_no_from_name(base_stem, subjective_offset=subjective_offset)
            if problem_no is not None:
                scan_index.setdefault(problem_no, item)
            continue

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
    return answer_index, solution_index, scan_index


def _write_scan_png(scan_source: Path, scan_target: Path) -> Optional[str]:
    if scan_source.suffix.lower() == ".png":
        shutil.copy2(scan_source, scan_target)
        return None

    if Image is None:
        shutil.copy2(scan_source, scan_target)
        return (
            "Pillow가 없어 스캔 삽화를 PNG로 변환하지 못했습니다. "
            "원본 바이트를 scan.png로 복사했습니다."
        )

    try:
        with Image.open(scan_source) as raw_img:
            converted = raw_img.convert("RGBA")
            converted.save(scan_target, format="PNG")
        return None
    except Exception as exc:  # pylint: disable=broad-except
        shutil.copy2(scan_source, scan_target)
        return (
            "scan 이미지 PNG 변환에 실패했습니다 "
            f"({exc}). 원본 바이트를 scan.png로 복사했습니다."
        )


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
    has_scan_asset: bool,
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
    cleaned_question = _clean_question_body(extracted_text)
    q_lines: List[str] = []
    if used_ocr and cleaned_question:
        q_lines.append(cleaned_question)
    else:
        q_lines.append("(OCR 결과가 없어서 문제 텍스트를 자동 입력하지 못했습니다.)")
        q_lines.append("(아래 원본 이미지를 참고해 문제 텍스트를 입력하세요.)")

    if ocr_warning:
        q_lines.append("")
        q_lines.append(f"(OCR 참고: {ocr_warning})")

    if config.include_original_preview_in_q:
        q_lines.append("")
        q_lines.append(f"![원본 이미지](assets/original/{original_asset_filename})")

    if has_scan_asset:
        q_lines.append("")
        q_lines.append('<img src="assets/scan.png" style="width: 100%; max-width: 100%;">')

    used_ai = used_ai_generation
    tags = _tags(source_no=source_question_no, qtype=qtype, used_ocr=used_ocr, used_ai=used_ai)
    tags_block = _yaml_tags_block(tags)
    choices_body = choices_markdown.strip() or _choices_template(qtype)
    asset_lines: List[str] = []
    if has_scan_asset:
        asset_lines.append("  - assets/scan.png")
    asset_lines.append("  # Raw source image archive.")
    asset_lines.append("  - assets/original/")
    asset_lines.append(f"  - assets/original/{original_asset_filename}")
    assets_block = "\n".join(asset_lines)

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
unit: "{'>'.join([item for item in [unit_l1.strip(), unit_l2.strip(), unit_l3.strip()] if item])}"
unit_l1: "{unit_l1}"
unit_l2: "{unit_l2}"
unit_l3: "{unit_l3}"
source: "{source_record_label}"
tags:
{tags_block}
assets:
{assets_block}
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
    original_dir: Path,
    subjective_offset: int = 100,
    images: Optional[Sequence[Path]] = None,
) -> List[ImageCandidate]:
    source_images = list(images) if images is not None else list_original_images(original_dir)
    candidates = [detect_candidate(path=item, subjective_offset=subjective_offset) for item in source_images]
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

    original_images = list_original_images(original_dir)
    all_candidates = build_candidates(
        original_dir=original_dir,
        subjective_offset=config.subjective_offset,
        images=original_images,
    )
    if selected_filenames is None:
        candidates = all_candidates
    else:
        selected = set(selected_filenames)
        candidates = [item for item in all_candidates if item.filename in selected]

    answer_index, solution_index, scan_index = _companion_indexes(
        images=original_images, subjective_offset=config.subjective_offset
    )

    ai_provider = (config.ai_provider or "gemini").strip().lower()
    if ai_provider not in {"gemini", "groq", "openai"}:
        ai_provider = "gemini"
    selected_groq_model = (
        DEFAULT_GROQ_MODEL if config.groq_model in DEPRECATED_GROQ_MODELS else config.groq_model
    )

    ocr_ready, ocr_message = detect_ocr_ready()
    if config.use_ai_solver:
        if ai_provider == "groq":
            selected_key = config.groq_api_key
        elif ai_provider == "openai":
            selected_key = config.openai_api_key
        else:
            selected_key = config.gemini_api_key
    else:
        selected_key = ""

    if config.use_ai_solver and not selected_key.strip():
        if ai_provider == "groq":
            provider_name = "Groq"
        elif ai_provider == "openai":
            provider_name = "OpenAI"
        else:
            provider_name = "Gemini"
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
            warnings.append(
                f"{problem_id}: copy_to_scan_png 옵션은 비활성화되었습니다. "
                "원본 문제 이미지는 scan.png로 복사하지 않습니다. "
                "삽화는 *_scan 파일을 사용하세요."
            )

        extracted_text = ""
        ocr_warning: Optional[str] = None
        choices_markdown = ""
        answer_text = ""
        solution_text = ""
        has_scan_asset = False
        effective_qtype = item.qtype
        ai_result: Optional[Any] = None
        ai_error: Optional[str] = None
        used_ocr_flow = False

        scan_source = scan_index.get(problem_no)
        if scan_source is not None:
            copied_scan = _resolve_unique_path(original_assets / scan_source.name)
            shutil.copy2(scan_source, copied_scan)
            scan_warning = _write_scan_png(copied_scan, assets / "scan.png")
            has_scan_asset = (assets / "scan.png").exists()
            if scan_warning:
                warnings.append(f"{problem_id}: {scan_warning}")

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
                    elif ai_provider == "openai":
                        ai_result = solve_problem_with_openai(
                            api_key=config.openai_api_key,
                            model=config.openai_model,
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
                    if ai_provider == "groq":
                        provider_name = "Groq"
                    elif ai_provider == "openai":
                        provider_name = "OpenAI"
                    else:
                        provider_name = "Gemini"
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

            if effective_qtype == "객관식":
                question_body, parsed_choices = _extract_objective_question_and_choices(extracted_text)
                if parsed_choices:
                    extracted_text = question_body
                    choices_markdown = parsed_choices
                else:
                    warnings.append(
                        f"{problem_id}: 객관식 선택지 OCR 파싱 실패(수동 검수 필요)."
                    )

            if len(_clean_question_body(extracted_text)) < 18:
                warnings.append(
                    f"{problem_id}: 문제 본문 OCR 인식이 불충분합니다(수동 검수 필요)."
                )

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
            hinted_unit = _unit_triplet_from_filename_hint(item.filename)
            if hinted_unit is not None:
                unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
                    hinted_unit[0],
                    hinted_unit[1],
                    hinted_unit[2],
                    grade=config.grade,
                )
            else:
                unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
                    classification.unit_l1,
                    classification.unit_l2,
                    classification.unit_l3,
                    grade=config.grade,
                )
                if _extract_unit_hint_from_filename(item.filename):
                    warnings.append(
                        f"{problem_id}: filename unit hint not matched "
                        f"({item.filename}). classifier result used."
                    )
            content = _build_problem_markdown(
                problem_id=problem_id,
                config=config,
                qtype=effective_qtype,
                source_question_no=item.source_question_no,
                original_asset_filename=dest_file.name,
                extracted_text=extracted_text,
                ocr_warning=ocr_warning,
                choices_markdown=choices_markdown,
                answer_text=answer_text,
                solution_text=solution_text,
                unit_l1=unit_l1,
                unit_l2=unit_l2,
                unit_l3=unit_l3,
                level=classification.level,
                used_ai_generation=(ai_result is not None),
                has_scan_asset=has_scan_asset,
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
