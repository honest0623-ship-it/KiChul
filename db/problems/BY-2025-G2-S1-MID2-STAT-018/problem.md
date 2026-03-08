---
id: BY-2025-G2-S1-MID2-STAT-018
school: BY
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-18
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2025.G2.S1.MID2.STAT.Q018.original.png
---

## Q
집합 $X=\{a,b,c,d,e\}$, $Y=\{1,2,3,4,5\}$에 대하여
다음 조건을 만족시키는 함수 $f:X\to Y$의 개수는?

(가) $f(a)\times f(b)\times f(c)$은 홀수이다.

(나) $f(d)<f(e)$

(다) 함수 $f$의 치역의 원소의 개수는 3이다.

## Choices
① 64
② 81
③ 100
④ 121
⑤ 144

## Answer
⑤

## Solution
$f(a),f(b),f(c)$는 모두 홀수이므로 각각 $\{1,3,5\}$에서 고른다.

$(a,b,c)$의 값 집합 크기에 따라 나눈다.

1. 값 집합 크기 1

경우의 수는 3가지.
이때 $(f(d),f(e))$의 값 집합이 기존 값을 제외한 2개가 되어야 하므로
$$
{}_{4}C_{2}=6
$$
가지.
기여도는 $3\times 6=18$.

2. 값 집합 크기 2

경우의 수는
$$
{}_{3}C_{2}\times (2^3-2)=18
$$
가지.
이때 $(d,e)$의 두 값은 기존 2개 중 1개와 나머지 3개 중 1개를 골라야 하므로
$$
2\times 3=6
$$
가지.
기여도는 $18\times 6=108$.

3. 값 집합 크기 3

경우의 수는 $3!=6$가지.
이때 $(d,e)$의 값은 그 3개 중 2개를 고르는
$$
{}_{3}C_{2}=3
$$
가지.
기여도는 $6\times 3=18$.

따라서 전체 개수는
$$
18+108+18=144
$$
이다.
