---
id: HN-2024-G1-S1-MID-007
school: HN
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: "7"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 객관식
  - 출제번호-7
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/007_2-1. 복소수와 이차방정식_2.png
---

## Q
$a-b=6$, $a^2+b^2=20$일 때, $\left(\sqrt{a}+\frac{1}{\sqrt{b}}\right)\left(\sqrt{a}+\frac{4}{\sqrt{b}}\right)$의 값은? (단, $a<3$이고 $b$는 실수이다.)

## Choices
① $-2-5\sqrt{2}i$
② $-2+5\sqrt{2}i$
③ $2-5\sqrt{2}i$
④ $-1-\frac{5\sqrt{2}i}{2}$
⑤ $1-\frac{5\sqrt{2}i}{2}$

## Answer
⑤

## Solution
주어진 조건 $a-b=6$과 $a^2+b^2=20$을 이용하여 $ab$의 값을 구합니다.
$(a-b)^2 = a^2-2ab+b^2$
$6^2 = 20 - 2ab$
$36 = 20 - 2ab$
$2ab = 20 - 36$
$2ab = -16$
$ab = -8$

이제 $a-b=6$과 $ab=-8$을 연립하여 $a, b$의 값을 구합니다.
$a = b+6$을 $ab=-8$에 대입하면:
$(b+6)b = -8$
$b^2+6b = -8$
$b^2+6b+8 = 0$
$(b+2)(b+4) = 0$
따라서 $b=-2$ 또는 $b=-4$ 입니다.

각 경우에 대해 $a$ 값을 구하고 조건 $a<3$을 확인합니다.
1. $b=-2$일 때, $a = -2+6 = 4$. 이 경우 $a=4$는 $a<3$ 조건을 만족하지 않습니다.
2. $b=-4$일 때, $a = -4+6 = 2$. 이 경우 $a=2$는 $a<3$ 조건을 만족합니다.
따라서 $a=2$이고 $b=-4$ 입니다.

이제 주어진 식 $\left(\sqrt{a}+\frac{1}{\sqrt{b}}\right)\left(\sqrt{a}+\frac{4}{\sqrt{b}}\right)$에 $a=2, b=-4$를 대입합니다.
$\sqrt{a} = \sqrt{2}$
$\sqrt{b} = \sqrt{-4} = \sqrt{4}i = 2i$

식을 전개하면:
$\left(\sqrt{2}+\frac{1}{2i}\right)\left(\sqrt{2}+\frac{4}{2i}\right)$
$\frac{1}{2i} = \frac{1 \cdot i}{2i \cdot i} = \frac{i}{-2} = -\frac{i}{2}$
$\frac{4}{2i} = \frac{2}{i} = \frac{2 \cdot i}{i \cdot i} = \frac{2i}{-1} = -2i$

대입하여 계산하면:
$\left(\sqrt{2}-\frac{i}{2}\right)(\sqrt{2}-2i)$
$= (\sqrt{2})(\sqrt{2}) + (\sqrt{2})(-2i) + \left(-\frac{i}{2}\right)(\sqrt{2}) + \left(-\frac{i}{2}\right)(-2i)$
$= 2 - 2\sqrt{2}i - \frac{\sqrt{2}}{2}i + i^2$
$= 2 - 2\sqrt{2}i - \frac{\sqrt{2}}{2}i - 1$ (∵ $i^2=-1$)
$= (2-1) + \left(-2\sqrt{2} - \frac{\sqrt{2}}{2}\right)i$
$= 1 + \left(-\frac{4\sqrt{2}}{2} - \frac{\sqrt{2}}{2}\right)i$
$= 1 - \frac{5\sqrt{2}}{2}i$

따라서 정답은 ⑤번입니다.
