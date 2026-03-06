---
id: HN-2022-G2-S1-MID-ALG-105
school: HN
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: subjective
source_question_no: 5
source_question_kind: subjective
source_question_label: 서답5번
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-2. 지수함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-2. 지수함수
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답5번
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/HN-2022-G2-S1-MID-ALG-105_original.png
---

## Q
그림과 같이 함수 $y=2^x$의 그래프 위의 점 $A(1,2)$에서 $x$축, $y$축에 내린 수선의 발을 각각 $B$, $C$라 하자. 점 $C$를 $y$축의 방향으로 $k$만큼 평행이동시킨 점을 $D$, 점 $D$를 지나고 $x$축과 평행한 직선이 함수 $y=2^x$의 그래프와 만나는 점을 $E$, 점 $E$에서 $x$축에 내린 수선의 발을 $F$라 하자. 사각형 $ACDE$, $ABFE$의 넓이의 합이 $22$일 때, 자연수 $k$의 값을 구하는 과정을 서술하시오.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">&lt;부분점수 기준&gt;<br />
점 $D$, $E$, $F$의 좌표를 구했을 때 [각 1점]<br />
사각형 $ACDE$, $ABFE$의 넓이를 표현했을 때 [3점]<br />
$k$의 값을 구했을 때 [1점]</div>

## Choices


## Answer
6

## Solution
\[
B(1,0),\quad C(0,2),\quad D(0,2+k)
\]
이다.

점 $E$는 $y=2^x$ 위에 있고 $y$좌표가 $2+k$이므로
\[
E\bigl(\log_2(2+k),\,2+k\bigr)
\]
이고,
\[
F\bigl(\log_2(2+k),\,0\bigr)
\]
이다.

사각형 $ACDE$의 넓이는
\[
\frac{k\{1+\log_2(2+k)\}}{2}
\]
이고,
사각형 $ABFE$의 넓이는
\[
\frac{(4+k)\{\log_2(2+k)-1\}}{2}
\]
이다.

두 넓이의 합이 $22$이므로 자연수 $k$를 대입해 보면 $k=6$일 때
\[
\log_2(2+k)=\log_2 8=3
\]
이고,
\[
\frac{6(1+3)}{2}+\frac{10(3-1)}{2}=12+10=22
\]
가 된다.

따라서
\[
k=6
\]
이다.
