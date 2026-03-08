---
id: JJ-2022-G1-S1-MID-014
school: JJ
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: objective
source_question_no: 14
source_question_kind: objective
source_question_label: '14'
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
- objective
- 출제번호-14
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/JJ.2022.G1.S1.MID.COM1.pdf
---
## Q
$\dfrac{\sqrt{x+4}}{\sqrt{x-1}}=-\sqrt{\dfrac{x+4}{x-1}}$를 만족하는 $x$의 범위에서 이차함수 $f(x)=2x^2+4x+1$의 최댓값과 최솟값의 합은?

## Choices
① $12$
② $14$
③ $16$
④ $18$
⑤ $20$

## Answer
③

## Solution
먼저 $x>1$이면
\[
\frac{\sqrt{x+4}}{\sqrt{x-1}}>0
\]
이고
\[
-\sqrt{\frac{x+4}{x-1}}<0
\]
이므로 주어진 식을 만족할 수 없다.

한편 $-4\le x<1$이면
\[
\sqrt{x-1}=i\sqrt{1-x}
\]
이고
\[
\sqrt{\frac{x+4}{x-1}}=i\sqrt{\frac{x+4}{1-x}}
\]
이므로
\[
\frac{\sqrt{x+4}}{\sqrt{x-1}}
=\frac{\sqrt{x+4}}{i\sqrt{1-x}}
=-i\sqrt{\frac{x+4}{1-x}}
\]
\[
-\sqrt{\frac{x+4}{x-1}}
=-i\sqrt{\frac{x+4}{1-x}}
\]
가 되어 등식이 성립한다. 따라서 해는
\[
-4\le x<1
\]
이다.

\[
f(x)=2x^2+4x+1=2(x+1)^2-1
\]
이므로 최솟값은 $x=-1$에서 $-1$이다. 또 위 구간에서 최댓값은 왼쪽 끝점 $x=-4$에서
\[
f(-4)=17
\]
이다. 따라서 최댓값과 최솟값의 합은
\[
17+(-1)=16
\]
이다.

따라서 정답은 ③이다.
