---
id: HN-2025-G2-S1-MID2-STAT-017
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
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
source: user_upload_2026-03-05
tags:
- 수동작성
- 객관식
- 출제번호-17
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
어느 양궁 선수가 10점 과녁을 맞힐 확률은 $\frac{2}{3}$이라고 한다.
이 선수가 4발을 쏘았을 때, 적어도 두 발 이상은 10점 과녁을 맞힐 확률은?

## Choices
① $\frac{7}{9}$
② $\frac{8}{9}$
③ $\frac{25}{27}$
④ $\frac{26}{27}$
⑤ $\frac{79}{81}$

## Answer
②

## Solution
$X$를 10점 과녁을 맞힌 횟수라 하면
$$
X\sim B\left(4,\frac{2}{3}\right)
$$
이다.

구하는 확률은
$$
P(X\ge 2)=1-P(X=0)-P(X=1)
$$
이다.

$$
P(X=0)=\left(\frac{1}{3}\right)^4=\frac{1}{81}
$$
$$
P(X=1)={}_{4}C_{1}\left(\frac{2}{3}\right)\left(\frac{1}{3}\right)^3=\frac{8}{81}
$$
따라서
$$
P(X\ge 2)=1-\frac{1}{81}-\frac{8}{81}=\frac{72}{81}=\frac{8}{9}
$$
이다.
