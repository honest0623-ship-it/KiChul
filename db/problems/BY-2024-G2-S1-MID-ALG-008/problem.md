---
id: BY-2024-G2-S1-MID-ALG-008
school: BY
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: '8'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-8
- 과목-대수
assets:
- assets/original/
- assets/original/BY.2024.G2.S1.MID1.ALG.pdf
---

## Q
함수 $f(x)=\log_2\left(1+\dfrac{1}{x+3}\right)$에서 $f(1)+f(2)+f(3)+\cdots+f(n)=5$를 만족시키는 자연수 $n$의 값은?

## Choices
① 28
② 60
③ 124
④ 252
⑤ 508

## Answer
③

## Solution
$f(k)=\log_2\dfrac{k+4}{k+3}$이므로
$$
\sum_{k=1}^{n} f(k)=\log_2\left(\frac54\cdot\frac65\cdot\frac76\cdots\frac{n+4}{n+3}\right)=\log_2\frac{n+4}{4}
$$
이다. 따라서
$$
\log_2\frac{n+4}{4}=5 \Rightarrow \frac{n+4}{4}=32 \Rightarrow n=124
$$
