---
id: JE-2024-G1-S1-Final-102
school: JE
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM1
type: 서답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-3. 여러 가지 방정식
source: user_upload_2026-03-07
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서2
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JE.2024.G1.S1.Final.COM1.pdf
---
## Q
$x$에 대한 방정식
\[
\left|x^2-1\right|=-x+k
\]
가 서로 다른 네 실근을 가질 때, 실수 $k$의 값 또는 범위를 구하시오.

## Choices

## Answer
\[
1<k<\frac{5}{4}
\]

## Solution
\[
\left|x^2-1\right|
\]
를 구간에 따라 나누면
\[
\left|x^2-1\right|=
\begin{cases}
x^2-1 & (x\le -1 \text{ 또는 } x\ge 1) \\
1-x^2 & (-1<x<1)
\end{cases}
\]
이다.

먼저
\[
x^2-1=-x+k
\]
이면
\[
x^2+x-(k+1)=0
\]
이다.

이 방정식의 두 근은
\[
\frac{-1\pm\sqrt{4k+5}}{2}
\]
이므로, 바깥쪽 구간
\[
x\le -1,\quad x\ge 1
\]
에서 각각 한 근씩 가지려면
\[
k>1
\]
이어야 한다.

다음으로
\[
1-x^2=-x+k
\]
이면
\[
x^2-x+(k-1)=0
\]
이다.

이 방정식이 안쪽 구간
\[
-1<x<1
\]
에서 서로 다른 두 근을 가지려면 판별식이 양수여야 하므로
\[
1-4(k-1)>0
\]
\[
5-4k>0
\]
\[
k<\frac{5}{4}
\]
이다.

또 큰 근이 $1$보다 작아야 하므로
\[
\frac{1+\sqrt{5-4k}}{2}<1
\]
이고, 이것은
\[
k>1
\]
과 같다.

따라서 서로 다른 네 실근을 가지는 $k$의 범위는
\[
1<k<\frac{5}{4}
\]
이다.
