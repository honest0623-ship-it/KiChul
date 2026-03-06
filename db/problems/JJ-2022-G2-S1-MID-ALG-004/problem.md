---
id: JJ-2022-G2-S1-MID-ALG-004
school: JJ
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: objective
source_question_no: 4
source_question_kind: objective
source_question_label: '4'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-4
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ-2022-G2-S1-MID-ALG-004_original.png
---

## Q
자연수 $n$에 대하여 $\log a=\log b+\dfrac{64}{2^n}$를 만족시키는 $100$이하의 두 자연수 $a$, $b$의 순서쌍 $(a,b)$의 개수를 $f(n)$이라 할 때, $f(4)+f(5)+f(6)$의 값은?

## Choices
① $9$
② $10$
③ $11$
④ $12$
⑤ $13$

## Answer
③

## Solution
\[
\log\frac{a}{b}=2^{6-n}
\]
이므로
\[
\frac{a}{b}=10^{2^{6-n}}
\]
이다.

$n=4$이면 $\dfrac{a}{b}=10^4$이므로 가능한 순서쌍이 없다.
따라서 $f(4)=0$이다.

$n=5$이면 $\dfrac{a}{b}=100$이므로 $(a,b)=(100,1)$ 하나뿐이어서 $f(5)=1$이다.

$n=6$이면 $\dfrac{a}{b}=10$이므로
\[
(a,b)=(10,1),(20,2),\ldots,(100,10)
\]
의 $10$개가 가능하다.

따라서
\[
f(4)+f(5)+f(6)=0+1+10=11
\]
이다.
