---
id: HN-2025-G1-S1-MID-104-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-02-27
tags:
- 서답형-서술형
- 출제번호-4
assets:
- assets/original/
- assets/original/서답4번.png
derived_from: HN-2025-G1-S1-MID-104
similarity_type: parameter_change
generation_batch_id: sim_20260309_140840
generation_model: openai:gpt-5.2-pro
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T14:48:04'
---

## Q
이차방정식 $x^2-ax+b=0$에서 $a$를 잘못 보고 풀었더니 두 근이 $2+4i,\ 2-4i$가 되었고, $b$를 잘못 보고 풀었더니 두 근이 $2,\ 6$이 되었다. 처음 이차방정식의 근을 구하는 풀이 과정과 답을 쓰시오. (단, $a,\ b$는 실수이다.)

## Choices
(선택지 없음)

## Answer
$4+2i,\ 4-2i$

## Solution
$a$를 잘못 본 경우에는 $b$는 원래 값이므로
\[
b=(2+4i)(2-4i)=2^2+4^2=20.
\]

$b$를 잘못 본 경우에는 $a$는 원래 값이고, 두 근이 $2,6$이므로
\[
a=2+6=8.
\]

따라서 원래 방정식은
\[
x^2-8x+20=0.
\]
근의 공식을 이용하면
\[
x=\frac{8\pm\sqrt{64-80}}{2}=\frac{8\pm\sqrt{-16}}{2}=\frac{8\pm4i}{2}=4\pm2i.
\]
따라서 처음 이차방정식의 근은 $4+2i,\ 4-2i$이다.
