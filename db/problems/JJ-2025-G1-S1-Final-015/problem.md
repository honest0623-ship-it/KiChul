---
id: JJ-2025-G1-S1-Final-015
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>4. 행렬>4-1. 행렬과 그 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 4. 행렬
unit_l3: 4-1. 행렬과 그 연산
source: user_upload_2026-02-27
tags:
- 수동정제
- 객관식
- 출제번호-15
assets:
- assets/original/
- assets/original/015.png
---
## Q
행렬 $A=\begin{pmatrix}1 & 3 \cr -1 & -2\end{pmatrix}$에 대하여 $X=2A^5-4A^2+A$라 할 때, 행렬 $X$의 $(1,2)$ 성분은?

## Choices
① -4
② -3
③ 1
④ 5
⑤ 9

## Answer
⑤

## Solution
$A^2$를 계산하면
$$
A^2=\begin{pmatrix}-2 & -3 \cr 1 & 1\end{pmatrix}
$$
이므로
$$
A^2+A+I=O
$$
를 만족한다. 따라서
$$
A^3=I
$$
이고
$$
A^5=A^2
$$
이다.

그러므로
$$
X=2A^5-4A^2+A=-2A^2+A.
$$
또한 $A^2=-A-I$이므로
$$
X=-2(-A-I)+A=3A+2I
$$
이다.

따라서
$$
X=3\begin{pmatrix}1 & 3 \cr -1 & -2\end{pmatrix}+2\begin{pmatrix}1 & 0 \cr 0 & 1\end{pmatrix}=\begin{pmatrix}5 & 9 \cr -3 & -4\end{pmatrix}.
$$
따라서 $(1,2)$ 성분은 $9$이다.
