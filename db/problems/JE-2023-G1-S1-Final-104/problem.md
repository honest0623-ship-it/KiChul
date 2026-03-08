---
id: JE-2023-G1-S1-Final-104
school: JE
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서술형4
difficulty: 5
level: 5
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-1. 평면좌표
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-1. 평면좌표
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서술형4
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/original/JE-2023-G1-S1-Final-104_original.png
---

## Q
점 $A(x_1,y_1)$, $B(x_2,y_2)$, $C(x_3,y_3)$에 대하여 삼각형 $ABC$의 세 변 $\overline{AB}$, $\overline{BC}$, $\overline{CA}$의 중점이 각각 $D(3,3)$, $E(2,4)$, $F(1,2)$이다. 다음 물음에 답하시오.

(1) 삼각형 $ABC$의 무게중심의 좌표와 점 $A$, $B$, $C$의 좌표를 구하시오.

(2) 점 $(4,9)$과 직선 $\overline{AB}$의 방정식과 사이의 거리를 구하시오.

(3) 선분 $\overline{AB}$를 $3:2$로 내분하는 점 $P$와 선분 $\overline{BC}$를 $5:1$로 외분하는 점 $Q$를 구하시오.

## Choices


## Answer
(1) 무게중심 $(2,3)$, $A(2,1)$, $B(4,5)$, $C(0,3)$

(2) $\dfrac{4\sqrt{5}}{5}$

(3) $P\left(\dfrac{16}{5},\dfrac{17}{5}\right)$, $Q\left(-1,\dfrac{5}{2}\right)$

## Solution
중점의 성질에 의하여
$$
\begin{cases}
\dfrac{x_1+x_2}{2}=3,\quad \dfrac{y_1+y_2}{2}=3\\
\dfrac{x_2+x_3}{2}=2,\quad \dfrac{y_2+y_3}{2}=4\\
\dfrac{x_3+x_1}{2}=1,\quad \dfrac{y_3+y_1}{2}=2
\end{cases}
$$
이다.

따라서
$$
\begin{cases}
x_1+x_2=6\\
x_2+x_3=4\\
x_3+x_1=2
\end{cases}
\qquad
\begin{cases}
y_1+y_2=6\\
y_2+y_3=8\\
y_3+y_1=4
\end{cases}
$$
이다.

이를 풀면
$$
A(2,1),\quad B(4,5),\quad C(0,3)
$$
이다.

따라서 무게중심은
$$
\left(\frac{2+4+0}{3},\frac{1+5+3}{3}\right)=(2,3)
$$
이다.

(2) 직선 $\overline{AB}$의 기울기는
$$
\frac{5-1}{4-2}=2
$$
이므로 방정식은
$$
y-1=2(x-2)
$$
즉
$$
2x-y-3=0
$$
이다.

따라서 점 $(4,9)$와 이 직선 사이의 거리는
$$
\frac{|2\cdot 4-9-3|}{\sqrt{2^2+(-1)^2}}=\frac{4}{\sqrt{5}}=\frac{4\sqrt{5}}{5}
$$
이다.

(3) 선분 $\overline{AB}$를 $3:2$로 내분하는 점 $P$는
$$
P\left(\frac{2\cdot 2+3\cdot 4}{3+2},\frac{2\cdot 1+3\cdot 5}{3+2}\right)=\left(\frac{16}{5},\frac{17}{5}\right)
$$
이다.

또 선분 $\overline{BC}$를 $5:1$로 외분하는 점 $Q$는
$$
Q\left(\frac{5\cdot 0-1\cdot 4}{5-1},\frac{5\cdot 3-1\cdot 5}{5-1}\right)=\left(-1,\frac{5}{2}\right)
$$
이다.
