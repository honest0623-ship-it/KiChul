---
id: JEW-2023-G2-S1-MID2-CAL1-008
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: 8
difficulty: 3
level: 3
unit: 미적분 I(2022개정)>1. 함수의 극한과 연속>1-1. 함수의 극한
unit_l1: 미적분 I(2022개정)
unit_l2: 1. 함수의 극한과 연속
unit_l3: 1-1. 함수의 극한
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-8
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-008_original.png
---

## Q
함수 $f(x)$가 모든 실수 $x$에 대하여
$$
2x\le f(x)\le 2x+1
$$
을 만족시킬 때,
$$
\lim_{x\to\infty}\frac{x f(x)}{x^2+5}
$$
의 값은?

## Choices
① $\dfrac{1}{2}$
② $1$
③ $0$
④ $2$
⑤ $3$

## Answer
④

## Solution
주어진 부등식에 $x>0$를 곱하면
$$
2x^2\le x f(x)\le 2x^2+x
$$
이다.

따라서
$$
\frac{2x^2}{x^2+5}\le \frac{x f(x)}{x^2+5}\le \frac{2x^2+x}{x^2+5}
$$
이다.

이때
$$
\lim_{x\to\infty}\frac{2x^2}{x^2+5}=2,\qquad
\lim_{x\to\infty}\frac{2x^2+x}{x^2+5}=2
$$
이므로 샌드위치 정리에 의하여
$$
\lim_{x\to\infty}\frac{x f(x)}{x^2+5}=2
$$
이다.
