---
id: BY-2020-G2-S1-MID-104
school: BY
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: 5
level: 5
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-11
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서답4
- 과목-ALG
- 생성일-2026-03-11
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID.ALG.SUB04.question.png
---

## Q
$0\le\theta<2\pi$일 때, 모든 실수 $x$에 대하여 부등식
\[
x^2-2\sin\theta\,x-\cos^2\theta-2\cos\theta+2\ge 0
\]
이 항상 성립하도록 하는 모든 $\theta$의 값의 범위는 $\alpha\le\theta\le\beta$이다. $\beta-2\alpha$의 값을 구하는 풀이과정을 쓰고 답을 구하여라.

## Choices


## Answer
$\pi$

## Solution
이차식
\[
F(x)=x^2-2\sin\theta\,x-\cos^2\theta-2\cos\theta+2
\]
가 모든 실수 $x$에 대해 $F(x)\ge 0$이려면 판별식이 $0$ 이하이면 된다.

\[
\Delta=(-2\sin\theta)^2-4\cdot1\cdot(-\cos^2\theta-2\cos\theta+2)
\]
\[
=4\sin^2\theta+4(\cos^2\theta+2\cos\theta-2)
\]
\[
=4(\sin^2\theta+\cos^2\theta+2\cos\theta-2)
=4(2\cos\theta-1)
\]
따라서
\[
\Delta\le0\iff 2\cos\theta-1\le0\iff \cos\theta\le\frac12
\]
이다.

$0\le\theta<2\pi$에서
\[
\frac\pi3\le\theta\le\frac{5\pi}3
\]
이므로
\[
\alpha=\frac\pi3,\qquad \beta=\frac{5\pi}3
\]
이다.

따라서
\[
\beta-2\alpha
=\frac{5\pi}3-2\cdot\frac\pi3
=\pi
\]
이다.
