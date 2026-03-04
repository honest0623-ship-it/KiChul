---
id: BY-2024-G1-S1-MID-104
school: BY
year: 2024
grade: 1
semester: 1
exam: MID
type: 서술형
source_question_no: 4
source_question_kind: subjective
source_question_label: "서답4"
difficulty: 3
level: 3
unit: "공통수학1(2022개정)>1. 다항식>1-2. 나머지정리"
unit_l1: "공통수학1(2022개정)"
unit_l2: "1. 다항식"
unit_l3: "1-2. 나머지정리"
source: "user_upload_2026-03-04"
tags:
  - 자동입력
  - 서술형
  - 출제번호-4
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답4번_1-2. 나머지정리.png
---

## Q
[오류문항] 조건 (가), (나)를 엄밀히 동시에 적용하면 모순이 발생하여 해당 다항식 $f(x)$가 존재하지 않는다.

다항식 $f(x)$가 다음 조건을 만족시킨다.

(가) 다항식 $f(x)$를 $x^2-4x+3$으로 나눈 몫을 $Q(x)$, 나머지는 $-Q(x)$이다.

(나) 다항식 $f(x)$를 $x^2+2x+1$로 나눈 몫을 $Q_1(x)$, 나머지를 $R(x)$라 하면,
\[
R(x)=x\{f(2)-f(1)\},\quad f(0)-f(3)=48
\]
을 만족한다.

이때 $f(-2)$의 값을 구하는 풀이과정을 쓰고 답을 구하시오.

## Choices


## Answer
조건 모순으로 해가 존재하지 않음

## Solution
(가)에서
\[
f(x)=(x^2-4x+3)Q(x)-Q(x)=(x^2-4x+2)Q(x)
\]
이고, 나머지의 차수 조건 때문에 $Q(x)$는 일차식이라 둘 수 있다.
\[
Q(x)=ux+v
\]
따라서
\[
f(x)=(x^2-4x+2)(ux+v)
\]

또
\[
k=f(2)-f(1)
\]
라 두면 (나)에서
\[
R(x)=kx
\]
이다.

$f(x)=(x+1)^2Q_1(x)+R(x)$이므로
\[
f(-1)=R(-1)=-k,\quad f'(-1)=R'(-1)=k
\]
가 성립한다.

한편
\[
f(2)-f(1)=-3u-v
\]
이므로
\[
k=-3u-v
\]

또 직접 계산하면
\[
f(-1)=-7u+7v,\quad f'(-1)=13u-6v
\]
따라서
\[
-7u+7v=-k=3u+v \Rightarrow 5u=3v \quad \cdots (1)
\]
\[
13u-6v=k=-3u-v \Rightarrow 16u=5v \quad \cdots (2)
\]

(1), (2)를 동시에 만족하려면
\[
u=v=0
\]
뿐이다.

그러면 $f(x)\equiv 0$이 되어
\[
f(0)-f(3)=0
\]
인데, 이는 조건 $f(0)-f(3)=48$과 모순이다.

즉, 주어진 조건을 모두 만족하는 다항식 $f(x)$는 존재하지 않는다.
