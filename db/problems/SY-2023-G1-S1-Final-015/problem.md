---
id: SY-2023-G1-S1-Final-015
school: SY
year: 2023
grade: 1
semester: 1
exam: FINAL
subject: COM1
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-15
- 과목-COM1
- 생성일-2026-03-08
assets:
- assets/original/SY-2023-G1-S1-Final-015_original.png
---

## Q
삼차방정식
\[
x^3=1
\]
의 한 허근을 \(w\)라 할 때,
\[
(w+1)^n+(w^2+1)^n=1
\]
을 만족하는 \(50\) 이하의 정수 \(n\)의 개수는?

## Choices
① \(8\)
② \(9\)
③ \(16\)
④ \(17\)
⑤ \(18\)

## Answer
④

## Solution
\(w\)는 \(x^3=1\)의 허근이므로
\[
w^3=1,\quad 1+w+w^2=0
\]
이다.

따라서
\[
w+1=-w^2,\quad w^2+1=-w
\]
이므로
\[
(w+1)^n+(w^2+1)^n
=(-w^2)^n+(-w)^n
=(-1)^n\left(w^{2n}+w^n\right)
\]
이다.

\(w^3=1\)이므로 \(n\)을 \(6\)으로 나눈 나머지에 따라 값을 조사하면 된다.

\[
\begin{array}{c|c}
n\text{을 }6\text{으로 나눈 나머지} & (-1)^n(w^{2n}+w^n) \\
\hline
0 & 2 \\
1 & -(w^2+w)=1 \\
2 & w+w^2=-1 \\
3 & -2 \\
4 & w+w^2=-1 \\
5 & -(w+w^2)=1
\end{array}
\]

따라서 조건을 만족하는 것은 \(n\)을 \(6\)으로 나눈 나머지가 \(1\) 또는 \(5\)일 때이다.

\(1\)부터 \(50\)까지의 정수 중에서
\[
1,\ 5,\ 7,\ 11,\ \dots,\ 49
\]
이고, 개수는
\[
9+8=17
\]
이다.

따라서 정답은 ④이다.
