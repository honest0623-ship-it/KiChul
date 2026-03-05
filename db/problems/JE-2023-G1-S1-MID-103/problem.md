---
id: JE-2023-G1-S1-MID-103
school: JE
year: 2023
grade: 1
semester: 1
exam: MID
type: 서답형
source_question_no: 3
source_question_kind: subjective
source_question_label: "서답3번"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-2. 이차방정식과 이차함수"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 서답형
  - 출제번호-서답3
assets:
  - assets/original/
  - assets/original/서답3번_2-2. 이차방정식과 이차함수.png
---

## Q
\(x\)에 대한 이차방정식
\[
x^2-2kx+k^2-k-3=0
\]
의 두 실근을 \(\alpha,\ \beta\)라 할 때,
\[
\alpha^2+\beta^2
\]
의 최댓값과 최솟값을 구하시오.
\[
(-1\le k\le 4)
\]

## Choices

## Answer
최댓값 \(46\), 최솟값 \(\dfrac{11}{2}\)

## Solution
근과 계수의 관계에서
\[
\alpha+\beta=2k,\quad \alpha\beta=k^2-k-3.
\]
따라서
\[
\alpha^2+\beta^2
=(\alpha+\beta)^2-2\alpha\beta
\]
\[
=4k^2-2(k^2-k-3)
=2k^2+2k+6.
\]

이 식을
\[
g(k)=2k^2+2k+6
\]
이라 두면, 위로 열린 이차함수이다.

정점은
\[
k=-\frac{2}{2\cdot 2}=-\frac{1}{2}
\]
이므로 최솟값은
\[
g\!\left(-\frac{1}{2}\right)
=2\cdot\frac14+2\cdot\left(-\frac12\right)+6
=\frac{11}{2}.
\]

최댓값은 구간 끝점에서 비교한다.
\[
g(-1)=6,\quad g(4)=46.
\]
따라서 최댓값은 \(46\), 최솟값은 \(\dfrac{11}{2}\)이다.

