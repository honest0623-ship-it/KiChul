---
id: JE-2023-G1-S1-MID-009
school: JE
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: "9"
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
  - 출제번호-9
assets:
  - assets/original/
  - assets/original/009_1-2. 나머지정리.png
---

## Q
다항식 \(P(x)\)를 \((x+4)^2\)로 나누었을 때의 나머지는 \(x+5\)이고,  
\(x+3\)으로 나누었을 때의 나머지는 \(3\)이다.

\(P(x)\)를 \((x+4)^2(x+3)\)으로 나누었을 때의 나머지를 \(R(x)\)라 할 때,  
\(R(1)\)의 값은?

## Choices
① 28  
② 29  
③ 30  
④ 32  
⑤ 31

## Answer
31

## Solution
\(P(x)\)를 \((x+4)^2(x+3)\)으로 나눈 나머지를 \(R(x)\)라 하면,  
\(R(x)\)는 차수가 \(2\) 이하이다.

\((x+4)^2\)로 나눈 나머지가 \(x+5\)이므로
\[
R(x)\equiv x+5 \pmod{(x+4)^2}.
\]
따라서 어떤 상수 \(k\)가 존재하여
\[
R(x)=x+5+k(x+4)^2
\]
로 둘 수 있다.  
(이유: 차수 \(2\) 이하에서 \((x+4)^2\)의 배수는 상수배뿐이다.)

또한 \(x+3\)으로 나눈 나머지가 \(3\)이므로
\[
R(-3)=3.
\]
위 식에 \(x=-3\)을 대입하면
\[
3=(-3+5)+k(-3+4)^2=2+k
\]
이므로
\[
k=1.
\]

따라서
\[
R(x)=x+5+(x+4)^2=x^2+9x+21.
\]
그러므로
\[
R(1)=1+9+21=31.
\]
