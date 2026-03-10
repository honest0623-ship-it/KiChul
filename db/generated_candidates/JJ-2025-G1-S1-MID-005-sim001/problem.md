---
id: JJ-2025-G1-S1-MID-005-sim002
school: JJ
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
- 객관식
- 출제번호-5
- 과목-COM1
assets:
- assets/original/
- assets/original/JJ.2025.G1.S1.MID.COM1.pdf
derived_from: JJ-2025-G1-S1-MID-005
similarity_type: parameter_change
generation_batch_id: sim_20260309_180131
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:01:31'
---

## Q
다항식 $2x^3+x^2-x+1$을 $2x-1$로 나누었을 때의 몫을 $Q(x)$, 나머지를 $R$이라 하자. 이때 $Q(1)-R$의 값은?

## Choices
① 1
② 0
③ 2
④ -1
⑤ 3

## Answer
①

## Solution
다항식 $f(x)=2x^3+x^2-x+1$에 대해 나머지정리에 의해 $2x-1$로 나눈 나머지 $R$는 $x=\tfrac{1}{2}$에서의 값이다. 즉
$$R=f\left(\tfrac{1}{2}\right).$$
또한
$$f(x)=(2x-1)Q(x)+R$$
이므로 $x=1$를 대입하면
$$f(1)=(2\cdot1-1)Q(1)+R=Q(1)+R$$
이고 따라서
$$Q(1)-R=f(1)-2R=f(1)-2f\left(\tfrac{1}{2}\right).$$
이제 값을 계산하면
$$f(1)=2+1-1+1=3,$$
$$f\left(\tfrac{1}{2}\right)=2\left(\tfrac{1}{8}\right)+\tfrac{1}{4}-\tfrac{1}{2}+1=1.$$
따라서
$$Q(1)-R=3-2\cdot1=1.$$
