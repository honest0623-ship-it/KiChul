---
id: JE-2025-G2-S1-MID-014
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-14
assets:
- assets/original/
- assets/original/014_1-3. 로그함수.png
---
## Q
어느 기업에서 올해 기업의 부채가 자기 자본의 $2$배에 이르자, 내년부터 매년 부채를 전년도에 비해 $20\%$씩 줄이고, 자기 자본은 $20\%$씩 늘리는 계획을 세웠다. 이 계획대로 진행될 때, 이 기업의 자기 자본이 처음으로 부채보다 많아지는 해는 올해로부터 몇 년 후인지 구하면?

(단, $\log 2=0.3010$, $\log 3=0.4771$로 계산한다.)

## Choices
① $1$  
② $2$  
③ $3$  
④ $4$  
⑤ $5$

## Answer
②

## Solution
올해 자기 자본을 $C$라 하면 올해 부채는 $2C$이다.

올해로부터 $n$년 후($n\ge 1$)를 보면
$$
\text{부채}=2C\cdot(0.8)^n,\qquad
\text{자기 자본}=C\cdot(1.2)^n
$$
이다.

자기 자본이 부채보다 많아지려면
$$
C(1.2)^n>2C(0.8)^n
$$
$$
\left(\frac{1.2}{0.8}\right)^n>2
\Rightarrow \left(\frac{3}{2}\right)^n>2
$$
이어야 한다.

상용로그를 취하면
$$
n\log\frac{3}{2}>\log 2
$$
$$
n>\frac{\log 2}{\log 3-\log 2}
=\frac{0.3010}{0.4771-0.3010}
=\frac{0.3010}{0.1761}
\approx 1.71
$$
이므로 이를 만족하는 최소 자연수는
$$
n=2
$$
이다.

따라서 올해로부터 $2$년 후이다.
