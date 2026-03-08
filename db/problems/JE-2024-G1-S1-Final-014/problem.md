---
id: JE-2024-G1-S1-Final-014
school: JE
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM1
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-07
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-14
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JE.2024.G1.S1.Final.COM1.pdf
---
## Q
오류문항: 원문대로 해석하면 실수해가 $2$개일 수 없다. 
문맥상 자연스러운 "정수해가 $2$개"로 수정해야 한다.

연립부등식
\[
\begin{cases}
\left|x-k\right|<2 \\
3x^2-14x-5<0
\end{cases}
\]
의 해 $x$가 $2$개일 때, 정수 $k$값의 합을 구하면?

## Choices
① $2$
② $3$
③ $4$
④ $5$
⑤ $6$

## Answer
③

## Solution
둘째 부등식을 풀면
\[
3x^2-14x-5<0
\]
\[
(3x+1)(x-5)<0
\]
이므로
\[
-\frac{1}{3}<x<5
\]
이다.

따라서 정수해는
\[
0,\ 1,\ 2,\ 3,\ 4
\]
이다.

첫째 부등식
\[
\left|x-k\right|<2
\]
를 만족하는 정수 $x$는
\[
k-1,\ k,\ k+1
\]
뿐이다.

이 가운데
\[
0,\ 1,\ 2,\ 3,\ 4
\]
와 겹치는 수가 정확히 $2$개가 되어야 한다.

이를 확인하면
\[
k=0 \text{일 때 } \{-1,0,1\}\cap\{0,1,2,3,4\}=\{0,1\}
\]
\[
k=4 \text{일 때 } \{3,4,5\}\cap\{0,1,2,3,4\}=\{3,4\}
\]
가 된다.

그 밖의 정수 $k$에 대해서는 겹치는 정수의 개수가 $2$가 아니다.

따라서 정수 $k$의 값은
\[
0,\ 4
\]
이고, 그 합은
\[
4
\]
이다.

그러므로 정답은 ③이다.
