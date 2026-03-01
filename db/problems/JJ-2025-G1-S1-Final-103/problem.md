---
id: JJ-2025-G1-S1-Final-103
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 단답형
source_question_no: 3
source_question_kind: subjective
source_question_label: 서답3
difficulty: '4'
level: 4
unit: 공통수학1(2022개정)>4. 행렬>4-1. 행렬과 그 연산
unit_l1: 공통수학1(2022개정)
unit_l2: 4. 행렬
unit_l3: 4-1. 행렬과 그 연산
source: user_upload_2026-02-27
tags:
- 수동정제
- 단답형
- 출제번호-3
assets:
- assets/original/
- assets/original/서답3번.png
---
## Q
이차정사각행렬 $A,B$가 다음 조건을 만족할 때, $A^6+B^6=kE$이다. 상수 $k$의 값을 구하시오. (단, $E$는 단위행렬이고, $O$는 영행렬이다.)

(가) $A=B+2E$
(나) $AB=O$

## Choices


## Answer
64

## Solution
$A=B+2E$를 $AB=O$에 대입하면
$$
(B+2E)B=O\Rightarrow B^2+2B=O\Rightarrow B^2=-2B
$$
이다. 따라서
$$
B^6=(-2)^5B=-32B.
$$

또한
$$
A^2=(B+2E)^2=B^2+4B+4E=2B+4E=2A
$$
이므로
$$
A^6=2^5A=32A=32(B+2E)=32B+64E.
$$
따라서
$$
A^6+B^6=(32B+64E)+(-32B)=64E
$$
이므로
$$
k=64
$$
이다.
