---
id: JJ-2024-G1-S1-MID-009
school: JJ
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 9
source_question_kind: objective
source_question_label: '9'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-04
tags:
- 자동입력
- 객관식
- 출제번호-9
- manual-fix
assets:
- assets/original/
- assets/original/009_2-1. 복소수와 이차방정식.png
---

## Q
다음 조건을 만족하는 실수 $p, q$에 대하여 $|pq|$의 값을 구하시오.

(가) 이차방정식 $x^2+px+q=0$의 서로 다른 두 실근은 $\alpha,\beta$이다.
(나) 이차방정식 $x^2+(p+q)x+(8p+q)=0$의 두 실근은 $|\alpha|,|\beta|$이다.

## Choices
① $16$
② $20$
③ $24$
④ $28$
⑤ $32$

## Answer
①

## Solution
$\alpha+\beta=-p$, $\alpha\beta=q$이다.
두 번째 방정식의 근이 $|\alpha|,|\beta|$이므로
$|\alpha|+|\beta|=-(p+q)$,
$|\alpha\beta|=|q|=8p+q$.

$q\ge0$이면 $|q|=q$이므로 $8p=0\Rightarrow p=0$인데, 이때 첫 방정식은 서로 다른 두 실근을 갖기 어렵다. 따라서 $q<0$.

그러면 $|q|=-q$이므로
$-q=8p+q\Rightarrow p=-\frac{q}{4}$.

$q<0$에서는 $\alpha,\beta$ 부호가 반대이므로
$|\alpha|+|\beta|=\sqrt{(\alpha+\beta)^2-4\alpha\beta}=\sqrt{p^2-4q}$.
따라서
$\sqrt{p^2-4q}=-(p+q)$.

$q=-t\;(t>0)$로 두면 $p=\frac{t}{4}$,
$\frac{1}{4}\sqrt{t(t+64)}=\frac{3t}{4}$.
$\sqrt{t(t+64)}=3t\Rightarrow t(t+64)=9t^2\Rightarrow t=8$.

따라서 $q=-8$, $p=2$이고
$|pq|=|2\cdot(-8)|=16$.

정답은 ①이다.
