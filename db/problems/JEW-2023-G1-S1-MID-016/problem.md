---
id: JEW-2023-G1-S1-MID-016
school: JEW
year: 2023
grade: 1
semester: 1
exam: MID
type: "객관식"
source_question_no: 16
source_question_kind: objective
source_question_label: "16"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-1. 복소수와 이차방정식"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-16
assets:
  - assets/original/
  - assets/original/016_2-1. 복소수와 이차방정식.png
---

## Q
\[
\left(\frac{\sqrt{2}}{1+i}\right)^n+\left(\frac{-1+\sqrt{3}i}{2}\right)^n=2
\]
를 만족시키는 자연수 \(n\)의 최솟값은? (단, \(i=\sqrt{-1}\))

## Choices
① 6
② 12
③ 15
④ 18
⑤ 24

## Answer
⑤

## Solution
먼저
\[
\frac{\sqrt{2}}{1+i}
=\frac{\sqrt{2}(1-i)}{(1+i)(1-i)}
=\frac{1-i}{\sqrt{2}}
=\cos\left(-\frac{\pi}{4}\right)+i\sin\left(-\frac{\pi}{4}\right),
\]
\[
\frac{-1+\sqrt{3}i}{2}
=\cos\left(\frac{2\pi}{3}\right)+i\sin\left(\frac{2\pi}{3}\right).
\]

두 수는 모두 절댓값이 \(1\)인 복소수이다.
절댓값이 \(1\)인 복소수 두 개의 합이 \(2\)가 되려면 두 복소수가 모두 \(1\)이어야 한다.

따라서
\[
\left(\frac{\sqrt{2}}{1+i}\right)^n=1,\quad
\left(\frac{-1+\sqrt{3}i}{2}\right)^n=1.
\]

첫째 조건에서
\[
-\frac{n\pi}{4}=2m\pi
\]
이므로 \(n\)은 \(8\)의 배수이다.

둘째 조건에서
\[
\frac{2n\pi}{3}=2\ell\pi
\]
이므로 \(n\)은 \(3\)의 배수이다.

따라서 \(n\)의 최솟값은
\[
8과 3의 최소공배수인 24
\]
정답은 ⑤이다.
