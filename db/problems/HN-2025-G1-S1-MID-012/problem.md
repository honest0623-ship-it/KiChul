---
id: HN-2025-G1-S1-MID-012
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-12
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
---

## Q
복소수 $z = \frac{1-i}{1+i}$에 대하여 $z+z^2+z^3+\dots+z^{99}$의 값은?

## Choices
① -1
② 0
③ 1
④ -i
⑤ i

## Answer
-1

## Solution
먼저 복소수 $z$를 간단히 합니다.
$z = \frac{1-i}{1+i} = \frac{(1-i)(1-i)}{(1+i)(1-i)} = \frac{1 - 2i + i^2}{1 - i^2} = \frac{1 - 2i - 1}{1 + 1} = \frac{-2i}{2} = -i$

이제 $z$의 거듭제곱을 계산하여 규칙성을 찾습니다.
$z^1 = -i$
$z^2 = (-i)^2 = i^2 = -1$
$z^3 = (-i)^3 = -i^3 = -(-i) = i$
$z^4 = (-i)^4 = i^4 = 1$

$z^5 = z^4 \cdot z = 1 \cdot (-i) = -i$

$z$의 거듭제곱은 $-i, -1, i, 1$의 순서로 4개 항마다 반복됩니다.
이 4개 항의 합은 다음과 같습니다.
$z+z^2+z^3+z^4 = (-i) + (-1) + i + 1 = 0$

구하고자 하는 합은 $z+z^2+z^3+\dots+z^{99}$입니다.
총 99개의 항이 있습니다.
99를 4로 나누면 몫은 24이고 나머지는 3입니다.
$99 = 4 \times 24 + 3$

이는 4개 항의 묶음이 24번 반복되고, 마지막에 3개의 항이 남는다는 의미입니다.
$z+z^2+\dots+z^{99} = (z+z^2+z^3+z^4) + (z^5+\dots+z^8) + \dots + (z^{93}+z^{94}+z^{95}+z^{96}) + z^{97}+z^{98}+z^{99}$

각 4개 항의 묶음의 합은 0이므로, 처음 96개 항의 합은 $24 \times 0 = 0$입니다.
따라서 구하는 합은 마지막 3개 항의 합과 같습니다.
$z^{97}+z^{98}+z^{99}$

주기성을 이용하면:
$z^{97} = z^{4 \times 24 + 1} = z^1 = -i$
$z^{98} = z^{4 \times 24 + 2} = z^2 = -1$
$z^{99} = z^{4 \times 24 + 3} = z^3 = i$

따라서, $z^{97}+z^{98}+z^{99} = (-i) + (-1) + i = -1$

정답은 -1입니다.
