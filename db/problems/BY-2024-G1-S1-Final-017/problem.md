---
id: BY-2024-G1-S1-Final-017
school: BY
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM1
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-03-07
tags:
- 객관식
- 출제번호-17
assets:
- assets/original/BY-2024-G1-S1-Final-017_original.png
---

## Q
$x$에 대한 삼차방정식
\[
x^3-3x^2+(k+2)x-k=0
\]
의 세 실근 $\alpha$, $\beta$, $\gamma$ $(\alpha<\beta<\gamma)$가 존재할 때, 다음을 만족시키는 실수 $k$에 대하여 $k^2$의 값은?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
\[
(\alpha-1)(\beta+1)(\gamma-1)=-6
\]
</div>

## Choices
① 4
② 7
③ 9
④ 13
⑤ 16

## Answer
①

## Solution
주어진 삼차방정식의 왼쪽을 $f(x)$라고 하면
\[
f(1)=1-3+(k+2)-k=0
\]
이므로 $x=1$은 한 근이다.

따라서
\[
x^3-3x^2+(k+2)x-k=(x-1)(x^2-2x+k)
\]
이다.

세 실근이 존재하려면 이차방정식
\[
x^2-2x+k=0
\]
이 서로 다른 두 실근을 가져야 하므로
\[
(-2)^2-4k>0
\]
에서
\[
k<1
\]
이다.

\[
1-k=s^2\quad (s>0)
\]
라고 두면 이 세 근은
\[
1-s,\ 1,\ 1+s
\]
이다.

또 $\alpha<\beta<\gamma$이므로
\[
\alpha=1-s,\quad \beta=1,\quad \gamma=1+s
\]
이다.

주어진 조건에 대입하면
\[
(\alpha-1)(\beta+1)(\gamma-1)
=(-s)\cdot 2\cdot s
=-2s^2
\]
이다.

이 값이 $-6$이므로
\[
-2s^2=-6
\]
\[
s^2=3
\]
이다.

따라서
\[
1-k=3
\]
이므로
\[
k=-2
\]
이다.

그러므로
\[
k^2=4
\]
이다.

정답은 $①$이다.

