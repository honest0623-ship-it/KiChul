---
id: BY-2023-G1-S1-Final-104
school: BY
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 서답형(서술형)
source_question_no: 4
source_question_kind: subjective
source_question_label: '서답4번'
difficulty: 4
level: 4
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-2. 직선의 방정식
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-2. 직선의 방정식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 서답형(서술형)
- 출제번호-서답4번
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/original/
- assets/original/BY.2023.G1.S1.Final.COM1.pdf
---
## Q
좌표평면 위의 세 직선
$$
4x+y+6=0,\qquad x+y-3=0,\qquad ax+y+1=0
$$
이 삼각형을 이루지 않도록 하는 모든 실수 $a$의 값의 합을 구하는 풀이과정을 쓰고 답을 구하시오.

## Choices

## Answer
$\frac{22}{3}$

## Solution
세 직선이 삼각형을 이루지 않으려면
1. 서로 평행한 두 직선이 있거나
2. 세 직선이 한 점에서 만나야 한다.

먼저 각 직선의 기울기를 구하면
$$
4x+y+6=0\ \Rightarrow\ y=-4x-6
$$
$$
x+y-3=0\ \Rightarrow\ y=-x+3
$$
$$
ax+y+1=0\ \Rightarrow\ y=-ax-1
$$
이다.

따라서 세 번째 직선이 첫 번째 직선과 평행하려면
$$
a=4
$$
이고, 두 번째 직선과 평행하려면
$$
a=1
$$
이다.

다음으로 세 직선이 한 점에서 만나는 경우를 찾는다.

처음 두 직선의 교점을 구하면
$$
\begin{cases}
4x+y+6=0\\
x+y-3=0
\end{cases}
$$
에서 두 식을 빼면
$$
3x+9=0
$$
이므로
$$
x=-3
$$
이다.

이를 $x+y-3=0$에 대입하면
$$
-3+y-3=0
$$
이므로
$$
y=6
$$
이다.

즉, 교점은
$$
(-3,6)
$$
이다.

이 점이 세 번째 직선 위에도 있어야 하므로
$$
a(-3)+6+1=0
$$
$$
-3a+7=0
$$
$$
a=\frac{7}{3}
$$
이다.

따라서 구하는 모든 $a$의 값은
$$
4,\ 1,\ \frac{7}{3}
$$
이고, 그 합은
$$
4+1+\frac{7}{3}=\frac{22}{3}
$$
이다.
