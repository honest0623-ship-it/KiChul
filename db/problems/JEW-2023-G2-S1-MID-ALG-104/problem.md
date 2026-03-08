---
id: JEW-2023-G2-S1-MID-ALG-104
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서답형(단답형)
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 5
level: 5
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(단답형)
- 출제번호-서답4번
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-104_original.png
---

## Q
양의 실수 전체 집합에서 정의된 함수 $f(x)$가 다음을 만족시킨다.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
(가)
$$
f(x)=
\begin{cases}
3^x-1 & (0\le x\le 1)\\
3-3^{x-1} & (1< x\le 2)
\end{cases}
$$
(나) 자연수 $n$에 대하여
$$
3^n f(x)=f(x-2n)\qquad (2n<x\le 2n+2)
$$
</div>

함수 $y=f(x)\ (2n<x\le 2n+2)$의 그래프와 $x$축으로 둘러싸인 부분의 넓이를 $a_n$이라 하자.
수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 할 때, $S_3$의 값을 구하시오.

## Choices


## Answer
$\dfrac{26}{27}$

## Solution
먼저 $0\le x\le 2$에서 그래프와 $x$축으로 둘러싸인 넓이를 $A$라 하자.

$0\le x\le 1$에서
$$
f(x)=3^x-1
$$
이고, $1< x\le 2$에서 $t=x-1$로 놓으면 $0<t\le 1$이므로
$$
f(x)=3-3^{x-1}=3-3^t
$$
이다.

이때
$$
(3^t-1)+(3-3^t)=2
$$
이므로 구간 $0\le x\le 1$의 그래프와 구간 $1< x\le 2$의 그래프는 직선 $y=1$에 대하여 서로 대칭이다.
따라서 두 부분의 넓이의 합은 가로의 길이가 $1$, 세로의 길이가 $2$인 직사각형의 넓이와 같으므로
$$
A=2
$$
이다.

또
$$
3^n f(x)=f(x-2n)\qquad (2n<x\le 2n+2)
$$
이므로
$$
f(x)=\frac{1}{3^n}f(x-2n)
$$
이다.
즉, $0\le x\le 2$에서의 그래프를 오른쪽으로 $2n$만큼 옮기고 높이를 $\dfrac{1}{3^n}$배 한 것이 구간 $2n<x\le 2n+2$에서의 그래프이다.
따라서 넓이도 $\dfrac{1}{3^n}$배가 되어
$$
a_n=\frac{A}{3^n}=\frac{2}{3^n}
$$
이다.

그러므로
$$
S_3=a_1+a_2+a_3
=\frac{2}{3}+\frac{2}{9}+\frac{2}{27}
=\frac{26}{27}
$$
이다.
