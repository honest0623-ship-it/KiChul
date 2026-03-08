---
id: JE-2025-G2-S1-MID-102
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
subject: ALG
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 5
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-03
tags:
- 단답형
- 출제번호-서답2
assets:
- assets/original/JE-2025-G2-S1-MID-102_original.png
---

## Q
정의역이 $\{x\mid0\le x\le3\}$일 때, 함수
$$
y=\log_2(-x^2+2x+a)
$$
의 최댓값이 $3$일 때, 최솟값을 구하시오.

## Choices


## Answer
2

## Solution
안쪽 식을
$$
f(x)=-x^2+2x+a=-(x-1)^2+a+1
$$
라 두자.

정의역 $0\le x\le3$에서 $f(x)$의 최댓값은 $x=1$일 때 $a+1$이다.
또 $\log_2$는 증가함수이므로
$$
\log_2(a+1)=3
$$
이고, 따라서
$$
a+1=8\Rightarrow a=7
$$
이다.

이제
$$
f(x)=-x^2+2x+7
$$
이고, $[0,3]$에서 최솟값은 끝점에서 비교하면
$$
f(0)=7,
f(3)=4
$$
이므로 $4$이다.

따라서 함수 $y$의 최솟값은
$$
\log_2 4=2
$$
이다.
