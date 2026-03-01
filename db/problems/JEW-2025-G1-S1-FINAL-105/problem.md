---
id: JEW-2025-G1-S1-FINAL-105
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 서답형(서술형)
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>4. 행렬>4-1. 행렬과 그 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 4. 행렬
unit_l3: 4-1. 행렬과 그 연산
source: user_upload_2026-02-27
tags:
- 서답형(서술형)
- 출제번호-5
assets:
- assets/original/
- assets/original/서답5번_수정.png
---
## Q
삼차방정식 $x^3-1=0$의 한 허근을 $\omega$라 할 때, 두 행렬의 곱 $\left(\matrix{\omega\quad 1\cr \omega^2\quad -1}\right)\left(\matrix{\omega+1\quad \omega\cr 0\quad \omega^2}\right)$의 모든 성분의 합을 $a\omega+b$라 하자. 이때 실수 $a,b$값을 각각 구하시오.

## Choices


## Answer
a = -2, b = -1

## Solution
행렬곱은 $\left(\matrix{\omega^2+\omega\quad 2\omega^2\cr 1+\omega^2\quad 1-\omega^2}\right)$ 이다.

모든 성분의 합은 $(\omega^2+\omega)+2\omega^2+(1+\omega^2)+(1-\omega^2)=\omega+3\omega^2+2$ 이다.

$\omega$는 $x^3-1=0$의 허근이므로 $\omega^2+\omega+1=0$, 즉 $\omega^2=-\omega-1$ 이다.

이를 대입하면 $\omega+3(-\omega-1)+2=-2\omega-1$ 이고, 따라서 $a=-2,\ b=-1$ 이다.
