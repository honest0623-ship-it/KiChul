---
id: BY-2024-G2-S1-MID-ALG-018
school: BY
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: 3
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-3. 로그함수
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-3. 로그함수
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-18
- 과목-대수
assets:
- assets/scan.png
- assets/original/
- assets/original/BY.2024.G2.S1.MID1.ALG.pdf
---

## Q
그림과 같이 두 함수 $y=\log_{\frac12}x$, $y=\left(\dfrac12\right)^x$의 그래프의 교점을 $A$라 하고, 이 두 함수의 그래프와 함수 $y=\log_2(x-1)$의 그래프의 교점을 각각 $B$, $C$라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?

<img src="assets/scan.png" alt="세 함수의 그래프" style="width:60% !important; max-width:60% !important; height:auto;" />

<div style="border:1px solid #000; padding:8px; margin:8px 0;">ㄱ. 원점 $O$에 대하여 $\overline{OA}>\dfrac{\sqrt{2}}{2}$이다.<br/>ㄴ. 점 $B$의 $x$좌표를 $b$라 하면 $\dfrac32<b<2$이다.<br/>ㄷ. 점 $C$와 직선 $y=x$ 사이의 거리는 $\sqrt{2}$보다 크다.</div>

## Choices
① ㄱ
② ㄱ, ㄴ
③ ㄱ, ㄷ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
②

## Solution
점 $B$는 $\log_{\frac12}x=\log_2(x-1)$에서 정해지므로
$$
-\log_2 x=\log_2(x-1)\Rightarrow \log_2\frac{1}{x}=\log_2(x-1)\Rightarrow x^2-x-1=0
$$
이다. 따라서
$$
b=\frac{1+\sqrt5}{2}
$$
이므로 $\dfrac32<b<2$이다.

점 $A$는 $y=\log_{\frac12}x$와 $y=\left(\dfrac12\right)^x$의 교점이므로 $x=y$인 제1사분면의 점이며, 수치적으로 $A\approx(0.641,0.641)$이다. 따라서
$$
\overline{OA}\approx \sqrt{2}\times 0.641 > \frac{\sqrt2}{2}
$$
이어서 ㄱ은 참이다.

또 점 $C$는 대략 $C\approx(2.167,0.223)$이므로 직선 $y=x$와의 거리는
$$
\frac{|2.167-0.223|}{\sqrt2}<\sqrt2
$$
가 되어 ㄷ은 거짓이다. 따라서 옳은 것은 ㄱ, ㄴ이다.
