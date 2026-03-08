---
id: JEW-2024-G2-S1-MID-ALG-105
school: JEW
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: '서답5번'
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서술형
- 출제번호-서답5번
- 과목-대수
assets:
- assets/original/
- assets/original/JEW.2024.G2.S1.MID1.ALG.pdf
---

## Q
$1<a<b$일 때, 직선 $x=k$가 세 함수 $f(x)=\log_a x$, $g(x)=\log_b x$, $h(x)=-\log_a x$의 그래프와 만나는 점을 각각 $P,Q,R$라 하자. $\overline{PQ}:\overline{PR}=2:5$일 때, $f(b)$의 값을 구하시오. (단, $a,b,k$는 상수이고, $k>1$)

## Choices

## Answer
$5$

## Solution
$x=k$일 때
$$
P(k,\log_a k),\quad Q(k,\log_b k),\quad R(k,-\log_a k)
$$
이다.
따라서
$$
\overline{PQ}=\log_a k-\log_b k,\qquad \overline{PR}=2\log_a k
$$
이고,
$$
\frac{\overline{PQ}}{\overline{PR}}=\frac{2}{5}
$$
이므로
$$
\frac{\frac1{\log a}-\frac1{\log b}}{\frac{2}{\log a}}=\frac25
$$
에서 $\log b=5\log a$를 얻는다.
따라서 $b=a^5$이고
$$
f(b)=\log_a b=\log_a a^5=5
$$
