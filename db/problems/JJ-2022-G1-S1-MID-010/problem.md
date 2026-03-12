---
id: JJ-2022-G1-S1-MID-010
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: objective
source_question_no: 10
source_question_kind: objective
source_question_label: '10'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-3. 인수분해
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-3. 인수분해
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-10
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---

## Q
세 변의 길이가 $a$, $b$, $c$인 삼각형 $ABC$가 다음 조건을 만족한다.

(가) $x$에 관한 다항식
\[
\begin{aligned}
f(x) &= x^3-(b+c)x^2-(b^2+c^2)x \\
     &\quad + b^3+c^3+b^2c+bc^2
\end{aligned}
\]은 $x-a$로 나누어 떨어진다.
(나) $2b=3(a-c)$
(다) 삼각형 $ABC$의 넓이는 $30$이다.

삼각형 $ABC$의 둘레의 길이를 구하시오.

## Choices
① $28$
② $30$
③ $32$
④ $34$
⑤ $36$

## Answer
②

## Solution
$f(x)$가 $x-a$로 나누어떨어지므로
\[
f(a)=a^3-(b+c)a^2-(b^2+c^2)a+b^3+c^3+b^2c+bc^2=0
\]
이다. 이를 인수분해하면
\[
(a-b-c)(a^2-b^2-c^2)=0
\]
이다.

삼각형의 세 변은 $a<b+c$를 만족하므로 $a-b-c\ne 0$이다. 따라서
\[
a^2=b^2+c^2
\]
이고, 삼각형 $ABC$는 직각삼각형이다.

조건 $2b=3(a-c)$에서
\[
a-c=2t,\qquad b=3t
\]
라 두면 $a=c+2t$이다. 이를
\[
a^2=b^2+c^2
\]
에 대입하면
\[
(c+2t)^2=(3t)^2+c^2
\]
\[
4ct+4t^2=9t^2
\]
이므로
\[
c=\frac{5t}{4},\qquad a=\frac{13t}{4}
\]
이다.

넓이가 $30$이므로
\[
\frac{1}{2}bc=\frac{1}{2}\cdot 3t\cdot \frac{5t}{4}=30
\]
이다. 따라서
\[
\frac{15t^2}{8}=30 \Rightarrow t^2=16 \Rightarrow t=4
\]
이다. 그러므로
\[
a=13,\qquad b=12,\qquad c=5
\]
이고, 둘레는
\[
13+12+5=30
\]
이다.

따라서 정답은 ②이다.
