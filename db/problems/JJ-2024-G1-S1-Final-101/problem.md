---
id: JJ-2024-G1-S1-Final-101
school: JJ
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM1
type: 서답형
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-03-07
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서1
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2024.G1.S1.Final.COM1.pdf
---

## Q
삼차방정식
\[
x^3+2(1-k)x^2+(6-3k)x+2k+12=0
\]
이
\[
1\le x\le 3
\]
에서 실근을 갖도록 하는 실수 $k$의 값의 범위를 구하시오.

## Choices

## Answer
\[
3\le k\le 7
\]

## Solution
주어진 방정식을 $k$에 대하여 정리하면
\[
x^3+2x^2+6x+12-k(2x^2+3x-2)=0
\]
이다.

따라서 실근 $x$에 대하여
\[
k=\frac{x^3+2x^2+6x+12}{2x^2+3x-2}
\]
이다.

분자와 분모를 인수분해하면
\[
x^3+2x^2+6x+12=(x+2)(x^2+6)
\]
\[
2x^2+3x-2=(2x-1)(x+2)
\]
이므로
\[
k=\frac{x^2+6}{2x-1}
\]
이다.

이제
\[
f(x)=\frac{x^2+6}{2x-1}
\]
이라 두자.

$1\le x\le 3$에서
\[
f'(x)=\frac{2x(2x-1)-2(x^2+6)}{(2x-1)^2}
\]
\[
=\frac{2(x-3)(x+2)}{(2x-1)^2}
\]
이다.

$1\le x\le 3$에서는
\[
f'(x)\le 0
\]
이므로 $f(x)$는 감소한다.

따라서
\[
f(3)\le k\le f(1)
\]
이다.

이때
\[
f(3)=\frac{9+6}{6-1}=3,\qquad
f(1)=\frac{1+6}{2-1}=7
\]
이므로
\[
3\le k\le 7
\]
이다.
