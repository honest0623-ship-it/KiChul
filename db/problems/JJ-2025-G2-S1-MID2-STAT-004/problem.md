---
id: JJ-2025-G2-S1-MID2-STAT-004
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 4
source_question_kind: objective
source_question_label: '4'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-4
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
- assets/scan.png
---

## Q
아래 그림과 같은 도로망에서 A 지점에서 C 지점을 거치지 않고 B 지점까지 최단 거리로 가는 경우의 수는?

<img src="assets/scan.png" alt="도로망 그림" style="width:60% !important; max-width:60% !important; height:auto;" />

## Choices
① 60
② 66
③ 72
④ 78
⑤ 84

## Answer
②

## Solution
그림에서 A에서 B까지 최단 거리로 가려면
오른쪽으로 5번, 위로 4번 이동하므로 전체 경우의 수는
$$
{}_{9}C_{4}=126
$$
이다.

C를 거치는 최단 경로 수를 구하면,
A에서 C까지는 오른쪽 3번, 위로 2번이므로
$$
{}_{5}C_{2}=10
$$
C에서 B까지는 오른쪽 2번, 위로 2번이므로
$$
{}_{4}C_{2}=6
$$
이다.

따라서 C를 거치지 않는 경우의 수는
$$
126-10\times 6=66
$$
이다.
