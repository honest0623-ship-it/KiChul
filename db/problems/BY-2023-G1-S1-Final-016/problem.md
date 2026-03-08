---
id: BY-2023-G1-S1-Final-016
school: BY
year: 2023
grade: 1
semester: 1
exam: Final
subject: COM1
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-4. 여러 가지 부등식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-4. 여러 가지 부등식
source: user_upload_2026-03-08
tags:
- 수동생성
- PDF
- 객관식
- 출제번호-16
- 과목-COM1
- 생성일-2026-03-08
assets:
- assets/original/
- assets/original/BY.2023.G1.S1.Final.COM1.pdf
---
## Q
$x$에 대한 이차부등식 $x^2-4ax+a^2+8a\ge 0$이 임의의 음이 아닌 실수 $x$에 대하여 항상 성립하도록 하는 실수 $a$의 값의 범위가 $a\le p$ 또는 $0\le a\le q$이다. 이때 $3q-p$의 값은? (단, $p,q$는 상수)

## Choices
① $8$
② $12$
③ $16$
④ $20$
⑤ $24$

## Answer
③

## Solution
주어진 식의 왼쪽을
$$
f(x)=x^2-4ax+a^2+8a
$$
라 하자.

완전제곱식으로 고치면
$$
f(x)=(x-2a)^2-3a^2+8a
$$
이다.

이제 $x\ge 0$에서의 최솟값을 생각한다.

$a<0$이면 꼭짓점의 $x$좌표 $2a$가 음수이므로, $x\ge 0$에서 최솟값은 $x=0$일 때이다.
따라서
$$
f(0)=a^2+8a=a(a+8)\ge 0
$$
이어야 하므로
$$
a\le -8
$$
이다.

$a\ge 0$이면 꼭짓점의 $x$좌표 $2a$도 음이 아니므로, $x\ge 0$에서 최솟값은 $x=2a$일 때이다.
따라서
$$
f(2a)=-3a^2+8a=a(8-3a)\ge 0
$$
이어야 하므로
$$
0\le a\le \frac{8}{3}
$$
이다.

따라서
$$
p=-8,\quad q=\frac{8}{3}
$$
이므로
$$
3q-p=8-(-8)=16
$$
이다.
