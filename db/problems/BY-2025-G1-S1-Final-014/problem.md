---
id: BY-2025-G1-S1-Final-014
school: BY
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-14
assets:
- assets/original/
- assets/original/014.png
---
## Q
연립이차부등식
$$
\begin{cases}
x^2<x+12 \\
x^2-(2k+3)x+k^2+3k+2>0
\end{cases}
$$
을 만족시키는 정수해의 개수가 4가 되도록 하는 모든 정수 $k$의 값의 합은?
## Choices
① $-5$
② $-4$
③ $-3$
④ $-2$
⑤ $-1$

## Answer
①

## Solution
첫째 부등식은
$$
(x-4)(x+3)<0\Rightarrow -3<x<4
$$
이므로 정수해 후보는 $\{-2,-1,0,1,2,3\}$ (6개)이다.

둘째 부등식은
$$
(x-(k+1))(x-(k+2))>0
$$
이므로 $x=k+1,\ k+2$에서는 성립하지 않는다.
정수해가 4개가 되려면 후보 6개 중 정확히 2개가 제외되어야 하므로
$k+1,\ k+2$가 모두 후보 집합 안에 있어야 한다.
즉
$$
-2\le k+1\le3,\quad -2\le k+2\le3
$$
에서 $k=-3,-2,-1,0,1$.
합은
$$
-3-2-1+0+1=-5.
$$