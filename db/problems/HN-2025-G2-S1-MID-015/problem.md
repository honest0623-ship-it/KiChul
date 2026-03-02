---
id: HN-2025-G2-S1-MID-015
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: '4'
level: 4
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-15
assets:
- assets/original/015_2-2. 삼각함수의 그래프.png
---
## Q
$0 < t < 2\pi$인 실수 $t$에 대하여 함수
$$ f(x) = \begin{cases} \sin x - \sin t & (0 \le x \le t) \\ \sin t - \sin x & (t < x \le 2\pi) \end{cases} $$
의 최댓값을 $M(t)$, 최솟값을 $m(t)$라 하자. $M(t) - m(t) = 3$을 만족하는 $t$의 합은?

## Choices
① $\pi$
② $2\pi$
③ $3\pi$
④ $4\pi$
⑤ $5\pi$

## Answer
②

## Solution
$c = \sin t$라 하자. 함수 $f(x)$의 구간에 따른 최댓값과 최솟값을 구해보자.

(i) $t = \frac{\pi}{2}$일 때, $\sin t = 1$
$0 \le x \le \frac{\pi}{2}$에서 $f(x) = \sin x - 1$이므로 최댓값은 $0$, 최솟값은 $-1$이다.
$\frac{\pi}{2} < x \le 2\pi$에서 $f(x) = 1 - \sin x$이므로 최댓값은 $1 - (-1) = 2$, 최솟값은 $1 - 1 = 0$이다.
전체 최댓값 $M = 2$, 최솟값 $m = -1$이 되어 $M - m = 3$을 만족한다.

(ii) $t = \frac{3\pi}{2}$일 때, $\sin t = -1$
$0 \le x \le \frac{3\pi}{2}$에서 $f(x) = \sin x + 1$이므로 최댓값은 $1 + 1 = 2$, 최솟값은 $-1 + 1 = 0$이다.
$\frac{3\pi}{2} < x \le 2\pi$에서 $f(x) = -1 - \sin x$이므로 최댓값은 $-1 - (-1) = 0$, 최솟값은 $-1 - 0 = -1$이다.
전체 최댓값 $M = 2$, 최솟값 $m = -1$이 되어 $M - m = 3$을 만족한다.

(iii) 그 외의 $t$일 때
$0 < t < \pi$ ($t \neq \frac{\pi}{2}$)인 경우, $0 < c < 1$이다. 이 구간에서 $f(x)$의 최댓값은 $c + 1$, 최솟값은 $-c$ 또는 $c-1$이다. 만약 $M - m = 3$이려면 $c + 1 - (-c) = 3 \implies c = 1$이 되어야 하므로 모순이다.
$\pi < t < 2\pi$ ($t \neq \frac{3\pi}{2}$)인 경우, $-1 < c < 0$이다. 이 구간에서 $f(x)$의 최댓값은 $1 - c$, 최솟값은 $c$ 또는 $-1-c$이다. 만약 $M - m = 3$이려면 $1 - c - c = 3 \implies c = -1$이 되어야 하므로 모순이다.

따라서 조건을 만족하는 $t$의 값은 $\frac{\pi}{2}, \frac{3\pi}{2}$이며, 모든 $t$의 합은 $\frac{\pi}{2} + \frac{3\pi}{2} = 2\pi$이다.
