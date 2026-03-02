---
id: HN-2025-G2-S1-MID-014
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: '3'
level: 3
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-14
assets:
- assets/original/014_2-2. 삼각함수의 그래프.png
---
## Q
모든 실수 $x$에 대하여 부등식 $\cos^2x + 4\sin x - a + 2 \ge 0$이 항상 성립하도록 하는 실수 $a$의 최댓값은?

## Choices
① $-2$
② $-1$
③ $0$
④ $1$
⑤ $2$

## Answer
①

## Solution
주어진 부등식의 $\cos^2x$를 $1 - \sin^2x$로 바꾸면
$$ (1 - \sin^2x) + 4\sin x - a + 2 \ge 0 $$
$$ -\sin^2x + 4\sin x + 3 - a \ge 0 $$
$\sin x = t$라 하면 모든 실수 $x$에 대하여 $-1 \le t \le 1$이다.
주어진 부등식은 $t$에 대한 부등식
$$ -t^2 + 4t + 3 - a \ge 0 $$
$$ t^2 - 4t - 3 + a \le 0 $$
로 나타낼 수 있고, 이 부등식이 $-1 \le t \le 1$인 모든 $t$에 대하여 항상 성립해야 한다.
$f(t) = t^2 - 4t - 3 + a$라 하면
$$ f(t) = (t - 2)^2 - 7 + a $$
이다.
구간 $[-1, 1]$에서 함수 $f(t)$는 감소하므로 $t = -1$일 때 최댓값을 갖는다.
모든 $t \in [-1, 1]$에 대하여 $f(t) \le 0$이 항상 성립하려면 구간 내에서의 함수 $f(t)$의 최댓값이 $0$ 이하이어야 하므로
$$ f(-1) = (-1)^2 - 4(-1) - 3 + a = a + 2 \le 0 $$
$$ a \le -2 $$
따라서 실수 $a$의 최댓값은 $-2$이다.
