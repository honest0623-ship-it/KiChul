---
id: JJ-2025-G2-S1-MID2-STAT-015
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-15
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
다음 식의 값을 만족하는 모든 자연수 $r$의 값의 합은?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">$ {}_{2}C_{0}+{}_{3}C_{1}+{}_{4}C_{2}+\cdots+{}_{10}C_{8}={}_{11}C_{r}$</div>

## Choices
① 9
② 10
③ 11
④ 12
⑤ 13

## Answer
③

## Solution
왼쪽은
$$
\sum_{k=0}^{8} {}_{k+2}C_{k}
=\sum_{i=2}^{10} {}_{i}C_{2}
$$
이고 항등식
$$
\sum_{i=2}^{10} {}_{i}C_{2} = {}_{11}C_{3}
$$
을 이용하면
$$
{}_{11}C_{r}={}_{11}C_{3}
$$
이다.
따라서
$$
r=3,\ 8
$$
이고 구하는 합은
$$
3+8=11
$$
이다.
