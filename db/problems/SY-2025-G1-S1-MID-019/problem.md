---
id: SY-2025-G1-S1-MID-019
school: SY
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 19
source_question_kind: objective
source_question_label: '19'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-19
assets:
- assets/original/
- assets/original/019.png
---
## Q
$$
\frac{1}{i}-\frac{1}{i^2}+\frac{1}{i^3}-\frac{1}{i^4}+\cdots+\frac{(-1)^{n+1}}{i^n}=1
$$
이 성립하도록 하는 $100$ 이하의 자연수 $n$의 개수는?

## Choices
① $23$  
② $24$  
③ $25$  
④ $26$  
⑤ $27$

## Answer
③

## Solution
각 항을 계산하면
$$
\frac{1}{i}=-i,\quad -\frac{1}{i^2}=1,\quad \frac{1}{i^3}=i,\quad -\frac{1}{i^4}=-1
$$
이므로 4항씩 주기가 반복된다.
부분합을 $S_n$이라 하면
$$
S_1=-i,\ S_2=1-i,\ S_3=1,\ S_4=0
$$
이고 이후 동일하게 반복되므로 $S_n=1$은
$$
n\equiv3\pmod{4}
$$
일 때 성립한다.
$100$ 이하에서 $n=3,7,11,\dots,99$ 이므로 개수는
$$
\frac{99-3}{4}+1=25.
$$
