---
id: HN-2025-G1-S1-MID-101-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 단답형
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1번
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
- 단답형
- 출제번호-서답1번
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-101
similarity_type: parameter_change
generation_batch_id: sim_20260309_140840
generation_model: openai:gpt-5.2-pro
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T14:43:10'
---

## Q
다항식 $f(x)=-x^3+5x^2+2x-7$을 일차식 $x+2$로 나누었을 때의 나머지를 구하시오.

## Choices
(선택지 없음)

## Answer
17

## Solution
나머지정리에 의해 $f(x)$를 $x-a$로 나눌 때의 나머지는 $f(a)$이다.

여기서 $x+2=x-(-2)$이므로 $a=-2$.
\[
\begin{aligned}
\text{나머지} &= f(-2)\\
&= -(-2)^3 + 5(-2)^2 + 2(-2) - 7\\
&= -(-8) + 5\cdot 4 - 4 - 7\\
&= 8 + 20 - 4 - 7 = 17
\end{aligned}
\]
따라서 나머지는 $17$이다.
