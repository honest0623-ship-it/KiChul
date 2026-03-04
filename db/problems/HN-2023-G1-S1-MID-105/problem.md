---
id: HN-2023-G1-S1-MID-105
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: "서답5"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 서술형
  - 출제번호-5
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답5번_1-2. 나머지정리.png
---

## Q
최고차항의 계수가 \(2\)인 사차다항식 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(4)\)의 값을 구하시오.

가) \(f(x)\)를 \(x+1\)로 나눈 나머지와 \(f(x)\)를 \(x^2-3\)으로 나눈 나머지는 서로 같다.  
나) \(f(x+1)-5\)는 \(x^2+x\)로 나누어떨어진다.

## Choices

## Answer
-19

## Solution
가)에서 \(f(x)\)를 \(x+1\)로 나눈 나머지를 \(r\)이라 하면, \(x^2-3\)으로 나눈 나머지도 같은 식 \(r\)이다.  
따라서
\[
f(x)-r
\]
는 \((x+1)(x^2-3)\)의 배수이다.

최고차항의 계수가 \(2\)인 사차식이므로 어떤 상수 \(t\)에 대해
\[
f(x)-r=2(x+1)(x^2-3)(x-t)
\]
로 쓸 수 있다.

나)에서 \(f(x+1)-5\)가 \(x(x+1)\)로 나누어떨어지므로
\[
f(0)=5,\quad f(1)=5.
\]

위 식에 대입하면
\[
f(0)-r=6t,\quad f(1)-r=8(t-1).
\]
즉
\[
5-r=6t,\quad 5-r=8(t-1).
\]
따라서
\[
6t=8t-8 \Rightarrow t=4.
\]
이를 \(5-r=6t\)에 넣으면
\[
5-r=24 \Rightarrow r=-19.
\]

이제
\[
f(4)=r+2(4+1)(4^2-3)(4-4)=r
\]
이므로
\[
f(4)=-19.
\]

