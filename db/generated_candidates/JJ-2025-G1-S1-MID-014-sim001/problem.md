---
id: JJ-2025-G1-S1-MID-014-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: web_upload_2026-02-27
tags:
- 자동입력
- 객관식
- 출제번호-14
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/014.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-014
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:40:10'
---

## Q
이차함수 \(y=x^2-2kx+a\)의 그래프와 직선 \(y=bx-k^2+2k\)가 실수 \(k\)의 값에 관계없이 항상 한 점에서 만날 때, 실수 \(a,b\)에 대하여 \(a+b\)의 값은?

## Choices
① -3
② -2
③ -1
④ 0
⑤ 1

## Answer
③

## Solution
두 그래프의 교점을 위해 식을 같게 두면
\[x^2-2kx+a=bx-k^2+2k\]
이므로
\[x^2-(2k+b)x+(k^2-2k+a)=0\]
을 얻는다.
모든 실수 \(k\)에 대해 항상 한 점에서 만나려면 위 이차방정식이 항상 중근을 가져야 하므로 판별식이 0이어야 한다.
\[D=(2k+b)^2-4(k^2-2k+a)=0\]
전개하면
\[4(b+2)k+(b^2-4a)=0\]
이 식이 모든 \(k\)에서 성립하려면
\[b+2=0,\quad b^2-4a=0\]
이므로 \(b=-2\), \(a=1\). 따라서 \(a+b=-1\)이고, 정답은 ③이다.
