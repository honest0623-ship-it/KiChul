---
id: HN-2025-G2-S1-MID2-STAT-105
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5번
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
- 출제번호-서답5번
- 과목-확률과통계
- ??????-2026-03-05
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
${}_{20}C_{0}+{}_{20}C_{2}\cdot 3^2+{}_{20}C_{4}\cdot 3^4+{}_{20}C_{6}\cdot 3^6+\cdots+{}_{20}C_{20}\cdot 3^{20}
=2^m(2^{20}+1)$일 때, 자연수 $m$의 값을 구하는 풀이 과정과 답을 쓰시오.

## Choices


## Answer
19

## Solution
주어진 합을 $S$라 하자.

짝수차 항의 합 공식으로
$$
S=\frac{(1+3)^{20}+(1-3)^{20}}{2}
$$
이다.

따라서
$$
S=\frac{4^{20}+(-2)^{20}}{2}
=\frac{2^{40}+2^{20}}{2}
=2^{39}+2^{19}
=2^{19}(2^{20}+1)
$$
이 된다.

그러므로 $m=19$이다.
