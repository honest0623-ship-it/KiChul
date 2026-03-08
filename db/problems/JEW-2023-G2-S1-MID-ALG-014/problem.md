---
id: JEW-2023-G2-S1-MID-ALG-014
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 14
source_question_kind: objective
source_question_label: 14
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동작성
- 객관식
- 출제번호-14
- 과목-대수
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID-ALG-014_original.png
---

## Q
두 실수 $a,\ b$가
$$
ab=\log_5 \sqrt{7},\qquad b-a=\log_2 7
$$
을 만족시킬 때,
$$
2^{\frac1a}\div 2^{\frac1b}
$$
의 값은?

## Choices
① $\dfrac{25}{2}$
② $4$
③ $5$
④ $25$
⑤ $32$

## Answer
④

## Solution
$$
2^{\frac1a}\div 2^{\frac1b}=2^{\frac1a-\frac1b}
=2^{\frac{b-a}{ab}}
$$
이다.

따라서
$$
\frac{b-a}{ab}
=\frac{\log_2 7}{\log_5 \sqrt{7}}
=\frac{\log_2 7}{\frac12 \log_5 7}
=2\cdot \frac{\log_2 7}{\log_5 7}
$$
이다.

밑변환을 이용하면
$$
\frac{\log_2 7}{\log_5 7}=\log_2 5
$$
이므로
$$
\frac{b-a}{ab}=2\log_2 5=\log_2 25
$$
이다.

따라서
$$
2^{\frac1a}\div 2^{\frac1b}=2^{\log_2 25}=25
$$
이다.
