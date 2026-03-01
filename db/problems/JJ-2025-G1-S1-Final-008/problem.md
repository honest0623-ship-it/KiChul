---
id: JJ-2025-G1-S1-Final-008
school: JJ
year: 2025
grade: 1
semester: 1
exam: Final
type: 객관식
source_question_no: 8
source_question_kind: objective
source_question_label: '8'
difficulty: '3'
level: 3
unit: 공통수학1(2022개정)>3. 경우의 수>3-2. 순열과 조합
unit_l1: 공통수학1(2022개정)
unit_l2: 3. 경우의 수
unit_l3: 3-2. 순열과 조합
source: user_upload_2026-02-27
tags:
- 수동정제
- 객관식
- 출제번호-8
assets:
- assets/original/
- assets/original/008.png
---
## Q
6개의 문자 $a,b,c,d,e,f$를 사전식으로 배열할 때, 444번째로 배열된 문자는?

## Choices
① cfeadb
② daefcb
③ dbcafe
④ dcfaeb
⑤ debfca

## Answer
⑤

## Solution
첫 글자별 경우의 수는 $5!=120$이다.

$444$번째는
$$
361\sim 480
$$
구간에 있으므로 첫 글자는 $d$이다.

이제 남은 순번은 $444-360=84$번째이다. 둘째 글자별 경우의 수는 $4!=24$이므로
$$
73\sim 96
$$
구간에 해당하는 둘째 글자는 $e$이다.

남은 순번은 $84-72=12$번째이고, 셋째 글자별 경우의 수는 $3!=6$이므로 셋째 글자는 $b$이다.

남은 순번은 $12-6=6$번째이고, 넷째 글자별 경우의 수는 $2!=2$이므로 넷째 글자는 $f$이다.

남은 두 글자 $a,c$에서 $6$번째는 둘째 자리 선택이 $c$이므로 문자열은
$$
debfca
$$
이다.
