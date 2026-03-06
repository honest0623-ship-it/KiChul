---
id: JJ-2025-G2-S1-MID2-STAT-102
school: JJ
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
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답2번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
1에서 10까지의 자연수가 하나씩 적힌 10장의 카드 중에서 한 장의 카드를 뽑아서 숫자를 확인하는 시행을 세 번 반복한다. 세 번 반복한 결과 얻은 세 수를 차례대로 $x,y,z$라고 할 때, 세 수 $x,y,z$의 합이 3으로 나누어 떨어지는 경우의 수를 구하여라.

## Choices

## Answer
334

## Solution
1부터 10까지를 3으로 나눈 나머지별 개수는
$$
0\text{인 수 }3\text{개},\quad
1\text{인 수 }4\text{개},\quad
2\text{인 수 }3\text{개}
$$
이다.

합이 3의 배수가 되는 나머지 조합은
$$
(0,0,0),\ (1,1,1),\ (2,2,2),\ (0,1,2)의 순열
$$
이다.

따라서 경우의 수는
$$
3^3 + 4^3 + 3^3 + 6\times 3\times 4\times 3
=27+64+27+216=334
$$
이다.
