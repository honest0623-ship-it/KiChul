---
id: JJ-2022-G1-S1-MID-103
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 3
source_question_kind: subjective
source_question_label: 서3
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서3
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---

## Q
실수 $t$에 대하여 $t\le x\le t+2$인 함수 $f(x)=x^2-4x+6$의 최솟값을 $g(t)$라고 하자. 방정식 $g(t)=6$의 서로 다른 두 실근을 $\alpha$, $\beta$라 할 때, $(\alpha-\beta)^2$의 값을 구하시오.

## Choices


## Answer
$36$

## Solution
\[
f(x)=x^2-4x+6=(x-2)^2+2
\]
이므로 꼭짓점은 $(2,2)$이다.
구간 $[t, t+2]$에서의 최솟값 $g(t)$를 생각하면

- $t\le 0$이면 구간이 꼭짓점의 왼쪽에 있으므로 $g(t)=f(t+2)=t^2+2$
- $0\le t\le 2$이면 구간 안에 $x=2$가 포함되므로 $g(t)=2$
- $t\ge 2$이면 구간이 꼭짓점의 오른쪽에 있으므로 $g(t)=f(t)=(t-2)^2+2$

이제 $g(t)=6$을 풀면
\[
t^2+2=6 \Rightarrow t=-2,\qquad (t-2)^2+2=6 \Rightarrow t=4
\]
이다. 따라서 $\alpha=-2$, $\beta=4$이고
\[
(\alpha-\beta)^2=(-2-4)^2=36
\]
이다.
