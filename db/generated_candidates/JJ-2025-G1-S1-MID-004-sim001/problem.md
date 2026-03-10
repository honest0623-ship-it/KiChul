---
id: JJ-2025-G1-S1-MID-004-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 4
source_question_kind: objective
source_question_label: '4'
difficulty: 2
level: 2
unit: 공통수학1(2022개정)>1. 다항식>1-3. 인수분해
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-3. 인수분해
source: user_upload_2026-03-05
tags:
- 수동작성
- 객관식
- 출제번호-4
- 과목-COM1
assets:
- assets/original/
- assets/original/JJ.2025.G1.S1.MID.COM1.pdf
derived_from: JJ-2025-G1-S1-MID-004
similarity_type: parameter_change
generation_batch_id: sim_20260309_155400
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T15:55:26'
---

## Q
다항식 $x^3+(1-a)x^2-(a+6)x+6a$가 서로 다른 세 일차식의 곱으로 인수분해될 때, 다음 중 상수 $a$의 값이 될 수 없는 것은?

## Choices
① 1
② 2
③ 3
④ 4
⑤ 5

## Answer
②

## Solution
먼저 $x=2$를 대입하면
$$
2^3+(1-a)2^2-(a+6)2+6a=8+4-4a-2a-12+6a=0
$$
이므로 $(x-2)$는 인수이다. 따라서
$$
x^3+(1-a)x^2-(a+6)x+6a=(x-2)(x^2+(3-a)x-3a).
$$
이차식은
$$
x^2+(3-a)x-3a=(x-a)(x+3)
$$
이므로 전체 인수분해는
$$
(x-2)(x-a)(x+3)
$$
가 된다. 서로 다른 세 일차식이 되려면 $a\neq2$이고 $a\neq-3$이어야 한다. 선택지(①~⑤) 중 불가능한 값은 $a=2$이므로 정답은 ②이다.
