---
id: SY-2022-G2-S1-MID-ALG-104
school: SY
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: subjective
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답4번
- 과목-ALG
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID-ALG-104_original.png
---

## Q
$x$에 대한 로그부등식
\[
\log_3(x-1)\le \log_3\left(\frac{1}{2}x+k\right)
\]
를 만족시키는 모든 정수 $x$의 개수가 $5$일 때, 자연수 $k$의 값을 구하시오.

## Choices


## Answer
$2$

## Solution
밑이 $3$으로 $1$보다 크므로
\[
x-1\le \frac{1}{2}x+k
\]
와 동치이다.

정의역 조건은
\[
x-1>0,\qquad \frac{1}{2}x+k>0
\]
이다. 자연수 $k$에 대하여 두 번째 조건은 $x>1$보다 약하다.

따라서
\[
x>1,\qquad x\le 2k+2
\]
이다.

정수해는
\[
2,3,\ldots,2k+2
\]
이므로 개수는
\[
(2k+2)-2+1=2k+1
\]
이다.

이것이 $5$이므로
\[
2k+1=5
\]
에서
\[
k=2
\]
이다.
