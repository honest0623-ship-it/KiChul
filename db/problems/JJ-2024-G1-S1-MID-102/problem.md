---
id: JJ-2024-G1-S1-MID-102
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-3. 인수분해
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-3. 인수분해
source: user_upload_2026-03-04
tags:
- 자동입력
- 단답형
- 출제번호-2
- manual-fix
assets:
- assets/original/
- assets/original/서답2번_1-3. 인수분해.png
---

## Q
두 자연수 $a, b$에 대하여 다항식 $p(x)$가 다음 조건을 만족시킬 때, $p(5)$의 값을 구하시오.

(가) $p(x)=x^4-20x^2+b$
(나) 다항식 $p(x)$는 $x+a$를 인수로 갖는다.
(다) 다항식 $p(x)$는 계수와 상수항이 모두 정수인 서로 다른 네 개의 일차식의 곱으로 인수분해된다.

## Choices


## Answer
$189$

## Solution
(다)에 의해
$p(x)=(x-m)(x+m)(x-n)(x+n)$
$(m,n\in\mathbb{N},\;m\ne n)$로 둘 수 있다.

그러면
$p(x)=x^4-(m^2+n^2)x^2+m^2n^2$.

(가)와 비교하여
$m^2+n^2=20$, $b=m^2n^2$.

자연수 제곱의 합이 20이 되는 경우는
$4+16$뿐이므로 $(m,n)=(2,4)$ (순서 무관).

따라서
$b=2^2\cdot4^2=64$,
$p(5)=5^4-20\cdot5^2+64=625-500+64=189$.

따라서 $p(5)=189$이다.
