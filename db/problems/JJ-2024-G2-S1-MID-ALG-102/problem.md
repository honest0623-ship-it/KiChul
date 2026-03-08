---
id: JJ-2024-G2-S1-MID-ALG-102
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: '서답2번'
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 단답형
- 출제번호-서답2번
- 과목-대수
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID1.ALG.pdf
---

## Q
$a>1$, $b>1$일 때, $\left(\log_a a^2b^3\right)\left(\log_b a^3b^2\right)$의 최솟값을 구하시오.

## Choices

## Answer
$25$

## Solution
$t=\log_a b$라 두면 $t>0$이고
$$
\log_a a^2b^3=2+3t,\qquad \log_b a^3b^2=2+\frac{3}{t}
$$
이다.
따라서 곱은
$$
(2+3t)\left(2+\frac{3}{t}\right)=13+6\left(t+\frac1t\right)
$$
이고, $t+\dfrac1t\ge2$이므로 최솟값은 $25$이다.
