---
id: JJ-2025-G2-S1-MID2-STAT-101
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 1
source_question_kind: subjective
source_question_label: '서답1번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답1번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
네 명의 남학생 $A,B,C,D$와 네 명의 여학생 $E,F,G,H$가 있다. 이 8명의 학생이 일정한 간격을 두고 원 모양의 탁자에 다음 조건을 만족하도록 모두 둘러앉는 경우의 수는?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">(가) $A$와 $B$는 서로 이웃한다.<br/>(나) $E$는 여학생과 이웃하지 않는다.</div>

## Choices

## Answer
288

## Solution
원순열이므로 $E$의 자리를 고정한다.
그러면 $E$의 양옆 두 자리는 남학생이어야 한다.

1. $E$의 양옆이 $C,D$인 경우(순서 고려 2가지)  
남은 5자리(일렬)에는 $A,B,F,G,H$를 배치한다.
이때 $A,B$가 이웃해야 하므로
$$
2\times 4!=48
$$
가지.
따라서
$$
2\times 48=96
$$
가지.

2. $E$의 양옆에 $A$ 또는 $B$가 정확히 하나 있는 경우  
(양옆이 $A,B$인 경우는 $A,B$가 서로 이웃하지 않으므로 제외)
경우의 수는
$$
2\ (선택: A 또는 B)\times
2\ (위치: 왼쪽/오른쪽)\times
2\ (다른 옆자리: C 또는 D)
=8
$$
가지.
남은 한 명($A$ 또는 $B$)의 자리는 이웃 조건 때문에 자동으로 정해지고,
나머지 4명은 자유롭게 배치되므로 $4!=24$가지.
따라서
$$
8\times 24=192
$$
가지.

전체 경우의 수는
$$
96+192=288
$$
이다.
