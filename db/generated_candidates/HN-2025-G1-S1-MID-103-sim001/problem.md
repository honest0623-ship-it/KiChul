---
id: HN-2025-G1-S1-MID-103-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-02-27
tags:
- 서답형-단답형
- 출제번호-3
assets:
- assets/original/
- assets/original/서답3번.png
derived_from: HN-2025-G1-S1-MID-103
similarity_type: parameter_change
generation_batch_id: sim_20260310_103350
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-10T10:39:14'
---

## Q
실수 \(a\)에 대하여 최고차항의 계수가 정수인 이차함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(a+4)\)의 값을 구하시오.

(가) 방정식 \(f(x)=0\)의 두 근은 \(a,\ a+6\)이다.

(나) \(a+1\le x\le a+5\)일 때, 함수 \(f(x)\)의 최댓값은 \(9\)이다.

## Choices


## Answer
8

## Solution
조건 (가)에서
\[
f(x)=n(x-a)(x-a-6)\quad(n\in\mathbb{Z}).
\]
두 근의 중점인 꼭짓점의 x좌표는 \(x=a+3\)이고, 구간 \([a+1,a+5]\) 안에 있다. 최댓값이 \(9\)이므로 포물선은 아래로 열려야 하며 \(n<0\)이다. 꼭짓점에서의 함수값은
\[
f(a+3)=n\cdot3\cdot(-3)=-9n=9
\]
이므로 \(n=-1\)이다. 따라서
\[
f(a+4)=n\cdot4\cdot(-2)=-8n=-8(-1)=8.
\]
결론: \(f(a+4)=8\).
