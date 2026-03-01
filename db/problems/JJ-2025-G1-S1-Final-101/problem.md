---
id: JJ-2025-G1-S1-Final-101
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 서술형
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 수동정제
- 서술형
- 출제번호-1
assets:
- assets/original/
- assets/original/서답1번.png
---
## Q
삼차식 $f(x)=x^3+ax^2+bx+c$이 다음 조건을 만족할 때, $f(3)$의 값을 $a_1,a_2,a_3,a_4,a_5$라 하자. 이때 $a_2+a_4$의 값을 구하시오. (단, $a,b,c$는 실수)

(가) 방정식 $f(x)=0$의 근 중 허근이 존재한다.
(나) $f(\alpha)=0$이면 $f(\alpha^3)=0$을 만족한다.
(다) $a_1<a_2<a_3<a_4<a_5$

## Choices


## Answer
56

## Solution
근을 $r_1,r_2,r_3$라 하자. 조건 (나)에서 근 집합은 사상 $x\mapsto x^3$에 대해 닫혀 있다.

실근 $t$에 대해서는 $t^3$도 실근이므로 $t^3=t$, 즉
$$
t\in\{-1,0,1\}
$$
이다.

허근을 $z$라 하면 실계수 다항식이므로 $\bar z$도 근이다. 가능한 경우를 나누면:

1) $z^3=\bar z$
$$
z^4=1\Rightarrow z=\pm i
$$
이때 근은 $\{i,-i,t\}$, $t\in\{-1,0,1\}$이고
$$
f(3)=(3-i)(3+i)(3-t)=10(3-t)
$$
이므로 값은 $20,30,40$.

2) $z^3=t$ (실근)
이 경우 $t=\pm1$이고 근은 각각 $x^3-1=0$ 또는 $x^3+1=0$의 세 근이 된다.
따라서
$$
f(3)=26,28.
$$

가능한 $f(3)$의 값은
$$
20,26,28,30,40
$$
이므로
$$
a_2+a_4=26+30=56
$$
이다.
