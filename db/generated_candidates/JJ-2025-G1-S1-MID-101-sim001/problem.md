---
id: JJ-2025-G1-S1-MID-101-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '4'
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-1
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답1번.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
derived_from: JJ-2025-G1-S1-MID-101
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:41:33'
---

## Q
다항식 \(x^{2019}+3x+2\)를 \(x^2-1\)으로 나누었을 때의 몫을 \(Q(x)\)라 할 때, \(Q(x)\)의 상수를 포함한 모든 계수의 합을 구하시오.

## Choices


## Answer
1009

## Solution
나머지를 \(R(x)=ax+b\)라 두면
\(R(1)=1^{2019}+3\cdot1+2=6,\quad R(-1)=(-1)^{2019}+3(-1)+2=-2\)
이므로
\(a+b=6,\; -a+b=-2\)에서 \(b=2,\; a=4\)이고 \(R(x)=4x+2\)이다.
따라서 몫은
\[Q(x)=\frac{x^{2019}+3x+2-(4x+2)}{x^2-1}=\frac{x^{2019}-x}{x^2-1}.
\]
여기서
\(x^{2019}-x=x(x^{2018}-1)=x\bigl((x^2)^{1009}-1\bigr)=x(x^2-1)(1+x^2+x^4+\cdots+x^{2016})\)이므로
\[Q(x)=x(1+x^2+x^4+\cdots+x^{2016}).\]
계수의 합은 \(Q(1)\)이므로
\[Q(1)=1\cdot(1+1+\cdots+1)=1009.\]
따라서 답은 \(1009\)이다.
