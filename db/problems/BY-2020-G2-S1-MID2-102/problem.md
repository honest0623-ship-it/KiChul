---
id: BY-2020-G2-S1-MID2-102
school: BY
year: 2020
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2번
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 서답형(단답형)
- 출제번호-서답2번
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q102.original.png
---

## Q
4개의 수 0, 1, 2, 3에서 중복을 허용하여 만들 수 있는 자연수를 크기가 작은 수부터 순서대로 나열할 때, 230은 몇 번째에 오는 수인지 구하여라.

## Choices


## Answer
$44$

## Solution
230보다 작거나 같은 수 중에서, 숫자 0,1,2,3만으로 만들어지는 자연수의 개수를 센다.

한 자리 수: $1,2,3$으로 3개.

두 자리 수: 십의 자리는 1,2,3 중 하나(3가지), 일의 자리는 0,1,2,3(4가지)이므로 $3\times 4=12$개.

세 자리 수에서 230 이하:
- 백의 자리가 1이면 $4\times 4=16$개
- 백의 자리가 2이면, 십의 자리는 0 또는 1 또는 2 만 가능하므로 $3\times 4=12$개
- 그리고 230 자체 1개

따라서 순서는
$$
3+12+16+12+1=44
$$
번째이다.
