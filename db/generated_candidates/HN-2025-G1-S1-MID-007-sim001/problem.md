---
id: HN-2025-G1-S1-MID-007-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: '7'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-1. 다항식의 연산
source: manual_agent_2026-03-10
tags:
- 수동생성
- AI
- 객관식
- 출제번호-7
- 과목-COM1
derived_from: HN-2025-G1-S1-MID-007
similarity_type: parameter_change
generation_batch_id: sim_20260310_120048
generation_model: openai:gpt-5-mini
review_status: approved
review_note: ''
promoted_to: ''
generated_at: '2026-03-10T13:35:00'
reviewed_at: '2026-03-10T12:15:34'
---

## Q
다음은 조립제법을 이용하여 다항식 $x^3+ax^2-3x+b$를 $x-2$로 나누었을 때의 계산 과정이다. $a\sim e$의 값으로 옳지 않은 것은?

$$
\begin{array}{r|rrrr}
2e & 1 & a & -3 & b \\
   &   & c & d & 14 \\
\hline
   & 1 & 5 & 7 & 4
\end{array}
$$

## Choices
① $a=3$
② $b=-10$
③ $c=3$
④ $d=10$
⑤ $e=1$

## Answer
③

## Solution
나누는 식이 $x-2$이므로 조립제법의 수는 $2$이다. 따라서 $2e=2$에서 $e=1$이다.

표를 따라 계산하면

1. 첫 계수 $1$을 내려서 다음 칸의 곱은 $c=1\times2=2$.
2. 둘째 열 합이 $5$이므로 $a+c=5 \Rightarrow a+2=5 \Rightarrow a=3$.
3. 다음 곱은 $d=5\times2=10$.
4. 셋째 열 합이 $7$인지 확인하면 $-3+d=-3+10=7$로 맞다.
5. 마지막 곱은 $7\times2=14$이고, 나머지가 $4$이므로 $b+14=4 \Rightarrow b=-10$.

따라서 실제 값은 $a=3,\ b=-10,\ c=2,\ d=10,\ e=1$이므로 옳지 않은 것은 **③ $c=3$**이다.
