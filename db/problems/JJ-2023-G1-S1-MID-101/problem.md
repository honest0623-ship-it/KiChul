---
id: JJ-2023-G1-S1-MID-101
school: JJ
year: 2023
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 1
source_question_kind: subjective
source_question_label: "서답1"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>1. 다항식>1-3. 인수분해"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-3. 인수분해"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 단답형
  - 출제번호-1
assets:
  - assets/original/
  - assets/original/서답1번_1-3. 인수분해.png
---

## Q
다항식 $x^2-20x+k$이 있다. 서로 다른 자연수 $m$, $n$에 대하여 $(x-m)(x-n)$의 꼴로 인수분해되도록 하는 자연수 $k$의 최댓값이 $M$, 최솟값이 $m$일 때, $M-m$의 값을 구하시오.

## Choices

## Answer
80

## Solution
$(x-m)(x-n)=x^2-(m+n)x+mn$이므로
$$
m+n=20,\quad k=mn
$$
을 만족해야 한다.

$m$, $n$은 서로 다른 자연수이므로 가능한 쌍은
$$
(1,19),(2,18),\dots,(9,11)
$$
이다.

각 경우의 $k=mn$을 계산하면 최솟값은
$$
1\times 19=19,
$$
최댓값은
$$
9\times 11=99
$$
이다.

따라서
$$
M-m=99-19=80.
$$
