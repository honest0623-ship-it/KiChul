---
id: HN-2025-G1-S1-MID-012-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-12
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
derived_from: HN-2025-G1-S1-MID-012
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:31:33'
---

## Q
복소수 $z=\dfrac{1+i}{1-i}$에 대하여 $z+z^2+z^3+\dots+z^{99}$의 값은?

## Choices
① 0
② 1
③ -1
④ i
⑤ -i

## Answer
③ -1

## Solution
먼저 복소수 $z$를 간단히 계산합니다.
$z=\dfrac{1+i}{1-i}=\dfrac{(1+i)(1+i)}{(1-i)(1+i)}=\dfrac{1+2i+i^2}{1-i^2}=\dfrac{1+2i-1}{1+1}=\dfrac{2i}{2}=i$.
따라서 $z=i$이고, $i$의 거듭제곱은 주기 4를 가집니다: $i, -1, -i, 1, \dots$.
한 주기(4개 항)의 합은 $i+(-1)+(-i)+1=0$입니다.
구하는 합은 99항이므로 $99=4\times24+3$ 이고 처음 96항(=24주기)은 0이므로 남는 항은 마지막 3개뿐입니다.
$z^{97}+z^{98}+z^{99}=i^{97}+i^{98}+i^{99}=i^{1}+i^{2}+i^{3}=i+(-1)+(-i)=-1$.
따라서 답은 $-1$이며 정답은 ③입니다.
