---
id: HN-2025-G1-S1-MID-106-sim002
school: HN
year: 2025
grade: 1
semester: 1
exam: MID
type: 서술형
difficulty: '4'
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-2. 이차방정식과 이차함수
source: user_upload_2026-02-27
tags:
- 서답형-서술형
- 출제번호-6
assets:
- assets/scan.png
- assets/original/
level: 4
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-2. 이차방정식과 이차함수
derived_from: HN-2025-G1-S1-MID-106
similarity_type: parameter_change
generation_batch_id: sim_20260309_182621
generation_model: openai:gpt-5-mini
review_status: pending
review_note: ''
promoted_to: ''
generated_at: '2026-03-09T18:34:03'
---

## Q
구간 $[k-1,k+1]$에서 이차함수 $y=(x-3)^2+k$의 최솟값이 $4$일 때, 가능한 모든 상수 $k$의 값의 합을 구하시오.

## Choices


## Answer
4

## Solution
이차함수의 꼭짓점은 $x=3$이고 그때의 함수값은 $y=k$이다.

(1) $3\in[k-1,k+1]$ 즉 $k-1\le3\le k+1\iff 2\le k\le4$인 경우: 최솟값은 $k$이므로 $k=4$이어야 한다. ($k=4$는 조건을 만족함)

(2) $3\notin[k-1,k+1]$인 경우
- 만약 $k<2$이면 구간의 오른쪽 끝점 $x=k+1$에서 최소가 되고,
  \[y((k+1))=(k+1-3)^2+k=(k-2)^2+k=k^2-3k+4.\]
  이를 $4$로 놓으면 $k^2-3k+4=4\iff k(k-3)=0$이므로 $k=0,3$. 그러나 $k<2$이어야 하므로 $k=0$만 허용된다.

- 만약 $k>4$이면 구간의 왼쪽 끝점 $x=k-1$에서 최소가 되고,
  \[y((k-1))=(k-1-3)^2+k=(k-4)^2+k=k^2-7k+16.\]
  이를 $4$로 놓으면 $k^2-7k+12=0\iff (k-3)(k-4)=0$이므로 $k=3,4$이나 $k>4$인 해는 없다.

따라서 가능한 $k$값은 $0,\,4$이고 그 합은 $0+4=4$이다.
