import os
from pathlib import Path

# ===== 설정만 바꾸면 됨 =====
BASE_DIR = Path("db/problems")      # 생성 위치
SCHOOL = "JEHS"                     # 학교 약칭
YEAR = 2025
GRADE = 1
SEMESTER = 1
EXAM = "MID"                        # MID 또는 FINAL
START_NUM = 1
END_NUM = 100                       # 100문항
DIFFICULTY_DEFAULT = ""             # 처음엔 비워도 OK
UNIT_DEFAULT = ""                   # 처음엔 비워도 OK

TEMPLATE = """---
id: {id}
school: {school}
year: {year}
grade: {grade}
semester: {semester}
exam: {exam}
type: {qtype}
difficulty: {difficulty}
unit: {unit}
source: ""
tags: []
assets:
  # Used only for inline figure images referenced in Q/Choices markdown.
  # Example: ![도형](assets/scan.png)
  # Do not use this for raw source archives.
  - assets/scan.png
  # Raw source image archive location.
  - assets/original/
---

## Q
(여기에 문제 텍스트)

## Choices
①
②
③
④
⑤

## Answer
(정답) 

## Solution
(풀이. 지금은 비워도 됨)
"""

def main():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    for n in range(START_NUM, END_NUM + 1):
        qid = f"{SCHOOL}-{YEAR}-G{GRADE}-S{SEMESTER}-{EXAM}-{n:03d}"
        folder = BASE_DIR / qid
        assets = folder / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        (assets / "original").mkdir(parents=True, exist_ok=True)

        md_path = folder / "problem.md"
        if not md_path.exists():
            md_path.write_text(
                TEMPLATE.format(
                    id=qid,
                    school=SCHOOL,
                    year=YEAR,
                    grade=GRADE,
                    semester=SEMESTER,
                    exam=EXAM,
                    qtype="객관식",
                    difficulty=DIFFICULTY_DEFAULT,
                    unit=UNIT_DEFAULT,
                ),
                encoding="utf-8"
            )

    print(f"Done: {END_NUM - START_NUM + 1} problems created under: {BASE_DIR}")

if __name__ == "__main__":
    main()
