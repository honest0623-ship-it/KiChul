---
id: HN-2025-G2-S1-MID-017
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: '5'
level: 5
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-17
assets:
- assets/original/017_2-2. 삼각함수의 그래프.png
---
## Q
실수 전체의 집합에서 정의된 함수 $f(x)$가 다음 조건을 만족시킨다.

(가) 양수 $a$에 대하여
$$ f(x) = \begin{cases} a\tan\frac{\pi}{2}x & (0 \le x < 1 \text{ 또는 } 1 < x \le 2) \\ 0 & (x = 1) \end{cases} $$
(나) 모든 실수 $x$에 대하여 $f(-x) = f(x)$, $f(x+4) = f(x)$이다.

$0 < x < 10$일 때, $f(x+1) + f(x) = 0$인 모든 근의 개수는?

## Choices
① $5$
② $9$
③ $10$
④ $14$
⑤ $15$

## Answer
④

## Solution
함수 $f(x)$는 주기가 $4$인 우함수이다.
먼저 정수 $x$에 대하여 $f(x)$의 값을 구해보자.
$f(0) = a\tan 0 = 0$
$f(1) = 0$ (조건에 의해)
$f(2) = a\tan\pi = 0$
$f(3) = f(-1) = f(1) = 0$
$f(4) = f(0) = 0$
따라서 모든 정수 $n$에 대하여 $f(n) = 0$이다.
$f(x+1) + f(x) = 0$에 정수 $x$를 대입하면 항상 $0 + 0 = 0$이 성립하므로 모든 정수는 주어진 방정식의 근이다.
$0 < x < 10$ 범위에 있는 정수 근은 $1, 2, 3, 4, 5, 6, 7, 8, 9$로 총 $9$개이다.

이제 정수가 아닌 $x$에 대하여 $f(x+1) = -f(x)$를 만족하는 근을 찾아보자.
$f(x)$의 주기가 $4$이므로 $x \in (0, 4)$ 구간에서 먼저 해를 찾는다.

① $0 < x < 1$일 때
$x+1 \in (1, 2)$이다.
$f(x) = a\tan\frac{\pi}{2}x$
$f(x+1) = a\tan\frac{\pi}{2}(x+1)$
$= a\tan\left(\frac{\pi}{2}x + \frac{\pi}{2}\right) = -a\cot\frac{\pi}{2}x$
$f(x+1) = -f(x)$ 이면 $-a\cot\frac{\pi}{2}x = -a\tan\frac{\pi}{2}x$
$\tan^2\frac{\pi}{2}x = 1$
$0 < x < 1$에서 $\tan\frac{\pi}{2}x > 0$이므로 $\tan\frac{\pi}{2}x = 1$, $\frac{\pi}{2}x = \frac{\pi}{4} \implies x = \frac{1}{2}$

② $1 < x < 2$일 때
$x+1 \in (2, 3)$이다. $x+1-4 = x-3 \in (-2, -1)$
$f(x+1) = f(x-3) = f(3-x)$
$= a\tan\frac{\pi}{2}(3-x)$
$= a\tan\left(\frac{3\pi}{2} - \frac{\pi}{2}x\right) = a\cot\frac{\pi}{2}x$
$f(x) = a\tan\frac{\pi}{2}x$
$f(x+1) = -f(x)$ 이면 $a\cot\frac{\pi}{2}x = -a\tan\frac{\pi}{2}x$
$\tan^2\frac{\pi}{2}x = -1$ 이 되어 실근이 존재하지 않는다.

③ $2 < x < 3$일 때
$x-2 = t$라 하면 $0 < t < 1$이다.
$f(x) = f(t+2) = f(t-2) = f(2-t)$
$= a\tan\frac{\pi}{2}(2-t) = -a\tan\frac{\pi}{2}t$
$f(x+1) = f(t+3) = f(t-1) = f(1-t)$
$= a\tan\frac{\pi}{2}(1-t) = a\cot\frac{\pi}{2}t$
$f(x+1) = -f(x)$ 이면 $a\cot\frac{\pi}{2}t = a\tan\frac{\pi}{2}t$
$\tan^2\frac{\pi}{2}t = 1$
$0 < t < 1$에서 $t = \frac{1}{2}$이므로 $x = \frac{5}{2}$

④ $3 < x < 4$일 때
$x-3 = t$라 하면 $0 < t < 1$이다.
$f(x) = f(t+3) = f(1-t) = a\cot\frac{\pi}{2}t$
$f(x+1) = f(t+4) = f(t) = a\tan\frac{\pi}{2}t$
$f(x+1) = -f(x)$ 이면 $a\tan\frac{\pi}{2}t = -a\cot\frac{\pi}{2}t$
$\tan^2\frac{\pi}{2}t = -1$ 이 되어 실근이 존재하지 않는다.

따라서 구간 $(0, 4]$에서 정수가 아닌 근은 $0.5, 2.5$의 $2$개이다.
주기가 $4$이므로 $0 < x < 10$ 범위에서 정수가 아닌 근은
$0.5, 2.5, 4.5, 6.5, 8.5$ 로 총 $5$개이다.

모든 근의 개수는 정수 근 $9$개와 정수가 아닌 근 $5$개를 합하여 총 $14$개이다.
