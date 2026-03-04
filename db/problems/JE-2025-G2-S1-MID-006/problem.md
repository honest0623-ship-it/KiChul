---
id: JE-2025-G2-S1-MID-006
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 6
source_question_kind: objective
source_question_label: '6'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-6
assets:
- assets/original/
- assets/original/006_1-1. 지수와 로그.png
---
## Q
자연수 $n$에 대하여
$$
\sqrt[n+1]{64}
$$
이 어떤 자연수의 네제곱근이 되도록 하는 모든 $n$의 합은?

## Choices
① $32$  
② $41$  
③ $52$  
④ $61$  
⑤ $72$

## Answer
③

## Solution
어떤 자연수 $m$에 대하여
$$
\sqrt[n+1]{64}=\sqrt[4]{m}
$$
라 하자.

양변을 $4$제곱하면
$$
m=64^{\frac{4}{n+1}}
=\left(2^6\right)^{\frac{4}{n+1}}
=2^{\frac{24}{n+1}}
$$
이다.

$m$이 자연수이려면 $\dfrac{24}{n+1}$이 자연수여야 하므로
$$
n+1\mid 24
$$
이다.

$24$의 약수 중 $1$을 제외하면
$$
n+1=2,3,4,6,8,12,24
$$
이므로
$$
n=1,2,3,5,7,11,23
$$
이다.

따라서 모든 $n$의 합은
$$
1+2+3+5+7+11+23=52
$$
이다.
