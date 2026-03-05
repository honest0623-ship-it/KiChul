from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Dict, List, Tuple

import yaml
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
CROPS = ROOT / "_tmp_missing_crops"
REPORT_PATH = ROOT / "_tmp_hn_jj_2025_g1_mid_com1_missing_report.txt"
RAW_JSON_PATH = ROOT / "_tmp_hn_jj_2025_g1_mid_com1_missing_raw.json"

SOURCE_PDF_BY_SCHOOL = {
    "HN": "HN.2025.G1.S1.MID.COM1.PDF.pdf",
    "JJ": "JJ.2025.G1.S1.MID.COM1.PDF.pdf",
}

FIXED_META = {
    "year": 2025,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "subject": "COM1",
    "source": "user_upload_2026-03-05",
    "subjective_offset": 100,
}

GEMINI_MODEL = "gemini-2.5-flash"
API_SLEEP_SEC = 8.5

BINOM_RE = re.compile(r"\\binom\s*\{([^{}]+)\}\s*\{([^{}]+)\}")
SCORE_TOKEN_RE = re.compile(r"[\(\[]\s*\d+(?:\.\d+)?\s*점\s*[\)\]]")
LEADING_LABEL_RE = re.compile(
    r"^\s*(?:\[\s*)?(?:서답형(?:\([^)]+\))?|서술형|단답형)\s*\d+번(?:\s*\])?\s*",
    re.MULTILINE,
)
LEADING_QNO_RE = re.compile(r"^\s*\d+\.\s*")


@dataclass(frozen=True)
class Task:
    pid: str
    qtype_override: str = ""


TASKS: List[Task] = [
    Task("HN-2025-G1-S1-MID-001"),
    Task("HN-2025-G1-S1-MID-002"),
    Task("HN-2025-G1-S1-MID-003"),
    Task("HN-2025-G1-S1-MID-004"),
    Task("HN-2025-G1-S1-MID-005"),
    Task("HN-2025-G1-S1-MID-007"),
    Task("HN-2025-G1-S1-MID-009"),
    Task("HN-2025-G1-S1-MID-010"),
    Task("HN-2025-G1-S1-MID-011"),
    Task("HN-2025-G1-S1-MID-012"),
    Task("HN-2025-G1-S1-MID-015"),
    Task("HN-2025-G1-S1-MID-016"),
    Task("HN-2025-G1-S1-MID-101", qtype_override="단답형"),
    Task("JJ-2025-G1-S1-MID-001"),
    Task("JJ-2025-G1-S1-MID-002"),
    Task("JJ-2025-G1-S1-MID-003"),
    Task("JJ-2025-G1-S1-MID-004"),
    Task("JJ-2025-G1-S1-MID-005"),
    Task("JJ-2025-G1-S1-MID-006"),
    Task("JJ-2025-G1-S1-MID-007"),
    Task("JJ-2025-G1-S1-MID-011"),
    Task("JJ-2025-G1-S1-MID-012"),
    Task("JJ-2025-G1-S1-MID-105", qtype_override="서술형"),
]


def _load_pyc_module(name: str):
    path = ROOT / "__pycache__" / f"{name}.cpython-312.pyc"
    if not path.is_file():
        raise FileNotFoundError(f"Missing pyc module: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to create module spec for {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _math_normalize(text: str) -> str:
    out = text or ""
    out = out.replace("\\begin{bmatrix}", "\\begin{pmatrix}")
    out = out.replace("\\end{bmatrix}", "\\end{pmatrix}")
    while True:
        next_text = BINOM_RE.sub(
            lambda m: f"{{}}_{{{m.group(1).strip()}}}C_{{{m.group(2).strip()}}}",
            out,
        )
        if next_text == out:
            break
        out = next_text
    return out


def _strip_score_and_labels(text: str) -> str:
    out = text or ""
    out = SCORE_TOKEN_RE.sub("", out)
    out = LEADING_LABEL_RE.sub("", out)
    out = LEADING_QNO_RE.sub("", out, count=1)
    return out.strip()


def _normalize_question(text: str) -> str:
    out = _strip_score_and_labels(text)
    out = _math_normalize(out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def _normalize_solution(text: str) -> str:
    out = _strip_score_and_labels(text)
    out = _math_normalize(out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def _normalize_choices(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        return ""
    raw = _math_normalize(raw)
    raw = SCORE_TOKEN_RE.sub("", raw)
    raw = re.sub(r"\s*([①②③④⑤])\s*", r"\n\1 ", raw).strip()
    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    has_marker = any(re.match(r"^[①②③④⑤]\s*", line) for line in lines)
    if not has_marker and len(lines) >= 5:
        marks = ["①", "②", "③", "④", "⑤"]
        lines = [f"{marks[idx]} {line}" for idx, line in enumerate(lines[:5])]
    return "\n".join(lines).strip()


def _normalize_answer(text: str) -> str:
    out = (text or "").strip()
    out = _strip_score_and_labels(out)
    out = _math_normalize(out)
    return out.strip()


def _pid_meta(pid: str) -> Tuple[str, int, str, int]:
    school = pid.split("-", 1)[0]
    number = int(pid.rsplit("-", 1)[-1])
    if number >= FIXED_META["subjective_offset"]:
        source_no = number - FIXED_META["subjective_offset"]
        source_kind = "subjective"
    else:
        source_no = number
        source_kind = "objective"
    return school, number, source_kind, source_no


def _default_qtype(source_kind: str) -> str:
    return "객관식" if source_kind == "objective" else "서술형"


def _build_front(
    pid: str,
    qtype: str,
    source_kind: str,
    source_no: int,
    unit_triplet: Tuple[str, str, str],
    level: int,
    source_pdf_name: str,
) -> Dict[str, object]:
    school, *_ = _pid_meta(pid)
    source_label = str(source_no) if source_kind == "objective" else f"서답{source_no}번"
    l1, l2, l3 = unit_triplet
    return {
        "id": pid,
        "school": school,
        "year": FIXED_META["year"],
        "grade": FIXED_META["grade"],
        "semester": FIXED_META["semester"],
        "exam": FIXED_META["exam"],
        "subject": FIXED_META["subject"],
        "type": qtype,
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": source_label,
        "difficulty": int(level),
        "level": int(level),
        "unit": f"{l1}>{l2}>{l3}",
        "unit_l1": l1,
        "unit_l2": l2,
        "unit_l3": l3,
        "source": FIXED_META["source"],
        "tags": [
            "수동작성",
            "OCR",
            "AI",
            qtype,
            f"출제번호-{source_label}",
            f"과목-{FIXED_META['subject']}",
        ],
        "assets": [
            "assets/original/",
            f"assets/original/{source_pdf_name}",
        ],
    }


def _write_problem_md(
    folder: Path,
    front: Dict[str, object],
    question: str,
    choices: str,
    answer: str,
    solution: str,
) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{question.strip()}\n\n"
        f"## Choices\n{choices.strip()}\n\n"
        f"## Answer\n{answer.strip()}\n\n"
        f"## Solution\n{solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def main() -> int:
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    review_paths: List[str] = []
    raw_dump: Dict[str, Dict[str, str]] = {}

    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("[ERROR] GEMINI_API_KEY is not set.")
        return 1

    _load_pyc_module("ai_solver_utils")
    gemini_solver = _load_pyc_module("gemini_solver")
    solve_problem_with_gemini = gemini_solver.solve_problem_with_gemini

    ocr = RapidOCR()

    for index, task in enumerate(TASKS):
        pid = task.pid
        school, number, source_kind, source_no = _pid_meta(pid)
        target = PROBLEMS / pid
        crop_path = CROPS / f"{pid}.png"

        if target.exists():
            summary["skipped"] += 1
            results.append(f"{pid} | skipped | duplicate-folder-exists")
            continue

        if not crop_path.is_file():
            warnings.append(f"{pid}: crop image missing ({crop_path.name})")
            results.append(f"{pid} | warning | crop-missing")
            continue

        source_pdf_name = SOURCE_PDF_BY_SCHOOL.get(school, "")
        source_pdf_path = ORIGINAL / source_pdf_name
        if not source_pdf_name or not source_pdf_path.is_file():
            warnings.append(f"{pid}: source PDF missing for school={school}")
            results.append(f"{pid} | warning | source-pdf-missing")
            continue

        if index > 0:
            time.sleep(API_SLEEP_SEC)

        ocr_result, _ = ocr(str(crop_path))
        ocr_hint = "\n".join([row[1] for row in (ocr_result or [])[:80]])

        try:
            solved = solve_problem_with_gemini(
                api_key=gemini_key,
                model=GEMINI_MODEL,
                image_path=crop_path,
                ocr_hint=ocr_hint,
                timeout_sec=180,
            )
        except Exception as exc:  # pylint: disable=broad-except
            warnings.append(f"{pid}: ai-solve-failed ({exc})")
            results.append(f"{pid} | warning | ai-solve-failed")
            uncertain.append(pid)
            continue

        raw_dump[pid] = {
            "qtype": solved.qtype,
            "question_markdown": solved.question_markdown,
            "choices_markdown": solved.choices_markdown,
            "answer_text": solved.answer_text,
            "solution_markdown": solved.solution_markdown,
            "raw_response_text": solved.raw_response_text,
        }

        qtype = task.qtype_override.strip() or solved.qtype.strip() or _default_qtype(source_kind)
        if source_kind == "objective":
            qtype = "객관식"

        question = _normalize_question(solved.question_markdown)
        choices = _normalize_choices(solved.choices_markdown) if source_kind == "objective" else ""
        answer = _normalize_answer(solved.answer_text)
        solution = _normalize_solution(solved.solution_markdown)

        if source_kind == "objective":
            if not choices or len([ln for ln in choices.splitlines() if ln.strip()]) < 5:
                uncertain.append(pid)
                warnings.append(f"{pid}: objective choices may be incomplete")
            if not answer:
                uncertain.append(pid)
                warnings.append(f"{pid}: objective answer empty")
        else:
            if not answer:
                uncertain.append(pid)
                warnings.append(f"{pid}: subjective answer empty")

        if not question:
            uncertain.append(pid)
            warnings.append(f"{pid}: question text empty")
            results.append(f"{pid} | warning | empty-question")
            continue
        if not solution:
            uncertain.append(pid)
            warnings.append(f"{pid}: solution text empty")

        classified = classify_unit_and_level(
            question_text=question,
            choices_text=choices,
            answer_text=answer,
            solution_text=solution,
            qtype=qtype,
            grade=FIXED_META["grade"],
            problem_no=number,
        )
        unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
            classified.unit_l1,
            classified.unit_l2,
            classified.unit_l3,
            grade=FIXED_META["grade"],
        )

        target.mkdir(parents=True, exist_ok=False)
        assets_original = target / "assets" / "original"
        assets_original.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_pdf_path, assets_original / source_pdf_name)

        front = _build_front(
            pid=pid,
            qtype=qtype,
            source_kind=source_kind,
            source_no=source_no,
            unit_triplet=(unit_l1, unit_l2, unit_l3),
            level=int(classified.level),
            source_pdf_name=source_pdf_name,
        )
        _write_problem_md(
            folder=target,
            front=front,
            question=question,
            choices=choices,
            answer=answer,
            solution=solution,
        )

        summary["created"] += 1
        review_paths.append(str((target / "problem.md").resolve()))
        results.append(
            f"{pid} | created | kind={source_kind} source_no={source_no} "
            f"unit={unit_l3} level={classified.level}"
        )

    # De-dup uncertain list while preserving insertion order.
    seen = set()
    uncertain_unique: List[str] = []
    for pid in uncertain:
        if pid in seen:
            continue
        seen.add(pid)
        uncertain_unique.append(pid)

    summary["warnings"] = len(warnings)
    RAW_JSON_PATH.write_text(
        json.dumps(raw_dump, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report_lines: List[str] = [
        (
            f"created={summary['created']} updated={summary['updated']} "
            f"skipped={summary['skipped']} warnings={summary['warnings']}"
        ),
        "",
        "[RESULTS]",
    ]
    report_lines.extend(results)

    report_lines.extend(["", "[OCR_OR_MATH_UNCERTAIN]"])
    if uncertain_unique:
        report_lines.extend([f"- {pid}" for pid in uncertain_unique])
    else:
        report_lines.append("- none")

    report_lines.extend(["", "[WARNINGS]"])
    if warnings:
        report_lines.extend([f"- {msg}" for msg in warnings])
    else:
        report_lines.append("- none")

    report_lines.extend(["", "[REVIEW_PATHS]"])
    if review_paths:
        report_lines.extend([f"- {path}" for path in review_paths])
    else:
        report_lines.append("- none")

    report_lines.extend(["", f"[RAW_AI_DUMP] {RAW_JSON_PATH}"])
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print(f"\nreport: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
