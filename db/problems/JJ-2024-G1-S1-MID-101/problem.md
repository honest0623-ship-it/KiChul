---
id: JJ-2024-G1-S1-MID-101
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 1
source_question_kind: subjective
source_question_label: 서답1
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-04
tags:
- 자동입력
- 서술형
- 출제번호-1
- manual-fix
assets:
- assets/original/
- assets/original/서답1번_2-1. 복소수와 이차방정식.png
---

## Q
실수를 계수로 가지는 두 다항식 $f(x), g(x)$가 다음 조건을 만족한다.

(가) $f(x)=x^2+px+q$
(나) $z=1+i$일 때, $f(z)=0$, $g(z)=z^4+z$

이때, $g(x)$를 $f(x)$로 나눈 나머지를 구하시오.

## Choices


## Answer
$x-4$

## Solution
$f(x)$의 계수가 실수이고 $f(1+i)=0$이므로 켤레근 $1-i$도 근이다.
따라서
$f(x)=(x-(1+i))(x-(1-i))=x^2-2x+2$.

$g(x)$를 $f(x)$로 나눈 나머지를 $r(x)=mx+n$이라 두면
$r(1+i)=g(1+i)$, $r(1-i)=g(1-i)$이다.

$g(1+i)=(1+i)^4+(1+i)$,
$(1+i)^2=2i$, $(1+i)^4=-4$이므로
$g(1+i)=-3+i$.

$r(1+i)=m(1+i)+n=-3+i$에서
허수부 비교로 $m=1$, 실수부 비교로 $1+n=-3\Rightarrow n=-4$.

따라서 나머지는
$r(x)=x-4$이다.
