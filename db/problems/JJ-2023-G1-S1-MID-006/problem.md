---
id: JJ-2023-G1-S1-MID-006
school: JJ
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 6
source_question_kind: objective
source_question_label: "6"
difficulty: 2
level: 2
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-6
assets:
  - assets/original/
  - assets/original/006_1-2. 나머지정리.png
---

## Q
다항식 $x^5-x^4+x$를 $x+1$로 나누었을 때의 몫을 $Q(x)$라 할 때, $Q(x)$를 $(x-1)(x-2)$로 나누었을 때의 나머지를 $R(x)$라 하자. 이때, $R(-1)$의 값을 구하시오.

## Choices
① $-10$
② $-8$
③ $-6$
④ $-4$
⑤ $-2$

## Answer
②

## Solution
$P(x)=x^5-x^4+x$라 두면
$$
P(x)=(x+1)Q(x)+P(-1)
$$
이고 $P(-1)=-3$이므로
$$
P(x)=(x+1)Q(x)-3.
$$

$x=1,2$를 대입하면
$$
\begin{aligned}
P(1)=1&=2Q(1)-3 \Rightarrow Q(1)=2,\\
P(2)=18&=3Q(2)-3 \Rightarrow Q(2)=7.
\end{aligned}
$$

$R(x)$는 일차식이므로 $R(x)=ax+b$라 두면
$$
R(1)=2,\quad R(2)=7
$$
이어서
$$
R(x)=5x-3.
$$
따라서
$$
R(-1)=5(-1)-3=-8.
$$
정답은 ②이다.
