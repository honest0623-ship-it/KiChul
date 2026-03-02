---
id: HN-2025-G2-S1-MID-011
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 객관식
source_question_no: 11
source_question_kind: objective
source_question_label: '11'
difficulty: '3'
level: 3
unit: 대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그
unit_l1: 대수(2022개정)
unit_l2: 1. 지수함수와 로그함수
unit_l3: 1-1. 지수와 로그
source: user_upload_2026-03-01
tags:
- 객관식
- 출제번호-11
assets:
- assets/original/011_1-1. 지수와 로그.png
---
## Q
어떤 물고기는 바다 수면에 비치는 햇빛의 양이 $27\%$ 이상 도달하는 깊이까지 살 수 있다고 한다. 어떤 지역에서 햇빛이 수면으로부터 $30\mathrm{m}$씩 내려갈 때마다 햇빛의 양이 $37\%$씩 감소된다고 할 때, 이 물고기가 살 수 있는 깊이는 최대 몇 $\mathrm{m}$인가?
(단, $\log 6.3 = 0.8$, $\log 2.7 = 0.4$로 계산한다.)

## Choices
① $60$
② $80$
③ $90$
④ $99$
⑤ $120$

## Answer
③

## Solution
수면에 비치는 햇빛의 양을 $I_0$라 하자.
수면으로부터 깊이가 $30\mathrm{m}$씩 내려갈 때마다 햇빛의 양이 $37\%$씩 감소하므로, 깊이가 $x\mathrm{m}$인 곳의 햇빛의 양은 $I_0 \times (1 - 0.37)^{\frac{x}{30}} = I_0 \times (0.63)^{\frac{x}{30}}$이다.
물고기가 살 수 있는 깊이는 햇빛의 양이 $27\%$ 이상 도달하는 곳이므로
$$ I_0 \times (0.63)^{\frac{x}{30}} \ge 0.27 \times I_0 $$
$$ (0.63)^{\frac{x}{30}} \ge 0.27 $$
양변에 상용로그를 취하면
$$ \log (0.63)^{\frac{x}{30}} \ge \log 0.27 $$
$$ \frac{x}{30} \log 0.63 \ge \log 0.27 $$
이때 $\log 0.63 = \log(6.3 \times 10^{-1}) = \log 6.3 - 1 = 0.8 - 1 = -0.2$,
$\log 0.27 = \log(2.7 \times 10^{-1}) = \log 2.7 - 1 = 0.4 - 1 = -0.6$ 이므로
$$ \frac{x}{30} \times (-0.2) \ge -0.6 $$
양변을 $-0.2$로 나누면
$$ \frac{x}{30} \le 3 $$
$$ x \le 90 $$
따라서 이 물고기가 살 수 있는 깊이는 최대 $90\mathrm{m}$이다.
