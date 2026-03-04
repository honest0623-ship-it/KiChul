---
id: JE-2025-G2-S1-MID-016
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-16
assets:
- assets/scan.png
- assets/original/
- assets/original/016_1-3. 로그함수.png
- assets/original/016_1-3. 로그함수_scan.png
---
## Q
$a>1$인 실수 $a$에 대하여 직선 $y=-x+7$가 두 곡선
$$
y=a^{x-3},\qquad y=\log_a(x-3)
$$
과 만나는 점을 각각 $A$, $B$라 하고, $y=a^{x-3}$이 $y$축과 만나는 점을 $C$라 하자.

$\overline{AB}=2\sqrt2$일 때, 삼각형 $ABC$의 넓이를 $\dfrac{p}{q}$라 할 때 $p+q$의 값은?

<img src="assets/scan.png" style="width: 100%; max-width: 100%;">

## Choices
① $212$  
② $213$  
③ $214$  
④ $215$  
⑤ $216$

## Answer
④

## Solution
$A$를
$$
A=(u+3,\ 4-u)
$$
라 두면 $A$가 $y=a^{x-3}$ 위의 점이므로
$$
4-u=a^u
$$
이다.

$B$를
$$
B=(v+3,\ 4-v)
$$
라 두면 $B$가 $y=\log_a(x-3)$ 위의 점이므로
$$
4-v=\log_a v
\Longleftrightarrow v=a^{4-v}
$$
이다.

위 두 식을 비교하면 $u+v=4$이고,
$$
\overline{AB}
=\sqrt{(v-u)^2+(u-v)^2}
=\sqrt2\,|v-u|
$$
이므로
$$
2\sqrt2=\sqrt2\,|v-u|
\Longrightarrow |v-u|=2
$$
이다.

$u+v=4$, $|v-u|=2$에서 $\{u,v\}=\{1,3\}$인데,
$a>1$이므로 $4-u=a^u$를 만족하는 것은 $u=1$이다.
따라서
$$
a=3,\quad A=(4,3),\quad B=(6,1)
$$
이다.

$C$는 $x=0$일 때의 점이므로
$$
C=(0,\ a^{-3})=\left(0,\frac{1}{27}\right)
$$
이다.

이제 좌표로 넓이를 구하면
$$
[ABC]
=\frac12\left|
2\left(\frac{1}{27}-3\right)-(-2)(-4)
\right|
=\frac12\left|\,-\frac{376}{27}\right|
=\frac{188}{27}
$$
이다.

즉
$$
p=188,\ q=27
$$
이므로
$$
p+q=215
$$
이다.
