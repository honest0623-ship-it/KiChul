---
id: HN-2025-G1-S1-MID-003-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 3
source_question_kind: objective
source_question_label: '3'
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
- 출제번호-3
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-003
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:26:21'
---

## Q
다항식 $3x^2+2x-3=0$ 일 때, 다음 식의 값은?

$\displaystyle 9x^2+3x+1-\frac{3}{x}+\frac{9}{x^2}$

## Choices
① 17
② 19
③ 21
④ 23
⑤ 25

## Answer
③

## Solution
주어진 식 $3x^2+2x-3=0$ 에서 양변을 $x$로 나누면(단, $x\neq0$),

$3x+2-\dfrac{3}{x}=0$ 
$\Rightarrow 3\left(x-\dfrac{1}{x}\right)=-2$ 
$\Rightarrow x-\dfrac{1}{x}=-\dfrac{2}{3}$.

이에 따라

$x^2+\dfrac{1}{x^2}=\left(x-\dfrac{1}{x}\right)^2+2=\left(-\dfrac{2}{3}\right)^2+2=\dfrac{4}{9}+2=\dfrac{22}{9}$.

구하고자 하는 식을 정리하면

$9x^2+3x+1-\dfrac{3}{x}+\dfrac{9}{x^2}=9\left(x^2+\dfrac{1}{x^2}\right)+3\left(x-\dfrac{1}{x}\right)+1$.

여기에 위 값을 대입하면

$9\cdot\dfrac{22}{9}+3\cdot\left(-\dfrac{2}{3}\right)+1=22-2+1=21$.

따라서 정답은 21로, 선택지는 ③ 이다.
