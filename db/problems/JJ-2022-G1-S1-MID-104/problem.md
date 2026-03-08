---
id: JJ-2022-G1-S1-MID-104
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 4
source_question_kind: subjective
source_question_label: 서4
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서4
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---

## Q
최고차항의 계수가 $1$인 삼차식 $f(x)$가 다음 조건을 만족한다.

(가) $f(x)$를 $x-1$로 나눈 나머지가 $2$이다.
(나) 모든 실수 $x$에 대하여 $f(2+x)=-f(2-x)$이 성립한다.

다항식 $f(x)$를 $x^2-4x+3$로 나눈 나머지를 구하시오.

## Choices


## Answer
$-2x+4$

## Solution
조건 (나)를 이용하기 쉽도록
\[
f(x)=(x-2)^3+p(x-2)^2+q(x-2)+r
\]
로 두자.

그러면
\[
f(2+x)=x^3+px^2+qx+r
\]
이고,
\[
f(2-x)=(-x)^3+p(-x)^2+q(-x)+r=-x^3+px^2-qx+r
\]
이므로
\[
-f(2-x)=x^3-px^2+qx-r
\]
이다.

조건 $f(2+x)=-f(2-x)$에서
\[
x^3+px^2+qx+r=x^3-px^2+qx-r
\]
이므로
\[
p=0,\qquad r=0
\]
이다. 따라서
\[
f(x)=(x-2)^3+q(x-2)
\]
이다.

또 $f(x)$를 $x-1$로 나눈 나머지가 $2$이므로 $f(1)=2$이다. 따라서
\[
(-1)^3+q(-1)=2
\]
\[
-1-q=2
\]
\[
q=-3
\]
이다.

따라서
\[
f(x)=(x-2)^3-3(x-2)=x^3-6x^2+9x-2
\]
이다.

이제 $f(x)$를 $x^2-4x+3=(x-1)(x-3)$로 나눈 나머지를 $R(x)=ax+b$라 하자.
그러면
\[
R(1)=f(1)=2,\qquad R(3)=f(3)=-2
\]
이다.

두 점 $(1,2)$, $(3,-2)$를 지나는 일차식은
\[
R(x)=-2x+4
\]
이므로 구하는 나머지는
\[
\boxed{-2x+4}
\]
이다.
