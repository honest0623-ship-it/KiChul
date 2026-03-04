---
id: BY-2025-G2-S1-MID-014
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: "14"
difficulty: 5
level: 5
unit: "대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프"
unit_l1: "대수(2022개정)"
unit_l2: "2. 삼각함수"
unit_l3: "2-2. 삼각함수의 그래프"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 객관식
  - 출제번호-14
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/014_2-2. 삼각함수의 그래프_3.png
---

## Q
함수 $y=\sin^2x-2\cos x+3$ 의 최댓값을 $M$, 최솟값을 $m$이라고 할 때, $M+m$의 값은?

## Choices
① 6
② 7
③ 9
④ 10
⑤ 11

## Answer
6

## Solution
주어진 함수는 $y=\sin^2x-2\cos x+3$ 입니다.
삼각함수의 관계식 $\sin^2x = 1-\cos^2x$ 를 이용하여 함수를 $\cos x$에 대한 식으로 변환합니다.
$y = (1-\cos^2x) - 2\cos x + 3$
$y = -\cos^2x - 2\cos x + 4$

여기서 $\cos x = t$ 로 치환합니다. $x$가 모든 실수일 때 $\cos x$의 값의 범위는 $-1 \le \cos x \le 1$ 이므로, $t$의 범위는 $-1 \le t \le 1$ 입니다.
함수는 $f(t) = -t^2 - 2t + 4$ 가 됩니다.

이 이차함수의 최댓값과 최솟값을 구하기 위해 완전제곱식으로 변형합니다.
$f(t) = -(t^2 + 2t) + 4$
$f(t) = -(t^2 + 2t + 1 - 1) + 4$
$f(t) = -((t+1)^2 - 1) + 4$
$f(t) = -(t+1)^2 + 1 + 4$
$f(t) = -(t+1)^2 + 5$

이 이차함수는 위로 볼록한 포물선이며, 꼭짓점은 $t=-1$ 입니다.
$t$의 범위는 $[-1, 1]$ 입니다.

1. 최댓값 ($M$):
꼭짓점 $t=-1$이 범위 $[-1, 1]$에 포함되므로, 최댓값은 $t=-1$일 때 발생합니다.
$M = f(-1) = -(-1+1)^2 + 5 = 0 + 5 = 5$

2. 최솟값 ($m$):
위로 볼록한 함수이므로, 꼭짓점에서 멀어질수록 값이 작아집니다. 범위의 양 끝점 중 꼭짓점 $t=-1$에서 더 먼 $t=1$에서 최솟값이 발생합니다.
$m = f(1) = -(1+1)^2 + 5 = -(2)^2 + 5 = -4 + 5 = 1$

따라서, 최댓값 $M=5$ 이고 최솟값 $m=1$ 입니다.

문제에서 요구하는 $M+m$의 값은:
$M+m = 5 + 1 = 6$

그러므로 정답은 6입니다.
