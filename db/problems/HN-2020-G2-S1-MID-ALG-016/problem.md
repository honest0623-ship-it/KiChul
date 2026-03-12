---
id: HN-2020-G2-S1-MID-ALG-016
school: HN
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-11
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-16
- 과목-ALG
- 생성일-2026-03-11
assets:
- assets/original/
- assets/original/HN.2020.G2.S1.MID.ALG.016.question.png
---

## Q
정의역 $\{x\mid1\le x\le4\}$인 함수
\[
f(x)=9\times x^{-4+\log_3 x^2}
\]
의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M-m$의 값은?

## Choices
① $4$
② $5$
③ $6$
④ $7$
⑤ $8$

## Answer
⑤

## Solution
$x=3^t$라 두면 $t=\log_3x$이고
\[
0\le t\le\log_34
\]
이다.

\[
\log_3x^2=2\log_3x=2t
\]
이므로
\[
f(x)=9(3^t)^{-4+2t}
=3^2\cdot3^{-4t+2t^2}
=3^{2(t-1)^2}
\]
이다.

따라서 $f(x)$의 최소는 $(t-1)^2$가 최소일 때이며 $t=1$에서
\[
m=3^0=1
\]
이다.

최대는 구간 끝점에서 비교하면
\[
t=0\Rightarrow f=3^2=9,\quad
t=\log_34\Rightarrow f<9
\]
이므로
\[
M=9
\]
이다.

따라서
\[
M-m=9-1=8
\]
이고 정답은 ⑤이다.
