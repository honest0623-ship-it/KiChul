---
id: BY-2025-G2-S1-MID-018
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: "18"
difficulty: 4
level: 4
unit: "대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프"
unit_l1: "대수(2022개정)"
unit_l2: "2. 삼각함수"
unit_l3: "2-2. 삼각함수의 그래프"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 객관식
  - 출제번호-18
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/018_2-2. 삼각함수의 그래프.png
---

## Q
두 점 O(0, 0), A($\pi$, 0)을 이은 선분 OA를 16등분 한 점을 차례로 P$_1$, P$_2$, ..., P$_{15}$라고 하자.
점 P$_k$(k=1, 2, ..., 15)를 지나 $x$축에 수직인 직선과 함수 $y=\sqrt{2}\sin x$의 그래프의 교점을 Q$_k$라고 할 때,
$\overline{\text{P}_1\text{Q}_1}^2 + \overline{\text{P}_2\text{Q}_2}^2 + \cdots + \overline{\text{P}_{15}\text{Q}_{15}}^2$의 값은?

## Choices
① 13
② 14
③ 15
④ 16
⑤ 17

## Answer
16

## Solution
두 점 O(0, 0)과 A($\pi$, 0)을 이은 선분 OA를 16등분 한 점 P$_k$의 $x$좌표는 $x_k = k \frac{\pi}{16}$ ($k=1, 2, \dots, 15$)입니다. 따라서 P$_k = (k \frac{\pi}{16}, 0)$입니다.

점 P$_k$를 지나 $x$축에 수직인 직선은 $x = k \frac{\pi}{16}$입니다. 이 직선과 함수 $y=\sqrt{2}\sin x$의 그래프의 교점을 Q$_k$라고 했으므로, Q$_k$의 좌표는 $(k \frac{\pi}{16}, \sqrt{2}\sin(k \frac{\pi}{16}))$입니다.

선분 P$_k$Q$_k$의 길이는 Q$_k$의 $y$좌표의 절댓값과 같습니다. 즉, $\overline{\text{P}_k\text{Q}_k} = |\sqrt{2}\sin(k \frac{\pi}{16})|$입니다.
$k=1, 2, \dots, 15$일 때, $k \frac{\pi}{16}$는 $(0, \pi)$ 범위에 있으므로 $\sin(k \frac{\pi}{16}) > 0$입니다.
따라서 $\overline{\text{P}_k\text{Q}_k} = \sqrt{2}\sin(k \frac{\pi}{16})$입니다.

우리가 구해야 하는 값은 $\sum_{k=1}^{15} \overline{\text{P}_k\text{Q}_k}^2$입니다.
$\overline{\text{P}_k\text{Q}_k}^2 = (\sqrt{2}\sin(k \frac{\pi}{16}))^2 = 2\sin^2(k \frac{\pi}{16})$입니다.

삼각함수 항등식 $\sin^2 \theta = \frac{1 - \cos(2\theta)}{2}$를 이용하면:
$2\sin^2(k \frac{\pi}{16}) = 2 \cdot \frac{1 - \cos(2k \frac{\pi}{16})}{2} = 1 - \cos(k \frac{\pi}{8})$

따라서 구하는 합은:
$\sum_{k=1}^{15} (1 - \cos(k \frac{\pi}{8})) = \sum_{k=1}^{15} 1 - \sum_{k=1}^{15} \cos(k \frac{\pi}{8})$
$= 15 - \sum_{k=1}^{15} \cos(k \frac{\pi}{8})$

이제 $\sum_{k=1}^{15} \cos(k \frac{\pi}{8})$의 값을 계산합니다.
이 합은 다음과 같이 전개할 수 있습니다:
$\cos(\frac{\pi}{8}) + \cos(\frac{2\pi}{8}) + \dots + \cos(\frac{7\pi}{8}) + \cos(\frac{8\pi}{8}) + \cos(\frac{9\pi}{8}) + \dots + \cos(\frac{15\pi}{8})$

여기서 $\cos(\frac{8\pi}{8}) = \cos(\pi) = -1$입니다.
또한, $\cos(\pi + \theta) = -\cos(\theta)$이므로:
$\cos(\frac{9\pi}{8}) = \cos(\pi + \frac{\pi}{8}) = -\cos(\frac{\pi}{8})$
$\cos(\frac{10\pi}{8}) = \cos(\pi + \frac{2\pi}{8}) = -\cos(\frac{2\pi}{8})$
... 
$\cos(\frac{15\pi}{8}) = \cos(\pi + \frac{7\pi}{8}) = -\cos(\frac{7\pi}{8})$

따라서, $\sum_{k=1}^{15} \cos(k \frac{\pi}{8})$는 다음과 같이 계산됩니다:
$(\cos(\frac{\pi}{8}) + \dots + \cos(\frac{7\pi}{8})) + \cos(\pi) + (-\cos(\frac{\pi}{8}) - \dots - \cos(\frac{7\pi}{8}))$
$= (\sum_{k=1}^{7} \cos(k \frac{\pi}{8})) - 1 - (\sum_{k=1}^{7} \cos(k \frac{\pi}{8}))$
$= -1$

최종적으로 구하는 값은 $15 - (-1) = 15 + 1 = 16$입니다.

정답은 16입니다.
