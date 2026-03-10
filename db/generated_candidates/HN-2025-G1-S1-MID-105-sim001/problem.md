---
id: HN-2025-G1-S1-MID-105-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5
difficulty: '5'
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-02-27
tags:
- 서답형-서술형
- 출제번호-5
assets:
- assets/original/
- assets/original/서답5번.png
derived_from: HN-2025-G1-S1-MID-105
similarity_type: parameter_change
generation_batch_id: sim_20260309_140840
generation_model: openai:gpt-5.2-pro
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T14:49:22'
---

## Q
$x$에 대한 이차방정식
$$
x^2-2(k+a)x+k^2+6k-b+5=0
$$
이 실수 $k$의 값에 관계없이 항상 중근을 가질 때, $a^2+b^2$의 값을 구하시오. (단, $a,\ b$는 실수이다.)

## Choices
(선택지 없음)

## Answer
25

## Solution
이차방정식이 중근을 가지려면 판별식 $D=0$이어야 한다.

계수 $A=1$, $B=-2(k+a)$, $C=k^2+6k-b+5$ 이므로
$$\frac{D}{4}=(k+a)^2-(k^2+6k-b+5).$$
정리하면
$$\frac{D}{4}=\bigl(k^2+2ak+a^2\bigr)-k^2-6k+b-5=(2a-6)k+(a^2+b-5).$$
모든 실수 $k$에 대하여 항상 중근이므로 $D\equiv0$, 즉
$$2a-6=0,\quad a^2+b-5=0.$$
따라서
$$a=3,\quad 9+b-5=0\Rightarrow b=-4.$$
그러므로
$$a^2+b^2=3^2+(-4)^2=9+16=25.$$
정답은 $25$이다.
