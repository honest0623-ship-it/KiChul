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

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet


PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "JE.2023.G1.S1.Final.COM1.pdf"
REPORT_PATH = ROOT / "_tmp_je_2023_g1_s1_final_report.txt"

FIXED_META = {
    "school": "JE",
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "Final",
    "source": "user_upload_2026-03-08",
    "subjective_offset": 100,
    "created_on": "2026-03-08",
}

RENDER_SCALE = 2.5

COM1_REM = ("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리")
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
    rotate_180: bool = False


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
    level_hint: Optional[int] = None
    ocr_uncertain: bool = False


DATA: Sequence[ProblemData] = (
    ProblemData(
        pid="JE-2023-G1-S1-Final-001",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (40, 300, 850, 820)),
        source_label="1",
        question=r"""부등식 $|x-2|<3$을 만족시키는 정수 $x$의 개수는?""",
        choices=r"""① $2$
② $3$
③ $4$
④ $5$
⑤ $6$""",
        answer="④",
        solution=r"""절댓값의 성질에 의하여
$$
-3<x-2<3
$$
이다.

양변에 $2$를 더하면
$$
-1<x<5
$$
이다.

이를 만족시키는 정수는
$$
0,\ 1,\ 2,\ 3,\ 4
$$
이므로 그 개수는 $5$이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-002",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(0, (40, 760, 850, 1240)),
        source_label="2",
        question=r"""수직선 위의 두 점 $A(0)$, $B(3)$가 있다. 선분 $\overline{AB}$의 $2:1$ 내분점 $P$와 외분점 $Q$에 대하여 $\overline{PQ}$의 길이는?""",
        choices=r"""① $1$
② $2$
③ $3$
④ $4$
⑤ $5$""",
        answer="④",
        solution=r"""점 $P$가 선분 $\overline{AB}$를 $2:1$로 내분하므로
$$
AP:PB=2:1
$$
이다.

따라서
$$
P=\frac{1\cdot 0+2\cdot 3}{2+1}=2
$$
이다.

또 점 $Q$가 $\overline{AB}$를 $2:1$로 외분하므로
$$
AQ:QB=2:1
$$
이고,
$$
Q=\frac{2\cdot 3-1\cdot 0}{2-1}=6
$$
이다.

따라서
$$
\overline{PQ}=|6-2|=4
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-003",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (40, 1180, 850, 1640)),
        source_label="3",
        question=r"""방정식 $x^4+x^3+5x^2-x-6=0$의 모든 실근의 곱은?""",
        choices=r"""① $6$
② $1$
③ $0$
④ $-1$
⑤ $-6$""",
        answer="④",
        solution=r"""$x=1$을 대입하면
$$
1+1+5-1-6=0
$$
이므로 $x-1$은 인수이다.

따라서
$$
x^4+x^3+5x^2-x-6=(x-1)(x^3+2x^2+7x+6)
$$
이다.

또 $x=-1$을 대입하면
$$
-1+2-7+6=0
$$
이므로 $x+1$도 인수이다.

따라서
$$
x^4+x^3+5x^2-x-6=(x-1)(x+1)(x^2+x+6)
$$
이다.

$x^2+x+6=0$의 판별식은
$$
1-24<0
$$
이므로 실근을 가지지 않는다.

따라서 모든 실근은 $1$, $-1$이고, 그 곱은
$$
-1
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-004",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (40, 1600, 850, 2360)),
        source_label="4",
        question=r"""한 개에 $1500$원인 아이스크림과 한 개에 $1000$원인 음료를 합하여 모두 $18$개를 사려고 한다. 총 금액은 $25000$원을 넘길 수 없다고 할 때, 살 수 있는 최대의 아이스크림 개수는?""",
        choices=r"""① $12$
② $13$
③ $14$
④ $15$
⑤ $16$""",
        answer="③",
        solution=r"""아이스크림의 개수를 $x$개라 하면 음료의 개수는
$$
18-x
$$
개이다.

총 금액은
$$
1500x+1000(18-x)
$$
원이므로
$$
1500x+1000(18-x)\le 25000
$$
이다.

정리하면
$$
18000+500x\le 25000
$$
$$
500x\le 7000
$$
$$
x\le 14
$$
이다.

따라서 살 수 있는 아이스크림의 최대 개수는 $14$개이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-005",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(0, (920, 260, 1790, 880)),
        source_label="5",
        question=r"""세 점 $A(3,2)$, $B(6,1)$, $C(3,6)$을 꼭짓점으로 하는 삼각형 $ABC$와 합동인 삼각형 $DEF$가 다음 조건을 만족시킨다. 점 $F$의 좌표를 $(a,b)$라고 할 때, $45ab$의 값은?

<div style="border:1px solid #333; padding:12px; margin:12px 0;">
<p style="margin:0 0 8px 0; text-align:center;"><strong>&lt;조건&gt;</strong></p>
<p style="margin:0 0 6px 0;">a. 삼각형 $DEF$의 무게중심은 원점이다.</p>
<p style="margin:0;">b. 점 $D$는 $x$축 위에 있고, 점 $F$는 제3사분면 위에 있다.</p>
</div>""",
        choices=r"""① $140$
② $150$
③ $160$
④ $170$
⑤ $180$""",
        answer="⑤",
        solution=r"""삼각형 $ABC$의 무게중심을 $G$라 하면
$$
G\left(\frac{3+6+3}{3},\frac{2+1+6}{3}\right)=(4,3)
$$
이다.

따라서
$$
GA=\sqrt{(3-4)^2+(2-3)^2}=\sqrt{2}
$$
$$
GC=\sqrt{(3-4)^2+(6-3)^2}=\sqrt{10}
$$
이다.

삼각형 $DEF$는 삼각형 $ABC$와 합동이고 그 무게중심이 원점이므로, 원점에서 점 $D$, $F$까지의 거리는 각각
$$
\sqrt{2},\ \sqrt{10}
$$
이다.

또
$$
\overline{FD}=\overline{CA}=4
$$
이다.

점 $D$가 $x$축 위에 있으므로
$$
D=(\pm \sqrt{2},0)
$$
이다.

점 $F=(a,b)$라 하면
$$
a^2+b^2=10
$$
이고,
$$
(a-\sqrt{2})^2+b^2=16
$$
이다.

두 식을 빼면
$$
-2\sqrt{2}a+2=6
$$
$$
a=-\sqrt{2}
$$
이다.

따라서
$$
b^2=10-2=8
$$
이고, 점 $F$는 제3사분면 위에 있으므로
$$
b=-2\sqrt{2}
$$
이다.

그러므로
$$
45ab=45\cdot (-\sqrt{2})\cdot (-2\sqrt{2})=180
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-006",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (920, 840, 1790, 1360)),
        source_label="6",
        question=r"""등식 $|x-2|+|x+4|<8-x$를 만족시키는 모든 정수 $x$의 값의 합은?""",
        choices=r"""① $-44$
② $-42$
③ $-35$
④ $-27$
⑤ $-14$""",
        answer="①",
        solution=r"""절댓값의 기준점은 $x=-4$, $x=2$이므로 경우를 나눈다.

1. $x<-4$일 때
$$
|x-2|+|x+4|=-(x-2)-(x+4)=-2x-2
$$
이므로
$$
-2x-2<8-x
$$
$$
x>-10
$$
이다.

따라서
$$
-10<x<-4
$$
이다.

2. $-4\le x<2$일 때
$$
|x-2|+|x+4|=-(x-2)+(x+4)=6
$$
이므로
$$
6<8-x
$$
$$
x<2
$$
이다.

따라서 이 구간에서는 항상 성립한다.

3. $x\ge 2$일 때
$$
|x-2|+|x+4|=(x-2)+(x+4)=2x+2
$$
이므로
$$
2x+2<8-x
$$
$$
3x<6
$$
$$
x<2
$$
가 되어 성립하지 않는다.

따라서 정수해는
$$
-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1
$$
이고, 그 합은
$$
-44
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-007",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(0, (920, 1320, 1790, 2360)),
        source_label="7",
        question=r"""두 직선
$$
l_1:(a-1)x-y+a+3=0,\qquad l_2:3x+ay+2a-9=0
$$
에 대하여 <보기>에서 옳은 것을 고른 것은?

<div style="border:1px solid #333; padding:12px; margin:12px 0;">
<p style="margin:0 0 8px 0; text-align:center;"><strong>&lt;보기&gt;</strong></p>
<p style="margin:0 0 6px 0;">ㄱ. $a=\frac32$일 때, 두 직선 $l_1$과 $l_2$는 서로 수직이다.</p>
<p style="margin:0 0 6px 0;">ㄴ. 두 직선 $l_1$과 $l_2$가 평행이 되기 위한 $a$의 값이 존재한다.</p>
<p style="margin:0;">ㄷ. 직선 $l_2$는 $a$의 값에 관계없이 항상 점 $(3,-2)$를 지난다.</p>
</div>""",
        choices=r"""① ㄱ
② ㄱ, ㄷ
③ ㄴ
④ ㄴ, ㄷ
⑤ ㄱ, ㄴ, ㄷ""",
        answer="②",
        solution=r"""직선 $l_1$은
$$
y=(a-1)x+a+3
$$
이므로 기울기는
$$
a-1
$$
이다.

직선 $l_2$는 $a\ne 0$일 때
$$
y=-\frac{3}{a}x-\frac{2a-9}{a}
$$
이므로 기울기는
$$
-\frac{3}{a}
$$
이다.

ㄱ. $a=\frac32$이면
$$
m_1=\frac12,\qquad m_2=-2
$$
이므로
$$
m_1m_2=-1
$$
이다. 따라서 서로 수직이다.

ㄴ. 두 직선이 평행하려면
$$
a-1=-\frac{3}{a}
$$
이어야 한다.

정리하면
$$
a^2-a+3=0
$$
인데, 이 방정식의 판별식은
$$
1-12<0
$$
이므로 실수해가 없다.

또 $a=0$이면 $l_2$는 $x=3$인 직선이고, $l_1$은 기울기가 $-1$인 직선이므로 평행하지 않다.

따라서 ㄴ은 거짓이다.

ㄷ. 점 $(3,-2)$를 $l_2$에 대입하면
$$
3\cdot 3+a(-2)+2a-9=9-2a+2a-9=0
$$
이므로 항상 성립한다.

따라서 옳은 것은 ㄱ, ㄷ이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-008",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_CPX,
        crop=CropSpec(1, (40, 200, 850, 860)),
        source_label="8",
        question=r"""연립방정식
$$
\begin{cases}
y=6x-17\\
x^2-y=8
\end{cases}
$$
의 해를 $x=\alpha$, $y=\beta$라고 할 때, $\alpha+7\beta$의 최댓값은?""",
        choices=r"""① $-2$
② $-1$
③ $0$
④ $7$
⑤ $10$""",
        answer="⑤",
        solution=r"""첫째 식의 $y$를 둘째 식에 대입하면
$$
x^2-(6x-17)=8
$$
$$
x^2-6x+9=0
$$
$$
(x-3)^2=0
$$
이다.

따라서
$$
\alpha=3
$$
이고,
$$
\beta=6\cdot 3-17=1
$$
이다.

그러므로
$$
\alpha+7\beta=3+7\cdot 1=10
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-009",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(1, (40, 820, 850, 1360)),
        source_label="9",
        question=r"""연립부등식
$$
\begin{cases}
|x|+|x-2|<8\\
x^2-5x+4>0
\end{cases}
$$
를 만족하는 정수 $x$의 개수는?""",
        choices=r"""① $2$
② $3$
③ $4$
④ $5$
⑤ $6$""",
        answer="②",
        solution=r"""먼저
$$
|x|+|x-2|<8
$$
을 푼다.

1. $x<0$일 때
$$
-x+(2-x)<8
$$
$$
-2x<6
$$
$$
x>-3
$$
이므로
$$
-3<x<0
$$
이다.

2. $0\le x<2$일 때
$$
x+(2-x)=2<8
$$
이므로 항상 성립한다.

3. $x\ge 2$일 때
$$
x+(x-2)<8
$$
$$
2x<10
$$
$$
x<5
$$
이므로
$$
2\le x<5
$$
이다.

따라서 첫째 부등식의 해는
$$
-3<x<5
$$
이다.

다음으로
$$
x^2-5x+4>0
$$
은
$$
(x-1)(x-4)>0
$$
이므로
$$
x<1 \quad \text{또는} \quad x>4
$$
이다.

두 조건을 함께 만족하는 범위는
$$
-3<x<1
$$
또는
$$
4<x<5
$$
이다.

따라서 정수해는
$$
-2,\ -1,\ 0
$$
의 $3$개이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-010",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (40, 1320, 850, 1780)),
        source_label="10",
        question=r"""두 점 $(-1,-2)$, $(2,-8)$을 지나는 직선의 방정식을 $y=ax+b$라 할 때, 상수 $a$, $b$의 곱 $ab$의 값은?""",
        choices=r"""① $4$
② $5$
③ $6$
④ $7$
⑤ $8$""",
        answer="⑤",
        solution=r"""직선의 기울기는
$$
a=\frac{-8-(-2)}{2-(-1)}=\frac{-6}{3}=-2
$$
이다.

따라서 직선의 방정식은
$$
y=-2x+b
$$
이다.

점 $(-1,-2)$를 대입하면
$$
-2=2+b
$$
$$
b=-4
$$
이다.

그러므로
$$
ab=(-2)(-4)=8
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-011",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (40, 1750, 850, 2360)),
        source_label="11",
        question=r"""좌표평면 위의 두 직선 $2x+ay=1$, $2bx+y=1$이 서로 수직일 때, $\dfrac{a}{a-b}$의 값은? (단, $ab\ne 0$이다.)""",
        choices=r"""① $\frac{6}{5}$
② $\frac{4}{5}$
③ $0$
④ $1$
⑤ $-\frac{6}{5}$""",
        answer="②",
        solution=r"""두 직선의 기울기는 각각
$$
-\frac{2}{a},\quad -2b
$$
이다.

서로 수직이므로
$$
\left(-\frac{2}{a}\right)(-2b)=-1
$$
이다.

따라서
$$
\frac{4b}{a}=-1
$$
$$
a=-4b
$$
이다.

그러므로
$$
\frac{a}{a-b}=\frac{-4b}{-4b-b}=\frac{4}{5}
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-012",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (920, 200, 1790, 760)),
        source_label="12",
        question=r"""점 $(1,2)$를 지나고 직선 $x-2y-3=0$에 수직인 직선의 $y$절편은?""",
        choices=r"""① $4$
② $2$
③ $0$
④ $-2$
⑤ $-4$""",
        answer="①",
        solution=r"""직선 $x-2y-3=0$을 기울기절편형으로 나타내면
$$
y=\frac12x-\frac32
$$
이므로 기울기는
$$
\frac12
$$
이다.

이에 수직인 직선의 기울기는
$$
-2
$$
이다.

점 $(1,2)$를 지나므로
$$
y-2=-2(x-1)
$$
$$
y=-2x+4
$$
이다.

따라서 $y$절편은 $4$이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-013",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (920, 720, 1790, 1630)),
        source_label="13",
        question=r"""세 점 $A(-1,1)$, $B(4,2)$, $C(2,-3)$을 꼭짓점으로 하는 삼각형 $ABC$가 있을 때, $y$축과 평행한 직선의 방정식은 $x=k$이고, 삼각형 $ABC$의 넓이를 이등분할 때,
$$
(k+1)^2=\frac{q}{p}
$$
이다. 이때, $q-p$의 값은? (단, $p$와 $q$는 서로소인 자연수이다.)""",
        choices=r"""① $12$
② $13$
③ $14$
④ $15$
⑤ $16$""",
        answer="②",
        solution=r"""직선 $x=k$가 변 $\overline{AB}$, $\overline{AC}$와 만나는 점을 각각 $P$, $Q$라 하자.

직선 $\overline{AB}$의 방정식은
$$
y=\frac{x+6}{5}
$$
이고, 직선 $\overline{AC}$의 방정식은
$$
y=\frac{-4x-1}{3}
$$
이다.

따라서 점 $P$, $Q$의 좌표는
$$
P\left(k,\frac{k+6}{5}\right),\qquad Q\left(k,\frac{-4k-1}{3}\right)
$$
이다.

그러므로
$$
PQ=\frac{k+6}{5}-\frac{-4k-1}{3}=\frac{23(k+1)}{15}
$$
이다.

삼각형 $APQ$의 높이는 직선 $x=k$까지의 거리이므로
$$
k-(-1)=k+1
$$
이다.

따라서 삼각형 $APQ$의 넓이는
$$
\frac12\cdot \frac{23(k+1)}{15}\cdot (k+1)=\frac{23(k+1)^2}{30}
$$
이다.

삼각형 $ABC$의 넓이는
$$
\frac12\left|(-1)(2-(-3))+4((-3)-1)+2(1-2)\right|=\frac{23}{2}
$$
이므로 이를 이등분한 넓이는
$$
\frac{23}{4}
$$
이다.

따라서
$$
\frac{23(k+1)^2}{30}=\frac{23}{4}
$$
이므로
$$
(k+1)^2=\frac{15}{2}
$$
이다.

즉
$$
\frac{q}{p}=\frac{15}{2}
$$
이므로
$$
q-p=15-2=13
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-014",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(1, (920, 1560, 1790, 2360)),
        source_label="14",
        question=r"""$16\%$의 소금물 $200\text{ g}$이 있다. 이 소금물에 소금을 더 넣어 $25\%$ 이상 $30\%$ 이하의 소금물을 만들려고 할 때, 더 넣어야 하는 소금의 양의 최댓값과 최솟값의 차는?""",
        choices=r"""① $16$
② $18$
③ $20$
④ $22$
⑤ $24$""",
        answer="①",
        solution=r"""처음 들어 있는 소금의 양은
$$
200\times \frac{16}{100}=32\text{ g}
$$
이다.

더 넣는 소금의 양을 $x\text{ g}$라 하면 소금물의 농도는
$$
\frac{32+x}{200+x}
$$
이다.

조건에 의하여
$$
\frac{25}{100}\le \frac{32+x}{200+x}\le \frac{30}{100}
$$
이다.

먼저
$$
\frac{32+x}{200+x}\ge \frac14
$$
이면
$$
4(32+x)\ge 200+x
$$
$$
3x\ge 72
$$
$$
x\ge 24
$$
이다.

또
$$
\frac{32+x}{200+x}\le \frac{3}{10}
$$
이면
$$
10(32+x)\le 3(200+x)
$$
$$
320+10x\le 600+3x
$$
$$
7x\le 280
$$
$$
x\le 40
$$
이다.

따라서 더 넣어야 하는 소금의 양의 최솟값은 $24\text{ g}$, 최댓값은 $40\text{ g}$이므로 그 차는
$$
40-24=16
$$
이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-015",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(2, (40, 180, 850, 900)),
        source_label="15",
        question=r"""세 점 $A(3,1)$, $B(5,-2)$, $C(6,3)$을 꼭짓점으로 하는 삼각형 $ABC$는 어떤 삼각형인지 고르면?""",
        choices=r"""① 정삼각형
② $\angle B=90^\circ$인 직각삼각형
③ $\overline{AB}=\overline{AC}$인 직각 이등변삼각형
④ $\overline{AB}=\overline{BC}$인 이등변삼각형
⑤ 둔각삼각형""",
        answer="③",
        solution=r"""세 변의 길이의 제곱을 구하면
$$
\overline{AB}^2=(5-3)^2+(-2-1)^2=4+9=13
$$
$$
\overline{AC}^2=(6-3)^2+(3-1)^2=9+4=13
$$
$$
\overline{BC}^2=(6-5)^2+(3-(-2))^2=1+25=26
$$
이다.

따라서
$$
\overline{AB}=\overline{AC}
$$
이고,
$$
\overline{AB}^2+\overline{AC}^2=\overline{BC}^2
$$
이므로 $\angle A=90^\circ$이다.

따라서 삼각형 $ABC$는 직각 이등변삼각형이다.""",
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-016",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (40, 860, 850, 1700)),
        source_label="16",
        question=r"""직선 $l:(1+2k)x+(2-k)y+5=0$이 실수 $k$의 값과 관계없이 항상 지나는 점을 $A$라 한다. 점 $B(-2,1)$에서 직선 $l$에 내린 수선의 발을 $H$라고 하고, $\overline{AH}=2\sqrt{2}$가 되도록 하는 모든 실수 $k$의 값의 곱은?""",
        choices=r"""① $-1$
② $-\frac13$
③ $0$
④ $\frac13$
⑤ $1$""",
        answer="⑤",
        solution=r"""주어진 직선을 정리하면
$$
x+2y+5+k(2x-y)=0
$$
이다.

직선이 항상 지나는 점 $A(x,y)$는 모든 $k$에 대하여 이 식을 만족해야 하므로
$$
\begin{cases}
x+2y+5=0\\
2x-y=0
\end{cases}
$$
를 만족한다.

따라서
$$
A(-1,-2)
$$
이다.

이제
$$
\overline{AB}=\sqrt{(-2+1)^2+(1+2)^2}=\sqrt{10}
$$
이다.

삼각형 $ABH$는 점 $H$에서 직각이므로
$$
\overline{BH}^2=\overline{AB}^2-\overline{AH}^2=10-8=2
$$
이다.

즉 점 $B$와 직선 $l$ 사이의 거리는
$$
\sqrt{2}
$$
이다.

따라서
$$
\frac{|(1+2k)(-2)+(2-k)\cdot 1+5|}{\sqrt{(1+2k)^2+(2-k)^2}}=\sqrt{2}
$$
이다.

정리하면
$$
\frac{|5-5k|}{\sqrt{5+5k^2}}=\sqrt{2}
$$
$$
\frac{5|1-k|}{\sqrt{5}\sqrt{1+k^2}}=\sqrt{2}
$$
이다.

양변을 제곱하면
$$
25(1-k)^2=10(1+k^2)
$$
$$
15k^2-50k+15=0
$$
$$
3k^2-10k+3=0
$$
이다.

따라서
$$
(3k-1)(k-3)=0
$$
이므로
$$
k=\frac13,\ 3
$$
이다.

그러므로 모든 실수 $k$의 값의 곱은
$$
\frac13\cdot 3=1
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-101",
        subject="COM1",
        qtype="단답형",
        unit_triplet=COM1_REM,
        crop=CropSpec(2, (40, 1680, 850, 2450)),
        source_label="서답1번",
        question=r"""$x^3$의 계수가 $1$인 삼차식 $f(x)$가 $f(0)=25$, $f(1)=f(2)=f(3)=a$를 만족시킬 때, 실수 $a$의 값을 구하시오. (단, $a\ne 0$)""",
        choices="",
        answer="$31$",
        solution=r"""식
$$
g(x)=f(x)-a
$$
를 생각하자.

$f(1)=f(2)=f(3)=a$이므로
$$
g(1)=g(2)=g(3)=0
$$
이다.

또 $f(x)$는 $x^3$의 계수가 $1$인 삼차식이므로 $g(x)$도 최고차항의 계수가 $1$인 삼차식이다.

따라서
$$
g(x)=(x-1)(x-2)(x-3)
$$
이다.

즉
$$
f(x)=(x-1)(x-2)(x-3)+a
$$
이다.

$x=0$을 대입하면
$$
25=f(0)=(-1)(-2)(-3)+a=-6+a
$$
이므로
$$
a=31
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-102",
        subject="COM2",
        qtype="단답형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (920, 140, 1790, 1180)),
        source_label="서답2번",
        question=r"""세 점 $D(3k+1,5)$, $E(3,6)$, $F(-1,8)$이 한 직선 위에 있을 때, 상수 $k$값을 구하시오.""",
        choices="",
        answer=r"$\frac{4}{3}$",
        solution=r"""세 점이 한 직선 위에 있으므로 기울기가 서로 같다.

먼저
$$
\text{기울기 }EF=\frac{8-6}{-1-3}=\frac{2}{-4}=-\frac12
$$
이다.

또
$$
\text{기울기 }DE=\frac{6-5}{3-(3k+1)}=\frac{1}{2-3k}
$$
이다.

따라서
$$
\frac{1}{2-3k}=-\frac12
$$
이므로
$$
2=-(2-3k)
$$
$$
2=-2+3k
$$
$$
k=\frac43
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-103",
        subject="COM1",
        qtype="서술형",
        unit_triplet=COM1_CPX,
        crop=CropSpec(2, (920, 1120, 1790, 2380)),
        source_label="서답3번",
        question=r"""이차방정식 $x^2-2x+4=0$의 한 허근을 $\omega$라 할 때, 다음 물음에 답하시오.

(1) $\omega^3$의 값을 구하시오.

(2) $\omega^2-2\omega$의 값을 구하시오.

(3) $\dfrac{-4}{\omega^3-\omega^2+2\omega}$의 값을 구하시오.""",
        choices="",
        answer=r"""(1) $-8$

(2) $-4$

(3) $1$""",
        solution=r"""$\omega$는 이차방정식
$$
x^2-2x+4=0
$$
의 근이므로
$$
\omega^2-2\omega+4=0
$$
즉
$$
\omega^2=2\omega-4
$$
이다.

(1)
$$
\omega^3=\omega\cdot \omega^2=\omega(2\omega-4)=2\omega^2-4\omega
$$
이고,
$$
2\omega^2-4\omega=2(2\omega-4)-4\omega=-8
$$
이므로
$$
\omega^3=-8
$$
이다.

(2)
$$
\omega^2-2\omega=(2\omega-4)-2\omega=-4
$$
이다.

(3)
$$
\omega^3-\omega^2+2\omega=-8-(2\omega-4)+2\omega=-4
$$
이므로
$$
\frac{-4}{\omega^3-\omega^2+2\omega}=\frac{-4}{-4}=1
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-104",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(3, (40, 120, 850, 1510), rotate_180=True),
        source_label="서술형4",
        question=r"""점 $A(x_1,y_1)$, $B(x_2,y_2)$, $C(x_3,y_3)$에 대하여 삼각형 $ABC$의 세 변 $\overline{AB}$, $\overline{BC}$, $\overline{CA}$의 중점이 각각 $D(3,3)$, $E(2,4)$, $F(1,2)$이다. 다음 물음에 답하시오.

(1) 삼각형 $ABC$의 무게중심의 좌표와 점 $A$, $B$, $C$의 좌표를 구하시오.

(2) 점 $(4,9)$과 직선 $\overline{AB}$의 방정식과 사이의 거리를 구하시오.

(3) 선분 $\overline{AB}$를 $3:2$로 내분하는 점 $P$와 선분 $\overline{BC}$를 $5:1$로 외분하는 점 $Q$를 구하시오.""",
        choices="",
        answer=r"""(1) 무게중심 $(2,3)$, $A(2,1)$, $B(4,5)$, $C(0,3)$

(2) $\dfrac{4\sqrt{5}}{5}$

(3) $P\left(\dfrac{16}{5},\dfrac{17}{5}\right)$, $Q\left(-1,\dfrac{5}{2}\right)$""",
        solution=r"""중점의 성질에 의하여
$$
\begin{cases}
\dfrac{x_1+x_2}{2}=3,\quad \dfrac{y_1+y_2}{2}=3\\
\dfrac{x_2+x_3}{2}=2,\quad \dfrac{y_2+y_3}{2}=4\\
\dfrac{x_3+x_1}{2}=1,\quad \dfrac{y_3+y_1}{2}=2
\end{cases}
$$
이다.

따라서
$$
\begin{cases}
x_1+x_2=6\\
x_2+x_3=4\\
x_3+x_1=2
\end{cases}
\qquad
\begin{cases}
y_1+y_2=6\\
y_2+y_3=8\\
y_3+y_1=4
\end{cases}
$$
이다.

이를 풀면
$$
A(2,1),\quad B(4,5),\quad C(0,3)
$$
이다.

따라서 무게중심은
$$
\left(\frac{2+4+0}{3},\frac{1+5+3}{3}\right)=(2,3)
$$
이다.

(2) 직선 $\overline{AB}$의 기울기는
$$
\frac{5-1}{4-2}=2
$$
이므로 방정식은
$$
y-1=2(x-2)
$$
즉
$$
2x-y-3=0
$$
이다.

따라서 점 $(4,9)$와 이 직선 사이의 거리는
$$
\frac{|2\cdot 4-9-3|}{\sqrt{2^2+(-1)^2}}=\frac{4}{\sqrt{5}}=\frac{4\sqrt{5}}{5}
$$
이다.

(3) 선분 $\overline{AB}$를 $3:2$로 내분하는 점 $P$는
$$
P\left(\frac{2\cdot 2+3\cdot 4}{3+2},\frac{2\cdot 1+3\cdot 5}{3+2}\right)=\left(\frac{16}{5},\frac{17}{5}\right)
$$
이다.

또 선분 $\overline{BC}$를 $5:1$로 외분하는 점 $Q$는
$$
Q\left(\frac{5\cdot 0-1\cdot 4}{5-1},\frac{5\cdot 3-1\cdot 5}{5-1}\right)=\left(-1,\frac{5}{2}\right)
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-105",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(3, (40, 1490, 850, 2460), rotate_180=True),
        source_label="서술형5",
        question=r"""두 점 $A(1,0)$, $B(3,4)$과 $y$축 위의 점 $P$에 대하여 $\overline{AP}^2+\overline{BP}^2$가 최소가 되도록 하는 점 $P$의 좌표를 구하시오.""",
        choices="",
        answer=r"$\left(0,2\right)$",
        solution=r"""점 $P$를
$$
P(0,b)
$$
라 하자.

그러면
$$
\overline{AP}^2=(0-1)^2+(b-0)^2=1+b^2
$$
이고,
$$
\overline{BP}^2=(0-3)^2+(b-4)^2=9+(b-4)^2
$$
이다.

따라서
$$
\overline{AP}^2+\overline{BP}^2=1+b^2+9+(b-4)^2
$$
$$
=2b^2-8b+26
$$
$$
=2(b-2)^2+18
$$
이다.

이 값이 최소가 되려면
$$
b=2
$$
이어야 하므로
$$
P=(0,2)
$$
이다.""",
        level_hint=4,
    ),
    ProblemData(
        pid="JE-2023-G1-S1-Final-106",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(3, (920, 120, 1790, 2460), rotate_180=True),
        source_label="서술형6",
        question=r"""두 직선 $x-2y-1=0$, $2x-y-5=0$의 교점을 지나는 직선 중에서 원점에서 거리가 $1$인 서로 다른 두 직선 $l_1$, $l_2$가 있다. 두 직선 $l_1$, $l_2$와 $y$축에 둘러싸인 삼각형의 넓이를 $\dfrac{P}{q}$라 할 때, $\dfrac{P}{3q}$를 구하시오.""",
        choices="",
        answer=r"$\frac{9}{8}$",
        solution=r"""두 직선
$$
x-2y-1=0,\qquad 2x-y-5=0
$$
의 교점을 구하면
$$
\begin{cases}
x-2y=1\\
2x-y=5
\end{cases}
$$
이므로
$$
(x,y)=(3,1)
$$
이다.

따라서 이 점을 지나는 직선의 방정식을
$$
y-1=m(x-3)
$$
라 하자.

이를 일반형으로 쓰면
$$
mx-y-3m+1=0
$$
이다.

원점에서 이 직선까지의 거리가 $1$이므로
$$
\frac{|1-3m|}{\sqrt{m^2+1}}=1
$$
이다.

양변을 제곱하면
$$
(1-3m)^2=m^2+1
$$
$$
8m^2-6m=0
$$
$$
2m(4m-3)=0
$$
이다.

따라서
$$
m=0,\qquad m=\frac34
$$
이다.

즉
$$
l_1:y=1,\qquad l_2:y=\frac34x-\frac54
$$
이다.

이 두 직선과 $y$축이 둘러싸는 삼각형의 꼭짓점은
$$
(0,1),\ (0,-\frac54),\ (3,1)
$$
이다.

따라서 그 넓이는
$$
\frac12\cdot \left(1-\left(-\frac54\right)\right)\cdot 3
$$
$$
=\frac12\cdot \frac94\cdot 3=\frac{27}{8}
$$
이다.

즉
$$
\frac{P}{q}=\frac{27}{8}
$$
이므로
$$
\frac{P}{3q}=\frac{27}{24}=\frac98
$$
이다.""",
        level_hint=4,
        ocr_uncertain=True,
    ),
)


def _source_meta(pid: str) -> Tuple[int, int, str]:
    number = int(pid.rsplit("-", 1)[-1])
    if number >= FIXED_META["subjective_offset"]:
        return number, number - FIXED_META["subjective_offset"], "subjective"
    return number, number, "objective"


def _level_for(row: ProblemData) -> int:
    number, _, _ = _source_meta(row.pid)
    result = classify_unit_and_level(
        question_text=row.question,
        choices_text=row.choices,
        answer_text=row.answer,
        solution_text=row.solution,
        qtype=row.qtype,
        grade=FIXED_META["grade"],
        problem_no=number,
    )
    level = int(result.level)
    if row.qtype in {"서술형", "단답형"} and level < 4:
        level = 4
    if row.level_hint is not None:
        level = max(level, row.level_hint)
    return max(1, min(5, level))


def _front_matter(row: ProblemData, original_asset_name: str) -> Dict[str, object]:
    _, source_no, source_kind = _source_meta(row.pid)
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(*row.unit_triplet)
    level = _level_for(row)
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
        "difficulty": level,
        "level": level,
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


def _pdf_rect(page: fitz.Page, crop: CropSpec) -> fitz.Rect:
    left, top, right, bottom = crop.box
    if not crop.rotate_180:
        return fitz.Rect(
            left / RENDER_SCALE,
            top / RENDER_SCALE,
            right / RENDER_SCALE,
            bottom / RENDER_SCALE,
        )

    width = page.rect.width
    height = page.rect.height
    return fitz.Rect(
        width - right / RENDER_SCALE,
        height - bottom / RENDER_SCALE,
        width - left / RENDER_SCALE,
        height - top / RENDER_SCALE,
    )


def _render_crop(doc: fitz.Document, crop: CropSpec, out_path: Path) -> None:
    page = doc[crop.page]
    rect = _pdf_rect(page=page, crop=crop)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
    image = Image.open(BytesIO(pix.tobytes("png")))
    if crop.rotate_180:
        image = image.rotate(180, expand=True)
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
    ocr_uncertain: List[str] = []

    try:
        for row in DATA:
            folder = PROBLEMS / row.pid
            if folder.exists():
                duplicates.append(row.pid)
                results.append(f"{row.pid} | skipped | duplicate-folder")
                continue

            _write_problem(row=row, doc=doc, results=results, review_paths=review_paths)
            if row.ocr_uncertain:
                ocr_uncertain.append(f"{row.pid}: 문장 일부를 스캔 판독 후 수동 복원")
    finally:
        doc.close()

    created = sum(1 for row in results if "| created |" in row)
    skipped = sum(1 for row in results if "| skipped |" in row)
    report_lines: List[str] = [
        f"created={created} updated=0 skipped={skipped} warnings=0",
        "",
        "[FILES]",
        *results,
        "",
        "[DUPLICATE_FOLDERS]",
        *(duplicates or ["none"]),
        "",
        "[OCR_UNCERTAIN]",
        *(ocr_uncertain or ["none"]),
        "",
        "[WARNINGS]",
        "none",
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
