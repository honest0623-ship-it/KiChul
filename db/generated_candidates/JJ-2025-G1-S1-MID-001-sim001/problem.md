---
id: JJ-2025-G1-S1-MID-001-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 1
source_question_kind: objective
source_question_label: '1'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-1. 다항식의 연산
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-1
- 과목-COM1
assets:
- assets/original/
- assets/original/JJ.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: JJ-2025-G1-S1-MID-001
similarity_type: parameter_change
generation_batch_id: sim_20260309_155400
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T15:54:00'
---

## Q
두 다항식 $A, B$에 대하여 $A+B = 5x^2 + 2x - 4$ 이고 $A-2B = 2x^2 - 7x + 8$ 일 때, 다항식 $A = ax^2+bx+c$ 에 대하여 $a+b+c$ 의 값을 구하시오.

## Choices
① -1
② 0
③ 2
④ 3
⑤ 4

## Answer
3

## Solution
주어진 식은 다음과 같습니다.
(1) $A+B = 5x^2 + 2x - 4$
(2) $A-2B = 2x^2 - 7x + 8$
(1)−(2)를 계산하면 $3B$를 구할 수 있습니다.
$(A+B)-(A-2B)= (5x^2+2x-4) - (2x^2-7x+8) = 3x^2 + 9x - 12$
따라서 $3B = 3x^2 + 9x - 12$ 이므로 $B = x^2 + 3x - 4$.
이를 (1)에 대입하여 $A$를 구하면,
$A = (A+B) - B = (5x^2 + 2x - 4) - (x^2 + 3x - 4) = 4x^2 - x$.
즉, $A = 4x^2 - x + 0$ 이므로 $a=4, b=-1, c=0$이고, $a+b+c = 4+(-1)+0 = 3$.
