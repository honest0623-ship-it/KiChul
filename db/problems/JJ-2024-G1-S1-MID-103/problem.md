---
id: JJ-2024-G1-S1-MID-103
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-04
tags:
- 자동입력
- 단답형
- 출제번호-3
- manual-fix
assets:
- assets/original/
- assets/original/서답3번_2-1. 복소수와 이차방정식.png
---

## Q
다음 조건을 만족하는 순서쌍 $(m,n)$의 개수를 구하시오.

(가) $m,n$은 20 이하의 자연수이다.
(나) $\{(-1)^m+i^m\}^n$의 값이 양수이다.

## Choices


## Answer
$120$

## Solution
$A_m=(-1)^m+i^m$로 두고 $m$을 4로 나눈 나머지를 본다.

$m\equiv0\pmod4$: $A_m=1+1=2$
$\Rightarrow A_m^n=2^n>0$ (모든 $n$ 가능)

$m\equiv2\pmod4$: $A_m=1-1=0$
$\Rightarrow A_m^n=0$ (양수 아님)

$m\equiv1\pmod4$: $A_m=-1+i=\sqrt2\,e^{i3\pi/4}$
$m\equiv3\pmod4$: $A_m=-1-i=\sqrt2\,e^{-i3\pi/4}$.

$A_m^n$이 양의 실수가 되려면 편각이 $2k\pi$여야 하므로
$\frac{3n\pi}{4}=2k\pi\Rightarrow 3n=8k$,
즉 $n$은 8의 배수.

$1\le n\le20$에서 가능한 $n$은 $8,16$ 두 개.

개수 계산:
- $m\equiv0\pmod4$: $m=4,8,12,16,20$ (5개), 각 $n$ 20개 $\Rightarrow 100$개
- $m\equiv1,3\pmod4$: 총 10개, 각 $n$ 2개 $\Rightarrow 20$개

총 $100+20=120$.
따라서 순서쌍의 개수는 $120$이다.
