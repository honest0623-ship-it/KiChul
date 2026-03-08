---
id: BY-2024-G2-S1-MID-ALG-104
school: BY
year: 2024
grade: 2
semester: 1
exam: MID
subject: ALG
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: 서답4번
difficulty: 4
level: 4
unit: 대수(2022개정)>2. 삼각함수>2-2. 삼각함수의 그래프
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-2. 삼각함수의 그래프
source: user_upload_2026-03-06
tags:
- 수동작성
- PDF
- 서술형
- 출제번호-서답4번
- 과목-대수
assets:
- assets/original/
- assets/original/BY.2024.G2.S1.MID1.ALG.pdf
---

## Q
실수 $p$, $q$에 대하여 함수 $f(x)=\sin^2\left(x+\dfrac{\pi}{3}\right)-2\sin\left(x-\dfrac{\pi}{6}\right)+p$는 $x=q\pi$일 때 최댓값 $5$를 갖는다. $p+q$의 값을 구하는 풀이과정을 쓰고 답을 구하시오. (단, $0\le x<2\pi$)

## Choices


## Answer
$\dfrac{14}{3}$

## Solution
$t=x-\dfrac{\pi}{6}$이라 두면
$$
\sin^2\left(x+\frac{\pi}{3}\right)=\sin^2\left(t+\frac{\pi}{2}\right)=\cos^2 t
$$
이므로
$$
f(x)=\cos^2 t-2\sin t+p=1-\sin^2 t-2\sin t+p=-(\sin t+1)^2+p+2
$$
이다.
따라서 최댓값은 $p+2$이고, 이것이 $5$이므로 $p=3$이다.
최댓값은 $\sin t=-1$일 때 이루어지므로
$$
x-\frac{\pi}{6}=-\frac{\pi}{2}+2n\pi
$$
이다.
$0\le x<2\pi$에서 이를 만족하는 값은 $x=\dfrac{5\pi}{3}$이므로 $q=\dfrac53$이다.
$$
p+q=3+\frac53=\frac{14}{3}
$$
