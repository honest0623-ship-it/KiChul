---
id: JJ-2025-G2-S1-MID2-STAT-104
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: '서답4번'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답4번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
다음 조건을 만족시키는 두 자연수 $a,b$의 순서쌍 $(a,b)$의 개수는?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">(가) 두 수 $a,b$의 곱은 짝수이다.<br/>(나) $5\le a\le b\le 15$</div>

## Choices

## Answer
45

## Solution
$5\le a\le b\le 15$를 만족하는 $(a,b)$의 전체 개수는
11개에서 중복조합 2개를 뽑는 것과 같으므로
$$
{}_{12}C_{2}=66
$$
이다.

곱이 짝수가 아니려면 $a,b$가 모두 홀수여야 한다.
5부터 15까지의 홀수는
$$
5,7,9,11,13,15
$$
로 6개.
따라서 $a\le b$인 홀수쌍의 개수는
$$
{}_{7}C_{2}=21
$$
이다.

구하는 개수는
$$
66-21=45
$$
이다.
