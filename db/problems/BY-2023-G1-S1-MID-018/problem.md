---
id: BY-2023-G1-S1-MID-018
school: BY
year: 2023
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: "18"
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-05
tags:
  - 수동작성
  - 객관식
  - 출제번호-18
  - 과목-COM1
assets:
  - assets/original/
  - assets/original/BY.2023.G1.S1.MID.COM1.pdf
---

## Q
$k\ge2$인 실수 $k$에 대하여
$$
f(x)=x^2,\quad
g(x)=(x-2k)^2+k+1,\quad
h(x)=x^2-2(k-1)x+k^2+2
$$
의 그래프의 꼭짓점을 각각 $A,B,C$라 하자. 삼각형 $ABC$의 넓이를 $S(k)$라 할 때, $S(k)$의 최솟값은?

## Choices
① $6$
② $\frac{17}{2}$
③ $\frac{49}{6}$
④ $\frac{47}{6}$
⑤ $\frac{15}{2}$

## Answer
②

## Solution
꼭짓점은
$$
A=(0,0),\quad B=(2k,k+1),\quad C=(k-1,2k+1)
$$
이다.

따라서
$$
S(k)=\frac12\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|
$$
를 이용하면
$$
S(k)=\frac12\left|0\{(k+1)-(2k+1)\}+2k\{(2k+1)-0\}+(k-1)\{0-(k+1)\}\right|
$$
$$
=\frac12(3k^2+2k+1)
$$
이다.

$k\ge2$에서 $3k^2+2k+1$은 증가하므로 최솟값은 $k=2$에서 얻고
$$
S_{\min}=\frac12(12+4+1)=\frac{17}{2}
$$
이다.
