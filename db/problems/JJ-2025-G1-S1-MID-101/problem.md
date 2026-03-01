---
id: JJ-2025-G1-S1-MID-101
school: JJ
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '4'
unit: 공통수학1(2022개정)>1. 다항식>1-2. 나머지정리
source: web_upload_2026-02-27
tags:
- 자동입력
- 서술형
- 출제번호-1
- OCR
- AI
assets:
- assets/scan.png
- assets/original/
- assets/original/서답1번.png
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 1. 다항식
unit_l3: 1-2. 나머지정리
---
## Q
x에 대한 다항식 $x^{2025} +x+1$을 $x^2-1$로 나누었을 때의 몫을 $Q(x)$라 할 때, $Q(x)$의 상수를 포함힌 모든 계수의 합을 구하시오.

## Choices


## Answer
1012

## Solution
$x^{2025}+x+1$을 $x^2-1$로 나눌 때의 나머지를 $R(x)$라 하면,
$$
R(x)=ax+b
$$
로 둘 수 있다.

$x=1,-1$을 대입하면
$$
R(1)=1^{2025}+1+1=3,\qquad R(-1)=(-1)^{2025}+(-1)+1=-1
$$
이므로 $R(x)=2x+1$이다.

따라서 몫 $Q(x)$는
$$
Q(x)=\frac{x^{2025}+x+1-(2x+1)}{x^2-1}
=\frac{x^{2025}-x}{x^2-1}.
$$

계수의 합은 $Q(1)$이므로
$$
Q(1)=\lim_{x\to1}\frac{x^{2025}-x}{x^2-1}
=\lim_{x\to1}\frac{2025x^{2024}-1}{2x}
=\frac{2024}{2}=1012.
$$
