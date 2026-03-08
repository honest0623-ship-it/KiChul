---
id: SY-2022-G2-S1-MID2-STAT-105
school: SY
year: 2022
grade: 2
semester: 1
exam: MID2
subject: STAT
type: subjective
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5번
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답5번
- 과목-STAT
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/SY-2022-G2-S1-MID2-STAT-105_original.png
---

## Q
네 개의 숫자 $1$, $2$, $3$, $4$에서 중복을 허용하여 $4$개를 뽑아 네 자리 자연수를 만들 때, $1$은 연속하여 사용하지 않고 만들 수 있는 자연수의 개수를 구하시오.

## Choices


## Answer
$216$

## Solution
전체 네 자리 수의 개수는
\[
4^4=256
\]
이다.

이제 $11$이 적어도 한 번 나타나는 경우를 뺀다.

\[
A_1=\text{앞의 두 자리가 }11,\quad
A_2=\text{가운데 두 자리가 }11,\quad
A_3=\text{뒤의 두 자리가 }11
\]
라 하자.

그러면
\[
|A_1|=|A_2|=|A_3|=4^2=16
\]
이고,
\[
|A_1\cap A_2|=4,\quad |A_2\cap A_3|=4,\quad |A_1\cap A_3|=1
\]
이며,
\[
|A_1\cap A_2\cap A_3|=1
\]
이다.

따라서 포함배제의 원리에 의해 $11$이 적어도 한 번 나타나는 경우의 수는
\[
16+16+16-4-4-1+1=40
\]
이다.

그러므로 구하는 개수는
\[
256-40=216
\]
이다.
