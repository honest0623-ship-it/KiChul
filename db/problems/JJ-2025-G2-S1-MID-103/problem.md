---
id: JJ-2025-G2-S1-MID-103
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: '서답3'
difficulty: '5'
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-02
tags:
- 단답형
- 출제번호-3
assets:
- assets/original/
- assets/original/서답3번_1-1. 지수와 로그.png
---
## Q
$1000$ 이하의 자연수 $n$에 대하여
\[
3\log_{81}\left(\left(\frac{2}{3n+15}\right)^2\right)
\]
의 값이 정수가 되도록 하는 $n$의 최댓값을 구하시오.

## Choices

## Answer
$481$

## Solution
\[
3\log_{81}\left(\left(\frac{2}{3n+15}\right)^2\right)=m
\]
($m$은 정수)라 두면
\[
\left(\frac{2}{3n+15}\right)^2 = 81^{m/3}=3^{\frac{4m}{3}}
\]
이다.

왼쪽은 유리수이므로 $3^{\frac{4m}{3}}$도 유리수여야 한다.
따라서 $m$은 $3$의 배수여야 하므로 $m=3q$로 둘 수 있다.

그러면
\[
\left(\frac{2}{3n+15}\right)^2 = 81^q
\]
이고, 왼쪽이 $1$보다 작으므로 $q=-r$ ($r$은 자연수)이다.
즉
\[
\left(\frac{2}{3n+15}\right)^2 = 81^{-r}=3^{-4r}
\]
이므로
\[
\frac{2}{3n+15}=3^{-2r}
\]
\[
3n+15=2\cdot 3^{2r}
\]
\[
n+5=2\cdot 3^{2r-1}
\]
을 얻는다.

$n\le 1000$에서 가능한 값은
\[
r=1,2,3
\]
이고, 이때
\[
n=1,\ 49,\ 481
\]
이다.
따라서 최댓값은
\[
481
\]
이다.
