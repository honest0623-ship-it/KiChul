---
id: HN-2020-G2-S1-MID-ALG-009
school: HN
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: '9'
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
- 출제번호-9
- 과목-ALG
- 생성일-2026-03-11
assets:
- assets/original/
- assets/original/HN.2020.G2.S1.MID.ALG.009.question.png
---

## Q
함수 $f(x)=a^x-a^{-x}$ ($a>0$, $a\ne1$)과 실수 $k$에 대하여
\[
f(k)=2
\]
일 때, $f(2k)$를 구하면?

## Choices
① $\sqrt2$
② $2\sqrt2$
③ $3\sqrt2$
④ $4\sqrt2$
⑤ $5\sqrt2$

## Answer
④

## Solution
$u=a^k$라 두면 $u>0$이고
\[
u-\frac1u=2
\]
이다.

따라서
\[
u^2-2u-1=0
\]
이고 $u=1+\sqrt2$ (양수이므로)이다.
그러면
\[
\frac1u=\sqrt2-1
\]
이다.

\[
f(2k)=a^{2k}-a^{-2k}
=u^2-\frac1{u^2}
=\left(u-\frac1u\right)\left(u+\frac1u\right)
\]
\[
=2\left((1+\sqrt2)+(\sqrt2-1)\right)
=2(2\sqrt2)=4\sqrt2
\]
이므로 정답은 ④이다.
