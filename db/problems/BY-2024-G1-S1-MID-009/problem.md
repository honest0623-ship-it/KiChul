---
id: BY-2024-G1-S1-MID-009
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: "9"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 객관식
  - 출제번호-9
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/009_2-1. 복소수와 이차방정식.png
---

## Q
0이 아닌 두 실수 $a$, $b$에 대하여 $\sqrt{a}\sqrt{b}=-\sqrt{ab}$일 때,
\[
\sqrt{(a+b)^2}+3|a|-2\sqrt{a^2}+\sqrt{b^2}
\]
를 간단히 하면?

## Choices
① $-2a-2b$
② $-2a+2b$
③ $a-2b$
④ $a+2b$
⑤ $3a$

## Answer
$-2a-2b$

## Solution
\[
\sqrt{a}\sqrt{b}=-\sqrt{ab}
\]
가 성립하려면 $a,b$의 부호를 확인해야 한다.

- $a,b>0$이면 좌변은 $\sqrt{ab}$, 우변은 $-\sqrt{ab}$이므로 불가능.
- $a<0,\ b<0$이면
\[
\sqrt{a}=i\sqrt{-a},\ \sqrt{b}=i\sqrt{-b}
\]
이므로
\[
\sqrt{a}\sqrt{b}
=(i\sqrt{-a})(i\sqrt{-b})
=-\sqrt{(-a)(-b)}
=-\sqrt{ab}
\]
가 성립한다.

따라서
\[
a<0,\quad b<0
\]
이다.

이제 식을 정리하면
\[
\sqrt{(a+b)^2}=|a+b|=-(a+b),
\quad |a|=-a,\quad \sqrt{a^2}=|a|=-a,\quad \sqrt{b^2}=|b|=-b
\]
이므로
\[
\sqrt{(a+b)^2}+3|a|-2\sqrt{a^2}+\sqrt{b^2}
\]
\[
=-(a+b)+3(-a)-2(-a)+(-b)
\]
\[
=-2a-2b
\]

정답은 ①이다.
