---
id: JE-2025-G2-S1-MID-104
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-4
assets:
- assets/original/
- assets/original/서답4번_1-1. 지수와 로그.png
---
## Q
$$
2^x=(\sqrt5)^y=(\sqrt{10})^z
$$
일 때,
$$
\frac{2}{x}+\frac{4}{y}-\frac{4}{z}
$$
의 값을 구하는 과정을 서술하시오. (단, $xyz\ne 0$)

## Choices

## Answer
$0$

## Solution
공통값을 $t$라 두면
$$
2^x=t,\quad (\sqrt5)^y=t,\quad (\sqrt{10})^z=t
$$
이다.

따라서
$$
x=\log_2 t,\quad
y=\log_{\sqrt5} t,\quad
z=\log_{\sqrt{10}} t
$$
이다.

이제 각 항을 자연로그로 바꾸면
$$
\frac{2}{x}
=\frac{2}{\log_2 t}
=\frac{2\ln2}{\ln t}
$$
$$
\frac{4}{y}
=\frac{4}{\log_{\sqrt5} t}
=\frac{4\ln\sqrt5}{\ln t}
=\frac{2\ln5}{\ln t}
$$
$$
\frac{4}{z}
=\frac{4}{\log_{\sqrt{10}} t}
=\frac{4\ln\sqrt{10}}{\ln t}
=\frac{2\ln10}{\ln t}
$$
이다.

그러므로
$$
\frac{2}{x}+\frac{4}{y}-\frac{4}{z}
=\frac{2\ln2+2\ln5-2\ln10}{\ln t}
=0
$$
이다.
