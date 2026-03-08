---
id: SY-2022-G2-S1-MID-ALG-105
school: SY
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: subjective
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5번
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답5번
- 과목-ALG
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID-ALG-105_original.png
---

## Q
두 집합
\[
A=\left\{x\mid 2^{2x}+2^{x+2}-32<0\right\},\qquad
B=\left\{x\mid (\log_2 x)^2-a\log_2 x+b\le 0\right\}
\]
에 대하여 $A\cap B=\varnothing$, $A\cup B=\{x\mid x\le 128\}$을 만족시킬 때, $a+b$의 값을 구하시오. (단, $a$, $b$는 상수이다.)

## Choices


## Answer
$15$

## Solution
먼저 집합 $A$를 구하자.
\[
t=2^x\quad (t>0)
\]
라 두면
\[
t^2+4t-32<0
\iff (t-4)(t+8)<0
\]
이다.

$t>0$이므로
\[
0<t<4
\]
이고,
\[
x<2
\]
이다. 따라서
\[
A=\{x\mid x<2\}
\]
이다.

또
\[
A\cap B=\varnothing,\qquad A\cup B=\{x\mid x\le 128\}
\]
이므로
\[
B=\{x\mid 2\le x\le 128\}
\]
이어야 한다.

\[
y=\log_2 x
\]
라 두면 $2\le x\le 128$은
\[
1\le y\le 7
\]
과 같다.

따라서
\[
y^2-ay+b\le 0
\]
의 해가 $1\le y\le 7$이 되어야 하므로
\[
y^2-ay+b=(y-1)(y-7)=y^2-8y+7
\]
이다.

따라서
\[
a=8,\qquad b=7
\]
이고,
\[
a+b=15
\]
이다.
