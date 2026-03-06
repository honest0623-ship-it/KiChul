---
id: JJ-2025-G2-S1-MID2-STAT-010
school: JJ
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 10
source_question_kind: objective
source_question_label: '10'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-10
- 과목-확률과통계
assets:
- assets/original/
- assets/original/JJ.2025.G2.S1.MID2.STAT.pdf
---

## Q
집합 $X=\{1,2,3,4,5\}$에 대하여 $X$에서 $X$로의 함수 중에서 임의로 하나를 선택할 때, $f(1)+f(2)+f(3)=6$을 만족시키고 집합 $\{y\mid y=f(x),\ x\in X\}$의 원소의 개수가 2개인 함수 $f$의 개수는?

## Choices
① 16
② 18
③ 20
④ 22
⑤ 24

## Answer
⑤

## Solution
$(f(1),f(2),f(3))=(a,b,c)$라 하자.
$a+b+c=6$이고 각 값은 1부터 5까지이다.

가능한 순서쌍 형태는
$$
(2,2,2),\quad (1,1,4)\text{의 순열},\quad (1,2,3)\text{의 순열}
$$
이다.

1. $(2,2,2)$인 경우  
첫 세 값의 상은 $\{2\}$이다. 전체 상의 개수가 2가 되려면
$f(4),f(5)$는 $2$와 어떤 값 $t(\ne 2)$만 사용해야 하고,
둘 다 2인 경우는 제외한다.
$t$ 선택 4가지, 각 $t$마다 $(f(4),f(5))$는 3가지이므로 12가지.

2. $(1,1,4)$의 순열인 경우  
순열은 3가지.
이미 상이 $\{1,4\}$이므로 $f(4),f(5)$는 각각 1 또는 4여야 한다.
각 순열마다 $2^2=4$가지이므로 12가지.

3. $(1,2,3)$의 순열인 경우  
이미 상의 개수가 3이므로 불가능.

따라서 전체 개수는
$$
12+12=24
$$
이다.
