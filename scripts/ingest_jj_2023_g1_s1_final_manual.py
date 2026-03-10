from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import sys

import fitz
from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_taxonomy import normalize_unit_triplet


PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "JJ.2023.G1.S1.Final.COM1.pdf"
REPORT_PATH = ROOT / "_tmp_jj_2023_g1_s1_final_report.txt"

FIXED_META = {
    "school": "JJ",
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "Final",
    "source": "user_upload_2026-03-08",
    "subjective_offset": 100,
    "created_on": "2026-03-08",
}

RENDER_SCALE = 2.5

COM1_CPX = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식")
COM1_EQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식")
COM1_INEQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식")
COM2_COORD = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-1. 평면좌표")
COM2_LINE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식")
COM2_CIRCLE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식")


@dataclass(frozen=True)
class CropSpec:
    page: int
    box: Tuple[int, int, int, int]


@dataclass(frozen=True)
class ProblemData:
    pid: str
    subject: str
    qtype: str
    unit_triplet: Tuple[str, str, str]
    crop: CropSpec
    question: str
    choices: str
    answer: str
    solution: str
    source_label: str
    level: int
    warning: Optional[str] = None
    ocr_uncertain: bool = False


DATA: Sequence[ProblemData] = (
    ProblemData(
        pid="JJ-2023-G1-S1-Final-001",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (40, 330, 870, 760)),
        source_label="1",
        level=3,
        question=r"""방정식
\[
x^3-x^2-kx+k=0
\]
이 한 개의 실근과 두 개의 허근을 가질 때, 정수 $k$의 최댓값은?""",
        choices=r"""① $-2$
② $-1$
③ $0$
④ $1$
⑤ $2$""",
        answer="②",
        solution=r"""주어진 식을 인수분해하면
\[
x^3-x^2-kx+k=(x-1)(x^2-k)
\]
이다.

따라서 근은
\[
x=1,\qquad x=\pm \sqrt{k}
\]
이다.

한 개의 실근과 두 개의 허근을 가지려면
\[
x^2-k=0
\]
이 실근을 가지지 않아야 하므로
\[
k<0
\]
이다.

이 조건을 만족하는 정수 $k$의 최댓값은
\[
-1
\]
이므로 정답은 ②이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-002",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(0, (40, 1080, 870, 1530)),
        source_label="2",
        level=3,
        question=r"""연립방정식
\[
\begin{cases}
\sqrt{3}x-y=2k \\
x^2+y^2=16
\end{cases}
\]
가 두 쌍의 해를 갖도록 하는 정수 $k$의 개수는?""",
        choices=r"""① $7$
② $8$
③ $9$
④ $10$
⑤ $11$""",
        answer="①",
        solution=r"""직선
\[
\sqrt{3}x-y=2k
\]
를
\[
\sqrt{3}x-y-2k=0
\]
이라 두자.

원
\[
x^2+y^2=16
\]
의 중심은 원점이고 반지름은 $4$이다.

연립방정식이 두 쌍의 해를 갖는다는 것은 직선과 원이 서로 다른 두 점에서 만난다는 뜻이므로, 원점에서 직선까지의 거리가 $4$보다 작아야 한다.

거리 $d$는
\[
d=\frac{|{-2k}|}{\sqrt{(\sqrt{3})^2+(-1)^2}}
\]
\[
=\frac{2|k|}{2}=|k|
\]
이다.

따라서
\[
|k|<4
\]
이므로 가능한 정수 $k$는
\[
-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3
\]
의 $7$개이다.

따라서 정답은 ①이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-003",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (40, 1770, 870, 2290)),
        source_label="3",
        level=3,
        question=r"""삼차방정식
\[
x^3-3x^2-3x+2=0
\]
의 세 근을 $\alpha$, $\beta$, $\gamma$라고 할 때,
\[
(3+\alpha)(3+\beta)(3+\gamma)
\]
의 값은?""",
        choices=r"""① $43$
② $44$
③ $45$
④ $46$
⑤ $47$""",
        answer="①",
        solution=r"""다항식
\[
f(x)=x^3-3x^2-3x+2
\]
라 두면
\[
f(x)=(x-\alpha)(x-\beta)(x-\gamma)
\]
이다.

따라서
\[
f(-3)=(-3-\alpha)(-3-\beta)(-3-\gamma)
\]
\[
=-(3+\alpha)(3+\beta)(3+\gamma)
\]
이다.

이때
\[
f(-3)=(-3)^3-3(-3)^2-3(-3)+2=-27-27+9+2=-43
\]
이므로
\[
(3+\alpha)(3+\beta)(3+\gamma)=43
\]
이다.

따라서 정답은 ①이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-004",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (930, 60, 1790, 560)),
        source_label="4",
        level=3,
        question=r"""세 변의 길이가 각각 $x-1$, $x$, $x+1$인 삼각형이 둔각삼각형이 되도록 하는 자연수 $x$의 값은?""",
        choices=r"""① $1$
② $2$
③ $3$
④ $4$
⑤ $5$""",
        answer="③",
        solution=r"""삼각형이 되려면
\[
(x-1)+x>x+1
\]
이어야 하므로
\[
x>2
\]
이다.

가장 긴 변은 $x+1$이므로 둔각삼각형이 되기 위한 조건은
\[
(x+1)^2>x^2+(x-1)^2
\]
이다.

이를 정리하면
\[
x^2+2x+1>2x^2-2x+1
\]
\[
x^2-4x<0
\]
\[
0<x<4
\]
이다.

자연수 조건 $x>2$와 함께 보면
\[
x=3
\]
만 가능하다.

따라서 정답은 ③이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-005",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (930, 900, 1790, 1360)),
        source_label="5",
        level=4,
        question=r"""부등식
\[
|x-3|+|x+1|<x+5
\]
를 만족시키는 정수 $x$의 개수는?""",
        choices=r"""① $4$
② $5$
③ $6$
④ $7$
⑤ $8$""",
        answer="④",
        solution=r"""절댓값의 기준점은 $x=-1$, $x=3$이다.

\[
\text{(1) }x<-1
\]
이면
\[
|x-3|+|x+1|=(3-x)+(-x-1)=2-2x
\]
이므로
\[
2-2x<x+5
\]
\[
x>-1
\]
이 되어 모순이다.

\[
\text{(2) }-1\le x\le 3
\]
이면
\[
|x-3|+|x+1|=(3-x)+(x+1)=4
\]
이므로
\[
4<x+5
\]
\[
x>-1
\]
이다.

따라서 이 구간에서 가능한 정수는
\[
0,\ 1,\ 2,\ 3
\]
이다.

\[
\text{(3) }x>3
\]
이면
\[
|x-3|+|x+1|=(x-3)+(x+1)=2x-2
\]
이므로
\[
2x-2<x+5
\]
\[
x<7
\]
이다.

따라서 이 구간에서 가능한 정수는
\[
4,\ 5,\ 6
\]
이다.

전체 개수는
\[
4+3=7
\]
이므로 정답은 ④이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-006",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (930, 1720, 1790, 2200)),
        source_label="6",
        level=3,
        question=r"""부등식
\[
(x-2)(x-3)\le a
\]
의 해가
\[
1\le x\le b
\]
일 때, 실수 $a$, $b$에 대하여 $a+b$의 값은?""",
        choices=r"""① $2$
② $3$
③ $4$
④ $5$
⑤ $6$""",
        answer="⑤",
        solution=r"""해의 구간이
\[
1\le x\le b
\]
이므로 $x=1$은 경계점이다.

따라서
\[
a=(1-2)(1-3)=2
\]
이다.

이 값을 원래 부등식에 대입하면
\[
(x-2)(x-3)\le 2
\]
\[
x^2-5x+4\le 0
\]
\[
(x-1)(x-4)\le 0
\]
이므로
\[
1\le x\le 4
\]
이다.

따라서
\[
b=4
\]
이므로
\[
a+b=2+4=6
\]
이다.

따라서 정답은 ⑤이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-007",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_CPX,
        crop=CropSpec(1, (40, 80, 870, 620)),
        source_label="7",
        level=3,
        question=r"""이차방정식
\[
x^2-kx-k=0
\]
은 실근을 갖고, 이차방정식
\[
x^2-2kx-5k+6=0
\]
은 허근을 갖도록 하는 정수 $k$의 최솟값은?""",
        choices=r"""① $-6$
② $-5$
③ $-4$
④ $-3$
⑤ $-2$""",
        answer="②",
        solution=r"""첫 번째 이차방정식이 실근을 가지려면 판별식이
\[
\Delta_1=(-k)^2-4\cdot 1\cdot (-k)=k^2+4k
\]
이므로
\[
k(k+4)\ge 0
\]
이어야 한다.

따라서
\[
k\le -4 \quad \text{또는} \quad k\ge 0
\]
이다.

두 번째 이차방정식이 허근을 가지려면 판별식이 음수여야 하므로
\[
\Delta_2=(-2k)^2-4\cdot 1\cdot (-5k+6)<0
\]
\[
4k^2+20k-24<0
\]
\[
k^2+5k-6<0
\]
\[
(k+6)(k-1)<0
\]
이므로
\[
-6<k<1
\]
이다.

두 조건을 함께 만족하는 정수는
\[
-5,\ -4,\ 0
\]
이므로 최솟값은
\[
-5
\]
이다.

따라서 정답은 ②이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-008",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (40, 910, 870, 1460)),
        source_label="8",
        level=3,
        question=r"""두 점 $A(3,-1)$, $B(a,2)$ 사이의 거리가 $3\sqrt{5}$가 되도록 하는 모든 $a$의 값의 곱은?""",
        choices=r"""① $-30$
② $-29$
③ $-28$
④ $-27$
⑤ $-26$""",
        answer="④",
        solution=r"""두 점 사이의 거리 공식에 의하여
\[
\sqrt{(a-3)^2+\{2-(-1)\}^2}=3\sqrt{5}
\]
이다.

양변을 제곱하면
\[
(a-3)^2+9=45
\]
\[
(a-3)^2=36
\]
이므로
\[
a-3=\pm 6
\]
이다.

따라서
\[
a=9 \quad \text{또는} \quad a=-3
\]
이므로 그 곱은
\[
9\cdot (-3)=-27
\]
이다.

따라서 정답은 ④이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-009",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (40, 1650, 870, 2440)),
        source_label="9",
        level=4,
        question=r"""$0<t<1$일 때, 두 점 $A(-3,-5)$, $B(1,7)$을 잇는 선분 $\overline{AB}$를 $t:(1-t)$로 내분하는 점이 $x$축에 있다. 이때,
\[
t=\frac{p}{q}
\]
라 할 때, $p+q$의 값은? (단, $p$, $q$는 서로소인 자연수)""",
        choices=r"""① $7$
② $9$
③ $13$
④ $15$
⑤ $17$""",
        answer="⑤",
        solution=r"""점 $P$가 선분 $\overline{AB}$를 $t:(1-t)$로 내분하면 $P$의 $y$좌표는
\[
-5(1-t)+7t
\]
이다.

점 $P$가 $x$축 위에 있으므로 $y$좌표가 $0$이어서
\[
-5(1-t)+7t=0
\]
이다.

이를 정리하면
\[
-5+12t=0
\]
\[
t=\frac{5}{12}
\]
이다.

따라서
\[
p=5,\qquad q=12
\]
이므로
\[
p+q=17
\]
이다.

따라서 정답은 ⑤이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-010",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (930, 80, 1790, 650)),
        source_label="10",
        level=3,
        question=r"""세 점 $A(6,-3)$, $B(a,9)$, $C(-2,b)$를 꼭짓점으로 하는 삼각형 $ABC$의 무게중심이 원점이다. 이때, 실수 $a$, $b$에 대하여 $ab$의 값은?""",
        choices=r"""① $21$
② $22$
③ $23$
④ $24$
⑤ $25$""",
        answer="④",
        solution=r"""삼각형의 무게중심의 좌표는 세 꼭짓점 좌표의 평균이다.

무게중심이 원점이므로
\[
\frac{6+a-2}{3}=0,\qquad \frac{-3+9+b}{3}=0
\]
이다.

따라서
\[
a+4=0,\qquad b+6=0
\]
이므로
\[
a=-4,\qquad b=-6
\]
이다.

따라서
\[
ab=(-4)(-6)=24
\]
이므로 정답은 ④이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-011",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (930, 930, 1790, 1510)),
        source_label="11",
        level=3,
        question=r"""세 점 $A(-1,-1)$, $B(1,a)$, $C(-a,-5)$가 한 직선 위에 있다. 이때, 양수 $a$의 값은?""",
        choices=r"""① $1$
② $2$
③ $3$
④ $4$
⑤ $5$""",
        answer="③",
        solution=r"""세 점이 한 직선 위에 있으므로 직선 $AB$의 기울기와 직선 $AC$의 기울기가 같다.

\[
\text{직선 }AB\text{의 기울기}=\frac{a-(-1)}{1-(-1)}=\frac{a+1}{2}
\]

\[
\text{직선 }AC\text{의 기울기}=\frac{-5-(-1)}{-a-(-1)}=\frac{-4}{1-a}=\frac{4}{a-1}
\]

따라서
\[
\frac{a+1}{2}=\frac{4}{a-1}
\]
이다.

양변을 정리하면
\[
(a+1)(a-1)=8
\]
\[
a^2-1=8
\]
\[
a^2=9
\]
이므로
\[
a=\pm 3
\]
이다.

이때 양수 $a$는
\[
3
\]
이므로 정답은 ③이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-012",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (930, 1720, 1790, 2350)),
        source_label="12",
        level=2,
        question=r"""두 점 $(1,0)$, $(0,-2)$를 지나는 직선이 점 $(a,a+3)$을 지날 때, $a$의 값은?""",
        choices=r"""① $1$
② $2$
③ $3$
④ $4$
⑤ $5$""",
        answer="⑤",
        solution=r"""두 점 $(1,0)$, $(0,-2)$를 지나는 직선의 기울기는
\[
\frac{0-(-2)}{1-0}=2
\]
이다.

따라서 직선의 방정식은
\[
y=2x-2
\]
이다.

점 $(a,a+3)$이 이 직선 위에 있으므로
\[
a+3=2a-2
\]
이다.

따라서
\[
a=5
\]
이므로 정답은 ⑤이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-013",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (40, 80, 870, 750)),
        source_label="13",
        level=3,
        question=r"""직선
\[
ax+y-2=0
\]
이 직선
\[
x+2y+5=0
\]
에 수직이고, 직선
\[
2x+(3+b)y=0
\]
과 평행할 때, 상수 $a$, $b$에 대하여 $a+b$의 값은?""",
        choices=r"""① $-6$
② $-5$
③ $-4$
④ $-3$
⑤ $-2$""",
        answer="①",
        solution=r"""직선
\[
x+2y+5=0
\]
의 기울기는
\[
-\frac{1}{2}
\]
이다.

이에 수직인 직선의 기울기는
\[
2
\]
이다.

한편 직선
\[
ax+y-2=0
\]
은
\[
y=-ax+2
\]
이므로 기울기는
\[
-a
\]
이다.

따라서
\[
-a=2
\]
이므로
\[
a=-2
\]
이다.

또 직선
\[
2x+(3+b)y=0
\]
은
\[
y=-\frac{2}{3+b}x
\]
이므로 기울기는
\[
-\frac{2}{3+b}
\]
이다.

이 직선이 기울기 $2$인 직선과 평행하므로
\[
-\frac{2}{3+b}=2
\]
이다.

따라서
\[
3+b=-1,\qquad b=-4
\]
이므로
\[
a+b=-2+(-4)=-6
\]
이다.

따라서 정답은 ①이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-014",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (40, 930, 870, 1570)),
        source_label="14",
        level=4,
        question=r"""세 직선
\[
3x-y-2=0,\qquad x-y+2=0,\qquad mx+2y-12=0
\]
이 삼각형을 이루지 않도록 하는 양수 $m$의 값은?""",
        choices=r"""① $1$
② $2$
③ $3$
④ $4$
⑤ $5$""",
        answer="②",
        solution=r"""세 직선이 삼각형을 이루지 않으려면 세 직선이 한 점에서 만나거나, 두 직선이 서로 평행해야 한다.

직선
\[
3x-y-2=0,\qquad x-y+2=0
\]
의 교점을 구하면
\[
y=3x-2,\qquad y=x+2
\]
이므로
\[
3x-2=x+2
\]
\[
x=2,\qquad y=4
\]
이다.

세 직선이 한 점에서 만나려면 점 $(2,4)$가
\[
mx+2y-12=0
\]
위에 있어야 하므로
\[
2m+2\cdot 4-12=0
\]
\[
2m-4=0
\]
\[
m=2
\]
이다.

또 세 번째 직선의 기울기는
\[
-\frac{m}{2}
\]
이고, 앞의 두 직선의 기울기는 각각 $3$, $1$이다.

\[
-\frac{m}{2}=3 \quad \text{또는} \quad -\frac{m}{2}=1
\]
을 만족하는 양수 $m$은 없다.

따라서 양수 $m$의 값은
\[
2
\]
이므로 정답은 ②이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-015",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (40, 1720, 870, 2390)),
        source_label="15",
        level=3,
        question=r"""직선
\[
x-2y=0
\]
에 수직이고 점 $(1,1)$과의 거리가 $\sqrt{5}$인 모든 직선의 $y$절편의 합은?""",
        choices=r"""① $-6$
② $-3$
③ $0$
④ $3$
⑤ $6$""",
        answer="⑤",
        solution=r"""직선
\[
x-2y=0
\]
은
\[
y=\frac{1}{2}x
\]
이므로 기울기는
\[
\frac{1}{2}
\]
이다.

이에 수직인 직선의 기울기는
\[
-2
\]
이므로 모든 직선은
\[
y=-2x+n
\]
의 꼴로 놓을 수 있다.

이를 일반형으로 쓰면
\[
2x+y-n=0
\]
이다.

점 $(1,1)$에서 이 직선까지의 거리가 $\sqrt{5}$이므로
\[
\frac{|2\cdot 1+1-n|}{\sqrt{2^2+1^2}}=\sqrt{5}
\]
이다.

따라서
\[
\frac{|3-n|}{\sqrt{5}}=\sqrt{5}
\]
\[
|3-n|=5
\]
이므로
\[
n=-2 \quad \text{또는} \quad n=8
\]
이다.

$y$절편의 합은
\[
-2+8=6
\]
이므로 정답은 ⑤이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-101",
        subject="COM1",
        qtype="서답형",
        unit_triplet=COM1_CPX,
        crop=CropSpec(3, (0, 0, 920, 980)),
        source_label="서답1",
        level=4,
        question=r"""방정식
\[
x^3-1=0
\]
의 한 허근을 $w$라고 할 때,
\[
(\overline{w}^{\,2}+7\overline{w}+3)(w^2+4w+2)
\]
의 값을 구하시오. (단, $\overline{w}$는 $w$의 켤레복소수이다.)""",
        choices="",
        answer="14",
        solution=r"""$w$는
\[
x^3-1=0
\]
의 허근이므로
\[
w^3=1,\qquad w\ne 1
\]
이다.

따라서
\[
w^2+w+1=0
\]
이고, 또
\[
\overline{w}=w^2
\]
이다.

주어진 식의 첫 번째 괄호는
\[
\overline{w}^{\,2}+7\overline{w}+3=w+7w^2+3
\]
이고, 두 번째 괄호는
\[
w^2+4w+2
\]
이다.

\[
w^2=-w-1
\]
을 이용하면
\[
w+7w^2+3=w+7(-w-1)+3=-6w-4
\]
\[
w^2+4w+2=(-w-1)+4w+2=3w+1
\]
이다.

따라서 주어진 값은
\[
(-6w-4)(3w+1)
\]
\[
=-18w^2-18w-4
\]
이다.

여기서 다시
\[
w^2=-w-1
\]
을 대입하면
\[
-18(-w-1)-18w-4=18w+18-18w-4=14
\]
이다.

따라서 구하는 값은
\[
14
\]
이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-102",
        subject="COM1",
        qtype="서답형",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(3, (0, 1250, 920, 2060)),
        source_label="서답2",
        level=4,
        warning="JJ-2023-G1-S1-Final-102: PDF 정답표에는 110으로 표기되어 있으나 계산상 정답은 10임",
        question=r"""[정답표 오류: PDF 정답표에는 $110$으로 적혀 있으나, 문제 조건으로 계산한 정답은 $10$이다.]

연립부등식
\[
\begin{cases}
x^2-6x+5>0 \\
x^2-(2+a)x+2a<0
\end{cases}
\]
의 정수인 해가 $2$개다. 이때, 실수 $a$의 최댓값을 $M$, 최솟값을 $m$이라고 할 때, $M-m$의 값을 구하여라.""",
        choices="",
        answer="10",
        solution=r"""첫 번째 부등식은
\[
x^2-6x+5=(x-1)(x-5)
\]
이므로
\[
x<1 \quad \text{또는} \quad x>5
\]
이다.

두 번째 부등식은
\[
x^2-(2+a)x+2a=(x-2)(x-a)
\]
이므로
\[
(x-2)(x-a)<0
\]
의 해는 $x$가 $2$와 $a$ 사이에 있을 때이다.

\[
\text{(1) }a<2
\]
이면 두 번째 부등식의 해는
\[
a<x<2
\]
이다.

이 구간에서 첫 번째 부등식을 함께 만족하는 정수는 $1$보다 작은 정수뿐이므로, 정수해가 정확히 $2$개가 되려면 그 해가
\[
-1,\ 0
\]
뿐이어야 한다.

따라서
\[
-2\le a<-1
\]
이다.

\[
\text{(2) }a>2
\]
이면 두 번째 부등식의 해는
\[
2<x<a
\]
이다.

이 구간에서 첫 번째 부등식을 함께 만족하는 정수는 $5$보다 큰 정수뿐이므로, 정수해가 정확히 $2$개가 되려면 그 해가
\[
6,\ 7
\]
뿐이어야 한다.

따라서
\[
7<a\le 8
\]
이다.

결국 가능한 $a$의 범위는
\[
-2\le a<-1 \quad \text{또는} \quad 7<a\le 8
\]
이므로
\[
m=-2,\qquad M=8
\]
이다.

따라서
\[
M-m=8-(-2)=10
\]
이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-103",
        subject="COM2",
        qtype="서답형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(3, (900, 0, 1820, 1120)),
        source_label="서답3",
        level=4,
        question=r"""선분 $\overline{AB}$를 $3:2$로 내분하는 점의 좌표가 $(8,-2)$, 외분하는 점의 좌표가 $(2,6)$이다. 이때, 두 점 $A$, $B$ 사이의 거리를
\[
\overline{AB}=\frac{p}{q}
\]
라 할 때, $p+q$의 값을 구하시오. (단, $p$, $q$는 서로소인 자연수이다.)""",
        choices="",
        answer="31",
        solution=r"""두 점의 좌표를
\[
A(x_1,y_1),\qquad B(x_2,y_2)
\]
라 두자.

점 $(8,-2)$가 선분 $\overline{AB}$를 $3:2$로 내분하므로 내분점 공식에 의하여
\[
\left(\frac{2x_1+3x_2}{5},\frac{2y_1+3y_2}{5}\right)=(8,-2)
\]
이다.

따라서
\[
2x_1+3x_2=40,\qquad 2y_1+3y_2=-10
\]
이다.

또 점 $(2,6)$이 $\overline{AB}$를 $3:2$로 외분하므로 외분점 공식에 의하여
\[
(-2x_1+3x_2,\ -2y_1+3y_2)=(2,6)
\]
이다.

따라서
\[
-2x_1+3x_2=2,\qquad -2y_1+3y_2=6
\]
이다.

두 식을 각각 풀면
\[
x_1=\frac{19}{2},\qquad x_2=7,\qquad y_1=-4,\qquad y_2=-\frac{2}{3}
\]
이다.

그러므로
\[
\overline{AB}
=\sqrt{\left(\frac{19}{2}-7\right)^2+\left(-4+\frac{2}{3}\right)^2}
\]
\[
=\sqrt{\left(\frac{5}{2}\right)^2+\left(\frac{10}{3}\right)^2}
\]
\[
=\sqrt{\frac{25}{4}+\frac{100}{9}}
=\sqrt{\frac{625}{36}}
=\frac{25}{6}
\]
이다.

따라서
\[
p=25,\qquad q=6
\]
이므로
\[
p+q=31
\]
이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-104",
        subject="COM1",
        qtype="서술형",
        unit_triplet=COM1_CPX,
        crop=CropSpec(4, (0, 0, 920, 980)),
        source_label="서술4",
        level=5,
        question=r"""※ 풀이과정 및 정답을 쓰시오. (정답만 쓰면 $0$점)

방정식
\[
(x^2+3x+2)(x^2+7x+12)=15
\]
의 두 실근을 $\alpha$, $\beta$, 두 허근을 $\gamma$, $\delta$라 할 때,
\[
\frac{\gamma\delta}{\alpha\beta}
\]
의 값을 구하시오.""",
        choices="",
        answer="9",
        solution=r"""식을 한쪽으로 모으면
\[
(x^2+3x+2)(x^2+7x+12)-15=0
\]
이다.

전개하면
\[
x^4+10x^3+35x^2+50x+9=0
\]
이다.

이 식을
\[
(x^2+5x+a)(x^2+5x+b)=0
\]
의 꼴로 놓으면
\[
a+b=10,\qquad ab=9
\]
이어야 하므로
\[
a=1,\qquad b=9
\]
이다.

따라서
\[
(x^2+5x+1)(x^2+5x+9)=0
\]
이다.

이제
\[
x^2+5x+1=0
\]
의 두 실근을 $\alpha$, $\beta$라 하고,
\[
x^2+5x+9=0
\]
의 두 허근을 $\gamma$, $\delta$라 보면, 근과 계수의 관계에 의하여
\[
\alpha\beta=1,\qquad \gamma\delta=9
\]
이다.

그러므로
\[
\frac{\gamma\delta}{\alpha\beta}=\frac{9}{1}=9
\]
이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-105",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(4, (0, 1200, 920, 2080)),
        source_label="서술5",
        level=4,
        question=r"""※ 풀이과정 및 정답을 쓰시오. (정답만 쓰면 $0$점)

두 점 $A(1,4)$, $B(6,1)$와 $y$축 위의 점 $P$, $x$축 위의 점 $Q$에 대하여
\[
\overline{AP}^2+\overline{PQ}^2+\overline{BQ}^2
\]
의 최솟값을 구하시오.""",
        choices="",
        answer="28",
        solution=r"""점 $P$를
\[
P=(0,p)
\]
라 하고, 점 $Q$를
\[
Q=(q,0)
\]
라 두자.

그러면
\[
\overline{AP}^2=(1-0)^2+(4-p)^2=1+(p-4)^2
\]
\[
\overline{PQ}^2=q^2+p^2
\]
\[
\overline{BQ}^2=(6-q)^2+(1-0)^2=(6-q)^2+1
\]
이다.

따라서
\[
\overline{AP}^2+\overline{PQ}^2+\overline{BQ}^2
\]
\[
=1+(p-4)^2+p^2+q^2+(6-q)^2+1
\]
\[
=2p^2-8p+2q^2-12q+54
\]
이다.

이를 완전제곱식으로 정리하면
\[
2(p^2-4p)+2(q^2-6q)+54
\]
\[
=2\{(p-2)^2-4\}+2\{(q-3)^2-9\}+54
\]
\[
=2(p-2)^2+2(q-3)^2+28
\]
이다.

따라서 최솟값은
\[
28
\]
이다.""",
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-Final-106",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(4, (900, 0, 1820, 1220)),
        source_label="서술6",
        level=5,
        question=r"""※ 풀이과정 및 정답을 쓰시오. (정답만 쓰면 $0$점)

두 직선
\[
2x-3y+3=0,\qquad x+2y-5=0
\]
의 교점과 $(1,1)$를 지나는 직선
\[
ax+by-2=0
\]
이 있다. 이때, 상수 $a$, $b$에 대하여
\[
a^2+b^2
\]
의 값을 구하시오.

(힌트: 기울기가 다른 두 직선
\[
ax+by+c=0,\qquad px+qy+r=0
\]
에 대하여
\[
(ax+by+c)+k(px+qy+r)=0
\]
은 실수 $k$의 값에 관계없이 일정한 한 점을 지나는 직선이다.)""",
        choices="",
        answer="10",
        solution=r"""두 직선
\[
2x-3y+3=0,\qquad x+2y-5=0
\]
의 교점을 지나는 직선은
\[
(2x-3y+3)+k(x+2y-5)=0
\]
의 꼴로 나타낼 수 있다.

이를 정리하면
\[
(2+k)x+(-3+2k)y+(3-5k)=0
\]
이다.

이 직선이 점 $(1,1)$을 지나므로
\[
(2+k)\cdot 1+(-3+2k)\cdot 1+(3-5k)=0
\]
이다.

이를 계산하면
\[
2-2k=0
\]
이므로
\[
k=1
\]
이다.

따라서 구하는 직선은
\[
(2x-3y+3)+(x+2y-5)=0
\]
\[
3x-y-2=0
\]
이다.

그러므로
\[
a=3,\qquad b=-1
\]
이므로
\[
a^2+b^2=3^2+(-1)^2=10
\]
이다.""",
    ),
)


def _source_meta(pid: str) -> Tuple[int, int, str]:
    number = int(pid.rsplit("-", 1)[-1])
    if number >= FIXED_META["subjective_offset"]:
        return number, number - FIXED_META["subjective_offset"], "subjective"
    return number, number, "objective"


def _front_matter(row: ProblemData, original_asset_name: str) -> Dict[str, object]:
    _, source_no, source_kind = _source_meta(row.pid)
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(*row.unit_triplet)
    return {
        "id": row.pid,
        "school": FIXED_META["school"],
        "year": FIXED_META["year"],
        "grade": FIXED_META["grade"],
        "semester": FIXED_META["semester"],
        "exam": FIXED_META["exam"],
        "subject": row.subject,
        "type": row.qtype,
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": row.source_label,
        "difficulty": row.level,
        "level": row.level,
        "unit": f"{unit_l1}>{unit_l2}>{unit_l3}",
        "unit_l1": unit_l1,
        "unit_l2": unit_l2,
        "unit_l3": unit_l3,
        "source": FIXED_META["source"],
        "tags": [
            "수동생성",
            "PDF",
            row.qtype,
            f"출제번호-{row.source_label}",
            f"과목-{row.subject}",
            f"생성일-{FIXED_META['created_on']}",
        ],
        "assets": [f"assets/original/{original_asset_name}"],
    }


def _pdf_rect(crop: CropSpec) -> fitz.Rect:
    left, top, right, bottom = crop.box
    return fitz.Rect(
        left / RENDER_SCALE,
        top / RENDER_SCALE,
        right / RENDER_SCALE,
        bottom / RENDER_SCALE,
    )


def _render_crop(doc: fitz.Document, crop: CropSpec, out_path: Path) -> None:
    page = doc[crop.page]
    rect = _pdf_rect(crop=crop)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
    image = Image.open(BytesIO(pix.tobytes("png")))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def _write_problem(row: ProblemData, doc: fitz.Document, results: List[str], review_paths: List[str]) -> None:
    folder = PROBLEMS / row.pid
    folder.mkdir(parents=True, exist_ok=False)

    assets_original = folder / "assets" / "original"
    assets_original.mkdir(parents=True, exist_ok=True)

    original_asset_name = f"{row.pid}_original.png"
    _render_crop(doc, row.crop, assets_original / original_asset_name)

    front = _front_matter(row=row, original_asset_name=original_asset_name)
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{row.question.strip()}\n\n"
        f"## Choices\n{row.choices.strip()}\n\n"
        f"## Answer\n{row.answer.strip()}\n\n"
        f"## Solution\n{row.solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")

    results.append(f"{row.pid} | created | {original_asset_name}")
    review_paths.append(str(folder / "problem.md"))


def main() -> int:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(SOURCE_PDF)

    doc = fitz.open(SOURCE_PDF)
    results: List[str] = []
    review_paths: List[str] = []
    duplicates: List[str] = []
    warnings: List[str] = []
    ocr_uncertain: List[str] = []

    try:
        for row in DATA:
            folder = PROBLEMS / row.pid
            if folder.exists():
                duplicates.append(row.pid)
                results.append(f"{row.pid} | skipped | duplicate-folder")
                continue

            _write_problem(row=row, doc=doc, results=results, review_paths=review_paths)
            if row.warning:
                warnings.append(row.warning)
            if row.ocr_uncertain:
                ocr_uncertain.append(f"{row.pid}: OCR 또는 수식 재검토 필요")
    finally:
        doc.close()

    created = sum(1 for line in results if "| created |" in line)
    skipped = sum(1 for line in results if "| skipped |" in line)
    report_lines: List[str] = [
        f"created={created} updated=0 skipped={skipped} warnings={len(warnings)}",
        "",
        "[FILES]",
        *results,
        "",
        "[DUPLICATE_FOLDERS]",
        *(duplicates or ["none"]),
        "",
        "[OCR_OR_FORMULA_UNCERTAIN]",
        *(ocr_uncertain or ["none"]),
        "",
        "[WARNINGS]",
        *(warnings or ["none"]),
        "",
        "[REVIEW_PATHS]",
        *(review_paths or ["none"]),
    ]
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(REPORT_PATH)
    print("\n".join(report_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
