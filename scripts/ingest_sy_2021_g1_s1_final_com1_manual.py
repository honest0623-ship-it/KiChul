from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import shutil
import sys
import textwrap

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
SOURCE_PDF = ORIGINAL / "SY.2021.G1.S1.Final.COM1.pdf"
REPORT_PATH = ROOT / "_tmp_sy_2021_g1_s1_final_report.txt"

FIXED_META = {
    "school": "SY",
    "year": 2021,
    "grade": 1,
    "semester": 1,
    "exam": "Final",
    "source": "user_upload_2026-03-10",
}

RENDER_SCALE = 4.0

COM1_POLY = ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산")
COM1_COMPLEX = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식")
COM1_QF = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수")
COM1_EQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식")
COM1_INEQ = ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식")
COM2_COORD = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-1. 평면좌표")
COM2_LINE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식")
COM2_CIRCLE = ("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식")

FIGURE_HTML = (
    '<img src="assets/scan.png" alt="문항 삽화" '
    'style="width:60% !important; max-width:60% !important; height:auto; display:block; margin:12px auto;" />'
)


def q(text: str) -> str:
    return textwrap.dedent(text).strip()


def _box(lines: Sequence[str]) -> str:
    body = "<br/>".join(lines)
    return f'<div style="border:1px solid #333; padding:6px; margin:6px 0;">{body}</div>'


@dataclass(frozen=True)
class CropSpec:
    page: int
    box: Tuple[int, int, int, int]


@dataclass(frozen=True)
class ProblemData:
    pid: str
    source_no: int
    source_label: str
    qtype: str
    unit_triplet: Tuple[str, str, str]
    crop: CropSpec
    question: str
    choices: str
    answer: str
    solution: str
    level_hint: Optional[int] = None
    scan_source: Optional[str] = None
    ocr_uncertain: bool = False
    uncertain_note: str = ""


DATA: Sequence[ProblemData] = (
    ProblemData(
        pid="SY-2021-G1-S1-Final-001",
        source_no=1,
        source_label="1",
        qtype="객관식",
        unit_triplet=COM1_POLY,
        crop=CropSpec(0, (60, 620, 1410, 1750)),
        question=q(
            """
            삼차방정식
            \\[
            x^3-x^2+2x-1=0
            \\]
            의 세 근을 \\(\\alpha,\\ \\beta,\\ \\gamma\\)라 할 때,
            \\[
            \\frac{\\beta+\\gamma}{\\alpha}+\\frac{\\gamma+\\alpha}{\\beta}+\\frac{\\alpha+\\beta}{\\gamma}
            \\]
            의 값을 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(-4\\)
            ② \\(-3\\)
            ③ \\(-2\\)
            ④ \\(-1\\)
            ⑤ \\(0\\)
            """
        ),
        answer="④",
        solution=q(
            """
            근과 계수의 관계에서
            \\[
            \\alpha+\\beta+\\gamma=1,\\quad
            \\alpha\\beta+\\beta\\gamma+\\gamma\\alpha=2,\\quad
            \\alpha\\beta\\gamma=1
            \\]
            이다.

            따라서
            \\[
            \\frac{\\beta+\\gamma}{\\alpha}+\\frac{\\gamma+\\alpha}{\\beta}+\\frac{\\alpha+\\beta}{\\gamma}
            =\\left(\\alpha+\\beta+\\gamma\\right)
            \\left(\\frac{1}{\\alpha}+\\frac{1}{\\beta}+\\frac{1}{\\gamma}\\right)-3
            \\]
            이다.

            또
            \\[
            \\frac{1}{\\alpha}+\\frac{1}{\\beta}+\\frac{1}{\\gamma}
            =\\frac{\\alpha\\beta+\\beta\\gamma+\\gamma\\alpha}{\\alpha\\beta\\gamma}
            =\\frac{2}{1}=2
            \\]
            이므로
            \\[
            1\\cdot 2-3=-1
            \\]
            이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-002",
        source_no=2,
        source_label="2",
        qtype="객관식",
        unit_triplet=COM1_COMPLEX,
        crop=CropSpec(0, (60, 1650, 1410, 2700)),
        question=q(
            """
            방정식 \\(x^3=1\\)의 한 허근을 \\(\\omega\\)라 할 때, 다음 <보기>에서 옳은 것을 모두 고른 것은?

            """
        )
        + _box(
            [
                "ㄱ. \\(\\omega^2+\\omega+1=0\\)",
                "ㄴ. \\(\\omega^3+\\omega^6+\\dfrac{1}{\\omega^9}=3\\)",
                "ㄷ. \\(\\omega^{99}+\\omega^{100}=-\\omega\\)",
            ]
        ),
        choices=q(
            """
            ① ㄱ
            ② ㄱ, ㄴ
            ③ ㄱ, ㄷ
            ④ ㄴ, ㄷ
            ⑤ ㄱ, ㄴ, ㄷ
            """
        ),
        answer="②",
        solution=q(
            """
            \\(x^3=1\\)의 허근 \\(\\omega\\)는 \\(\\omega\\neq 1\\), \\(\\omega^3=1\\)을 만족한다.

            \\[
            x^3-1=(x-1)(x^2+x+1)
            \\]
            이므로 \\(\\omega\\)는
            \\[
            \\omega^2+\\omega+1=0
            \\]
            을 만족한다. 따라서 ㄱ은 옳다.

            또 \\(\\omega^3=1\\)이므로
            \\[
            \\omega^6=1,\\quad \\omega^9=1,\\quad \\frac{1}{\\omega^9}=1
            \\]
            이다. 따라서
            \\[
            \\omega^3+\\omega^6+\\frac{1}{\\omega^9}=1+1+1=3
            \\]
            이므로 ㄴ도 옳다.

            한편
            \\[
            \\omega^{99}+\\omega^{100}
            =(\\omega^3)^{33}+\\omega(\\omega^3)^{33}
            =1+\\omega
            =-\\omega^2
            \\]
            이다.
            그러므로 ㄷ은 옳지 않다.

            따라서 정답은 ②이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-003",
        source_no=3,
        source_label="3",
        qtype="객관식",
        unit_triplet=COM1_EQ,
        crop=CropSpec(0, (60, 2500, 1800, 3450)),
        question=q(
            """
            이차방정식
            \\[
            \\lvert x-1 \\rvert^2-2\\lvert x-1 \\rvert-3=0
            \\]
            의 모든 근의 합을 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(-4\\)
            ② \\(-2\\)
            ③ \\(0\\)
            ④ \\(2\\)
            ⑤ \\(4\\)
            """
        ),
        answer="④",
        solution=q(
            """
            \\[
            t=\\lvert x-1 \\rvert
            \\]
            라 두면 \\(t\\ge 0\\)이고 주어진 식은
            \\[
            t^2-2t-3=0
            \\]
            이다.

            인수분해하면
            \\[
            (t-3)(t+1)=0
            \\]
            이므로 \\(t=3\\)이다.
            \\(t=-1\\)은 \\(t\\ge 0\\)에 맞지 않는다.

            따라서
            \\[
            \\lvert x-1 \\rvert=3
            \\]
            이고,
            \\[
            x=4\\quad \\text{또는}\\quad x=-2
            \\]
            이다.

            그러므로 모든 근의 합은
            \\[
            4+(-2)=2
            \\]
            이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=2,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-004",
        source_no=4,
        source_label="4",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(0, (1480, 620, 2850, 1480)),
        question=q(
            """
            연립방정식
            \\[
            \\begin{cases}
            x+y=4 \\\\
            ax+2y=9
            \\end{cases}
            \\]
            의 근이
            \\[
            \\begin{cases}
            x-2y=b \\\\
            x^2+y^2=10
            \\end{cases}
            \\]
            을 만족시킬 때, 정수 \\(a,\\ b\\)에 대하여 \\(a-b\\)의 값을 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(8\\)
            ② \\(9\\)
            ③ \\(10\\)
            ④ \\(11\\)
            ⑤ \\(12\\)
            """
        ),
        answer="①",
        solution=q(
            """
            먼저
            \\[
            x+y=4
            \\]
            와
            \\[
            x^2+y^2=10
            \\]
            을 함께 만족하는 점을 구하자.

            \\[
            (x+y)^2=x^2+2xy+y^2
            \\]
            이므로
            \\[
            16=10+2xy
            \\]
            에서 \\(xy=3\\)이다.

            따라서 \\(x, y\\)는
            \\[
            t^2-4t+3=0
            \\]
            의 두 근이므로
            \\[
            (x,y)=(1,3)\\quad \\text{또는}\\quad (3,1)
            \\]
            이다.

            이제
            \\[
            ax+2y=9
            \\]
            에 대입한다.
            \\((1,3)\\)일 때는
            \\[
            a+6=9 \\Rightarrow a=3
            \\]
            이고,
            \\[
            b=x-2y=1-6=-5
            \\]
            이다.

            \\((3,1)\\)일 때는
            \\[
            3a+2=9 \\Rightarrow a=\\frac{7}{3}
            \\]
            이므로 정수 \\(a\\)가 아니다.

            따라서
            \\[
            a-b=3-(-5)=8
            \\]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-005",
        source_no=5,
        source_label="5",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (1480, 1250, 2850, 2300)),
        question=q(
            """
            부등식
            \\[
            (k+2)x^2-2(k+2)x+4>0
            \\]
            이 모든 실수 \\(x\\)에 대하여 항상 성립하기 위한 정수 \\(k\\)의 개수를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(1\\)개
            ② \\(2\\)개
            ③ \\(3\\)개
            ④ \\(4\\)개
            ⑤ \\(5\\)개
            """
        ),
        answer="④",
        solution=q(
            """
            \\[
            A=k+2
            \\]
            라 두면 주어진 부등식은
            \\[
            Ax^2-2Ax+4>0
            \\]
            이다.

            이 식이 모든 실수 \\(x\\)에 대하여 항상 성립하려면 다음 두 경우를 생각하면 된다.

            첫째, \\(A=0\\)이면 식은
            \\[
            4>0
            \\]
            이 되어 항상 성립한다.
            따라서
            \\[
            k=-2
            \\]
            는 가능하다.

            둘째, \\(A>0\\)이고 판별식이 음수이면 항상 양수이다.
            판별식 \\(\\Delta\\)는
            \\[
            \\Delta=(-2A)^2-4\\cdot A\\cdot 4
            =4A^2-16A
            =4A(A-4)
            \\]
            이다.

            따라서
            \\[
            A>0,\\quad \\Delta<0
            \\]
            이려면
            \\[
            0<A<4
            \\]
            이어야 한다.
            다시 \\(A=k+2\\)를 대입하면
            \\[
            -2<k<2
            \\]
            이고, 정수 \\(k\\)는
            \\[
            -1,\\ 0,\\ 1
            \\]
            이다.

            여기에 \\(k=-2\\)를 더하면 가능한 정수는 모두 4개이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-006",
        source_no=6,
        source_label="6",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (1480, 2100, 2850, 3200)),
        question=q(
            """
            부등식
            \\[
            x^2-2x-2<2\\lvert x-1 \\rvert
            \\]
            의 해가 \\(\\alpha<x<\\beta\\)일 때, \\(\\beta-\\alpha\\)의 값을 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(2\\)
            ② \\(3\\)
            ③ \\(4\\)
            ④ \\(5\\)
            ⑤ \\(6\\)
            """
        ),
        answer="⑤",
        solution=q(
            """
            절댓값 때문에 \\(x\\ge 1\\)인 경우와 \\(x<1\\)인 경우로 나누어 푼다.

            \\[
            x\\ge 1
            \\]
            일 때는 \\(\\lvert x-1 \\rvert=x-1\\)이므로
            \\[
            x^2-2x-2<2x-2
            \\]
            이고,
            \\[
            x^2-4x<0
            \\]
            이므로
            \\[
            0<x<4
            \\]
            이다.
            따라서 이 경우의 해는
            \\[
            1\\le x<4
            \\]
            이다.

            \\[
            x<1
            \\]
            일 때는 \\(\\lvert x-1 \\rvert=1-x\\)이므로
            \\[
            x^2-2x-2<-2x+2
            \\]
            이고,
            \\[
            x^2-4<0
            \\]
            이므로
            \\[
            -2<x<2
            \\]
            이다.
            따라서 이 경우의 해는
            \\[
            -2<x<1
            \\]
            이다.

            두 경우를 합치면 전체 해는
            \\[
            -2<x<4
            \\]
            이므로
            \\[
            \\alpha=-2,\\quad \\beta=4
            \\]
            이다.

            따라서
            \\[
            \\beta-\\alpha=4-(-2)=6
            \\]
            이다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-007",
        source_no=7,
        source_label="7",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(0, (1480, 3150, 2850, 4120)),
        question=q(
            """
            모든 실수 \\(x\\)에 대하여
            \\[
            \\frac{1}{\\sqrt{(m+1)x^2-(m+1)x+1}}
            \\]
            이 정의될 때, 실수 \\(m\\)의 값의 범위를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(-3<m<1\\)
            ② \\(-1\\le m<3\\)
            ③ \\(-1\\le m\\le 3\\)
            ④ \\(m<-1\\) 또는 \\(m>3\\)
            ⑤ \\(m\\le -1\\) 또는 \\(m>3\\)
            """
        ),
        answer="②",
        solution=q(
            """
            주어진 식이 모든 실수 \\(x\\)에서 정의되려면
            \\[
            (m+1)x^2-(m+1)x+1>0
            \\]
            이 모든 실수 \\(x\\)에 대하여 성립해야 한다.

            먼저
            \\[
            m+1=0
            \\]
            이면 식은
            \\[
            1>0
            \\]
            이 되어 항상 성립한다.
            따라서
            \\[
            m=-1
            \\]
            은 가능하다.

            다음으로 \\(m+1>0\\)일 때는 이차식이 항상 양수가 되려면 판별식이 음수여야 한다.
            판별식 \\(\\Delta\\)는
            \\[
            \\Delta=\\bigl(-(m+1)\\bigr)^2-4(m+1)
            =(m+1)^2-4(m+1)
            =(m+1)(m-3)
            \\]
            이다.

            따라서
            \\[
            \\Delta<0
            \\]
            이려면
            \\[
            -1<m<3
            \\]
            이다.

            위 두 경우를 합치면
            \\[
            -1\\le m<3
            \\]
            이다.

            따라서 정답은 ②이다.
            """
        ),
        level_hint=3,
        ocr_uncertain=True,
        uncertain_note="원문 문장 일부가 흐려 식의 의미를 자연스럽게 복원함.",
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-008",
        source_no=8,
        source_label="8",
        qtype="객관식",
        unit_triplet=COM1_QF,
        crop=CropSpec(1, (60, 620, 1410, 1530)),
        question=q(
            """
            이차함수 \\(y=kx^2\\)의 그래프가 직선
            \\[
            y=-4x+3-k
            \\]
            보다 아래쪽에 있을 때, 실수 \\(k\\)의 값의 범위를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(k<-1\\) 또는 \\(k>4\\)
            ② \\(-1<k<4\\)
            ③ \\(k<-1\\)
            ④ \\(0<k<4\\)
            ⑤ \\(0\\le k\\le 4\\)
            """
        ),
        answer="③",
        solution=q(
            """
            그래프가 직선보다 항상 아래쪽에 있으려면 모든 실수 \\(x\\)에 대하여
            \\[
            kx^2<-4x+3-k
            \\]
            이어야 한다.

            이를 옮기면
            \\[
            kx^2+4x+k-3<0
            \\]
            이다.

            이 이차식이 모든 실수 \\(x\\)에 대하여 항상 음수가 되려면
            \\[
            k<0
            \\]
            이고 판별식이 음수여야 한다.

            판별식 \\(\\Delta\\)는
            \\[
            \\Delta=4^2-4k(k-3)=16-4k^2+12k
            \\]
            이므로
            \\[
            \\Delta<0
            \\]
            에서
            \\[
            4-k^2+3k<0
            \\]
            이고,
            \\[
            k^2-3k-4>0
            \\]
            이다.

            인수분해하면
            \\[
            (k-4)(k+1)>0
            \\]
            이므로
            \\[
            k<-1\\quad \\text{또는}\\quad k>4
            \\]
            이다.

            그런데 이미 \\(k<0\\)이어야 하므로
            \\[
            k<-1
            \\]
            이다.

            따라서 정답은 ③이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-009",
        source_no=9,
        source_label="9",
        qtype="객관식",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(1, (60, 1500, 1410, 2400)),
        question=q(
            """
            연립부등식
            \\[
            \\begin{cases}
            x^2-(1+a)x+a<0 \\\\
            x^2-2x-3<0
            \\end{cases}
            \\]
            의 해가 \\(1<x<3\\)일 때, 실수 \\(a\\)의 값의 범위를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(1<a\\le 3\\)
            ② \\(a\\le 1\\) 또는 \\(a\\ge 3\\)
            ③ \\(a\\ge 3\\)
            ④ \\(a>3\\)
            ⑤ \\(a\\le 3\\)
            """
        ),
        answer="③",
        solution=q(
            """
            먼저
            \\[
            x^2-2x-3=(x+1)(x-3)
            \\]
            이므로
            \\[
            x^2-2x-3<0
            \\]
            의 해는
            \\[
            -1<x<3
            \\]
            이다.

            또
            \\[
            x^2-(1+a)x+a=(x-1)(x-a)
            \\]
            이므로
            \\[
            x^2-(1+a)x+a<0
            \\]
            의 해는 \\(1\\)과 \\(a\\) 사이의 구간이다.

            두 부등식의 공통해가 정확히
            \\[
            1<x<3
            \\]
            이 되어야 하므로, \\((x-1)(x-a)<0\\)의 해구간은 \\((1,3)\\)을 모두 포함해야 한다.
            따라서
            \\[
            a\\ge 3
            \\]
            이다.

            실제로 \\(a=3\\)이면 해는 \\(1<x<3\\)이고, \\(a>3\\)이어도 \\((-1,3)\\)과의 공통부분은 계속 \\((1,3)\\)이다.

            따라서 정답은 ③이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-010",
        source_no=10,
        source_label="10",
        qtype="객관식",
        unit_triplet=COM2_COORD,
        crop=CropSpec(1, (60, 2360, 1410, 4050)),
        question=q(
            """
            세 점 \\(A(-2,0)\\), \\(B(3,0)\\), \\(C(0,3)\\)을 꼭짓점으로 하는 삼각형 \\(ABC\\)가 있다.
            점 \\(P\\)가 변 \\(AB\\) 위를 움직일 때,
            \\[
            \\overline{AP}^2+\\overline{CP}^2
            \\]
            의 최솟값을 가질 때의 점 \\(P\\)의 좌표를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(P(-1,0)\\)
            ② \\(P(1,0)\\)
            ③ \\(P(0,0)\\)
            ④ \\(P(0,-1)\\)
            ⑤ \\(P(0,1)\\)
            """
        ),
        answer="①",
        solution=q(
            """
            점 \\(P\\)가 변 \\(AB\\) 위에 있으므로
            \\[
            P=(x,0)
            \\]
            라 둘 수 있다.
            이때 \\(-2\\le x\\le 3\\)이다.

            그러면
            \\[
            \\overline{AP}^2=(x+2)^2
            \\]
            이고
            \\[
            \\overline{CP}^2=x^2+9
            \\]
            이다.

            따라서
            \\[
            \\overline{AP}^2+\\overline{CP}^2
            =(x+2)^2+x^2+9
            =2x^2+4x+13
            \\]
            이다.

            완전제곱식을 만들면
            \\[
            2x^2+4x+13=2(x+1)^2+11
            \\]
            이므로 최솟값은 \\(x=-1\\)일 때이다.

            따라서 점 \\(P\\)의 좌표는
            \\[
            (-1,0)
            \\]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-011",
        source_no=11,
        source_label="11",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (1480, 620, 2850, 1720)),
        question=q(
            """
            다음 그림과 같이 세 직선
            \\[
            y=2x,\\quad y=\\frac{1}{5}x,\\quad y=-x+6
            \\]
            으로 둘러싸인 삼각형 \\(AOB\\)의 넓이를 구하시오.

            """
        )
        + "\n\n"
        + FIGURE_HTML,
        choices=q(
            """
            ① \\(3\\)
            ② \\(4\\)
            ③ \\(6\\)
            ④ \\(8\\)
            ⑤ \\(9\\)
            """
        ),
        answer="⑤",
        solution=q(
            """
            점 \\(A\\)는
            \\[
            y=2x
            \\]
            와
            \\[
            y=-x+6
            \\]
            의 교점이므로
            \\[
            2x=-x+6
            \\]
            에서
            \\[
            x=2,\\quad y=4
            \\]
            이다.
            따라서
            \\[
            A(2,4)
            \\]
            이다.

            점 \\(B\\)는
            \\[
            y=\\frac{1}{5}x
            \\]
            와
            \\[
            y=-x+6
            \\]
            의 교점이므로
            \\[
            \\frac{1}{5}x=-x+6
            \\]
            에서
            \\[
            6x=30,\\quad x=5,\\quad y=1
            \\]
            이다.
            따라서
            \\[
            B(5,1)
            \\]
            이다.

            원점 \\(O(0,0)\\)와 두 점 \\(A, B\\)로 이루어진 삼각형의 넓이는
            \\[
            \\frac{1}{2}\\left|2\\cdot 1-4\\cdot 5\\right|
            =\\frac{1}{2}\\cdot 18
            =9
            \\]
            이다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=3,
        scan_source="SY.2021.G1.S1.Final.COM1.011.png",
        ocr_uncertain=True,
        uncertain_note="삽화의 기울기 표기는 별도 그림과 보기의 정합성을 기준으로 1/5로 복원함.",
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-012",
        source_no=12,
        source_label="12",
        qtype="객관식",
        unit_triplet=COM2_LINE,
        crop=CropSpec(1, (1480, 1700, 2850, 2850)),
        question=q(
            """
            두 직선
            \\[
            x+2y-2=0,\\quad mx-y+2m-1=0
            \\]
            이 제1사분면에서 만날 때, 상수 \\(m\\)의 값의 범위를 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(m=\\dfrac{1}{4}\\) 또는 \\(m=1\\)
            ② \\(m<\\dfrac{1}{4}\\) 또는 \\(m>1\\)
            ③ \\(\\dfrac{1}{4}\\le m\\le 1\\)
            ④ \\(m\\le \\dfrac{1}{4}\\) 또는 \\(m\\ge 1\\)
            ⑤ \\(\\dfrac{1}{4}<m<1\\)
            """
        ),
        answer="⑤",
        solution=q(
            """
            첫째 직선에서
            \\[
            x=2-2y
            \\]
            이다.

            이를 둘째 직선에 대입하면
            \\[
            m(2-2y)-y+2m-1=0
            \\]
            이고,
            \\[
            (2m+1)y=4m-1
            \\]
            이므로
            \\[
            y=\\frac{4m-1}{2m+1}
            \\]
            이다.

            또
            \\[
            x=2-2y
            =2-2\\cdot\\frac{4m-1}{2m+1}
            =\\frac{4(1-m)}{2m+1}
            \\]
            이다.

            제1사분면에서 만나려면
            \\[
            x>0,\\quad y>0
            \\]
            이어야 한다.

            \\(2m+1>0\\)인 경우에
            \\[
            4m-1>0,\\quad 1-m>0
            \\]
            이어야 하므로
            \\[
            m>\\frac{1}{4},\\quad m<1
            \\]
            이다.

            \\(2m+1<0\\)인 경우에는 두 부등식을 동시에 만족시킬 수 없다.

            따라서
            \\[
            \\frac{1}{4}<m<1
            \\]
            이다.

            따라서 정답은 ⑤이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-013",
        source_no=13,
        source_label="13",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(1, (1480, 2800, 2850, 4050)),
        question=q(
            """
            방정식
            \\[
            x^2+y^2-2y+A-2=0
            \\]
            이 원을 나타내도록 하는 정수 \\(A\\)의 최댓값을 구하시오.
            """
        ),
        choices=q(
            """
            ① \\(-1\\)
            ② \\(0\\)
            ③ \\(1\\)
            ④ \\(2\\)
            ⑤ \\(3\\)
            """
        ),
        answer="④",
        solution=q(
            """
            식을 정리하면
            \\[
            x^2+(y-1)^2=3-A
            \\]
            이다.

            이 식이 원을 나타내려면 반지름의 제곱이 양수여야 하므로
            \\[
            3-A>0
            \\]
            이어야 한다.

            따라서
            \\[
            A<3
            \\]
            이다.

            보기 중에서 이를 만족하는 정수의 최댓값은
            \\[
            2
            \\]
            이다.

            따라서 정답은 ④이다.
            """
        ),
        level_hint=2,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-014",
        source_no=14,
        source_label="14",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (60, 620, 1410, 1750)),
        question=q(
            """
            원
            \\[
            x^2+y^2-2x-4ay+b=0
            \\]
            이 점 \\((-3,4)\\)를 지나고 \\(x\\)축에 접할 때, \\(a+b\\)의 값을 구하시오.
            \\(\\text{단, } a, b\\text{는 상수이다.}\\)
            """
        ),
        choices=q(
            """
            ① \\(1\\)
            ② \\(3\\)
            ③ \\(5\\)
            ④ \\(7\\)
            ⑤ \\(9\\)
            """
        ),
        answer="②",
        solution=q(
            """
            식을 완전제곱식으로 고치면
            \\[
            (x-1)^2+(y-2a)^2=4a^2-b+1
            \\]
            이다.

            따라서 원의 중심은
            \\[
            (1, 2a)
            \\]
            이고, 반지름의 제곱은
            \\[
            4a^2-b+1
            \\]
            이다.

            이 원이 \\(x\\)축에 접하므로 반지름은 중심의 \\(y\\)좌표의 절댓값과 같다.
            따라서
            \\[
            4a^2-b+1=(2a)^2
            \\]
            이고,
            \\[
            b=1
            \\]
            이다.

            또 점 \\((-3,4)\\)를 지나므로
            \\[
            (-3-1)^2+(4-2a)^2=4a^2
            \\]
            이다.
            즉
            \\[
            16+(4-2a)^2=4a^2
            \\]
            이고,
            \\[
            16+16-16a+4a^2=4a^2
            \\]
            이므로
            \\[
            32-16a=0,\\quad a=2
            \\]
            이다.

            따라서
            \\[
            a+b=2+1=3
            \\]
            이다.

            따라서 정답은 ②이다.
            """
        ),
        level_hint=3,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-015",
        source_no=15,
        source_label="15",
        qtype="객관식",
        unit_triplet=COM2_CIRCLE,
        crop=CropSpec(2, (60, 1450, 2850, 2500)),
        question=q(
            """
            오른쪽 그림과 같이 원
            \\[
            (x-4)^2+(y-3)^2=25
            \\]
            위의 두 점 \\(A(-1,3)\\), \\(B(4,-2)\\)가 있다.
            원 위의 한 점 \\(P\\)에 대하여 삼각형 \\(PAB\\)의 넓이가 최대가 될 때,
            점 \\(P\\)와 원의 중심을 지나는 직선의 방정식을 구하시오.

            """
        )
        + "\n\n"
        + FIGURE_HTML,
        choices=q(
            """
            ① \\(y=x-1\\)
            ② \\(y=-x-1\\)
            ③ \\(y=\\dfrac{1}{2}x-1\\)
            ④ \\(y=-2x-1\\)
            ⑤ \\(y=-\\dfrac{1}{2}x-1\\)
            """
        ),
        answer="①",
        solution=q(
            """
            삼각형 \\(PAB\\)의 넓이는
            \\[
            \\frac{1}{2}\\times AB\\times \\text{점 }P\\text{에서 직선 }AB\\text{까지의 거리}
            \\]
            이다.

            여기서 \\(AB\\)의 길이는 일정하므로, 넓이가 최대가 되려면 점 \\(P\\)에서 직선 \\(AB\\)까지의 거리가 최대가 되어야 한다.
            원 위의 점에서 한 직선까지의 거리가 최대가 되는 점은 원의 중심을 지나면서 그 직선에 수직인 지름 위에 있다.

            따라서 중심과 점 \\(P\\)를 지나는 직선은 직선 \\(AB\\)에 수직이다.

            두 점 \\(A(-1,3)\\), \\(B(4,-2)\\)를 지나는 직선 \\(AB\\)의 기울기는
            \\[
            \\frac{-2-3}{4-(-1)}=-1
            \\]
            이다.

            그러므로 이에 수직인 직선의 기울기는
            \\[
            1
            \\]
            이다.

            원의 중심은
            \\[
            (4,3)
            \\]
            이므로, 구하는 직선은
            \\[
            y-3=1(x-4)
            \\]
            이다.

            따라서
            \\[
            y=x-1
            \\]
            이다.

            따라서 정답은 ①이다.
            """
        ),
        level_hint=3,
        scan_source="SY.2021.G1.S1.Final.COM1.015.png",
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-101",
        source_no=1,
        source_label="단답1",
        qtype="단답형",
        unit_triplet=COM1_POLY,
        crop=CropSpec(2, (60, 2750, 1450, 4050)),
        question=q(
            """
            서로 다른 세 실수 \\(\\alpha,\\ \\beta,\\ \\gamma\\)에 대하여 삼차식
            \\[
            f(x)=x^3-4x^2-10x+1
            \\]
            이
            \\[
            f(\\alpha)=f(\\beta)=f(\\gamma)=-3
            \\]
            을 만족시킬 때,
            \\[
            \\alpha^2+\\beta^2+\\gamma^2
            \\]
            의 값을 구하시오.
            """
        ),
        choices="",
        answer="36",
        solution=q(
            """
            \\[
            f(\\alpha)=f(\\beta)=f(\\gamma)=-3
            \\]
            이므로 \\(\\alpha, \\beta, \\gamma\\)는 모두 방정식
            \\[
            x^3-4x^2-10x+1=-3
            \\]
            의 근이다.

            따라서
            \\[
            x^3-4x^2-10x+4=0
            \\]
            의 세 근이 \\(\\alpha,\\beta,\\gamma\\)이다.

            근과 계수의 관계에서
            \\[
            \\alpha+\\beta+\\gamma=4,\\quad
            \\alpha\\beta+\\beta\\gamma+\\gamma\\alpha=-10
            \\]
            이다.

            그러므로
            \\[
            \\alpha^2+\\beta^2+\\gamma^2
            =(\\alpha+\\beta+\\gamma)^2-2(\\alpha\\beta+\\beta\\gamma+\\gamma\\alpha)
            \\]
            이고,
            \\[
            4^2-2(-10)=16+20=36
            \\]
            이다.

            따라서 답은 \\(36\\)이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-102",
        source_no=2,
        source_label="단답2",
        qtype="단답형",
        unit_triplet=COM2_COORD,
        crop=CropSpec(2, (1480, 620, 2850, 2450)),
        question=q(
            """
            오른쪽 그림과 같이 점 \\(P\\)는 점 \\(A(8,0)\\)에서 매초 \\(1\\)의 속력으로 \\(x\\)축을 따라 왼쪽으로 움직이고,
            점 \\(Q\\)는 점 \\(B(0,4)\\)에서 매초 \\(3\\)의 속력으로 \\(y\\)축을 따라 아래로 움직인다.
            두 점 \\(P, Q\\)가 동시에 출발할 때, 두 점 \\(P, Q\\) 사이의 거리의 최솟값을 구하시오.

            """
        )
        + "\n\n"
        + FIGURE_HTML,
        choices="",
        answer="\\(2\\sqrt{10}\\)",
        solution=q(
            """
            출발 후 \\(t\\)초 뒤의 점의 좌표를 구하면
            \\[
            P(8-t, 0),\\quad Q(0, 4-3t)
            \\]
            이다.

            두 점 사이의 거리의 제곱을 \\(D^2\\)라 하면
            \\[
            D^2=(8-t)^2+(4-3t)^2
            \\]
            이다.

            이를 정리하면
            \\[
            D^2=t^2-16t+64+9t^2-24t+16
            =10t^2-40t+80
            \\]
            이고,
            \\[
            D^2=10(t-2)^2+40
            \\]
            이다.

            따라서 \\(D^2\\)의 최솟값은 \\(40\\)이고, 거리 \\(D\\)의 최솟값은
            \\[
            \\sqrt{40}=2\\sqrt{10}
            \\]
            이다.

            따라서 답은 \\(2\\sqrt{10}\\)이다.
            """
        ),
        level_hint=4,
        scan_source="SY.2021.G1.S1.Final.COM1.서답2번.png",
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-103",
        source_no=1,
        source_label="서술1",
        qtype="서술형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(2, (1480, 2450, 2850, 4050)),
        question=q(
            """
            세 직선
            \\[
            x-y=0,\\quad 2x+y=0,\\quad x+2y-3=0
            \\]
            으로 둘러싸인 삼각형의 외접원의 반지름의 길이를 구하시오.
            """
        ),
        choices="",
        answer="\\(\\dfrac{5\\sqrt{2}}{6}\\)",
        solution=q(
            """
            세 직선의 교점을 차례로 구하면 삼각형의 세 꼭짓점은 다음과 같다.

            \\[
            x-y=0,\\ 2x+y=0
            \\]
            의 교점은
            \\[
            (0,0)
            \\]
            이다.

            \\[
            x-y=0,\\ x+2y-3=0
            \\]
            의 교점은
            \\[
            (1,1)
            \\]
            이다.

            \\[
            2x+y=0,\\ x+2y-3=0
            \\]
            의 교점은
            \\[
            (-1,2)
            \\]
            이다.

            이제 외접원의 중심을 구하기 위해 두 변의 수직이등분선을 구한다.

            점 \\((0,0)\\)과 점 \\((1,1)\\)의 중점은
            \\[
            \\left(\\frac{1}{2},\\frac{1}{2}\\right)
            \\]
            이고, 이 선분의 기울기는 \\(1\\)이므로 수직이등분선의 기울기는 \\(-1\\)이다.
            따라서 그 방정식은
            \\[
            y=-x+1
            \\]
            이다.

            점 \\((0,0)\\)과 점 \\((-1,2)\\)의 중점은
            \\[
            \\left(-\\frac{1}{2},1\\right)
            \\]
            이고, 이 선분의 기울기는 \\(-2\\)이므로 수직이등분선의 기울기는 \\(\\frac{1}{2}\\)이다.
            따라서 그 방정식은
            \\[
            y-1=\\frac{1}{2}\\left(x+\\frac{1}{2}\\right)
            \\]
            이다.

            두 수직이등분선의 교점을 구하면 외심은
            \\[
            \\left(-\\frac{1}{6},\\frac{7}{6}\\right)
            \\]
            이다.

            따라서 외접원의 반지름 \\(R\\)은
            \\[
            R^2=\\left(-\\frac{1}{6}\\right)^2+\\left(\\frac{7}{6}\\right)^2
            =\\frac{1}{36}+\\frac{49}{36}
            =\\frac{25}{18}
            \\]
            이므로
            \\[
            R=\\sqrt{\\frac{25}{18}}=\\frac{5\\sqrt{2}}{6}
            \\]
            이다.

            따라서 외접원의 반지름의 길이는
            \\[
            \\frac{5\\sqrt{2}}{6}
            \\]
            이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-104",
        source_no=2,
        source_label="서술2",
        qtype="서술형",
        unit_triplet=COM2_LINE,
        crop=CropSpec(3, (60, 620, 1410, 4050)),
        question=q(
            """
            세 직선
            \\[
            x+2y-6=0,\\quad 4x-3y-12=0,\\quad ax+y-1=0
            \\]
            으로 이루어지는 삼각형이 직각삼각형일 때, 모든 상수 \\(a\\)의 값의 합을 구하시오.
            """
        ),
        choices="",
        answer="\\(-\\dfrac{5}{4}\\)",
        solution=q(
            """
            세 직선의 기울기를 각각 구하면
            \\[
            x+2y-6=0 \\Rightarrow y=-\\frac{1}{2}x+3
            \\]
            이므로 기울기는
            \\[
            -\\frac{1}{2}
            \\]
            이다.

            또
            \\[
            4x-3y-12=0 \\Rightarrow y=\\frac{4}{3}x-4
            \\]
            이므로 기울기는
            \\[
            \\frac{4}{3}
            \\]
            이다.

            마지막 직선은
            \\[
            ax+y-1=0 \\Rightarrow y=-ax+1
            \\]
            이므로 기울기는
            \\[
            -a
            \\]
            이다.

            직각삼각형이 되려면 세 직선 중 어느 두 직선이 서로 수직이어야 한다.

            첫째 직선과 셋째 직선이 수직이면
            \\[
            -\\frac{1}{2}\\cdot(-a)=-1
            \\]
            이므로
            \\[
            a=-2
            \\]
            이다.

            둘째 직선과 셋째 직선이 수직이면
            \\[
            \\frac{4}{3}\\cdot(-a)=-1
            \\]
            이므로
            \\[
            a=\\frac{3}{4}
            \\]
            이다.

            첫째 직선과 둘째 직선은
            \\[
            -\\frac{1}{2}\\cdot\\frac{4}{3}=-\\frac{2}{3}
            \\]
            이므로 서로 수직이 아니다.

            따라서 가능한 모든 \\(a\\)의 값의 합은
            \\[
            -2+\\frac{3}{4}
            =-\\frac{8}{4}+\\frac{3}{4}
            =-\\frac{5}{4}
            \\]
            이다.

            따라서 답은
            \\[
            -\\frac{5}{4}
            \\]
            이다.
            """
        ),
        level_hint=4,
    ),
    ProblemData(
        pid="SY-2021-G1-S1-Final-105",
        source_no=3,
        source_label="서술3",
        qtype="서술형",
        unit_triplet=COM1_INEQ,
        crop=CropSpec(3, (1480, 620, 2850, 4050)),
        question=q(
            """
            세 실수 \\(x,\\ x+1,\\ x+2\\)가 둔각삼각형의 세 변의 길이가 되도록 하는 \\(x\\)의 값의 범위와
            이차부등식
            \\[
            ax^2+bx-3>0
            \\]
            의 해가 서로 같을 때, 상수 \\(a,\\ b\\)에 대하여 \\(a-b\\)의 값을 구하시오.
            """
        ),
        choices="",
        answer="\\(-5\\)",
        solution=q(
            """
            세 변의 길이가
            \\[
            x,\\quad x+1,\\quad x+2
            \\]
            이므로 가장 긴 변은 \\(x+2\\)이다.

            먼저 삼각형이 되려면
            \\[
            x+(x+1)>x+2
            \\]
            이어야 하므로
            \\[
            x>1
            \\]
            이다.

            또 둔각삼각형이 되려면 가장 긴 변에 대하여
            \\[
            x^2+(x+1)^2<(x+2)^2
            \\]
            이어야 한다.

            이를 정리하면
            \\[
            2x^2+2x+1<x^2+4x+4
            \\]
            이고,
            \\[
            x^2-2x-3<0
            \\]
            이다.

            인수분해하면
            \\[
            (x-3)(x+1)<0
            \\]
            이므로
            \\[
            -1<x<3
            \\]
            이다.

            따라서 둔각삼각형의 세 변의 길이가 되도록 하는 \\(x\\)의 범위는
            \\[
            1<x<3
            \\]
            이다.

            이제
            \\[
            ax^2+bx-3>0
            \\]
            의 해가 정확히 \\(1<x<3\\)와 같아야 하므로,
            이 이차식은 \\(x=1\\), \\(x=3\\)에서 0이 되고 그 사이에서 양수여야 한다.

            따라서
            \\[
            ax^2+bx-3=a(x-1)(x-3)
            \\]
            이고, 사이에서 양수이려면 \\(a<0\\)이다.

            또 상수항을 비교하면
            \\[
            3a=-3
            \\]
            이므로
            \\[
            a=-1
            \\]
            이다.

            따라서
            \\[
            ax^2+bx-3=-(x-1)(x-3)=-x^2+4x-3
            \\]
            이고,
            \\[
            b=4
            \\]
            이다.

            그러므로
            \\[
            a-b=-1-4=-5
            \\]
            이다.

            따라서 답은 \\(-5\\)이다.
            """
        ),
        level_hint=4,
    ),
)


def _render_pages() -> Dict[int, Image.Image]:
    doc = fitz.open(SOURCE_PDF)
    rendered: Dict[int, Image.Image] = {}
    try:
        for idx, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            rendered[idx] = image.rotate(90, expand=True)
    finally:
        doc.close()
    return rendered


def _problem_no_for_classifier(row: ProblemData) -> int:
    if row.qtype == "객관식":
        return row.source_no
    return 100 + row.source_no


def _level_for(row: ProblemData) -> int:
    result = classify_unit_and_level(
        question_text=row.question,
        choices_text=row.choices,
        answer_text=row.answer,
        solution_text=row.solution,
        qtype=row.qtype,
        grade=FIXED_META["grade"],
        problem_no=_problem_no_for_classifier(row),
    )
    level = int(result.level)
    if row.qtype in {"단답형", "서술형"} and level < 4:
        level = 4
    if row.level_hint is not None:
        level = max(level, row.level_hint)
    return max(1, min(5, level))


def _subject_from_unit(unit_triplet: Tuple[str, str, str]) -> str:
    unit_l1, _, _ = normalize_unit_triplet(*unit_triplet)
    if unit_l1.startswith("공통수학1"):
        return "COM1"
    if unit_l1.startswith("공통수학2"):
        return "COM2"
    if unit_l1.startswith("대수"):
        return "ALG"
    if unit_l1.startswith("미적분"):
        return "CAL1"
    if unit_l1.startswith("확률과 통계"):
        return "STAT"
    return "COM1"


def _front_matter(row: ProblemData, original_asset_name: str) -> Dict[str, object]:
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
        "subject": _subject_from_unit(row.unit_triplet),
        "type": row.qtype,
        "source_question_no": row.source_no,
        "source_question_kind": "objective" if row.qtype == "객관식" else "subjective",
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
            f"과목-{_subject_from_unit(row.unit_triplet)}",
        ],
        "assets": assets,
    }


def _body(row: ProblemData) -> str:
    parts = [
        "## Q",
        row.question.strip(),
        "",
        "## Choices",
        row.choices.strip(),
        "",
        "## Answer",
        row.answer.strip(),
        "",
        "## Solution",
        row.solution.strip(),
        "",
    ]
    return "\n".join(parts)


def _write_problem(folder: Path, row: ProblemData, rendered_pages: Dict[int, Image.Image]) -> None:
    assets_dir = folder / "assets"
    original_dir = assets_dir / "original"
    original_dir.mkdir(parents=True, exist_ok=True)

    original_asset_name = f"{row.pid}_original.png"
    crop_image = rendered_pages[row.crop.page].crop(row.crop.box)
    crop_image.save(original_dir / original_asset_name)

    if row.scan_source is not None:
        shutil.copy2(ORIGINAL / row.scan_source, assets_dir / "scan.png")

    front = _front_matter(row=row, original_asset_name=original_asset_name)
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = _body(row)
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def run() -> int:
    if not SOURCE_PDF.exists():
        print(f"[ERROR] missing-pdf: {SOURCE_PDF}")
        return 1

    for row in DATA:
        if row.scan_source is not None and not (ORIGINAL / row.scan_source).exists():
            print(f"[ERROR] missing-scan: {ORIGINAL / row.scan_source}")
            return 1

    rendered_pages = _render_pages()

    created = 0
    updated = 0
    skipped = 0
    warnings = 0
    report_lines: List[str] = []
    duplicates: List[str] = []
    uncertain: List[str] = []
    review_paths: List[str] = []

    for row in DATA:
        folder = PROBLEMS / row.pid
        if folder.exists():
            skipped += 1
            duplicates.append(row.pid)
            report_lines.append(f"{row.pid} | SKIP | duplicate-folder")
            continue

        _write_problem(folder=folder, row=row, rendered_pages=rendered_pages)
        created += 1
        review_paths.append(str((folder / "problem.md").resolve()))

        note_parts = [f"type={row.qtype}", f"unit={'>'.join(normalize_unit_triplet(*row.unit_triplet))}"]
        if row.scan_source is not None:
            note_parts.append(f"scan={row.scan_source}")
        report_lines.append(f"{row.pid} | CREATE | {' | '.join(note_parts)}")

        if row.ocr_uncertain:
            warnings += 1
            uncertain.append(f"{row.pid}: {row.uncertain_note}")

    summary_lines = [
        "=== SUMMARY ===",
        f"created: {created}",
        f"updated: {updated}",
        f"skipped: {skipped}",
        f"warnings: {warnings}",
        "",
        "=== PER_FILE ===",
        *report_lines,
        "",
        "=== DUPLICATE_FOLDERS ===",
        *(duplicates or ["none"]),
        "",
        "=== OCR_OR_FORMULA_UNCERTAIN ===",
        *(uncertain or ["none"]),
        "",
        "=== REVIEW_PATHS ===",
        *(review_paths or ["none"]),
    ]

    REPORT_PATH.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
