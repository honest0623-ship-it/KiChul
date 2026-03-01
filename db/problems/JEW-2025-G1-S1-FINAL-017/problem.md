---
id: JEW-2025-G1-S1-FINAL-017
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-17
assets:
- assets/original/
- assets/original/017.png
---
## Q
실수 $k$와 최고차항의 계수가 2인 이차함수 $f(x)$에 대하여 다음 조건을 만족시킨다.

(가) $f(k)=2k$
(나) 모든 실수 $x$에 대하여 $f(x)\ge 2k$

두 수 $k,2k$를 근으로 갖는 이차방정식 $g(x)=0$에 대하여 부등식 $f(x)>g(x)$를 만족시키는 모든 $x$의 범위가 $x>8$일 때, 실수 $k$의 값은?

## Choices
① 5
② 6
③ 7
④ 8
⑤ 9

## Answer
⑤

## Solution
(가), (나)에서 $f(x)$는 꼭짓점이 $(k,2k)$이고 위로 열린 포물선이므로
$$
f(x)=2(x-k)^2+2k
$$
이다.

$g(x)=0$의 근이 $k,2k$이므로
$$
g(x)=m(x-k)(x-2k)\quad(m\ne0)
$$
로 둔다.

$h(x)=f(x)-g(x)$라 하면 해집합은 $h(x)>0$의 해집합이다.
문제에서 해집합이 한쪽 반직선 $x>8$이므로 $h(x)$는 1차식이어야 한다.
따라서 $x^2$항이 없어져야 하므로 $m=2$.

그러면
$$
h(x)=2k(x-k+1)
$$
이다.

$h(x)>0$의 해가 $x>8$이려면 $k>0$이고 경계값이 $x=k-1$이어야 하므로
$$
k-1=8
$$
이다.

따라서
$$
k=9
$$
이다.
