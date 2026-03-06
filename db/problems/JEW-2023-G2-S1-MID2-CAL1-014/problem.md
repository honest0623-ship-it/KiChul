---
id: JEW-2023-G2-S1-MID2-CAL1-014
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: 3
level: 3
unit: 미적분 I(2022개정)>1. 함수의 극한과 연속>1-2. 함수의 연속
unit_l1: 미적분 I(2022개정)
unit_l2: 1. 함수의 극한과 연속
unit_l3: 1-2. 함수의 연속
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-14
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-014_original.png
---

## Q
두 실수 $a(a<1)$, $b$에 대하여 함수
$$
f(x)=
\begin{cases}
\dfrac{1-a}{x-1}+2 & (x\le a)\\
b(x-a)+1 & (x>a)
\end{cases}
$$
라 하자. 다음 중 옳은 것을 있는 대로 고른 것은?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
<보기><br />
ㄱ. $\lim_{x\to a^+}f(x)=1$<br />
ㄴ. $f(x)$는 $x=a$에서 연속이다.<br />
ㄷ. $\lim_{x\to\infty}f(x)$의 값이 존재하면, $f(a)=f(1)$이다.
</div>

## Choices
① ㄱ
② ㄱ, ㄴ
③ ㄴ, ㄷ
④ ㄱ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
⑤

## Solution
ㄱ. $x>a$에서의 식은
$$
f(x)=b(x-a)+1
$$
이므로
$$
\lim_{x\to a^+}f(x)=1
$$
이다.

ㄴ. $x=a$일 때
$$
f(a)=\frac{1-a}{a-1}+2=-1+2=1
$$
이다. 왼쪽 극한과 오른쪽 극한도 모두 1이므로 $x=a$에서 연속이다.

ㄷ. $\lim_{x\to\infty}f(x)$의 값이 존재하려면
$$
b=0
$$
이어야 한다. 그러면 $x>a$에서 $f(x)=1$이고, $a<1$이므로
$$
f(1)=1
$$
이다. 또한 $f(a)=1$이므로
$$
f(a)=f(1)
$$
이다.

따라서 ㄱ, ㄴ, ㄷ이 모두 옳다.
