---
id: JEW-2023-G2-S1-MID2-CAL1-107
school: JEW
year: 2023
grade: 2
semester: 1
exam: MID2
subject: CAL1
type: 서답형(서술형)
source_question_no: 7
source_question_kind: subjective
source_question_label: 서답7번
difficulty: 5
level: 5
unit: 미적분 I(2022개정)>2. 미분>2-1. 미분계수와 도함수
unit_l1: 미적분 I(2022개정)
unit_l2: 2. 미분
unit_l3: 2-1. 미분계수와 도함수
source: user_upload_2026-03-06
tags:
- 수동작성
- 서답형(서술형)
- 출제번호-서답7번
- 과목-미적분 I
- 생성일-2026-03-06
assets:
- assets/original/
- assets/original/JEW-2023-G2-S1-MID2-CAL1-107_original.png
---

## Q
이차함수 $y=f(x)$가 다음을 만족할 때, 다음 물음에 대하여 풀이과정과 함께 답안을 서술하시오.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
$$
\lim_{x\to 2}\frac{f(x)-1}{x-2}=3,\qquad
\lim_{x\to 1}\frac{x-1}{f(x)+f(2)}=1
$$
</div>

1. $\lim_{x\to 2}f(x)$와 $f(2)$를 구하시오.
2. $f(x)$의 $x=2$에서의 미분계수 $f'(2)$를 구하시오.
3. $f(1)$을 구하시오.
4. $f(x)$를 구하시오.
5. 연속함수의 성질을 이용하여 열린구간 $(1,2)$에서 방정식 $f(x)=0$이 적어도 하나의 실근을 가짐을 보이시오.

## Choices


## Answer
$f(x)=x^2-x-1$

## Solution
이차함수는 연속함수이므로 차례로 구해 보자.

1.
$$
\lim_{x\to 2}\frac{f(x)-1}{x-2}=3
$$
이 유한한 값이므로 분자도 0으로 가야 한다. 따라서
$$
\lim_{x\to 2}f(x)=1
$$
이다.
이차함수는 연속이므로
$$
f(2)=1
$$
이다.

2.
$$
\lim_{x\to 2}\frac{f(x)-1}{x-2}
=\lim_{x\to 2}\frac{f(x)-f(2)}{x-2}
=f'(2)
$$
이므로
$$
f'(2)=3
$$
이다.

3.
$$
\lim_{x\to 1}\frac{x-1}{f(x)+f(2)}=1
$$
이고 $f(2)=1$이므로, 분모가 0으로 가야 한다. 따라서
$$
f(1)+1=0
$$
이고
$$
f(1)=-1
$$
이다.

4. 이차함수를
$$
f(x)=ax^2+bx+c
$$
라 하자.
$$
f(2)=1,\qquad f'(2)=3,\qquad f(1)=-1
$$
이므로
$$
4a+2b+c=1,\qquad 4a+b=3,\qquad a+b+c=-1
$$
이다.

첫째 식에서 셋째 식을 빼면
$$
3a+b=2
$$
이고, 이것을
$$
4a+b=3
$$
와 연립하면
$$
a=1,\qquad b=-1
$$
이다.
다시
$$
a+b+c=-1
$$
에 대입하면
$$
c=-1
$$
이다.

따라서
$$
f(x)=x^2-x-1
$$
이다.

5.
$$
f(1)=-1,\qquad f(2)=1
$$
이므로
$$
f(1)<0<f(2)
$$
이다.
함수 $f(x)$는 연속이므로 연속함수의 성질에 의하여 열린구간 $(1,2)$에서 방정식
$$
f(x)=0
$$
은 적어도 하나의 실근을 가진다.
