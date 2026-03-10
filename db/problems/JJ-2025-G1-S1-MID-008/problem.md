---
id: JJ-2025-G1-S1-MID-008
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: '8'
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: web_upload_2026-02-28
tags:
- 자동입력
- 객관식
- 출제번호-8
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/008.png
level: 4
---

## Q
함수
$$
f(n)=\left(\frac{1-i}{1+i}\right)^{2n},\quad g(m)=\left(\frac{1+i}{1-i}\right)^{m+1}
$$
일 때,
$$
f(1)+g(1)+f(2)+g(2)+\cdots+f(13)+g(13)
$$
의 값을 구하시오.

## Choices
① $-1-i$
② $1-i$
③ $1+i$
④ $0$
⑤ $-2$

## Answer
⑤

## Solution
먼저 복소수 비를 정리하면
$$
\frac{1-i}{1+i}=-i,\quad \frac{1+i}{1-i}=i
$$
이므로
$$
f(n)=(-i)^{2n}=(-1)^n,\quad g(m)=i^{m+1}
$$
이다.

따라서
$$
\sum_{n=1}^{13} f(n)=\sum_{n=1}^{13}(-1)^n=-1
$$
이고,
$$
\sum_{m=1}^{13} g(m)=\sum_{m=1}^{13} i^{m+1}
$$
에서 $i^2,-i,1,i$가 주기 4로 반복되므로 12개 합은 0, 남는 $i^{14}=-1$이다.
즉
$$
\sum_{m=1}^{13} g(m)=-1
$$
이다.

결국
$$
f(1)+g(1)+\cdots+f(13)+g(13)=-1+(-1)=-2
$$
이므로 정답은 ⑤이다.
