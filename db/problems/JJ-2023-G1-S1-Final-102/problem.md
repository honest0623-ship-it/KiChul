---
id: JJ-2023-G1-S1-Final-102
school: JJ
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM1
type: 서답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 서답형
- 출제번호-서답2
- 과목-COM1
- 생성일-2026-03-08
assets:
- assets/original/JJ-2023-G1-S1-Final-102_original.png
---

## Q
연립부등식
\[
\begin{cases}
x^2-6x+5>0 \\
x^2-(2+a)x+2a<0
\end{cases}
\]
의 정수인 해가 $2$개다. 이때, 실수 $a$의 최댓값을 $M$, 최솟값을 $m$이라고 할 때, $M-m$의 값을 구하여라.

## Choices


## Answer
10

## Solution
첫 번째 부등식은
\[
x^2-6x+5=(x-1)(x-5)
\]
이므로
\[
x<1 \quad \text{또는} \quad x>5
\]
이다.

두 번째 부등식은
\[
x^2-(2+a)x+2a=(x-2)(x-a)
\]
이므로
\[
(x-2)(x-a)<0
\]
의 해는 $x$가 $2$와 $a$ 사이에 있을 때이다.

\[
\text{(1) }a<2
\]
이면 두 번째 부등식의 해는
\[
a<x<2
\]
이다.

이 구간에서 첫 번째 부등식을 함께 만족하는 정수는 $1$보다 작은 정수뿐이므로, 정수해가 정확히 $2$개가 되려면 그 해가
\[
-1,\ 0
\]
뿐이어야 한다.

따라서
\[
-2\le a<-1
\]
이다.

\[
\text{(2) }a>2
\]
이면 두 번째 부등식의 해는
\[
2<x<a
\]
이다.

이 구간에서 첫 번째 부등식을 함께 만족하는 정수는 $5$보다 큰 정수뿐이므로, 정수해가 정확히 $2$개가 되려면 그 해가
\[
6,\ 7
\]
뿐이어야 한다.

따라서
\[
7<a\le 8
\]
이다.

결국 가능한 $a$의 범위는
\[
-2\le a<-1 \quad \text{또는} \quad 7<a\le 8
\]
이므로
\[
m=-2,\qquad M=8
\]
이다.

따라서
\[
M-m=8-(-2)=10
\]
이다.
