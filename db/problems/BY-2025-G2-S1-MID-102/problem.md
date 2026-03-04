---
id: BY-2025-G2-S1-MID-102
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 2
source_question_kind: subjective
source_question_label: "서답2"
difficulty: 5
level: 5
unit: "대수(2022개정)>2. 삼각함수>2-1. 삼각함수"
unit_l1: "대수(2022개정)"
unit_l2: "2. 삼각함수"
unit_l3: "2-1. 삼각함수"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 서술형
  - 출제번호-2
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답2번_2-1. 삼각함수.png
---

## Q
이차방정식 $x^2 - k = 0$이 서로 다른 두 실근 $4\cos\theta$, $6\tan\theta$를 가질 때, 상수 $k^2$의 값을 구하시오.

## Choices


## Answer
144

## Solution
이차방정식 $x^2 - k = 0$의 두 실근을 $\alpha, \beta$라고 하면, 근과 계수의 관계에 의해
$\alpha + \beta = 0$
$\alpha \beta = -k$

주어진 두 실근은 $4\cos\theta$와 $6\tan\theta$이므로,

1. 두 근의 합:
$4\cos\theta + 6\tan\theta = 0$
$4\cos\theta + 6\frac{\sin\theta}{\cos\theta} = 0$
양변에 $\cos\theta$를 곱하면 (단, $\cos\theta \neq 0$):
$4\cos^2\theta + 6\sin\theta = 0$
$\cos^2\theta = 1 - \sin^2\theta$를 대입하면:
$4(1 - \sin^2\theta) + 6\sin\theta = 0$
$4 - 4\sin^2\theta + 6\sin\theta = 0$
$4\sin^2\theta - 6\sin\theta - 4 = 0$
양변을 2로 나누면:
$2\sin^2\theta - 3\sin\theta - 2 = 0$
$\sin\theta = t$로 치환하면 $2t^2 - 3t - 2 = 0$
$(2t + 1)(t - 2) = 0$
따라서 $t = -\frac{1}{2}$ 또는 $t = 2$.
$\sin\theta$의 값은 $-1 \le \sin\theta \le 1$이므로, $\sin\theta = 2$는 불가능하다.
그러므로 $\sin\theta = -\frac{1}{2}$이다.

2. 두 근의 곱:
$(4\cos\theta)(6\tan\theta) = -k$
$24\cos\theta \cdot \frac{\sin\theta}{\cos\theta} = -k$
$24\sin\theta = -k$
위에서 구한 $\sin\theta = -\frac{1}{2}$를 대입하면:
$24 \left(-\frac{1}{2}\right) = -k$
$-12 = -k$
$k = 12$

3. $k^2$의 값 계산:
$k^2 = 12^2 = 144$

또한, 이차방정식 $x^2 - k = 0$이 서로 다른 두 실근을 가지려면 $k > 0$이어야 한다.
$k=12$는 이 조건을 만족한다.
$\sin\theta = -1/2$일 때, $\cos\theta = \pm\sqrt{1 - (-1/2)^2} = \pm\sqrt{3}/2$.
만약 $\cos\theta = \sqrt{3}/2$이면, 두 근은 $4(\sqrt{3}/2) = 2\sqrt{3}$과 $6(-1/\sqrt{3}) = -2\sqrt{3}$이다.
만약 $\cos\theta = -\sqrt{3}/2$이면, 두 근은 $4(-\sqrt{3}/2) = -2\sqrt{3}$과 $6(1/\sqrt{3}) = 2\sqrt{3}$이다.
두 경우 모두 서로 다른 두 실근 $\pm 2\sqrt{3}$을 가지며, 이는 $x^2 - 12 = 0$의 근과 일치한다.

따라서 상수 $k^2$의 값은 144이다.
