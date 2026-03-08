---
id: JEW-2023-G2-S1-MID-ALG-103
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서답형(단답형)
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3번
difficulty: 4
level: 4
unit: 대수(2022개정)>3. 수열>3-2. 등비수열
unit_l1: 대수(2022개정)
unit_l2: 3. 수열
unit_l3: 3-2. 등비수열
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답3번
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-103_original.png
---

## Q
첫째항이 양수이고 공비가 음수인 등비수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 하자.
$$
a_4a_6=1,\qquad S_3=3a_3
$$
일 때, $a_3$의 값을 구하시오.

## Choices


## Answer
$4$

## Solution
첫째항을 $a$, 공비를 $r$이라 하면 $a>0,\ r<0$이고
$$
a_3=ar^2,\quad a_4=ar^3,\quad a_6=ar^5
$$
이다.

먼저
$$
a_4a_6=a^2r^8=1
$$
이다.

또
$$
S_3=a+ar+ar^2=a(1+r+r^2)
$$
이고
$$
S_3=3a_3=3ar^2
$$
이므로
$$
1+r+r^2=3r^2
$$
이다.

따라서
$$
2r^2-r-1=0
$$
이고,
$$
(2r+1)(r-1)=0
$$
이다.

공비가 음수이므로
$$
r=-\frac12
$$
이다.

이제
$$
a^2\left(-\frac12\right)^8=1
$$
에서
$$
a^2\cdot \frac{1}{256}=1
$$
이므로
$$
a=16
$$
이다.

따라서
$$
a_3=ar^2=16\cdot \frac14=4
$$
이다.
