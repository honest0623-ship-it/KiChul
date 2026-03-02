---
id: JEW-2025-G1-S1-FINAL-016
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-16
assets:
- assets/original/
- assets/original/016.png
---
## Q
어느 학교의 학급 대항 퀴즈대회는 국어, 영어, 수학, 사회의 순서로 4개의 라운드로 진행된다. 학급대표 선수 $A,B,C,D,E,F,G$ (7명)을 다음 규칙에 따라 네 라운드에 배정한다.

[규칙1] 모든 선수는 적어도 한 라운드에 배정한다.
[규칙2] 한 라운드에 배정된 선수는 바로 다음 라운드에는 배정될 수 없다.
[규칙3] 국어에 2명, 영어에 4명, 수학에 2명, 사회에 3명을 배정한다.

같은 라운드에 배정되는 선수들의 순서는 고려하지 않을 때, 가능한 모든 경우의 수는?

## Choices
① 420
② 1575
③ 2730
④ 3150
⑤ 3570

## Answer
③

## Solution
라운드별 집합을 $S_1,S_2,S_3,S_4$라 두면
$$
n(S_1)=2,\quad n(S_2)=4,\quad n(S_3)=2,\quad n(S_4)=3
$$
이고,
$$
S_1\cap S_2=\varnothing,\quad S_2\cap S_3=\varnothing,\quad S_3\cap S_4=\varnothing
$$
이다.

먼저 규칙1을 무시하면
$$
{}_{7}\mathrm{C}_{2}\times{}_{5}\mathrm{C}_{4}\times{}_{3}\mathrm{C}_{2}\times{}_{5}\mathrm{C}_{3}=3150
$$
이다.

이제 한 선수가 한 번도 배정되지 않는 경우를 뺀다.
특정 선수 1명을 고정하면 경우의 수는
$$
{}_{6}\mathrm{C}_{2}\times{}_{4}\mathrm{C}_{4}\times{}_{2}\mathrm{C}_{2}\times{}_{4}\mathrm{C}_{3}=60
$$
이고, 선수는 7명이므로
$$
7\times60=420
$$
이다.

두 명 이상이 빠지는 경우는 $S_2$의 4명을 채울 수 없어 불가능하다.

따라서 전체 경우의 수는
$$
3150-420=2730
$$
이다.
