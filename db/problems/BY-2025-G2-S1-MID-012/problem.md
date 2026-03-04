---
id: BY-2025-G2-S1-MID-012
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: "12"
difficulty: 4
level: 4
unit: "대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수"
unit_l1: "대수(2022개정)"
unit_l2: "1. 지수함수와 로그함수"
unit_l3: "1-2. 지수함수"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 객관식
  - 출제번호-12
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/012_1-2. 지수함수_2.png
---

## Q
$3^{2x} - 3^{x+1} = -1$ 일 때, $\frac{3^{3x} + 3^{-3x} + 2}{3^{2x} + 3^{-2x} - 2}$ 의 값은?

## Choices
① 1
② 2
③ 3
④ 4
⑤ 5

## Answer
④

## Solution
주어진 식 $3^{2x} - 3^{x+1} = -1$ 에서 $3^x = t$ 로 치환합니다. ($t > 0$)
그러면 식은 다음과 같이 변형됩니다.
$(3^x)^2 - 3^x \cdot 3^1 = -1$
$t^2 - 3t = -1$
$t^2 - 3t + 1 = 0$

양변을 $t$로 나누면 ( $t \neq 0$ 이므로 가능합니다):
$t - 3 + \frac{1}{t} = 0$
$t + \frac{1}{t} = 3$

이제 구하고자 하는 식 $\frac{3^{3x} + 3^{-3x} + 2}{3^{2x} + 3^{-2x} - 2}$ 에 $t = 3^x$ 를 대입합니다.
$\frac{(3^x)^3 + (3^x)^{-3} + 2}{(3^x)^2 + (3^x)^{-2} - 2} = \frac{t^3 + t^{-3} + 2}{t^2 + t^{-2} - 2} = \frac{t^3 + \frac{1}{t^3} + 2}{t^2 + \frac{1}{t^2} - 2}$

분모를 먼저 계산합니다:
$t^2 + \frac{1}{t^2} - 2 = (t - \frac{1}{t})^2$
우리는 $(t - \frac{1}{t})^2 = (t + \frac{1}{t})^2 - 4$ 임을 알고 있습니다.
$t + \frac{1}{t} = 3$ 이므로,
$(t - \frac{1}{t})^2 = 3^2 - 4 = 9 - 4 = 5$
따라서 분모는 5입니다.

분자를 계산합니다:
$t^3 + \frac{1}{t^3} + 2$
우리는 $t^3 + \frac{1}{t^3} = (t + \frac{1}{t})^3 - 3(t + \frac{1}{t})$ 임을 알고 있습니다.
$t + \frac{1}{t} = 3$ 이므로,
$t^3 + \frac{1}{t^3} = 3^3 - 3(3) = 27 - 9 = 18$
따라서 분자는 $18 + 2 = 20$ 입니다.

최종적으로 주어진 식의 값은:
$\frac{20}{5} = 4$

따라서 정답은 4입니다.
