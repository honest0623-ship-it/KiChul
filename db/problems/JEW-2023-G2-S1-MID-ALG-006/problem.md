---
id: JEW-2023-G2-S1-MID-ALG-006
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 6
source_question_kind: objective
source_question_label: 6
difficulty: 3
level: 3
unit: 대수(2022개정)>3. 수열>3-3. 수열의 합
unit_l1: 대수(2022개정)
unit_l2: 3. 수열
unit_l3: 3-3. 수열의 합
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-6
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-006_original.png
---

## Q
수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합 $S_n$이
$$
S_n=3^n-1
$$
일 때, 이 수열의 일반항 $a_n$은?

## Choices
① $2\cdot 3^{n-1}$
② $3^{n-1}$
③ $3^n$
④ $2\cdot 3^n$
⑤ $3^{n+1}$

## Answer
①

## Solution
$n\ge 2$일 때
$$
a_n=S_n-S_{n-1}
$$
이므로
$$
a_n=(3^n-1)-(3^{n-1}-1)=3^n-3^{n-1}=2\cdot 3^{n-1}
$$
이다.

첫째항도
$$
a_1=S_1=3-1=2
$$
이므로 일반항은
$$
a_n=2\cdot 3^{n-1}
$$
이다.
