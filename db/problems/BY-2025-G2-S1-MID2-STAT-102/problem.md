---
id: BY-2025-G2-S1-MID2-STAT-102
school: BY
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(단답형)
source_question_no: 2
source_question_kind: subjective
source_question_label: '서답2번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답2번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2025.G2.S1.MID2.STAT.Q102.original.png
---

## Q
${}_{12}C_{1}\times{}_{16}C_{16}+{}_{12}C_{2}\times{}_{16}C_{15}+{}_{12}C_{3}\times{}_{16}C_{14}+\cdots+{}_{12}C_{11}\times{}_{16}C_{6}+{}_{12}C_{12}\times{}_{16}C_{5}= {}_{a}C_{b}$일 때,
두 상수 $a,b$에 대하여 $a+b$의 값을 구하시오. (단, $a<2b$)

## Choices

## Answer
45

## Solution
주어진 합은
$$
\sum_{k=1}^{12} {}_{12}C_{k}\,{}_{16}C_{17-k}
$$
형태이다.
$k=0$일 때 항은 ${}_{16}C_{17}=0$이므로 범위를 0부터로 바꿔도 같다.

반더몬드 항등식으로
$$
\sum_{k=0}^{12} {}_{12}C_{k}\,{}_{16}C_{17-k}={}_{28}C_{17}
$$
이므로
$$
a=28,\ b=17
$$
이고,
$$
a+b=45
$$
이다.
