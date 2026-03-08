---
id: SY-2022-G2-S1-MID2-STAT-102
school: SY
year: 2022
grade: 2
semester: 1
exam: MID2
subject: STAT
type: subjective
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2번
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답2번
- 과목-STAT
- 생성일-2026-03-07
assets:
- assets/scan.png
- assets/original/
- assets/original/SY-2022-G2-S1-MID2-STAT-102_original.png
---

## Q
오른쪽 그림은 호수가 있는 어느 마을의 도로망이다. $A$지역에서 $B$지역까지 최단 거리로 가는 경우의 수를 구하시오.

<img src="assets/scan.png" alt="호수가 있는 도로망" style="width:60% !important; max-width:60% !important; height:auto;" />

## Choices


## Answer
$30$

## Solution
오른쪽 또는 위쪽으로만 움직이며 각 교차점까지의 최단 경로 수를 적어 가면 된다.

맨 아래 줄부터 차례로 적으면
\[
1,\ 1,\ 1,\ 1,\ 1,\ 1
\]
\[
1,\ 2,\ 0,\ 1,\ 2,\ 3
\]
\[
1,\ 3,\ 0,\ 0,\ 2,\ 5
\]
\[
1,\ 4,\ 4,\ 4,\ 6,\ 11
\]
\[
1,\ 5,\ 9,\ 13,\ 19,\ 30
\]
이다.

따라서 $B$지역까지 최단 거리로 가는 경우의 수는
\[
30
\]
이다.
