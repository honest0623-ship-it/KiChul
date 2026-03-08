---
id: BY-2025-G2-S1-MID2-STAT-014
school: BY
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
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
- 출제번호-14
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2025.G2.S1.MID2.STAT.Q014.original.png
---

## Q
다음 조건을 만족시키는 음이 아닌 정수 $x, y, z, w$의 모든 순서쌍 $(x,y,z,w)$의 개수는?

(가) $x+y+z+w=15$

(나) $1<x+y+z<9$

## Choices
① 161
② 169
③ 177
④ 186
⑤ 200

## Answer
①

## Solution
$s=x+y+z$라 두면 조건 (나)에 의해
$$
s=2,3,4,5,6,7,8
$$
이다.

각 $s$에 대해 $(x,y,z)$의 개수는
$$
{}_{s+2}C_{2}
$$
이고, $w=15-s$로 하나로 정해진다.

따라서 전체 개수는
$$
\sum_{s=2}^{8} {}_{s+2}C_{2}
= {}_{11}C_{3}-{}_{4}C_{3}
=165-4=161
$$
이다.
