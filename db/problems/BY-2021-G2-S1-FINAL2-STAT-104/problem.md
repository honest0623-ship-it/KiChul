---
id: BY-2021-G2-S1-FINAL2-STAT-104
school: BY
year: 2021
grade: 2
semester: 1
exam: FINAL2
subject: STAT
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 5
level: 5
unit: 확률과 통계(2022개정)>2. 확률>2-2. 조건부 확률
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-2. 조건부 확률
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서답형(서술형)
- 출제번호-서답4번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2021.G2.S1.FINAL2.STAT.q104.png
---

## Q
태은이와 민규는 체중감량을 위해 다음과 같은 규칙으로 가위바위보를 하여 계단을 오르는 게임을 한다.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">이긴 사람은 위로 두 계단 올라간다.<br/>진 사람은 아래로 한 계단 내려간다.<br/>비기면 두 사람 모두 위로 한 계단 올라간다.</div>

가위바위보를 5번 한 후, 태은이가 처음 위치보다 세 계단 올라갔을 때, 태은이가 가위바위보를 한 번도 이기지 못했을 확률을 구하여라.

(1) 태은이가 세 계단을 올라가는 사건을 $A$, 태은이가 가위바위보를 한 번도 이기지 못하는 사건을 $B$라 할 때, 문제에서 구하고자 하는 확률을 조건부확률을 이용하여 나타내어라.

(2) 가위바위보를 5번 한 후 태은이가 세 계단을 올라가는 경우를 각각 구하고, $P(A)$를 구하여라.

(3) $P(A\cap B)$를 구하여라.

(4) $P(B\mid A)$를 구하여라.

## Choices


## Answer
$\dfrac{1}{7}$

## Solution
태은이 기준으로 1회 결과를 다음과 같이 둔다.
이김 $W$ : $+2$, 짐 $L$ : $-1$, 비김 $D$ : $+1$.
각 결과의 확률은 모두 $\dfrac{1}{3}$이다.

(1) 구하려는 값은
$$
P(B\mid A)=\dfrac{P(A\cap B)}{P(A)}
$$
이다.

(2) 5회 후 상승량이 3이 되려면
$$
2w-l+d=3,\quad w+l+d=5
$$
을 만족해야 한다.
해는 $(w,d,l)=(0,4,1),(2,1,2)$뿐이다.
따라서 경우의 수는
$$
{}_{5}C_{1}+\dfrac{5!}{2!1!2!}=5+30=35
$$
이고
$$
P(A)=\dfrac{35}{3^{5}}=\dfrac{35}{243}
$$
이다.

(3) $A\cap B$는 "세 계단 상승"이면서 "한 번도 이기지 못함"이므로 $(w,d,l)=(0,4,1)$뿐이다.
따라서
$$
P(A\cap B)=\dfrac{{}_{5}C_{1}}{3^{5}}=\dfrac{5}{243}
$$
이다.

(4) 따라서
$$
P(B\mid A)=\dfrac{\frac{5}{243}}{\frac{35}{243}}=\dfrac{1}{7}
$$
이다.
