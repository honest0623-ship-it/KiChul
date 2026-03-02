---
id: JJ-2025-G1-S1-Final-012
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: '2'
level: 2
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 수동정제
- 객관식
- 출제번호-12
assets:
- assets/original/
- assets/original/012.png
---
## Q
동근이와 재홍이를 포함한 남학생 5명과 주영이를 포함한 여학생 5명 중에서 남학생 2명과 여학생 3명을 뽑아 릴레이 선수로 출전시키고자 한다. 동근이와 주영이는 반드시 출전하고 재홍이는 발목부상으로 출전하지 않을 때, 릴레이 선수를 뽑아 달리는 순서를 정하는 경우의 수는?

## Choices
① 2160
② 2200
③ 2240
④ 2280
⑤ 2320

## Answer
①

## Solution
남학생은 동근이를 반드시 포함하고 재홍이는 제외하므로, 나머지 3명 중 1명을 고른다.
$$
{}_3\mathrm{C}_1=3
$$

여학생은 주영이를 반드시 포함하므로, 나머지 4명 중 2명을 고른다.
$$
{}_4\mathrm{C}_2=6
$$

따라서 선수 선발 경우의 수는
$$
3\times 6=18
$$
이고, 선발된 5명의 달리는 순서는
$$
5!=120
$$
가지이다.

전체 경우의 수는
$$
18\times 120=2160
$$
이다.
