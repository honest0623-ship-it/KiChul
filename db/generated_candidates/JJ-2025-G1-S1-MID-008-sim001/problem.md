---
id: JJ-2025-G1-S1-MID-008-sim003
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: '8'
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: web_upload_2026-02-28
tags:
- 자동입력
- 객관식
- 출제번호-8
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/008.png
level: 4
derived_from: JJ-2025-G1-S1-MID-008
similarity_type: parameter_change
generation_batch_id: sim_20260309_170229
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T17:03:58'
---

## Q
함수
$$
f(n)=\left(\frac{1-i}{1+i}\right)^{n+1},\quad g(m)=\left(\frac{1+i}{1-i}\right)^{2m}
$$
일 때,
$$
f(1)+g(1)+f(2)+g(2)+\cdots+f(12)+g(12)
$$
의 값을 구하시오.

## Choices
① $0$
② $2$
③ $-2$
④ $i$
⑤ $-i$

## Answer
①

## Solution
먼저 복소수 비를 정리하면
$$
\frac{1-i}{1+i}=-i,\qquad \frac{1+i}{1-i}=i
$$
이므로
$$
f(n)=(-i)^{n+1},\qquad g(m)=i^{2m}=(-1)^m
$$
이다.

우선
$$
\sum_{m=1}^{12} g(m)=\sum_{m=1}^{12}(-1)^m=0
$$
(짝수 개의 항이므로 서로 소거).

다음으로 $(-i)^{k}$는 주기 4를 가지므로
$$
f(1),f(2),f(3),f(4) = -1,\; i,\; 1,\; -i
$$
이고 한 주기 합은 $-1+i+1-i=0$이다. 따라서 12개 항(=3주기)의 합도 0이다:
$$
\sum_{n=1}^{12} f(n)=0.
$$

결국 전체 합은 $0+0=0$이다. 따라서 정답은 ①이다.
