---
id: JJ-2024-G1-S1-MID-105
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-03-04
tags:
- 자동입력
- 서술형
- 출제번호-5
- manual-fix
assets:
- assets/original/
- assets/original/서답5번_1-2. 나머지정리.png
---

## Q
$x$에 대한 다항식
$f(x)=a_0+a_1x+a_2x^2+\cdots+a_{10}x^{10}$이 다음 조건을 만족한다.

(가) $a_0+a_2+a_4+a_6+a_8+a_{10}=2$
(나) $a_1+a_3+a_5+a_7+a_9=1$

다항식 $f(x)$를 $x^2-1$로 나눈 나머지를 구하시오.
(단, $a_0,a_1,\ldots,a_{10}$은 상수이다.)

## Choices


## Answer
$x+2$

## Solution
$x^2-1=(x-1)(x+1)$로 나눈 나머지를 $r(x)=px+q$라 두자.

$f(1)=a_0+a_1+\cdots+a_{10}=2+1=3$,
$f(-1)=(\text{짝수차 계수합})-(\text{홀수차 계수합})=2-1=1$.

따라서
$r(1)=p+q=3$,
$r(-1)=-p+q=1$.

연립하면
$q=2,\;p=1$.

그러므로 나머지는
$r(x)=x+2$이다.
