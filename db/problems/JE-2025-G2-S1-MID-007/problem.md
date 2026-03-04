---
id: JE-2025-G2-S1-MID-007
school: JE
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: '7'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 객관식
- 출제번호-7
assets:
- assets/original/
- assets/original/007_1-1. 지수와 로그.png
---
## Q
$4\le n\le 12$인 자연수 $n$에 대하여 $n^2-15n+50$의 $n$제곱근 중 실수인 것의 개수를 $f(n)$이라 하자. 이때, $f(n)=1$을 만족시키는 모든 $n$의 값의 합은?

## Choices
① $32$  
② $42$  
③ $52$  
④ $62$  
⑤ $72$

## Answer
②

## Solution
$f(n)$은 방정식
$$
x^n=n^2-15n+50
$$
의 실근 개수와 같다.

오른쪽 값을
$$
n^2-15n+50=(n-5)(n-10)
$$
로 두고 $4\le n\le 12$에서 조사한다.

- $n$이 홀수이면 $x^n=c$는 항상 실근이 $1$개
- $n$이 짝수이면
  $c>0$일 때 $2$개, $c=0$일 때 $1$개, $c<0$일 때 $0$개

각 $n$에 대해 계산하면
$$
n=5,7,9,10,11
$$
에서만 $f(n)=1$이다.

따라서 합은
$$
5+7+9+10+11=42
$$
이다.
