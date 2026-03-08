---
id: BY-2023-G1-S1-MID-104
school: BY
year: 2023
grade: 1
semester: 1
exam: MID
subject: COM1
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-05
tags:
  - 수동작성
  - 서답형(서술형)
  - 출제번호-서답4번
  - 과목-COM1
assets:
  - assets/original/
  - assets/original/BY.2023.G1.S1.MID.COM1.pdf
---

## Q
이차방정식 $x^2-x+1=0$의 두 근을 $\alpha,\beta$라고 할 때,
$P(\alpha)=\beta,\ P(\beta)=\alpha,\ P(1)=2$를 만족하는 이차식 $P(x)$에 대하여 다음 물음에 답하시오.

(1) 이차식 $P(x)$를 구하시오.

(2) 방정식 $P(x)=0$의 두 근의 합과 곱을 각각 $m,n$이라고 할 때, $m+n$의 값을 구하시오.

## Choices


## Answer
3

## Solution
$$
P(x)=ux^2+vx+w
$$
라 두자.

$\alpha,\beta$는 $x^2-x+1=0$의 근이므로
$$
\alpha+\beta=1,\quad \alpha\beta=1
$$
이다.

$P(\alpha)=\beta,\ P(\beta)=\alpha$를 빼면
$$
u(\alpha^2-\beta^2)+v(\alpha-\beta)=\beta-\alpha
$$
이고, 따라서
$$
u+v=-1
$$
이다.

두 식을 더하면
$$
u(\alpha^2+\beta^2)+v(\alpha+\beta)+2w=1
$$
인데
$$
\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=-1
$$
이므로
$$
-u+v+2w=1
$$
이다.

또 $P(1)=2$에서
$$
u+v+w=2
$$
이다.

연립하면
$$
u=2,\quad v=-3,\quad w=3
$$
이므로
$$
P(x)=2x^2-3x+3
$$
이다.

따라서 $P(x)=0$의 두 근의 합과 곱은 각각
$$
m=\frac{3}{2},\quad n=\frac{3}{2}
$$
이고
$$
m+n=3
$$
이다.
