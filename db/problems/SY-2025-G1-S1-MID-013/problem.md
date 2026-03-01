---
id: SY-2025-G1-S1-MID-013
school: SY
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-13
assets:
- assets/original/
- assets/original/013.png
---
## Q
이차방정식 $x^2+2x-2=0$의 두 근을 $\alpha,\beta$라 할 때, 두 수 $\dfrac{1}{2\alpha^2+6\alpha-1}$, $\dfrac{1}{2\beta^2+6\beta-1}$을 근으로 하고 $x^2$의 계수가 1인 이차방정식을 $f(x)$라 할 때, $f(1)$의 값은?

## Choices
① $\dfrac{2}{5}$  
② $\dfrac{2}{3}$  
③ $\dfrac{5}{7}$  
④ $1$  
⑤ $\dfrac{12}{11}$

## Answer
⑤

## Solution
$\alpha,\beta$는 $x^2+2x-2=0$의 근이므로 $\alpha+\beta=-2$, $\alpha\beta=-2$이다.
$\alpha^2=-2\alpha+2$이므로
$$
2\alpha^2+6\alpha-1=2(-2\alpha+2)+6\alpha-1=2\alpha+3
$$
이고 같은 방식으로 $2\beta^2+6\beta-1=2\beta+3$이다.
새 이차방정식의 근을
$$
r_1=\frac{1}{2\alpha+3},\quad r_2=\frac{1}{2\beta+3}
$$
라 하면
$$
r_1+r_2=\frac{2(\alpha+\beta)+6}{(2\alpha+3)(2\beta+3)}=\frac{-4+6}{4\alpha\beta+6(\alpha+\beta)+9}=\frac{2}{-11}=-\frac{2}{11},
$$
$$
r_1r_2=\frac{1}{(2\alpha+3)(2\beta+3)}=\frac{1}{-11}=-\frac{1}{11}.
$$
따라서
$$
f(x)=x^2-(r_1+r_2)x+r_1r_2=x^2+\frac{2}{11}x-\frac{1}{11}
$$
이고
$$
f(1)=1+\frac{2}{11}-\frac{1}{11}=\frac{12}{11}.
$$
