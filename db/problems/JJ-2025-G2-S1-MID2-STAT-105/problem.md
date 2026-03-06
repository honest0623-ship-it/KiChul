---
id: JJ-2025-G2-S1-MID2-STAT-105
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 5
source_question_kind: subjective
source_question_label: '서답5번'
difficulty: 5
level: 5
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답5번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
흰공 4개, 검은공 5개와 서로 다른 네 상자가 있다. 이 9개의 공을 4개의 상자에 다음 조건을 만족하도록 남김없이 나누어 넣는 경우의 수를 구하여라. (단, 같은 색의 공끼리는 서로 구별하지 않는다.)

<div style="border:1px solid #000; padding:8px; margin:8px 0;">(가) 흰 공만 들어있는 상자의 수는 2이다.<br/>(나) 검은 공만 들어있는 상자의 수는 1이다.<br/>(다) 모든 상자에는 적어도 하나의 공이 들어 있다.</div>

## Choices

## Answer
144

## Solution
조건 (가), (나), (다)에 의해 4개의 상자 유형은
$$
\text{흰공 전용 2개, 검은공 전용 1개, 섞인 상자 1개}
$$
로 정해진다.

먼저 상자 유형 배정:
섞인 상자를 고르는 방법 4가지,
남은 3개 중 검은공 전용 상자를 고르는 방법 3가지.
따라서
$$
4\times 3=12
$$
가지.

흰공 4개는 (흰공 전용 2상자 + 섞인 상자)로, 모두 1개 이상이므로
$$
w_1+w_2+w_3=4\ (w_i\ge 1)
$$
의 해의 수는
$$
{}_{3}C_{2}=3
$$
가지.

검은공 5개는 (검은공 전용 1상자 + 섞인 상자)로, 모두 1개 이상이므로
$$
b_1+b_2=5\ (b_i\ge 1)
$$
의 해의 수는
$$
{}_{4}C_{1}=4
$$
가지.

따라서 전체 경우의 수는
$$
12\times 3\times 4=144
$$
이다.
