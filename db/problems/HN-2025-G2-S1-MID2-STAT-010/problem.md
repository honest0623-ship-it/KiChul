---
id: HN-2025-G2-S1-MID2-STAT-010
school: HN
year: 2025
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
unit: 확률과 통계(2022개정)>2. 확률>2-1. 확률의 뜻과 활용
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-1. 확률의 뜻과 활용
source: user_upload_2026-03-05
tags:
- 수동작성
- 객관식
- 출제번호-10
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
1부터 10까지의 자연수가 각각 하나씩 적힌 카드 10장 중 임의로 1장을 뽑는 시행에서,
카드에 적힌 수가 10의 약수인 사건을 $A$, 8의 약수인 사건을 $B$라고 할 때,
사건 $A$와는 배반이고 사건 $B$와는 배반이 아닌 사건의 개수는?

## Choices
① 16
② 32
③ 48
④ 64
⑤ 80

## Answer
③

## Solution
표본공간을 $S=\{1,2,\dots,10\}$라 하자.

$A=\{1,2,5,10\}$, $B=\{1,2,4,8\}$이다.

사건 $E$가 $A$와 배반이라는 것은 $E\subseteq S-A$라는 뜻이다.
따라서 가능한 원소는
$$
S-A=\{3,4,6,7,8,9\}
$$
의 6개이다.

또 $E$가 $B$와 배반이 아니려면 $E\cap B\ne\varnothing$이어야 한다.
$S-A$ 안에서 $B$의 원소는 $\{4,8\}$이므로,
$E$는 4 또는 8을 적어도 하나 포함해야 한다.

전체 부분집합 수는 $2^6=64$,
4와 8을 모두 포함하지 않는 부분집합 수는 나머지 4원소 부분집합 수 $2^4=16$이다.

따라서
$$
64-16=48
$$
이다.
