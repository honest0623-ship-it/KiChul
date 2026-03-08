---
id: BY-2025-G2-S1-MID2-STAT-013
school: BY
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-13
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2025.G2.S1.MID2.STAT.Q013.original.png
---

## Q
다항식 $\left(x^3-\dfrac{a}{x^5}\right)^8$의 전개식에서 상수항이 448일 때,
$x^{16}$의 계수는? (단, $a$는 상수이다.)

## Choices
① 16
② 19
③ 22
④ 25
⑤ 28

## Answer
①

## Solution
일반항은
$$
{}_{8}C_{k}(x^3)^{8-k}\left(-\frac{a}{x^5}\right)^k
={}_{8}C_{k}(-a)^k x^{24-8k}
$$
이다.

상수항은 $24-8k=0$에서 $k=3$일 때이므로
$$
{}_{8}C_{3}(-a)^3=448
$$
$$
56(-a^3)=448\Rightarrow a^3=-8\Rightarrow a=-2
$$
이다.

$x^{16}$항은 $24-8k=16$에서 $k=1$일 때이므로 계수는
$$
{}_{8}C_{1}(-a)=8\times 2=16
$$
이다.
