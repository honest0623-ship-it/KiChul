---
id: JEW-2025-G1-S1-FINAL-010
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: 10
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>4. 행렬>4-1. 행렬과 그 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 4. 행렬
unit_l3: 4-1. 행렬과 그 연산
source: user_upload_2026-03-06
tags:
- 객관식
- 출제번호-10
assets:
- assets/scan.png
- assets/original/
- assets/original/010.png
---

## Q
두 이차정사각행렬
\[
A+B=\begin{pmatrix}2 & 1 \\ 4 & 3\end{pmatrix},\quad
A-B=\begin{pmatrix}0 & -1 \\ 2 & 1\end{pmatrix}
\]
일 때, 행렬 \(AB-BA\)의 \((1,2)\)성분은?

## Choices
① \(-2\)
② \(-1\)
③ 0
④ 1
⑤ 2
## Answer
2

## Solution
Using
\[
A=\frac{(A+B)+(A-B)}{2},
\qquad
B=\frac{(A+B)-(A-B)}{2},
\]
we get
\[
A=
\begin{pmatrix}
1 & 0 \\
3 & 2
\end{pmatrix},
\qquad
B=
\begin{pmatrix}
1 & 1 \\
1 & 1
\end{pmatrix}.
\]
Then
\[
AB=
\begin{pmatrix}
1 & 1 \\
5 & 5
\end{pmatrix},
\qquad
BA=
\begin{pmatrix}
4 & 2 \\
4 & 2
\end{pmatrix},
\]
so
\[
AB-BA=
\begin{pmatrix}
-3 & -1 \\
1 & 3
\end{pmatrix}.
\]
The \((1,2)\)-entry is \(-1\), so the correct choice is 2.
