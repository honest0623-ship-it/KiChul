---
id: JEW-2025-G1-S1-FINAL-018
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-18
assets:
- assets/original/
- assets/original/018.png
---
## Q
$x$에 대한 삼차방정식
$$
x^3-(2a+1)x^2+(a^2-a)x+a^2+a+2=0
$$
의 서로 다른 세 근을 $\alpha,\beta,\gamma$라 하자. $\alpha^2+\beta^2=10$을 만족하는 모든 실수 $a$값의 합은?

## Choices
① 2
② 3
③ 4
④ -5
⑤ -6

## Answer
①

## Solution
식은
$$
(x+1)\left(x^2-2(a+1)x+a^2+a+2\right)
$$
로 인수분해되므로 한 근은 항상 $-1$이다.

$\alpha^2+\beta^2=10$이 되려면 두 경우를 본다.

1) $\alpha,\beta$가 이차식의 두 근인 경우
$$
\alpha+\beta=2(a+1),\quad \alpha\beta=a^2+a+2
$$
이므로
$$
\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=2a^2+6a=10
$$
즉
$$
a^2+3a-5=0
$$
이다.

2) $\alpha,\beta$ 중 하나가 $-1$인 경우
다른 근을 $t$라 하면
$$
1+t^2=10
$$
이므로 $t=3$ 또는 $t=-3$이다.

$t=3$을 이차식에 대입하면
$$
a^2-5a+5=0
$$
이고, $t=-3$은
$$
a^2+7a+17=0
$$
이라 실수해가 없다.

따라서 가능한 실수 $a$는 $a^2+3a-5=0$, $a^2-5a+5=0$의 실근들이다.
실근의 합은
$$
(-3)+5=2
$$
이다.
