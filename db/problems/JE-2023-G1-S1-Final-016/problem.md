---
id: JE-2023-G1-S1-Final-016
school: JE
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
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
- 객관식
- 출제번호-16
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/original/JE-2023-G1-S1-Final-016_original.png
---

## Q
직선 $l:(1+2k)x+(2-k)y+5=0$이 실수 $k$의 값과 관계없이 항상 지나는 점을 $A$라 한다. 점 $B(-2,1)$에서 직선 $l$에 내린 수선의 발을 $H$라고 하고, $\overline{AH}=2\sqrt{2}$가 되도록 하는 모든 실수 $k$의 값의 곱은?

## Choices
① $-1$
② $-\frac13$
③ $0$
④ $\frac13$
⑤ $1$

## Answer
⑤

## Solution
주어진 직선을 정리하면
$$
x+2y+5+k(2x-y)=0
$$
이다.

직선이 항상 지나는 점 $A(x,y)$는 모든 $k$에 대하여 이 식을 만족해야 하므로
$$
\begin{cases}
x+2y+5=0\\
2x-y=0
\end{cases}
$$
를 만족한다.

따라서
$$
A(-1,-2)
$$
이다.

이제
$$
\overline{AB}=\sqrt{(-2+1)^2+(1+2)^2}=\sqrt{10}
$$
이다.

삼각형 $ABH$는 점 $H$에서 직각이므로
$$
\overline{BH}^2=\overline{AB}^2-\overline{AH}^2=10-8=2
$$
이다.

즉 점 $B$와 직선 $l$ 사이의 거리는
$$
\sqrt{2}
$$
이다.

따라서
$$
\frac{|(1+2k)(-2)+(2-k)\cdot 1+5|}{\sqrt{(1+2k)^2+(2-k)^2}}=\sqrt{2}
$$
이다.

정리하면
$$
\frac{|5-5k|}{\sqrt{5+5k^2}}=\sqrt{2}
$$
$$
\frac{5|1-k|}{\sqrt{5}\sqrt{1+k^2}}=\sqrt{2}
$$
이다.

양변을 제곱하면
$$
25(1-k)^2=10(1+k^2)
$$
$$
15k^2-50k+15=0
$$
$$
3k^2-10k+3=0
$$
이다.

따라서
$$
(3k-1)(k-3)=0
$$
이므로
$$
k=\frac13,\ 3
$$
이다.

그러므로 모든 실수 $k$의 값의 곱은
$$
\frac13\cdot 3=1
$$
이다.
