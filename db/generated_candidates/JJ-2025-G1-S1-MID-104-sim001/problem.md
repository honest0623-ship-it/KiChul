---
id: JJ-2025-G1-S1-MID-104-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '3'
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-4
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답4번.png
level: 3
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
derived_from: JJ-2025-G1-S1-MID-104
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:45:07'
---

## Q
다음은 나머지정리에 관한 문제이다.
다항식 $P(x)$를 $x^2-9$로 나누었을 때의 나머지가 $x+5$이고, $x^2-4$로 나누었을 때의 나머지가 $2x-3$이다. $P(x)$를 $x^2 - x - 6$으로 나누었을 때의 나머지를 구하시오.

## Choices


## Answer
$3x-1$

## Solution
$x^2 - x - 6=(x-3)(x+2)$이므로 나머지를 $R(x)=ax+b$라 두면 $R(3)=P(3)$, $R(-2)=P(-2)$이다.
- $P(x)$를 $x^2-9$로 나눌 때 나머지가 $x+5$이므로 $P(3)=3+5=8$.
- $P(x)$를 $x^2-4$로 나눌 때 나머지가 $2x-3$이므로 $P(-2)=2(-2)-3=-7$.
따라서 $3a+b=8$, $-2a+b=-7$. 연립하면 $5a=15 \Rightarrow a=3$, $b=8-3\cdot3=-1$.
따라서 나머지는 $R(x)=3x-1$이다.
