---
id: BY-2020-G2-S1-MID2-018
school: BY
year: 2020
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
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-18
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q018.original.png
---

## Q
빨간 공, 파란 공, 노란 공은 각각 2개씩 들어 있고 흰 공 1개 들어 있는 상자에서 차례로 7개의 공을 꺼내 일렬로 배열할 때, 빨간 공과 흰 공은 홀수 번째에만 올 수 있고 파란 공과 노란 공은 같은 색이 연속으로 배열되지 않도록 배열하는 경우의 수는? (단, 같은 색의 공은 서로 구분하지 않고, 꺼낸 공은 다시 넣지 않는다.)

## Choices
① 18
② 24
③ 30
④ 36
⑤ 42

## Answer
④

## Solution
홀수 위치는 4칸(1,3,5,7)이다.
빨간 공 2개와 흰 공 1개는 이 4칸에만 놓인다.

홀수 4칸 중에서 B 또는 Y가 들어갈 칸을 $X$라 하자.
그럼 나머지 홀수 3칸에는 R,R,W를 놓아야 하므로,
$X$가 정해졌을 때 R,R,W 배치는
$$
3
$$
가지이다.

이제 $X$의 위치에 따라 B,B,Y,Y 배치를 센다.

- $X=1$ 또는 $X=7$ (양 끝 홀수칸)인 경우:
인접 제약은 1개만 생긴다.
B,B,Y,Y를 4칸에 놓는 경우는
$$
\frac{4!}{2!2!}=6
$$
가지이고,
인접한 두 칸이 같은 색인 2가지를 빼면 4가지.

- $X=3$ 또는 $X=5$ (가운데 홀수칸)인 경우:
인접 제약이 2개 생긴다.
$X$의 색이 B이면 양옆은 Y로 고정,
$X$의 색이 Y이면 양옆은 B로 고정이므로
각 경우 2가지.

따라서 전체 경우의 수는
$$
(2\times 3\times 4)+(2\times 3\times 2)=24+12=36
$$
이다.
