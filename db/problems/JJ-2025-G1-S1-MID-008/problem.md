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
unit: 공통수학1 > 방정식과 부등식 > 복소수
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
unit_l1: 공통수학1
unit_l2: 방정식과 부등식
unit_l3: 복소수
---

## Q
함수 $f(n)=\left(\frac{1-i}{1+i}\right)^{2n}$, $g(m)=\left(\frac{1+i}{1-i}\right)^{m+1}$ 일 때, $f(1)+g(1)+f(2)+g(2)+\cdots+f(13)+g(13)$의 값은?

## Choices
① $-1-i$
② $1-i$
③ $1+i$
④ $0$
⑤ $-2$

## Answer
$-2$

## Solution
먼저 주어진 복소수 식을 간단히 합니다.
$\frac{1-i}{1+i} = \frac{(1-i)(1-i)}{(1+i)(1-i)} = \frac{1-2i+i^2}{1-i^2} = \frac{1-2i-1}{1+1} = \frac{-2i}{2} = -i$
$\frac{1+i}{1-i} = \frac{(1+i)(1+i)}{(1-i)(1+i)} = \frac{1+2i+i^2}{1-i^2} = \frac{1+2i-1}{1+1} = \frac{2i}{2} = i$

따라서 함수 $f(n)$과 $g(m)$은 다음과 같이 간단히 표현됩니다.
$f(n) = (-i)^{2n} = ((-i)^2)^n = (-1)^n$
$g(m) = i^{m+1}$

구하고자 하는 값은 $\sum_{k=1}^{13} (f(k) + g(k))$ 입니다. 이 합을 두 부분으로 나누어 계산합니다.

1. $\sum_{k=1}^{13} f(k)$ 계산:
$f(k) = (-1)^k$ 이므로,
$f(1) = -1$
$f(2) = 1$
$f(3) = -1$
...
$f(13) = -1$
$\sum_{k=1}^{13} f(k) = (-1+1) + (-1+1) + \cdots + (-1+1) + (-1)$ (총 6쌍의 합과 마지막 항)
$= 0 \times 6 - 1 = -1$

2. $\sum_{k=1}^{13} g(k)$ 계산:
$g(k) = i^{k+1}$ 이므로,
$g(1) = i^{1+1} = i^2 = -1$
$g(2) = i^{2+1} = i^3 = -i$
$g(3) = i^{3+1} = i^4 = 1$
$g(4) = i^{4+1} = i^5 = i$
$g(5) = i^{5+1} = i^6 = -1$
복소수 $i$의 거듭제곱은 주기가 4이므로, $g(k)$의 값도 주기가 4입니다.
$g(1)+g(2)+g(3)+g(4) = -1 + (-i) + 1 + i = 0$
총 13개의 항이 있으므로, $13 = 4 \times 3 + 1$ 입니다.
$\sum_{k=1}^{13} g(k) = (g(1)+g(2)+g(3)+g(4)) \times 3 + g(13)$
$= 0 \times 3 + i^{13+1}$
$= i^{14}$
$i^{14} = i^{4 \times 3 + 2} = (i^4)^3 \times i^2 = 1^3 \times (-1) = -1$
따라서 $\sum_{k=1}^{13} g(k) = -1$

3. 최종 합 계산:
$\sum_{k=1}^{13} (f(k) + g(k)) = \sum_{k=1}^{13} f(k) + \sum_{k=1}^{13} g(k) = -1 + (-1) = -2$

따라서 구하는 값은 $-2$입니다.
