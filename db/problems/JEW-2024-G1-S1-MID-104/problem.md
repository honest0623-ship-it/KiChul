---
id: JEW-2024-G1-S1-MID-104
school: JEW
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: "서답4"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 서술형
  - 출제번호-4
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답4번_1-2. 나머지정리.png
---

## Q
$x^3$의 계수가 $1$인 삼차식 $P(x)$에 대하여 $P(1)=2$, $P(2)=3$, $P(3)=4$일 때, 다음 물음에 답하시오.

(1) 다항식 $P(x)$를 구하는 과정을 서술하시오.

(2) 다항식 $P(x)$를 $x-7$로 나누었을 때의 나머지를 구하는 과정을 서술하시오.

## Choices


## Answer
(1) $P(x)=x^3-6x^2+12x-5$

(2) 나머지 $128$

## Solution
(1) $x^3$의 계수가 $1$인 삼차식이므로
\[
P(x)=x^3+ax^2+bx+c
\]
로 둔다.

$P(1)=2,\ P(2)=3,\ P(3)=4$를 대입하면
\[
a+b+c=1
\]
\[
4a+2b+c=-5
\]
\[
9a+3b+c=-23
\]

둘째 식-첫째 식, 셋째 식-둘째 식을 하면
\[
3a+b=-6,\quad 5a+b=-18
\]
이므로
\[
2a=-12,\ a=-6
\]
\[
b=12,\ c=-5
\]

따라서
\[
P(x)=x^3-6x^2+12x-5
\]

(2) 나머지정리에 의해 $x-7$로 나누었을 때의 나머지는 $P(7)$이다.
\[
P(7)=7^3-6\cdot 7^2+12\cdot 7-5
=343-294+84-5=128
\]

따라서 나머지는
\[
128
\]
이다.
