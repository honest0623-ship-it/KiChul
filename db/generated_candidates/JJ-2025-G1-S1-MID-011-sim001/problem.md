---
id: JJ-2025-G1-S1-MID-011-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 11
source_question_kind: objective
source_question_label: '11'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-05
tags:
- 수동작성
- 객관식
- 출제번호-11
- 과목-COM1
assets:
- assets/original/
- assets/original/JJ.2025.G1.S1.MID.COM1.pdf
derived_from: JJ-2025-G1-S1-MID-011
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:38:02'
---

## Q
이차방정식 $x^2+4x-5=0$의 두 근을 $\alpha,\beta$라고 할 때, 두 수 $\dfrac{\alpha}{1+\alpha}$, $\dfrac{\beta}{1+\beta}$를 두 근으로 하고 $x^2$의 계수가 8인 이차방정식을 구하면?

## Choices
① $8x^{2}-14x+5=0$
② $8x^{2}-14x-5=0$
③ $8x^{2}+14x+5=0$
④ $4x^{2}-7x+5=0$
⑤ $2x^{2}-7x+5=0$

## Answer
①

## Solution
주어진 이차방정식의 두 근에 대해
$\alpha+\beta=-4,\quad \alpha\beta=-5$.
새 근을
$u=\dfrac{\alpha}{1+\alpha},\quad v=\dfrac{\beta}{1+\beta}$라 하면

$u+v=\dfrac{\alpha(1+\beta)+\beta(1+\alpha)}{(1+\alpha)(1+\beta)}
=\dfrac{(\alpha+\beta)+2\alpha\beta}{1+(\alpha+\beta)+\alpha\beta}
=\dfrac{-4+2(-5)}{1-4-5}=\dfrac{-14}{-8}=\dfrac{7}{4},$

$uv=\dfrac{\alpha\beta}{(1+\alpha)(1+\beta)}=\dfrac{-5}{1-4-5}=\dfrac{5}{8}.$

따라서 단수(단계수)가 1인 이차방정식은
$x^{2}-\dfrac{7}{4}x+\dfrac{5}{8}=0$이고, $x^{2}$의 계수를 8로 맞추면
$8x^{2}-14x+5=0$이다. 따라서 정답은 ①.
