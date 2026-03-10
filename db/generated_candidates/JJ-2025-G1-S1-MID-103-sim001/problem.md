---
id: JJ-2025-G1-S1-MID-103-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 3
difficulty: '5'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: web_upload_2026-02-28
tags:
- 자동입력
- 단답형
- 출제번호-3
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답3번.png
level: 5
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-103
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:43:44'
---

## Q
닫힌 구간 $[2a,0)$에서 이차함수 $f(x)=ax^2+6ax-8a^2+6$의 최댓값이 $6$이 되도록 하는 $a$의 값을 구하시오.

## Choices


## Answer
$-1$

## Solution
주어진 함수에 대해 완전제곱으로 정리하면
$f(x)=a(x^2+6x)-8a^2+6=a(x+3)^2-9a-8a^2+6$이므로 축은 $x=-3$이고 구간은 $[2a,0)$이다.

먼저 $a>0$인 경우는 $2a>0$이므로 구간 $[2a,0)$이 존재하지 않아 불가능하다. 따라서 $a<0$만 고려한다.

(a) 축이 구간 안에 있는 경우: $2a\le -3<0$ 즉 $a\le -3/2$.
이때 최댓값은 $x=-3$에서 얻어지며
$f(-3)=-9a-8a^2+6=6$이므로 $-9a-8a^2=0$이다. 즉 $a=0$ 또는 $a=-9/8$이나 $a<0$이면서 $a\le -3/2$ 조건을 만족하지 않으므로 해가 아니다.

(b) 축이 구간 왼쪽 밖에 있는 경우: $-3<2a$ 즉 $-3/2<a<0$.
이때 함수는 구간에서 감소하므로 최댓값은 왼쪽 끝점 $x=2a$에서 얻어진다.
$f(2a)=a(2a)^2+6a(2a)-8a^2+6=4a^3+4a^2+6$이고, 이것이 $6$과 같아야 하므로
$4a^3+4a^2+6=6\Rightarrow4a^2(a+1)=0$이다. 따라서 $a=0$ 또는 $a=-1$이다.
조건 $-3/2<a<0$에 맞는 해는 $a=-1$뿐이다.

따라서 조건을 만족하는 $a$는 $\boxed{-1}$ 이다.
