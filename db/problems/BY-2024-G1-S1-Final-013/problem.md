---
id: BY-2024-G1-S1-Final-013
school: BY
year: 2024
grade: 1
semester: 1
exam: Final
subject: COM1
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-07
tags:
- 객관식
- 출제번호-13
assets:
- assets/original/BY-2024-G1-S1-Final-013_original.png
---

## Q
이차부등식
\[
ax^2+bx+c>0
\]
의 해가 $-2<x<3$일 때, 다음 연립부등식을 만족하는 정수 $x$의 값의 합은? (단, $a$, $b$, $c$는 상수이다.)

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
\[
\begin{cases}
ax^2-bx+c>0\\
cx^2-bx+a\ge 0
\end{cases}
\]
</div>

## Choices
① $-4$
② $-2$
③ 0
④ 2
⑤ 4

## Answer
②

## Solution
이차부등식
\[
ax^2+bx+c>0
\]
의 해가 $-2<x<3$이므로
\[
ax^2+bx+c=k(x+2)(x-3)
\]
로 놓을 수 있고, 해가 두 근 사이이므로
\[
k<0
\]
이다.

식을 전개하면
\[
k(x+2)(x-3)=k(x^2-x-6)
\]
이므로
\[
a=k,\quad b=-k,\quad c=-6k
\]
이다.

첫째 부등식은
\[
ax^2-bx+c>0
\]
\[
kx^2-(-k)x-6k>0
\]
\[
k(x^2+x-6)>0
\]
\[
k(x+3)(x-2)>0
\]
이다.

$k<0$이므로
\[
(x+3)(x-2)<0
\]
이고, 따라서
\[
-3<x<2
\]
이다.

둘째 부등식은
\[
cx^2-bx+a\ge 0
\]
\[
-6kx^2-(-k)x+k\ge 0
\]
\[
k(-6x^2+x+1)\ge 0
\]
이다.

$k<0$이므로
\[
-6x^2+x+1\le 0
\]
\[
6x^2-x-1\ge 0
\]
\[
(3x+1)(2x-1)\ge 0
\]
이다.

따라서
\[
x\le -\frac{1}{3}\quad \text{또는}\quad x\ge \frac{1}{2}
\]
이다.

이제 $-3<x<2$인 정수는
\[
-2,\ -1,\ 0,\ 1
\]
이고, 이 중 둘째 부등식도 만족하는 정수는
\[
-2,\ -1,\ 1
\]
이다.

따라서 그 합은
\[
-2+(-1)+1=-2
\]
이다.

정답은 $②$이다.

