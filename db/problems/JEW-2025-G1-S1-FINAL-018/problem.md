---
id: JEW-2025-G1-S1-FINAL-018
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-18
assets:
- assets/scan.png
- assets/original/
- assets/original/018.png
---

## Q
\(x\)에 대한 삼차방정식
\[
x^3-(2a+1)x^2+(a^2-a)x+a^2+a+2=0
\]
의 서로 다른 세 근을 \(\alpha,\ \beta,\ \gamma\)라 하자.
\(\alpha^2+\beta^2=10\)을 만족하는 모든 실수 \(a\)값의 합은?

## Choices
① 2
② 3
③ 4
④ \(-5\)
⑤ \(-6\)
## Answer
1

## Solution
Factor the cubic as
\[
x^3-(2a+1)x^2+(a^2-a)x+a^2+a+2
=(x+1)\bigl(x^2-2(a+1)x+a^2+a+2\bigr).
\]
So one root is always \(-1\).

Case 1: \(\alpha,\beta\) are the two roots of the quadratic factor.
Then
\[
\alpha+\beta=2(a+1),
\qquad
\alpha\beta=a^2+a+2.
\]
Hence
\[
\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=2a^2+6a.
\]
Setting this equal to 10 gives
\[
a^2+3a-5=0.
\]

Case 2: one of \(\alpha,\beta\) is \(-1\).
Then the other one, say \(t\), satisfies
\[
(-1)^2+t^2=10 \Rightarrow t=\pm3.
\]
Substituting into the quadratic factor,
\[
t=3 \Rightarrow a^2-5a+5=0,
\qquad
t=-3 \Rightarrow a^2+7a+17=0.
\]
The last equation has no real root.

Therefore all real values of \(a\) come from
\[
a^2+3a-5=0,
\qquad
a^2-5a+5=0.
\]
The sums of their real roots are \(-3\) and \(5\), so the total sum is
\[
-3+5=2.
\]
Therefore the correct choice is 1.
