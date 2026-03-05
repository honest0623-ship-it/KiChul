from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
from typing import Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"
REPORT = ROOT / "_tmp_jj_2025_g1_mid_com1_manual_missing_report.txt"

META = {
    "school": "JJ",
    "year": 2025,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "subject": "COM1",
    "source": "user_upload_2026-03-05",
    "subjective_offset": 100,
}

SOURCE_PDF = "JJ.2025.G1.S1.MID.COM1.pdf"


def txt(raw: str) -> str:
    return raw.strip()


@dataclass(frozen=True)
class Row:
    source_no: int
    kind: str
    qtype: str
    q: str
    choices: List[str]
    answer: str
    solution: str


ROWS: List[Row] = [
    Row(
        source_no=2,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            $(3x+2)(x^2+ax+a)$의 전개식에서 모든 항의 계수의 합이 35일 때, $x$의 계수는?
            """
        ),
        choices=["① 3", "② 7", "③ 11", "④ 15", "⑤ 19"],
        answer="④",
        solution=txt(
            r"""
            다항식의 모든 항의 계수의 합은 $x=1$을 대입한 값이므로
            $$
            (3\cdot1+2)\bigl(1^2+a\cdot1+a\bigr)=35
            $$
            $$
            5(1+2a)=35 \Rightarrow 1+2a=7 \Rightarrow a=3.
            $$
            따라서
            $$
            (3x+2)(x^2+3x+3)=3x^3+11x^2+15x+6
            $$
            이므로 $x$의 계수는 $15$이다.
            """
        ),
    ),
    Row(
        source_no=3,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            실수 $x, y$에 대하여 $x+y=5$, $x^2+xy+y^2=24$일 때, $x^3+y^3$의 값은?
            """
        ),
        choices=["① 80", "② 90", "③ 100", "④ 110", "⑤ 120"],
        answer="④",
        solution=txt(
            r"""
            $$
            x^2+xy+y^2=(x+y)^2-xy
            $$
            이므로
            $$
            24=25-xy \Rightarrow xy=1.
            $$
            따라서
            $$
            x^3+y^3=(x+y)^3-3xy(x+y)=5^3-3\cdot1\cdot5=125-15=110.
            $$
            """
        ),
    ),
    Row(
        source_no=4,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            $x^3+(1-a)x^2-(a+2)x+2a$가 서로 다른 세 일차식의 곱으로 인수분해 될 때, 다음 중 상수 $a$의 값이 될 수 없는 것은?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="①",
        solution=txt(
            r"""
            $x=1$을 대입하면
            $$
            1+(1-a)-(a+2)+2a=0
            $$
            이므로 $(x-1)$은 인수이다.

            따라서
            $$
            x^3+(1-a)x^2-(a+2)x+2a=(x-1)(x^2+(2-a)x-2a).
            $$
            이차식은
            $$
            x^2+(2-a)x-2a=(x-a)(x+2)
            $$
            이므로
            $$
            (x-1)(x-a)(x+2)
            $$
            로 인수분해된다.

            서로 다른 세 일차식이 되려면 $a\neq1$, $a\neq-2$여야 한다.
            선택지 $1,2,3,4,5$ 중 불가능한 값은 $a=1$이다.
            """
        ),
    ),
    Row(
        source_no=5,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            $x$에 대한 다항식 $6x^3+2x^2-x+1$을 $3x-2$로 나누었을 때, 몫을 $Q(x)$, 나머지를 $R$이라 하자. 이때 $Q(1)-R$의 값은?
            """
        ),
        choices=["① 8", "② -3", "③ 2", "④ 7", "⑤ 12"],
        answer="③",
        solution=txt(
            r"""
            다항식 나눗셈을 하면
            $$
            6x^3+2x^2-x+1=(3x-2)(2x^2+2x+1)+3
            $$
            이다.
            따라서
            $$
            Q(x)=2x^2+2x+1,\quad R=3.
            $$
            $$
            Q(1)-R=(2+2+1)-3=2.
            $$
            """
        ),
    ),
    Row(
        source_no=6,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            $\dfrac{2+3i}{i-1}$의 값을 $a+bi$라 할 때, $a+b$의 값은? (단, $a,b$는 실수)
            """
        ),
        choices=["① -3", "② -2", "③ -1", "④ 1", "⑤ 2"],
        answer="②",
        solution=txt(
            r"""
            분모를 실수로 만들기 위해 $i+1$을 곱하면
            $$
            \frac{2+3i}{i-1}
            =\frac{(2+3i)(i+1)}{(i-1)(i+1)}
            =\frac{-1+5i}{-2}
            =\frac12-\frac52 i.
            $$
            따라서
            $$
            a=\frac12,\quad b=-\frac52
            $$
            이고
            $$
            a+b=\frac12-\frac52=-2.
            $$
            """
        ),
    ),
    Row(
        source_no=7,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            등식 $\dfrac{z}{i}+3i\overline{z}=-4+2i$를 만족시키는 복소수 $z$의 허수 부분의 값은?
            """
        ),
        choices=["① -2", "② -1", "③ 0", "④ 1", "⑤ 2"],
        answer="②",
        solution=txt(
            r"""
            $z=a+bi$ ($a,b$는 실수)라 두면
            $$
            \frac{z}{i}=b-ai,\quad \overline{z}=a-bi,\quad 3i\overline{z}=3b+3ai.
            $$
            따라서
            $$
            \frac{z}{i}+3i\overline{z}=4b+2ai.
            $$
            주어진 식과 비교하면
            $$
            4b=-4,\quad 2a=2
            $$
            이므로
            $$
            b=-1,\quad a=1.
            $$
            $z$의 허수 부분은 $b=-1$이다.
            """
        ),
    ),
    Row(
        source_no=11,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            이차방정식 $x^2+2x-3=0$의 두 근을 $\alpha,\beta$라고 할 때, 두 수 $\dfrac{\alpha}{1+\alpha}$, $\dfrac{\beta}{1+\beta}$를 두 근으로 하고 $x^2$의 계수가 4인 이차방정식을 구하면?
            """
        ),
        choices=[
            "① $4x^2-8x+1=0$",
            "② $4x^2-8x+3=0$",
            "③ $4x^2+8x-1=0$",
            "④ $4x^2+8x+1=0$",
            "⑤ $4x^2+8x+3=0$",
        ],
        answer="②",
        solution=txt(
            r"""
            $\alpha,\beta$에 대해
            $$
            \alpha+\beta=-2,\quad \alpha\beta=-3.
            $$
            새 근을
            $$
            u=\frac{\alpha}{1+\alpha},\quad v=\frac{\beta}{1+\beta}
            $$
            라 두면
            $$
            u+v=\frac{\alpha(1+\beta)+\beta(1+\alpha)}{(1+\alpha)(1+\beta)}
            =\frac{(\alpha+\beta)+2\alpha\beta}{1+(\alpha+\beta)+\alpha\beta}
            =\frac{-2-6}{1-2-3}=2,
            $$
            $$
            uv=\frac{\alpha\beta}{(1+\alpha)(1+\beta)}
            =\frac{-3}{1-2-3}=\frac34.
            $$
            따라서 새 이차방정식은
            $$
            x^2-2x+\frac34=0.
            $$
            $x^2$의 계수를 4로 맞추면
            $$
            4x^2-8x+3=0.
            $$
            """
        ),
    ),
    Row(
        source_no=12,
        kind="objective",
        qtype="객관식",
        q=txt(
            r"""
            이차방정식 $f(x)=0$의 두 근의 합이 4일 때, 이차방정식 $f(2x-5)=0$의 두 근의 합을 구하면?
            """
        ),
        choices=["① -5", "② -2", "③ 1", "④ 4", "⑤ 7"],
        answer="⑤",
        solution=txt(
            r"""
            $f(x)=0$의 두 근을 $r_1,r_2$라 하면
            $$
            r_1+r_2=4.
            $$
            $f(2x-5)=0$의 근은
            $$
            2x-5=r_1,\quad 2x-5=r_2
            $$
            에서
            $$
            x_1=\frac{r_1+5}{2},\quad x_2=\frac{r_2+5}{2}.
            $$
            따라서
            $$
            x_1+x_2=\frac{r_1+r_2+10}{2}=\frac{4+10}{2}=7.
            $$
            """
        ),
    ),
    Row(
        source_no=5,
        kind="subjective",
        qtype="서술형",
        q=txt(
            r"""
            이차방정식 $x^2-abx+a+b=0$의 한 근이 $1+2i$일 때, 실수 $a,b$에 대하여 $a^3-b^3$의 값을 구하시오. (단, $a>b$이다.)
            """
        ),
        choices=[],
        answer=r"$23\sqrt{17}$",
        solution=txt(
            r"""
            계수가 실수이므로 다른 한 근은 $1-2i$이다.
            따라서 근의 합과 곱을 이용하면
            $$
            (1+2i)+(1-2i)=2=ab,
            $$
            $$
            (1+2i)(1-2i)=1+4=5=a+b.
            $$
            즉 $a,b$는
            $$
            t^2-5t+2=0
            $$
            의 두 근이므로
            $$
            a=\frac{5+\sqrt{17}}{2},\quad b=\frac{5-\sqrt{17}}{2}\quad(a>b).
            $$
            따라서
            $$
            a-b=\sqrt{17},\quad
            a^2+ab+b^2=(a+b)^2-ab=25-2=23.
            $$
            그러므로
            $$
            a^3-b^3=(a-b)(a^2+ab+b^2)=\sqrt{17}\cdot23=23\sqrt{17}.
            $$
            """
        ),
    ),
]


def problem_id(row: Row) -> str:
    number = row.source_no
    if row.kind == "subjective":
        number += META["subjective_offset"]
    return (
        f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-"
        f"{META['exam']}-{number:03d}"
    )


def source_label(row: Row) -> str:
    if row.kind == "objective":
        return str(row.source_no)
    return f"서답{row.source_no}번"


def make_front(row: Row, pid: str) -> Dict[str, object]:
    choices_text = "\n".join(row.choices).strip()
    level_info = classify_unit_and_level(
        question_text=row.q,
        choices_text=choices_text,
        answer_text=row.answer,
        solution_text=row.solution,
        qtype=row.qtype,
        grade=META["grade"],
        problem_no=int(pid.rsplit("-", 1)[-1]),
    )
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
        level_info.unit_l1,
        level_info.unit_l2,
        level_info.unit_l3,
        grade=META["grade"],
    )
    return {
        "id": pid,
        "school": META["school"],
        "year": META["year"],
        "grade": META["grade"],
        "semester": META["semester"],
        "exam": META["exam"],
        "subject": META["subject"],
        "type": row.qtype,
        "source_question_no": row.source_no,
        "source_question_kind": row.kind,
        "source_question_label": source_label(row),
        "difficulty": int(level_info.level),
        "level": int(level_info.level),
        "unit": f"{unit_l1}>{unit_l2}>{unit_l3}",
        "unit_l1": unit_l1,
        "unit_l2": unit_l2,
        "unit_l3": unit_l3,
        "source": META["source"],
        "tags": [
            "수동작성",
            row.qtype,
            f"출제번호-{source_label(row)}",
            f"과목-{META['subject']}",
        ],
        "assets": [
            "assets/original/",
            f"assets/original/{SOURCE_PDF}",
        ],
    }


def write_problem(row: Row) -> str:
    pid = problem_id(row)
    folder = PROBLEMS / pid
    if folder.exists():
        return f"{pid} | skipped | duplicate-folder-exists"

    source_path = ORIGINAL / SOURCE_PDF
    if not source_path.is_file():
        raise FileNotFoundError(f"source PDF not found: {source_path}")

    folder.mkdir(parents=True, exist_ok=False)
    original_dir = folder / "assets" / "original"
    original_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, original_dir / SOURCE_PDF)

    front = make_front(row, pid)
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    choices_text = "\n".join(row.choices).strip()
    body = (
        f"## Q\n{row.q.strip()}\n\n"
        f"## Choices\n{choices_text}\n\n"
        f"## Answer\n{row.answer.strip()}\n\n"
        f"## Solution\n{row.solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")
    return f"{pid} | created | kind={row.kind} source_no={row.source_no}"


def main() -> None:
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    review_paths: List[str] = []

    expected = [f"JJ-2025-G1-S1-MID-{n:03d}" for n in range(1, 16)] + [
        f"JJ-2025-G1-S1-MID-{100+n:03d}" for n in range(1, 7)
    ]
    duplicates = [pid for pid in expected if (PROBLEMS / pid).is_dir()]

    created = 0
    skipped = 0
    for row in ROWS:
        line = write_problem(row)
        results.append(line)
        pid = problem_id(row)
        if "| created |" in line:
            created += 1
            review_paths.append(str((PROBLEMS / pid / "problem.md").resolve()))
        else:
            skipped += 1
            uncertain.append(pid)

    # Manual uncertainty flags (source text partially occluded by pen marks).
    uncertain.extend(
        [
            "JJ-2025-G1-S1-MID-004",
            "JJ-2025-G1-S1-MID-006",
            "JJ-2025-G1-S1-MID-007",
            "JJ-2025-G1-S1-MID-105",
        ]
    )
    uncertain = sorted(set(uncertain))

    summary = {
        "created": created,
        "updated": 0,
        "skipped": skipped,
        "warnings": len(warnings),
    }

    report_lines: List[str] = [
        (
            f"created={summary['created']} updated={summary['updated']} "
            f"skipped={summary['skipped']} warnings={summary['warnings']}"
        ),
        "",
        "[DUPLICATE_FOLDERS]",
    ]
    report_lines.extend([f"- {pid}" for pid in duplicates])
    report_lines.extend(["", "[RESULTS]"])
    report_lines.extend(results)
    report_lines.extend(["", "[OCR_OR_MATH_UNCERTAIN]"])
    report_lines.extend([f"- {pid}" for pid in uncertain] if uncertain else ["- none"])
    report_lines.extend(["", "[WARNINGS]"])
    report_lines.extend([f"- {w}" for w in warnings] if warnings else ["- none"])
    report_lines.extend(["", "[REVIEW_PATHS]"])
    report_lines.extend([f"- {p}" for p in review_paths] if review_paths else ["- none"])

    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print(f"\nreport: {REPORT}")


if __name__ == "__main__":
    main()
