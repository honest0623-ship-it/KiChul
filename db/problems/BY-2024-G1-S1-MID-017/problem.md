---
id: BY-2024-G1-S1-MID-017
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: "17"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 객관식
  - 출제번호-17
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/017_2-1. 복소수와 이차방정식.png
---

## Q
이차방정식 $x^2+ax+b=0$이 다음 조건을 만족시킨다.

(가) $a$는 자연수이고 $b$는 $b\le 0$인 정수이다.

(나) $(\alpha-\beta)^2\le 10$인 서로 다른 두 실근 $\alpha,\beta$를 갖는다.

$a+b^2$의 최댓값과 최솟값의 합은?

## Choices
① 4
② 5
③ 6
④ 7
⑤ 8

## Answer
6

## Solution
이차방정식의 두 근을 $\alpha,\beta$라 하면
\[
(\alpha-\beta)^2=(\alpha+\beta)^2-4\alpha\beta=a^2-4b
\]
이므로 조건 (나)는
\[
0<a^2-4b\le 10
\]
이다. (서로 다른 두 실근이므로 $a^2-4b>0$)

또 $b\le 0$이므로 $-4b\ge 0$, 따라서
\[
a^2\le a^2-4b\le 10
\]
이어서
\[
a=1,2,3
\]

각 경우의 $b$를 구하면:

- $a=1$:
\[
0<1-4b\le 10 \Rightarrow -2\le b\le 0
\]
즉 $b=-2,-1,0$

- $a=2$:
\[
0<4-4b\le 10 \Rightarrow -1\le b\le 0
\]
즉 $b=-1,0$

- $a=3$:
\[
0<9-4b\le 10 \Rightarrow b=0
\]

가능한 $(a,b)$에서
\[
a+b^2
\]
의 값은
\[
5,\ 2,\ 1,\ 3,\ 2,\ 3
\]
이므로 최댓값은 $5$, 최솟값은 $1$.

따라서 그 합은
\[
5+1=6
\]
정답은 ③이다.
