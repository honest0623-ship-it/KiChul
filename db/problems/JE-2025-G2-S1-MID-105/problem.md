---
id: JE-2025-G2-S1-MID-105
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-5
assets:
- assets/original/
- assets/original/서답5번_1-2. 지수함수.png
---
## Q
방정식
$$
9^x-2(a+4)3^x-3a^2+24a=0
$$
의 서로 다른 두 근이 모두 양수가 되도록 하는 정수 $a$값의 합을 구하는 과정을 서술하시오.

## Choices

## Answer
$19$

## Solution
$$
t=3^x\ (t>0)
$$
로 두면
$$
t^2-2(a+4)t-3a^2+24a=0
$$
이다.

이 식은
$$
t^2-2(a+4)t+3a(8-a)=0
$$
이므로
$$
(t-3a)\{t-(8-a)\}=0
$$
로 인수분해된다.

따라서
$$
t=3a,\qquad t=8-a
$$
이다.

원래 방정식의 두 근 $x$가 서로 다르고 모두 양수이려면,
$t=3^x$는 서로 다르고 모두 $1$보다 커야 하므로
$$
3a>1,\quad 8-a>1,\quad 3a\ne 8-a
$$
가 필요충분하다.

정수 $a$에 대해 풀면
$$
a\ge 1,\quad a\le 6,\quad a\ne 2
$$
이므로
$$
a=1,3,4,5,6
$$
이다.

합은
$$
1+3+4+5+6=19
$$
이다.
