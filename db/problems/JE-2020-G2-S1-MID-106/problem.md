---
id: JE-2020-G2-S1-MID-106
school: JE
year: 2020
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 6
source_question_kind: subjective
source_question_label: 서답6
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-12
tags:
- 수동생성
- PDF
- 서술형
- 출제번호-서답6
- 과목-ALG
- 생성일-2026-03-12
assets:
- assets/scan.png
- assets/original/
- assets/original/JE.2020.G2.S1.MID.ALG.SUB06.question.png
- assets/original/JE.2020.G2.S1.MID.ALG.106.png
---

## Q
아래 그래프는 로그함수 \(y=\log_2 x\)의 그래프이다.
상수 \(c\)에 대하여 \(c^8\)은 몇 자리의 정수인지 구하시오.
(단, 점선은 \(x\)축, \(y\)축에 평행하고, \(\log 2=0.301\)로 계산한다.)

<img src="assets/scan.png" alt="JE-2020-G2-S1-MID-106 graph" style="width:75% !important; max-width:75% !important; height:auto;" />

## Choices


## Answer
$10$자리

## Solution
그래프의 점선 관계에서
\[
\log_2 a=1,\quad \log_2 b=a,\quad \log_2 c=b
\]
를 읽을 수 있다.

따라서
\[
a=2,\quad b=2^a=4,\quad c=2^b=16
\]
이다.

\[
c^8=16^8=(2^4)^8=2^{32}
\]
이므로
\[
\log(c^8)=\log(2^{32})=32\log2=32\times0.301=9.632
\]
이다.

따라서 \(c^8\)의 자릿수는
\[
\lfloor9.632\rfloor+1=10
\]
자리이다.
