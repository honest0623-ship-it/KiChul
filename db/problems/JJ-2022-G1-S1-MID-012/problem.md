---
id: JJ-2022-G1-S1-MID-012
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: objective
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-3. 인수분해
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-3. 인수분해
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-12
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---
## Q
다항식 $f(x)=x^3+2x^2-(k+3)x+k$가 $x$의 계수와 상수항이 정수인 세 일차식의 곱으로 인수분해될 때, $400$ 이하의 자연수 $k$의 개수는?

## Choices
① $14$
② $15$
③ $16$
④ $17$
⑤ $18$

## Answer
⑤

## Solution
최고차항의 계수가 $1$인 삼차다항식 $f(x)$가 $x-1$로 나누어떨어지므로
\[
f(x)=(x-1)(x^2+3x-k)
\]
로 둘 수 있다. 이때 이차방정식
\[
x^2+3x-k=0
\]
의 서로 다른 두 실근이 모두 정수가 되려면 판별식
\[
9+4k
\]
가 홀수의 제곱이어야 한다.

\[
9+4k=n^2
\]
라 두면 $n$은 홀수이고, $k\le 400$이므로
\[
n^2\le 1609
\]
이다. 따라서 가능한 홀수 $n$은
\[
5,7,9,\dots,39
\]
이고, 그 개수는
\[
\frac{39-5}{2}+1=18
\]
이다.

따라서 정답은 ⑤이다.
