---
id: BY-2025-G1-S1-Final-018
school: BY
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>4. 행렬>4-1. 행렬과 그 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 4. 행렬
unit_l3: 4-1. 행렬과 그 연산
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-18
assets:
- assets/original/
- assets/original/018.png
---
## Q
$$
x^2y^2+x^2+4y^2+12xy+16=0
$$
을 만족하는 두 실수 $x,y$에 대하여 $x^2=a,\ y^2=b$라 하자.
행렬
$$
A=\begin{pmatrix}a & b \\ 0 & 1\end{pmatrix}
$$
일 때, 행렬 $A$의 모든 성분의 합은?
## Choices
① $8$
② $9$
③ $10$
④ $11$
⑤ $12$

## Answer
④

## Solution
식은 $x$에 대한 이차식으로 보면
$$
(y^2+1)x^2+12yx+(4y^2+16)=0.
$$
실수해가 존재하려면 판별식이 0 이상이어야 하므로
$$
\Delta=144y^2-4(y^2+1)(4y^2+16)=-16(y^2-2)^2\ge0.
$$
따라서 $y^2=2$, 즉 $b=2$.
이때 원식을 만족하는 $x$는 $x=-2y$이므로
$$
a=x^2=4y^2=8.
$$
행렬 성분의 합은
$$
a+b+0+1=8+2+1=11.
$$