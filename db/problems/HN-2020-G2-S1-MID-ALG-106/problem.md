---
id: HN-2020-G2-S1-MID-ALG-106
school: HN
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 6
source_question_kind: subjective
source_question_label: 서답6
difficulty: 5
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-11
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서답6
- 과목-ALG
- 생성일-2026-03-11
assets:
- assets/original/
- assets/original/HN.2020.G2.S1.MID.ALG.SUB06.question.png
---

## Q
$x>0$에 대한 방정식
\[
(\log_2 x)^2-\log_2 x^2+a=0
\]
의 한 근이 방정식
\[
4x^2-9x+2=0
\]
의 두 근 사이에 존재할 때, 상수 $a$의 값의 범위를 구하여라.

## Choices


## Answer
$-8<a<1$

## Solution
먼저
\[
4x^2-9x+2=0
\]
의 근은
\[
x=\frac{9\pm\sqrt{81-32}}{8}
=\frac{9\pm7}{8}
\]
이므로
\[
\frac14,\ 2
\]
이다.

주어진 조건은 첫 번째 방정식의 근 중 하나가
\[
\frac14<x<2
\]
를 만족한다는 뜻이다.

$t=\log_2x$로 두면
\[
\log_2x^2=2\log_2x=2t
\]
이므로 식은
\[
t^2-2t+a=0
\]
가 된다.

또
\[
\frac14<x<2
\]
는
\[
-2<t<1
\]
와 같다.

이차방정식의 근은
\[
t=1\pm\sqrt{1-a}
\]
인데, $1+\sqrt{1-a}>1$이므로 구간 $(-2,1)$ 안에 들어갈 수 있는 근은
\[
t_1=1-\sqrt{1-a}
\]
뿐이다.

따라서
\[
-2<t_1<1
\]
이어야 하므로
\[
-2<1-\sqrt{1-a}
\Rightarrow \sqrt{1-a}<3
\Rightarrow a>-8
\]
그리고
\[
1-\sqrt{1-a}<1
\Rightarrow \sqrt{1-a}>0
\Rightarrow a<1
\]
이다.

따라서
\[
-8<a<1
\]
이다.
