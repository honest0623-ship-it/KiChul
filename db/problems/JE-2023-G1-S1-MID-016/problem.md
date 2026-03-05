---
id: JE-2023-G1-S1-MID-016
school: JE
year: 2023
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: "16"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-2. 이차방정식과 이차함수"
source: "user_upload_2026-03-04"
tags:
  - 수동작성
  - 객관식
  - 출제번호-16
assets:
  - assets/original/
  - assets/original/016_2-2. 이차방정식과 이차함수.png
---

## Q
\(f(x)\)는 이차함수이고
\[
2f(x)+f(1-x)=3x^2
\]
일 때, 보기에서 옳은 것을 모두 고른 것은?

<보기>  
ㄱ. \(f(0)=-1\)  
ㄴ. \(f(x)\)의 최솟값은 \(-2\)이다.  
ㄷ. 모든 \(x\)에 대하여 \(f(x)=f(-2-x)\)이다.

## Choices
① ㄱ  
② ㄷ  
③ ㄱ, ㄴ  
④ ㄱ, ㄷ  
⑤ ㄱ, ㄴ, ㄷ

## Answer
ㄱ, ㄴ, ㄷ

## Solution
\[
f(x)=ax^2+bx+c
\]
로 두면
\[
f(1-x)=a(1-x)^2+b(1-x)+c
\]
\[
=ax^2+(-2a-b)x+(a+b+c).
\]

따라서
\[
2f(x)+f(1-x)
\]
\[
=3ax^2+(b-2a)x+(a+b+3c).
\]
이것이 \(3x^2\)와 같으므로
\[
3a=3,\quad b-2a=0,\quad a+b+3c=0.
\]

즉
\[
a=1,\quad b=2,\quad c=-1.
\]
따라서
\[
f(x)=x^2+2x-1=(x+1)^2-2.
\]

이제 각 보기 확인:
\[
f(0)=-1
\]
이므로 ㄱ은 참.

\[
f(x)=(x+1)^2-2
\]
이므로 최솟값은 \(-2\), 즉 ㄴ은 참.

축이 \(x=-1\)이므로
\[
f(-1+t)=f(-1-t).
\]
여기서 \(t=x+1\)로 두면
\[
f(x)=f(-2-x).
\]
따라서 ㄷ도 참.

결론적으로 ㄱ, ㄴ, ㄷ이 모두 옳다.

