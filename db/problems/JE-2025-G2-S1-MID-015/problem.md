---
id: JE-2025-G2-S1-MID-015
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-15
assets:
- assets/original/
- assets/original/015_1-1. 지수와 로그.png
---
## Q
자연수 $a$, $k$에 대하여
$$
A=\{x\mid x=\log_{\sqrt{3}}a\text{인 자연수},\ 1\le a\le k\}
$$
의 원소의 개수가 $3$개일 때, 모든 자연수 $k$의 개수는?

## Choices
① $26$  
② $27$  
③ $45$  
④ $54$  
⑤ $55$

## Answer
④

## Solution
$x=\log_{\sqrt3}a$이면
$$
a=\left(\sqrt3\right)^x=3^{x/2}
$$
이다.

$a$가 자연수이려면 $x$는 짝수여야 하므로
$$
x=2t\ (t\in\mathbb{N}),\qquad a=3^t
$$
이다.

즉 $A$의 원소 개수는
$$
3^t\le k\ \text{를 만족하는 자연수 }t\text{의 개수}
$$
와 같다.

원소 개수가 $3$개이려면
$$
3^3\le k<3^4
$$
즉
$$
27\le k<81
$$
이어야 한다.

따라서 가능한 자연수 $k$의 개수는
$$
81-27=54
$$
이다.
