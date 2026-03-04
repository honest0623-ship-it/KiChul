---
id: JEW-2025-G2-S1-MID-012
school: JEW
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-12
assets:
- assets/original/
- assets/original/012_1-1. 지수와 로그.png
---
## Q
실수 $x$, $y$가
$$
\frac{1}{x}+\frac{1}{3y}=2
$$
를 만족시킬 때,
$$
5^{2x}=64^y=k
$$
가 성립한다. 상수 $k$의 값은?

## Choices
① $10$  
② $15$  
③ $20$  
④ $25$  
⑤ $30$

## Answer
①

## Solution
$5^{2x}=k$이므로
$$
x=\frac{1}{2}\log_5 k
$$
따라서
$$
\frac{1}{x}
=\frac{2}{\log_5 k}
=\frac{2\ln 5}{\ln k}
$$

또 $64^y=k$이므로
$$
y=\log_{64}k=\frac{\ln k}{\ln 64}=\frac{\ln k}{6\ln 2}
$$
따라서
$$
\frac{1}{3y}
=\frac{1}{3\cdot\frac{\ln k}{6\ln 2}}
=\frac{2\ln 2}{\ln k}
$$

주어진 식에 대입하면
$$
\frac{2\ln 5}{\ln k}+\frac{2\ln 2}{\ln k}=2
$$
$$
\frac{2\ln 10}{\ln k}=2
\Rightarrow \ln k=\ln 10
$$
이므로
$$
k=10
$$
이다.
