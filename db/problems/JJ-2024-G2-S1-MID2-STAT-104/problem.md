---
id: JJ-2024-G2-S1-MID2-STAT-104
school: JJ
year: 2024
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: '서답4번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서답형(서술형)
- 출제번호-서답4번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2024.G2.S1.MID2.STAT_q019.png
---

## Q
두 단계로 구성된 $A,B,C$ 미션이 있다. 각 미션은 1단계를 통과해야 2단계 미션을 통과할 수 있다. 예를 들어,

<div style="border:1px solid #000; padding:8px; margin:8px 0;">$A(1\text{단계}) \rightarrow B(1\text{단계}) \rightarrow A(2\text{단계})$<br/>$\rightarrow C(1\text{단계}) \rightarrow B(2\text{단계}) \rightarrow C(2\text{단계})$</div>

6개의 미션을 모두 수행하는 경우의 수를 구하시오.

## Choices

## Answer
90

## Solution
수행 순서를 $A_{1},A_{2},B_{1},B_{2},C_{1},C_{2}$의 배열로 보면
전체 순열 수는
$$
6!
$$
이다.
각 미션마다 1단계가 2단계보다 먼저 와야 하므로
각 쌍에서 절반만 허용된다.
세 쌍을 반영하면
$$
\frac{6!}{2^{3}}=\frac{720}{8}=90
$$
이다.
