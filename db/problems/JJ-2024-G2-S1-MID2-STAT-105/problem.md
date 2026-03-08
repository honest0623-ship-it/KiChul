---
id: JJ-2024-G2-S1-MID2-STAT-105
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 5
source_question_kind: subjective
source_question_label: '서답5번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서답형(서술형)
- 출제번호-서답5번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q020.png
---

## Q
다음 조건을 만족시키는 자연수 $N$의 개수를 구하시오.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">(가) $N$은 4자리의 자연수이며, 짝수이다.<br/>(나) $N$의 각 자리의 수의 합은 6이다.</div>

## Choices

## Answer
34

## Solution
천, 백, 십, 일의 자리를 $a,b,c,d$라 하면
$$
a+b+c+d=6,\quad a\ge 1,\quad d\text{는 짝수}
$$
이다.
$d=0,2,4,6$으로 나누어 센다.

1. $d=0$: $a-1+b+c=5$
$$
{}_{7}C_{2}=21
$$
2. $d=2$: $a-1+b+c=3$
$$
{}_{5}C_{2}=10
$$
3. $d=4$: $a-1+b+c=1$
$$
{}_{3}C_{2}=3
$$
4. $d=6$: 불가능

따라서 전체 개수는
$$
21+10+3=34
$$
이다.
