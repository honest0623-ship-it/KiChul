---
id: HN-2025-G2-S1-MID-103
school: HN
year: 2025
grade: 2
semester: 1
exam: MID
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: 4
level: 4
unit: 대수(2022개정)>2. 삼각함수>2-3. 삼각함수의 활용
unit_l1: 대수(2022개정)
unit_l2: 2. 삼각함수
unit_l3: 2-3. 삼각함수의 활용
source: user_upload_2026-03-06
tags:
- 단답형
- 출제번호-서답3
assets:
- assets/original/HN-2025-G2-S1-MID-103_original.png
subject: ALG
---

## Q
$-\pi\le\theta\le\frac\pi4$일 때
$$
(x-\cos\theta)^2+(y-\sin\theta)^2=\frac14
$$
을 만족하는 점 $(x,y)$에 대하여 $y-x$의 최댓값과 $y+x$의 최댓값을 각각 구하시오.

## Choices


## Answer
$1+\frac{\sqrt2}{2},\ \frac{3\sqrt2}{2}$

## Solution
주어진 식은 중심이 $P(\cos\theta,\sin\theta)$이고 반지름이 $\frac12$인 원이다.

고정된 $\theta$에서 $y-x$의 최댓값을 구하기 위해 직선
$$
y-x=t
$$
를 생각하자. 최댓값일 때 이 직선은 원에 접하므로,
중심 $P$와 직선 사이의 거리는 반지름 $\frac12$와 같다.
$$
\frac{|\,t-(\sin\theta-\cos\theta)\,|}{\sqrt2}=\frac12
$$
최댓값에서는 큰 쪽을 택하므로
$$
t_{\max}=\sin\theta-\cos\theta+\frac{\sqrt2}{2}.
$$
따라서
$$
\max(y-x)=\max(\sin\theta-\cos\theta)+\frac{\sqrt2}{2}.
$$

이제 $-\pi\le\theta\le\frac\pi4$에서 $\sin\theta-\cos\theta$의 최댓값을 구한다.

$-\pi\le\theta\le0$이면 $\sin\theta\le0$이므로
$$
\sin\theta-\cos\theta\le-\cos\theta\le1.
$$

$0\le\theta\le\frac\pi4$이면 $\sin\theta\le\cos\theta$이므로
$$
\sin\theta-\cos\theta\le0\le1.
$$

따라서 전체 구간에서 $\sin\theta-\cos\theta\le1$이고, $\theta=-\pi$일 때 $1$이 된다.
그러므로
$$
\max(y-x)=1+\frac{\sqrt2}{2}.
$$

같은 방법으로 $y+x$의 최댓값을 구하면,
직선 $y+x=s$가 원에 접할 때
$$
\frac{|\,s-(\sin\theta+\cos\theta)\,|}{\sqrt2}=\frac12
$$
이므로
$$
\max(y+x)=\max(\sin\theta+\cos\theta)+\frac{\sqrt2}{2}.
$$

이제 $\sin\theta+\cos\theta$의 최댓값을 구한다.

$-\pi\le\theta\le0$이면 $\sin\theta\le0$이므로
$$
\sin\theta+\cos\theta\le\cos\theta\le1.
$$

$0\le\theta\le\frac\pi4$이면 $\sin\theta,\cos\theta\ge0$이고
$$
(\sin\theta-\cos\theta)^2\ge0
$$
이므로
$$
(\sin\theta+\cos\theta)^2
=\sin^2\theta+\cos^2\theta+2\sin\theta\cos\theta
\le2(\sin^2\theta+\cos^2\theta)=2.
$$
따라서
$$
\sin\theta+\cos\theta\le\sqrt2,
$$
그리고 $\theta=\frac\pi4$일 때 등호가 성립한다.

결론적으로
$$
\max(y+x)=\sqrt2+\frac{\sqrt2}{2}=\frac{3\sqrt2}{2}.
$$
