---
id: BY-2020-G2-S1-MID2-012
school: BY
year: 2020
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 12
source_question_kind: objective
source_question_label: '12'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>1. 경우의 수>1-1. 순열
unit_l1: 확률과 통계(2022개정)
unit_l2: 1. 경우의 수
unit_l3: 1-1. 순열
source: user_upload_2026-03-13
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-12
- 과목-STAT
- 생성일-2026-03-13
assets:
- assets/original/
- assets/original/BY.2020.G2.S1.MID2.STAT.Q012.original.png
---

## Q
'mathematics'에 있는 11개의 문자를 일렬로 나열할 때, $e,i,c$는 $e,i,c$의 순서대로, $h,s$는 $s,h$의 순서로 왼쪽에서 오른쪽으로 배열되는 경우의 수는?

## Choices
① $\dfrac{11!}{3!\times 2!\times 2!\times 2!\times 2!}$
② $\dfrac{11!}{3!\times 2!\times 2!\times 2!}$
③ $\dfrac{11!}{2!\times 2!\times 2!\times 2!}$
④ $\dfrac{11!}{3!\times 2!\times 2!}$
⑤ $\dfrac{11!}{2!\times 2!\times 2!}$

## Answer
①

## Solution
'mathematics'의 전체 서로 다른 배열 수는
$$
\frac{11!}{2!\times 2!\times 2!}
$$
이다.
(중복 문자: $a,m,t$ 각각 2개)

$e,i,c$의 상대적 순서는 3!가지가 같게 나타나므로
조건 $e\to i\to c$는 그중 1가지이다.
즉 $\dfrac{1}{3!}$배.

또 $h,s$의 상대적 순서는 2가지가 같게 나타나므로
조건 $s\to h$는 그중 1가지이다.
즉 $\dfrac{1}{2}$배.

따라서 경우의 수는
$$
\frac{11!}{2!\times 2!\times 2!}\times\frac{1}{3!}\times\frac{1}{2}
=\frac{11!}{3!\times 2!\times 2!\times 2!\times 2!}
$$
이다.
