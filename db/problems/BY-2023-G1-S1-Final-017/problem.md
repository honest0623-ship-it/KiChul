---
id: BY-2023-G1-S1-Final-017
school: BY
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 5
level: 5
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-1. 평면좌표
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-1. 평면좌표
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-17
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/original/
- assets/original/BY.2023.G1.S1.Final.COM1.pdf
---
## Q
세 점 $A(a,b)$, $B(-1,1)$, $C(2,-2)$에 대하여 다음 <조건>을 모두 만족하는 점 $A$의 개수는?

<div style="border:1px solid #000; padding:0.7em 0.9em; margin:0.6em 0; display:inline-block;">
(가) $a,b$는 $20$ 이하의 자연수이다.<br/>
(나) 선분 $AB$와 $y$축이 만나는 점은 선분 $AB$를 $m:n$으로 내분하는 점이고, 선분 $AC$와 $x$축이 만나는 점은 선분 $AC$를 $m:n$으로 내분하는 점이다. (단, $m,n$은 자연수)
</div>

## Choices
① 6개
② 7개
③ 8개
④ 9개
⑤ 10개

## Answer
⑤

## Solution
선분 $AB$와 $y$축이 만나는 점을 $D$, 선분 $AC$와 $x$축이 만나는 점을 $E$라 하자.

점 $D$가 선분 $AB$를 $m:n$으로 내분한다면
$$
D\left(\frac{n\cdot a+m\cdot(-1)}{m+n},\frac{n\cdot b+m\cdot 1}{m+n}\right)
$$
이다.

그런데 $D$는 $y$축 위의 점이므로 $x$좌표가 $0$이다.
따라서
$$
\frac{na-m}{m+n}=0
$$
이고,
$$
m=na
$$
이다.

점 $E$가 선분 $AC$를 같은 비 $m:n$으로 내분하므로
$$
E\left(\frac{n\cdot a+m\cdot 2}{m+n},\frac{n\cdot b+m\cdot(-2)}{m+n}\right)
$$
이다.

그런데 $E$는 $x$축 위의 점이므로 $y$좌표가 $0$이다.
따라서
$$
\frac{nb-2m}{m+n}=0
$$
이고,
$$
nb=2m
$$
이다.

앞에서 $m=na$이므로
$$
nb=2na
$$
이고,
$$
b=2a
$$
이다.

이제 $a,b$는 $20$ 이하의 자연수이므로
$$
2a\le 20
$$
에서
$$
a=1,2,3,\dots,10
$$
이다.

각 $a$에 대하여 $b=2a$가 하나씩 정해지므로 점 $A$의 개수는
$$
10
$$
개이다.
