---
id: HN-2021-G1-S1-Final-013
school: HN
year: 2021
grade: 1
semester: 1
exam: FINAL
subject: COM1
type: 객관식
source_question_no: 13
source_question_kind: objective
source_question_label: '13'
difficulty: 3
level: 3
unit: 공통수학2(2022개정)>1. 도형의 방정식>1-1. 평면좌표
unit_l1: 공통수학2(2022개정)
unit_l2: 1. 도형의 방정식
unit_l3: 1-1. 평면좌표
source: user_upload_2026-03-10
tags:
- 객관식
- 출제번호-13
- 과목-COM1
assets:
- assets/original/
- assets/original/HN.2021.G1.S1.Final.COM1.pdf
---

## Q
세 점 \(A(-2,3)\), \(B(4,5)\), \(C(0,7)\)을 꼭짓점으로 하는 삼각형 \(ABC\)의 외접원의 반지름의 길이를 구하면?

## Choices
① \(2\sqrt{2}\)
② \(3\)
③ \(\sqrt{10}\)
④ \(\sqrt{11}\)
⑤ \(2\sqrt{3}\)

## Answer
③

## Solution
삼각형 \(ABC\)의 외심은 두 변의 수직이등분선의 교점이다.

\(A(-2,3),\ B(4,5)\)에서
중점은 \((1,4)\), \(\overline{AB}\)의 기울기는
\[
\frac{5-3}{4-(-2)}=\frac{2}{6}=\frac13
\]
이므로, 수직이등분선의 기울기는 \(-3\)이다.
따라서 \(\overline{AB}\)의 수직이등분선은
\[
y-4=-3(x-1)\quad\Rightarrow\quad y=-3x+7
\]

\(A(-2,3),\ C(0,7)\)에서
중점은 \((-1,5)\), \(\overline{AC}\)의 기울기는
\[
\frac{7-3}{0-(-2)}=\frac{4}{2}=2
\]
이므로, 수직이등분선의 기울기는 \(-\frac12\)이다.
따라서 \(\overline{AC}\)의 수직이등분선은
\[
y-5=-\frac12(x+1)\quad\Rightarrow\quad y=-\frac12x+\frac92
\]

두 직선
\[
y=-3x+7,\qquad y=-\frac12x+\frac92
\]
의 교점을 구하면 \(x=1,\ y=4\)이므로 외심은 \(O(1,4)\)이다.

외접원의 반지름 \(R\)은 \(OA\)의 길이와 같으므로, 두 점 사이의 거리공식으로
\[
R=OA=\sqrt{(1-(-2))^2+(4-3)^2}
=\sqrt{3^2+1^2}
=\sqrt{10}
\]

따라서 외접원의 반지름은 \(\sqrt{10}\)이고, 정답은 \(③\)이다.

<!-- classifier_reason: rule-score:8,hits:2 -->
