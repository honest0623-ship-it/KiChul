---
id: HN-2025-G2-S1-MID2-STAT-101
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1번
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-05
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답1번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
전체집합 $U=\{1,2,3,4,5,6,7,8\}$의 두 부분집합 $A,B$에 대하여 $A\cap B=\{1,3,5,7\}$을 만족하는 두 집합 $A,B$를 정하는 경우의 수를 구하시오.

## Choices


## Answer
81

## Solution
$1,3,5,7$은 교집합에 반드시 있어야 하므로 각 원소는 $(A,B)$에 대해 $(1,1)$로 고정된다.

나머지 원소 $2,4,6,8$은 교집합에 포함되면 안 되므로
각 원소마다 가능한 포함 형태는
$$
(0,0),\ (1,0),\ (0,1)
$$
의 3가지이다.

서로 독립적으로 4개 원소를 정하면 되므로
$$
3^4=81
$$
이다.
