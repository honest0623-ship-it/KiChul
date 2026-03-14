---
id: BY-2021-G2-S1-FINAL2-STAT-008
school: BY
year: 2021
grade: 2
semester: 1
exam: FINAL2
subject: STAT
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: '8'
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
- 출제번호-8
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2021.G2.S1.FINAL2.STAT.q008.png
---

## Q
주머니 $A$에는 노란 공 2개, 빨간 공 4개가 들어 있고, 주머니 $B$에는 노란 공 4개, 빨간 공 1개가 들어 있다. 두 주머니 $A$, $B$ 중에서 한 주머니를 임의로 택하여 2개의 공을 임의로 꺼냈더니 노란 공 1개, 빨간 공 1개가 나왔을 때, 꺼낸 공 2개가 주머니 $B$에서 나왔을 확률은?

## Choices
① $\dfrac{1}{7}$
② $\dfrac{3}{7}$
③ $\dfrac{5}{17}$
④ $\dfrac{7}{17}$
⑤ $\dfrac{9}{23}$

## Answer
②

## Solution
사건 $E$를 "노란 공 1개, 빨간 공 1개가 나온다"로 두면
$$
P(E\mid A)=\dfrac{{}_{2}C_{1}{}_{4}C_{1}}{{}_{6}C_{2}}=\dfrac{8}{15},
\quad
P(E\mid B)=\dfrac{{}_{4}C_{1}{}_{1}C_{1}}{{}_{5}C_{2}}=\dfrac{2}{5}
$$
이다. 또 $P(A)=P(B)=\dfrac{1}{2}$이므로
$$
P(B\mid E)
=\dfrac{P(E\mid B)P(B)}{P(E\mid A)P(A)+P(E\mid B)P(B)}
=\dfrac{\frac{2}{5}}{\frac{8}{15}+\frac{2}{5}}
=\dfrac{3}{7}
$$
이다.
