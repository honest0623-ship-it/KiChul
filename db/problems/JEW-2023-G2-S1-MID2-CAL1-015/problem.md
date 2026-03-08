---
id: JEW-2023-G2-S1-MID2-CAL1-015
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: 15
difficulty: 4
level: 4
unit: 미적분 I(2022개정)>2. 미분>2-1. 미분계수와 도함수
unit_l1: 미적분 I(2022개정)
unit_l2: 2. 미분
unit_l3: 2-1. 미분계수와 도함수
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-15
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-015_original.png
---

## Q
실수 전체에서 정의된 함수 $f(x)$에 대하여 다음 중 옳은 것을 있는 대로 고른 것은?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
<보기><br />
ㄱ. $\lim_{x\to 1}\dfrac{f(x)-f(1)}{x-1}=0$이면, $f(1)=\lim_{x\to 1}f(x)$이다.<br />
ㄴ. $\lim_{h\to 0}\dfrac{f(1+h)-f(1-h)}{2h}=2$이면, 미분계수 $f'(1)$가 존재하고, 그 값은 $1$이다.<br />
ㄷ. $f'(1)$이 존재하고, 모든 실수 $x$에 대하여 $f(x)=f(-x)$이면, $f'(-1)=-f'(1)$이다.
</div>

## Choices
① ㄱ
② ㄱ, ㄴ
③ ㄱ, ㄷ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
③

## Solution
ㄱ. 주어진 식에서
$$
\lim_{x\to 1}\frac{f(x)-f(1)}{x-1}=0
$$
이면 분자
$$
f(x)-f(1)\to 0
$$
이므로
$$
\lim_{x\to 1}f(x)=f(1)
$$
이다. 따라서 참이다.

ㄴ. 식
$$
\frac{f(1+h)-f(1-h)}{2h}
$$
의 극한은 좌우에서 대칭으로 본 평균변화율이다. 이 값이 2라고 해서 미분계수가 반드시 존재하는 것은 아니며, 미분가능하다 하더라도 그 값은 2가 된다. 따라서 거짓이다.

ㄷ. 모든 실수 $x$에 대하여 $f(x)=f(-x)$이므로 $f$는 짝함수이다. 짝함수의 도함수는 홀함수가 되므로
$$
f'(-1)=-f'(1)
$$
이다. 따라서 참이다.

그러므로 옳은 것은 ㄱ, ㄷ이다.
