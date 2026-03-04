---
id: HN-2023-G1-S1-MID-103
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: "서답3"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 단답형
  - 출제번호-3
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답3번_2-1. 복소수와 이차방정식.png
---

## Q
\(x\)에 대한 이차방정식
\[
x^2+kx+1=0
\]
의 두 근을 \(\alpha,\beta\)라 하자. 최고차항의 계수가 \(1\)인 이차식 \(f(x)\)에 대하여 다음 조건을 만족시키는 모든 실수 \(k\)의 값의 합을 구하시오.

가) \(f(\alpha)=\dfrac{1}{\beta},\quad f(\beta)=\dfrac{1}{\alpha}\)  
나) \(y=f(x)\)는 \(x\)축에 접한다.

## Choices

## Answer
-2

## Solution
\(\alpha,\beta\)는
\[
x^2+kx+1=0
\]
의 근이므로
\[
\alpha\beta=1.
\]
따라서
\[
\frac1\beta=\alpha,\quad \frac1\alpha=\beta
\]
이고 조건 가)는
\[
f(\alpha)=\alpha,\quad f(\beta)=\beta
\]
가 된다.

조건 나)에서 \(f(x)\)는 \(x\)축에 접하므로 어떤 실수 \(t\)에 대하여
\[
f(x)=(x-t)^2
\]
이다.

그러면
\[
(\alpha-t)^2=\alpha,\quad (\beta-t)^2=\beta
\]
이고, \(\alpha,\beta\)는 다음 이차방정식의 근이다.
\[
x^2-(2t+1)x+t^2=0.
\]

한편 \(\alpha,\beta\)는
\[
x^2+kx+1=0
\]
의 근이기도 하므로, 두 식은 최고차항 계수가 같은 이차식이어서 계수가 일치한다.
\[
k=-(2t+1),\quad t^2=1.
\]

\[
t=1 \Rightarrow k=-3,\qquad
t=-1 \Rightarrow k=1.
\]

따라서 모든 실수 \(k\)의 합은
\[
-3+1=-2
\]
이다.

