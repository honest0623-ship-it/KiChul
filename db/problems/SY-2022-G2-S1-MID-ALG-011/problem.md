---
id: SY-2022-G2-S1-MID-ALG-011
school: SY
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: objective
source_question_no: 11
source_question_kind: objective
source_question_label: '11'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-11
- 과목-ALG
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID-ALG-011_original.png
---

## Q
$x>0$, $y>0$일 때, $\log_4\left(x+\dfrac{1}{y}\right)+\log_4\left(y+\dfrac{9}{x}\right)$의 최솟값은?

## Choices
① $\dfrac{3}{2}$
② $2$
③ $3$
④ $\dfrac{7}{2}$
⑤ $4$

## Answer
②

## Solution
로그의 성질로
\[
\log_4\left(x+\frac{1}{y}\right)+\log_4\left(y+\frac{9}{x}\right)
=\log_4\left\{\left(x+\frac{1}{y}\right)\left(y+\frac{9}{x}\right)\right\}
\]
이다.

곱을 전개하면
\[
\left(x+\frac{1}{y}\right)\left(y+\frac{9}{x}\right)
=xy+10+\frac{9}{xy}
\]
이다.

$xy>0$이므로 산술평균과 기하평균의 관계에 의해
\[
xy+\frac{9}{xy}\ge 2\sqrt{9}=6
\]
이다.

따라서
\[
xy+10+\frac{9}{xy}\ge 16
\]
이므로 최솟값은
\[
\log_4 16=2
\]
이다.
