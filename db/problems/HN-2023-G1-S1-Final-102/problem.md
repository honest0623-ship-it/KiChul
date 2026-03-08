---
id: HN-2023-G1-S1-Final-102
school: HN
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2번
difficulty: 5
level: 5
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-2. 직선의 방정식
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-2. 직선의 방정식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 단답형
- 출제번호-서답2번
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/original/HN-2023-G1-S1-Final-102_original.png
---

## Q
좌표평면 위의 두 점 $A(2,0)$, $B(0,1)$과 원점 $O$를 꼭짓점으로 하는 삼각형 $OAB$가 있다. 직선 $y=\frac12x$ 위의 한 점 $P$가 삼각형 $OAB$의 내부에 있을 때, 점 $P$를 지나고 직선 $y=\frac12x$에 수직인 직선이 $x$축과 만나는 점을 $Q$, 선분 $AB$와 만나는 점을 $R$라 하자. 삼각형 $QAR$의 넓이가 $\frac13$일 때, 점 $P$의 좌표를 $(a,b)$라 하면 $5(a+b)$의 값을 구하시오.

## Choices


## Answer
$6$

## Solution
점 $P$가 직선 $y=\frac12x$ 위에 있으므로
$$
P\left(t,\frac{t}{2}\right)
$$
로 둘 수 있다.

직선 $y=\frac12x$에 수직인 직선의 기울기는 $-2$이므로, 점 $P$를 지나는 직선의 방정식은
$$
y-\frac{t}{2}=-2(x-t)
$$
$$
y=-2x+\frac52t
$$
이다.

이 직선이 $x$축과 만나는 점이 $Q$이므로
$$
Q\left(\frac54t,0\right)
$$
이다.

또 선분 $AB$가 놓인 직선의 방정식은
$$
y=-\frac12x+1
$$
이다.

따라서 점 $R$은 두 직선
$$
y=-2x+\frac52t,\qquad y=-\frac12x+1
$$
의 교점이므로
$$
R\left(\frac{5t-2}{3},\frac{8-5t}{6}\right)
$$
이다.

삼각형 $QAR$의 밑변 $QA$는 $x$축 위에 있으므로
$$
QA=2-\frac54t=\frac{8-5t}{4}
$$
이고, 높이는
$$
\frac{8-5t}{6}
$$
이다.

따라서
$$
\frac12\cdot \frac{8-5t}{4}\cdot \frac{8-5t}{6}=\frac13
$$
$$
\frac{(8-5t)^2}{48}=\frac13
$$
$$
(8-5t)^2=16
$$
이다.

점 $P$는 삼각형 내부에 있으므로 $0<t<1$이고, 따라서
$$
8-5t=4
$$
$$
t=\frac45
$$
이다.

그러므로
$$
P\left(\frac45,\frac25\right)
$$
이므로
$$
5(a+b)=5\left(\frac45+\frac25\right)=6
$$
이다.
