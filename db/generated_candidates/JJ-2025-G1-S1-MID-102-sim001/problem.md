---
id: JJ-2025-G1-S1-MID-102-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-2
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답2번.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: JJ-2025-G1-S1-MID-102
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:42:45'
---

## Q
이차함수 $f(x)$가 다음 조건을 만족시킬 때, $f(-3)$의 값을 구하시오.

(가) $x$에 대한 방정식 $f(x)=0$의 두 근은 $-2$와 $6$이다.
(나) $5\le x\le 8$에서 이차함수 $f(x)$의 최댓값은 $100$이다.

## Choices


## Answer
45

## Solution
조건 (가)에서 두 근이 $-2,6$이므로
\[
f(x)=a(x+2)(x-6)
\]
로 놓을 수 있다.

두 근의 평균으로 꼭짓점의 $x$좌표는
\[
\frac{-2+6}{2}=2
\]
이다. 구간 $[5,8]$에서는 꼭짓점의 $x$좌표 $2$보다 오른쪽에 있으므로 함수는 한쪽 방향으로만 변한다. 최댓값이 $100$이고 양수이므로 이 경우 $a>0$이고 최댓값은 오른쪽 끝점 $x=8$에서 얻어진다.

따라서
\[
f(8)=a(8+2)(8-6)=a\cdot10\cdot2=20a=100\Rightarrow a=5.
\]
그러면
\[
f(-3)=5(-3+2)(-3-6)=5(-1)(-9)=45.
\]
따라서 $f(-3)=45$.
