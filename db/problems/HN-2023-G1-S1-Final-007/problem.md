---
id: HN-2023-G1-S1-Final-007
school: HN
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM1
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: '7'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-7
- 과목-COM1
- 생성일-2026-03-08
assets:
- assets/original/HN-2023-G1-S1-Final-007_original.png
---

## Q
연립부등식
$$
\begin{cases}
x^2-4>0\\
(2x-9)(x-k)<0
\end{cases}
$$
을 만족시키는 정수 $x$가 $2$개일 때, 정수 $k$의 개수는?

## Choices
① $3$
② $4$
③ $5$
④ $6$
⑤ $7$

## Answer
⑤

## Solution
$x^2-4>0$이므로
$$
x<-2 \quad \text{또는} \quad x>2
$$
이다.

또
$$
(2x-9)(x-k)<0
$$
이므로 $x$는 두 근 $k$, $\frac92$ 사이에 있어야 한다.

정수 $k$에 따라 경우를 나눈다.

1. $k\le 4$일 때는
$$
k<x<\frac92
$$
이다. 이 구간에서 $x^2-4>0$까지 만족하는 정수해가 $2$개가 되려면
$$
k=-3,-2,-1,0,1,2
$$
여야 한다.

2. $k\ge 5$일 때는
$$
\frac92<x<k
$$
이다. 이 구간의 정수는 $5,6,\dots,k-1$이므로 개수는 $k-5$개이다.

정수해가 $2$개가 되려면
$$
k-5=2
$$
이어서
$$
k=7
$$
이다.

따라서 가능한 정수 $k$는
$$
-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 7
$$
의 $7$개이다.
