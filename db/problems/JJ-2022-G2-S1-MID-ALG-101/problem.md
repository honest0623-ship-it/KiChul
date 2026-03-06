---
id: JJ-2022-G2-S1-MID-ALG-101
school: JJ
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: subjective
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1번
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답1번
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ-2022-G2-S1-MID-ALG-101_original.png
---

## Q
세 양수 $x$, $y$, $z$에 대하여 $2^x=3^y=n^z$, $xy=yz+zx$일 때, 양수 $n$의 값을 구하시오.

## Choices


## Answer
6

## Solution
$2^x=3^y=n^z=M$이라 하자.
그러면
\[
x=z\log_2 n,\qquad y=z\log_3 n
\]
이다.

이를 $xy=yz+zx$에 대입하면
\[
z^2\log_2 n\log_3 n=z^2(\log_3 n+\log_2 n)
\]
이다.

$z>0$이므로
\[
\log_2 n\log_3 n=\log_3 n+\log_2 n
\]
이다.

자연로그로 바꾸면
\[
\frac{\ln n}{\ln 2}\cdot\frac{\ln n}{\ln 3}
=\frac{\ln n}{\ln 2}+\frac{\ln n}{\ln 3}
\]
이고, $\ln n>0$이므로
\[
\ln n=\ln 2+\ln 3=\ln 6
\]
이다.

따라서
\[
n=6
\]
이다.
