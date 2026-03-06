---
id: HN-2022-G2-S1-MID-ALG-017
school: HN
year: 2022
grade: 2
semester: 1
exam: MID
subject: ALG
type: objective
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 3
level: 3
unit: 대수(2022개정)>2. 삼각함수>2-3. 삼각함수의 활용
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-3. 삼각함수의 활용
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-17
- 과목-대수
- 생성일-2026-03-07
assets:
- assets/scan.png
- assets/original/
- assets/original/HN-2022-G2-S1-MID-ALG-017_original.png
---

## Q
그림과 같이 선분 $AB$를 지름으로 하는 원 $O$ 위의 두 점 $C$, $D$에 대하여 $\overline{AB}=6$, $\overline{BC}=4$이다. $\angle ABC=\alpha$, $\angle BDC=\beta$라 할 때, $\cos(2\alpha+\beta)\tan(\alpha+2\beta)$의 값은?

<img src="assets/scan.png" alt="HN-2022-G2-S1-MID-ALG-017 geometry" style="width:60% !important; max-width:60% !important; height:auto;" />

## Choices
① $-\dfrac{4\sqrt{5}}{15}$
② $-\dfrac{2}{3}$
③ $\dfrac{2}{3}$
④ $\dfrac{5}{6}$
⑤ $\dfrac{4\sqrt{5}}{15}$

## Answer
④

## Solution
$AB$가 지름이므로 $\triangle ABC$는 $C$에서 직각이다.
따라서
\[
AC=\sqrt{AB^2-BC^2}=\sqrt{36-16}=2\sqrt{5}
\]
이다.

그러므로
\[
\cos\alpha=\frac{BC}{AB}=\frac{2}{3},\qquad
\sin\alpha=\frac{AC}{AB}=\frac{\sqrt{5}}{3}
\]
이다.

또 $\angle BAC$와 $\angle BDC$는 같은 호 $BC$를 보고 있으므로
\[
\beta=\frac{\pi}{2}-\alpha
\]
이다.

따라서
\[
\cos(2\alpha+\beta)=\cos\left(\alpha+\frac{\pi}{2}\right)=-\sin\alpha=-\frac{\sqrt{5}}{3}
\]
이고
\[
\tan(\alpha+2\beta)=\tan(\pi-\alpha)=-\tan\alpha=-\frac{\sqrt{5}}{2}
\]
이다.

그러므로
\[
\cos(2\alpha+\beta)\tan(\alpha+2\beta)=\frac{5}{6}
\]
이다.
