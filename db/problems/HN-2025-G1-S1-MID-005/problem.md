---
id: HN-2025-G1-S1-MID-005
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 5
source_question_kind: objective
source_question_label: '5'
difficulty: 3
level: 3
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-03-05
tags:
- 수동작성
- OCR
- AI
- 객관식
- 출제번호-5
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2025.G1.S1.MID.COM1.PDF.pdf
---

## Q
다항식 $f(x)$를 $x-2$로 나누었을 때의 나머지는 1이고, $x+1$로 나누었을 때의 나머지는 $-5$이다. $f(x)$를 $x^2-x-2$로 나누었을 때의 나머지를 $R(x)$라 할 때, $R(3)$의 값은?

## Choices
① 1
② 3
③ 5
④ 7
⑤ 9

## Answer
③

## Solution
나머지 정리에 의해 $f(x)$를 $x-2$로 나누었을 때의 나머지가 1이므로 $f(2)=1$이다.
또한, $f(x)$를 $x+1$로 나누었을 때의 나머지가 $-5$이므로 $f(-1)=-5$이다.

$f(x)$를 $x^2-x-2$로 나누었을 때의 몫을 $Q(x)$, 나머지를 $R(x)$라고 하면,
$x^2-x-2 = (x-2)(x+1)$이므로, $R(x)$는 일차식 또는 상수항이 된다. 따라서 $R(x) = ax+b$로 둘 수 있다.

$f(x) = (x-2)(x+1)Q(x) + ax+b$

위 식에 $x=2$를 대입하면:
$f(2) = (2-2)(2+1)Q(2) + 2a+b$
$1 = 0 + 2a+b \Rightarrow 2a+b=1 \quad \cdots \text{①}$

위 식에 $x=-1$을 대입하면:
$f(-1) = (-1-2)(-1+1)Q(-1) + a(-1)+b$
$-5 = 0 -a+b \Rightarrow -a+b=-5 \quad \cdots \text{②}$

①에서 ②를 빼면:
$(2a+b) - (-a+b) = 1 - (-5)$
$3a = 6$
$a = 2$

$a=2$를 ①에 대입하면:
$2(2)+b = 1$
$4+b = 1$
$b = -3$

따라서 나머지 $R(x) = 2x-3$이다.

구하고자 하는 값은 $R(3)$이므로:
$R(3) = 2(3)-3 = 6-3 = 3$

정답은 3이다.
