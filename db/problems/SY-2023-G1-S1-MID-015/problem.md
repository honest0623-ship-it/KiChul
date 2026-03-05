---
id: SY-2023-G1-S1-MID-015
school: SY
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: 15
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
source: user_upload_2026-03-04
tags:
  - 수동작성
  - 객관식
  - 출제번호-15
assets:
  - assets/original/
  - assets/original/2023_서영여고1_1학기_1차고사_문제지_정답 (다힝식~이차함수).pdf
---

## Q
두 이차함수
\[
y=x^2+mx+3,\quad y=-x^2+2x+n
\]
의 그래프가 만나지 않을 때,
자연수 \(m,\ n\)의 순서쌍 \((m,n)\)의 개수는?

## Choices
① 8
② 9
③ 10
④ 11
⑤ 12

## Answer
②

## Solution
두 그래프가 만나지 않으려면
\[
x^2+mx+3=-x^2+2x+n
\]
\[
2x^2+(m-2)x+(3-n)=0
\]
이 실근을 가지지 않아야 하므로 판별식이 음수:
\[
(m-2)^2-8(3-n)<0.
\]
즉
\[
8n<24-(m-2)^2.
\]

자연수 \(m\)에 대해 경우를 보면

\(m=1:\ 8n<23\Rightarrow n=1,2\) (2개)

\(m=2:\ 8n<24\Rightarrow n=1,2\) (2개)

\(m=3:\ 8n<23\Rightarrow n=1,2\) (2개)

\(m=4:\ 8n<20\Rightarrow n=1,2\) (2개)

\(m=5:\ 8n<15\Rightarrow n=1\) (1개)

\(m\ge 6\)에서는 가능한 \(n\)이 없다.

따라서 개수는
\[
2+2+2+2+1=9.
\]
정답은 ②이다.
