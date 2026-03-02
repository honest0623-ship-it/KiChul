---
id: JJ-2025-G1-S1-MID-104
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '3'
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-4
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답4번.png
level: 3
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
---
## Q
다항식 $P(x)$를 $x^2-1$로 나누었을 때 나머지가 $x+3$이고, $x^2-4$로 나누었을 때 나머지가 $x$이다. $P(x)$를 $x^2+x-2$으로 나누었을 때, 나머지를 구하시오.

## Choices


## Answer
$2x+2$

## Solution
$x^2+x-2=(x-1)(x+2)$로 나눈 나머지를
$$
R(x)=ax+b
$$
라 두자.

주어진 조건에서
$P(x)$를 $x^2-1$로 나눈 나머지가 $x+3$
이므로 $x=1$을 대입하면
$$
P(1)=1+3=4.
$$
또
$P(x)$를 $x^2-4$로 나눈 나머지가 $x$
이므로 $x=-2$를 대입하면
$$
P(-2)=-2.
$$

한편 $P(x)$를 $x^2+x-2$로 나눌 때
$$
P(x)=(x^2+x-2)Q(x)+R(x)
$$
이므로
$$
R(1)=P(1)=4,\quad R(-2)=P(-2)=-2.
$$
즉
$$
a+b=4,\quad -2a+b=-2.
$$
연립하면
$$
a=2,\quad b=2.
$$
따라서 나머지는
$$
R(x)=2x+2.
$$
