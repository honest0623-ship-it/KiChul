---
id: JEW-2025-G1-S1-FINAL-103
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 서답형(단답형)
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-02-27
tags:
- 서답형(단답형)
- 출제번호-3
assets:
- assets/original/
- assets/original/서답3번.png
---
## Q
$x$에 대한 부등식 $|2x-1|\le n$을 만족시키는 정수 $x$의 개수가 $10$이 되도록 하는 모든 자연수 $n$의 값의 합을 구하시오.

## Choices


## Answer
19

## Solution
$$
|2x-1|\le n
$$
은
$$
-n\le2x-1\le n
$$
과 같다.

따라서
$$
\frac{1-n}{2}\le x\le\frac{1+n}{2}
$$
이다.

$n=2m$(짝수)일 때 정수해 개수는 $n$개,
$n=2m+1$(홀수)일 때 정수해 개수는 $n+1$개이다.

정수해 개수가 $10$이려면
- 짝수인 경우: $n=10$
- 홀수인 경우: $n+1=10\Rightarrow n=9$

따라서 가능한 $n$은 $9,10$이고 합은
$$
9+10=19
$$
이다.
