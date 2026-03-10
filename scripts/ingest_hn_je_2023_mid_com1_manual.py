from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet


PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
REPORT_PATH = ROOT / "_tmp_hn_je_2023_mid_com1_manual_report.txt"

SOURCE_BY_SCHOOL: Dict[str, str] = {
    "HN": "HN.2023.G1.S1.MID.COM1.pdf",
    "JE": "JE.2023.G1.S1.MID.COM1.pdf",
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
class ProblemData:
    pid: str
    qtype: str
    question: str
    choices: str
    answer: str
    solution: str
    source_label: Optional[str] = None


DATA: List[ProblemData] = [
    ProblemData(
        pid="HN-2023-G1-S1-MID-001",
        qtype="객관식",
        question=(
            r"다항식 \(A=x^2+5xy-4y^2\), \(B=2x^2-xy+y^2\)에 대하여 "
            r"\((2A-B)-(A+B)\)를 바르게 계산한 것은?"
        ),
        choices=(
            r"① \(3x^2+7xy+6y^2\)" "\n"
            r"② \(-3x^2+7xy-6y^2\)" "\n"
            r"③ \(2x^2+xy-6y^2\)" "\n"
            r"④ \(2x^2+3xy-6y^2\)" "\n"
            r"⑤ \(2x^2+7xy-y^2\)"
        ),
        answer="②",
        solution=(
            r"\((2A-B)-(A+B)=A-2B\)이므로" "\n"
            r"\[" "\n"
            r"A-2B=(x^2+5xy-4y^2)-2(2x^2-xy+y^2)" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"=x^2+5xy-4y^2-4x^2+2xy-2y^2" "\n"
            r"=-3x^2+7xy-6y^2." "\n"
            r"\]" "\n"
            r"따라서 정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-002",
        qtype="객관식",
        question=r"\(x-y=4,\ xy=-1\)일 때, \(x^3-y^3\)의 값은?",
        choices="① 44\n② 46\n③ 48\n④ 50\n⑤ 52",
        answer="⑤",
        solution=(
            r"\[" "\n"
            r"x^3-y^3=(x-y)(x^2+xy+y^2)" "\n"
            r"\]" "\n"
            r"이고" "\n"
            r"\[" "\n"
            r"x^2+y^2=(x-y)^2+2xy=16-2=14" "\n"
            r"\]" "\n"
            r"이므로" "\n"
            r"\[" "\n"
            r"x^2+xy+y^2=14+(-1)=13." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"x^3-y^3=4\times 13=52" "\n"
            r"\]" "\n"
            r"이므로 정답은 \(⑤\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-004",
        qtype="객관식",
        question=r"다항식 \(P(x)=x^3-x^2+3x+1\)을 일차식 \(x-2\)로 나누었을 때의 나머지는?",
        choices="① 9\n② 10\n③ 11\n④ 12\n⑤ 13",
        answer="③",
        solution=(
            r"나머지정리에 의해 나머지는 \(P(2)\)이다." "\n"
            r"\[" "\n"
            r"P(2)=2^3-2^2+3\cdot 2+1=8-4+6+1=11." "\n"
            r"\]" "\n"
            r"따라서 정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-005",
        qtype="객관식",
        question=(
            r"다항식 \(2x^3-x^2+5x-6\)을 인수분해하면 "
            r"\((x-1)(ax^2+bx+c)\)일 때, \(a+b+c\)의 값은? "
            r"(단, \(a,b,c\)는 상수이다.)"
        ),
        choices="① 9\n② 8\n③ 7\n④ 6\n⑤ 5",
        answer="①",
        solution=(
            r"\[" "\n"
            r"(x-1)(ax^2+bx+c)=ax^3+(b-a)x^2+(c-b)x-c" "\n"
            r"\]" "\n"
            r"이므로 계수 비교를 하면" "\n"
            r"\[" "\n"
            r"a=2,\quad b-a=-1,\quad c-b=5,\quad -c=-6." "\n"
            r"\]" "\n"
            r"따라서 \(a=2,\ b=1,\ c=6\)이므로" "\n"
            r"\[" "\n"
            r"a+b+c=2+1+6=9." "\n"
            r"\]" "\n"
            r"정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-008",
        qtype="객관식",
        question=(
            r"다항식 \(P(x)\)를 일차식 \(x-a\)로 나누었을 때의 몫을 \(Q(x)\), 나머지를 \(R\)라고 할 때, "
            r"\(xP(x)\)를 \(x-a\)로 나누었을 때의 나머지는? "
            r"(단, \(a\)는 상수이다.)"
        ),
        choices=(
            r"① \(\dfrac{R}{a}\)" "\n"
            r"② \(R\)" "\n"
            r"③ \(aR\)" "\n"
            r"④ \(xR\)" "\n"
            r"⑤ \(-aR\)"
        ),
        answer="③",
        solution=(
            r"\[" "\n"
            r"P(x)=(x-a)Q(x)+R" "\n"
            r"\]" "\n"
            r"에서 양변에 \(x\)를 곱하면" "\n"
            r"\[" "\n"
            r"xP(x)=x(x-a)Q(x)+xR." "\n"
            r"\]" "\n"
            r"따라서 \(x-a\)로 나눌 때 나머지는 \(xR\)에 \(x=a\)를 대입한" "\n"
            r"\[" "\n"
            r"aR" "\n"
            r"\]" "\n"
            r"이다. 정답은 \(③\)."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-010",
        qtype="객관식",
        question=(
            r"두 복소수 \(\alpha=-2+\mathrm{i}\), \(\beta=1-2\mathrm{i}\)에 대하여 "
            r"\(\alpha\overline{\alpha}+\alpha\overline{\beta}+\overline{\alpha}\beta+\beta\overline{\beta}\)의 값은? "
            r"(단, \(\overline{\alpha},\overline{\beta}\)는 각각 \(\alpha,\beta\)의 켤레복소수이다.)"
        ),
        choices="① 5\n② 4\n③ 3\n④ 2\n⑤ 1",
        answer="④",
        solution=(
            r"\[" "\n"
            r"\alpha\overline{\alpha}+\alpha\overline{\beta}+\overline{\alpha}\beta+\beta\overline{\beta}" "\n"
            r"=(\alpha+\beta)(\overline{\alpha}+\overline{\beta})" "\n"
            r"=|\alpha+\beta|^2." "\n"
            r"\]" "\n"
            r"\(\alpha+\beta=(-2+\mathrm{i})+(1-2\mathrm{i})=-1-\mathrm{i}\)이므로" "\n"
            r"\[" "\n"
            r"|\alpha+\beta|^2=(-1)^2+(-1)^2=2." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-011",
        qtype="객관식",
        question="다음 중 옳지 않은 것은?",
        choices=(
            r"① \(a>0\)일 때, \(\sqrt{-a}=\sqrt{a}\,\mathrm{i}\)" "\n"
            r"② \(1+2\mathrm{i}\)의 실수부분은 \(1\), 허수부분은 \(2\)이다." "\n"
            r"③ \(\sqrt{-1}\sqrt{-1}=1\)이다." "\n"
            r"④ \(a>0\)일 때, \(-a\)의 제곱근은 \(\sqrt{a}\,\mathrm{i}\)와 \(-\sqrt{a}\,\mathrm{i}\)이다." "\n"
            r"⑤ \(\sqrt{2}\)의 켤레복소수는 \(\sqrt{2}\)이다."
        ),
        answer="③",
        solution=(
            r"\(\sqrt{-1}=\mathrm{i}\)이므로" "\n"
            r"\[" "\n"
            r"\sqrt{-1}\sqrt{-1}=\mathrm{i}^2=-1" "\n"
            r"\]" "\n"
            r"이다. 따라서 ③이 옳지 않다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-014",
        qtype="객관식",
        question=r"이차방정식 \(x^2-6x+k=0\)이 서로 다른 두 실근을 갖도록 하는 정수 \(k\)의 최댓값은?",
        choices="① 8\n② 7\n③ 6\n④ 5\n⑤ 4",
        answer="①",
        solution=(
            r"서로 다른 두 실근을 가지려면 판별식이 \(0\)보다 커야 한다." "\n"
            r"\[" "\n"
            r"\Delta = (-6)^2-4k=36-4k>0" "\n"
            r"\]" "\n"
            r"이므로 \(k<9\). 정수 \(k\)의 최댓값은 \(8\)이다." "\n"
            r"따라서 정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-015",
        qtype="객관식",
        question=(
            r"등식 \(z(3-\mathrm{i})+\overline{z}(2-\mathrm{i})=5\)를 만족시키는 복소수 "
            r"\(z=a+b\mathrm{i}\) (\(a,b\)는 실수)라 할 때, \(a+2b\)의 값은? "
            r"(단, \(\overline{z}\)는 \(z\)의 켤레복소수이다.)"
        ),
        choices="① 2\n② 3\n③ 4\n④ 5\n⑤ 6",
        answer="④",
        solution=(
            r"\(z=a+b\mathrm{i}\), \(\overline{z}=a-b\mathrm{i}\)를 대입하면" "\n"
            r"\[" "\n"
            r"(a+b\mathrm{i})(3-\mathrm{i})+(a-b\mathrm{i})(2-\mathrm{i})=5" "\n"
            r"\]" "\n"
            r"이고, 실수부와 허수부를 비교하면" "\n"
            r"\[" "\n"
            r"5a=5,\quad b-2a=0." "\n"
            r"\]" "\n"
            r"따라서 \(a=1,\ b=2\). 그러므로" "\n"
            r"\[" "\n"
            r"a+2b=1+4=5." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-101",
        qtype="단답형",
        source_label="서답1",
        question=(
            r"이차방정식 \(x^2-3x-11=0\)의 두 근을 \(\alpha,\beta\)라고 할 때, "
            r"두 수 \(\alpha+\beta\)와 \(\alpha\beta\)를 근으로 하고 \(x^2\)의 계수가 \(1\)인 "
            r"이차방정식의 일차항의 계수를 구하시오."
        ),
        choices="",
        answer="8",
        solution=(
            r"주어진 이차방정식에서 근과 계수의 관계로" "\n"
            r"\[" "\n"
            r"\alpha+\beta=3,\quad \alpha\beta=-11." "\n"
            r"\]" "\n"
            r"새 이차방정식의 근은 \(3,\,-11\)이므로" "\n"
            r"\[" "\n"
            r"(x-3)(x+11)=x^2+8x-33." "\n"
            r"\]" "\n"
            r"따라서 일차항의 계수는 \(8\)이다."
        ),
    ),
    ProblemData(
        pid="HN-2023-G1-S1-MID-106",
        qtype="서술형",
        source_label="서답6",
        question=(
            r"실수 \(t\)에 대하여 \(t\le x\le t+1\)에서 이차함수 "
            r"\(f(x)=x^2-8x+18\)의 최댓값을 \(g(t)\)라 할 때, "
            r"방정식 \(g(t)=6\)의 모든 실근의 합을 구하시오."
        ),
        choices="",
        answer="7",
        solution=(
            r"\[" "\n"
            r"f(x)=x^2-8x+18=(x-4)^2+2" "\n"
            r"\]" "\n"
            r"이므로 구간 \([t,t+1]\)에서 최댓값은 양 끝값 중 큰 값이다." "\n"
            r"\[" "\n"
            r"g(t)=\max\{f(t),f(t+1)\}." "\n"
            r"\]" "\n"
            r"또" "\n"
            r"\[" "\n"
            r"f(t+1)-f(t)=2t-7" "\n"
            r"\]" "\n"
            r"이므로 \(t\le \dfrac{7}{2}\)일 때 \(g(t)=f(t)\), \(t\ge \dfrac{7}{2}\)일 때 \(g(t)=f(t+1)\)." "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"t\le \frac72:\ f(t)=6 \Rightarrow t^2-8t+12=0 \Rightarrow t=2,6 \Rightarrow t=2" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"t\ge \frac72:\ f(t+1)=6 \Rightarrow t^2-6t+5=0 \Rightarrow t=1,5 \Rightarrow t=5." "\n"
            r"\]" "\n"
            r"모든 실근은 \(2,5\)이고 합은 \(7\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-001",
        qtype="객관식",
        question=(
            r"다항식 \(A,\ B\)에 대하여 "
            r"\(A+B=4x^2-9x+7,\ A-2B=x^2+3x+1\)일 때, "
            r"\(2A+B=ax^2+bx+c\)이다. 상수 \(a,b,c\)에 대하여 \(a+b+c\)의 값은?"
        ),
        choices="① 4\n② 5\n③ 6\n④ 7\n⑤ 8",
        answer="②",
        solution=(
            r"\[" "\n"
            r"(A+B)-(A-2B)=3B" "\n"
            r"\]" "\n"
            r"이므로" "\n"
            r"\[" "\n"
            r"3B=(4x^2-9x+7)-(x^2+3x+1)=3x^2-12x+6" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"B=x^2-4x+2." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"A=(A+B)-B=3x^2-5x+5" "\n"
            r"\]" "\n"
            r"이고" "\n"
            r"\[" "\n"
            r"2A+B=7x^2-14x+12." "\n"
            r"\]" "\n"
            r"즉 \(a=7,\ b=-14,\ c=12\)이므로" "\n"
            r"\[" "\n"
            r"a+b+c=5." "\n"
            r"\]" "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-002",
        qtype="객관식",
        question=r"다항식 \(x^3-27y^3\)을 인수분해하면?",
        choices=(
            r"① \((x+3y)(x^2-3xy+9y^2)\)" "\n"
            r"② \((x+3y)(x^2+3xy+9y^2)\)" "\n"
            r"③ \((x-3y)(x^2-3xy+9y^2)\)" "\n"
            r"④ \((x-3y)(x^2-3xy-9y^2)\)" "\n"
            r"⑤ \((x-3y)(x^2+3xy+9y^2)\)"
        ),
        answer="⑤",
        solution=(
            r"\[" "\n"
            r"x^3-27y^3=x^3-(3y)^3=(x-3y)(x^2+3xy+9y^2)." "\n"
            r"\]" "\n"
            r"따라서 정답은 \(⑤\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-003",
        qtype="객관식",
        question=r"\(x=1+\sqrt2,\ y=1-\sqrt2\)일 때, \(x^3+y^3+2xy\)의 값을 구하면?",
        choices="① 6\n② 8\n③ 10\n④ 12\n⑤ 14",
        answer="④",
        solution=(
            r"\[" "\n"
            r"x+y=2,\quad xy=(1+\sqrt2)(1-\sqrt2)=-1." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"x^3+y^3=(x+y)^3-3xy(x+y)=8-3(-1)\cdot 2=14" "\n"
            r"\]" "\n"
            r"이고" "\n"
            r"\[" "\n"
            r"x^3+y^3+2xy=14+2(-1)=12." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-004",
        qtype="객관식",
        question=(
            r"다항식 \(P(x)=x^3-ax^2+bx-2\)가 \((x-1)(x+2)\)로 나누어떨어질 때, "
            r"상수 \(ab\)의 값은?"
        ),
        choices="① -1\n② -2\n③ 1\n④ 2\n⑤ 3",
        answer="④",
        solution=(
            r"\((x-1)(x+2)\)로 나누어떨어지므로 \(P(1)=0,\ P(-2)=0\)." "\n"
            r"\[" "\n"
            r"P(1)=1-a+b-2=0 \Rightarrow b=a+1" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"P(-2)=-8-4a-2b-2=0 \Rightarrow 2a+b=-5." "\n"
            r"\]" "\n"
            r"대입하면" "\n"
            r"\[" "\n"
            r"2a+(a+1)=-5 \Rightarrow a=-2,\ b=-1." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"ab=2." "\n"
            r"\]" "\n"
            r"정답은 \(④\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-005",
        qtype="객관식",
        question=(
            r"다음 등식이 \(x\)에 대한 항등식이 되도록 상수 \(a,b\)를 정할 때, "
            r"\(12a+3b\)의 값은?" "\n"
            r"\[" "\n"
            r"2x^2+ax=(2x+1)(x+b)-3" "\n"
            r"\]"
        ),
        choices="① 89\n② 91\n③ 93\n④ 95\n⑤ 97",
        answer="③",
        solution=(
            r"우변을 전개하면" "\n"
            r"\[" "\n"
            r"(2x+1)(x+b)-3=2x^2+(2b+1)x+b-3." "\n"
            r"\]" "\n"
            r"항등식이므로 계수 비교를 하면" "\n"
            r"\[" "\n"
            r"a=2b+1,\quad b-3=0." "\n"
            r"\]" "\n"
            r"따라서 \(b=3,\ a=7\). 그러므로" "\n"
            r"\[" "\n"
            r"12a+3b=12\cdot 7+3\cdot 3=84+9=93." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-007",
        qtype="객관식",
        question=r"다항식 \((x^2-x)^2-8(x^2-x)+12\)를 바르게 인수분해한 것은?",
        choices=(
            r"① \((x-3)(x-1)(x+2)^2\)" "\n"
            r"② \((x-2)^2(x+1)(x+3)\)" "\n"
            r"③ \((x-2)(x+1)(x-3)(x+2)\)" "\n"
            r"④ \((x+1)(x+2)(x+3)(x-2)\)" "\n"
            r"⑤ \((x-1)(x-2)(x-3)(x+2)\)"
        ),
        answer="③",
        solution=(
            r"\(t=x^2-x\)로 두면" "\n"
            r"\[" "\n"
            r"t^2-8t+12=(t-2)(t-6)." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"(x^2-x-2)(x^2-x-6)" "\n"
            r"=(x-2)(x+1)(x-3)(x+2)." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-008",
        qtype="객관식",
        question=(
            r"등식 \(2x+(x-2y)\mathrm{i}=\overline{(4-4\mathrm{i})}\)를 만족시키는 실수 \(x,y\)에 대하여 "
            r"\(x^2+y^2\)의 값은? (단, \(\overline{(4-4\mathrm{i})}\)는 \(4-4\mathrm{i}\)의 켤레복소수이다.)"
        ),
        choices="① 2\n② 5\n③ 8\n④ 9\n⑤ 11",
        answer="②",
        solution=(
            r"\(\overline{(4-4\mathrm{i})}=4+4\mathrm{i}\)이므로" "\n"
            r"\[" "\n"
            r"2x=4,\quad x-2y=4." "\n"
            r"\]" "\n"
            r"첫째 식에서 \(x=2\), 둘째 식에서 \(2-2y=4\Rightarrow y=-1\)." "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"x^2+y^2=2^2+(-1)^2=5." "\n"
            r"\]" "\n"
            r"정답은 \(②\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-010",
        qtype="객관식",
        question=(
            r"두 수 \(3+\sqrt7\,\mathrm{i},\ 3-\sqrt7\,\mathrm{i}\)를 근으로 하고, "
            r"\(x^2\)의 계수가 \(1\)인 이차방정식을 구하면?"
        ),
        choices=(
            r"① \(x^2-6x+16=0\)" "\n"
            r"② \(x^2+6x+16=0\)" "\n"
            r"③ \(x^2+6x-16=0\)" "\n"
            r"④ \(x^2-16x+16=0\)" "\n"
            r"⑤ \(x^2+16x-6=0\)"
        ),
        answer="①",
        solution=(
            r"근의 합은 \(6\), 근의 곱은" "\n"
            r"\[" "\n"
            r"(3+\sqrt7\,\mathrm{i})(3-\sqrt7\,\mathrm{i})=9+7=16." "\n"
            r"\]" "\n"
            r"따라서 구하는 이차방정식은" "\n"
            r"\[" "\n"
            r"x^2-6x+16=0" "\n"
            r"\]" "\n"
            r"이므로 정답은 \(①\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-011",
        qtype="객관식",
        question=(
            r"이차함수 \(y=2x^2+x+a\)의 그래프와 직선 \(y=5x+2\)가 만나지 않도록 "
            r"실수 \(a\)값의 범위는?"
        ),
        choices=r"① \(a>-4\)" "\n" r"② \(a<-8\)" "\n" r"③ \(a>4\)" "\n" r"④ \(a>8\)" "\n" r"⑤ \(a<12\)",
        answer="③",
        solution=(
            r"두 그래프의 교점을 구하는 식은" "\n"
            r"\[" "\n"
            r"2x^2+x+a=5x+2 \Rightarrow 2x^2-4x+(a-2)=0." "\n"
            r"\]" "\n"
            r"만나지 않으려면 실근이 없어야 하므로 판별식이 음수:" "\n"
            r"\[" "\n"
            r"\Delta=(-4)^2-4\cdot 2\cdot (a-2)<0" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"16-8(a-2)<0 \Rightarrow 32-8a<0 \Rightarrow a>4." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-012",
        qtype="객관식",
        question=(
            r"다음 이차방정식 \(x^2-3x-1=0\)의 두 근의 합을 \(\alpha\), 두 근의 곱을 \(\beta\)라고 할 때, "
            r"\(9\alpha-4\beta\)의 값은?"
        ),
        choices="① 29\n② 30\n③ 31\n④ 32\n⑤ 33",
        answer="③",
        solution=(
            r"근과 계수의 관계에서" "\n"
            r"\[" "\n"
            r"\alpha=3,\quad \beta=-1." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"9\alpha-4\beta=9\cdot 3-4(-1)=27+4=31." "\n"
            r"\]" "\n"
            r"정답은 \(③\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-101",
        qtype="서답형",
        source_label="서답1",
        question=(
            r"다항식 \(A,B\)에 대하여 \(A\star B=3A-2B\)라 할 때, "
            r"\((3x^2-2)\star(x^2-3x+2)\)를 계산하시오."
        ),
        choices="",
        answer=r"\(7x^2+6x-10\)",
        solution=(
            r"\[" "\n"
            r"(3x^2-2)\star(x^2-3x+2)=3(3x^2-2)-2(x^2-3x+2)" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"=9x^2-6-2x^2+6x-4" "\n"
            r"=7x^2+6x-10." "\n"
            r"\]" "\n"
            r"따라서 답은 \(\,7x^2+6x-10\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-104",
        qtype="서답형",
        source_label="서답4",
        question=(
            r"\(x\)에 대한 이차방정식 \(x^2-2(a+1)x+a^2+5=0\)이 다음과 같이 근을 가질 때, "
            r"실수 \(a\)의 값 또는 범위를 구하시오." "\n"
            r"(1) 서로 다른 두 실근" "\n"
            r"(2) 중근" "\n"
            r"(3) 서로 다른 두 허근"
        ),
        choices="",
        answer=r"(1) \(a>2\), (2) \(a=2\), (3) \(a<2\)",
        solution=(
            r"판별식을 \(\Delta\)라 하면" "\n"
            r"\[" "\n"
            r"\Delta=[-2(a+1)]^2-4(a^2+5)" "\n"
            r"=4\{(a+1)^2-a^2-5\}=8(a-2)." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"(1)\ \Delta>0 \Rightarrow a>2" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"(2)\ \Delta=0 \Rightarrow a=2" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"(3)\ \Delta<0 \Rightarrow a<2." "\n"
            r"\]" "\n"
            r"즉 정답은 (1) \(a>2\), (2) \(a=2\), (3) \(a<2\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-105",
        qtype="서술형",
        source_label="서답5",
        question=(
            r"어느 직육면체의 겉넓이가 \(76\)이고, 모든 모서리의 길이의 합이 \(36\)일 때, "
            r"이 직육면체의 대각선의 길이를 구하시오."
        ),
        choices="",
        answer=r"\(\sqrt5\)",
        solution=(
            r"직육면체의 세 변의 길이를 \(a,b,c\)라 하면" "\n"
            r"\[" "\n"
            r"2(ab+bc+ca)=76 \Rightarrow ab+bc+ca=38" "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"4(a+b+c)=36 \Rightarrow a+b+c=9." "\n"
            r"\]" "\n"
            r"대각선의 길이를 \(d\)라 하면" "\n"
            r"\[" "\n"
            r"d^2=a^2+b^2+c^2" "\n"
            r"=(a+b+c)^2-2(ab+bc+ca)" "\n"
            r"=9^2-2\cdot 38=81-76=5." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"d=\sqrt5." "\n"
            r"\]"
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-106",
        qtype="서술형",
        source_label="서답6",
        question=(
            r"\[" "\n"
            r"N=\frac{(2023+\sqrt{2022})^3+(2023-\sqrt{2022})^3}{2023}" "\n"
            r"\]" "\n"
            r"라 할 때, 자연수 \(N\)의 일의 자리 수를 구하시오."
        ),
        choices="",
        answer="0",
        solution=(
            r"\(a=2023,\ b=\sqrt{2022}\)로 두면" "\n"
            r"\[" "\n"
            r"N=\frac{(a+b)^3+(a-b)^3}{a}." "\n"
            r"\]" "\n"
            r"항등식 \((a+b)^3+(a-b)^3=2a^3+6ab^2\)를 이용하면" "\n"
            r"\[" "\n"
            r"N=\frac{2a^3+6ab^2}{a}=2(a^2+3b^2)." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"N=2\{2023^2+3\cdot 2022\}=2(4\,092\,529+6\,066)=8\,197\,190." "\n"
            r"\]" "\n"
            r"그러므로 일의 자리 수는 \(0\)이다."
        ),
    ),
    ProblemData(
        pid="JE-2023-G1-S1-MID-107",
        qtype="서술형",
        source_label="서답7",
        question=(
            r"\(x\)에 대한 이차방정식 \(x^2-2kx+k^2-k-3=0\)의 두 실근을 \(\alpha,\beta\)라 할 때, "
            r"\(\alpha^2+\beta^2\)의 최댓값과 최솟값을 구하시오. "
            r"(단, \(-1\le k\le 4\))"
        ),
        choices="",
        answer=r"최댓값 \(46\), 최솟값 \(\dfrac{11}{2}\)",
        solution=(
            r"근과 계수의 관계에서" "\n"
            r"\[" "\n"
            r"\alpha+\beta=2k,\quad \alpha\beta=k^2-k-3." "\n"
            r"\]" "\n"
            r"따라서" "\n"
            r"\[" "\n"
            r"\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta" "\n"
            r"=4k^2-2(k^2-k-3)=2k^2+2k+6." "\n"
            r"\]" "\n"
            r"\[" "\n"
            r"2k^2+2k+6=2\left(k+\frac12\right)^2+\frac{11}{2}" "\n"
            r"\]" "\n"
            r"이므로 최솟값은 \(k=-\dfrac12\)일 때 \(\dfrac{11}{2}\)." "\n"
            r"최댓값은 구간 끝점 비교로" "\n"
            r"\[" "\n"
            r"k=-1\Rightarrow 6,\quad k=4\Rightarrow 46" "\n"
            r"\]" "\n"
            r"이어서 \(46\)이다."
        ),
    ),
]


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
    unit = classify_unit_and_level(
        question_text=data.question,
        choices_text=data.choices,
        answer_text=data.answer,
        solution_text=data.solution,
        qtype=data.qtype,
        grade=FIXED_META["grade"],
        problem_no=number,
    )
    l1, l2, l3 = normalize_unit_triplet(unit.unit_l1, unit.unit_l2, unit.unit_l3)
    source_label = data.source_label or _default_source_label(source_kind=source_kind, source_no=source_no)
    source_pdf = SOURCE_BY_SCHOOL[school]
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
        "difficulty": int(unit.level),
        "level": int(unit.level),
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
        "assets": [
            "assets/original/",
            f"assets/original/{source_pdf}",
        ],
    }


def _write_problem(folder: Path, data: ProblemData) -> None:
    front = _front_matter(data)
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{data.question.strip()}\n\n"
        f"## Choices\n{data.choices.strip()}\n\n"
        f"## Answer\n{data.answer.strip()}\n\n"
        f"## Solution\n{data.solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def _copy_source_pdf(folder: Path, school: str) -> None:
    src = ORIGINAL / SOURCE_BY_SCHOOL[school]
    dst = folder / "assets" / "original" / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)


def main() -> int:
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = [
        "JE-2023-G1-S1-MID 서답/서술 번호 체계가 겹쳐 기존 ID(102,103)와 의미 충돌 가능성 있음.",
    ]
    review_paths: List[str] = []

    for item in DATA:
        school, _, _, _ = _pid_meta(item.pid)
        folder = PROBLEMS / item.pid
        if folder.exists():
            summary["skipped"] += 1
            duplicates.append(item.pid)
            results.append(f"{item.pid} | SKIPPED (folder exists)")
            continue

        try:
            folder.mkdir(parents=True, exist_ok=False)
            (folder / "assets" / "original").mkdir(parents=True, exist_ok=True)
            _copy_source_pdf(folder=folder, school=school)
            _write_problem(folder=folder, data=item)
            summary["created"] += 1
            results.append(f"{item.pid} | CREATED")
            review_paths.append(str(folder / "problem.md"))
        except Exception as exc:  # pragma: no cover
            summary["warnings"] += 1
            msg = f"{item.pid} | WARNING: {exc}"
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
