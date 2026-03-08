---
id: JJ-2024-G2-S1-MID2-STAT-101
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 1
source_question_kind: subjective
source_question_label: '서답1번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서답형(단답형)
- 출제번호-서답1번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q016.png
---

## Q
좌표평면 위에서 좌우 방향 또는 상하 방향으로 한 번에 한 칸씩 움직이는 점 $A$가 있다. 원점 $O$에서 출발한 점 $A$가 5번 움직여서 점 $B(1,2)$의 위치에 오는 경우의 수를 구하시오.

## Choices

## Answer
50

## Solution
오른쪽, 왼쪽, 위, 아래 이동 횟수를 각각 $R,L,U,D$라 하면
$$
R-L=1,\quad U-D=2,\quad R+L+U+D=5
$$
이다.
$R=L+1$, $U=D+2$를 대입하면
$$
2L+2D+3=5\Rightarrow L+D=1
$$
이므로 경우는 두 가지이다.

1. $(L,D)=(0,1)$이면 $(R,U)=(1,3)$
$$
\frac{5!}{1!3!1!}=20
$$
2. $(L,D)=(1,0)$이면 $(R,U)=(2,2)$
$$
\frac{5!}{2!2!1!}=30
$$
따라서 전체 경우의 수는
$$
20+30=50
$$
이다.
