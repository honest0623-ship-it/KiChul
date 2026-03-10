---
id: HN-2025-G1-S1-MID-006-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
difficulty: '2'
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-6
assets:
- assets/scan.png
- assets/original/
level: 2
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
derived_from: HN-2025-G1-S1-MID-006
similarity_type: parameter_change
generation_batch_id: sim_20260309_154927
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T15:49:27'
---

## Q
다항식 $f(x)$를 $x^2+x+1$로 나누었을 때의 나머지가 $2x+1$이고, $x-1$로 나누면 나머지는 $-3$이다. $f(x)$를 $x^3-1$로 나누었을 때의 나머지를 $R(x)$라고 할 때, $R(2)$의 값은?

## Choices
① -15
② -12
③ -9
④ -6
⑤ -3

## Answer
③

## Solution
$x^3-1=(x-1)(x^2+x+1)$이므로, $f(x)$를 $x^3-1$로 나눈 나머지 $R(x)$는 $\deg R<3$이고, $x^2+x+1$로 나눈 나머지가 $2x+1$과 같아야 한다. 따라서 $R(x)=2x+1+c(x^2+x+1)$로 놓는다.
또한 나머지정리에 의해 $R(1)=f(1)=-3$이므로,
$3+3c=-3 \Rightarrow c=-2$.
따라서 $R(x)=2x+1-2(x^2+x+1)=-2x^2-1$이고,
$R(2)=-2\cdot 4-1=-9$이므로 정답은 ③이다.
