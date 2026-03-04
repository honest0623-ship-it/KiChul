---
id: HN-2023-G1-S1-MID-102
school: HN
year: 2023
grade: 1
semester: 1
exam: MID
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: "서답2"
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
  - 출제번호-2
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답2번_2-1. 복소수와 이차방정식.png
---

## Q
실수 \(p\)에 대하여 \(x\)에 대한 이차방정식
\[
x^2-px+2p=0
\]
이 허근 \(\alpha\)를 가진다. \(\alpha^3\)이 실수일 때,
\[
\alpha^5-2\alpha^4+2\alpha^2-4\alpha
\]
의 값을 구하시오.

## Choices

## Answer
24

## Solution
\(\alpha\)가 허근이므로 \(\alpha=a+b\mathrm{i}\) \((b\ne 0)\)라 두면, 계수가 실수이므로 켤레복소수 \(\overline{\alpha}=a-b\mathrm{i}\)도 근이다.

비에타 정리에 의해
\[
\alpha+\overline{\alpha}=p,\quad
\alpha\overline{\alpha}=2p
\]
이므로
\[
2a=p,\quad a^2+b^2=2p=4a.
\]
따라서
\[
a^2+b^2=4a \quad \cdots (1)
\]
이다.

또한 \(\alpha^3\)이 실수이므로 \(\operatorname{Im}(\alpha^3)=0\)이다.
\[
(a+b\mathrm{i})^3
=(a^3-3ab^2)+(3a^2b-b^3)\mathrm{i}
\]
에서
\[
3a^2b-b^3=0
\]
이고 \(b\ne 0\)이므로
\[
b^2=3a^2 \quad \cdots (2)
\]
이다.

\((2)\)를 \((1)\)에 대입하면
\[
a^2+3a^2=4a \Rightarrow 4a^2=4a \Rightarrow a=1
\]
이고, 따라서
\[
b^2=3 \Rightarrow b=\pm\sqrt{3}.
\]
즉
\[
\alpha=1\pm\sqrt{3}\,\mathrm{i}.
\]

이때
\[
\alpha^3=\left(2\left(\cos\frac{\pi}{3}\pm \mathrm{i}\sin\frac{\pi}{3}\right)\right)^3=-8
\]
이고
\[
\alpha(\alpha-2)=(1\pm\sqrt{3}\,\mathrm{i})(-1\pm\sqrt{3}\,\mathrm{i})=-4.
\]

주어진 식을 인수분해하면
\[
\alpha^5-2\alpha^4+2\alpha^2-4\alpha
=\alpha(\alpha-2)(\alpha^3+2)
\]
이므로
\[
\alpha(\alpha-2)(\alpha^3+2)=(-4)(-8+2)=24.
\]
따라서 답은 \(24\)이다.

