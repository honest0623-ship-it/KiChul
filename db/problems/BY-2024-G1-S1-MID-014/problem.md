---
id: BY-2024-G1-S1-MID-014
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: "14"
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
  - 출제번호-14
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/014_1-2. 나머지정리.png
---

## Q
$f(x)$를 $x^2-4x+7$로 나누었을 때의 몫이 $Q_1(x)$, 나머지를 $2x+3$이라 하고, $Q_1(x)$를 $x^2+2x-4$로 나누었을 때의 몫이 $(x-2)Q_2(x)$, 나머지가 $x+1$이라 하자. $f(x)$를 $x^3-6x^2+15x-14$로 나누었을 때의 나머지를 $R(x)$라 할 때, $R(1)$의 값은?

## Choices
① 14
② 15
③ 16
④ 17
⑤ 18

## Answer
17

## Solution
\[
f(x)=(x^2-4x+7)Q_1(x)+(2x+3)
\]
이므로
\[
f(x)\equiv 2x+3 \pmod{x^2-4x+7}
\]

또
\[
x^3-6x^2+15x-14=(x-2)(x^2-4x+7)
\]
이므로 $R(x)$를 $x^3-6x^2+15x-14$로 나눈 나머지라 하면
\[
R(x)=c(x^2-4x+7)+2x+3
\]
로 둘 수 있다. ($R$의 차수는 2 이하)

이제 $x=2$를 대입해 $c$를 구한다.

먼저
\[
Q_1(x)=(x^2+2x-4)(x-2)Q_2(x)+(x+1)
\]
이므로
\[
Q_1(2)=3
\]

따라서
\[
f(2)=(2^2-4\cdot 2+7)Q_1(2)+(2\cdot 2+3)
=3\cdot 3+7=16
\]

또한 $x=2$는 $x^3-6x^2+15x-14$의 근이므로
\[
R(2)=f(2)=16
\]

\[
R(2)=c(4-8+7)+7=3c+7=16
\]
이므로
\[
c=3
\]

따라서
\[
R(1)=3(1-4+7)+2\cdot 1+3
=3\cdot 4+5
=17
\]

정답은 ④이다.
