---
id: SY-2022-G1-S1-MID-102
school: SY
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 2
source_question_kind: subjective
source_question_label: 서2
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서2
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/scan.png
- assets/original/
- assets/original/SY.2022.G1.S1.MID.COM1.pdf
---

## Q
오른쪽 그림과 같이 한 변의 길이가 $8$인 정사각형 $ABCD$에 내접하는 정사각형 $EFGH$가 있다. 이때 점 $E, F, G, H$는 각각 변 $AB, BC, CD, DA$ 위에 있다. 정사각형 $EFGH$의 넓이의 최솟값을 구하시오.

<img src="assets/scan.png" alt="문항 원본" style="width:40% !important; max-width:40% !important; height:auto;" />

## Choices


## Answer
$32$

## Solution
정사각형 $EFGH$의 한 변의 길이를 $s$, 변 $AD$와 이루는 각을 $\theta$라 하자.
정사각형 $ABCD$의 한 변의 길이가 $8$이므로
\[
s\cos\theta+s\sin\theta=8
\]
이고 따라서
\[
s=\frac{8}{\sin\theta+\cos\theta}
\]
이다. 정사각형 $EFGH$의 넓이를 $S$라 하면
\[
S=s^2=\frac{64}{(\sin\theta+\cos\theta)^2}
\]
이다. 그런데
\[
(\sin\theta+\cos\theta)^2=1+\sin2\theta\le 2
\]
이므로
\[
S\ge \frac{64}{2}=32
\]
이다. 따라서 넓이의 최솟값은 $32$이다.
