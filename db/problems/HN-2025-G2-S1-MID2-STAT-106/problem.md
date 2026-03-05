---
id: HN-2025-G2-S1-MID2-STAT-106
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 6
source_question_kind: subjective
source_question_label: 서답6번
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>2. 확률>2-2. 조건부 확률
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-2. 조건부 확률
source: user_upload_2026-03-05
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답6번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
주머니 $A$에는 흰 구슬 3개, 검은 구슬 5개가 들어 있고,
주머니 $B$에는 흰 구슬 3개, 검은 구슬 2개가 들어 있다.
임의로 주머니 한 개를 택하여 꺼낸 두 개의 구슬이 흰 구슬 1개, 검은 구슬 1개이었을 때,
그 구슬이 주머니 $A$에서 나왔을 확률은 $\frac{q}{p}$($p,q$는 서로 소인 자연수)이다.
이때 $p+q$의 값을 구하는 풀이 과정과 답을 쓰시오.
(단, 각 주머니를 선택할 확률은 같다.)

## Choices


## Answer
78

## Solution
사건을 다음과 같이 두자.

$E$: 꺼낸 2개의 구슬이 흰 1개, 검은 1개

각 주머니를 선택할 확률은 $\frac12$이다.

$$
P(E|A)=\frac{{}_{3}C_{1}\cdot {}_{5}C_{1}}{{}_{8}C_{2}}=\frac{15}{28}
$$
$$
P(E|B)=\frac{{}_{3}C_{1}\cdot {}_{2}C_{1}}{{}_{5}C_{2}}=\frac{6}{10}=\frac35
$$

베이즈 정리를 쓰면
$$
P(A|E)
=\frac{P(E|A)P(A)}{P(E|A)P(A)+P(E|B)P(B)}
=\frac{\frac{15}{28}\cdot\frac12}{\frac{15}{28}\cdot\frac12+\frac35\cdot\frac12}
=\frac{15/28}{15/28+3/5}
$$
$$
=\frac{15/28}{159/140}
=\frac{25}{53}
$$
이다.

따라서 $\frac{q}{p}=\frac{25}{53}$이므로
$$
p+q=53+25=78
$$
이다.
