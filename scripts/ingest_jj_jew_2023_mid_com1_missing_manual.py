from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
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
REPORT_PATH = ROOT / "_tmp_jj_jew_2023_mid_com1_missing_report.txt"

SOURCE_PDF: Dict[str, str] = {
    "JJ": "JJ.2023.G1.S1.MID.COM1.pdf",
    "JEW": "JEW.2023.G1.S1.MID.COM1.pdf",
}

FIXED_META = {
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "subject": "COM1",
    "source": "user_upload_2026-03-06",
    "subjective_offset": 100,
}


@dataclass(frozen=True)
class ScanSpec:
    page: int
    rect: Tuple[float, float, float, float]
    original_name: str


@dataclass(frozen=True)
class ProblemData:
    pid: str
    qtype: str
    question: str
    choices: str
    answer: str
    solution: str
    source_label: Optional[str] = None
    scan_spec: Optional[ScanSpec] = None


DATA: List[ProblemData] = [
    ProblemData(
        pid="JJ-2023-G1-S1-MID-001",
        qtype="객관식",
        question=r"다항식 \((4x^2-x+a)(x^2+x-7)\)의 전개식에서 \(x^2\)의 계수가 \(-23\)일 때, 상수 \(a\)의 값은?",
        choices="① 2\n② 3\n③ 4\n④ 5\n⑤ 6",
        answer="⑤",
        solution=(
            r"\((4x^2-x+a)(x^2+x-7)\)에서 \(x^2\)항은" "\n"
            r"\[" "\n"
            r"4x^2\cdot(-7),\quad (-x)\cdot x,\quad a\cdot x^2" "\n"
            r"\]" "\n"
            r"에서 나온다. 따라서 \(x^2\)의 계수는" "\n"
            r"\[" "\n"
            r"-28-1+a=a-29." "\n"
            r"\]" "\n"
            r"조건에 의해 \(a-29=-23\)이므로" "\n"
            r"\[" "\n"
            r"a=6." "\n"
            r"\]" "\n"
            r"정답은 \(⑤\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-002",
        qtype="객관식",
        scan_spec=ScanSpec(
            page=0,
            rect=(246.0, 343.0, 357.0, 520.0),
            original_name="JJ2023_q2_figure.png",
        ),
        question=(
            r"오른쪽 그림과 같이 세 모서리의 길이가 각각 \(a,\ b,\ c\)인 직육면체의 겉넓이가 \(52\)이고, "
            r"대각선의 길이가 \(\sqrt{29}\)일 때, 모든 모서리의 길이의 합은?" "\n\n"
            r'<img src="assets/scan.png" alt="JJ2023-Q2-figure" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices="① 9\n② 18\n③ 27\n④ 36\n⑤ 45",
        answer="④",
        solution=(
            r"직육면체의 변의 길이를 \(a,b,c\)라 하면" "\n"
            r"\[" "\n"
            r"2(ab+bc+ca)=52 \Rightarrow ab+bc+ca=26" "\n"
            r"\]" "\n"
            r"이고 대각선 조건에서" "\n"
            r"\[" "\n"
            r"a^2+b^2+c^2=29." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"(a+b+c)^2=a^2+b^2+c^2+2(ab+bc+ca)=29+52=81" "\n"
            r"\]" "\n"
            r"이므로 \(a+b+c=9\). 모든 모서리의 길이의 합은" "\n"
            r"\[" "\n"
            r"4(a+b+c)=36." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-004",
        qtype="객관식",
        question=(
            r"\(x\)의 값에 관계없이 등식" "\n"
            r"\[" "\n"
            r"(x-2)^3=a(x+1)^3+b(x+1)^2+c(x+1)+d" "\n"
            r"\]" "\n"
            r"가 항상 성립할 때, 상수 \(a,b,c,d\)에 대하여 \(a+b-c-d\)의 값은?"
        ),
        choices="① -10\n② -9\n③ -8\n④ -7\n⑤ -6",
        answer="③",
        solution=(
            r"\(t=x+1\)로 두면 \(x-2=t-3\)이므로" "\n"
            r"\[" "\n"
            r"(t-3)^3=t^3-9t^2+27t-27." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"a=1,\quad b=-9,\quad c=27,\quad d=-27." "\n"
            r"\]" "\n"
            r"구하는 값은" "\n"
            r"\[" "\n"
            r"a+b-c-d=1-9-27-(-27)=-8." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-005",
        qtype="객관식",
        question=r"\((x^2+4x-4)(x^2+4x+2)-7\)의 인수가 아닌 것은?",
        choices=r"① \(x-3\)" "\n" r"② \(x-1\)" "\n" r"③ \(x+1\)" "\n" r"④ \(x+3\)" "\n" r"⑤ \(x+5\)",
        answer="①",
        solution=(
            r"\(t=x^2+4x\)로 두면" "\n"
            r"\[" "\n"
            r"(t-4)(t+2)-7=t^2-2t-15=(t-5)(t+3)." "\n"
            r"\]" "\n"
            r"원래 식으로 바꾸면" "\n"
            r"\[" "\n"
            r"(x^2+4x-5)(x^2+4x+3)" "\n"
            r"=(x-1)(x+5)(x+1)(x+3)." "\n"
            r"\]" "\n"
            r"따라서 인수가 아닌 것은 \(x-3\)이고 정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-009",
        qtype="객관식",
        question=(
            r"이차함수 \(y=2x^2+3x\)의 그래프와 직선 \(y=5x+m-3\)이 만나지 않도록 하는 "
            r"자연수 \(m\)의 개수는?"
        ),
        choices="① 1\n② 2\n③ 3\n④ 4\n⑤ 5",
        answer="②",
        solution=(
            r"교점을 구하는 방정식은" "\n"
            r"\[" "\n"
            r"2x^2+3x=5x+m-3" "\n"
            r"\Rightarrow 2x^2-2x+(3-m)=0." "\n"
            r"\]" "\n"
            r"만나지 않으려면 판별식이 음수이므로" "\n"
            r"\[" "\n"
            r"\Delta=(-2)^2-4\cdot 2\cdot (3-m)<0" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"4-8(3-m)<0 \Rightarrow 8m-20<0 \Rightarrow m<\frac52." "\n"
            r"\]" "\n"
            r"자연수 \(m\)은 \(1,2\) 두 개이므로 정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-010",
        qtype="객관식",
        question=(
            r"두 복소수 \(\alpha=-2+\mathrm{i},\ \beta=1-2\mathrm{i}\)에 대하여 "
            r"\(\alpha\overline{\alpha}+\alpha\overline{\beta}+\overline{\alpha}\beta+\beta\overline{\beta}\)의 값은? "
            r"(단, \(\overline{\alpha},\overline{\beta}\)는 각각 \(\alpha,\beta\)의 켤레복소수이다.)"
        ),
        choices="① 1\n② 2\n③ 3\n④ 4\n⑤ 5",
        answer="②",
        solution=(
            r"\[" "\n"
            r"\alpha\overline{\alpha}+\alpha\overline{\beta}+\overline{\alpha}\beta+\beta\overline{\beta}" "\n"
            r"=(\alpha+\beta)(\overline{\alpha}+\overline{\beta})=|\alpha+\beta|^2." "\n"
            r"\]" "\n"
            r"\(\alpha+\beta=-1-\mathrm{i}\)이므로" "\n"
            r"\[" "\n"
            r"|\alpha+\beta|^2=(-1)^2+(-1)^2=2." "\n"
            r"\]" "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-014",
        qtype="객관식",
        question=r"이차방정식 \(x^2+ax+b=0\)의 한 근이 \(2-\sqrt2\,\mathrm{i}\)일 때, 실수 \(a,b\)에 대하여 \(b-a\)의 값은?",
        choices="① 2\n② 4\n③ 6\n④ 8\n⑤ 10",
        answer="⑤",
        solution=(
            r"계수가 실수이므로 다른 한 근은 \(2+\sqrt2\,\mathrm{i}\)이다." "\n"
            r"근의 합과 곱에서" "\n"
            r"\[" "\n"
            r"(2-\sqrt2\,\mathrm{i})+(2+\sqrt2\,\mathrm{i})=4=-a \Rightarrow a=-4" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"(2-\sqrt2\,\mathrm{i})(2+\sqrt2\,\mathrm{i})=4+2=6=b." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"b-a=6-(-4)=10." "\n"
            r"\]" "\n"
            r"정답은 \(⑤\)이다."
        ),
    ),
    ProblemData(
        pid="JJ-2023-G1-S1-MID-106",
        qtype="서술형",
        source_label="서답6",
        question=(
            r"복소수 \(z=-1+3\mathrm{i}\)에 대하여" "\n"
            r"\[" "\n"
            r"\frac{z+1}{\overline{z}}-\frac{\overline{z}-1}{z}=a+b\mathrm{i}" "\n"
            r"\]" "\n"
            r"일 때, 실수 \(a,b\)에 대하여 \(a-b\)의 값을 구하시오. "
            r"(단, \(\overline{z}\)는 \(z\)의 켤레복소수이다.)"
        ),
        choices="",
        answer="1",
        solution=(
            r"\(z=-1+3\mathrm{i},\ \overline{z}=-1-3\mathrm{i}\)." "\n"
            r"\[" "\n"
            r"\frac{z+1}{\overline{z}}=\frac{3\mathrm{i}}{-1-3\mathrm{i}}"
            r"=\frac{-9-3\mathrm{i}}{10}" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"\frac{\overline{z}-1}{z}=\frac{-2-3\mathrm{i}}{-1+3\mathrm{i}}"
            r"=\frac{-7+9\mathrm{i}}{10}" "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"\frac{z+1}{\overline{z}}-\frac{\overline{z}-1}{z}" "\n"
            r"=\frac{-9-3\mathrm{i}-(-7+9\mathrm{i})}{10}" "\n"
            r"=-\frac15-\frac65\mathrm{i}." "\n"
            r"\]" "\n"
            r"즉 \(a=-\frac15,\ b=-\frac65\)이므로" "\n"
            r"\[" "\n"
            r"a-b=-\frac15-\left(-\frac65\right)=1." "\n"
            r"\]"
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-001",
        qtype="객관식",
        question=(
            r"두 다항식 \(A=x^2+3x-1,\ B=2x^3-3x^2+5\)에 대하여 "
            r"\(A-2B\)를 계산한 것으로 알맞은 것은?"
        ),
        choices=(
            r"① \(4x^3-5x^2+3x+9\)" "\n"
            r"② \(-4x^3+5x^2+3x+9\)" "\n"
            r"③ \(-4x^3+7x^2+3x-9\)" "\n"
            r"④ \(-4x^3+7x^2+3x-11\)" "\n"
            r"⑤ \(-4x^3+7x^2-3x-11\)"
        ),
        answer="④",
        solution=(
            r"\[" "\n"
            r"A-2B=(x^2+3x-1)-2(2x^3-3x^2+5)" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"=x^2+3x-1-4x^3+6x^2-10" "\n"
            r"=-4x^3+7x^2+3x-11." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-002",
        qtype="객관식",
        question=r"다음 등식을 만족시키는 실수 \(x,y\)에 대해 \(x+y\)의 값은? \[2x+(x-2y)\mathrm{i}=4+6\mathrm{i}\]",
        choices="① 0\n② 2\n③ 4\n④ 6\n⑤ 8",
        answer="①",
        solution=(
            r"실수부와 허수부를 비교하면" "\n"
            r"\[" "\n"
            r"2x=4,\quad x-2y=6." "\n"
            r"\]" "\n"
            r"따라서 \(x=2\), 그리고 \(2-2y=6\Rightarrow y=-2\)." "\n"
            r"그러므로" "\n"
            r"\[" "\n"
            r"x+y=2+(-2)=0." "\n"
            r"\]" "\n"
            r"정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-003",
        qtype="객관식",
        question=r"다음 중 방정식 \(2x^3+x^2-2x-1=0\)의 근은?",
        choices="① 1\n② 2\n③ 3\n④ 4\n⑤ 5",
        answer="①",
        solution=(
            r"\(x=1\)을 대입하면" "\n"
            r"\[" "\n"
            r"2(1)^3+(1)^2-2(1)-1=2+1-2-1=0" "\n"
            r"\]" "\n"
            r"이므로 \(x=1\)은 근이다. 정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-004",
        qtype="객관식",
        question=r"\(x\)에 대한 이차함수 \(y=x^2-2kx+2k-1\)의 그래프가 \(x\)축과 한 점에서 만나도록 하는 실수 \(k\)의 값은?",
        choices="① 0\n② 1\n③ 2\n④ 3\n⑤ 5",
        answer="②",
        solution=(
            r"\(x\)축과 한 점에서 만나려면 판별식이 \(0\)이어야 한다." "\n"
            r"\[" "\n"
            r"\Delta=(-2k)^2-4(2k-1)=4(k^2-2k+1)=4(k-1)^2." "\n"
            r"\]" "\n"
            r"\(\Delta=0\Rightarrow (k-1)^2=0\Rightarrow k=1\)." "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-006",
        qtype="객관식",
        question=r"이차방정식 \(x^2-5x+k=0\)이 서로 다른 두 허근을 갖도록 하는 정수 \(k\)의 최솟값은?",
        choices="① 4\n② 5\n③ 6\n④ 7\n⑤ 8",
        answer="④",
        solution=(
            r"서로 다른 두 허근을 가지려면 판별식이 음수여야 한다." "\n"
            r"\[" "\n"
            r"\Delta=25-4k<0 \Rightarrow k>\frac{25}{4}=6.25." "\n"
            r"\]" "\n"
            r"정수 \(k\)의 최솟값은 \(7\)이므로 정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-007",
        qtype="객관식",
        question=r"\(x+y=3,\ xy=-2\)일 때, \(x^3+y^3\)의 값은?",
        choices="① 43\n② 44\n③ 45\n④ 46\n⑤ 47",
        answer="③",
        solution=(
            r"\[" "\n"
            r"x^3+y^3=(x+y)^3-3xy(x+y)" "\n"
            r"\]" "\n"
            r"이므로" "\n"
            r"\[" "\n"
            r"x^3+y^3=3^3-3(-2)\cdot 3=27+18=45." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-008",
        qtype="객관식",
        question=(
            r"다음 연립방정식" "\n"
            r"\[" "\n"
            r"\begin{cases}" "\n"
            r"x-y=1\\"
            r"x^2+2xy+y^2=9"
            r"\end{cases}" "\n"
            r"\]" "\n"
            r"의 해는?"
        ),
        choices=(
            r"① \(\begin{cases}x=1\\y=2\end{cases}\) 또는 \(\begin{cases}x=-1\\y=-2\end{cases}\)" "\n"
            r"② \(\begin{cases}x=2\\y=1\end{cases}\) 또는 \(\begin{cases}x=-1\\y=-2\end{cases}\)" "\n"
            r"③ \(\begin{cases}x=2\\y=1\end{cases}\) 또는 \(\begin{cases}x=-2\\y=-1\end{cases}\)" "\n"
            r"④ \(\begin{cases}x=2\\y=1\end{cases}\) 또는 \(\begin{cases}x=1\\y=2\end{cases}\)" "\n"
            r"⑤ \(\begin{cases}x=1\\y=2\end{cases}\) 또는 \(\begin{cases}x=-2\\y=-1\end{cases}\)"
        ),
        answer="②",
        solution=(
            r"둘째 식은 \((x+y)^2=9\)이므로" "\n"
            r"\[" "\n"
            r"x+y=3 \quad \text{또는} \quad x+y=-3." "\n"
            r"\]" "\n"
            r"또 \(x-y=1\)과 함께 풀면" "\n"
            r"\[" "\n"
            r"x+y=3 \Rightarrow (x,y)=(2,1)," "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"x+y=-3 \Rightarrow (x,y)=(-1,-2)." "\n"
            r"\]" "\n"
            r"따라서 정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-009",
        qtype="객관식",
        question=r"이차함수 \(y=x^2+ax+b\)의 그래프가 \(x\)축과 두 점 \((-4,0),\ (2,0)\)에서 만날 때, 실수 \(a,b\)의 값은?",
        choices=(
            r"① \(a=-2,\ b=4\)" "\n"
            r"② \(a=-2,\ b=-8\)" "\n"
            r"③ \(a=-2,\ b=8\)" "\n"
            r"④ \(a=2,\ b=-8\)" "\n"
            r"⑤ \(a=2,\ b=8\)"
        ),
        answer="④",
        solution=(
            r"근이 \(-4,\ 2\)이므로" "\n"
            r"\[" "\n"
            r"y=(x+4)(x-2)=x^2+2x-8." "\n"
            r"\]" "\n"
            r"따라서 \(a=2,\ b=-8\)이고 정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-010",
        qtype="객관식",
        question=(
            r"\(x\)의 값에 관계없이 등식" "\n"
            r"\[" "\n"
            r"(x-2)^3=a(x-1)^3+b(x-1)^2+c(x-1)+d" "\n"
            r"\]" "\n"
            r"가 항상 성립할 때, 상수 \(a,b,c,d\)에 대하여 \(a+b+c+d\)의 값은?"
        ),
        choices="① -1\n② 0\n③ 1\n④ 2\n⑤ 3",
        answer="②",
        solution=(
            r"\(t=x-1\)로 두면 \(x-2=t-1\)이므로" "\n"
            r"\[" "\n"
            r"(t-1)^3=t^3-3t^2+3t-1." "\n"
            r"\]" "\n"
            r"따라서 \(a=1,\ b=-3,\ c=3,\ d=-1\)이므로" "\n"
            r"\[" "\n"
            r"a+b+c+d=1-3+3-1=0." "\n"
            r"\]" "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-012",
        qtype="객관식",
        question=(
            r"방정식 \(x^3-1=0\)의 한 허근을 \(\omega\)라고 할 때, "
            r"\(\dfrac{\omega+\overline{\omega}}{\omega\overline{\omega}}\)의 값은?"
        ),
        choices="① -2\n② -1\n③ 0\n④ 1\n⑤ 2",
        answer="②",
        solution=(
            r"\(\omega\)는 \(1\)이 아닌 세제곱근이므로" "\n"
            r"\[" "\n"
            r"\omega^2+\omega+1=0,\quad \overline{\omega}=\omega^2,\quad \omega\overline{\omega}=1." "\n"
            r"\]" "\n"
            r"또 \(\omega+\omega^2=-1\)이므로" "\n"
            r"\[" "\n"
            r"\frac{\omega+\overline{\omega}}{\omega\overline{\omega}}" "\n"
            r"=\frac{\omega+\omega^2}{1}=-1." "\n"
            r"\]" "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-013",
        qtype="객관식",
        question=(
            r"다항식 \(P(x),Q(x)\)에 대하여 \(P(x)\)를 \(x-1\)로 나눈 나머지가 \(8\)이고, "
            r"\(P(x)+2Q(x)\)가 \(x-1\)로 나누어떨어질 때, "
            r"\(Q(x)\)를 \(x-1\)로 나눈 나머지는?"
        ),
        choices="① 0\n② -1\n③ -2\n④ -3\n⑤ -4",
        answer="⑤",
        solution=(
            r"\(P(1)=8\)." "\n"
            r"또 \(P(x)+2Q(x)\)가 \(x-1\)로 나누어떨어지므로" "\n"
            r"\[" "\n"
            r"P(1)+2Q(1)=0." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"8+2Q(1)=0 \Rightarrow Q(1)=-4." "\n"
            r"\]" "\n"
            r"즉 \(Q(x)\)를 \(x-1\)로 나눈 나머지는 \(-4\)이고 정답은 \(⑤\)이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-101",
        qtype="서답형(단답형)",
        source_label="서답1",
        question=r"이차함수 \(y=x^2+2x+3\)의 그래프와 직선 \(y=-2x-3\)의 교점의 개수를 구하시오.",
        choices="",
        answer="0개",
        solution=(
            r"두 식을 같게 두면" "\n"
            r"\[" "\n"
            r"x^2+2x+3=-2x-3 \Rightarrow x^2+4x+6=0." "\n"
            r"\]" "\n"
            r"판별식은" "\n"
            r"\[" "\n"
            r"\Delta=4^2-4\cdot 1\cdot 6=16-24=-8<0" "\n"
            r"\]" "\n"
            r"이므로 실수 교점이 없다. 따라서 교점의 개수는 \(0\)개이다."
        ),
    ),
    ProblemData(
        pid="JEW-2023-G1-S1-MID-102",
        qtype="서답형(단답형)",
        source_label="서답2",
        question=r"\((x^2+x+1)(x^2+x-2)\)를 전개하시오.",
        choices="",
        answer=r"\(x^4+2x^3-x-2\)",
        solution=(
            r"\(t=x^2+x\)로 두면" "\n"
            r"\[" "\n"
            r"(x^2+x+1)(x^2+x-2)=(t+1)(t-2)=t^2-t-2." "\n"
            r"\]" "\n"
            r"다시 \(t=x^2+x\)를 대입하면" "\n"
            r"\[" "\n"
            r"t^2-t-2=(x^2+x)^2-(x^2+x)-2" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"=x^4+2x^3+x^2-x^2-x-2=x^4+2x^3-x-2." "\n"
            r"\]"
        ),
    ),
]


def _expected_ids() -> List[str]:
    jj = [f"JJ-2023-G1-S1-MID-{i:03d}" for i in range(1, 16)] + [f"JJ-2023-G1-S1-MID-{i:03d}" for i in range(101, 107)]
    jew = [f"JEW-2023-G1-S1-MID-{i:03d}" for i in range(1, 18)] + [f"JEW-2023-G1-S1-MID-{i:03d}" for i in range(101, 107)]
    return jj + jew


def _pid_meta(pid: str) -> Tuple[str, int, str, int]:
    school = pid.split("-", 1)[0]
    number = int(pid.rsplit("-", 1)[-1])
    if number >= FIXED_META["subjective_offset"]:
        source_no = number - FIXED_META["subjective_offset"]
        source_kind = "subjective"
    else:
        source_no = number
        source_kind = "objective"
    return school, number, source_kind, source_no


def _default_source_label(source_kind: str, source_no: int) -> str:
    if source_kind == "objective":
        return str(source_no)
    return f"서답{source_no}"


def _front_matter(data: ProblemData) -> Dict[str, object]:
    school, number, source_kind, source_no = _pid_meta(data.pid)
    cls = classify_unit_and_level(
        question_text=data.question,
        choices_text=data.choices,
        answer_text=data.answer,
        solution_text=data.solution,
        qtype=data.qtype,
        grade=FIXED_META["grade"],
        problem_no=number,
    )
    l1, l2, l3 = normalize_unit_triplet(cls.unit_l1, cls.unit_l2, cls.unit_l3)
    # PDF subject is COM1; keep unit hierarchy inside COM1 even when keyword classifier drifts.
    if not l1.startswith("공통수학1"):
        l1, l2, l3 = normalize_unit_triplet("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산")
    source_label = data.source_label or _default_source_label(source_kind=source_kind, source_no=source_no)
    return {
        "id": data.pid,
        "school": school,
        "year": FIXED_META["year"],
        "grade": FIXED_META["grade"],
        "semester": FIXED_META["semester"],
        "exam": FIXED_META["exam"],
        "subject": FIXED_META["subject"],
        "type": data.qtype,
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": source_label,
        "difficulty": int(cls.level),
        "level": int(cls.level),
        "unit": f"{l1}>{l2}>{l3}",
        "unit_l1": l1,
        "unit_l2": l2,
        "unit_l3": l3,
        "source": FIXED_META["source"],
        "tags": [
            "수동작성",
            data.qtype,
            f"출제번호-{source_label}",
        ],
        "assets": [],
    }


def _save_scan_if_needed(data: ProblemData, folder: Path, source_pdf_path: Path) -> Tuple[List[str], Optional[str]]:
    assets_extra: List[str] = []
    warning: Optional[str] = None

    if data.scan_spec is None:
        return assets_extra, warning

    try:
        doc = fitz.open(source_pdf_path)
        page = doc[data.scan_spec.page]
        rect = fitz.Rect(*data.scan_spec.rect)
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
        scan_path = folder / "assets" / "scan.png"
        scan_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(scan_path)
        raw_scan_path = folder / "assets" / "original" / data.scan_spec.original_name
        pix.save(raw_scan_path)
        assets_extra.extend(["assets/scan.png", f"assets/original/{data.scan_spec.original_name}"])
    except Exception as exc:  # pragma: no cover
        warning = f"{data.pid}: scan generation failed ({exc})"
    finally:
        try:
            doc.close()
        except Exception:  # pragma: no cover
            pass

    return assets_extra, warning


def _write_problem(folder: Path, data: ProblemData) -> Optional[str]:
    school, _, _, _ = _pid_meta(data.pid)
    source_pdf_name = SOURCE_PDF[school]
    source_pdf_path = ORIGINAL / source_pdf_name

    (folder / "assets" / "original").mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_pdf_path, folder / "assets" / "original" / source_pdf_name)

    front = _front_matter(data)
    scan_assets, warning = _save_scan_if_needed(data=data, folder=folder, source_pdf_path=source_pdf_path)
    assets = []
    assets.extend(scan_assets[:1] if scan_assets and scan_assets[0] == "assets/scan.png" else [])
    assets.append("assets/original/")
    assets.append(f"assets/original/{source_pdf_name}")
    for item in scan_assets:
        if item.startswith("assets/original/"):
            assets.append(item)
    front["assets"] = assets

    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{data.question.strip()}\n\n"
        f"## Choices\n{data.choices.strip()}\n\n"
        f"## Answer\n{data.answer.strip()}\n\n"
        f"## Solution\n{data.solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")
    return warning


def main() -> int:
    data_by_pid = {d.pid: d for d in DATA}
    expected = _expected_ids()

    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = [
        "JEW-2023-G1-S1-MID-008: 스캔 원본 화질로 인해 선택지 일부 서식(중괄호 배치)은 복원 작성함.",
        "JEW-2023-G1-S1-MID-012: 분수식은 원본 판독 결과를 바탕으로 \\(\\frac{\\omega+\\overline{\\omega}}{\\omega\\overline{\\omega}}\\)로 복원함.",
    ]
    review_paths: List[str] = []

    for pid in expected:
        folder = PROBLEMS / pid
        if folder.exists():
            summary["skipped"] += 1
            duplicates.append(pid)
            results.append(f"{pid} | SKIPPED (folder exists)")
            continue

        data = data_by_pid.get(pid)
        if data is None:
            summary["warnings"] += 1
            msg = f"{pid} | WARNING: no manual data for missing folder"
            warnings.append(msg)
            results.append(msg)
            continue

        try:
            folder.mkdir(parents=True, exist_ok=False)
            scan_warning = _write_problem(folder=folder, data=data)
            summary["created"] += 1
            results.append(f"{pid} | CREATED")
            review_paths.append(str(folder / "problem.md"))
            if scan_warning:
                summary["warnings"] += 1
                warnings.append(scan_warning)
        except Exception as exc:  # pragma: no cover
            summary["warnings"] += 1
            msg = f"{pid} | WARNING: {exc}"
            warnings.append(msg)
            results.append(msg)

    report_lines: List[str] = []
    report_lines.append(
        f"created={summary['created']} updated={summary['updated']} skipped={summary['skipped']} warnings={summary['warnings']}"
    )
    report_lines.append("")
    report_lines.append("[FILES]")
    report_lines.extend(results or ["none"])
    report_lines.append("")
    report_lines.append("[DUPLICATE_FOLDERS]")
    report_lines.extend(duplicates or ["none"])
    report_lines.append("")
    report_lines.append("[OCR_UNCERTAIN]")
    report_lines.extend(uncertain or ["none"])
    report_lines.append("")
    report_lines.append("[WARNINGS]")
    report_lines.extend(warnings or ["none"])
    report_lines.append("")
    report_lines.append("[REVIEW_PATHS]")
    report_lines.extend(review_paths or ["none"])

    REPORT_PATH.write_text("\n".join(report_lines).strip() + "\n", encoding="utf-8")
    print(REPORT_PATH)
    print("\n".join(report_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
