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
- assets/scan.png
- assets/original/
- assets/original/016.png
---

## Q
어느 학교의 학급 대항 퀴즈대회는 국어, 영어, 수학, 사회의 순서로 4개의 라운드로 경기가 진행된다.
다음은 학급대표 선수를 네 라운드에 배정하는 규칙이다.

[규칙1] 모든 선수를 적어도 한 라운드에 배정한다.
[규칙2] 한 라운드에 배정된 선수는 바로 다음 라운드에는 배정될 수 없다.
[규칙3] 국어에 2명, 영어에 4명, 수학에 2명, 사회에 3명을 배정한다.

학급대표 선수 \(A,B,C,D,E,F,G\) 7명을 이 규칙에 따라 네 라운드에 배정하는 모든 경우의 수는?
(단, 같은 라운드에 배정되는 선수들의 순서는 고려하지 않는다.)

## Choices
① 420
② 1575
③ 2730
④ 3150
⑤ 3570
## Answer
3

## Solution
A player can appear only in one of these non-consecutive round patterns:
\[
K,\ E,\ M,\ S,\ KM,\ KS,\ ES
\]
(where \(K\)=Korean, \(E\)=English, \(M\)=Math, \(S\)=Social Studies).
Let their counts be \(x_1,\dots,x_7\). Then the round-size conditions become
\[
\begin{aligned}
x_1+x_5+x_6&=2,\\
x_2+x_7&=4,\\
x_3+x_5&=2,\\
x_4+x_6+x_7&=3,\\
x_1+x_2+x_3+x_4+x_5+x_6+x_7&=7.
\end{aligned}
\]
The nonnegative integer solutions are exactly
\[
(0,2,0,1,2,0,2),\ (0,2,1,0,1,1,2),\ (1,1,1,0,1,0,3).
\]
Their counts are
\[
\frac{7!}{2!1!2!2!}=630,
\qquad
\frac{7!}{2!1!1!1!2!}=1260,
\qquad
\frac{7!}{1!1!1!1!3!}=840.
\]
So the total is
\[
630+1260+840=2730.
\]
Therefore the correct choice is 3.
