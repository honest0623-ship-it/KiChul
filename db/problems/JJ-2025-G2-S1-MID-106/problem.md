---
id: JJ-2025-G2-S1-MID-106
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 6
source_question_kind: subjective
source_question_label: '서답6'
difficulty: '5'
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-02
tags:
- 서술형
- 출제번호-6
assets:
- assets/original/
- assets/original/서답6번_1-1. 지수와 로그.png
---
## Q
$\sqrt[4]{2^3}$ 이 어떤 자연수의 $n$제곱근일 때, 자연수 $n$의 개수를 $k$라 하자.
\[
\frac{1}{2^{-k}+1}
+\cdots+
\frac{1}{2^{-2}+1}
+
\frac{1}{2^0+1}
+
\frac{1}{2^2+1}
+\cdots+
\frac{1}{2^k+1}
\]
의 값을 구하시오.
(단, $2\le n\le 75$, $n$은 자연수)

## Choices

## Answer
\[
\frac{19}{2}
\]

## Solution
\[
\sqrt[4]{2^3}=2^{3/4}
\]
가 어떤 자연수의 $n$제곱근이 되려면
\[
2^{3/4}=m^{1/n}
\]
인 자연수 $m$이 존재해야 한다.
즉
\[
m=2^{\frac{3n}{4}}
\]
가 자연수여야 하므로 $\frac{3n}{4}$는 정수이다.
따라서 $n$은 $4$의 배수이다.

$2\le n\le 75$에서 가능한 $n$은
\[
4,8,12,\ldots,72
\]
이고, 개수는
\[
k=18
\]
이다.

이제
\[
S=
\frac{1}{2^{-18}+1}
+\frac{1}{2^{-16}+1}
+\cdots+
\frac{1}{2^{18}+1}
\]
로 두자.

$j>0$에 대하여
\[
\frac{1}{2^j+1}+\frac{1}{2^{-j}+1}
=
\frac{1}{2^j+1}+\frac{2^j}{2^j+1}
=1
\]
이므로, $j=2,4,\ldots,18$의 $9$쌍의 합은 $9$이다.
또 가운데 항은
\[
\frac{1}{2^0+1}=\frac{1}{2}
\]
이다.

따라서
\[
S=9+\frac{1}{2}=\frac{19}{2}
\]
이다.

