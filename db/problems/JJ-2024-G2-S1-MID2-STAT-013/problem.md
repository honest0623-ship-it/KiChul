---
id: JJ-2024-G2-S1-MID2-STAT-013
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 2
level: 2
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-13
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q013.png
---

## Q
네 명의 학생 $A,B,C,D$를 포함한 8명의 학생이 원탁에 둘러앉을 때, 다음 조건을 모두 만족시키는 경우의 수는?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">(가) $A$와 $C$는 이웃하게 앉는다.<br/>(나) $B$와 $C$는 이웃하게 앉는다.<br/>(다) $B$와 $D$는 이웃하지 않게 앉는다.</div>

## Choices
① 120
② 144
③ 168
④ 192
⑤ 216

## Answer
④

## Solution
$A,C,B$를 붙어 있는 하나의 블록으로 보면(방향 2가지),
나머지 5명과 함께 총 6개 대상을 원탁에 배열하는 경우이다.
따라서 먼저
$$
2\times (6-1)!=2\times 120=240
$$
가지이다.
여기서 $B$와 $D$가 이웃한 경우를 뺀다.
$D$를 $B$ 옆에 붙인 블록으로 보면 대상 수는 5개이고,
방향 2가지를 고려하면
$$
2\times (5-1)!=2\times 24=48
$$
가지이다.
따라서 구하는 경우의 수는
$$
240-48=192
$$
이다.
