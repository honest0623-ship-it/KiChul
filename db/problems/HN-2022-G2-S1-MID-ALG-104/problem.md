---
id: HN-2022-G2-S1-MID-ALG-104
school: HN
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: subjective
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 4
level: 4
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- subjective
- 출제번호-서답4번
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/HN-2022-G2-S1-MID-ALG-104_original.png
---

## Q
지수가 정수일 때도 아래 주어진 지수법칙이 성립하는지 증명하는 과정을 서술하시오. (단, $a\ne 0$, $b\ne 0$이고 $m$, $n$이 음의 정수이다.)

\[
a^m\div a^n=a^{m-n},\qquad (ab)^n=a^n b^n
\]

<div style="border:1px solid #000; padding:8px; margin:8px 0;">&lt;부분점수 기준&gt;<br />
$a^m\div a^n=a^{m-n}$의 식을 증명했을 때 [3점]<br />
$(ab)^n=a^n b^n$의 식을 증명했을 때 [3점]</div>

## Choices


## Answer
성립한다.

## Solution
$m=-p$, $n=-q$라 하자. 여기서 $p$, $q$는 자연수이다.

먼저
\[
a^m\div a^n
=a^{-p}\div a^{-q}
=\frac{1}{a^p}\div \frac{1}{a^q}
=\frac{1}{a^p}\cdot a^q
=a^{q-p}
=a^{-p-(-q)}
=a^{m-n}
\]
이다.

또
\[
(ab)^n=(ab)^{-q}=\frac{1}{(ab)^q}
=\frac{1}{a^q b^q}
=a^{-q}b^{-q}
=a^n b^n
\]
이다.

따라서 음의 정수 지수에서도 주어진 지수법칙은 성립한다.
