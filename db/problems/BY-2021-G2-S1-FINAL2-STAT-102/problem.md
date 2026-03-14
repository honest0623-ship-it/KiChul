---
id: BY-2021-G2-S1-FINAL2-STAT-102
school: BY
year: 2021
grade: 2
semester: 1
exam: FINAL2
subject: STAT
type: 서답형(단답형)
source_question_no: 2
source_question_kind: subjective
source_question_label: '서답2번'
difficulty: 4
level: 4
unit: 확률과 통계(2022개정)>2. 확률>2-1. 확률의 뜻과 활용
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-1. 확률의 뜻과 활용
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서답형(단답형)
- 출제번호-서답2번
- 과목-확률과통계
assets:
- assets/original/
- assets/original/BY.2021.G2.S1.FINAL2.STAT.q102.png
---

## Q
두 직선 $y=x$와 $y=-x$ 위에 $x$좌표가 6 이하인 자연수인 점 3개를 선택하여 삼각형이 만들어질 때, 삼각형의 넓이가 6일 확률을 구하여라.

## Choices

## Answer
$\dfrac{2}{15}$

## Solution
점은 각 직선 위에 6개씩, 총 12개이다.
삼각형이 만들어지는 경우의 수는 같은 직선 위 3점을 제외하므로
$$
{}_{12}C_{3}-{}_{6}C_{3}-{}_{6}C_{3}=220-20-20=180
$$
이다.
한 직선에서 2점을 고르고 다른 직선에서 1점을 고르면 넓이는
$$
(\text{인덱스 차})\times(\text{다른 직선 점의 인덱스})
$$
가 된다.
넓이가 6이 되려면 가능한 차-인덱스 쌍은 $(1,6),(2,3),(3,2)$이고,
각각의 경우 수는 $5,4,3$가지이므로 한 방향에서 12가지,
두 방향 합쳐 24가지이다.
따라서 확률은
$$
\dfrac{24}{180}=\dfrac{2}{15}
$$
이다.
