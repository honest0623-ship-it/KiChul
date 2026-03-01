---
id: BY-2025-G1-S1-MID-015
school: BY
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 15
source_question_kind: objective
source_question_label: '15'
difficulty: '2'
level: 2
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
source: user_upload_2026-02-27
tags:
- 객관식
- 출제번호-15
- 오류문항
error: true
error_type: 조건모순
error_note: 원문에서 f(x)를 삼차식이라 했지만, f(3x+2)=f(2x+1)+2x의 최고차항 비교 시 모순이 발생함.
error_handling: 삼차식 표기를 오기(다항식)로 보정하여 기존 정답 ②를 유지함.
assets:
- assets/original/
- assets/original/015.png
---
## Q
> [오류문항] 조건오류: 원문의 "삼차식" 조건은 함수식과 양립하지 않습니다. (최고차항 비교 시 모순)

삼차식 $f(x)$를 $x-3$로 나누었을 때, 나머지가 $2$이고,
$$
f(3x+2)=f(2x+1)+2x
$$
를 만족한다고 하자. $f(x)$를 $x^2-13x+40$으로 나누었을 때의 나머지를 $R(x)$라 할 때, $R(3)$의 값은?

## Choices
① $\dfrac{2}{3}$  
② $\dfrac{4}{3}$  
③ $2$  
④ $\dfrac{8}{3}$  
⑤ $\dfrac{10}{3}$

## Answer
②

## Solution
원문 조건을 그대로 쓰면 모순이 생긴다.  
$f(x)=ax^3+\cdots$라 두면
$$
f(3x+2)-f(2x+1)
$$
의 $x^3$항 계수는 $(27a-8a)=19a$인데, 우변은 $2x$이므로 $x^3$항이 없어야 해서 $a=0$이 되어 삼차식과 모순이다.

따라서 출제 의도(삼차식 표기 오기)를 보정해 나머지정리 풀이를 진행하면 다음과 같다.

$x-3$으로 나눈 나머지가 $2$이므로
$$
f(3)=2.
$$

주어진 식에 $x=1$을 대입하면
$$
f(5)=f(3)+2=4.
$$
$x=2$를 대입하면
$$
f(8)=f(5)+4=8.
$$

$x^2-13x+40=(x-5)(x-8)$이므로 나머지 $R(x)$는 일차식이고
$$
R(5)=f(5)=4,\quad R(8)=f(8)=8.
$$
따라서
$$
R(x)=\frac{4}{3}x-\frac{8}{3},
$$
이므로
$$
R(3)=\frac{4}{3}.
$$
