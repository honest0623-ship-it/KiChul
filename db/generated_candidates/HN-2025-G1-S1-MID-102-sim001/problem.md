---
id: HN-2025-G1-S1-MID-102-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-02-27
tags:
- 서답형-단답형
- 출제번호-2
assets:
- assets/original/
- assets/original/서답2번.png
derived_from: HN-2025-G1-S1-MID-102
similarity_type: parameter_change
generation_batch_id: sim_20260310_103350
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-10T10:37:42'
---

## Q
삼차방정식 \(x^3-ax^2+bx-2a=0\)의 한 허근이 \(1+2i\)이고, 실근을 \(k\)라 할 때 \(a,b\)는 실수이다. \(a+b+k\)의 값을 구하시오.

## Choices


## Answer
\(\dfrac{37}{3}\)

## Solution
계수가 실수이므로 켤레복소수 \(1-2i\)도 근이다. 세 근을 \(1+2i,\ 1-2i,\ k\)라 하면

1) 근의 합에서
\[
a=(1+2i)+(1-2i)+k=2+k.\]

2) 근의 곱에서(단항식의 상수항이 \(-2a\)이므로 근의 곱은 \(-\!\)(상수항) = 2a)
\[
(1+2i)(1-2i)\,k=(1^2+2^2)k=5k=2a \Rightarrow a=\frac{5}{2}k.
\]

(1)과 (2)를 연립하면
\[
2+k=\frac{5}{2}k \Rightarrow 2=\frac{3}{2}k \Rightarrow k=\frac{4}{3}.
\]
따라서
\[
a=2+\frac{4}{3}=\frac{10}{3}.
\]

3) \(b\)는 두 근씩 곱의 합이므로
\[
b=(1+2i)(1-2i)+k\big((1+2i)+(1-2i)\big)=5+2k=5+\frac{8}{3}=\frac{23}{3}.
\]

따라서
\[
a+b+k=\frac{10}{3}+\frac{23}{3}+\frac{4}{3}=\frac{37}{3}.
\]
결론: \(a+b+k=\dfrac{37}{3}\).
