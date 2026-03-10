from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEM_ROOT = ROOT / "db" / "problems"
REPORT_PATH = ROOT / "output" / "com1_2022_mid_review_report.md"

TARGET_SCHOOLS = {"JEW", "JJ", "SY"}

UNIT_MAP = {
    "????1(2022??)": "공통수학1(2022개정)",
    "1. ???": "1. 다항식",
    "2. ???? ???": "2. 방정식과 부등식",
    "1-1. ???? ??": "1-1. 다항식의 연산",
    "1-2. ?????": "1-2. 나머지정리",
    "1-3. ????": "1-3. 인수분해",
    "2-1. ???? ?????": "2-1. 복소수와 이차방정식",
    "2-2. ?????? ????": "2-2. 이차방정식과 이차함수",
    "????1(2022??)>1. ???>1-1. ???? ??": "공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산",
    "????1(2022??)>1. ???>1-2. ?????": "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리",
    "????1(2022??)>1. ???>1-3. ????": "공통수학1(2022개정)>1. 다항식>1-3. 인수분해",
    "????1(2022??)>2. ???? ???>2-1. ???? ?????": "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식",
    "????1(2022??)>2. ???? ???>2-2. ?????? ????": "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수",
    "1-1. 다항식? ??": "1-1. 다항식의 연산",
    "2-1. 다항식? ?????": "2-1. 복소수와 이차방정식",
    "공통수학1(2022개정)>1. 다항식>1-1. 다항식? ??": "공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산",
    "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 다항식? ?????": "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식",
}

OBJECTIVE_ANSWERS = {
    "JEW": {
        "001": "③",
        "002": "④",
        "003": "⑤",
        "004": "②",
        "005": "③",
        "006": "①",
        "007": "④",
        "008": "①",
        "009": "③",
        "010": "②",
        "011": "④",
        "012": "⑤",
        "013": "①",
        "014": "②",
        "015": "②",
        "016": "⑤",
        "017": "③",
    },
    "JJ": {
        "001": "②",
        "002": "③",
        "003": "④",
        "004": "①",
        "005": "①",
        "006": "③",
        "007": "②",
        "008": "⑤",
        "009": "②",
        "010": "②",
        "011": "①",
        "012": "⑤",
        "013": "④",
        "014": "③",
        "015": "①",
    },
    "SY": {
        "001": "④",
        "002": "④",
        "003": "④",
        "004": "②",
        "005": "③",
        "006": "②",
        "007": "⑤",
        "008": "②",
        "009": "④",
        "010": "②",
        "011": "①",
        "012": "①",
        "013": "⑤",
        "014": "③",
        "015": "①",
    },
}


def replace_line(text: str, key: str, value: str) -> str:
    return re.sub(rf"^{re.escape(key)}:.*$", f"{key}: {value}", text, count=1, flags=re.M)


def fix_choices(text: str) -> str:
    match = re.search(r"## Choices\n(.*?)(\n## Answer)", text, re.S)
    if not match:
        return text
    body = match.group(1).rstrip("\n")
    lines = body.splitlines()
    if not lines:
        return text
    circled = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨"]
    new_lines = []
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped:
            new_lines.append(line)
            continue
        content = re.sub(r"^[①②③④⑤⑥⑦⑧⑨\?]\s*", "", stripped)
        prefix = circled[idx] if idx < len(circled) else f"{idx + 1}."
        new_lines.append(f"{prefix} {content}")
    new_body = "\n".join(new_lines)
    return text[: match.start(1)] + new_body + text[match.end(1) :]


def fix_answer(text: str, answer: str) -> str:
    return re.sub(r"(?s)(## Answer\n)(.*?)(\n## Solution|\Z)", rf"\1{answer}\3", text, count=1)


def extract_numeric_id(problem_id: str) -> str:
    return problem_id.rsplit("-", 1)[-1]


def build_tags(kind: str, label: str, created: str) -> list[str]:
    if kind == "objective":
        return [
            "- 수동생성",
            "- PDF",
            "- objective",
            f"- 출제번호-{label}",
            "- 과목-COM1",
            f"- 생성일-{created}",
        ]
    return [
        "- 수동생성",
        "- PDF",
        "- subjective",
        f"- 출제번호-{label}",
        "- 과목-COM1",
        f"- 생성일-{created}",
    ]


def replace_tags(text: str, tags: list[str]) -> str:
    return re.sub(r"(?ms)^tags:\n(?:- .*?\n)+", "tags:\n" + "\n".join(tags) + "\n", text, count=1)


def garble_score(text: str) -> int:
    # Use ASCII question marks as the corruption indicator for these files.
    return text.count("?")


def main() -> None:
    report_lines = [
        "# COM1 2022 MID Review Report",
        "",
        "Targets: `JEW`, `JJ`, `SY` / `2022 G1 S1 MID COM1`",
        "",
        "| Problem ID | Q `?` count | Solution `?` count | Notes |",
        "| --- | ---: | ---: | --- |",
    ]

    for problem_dir in sorted(PROBLEM_ROOT.iterdir()):
        if not problem_dir.is_dir():
            continue
        m = re.match(r"^(JEW|JJ|SY)-2022-G1-S1-MID-(\d+)$", problem_dir.name)
        if not m:
            continue
        school, numeric = m.groups()
        path = problem_dir / "problem.md"
        text = path.read_text(encoding="utf-8")

        kind_match = re.search(r"^source_question_kind:\s*(objective|subjective)\s*$", text, re.M)
        kind = kind_match.group(1) if kind_match else ("subjective" if int(numeric) >= 100 else "objective")
        label = numeric.lstrip("0") or "0"
        if kind == "subjective":
            subjective_no = str(int(numeric) - 100)
            label = f"서{subjective_no}"

        created_match = re.search(r"- 생성일-(\d{4}-\d{2}-\d{2})", text)
        created = created_match.group(1) if created_match else "2026-03-07"

        text = replace_line(text, "type", kind)
        text = replace_line(text, "source_question_label", f"'{label}'")
        text = replace_tags(text, build_tags(kind, label, created))

        for old, new in UNIT_MAP.items():
            text = text.replace(old, new)

        if kind == "objective":
            text = fix_choices(text)
            answer = OBJECTIVE_ANSWERS.get(school, {}).get(numeric)
            if answer:
                text = fix_answer(text, answer)

        if problem_dir.name in {"JJ-2022-G1-S1-MID-105", "SY-2022-G1-S1-MID-105"}:
            text = fix_answer(text, "(1) $3$\n\n(2) $-1,\\ 2$")

        path.write_text(text, encoding="utf-8")

        q_match = re.search(r"## Q\n(.*?)(?:\n## Choices|\n## Answer)", text, re.S)
        s_match = re.search(r"## Solution\n(.*)$", text, re.S)
        q_score = garble_score(q_match.group(1) if q_match else "")
        s_score = garble_score(s_match.group(1) if s_match else "")
        notes = []
        if q_score:
            notes.append("Q text still needs original-based restoration")
        if s_score:
            notes.append("solution text still garbled")
        report_lines.append(
            f"| {problem_dir.name} | {q_score} | {s_score} | {'; '.join(notes) if notes else 'cleaned common fields'} |"
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
