---
id: BY-2025-G1-S1-MID-017
school: BY
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: '3'
level: 3
unit: 공통수학1 > 방정식과 부등식 > 복소수
unit_l1: 공통수학1
unit_l2: 방정식과 부등식
unit_l3: 복소수
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-17
assets:
- assets/original/
- assets/original/017.png
---

## Q
최고차항의 계수가 $1$인 두 이차식 $P(x),\ Q(x)$에 대하여 모든 계수가 정수이고, $P(3)=Q(3)=0$, $P(2)Q(4)=3$을 만족한다. $P(x)Q(x)$는 $(x-k)^2$을 인수로 가지며 $P(x),Q(x)$는 각각 $(x-k)^2$을 인수로 갖지 않을 때, 가능한 $P(1)$의 최댓값은?

## Choices
① $-4$  
② $-2$  
③ $0$  
④ $2$  
⑤ $4$

## Answer
③

## Solution
$P(3)=Q(3)=0$이고 최고차항 계수가 1, 계수가 정수이므로
$$
P(x)=(x-3)(x-a),\quad Q(x)=(x-3)(x-b)\quad(a,b\in\mathbb{Z})
$$
로 둘 수 있다.

$$
P(2)=a-2,\quad Q(4)=4-b
$$
이므로
$$
(a-2)(4-b)=3.
$$
정수쌍을 찾으면
$$
(a-2,\ 4-b)=( -1,-3),(1,3),(3,1),(-3,-1).
$$
여기서 $P,Q$가 각각 $(x-3)^2$을 인수로 가지지 않아야 하므로 $a\ne3,\ b\ne3$.
가능한 경우는 $(a,b)=(1,7),\ (-1,5)$.

이때
$$
P(1)=(1-3)(1-a)=2(a-1)
$$
이므로
$$
a=1 \Rightarrow P(1)=0,\quad a=-1 \Rightarrow P(1)=-4.
$$
따라서 최댓값은 $0$.
