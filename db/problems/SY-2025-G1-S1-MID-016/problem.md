---
id: SY-2025-G1-S1-MID-016
school: SY
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: '2'
level: 2
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-16
assets:
- assets/original/
- assets/original/016.png
---
## Q
삼차식 $f(x)$에 대하여 다항식 $f(x)+8$이 $(x+2)^2$으로 나누어떨어지고, 다항식 $10-f(x)$가 $x^2-1$로 나누어떨어진다. $f(x)$를 $x+3$으로 나누었을 때의 나머지는?

## Choices
① $10$  
② $16$  
③ $22$  
④ $26$  
⑤ $34$

## Answer
④

## Solution
$f(x)=ax^3+bx^2+cx+d$라 하자.
$f(x)+8$이 $(x+2)^2$으로 나누어떨어지므로
$$
f(-2)=-8,\quad f'(-2)=0.
$$
또한 $10-f(x)$가 $x^2-1=(x-1)(x+1)$로 나누어떨어지므로
$$
f(1)=10,\quad f(-1)=10.
$$
이를 식으로 쓰면
$$
-8a+4b-2c+d=-8,\quad 12a-4b+c=0,
$$
$$
a+b+c+d=10,\quad -a+b-c+d=10.
$$
뒤의 두 식에서 $c=-a$이고
$$
b=-\frac{11}{4}c=\frac{11}{4}a
$$
를 얻는다. 이를 첫 식들과 함께 풀면
$$
a=-8,\quad b=-22,\quad c=8,\quad d=32.
$$
따라서
$$
f(-3)=(-8)(-27)+(-22)\cdot9+8(-3)+32=26.
$$
$x+3$으로 나눈 나머지는 $f(-3)=26$이다.
