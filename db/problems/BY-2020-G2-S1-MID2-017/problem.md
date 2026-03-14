---
id: BY-2020-G2-S1-MID2-017
school: BY
year: 2020
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-17
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q017.original.png
---

## Q
다항식 $2(x+m)^n$의 전개식에서 $x^{n-1}$의 계수와 다항식 $(x-1)(x+m)^n$의 전개식에서 $x^{n-1}$의 계수가 같도록 하는 자연수 $m,n$에 대하여 순서쌍 $(m,n)$의 개수는?

## Choices
① 1
② 2
③ 3
④ 4
⑤ 5

## Answer
④

## Solution
$(x+m)^n$에서 $x^{n-1}$의 계수는
$$
{}_{n}C_{n-1}m=nm
$$
이므로,
$$
2(x+m)^n
$$
에서 $x^{n-1}$의 계수는 $2nm$이다.

또
$$
(x-1)(x+m)^n=x(x+m)^n-(x+m)^n
$$
에서 $x^{n-1}$의 계수는
$$
{}_{n}C_{n-2}m^2-{}_{n}C_{n-1}m
={}_{n}C_{2}m^2-nm
$$
이다.

조건에 의해
$$
2nm={}_{n}C_{2}m^2-nm
$$
$$
3nm=\frac{n(n-1)}{2}m^2
$$
$$
m(n-1)=6
$$
이다.

자연수 해는
$$
(m,n)=(1,7),(2,4),(3,3),(6,2)
$$
의 4가지.
