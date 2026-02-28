---
id: HN-2025-G1-S1-MID-006
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
difficulty: '2'
unit: 공통수학1 > 다항식 > 나머지정리/인수정리
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-6
assets:
- assets/scan.png
- assets/original/
level: 2
unit_l1: 공통수학1
unit_l2: 다항식
unit_l3: 나머지정리/인수정리
---

## Q
다항식 $f(x)$를 $x^2+x+1$로 나누었을 때의 나머지가 $2x-1$이고, $x-1$로 나누면 나머지는 $-2$이다. $f(x)$를 $x^3-1$로 나누었을 때의 나머지를 $R(x)$라고 할 때, $R(2)$의 값은?

## Choices
① $-10$
② $-8$
③ $-6$
④ $-4$
⑤ $-2$

## Answer
④

## Solution
$f(x)$를 $x^3-1=(x-1)(x^2+x+1)$로 나누었을 때의 나머지를 $R(x)$라고 두면,
$R(x)\equiv 2x-1\pmod{x^2+x+1}$ 이므로 $R(x)=2x-1+c(x^2+x+1)$이다.

또한 $R(1)=f(1)=-2$이므로
$1+3c=-2 \Rightarrow c=-1$.

따라서 $R(x)=-x^2+x-2$이고,
$R(2)=-4$.
