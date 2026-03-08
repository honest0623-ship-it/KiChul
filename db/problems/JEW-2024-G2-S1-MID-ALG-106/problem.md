---
id: JEW-2024-G2-S1-MID-ALG-106
school: JEW
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 6
source_question_kind: subjective
source_question_label: '서답6번'
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서술형
- 출제번호-서답6번
- 과목-대수
assets:
- assets/original/
- assets/original/JEW.2024.G2.S1.MID1.ALG.pdf
---

## Q
$\dfrac13\le x\le 9$에서 함수 $y=kx^{-4+\log_3 x}$의 최댓값이 $9$이고, $x=\alpha$에서 최솟값 $m$을 가질 때, $\dfrac{\alpha k}{m}$의 값을 구하시오. (단, $k>0$)

## Choices

## Answer
$729$

## Solution
$t=\log_3 x$라 두면 $x=3^t$이고, $\dfrac13\le x\le9$에서 $-1\le t\le2$이다.
또
$$
x^{-4+\log_3 x}=(3^t)^{-4+t}=3^{t^2-4t}=3^{(t-2)^2-4}
$$
이므로
$$
y=k\cdot 3^{(t-2)^2-4}
$$
이다.
구간 $-1\le t\le2$에서 $(t-2)^2$의 최댓값은 $9$이므로 최댓값은 $243k$이다.
$$
243k=9 \Rightarrow k=\frac1{27}
$$
이다.
최솟값은 $(t-2)^2$가 가장 작을 때, 즉 $t=2$일 때 얻으므로 $\alpha=9$이고
$$
m=\frac1{27}\cdot 3^{-4}=3^{-7}
$$
이다.
$$
\frac{\alpha k}{m}=\frac{9\cdot \frac1{27}}{3^{-7}}=729
$$
