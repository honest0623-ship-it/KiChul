---
id: JJ-2025-G2-S1-MID2-STAT-103
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 3
source_question_kind: subjective
source_question_label: '서답3번'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답3번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
자연수 $n$에 대하여 $\left(x^{n}+\dfrac{2}{x}\right)^{n}$의 전개식에서 $\dfrac{1}{x^{n}}$의 계수를 $f(n)$이라 하자. 방정식 $\log_{\sqrt{2}} f(n)=20$을 만족하는 자연수 $n$의 값을 구하여라.

## Choices

## Answer
10

## Solution
전개식의 일반항은
$$
{}_{n}C_{k}(x^n)^{n-k}\left(\frac{2}{x}\right)^k
={}_{n}C_{k}2^k x^{n^2-(n+1)k}
$$
이다.
$\dfrac{1}{x^n}$항이 되려면
$$
n^2-(n+1)k=-n
$$
이어야 하므로 $k=n$.
따라서
$$
f(n)=2^n
$$
이다.

주어진 식은
$$
\log_{\sqrt{2}}(2^n)=20
$$
이고 $\sqrt{2}=2^{1/2}$이므로
$$
2n=20
$$
따라서
$$
n=10
$$
이다.
