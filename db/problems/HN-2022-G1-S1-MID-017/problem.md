---
id: HN-2022-G1-S1-MID-017
school: HN
year: 2022
grade: 1
semester: 1
exam: MID
subject: COM1
type: objective
source_question_no: 17
source_question_kind: objective
source_question_label: '17'
difficulty: 4
level: 4
unit: 공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식
unit_l1: 공통수학1(2022개정)
unit_l2: 2. 방정식과 부등식
unit_l3: 2-1. 복소수와 이차방정식
source: user_upload_2026-03-06
tags:
- 수동생성
- PDF
- objective
- 출제번호-17
- 과목-COM1
- 생성일-2026-03-07
assets:
- assets/original/
- assets/original/HN-2022-G1-S1-MID-017_original.png
---

## Q
\(n\)이 자연수일 때, 복소수
\[
z_n=\left(\frac{1+i}{\sqrt{2}}\right)^n
\]
에 대하여 &lt;보기&gt;에서 옳은 것만을 있는 대로 고른 것은? \((i=\sqrt{-1})\)

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
<strong>&lt;보기&gt;</strong><br />
ㄱ. \(z_2=-i\)<br />
ㄴ. 모든 자연수 \(n\)에 대하여 \(z_n+z_{n+4}=0\)이다.<br />
ㄷ. \(z_{65}\times z_k=z_{77}\)을 만족시키는 \(30\) 이하의 자연수 \(k\)의 개수는 \(3\)이다.
</div>

## Choices
① ㄱ
② ㄴ
③ ㄷ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ
## Answer
②

## Solution
\[
\frac{1+i}{\sqrt{2}}=\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}
\]
이므로
\[
z_n=\cos\frac{n\pi}{4}+i\sin\frac{n\pi}{4}
\]
이다.
ㄱ. \(z_2=\cos\frac{\pi}{2}+i\sin\frac{\pi}{2}=i\)이므로 거짓이다.

ㄴ. \(z_{n+4}=z_n\left(\frac{1+i}{\sqrt{2}}\right)^4=z_n(-1)=-z_n\)이므로
\[
z_n+z_{n+4}=0
\]
이다. 참이다.

ㄷ. \(z_{65}z_k=z_{77}\)이면 지수는 \(8\)씩 증가할 때 같은 값을 반복하므로,
\[
65+k
\]
를 \(8\)로 나누었을 때의 나머지와
\[
77
\]
을 \(8\)로 나누었을 때의 나머지가 같아야 한다. 따라서 \(k\)를 \(8\)로 나누었을 때의 나머지는 \(4\)이다. \(30\) 이하의 자연수는 \(4,12,20,28\)의 \(4\)개이므로 거짓이다.

따라서 옳은 것은 ㄴ만이다.
