---
id: JEW-2023-G2-S1-MID-ALG-106
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서답형(서술형)
source_question_no: 6
source_question_kind: subjective
source_question_label: 서답6번
difficulty: 5
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답6번
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-106_original.png
---

## Q
함수
$$
f(x)=-x^2+ax+3
$$
일 때, 함수
$$
y=\left(\frac14\right)^{f(x)}
$$
는 $x=1$일 때 최솟값 $k$를 갖는다.
이때
$$
2^{|f(x)+n|}=\frac{1}{k}
$$
을 만족하는 실근이 $3$개가 되도록 하는 자연수 $n$의 값을 구하시오. (단, $a,\ k$는 실수)

## Choices


## Answer
$4$

## Solution
밑이 $\dfrac14$이므로
$$
y=\left(\frac14\right)^{f(x)}
$$
가 최솟값을 가질 때는 $f(x)$가 최댓값을 가진다.

$f(x)=-x^2+ax+3$의 꼭짓점의 $x$좌표는 $\dfrac{a}{2}$이므로
$$
\frac{a}{2}=1
$$
에서
$$
a=2
$$
이다.

따라서
$$
f(x)=-x^2+2x+3=-(x-1)^2+4
$$
이고,
$$
k=\left(\frac14\right)^4=\frac{1}{256}
$$
이다.

그러므로
$$
\frac{1}{k}=256=2^8
$$
이므로 주어진 방정식은
$$
|f(x)+n|=8
$$
과 같다.

즉
$$
f(x)+n=8
$$
또는
$$
f(x)+n=-8
$$
이다.

첫째 식은
$$
-x^2+2x+3+n=8
$$
이므로
$$
x^2-2x-(n-5)=0
$$
이다.
이 방정식이 중근을 가지려면
$$
(-2)^2-4\cdot 1\cdot (-(n-5))=0
$$
이고,
$$
4+4(n-5)=0
$$
에서
$$
n=4
$$
이다.

둘째 식은
$$
-x^2+2x+3+n=-8
$$
이므로
$$
x^2-2x-(n+11)=0
$$
이다. 이 방정식은 항상 서로 다른 두 실근을 가진다.

따라서 전체 실근의 개수가 $3$개가 되려면 첫째 식이 중근을 가져야 하므로
$$
n=4
$$
이다.
