---
id: BY-2024-G2-S1-MID-ALG-102
school: BY
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: '서답2번'
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 단답형
- 출제번호-서답2번
- 과목-대수
assets:
- assets/original/
- assets/original/BY.2024.G2.S1.MID1.ALG.pdf
---

## Q
$a-1\le x\le a+1$에서 함수
$$
f(x)=\begin{cases}\left(\dfrac12\right)^{x-2} & (x<2)\\[4pt]\log_2 x & (x\ge 2)\end{cases}
$$
의 최댓값과 최솟값의 합이 $3$이 되도록 하는 모든 실수 $a$의 값의 곱을 구하시오.

## Choices

## Answer
$6$

## Solution
$x<2$에서는 $f(x)=2^{2-x}$로 감소하고, $x\ge2$에서는 $f(x)=\log_2 x$로 증가하며, $f(2)=1$이다.
따라서 구간이 $x=2$를 포함하면 최솟값은 $1$이다.

1. $a<1$이면 구간 전체가 $x<2$에 있으므로 최댓값과 최솟값의 합은 $3$이 될 수 없다.
2. $1\le a<3$이면 구간이 $x=2$를 포함하므로 최솟값은 $1$이고, 최댓값은 양 끝점 값 중 큰 값이다. 이때 합이 $3$이 되려면 최댓값이 $2$여야 하므로 $a=2$이다.
3. $a\ge3$이면 구간 전체가 $x\ge2$에 있으므로
$$
\log_2(a-1)+\log_2(a+1)=3\Rightarrow \log_2(a^2-1)=3\Rightarrow a^2=9
$$
이어서 $a=3$이다.
따라서 가능한 $a$는 $2,3$이고, 그 곱은 $6$이다.
