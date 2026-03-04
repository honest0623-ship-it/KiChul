---
id: JJ-2024-G1-S1-MID-104
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-1. 다항식의 연산
source: user_upload_2026-03-04
tags:
- 자동입력
- 서술형
- 출제번호-4
- manual-fix
assets:
- assets/original/
- assets/original/서답4번_1-1. 다항식의 연산.png
---

## Q
0이 아닌 세 실수 $a,b,c$가 다음 조건을 만족한다.

(가) $a+b+c=2$
(나) $a^2+b^2+c^2=6$
(다) $\frac{1}{ab}+\frac{1}{bc}+\frac{1}{ca}=-1$

이때 $(a-3)(b-3)(c-3)$의 값을 구하시오.

## Choices


## Answer
$-8$

## Solution
$s_1=a+b+c$, $s_2=ab+bc+ca$, $s_3=abc$라 두면
$s_1=2$.

또한
$a^2+b^2+c^2=s_1^2-2s_2=6$
$4-2s_2=6\Rightarrow s_2=-1$.

(다)에서
$\frac{1}{ab}+\frac{1}{bc}+\frac{1}{ca}=\frac{a+b+c}{abc}=\frac{s_1}{s_3}=-1$
$\frac{2}{s_3}=-1\Rightarrow s_3=-2$.

구하는 값은
$(a-3)(b-3)(c-3)$
$=abc-3(ab+bc+ca)+9(a+b+c)-27$
$=s_3-3s_2+9s_1-27$
$=-2-3(-1)+18-27=-8$.

따라서 값은 $-8$이다.
