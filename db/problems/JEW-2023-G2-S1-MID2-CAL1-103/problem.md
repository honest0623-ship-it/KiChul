---
id: JEW-2023-G2-S1-MID2-CAL1-103
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 서답형(단답형)
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3번
difficulty: 5
level: 5
unit: 미적분 I(2022개정)>1. 함수의 극한과 연속>1-1. 함수의 극한
unit_l1: 미적분 I(2022개정)
unit_l2: 1. 함수의 극한과 연속
unit_l3: 1-1. 함수의 극한
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답3번
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-103_original.png
---

## Q
$$
\lim_{x\to -a}\frac{x^2-a^2}{x^3+a^3}=2,\qquad
\lim_{x\to\infty}\left(\frac{\sqrt{x^2+2x+x}}{bx+1}\right)=1
$$
일 때, $a+b$의 값을 구하시오.
(단, $a,b$는 상수)

## Choices


## Answer
$\dfrac{2}{3}$

## Solution
먼저
$$
x^2-a^2=(x+a)(x-a),\qquad
x^3+a^3=(x+a)(x^2-ax+a^2)
$$
이므로
$$
\frac{x^2-a^2}{x^3+a^3}=\frac{x-a}{x^2-ax+a^2}
$$
이다.

따라서
$$
\lim_{x\to -a}\frac{x^2-a^2}{x^3+a^3}
=\frac{-a-a}{(-a)^2-(-a)a+a^2}
=\frac{-2a}{3a^2}
=-\frac{2}{3a}
$$
이다.

이 값이 2이므로
$$
-\frac{2}{3a}=2
$$
에서
$$
a=-\frac13
$$
이다.

또
$$
\sqrt{x^2+2x+x}=\sqrt{x^2+3x}
$$
이고, $x\to\infty$일 때 분자와 분모를 $x$로 나누어 생각하면
$$
\lim_{x\to\infty}\frac{\sqrt{x^2+3x}}{bx+1}
=\lim_{x\to\infty}\frac{x\sqrt{1+\frac{3}{x}}}{x\left(b+\frac{1}{x}\right)}
=\frac{1}{b}
$$
이다.

이 값이 1이므로
$$
b=1
$$
이다.

따라서
$$
a+b=-\frac13+1=\frac23
$$
이다.
