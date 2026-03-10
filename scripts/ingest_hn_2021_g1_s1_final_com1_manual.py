from __future__ import annotations

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

PDF_NAME = "HN.2021.G1.S1.Final.COM1.pdf"
SOURCE_TAG = "user_upload_2026-03-10"

IMG_TAG = '<img src="assets/scan.png" alt="문항 삽화" style="width:60% !important; max-width:60% !important; height:auto;" />'


@dataclass(frozen=True)
class Row:
    no: int
    kind: str  # objective | subjective
    q: str
    choices: Sequence[str]
    answer: str
    solution: str
    scan_source: str | None = None
    ocr_uncertain: bool = False
    uncertain_note: str = ""


def _box(lines: Sequence[str]) -> str:
    body = "<br/>".join(lines)
    return f'<div style="border:1px solid #333; padding:6px; margin:6px 0;">{body}</div>'


ROWS: List[Row] = [
    Row(
        no=1,
        kind="objective",
        q=r"방정식 \(x^4-2x^2+3x-2=0\)을 풀면?",
        choices=(
            r"\(x=-2,\ x=1,\ x=\dfrac{1\pm\sqrt{3}i}{2}\)",
            r"\(x=2,\ x=-1,\ x=\dfrac{1\pm\sqrt{5}}{2}\)",
            r"\(x=-1\text{(중근)},\ x=3\text{(중근)}\)",
            r"\(x=\pm\dfrac{\sqrt{2}}{2},\ x=\pm1\)",
            r"\(x=1,\ x=\dfrac{3}{2},\ x=\dfrac{-3\pm3\sqrt{3}i}{4}\)",
        ),
        answer="①",
        solution=(
            r"\(x=1\)을 대입하면 식이 0이므로 \((x-1)\)을 인수로 갖는다."
            "\n"
            r"또 \(x=-2\)도 근이므로"
            "\n"
            r"\["
            "\n"
            r"x^4-2x^2+3x-2=(x-1)(x+2)(x^2-x+1)."
            "\n"
            r"\]"
            "\n"
            r"\(x^2-x+1=0\)의 근은 \(x=\dfrac{1\pm\sqrt{3}i}{2}\)이므로"
            "\n"
            r"근은 \(-2,\ 1,\ \dfrac{1\pm\sqrt{3}i}{2}\)이다."
        ),
    ),
    Row(
        no=2,
        kind="objective",
        q=(
            r"오른쪽 그림과 같이 높이가 \(12\)규빗인 대나무가 바람에 부러져서 "
            r"그 끝이 처음 대나무가 나온 부분으로부터 \(6\)규빗 떨어진 곳에 닿았다. "
            r"이때 대나무의 부러진 부분의 길이를 구하면?"
            "\n\n"
            + IMG_TAG
        ),
        choices=(
            r"\(\dfrac{7}{2}\)",
            r"\(\dfrac{9}{2}\)",
            r"\(\dfrac{11}{2}\)",
            r"\(\dfrac{13}{2}\)",
            r"\(\dfrac{15}{2}\)",
        ),
        answer="⑤",
        solution=(
            r"남은 대나무 길이를 \(h\), 부러진 부분 길이를 \(L\)이라 하면"
            "\n"
            r"\["
            "\n"
            r"h+L=12,\qquad L^2=h^2+6^2."
            "\n"
            r"\]"
            "\n"
            r"\(L=12-h\)를 대입하면"
            "\n"
            r"\["
            "\n"
            r"(12-h)^2=h^2+36 \Rightarrow 144-24h=36 \Rightarrow h=\dfrac{9}{2}."
            "\n"
            r"\]"
            "\n"
            r"따라서 \(L=12-\dfrac{9}{2}=\dfrac{15}{2}\)이다."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.002.png",
    ),
    Row(
        no=3,
        kind="objective",
        q=(
            r"방정식 \(x^3+1=0\)의 한 허근을 \(\omega\)라고 할 때,"
            "\n"
            r"\["
            "\n"
            r"\left(\omega+\dfrac{1}{\omega}\right)+"
            r"\left(\omega^2+\dfrac{1}{\omega^2}\right)+"
            r"\left(\omega^3+\dfrac{1}{\omega^3}\right)+\cdots+"
            r"\left(\omega^{19}+\dfrac{1}{\omega^{19}}\right)"
            "\n"
            r"\]"
            "\n"
            r"의 값을 구하면?"
        ),
        choices=(r"-2", r"-1", r"0", r"1", r"2"),
        answer="④",
        solution=(
            r"\(x^3+1=0\)의 허근 \(\omega\)는 \(\omega^6=1\)을 만족하고 \(|\omega|=1\)이므로"
            "\n"
            r"\(\dfrac1{\omega^k}=\omega^{-k}\)이다."
            "\n"
            r"따라서 각 항은 \(\omega^k+\omega^{-k}=2\cos\dfrac{k\pi}{3}\)이고 주기는 6이다."
            "\n"
            r"\(k=1\)부터 \(6\)까지의 합은 0이므로 \(k=1\)부터 \(18\)까지 합도 0이다."
            "\n"
            r"남는 \(k=19\)는 6으로 나누면 나머지가 1이므로 첫 번째 항과 같아 값은 1이다."
        ),
    ),
    Row(
        no=4,
        kind="objective",
        q=(
            r"연립부등식"
            "\n"
            r"\["
            "\n"
            r"\begin{cases}"
            "\n"
            r"2x+1\le-7\\"
            "\n"
            r"5x+9\ge4x+10"
            "\n"
            r"\end{cases}"
            "\n"
            r"\]"
            "\n"
            r"을 풀면?"
        ),
        choices=(
            r"\(x=4\)",
            r"해는 없다",
            r"\(x\ne4\)인 모든 실수",
            r"\(-3<x\le3\)",
            r"모든 실수",
        ),
        answer="②",
        solution=(
            r"첫째 부등식에서 \(x\le-4\), 둘째 부등식에서 \(x\ge1\)이다."
            "\n"
            r"두 조건을 동시에 만족하는 실수는 없으므로 해는 없다."
        ),
    ),
    Row(
        no=5,
        kind="objective",
        q=(
            r"모든 실수 \(x\)에 대하여 성립하는 부등식을 \(<보기>\)에서 있는 대로 모두 고른 것은?"
            "\n\n"
            + _box(
                [
                    r"ㄱ. \(x^2+x\ge-1\)",
                    r"ㄴ. \(-x^2+3x\ge3\)",
                    r"ㄷ. \(3x-1>-x^2+2x-5\)",
                    r"ㄹ. \(x^2-4x<-4\)",
                    r"ㅁ. \(x^2-2x>-2\)",
                    r"ㅂ. \(|2x-1|>-7\)",
                ]
            )
        ),
        choices=(
            "ㄱ, ㄴ",
            "ㄴ, ㄹ, ㅂ",
            "ㄷ, ㄹ, ㅁ",
            "ㄱ, ㄴ, ㄷ, ㅁ",
            "ㄱ, ㄷ, ㅁ, ㅂ",
        ),
        answer="⑤",
        solution=(
            r"ㄱ: \(x^2+x+1\ge0\) (항상 참)"
            "\n"
            r"ㄴ: \(-x^2+3x-3\ge0\)은 항상 거짓"
            "\n"
            r"ㄷ: \(x^2+x+4>0\) (항상 참)"
            "\n"
            r"ㄹ: \((x-2)^2<0\) (항상 거짓)"
            "\n"
            r"ㅁ: \(x^2-2x+2>0\) (항상 참)"
            "\n"
            r"ㅂ: 절댓값은 항상 \(0\) 이상이므로 \(|2x-1|>-7\)은 항상 참"
            "\n"
            r"따라서 ㄱ, ㄷ, ㅁ, ㅂ이다."
        ),
    ),
    Row(
        no=6,
        kind="objective",
        q=(
            r"어느 타일 공장에서 직사각형 모양의 타일 규격을 \(A\)와 \(B\)의 두 가지로 정하려고 한다. "
            r"\(A\)와 \(B\)의 가로의 길이는 같고, \(A\)의 세로의 길이는 가로의 길이보다 \(20\text{ cm}\)만큼 길고, "
            r"\(B\)의 세로의 길이는 가로의 길이보다 \(30\text{ cm}\)만큼 짧다고 한다. "
            r"\(A\)의 넓이를 \(4800\text{ cm}^2\) 이상, \(B\)의 넓이를 \(4000\text{ cm}^2\) 이하가 되도록 할 때, "
            r"타일의 가로의 길이의 범위를 구하면?"
        ),
        choices=(
            r"\(60<x<70\)",
            r"\(60\le x<70\)",
            r"\(60\le x\le70\)",
            r"\(60<x\le80\)",
            r"\(60\le x\le80\)",
        ),
        answer="⑤",
        solution=(
            r"공통 가로 길이를 \(x\)라 하면"
            "\n"
            r"\(A\)의 넓이 조건: \(x(x+20)\ge4800\Rightarrow x\ge60\)."
            "\n"
            r"\(B\)의 넓이 조건: \(x(x-30)\le4000\Rightarrow -50\le x\le80\)."
            "\n"
            r"두 조건을 합치면 \(60\le x\le80\)이다."
        ),
    ),
    Row(
        no=7,
        kind="objective",
        q=(
            r"두 점 \(A(-4,3)\), \(B(1,8)\)에 대하여 두 점 \(A, B\)에서 같은 거리에 있고 "
            r"직선 \(y=x\) 위에 있는 점 \(Q\)의 좌표를 구하면?"
        ),
        choices=(
            r"\(Q(1,1)\)",
            r"\(Q(2,2)\)",
            r"\(Q(-3,3)\)",
            r"\(Q(4,-4)\)",
            r"\(Q(4,4)\)",
        ),
        answer="②",
        solution=(
            r"\(Q=(t,t)\)라 두고 \(QA=QB\)를 이용하면"
            "\n"
            r"\["
            "\n"
            r"(t+4)^2+(t-3)^2=(t-1)^2+(t-8)^2"
            "\n"
            r"\]"
            "\n"
            r"\(\Rightarrow 20t=40\Rightarrow t=2\)."
            "\n"
            r"따라서 \(Q=(2,2)\)이다."
        ),
    ),
    Row(
        no=8,
        kind="objective",
        q=(
            r"두 점 \(A(1,-2)\), \(B(8,5)\)를 잇는 선분 \(AB\)를 \(2:1\)로 외분하는 점이 "
            r"직선 \(y=ax-3\) 위에 있을 때, 상수 \(a\)의 값을 구하면?"
        ),
        choices=("1", "3", "5", "7", "9"),
        answer="①",
        solution=(
            r"\(2:1\) 외분점 \(P\)는"
            "\n"
            r"\["
            "\n"
            r"P=\frac{2B-1A}{2-1}=2B-A=(15,12)."
            "\n"
            r"\]"
            "\n"
            r"\(P\)가 \(y=ax-3\) 위의 점이므로"
            "\n"
            r"\(12=15a-3\Rightarrow a=1\)."
        ),
    ),
    Row(
        no=9,
        kind="objective",
        q=(
            r"오른쪽 그림과 같이 지점 \(O\)에서 수직으로 만나는 직선 도로가 있다. "
            r"서로 다른 도로에 있는 슬기와 현지가 지점 \(O\)에서 각각 \(1\text{ km}\) 떨어진 곳에서 "
            r"1분에 \(30\text{ m}\), \(40\text{ m}\)의 일정한 속력으로 지점 \(O\)를 향하여 직진하였다. "
            r"두 사람이 동시에 출발할 때, 두 사람 사이의 거리가 가장 가까워지는 것은 출발한 지 몇 분 후인지 구하면?"
            "\n\n"
            + IMG_TAG
        ),
        choices=("7분 후", "14분 후", "28분 후", "42분 후", "84분 후"),
        answer="③",
        solution=(
            r"출발 후 \(t\)분일 때 슬기, 현지의 좌표를 각각"
            "\n"
            r"\((0,1000-30t),\ (1000-40t,0)\)으로 둘 수 있다."
            "\n"
            r"거리의 제곱은"
            "\n"
            r"\["
            "\n"
            r"D^2=(1000-40t)^2+(1000-30t)^2"
            r"=2500t^2-140000t+2000000."
            "\n"
            r"\]"
            "\n"
            r"이차식의 최솟값은 꼭짓점에서 이루어지므로"
            "\n"
            r"\(t=\dfrac{140000}{2\cdot2500}=28\)."
            "\n"
            r"따라서 28분 후이다."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.011.png",
    ),
    Row(
        no=10,
        kind="objective",
        q=r"두 점 \((4,-5)\), \((-1,5)\)을 지나는 직선의 방정식을 구하면?",
        choices=(
            r"\(y=3x-3\)",
            r"\(y=-3x-3\)",
            r"\(y=3x+3\)",
            r"\(y=-2x+3\)",
            r"\(y=2x-3\)",
        ),
        answer="④",
        solution=(
            r"기울기는"
            "\n"
            r"\["
            "\n"
            r"m=\frac{5-(-5)}{-1-4}=\frac{10}{-5}=-2."
            "\n"
            r"\]"
            "\n"
            r"점 \((4,-5)\)를 대입하면"
            "\n"
            r"\(y+5=-2(x-4)\Rightarrow y=-2x+3\)."
        ),
    ),
    Row(
        no=11,
        kind="objective",
        q=(
            r"다음은 좌표평면에서 두 직선이 서로 수직일 조건을 증명하는 과정이다. "
            r"괄호 안의 내용이 올바르게 대응된 것을 고르면?"
            "\n\n"
            + _box(
                [
                    r"두 직선 \(l:y=mx+n,\ l':y=m'x+n'\)이 서로 수직이면,"
                    r"두 직선 \(l, l'\)과 각각 평행하고 원점을 지나는 두 직선"
                    r"\(l_1:y=mx,\ l_1':y=m'x\)도 서로 수직이다.",
                    r"즉 두 직선 \(l,l'\)이 서로 수직일 조건은 두 직선 \(l_1,l_1'\)이 서로 수직일 조건과 같다.",
                    r"두 직선 \(l_1,l_1'\)과 직선 \(x=1\)의 교점을 각각 \(P,Q\)라 하면"
                    r"\(P(가),\ Q(나)\)이고,"
                    r"\(\overline{OP}^2+\overline{OQ}^2=\overline{PQ}^2\),"
                    r"즉 \((다)^2+(1+m'^2)=(라)^2\)이다.",
                    r"이 식을 정리하면 \(mm'=(마)\)이다.",
                ]
            )
            + "\n\n"
            + IMG_TAG
        ),
        choices=(
            r"(가) \((1,m)\), (나) \((1,m')\), (다) \(1-m^2\), (라) \((m+m')^2\), (마) \(1\)",
            r"(가) \((m,1)\), (나) \((1,m')\), (다) \(m^2-1\), (라) \((m-m')^2\), (마) \(1\)",
            r"(가) \((2,m)\), (나) \((m',1)\), (다) \(2+m\), (라) \((m+m')^2\), (마) \(1\)",
            r"(가) \((1,m)\), (나) \((1,m')\), (다) \(1+m^2\), (라) \((m-m')^2\), (마) \(-1\)",
            r"(가) \((m,1)\), (나) \((m',1)\), (다) \(2+m^2\), (라) \((m+m')^2\), (마) \(-1\)",
        ),
        answer="④",
        solution=(
            r"\(x=1\)에서 \(l_1,y=mx\)의 점은 \(P(1,m)\), "
            r"\(l_1',y=m'x\)의 점은 \(Q(1,m')\)이므로"
            "\n"
            r"(가), (나)는 각각 \((1,m),\ (1,m')\)이다."
            "\n"
            r"또 \(\overline{OP}^2=1+m^2\), \(\overline{OQ}^2=1+m'^2\), \(\overline{PQ}^2=(m-m')^2\)."
            "\n"
            r"따라서 (다)=\(1+m^2\), (라)=\((m-m')^2\)이고"
            "\n"
            r"\((1+m^2)+(1+m'^2)=(m-m')^2\Rightarrow mm'=-1\)."
            "\n"
            r"즉 (마)=\(-1\)이다."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.012.png",
    ),
    Row(
        no=12,
        kind="objective",
        q=(
            r"두 직선 \(3x+y=0,\ x-3y+5=0\)으로부터 같은 거리에 있는 점 "
            r"\(P(x,y)\)가 나타내는 도형의 방정식을 구하면?"
        ),
        choices=(
            r"\(x+3y-4=0\)",
            r"\(3x-y+4=0\)",
            r"\(x+3y-4=0,\ 3x-y+4=0\)",
            r"\(2x+4y-5=0\)",
            r"\(2x+4y-5=0,\ 4x-2y+5=0\)",
        ),
        answer="⑤",
        solution=(
            r"점 \((x,y)\)에서 두 직선까지의 거리가 같으므로"
            "\n"
            r"\["
            "\n"
            r"\frac{|3x+y|}{\sqrt{10}}=\frac{|x-3y+5|}{\sqrt{10}}"
            r"\Rightarrow |3x+y|=|x-3y+5|."
            "\n"
            r"\]"
            "\n"
            r"따라서"
            "\n"
            r"\(3x+y=x-3y+5\) 또는 \(3x+y=-(x-3y+5)\)."
            "\n"
            r"정리하면 \(2x+4y-5=0\), \(4x-2y+5=0\)이다."
        ),
    ),
    Row(
        no=13,
        kind="objective",
        q=r"세 점 \(A(-2,3)\), \(B(4,5)\), \(C(0,7)\)을 꼭짓점으로 하는 삼각형 \(ABC\)의 외접원의 반지름의 길이를 구하면?",
        choices=(
            r"\(2\sqrt{2}\)",
            r"\(3\)",
            r"\(\sqrt{10}\)",
            r"\(\sqrt{11}\)",
            r"\(2\sqrt{3}\)",
        ),
        answer="③",
        solution=(
            r"\(BC=2\sqrt{5},\ CA=2\sqrt{5},\ AB=2\sqrt{10}\)이고"
            "\n"
            r"삼각형의 넓이는"
            "\n"
            r"\["
            "\n"
            r"\Delta=\frac12\left|\det\begin{pmatrix}6&2\\2&4\end{pmatrix}\right|"
            r"=\frac12|24-4|=10."
            "\n"
            r"\]"
            "\n"
            r"외접반지름 \(R\)은 \(R=\dfrac{abc}{4\Delta}\)이므로"
            "\n"
            r"\["
            "\n"
            r"R=\frac{(2\sqrt5)(2\sqrt5)(2\sqrt{10})}{4\cdot10}=\sqrt{10}."
            "\n"
            r"\]"
        ),
    ),
    Row(
        no=14,
        kind="objective",
        q=(
            r"연립부등식 \(|x-2|\le|x-1|+1\le x+3\)을 만족시키는 \(x\)의 최솟값을 구하면?"
        ),
        choices=(r"-2", r"-1", r"0", r"1", r"\(-\dfrac12\)"),
        answer="⑤",
        solution=(
            r"첫째 부등식 \(|x-2|\le|x-1|+1\)은 항상 성립한다."
            "\n"
            r"(역삼각부등식 \(||x-2|-|x-1||\le1\) 이용)"
            "\n"
            r"따라서 \(|x-1|+1\le x+3\)만 풀면 된다."
            "\n"
            r"\["
            "\n"
            r"|x-1|\le x+2"
            "\n"
            r"\]"
            "\n"
            r"이므로 \(x\ge-2\)이고, 양변 제곱하면"
            "\n"
            r"\((x-1)^2\le(x+2)^2\Rightarrow -2x+1\le4x+4\Rightarrow x\ge-\dfrac12\)."
            "\n"
            r"최솟값은 \(-\dfrac12\)이다."
        ),
    ),
    Row(
        no=15,
        kind="objective",
        q=(
            r"오른쪽 그림과 같이 좌표평면 위에 있는 두 직사각형의 넓이를 동시에 이등분하는 "
            r"직선의 방정식을 구하면?"
            "\n\n"
            + IMG_TAG
        ),
        choices=(
            r"\(5x-6y+2=0\)",
            r"\(3x-y+4=0\)",
            r"\(14x+17y+9=0\)",
            r"\(5x-6y-2=0\)",
            r"\(14x-17y-9=0\)",
        ),
        answer="⑤",
        solution=(
            r"직사각형의 넓이를 이등분하는 직선은 각 직사각형의 중심을 지난다."
            "\n"
            r"오른쪽 직사각형 중심은 \(\left(\dfrac{3+8}{2},\dfrac{3+5}{2}\right)=\left(\dfrac{11}{2},4\right)\),"
            "\n"
            r"왼쪽 직사각형 중심은 \(\left(\dfrac{-4+(-2)}{2},\dfrac{-4+(-2)}{2}\right)=(-3,-3)\)."
            "\n"
            r"두 점을 지나는 직선의 기울기는"
            "\n"
            r"\["
            "\n"
            r"m=\frac{4-(-3)}{\frac{11}{2}-(-3)}=\frac{7}{17/2}=\frac{14}{17}."
            "\n"
            r"\]"
            "\n"
            r"점 \((-3,-3)\)을 대입하면"
            "\n"
            r"\(y+3=\dfrac{14}{17}(x+3)\Rightarrow 14x-17y-9=0\)."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.015.png",
    ),
    Row(
        no=16,
        kind="objective",
        q=(
            r"[오류 가능 문항] 원문 판독 결과 \(|\overline{QA}-\overline{QB}|\) 조건은 "
            r"선택지와 충돌 가능성이 있어 검토가 필요함."
            "\n\n"
            r"두 점 \(A(1,-2)\), \(B(8,5)\)과 \(y\)축 위의 점 \(Q\)에 대하여 "
            r"\(|\overline{QA}-\overline{QB}|\)는 점 \(Q\)의 좌표가 \((0,a)\)일 때 최댓값 \(b\)를 갖는다. "
            r"이 때, \(a+b^2\)의 값을 구하면?"
        ),
        choices=("5", "7", "9", "11", "13"),
        answer="③",
        solution=(
            r"원문 OCR 판독상 조건과 선택지가 완전히 일치하지 않는 부분이 있어"
            "\n"
            r"해당 문항은 추가 원본 확인이 필요하다."
            "\n"
            r"현재 DB 입력에서는 원문 채점 표기(③)를 임시 반영하였다."
        ),
        ocr_uncertain=True,
        uncertain_note="조건식(|QA-QB|)과 선택지의 정합성 검토 필요",
    ),
    Row(
        no=17,
        kind="objective",
        q=(
            r"좌표평면 위의 서로 다른 두 점 \(A(x_1,y_1)\), \(B(x_2,y_2)\)와 점 "
            r"\(P(sx_1+tx_2,\ sy_1+ty_2)\)에 대하여 \(<보기>\)에서 옳은 것만을 있는 대로 모두 고른 것은?"
            "\n\n"
            + _box(
                [
                    r"ㄱ. \(s=4,\ t=-3\)이면 점 \(P\)는 \(\overline{AB}\)를 \(3:4\)로 내분하는 점이다.",
                    r"ㄴ. 실수 \(s,t\)에 대하여 \(s+t=1\)이면 점 \(P\)는 직선 \(AB\) 위에 존재한다.",
                    r"ㄷ. \(0\le s\le1,\ 0\le t\le1\)이고 \(s+t=\dfrac23\)일 때, 점 \(P\)가 그리는 도형의 길이는 \(\dfrac23\overline{AB}\)이다.",
                ]
            )
        ),
        choices=("ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"),
        answer="④",
        solution=(
            r"ㄱ: \(s=4, t=-3\)이면 \(P=4A-3B\)로 내분점이 아니므로 거짓."
            "\n"
            r"ㄴ: \(s+t=1\)이면 \(P=sA+tB\)는 \(A,B\)의 아핀결합이므로 항상 직선 \(AB\) 위의 점이다."
            "\n"
            r"ㄷ: \(t=\dfrac23-s\)로 두면"
            "\n"
            r"\["
            "\n"
            r"P=sA+\left(\frac23-s\right)B=\frac23B+s(A-B),\quad 0\le s\le\frac23."
            "\n"
            r"\]"
            "\n"
            r"따라서 \(P\)는 \(AB\)와 평행한 같은 방향의 선분을 그리고 그 길이는 \(\dfrac23\overline{AB}\)이다."
            "\n"
            r"즉 ㄴ, ㄷ이 옳다."
        ),
    ),
    Row(
        no=101,
        kind="subjective",
        q=r"두 점 \(A(2,9)\), \(B(-6,9)\) 사이의 거리를 구하시오.",
        choices=(),
        answer="8",
        solution=(
            r"두 점의 \(y\)좌표가 같으므로 수평거리만 보면 된다."
            "\n"
            r"\(|2-(-6)|=8\)이므로 거리도 8이다."
        ),
    ),
    Row(
        no=102,
        kind="subjective",
        q=(
            r"오른쪽 그림과 같이 두 점 \(A(0,3)\), \(B(1,0)\)을 꼭짓점으로 하는 정사각형 \(ABCD\)에 대하여 "
            r"직선 \(CD\)의 방정식을 구하시오. (단, 두 점 \(C,D\)는 제1사분면 위의 점이다.)"
            "\n\n"
            + IMG_TAG
        ),
        choices=(),
        answer=r"\(y=-3x+13\)",
        solution=(
            r"\(\overrightarrow{AB}=(1,-3)\)이므로 이에 수직이고 길이가 같은 벡터를 \((3,1)\)로 잡으면"
            "\n"
            r"\(C=B+(3,1)=(4,1),\ D=A+(3,1)=(3,4)\)가 되어 둘 다 제1사분면 위에 있다."
            "\n"
            r"따라서 \(CD\)의 기울기는"
            "\n"
            r"\(\dfrac{1-4}{4-3}=-3\),"
            "\n"
            r"점 \((4,1)\)을 지나므로"
            "\n"
            r"\(y-1=-3(x-4)\Rightarrow y=-3x+13\)."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.SUB02_scan.png",
    ),
    Row(
        no=103,
        kind="subjective",
        q=(
            r"직선 \(l:kx-y-3k+2=0\)이 있다. \(0<k\le\dfrac54\)일 때, "
            r"사각형 \(OABC\)의 내부에서 직선 \(l\)이 그려지는 범위의 넓이를 구하시오."
            "\n\n"
            + IMG_TAG
        ),
        choices=(),
        answer=r"\(\dfrac{72}{5}\)",
        solution=(
            r"직선을 \(y=k(x-3)+2\)로 쓰면 모든 직선은 점 \((3,2)\)를 지난다."
            "\n"
            r"그림에서 \(OABC\)는 \(0\le x\le7,\ 0\le y\le7\)인 정사각형이다."
            "\n"
            r"\(k=\dfrac54\)일 때 경계선은 \(y=\dfrac54(x-3)+2\)."
            "\n"
            r"따라서 직선이 지나가는 범위는"
            "\n"
            r"\(x<3\)에서는 \(\max\{0,\dfrac54(x-3)+2\}\le y\le2\),"
            "\n"
            r"\(x>3\)에서는 \(2\le y\le\dfrac54(x-3)+2\)이다."
            "\n"
            r"이 영역을 세 부분으로 나누면"
            "\n"
            r"\(x=0\)부터 \(x=\dfrac75\)까지의 직사각형(가로 \(\dfrac75\), 세로 \(2\)),"
            "\n"
            r"\(x=\dfrac75\)부터 \(x=3\)까지의 삼각형(밑변 \(\dfrac85\), 높이 \(2\)),"
            "\n"
            r"\(x=3\)부터 \(x=7\)까지의 삼각형(밑변 \(4\), 높이 \(5\))이다."
            "\n"
            r"따라서 면적은"
            "\n"
            r"\["
            "\n"
            r"\frac75\cdot2+\frac12\cdot\frac85\cdot2+\frac12\cdot4\cdot5"
            r"=\frac{14}{5}+\frac{8}{5}+10"
            r"=\frac{72}{5}."
            "\n"
            r"\]"
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.SUB03_scan.png",
        ocr_uncertain=True,
        uncertain_note="도형 낙서가 많아 경계 판독(정사각형 OABC) 재확인 권장",
    ),
    Row(
        no=104,
        kind="subjective",
        q=(
            r"그림과 같이 길이가 \(14\text{ cm}\)인 끈의 양 끝을 각각 \(x\text{ cm},\ 2x\text{ cm}\)만큼 자른 후 "
            r"세 조각의 끈을 세 변으로 하는 삼각형을 만들려고 한다. "
            r"세 조각의 끈을 세 변으로 하는 삼각형을 만들 수 있는 \(x\)의 값의 범위를 구하는 과정을 서술하시오."
            "\n"
            r"(단, 끈의 굵기는 무시한다.)"
            "\n\n"
            + IMG_TAG
        ),
        choices=(),
        answer=r"\(\dfrac73<x<\dfrac72\)",
        solution=(
            r"세 변의 길이는 \(x,\ 2x,\ 14-3x\)이다."
            "\n"
            r"삼각형이 되려면"
            "\n"
            r"\["
            "\n"
            r"\begin{cases}"
            r"x+2x>14-3x\\"
            r"x+(14-3x)>2x\\"
            r"2x+(14-3x)>x"
            r"\end{cases}"
            "\n"
            r"\]"
            "\n"
            r"즉"
            "\n"
            r"\(6x>14\Rightarrow x>\dfrac73\),"
            "\n"
            r"\(14>4x\Rightarrow x<\dfrac72\),"
            "\n"
            r"\(14>2x\Rightarrow x<7\) (앞의 조건보다 약함)."
            "\n"
            r"따라서 범위는 \(\dfrac73<x<\dfrac72\)이다."
        ),
        scan_source="HN.2021.G1.S1.Final.COM1.SUB04_scan.png",
    ),
    Row(
        no=105,
        kind="subjective",
        q=(
            r"두 점 \(A(1,5)\), \(B(6,2)\)을 잇는 선분 \(AB\) 위의 한 점 \((x,y)\)에 대하여 "
            r"\(\dfrac{y+3}{x+2}\)의 최댓값과 최솟값을 구하는 과정을 서술하시오."
        ),
        choices=(),
        answer=r"최댓값 \(\dfrac83\), 최솟값 \(\dfrac58\)",
        solution=(
            r"선분 \(AB\)의 직선식은"
            "\n"
            r"\["
            "\n"
            r"y-5=-\frac35(x-1)\Rightarrow y=-\frac35x+\frac{28}{5}."
            "\n"
            r"\]"
            "\n"
            r"따라서"
            "\n"
            r"\["
            "\n"
            r"\frac{y+3}{x+2}=\frac{-3x+43}{5x+10},\qquad 1\le x\le6."
            "\n"
            r"\]"
            "\n"
            r"\(1\le x_1<x_2\le6\)일 때"
            "\n"
            r"\["
            "\n"
            r"\frac{-3x_1+43}{5x_1+10}-\frac{-3x_2+43}{5x_2+10}"
            r"=\frac{-245(x_1-x_2)}{(5x_1+10)(5x_2+10)}>0."
            "\n"
            r"\]"
            "\n"
            r"따라서 \(x\)가 커질수록 값이 작아진다."
            "\n"
            r"따라서"
            "\n"
            r"\(x=1\)에서 최댓값 \(\dfrac83\),"
            "\n"
            r"\(x=6\)에서 최솟값 \(\dfrac58\)이다."
        ),
    ),
    Row(
        no=106,
        kind="subjective",
        q=(
            r"좌표평면 위의 두 점 \(A(0,0)\), \(B(3,4)\)를 연결한 직선 위의 점 \(P\)가 다음을 만족시킨다."
            "\n\n"
            + _box(
                [
                    r"(가) \(n\overline{PA}=m\overline{PB}\)",
                    r"(나) (가)조건을 만족시키는 점들 \(P\) 사이의 거리는 \(3\)이다.",
                    r"(다) \(m>0,\ n>0,\ m>n\)",
                ]
            )
            + "\n\n"
            + r"이 때, \(\dfrac{m}{n}\)의 값을 구하는 과정을 서술하시오."
        ),
        choices=(),
        answer=r"\(\dfrac{m}{n}=\dfrac{5+\sqrt{34}}{3}\)",
        solution=(
            r"\(AB=\sqrt{3^2+4^2}=5\)이다."
            "\n"
            r"\(\dfrac{m}{n}=r\ (r>1)\)라 두면 \(\overline{PA}:\overline{PB}=r:1\)이다."
            "\n"
            r"이 조건을 만족하는 점은 내분점 \(P_1\), 외분점 \(P_2\) 두 개이며"
            "\n"
            r"\["
            "\n"
            r"\overline{AP_1}=\frac{5r}{r+1},\qquad \overline{AP_2}=\frac{5r}{r-1}."
            "\n"
            r"\]"
            "\n"
            r"따라서"
            "\n"
            r"\["
            "\n"
            r"\overline{P_1P_2}=\frac{5r}{r-1}-\frac{5r}{r+1}=\frac{10r}{r^2-1}=3."
            "\n"
            r"\]"
            "\n"
            r"정리하면 \(3r^2-10r-3=0\)이고,"
            "\n"
            r"\["
            "\n"
            r"r=\frac{10\pm\sqrt{136}}{6}=\frac{5\pm\sqrt{34}}{3}."
            "\n"
            r"\]"
            "\n"
            r"\(r>1\)이므로 \(r=\dfrac{5+\sqrt{34}}{3}\)."
            "\n"
            r"즉 \(\dfrac{m}{n}=\dfrac{5+\sqrt{34}}{3}\)이다."
        ),
    ),
]


def pid_from_no(no: int) -> str:
    return f"HN-2021-G1-S1-Final-{no:03d}"


def source_meta(no: int) -> tuple[int, str, str, str]:
    if no >= 100:
        src_no = no - 100
        return src_no, "subjective", f"서답{src_no}번", "서답형"
    return no, "objective", str(no), "객관식"


def classify(row: Row) -> tuple[str, str, str, int, str]:
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
    src_no, src_kind, src_label, qtype_text = source_meta(row.no)
    unit_l1, unit_l2, unit_l3, level, reason = classify(row)
    unit = f"{unit_l1}>{unit_l2}>{unit_l3}"

    assets: List[str] = ["assets/original/", f"assets/original/{PDF_NAME}"]
    if row.scan_source:
        assets.insert(0, "assets/scan.png")
        assets.append(f"assets/original/{row.scan_source}")

    lines: List[str] = [
        "---",
        f"id: {pid}",
        "school: HN",
        "year: 2021",
        "grade: 1",
        "semester: 1",
        "exam: Final",
        "subject: COM1",
        f"type: {qtype_text}",
        f"source_question_no: {src_no}",
        f"source_question_kind: {src_kind}",
        f"source_question_label: '{src_label}'",
        f"difficulty: {level}",
        f"level: {level}",
        f"unit: {unit}",
        f"unit_l1: {unit_l1}",
        f"unit_l2: {unit_l2}",
        f"unit_l3: {unit_l3}",
        f"source: {SOURCE_TAG}",
        "tags:",
        f"- {qtype_text}",
        f"- 출제번호-{src_no}",
        "- 과목-COM1",
        "assets:",
    ]
    for a in assets:
        lines.append(f"- {a}")
    lines.extend(["---", "", "## Q", row.q, "", "## Choices", ""])

    if row.choices:
        labels = ["①", "②", "③", "④", "⑤"]
        for i, c in enumerate(row.choices):
            label = labels[i] if i < len(labels) else f"({i+1})"
            lines.append(f"{label} {c}")

    lines.extend(["", "## Answer", row.answer, "", "## Solution", row.solution, "", f"<!-- classifier_reason: {reason} -->", ""])
    return "\n".join(lines)


def run() -> int:
    src_pdf = ORIGINAL / PDF_NAME
    if not src_pdf.exists():
        print(f"[ERROR] missing-pdf: {src_pdf}")
        return 1

    created = 0
    updated = 0
    skipped = 0
    warnings = 0
    report_lines: List[str] = []
    duplicates: List[str] = []
    uncertain: List[str] = []

    for row in ROWS:
        pid = pid_from_no(row.no)
        pdir = PROBLEMS / pid
        if pdir.exists():
            skipped += 1
            duplicates.append(pid)
            report_lines.append(f"{pid} | SKIP | duplicate-folder")
            continue

        (pdir / "assets" / "original").mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_pdf, pdir / "assets" / "original" / PDF_NAME)

        if row.scan_source:
            src_scan = ORIGINAL / row.scan_source
            if src_scan.exists():
                shutil.copy2(src_scan, pdir / "assets" / "original" / row.scan_source)
                shutil.copy2(src_scan, pdir / "assets" / "scan.png")
            else:
                warnings += 1
                uncertain.append(f"{pid}: supplemental-scan-missing ({row.scan_source})")
                report_lines.append(f"{pid} | WARN | supplemental-scan-missing")

        md = make_problem_md(pid, row)
        (pdir / "problem.md").write_text(md, encoding="utf-8")
        created += 1

        if row.ocr_uncertain:
            uncertain.append(f"{pid}: {row.uncertain_note}")
        report_lines.append(f"{pid} | CREATED | source_no={source_meta(row.no)[0]} kind={row.kind}")

    print("=== SUMMARY ===")
    print(f"created={created}")
    print(f"updated={updated}")
    print(f"skipped_duplicate={skipped}")
    print(f"warnings={warnings}")
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
    print("=== OCR_OR_FORMULA_UNCERTAIN ===")
    if uncertain:
        for u in uncertain:
            print(u)
    else:
        print("(none)")
    print("")
    print("=== QUICK_REVIEW_PATHS ===")
    for row in ROWS:
        pid = pid_from_no(row.no)
        p = PROBLEMS / pid / "problem.md"
        if p.exists():
            print(p.resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
