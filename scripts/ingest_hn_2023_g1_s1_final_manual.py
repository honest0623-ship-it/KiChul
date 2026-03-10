from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import shutil
import sys

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet


PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "HN.2023.G1.S1.Final.COM1.pdf"
SCAN_106 = ORIGINAL / "HN.2023.G1.S1.Final.COM1.서답6번.png"
REPORT_PATH = ROOT / "_tmp_hn_2023_g1_s1_final_report.txt"

FIXED_META = {
    "school": "HN",
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "Final",
    "source": "user_upload_2026-03-08",
    "subjective_offset": 100,
    "created_on": "2026-03-08",
}

COM1_DA = ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산")
COM1_REM = ("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리")
COM1_FACT = ("공통수학1(2022개정)", "1. 다항식", "1-3. 인수분해")
COM1_CPX = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식")
COM1_QF = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수")
COM1_EQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식")
COM1_INEQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식")
COM2_COORD = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-1. 평면좌표")
COM2_LINE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식")
COM2_CIRCLE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식")


@dataclass(frozen=True)
class CropSpec:
    page: int
    rect: Tuple[float, float, float, float]


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
    scan_source: Optional[Path] = None


DATA: Sequence[ProblemData] = (
    ProblemData(
        pid="HN-2023-G1-S1-Final-001",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (10, 180, 360, 430)),
        source_label="1",
        question=r"""방정식 $x^3-7x^2+ax+15=0$의 한 근이 $-1$일 때, 나머지 두 근의 곱을 구하면?""",
        choices=r"""① $-5$
② $5$
③ $10$
④ $15$
⑤ $20$""",
        answer="④",
        solution=r"""$-1$을 주어진 방정식의 근으로 대입하면
$$
(-1)^3-7(-1)^2-a+15=0
$$
$$
-1-7-a+15=0
$$
$$
a=7
$$
이다.

세 근을 $-1$, $\alpha$, $\beta$라 하면 근과 계수의 관계에 의하여
$$
(-1)\alpha\beta=-15
$$
이므로
$$
\alpha\beta=15
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-002",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (10, 430, 360, 700)),
        source_label="2",
        question=r"""방정식 $x^3-x^2-kx+k=0$이 한 개의 실근과 두 개의 허근을 가질 때, 정수 $k$의 최댓값은?""",
        choices=r"""① $-2$
② $-1$
③ $0$
④ $1$
⑤ $2$""",
        answer="②",
        solution=r"""좌변을 인수분해하면
$$
x^3-x^2-kx+k=x^2(x-1)-k(x-1)=(x-1)(x^2-k)
$$
이다.

따라서 한 실근은 항상 $x=1$이고, 나머지 두 근은
$$
x^2-k=0
$$
의 근이다.

나머지 두 근이 허근이 되려면
$$
k<0
$$
이어야 한다.

정수 $k$ 중 최댓값은 $-1$이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-003",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_CPX,
        crop=CropSpec(0, (10, 695, 360, 995)),
        source_label="3",
        question=r"""방정식 $x^3+1=0$의 한 허근을 $w$라고 할 때,
$$
\overline{w}^3+2w^3+3w^2+5w+\overline{w}=aw+b
$$
이다. 실수 $a$, $b$에 대하여 $a+b$의 값은?

(단, $\overline{w}$는 $w$의 켤레복소수이다.)""",
        choices=r"""① $2$
② $4$
③ $6$
④ $8$
⑤ $10$""",
        answer="①",
        solution=r"""$w$는 $x^3+1=0$의 허근이므로
$$
w^3=-1,\qquad w^2-w+1=0
$$
이다.

따라서
$$
w^2=w-1
$$
이고, 켤레복소수의 성질에 의하여
$$
\overline{w}=1-w,\qquad \overline{w}^3=-1
$$
이다.

이를 식에 대입하면
$$
\overline{w}^3+2w^3+3w^2+5w+\overline{w}
$$
$$
=-1+2(-1)+3(w-1)+5w+(1-w)
$$
$$
=7w-5
$$
이므로
$$
a=7,\qquad b=-5
$$
이다.

따라서
$$
a+b=2
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-004",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(0, (365, 45, 718, 360)),
        source_label="4",
        question=r"""연립방정식
$$
\begin{cases}
x+2y=k\\
x^2+y^2=9
\end{cases}
$$
가 오직 한 쌍의 해를 갖도록 하는 양수 $k$의 값은?""",
        choices=r"""① $\sqrt{5}$
② $2\sqrt{5}$
③ $3\sqrt{5}$
④ $4\sqrt{5}$
⑤ $5\sqrt{5}$""",
        answer="③",
        solution=r"""$x^2+y^2=9$는 중심이 원점이고 반지름의 길이가 $3$인 원의 방정식이다.

직선 $x+2y=k$와 이 원이 오직 한 점에서 만나려면 직선이 원에 접해야 하므로, 원의 중심 $(0,0)$에서 직선까지의 거리가 반지름과 같아야 한다.
$$
\frac{|k|}{\sqrt{1^2+2^2}}=3
$$
$$
\frac{|k|}{\sqrt{5}}=3
$$
$$
|k|=3\sqrt{5}
$$
이다.

$k$가 양수이므로
$$
k=3\sqrt{5}
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-005",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (365, 370, 718, 670)),
        source_label="5",
        question=r"""부등식 $|x+1|+|x-1|<6$을 만족시키는 정수 $x$의 개수는?""",
        choices=r"""① $4$
② $5$
③ $6$
④ $7$
⑤ $8$""",
        answer="②",
        solution=r"""$x$의 범위를 나누어 생각한다.

1. $x\ge 1$일 때
$$
|x+1|+|x-1|=(x+1)+(x-1)=2x
$$
이므로
$$
2x<6 \Rightarrow x<3
$$
이다. 따라서 정수 $x$는 $1$, $2$이다.

2. $-1\le x<1$일 때
$$
|x+1|+|x-1|=(x+1)+(1-x)=2
$$
이므로 항상 성립한다. 따라서 정수 $x$는 $0$이다.

3. $x<-1$일 때
$$
|x+1|+|x-1|=-(x+1)-(x-1)=-2x
$$
이므로
$$
-2x<6 \Rightarrow x>-3
$$
이다. 따라서 정수 $x$는 $-2$, $-1$이다.

따라서 조건을 만족시키는 정수는
$$
-2,\ -1,\ 0,\ 1,\ 2
$$
의 $5$개이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-006",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (365, 670, 718, 995)),
        source_label="6",
        question=r"""모든 실수 $x$에 대하여 부등식 $-x^2+1<x^2+2x+a\le 3x^2+5$가 성립하도록 하는 실수 $a$의 값의 최댓값은?""",
        choices=r"""① $\frac{5}{2}$
② $3$
③ $\frac{7}{2}$
④ $4$
⑤ $\frac{9}{2}$""",
        answer="⑤",
        solution=r"""주어진 부등식이 모든 실수 $x$에 대하여 성립해야 하므로 두 조건을 각각 만족해야 한다.

1. $-x^2+1<x^2+2x+a$
$$
2x^2+2x+a-1>0
$$
이다.

좌변을 완전제곱식으로 정리하면
$$
2x^2+2x+a-1=2\left(x+\frac12\right)^2+a-\frac32
$$
이므로 모든 실수 $x$에 대하여 양수가 되려면
$$
a-\frac32>0
$$
$$
a>\frac32
$$
이다.

2. $x^2+2x+a\le 3x^2+5$
$$
2x^2-2x+5-a\ge 0
$$
이다.

좌변을 완전제곱식으로 정리하면
$$
2x^2-2x+5-a=2\left(x-\frac12\right)^2+\frac92-a
$$
이므로 모든 실수 $x$에 대하여 $0$ 이상이 되려면
$$
\frac92-a\ge 0
$$
$$
a\le \frac92
$$
이다.

따라서 $a$의 최댓값은
$$
\frac92
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-007",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(1, (10, 45, 360, 370)),
        source_label="7",
        question=r"""연립부등식
$$
\begin{cases}
x^2-4>0\\
(2x-9)(x-k)<0
\end{cases}
$$
을 만족시키는 정수 $x$가 $2$개일 때, 정수 $k$의 개수는?""",
        choices=r"""① $3$
② $4$
③ $5$
④ $6$
⑤ $7$""",
        answer="⑤",
        solution=r"""$x^2-4>0$이므로
$$
x<-2 \quad \text{또는} \quad x>2
$$
이다.

또
$$
(2x-9)(x-k)<0
$$
이므로 $x$는 두 근 $k$, $\frac92$ 사이에 있어야 한다.

정수 $k$에 따라 경우를 나눈다.

1. $k\le 4$일 때는
$$
k<x<\frac92
$$
이다. 이 구간에서 $x^2-4>0$까지 만족하는 정수해가 $2$개가 되려면
$$
k=-3,-2,-1,0,1,2
$$
여야 한다.

2. $k\ge 5$일 때는
$$
\frac92<x<k
$$
이다. 이 구간의 정수는 $5,6,\dots,k-1$이므로 개수는 $k-5$개이다.

정수해가 $2$개가 되려면
$$
k-5=2
$$
이어서
$$
k=7
$$
이다.

따라서 가능한 정수 $k$는
$$
-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 7
$$
의 $7$개이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-008",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (10, 375, 360, 670)),
        source_label="8",
        question=r"""두 점 $A(4,1)$, $B(6,3)$에서 같은 거리에 있고 $y$축 위에 있는 점 $Q$의 좌표를 $(0,b)$라 할 때, $b$의 값은?""",
        choices=r"""① $4$
② $5$
③ $6$
④ $7$
⑤ $8$""",
        answer="④",
        solution=r"""좌표평면에서 점 $Q(0,b)$가 두 점 $A$, $B$에서 같은 거리에 있으므로
$$
AQ^2=BQ^2
$$
이다.

따라서
$$
(0-4)^2+(b-1)^2=(0-6)^2+(b-3)^2
$$
$$
16+(b-1)^2=36+(b-3)^2
$$
이다.

전개하면
$$
16+b^2-2b+1=36+b^2-6b+9
$$
$$
17-2b=45-6b
$$
$$
4b=28
$$
$$
b=7
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-009",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (10, 675, 360, 995)),
        source_label="9",
        question=r"""세 점 $A(2,1)$, $B(4,5)$, $C(4,0)$을 꼭짓점으로 하는 삼각형 $ABC$에서 $\angle A$의 이등분선과 변 $BC$가 만나는 점 $D$의 좌표를 $(a,b)$라 할 때, $ab$의 값은?""",
        choices=r"""① $\frac{16}{3}$
② $6$
③ $\frac{20}{3}$
④ $\frac{22}{3}$
⑤ $8$""",
        answer="③",
        solution=r"""$\angle A$의 이등분선이므로 각의 이등분선의 정리에 의하여
$$
BD:DC=AB:AC
$$
이다.

먼저 두 변의 길이를 구하면
$$
AB=\sqrt{(4-2)^2+(5-1)^2}=\sqrt{20}=2\sqrt{5}
$$
$$
AC=\sqrt{(4-2)^2+(0-1)^2}=\sqrt{5}
$$
이므로
$$
BD:DC=2:1
$$
이다.

점 $D$는 선분 $BC$를 $2:1$로 내분하므로
$$
D\left(4,\frac{1\cdot 5+2\cdot 0}{2+1}\right)=\left(4,\frac53\right)
$$
이다.

따라서
$$
ab=4\cdot \frac53=\frac{20}{3}
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-010",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (365, 45, 718, 360)),
        source_label="10",
        question=r"""삼각형 $ABC$에서 변 $AB$를 $1:2$로 내분하는 점을 $D$, 변 $BC$를 $1:2$로 외분하는 점을 $E$, 변 $CA$를 $3:2$로 외분하는 점을 $F$라 하자. 삼각형 $ADC$의 넓이가 $\frac12$일 때, 삼각형 $FEC$의 넓이는?""",
        choices=r"""① $\frac{9}{2}$
② $6$
③ $\frac{15}{2}$
④ $9$
⑤ $\frac{21}{2}$""",
        answer="④",
        solution=r"""$D$는 변 $AB$를 $1:2$로 내분하므로
$$
AD:DB=1:2
$$
이다.

삼각형 $ADC$와 삼각형 $ABC$는 꼭짓점 $C$에서 같은 높이를 가지므로
$$
[ADC]:[ABC]=AD:AB=1:3
$$
이다.

$[ADC]=\frac12$이므로
$$
[ABC]=\frac32
$$
이다.

$E$는 변 $BC$를 $1:2$로 외분하므로 $BE:EC=1:2$이고 점의 배열은 $E-B-C$이다. 따라서
$$
EC=2BC
$$
이다.

또 $F$는 변 $CA$를 $3:2$로 외분하므로 $CF:FA=3:2$이고 점의 배열은 $C-A-F$이다. 따라서
$$
CF=3CA
$$
이다.

삼각형 $CEF$와 삼각형 $CBA$는 끼인각 $\angle ECF=\angle BCA$가 같으므로
$$
[CEF]=\frac{EC}{BC}\cdot \frac{CF}{CA}\cdot [CBA]
$$
$$
=2\cdot 3\cdot [ABC]
$$
$$
=6\cdot \frac32=9
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-011",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (365, 365, 718, 670)),
        source_label="11",
        question=r"""세 직선 $x+3y=0$, $x-y-4=0$, $mx+2y+1=0$이 삼각형을 이루지 않도록 하는 상수 $m$의 값을 모두 더하면?""",
        choices=r"""① $-\frac{5}{3}$
② $-\frac{4}{3}$
③ $-1$
④ $-\frac{2}{3}$
⑤ $-\frac{1}{3}$""",
        answer="③",
        solution=r"""세 직선이 삼각형을 이루지 않으려면
1. 서로 평행한 두 직선이 있거나
2. 세 직선이 한 점에서 만나야 한다.

먼저 기울기를 구하면
$$
x+3y=0 \Rightarrow y=-\frac13x,\qquad x-y-4=0 \Rightarrow y=x-4,\qquad mx+2y+1=0 \Rightarrow y=-\frac{m}{2}x-\frac12
$$
이다.

첫째 직선과 셋째 직선이 평행할 때
$$
-\frac{m}{2}=-\frac13 \Rightarrow m=\frac23
$$
이다.

둘째 직선과 셋째 직선이 평행할 때
$$
-\frac{m}{2}=1 \Rightarrow m=-2
$$
이다.

이제 첫째 직선과 둘째 직선의 교점을 구하면
$$
\begin{cases}
x+3y=0\\
x-y-4=0
\end{cases}
$$
$$
(x,y)=(3,-1)
$$
이다.

세 직선이 한 점에서 만나려면 이 점이 셋째 직선 위에도 있어야 하므로
$$
3m+2(-1)+1=0
$$
$$
3m-1=0
$$
$$
m=\frac13
$$
이다.

따라서 구하는 값은
$$
\frac23+(-2)+\frac13=-1
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-012",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (365, 675, 718, 995)),
        source_label="12",
        question=r"""두 점 $A(-2,5)$, $B(4,-1)$에 대하여 선분 $AB$를 $2:1$로 내분하는 점을 지나고 직선 $3x-y+1=0$과 수직인 직선의 방정식의 $y$절편은?""",
        choices=r"""① $\frac13$
② $\frac23$
③ $1$
④ $\frac43$
⑤ $\frac53$""",
        answer="⑤",
        solution=r"""선분 $AB$를 $2:1$로 내분하는 점을 $P$라 하면
$$
P\left(\frac{1\cdot (-2)+2\cdot 4}{2+1},\frac{1\cdot 5+2\cdot (-1)}{2+1}\right)=(2,1)
$$
이다.

직선 $3x-y+1=0$은
$$
y=3x+1
$$
이므로 기울기는 $3$이다.

이에 수직인 직선의 기울기는
$$
-\frac13
$$
이다.

따라서 점 $(2,1)$을 지나고 기울기가 $-\frac13$인 직선의 방정식은
$$
y-1=-\frac13(x-2)
$$
$$
y=-\frac13x+\frac53
$$
이다.

그러므로 $y$절편은
$$
\frac53
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-013",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (10, 45, 360, 360)),
        source_label="13",
        question=r"""직선 $x+ay+1=0$이 직선 $3x-y+1=0$과 수직이고, 직선 $2x+(2-b)y-1=0$과 평행할 때, 상수 $a$, $b$에 대하여 $a-b$의 값은?""",
        choices=r"""① $7$
② $5$
③ $3$
④ $1$
⑤ $-1$""",
        answer="①",
        solution=r"""직선 $x+ay+1=0$은
$$
y=-\frac1a x-\frac1a
$$
이므로 기울기는 $-\frac1a$이다.

직선 $3x-y+1=0$은
$$
y=3x+1
$$
이므로 기울기는 $3$이다.

두 직선이 수직이므로
$$
3\left(-\frac1a\right)=-1
$$
$$
a=3
$$
이다.

이제 직선 $x+3y+1=0$과 직선 $2x+(2-b)y-1=0$이 평행해야 하므로 기울기가 같다.
$$
-\frac13=-\frac{2}{2-b}
$$
$$
\frac13=\frac{2}{2-b}
$$
$$
2-b=6
$$
$$
b=-4
$$
이다.

따라서
$$
a-b=3-(-4)=7
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-014",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (10, 360, 360, 670)),
        source_label="14",
        question=r"""방정식 $x^2+y^2+4x+6y-3=0$이 나타내는 원의 중심의 좌표를 $(a,b)$, 반지름의 길이를 $r$이라 할 때, $a+b+r$의 값은?""",
        choices=r"""① $-3$
② $-1$
③ $1$
④ $3$
⑤ $5$""",
        answer="②",
        solution=r"""제곱을 완성하면
$$
x^2+4x+y^2+6y=3
$$
$$
(x+2)^2-4+(y+3)^2-9=3
$$
$$
(x+2)^2+(y+3)^2=16
$$
이다.

따라서 원의 중심은
$$
(-2,-3)
$$
이고, 반지름의 길이는
$$
4
$$
이다.

그러므로
$$
a+b+r=-2+(-3)+4=-1
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-015",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (10, 665, 360, 995)),
        source_label="15",
        question=r"""점 $(3,1)$에서 원 $x^2+y^2=5$에 그은 접선의 방정식은? (단, 기울기는 양수이다.)""",
        choices=r"""① $2x-y=5$
② $x-2y=5$
③ $x+2y=5$
④ $2x+y=7$
⑤ $3x-y=8$""",
        answer="①",
        solution=r"""기울기를 $m$이라 하면 접선의 방정식은
$$
y-1=m(x-3)
$$
$$
mx-y+1-3m=0
$$
이다.

이 직선이 원 $x^2+y^2=5$에 접하려면 원의 중심 $(0,0)$에서 직선까지의 거리가 반지름 $\sqrt5$와 같아야 하므로
$$
\frac{|1-3m|}{\sqrt{m^2+1}}=\sqrt5
$$
이다.

양변을 제곱하면
$$
(1-3m)^2=5(m^2+1)
$$
$$
4m^2-6m-4=0
$$
$$
2m^2-3m-2=0
$$
$$
(2m+1)(m-2)=0
$$
이다.

기울기가 양수이므로
$$
m=2
$$
이다.

따라서 접선의 방정식은
$$
y-1=2(x-3)
$$
$$
2x-y=5
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-016",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (365, 45, 718, 375)),
        source_label="16",
        question=r"""두 직선 $y=2x$, $y=2x+10$에 동시에 접하고 원점을 지나는 원의 방정식의 중심의 좌표를 $(a,b)$라 할 때, $a+b$의 값은?""",
        choices=r"""① $5$
② $3$
③ $1$
④ $-1$
⑤ $-3$""",
        answer="④",
        solution=r"""두 직선은 서로 평행하므로, 원의 중심은 두 직선에서 같은 거리에 있는 직선 위에 있다.

두 직선의 중간 직선은
$$
y=2x+5
$$
이므로 중심을 $(a,b)$라 하면
$$
b=2a+5
$$
이다.

두 평행선 사이의 거리는
$$
\frac{10}{\sqrt{2^2+(-1)^2}}=\frac{10}{\sqrt5}=2\sqrt5
$$
이므로 반지름의 길이는
$$
\sqrt5
$$
이다.

원점이 원 위에 있으므로
$$
\sqrt{a^2+b^2}=\sqrt5
$$
$$
a^2+b^2=5
$$
이다.

$b=2a+5$를 대입하면
$$
a^2+(2a+5)^2=5
$$
$$
5a^2+20a+20=0
$$
$$
(a+2)^2=0
$$
$$
a=-2
$$
이다.

따라서
$$
b=2(-2)+5=1
$$
이므로
$$
a+b=-1
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-017",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (365, 380, 718, 860)),
        source_label="17",
        question=r"""좌표평면 위의 두 점 $A(3,0)$, $B(0,3)$에 대하여 $AP:BP=1:2$를 만족시키는 점 $P$가 있다. 세 점 $A$, $B$, $P$를 꼭짓점으로 하는 삼각형 $ABP$의 넓이의 최댓값은?""",
        choices=r"""① $4$
② $4\sqrt{2}$
③ $6$
④ $6\sqrt{2}$
⑤ $8$""",
        answer="③",
        solution=r"""점 $P(x,y)$라 하면
$$
AP:BP=1:2
$$
이므로
$$
4AP^2=BP^2
$$
이다.

따라서
$$
4\left((x-3)^2+y^2\right)=x^2+(y-3)^2
$$
이고, 정리하면
$$
x^2+y^2-8x+2y+9=0
$$
$$
(x-4)^2+(y+1)^2=8
$$
이 된다.

즉 점 $P$의 자취는 중심이 $(4,-1)$이고 반지름의 길이가 $2\sqrt2$인 원이다.

직선 $AB$의 방정식은
$$
x+y=3
$$
이고, 중심 $(4,-1)$을 대입하면
$$
4+(-1)=3
$$
이므로 이 직선은 원의 중심을 지난다.

따라서 점 $P$에서 직선 $AB$까지의 거리의 최댓값은 반지름의 길이
$$
2\sqrt2
$$
이다.

한편
$$
AB=\sqrt{(3-0)^2+(0-3)^2}=3\sqrt2
$$
이므로 삼각형 $ABP$의 넓이의 최댓값은
$$
\frac12\cdot 3\sqrt2 \cdot 2\sqrt2=6
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-101",
        subject="COM2",
        qtype="단답형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(3, (10, 105, 360, 450)),
        source_label="서답1번",
        question=r"""두 점 $A(1,-2)$, $B(8,5)$를 잇는 선분 $AB$를 $5:2$로 내분하는 점이 직선 $y=-x+a$ 위에 있을 때, 상수 $a$의 값을 구하시오.""",
        choices="",
        answer="$9$",
        solution=r"""선분 $AB$를 $5:2$로 내분하는 점을 $P$라 하면
$$
P\left(\frac{2\cdot 1+5\cdot 8}{5+2},\frac{2\cdot (-2)+5\cdot 5}{5+2}\right)=(6,3)
$$
이다.

점 $P$가 직선 $y=-x+a$ 위에 있으므로
$$
3=-6+a
$$
$$
a=9
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-102",
        subject="COM2",
        qtype="단답형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(3, (10, 500, 360, 975)),
        source_label="서답2번",
        question=r"""좌표평면 위의 두 점 $A(2,0)$, $B(0,1)$과 원점 $O$를 꼭짓점으로 하는 삼각형 $OAB$가 있다. 직선 $y=\frac12x$ 위의 한 점 $P$가 삼각형 $OAB$의 내부에 있을 때, 점 $P$를 지나고 직선 $y=\frac12x$에 수직인 직선이 $x$축과 만나는 점을 $Q$, 선분 $AB$와 만나는 점을 $R$라 하자. 삼각형 $QAR$의 넓이가 $\frac13$일 때, 점 $P$의 좌표를 $(a,b)$라 하면 $5(a+b)$의 값을 구하시오.""",
        choices="",
        answer="$6$",
        solution=r"""점 $P$가 직선 $y=\frac12x$ 위에 있으므로
$$
P\left(t,\frac{t}{2}\right)
$$
로 둘 수 있다.

직선 $y=\frac12x$에 수직인 직선의 기울기는 $-2$이므로, 점 $P$를 지나는 직선의 방정식은
$$
y-\frac{t}{2}=-2(x-t)
$$
$$
y=-2x+\frac52t
$$
이다.

이 직선이 $x$축과 만나는 점이 $Q$이므로
$$
Q\left(\frac54t,0\right)
$$
이다.

또 선분 $AB$가 놓인 직선의 방정식은
$$
y=-\frac12x+1
$$
이다.

따라서 점 $R$은 두 직선
$$
y=-2x+\frac52t,\qquad y=-\frac12x+1
$$
의 교점이므로
$$
R\left(\frac{5t-2}{3},\frac{8-5t}{6}\right)
$$
이다.

삼각형 $QAR$의 밑변 $QA$는 $x$축 위에 있으므로
$$
QA=2-\frac54t=\frac{8-5t}{4}
$$
이고, 높이는
$$
\frac{8-5t}{6}
$$
이다.

따라서
$$
\frac12\cdot \frac{8-5t}{4}\cdot \frac{8-5t}{6}=\frac13
$$
$$
\frac{(8-5t)^2}{48}=\frac13
$$
$$
(8-5t)^2=16
$$
이다.

점 $P$는 삼각형 내부에 있으므로 $0<t<1$이고, 따라서
$$
8-5t=4
$$
$$
t=\frac45
$$
이다.

그러므로
$$
P\left(\frac45,\frac25\right)
$$
이므로
$$
5(a+b)=5\left(\frac45+\frac25\right)=6
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-103",
        subject="COM1",
        qtype="단답형",
        unit_triplet=COM1_EQ,
        crop=CropSpec(3, (365, 55, 718, 430)),
        source_label="서답3번",
        question=r"""사차방정식 $x^4-20x^2+5k-1=0$이 서로 다른 네 실근 $\alpha$, $\beta$, $\gamma$, $\delta$ $(\alpha>\beta>\gamma>\delta)$를 가진다. $\alpha-\beta=2\beta+\gamma$일 때, 상수 $k$의 값을 구하시오.""",
        choices="",
        answer="$13$",
        solution=r"""$x^2=t$로 놓으면
$$
t^2-20t+5k-1=0
$$
이다.

서로 다른 네 실근을 가지려면 $t$의 두 근이 서로 다른 양수여야 한다. 이를 큰 근부터 $r$, $s$ $(r>s>0)$라 하면
$$
x=\pm \sqrt{r},\ \pm \sqrt{s}
$$
가 네 실근이 된다.

따라서
$$
\alpha=\sqrt{r},\quad \beta=\sqrt{s},\quad \gamma=-\sqrt{s},\quad \delta=-\sqrt{r}
$$
이다.

주어진 조건
$$
\alpha-\beta=2\beta+\gamma
$$
에 대입하면
$$
\sqrt{r}-\sqrt{s}=2\sqrt{s}-\sqrt{s}=\sqrt{s}
$$
$$
\sqrt{r}=2\sqrt{s}
$$
$$
r=4s
$$
이다.

또 $r$과 $s$는
$$
t^2-20t+5k-1=0
$$
의 두 근이므로
$$
r+s=20
$$
이다.

$r=4s$를 대입하면
$$
5s=20
$$
$$
s=4,\qquad r=16
$$
이다.

또
$$
rs=5k-1
$$
이므로
$$
16\cdot 4=5k-1
$$
$$
64=5k-1
$$
$$
k=13
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-104",
        subject="COM1",
        qtype="서술형",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(3, (365, 520, 718, 830)),
        source_label="서답4번",
        question=r"""모든 실수 $x$에 대하여 부등식 $(k+2)x^2-2(k+2)x+7>0$이 성립하도록 하는 모든 정수 $k$의 값의 합을 $M$이라 하고, $3\le x\le 5$에서 이차부등식 $x^2-4x-4b+3\le 0$이 항상 성립하도록 하는 상수 $b$의 최솟값을 $m$이라 할 때, $M+m$의 값을 구하고 풀이 과정을 쓰시오.""",
        choices="",
        answer="$9$",
        solution=r"""먼저
$$
(k+2)x^2-2(k+2)x+7
$$
을 정리하면
$$
(k+2)(x-1)^2+5-k
$$
이다.

이 식이 모든 실수 $x$에 대하여 양수가 되려면
- $k+2\ge 0$이어야 하고
- 최솟값이 양수여야 한다.

$k=-2$이면 식의 값은 항상 $7$이므로 가능하다.

$k>-2$이면 최솟값은 $x=1$에서
$$
5-k
$$
이므로
$$
5-k>0 \Rightarrow k<5
$$
이다.

따라서 가능한 정수 $k$는
$$
-2,-1,0,1,2,3,4
$$
이고,
$$
M=-2-1+0+1+2+3+4=7
$$
이다.

다음으로
$$
f(x)=x^2-4x-4b+3
$$
라 하자.

$3\le x\le 5$에서
$$
f'(x)=2x-4>0
$$
이므로 $f(x)$는 증가한다.

따라서 구간에서의 최댓값은 $x=5$일 때이고, 항상
$$
f(x)\le 0
$$
이 되려면
$$
f(5)\le 0
$$
이면 충분하다.

즉
$$
25-20-4b+3\le 0
$$
$$
8-4b\le 0
$$
$$
b\ge 2
$$
이므로
$$
m=2
$$
이다.

따라서
$$
M+m=7+2=9
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-105",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(4, (10, 55, 360, 340)),
        source_label="서답5번",
        question=r"""세 점 $A(0,5)$, $B(-1,1)$, $C(2,2)$를 꼭짓점으로 하는 삼각형 $ABC$의 넓이를 다음 단계에 의하여 구하시오.

(1) 선분 $BC$의 길이를 구하시오.
(2) 직선 $BC$의 방정식을 구하시오.
(3) 점 $A$와 직선 $BC$ 사이의 거리를 구하시오.
(4) 삼각형 $ABC$의 넓이를 구하시오.""",
        choices="",
        answer=r"""(1) $\sqrt{10}$, (2) $x-3y+4=0$, (3) $\frac{11}{\sqrt{10}}$, (4) $\frac{11}{2}$""",
        solution=r"""(1) 선분 $BC$의 길이
$$
BC=\sqrt{(2-(-1))^2+(2-1)^2}=\sqrt{3^2+1^2}=\sqrt{10}
$$
이다.

(2) 직선 $BC$의 방정식

점 $B(-1,1)$, $C(2,2)$를 지나므로 기울기는
$$
\frac{2-1}{2-(-1)}=\frac13
$$
이다.

따라서
$$
y-1=\frac13(x+1)
$$
$$
x-3y+4=0
$$
이다.

(3) 점 $A$와 직선 $BC$ 사이의 거리
$$
\frac{|0-3\cdot 5+4|}{\sqrt{1^2+(-3)^2}}=\frac{11}{\sqrt{10}}
$$
이다.

(4) 삼각형 $ABC$의 넓이
$$
[ABC]=\frac12\cdot BC\cdot \text{높이}
$$
$$
=\frac12\cdot \sqrt{10}\cdot \frac{11}{\sqrt{10}}=\frac{11}{2}
$$
이다.""",
    ),
    ProblemData(
        pid="HN-2023-G1-S1-Final-106",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(4, (365, 55, 718, 720)),
        source_label="서답6번",
        scan_source=SCAN_106,
        question=r"""그림과 같이 중심이 제1사분면 위에 있는 원이 직선 $y=2x$와 두 점 $A$, $B$에서 만나고, 직선 $y=-\frac12x+2$와 두 점 $B$, $C$에서 만난다.

<img src="assets/scan.png" alt="서답6번 그림" style="width:60% !important; max-width:60% !important; height:auto;" />

$\overline{AB}=2\sqrt{5}$, $\overline{BC}=4\sqrt{5}$이고, 원의 방정식을 $(x-a)^2+(y-b)^2=r^2$이라 할 때, $5(a-b)+r$의 값을 구하고 풀이 과정을 쓰시오.""",
        choices="",
        answer="$26$",
        solution=r"""두 직선의 교점이 점 $B$이므로
$$
2x=-\frac12x+2
$$
$$
\frac52x=2
$$
$$
x=\frac45,\qquad y=\frac85
$$
이다.

따라서
$$
B\left(\frac45,\frac85\right)
$$
이다.

직선 $y=2x$의 방향벡터는 $(1,2)$이고 그 길이는 $\sqrt5$이므로, $\overline{AB}=2\sqrt5$에서
$$
A=B+2(1,2)=\left(\frac{14}{5},\frac{28}{5}\right)
$$
이다.

직선 $y=-\frac12x+2$의 방향벡터는 $(2,-1)$이고 그 길이는 $\sqrt5$이므로, $\overline{BC}=4\sqrt5$에서
$$
C=B+4(2,-1)=\left(\frac{44}{5},-\frac{12}{5}\right)
$$
이다.

직선 $AB$의 기울기는 $2$, 직선 $BC$의 기울기는 $-\frac12$이므로 두 직선은 서로 수직이다.

따라서
$$
\angle ABC=90^\circ
$$
이고, 점 $A$, $B$, $C$가 모두 원 위에 있으므로 $AC$는 원의 지름이다.

그러므로 원의 중심은 선분 $AC$의 중점이어서
$$
\left(\frac{\frac{14}{5}+\frac{44}{5}}{2},\frac{\frac{28}{5}+\left(-\frac{12}{5}\right)}{2}\right)=\left(\frac{29}{5},\frac85\right)
$$
이다.

즉
$$
a=\frac{29}{5},\qquad b=\frac85
$$
이다.

또
$$
AC=\sqrt{\left(\frac{44}{5}-\frac{14}{5}\right)^2+\left(-\frac{12}{5}-\frac{28}{5}\right)^2}
$$
$$
=\sqrt{6^2+(-8)^2}=10
$$
이므로 반지름의 길이는
$$
r=5
$$
이다.

따라서
$$
5(a-b)+r=5\left(\frac{29}{5}-\frac85\right)+5=21+5=26
$$
이다.""",
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
        return 4
    if row.pid.endswith("-106") and level < 5:
        return 5
    if row.pid.endswith("-017") and level < 4:
        return 4
    return level


def _front_matter(row: ProblemData, original_asset_name: str, extra_assets: List[str]) -> Dict[str, object]:
    _, source_no, source_kind = _source_meta(row.pid)
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(*row.unit_triplet)
    level = _level_for(row)
    assets = [f"assets/original/{original_asset_name}"]
    assets.extend(extra_assets)
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
        "assets": assets,
    }


def _render_crop(doc: fitz.Document, crop: CropSpec, out_path: Path) -> None:
    page = doc[crop.page]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(*crop.rect), alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def _write_problem(row: ProblemData, doc: fitz.Document, results: List[str], warnings: List[str], review_paths: List[str]) -> None:
    folder = PROBLEMS / row.pid
    if folder.exists():
        results.append(f"{row.pid} | skipped | duplicate-folder")
        return

    folder.mkdir(parents=True, exist_ok=False)
    assets_original = folder / "assets" / "original"
    assets_original.mkdir(parents=True, exist_ok=True)

    original_asset_name = f"{row.pid}_original.png"
    _render_crop(doc, row.crop, assets_original / original_asset_name)

    extra_assets: List[str] = []
    if row.scan_source is not None:
        if row.scan_source.exists():
            shutil.copy2(row.scan_source, assets_original / row.scan_source.name)
            shutil.copy2(row.scan_source, folder / "assets" / "scan.png")
            extra_assets.extend([f"assets/original/{row.scan_source.name}", "assets/scan.png"])
        else:
            warnings.append(f"{row.pid}: missing scan source ({row.scan_source.name})")

    front = _front_matter(row=row, original_asset_name=original_asset_name, extra_assets=extra_assets)
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
    warnings: List[str] = []
    review_paths: List[str] = []
    duplicates: List[str] = []

    try:
        for row in DATA:
            folder = PROBLEMS / row.pid
            if folder.exists():
                duplicates.append(row.pid)
                results.append(f"{row.pid} | skipped | duplicate-folder")
                continue
            _write_problem(row=row, doc=doc, results=results, warnings=warnings, review_paths=review_paths)
    finally:
        doc.close()

    created = sum(1 for row in results if "| created |" in row)
    skipped = sum(1 for row in results if "| skipped |" in row)
    report_lines: List[str] = [
        f"created={created} updated=0 skipped={skipped} warnings={len(warnings)}",
        "",
        "[FILES]",
        *results,
        "",
        "[DUPLICATE_FOLDERS]",
        *(duplicates or ["none"]),
        "",
        "[OCR_UNCERTAIN]",
        "none",
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

