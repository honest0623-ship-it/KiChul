---
id: JEW-2024-G1-S1-MID-016
school: JEW
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: "16"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-3. 여러 가지 방정식"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 객관식
  - 출제번호-16
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/016_2-3. 여러 가지 방정식.png
---

## Q
삼차방정식 $x^3-4x^2+6x-4=0$의 한 허근을 $w$라 할 때, $\{w(\overline{w}-1)\}^n=256$을 만족시키는 자연수 $n$의 값은? (단, $\overline{w}$는 $w$의 켤레복소수이다.)

## Choices
① 4
② 9
③ 16
④ 25
⑤ 36

## Answer
16

## Solution
\[
x^3-4x^2+6x-4=(x-2)(x^2-2x+2)
\]
이므로 허근은 $1+i,\ 1-i$이다.

$w=1+i$로 두면
\[
\overline{w}-1=(1-i)-1=-i
\]
\[
w(\overline{w}-1)=(1+i)(-i)=1-i
\]
($w=1-i$를 택해도 켤레가 되어 결론은 같다.)

따라서
\[
(1-i)^n=256
\]

$1-i=\sqrt{2}\left(\cos\left(-\frac{\pi}{4}\right)+i\sin\left(-\frac{\pi}{4}\right)\right)$이므로
\[
(1-i)^n=(\sqrt{2})^n
\left(\cos\left(-\frac{n\pi}{4}\right)+i\sin\left(-\frac{n\pi}{4}\right)\right)
\]

오른쪽이 실수 $256=2^8$이 되려면
\[
(\sqrt{2})^n=2^8
\]
이어야 하므로
\[
2^{n/2}=2^8,\quad n=16
\]

또
\[
\cos\left(-\frac{16\pi}{4}\right)+i\sin\left(-\frac{16\pi}{4}\right)
=\cos(-4\pi)+i\sin(-4\pi)=1
\]
이므로 실제로
\[
(1-i)^{16}=256
\]
이 성립한다.

따라서 정답은 ③, $n=16$이다.
