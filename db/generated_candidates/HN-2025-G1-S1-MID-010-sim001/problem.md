---
id: HN-2025-G1-S1-MID-010-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: '10'
difficulty: 2
level: 2
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
- 출제번호-10
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-010
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:30:25'
reviewed_at: '2026-03-09T23:38:09'
---

## Q
다항식 $P(x)=x^4-5x-6$가 $(x-2)(x+1)(x^2+ax+b)$로 인수분해된다. 이때 상수 $a+b$의 값은?

## Choices
① -2
② -1
③ 0
④ 2
⑤ 4

## Answer
4

## Solution
(x-2)(x+1)=x^2-x-2 이므로
\[P(x)=(x^2-x-2)(x^2+ax+b)=x^4+(a-1)x^3+(b-a-2)x^2+(-b-2a)x-2b.\]
주어진 다항식과 계수를 비교하면
\[a-1=0,\quad b-a-2=0,\quad -b-2a=-5,\quad -2b=-6.\]
첫 식에서 $a=1$이고, 넷째 식에서 $b=3$이다. 두 값을 확인하면 세 번째 식도 성립한다. 따라서
\[a+b=1+3=4.\]
정답: 4 (⑤)
