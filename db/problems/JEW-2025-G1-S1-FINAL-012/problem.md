---
id: JEW-2025-G1-S1-FINAL-012
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-12
assets:
- assets/scan.png
- assets/original/
- assets/original/012.png
subject: COM1
---

## Q
다음 그림과 같이 1학년 3명과 2학년 3명이 자리에 앉아 공부를 하려고 한다.
1학년 1명과 2학년 1명이 짝을 지어 2명씩 같이 앉을 때, 6명이 모두 자리에 앉는 경우의 수를 구하면?
(단, 남은 자리는 비워둔다.)

<img src="assets/scan.png" alt="문항 도형" style="width:100% !important; max-width:100% !important; height:auto;" />

## Choices
① 192
② 384
③ 576
④ 1152
⑤ 2304
## Answer
4

## Solution
Match 3 first-year students with 3 second-year students:
\[
3! = 6
\]
ways.
Arrange the 3 pairs into 3 of the 4 two-seat blocks:
\[
{}_4P_3 = 4\times3\times2 = 24
\]
ways.
Each pair can switch left/right seats:
\[
2^3 = 8.
\]
Hence the total number of seatings is
\[
6\times24\times8 = 1152.
\]
So the correct choice is 4.
