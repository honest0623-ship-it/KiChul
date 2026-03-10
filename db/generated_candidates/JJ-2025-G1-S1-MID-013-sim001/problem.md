---
id: JJ-2025-G1-S1-MID-013-sim001
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
- 출제번호-13
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/013.png
level: 3
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-013
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:39:44'
---

## Q
이차함수 $y=x^2-4x+m-1$의 그래프와 $x$축이 만나는 두 점 사이의 거리가 $4$일 때, 실수 $m$의 값은?

## Choices
① -1
② 0
③ 1
④ 2
⑤ 3

## Answer
③

## Solution
그래프의 $x$절편은 방정식 $x^2-4x+m-1=0$의 두 근 $x_1, x_2$이다. 근의 공식을 이용하면
$$x=\frac{4\pm\sqrt{16-4(m-1)}}{2}=2\pm\sqrt{5-m}$$
이므로 두 점 사이의 거리는
$$|x_2-x_1|=2\sqrt{5-m}.$$ 
주어진 조건 $2\sqrt{5-m}=4$에서 $\sqrt{5-m}=2\Rightarrow 5-m=4\Rightarrow m=1.$
따라서 정답은 ③이다.
