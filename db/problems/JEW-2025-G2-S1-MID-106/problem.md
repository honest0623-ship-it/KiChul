---
id: JEW-2025-G2-S1-MID-106
school: JEW
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 6
source_question_kind: subjective
source_question_label: 서답6
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-6
assets:
- assets/original/
- assets/original/서답6번_1-1. 지수와 로그.png
---
## Q
다음 이차방정식
$$
x^2-4x-9=0
$$
의 두 근이 $\log_2 a$, $\log_2 b$일 때,
$$
\log_a b-\log_b a=\frac{n\sqrt{13}}{m}
$$
이다. 이때 $m\times n$의 값을 구하는 과정과 답을 쓰시오.

(단, $a,\ b,\ m,\ n$은 실수이고 $b>a$이다.)

## Choices

## Answer
$-72$

## Solution
두 근을
$$
p=\log_2 a,\qquad q=\log_2 b
$$
라 두면 $b>a$이므로 $q>p$이다.

이차방정식 $x^2-4x-9=0$의 근은
$$
2\pm\sqrt{13}
$$
이므로
$$
p=2-\sqrt{13},\qquad q=2+\sqrt{13}
$$
이다.

따라서
$$
p+q=4,\qquad pq=-9,\qquad q-p=2\sqrt{13}
$$
이다.

또
$$
\log_a b=\frac{\log_2 b}{\log_2 a}=\frac{q}{p},\qquad
\log_b a=\frac{\log_2 a}{\log_2 b}=\frac{p}{q}
$$
이므로
$$
\log_a b-\log_b a
=\frac{q}{p}-\frac{p}{q}
=\frac{q^2-p^2}{pq}
=\frac{(q-p)(q+p)}{pq}
$$
$$
=\frac{(2\sqrt{13})\cdot 4}{-9}
=-\frac{8\sqrt{13}}{9}
$$
이다.

따라서
$$
\frac{n\sqrt{13}}{m}=-\frac{8\sqrt{13}}{9}
$$
에서 $n=-8$, $m=9$로 둘 수 있으므로
$$
m\times n=9\times(-8)=-72
$$
이다.
