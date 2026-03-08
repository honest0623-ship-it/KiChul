---
id: JEW-2024-G2-S1-MID-ALG-017
school: JEW
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-17
- 과목-대수
assets:
- assets/original/
- assets/original/JEW.2024.G2.S1.MID1.ALG.pdf
---

## Q
$a>1$인 상수 $a$와 $n\ge2$인 자연수 $n$에 대하여 곡선 $y=a^x$와 직선 $y=n$이 만나는 점을 $P_n$이라 하자. 선분 $P_nP_{n+1}$을 대각선으로 하고 모든 변이 $x$축 또는 $y$축과 평행한 직사각형의 넓이를 $f(n)$이라 할 때, $f(4)+f(5)+f(6)+f(7)+f(8)=2$이다. $a$의 값을 구하시오.

## Choices
① $\dfrac12$
② 1
③ $\dfrac32$
④ 2
⑤ $\dfrac52$

## Answer
③

## Solution
$P_n=(\log_a n,n)$이므로 직사각형의 높이는 1, 너비는 $\log_a(n+1)-\log_a n$이다.
따라서
$$
f(n)=\log_a\frac{n+1}{n}
$$
이다.
$$
\sum_{n=4}^{8} f(n)=\log_a\frac94=2
$$
이므로 $a^2=\dfrac94$, $a>1$에서
$$
a=\frac32
$$
