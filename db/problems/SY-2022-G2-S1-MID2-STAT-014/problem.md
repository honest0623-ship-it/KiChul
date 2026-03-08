---
id: SY-2022-G2-S1-MID2-STAT-014
school: SY
year: 2022
grade: 2
semester: 1
exam: MID2
subject: STAT
type: objective
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: 2
level: 2
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-14
- 과목-STAT
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID2-STAT-014_original.png
---

## Q
하연을 포함하여 다섯 명의 학생이 전학을 와서 $A$반, $B$반, $C$반에 배정하려고 한다. 하연이 $A$반에 배정되었을 때, 나머지 네 명의 학생을 배정하는 방법의 수는? (단, 각 반에 적어도 한 명 이상 배정한다.)

## Choices
① $30$
② $35$
③ $40$
④ $45$
⑤ $50$

## Answer
⑤

## Solution
하연은 이미 $A$반에 배정되어 있다.

나머지 $4$명은 각각 $A$, $B$, $C$반 중 한 반에 배정될 수 있으므로 전체 경우의 수는
\[
3^4=81
\]
이다.

여기서 $B$반이 비는 경우는 $A$, $C$반에만 배정하는 경우이므로
\[
2^4=16
\]
가지이고, $C$반이 비는 경우도
\[
2^4=16
\]
가지이다.

두 경우를 모두 빼면 $B$반과 $C$반이 모두 비는 경우를 두 번 뺀 것이므로
\[
1
\]
가지를 다시 더해 주어야 한다.

따라서 구하는 경우의 수는
\[
81-16-16+1=50
\]
이다.
