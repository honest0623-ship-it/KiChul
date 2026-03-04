---
id: BY-2025-G2-S1-MID-103
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 3
source_question_kind: subjective
source_question_label: "서답3"
difficulty: 5
level: 5
unit: "대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프"
unit_l1: "대수(2022개정)"
unit_l2: "2. 삼각함수"
unit_l3: "2-2. 삼각함수의 그래프"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 서술형
  - 출제번호-3
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답3번_2-2. 삼각함수의 그래프.png
---

## Q
부등식 $4\sin^2(\pi-\theta)+4\sin\left(\frac{\pi}{2}+\theta\right)-2+k \le 0$ 가 모든 실수 $\theta$에 대하여 항상 성립하도록 하는 실수 $k$의 최댓값을 구하는 풀이과정을 쓰고 답을 구하시오.

## Choices


## Answer
-3

## Solution
주어진 부등식 $4\sin^2(\pi-\theta)+4\sin\left(\frac{\pi}{2}+\theta\right)-2+k \le 0$ 를 정리한다.
삼각함수의 성질에 의해 $\sin(\pi-\theta) = \sin\theta$ 이고 $\sin\left(\frac{\pi}{2}+\theta\right) = \cos\theta$ 이므로,
$4\sin^2\theta + 4\cos\theta - 2 + k \le 0$
$\sin^2\theta = 1-\cos^2\theta$ 이므로,
$4(1-\cos^2\theta) + 4\cos\theta - 2 + k \le 0$
$4 - 4\cos^2\theta + 4\cos\theta - 2 + k \le 0$
$-4\cos^2\theta + 4\cos\theta + 2 + k \le 0$

$\cos\theta = t$ 로 치환하면, $-1 \le t \le 1$ 이다.
부등식은 $-4t^2 + 4t + 2 + k \le 0$ 이 된다.
이 부등식이 모든 실수 $\theta$에 대하여 항상 성립하려면, $-1 \le t \le 1$ 범위에서 함수 $f(t) = -4t^2 + 4t + 2$ 의 최댓값이 $-k$ 보다 작거나 같아야 한다. 즉, $f(t)_{\text{max}} \le -k$ 이다.
또는 $k \le 4t^2 - 4t - 2$ 이므로, $k$는 $g(t) = 4t^2 - 4t - 2$ 의 최솟값보다 작거나 같아야 한다. 즉, $k \le g(t)_{\text{min}}$ 이다.

$g(t) = 4t^2 - 4t - 2$ 의 최솟값을 구한다.
$g(t) = 4(t^2 - t) - 2 = 4\left(t - \frac{1}{2}\right)^2 - 4\left(\frac{1}{4}\right) - 2 = 4\left(t - \frac{1}{2}\right)^2 - 1 - 2 = 4\left(t - \frac{1}{2}\right)^2 - 3$
이 이차함수는 아래로 볼록하며, 꼭짓점의 $t$ 좌표는 $t = \frac{1}{2}$ 이다.
정의역이 $[-1, 1]$ 이고, $t = \frac{1}{2}$ 은 이 범위 안에 포함된다.
따라서 $g(t)$의 최솟값은 $t = \frac{1}{2}$ 일 때 $g\left(\frac{1}{2}\right) = 4\left(\frac{1}{2} - \frac{1}{2}\right)^2 - 3 = -3$ 이다.

부등식 $k \le g(t)$ 가 항상 성립하려면 $k$는 $g(t)$의 최솟값보다 작거나 같아야 한다.
$k \le -3$
따라서 실수 $k$의 최댓값은 $-3$ 이다.
