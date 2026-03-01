---
id: BY-2025-G1-S1-Final-102
school: BY
year: 2025
grade: 1
semester: 1
exam: Final
type: 서답형(단답형)
source_question_no: 102
source_question_kind: subjective
source_question_label: '서답2번'
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-03-01
tags:
- 서답형(단답형)
- 출제번호-서답2번
assets:
- assets/original/
- assets/original/서답2번.png
---
## Q
학생 5명에게 서로 다른 빵 3개와 서로 다른 과자 4개를 나누어 주려고 한다.
빵을 받지 않는 학생에게만 과자를 1개씩 나누어 줄 수 있으며 나누어 준 후 빵은 남지 않고, 과자는 남는다.
학생 5명에게 빵과 과자를 나누어 주는 방법의 수를 구하시오.
(단, 한 학생이 빵을 2개 이상 받을 수 있다.)
## Choices


## Answer
2160

## Solution
빵 3개를 분배하는 경우를 빵을 받지 않는 학생 수로 나눈다.

- 빵을 3명이 받는 경우(각 1개씩):
$$
\binom{5}{3}\cdot 3!=60
$$
이때 빵을 받지 않는 2명에게 서로 다른 과자 2개를 배정하는 방법은
$$
{}_4P_2=4\cdot3=12
$$
이므로 $60\cdot12=720$가지.

- 빵을 2명이 받는 경우(2개, 1개):
$$
5\cdot4\cdot\binom{3}{2}=60
$$
이때 빵을 받지 않는 3명에게 서로 다른 과자 3개를 배정하는 방법은
$$
{}_4P_3=4\cdot3\cdot2=24
$$
이므로 $60\cdot24=1440$가지.

- 빵을 1명이 모두 받는 경우는 빵을 받지 않는 학생이 4명이라 과자가 남지 않으므로 제외.

따라서 전체 방법 수는
$$
720+1440=2160.
$$