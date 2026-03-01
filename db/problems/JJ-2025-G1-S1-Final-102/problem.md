---
id: JJ-2025-G1-S1-Final-102
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 수동정제
- 단답형
- 출제번호-2
assets:
- assets/original/
- assets/original/서답2번.png
---
## Q
$A,B,C$를 포함한 6명을 일렬로 나열하고자 한다. $A,B$와 $A,C$는 서로 이웃하지 않게 나열하는 방법의 수를 구하시오.

## Choices


## Answer
288

## Solution
전체 경우의 수는
$$
6!=720
$$
이다.

$A$와 $B$가 이웃하는 경우: $AB$를 한 묶음으로 보면
$$
5!\times2=240
$$

$A$와 $C$가 이웃하는 경우도
$$
240
$$

두 경우가 모두 성립하려면 $A$가 가운데에 와서 $BAC$ 또는 $CAB$ 형태이므로
$$
4!\times2=48
$$

포함배제를 적용하면
$$
720-240-240+48=288
$$
이다.
