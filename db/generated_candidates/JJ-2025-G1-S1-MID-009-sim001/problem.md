---
id: JJ-2025-G1-S1-MID-009-sim001
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 9
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
source: web_upload_2026-02-28
tags:
- 자동입력
- 객관식
- 출제번호-9
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/009.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
derived_from: JJ-2025-G1-S1-MID-009
similarity_type: parameter_change
generation_batch_id: sim_20260309_163501
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T16:35:01'
---

## Q
0이 아닌 세 실수 $a, b, c$에 대하여 $\sqrt{a}\sqrt{b} = -\sqrt{ab}$, $\dfrac{\sqrt{c}}{\sqrt{a}} = -\sqrt{\dfrac{c}{a}}$일 때, 항상 서로 다른 두 실근을 갖는 이차방정식을 고르시오.

## Choices
① $x^2 - ax + c = 0$
② $x^2 + bx - 3a = 0$
③ $x^2 + 2ax + b = 0$
④ $ax^2 - cx + b = 0$
⑤ $bx^2 - 2ax - c = 0$

## Answer
③

## Solution
주어진 조건으로 $a,b,c$의 부호를 결정한다.

1) $\sqrt{a}\sqrt{b} = -\sqrt{ab}$ 은 문제의 조건과 해석에 따라 $a<0$, $b<0$ 일 때 성립한다(0이 아님). 따라서 $a<0$, $b<0$.

2) $\dfrac{\sqrt{c}}{\sqrt{a}} = -\sqrt{\dfrac{c}{a}}$ 은 $\sqrt{a}$가 음의 분모 역할을 하므로 $a<0$이어야 하고, $\sqrt{c}$가 실수로 존재하려면 $c>0$ 이어야 한다. 따라서 $c>0$, $a<0$.

종합: $a<0,\ b<0,\ c>0$.

각 이차방정식의 판별식 $D=B^2-4AC$ 를 계산하여 항상 $D>0$ 인지를 본다.

① $x^2 - ax + c=0:\ D=a^2-4c$. 여기서 $a^2>0,\ c>0$ 이므로 $a^2-4c$는 양수일 수도 있고 음수일 수도 있다. (예: $a=-1,c=1$이면 $1-4<0$)

② $x^2 + bx - 3a=0:\ D=b^2-4(1)(-3a)=b^2+12a$. $b^2>0,\ a<0$ 이므로 음수가 될 수 있다. (예: $b=-1,a=-1$이면 $1-12<0$)

③ $x^2 + 2ax + b=0:\ D=(2a)^2-4b=4a^2-4b=4(a^2-b)$. 여기서 $a^2>0$ 이고 $b<0$ 이므로 $-b>0$ 이며 따라서 $a^2-b=a^2+(-b)>0$ 이다. 따라서 $D>0$ 이고 항상 서로 다른 두 실근을 가진다.

④ $ax^2 - cx + b=0:\ D=(-c)^2-4ab=c^2-4ab$. $a<0,b<0$ 이므로 $ab>0$ 이고 $c^2-4ab$은 양수일 수도 음수일 수도 있다. (예: $a=-1,b=-1,c=1$이면 $1-4<0$)

⑤ $bx^2 - 2ax - c=0:\ D=(-2a)^2-4b(-c)=4a^2+4bc$. $bc<0$ 이므로 $4a^2+4bc$는 음수가 될 수 있다. (예: $a=-1,b=-1,c=1$이면 $4+4(-1)<0$)

따라서 항상 서로 다른 두 실근을 갖는 것은 ③번이다.
