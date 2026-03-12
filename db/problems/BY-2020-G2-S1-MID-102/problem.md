---
id: BY-2020-G2-S1-MID-102
school: BY
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-11
tags:
- 수동생성
- PDF
- 단답형
- 출제번호-서답2
- 과목-ALG
- 생성일-2026-03-11
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID.ALG.SUB02.question.png
---

## Q
$2\le n\le 100$인 자연수 $n$에 대하여
\[
\left(\sqrt{7^5}\right)^{\frac13}
\]
이 어떤 자연수의 $n$제곱근이 되도록 하는 $n$의 개수를 구하여라.

## Choices


## Answer
$16$

## Solution
주어진 수를 정리하면
\[
\left(\sqrt{7^5}\right)^{1/3}
=\left(7^{5/2}\right)^{1/3}
=7^{5/6}
\]
이다.

이 수가 어떤 자연수의 $n$제곱근이 되려면
\[
\left(7^{5/6}\right)^n=7^{5n/6}
\]
이 자연수가 되어야 한다. 즉 지수 $\dfrac{5n}{6}$이 정수여야 하므로
\[
6\mid 5n
\]
이고, $\gcd(5,6)=1$이므로 $6\mid n$이다.

$2\le n\le 100$에서 $6$의 배수는
\[
6,12,18,\dots,96
\]
으로 총
\[
\frac{96-6}{6}+1=16
\]
개이다.

따라서 구하는 개수는 $16$이다.
