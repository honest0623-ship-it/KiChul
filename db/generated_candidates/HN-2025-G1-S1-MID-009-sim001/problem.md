---
id: HN-2025-G1-S1-MID-009-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: '9'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-3. 인수분해
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-3. 인수분해
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-9
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-009
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:30:02'
---

## Q
다항식 $x^4+3x^3-4x^2-10x-4$를 인수분해하면 $(x-2)(x+1)(x^2+ax+b)$이다. 이때 상수 $a+b$의 값은?

## Choices
① $1$ 
② $-2$ 
③ $6$ 
④ $0$ 
⑤ $8$

## Answer
6

## Solution
먼저 $(x-2)(x+1)=x^2-x-2$이므로
$$x^4+3x^3-4x^2-10x-4=(x^2-x-2)(x^2+ax+b).$$
우변을 전개하면
$(x^2-x-2)(x^2+ax+b)=x^4+(a-1)x^3+(b-a-2)x^2+(-b-2a)x-2b.$
계수 비교로
1) $x^3$의 계수: $a-1=3\Rightarrow a=4$
2) $x^2$의 계수: $b-a-2=-4\Rightarrow b-4-2=-4\Rightarrow b=2$
따라서 $a+b=4+2=6$.
(확인: $x$의 계수 $-b-2a=-2-8=-10$, 상수항 $-2b=-4$로 일치함.)
