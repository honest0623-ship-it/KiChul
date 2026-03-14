---
id: BY-2020-G2-S1-MID2-014
school: BY
year: 2020
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
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-14
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q014.original.png
---

## Q
21개의 서로 다른 볼펜과 20개의 똑같은 연필 중에서 10개를 골라 선물 세트를 만들려고 한다. 만들 수 있는 선물 세트의 방법의 수는?

## Choices
① $2^{20}$
② $2^{20}+1$
③ $2^{21}-1$
④ $2^{21}$
⑤ $2^{21}+1$

## Answer
①

## Solution
볼펜을 $k$개 고르면 $(0\le k\le 10)$, 연필은 $10-k$개로 자동 결정된다.
따라서 경우의 수는
$$
\sum_{k=0}^{10} {}_{21}C_k
$$
이다.

$21$은 홀수이므로 이항계수 대칭성에 의해
$$
\sum_{k=0}^{10} {}_{21}C_k=2^{20}
$$
이다.
