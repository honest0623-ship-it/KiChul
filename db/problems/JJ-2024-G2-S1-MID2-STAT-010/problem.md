---
id: JJ-2024-G2-S1-MID2-STAT-010
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: '10'
difficulty: 2
level: 2
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-10
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q010.png
---

## Q
100 이하의 자연수 $n$ 중에서 $ {}_{n}C_{1}+{}_{n}C_{2}+{}_{n}C_{3}+\cdots+{}_{n}C_{n}$의 값이 5의 배수가 되도록 하는 자연수 $n$의 개수는?

## Choices
① 20
② 21
③ 22
④ 24
⑤ 25

## Answer
⑤

## Solution
이항정리로
$$
{}_{n}C_{1}+{}_{n}C_{2}+\cdots+{}_{n}C_{n}=2^{n}-1
$$
이다.
따라서 $2^{n}$을 5로 나누었을 때 나머지가 1이어야 한다.
$2^{1},2^{2},2^{3},2^{4}$를 5로 나눈 나머지는 차례로 $2,4,3,1$이고,
이 패턴이 4번마다 반복된다.
그러므로 $n$은 4의 배수여야 한다.
1부터 100까지 4의 배수는
$$
100\div 4=25
$$
개이다.
