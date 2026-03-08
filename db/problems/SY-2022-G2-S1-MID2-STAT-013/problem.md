---
id: SY-2022-G2-S1-MID2-STAT-013
school: SY
year: 2022
grade: 2
semester: 1
exam: MID2
subject: STAT
type: objective
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-13
- 과목-STAT
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID2-STAT-013_original.png
---

## Q
크기와 모양이 각각 같은 축구공 $6$개, 배구공 $11$개, 농구공 $11$개 중에서 $11$개의 공을 택하는 경우의 수는?

## Choices
① $56$
② $60$
③ $63$
④ $68$
⑤ $77$

## Answer
③

## Solution
축구공, 배구공, 농구공을 각각 $x$, $y$, $z$개 고른다고 하면
\[
x+y+z=11
\]
이고,
\[
0\le x\le 6,\qquad y\ge 0,\qquad z\ge 0
\]
이다.

제한이 없다면 음이 아닌 정수해의 개수는
\[
{}_{3}H_{11}={}_{13}C_{2}=78
\]
이다.

여기서 축구공을 $7$개 이상 고르는 경우를 빼야 한다.
$x'=x-7$이라 두면
\[
x'+y+z=4
\]
의 음이 아닌 정수해 개수와 같으므로
\[
{}_{3}H_{4}={}_{6}C_{2}=15
\]
이다.

따라서 구하는 경우의 수는
\[
78-15=63
\]
이다.
