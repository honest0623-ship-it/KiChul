---
id: JEW-2023-G2-S1-MID2-CAL1-016
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: 16
difficulty: 4
level: 4
unit: 미적분 I(2022개정)>1. 함수의 극한과 연속>1-1. 함수의 극한
unit_l1: 미적분 I(2022개정)
unit_l2: 1. 함수의 극한과 연속
unit_l3: 1-1. 함수의 극한
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-16
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-016_original.png
---

## Q
함수 $f(x)$에 대하여 $x=1$에서
$$
\lim_{x\to 1^+}f(x)=\lim_{x\to 1^-}f(x)
$$
이고,
$$
\lim_{x\to 1}\frac{f(x)-1}{x^2-3f(1)}=1
$$
이다. 다음 중 옳은 것을 있는 대로 고른 것은?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
<보기><br />
ㄱ. $f(1)=\dfrac{1}{3}$이면, 함수 $g(x)=\{f(x)\}^2-\dfrac{4}{3}f(x)$는 $x=1$에서 연속이다.<br />
ㄴ. $f(x)$가 $x=1$에서 불연속이면, $3f(1)+\lim_{x\to 1^+}f(x)=2$이다.<br />
ㄷ. $f(x)$가 $x=1$에서 연속이면, $f(1)=\dfrac{1}{2}$이다.
</div>

## Choices
① ㄱ
② ㄴ
③ ㄱ, ㄷ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
⑤

## Solution
공통된 극한값을
$$
L=\lim_{x\to 1}f(x)
$$
라 하자.

ㄱ. $f(1)=\dfrac13$이면 분모는
$$
x^2-1
$$
이 되어 $x\to 1$일 때 0으로 간다. 주어진 극한값이 1이므로 분자도 0으로 가야 하여
$$
L=1
$$
이다. 따라서
$$
\lim_{x\to 1}g(x)=L^2-\frac43L=1-\frac43=-\frac13
$$
이고,
$$
g(1)=\left(\frac13\right)^2-\frac43\cdot \frac13=-\frac13
$$
이므로 $g(x)$는 $x=1$에서 연속이다.

ㄴ. $f(x)$가 $x=1$에서 불연속이면 $L\ne f(1)$이다. 이때 주어진 식에서
$$
L-1=1-3f(1)
$$
이므로
$$
3f(1)+L=2
$$
이다. 또한 $L=\lim_{x\to 1^+}f(x)$이므로 ㄴ은 참이다.

ㄷ. $f(x)$가 $x=1$에서 연속이면
$$
L=f(1)
$$
이다. 따라서
$$
f(1)-1=1-3f(1)
$$
이고,
$$
4f(1)=2
$$
이므로
$$
f(1)=\frac12
$$
이다. 따라서 ㄷ도 참이다.

그러므로 ㄱ, ㄴ, ㄷ이 모두 옳다.
