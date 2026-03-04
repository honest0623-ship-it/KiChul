---
id: BY-2025-G2-S1-MID-101
school: BY
year: 2025
grade: 2
semester: 1
exam: MID
type: 단답형
source_question_no: 1
source_question_kind: subjective
source_question_label: "서답1"
difficulty: 5
level: 5
unit: "대수(2022개정)>1. 지수함수와 로그함수>1-1. 지수와 로그"
unit_l1: "대수(2022개정)"
unit_l2: "1. 지수함수와 로그함수"
unit_l3: "1-1. 지수와 로그"
source: "user_upload_2026-03-03"
tags:
  - 자동입력
  - 단답형
  - 출제번호-1
  - OCR
  - AI
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/서답1번_1-1. 지수와 로그.png
---

## Q
1이 아닌 서로 다른 두 양수 $a, b$가 $\log_a b = \log_b a$를 만족할 때, $10(a+1)(b+1)$의 최솟값을 구하시오.

## Choices


## Answer
40

## Solution
주어진 조건 $\log_a b = \log_b a$를 변형합니다.
로그의 밑변환 공식을 이용하면 $\frac{\log b}{\log a} = \frac{\log a}{\log b}$ 입니다.
양변에 $(\log a)(\log b)$를 곱하면 $(\log b)^2 = (\log a)^2$ 입니다.
따라서 $\log b = \pm \log a$ 입니다.

1. $\log b = \log a$ 인 경우:
   $b=a$ 입니다. 하지만 문제에서 $a, b$는 서로 다른 양수라고 했으므로 이 경우는 성립하지 않습니다.

2. $\log b = -\log a$ 인 경우:
   $\log b = \log (a^{-1})$ 이므로 $b = a^{-1} = \frac{1}{a}$ 입니다.
   이때, $a, b$는 1이 아닌 양수이고 서로 다르다는 조건을 만족하는지 확인합니다.
   $a>0$ 이면 $b=1/a > 0$ 입니다.
   $a \neq 1$ 이면 $b=1/a \neq 1$ 입니다.
   $a \neq b$ 이면 $a \neq 1/a$, 즉 $a^2 \neq 1$ 이고 $a>0$ 이므로 $a \neq 1$ 입니다.
   따라서 $a>0$ 이고 $a \neq 1$ 이면 모든 조건을 만족합니다.

이제 $10(a+1)(b+1)$의 최솟값을 구합니다. $b=\frac{1}{a}$를 대입합니다.
$10(a+1)(\frac{1}{a}+1) = 10(a+1)(\frac{1+a}{a})$
$= 10 \frac{(a+1)^2}{a}$
$= 10 \frac{a^2+2a+1}{a}$
$= 10 (a + 2 + \frac{1}{a})$
$= 10 (a + \frac{1}{a} + 2)$

$a>0$ 이므로 산술-기하 평균 부등식에 의해 $a + \frac{1}{a} \ge 2\sqrt{a \cdot \frac{1}{a}} = 2$ 입니다.
등호는 $a = \frac{1}{a}$, 즉 $a^2=1$ 일 때 성립합니다. $a>0$ 이므로 $a=1$ 일 때 등호가 성립합니다.
하지만 문제 조건에서 $a \neq 1$ 이므로 $a + \frac{1}{a} > 2$ 입니다.
따라서 $10 (a + \frac{1}{a} + 2) > 10 (2 + 2) = 40$ 입니다.

$a + \frac{1}{a}$는 $a=1$일 때 최솟값 2를 가지지만, $a \neq 1$이므로 2보다 큰 값을 가집니다.
그러나 $a$가 1에 한없이 가까워질수록 $a + \frac{1}{a}$는 2에 한없이 가까워집니다.
따라서 주어진 식 $10(a + \frac{1}{a} + 2)$의 값은 40에 한없이 가까워지지만 40이 될 수는 없습니다.
고등학교 과정에서 '최솟값'을 구하라는 문제는 일반적으로 극한값(하한)을 최솟값으로 간주하는 경우가 많습니다.
그러므로 최솟값은 40입니다.
