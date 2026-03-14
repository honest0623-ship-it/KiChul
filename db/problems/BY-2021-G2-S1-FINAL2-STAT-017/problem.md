---
id: BY-2021-G2-S1-FINAL2-STAT-017
school: BY
year: 2021
grade: 2
semester: 1
exam: FINAL2
subject: STAT
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>2. 확률>2-2. 조건부 확률
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-2. 조건부 확률
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-17
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2021.G2.S1.FINAL2.STAT.q017.png
---

## Q
좌표평면 위를 움직이는 점 $P$가 있다. 주사위를 던져서 홀수의 눈이 나오면 $x$축의 양의 방향으로 1만큼 이동하고, 짝수의 눈이 나오면 $y$축의 양의 방향으로 1만큼 이동한다. 원점 $O$에서 시작하여 주사위를 8회 던졌을 때, 원점 $O$에서 $P$까지의 거리가 6 이하가 될 확률은 $\dfrac{k}{2^{7}}$이다. 자연수 $k$의 값은?

## Choices
① 70
② 91
③ 103
④ 112
⑤ 182

## Answer
②

## Solution
홀수의 눈이 나온 횟수를 $o$라 하면 짝수의 횟수는 $8-o$이고,
최종 좌표는 $(o,8-o)$이다.
거리 조건은
$$
o^{2}+(8-o)^{2}\le 36
$$
이므로 풀면 $o=3,4,5$.
따라서 경우의 수는
$$
{}_{8}C_{3}+{}_{8}C_{4}+{}_{8}C_{5}=56+70+56=182
$$
이고,
$$
P=\dfrac{182}{2^{8}}=\dfrac{91}{2^{7}}
$$
이므로 $k=91$이다.
