---
id: JE-2020-G2-S1-MID-006
school: JE
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 6
source_question_kind: objective
source_question_label: '6'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-12
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-6
- 과목-ALG
- 생성일-2026-03-12
assets:
- assets/original/
- assets/original/JE.2020.G2.S1.MID.ALG.006.question.png
---

## Q
다음은 \(1\)이 아닌 세 양수 \(a,b,c\)에 대하여
\[
a^{\log_b c}=(\text{다})
\]
가 성립함을 보이는 과정이다. 물음에 답하여라.

<div style="border:1px solid #000; padding:10px; margin:8px 0; font-family: inherit; line-height:1.8;">
\(a^{\log_b c}=x\)로 놓으면 로그의 정의에 따라
\[
\log_a x=\log_b c
\]

양변을 각각 \(c\)를 밑으로 하는 로그로 나타내면
\[
\frac{\log_c x}{\log_c a}=(\text{가})
\]
즉,
\[
\log_c x=(\text{나})
\]이므로 로그의 정의에 따라
\[
x=(\text{다})
\]
\[
\therefore\ a^{\log_b c}=(\text{다})
\]
</div>

빈칸에 들어갈 식 \((\text{가})\)와 \((\text{나})\)에 대하여
\[
f(a,b,c)=(\text{가})+(\text{나})
\]라 할 때, \(f(2,4,8)\)의 값을 구하여라.

## Choices
① $\dfrac56$
② $\dfrac76$
③ $\dfrac32$
④ $\dfrac{11}{6}$
⑤ $2$

## Answer
⑤

## Solution
변환 공식으로
\[
\log_a x=\log_b c
\Rightarrow
\frac{\log_c x}{\log_c a}=\frac{\log_c c}{\log_c b}
\]
이므로
\[
(\text{가})=\frac{1}{\log_c b},\quad
(\text{나})=\frac{\log_c a}{\log_c b}=\log_b a
\]
이다.

따라서
\[
f(2,4,8)=\frac{1}{\log_8 4}+\log_4 2
=\frac{1}{2/3}+\frac12
=\frac32+\frac12=2
\]
이다.
