---
id: SY-2023-G1-S1-MID-014
school: SY
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: 14
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
  - 출제번호-14
assets:
  - assets/original/
  - assets/original/2023_서영여고1_1학기_1차고사_문제지_정답 (다힝식~이차함수).pdf
---

## Q
이차함수
\[
y=x^2-x+1
\]
의 그래프와 직선
\[
y=x+n
\]
의 그래프가 만나는 서로 다른 두 점의 \(x\)좌표를 각각 \(\alpha,\ \beta\)라 하자.
\[
|\alpha|+|\beta|
\]
의 값이 자연수가 되도록 하는 \(50\) 이하의 자연수 \(n\)의 합은?

## Choices
① 140
② 138
③ 136
④ 134
⑤ 132

## Answer
①

## Solution
교점의 \(x\)좌표는
\[
x^2-x+1=x+n
\]
\[
x^2-2x+(1-n)=0
\]
의 근이다.
따라서
\[
\alpha=1+\sqrt{n},\quad \beta=1-\sqrt{n}
\]
(\(n>0\)에서 서로 다른 두 점)이다.

\(n=1\)이면 \(\alpha=2,\ \beta=0\)이므로
\[
|\alpha|+|\beta|=2
\]
는 자연수이다.

\(n>1\)이면 \(\beta<0\)이므로
\[
|\alpha|+|\beta|=(1+\sqrt{n})+(\sqrt{n}-1)=2\sqrt{n}.
\]
이 값이 자연수가 되려면 \(\sqrt{n}\)이 정수여야 하므로
\(n\)은 완전제곱수이다.

\(50\) 이하의 완전제곱수:
\[
1,\ 4,\ 9,\ 16,\ 25,\ 36,\ 49.
\]
합은
\[
1+4+9+16+25+36+49=140.
\]
정답은 ①이다.
