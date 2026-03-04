---
id: HN-2023-G1-S1-MID-007
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: "7"
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
  - 출제번호-7
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/007_1-2. 나머지정리.png
---

## Q
최고차항의 계수가 \(3\)인 다항식 \(f(x)\)를 다항식 \(g(x)\)로 나누었을 때의 몫과 나머지가 모두 \(g(x)-3x\)일 때,
\[
\{f(x)\}^4+\{g(x)\}^4
\]
을 \(3x+1\)로 나눈 나머지를 구하시오.

## Choices
① 1  
② 2  
③ 3  
④ 4  
⑤ 5

## Answer
①

## Solution
몫과 나머지가 모두 \(g(x)-3x\)이므로
\[
f(x)=g(x)\{g(x)-3x\}+\{g(x)-3x\}
=\{g(x)+1\}\{g(x)-3x\}
\]
이다.

나머지는 나누는 식의 차수보다 낮아야 하므로
\[
\deg\{g(x)-3x\}<\deg g(x)
\]
이고, 따라서 \(g(x)-3x\)는 상수이다. 그러므로
\[
g(x)=3x+b
\]
로 둘 수 있다.

그러면
\[
f(x)=\{3x+b+1\}\cdot b
\]
이고, \(f(x)\)의 최고차항 계수가 \(3\)이므로
\[
3b=3 \Rightarrow b=1.
\]
따라서
\[
g(x)=3x+1.
\]

\(3x+1\)로 나눈 나머지는 \(x=-\frac13\) 대입값이다.
\[
g\!\left(-\frac13\right)=0,\quad
f\!\left(-\frac13\right)=\{0+1\}\{0-3(-\tfrac13)\}=1.
\]
그러므로
\[
\{f(x)\}^4+\{g(x)\}^4
\]
의 나머지는
\[
1^4+0^4=1
\]
이다. 정답은 \(①\)이다.

