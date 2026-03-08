---
id: JEW-2023-G2-S1-MID-ALG-017
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: 17
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-17
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-017_original.png
---

## Q
자연수 $m\ (m\ge 2)$에 대하여 $2^m$의 $n$제곱근 중에서 정수가 존재하도록 하는 $2$ 이상의 자연수 $n$의 개수를 $f(m)$이라 하자.
$f(m)=1$을 만족하는 $10$ 이하의 자연수 $m$의 값의 합은?

## Choices
① $15$
② $17$
③ $25$
④ $26$
⑤ $30$

## Answer
②

## Solution
$2^m$의 $n$제곱근이 정수라고 하자. 그러면 그 정수를 $2^k$라 놓을 수 있고
$$
(2^k)^n=2^m
$$
이므로
$$
2^{kn}=2^m
$$
이다. 따라서
$$
kn=m
$$
이므로 $m$은 $n$의 배수이다.

따라서 $f(m)$은 $m$의 약수 중 $2$ 이상인 것의 개수와 같다.

$f(m)=1$이 되려면 $m$의 약수가 $1$과 자기 자신뿐이어야 하므로 $m$은 소수이다.
$10$ 이하의 자연수 중 $2$ 이상인 소수는
$$
2,\ 3,\ 5,\ 7
$$
이다.

따라서 그 합은
$$
2+3+5+7=17
$$
이다.
