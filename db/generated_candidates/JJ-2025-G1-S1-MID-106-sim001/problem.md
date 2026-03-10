---
id: JJ-2025-G1-S1-MID-106-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 6
difficulty: '5'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: web_upload_2026-02-28
tags:
- 자동입력
- 서술형
- 출제번호-6
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답6번.png
level: 5
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-106
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:46:44'
---

## Q
$-4 \le x \le 3$일 때, 이차함수 $f(x)=(3-x)(5+x)+k$의 최댓값이 12이다. 이때 $k$의 값을 구하고, 이 함수의 최솟값을 구하시오. (단, $k$는 실수)

## Choices


## Answer
k = -4, 최솟값 = -4

## Solution
함수를 전개하면
$f(x)=(3-x)(5+x)+k=-x^2-2x+15+k$ 이다.
최고차항 계수가 음수이므로 포물선은 아래로 볼록하여 꼭짓점에서 최댓값을 가진다.
꼭짓점의 x좌표는 $x=-\dfrac{-2}{2(-1)}=-1$ 이고, 이때의 함수값은
$f(-1)=-(-1)^2-2(-1)+15+k=16+k$이다.
문제에서 최댓값이 12이므로 $16+k=12$ 이고, 따라서 $k=-4$.
$k=-4$를 대입하면 $f(x)=-x^2-2x+11$ 이다.
정의역의 끝점에서 최솟값이 발생하므로 $x=-4,3$에서 값을 비교한다.
$f(-4)=-(-4)^2-2(-4)+11=-16+8+11=3$,
$f(3)=-(3)^2-2(3)+11=-9-6+11=-4$.
따라서 최솟값은 $f(3)=-4$이다.
정리: $k=-4$, 최솟값 $=-4$.
