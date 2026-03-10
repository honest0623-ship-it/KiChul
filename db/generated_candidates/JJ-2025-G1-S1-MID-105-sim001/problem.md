---
id: JJ-2025-G1-S1-MID-105-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5번
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-05
tags:
- 수동작성
- 서술형
- 출제번호-서답5번
- 과목-COM1
assets:
- assets/original/
- assets/original/JJ.2025.G1.S1.MID.COM1.pdf
derived_from: JJ-2025-G1-S1-MID-105
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:45:40'
---

## Q
이차방정식 $x^2-abx+a+b=0$의 한 근이 $2+3i$일 때, 실수 $a,b$에 대하여 $a^3-b^3$의 값을 구하시오. (단, $a>b$이다.)

## Choices


## Answer
$495\sqrt{17}$

## Solution
계수가 실수이므로 다른 한 근은 공액인 $2-3i$이다. 근과 계수의 관계에서

- 근의 합: $(2+3i)+(2-3i)=4=ab$,
- 근의 곱: $(2+3i)(2-3i)=4+9=13=a+b$.

따라서 $a,b$는 방정식
\[t^2-(a+b)t+ab=t^2-13t+4=0\]
의 두 근이며,
\[a,b=\frac{13\pm\sqrt{169-16}}{2}=\frac{13\pm\sqrt{153}}{2}=\frac{13\pm3\sqrt{17}}{2}\quad(a>b).\]

이로부터
\[a-b=3\sqrt{17},\qquad a^2+ab+b^2=(a+b)^2-ab=169-4=165.\]
따라서
\[a^3-b^3=(a-b)(a^2+ab+b^2)=3\sqrt{17}\times165=495\sqrt{17}.\]
결론: $495\sqrt{17}$.
