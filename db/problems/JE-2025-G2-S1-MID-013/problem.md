---
id: JE-2025-G2-S1-MID-013
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-13
assets:
- assets/scan.png
- assets/original/
- assets/original/013_1-2. 지수함수.png
- assets/original/013_1-2. 지수함수_scan.png
---
## Q
다음 그림의 일차함수 $y=f(x)$와 $y=g(x)$에 대하여
$$
\left(\frac{1}{3}\right)^{f(x)g(x)}
<
\left(\frac{1}{27}\right)^{f(x)}
$$
을 만족하는 정수 $x$값의 합을 구하면?

<img src="assets/scan.png" style="width: 100%; max-width: 100%;">

## Choices
① $-3$  
② $-2$  
③ $-1$  
④ $1$  
⑤ $2$

## Answer
②

## Solution
그림에서 $f(x)$는 $(-3,0)$, $(2,3)$을 지나므로
$$
f(x)=\frac{3}{5}(x+3)
$$
이고,

$g(x)$는 $(2,3)$, $(4,0)$을 지나므로
$$
g(x)=-\frac{3}{2}x+6
$$
이다.

또
$$
\left(\frac{1}{27}\right)^{f(x)}
=\left(\frac{1}{3}\right)^{3f(x)}
$$
이고 밑 $\frac{1}{3}$은 $1$보다 작으므로 지수의 대소가 반대로 되어
$$
f(x)g(x)>3f(x)
$$
즉
$$
f(x)\{g(x)-3\}>0
$$
이다.

여기서
$$
f(x)=\frac{3}{5}(x+3),\qquad
g(x)-3=-\frac{3}{2}(x-2)
$$
이므로
$$
\frac{3}{5}(x+3)\cdot\left(-\frac{3}{2}\right)(x-2)>0
$$
$$
\Longleftrightarrow (x+3)(x-2)<0
$$
따라서
$$
-3<x<2
$$
이다.

정수해는 $x=-2,-1,0,1$이고 합은
$$
-2
$$
이다.
