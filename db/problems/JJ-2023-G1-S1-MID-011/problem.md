---
id: JJ-2023-G1-S1-MID-011
school: JJ
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 11
source_question_kind: objective
source_question_label: "11"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-2. 이차방정식과 이차함수"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-11
assets:
  - assets/original/
  - assets/original/011_2-2. 이차방정식과 이차함수.png
---

## Q
0이 아닌 두 실수 $a$, $b$가
$$
\frac{\sqrt{a}}{\sqrt{b}}=-\sqrt{\frac{a}{b}}
$$
를 만족시킬 때, [보기]에서 함수 $f(x)=x^2+ax+b$에 대한 설명으로 옳은 것만을 고른 것은?

[보기]

ㄱ. $f\!\left(-\frac{a}{2}\right)f(0)>0$

ㄴ. $f(x)$는 $x$축과 항상 서로 다른 두 점에서 만난다.

ㄷ. $(0,b)$에서의 접선의 방정식의 $x$절편은 $\frac{b}{a}$이다.

## Choices
① ㄱ
② ㄴ
③ ㄱ, ㄴ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
③

## Solution
주어진 식이 성립하려면 $a$와 $b$의 부호가 달라야 하고, 실제로 $a>0$, $b<0$일 때
$$
\frac{\sqrt{a}}{\sqrt{b}}
=\frac{\sqrt{a}}{i\sqrt{-b}}
=-i\sqrt{\frac{a}{-b}}
$$
이며
$$
-\sqrt{\frac{a}{b}}
=-\sqrt{-\frac{a}{-b}}
=-i\sqrt{\frac{a}{-b}}
$$
가 되어 성립한다.

이제 $a>0$, $b<0$에서 보기의 참거짓을 판단하면,
$$
f\!\left(-\frac{a}{2}\right)=b-\frac{a^2}{4}<0,\quad f(0)=b<0
$$
이므로 ㄱ은 참이다.

또한 판별식
$$
\Delta=a^2-4b>a^2>0
$$
이므로 서로 다른 두 실근을 가져 ㄴ도 참이다.

한편 $f'(x)=2x+a$이므로 $(0,b)$에서 접선은
$$
y=ax+b
$$
이고, $x$절편은 $x=-\frac{b}{a}$이다. 따라서 ㄷ은 거짓이다.

따라서 옳은 것은 ㄱ, ㄴ이므로 정답은 ③이다.
