---
id: HN-2024-G1-S1-MID-016
school: HN
year: 2024
grade: 1
semester: 1
exam: MID
type: 객관식
source_question_no: 16
source_question_kind: objective
source_question_label: "16"
difficulty: 4
level: 4
unit: "공통수학1(2022개정)>2. 방정식과 부등식>2-3. 여러 가지 방정식"
unit_l1: "공통수학1(2022개정)"
unit_l2: "2. 방정식과 부등식"
unit_l3: "2-3. 여러 가지 방정식"
source: "user_upload_2026-03-03"
tags:
  - 수동보정
  - 객관식
  - 출제번호-16
assets:
  # Raw source image archive.
  - assets/original/
  - assets/original/016_2-3. 여러 가지 방정식.png
---

## Q
사차방정식 $x^4-x^2+4=0$의 한 근을 $\alpha$라 할 때, `<보기>`에서 옳은 것을 모두 고른 것은?

`<보기>`

ㄱ. $\alpha+\dfrac{1}{\alpha}=2$이 되는 $\alpha$가 존재한다.

ㄴ. $\alpha^2+\sqrt{3}i\alpha-2=0$이 되는 $\alpha$가 존재한다. (단, $i=\sqrt{-1}$)

ㄷ. $(\alpha+m)^2$이 음수가 되도록 하는 실수 $m$의 값은 네 개다.

## Choices
① ㄱ
② ㄴ
③ ㄱ, ㄴ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ

## Answer
②

## Solution
주어진 식을 인수분해하면
\[
x^4-x^2+4=(x^2+\sqrt{5}x+2)(x^2-\sqrt{5}x+2)=0
\]
이므로 $\alpha$는 위 두 이차방정식의 근이다.

ㄱ. $\alpha+\dfrac1\alpha=2$라면
\[
\alpha^2-2\alpha+1=0 \Rightarrow (\alpha-1)^2=0
\]
이어서 $\alpha=1$이어야 한다.  
하지만 $x=1$은 $x^4-x^2+4=0$의 근이 아니므로 거짓.

ㄴ. $\alpha^2+\sqrt{3}i\alpha-2=0$의 근은
\[
\alpha=\frac{-\sqrt{3}i\pm\sqrt{5}}{2}
=\frac{\pm\sqrt5-\sqrt3\,i}{2}
\]
이다.  
이는 각각
\[
x^2-\sqrt5x+2=0,\quad x^2+\sqrt5x+2=0
\]
의 근과 일치하므로 참.

ㄷ. $\alpha=p+qi\ (q\neq0),\ m\in\mathbb{R}$라 두면
\[
(\alpha+m)^2=((p+m)^2-q^2)+2q(p+m)i
\]
이다. 음수(실수)가 되려면 허수부가 0이어야 하므로
\[
2q(p+m)=0 \Rightarrow m=-p
\]
뿐이다. 이때 값은
\[
(\alpha-p)^2=(qi)^2=-q^2<0
\]
이므로 가능한 $m$은 1개이다. 따라서 거짓.

따라서 옳은 것은 ㄴ만이므로 정답은 **②**.
