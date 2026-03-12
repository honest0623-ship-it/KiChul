---
id: JE-2020-G2-S1-MID-104
school: JE
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-12
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서답4
- 과목-ALG
- 생성일-2026-03-12
assets:
- assets/original/
- assets/original/JE.2020.G2.S1.MID.ALG.SUB04.question.png
---

## Q
함수
\[
f(x)=\log_x(x+1)
\]
에서
\[
f(2)\cdot f(3)\cdots f(n)=6
\]
을 만족시키는 자연수 \(n\)의 값을 구하시오.

## Choices


## Answer
$63$

## Solution
밑변환을 이용하면
\[
f(k)=\log_k(k+1)=\frac{\log(k+1)}{\log k}
\]
이다.

따라서
\[
f(2)f(3)\cdots f(n)
=\frac{\log3}{\log2}\cdot\frac{\log4}{\log3}\cdots\frac{\log(n+1)}{\log n}
=\frac{\log(n+1)}{\log2}
=\log_2(n+1)
\]
이다.

\[
\log_2(n+1)=6
\Rightarrow n+1=2^6=64
\Rightarrow n=63
\]
이다.
