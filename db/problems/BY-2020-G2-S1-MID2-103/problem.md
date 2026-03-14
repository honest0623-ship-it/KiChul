---
id: BY-2020-G2-S1-MID2-103
school: BY
year: 2020
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 서답형(서술형)
source_question_no: 3
source_question_kind: subjective
source_question_label: '서답3번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-2. 조합
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-2. 조합
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 서답형(서술형)
- 출제번호-서답3번
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q103.original.png
---

## Q
$(1+x)^4(1+x^2)^6$의 전개식에 대하여 다음 물음에 풀이과정을 쓰고 답을 구하여라.

(1) $(1+x)^4(1+x^2)^6$의 전개식의 일반항을 구하여라.

(2) 일반항을 이용하여 $(1+x)^4(1+x^2)^6$의 전개식에서 $x^4$의 계수를 구하여라.

## Choices

## Answer
52

## Solution
(1)
$$
(1+x)^4\ \text{의 }x^r\text{항}={}_{4}C_r x^r
\quad (r=0,1,2,3,4)
$$
$$
(1+x^2)^6\ \text{의 }x^{2s}\text{항}={}_{6}C_s x^{2s}
\quad (s=0,1,2,3,4,5,6)
$$
이므로 전체 일반항은
$$
{}_{4}C_r\,{}_{6}C_s\,x^{r+2s}
$$
이다.

(2) $x^4$항은 $r+2s=4$를 만족하는 경우에서 나온다.
가능한 $(r,s)$는
$$
(4,0),\ (2,1),\ (0,2)
$$
이다.

따라서 계수는
$$
{}_{4}C_{4}{}_{6}C_{0}+{}_{4}C_{2}{}_{6}C_{1}+{}_{4}C_{0}{}_{6}C_{2}
=1+6\times 6+15
=52
$$
이다.
