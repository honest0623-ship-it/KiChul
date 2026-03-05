---
id: JEW-2023-G1-S1-MID-104
school: JEW
year: 2023
grade: 1
semester: 1
exam: MID
type: "서답형(단답형)"
source_question_no: 4
source_question_kind: subjective
source_question_label: "서답4"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-2. 이차방정식과 이차함수"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 서답형(단답형)
  - 출제번호-서답4
assets:
  - assets/original/
  - assets/original/서답4번_2-2. 이차방정식과 이차함수.png
---

## Q
\(1\le x\le 2\)에서 이차함수
\[
y=x^2-2ax+a^2+b
\]
의 최솟값이 \(4\)가 되도록 하는 두 실수 \(a,\ b\)에 대하여
\(2a+b\)의 최댓값을 구하시오.

## Choices


## Answer
9

## Solution
\[
y=(x-a)^2+b
\]
이다.

구간 \([1,2]\)에서의 최솟값은
\[
\min_{1\le x\le2}(x-a)^2+b=d^2+b
\]
이고, 여기서 \(d\)는 점 \(a\)와 구간 \([1,2]\) 사이의 거리이다.

최솟값이 \(4\)이므로
\[
b=4-d^2.
\]
따라서
\[
2a+b=2a+4-d^2.
\]

경우를 나눈다.

\[
a<1\Rightarrow d=1-a,\quad
2a+b=2a+4-(1-a)^2=-a^2+4a+3<6.
\]

\[
1\le a\le2\Rightarrow d=0,\quad
2a+b=2a+4\le8.
\]

\[
a>2\Rightarrow d=a-2,\quad
2a+b=2a+4-(a-2)^2=-(a-3)^2+9\le9.
\]

최댓값은 \(a=3\)일 때 \(9\)이다.
(이때 \(b=3\), 실제 최솟값은 \(x=2\)에서 \(4\)가 된다.)
