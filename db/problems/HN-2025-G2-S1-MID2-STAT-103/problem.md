---
id: HN-2025-G2-S1-MID2-STAT-103
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3번
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>2. 확률>2-2. 조건부 확률
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-2. 조건부 확률
source: user_upload_2026-03-05
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답3번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
좌표평면의 원점에 점 $P$가 있다.
주사위를 한 번 던져서 짝수의 눈이 나오면 $x$축의 방향으로 2만큼 평행이동하고,
홀수의 눈이 나오면 $y$축의 방향으로 3만큼 평행이동한다.
주사위를 6번 던질 때, 점 $P$가 직선 $y=2x-3$ 위에 있을 확률을 구하시오.

## Choices


## Answer
$\frac{5}{16}$

## Solution
주사위를 6번 던져 짝수가 나온 횟수를 $e$, 홀수가 나온 횟수를 $o$라 하면
$$
e+o=6
$$
이다.

이때 최종 좌표는
$$
(x,y)=(2e,\ 3o)=(2e,\ 3(6-e))=(2e,\ 18-3e)
$$
이다.

직선 $y=2x-3$ 위에 있으려면
$$
18-3e=2(2e)-3
$$
$$
21=7e\Rightarrow e=3
$$
이어야 한다.

즉 6번 중 짝수가 정확히 3번 나올 확률이므로
$$
{}_{6}C_{3}\left(\frac12\right)^6=\frac{20}{64}=\frac{5}{16}
$$
이다.
