---
id: BY-2024-G1-S1-MID-103
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 3
source_question_kind: subjective
source_question_label: "서답3"
difficulty: 5
level: 5
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-2. 이차방정식과 이차함수"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 서술형
  - 출제번호-3
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답3번_2-2. 이차방정식과 이차함수.png
---

## Q
이차함수 $f(x)=ax^2+bx+4$가 다음 조건을 만족시킨다.

(가) 함수 $f(x)$는 $x=0$에서 최솟값을 갖는다.

(나) 함수 $y=f(x)$의 그래프는 직선 $y=2x$와 접하거나 이 직선보다 항상 위쪽에 있다.

이때 $f(2)$의 최솟값을 구하는 풀이과정을 쓰고 답을 구하시오. (단, $a,\ b$는 실수이다.)

## Choices


## Answer
5

## Solution
(가)에서 $x=0$에서 최솟값을 가지므로 꼭짓점의 $x$좌표가 0이다.
따라서
\[
b=0,\quad f(x)=ax^2+4
\]
이고 최솟값을 가지려면
\[
a>0
\]
이다.

(나)는 모든 $x$에 대하여
\[
f(x)\ge 2x
\]
이므로
\[
ax^2-2x+4\ge 0 \quad (\forall x)
\]
이다.

이 이차식이 모든 실수에서 0 이상이려면 판별식이 0 이하:
\[
(-2)^2-4\cdot a\cdot 4\le 0
\]
\[
4-16a\le 0
\]
\[
a\ge \frac{1}{4}
\]

이제
\[
f(2)=4a+4
\]
이므로 $a\ge \frac14$에서 최솟값은
\[
a=\frac14
\]
일 때이고
\[
f(2)_{\min}=4\cdot \frac14+4=5
\]

따라서 $f(2)$의 최솟값은 5이다.
