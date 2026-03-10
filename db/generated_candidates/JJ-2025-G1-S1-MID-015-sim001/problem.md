---
id: JJ-2025-G1-S1-MID-015-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
difficulty: '3'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: web_upload_2026-02-27
tags:
- 자동입력
- 객관식
- 출제번호-15
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/015.png
level: 3
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-015
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:40:54'
---

## Q
학교 축제 기념 에코백을 24000원에 판매하면 하루에 48개를 팔 수 있고, 가격을 1000원씩 내릴 때마다 판매 수량이 12개씩 증가한다. 하루 판매액을 최대로 하려면 에코백 한 개의 가격을 얼마로 정해야 하는가?

## Choices
① 12000원
② 13000원
③ 14000원
④ 15000원
⑤ 16000원

## Answer
③

## Solution
가격을 1000원씩 내린 횟수를 t라 두면,
판매 가격과 판매 수량은
\[ p=24000-1000t,\quad q=48+12t \]
이다.
하루 매출액 R(t)은
\[
R(t)=pq=(24000-1000t)(48+12t)
=-12000t^2+240000t+1152000
\]
으로 아래로 열린 이차함수이다.
최대값은 꼭짓점에서 얻어지며,
\[
t=-\frac{240000}{2(-12000)}=10.
\]
이때 가격은
\[
p=24000-1000\cdot 10=14000
\]
이므로, 최대 매출이 되게 하는 가격은 14000원이다.
