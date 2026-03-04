---
id: JEW-2025-G2-S1-MID-104
school: JEW
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-4
assets:
- assets/original/
- assets/original/서답4번_1-3. 로그함수.png
---
## Q
함수
$$
f(x)=\frac{9^x+9^{-x}}{2}
$$
의 역함수를 $g(x)$라 할 때, $g\!\left(\dfrac{5}{2}\right)=k$라 하자. 이때
$$
\frac{3^{6k}+1}{3^{4k}+3^{2k}}
$$
의 값을 구하는 과정과 답을 쓰시오. (단, $k$는 실수)

## Choices

## Answer
$4$

## Solution
$g\!\left(\dfrac{5}{2}\right)=k$이므로
$$
f(k)=\frac{5}{2}
$$
이다. 따라서
$$
\frac{9^k+9^{-k}}{2}=\frac{5}{2}
\Rightarrow 9^k+9^{-k}=5
$$

$t=9^k$라 두면 $t>0$이고
$$
t+\frac{1}{t}=5
$$
이다.

또 $3^{2k}=9^k=t$이므로
$$
\frac{3^{6k}+1}{3^{4k}+3^{2k}}
=\frac{t^3+1}{t^2+t}
=\frac{(t+1)(t^2-t+1)}{t(t+1)}
=t-1+\frac{1}{t}
$$
이다.

그러므로
$$
t-1+\frac{1}{t}
=\left(t+\frac{1}{t}\right)-1
=5-1
=4
$$
이므로 구하는 값은 $4$이다.
