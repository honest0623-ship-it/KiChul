---
id: HN-2023-G1-S1-MID-013
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: "13"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-13
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/013_1-2. 나머지정리.png
---

## Q
다항식 \(P(x)\), \(Q(x)\)가 다음 조건을 만족시킨다.

가) \(P(x)\)를 \(x+1\)로 나눈 나머지는 \(4\)이다.  
나) \(P(x)=(x-1)^3Q(x)+2x^2-7x+5\)

다항식 \(P(x)\)를 \((x-1)^2(x+1)\)로 나누었을 때의 나머지를 \(R(x)\)라 할 때, \(R(-3)\)의 값을 구하시오.

## Choices
① 2  
② 4  
③ 6  
④ 8  
⑤ 10

## Answer
②

## Solution
\[
P(x)=(x-1)^3Q(x)+2x^2-7x+5
\]
이므로
\[
P(x)-\left(2x^2-7x+5\right)
\]
는 \((x-1)^3\)의 배수이다.

따라서 \(P(x)\)를 \((x-1)^2(x+1)\)로 나눈 나머지 \(R(x)\)는
\[
R(1)=0,\quad R'(1)=-3
\]
을 만족한다. 또한 가)에서
\[
R(-1)=P(-1)=4
\]
이다.

\(R(x)=ax^2+bx+c\)라 두면
\[
\begin{aligned}
R(1)&=a+b+c=0,\\
R'(1)&=2a+b=-3,\\
R(-1)&=a-b+c=4.
\end{aligned}
\]
이를 풀면
\[
a=-\frac12,\quad b=-2,\quad c=\frac52.
\]

따라서
\[
R(x)=-\frac12x^2-2x+\frac52
\]
이고,
\[
R(-3)=-\frac12\cdot 9+6+\frac52=4.
\]
정답은 \(②\)이다.

