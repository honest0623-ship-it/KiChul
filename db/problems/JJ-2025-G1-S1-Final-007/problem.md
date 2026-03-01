---
id: JJ-2025-G1-S1-Final-007
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 7
source_question_kind: objective
source_question_label: '7'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-02-27
tags:
- 수동정제
- 객관식
- 출제번호-7
assets:
- assets/original/
- assets/original/007.png
---
## Q
부등식 $2|x-1|+|x+1|\le a$를 만족하는 실수 $x$의 범위가 $-2\le x\le b$가 되도록 하는 상수 $a,b$에 대하여 $3ab$의 값은?

## Choices
① 54
② 56
③ 58
④ 60
⑤ 62

## Answer
②

## Solution
$f(x)=2|x-1|+|x+1|$로 두고 구간별로 정리하면
$$
f(x)=
\begin{cases}
1-3x & (x\le -1),\\
3-x & (-1\le x\le 1),\\
3x-1 & (x\ge 1).
\end{cases}
$$
해집합의 왼쪽 끝이 $-2$이므로 $a=f(-2)=7$이다.

이제 $f(x)\le 7$을 풀면
$$
-2\le x\le \frac{8}{3}
$$
이므로 $b=\frac{8}{3}$이다.

따라서
$$
3ab=3\cdot 7\cdot \frac{8}{3}=56
$$
이다.
