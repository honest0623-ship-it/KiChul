---
id: JJ-2022-G1-S1-MID-102
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 2
source_question_kind: subjective
source_question_label: 서2
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
- subjective
- 출제번호-서2
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---

## Q
다항식 $f(x)=x^4+mx^3+nx^2+8$가 $(x-a)(x-b)$를 인수로 가질 때, $m^2+n^2$의 값을 구하시오. (단, $a, b$는 서로 다른 자연수이고, $m, n$은 정수이다.)

## Choices


## Answer
$153$

## Solution
$(x-a)(x-b)$가 인수이므로
\[
f(x)=(x-a)(x-b)(x^2+px+q)
\]
로 둘 수 있다. 전개하면
\[
f(x)=x^4+(p-a-b)x^3+(q-p(a+b)+ab)x^2+\{-q(a+b)+abp\}x+abq
\]
이다. 상수항이 $8$이고 $x$의 계수가 $0$이므로
\[
abq=8,\qquad -q(a+b)+abp=0
\]
를 만족한다.
서로 다른 자연수 $a, b$에 대해 $ab$는 $8$의 약수이므로 가능한 경우를 조사하면 $(a,b)=(1,2)$일 때만 정수 $p, q$가 존재한다.
이때 $ab=2$이므로 $q=4$,
\[
-4(1+2)+2p=0 \Rightarrow p=6
\]
이다. 따라서
\[
f(x)=(x-1)(x-2)(x^2+6x+4)=x^4+3x^3-12x^2-8x+8
\]
이므로 $m=3$, $n=-12$이다. 따라서
\[
m^2+n^2=3^2+(-12)^2=153
\]
이다.
