---
id: SY-2023-G1-S1-Final-102
school: SY
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM2
type: 단답형
source_question_no: 2
source_question_kind: subjective
source_question_label: 서답2
difficulty: 5
level: 5
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-1. 평면좌표
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-1. 평면좌표
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 단답형
- 출제번호-서답2
- 과목-COM2
- 생성일-2026-03-08
assets:
- assets/scan.png
- assets/original/SY-2023-G1-S1-Final-102_original.png
---

## Q
두 점 \(A(5,2)\), \(B(-1,3)\)과 \(x\)축 위를 움직이는 점 \(C(a,0)\), \(D(a+1,0)\)에 대하여 사각형 \(ABCD\)의 둘레의 길이의 최솟값은
\[
1+m\sqrt{2}+\sqrt{n}
\]
이다. 두 자연수 \(m,\ n\)에 대하여 \(m+n\)의 값을 구하시오.

(단, \(a\)는 실수이다.)

<img src="assets/scan.png" alt="문항 그림" style="width:60%; max-width:60%; height:auto; display:block; margin:12px auto;" />

## Choices


## Answer
\(m=5,\ n=37,\ m+n=42\)

## Solution
사각형의 둘레는
\[
\overline{AB}+\overline{BC}+\overline{CD}+\overline{DA}
\]
이다.

여기서
\[
\overline{AB}
=\sqrt{(5-(-1))^2+(2-3)^2}
=\sqrt{37}
\]
이고
\[
\overline{CD}=1
\]
이다.

따라서 \(\overline{BC}+\overline{DA}\)의 최솟값만 구하면 된다.

점 \(D(a+1,0)\) 대신 점 \(C(a,0)\)를 기준으로 보면
\[
\overline{DA}=\sqrt{(a-4)^2+2^2}
\]
이다.

점 \(A'(4,2)\)를 잡으면
\[
\overline{DA}=\overline{CA'}
\]
이다.

이제 \(B(-1,3)\)를 \(x\)축에 대하여 대칭이동한 점을 \(B'(-1,-3)\)라 하면
\[
\overline{BC}=\overline{B'C}
\]
이므로
\[
\overline{BC}+\overline{DA}
=\overline{B'C}+\overline{CA'}
\ge \overline{B'A'}
\]
이다.

따라서 최솟값은
\[
\overline{B'A'}
=\sqrt{(4-(-1))^2+(2-(-3))^2}
=\sqrt{25+25}
=5\sqrt{2}
\]
이다.

그러므로 사각형 \(ABCD\)의 둘레의 최솟값은
\[
\sqrt{37}+1+5\sqrt{2}
\]
이다.

따라서
\[
m=5,\quad n=37
\]
이므로
\[
m+n=42
\]
이다.
