---
id: HN-2023-G1-S1-Final-104
school: HN
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM1
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서답4번
- 과목-COM1
- 생성일-2026-03-08
assets:
- assets/original/HN-2023-G1-S1-Final-104_original.png
---

## Q
모든 실수 $x$에 대하여 부등식 $(k+2)x^2-2(k+2)x+7>0$이 성립하도록 하는 모든 정수 $k$의 값의 합을 $M$이라 하고, $3\le x\le 5$에서 이차부등식 $x^2-4x-4b+3\le 0$이 항상 성립하도록 하는 상수 $b$의 최솟값을 $m$이라 할 때, $M+m$의 값을 구하고 풀이 과정을 쓰시오.

## Choices


## Answer
$9$

## Solution
먼저
$$
(k+2)x^2-2(k+2)x+7
$$
을 정리하면
$$
(k+2)(x-1)^2+5-k
$$
이다.

이 식이 모든 실수 $x$에 대하여 양수가 되려면
- $k+2\ge 0$이어야 하고
- 최솟값이 양수여야 한다.

$k=-2$이면 식의 값은 항상 $7$이므로 가능하다.

$k>-2$이면 최솟값은 $x=1$에서
$$
5-k
$$
이므로
$$
5-k>0 \Rightarrow k<5
$$
이다.

따라서 가능한 정수 $k$는
$$
-2,-1,0,1,2,3,4
$$
이고,
$$
M=-2-1+0+1+2+3+4=7
$$
이다.

다음으로
$$
f(x)=x^2-4x-4b+3
$$
라 하자.

$3\le x\le 5$에서
$$
f'(x)=2x-4>0
$$
이므로 $f(x)$는 증가한다.

따라서 구간에서의 최댓값은 $x=5$일 때이고, 항상
$$
f(x)\le 0
$$
이 되려면
$$
f(5)\le 0
$$
이면 충분하다.

즉
$$
25-20-4b+3\le 0
$$
$$
8-4b\le 0
$$
$$
b\ge 2
$$
이므로
$$
m=2
$$
이다.

따라서
$$
M+m=7+2=9
$$
이다.
