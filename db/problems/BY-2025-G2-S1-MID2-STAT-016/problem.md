---
id: BY-2025-G2-S1-MID2-STAT-016
school: BY
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
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
- 출제번호-16
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2025.G2.S1.MID2.STAT.Q016.original.png
---

## Q
같은 종류의 연필 7자루와 서로 다른 지우개 2개를
5명의 학생 $A,B,C,D,E$에게 남김없이 나누어 주려고 한다.
지우개를 받은 학생에게 적어도 2자루의 연필을 나누어 주는 경우의 수는?
(단, 연필과 지우개를 못 받는 학생이 있을 수 있다.)

## Choices
① 790
② 970
③ 1070
④ 1210
⑤ 1330

## Answer
⑤

## Solution
경우를 나눈다.

1. 지우개 2개를 서로 다른 두 학생이 받는 경우

지우개가 서로 다르므로 학생 선택은
$$
{}_{5}P_{2}=20
$$
가지이다.

이 두 학생은 각각 연필을 2자루 이상 받아야 하므로 먼저 2자루씩 주면,
남은 연필 3자루를 5명에게 자유롭게 주는 방법은
$$
{}_{3+5-1}C_{5-1}={}_{7}C_{4}=35
$$
가지이다.

따라서
$$
20\times 35=700
$$
가지.

2. 지우개 2개를 한 학생이 모두 받는 경우

학생 선택은 5가지이고,
그 학생에게 연필 2자루를 먼저 주면 남은 연필 5자루를 5명에게 주는 방법은
$$
{}_{5+5-1}C_{5-1}={}_{9}C_{4}=126
$$
가지이다.

따라서
$$
5\times 126=630
$$
가지.

전체 경우의 수는
$$
700+630=1330
$$
이다.
