---
id: JEW-2023-G2-S1-MID-ALG-015
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: 15
difficulty: 3
level: 3
unit: 대수(2022개정)>3. 수열>3-3. 수열의 합
unit_l1: 대수(2022개정)
unit_l2: 3. 수열
unit_l3: 3-3. 수열의 합
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-15
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-015_original.png
---

## Q
첫째항이 $10$인 등차수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 하면
$$
S_5=S_6
$$
이 성립한다. 부등식
$$
S_n>S_{n+1}
$$
을 만족시키는 $n$의 최솟값은?

## Choices
① $4$
② $5$
③ $6$
④ $7$
⑤ $8$

## Answer
③

## Solution
$$
S_6-S_5=a_6
$$
이므로
$$
a_6=0
$$
이다.

첫째항이 $10$인 등차수열이므로
$$
a_6=10+5d=0
$$
에서
$$
d=-2
$$
이다.

또
$$
S_{n+1}-S_n=a_{n+1}
$$
이므로 $S_n>S_{n+1}$이려면
$$
a_{n+1}<0
$$
이어야 한다.

$$
a_{n+1}=10+n(-2)=10-2n<0
$$
이므로
$$
n>5
$$
이다.

따라서 최솟값은
$$
6
$$
이다.
