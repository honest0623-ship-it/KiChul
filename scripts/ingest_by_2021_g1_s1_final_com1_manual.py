from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level


ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

PDF_NAME = "BY.2021.G1.S1.Final.COM1.pdf"
SUP_SCAN_NAME = "BN.2021.G1.S1.Final.COM1.006.png"


@dataclass(frozen=True)
class Row:
    no: int
    kind: str  # objective | subjective
    q: str
    choices: Sequence[str]
    answer: str
    solution: str
    use_scan: bool = False
    ocr_uncertain: bool = False
    uncertain_note: str = ""


DATA: List[Row] = [
    Row(
        no=1,
        kind="objective",
        q=r"다음 방정식 \(x^3-6x^2-x+6=0\)의 해는?",
        choices=(
            r"\(x=-1\) 또는 \(x=1\) 또는 \(x=6\)",
            r"\(x=-1\) 또는 \(x=1\) 또는 \(x=2\)",
            r"\(x=1\) 또는 \(x=2\) 또는 \(x=3\)",
            r"\(x=1\) 또는 \(x=-2\) 또는 \(x=6\)",
            r"\(x=6\) 또는 \(x=1\)",
        ),
        answer="①",
        solution=(
            r"$x^3-6x^2-x+6=(x^2-1)(x-6)=(x-1)(x+1)(x-6)$ 이므로 "
            r"해는 \(-1,1,6\)이다."
        ),
    ),
    Row(
        no=2,
        kind="objective",
        q=r"다음 이차부등식 \(x^2-7x+6<0\)의 해가 \(\alpha<x<\beta\)일 때, \(\alpha+\beta\)의 값은?",
        choices=(r"8", r"7", r"6", r"-6", r"-7"),
        answer="②",
        solution=(
            r"$x^2-7x+6=(x-1)(x-6)$ 이므로 해는 \(1<x<6\)이다. "
            r"따라서 \(\alpha+\beta=1+6=7\)이다."
        ),
    ),
    Row(
        no=3,
        kind="objective",
        q=(
            r"두 점 \(A(-2,3)\), \(B(4,-7)\)을 지름의 양 끝으로 하는 원의 방정식이 "
            r"\((x+a)^2+(y+b)^2=c\)일 때, 세 상수 \(a,b,c\)의 합 \(a+b+c\)의 값은?"
        ),
        choices=(r"17", r"26", r"28", r"35", r"37"),
        answer="④",
        solution=(
            r"중점은 \((1,-2)\)이고 반지름의 제곱은 "
            r"\(\frac{(4+2)^2+(-7-3)^2}{4}=34\)이다. "
            r"원은 \((x-1)^2+(y+2)^2=34\)이므로 \(a=-1,b=2,c=34\)이다. "
            r"따라서 \(a+b+c=35\)이다."
        ),
    ),
    Row(
        no=4,
        kind="objective",
        q=(
            r"두 점 \(A(2,-3)\), \(B(-7,3)\)에 대하여 선분 \(AB\)를 \(2:1\)로 내분하는 점을 \(P\), "
            r"선분 \(AB\)를 \(2:1\)로 외분하는 점을 \(Q\)라 할 때, \(P,Q\)의 중점의 좌표는?"
        ),
        choices=(
            r"\((-8,-4)\)",
            r"\((-8,-2)\)",
            r"\((-10,2)\)",
            r"\((-10,4)\)",
            r"\((-10,5)\)",
        ),
        answer="⑤",
        solution=(
            r"\(P=\frac{1\cdot A+2\cdot B}{3}=(-4,1)\), "
            r"\(Q=2B-A=(-16,9)\)이므로 "
            r"중점은 \(\left(\frac{-4-16}{2},\frac{1+9}{2}\right)=(-10,5)\)이다."
        ),
    ),
    Row(
        no=5,
        kind="objective",
        q=(
            r"직선 \(y=x\) 위의 점 \(P\)에서 두 점 \(A(0,5)\), \(B(1,6)\)까지의 거리가 각각 같을 때, "
            r"점 \(P\)의 좌표는?"
        ),
        choices=(r"\((-1,-1)\)", r"\((0,0)\)", r"\((1,1)\)", r"\((2,2)\)", r"\((3,3)\)"),
        answer="⑤",
        solution=(
            r"\(PA=PB\)인 점의 자취는 \(AB\)의 수직이등분선이다. "
            r"\(AB\)의 중점은 \(\left(\frac12,\frac{11}{2}\right)\), 기울기는 \(1\)이므로 수직이등분선은 "
            r"\(y=-x+6\)이다. 직선 \(y=x\)와의 교점은 \((3,3)\)이다."
        ),
    ),
    Row(
        no=6,
        kind="objective",
        q=(
            r"다음 그림과 같이 세 점 \(A(-4,2)\), \(B(2,4)\), \(C(-2,-2)\)를 꼭짓점으로 하는 "
            r"삼각형 \(ABC\)의 넓이는?"
            "\n\n"
            '<img src="assets/scan.png" alt="문항 삽화" '
            'style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices=(r"12", r"14", r"16", r"18", r"20"),
        answer="②",
        solution=(
            r"\(\overrightarrow{AB}=(6,2)\), \(\overrightarrow{AC}=(2,-4)\)이므로 "
            r"넓이는 "
            r"\(\frac12\left|6\cdot(-4)-2\cdot2\right|=\frac12\cdot28=14\)이다."
        ),
        use_scan=True,
    ),
    Row(
        no=7,
        kind="objective",
        q=r"다음 연립부등식 \(2x-3\le x+1<3x-5\)의 해는?",
        choices=(r"\(3<x\le4\)", r"\(3\le x<4\)", r"\(-4<x\le3\)", r"\(-4\le x<3\)", r"\(-3<x\le4\)"),
        answer="①",
        solution=(
            r"\(2x-3\le x+1\)에서 \(x\le4\), "
            r"\(x+1<3x-5\)에서 \(x>3\)이므로 "
            r"해는 \(3<x\le4\)이다."
        ),
    ),
    Row(
        no=8,
        kind="objective",
        q=r"원 \(x^2+y^2=5\)와 직선 \(y=2x+m\)가 서로 다른 두 점에서 만나도록 하는 정수 \(m\)의 개수는?",
        choices=(r"8", r"9", r"10", r"11", r"12"),
        answer="②",
        solution=(
            r"직선을 \(2x-y+m=0\)이라 두면 원의 중심 \((0,0)\)에서 직선까지 거리는 "
            r"\(\frac{|m|}{\sqrt5}\)이다. 서로 다른 두 점에서 만나려면 "
            r"\(\frac{|m|}{\sqrt5}<\sqrt5\), 즉 \(|m|<5\)이다. "
            r"정수 \(m\)은 \(-4,-3,\dots,4\)로 \(9\)개이다."
        ),
    ),
    Row(
        no=9,
        kind="objective",
        q=r"부등식 \(|x+1|-2|x-2|\ge3\)을 만족시키는 정수 \(x\)의 개수는?",
        choices=(r"1", r"2", r"3", r"4", r"5"),
        answer="①",
        solution=(
            r"구간을 나누어 계산하면 \(x\ge2\)에서 식은 \(5-x\), "
            r"\(-1\le x<2\)에서 \(3x-3\), \(x<-1\)에서 \(x-5\)가 된다. "
            r"조건을 만족하는 정수는 \(x=2\) 하나뿐이다."
        ),
    ),
    Row(
        no=10,
        kind="objective",
        q=r"원 \((x-2)^2+y^2=9\)와 직선 \(mx-y+3m+3=0\)이 제1사분면에서 만나도록 하는 실수 \(m\)의 범위는?",
        choices=(
            r"\(-\frac14\le m<0\)",
            r"\(-\frac14<m\le0\)",
            r"\(-\frac38<m\le0\)",
            r"\(-\frac38\le m<0\)",
            r"\(-\frac12\le m<0\)",
        ),
        answer="③",
        solution=(
            r"중심 \((2,0)\)에서 직선까지 거리 조건으로 "
            r"\(\frac{|5m+3|}{\sqrt{m^2+1}}\le3\)를 얻고, 교점의 \(y>0\) 조건을 함께 보면 "
            r"경계 \(m=-\frac38\)에서는 \(x\)축 위 점에서만 만나므로 제외된다. "
            r"따라서 \(-\frac38<m\le0\)이다."
        ),
        ocr_uncertain=True,
        uncertain_note="보기 ⑤의 끝 부분 OCR 가독성 낮음(정답에는 영향 없음).",
    ),
    Row(
        no=11,
        kind="objective",
        q=r"두 직선 \(4x+y-3=0\), \(x-4y+3=0\)이 이루는 각의 이등분선의 방정식은?",
        choices=(
            r"\(3x+5y+6=0\)",
            r"\(3x-5y+6=0\)",
            r"\(3x-5y-6=0\)",
            r"\(5x-3y=0\)",
            r"\(x+3y=0\)",
        ),
        answer="④",
        solution=(
            r"이등분선 조건은 "
            r"\(\frac{|4x+y-3|}{\sqrt{17}}=\frac{|x-4y+3|}{\sqrt{17}}\)이다. "
            r"따라서 "
            r"\(4x+y-3=\pm(x-4y+3)\)이고, 여기서 "
            r"\(5x-3y=0\)을 얻는다. 보기와 일치하는 것은 ④이다."
        ),
        ocr_uncertain=True,
        uncertain_note="보기 ① 상수항 부호 OCR 가독성 낮음(정답에는 영향 없음).",
    ),
    Row(
        no=12,
        kind="objective",
        q=(
            r"두 이차함수 \(f(x)=x^2+3x-2\), \(g(x)=-x^2+3x+k+1\)가 있다. "
            r"\(-2\le x\le2\)인 모든 실수 \(x\)에 대하여 \(f(x)\le g(x)\)를 만족시키는 실수 \(k\)의 최솟값은?"
        ),
        choices=(r"3", r"4", r"5", r"6", r"7"),
        answer="③",
        solution=(
            r"\(f(x)\le g(x)\)는 \(2x^2\le k+3\), 즉 \(k\ge2x^2-3\)과 같다. "
            r"\(-2\le x\le2\)에서 \(2x^2-3\)의 최댓값은 \(x=\pm2\)일 때 \(5\)이므로 "
            r"\(k_{\min}=5\)이다."
        ),
    ),
    Row(
        no=13,
        kind="objective",
        q=(
            r"직선 \(x-y+2=0\)을 \(x\)축의 방향으로 \(m\)만큼, \(y\)축의 방향으로 \(-1\)만큼 평행이동한 직선과 "
            r"\(x\)축, \(y\)축으로 둘러싸인 부분의 넓이가 \(8\)일 때, \(m\)의 값은? (단, \(m>1\))"
        ),
        choices=(r"2", r"3", r"4", r"5", r"6"),
        answer="④",
        solution=(
            r"평행이동한 직선은 \(y=x-m+1\)이다. "
            r"\(x\)절편은 \(m-1\), \(y\)절편은 \(1-m\)이므로 넓이는 "
            r"\(\frac12(m-1)^2\). "
            r"\(\frac12(m-1)^2=8\), \(m>1\)에서 \(m=5\)이다."
        ),
    ),
    Row(
        no=14,
        kind="objective",
        q=(
            r"세 점 \(O(0,0)\), \(A(-2,4)\), \(B(a,b)\)를 꼭짓점으로 하는 삼각형 \(OAB\)에서 "
            r"\(\angle AOB=90^\circ\)이고 \(OB=2OA\)일 때, 두 양수 \(a,b\)의 합 \(a+b\)의 값은?"
        ),
        choices=(r"8", r"9", r"10", r"11", r"12"),
        answer="⑤",
        solution=(
            r"\(\overrightarrow{OA}=(-2,4)\), \(|OA|=2\sqrt5\). "
            r"\(\overrightarrow{OB}\)는 \(\overrightarrow{OA}\)에 수직이고 길이가 \(4\sqrt5\)이므로 "
            r"\(\overrightarrow{OB}=2(4,2)=(8,4)\) 또는 \((-8,-4)\). "
            r"\(a,b>0\)이므로 \(B=(8,4)\), 따라서 \(a+b=12\)이다."
        ),
    ),
    Row(
        no=15,
        kind="objective",
        q=(
            r"삼차방정식 \(x^3=1\)의 한 허근을 \(\omega\)라 할 때, 다음 식의 값은?"
            "\n\n"
            '<div style="border:1px solid #333; padding:6px;">'
            r"\((\omega^2+3\omega+2)(\bar{\omega}^2+3\bar{\omega}+2)\)"
            "</div>"
        ),
        choices=(r"\(-2\)", r"\(-i\)", r"1", r"2", r"3"),
        answer="⑤",
        solution=(
            r"\(\omega^2+\omega+1=0\), \(\bar{\omega}=\omega^2\)를 이용하면 "
            r"\(\omega^2+3\omega+2=1+2\omega\), "
            r"\(\bar{\omega}^2+3\bar{\omega}+2=1+2\omega^2\). "
            r"따라서 "
            r"\((1+2\omega)(1+2\omega^2)=1+2(\omega+\omega^2)+4\omega^3=1-2+4=3\)이다."
        ),
    ),
    Row(
        no=16,
        kind="objective",
        q=(
            r"연립방정식"
            "\n"
            r"\["
            "\n"
            r"\begin{cases}"
            "\n"
            r"x^2-xy-2y^2=0,\\"
            "\n"
            r"x^2+y^2=20"
            "\n"
            r"\end{cases}"
            "\n"
            r"\]"
            "\n"
            r"을 만족시키는 상수 \(x,y\)에 대하여 \(x+y\)의 최댓값은?"
        ),
        choices=(r"2", r"4", r"6", r"9", r"10"),
        answer="③",
        solution=(
            r"첫 식은 \((x-2y)(x+y)=0\). "
            r"\(x=2y\)이면 \(5y^2=20\), \((x,y)=(4,2),(-4,-2)\)이고 \(x+y=6,-6\). "
            r"\(x=-y\)이면 \(2y^2=20\), \(x+y=0\). "
            r"따라서 최댓값은 \(6\)이다."
        ),
    ),
    Row(
        no=17,
        kind="objective",
        q=(
            r"원 \(x^2+y^2-6x+8y=0\)을 직선 \(y=x\)에 대하여 대칭이동한 원을 \(C_1\), "
            r"\(x\)축의 방향으로 \(+1\)만큼, \(y\)축의 방향으로 \(-1\)만큼 평행이동한 원을 \(C_2\)라 할 때, "
            r"원 \(C_1\) 위의 점과 원 \(C_2\) 위의 점 사이의 거리의 최댓값은?"
        ),
        choices=(r"14", r"18", r"\(6\sqrt2+10\)", r"20", r"\(8\sqrt2+10\)"),
        answer="⑤",
        solution=(
            r"원 \(x^2+y^2-6x+8y=0\)의 중심은 \((3,-4)\), 반지름은 \(5\)이다. "
            r"\(C_1\)의 중심은 \((-4,3)\), \(C_2\)의 중심은 \((4,-5)\). "
            r"중심거리 \(d=\sqrt{8^2+(-8)^2}=8\sqrt2\). "
            r"두 원 위 점 사이 거리의 최댓값은 \(d+5+5=8\sqrt2+10\)이다."
        ),
    ),
    Row(
        no=18,
        kind="objective",
        q=r"원 \(x^2+(y-2)^2=4\)를 직선 \(y=x\)에 대하여 대칭이동한 도형의 내부와 처음 원의 내부의 공통부분의 넓이는?",
        choices=(r"\(2\pi-4\)", r"\(2\pi-2\)", r"\(2\pi\)", r"\(2\pi+2\)", r"\(2\pi+4\)"),
        answer="①",
        solution=(
            r"두 원의 반지름은 모두 \(2\), 중심은 \((0,2)\), \((2,0)\)이므로 중심거리 \(d=2\sqrt2\). "
            r"공통부분 넓이는 "
            r"\(2r^2\cos^{-1}\!\left(\frac{d}{2r}\right)-\frac{d}{2}\sqrt{4r^2-d^2}\). "
            r"\(\cos^{-1}(\sqrt2/2)=\pi/4\)를 대입하면 "
            r"\(2\pi-4\)이다."
        ),
    ),
    Row(
        no=101,
        kind="subjective",
        q=r"\(x\)에 대한 삼차방정식 \(x^3-4x^2+(k+4)x-2k=0\)의 근이 모두 실수가 되도록 하는 실수 \(k\)의 범위를 구하여라.",
        choices=(),
        answer=r"\(k\le1\)",
        solution=(
            r"\(x^3-4x^2+(k+4)x-2k=(x-2)(x^2-2x+k)\). "
            r"근이 모두 실수이려면 이차식의 판별식이 \(0\) 이상이어야 하므로 "
            r"\(4-4k\ge0\), 즉 \(k\le1\)."
        ),
    ),
    Row(
        no=102,
        kind="subjective",
        q=(
            r"\(x\)에 대한 부등식 \((a-3b)x+a-b\ge0\)의 해가 존재하지 않을 때, "
            r"부등식 \((a-2b)x+a+2b>0\)의 해를 구하여라."
        ),
        choices=(),
        answer=r"\(x<-5\)",
        solution=(
            r"\((a-3b)x+a-b\ge0\)의 해가 없으려면 "
            r"\(a-3b=0\)이고 \(a-b<0\)이어야 한다. "
            r"따라서 \(a=3b\), \(b<0\). "
            r"둘째 부등식은 \(bx+5b>0\), 즉 \(b(x+5)>0\). "
            r"\(b<0\)이므로 \(x+5<0\), 따라서 \(x<-5\)."
        ),
    ),
    Row(
        no=103,
        kind="subjective",
        q=(
            r"[서술형] 다음 도형의 방정식"
            "\n"
            r"\[x^2+y^2-2x+4y-4=0\]"
            "\n"
            r"과 점 \(P(-2,3)\)에 대하여 다음 물음에 답하여라."
            "\n\n"
            r"(1) 점 \(P\)에서 도형에 그은 접선 중 기울기가 \(m\)인 직선의 방정식을 구하여라."
            "\n\n"
            r"(2) (1)의 접선에서 \(m\)의 값을 구하여라. (단, \(m\ne0\))"
            "\n\n"
            r"(3) 접점을 \(T\)라 할 때, \(PT\)의 길이를 구하여라."
        ),
        choices=(),
        answer=(
            r"(1) \(y-3=m(x+2)\), "
            r"(2) \(m=-\frac{8}{15}\), "
            r"(3) \(PT=5\)"
        ),
        solution=(
            r"원은 \((x-1)^2+(y+2)^2=9\), 중심 \(C(1,-2)\), 반지름 \(3\). "
            r"점 \(P(-2,3)\)을 지나는 기울기 \(m\)인 직선은 \(y-3=m(x+2)\). "
            r"직선 \(mx-y+2m+3=0\)에서 중심까지의 거리가 \(3\)이므로 "
            r"\(\frac{|3m+5|}{\sqrt{m^2+1}}=3\). "
            r"정리하면 \(m=-\frac{8}{15}\). "
            r"또한 \(PC=\sqrt{(-3)^2+5^2}=\sqrt{34}\)이므로 "
            r"접선의 길이 \(PT=\sqrt{PC^2-r^2}=\sqrt{34-9}=5\)."
        ),
    ),
    Row(
        no=104,
        kind="subjective",
        q=(
            r"[서술형] 세 점 \(A(6,2)\), \(B(a,0)\), \(C(b,2b)\)를 꼭짓점으로 하는 삼각형 \(ABC\)에서 "
            r"둘레의 길이가 최소일 때, 삼각형의 넓이와 \(3ab\)의 값을 구하여라."
            "\n\n"
            '<div style="border:1px solid #333; padding:6px;">'
            r"(1) 빈칸 채우기: 점 \(B\)는 (①) 위의 점이고, 점 \(C\)는 직선 (②) 위의 점이다."
            r" 점 \(A\)를 (①)에 대하여 대칭이동한 점을 \(A'\), 점 \(A\)를 직선 (②)에 대하여 대칭이동한 점을 \(A''\)라 하면, "
            r"선분 \(A'A''\)의 길이가 둘레의 최소값이 된다."
            "</div>"
            "\n\n"
            r"(2) \(A'\), \(A''\)의 좌표를 구하여라."
            "\n\n"
            r"(3) \(A'\), \(A''\)를 지나는 직선의 방정식을 구하여라."
            "\n\n"
            r"(4) \(3ab\)와 삼각형 \(ABC\)의 넓이를 구하여라."
        ),
        choices=(),
        answer=(
            r"① \(x\)축, ② \(y=2x\), "
            r"\(A'=(6,-2)\), \(A''=(-2,6)\), "
            r"직선 \(x+y-4=0\), "
            r"\(3ab=16\), "
            r"넓이 \(=\frac{16}{3}\)"
        ),
        solution=(
            r"\(B(a,0)\)이므로 \(B\)는 \(x\)축 위의 점, "
            r"\(C(b,2b)\)이므로 \(C\)는 \(y=2x\) 위의 점이다. "
            r"점 \(A(6,2)\)를 \(x\)축에 대칭이동하면 \(A'=(6,-2)\). "
            r"직선 \(y=2x\)에 대한 대칭이동으로 \(A''=(-2,6)\). "
            r"\(A'A''\)의 방정식은 \(x+y-4=0\). "
            r"이 직선과 \(x\)축의 교점은 \(B=(4,0)\), "
            r"직선 \(y=2x\)와의 교점은 \(C=\left(\frac43,\frac83\right)\). "
            r"따라서 \(a=4\), \(b=\frac43\), "
            r"\(3ab=16\). "
            r"넓이는 "
            r"\(\frac12\left|\det\!\left(B-A,\;C-A\right)\right|=\frac{16}{3}\)."
        ),
    ),
]


def pid_from_no(no: int) -> str:
    return f"BY-2021-G1-S1-Final-{no:03d}"


def source_no_kind(no: int) -> tuple[int, str, str]:
    if no >= 100:
        src_no = no - 100
        return src_no, "subjective", f"서답{src_no}"
    return no, "objective", str(no)


def classify(row: Row) -> tuple[str, str, str, int, str]:
    src_no, _, _ = source_no_kind(row.no)
    result = classify_unit_and_level(
        question_text=row.q,
        choices_text="\n".join(row.choices),
        answer_text=row.answer,
        solution_text=row.solution,
        qtype=row.kind,
        grade=1,
        problem_no=row.no,
    )
    return result.unit_l1, result.unit_l2, result.unit_l3, result.level, result.reason


def make_problem_md(pid: str, row: Row) -> str:
    src_no, src_kind, src_label = source_no_kind(row.no)
    unit_l1, unit_l2, unit_l3, level, reason = classify(row)
    unit = f"{unit_l1}>{unit_l2}>{unit_l3}"
    qtype_text = "객관식" if src_kind == "objective" else "서답형"

    assets: List[str] = [
        "assets/original/",
        f"assets/original/{PDF_NAME}",
    ]
    if row.use_scan:
        assets.insert(0, "assets/scan.png")
        assets.append(f"assets/original/{SUP_SCAN_NAME}")

    fm = [
        "---",
        f"id: {pid}",
        "school: BY",
        "year: 2021",
        "grade: 1",
        "semester: 1",
        "exam: Final",
        f"type: {qtype_text}",
        f"source_question_no: {src_no}",
        f"source_question_kind: {src_kind}",
        f"source_question_label: '{src_label}'",
        f"difficulty: '{level}'",
        f"level: {level}",
        f"unit: {unit}",
        f"unit_l1: {unit_l1}",
        f"unit_l2: {unit_l2}",
        f"unit_l3: {unit_l3}",
        "source: user_upload_2026-03-06",
        "tags:",
        f"- {qtype_text}",
        f"- 출제번호-{src_no}",
        "assets:",
    ]
    for a in assets:
        fm.append(f"- {a}")
    fm.append("---")

    body: List[str] = []
    body.extend(fm)
    body.append("## Q")
    body.append(row.q)
    body.append("")
    body.append("## Choices")
    body.append("")
    if row.choices:
        labels = ["①", "②", "③", "④", "⑤"]
        for idx, c in enumerate(row.choices):
            label = labels[idx] if idx < len(labels) else f"({idx+1})"
            body.append(f"{label} {c}")
    body.append("")
    body.append("## Answer")
    body.append(row.answer)
    body.append("")
    body.append("## Solution")
    body.append(row.solution)
    body.append("")
    body.append(f"<!-- classifier_reason: {reason} -->")
    body.append("")
    return "\n".join(body)


def write_row(row: Row, report_lines: List[str], duplicates: List[str], uncertain: List[str]) -> str:
    pid = pid_from_no(row.no)
    pdir = PROBLEMS / pid
    if pdir.exists():
        duplicates.append(pid)
        report_lines.append(f"{pid} | SKIP | duplicate-folder")
        return "skip"

    (pdir / "assets" / "original").mkdir(parents=True, exist_ok=True)

    src_pdf = ORIGINAL / PDF_NAME
    dst_pdf = pdir / "assets" / "original" / PDF_NAME
    shutil.copy2(src_pdf, dst_pdf)

    if row.use_scan:
        src_scan = ORIGINAL / SUP_SCAN_NAME
        if src_scan.exists():
            shutil.copy2(src_scan, pdir / "assets" / "original" / SUP_SCAN_NAME)
            shutil.copy2(src_scan, pdir / "assets" / "scan.png")
        else:
            report_lines.append(f"{pid} | WARN | supplemental-scan-missing: {SUP_SCAN_NAME}")
            uncertain.append(f"{pid}: supplemental-scan-missing")

    md = make_problem_md(pid, row)
    (pdir / "problem.md").write_text(md, encoding="utf-8")

    if row.ocr_uncertain:
        uncertain.append(f"{pid}: {row.uncertain_note}")
    report_lines.append(f"{pid} | CREATED | source_no={source_no_kind(row.no)[0]} kind={row.kind}")
    return "created"


def pick_rows(phase: str) -> List[Row]:
    if phase == "objective":
        return [r for r in DATA if r.no < 100]
    if phase == "subjective":
        return [r for r in DATA if r.no >= 100]
    return list(DATA)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=("objective", "subjective", "all"),
        default="all",
    )
    args = parser.parse_args()

    src_pdf = ORIGINAL / PDF_NAME
    if not src_pdf.exists():
        print(f"[ERROR] missing-pdf: {src_pdf}")
        return 1

    rows = pick_rows(args.phase)
    duplicates: List[str] = []
    report_lines: List[str] = []
    uncertain: List[str] = []
    created = 0
    skipped = 0

    for row in rows:
        status = write_row(row, report_lines=report_lines, duplicates=duplicates, uncertain=uncertain)
        if status == "created":
            created += 1
        else:
            skipped += 1

    print("=== SUMMARY ===")
    print(f"phase={args.phase}")
    print(f"created={created}")
    print(f"skipped_duplicate={skipped}")
    print(f"warnings={len(uncertain)}")
    print("")
    print("=== PER_FILE ===")
    for line in report_lines:
        print(line)
    print("")
    print("=== DUPLICATE_FOLDERS ===")
    if duplicates:
        for d in duplicates:
            print(d)
    else:
        print("(none)")
    print("")
    print("=== OCR_UNCERTAIN ===")
    if uncertain:
        for u in uncertain:
            print(u)
    else:
        print("(none)")
    print("")
    print("=== QUICK_REVIEW_PATHS ===")
    for row in rows:
        pid = pid_from_no(row.no)
        print((PROBLEMS / pid / "problem.md").resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
