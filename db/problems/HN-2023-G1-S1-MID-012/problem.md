---
id: HN-2023-G1-S1-MID-012
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: "12"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-12
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/012_2-1. 복소수와 이차방정식.png
---

## Q
복소수
\[
z=\frac{1-\mathrm{i}}{1+\mathrm{i}}
\]
에 대하여
\[
z^n+z^{2n}+z^{3n}=-1
\]
이 성립하도록 하는 \(100\) 이하의 자연수 \(n\)의 개수를 구하시오. \((\mathrm{i}=\sqrt{-1})\)

## Choices
① 25  
② 40  
③ 50  
④ 60  
⑤ 75

## Answer
⑤

## Solution
\[
z=\frac{1-\mathrm{i}}{1+\mathrm{i}}
=\frac{(1-\mathrm{i})^2}{(1+\mathrm{i})(1-\mathrm{i})}
=\frac{1-2\mathrm{i}-1}{2}
=-\mathrm{i}
\]
이므로
\[
(-\mathrm{i})^n+(-\mathrm{i})^{2n}+(-\mathrm{i})^{3n}=-1.
\]

\(w=(-\mathrm{i})^n\)이라 두면
\[
w+w^2+w^3=-1
\]
이고
\[
w^3+w^2+w+1=0
\]
이므로
\[
(w+1)(w^2+1)=0.
\]
따라서
\[
w\in\{-1,\mathrm{i},-\mathrm{i}\}.
\]

\((- \mathrm{i})^n\)의 주기는 \(4\)이고,
\[
n\equiv 0\pmod 4 \Rightarrow (-\mathrm{i})^n=1
\]
은 조건을 만족하지 않는다.

즉 \(1\)부터 \(100\)까지에서 \(4\)의 배수만 제외하면 되므로
\[
100-\frac{100}{4}=100-25=75.
\]
따라서 정답은 \(⑤\)이다.

