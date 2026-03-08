---
id: JEW-2025-G1-S1-FINAL-011
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 11
source_question_kind: objective
source_question_label: '11'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-11
assets:
- assets/scan.png
- assets/original/
- assets/original/011.png
---

## Q
삼차방정식 \(x^3+ax^2-2ax-8=0\)의 실근이 하나가 되도록 하는 정수 \(a\)의 개수는?

## Choices
① 7개
② 8개
③ 9개
④ 10개
⑤ 11개
## Answer
2

## Solution
Since
\[
2^3+a\cdot2^2-2a\cdot2-8=0,
\]
we have \((x-2)\) as a factor:
\[
x^3+ax^2-2ax-8=(x-2)(x^2+(a+2)x+4).
\]
To have exactly one real root, either the quadratic has no real root, or its double root is the same as \(x=2\).
Its discriminant is
\[
(a+2)^2-16=(a+6)(a-2).
\]
If it is negative, then
\[
-6<a<2,
\]
so there are 7 integers.
If it is zero, \(a=-6\) or \(a=2\). Only \(a=-6\) gives \((x-2)^3\), which has one real root.
Therefore the number of integers is
\[
7+1=8.
\]
So the correct choice is 2.
