---
id: JEW-2025-G2-S1-MID-105
school: JEW
year: 2025
grade: 2
semester: 1
exam: MID
type: 서술형
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5
difficulty: '4'
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-03
tags:
- 서답형-서술형
- 출제번호-5
assets:
- assets/original/
- assets/original/서답5번_1-1. 지수와 로그.png
---
## Q
어떤 미생물의 개체 수는 매시간 $r\%$씩 일정하게 증가하여 $n$시간 후의 개체 수는 처음의
$$
\left(1+\frac{r}{100}\right)^n
$$
배가 된다고 한다. 이 미생물의 개체 수가 매시간 $40\%$씩 일정하게 증가할 때, $19$시간 후의 개체 수는 처음의 약 몇 배가 되는지를 구하는 과정과 답을 쓰시오.

(단, $\log 1.4=0.1461$, $\log 5.97=0.7759$로 계산한다.)

## Choices

## Answer
약 $597$배

## Solution
매시간 $40\%$ 증가이므로 증가배수는 $1.4$이다.

따라서 $19$시간 후의 배수는
$$
1.4^{19}
$$
이다.

상용로그를 취하면
$$
\log(1.4^{19})=19\log 1.4=19\times 0.1461=2.7759
$$
이고
$$
2.7759=2+0.7759
$$
이므로
$$
1.4^{19}=10^{2.7759}=10^2\cdot 10^{0.7759}
$$
이다.

주어진 값 $\log 5.97=0.7759$에서
$$
10^{0.7759}=5.97
$$
이므로
$$
1.4^{19}=100\times 5.97=597
$$
이다.

따라서 처음의 약 $597$배가 된다.
