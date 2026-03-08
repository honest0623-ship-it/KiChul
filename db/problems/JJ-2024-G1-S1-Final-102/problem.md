---
id: JJ-2024-G1-S1-Final-102
school: JJ
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM2
type: 서답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 4
level: 4
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-1. 평면좌표
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-1. 평면좌표
source: user_upload_2026-03-07
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서2
- 과목-COM2
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2024.G1.S1.Final.COM1.pdf
---

## Q
좌표평면 위의 점 $A(2,4)$를 꼭짓점으로 하는 정삼각형 $ABC$의 무게중심의 좌표가 $G(2,2)$이다.
변 $BC$ 위의 한 점 $P$에 대하여
\[
PA^2+PB^2
\]
의 최솟값을 구하시오.

## Choices

## Answer
\[
\frac{21}{2}
\]

## Solution
정삼각형에서 무게중심 $G$는 중선 $AM$ 위에 있고
\[
AG:GM=2:1
\]
이다.

여기서 $M$을 변 $BC$의 중점이라 하면
\[
A(2,4),\quad G(2,2)
\]
이므로
\[
M(2,1)
\]
이다.

정삼각형이므로 중선 $AM$은 높이이기도 하다.
따라서 변 $BC$는 직선
\[
y=1
\]
위에 있다.

또
\[
AM=3
\]
이고, 정삼각형의 높이는 한 변의 길이를 $s$라 할 때
\[
\frac{\sqrt{3}}{2}s
\]
이므로
\[
\frac{\sqrt{3}}{2}s=3
\]
\[
s=2\sqrt{3}
\]
이다.

따라서
\[
BM=\frac{s}{2}=\sqrt{3}
\]
이므로
\[
B(2-\sqrt{3},1),\qquad C(2+\sqrt{3},1)
\]
이다.

점 $P$를
\[
P(t,1)
\]
이라 두면
\[
PA^2=(t-2)^2+(1-4)^2=(t-2)^2+9
\]
이고
\[
PB^2=\{t-(2-\sqrt{3})\}^2
\]
이다.

따라서
\[
PA^2+PB^2=(t-2)^2+9+\{t-(2-\sqrt{3})\}^2
\]
\[
=2(t-2)^2+2\sqrt{3}(t-2)+12
\]
\[
=2\left(t-2+\frac{\sqrt{3}}{2}\right)^2+\frac{21}{2}
\]
이다.

그러므로 최솟값은
\[
\frac{21}{2}
\]
이다.
