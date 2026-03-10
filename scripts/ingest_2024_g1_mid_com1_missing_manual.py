from __future__ import annotations

from dataclasses import dataclass
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import fitz
import yaml

import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level  # noqa: E402
from unit_taxonomy import normalize_unit_triplet  # noqa: E402


ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"
REPORT = ROOT / "_tmp_2024_g1_mid_com1_missing_report.txt"

META_COMMON = {
    "year": 2024,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "subject": "COM1",
    "source": "user_upload_2026-03-05",
    "subjective_offset": 100,
}


PDF_BY_SCHOOL = {
    "BY": "BY.2024.G1.S1.MID.COM1.pdf",
    "HN": "HN.2024.G1.S1.MID.COM1.pdf",
    "JEW": "JEW.2024.G1.S1.MID.COM1.pdf",
    "JJ": "JJ.2024.G1.S1.MID.COM1.pdf",
}


MISSING_OBJECTIVE: Dict[str, List[int]] = {
    "BY": [1, 2, 3, 4, 6, 7, 8, 10, 11, 13],
    "HN": [1, 2, 3, 5, 6, 8, 11, 12, 13],
    "JEW": [1, 2, 3, 4, 5, 6, 7, 11, 15, 17],
    "JJ": [2, 3, 5, 8],
}


MISSING_SUBJECTIVE: Dict[str, List[int]] = {
    "BY": [],
    "HN": [1, 2],
    "JEW": [1, 2],
    "JJ": [],
}


ANSWER_OBJECTIVE: Dict[str, Dict[int, str]] = {
    "BY": {
        1: "③",
        2: "①",
        3: "②",
        4: "④",
        6: "⑤",
        7: "⑤",
        8: "④",
        10: "②",
        11: "①",
        13: "①",
    },
    "HN": {
        1: "④",
        2: "②",
        3: "④",
        5: "③",
        6: "②",
        8: "①",
        11: "③",
        12: "⑤",
        13: "①",
    },
    "JEW": {
        1: "③",
        2: "②",
        3: "①",
        4: "①",
        5: "④",
        6: "②",
        7: "⑤",
        11: "⑤",
        15: "②",
        17: "①",
    },
    "JJ": {
        2: "⑤",
        3: "③",
        5: "⑤",
        8: "②",
    },
}


ANSWER_SUBJECTIVE: Dict[str, Dict[int, str]] = {
    "HN": {
        1: "3",
        2: "31",
    },
    "JEW": {
        1: r"$3-2i$",
        2: "-8",
    },
}


PUA_MAP = {
    "\ue000": "A",
    "\ue001": "B",
    "\ue002": "C",
    "\ue00f": "P",
    "\ue010": "Q",
    "\ue011": "R",
    "\ue012": "S",
    "\ue034": "1",
    "\ue035": "2",
    "\ue036": "3",
    "\ue037": "4",
    "\ue038": "5",
    "\ue039": "6",
    "\ue03a": "7",
    "\ue03b": "8",
    "\ue03c": "9",
    "\ue03d": "0",
    "\ue044": "(",
    "\ue045": ")",
    "\ue046": "-",
    "\ue047": "=",
    "\ue048": "+",
    "\ue04b": "{",
    "\ue04c": "}",
    "\ue04d": "|",
    "\ue052": ",",
    "\ue055": "<",
    "\ue056": ">",
    "\ue05c": "√",
    "\ue06d": "/",
    "\ue078": "{",
    "\ue079": "|",
    "\ue07a": "}",
    "\ue07b": "",
    "\ue09d": "α",
    "\ue09e": "β",
    "\ue09f": "γ",
    "\ue0e5": "a",
    "\ue0e6": "b",
    "\ue0e7": "c",
    "\ue0e8": "d",
    "\ue0e9": "e",
    "\ue0ea": "f",
    "\ue0eb": "g",
    "\ue0ed": "i",
    "\ue0ef": "k",
    "\ue0f1": "m",
    "\ue0f2": "n",
    "\ue0f4": "p",
    "\ue0f5": "q",
    "\ue0f6": "r",
    "\ue0f8": "t",
    "\ue0fb": "w",
    "\ue0fc": "x",
    "\ue0fd": "y",
    "\ue0fe": "z",
    "\ue101": "|",
}


OBJ_BLOCK_RE = re.compile(
    r"(?ms)^\s*(\d{1,2})\.\s*(.+?)(?=^\s*\d{1,2}\.\s|^\s*서답형|^\s*서\d\.|^시험지에 이름을 꼭 써주세요|\Z)"
)
MARKER_SPLIT_RE = re.compile(r"(①|②|③|④|⑤)")


def decode_pua(text: str) -> str:
    out = text
    for src, dst in PUA_MAP.items():
        out = out.replace(src, dst)
    out = out.replace("", "10")
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def load_pdf_text_by_page(pdf_path: Path) -> List[str]:
    doc = fitz.open(pdf_path)
    pages: List[str] = []
    for page in doc:
        pages.append(decode_pua(page.get_text("text")))
    doc.close()
    return pages


def clean_question_text(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r"\[\d+(?:\.\d+)?점\]\s*\d+\)\s*$", "", text)
    text = re.sub(r"\[\d+(?:\.\d+)?점\]\s*$", "", text)
    text = re.sub(r"\s+\d+\)\s*$", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def parse_objective_questions(text_pages: List[str]) -> Dict[int, Tuple[str, List[str]]]:
    joined = "\n\n".join(text_pages[:-1])  # exclude answer page
    parsed: Dict[int, Tuple[str, List[str]]] = {}
    for matched in OBJ_BLOCK_RE.finditer(joined):
        qno = int(matched.group(1))
        body = matched.group(2).strip()
        parts = MARKER_SPLIT_RE.split(body)
        if len(parts) < 3:
            continue
        question = clean_question_text(parts[0])
        choice_map: Dict[str, str] = {}
        for idx in range(1, len(parts) - 1, 2):
            marker = parts[idx].strip()
            value = parts[idx + 1].strip()
            value = re.sub(r"\n{2,}", "\n", value).strip()
            choice_map[marker] = value
        choices = [
            choice_map.get("①", ""),
            choice_map.get("②", ""),
            choice_map.get("③", ""),
            choice_map.get("④", ""),
            choice_map.get("⑤", ""),
        ]
        parsed[qno] = (question, choices)
    return parsed


def extract_subjective_q12(school: str, pages: List[str]) -> Dict[int, str]:
    joined = "\n\n".join(pages[:-1])
    out: Dict[int, str] = {}
    if school == "HN":
        m1 = re.search(r"서답형\.\s*1번\)\s*(.+?)\s*\[3점\]\s*18\)", joined, flags=re.S)
        m2 = re.search(r"서답형\.\s*2번\)\s*(.+?)\s*\[3점\]\s*19\)", joined, flags=re.S)
        if m1:
            out[1] = clean_question_text(m1.group(1))
        if m2:
            out[2] = clean_question_text(m2.group(1))
    elif school == "JEW":
        m1 = re.search(r"서1\.\s*(.+?)\s*\[2점\].*?18\)", joined, flags=re.S)
        m2 = re.search(r"서2\.\s*(.+?)\s*\[2점\].*?19\)", joined, flags=re.S)
        if m1:
            out[1] = clean_question_text(m1.group(1).replace("<단답형>", ""))
        if m2:
            out[2] = clean_question_text(m2.group(1).replace("<단답형>", ""))
    return out


def normalize_choices(choices: List[str]) -> List[str]:
    out: List[str] = []
    for value in choices:
        text = value.strip()
        text = re.sub(r"\[\d+(?:\.\d+)?점\]", "", text)
        text = re.sub(r"\n{2,}", "\n", text).strip()
        out.append(text)
    return out


def build_pid(school: str, number: int) -> str:
    return f"{school}-{META_COMMON['year']}-G{META_COMMON['grade']}-S{META_COMMON['semester']}-{META_COMMON['exam']}-{number:03d}"


def write_problem_md(
    folder: Path,
    front: Dict[str, object],
    question: str,
    choices: List[str],
    answer: str,
    solution: str,
) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    parts = [f"## Q\n{question.strip()}"]
    if choices:
        choice_lines = [
            f"① {choices[0]}",
            f"② {choices[1]}",
            f"③ {choices[2]}",
            f"④ {choices[3]}",
            f"⑤ {choices[4]}",
        ]
        parts.append("## Choices\n" + "\n".join(choice_lines).strip())
    else:
        parts.append("## Choices\n")
    parts.append(f"## Answer\n{answer.strip()}")
    parts.append(f"## Solution\n{solution.strip()}")
    body = "\n\n".join(parts).strip() + "\n"
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def classify_triplet(
    question: str,
    choices: List[str],
    answer: str,
    solution: str,
    qtype: str,
) -> Tuple[Tuple[str, str, str], int]:
    result = classify_unit_and_level(
        question_text=question,
        choices_text="\n".join([f"① {choices[0]}", f"② {choices[1]}", f"③ {choices[2]}", f"④ {choices[3]}", f"⑤ {choices[4]}"])
        if choices
        else "",
        answer_text=answer,
        solution_text=solution,
        qtype=qtype,
        grade=int(META_COMMON["grade"]),
    )
    l1, l2, l3 = normalize_unit_triplet(
        result.unit_l1,
        result.unit_l2,
        result.unit_l3,
        grade=int(META_COMMON["grade"]),
    )
    return (l1, l2, l3), int(result.level)


def make_front(
    school: str,
    pid: str,
    source_no: int,
    source_kind: str,
    qtype: str,
    unit_triplet: Tuple[str, str, str],
    level: int,
    source_pdf: str,
) -> Dict[str, object]:
    l1, l2, l3 = unit_triplet
    source_label = str(source_no) if source_kind == "objective" else f"서답{source_no}"
    return {
        "id": pid,
        "school": school,
        "year": META_COMMON["year"],
        "grade": META_COMMON["grade"],
        "semester": META_COMMON["semester"],
        "exam": META_COMMON["exam"],
        "subject": META_COMMON["subject"],
        "type": qtype,
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": source_label,
        "difficulty": level,
        "level": level,
        "unit": f"{l1}>{l2}>{l3}",
        "unit_l1": l1,
        "unit_l2": l2,
        "unit_l3": l3,
        "source": META_COMMON["source"],
        "tags": [qtype, f"출제번호-{source_label}"],
        "assets": [
            "assets/original/",
            f"assets/original/{source_pdf}",
        ],
    }


def run() -> int:
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    duplicates: List[str] = []
    review_paths: List[str] = []

    parsed_objective: Dict[str, Dict[int, Tuple[str, List[str]]]] = {}
    parsed_subjective: Dict[str, Dict[int, str]] = {}

    for school, pdf_name in PDF_BY_SCHOOL.items():
        pdf_path = ORIGINAL / pdf_name
        if not pdf_path.is_file():
            warnings.append(f"{school}: source PDF missing ({pdf_name})")
            continue
        pages = load_pdf_text_by_page(pdf_path)
        parsed_objective[school] = parse_objective_questions(pages)
        parsed_subjective[school] = extract_subjective_q12(school, pages)

    for school in ["BY", "HN", "JEW", "JJ"]:
        pdf_name = PDF_BY_SCHOOL[school]
        pdf_path = ORIGINAL / pdf_name
        if not pdf_path.is_file():
            continue

        # Objective
        for source_no in MISSING_OBJECTIVE.get(school, []):
            pid = build_pid(school, source_no)
            folder = PROBLEMS / pid
            if folder.exists():
                summary["skipped"] += 1
                duplicates.append(pid)
                results.append(f"{pid} | skipped | duplicate-folder-exists")
                continue

            parsed = parsed_objective.get(school, {}).get(source_no)
            if not parsed:
                summary["warnings"] += 1
                uncertain.append(pid)
                warnings.append(f"{pid}: objective question parse failed")
                results.append(f"{pid} | warning | objective-parse-failed")
                continue

            question, choices = parsed
            choices = normalize_choices(choices)
            if any(not item for item in choices):
                uncertain.append(pid)
                choices = [item if item else "(OCR 확인 필요)" for item in choices]

            answer = ANSWER_OBJECTIVE.get(school, {}).get(source_no, "")
            if not answer:
                uncertain.append(pid)
                answer = "(정답 확인 필요)"

            solution = f"정답은 {answer}이다."
            unit_triplet, level = classify_triplet(
                question=question,
                choices=choices,
                answer=answer,
                solution=solution,
                qtype="객관식",
            )

            assets_original = folder / "assets" / "original"
            assets_original.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf_path, assets_original / pdf_name)

            front = make_front(
                school=school,
                pid=pid,
                source_no=source_no,
                source_kind="objective",
                qtype="객관식",
                unit_triplet=unit_triplet,
                level=level,
                source_pdf=pdf_name,
            )
            write_problem_md(folder, front, question, choices, answer, solution)

            summary["created"] += 1
            review_paths.append(str((folder / "problem.md").resolve()))
            results.append(f"{pid} | created | kind=objective source_no={source_no}")

        # Subjective (only explicit missing list)
        for source_no in MISSING_SUBJECTIVE.get(school, []):
            pid = build_pid(school, source_no + int(META_COMMON["subjective_offset"]))
            folder = PROBLEMS / pid
            if folder.exists():
                summary["skipped"] += 1
                duplicates.append(pid)
                results.append(f"{pid} | skipped | duplicate-folder-exists")
                continue

            question = parsed_subjective.get(school, {}).get(source_no, "")
            if not question:
                summary["warnings"] += 1
                uncertain.append(pid)
                warnings.append(f"{pid}: subjective question parse failed")
                results.append(f"{pid} | warning | subjective-parse-failed")
                continue

            answer = ANSWER_SUBJECTIVE.get(school, {}).get(source_no, "")
            if not answer:
                uncertain.append(pid)
                answer = "(정답 확인 필요)"

            solution = f"계산하면 {answer}이다."
            unit_triplet, level = classify_triplet(
                question=question,
                choices=[],
                answer=answer,
                solution=solution,
                qtype="단답형",
            )

            assets_original = folder / "assets" / "original"
            assets_original.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf_path, assets_original / pdf_name)

            front = make_front(
                school=school,
                pid=pid,
                source_no=source_no,
                source_kind="subjective",
                qtype="단답형",
                unit_triplet=unit_triplet,
                level=level,
                source_pdf=pdf_name,
            )
            write_problem_md(folder, front, question, [], answer, solution)

            summary["created"] += 1
            review_paths.append(str((folder / "problem.md").resolve()))
            results.append(f"{pid} | created | kind=subjective source_no={source_no}")

    lines: List[str] = []
    lines.append(
        f"created={summary['created']} updated={summary['updated']} "
        f"skipped={summary['skipped']} warnings={summary['warnings']}"
    )
    lines.append("")
    lines.append("[DUPLICATE_FOLDERS]")
    if duplicates:
        for item in sorted(set(duplicates)):
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("[RESULTS]")
    if results:
        lines.extend(results)
    else:
        lines.append("- none")
    lines.append("")
    lines.append("[OCR_OR_MATH_UNCERTAIN]")
    if uncertain:
        for item in sorted(set(uncertain)):
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("[WARNINGS]")
    if warnings:
        for item in warnings:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("[REVIEW_PATHS]")
    if review_paths:
        for item in review_paths:
            lines.append(f"- {item}")
    else:
        lines.append("- none")

    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(REPORT)
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
