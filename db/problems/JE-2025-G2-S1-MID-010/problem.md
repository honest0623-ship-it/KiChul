---
id: JE-2025-G2-S1-MID-010
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: '10'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-10
assets:
- assets/original/
- assets/original/010_1-1. 지수와 로그.png
---
## Q
등식
$$
\left(3^a+3^{-a}\right)^2=7\left(3^a+3^{-a}\right)-6
$$
을 만족시키는 실수 $a$에 대하여 $27^a+27^{-a}$의 값을 구하면?

## Choices
① $194$  
② $195$  
③ $196$  
④ $197$  
⑤ $198$

## Answer
⑤

## Solution
$$
t=3^a+3^{-a}
$$
로 두면 주어진 식은
$$
t^2=7t-6
\Rightarrow t^2-7t+6=0
$$
이므로
$$
t=1 \text{ 또는 } t=6
$$
이다.

그런데
$$
3^a+3^{-a}\ge 2
$$
이므로 $t=6$이다.

이제
$$
27^a+27^{-a}=3^{3a}+3^{-3a}
$$
이고,
$$
\left(u+\frac{1}{u}\right)^3
=u^3+\frac{1}{u^3}+3\left(u+\frac{1}{u}\right)
$$
를 $u=3^a$에 적용하면
$$
3^{3a}+3^{-3a}=t^3-3t
$$
이다.

따라서
$$
27^a+27^{-a}=6^3-3\cdot 6=216-18=198
$$
이다.
