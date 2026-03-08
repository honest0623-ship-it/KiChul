---
id: JE-2022-G1-S1-MID-106
school: JE
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 6
source_question_kind: subjective
source_question_label: '서술형2'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-6
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JE-2022-G1-S1-MID-106_original.png
---

## Q
복소수 \(\alpha\)에 대하여
\[
\frac{\alpha}{1-\alpha^2}
\]
가 실수일 때, 복소수 \(\alpha\)가 실수인지 허수인지 판별하시오.

## Choices

## Answer
\(\alpha\)는 실수이다.

## Solution
\[
\alpha=x+yi
\]
\((x, y)\)는 실수라고 하자. 그러면
\[
1-\alpha^2=1-(x+yi)^2=1-x^2+y^2-2xyi
\]
이다.
따라서
\[
\frac{\alpha}{1-\alpha^2}
=\frac{(x+yi)(1-x^2+y^2+2xyi)}{(1-x^2+y^2)^2+(2xy)^2}
\]
이다.
이 값이 실수이므로 분자의 허수 부분이 \(0\)이어야 한다. 허수 부분은
\[
y(1-x^2+y^2)+2x^2y=y(1+x^2+y^2)
\]
이다.
그런데 \(1+x^2+y^2>0\)이므로
\[
y=0
\]
이다. 따라서
\[
\alpha=x
\]
이므로 \(\alpha\)는 실수이다.
