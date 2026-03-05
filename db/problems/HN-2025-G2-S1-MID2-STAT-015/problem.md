---
id: HN-2025-G2-S1-MID2-STAT-015
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
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
- 출제번호-15
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
어느 거짓말 탐지기는 참말을 '참'으로 판단할 확률이 0.9이고
거짓말을 '거짓'으로 판단할 확률이 0.95라고 한다.
거짓말을 할 확률이 0.9인 어떤 용의자의 답변을 거짓말 탐지기로 판단한 결과 중에서
임의로 택한 결과가 '참'이었을 때,
그 답변이 실제로 참이었을 확률은?

## Choices
① $\frac{1}{3}$
② $\frac{1}{2}$
③ $\frac{2}{3}$
④ $\frac{4}{5}$
⑤ $\frac{9}{10}$

## Answer
③

## Solution
사건을 다음과 같이 두자.

$T$: 실제로 참말, $L$: 실제로 거짓말, $R$: 탐지 결과가 '참'

문제에서
$$
P(T)=0.1,\quad P(L)=0.9,
$$
$$
P(R|T)=0.9,\quad P(R|L)=1-0.95=0.05
$$
이다.

베이즈 정리를 적용하면
$$
P(T|R)=\frac{P(R|T)P(T)}{P(R|T)P(T)+P(R|L)P(L)}
=\frac{0.9\cdot 0.1}{0.9\cdot 0.1+0.05\cdot 0.9}
=\frac{0.09}{0.135}
=\frac{2}{3}
$$
이다.
