---
id: BY-2021-G2-S1-FINAL2-STAT-018
school: BY
year: 2021
grade: 2
semester: 1
exam: FINAL2
subject: STAT
type: 객관식
source_question_no: 18
source_question_kind: objective
source_question_label: '18'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>2. 확률>2-1. 확률의 뜻과 활용
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-1. 확률의 뜻과 활용
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 객관식
- 출제번호-18
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2021.G2.S1.FINAL2.STAT.q018.png
---

## Q
집합 $X=\{1,2,3,4,5,6,7\}$에서 $k(2\le k\le 6)$개의 원소를 선택할 때, 이 원소가 연속하는 자연수일 확률을 $P_{k}$라 한다. 다음 <보기>에서 옳은 것을 모두 고르면?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">ㄱ. $P_{2}=\dfrac{2}{7}$<br/>ㄴ. $P_{k}=P_{8-k}$<br/>ㄷ. $P_{k}$ 중에서 최소값은 $P_{6}$이다.</div>

## Choices
① ㄱ
② ㄷ
③ ㄱ, ㄴ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
①

## Solution
$k$개의 연속한 수를 고르는 경우의 수는 시작값을 정하면 되므로 $8-k$가지이다.
전체 경우의 수는 ${}_{7}C_{k}$이므로
$$
P_{k}=\dfrac{8-k}{{}_{7}C_{k}}
$$
이다.
ㄱ. $P_{2}=\dfrac{6}{{}_{7}C_{2}}=\dfrac{6}{21}=\dfrac{2}{7}$ (참)
ㄴ. 일반적으로 $\dfrac{8-k}{{}_{7}C_{k}}\ne\dfrac{k}{{}_{7}C_{8-k}}$ (거짓)
ㄷ. $P_{2}=\dfrac{2}{7},\ P_{3}=\dfrac{1}{7},\ P_{4}=\dfrac{4}{35},\ P_{5}=\dfrac{1}{7},\ P_{6}=\dfrac{2}{7}$이므로 최소는 $P_{4}$ (거짓)
따라서 옳은 것은 ㄱ만이다.
