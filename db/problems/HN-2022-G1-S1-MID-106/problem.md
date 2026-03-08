---
id: HN-2022-G1-S1-MID-106
school: HN
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: subjective
source_question_no: 6
source_question_kind: subjective
source_question_label: '서답형6(서술형)'
difficulty: 5
level: 5
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-6
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/HN-2022-G1-S1-MID-106_original.png
---

## Q
실수 \(a\)에 대하여 두 함수
<div style="border:1px solid #000; padding:8px; margin:8px 0;">
\[
f_1(x)=(x-a)^2+(a-2)^2 \quad (x\ge a)
\]
\[
f_2(x)=(x-a)^2+(a+2)^2 \quad (x\le a)
\]
</div>
의 최솟값을 각각 \(s_1(a)\), \(s_2(a)\)라 하고 \(s_1(a)\)와 \(s_2(a)\) 중에서 최소인 값을 \(g(a)\)라 하자. \(y=g(a)\)의 그래프와 직선 \(y=n\) \((n\)은 정수\()\)의 교점의 개수를 \(h(n)\)이라 할 때, \(h(0)+h(2)+h(4)+h(6)\)의 값을 구하는 풀이 과정과 답을 쓰시오.

## Choices

## Answer
11

## Solution
각 함수의 최솟값은 모두 \(x=a\)에서 나온다. 따라서
\[
s_1(a)=(a-2)^2,
\quad s_2(a)=(a+2)^2
\]
이다.
그러므로
\[
g(a)=\min\{(a-2)^2,(a+2)^2\}
\]
이다.
\((a-2)^2\le (a+2)^2\)는 \(a\ge 0\)일 때 성립하므로
\[
g(a)=
\begin{cases}
(a+2)^2 & (a\le 0) \\
(a-2)^2 & (a\ge 0)
\end{cases}
\]
이다.
이제 정수 \(n\)에 대하여 교점 개수를 센다.
\[
h(0)=2 \quad (a=-2,2)
\]
\[
h(2)=4 \quad (a=-2\pm\sqrt{2},\ 2\pm\sqrt{2})
\]
\[
h(4)=3 \quad (a=-4,0,4)
\]
\[
h(6)=2 \quad (a=-2-\sqrt{6},\ 2+\sqrt{6})
\]
이다. 따라서
\[
h(0)+h(2)+h(4)+h(6)=2+4+3+2=11
\]
이다.
