---
id: JJ-2024-G1-S1-MID-013
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-04
tags:
- 자동입력
- 객관식
- 출제번호-13
- manual-fix
assets:
- assets/original/
- assets/original/013_2-2. 이차방정식과 이차함수.png
---

## Q
[문항 오류 정정] 원문의 정정 조건을 반영하여, $d$는 상수로 본다.

이차함수 $y=x^2-kx+k+6$의 그래프가 $x$축과 만나는 두 점 사이의 거리를 $d$라 할 때, 모든 실수 $k$값의 곱이 $-60$이 되도록 하는 양수 $d$의 값을 구하시오.

## Choices
① $5$
② $6$
③ $7$
④ $8$
⑤ $9$

## Answer
②

## Solution
$x$축과 만나는 두 점의 $x$좌표를 $x_1,x_2$라 하면
$d=|x_1-x_2|=\sqrt{(x_1+x_2)^2-4x_1x_2}$.

여기서
$x_1+x_2=k$, $x_1x_2=k+6$이므로
$d^2=k^2-4(k+6)=(k-2)^2-28$.

따라서
$(k-2)^2=d^2+28$
$k=2\pm\sqrt{d^2+28}$.

이 두 실수 $k$의 곱은
$\left(2+\sqrt{d^2+28}\right)\left(2-\sqrt{d^2+28}\right)$
$=4-(d^2+28)=-d^2-24$.

이 값이 $-60$이므로
$-d^2-24=-60\Rightarrow d^2=36$.

양수 $d=6$.
정답은 ②이다.
