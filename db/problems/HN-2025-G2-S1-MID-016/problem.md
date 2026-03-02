---
id: HN-2025-G2-S1-MID-016
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: '3'
level: 3
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-16
assets:
- assets/original/016_2-2. 삼각함수의 그래프.png
---
## Q
양수 $a$와 상수 $b$에 대하여 두 함수
$$ f(x) = 3\sin\left(ax + \frac{\pi}{4}\right), \quad g(x) = \log_{\frac{1}{2}}x - b $$
가 다음 조건을 만족시킨다.

(가) 모든 실수 $x$에 대하여 $f(x+t) = f(x)$를 만족시키는 가장 작은 양수 $t$는 $\pi$이다.
(나) 함수 $y = g(x)$의 그래프는 점 $(2, -4)$를 지난다.

$0 \le x \le \frac{\pi}{4}$에서 정의된 함수 $(g \circ f)(x)$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M - m$의 값은?

## Choices
① $\frac{1}{2}$
② $\frac{\sqrt{2}}{2}$
③ $\sqrt{2}$
④ $2\sqrt{2}$
⑤ $4$

## Answer
①

## Solution
조건 (가)에서 함수 $f(x)$의 주기가 $\pi$이므로
$$ \frac{2\pi}{|a|} = \pi $$
양수 $a$에 대하여 $a = 2$이다.
따라서 $f(x) = 3\sin\left(2x + \frac{\pi}{4}\right)$이다.

조건 (나)에서 $y = g(x)$의 그래프가 $(2, -4)$를 지나므로
$$ g(2) = \log_{\frac{1}{2}}2 - b = -4 $$
$$ -1 - b = -4 \implies b = 3 $$
따라서 $g(x) = \log_{\frac{1}{2}}x - 3$이다.

$0 \le x \le \frac{\pi}{4}$일 때, $\theta = 2x + \frac{\pi}{4}$라 하면
$$ 0 \le 2x \le \frac{\pi}{2} \implies \frac{\pi}{4} \le 2x + \frac{\pi}{4} \le \frac{3\pi}{4} $$
이 구간에서 $\sin\theta$의 값의 범위는 $\frac{\sqrt{2}}{2} \le \sin\theta \le 1$이다.
따라서 $f(x) = 3\sin\theta$의 값의 범위는
$$ \frac{3\sqrt{2}}{2} \le f(x) \le 3 $$
이다.

함수 $(g \circ f)(x) = g(f(x))$의 최댓값과 최솟값을 구하기 위해 $f(x) = t$라 하면 $t$의 범위는 $\frac{3\sqrt{2}}{2} \le t \le 3$이다.
$g(t) = \log_{\frac{1}{2}}t - 3$에서 밑이 $\frac{1}{2}$로 $1$보다 작으므로 $g(t)$는 감소함수이다.
따라서 $t = \frac{3\sqrt{2}}{2}$일 때 최댓값 $M$을, $t = 3$일 때 최솟값 $m$을 갖는다.
$$ M = g\left(\frac{3\sqrt{2}}{2}\right) = \log_{\frac{1}{2}}\left(\frac{3\sqrt{2}}{2}\right) - 3 $$
$$ m = g(3) = \log_{\frac{1}{2}}3 - 3 $$
따라서 $M - m$의 값은
$$ M - m = \left( \log_{\frac{1}{2}}\left(\frac{3\sqrt{2}}{2}\right) - 3 \right) - \left( \log_{\frac{1}{2}}3 - 3 \right) $$
$$ = \log_{\frac{1}{2}}\left(\frac{3\sqrt{2}}{2}\right) - \log_{\frac{1}{2}}3 $$
$$ = \log_{\frac{1}{2}}\left( \frac{\frac{3\sqrt{2}}{2}}{3} \right) = \log_{\frac{1}{2}}\left(\frac{\sqrt{2}}{2}\right) $$
이때 $\frac{\sqrt{2}}{2} = \frac{1}{\sqrt{2}} = \left(\frac{1}{2}\right)^{\frac{1}{2}}$이므로
$$ M - m = \log_{\frac{1}{2}}\left(\frac{1}{2}\right)^{\frac{1}{2}} = \frac{1}{2} $$
이다.
