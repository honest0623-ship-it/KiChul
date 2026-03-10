---
id: HN-2025-G1-S1-MID-011-sim001
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
subject: COM1
type: 객관식
source_question_no: 11
source_question_kind: objective
source_question_label: '11'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: manual_agent_2026-03-10
tags:
- 수동생성
- AI
- 객관식
- 출제번호-11
- 과목-COM1
derived_from: HN-2025-G1-S1-MID-011
similarity_type: parameter_change
generation_batch_id: sim_20260310_160500
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-10T16:05:00'
---

## Q
방정식 $(2-i)z + 2i\bar{z} - 5 - 2i = 0$을 만족시키는 복소수 $z$를 구하시오. (단, $\bar{z}$는 $z$의 켤레복소수이다.)

## Choices
① $4+i$
② $4-i$
③ $-4+i$
④ $1-4i$
⑤ $-1+4i$

## Answer
②

## Solution
복소수 $z$를 $z=x+yi$ ($x,y$는 실수)라 두면, $\bar{z}=x-yi$이다.

주어진 식에 대입하면
$$(2-i)(x+yi)+2i(x-yi)-5-2i=0$$

각 항을 정리하면
$$(2x+3y-5) + (x+2y-2)i = 0$$

따라서 연립방정식
$$\begin{cases}
2x+3y=5\\
x+2y=2
\end{cases}$$
를 얻는다.

둘째 식에서 $x=2-2y$이므로 첫째 식에 대입하면
$$2(2-2y)+3y=5 \Rightarrow 4-y=5 \Rightarrow y=-1$$

그러면
$$x+2(-1)=2 \Rightarrow x=4$$

따라서
$$z=x+yi=4-i$$
이므로 정답은 **②**이다.
