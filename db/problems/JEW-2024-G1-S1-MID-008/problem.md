---
id: JEW-2024-G1-S1-MID-008
school: JEW
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: "8"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 객관식
  - 출제번호-8
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/008_1-2. 나머지정리.png
---

## Q
다항식 $256x^8-1$을 $(2x-1)^2$으로 나누었을 때의 나머지를 $R(x)$라고 할 때, $R(10)$의 값은?

## Choices
① 149
② 150
③ 151
④ 152
⑤ 153

## Answer
152

## Solution
다항식 $P(x) = 256x^8 - 1$을 $(2x-1)^2$으로 나누었을 때의 몫을 $Q(x)$, 나머지를 $R(x)$라고 하자.
나누는 식이 이차식이므로 나머지 $R(x)$는 일차식 또는 상수항이 된다. 따라서 $R(x) = ax + b$로 놓을 수 있다.

$P(x) = (2x-1)^2 Q(x) + ax + b$

먼저 $x = \frac{1}{2}$을 대입한다.
$P\left(\frac{1}{2}\right) = 256\left(\frac{1}{2}\right)^8 - 1 = 256 \cdot \frac{1}{256} - 1 = 1 - 1 = 0$

$P\left(\frac{1}{2}\right) = \left(2 \cdot \frac{1}{2} - 1\right)^2 Q\left(\frac{1}{2}\right) + a\left(\frac{1}{2}\right) + b$
$0 = (1-1)^2 Q\left(\frac{1}{2}\right) + \frac{1}{2}a + b$
$0 = 0 + \frac{1}{2}a + b$
따라서 $\frac{1}{2}a + b = 0 \implies a + 2b = 0 \quad \cdots (1)$

다음으로 $P(x)$를 미분한다.
$P'(x) = \frac{d}{dx}(256x^8 - 1) = 256 \cdot 8x^7 = 2048x^7$

$P(x) = (2x-1)^2 Q(x) + ax + b$를 미분하면:
$P'(x) = 2(2x-1) \cdot 2 \cdot Q(x) + (2x-1)^2 Q'(x) + a$
$P'(x) = 4(2x-1)Q(x) + (2x-1)^2 Q'(x) + a$

여기에 $x = \frac{1}{2}$을 대입한다.
$P'\left(\frac{1}{2}\right) = 2048\left(\frac{1}{2}\right)^7 = 2048 \cdot \frac{1}{128} = 16$

$P'\left(\frac{1}{2}\right) = 4\left(2 \cdot \frac{1}{2} - 1\right)Q\left(\frac{1}{2}\right) + \left(2 \cdot \frac{1}{2} - 1\right)^2 Q'\left(\frac{1}{2}\right) + a$
$16 = 4(1-1)Q\left(\frac{1}{2}\right) + (1-1)^2 Q'\left(\frac{1}{2}\right) + a$
$16 = 0 + 0 + a$
따라서 $a = 16 \quad \cdots (2)$

(2)를 (1)에 대입한다.
$16 + 2b = 0$
$2b = -16$
$b = -8$

따라서 나머지 $R(x) = 16x - 8$이다.

문제에서 요구하는 $R(10)$의 값은:
$R(10) = 16(10) - 8 = 160 - 8 = 152$

정답은 152이다.
