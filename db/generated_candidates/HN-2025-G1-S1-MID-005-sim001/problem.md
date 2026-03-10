---
id: HN-2025-G1-S1-MID-005-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 5
source_question_kind: objective
source_question_label: '5'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-5
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-005
similarity_type: parameter_change
generation_batch_id: sim_20260309_140840
generation_model: openai:gpt-5.2-pro
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T14:14:19'
---

## Q
다항식 $f(x)$를 $x-1$로 나누었을 때의 나머지는 $4$이고, $x+2$로 나누었을 때의 나머지는 $-2$이다. $f(x)$를 $x^2+x-2$로 나누었을 때의 나머지를 $R(x)$라 할 때, $R(0)$의 값은?

## Choices
① $-2$
② $0$
③ $2$
④ $4$
⑤ $6$

## Answer
③

## Solution
나머지정리에 의해 $f(1)=4$, $f(-2)=-2$이다.

$x^2+x-2=(x-1)(x+2)$이므로 $f(x)$를 $x^2+x-2$로 나눌 때의 나머지 $R(x)$는 일차식이라 두고
$$R(x)=ax+b$$
라 하자. 그러면 $f(1)=R(1)$, $f(-2)=R(-2)$이므로
$$a+b=4 \quad (1)$$
$$-2a+b=-2 \quad (2)$$
(1)−(2)에서 $3a=6$이므로 $a=2$, 이를 (1)에 대입하면 $b=2$.
따라서 $R(x)=2x+2$이고,
$$R(0)=2.$$
그러므로 정답은 $2$이다.
