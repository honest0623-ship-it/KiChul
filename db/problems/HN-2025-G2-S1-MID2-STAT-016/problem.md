---
id: HN-2025-G2-S1-MID2-STAT-016
school: HN
year: 2025
grade: 2
semester: 1
exam: MID2
subject: STAT
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: '16'
difficulty: 3
level: 3
unit: 확률과 통계(2022개정)>2. 확률>2-2. 조건부 확률
unit_l1: 확률과 통계(2022개정)
unit_l2: 2. 확률
unit_l3: 2-2. 조건부 확률
source: user_upload_2026-03-05
tags:
- 수동작성
- 객관식
- 출제번호-16
- 과목-확률과통계
assets:
- assets/original/
- assets/original/HN.2025.G2.S1.MID.010.STAT.PDF
---

## Q
표본공간 $S$의 두 사건 $A, B$에 대하여 다음 <보기>에서 옳은 것의 개수는?
(단, $0<P(A)<1$, $0<P(B)<1$)

<보기>
ㄱ. 서로 배반이 아닌 두 사건은 독립사건이다.
ㄴ. 서로 배반인 두 사건은 종속사건이다.
ㄷ. 서로 종속인 두 사건은 배반사건이 아니다.
ㄹ. $A, B$가 서로 독립이면 $P(A\mid B^c)=1-P(A^c\mid B)$이다.
ㅁ. $A\cup B=S$이면 $P(A)+P(B)=1$이다.
ㅂ. $A, B$가 서로 독립이면 $A^c, B^c$은 서로 종속이다.

## Choices
① 1개
② 2개
③ 3개
④ 4개
⑤ 5개

## Answer
②

## Solution
각 문장을 판단한다.

ㄱ. 배반이 아니어도 독립일 필요는 없으므로 거짓.

ㄴ. 배반이면 $P(A\cap B)=0$이고, $0<P(A),P(B)<1$에서 $P(A)P(B)>0$이므로
독립이 아니고 종속이다. 참.

ㄷ. 종속이라도 배반일 수 있다(ㄴ의 경우). 거짓.

ㄹ. $A,B$가 독립이면 $A$와 $B^c$도 독립이므로
$$
P(A|B^c)=P(A)
$$
또한 $A^c$와 $B$도 독립이므로
$$
P(A^c|B)=P(A^c)=1-P(A)
$$
따라서
$$
1-P(A^c|B)=P(A)=P(A|B^c)
$$
이므로 참.

ㅁ. 일반적으로
$$
P(A\cup B)=P(A)+P(B)-P(A\cap B)
$$
인데 $P(A\cup B)=1$이므로 $P(A)+P(B)=1+P(A\cap B)$이다.
항상 1은 아니므로 거짓.

ㅂ. 독립이면 여사건들 $A^c,B^c$도 독립이다. 종속이라는 말은 거짓.

옳은 것은 ㄴ, ㄹ의 2개이다.
