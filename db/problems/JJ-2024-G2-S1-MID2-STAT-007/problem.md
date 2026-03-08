---
id: JJ-2024-G2-S1-MID2-STAT-007
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: '7'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-7
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q007.png
---

## Q
일곱 개의 숫자 $0,1,1,2,2,2,3$을 모두 사용하여 만들 수 있는 일곱 자리의 자연수 중에서 짝수의 개수는?

## Choices
① 120
② 150
③ 180
④ 210
⑤ 240

## Answer
④

## Solution
끝자리가 0인 경우:
남은 6자리 배열 수는
$$
\frac{6!}{2!3!}=60
$$
이다.

끝자리가 2인 경우:
남은 배열 수는
$$
\frac{6!}{2!2!}=180
$$
인데, 맨 앞이 0인 경우
$$
\frac{5!}{2!2!}=30
$$
을 빼면 $150$이다.

따라서 전체는
$$
60+150=210
$$
이다.
