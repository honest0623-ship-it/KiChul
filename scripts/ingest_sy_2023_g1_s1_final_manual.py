from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import shutil
import sys
import textwrap

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet


PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "SY.2023.G1.S1.Final.COM1.pdf"
SCAN_012 = ORIGINAL / "SY.2023.G1.S1.Final.COM1.012.png"
SCAN_102 = ORIGINAL / "SY.2023.G1.S1.Final.COM1.서답2번.png"
REPORT_PATH = ROOT / "_tmp_sy_2023_g1_s1_final_report.txt"

FIXED_META = {
    "school": "SY",
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
COM1_QF = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수")
COM1_EQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식")
COM1_INEQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식")
COM2_COORD = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-1. 평면좌표")
COM2_LINE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식")
COM2_CIRCLE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식")
COM2_MOVE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-4. 도형의 이동")


def q(text: str) -> str:
    return textwrap.dedent(text).strip()


FIGURE_HTML = (
    '<img src="assets/scan.png" alt="문항 그림" '
    'style="width:60%; max-width:60%; height:auto; display:block; margin:12px auto;" />'
)


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
    level_hint: Optional[int] = None
    scan_source: Optional[Path] = None
    ocr_uncertain: bool = False


DATA: Sequence[ProblemData] = (
    ProblemData(
        pid="SY-2023-G1-S1-Final-001",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(0, (40, 220, 840, 640)),
        source_label="1",
        question=q(
            r"""
            다음 중 직선을 나타내는 방정식이 아닌 것은?
            """
        ),
        choices=q(
            r"""
            ① \(x+2y+3=0\)
            ② \(y=-x+2\)
            ③ \(2x+3=0\)
            ④ \(2y-3=0\)
            ⑤ \(xy=2\)
            """
        ),
        answer="⑤",
        solution=q(
            r"""
            \(x\)와 \(y\)에 대한 일차방정식은 직선을 나타낸다.

            ①, ②, ③, ④는 모두 \(x,\ y\)의 최고차항이 \(1\)차이므로 직선의 방정식이다.

            ⑤는
            \[
            xy=2
            \]
            와 같이 \(xy\)항이 있는 이차식이므로 직선을 나타내지 않는다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=2,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-002",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(0, (40, 760, 840, 1280)),
        source_label="2",
        question=q(
            r"""
            직선
            \[
            y=x+4
            \]
            에 평행한 직선의 기울기를 \(m\), 수직인 직선의 기울기를 \(n\)이라 할 때, \(m+n\)의 값은?

            (단, \(m,\ n\)은 실수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(-2\)
            ② \(-1\)
            ③ \(0\)
            ④ \(1\)
            ⑤ \(2\)
            """
        ),
        answer="③",
        solution=q(
            r"""
            직선
            \[
            y=x+4
            \]
            의 기울기는 \(1\)이다.

            따라서 평행한 직선의 기울기는
            \[
            m=1
            \]
            이다.

            또 이에 수직인 직선의 기울기는
            \[
            n=-1
            \]
            이다.

            그러므로
            \[
            m+n=1+(-1)=0
            \]
            이다.

            따라서 정답은 ③이다.
            """
        ),
        level_hint=2,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-003",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (40, 1430, 840, 1940)),
        source_label="3",
        question=q(
            r"""
            연립부등식
            \[
            \begin{cases}
            x+6>3\\
            -2x-4>0
            \end{cases}
            \]
            의 해가 \(a<x<b\)일 때, \(a+b\)의 값은?

            (단, \(a,\ b\)는 실수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(-5\)
            ② \(-4\)
            ③ \(-3\)
            ④ \(-2\)
            ⑤ \(-1\)
            """
        ),
        answer="①",
        solution=q(
            r"""
            첫째 부등식에서
            \[
            x+6>3
            \]
            이므로
            \[
            x>-3
            \]
            이다.

            둘째 부등식에서
            \[
            -2x-4>0
            \]
            이므로
            \[
            -2x>4,\quad x<-2
            \]
            이다.

            따라서 해는
            \[
            -3<x<-2
            \]
            이므로
            \[
            a=-3,\quad b=-2
            \]
            이다.

            그러므로
            \[
            a+b=-5
            \]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=2,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-004",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(0, (930, 120, 1790, 620)),
        source_label="4",
        question=q(
            r"""
            방정식
            \[
            x^2+y^2-6x+2y+6=0
            \]
            은 중심의 좌표가 \((a,b)\)이고 반지름의 길이가 \(r\)인 원이다. 상수 \(a+b+r\)의 값은?
            """
        ),
        choices=q(
            r"""
            ① \(3\)
            ② \(4\)
            ③ \(5\)
            ④ \(6\)
            ⑤ \(7\)
            """
        ),
        answer="②",
        solution=q(
            r"""
            주어진 식을 완전제곱식으로 고치면
            \[
            (x^2-6x)+(y^2+2y)+6=0
            \]
            \[
            (x-3)^2-9+(y+1)^2-1+6=0
            \]
            \[
            (x-3)^2+(y+1)^2=4
            \]
            이다.

            따라서 중심은
            \[
            (a,b)=(3,-1)
            \]
            이고 반지름은
            \[
            r=2
            \]
            이다.

            그러므로
            \[
            a+b+r=3+(-1)+2=4
            \]
            이다.

            따라서 정답은 ②이다.
            """
        ),
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-005",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_MOVE,
        crop=CropSpec(0, (930, 720, 1790, 1300)),
        source_label="5",
        question=q(
            r"""
            원
            \[
            (x-2)^2+(y+1)^2=1
            \]
            을 \(x\)축 방향으로 \(a\)만큼, \(y\)축 방향으로 \(b\)만큼 평행이동하였더니 원
            \[
            (x+3)^2+(y-1)^2=1
            \]
            이 되었다. 이때 상수 \(a,\ b\)에 대하여 \(a+b\)의 값은?
            """
        ),
        choices=q(
            r"""
            ① \(-3\)
            ② \(-2\)
            ③ \(-1\)
            ④ \(2\)
            ⑤ \(3\)
            """
        ),
        answer="①",
        solution=q(
            r"""
            처음 원의 중심은
            \[
            (2,-1)
            \]
            이고, 옮긴 뒤의 원의 중심은
            \[
            (-3,1)
            \]
            이다.

            따라서 평행이동한 양은
            \[
            a=-3-2=-5,\quad b=1-(-1)=2
            \]
            이다.

            그러므로
            \[
            a+b=-5+2=-3
            \]
            이다.

            따라서 정답은 ①이다.
            """
        ),
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-006",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (930, 1400, 1790, 1880)),
        source_label="6",
        question=q(
            r"""
            방정식
            \[
            x^3+x^2+4x-6=0
            \]
            의 서로 다른 두 허근의 곱은?
            """
        ),
        choices=q(
            r"""
            ① \(7\)
            ② \(6\)
            ③ \(5\)
            ④ \(4\)
            ⑤ \(3\)
            """
        ),
        answer="②",
        solution=q(
            r"""
            \(x=1\)을 대입하면
            \[
            1+1+4-6=0
            \]
            이므로 \(x-1\)은 인수이다.

            따라서
            \[
            x^3+x^2+4x-6=(x-1)(x^2+2x+6)
            \]
            이다.

            서로 다른 두 허근은
            \[
            x^2+2x+6=0
            \]
            의 근이므로, 그 곱은 근과 계수의 관계에 의하여
            \[
            6
            \]
            이다.

            따라서 정답은 ②이다.
            """
        ),
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-007",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(1, (40, 120, 840, 560)),
        source_label="7",
        question=q(
            r"""
            연립방정식
            \[
            \begin{cases}
            3x-y=1\\
            x^2-3xy+y^2=a
            \end{cases}
            \]
            이 실근을 가질 때, 정수 \(a\)의 최솟값은?
            """
        ),
        choices=q(
            r"""
            ① \(-5\)
            ② \(-4\)
            ③ \(-3\)
            ④ \(-2\)
            ⑤ \(-1\)
            """
        ),
        answer="⑤",
        solution=q(
            r"""
            첫째 식에서
            \[
            y=3x-1
            \]
            이다.

            이를 둘째 식에 대입하면
            \[
            x^2-3x(3x-1)+(3x-1)^2=a
            \]
            \[
            x^2-9x^2+3x+9x^2-6x+1=a
            \]
            \[
            x^2-3x+1=a
            \]
            이다.

            좌변을 완전제곱식으로 고치면
            \[
            x^2-3x+1=\left(x-\frac32\right)^2-\frac54
            \]
            이므로 최솟값은
            \[
            -\frac54
            \]
            이다.

            따라서 실근을 가지려면
            \[
            a\ge -\frac54
            \]
            이어야 하므로, 가능한 정수 \(a\)의 최솟값은
            \[
            -1
            \]
            이다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-008",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (40, 760, 840, 1260)),
        source_label="8",
        question=q(
            r"""
            좌표평면 위의 세 점 \(A(-1,1)\), \(B(5,5)\), \(C(a,b)\)에 대하여
            \[
            \overline{CA}^{\,2}+\overline{CB}^{\,2}
            \]
            의 최솟값은?

            (단, \(a,\ b\)는 실수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(22\)
            ② \(23\)
            ③ \(24\)
            ④ \(25\)
            ⑤ \(26\)
            """
        ),
        answer="⑤",
        solution=q(
            r"""
            두 점 \(A\), \(B\)의 중점을 \(M\)이라 하면
            \[
            M\left(\frac{-1+5}{2},\frac{1+5}{2}\right)=(2,3)
            \]
            이다.

            좌표를 이용하면
            \[
            \overline{CA}^{\,2}+\overline{CB}^{\,2}
            =\{(a+1)^2+(b-1)^2\}+\{(a-5)^2+(b-5)^2\}
            \]
            \[
            =2(a-2)^2+2(b-3)^2+26
            \]
            이다.

            따라서 최솟값은
            \[
            26
            \]
            이고, 이때는 \(C=(2,3)\)이다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-009",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (40, 1420, 840, 1920)),
        source_label="9",
        question=q(
            r"""
            평행한 두 직선
            \[
            y=x+1,\quad y=x+a
            \]
            사이의 거리가 \(2\sqrt{2}\)일 때, 자연수 \(a\)의 값은?
            """
        ),
        choices=q(
            r"""
            ① \(3\)
            ② \(4\)
            ③ \(5\)
            ④ \(6\)
            ⑤ \(7\)
            """
        ),
        answer="③",
        solution=q(
            r"""
            두 직선을 일반형으로 나타내면
            \[
            x-y+1=0,\quad x-y+a=0
            \]
            이다.

            평행한 두 직선 사이의 거리는
            \[
            \frac{|a-1|}{\sqrt{1^2+(-1)^2}}
            =\frac{|a-1|}{\sqrt{2}}
            \]
            이다.

            이것이 \(2\sqrt{2}\)이므로
            \[
            \frac{|a-1|}{\sqrt{2}}=2\sqrt{2}
            \]
            \[
            |a-1|=4
            \]
            이다.

            따라서
            \[
            a=5 \quad \text{또는} \quad a=-3
            \]
            이고, \(a\)는 자연수이므로
            \[
            a=5
            \]
            이다.

            따라서 정답은 ③이다.
            """
        ),
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-010",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_CPX,
        crop=CropSpec(1, (930, 80, 1790, 540)),
        source_label="10",
        question=q(
            r"""
            사차방정식
            \[
            x^4+4x^3+3x^2+ax+b=0
            \]
            의 한 근이 \(-1-i\)일 때, 실수 \(a,\ b\)의 곱 \(a\times b\)의 값은?

            (단, \(i=\sqrt{-1}\)이다.)
            """
        ),
        choices=q(
            r"""
            ① \(6\)
            ② \(8\)
            ③ \(10\)
            ④ \(12\)
            ⑤ \(14\)
            """
        ),
        answer="④",
        solution=q(
            r"""
            계수가 모두 실수이므로 \(-1+i\)도 근이다.

            따라서
            \[
            (x+1+i)(x+1-i)=(x+1)^2+1=x^2+2x+2
            \]
            는 주어진 방정식의 인수이다.

            나머지 인수를
            \[
            x^2+2x+t
            \]
            라 두면
            \[
            (x^2+2x+2)(x^2+2x+t)
            \]
            의 \(x^2\)의 계수는 \(t+6\)이다.

            이것이 \(3\)과 같으므로
            \[
            t+6=3,\quad t=-3
            \]
            이다.

            따라서
            \[
            x^4+4x^3+3x^2+ax+b=(x^2+2x+2)(x^2+2x-3)
            \]
            이고 전개하면
            \[
            x^4+4x^3+3x^2-2x-6
            \]
            이다.

            그러므로
            \[
            a=-2,\quad b=-6
            \]
            이고
            \[
            a\times b=12
            \]
            이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-011",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(1, (930, 830, 1790, 1290)),
        source_label="11",
        question=q(
            r"""
            부등식
            \[
            |3x+1|<|x-1|+8
            \]
            의 해가 \(a<x<b\)일 때, \(a+b\)의 값은?

            (단, \(a,\ b\)는 실수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(-1\)
            ② \(-2\)
            ③ \(-3\)
            ④ \(-4\)
            ⑤ \(-5\)
            """
        ),
        answer="②",
        solution=q(
            r"""
            절댓값의 기준이 되는 점은
            \[
            x=-\frac13,\quad x=1
            \]
            이다.

            1. \(x<-\frac13\)일 때
            \[
            |3x+1|=-(3x+1),\quad |x-1|=1-x
            \]
            이므로
            \[
            -3x-1<1-x+8
            \]
            \[
            -2x<10,\quad x>-5
            \]
            이다.

            따라서
            \[
            -5<x<-\frac13
            \]
            이다.

            2. \(-\frac13\le x<1\)일 때
            \[
            3x+1<1-x+8
            \]
            \[
            4x<8,\quad x<2
            \]
            이므로 이 구간에서는 항상 성립한다.

            3. \(x\ge 1\)일 때
            \[
            3x+1<x-1+8
            \]
            \[
            2x<6,\quad x<3
            \]
            이므로
            \[
            1\le x<3
            \]
            이다.

            따라서 전체 해는
            \[
            -5<x<3
            \]
            이므로
            \[
            a=-5,\quad b=3
            \]
            이다.

            그러므로
            \[
            a+b=-2
            \]
            이다.

            따라서 정답은 ②이다.
            """
        ),
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-012",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_QF,
        crop=CropSpec(2, (40, 90, 840, 1120)),
        source_label="12",
        question=q(
            rf"""
            이차항의 계수가 각각 \(1\), \(-1\)인 두 이차함수 \(y=f(x)\), \(y=g(x)\)의 그래프가 다음 그림과 같을 때, 부등식
            \[
            f(x)g(x)\ge 0
            \]
            을 만족하는 정수 \(x\)의 개수는?

            {FIGURE_HTML}
            """
        ),
        choices=q(
            r"""
            ① \(3\)
            ② \(4\)
            ③ \(5\)
            ④ \(6\)
            ⑤ \(7\)
            """
        ),
        answer="③",
        solution=q(
            r"""
            그래프에서 이차항의 계수가 \(1\)인 함수는 위로 열린 포물선이고, \(x\)축과 만나는 점은
            \[
            x=2,\quad x=6
            \]
            이다.

            따라서
            \[
            f(x)\ge 0 \quad \text{인 범위는} \quad x\le 2 \text{ 또는 } x\ge 6
            \]
            이다.

            또 이차항의 계수가 \(-1\)인 함수는 아래로 열린 포물선이고, \(x\)축과 만나는 점은
            \[
            x=-1,\quad x=6
            \]
            이다.

            따라서
            \[
            g(x)\ge 0 \quad \text{인 범위는} \quad -1\le x\le 6
            \]
            이다.

            곱
            \[
            f(x)g(x)\ge 0
            \]
            이 되려면 두 값의 부호가 같거나 둘 중 하나가 \(0\)이어야 한다.

            그래프에서 이를 만족하는 정수 \(x\)는
            \[
            -1,\ 0,\ 1,\ 2,\ 6
            \]
            의 \(5\)개이다.

            따라서 정답은 ③이다.
            """
        ),
        level_hint=4,
        scan_source=SCAN_012,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-013",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (40, 1320, 840, 1880)),
        source_label="13",
        question=q(
            r"""
            좌표평면 위의 점 \(A(2,2)\)와 직선
            \[
            (k+2)x+(k-1)y+1-4k=0
            \]
            사이의 거리의 최댓값은?

            (단, \(k\)는 실수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(\sqrt{2}\)
            ② \(\sqrt{3}\)
            ③ \(2\)
            ④ \(\sqrt{5}\)
            ⑤ \(6\)
            """
        ),
        answer="①",
        solution=q(
            r"""
            점 \(A(2,2)\)에서 직선까지의 거리를 \(d\)라 하면
            \[
            d=
            \frac{|(k+2)\cdot 2+(k-1)\cdot 2+1-4k|}
            {\sqrt{(k+2)^2+(k-1)^2}}
            \]
            이다.

            분자를 정리하면
            \[
            2k+4+2k-2+1-4k=3
            \]
            이므로
            \[
            d=\frac{3}{\sqrt{(k+2)^2+(k-1)^2}}
            \]
            이다.

            따라서 \(d\)가 최대가 되려면 분모가 최소가 되어야 한다.

            \[
            (k+2)^2+(k-1)^2
            =2k^2+2k+5
            \]
            \[
            =2\left(k+\frac12\right)^2+\frac92
            \]
            이므로 최솟값은
            \[
            \frac92
            \]
            이다.

            따라서 분모의 최솟값은
            \[
            \sqrt{\frac92}=\frac{3}{\sqrt{2}}
            \]
            이고,
            \[
            d_{\max}=\frac{3}{3/\sqrt{2}}=\sqrt{2}
            \]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-014",
        subject="COM2",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (930, 80, 1790, 960)),
        source_label="14",
        question=q(
            r"""
            원
            \[
            x^2+y^2=25
            \]
            와 직선
            \[
            4x+3y-12=0
            \]
            이 만나는 두 점을 각각 \(A\), \(B\)라 하자. 삼각형 \(ABC\)의 넓이가 최대가 되도록 원 위의 점 \(C\)를 잡을 때, 점 \(C\)에서의 접선의 방정식은 \(ax+by+c=0\)이다. \(a+b+c\)의 값은?

            (단, \(a,\ b,\ c\)는 서로소인 자연수이다.)
            """
        ),
        choices=q(
            r"""
            ① \(32\)
            ② \(33\)
            ③ \(34\)
            ④ \(35\)
            ⑤ \(36\)
            """
        ),
        answer="①",
        solution=q(
            r"""
            선분 \(AB\)의 길이는 일정하므로, 삼각형 \(ABC\)의 넓이가 최대가 되려면 점 \(C\)에서 직선
            \[
            4x+3y-12=0
            \]
            까지의 거리가 최대가 되어야 한다.

            원의 중심은 원점 \(O(0,0)\)이고 반지름은 \(5\)이다.
            따라서 직선에 가장 멀리 있는 원 위의 점은 이 직선에 수직인 방향에 있는 점이다.

            직선의 법선벡터는 \((4,3)\)이므로 반지름 \(5\)인 원 위의 해당 점은
            \[
            (4,3),\quad (-4,-3)
            \]
            이다.

            두 점에서 직선까지의 거리를 비교하면
            \[
            \frac{|4\cdot 4+3\cdot 3-12|}{5}=\frac{13}{5},
            \quad
            \frac{|4\cdot (-4)+3\cdot (-3)-12|}{5}=\frac{37}{5}
            \]
            이므로 더 먼 점은
            \[
            C(-4,-3)
            \]
            이다.

            원
            \[
            x^2+y^2=25
            \]
            위의 점 \((x_1,y_1)\)에서의 접선의 방정식은
            \[
            x_1x+y_1y=25
            \]
            이므로, 점 \(C(-4,-3)\)에서의 접선은
            \[
            -4x-3y=25
            \]
            이다.

            이를 정리하면
            \[
            4x+3y+25=0
            \]
            이므로
            \[
            a=4,\quad b=3,\quad c=25
            \]
            이다.

            따라서
            \[
            a+b+c=32
            \]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=5,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-015",
        subject="COM1",
        qtype="객관식",
        unit_triplet=COM1_CPX,
        crop=CropSpec(2, (930, 1300, 1790, 1880)),
        source_label="15",
        question=q(
            r"""
            삼차방정식
            \[
            x^3=1
            \]
            의 한 허근을 \(w\)라 할 때,
            \[
            (w+1)^n+(w^2+1)^n=1
            \]
            을 만족하는 \(50\) 이하의 정수 \(n\)의 개수는?
            """
        ),
        choices=q(
            r"""
            ① \(8\)
            ② \(9\)
            ③ \(16\)
            ④ \(17\)
            ⑤ \(18\)
            """
        ),
        answer="④",
        solution=q(
            r"""
            \(w\)는 \(x^3=1\)의 허근이므로
            \[
            w^3=1,\quad 1+w+w^2=0
            \]
            이다.

            따라서
            \[
            w+1=-w^2,\quad w^2+1=-w
            \]
            이므로
            \[
            (w+1)^n+(w^2+1)^n
            =(-w^2)^n+(-w)^n
            =(-1)^n\left(w^{2n}+w^n\right)
            \]
            이다.

            \(w^3=1\)이므로 \(n\)을 \(6\)으로 나눈 나머지에 따라 값을 조사하면 된다.

            \[
            \begin{array}{c|c}
            n\text{을 }6\text{으로 나눈 나머지} & (-1)^n(w^{2n}+w^n) \\
            \hline
            0 & 2 \\
            1 & -(w^2+w)=1 \\
            2 & w+w^2=-1 \\
            3 & -2 \\
            4 & w+w^2=-1 \\
            5 & -(w+w^2)=1
            \end{array}
            \]

            따라서 조건을 만족하는 것은 \(n\)을 \(6\)으로 나눈 나머지가 \(1\) 또는 \(5\)일 때이다.

            \(1\)부터 \(50\)까지의 정수 중에서
            \[
            1,\ 5,\ 7,\ 11,\ \dots,\ 49
            \]
            이고, 개수는
            \[
            9+8=17
            \]
            이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-101",
        subject="COM1",
        qtype="단답형",
        unit_triplet=COM1_CPX,
        crop=CropSpec(3, (40, 120, 840, 760)),
        source_label="서답1",
        question=q(
            r"""
            이차방정식
            \[
            x^2-2ax-a+12=0
            \]
            의 두 근이 모두 양수일 때, 정수 \(a\)의 값들의 합을 구하시오.
            """
        ),
        choices="",
        answer="63",
        solution=q(
            r"""
            두 근을 \(\alpha,\ \beta\)라 하자.

            두 근이 모두 양수이려면
            \[
            \alpha+\beta>0,\quad \alpha\beta>0
            \]
            이어야 하고, 실근을 가져야 하므로 판별식도 \(0\) 이상이어야 한다.

            근과 계수의 관계에 의하여
            \[
            \alpha+\beta=2a,\quad \alpha\beta=12-a
            \]
            이므로
            \[
            2a>0,\quad 12-a>0
            \]
            즉
            \[
            a>0,\quad a<12
            \]
            이다.

            또 판별식은
            \[
            D=(-2a)^2-4(1)(12-a)=4a^2+4a-48
            \]
            \[
            =4(a+4)(a-3)
            \]
            이므로
            \[
            D\ge 0 \Rightarrow a\le -4 \text{ 또는 } a\ge 3
            \]
            이다.

            이를 모두 합치면
            \[
            3\le a<12
            \]
            이다.

            따라서 가능한 정수 \(a\)는
            \[
            3,\ 4,\ 5,\ 6,\ 7,\ 8,\ 9,\ 10,\ 11
            \]
            이고, 그 합은
            \[
            \frac{(3+11)\times 9}{2}=63
            \]
            이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-102",
        subject="COM2",
        qtype="단답형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(3, (40, 1180, 840, 2280)),
        source_label="서답2",
        question=q(
            rf"""
            두 점 \(A(5,2)\), \(B(-1,3)\)과 \(x\)축 위를 움직이는 점 \(C(a,0)\), \(D(a+1,0)\)에 대하여 사각형 \(ABCD\)의 둘레의 길이의 최솟값은
            \[
            1+m\sqrt{{2}}+\sqrt{{n}}
            \]
            이다. 두 자연수 \(m,\ n\)에 대하여 \(m+n\)의 값을 구하시오.

            (단, \(a\)는 실수이다.)

            {FIGURE_HTML}
            """
        ),
        choices="",
        answer=q(
            r"""
            \(m=5,\ n=37,\ m+n=42\)
            """
        ),
        solution=q(
            r"""
            사각형의 둘레는
            \[
            \overline{AB}+\overline{BC}+\overline{CD}+\overline{DA}
            \]
            이다.

            여기서
            \[
            \overline{AB}
            =\sqrt{(5-(-1))^2+(2-3)^2}
            =\sqrt{37}
            \]
            이고
            \[
            \overline{CD}=1
            \]
            이다.

            따라서 \(\overline{BC}+\overline{DA}\)의 최솟값만 구하면 된다.

            점 \(D(a+1,0)\) 대신 점 \(C(a,0)\)를 기준으로 보면
            \[
            \overline{DA}=\sqrt{(a-4)^2+2^2}
            \]
            이다.

            점 \(A'(4,2)\)를 잡으면
            \[
            \overline{DA}=\overline{CA'}
            \]
            이다.

            이제 \(B(-1,3)\)를 \(x\)축에 대하여 대칭이동한 점을 \(B'(-1,-3)\)라 하면
            \[
            \overline{BC}=\overline{B'C}
            \]
            이므로
            \[
            \overline{BC}+\overline{DA}
            =\overline{B'C}+\overline{CA'}
            \ge \overline{B'A'}
            \]
            이다.

            따라서 최솟값은
            \[
            \overline{B'A'}
            =\sqrt{(4-(-1))^2+(2-(-3))^2}
            =\sqrt{25+25}
            =5\sqrt{2}
            \]
            이다.

            그러므로 사각형 \(ABCD\)의 둘레의 최솟값은
            \[
            \sqrt{37}+1+5\sqrt{2}
            \]
            이다.

            따라서
            \[
            m=5,\quad n=37
            \]
            이므로
            \[
            m+n=42
            \]
            이다.
            """
        ),
        level_hint=4,
        scan_source=SCAN_102,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-103",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(3, (930, 120, 1790, 1120)),
        source_label="서답3",
        question=q(
            r"""
            점 \(A(4,0)\)에서 원
            \[
            x^2+y^2=4
            \]
            에 그은 접선의 두 접점을 \(P\), \(Q\)라 하자. 삼각형 \(APQ\)의 넓이를 구하시오.

            (1) 접선의 방정식을 이용하여 두 접점 \(P\), \(Q\)의 좌표를 구하시오.

            (2) 삼각형 \(APQ\)의 넓이를 구하시오.
            """
        ),
        choices="",
        answer=q(
            r"""
            (1) \(P(1,\sqrt{3})\), \(Q(1,-\sqrt{3})\)

            (2) \(3\sqrt{3}\)
            """
        ),
        solution=q(
            r"""
            점 \(A(4,0)\)을 지나고 기울기가 \(m\)인 접선의 방정식을
            \[
            y=m(x-4)
            \]
            라 하자.

            이 직선이 원
            \[
            x^2+y^2=4
            \]
            에 접하려면 원의 중심 \(O(0,0)\)에서 이 직선까지의 거리가 반지름 \(2\)와 같아야 한다.

            따라서
            \[
            \frac{|4m|}{\sqrt{m^2+1}}=2
            \]
            이고,
            \[
            16m^2=4(m^2+1)
            \]
            \[
            3m^2=1
            \]
            이므로
            \[
            m=\pm \frac{\sqrt{3}}{3}
            \]
            이다.

            따라서 두 접선의 방정식은
            \[
            y=\frac{\sqrt{3}}{3}(x-4),\quad
            y=-\frac{\sqrt{3}}{3}(x-4)
            \]
            이다.

            첫째 직선과 원의 접점을 구하면
            \[
            x=1,\quad y=\sqrt{3}
            \]
            이고, 둘째 직선의 접점은
            \[
            x=1,\quad y=-\sqrt{3}
            \]
            이다.

            따라서
            \[
            P(1,\sqrt{3}),\quad Q(1,-\sqrt{3})
            \]
            이다.

            이제
            \[
            \overline{PQ}=2\sqrt{3}
            \]
            이고, 점 \(A(4,0)\)에서 직선 \(x=1\)까지의 거리는
            \[
            3
            \]
            이므로 삼각형 \(APQ\)의 넓이는
            \[
            \frac12\cdot 2\sqrt{3}\cdot 3=3\sqrt{3}
            \]
            이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-104",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(4, (40, 100, 840, 1260)),
        source_label="서답4",
        question=q(
            r"""
            좌표평면 위의 두 점 \(A(1,2)\), \(B(7,-1)\)에 대하여 선분 \(AB\)를 \(2:1\)로 내분하는 점을 \(P\), \(3:2\)로 외분하는 점을 \(Q\)라 하자. 두 점 \(P,\ Q\)를 지나는 직선의 방정식을 \(y=mx+n\)이라 할 때 \(m+n\)의 값을 구하시오.

            (단, \(m,\ n\)은 실수이다.)

            (1) 점 \(P\)의 좌표를 구하시오.

            (2) 점 \(Q\)의 좌표를 구하시오.

            (3) 두 점 \(P,\ Q\)를 지나는 직선의 방정식을 구하여 \(m+n\)의 값을 구하시오.
            """
        ),
        choices="",
        answer=q(
            r"""
            (1) \(P(5,0)\)

            (2) \(Q(19,-7)\)

            (3) \(y=-\frac12x+\frac52\), 따라서 \(m+n=2\)
            """
        ),
        solution=q(
            r"""
            (1) 점 \(P\)는 선분 \(AB\)를 \(2:1\)로 내분하므로
            \[
            P\left(
            \frac{1\cdot 1+2\cdot 7}{2+1},
            \frac{1\cdot 2+2\cdot (-1)}{2+1}
            \right)
            =(5,0)
            \]
            이다.

            (2) 점 \(Q\)는 선분 \(AB\)를 \(3:2\)로 외분하므로
            \[
            Q\left(
            \frac{3\cdot 7-2\cdot 1}{3-2},
            \frac{3\cdot (-1)-2\cdot 2}{3-2}
            \right)
            =(19,-7)
            \]
            이다.

            (3) 직선 \(PQ\)의 기울기는
            \[
            \frac{-7-0}{19-5}=-\frac12
            \]
            이다.

            따라서 직선의 방정식을
            \[
            y=-\frac12x+n
            \]
            이라 두고 점 \(P(5,0)\)을 대입하면
            \[
            0=-\frac12\cdot 5+n
            \]
            \[
            n=\frac52
            \]
            이다.

            그러므로
            \[
            y=-\frac12x+\frac52
            \]
            이고,
            \[
            m+n=-\frac12+\frac52=2
            \]
            이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2023-G1-S1-Final-105",
        subject="COM2",
        qtype="서술형",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(4, (930, 100, 1790, 1260)),
        source_label="서답5",
        question=q(
            r"""
            점 \((-2,1)\)을 지나고 \(x\)축과 \(y\)축에 동시에 접하는 두 원의 교점을 지나는 직선이 \(x\)축, \(y\)축과 만나는 점을 \(A,\ B\)라 할 때 삼각형 \(OAB\)의 넓이를 구하시오.

            (단, \(O\)는 원점이다.)

            (1) 점 \((-2,1)\)을 지나고 \(x\)축과 \(y\)축에 동시에 접하는 두 원의 방정식을 구하시오.

            (2) 두 원의 교점을 지나는 직선의 방정식을 구하시오.

            (3) 삼각형 \(OAB\)의 넓이를 구하시오.
            """
        ),
        choices="",
        answer=q(
            r"""
            (1) \((x+1)^2+(y-1)^2=1\), \((x+5)^2+(y-5)^2=25\)

            (2) \(x-y+3=0\)

            (3) \(\frac{9}{2}\)
            """
        ),
        solution=q(
            r"""
            (1) \(x\)축과 \(y\)축에 동시에 접하는 원의 중심은 \((-r,r)\) 꼴이다.
            따라서 반지름을 \(r\)이라 하면 원의 방정식은
            \[
            (x+r)^2+(y-r)^2=r^2
            \]
            이다.

            이 원이 점 \((-2,1)\)을 지나므로
            \[
            (-2+r)^2+(1-r)^2=r^2
            \]
            이다.

            정리하면
            \[
            r^2-6r+5=0
            \]
            \[
            (r-1)(r-5)=0
            \]
            이므로
            \[
            r=1 \quad \text{또는} \quad r=5
            \]
            이다.

            따라서 두 원의 방정식은
            \[
            (x+1)^2+(y-1)^2=1,
            \quad
            (x+5)^2+(y-5)^2=25
            \]
            이다.

            (2) 첫째 원을 전개하면
            \[
            x^2+y^2+2x-2y+1=0
            \]
            이고, 둘째 원을 전개하면
            \[
            x^2+y^2+10x-10y+25=0
            \]
            이다.

            두 식을 빼면
            \[
            8x-8y+24=0
            \]
            이므로 교점을 지나는 직선의 방정식은
            \[
            x-y+3=0
            \]
            이다.

            (3) \(x\)축과 만나는 점은
            \[
            A(-3,0)
            \]
            이고, \(y\)축과 만나는 점은
            \[
            B(0,3)
            \]
            이다.

            따라서 삼각형 \(OAB\)의 넓이는
            \[
            \frac12\cdot 3\cdot 3=\frac92
            \]
            이다.
            """
        ),
        level_hint=5,
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
    assets: List[str] = []
    if row.scan_source is not None:
        assets.append("assets/scan.png")
    assets.append(f"assets/original/{original_asset_name}")
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
    rect = _pdf_rect(crop)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def _write_problem(
    row: ProblemData,
    doc: fitz.Document,
    results: List[str],
    review_paths: List[str],
    warnings: List[str],
) -> None:
    folder = PROBLEMS / row.pid
    folder.mkdir(parents=True, exist_ok=False)

    assets_original = folder / "assets" / "original"
    assets_original.mkdir(parents=True, exist_ok=True)

    original_asset_name = f"{row.pid}_original.png"
    _render_crop(doc, row.crop, assets_original / original_asset_name)

    if row.scan_source is not None:
        if row.scan_source.exists():
            shutil.copyfile(row.scan_source, folder / "assets" / "scan.png")
        else:
            warnings.append(f"{row.pid}: scan source missing -> {row.scan_source}")

    front = _front_matter(row=row, original_asset_name=original_asset_name)
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{row.question.strip()}\n\n"
        f"## Choices\n{row.choices.strip()}\n\n"
        f"## Answer\n{row.answer.strip()}\n\n"
        f"## Solution\n{row.solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")

    results.append(
        f"{row.pid} | created | {original_asset_name}"
        + (" | scan=assets/scan.png" if row.scan_source is not None else "")
    )
    review_paths.append(str(folder / "problem.md"))


def main() -> int:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(SOURCE_PDF)

    doc = fitz.open(SOURCE_PDF)
    results: List[str] = []
    review_paths: List[str] = []
    duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []

    try:
        for row in DATA:
            folder = PROBLEMS / row.pid
            if folder.exists():
                duplicates.append(row.pid)
                results.append(f"{row.pid} | skipped | duplicate-folder")
                continue

            _write_problem(
                row=row,
                doc=doc,
                results=results,
                review_paths=review_paths,
                warnings=warnings,
            )
            if row.ocr_uncertain:
                uncertain.append(row.pid)
    finally:
        doc.close()

    created = sum(1 for item in results if "| created |" in item)
    skipped = sum(1 for item in results if "| skipped |" in item)
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
        *(uncertain or ["none"]),
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
