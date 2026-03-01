---
id: BY-2025-G1-S1-MID-102
school: BY
year: 2025
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-02-27
tags:
- 서답형-단답형
- 출제번호-2
assets:
- assets/original/
- assets/original/서답2번.png
---
## Q
다항식 $f(x), g(x)$에 대하여 $f(x)$의 최고차항의 계수가 $3$이고, $f(x)$를 $g(x)$로 나누었을 때의 몫과 나머지가 모두 $g(x)-3x$라 하자. $f(x)g(x)$를 $3x-1$로 나누었을 때의 몫을 $Q(x)$, 나머지를 $R$이라 할 때, $Q(0)+R$의 값을 구하시오.

## Choices


## Answer
10

## Solution
$f(x)$를 $g(x)$로 나누었을 때 몫과 나머지가 모두 $g(x)-3x$이므로
$$
f(x)=g(x)\{g(x)-3x\}+\{g(x)-3x\}.
$$
여기서 나머지의 차수는 $g(x)$의 차수보다 작아야 하므로
$$
\deg(g(x)-3x)<\deg g(x)
$$
이다. 따라서 $g(x)$는 일차식이고 $x$의 계수가 $3$이어야 한다.

$$
g(x)=3x+c \Rightarrow g(x)-3x=c.
$$
그러면 몫과 나머지는 모두 상수 $c$이고
$$
f(x)=g(x)\cdot c + c = c(g(x)+1)=c(3x+c+1).
$$
$f(x)$의 최고차항 계수가 $3$이므로 $3c=3$, 즉 $c=1$.
따라서
$$
g(x)=3x+1,\quad f(x)=3x+2.
$$

그러므로
$$
f(x)g(x)=(3x+2)(3x+1)=9x^2+9x+2.
$$
이를 $3x-1$로 나누면
$$
9x^2+9x+2=(3x-1)(3x+4)+6.
$$
따라서
$$
Q(x)=3x+4,\ R=6.
$$
그러므로
$$
Q(0)+R=4+6=10.
$$
