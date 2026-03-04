---
id: BY-2024-G1-S1-MID-015
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: "15"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-1. 다항식의 연산"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 객관식
  - 출제번호-15
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/015_1-1. 다항식의 연산.png
---

## Q
\[
ab+bc+ca=6,\quad a+b+c=5,\quad
\frac{a^2b^2+b^2c^2+c^2a^2}{a^4+b^4+c^4+7}=\frac{1}{14}
\]
일 때, $abc$의 값은?

## Choices
① $\frac{3}{2}$
② 2
③ $\frac{5}{2}$
④ 3
⑤ $\frac{7}{2}$

## Answer
$\frac{5}{2}$

## Solution
\[
s_1=a+b+c=5,\quad s_2=ab+bc+ca=6,\quad s_3=abc
\]
라 두자.

먼저
\[
a^2b^2+b^2c^2+c^2a^2
=(ab+bc+ca)^2-2abc(a+b+c)
\]
이므로
\[
a^2b^2+b^2c^2+c^2a^2
=s_2^2-2s_1s_3
=36-10s_3
\]

또
\[
a^2+b^2+c^2=s_1^2-2s_2=25-12=13
\]
이므로
\[
a^4+b^4+c^4
=(a^2+b^2+c^2)^2-2(a^2b^2+b^2c^2+c^2a^2)
\]
\[
=13^2-2(36-10s_3)
=169-72+20s_3
=97+20s_3
\]
따라서 분모는
\[
a^4+b^4+c^4+7=104+20s_3
\]

주어진 식에 대입하면
\[
\frac{36-10s_3}{104+20s_3}=\frac{1}{14}
\]
\[
14(36-10s_3)=104+20s_3
\]
\[
504-140s_3=104+20s_3
\]
\[
400=160s_3
\]
\[
s_3=\frac{5}{2}
\]

즉,
\[
abc=\frac{5}{2}
\]
이고 정답은 ③이다.
