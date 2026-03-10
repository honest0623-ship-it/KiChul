---
id: HN-2025-G1-S1-MID-014-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: '2'
level: 2
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-14
assets:
- assets/original/
- assets/original/014.png
derived_from: HN-2025-G1-S1-MID-014
similarity_type: parameter_change
generation_batch_id: sim_20260309_140840
generation_model: openai:gpt-5.2-pro
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T14:34:30'
---

## Q
$x^3$의 계수가 1인 삼차식 $P(x)$에 대하여
$$
P(1)=5,\quad P(2)=7,\quad P(4)=11
$$
일 때, $P(x)$를 $x-3$으로 나누었을 때의 나머지를 $R$이라 하자. $R$의 값은?

## Choices
① 3
② 5
③ 7
④ 9
⑤ 11

## Answer
③

## Solution
$P(1)=5,\,P(2)=7,\,P(4)=11$이므로 이를 만족하는 일차식은 $2x+3$이다.

$Q(x)=P(x)-(2x+3)$이라 두면
$$
Q(1)=Q(2)=Q(4)=0
$$
이고 $P(x)$의 최고차항 계수가 1이므로 $Q(x)$도 최고차항 계수가 1인 삼차식이다. 따라서
$$
Q(x)=(x-1)(x-2)(x-4)
$$
이므로
$$
P(x)=(x-1)(x-2)(x-4)+2x+3.
$$
나머지정리에 의해 $R=P(3)$이므로
$$
R=(3-1)(3-2)(3-4)+2\cdot3+3=2\cdot1\cdot(-1)+9=-2+9=7.
$$
따라서 $R=7$이다.
