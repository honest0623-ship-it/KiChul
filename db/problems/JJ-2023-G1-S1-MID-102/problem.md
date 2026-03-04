---
id: JJ-2023-G1-S1-MID-102
school: JJ
year: 2023
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: "서답2"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>1. 다항식>1-1. 다항식의 연산"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-1. 다항식의 연산"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 단답형
  - 출제번호-2
assets:
  - assets/original/
  - assets/original/서답2번_1-1. 다항식의 연산.png
---

## Q
등식
$$
(1+x)^{19}=a_0+a_1x+a_2x^2+\cdots+a_{18}x^{18}+a_{19}x^{19}
$$
이 $x$에 대한 항등식일 때,
$$
a_1-a_3+a_5-a_7+\cdots+a_{17}-a_{19}
$$
의 값을 구하시오. (단, $a_0,a_1,a_2,\dots,a_{19}$는 상수)

## Choices

## Answer
512

## Solution
$f(x)=(1+x)^{19}$라 두고 $x=i$를 대입하면
$$
f(i)=a_0+a_1i+a_2i^2+\cdots+a_{19}i^{19}.
$$
이 식의 허수부분은
$$
a_1-a_3+a_5-a_7+\cdots+a_{17}-a_{19}
$$
와 같다.

한편
$$
f(i)=(1+i)^{19}.
$$
$1+i=\sqrt{2}\left(\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}\right)$이므로
$$
(1+i)^{19}
=2^{\frac{19}{2}}\left(\cos\frac{19\pi}{4}+i\sin\frac{19\pi}{4}\right)
$$
$$
=2^{\frac{19}{2}}\left(-\frac{\sqrt{2}}{2}+i\frac{\sqrt{2}}{2}\right)
=512(-1+i).
$$
따라서 허수부분은 $512$이다.

즉,
$$
a_1-a_3+a_5-a_7+\cdots+a_{17}-a_{19}=512.
$$

