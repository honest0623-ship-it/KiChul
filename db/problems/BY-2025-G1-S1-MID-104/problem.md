---
id: BY-2025-G1-S1-MID-104
school: BY
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-02-27
tags:
- 서답형-서술형
- 출제번호-4
assets:
- assets/original/
- assets/original/서답4번.png
---
## Q
$$
f(x)=x^2-4mx+5m^2+6m+1
$$
의 최솟값을 $g(m)$이라 할 때, 다음 물음에 대하여 풀이과정을 쓰고 답을 구하시오.

(1) $g(m)$를 구하시오.

(2) $m$의 값의 범위가 $-5\le m\le 1$일 때, $g(m)$은 $m=a$에서 최댓값 $b$, $m=c$에서 최솟값 $d$를 갖는다. 이때 $abcd$의 값을 구하시오.

## Choices


## Answer
192

## Solution
완전제곱으로 정리하면
$$
f(x)=x^2-4mx+5m^2+6m+1
=(x-2m)^2+(m^2+6m+1).
$$
따라서 $x$에 대한 최솟값은
$$
g(m)=m^2+6m+1=(m+3)^2-8.
$$

이제 $-5\le m\le 1$에서 $g(m)$을 본다.

- 위로 열린 이차함수이므로 최솟값은 꼭짓점 $m=-3$에서
$$
d=g(-3)=-8,\quad c=-3.
$$
- 최댓값은 구간 끝점에서 비교:
$$
g(-5)=25-30+1=-4,\quad g(1)=1+6+1=8.
$$
따라서
$$
b=8,\quad a=1.
$$

그러므로
$$
abcd=1\cdot 8\cdot(-3)\cdot(-8)=192.
$$
