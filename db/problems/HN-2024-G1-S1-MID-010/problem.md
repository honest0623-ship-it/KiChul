---
id: HN-2024-G1-S1-MID-010
school: HN
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: "10"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-3. 여러 가지 방정식"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 객관식
  - 출제번호-10
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/010_2-3. 여러 가지 방정식.png
---

## Q
방정식 $x^3+1=0$의 한 허근 $w$에 대하여 $f(n)$을 $f(n)=(\bar{w})^n+\frac{1}{w^n}$ ($n$은 자연수)으로 정의할 때, $f(1)+f(2)+f(3)+\cdots+f(125)$의 값은? (단, $\bar{w}$는 $w$의 켤레복소수이다.)

## Choices
① -2
② -1
③ 0
④ 1
⑤ 2

## Answer
-2

## Solution
주어진 방정식 $x^3+1=0$은 $(x+1)(x^2-x+1)=0$으로 인수분해됩니다. $w$는 허근이므로 $w \neq -1$이고, 따라서 $w$는 이차방정식 $x^2-x+1=0$의 근입니다.

$w^2-w+1=0$이므로 다음 성질들을 알 수 있습니다.
1. $w^2 = w-1$
2. 양변을 $w$로 나누면 $w-1+\frac{1}{w}=0 \implies w+\frac{1}{w}=1$
3. $x^2-x+1=0$의 두 근은 $w$와 $\bar{w}$이므로, 근과 계수의 관계에 의해 $w\bar{w}=1$입니다.
4. $w^3+1=0 \implies w^3=-1$. 따라서 $w^6 = (w^3)^2 = (-1)^2 = 1$입니다.

주어진 함수 $f(n)$은 $f(n)=(\bar{w})^n+\frac{1}{w^n}$입니다.
위에서 $w\bar{w}=1$이므로 $\frac{1}{w}=\bar{w}$입니다. 이를 $f(n)$에 대입하면
$f(n) = (\bar{w})^n + (\bar{w})^n = 2(\bar{w})^n$이 됩니다.

이제 $f(n)$의 값을 $n=1, 2, \dots, 6$에 대해 계산해 봅시다. $\bar{w}$도 $x^2-x+1=0$의 근이므로 $\bar{w}^3=-1$이고 $\bar{w}^6=1$입니다. 따라서 $f(n)$의 값은 주기가 6입니다.

*   $f(1) = 2\bar{w}$
*   $f(2) = 2\bar{w}^2$
*   $f(3) = 2\bar{w}^3 = 2(-1) = -2$
*   $f(4) = 2\bar{w}^4 = 2\bar{w}^3 \cdot \bar{w} = 2(-1)\bar{w} = -2\bar{w}$
*   $f(5) = 2\bar{w}^5 = 2\bar{w}^3 \cdot \bar{w}^2 = 2(-1)\bar{w}^2 = -2\bar{w}^2$
*   $f(6) = 2\bar{w}^6 = 2(1) = 2$

한 주기(6개 항)의 합을 계산하면:
$S_6 = f(1)+f(2)+f(3)+f(4)+f(5)+f(6)$
$S_6 = (2\bar{w}) + (2\bar{w}^2) + (-2) + (-2\bar{w}) + (-2\bar{w}^2) + (2)$
$S_6 = (2\bar{w} - 2\bar{w}) + (2\bar{w}^2 - 2\bar{w}^2) + (-2 + 2) = 0$

이제 $f(1)+f(2)+f(3)+\cdots+f(125)$의 값을 구해야 합니다.
총 125개의 항이 있으며, $125 = 6 \times 20 + 5$입니다.
이는 6개 항의 주기가 20번 반복되고, 마지막에 5개 항이 남는다는 의미입니다.

따라서 전체 합은 $20 \times S_6 + (f(1)+f(2)+f(3)+f(4)+f(5))$와 같습니다.
$20 \times S_6 = 20 \times 0 = 0$이므로,

구하는 합은 $f(1)+f(2)+f(3)+f(4)+f(5)$와 같습니다.
$f(1)+f(2)+f(3)+f(4)+f(5) = (2\bar{w}) + (2\bar{w}^2) + (-2) + (-2\bar{w}) + (-2\bar{w}^2)$
$= (2\bar{w} - 2\bar{w}) + (2\bar{w}^2 - 2\bar{w}^2) - 2$
$= 0 + 0 - 2 = -2$

따라서 $f(1)+f(2)+f(3)+\cdots+f(125)$의 값은 $-2$입니다.
