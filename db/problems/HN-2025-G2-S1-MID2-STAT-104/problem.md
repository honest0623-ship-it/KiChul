---
id: HN-2025-G2-S1-MID2-STAT-104
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-05
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답4번
- 과목-확률과통계
- ??????-2026-03-05
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
다음 조건을 만족시키는 음이 아닌 정수 $a,b,c,d$의 순서쌍 $(a,b,c,d)$의 개수를
구하는 풀이 과정과 답을 쓰시오.

(가) $a+b+c+d=6$
(나) $a\ne b$

## Choices


## Answer
68

## Solution
먼저 $a,b,c,d\ge 0$에서
$$
a+b+c+d=6
$$
의 전체 해의 개수는
$$
{}_{6+4-1}C_{4-1}={}_{9}C_{3}=84
$$
이다.

이제 조건 $a\ne b$를 반영하기 위해 $a=b$인 경우를 뺀다.
$a=b=t$로 두면
$$
2t+c+d=6
$$
이다.

$t=0,1,2,3$에 대해 $(c,d)$의 개수는 각각
$$
7,\ 5,\ 3,\ 1
$$
이므로 합은 $16$이다.

따라서 조건을 만족하는 개수는
$$
84-16=68
$$
이다.
