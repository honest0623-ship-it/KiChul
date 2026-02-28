---
id: JJ-2025-G1-S1-MID-104
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '3'
unit: 공통수학1 > 다항식 > 나머지정리/인수정리
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-4
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답4번.png
level: 3
unit_l1: 공통수학1
unit_l2: 다항식
unit_l3: 나머지정리/인수정리
---

## Q
다항식 $P(x)$를 $x^2-1$로 나누었을 때 나머지가 $x+3$이고, $x^2-4$로 나누었을 때 나머지가 $x$이다. $P(x)$를 $x^2+x-2$으로 나누었을 때, 나머지를 구하시오.

## Choices


## Answer
(AI 정답 추출 실패)

## Solution
나머지 정리와 다항식의 나눗셈 정리를 이용하면 다음과 같이 풀 수 있습니다.

우선 $P(x)$는 다음과 같이 표현할 수 있습니다.

$$P(x) = (x^2 - 1)Q_1(x) + x + 3,$$
$$P(x) = (x^2 - 4)Q_2(x) + x.$$

이를 $x^2 + x - 2 = (x+2)(x-1)$으로 나누는 문제로 변환하면,

$$P(x) = (x^2 + x - 2)Q_3(x) + ax + b.$$

이제 $x = 1$과 $x = -2$일 때의 $P(x)$값을 이용해서 $a$와 $b$를 구할 수 있습니다.

$x=1$을 대입하면,

$$P(1) = 1 + 3 = 4 = a + b.$$

$x=-2$을 대입하면,

$$P(-2) = -2 = -2a + b.$$

이를 연립방정식으로 풀면,

$$a = \frac{6}{3} = 2, \quad b = 2.$$

따라서 나머지는 $2x + 2$입니다.
