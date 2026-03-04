---
id: HN-2024-G1-S1-MID-004
school: HN
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 4
source_question_kind: objective
source_question_label: "4"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>1. 다항식>1-3. 인수분해"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-3. 인수분해"
source: "user_upload_2026-03-03"
tags:
  - 수동보정
  - 객관식
  - 출제번호-4
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/004_1-3. 인수분해.png
---

## Q
$2x^3+ax^2-(3+3a)x-45$는 계수가 모두 정수인 서로 다른 세 일차식의 곱으로 인수분해될 때, 정수 $a$의 값의 개수는?

## Choices
① 5
② 6
③ 7
④ 8
⑤ 9

## Answer
③

## Solution
\[
P(x)=2x^3+ax^2-(3+3a)x-45
\]
에서 $x=3$을 대입하면
\[
P(3)=54+9a-(9+9a)-45=0
\]
이므로 항상 $(x-3)$을 인수로 가진다.

따라서
\[
P(x)=(x-3)\left(2x^2+(a+6)x+15\right)
\]
이고, 두 번째 인수가 정수계수 일차식의 곱이 되려면
\[
2x^2+(a+6)x+15=(2x+m)(x+n)
\]
($m,n\in\mathbb{Z}$)이라 둘 수 있다.

그러면
\[
mn=15,\qquad a+6=2n+m
\]
이다.

$mn=15$의 순서쌍은 8개이고, 각각에서
\[
a=2n+m-6
\]
으로 정수 $a$가 정해진다.

다만 “서로 다른 세 일차식”이어야 하므로 $(x-3)$이 중복되면 안 된다.  
$n=-3,\ m=-5$일 때
\[
2x^2+(a+6)x+15=(2x-5)(x-3)
\]
이 되어 전체가
\[
(x-3)^2(2x-5)
\]
가 되므로 제외한다.

즉 8개 중 1개를 제외하여 가능한 $a$의 개수는
\[
7
\]
이다.

따라서 정답은 **③**.
