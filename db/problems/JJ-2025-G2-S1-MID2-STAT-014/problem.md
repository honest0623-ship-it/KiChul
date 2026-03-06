---
id: JJ-2025-G2-S1-MID2-STAT-014
school: JJ
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
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
네 명의 학생 $A,B,C,D$에게 같은 종류의 사과 5개와 같은 종류의 배 2개를 다음 조건을 만족하도록 남김없이 나누어 주는 방법의 수는?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">모든 학생이 사과 또는 배를 1개 이상씩 받도록 한다.</div>

## Choices
① 120
② 130
③ 140
④ 150
⑤ 160

## Answer
⑤

## Solution
조건 없이 나누는 방법은
$$
{}_{8}C_{3}\times {}_{5}C_{3}=56\times 10=560
$$
이다.

이제 포함배제를 쓴다.

한 학생이 아무것도 받지 않는 경우(예: A)는
$$
{}_{7}C_{2}\times {}_{4}C_{2}=21\times 6=126
$$
이고 학생 선택 4가지이므로 $4\times 126=504$.

두 학생이 아무것도 받지 않는 경우는
$$
{}_{6}C_{1}\times {}_{3}C_{1}=6\times 3=18
$$
이고 학생쌍 선택 6가지이므로 $6\times 18=108$.

세 학생이 아무것도 받지 않는 경우는 4가지.

따라서
$$
560-504+108-4=160
$$
이다.
