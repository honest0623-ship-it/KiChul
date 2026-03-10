---
id: HN-2025-G1-S1-MID-018-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: ''
tags:
- 이차함수
- 도형
- 둘레최대
- 넓이
assets:
- assets/scan.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: HN-2025-G1-S1-MID-018
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:32:35'
---

## Q
오른쪽 그림의 직사각형 $ABCD$에서 두 점 $A$와 $B$는 $x$축 위에 있고, 두 점 $C$와 $D$는 이차함수
$$
y=-x^2+4x
$$
의 그래프 위에 있다. 이때 직사각형 $ABCD$의 둘레의 길이의 최댓값을 $\alpha$라고 하고, 그때의 직사각형의 넓이를 $\beta$라 할 때, $\alpha+\beta$의 값은? (단, 두 점 $C,D$는 제1사분면 위의 점이다.)

## Choices
① 8
② 10
③ 12
④ 14
⑤ 16

## Answer
⑤

## Solution
함수
$$f(x)=-x^2+4x=-(x-2)^2+4$$
은 $x=2$에 대해 대칭이므로 윗변이 닿는 두 점을
$$x=2\pm t\qquad(t>0)$$
로 두면 폭은 $2t$이다.

높이는
$$h=f(2-t)=-(t^2)+4=4-t^2.$$ 

둘레는
\[P(t)=2(2t+h)=2(2t+4-t^2)=-2t^2+4t+8.\]
이므로 이차함수의 최대는 꼭짓점에서 이루어지고,
$$t=\frac{-4}{2(-2)}=1.$$
따라서
$$\alpha=P(1)=-2(1)^2+4(1)+8=10.$$

넓이는
$$A(t)=(2t)h=2t(4-t^2)=-2t^3+8t,$$
이므로
$$\beta=A(1)=-2+8=6.$$
따라서
$$\alpha+\beta=10+6=16.$$ (정답 ⑤)
