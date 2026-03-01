---
id: JJ-2025-G1-S1-Final-006
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 6
source_question_kind: objective
source_question_label: '6'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-02-27
tags:
- 수동정제
- 객관식
- 출제번호-6
assets:
- assets/original/
- assets/original/006.png
---
## Q
두 부등식 $x^2+ax+b\ge 0$, $x^2+cx+d\le 0$을 동시에 만족하는 $x$값의 범위가 $-3\le x\le -1$ 또는 $x=2$로 주어졌다. 이때, 상수 $a,b,c,d$에 대하여 $a^2+b^2+c^2+d^2$의 값은?

## Choices
① 34
② 36
③ 38
④ 40
⑤ 42

## Answer
⑤

## Solution
$x^2+cx+d\le 0$의 해집합은 한 구간이므로
$$
[-3,2]
$$
가 되어야 한다. 따라서
$$
x^2+cx+d=(x+3)(x-2)=x^2+x-6
$$
이어서 $c=1$, $d=-6$이다.

교집합이 $[-3,-1]\cup\{2\}$가 되려면
$$
x^2+ax+b\ge 0
$$
의 해집합이 $(-\infty,-1]\cup[2,\infty)$이어야 하므로
$$
x^2+ax+b=(x+1)(x-2)=x^2-x-2
$$
에서 $a=-1$, $b=-2$이다.

그러므로
$$
a^2+b^2+c^2+d^2=1+4+1+36=42
$$
이다.
