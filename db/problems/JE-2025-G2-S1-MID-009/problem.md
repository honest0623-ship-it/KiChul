---
id: JE-2025-G2-S1-MID-009
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: '9'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-9
assets:
- assets/original/
- assets/original/009_1-1. 지수와 로그.png
---
## Q
함수
$$
f(x)=\frac{x+1}{2x-1}
$$
에 대하여 $\log_5 2=a$, $\log_5 3=b$일 때, $f(\log_3 24)$의 값을 $a$, $b$로 나타낸 것은?

## Choices
① $\dfrac{a+2b}{6a+3b}$  
② $\dfrac{3a+b}{6a+2b}$  
③ $\dfrac{3a+2b}{6a+b}$  
④ $\dfrac{6a+2b}{3a+b}$  
⑤ $\dfrac{6a+b}{3a+2b}$

## Answer
③

## Solution
$$
\log_3 2=\frac{\log_5 2}{\log_5 3}=\frac{a}{b}
$$
이므로
$$
\log_3 24=\log_3(3\cdot 2^3)=1+3\log_3 2=1+\frac{3a}{b}
=\frac{b+3a}{b}
$$
이다.

따라서
$$
f(\log_3 24)
=\frac{\frac{b+3a}{b}+1}{2\cdot\frac{b+3a}{b}-1}
=\frac{\frac{2b+3a}{b}}{\frac{b+6a}{b}}
=\frac{3a+2b}{6a+b}
$$
이다.
