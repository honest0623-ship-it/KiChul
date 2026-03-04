---
id: JE-2025-G2-S1-MID-103
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-3
assets:
- assets/original/
- assets/original/서답3번_1-3. 로그함수.png
---
## Q
$a>1$인 실수 $a$에 대하여 곡선
$$
y=\log_4(x-a)
$$
가 $x$축과 만나는 점을 $A$, 직선 $y=\dfrac12$와 만나는 점을 $B$라 하고, 점 $A$를 지나고 $x$축에 수직인 직선이 곡선
$$
y=2^{x-1}+2
$$
와 만나는 점을 $C$라 하자.

직선 $AB$와 수직이고 점 $A$를 지나는 직선이 곡선 $y=2^{x-1}+2$와 만나는 점을 $D$라 할 때, 삼각형 $ABD$의 넓이는 $\dfrac{5}{2}$이다.

이때 삼각형 $BCD$의 넓이를 구하는 과정과 답을 쓰시오.

## Choices

## Answer
$\dfrac{25}{2}$

## Solution
$A$는 $x$축 위의 점이므로
$$
\log_4(x-a)=0\Rightarrow x=a+1
$$
따라서
$$
A=(a+1,0)
$$
이다.

$B$는 $y=\dfrac12$ 위의 점이므로
$$
\log_4(x-a)=\frac12\Rightarrow x-a=2
$$
따라서
$$
B=(a+2,\frac12)
$$
이다.

그러므로
$$
\overline{AB}
=\sqrt{1^2+\left(\frac12\right)^2}
=\frac{\sqrt5}{2}
$$
이다.

또 $AD\perp AB$이므로 $\triangle ABD$는 직각삼각형이고
$$
\frac12\cdot \overline{AB}\cdot \overline{AD}
=\frac52
$$
에서
$$
\overline{AD}
=\frac{5}{\overline{AB}}
=\frac{5}{\sqrt5/2}
=2\sqrt5
$$
이다.

$AB$의 기울기는 $\dfrac12$이므로 $AD$의 기울기는 $-2$이다.
점 $A(a+1,0)$를 지나므로
$$
AD:\ y=-2(x-a-1)
$$
이다.

$\overline{AD}=2\sqrt5$이고 방향벡터를 $(1,-2)$로 보면
$$
D=(a-1,4)
$$
를 얻는다.

$D$가 $y=2^{x-1}+2$ 위의 점이므로
$$
4=2^{(a-1)-1}+2
\Rightarrow 2^{a-2}=2
\Rightarrow a=3
$$
이다.

따라서
$$
B=\left(5,\frac12\right),\quad
C=(4,10),\quad
D=(2,4)
$$
이다.

삼각형 $BCD$의 넓이는
$$
[BCD]
=\frac12\left|
(-1)\cdot\frac72-\frac{19}{2}\cdot(-3)
\right|
=\frac12\cdot 25
=\frac{25}{2}
$$
이다.
