---
id: HN-2022-G2-S1-MID-ALG-014
school: HN
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: objective
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-14
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/HN-2022-G2-S1-MID-ALG-014_original.png
---

## Q
함수 $f(x)=a^x-a^{-x}\ (a>0,\ a\ne 1)$과 실수 $k$에 대하여 $f(k)=2$일 때, $f(2k)f(3k)$의 값은?

## Choices
① $56\sqrt{2}$
② $28\sqrt{2}$
③ $14\sqrt{2}$
④ $14$
⑤ $7$

## Answer
①

## Solution
$u=a^k$라고 하면
\[
u-\frac{1}{u}=2
\]
이다.

따라서
\[
\left(u+\frac{1}{u}\right)^2
=\left(u-\frac{1}{u}\right)^2+4
=8
\]
이므로
\[
u+\frac{1}{u}=2\sqrt{2}
\]
이다.

그러므로
\[
f(2k)=\left(u-\frac{1}{u}\right)\left(u+\frac{1}{u}\right)=4\sqrt{2}
\]
이고,
\[
u^2+\frac{1}{u^2}
=\left(u+\frac{1}{u}\right)^2-2
=6
\]
이므로
\[
f(3k)=\left(u-\frac{1}{u}\right)\left(u^2+1+\frac{1}{u^2}\right)=2(6+1)=14
\]
이다.

따라서
\[
f(2k)f(3k)=56\sqrt{2}
\]
이다.
