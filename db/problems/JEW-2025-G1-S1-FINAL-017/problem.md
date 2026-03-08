---
id: JEW-2025-G1-S1-FINAL-017
school: JEW
year: 2025
grade: 1
semester: 1
exam: FINAL
type: 객관식
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-17
assets:
- assets/scan.png
- assets/original/
- assets/original/017.png
subject: COM1
---

## Q
실수 \(k\)와 최고차항의 계수가 2인 이차함수 \(f(x)\)에 대하여 다음 조건을 만족시킨다.

(가) \(f(k)=2k\)
(나) 모든 실수 \(x\)에 대하여 \(f(x)\ge2k\)이다.

두 수 \(k,\ 2k\)를 근으로 갖는 이차방정식 \(g(x)=0\)에 대하여
부등식 \(f(x)>g(x)\)를 만족시키는 모든 \(x\)의 값의 범위가 \(x>8\)일 때,
실수 \(k\)의 값은?

## Choices
① 5
② 6
③ 7
④ 8
⑤ 9
## Answer
5

## Solution
From \((a)\) and \((b)\), the quadratic \(f(x)\) has vertex \((k,2k)\) and leading coefficient 2, so
\[
f(x)=2(x-k)^2+2k.
\]
For the solution set of \(f(x)>g(x)\) to be the single half-line \(x>8\), the quadratic terms of \(f-g\) must cancel. Hence \(g(x)\) also has leading coefficient 2, and since its roots are \(k\) and \(2k\),
\[
g(x)=2(x-k)(x-2k).
\]
Then
\[
f(x)-g(x)=2(x-k)^2+2k-2(x-k)(x-2k)=2k(x-k+1).
\]
So the inequality becomes
\[
2k(x-k+1)>0.
\]
Its solution set is \(x>k-1\) when \(k>0\). Since the given solution set is \(x>8\),
\[
k-1=8,
\]
so
\[
k=9.
\]
Therefore the correct choice is 5.
