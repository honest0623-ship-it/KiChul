from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
import textwrap
from typing import Dict, List, Optional, Sequence, Tuple

import fitz
from PIL import Image
import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level  # noqa: E402
from unit_taxonomy import normalize_unit_triplet  # noqa: E402


ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"
REPORT = ROOT / "_tmp_hn_jj_2022_g2_s1_mid_alg_ingest_report.txt"
SOURCE = "user_upload_2026-03-06"
PIXEL_SCALE = 2.5
UNIT_L1 = "대수(2022개정)"


def _q(text: str) -> str:
    return textwrap.dedent(text).strip()


def _scan(alt: str) -> str:
    return (
        f'\n\n<img src="assets/scan.png" alt="{alt}" '
        'style="width:60% !important; max-width:60% !important; height:auto;" />'
    )


def _box(lines: Sequence[str]) -> str:
    joined = "<br />\n".join(lines)
    return f'<div style="border:1px solid #000; padding:8px; margin:8px 0;">{joined}</div>'


@dataclass(frozen=True)
class ProblemRow:
    page_no: int
    crop_box: Tuple[int, int, int, int]
    source_no: int
    kind: str
    question: str
    choices: Tuple[str, ...]
    answer: str
    solution: str
    unit_l2: str
    unit_l3: str
    scan_file: Optional[str] = None
    note: str = ""


@dataclass(frozen=True)
class ExamSpec:
    label: str
    school: str
    year: int
    grade: int
    semester: int
    exam: str
    subject: str
    source_pdf: str
    rows: Sequence[ProblemRow]


def obj(
    *,
    page_no: int,
    crop_box: Tuple[int, int, int, int],
    source_no: int,
    question: str,
    choices: Sequence[str],
    answer: str,
    solution: str,
    unit_l2: str,
    unit_l3: str,
    scan_file: Optional[str] = None,
    note: str = "",
) -> ProblemRow:
    return ProblemRow(
        page_no=page_no,
        crop_box=crop_box,
        source_no=source_no,
        kind="objective",
        question=question,
        choices=tuple(choices),
        answer=answer,
        solution=solution,
        unit_l2=unit_l2,
        unit_l3=unit_l3,
        scan_file=scan_file,
        note=note,
    )


def sub(
    *,
    page_no: int,
    crop_box: Tuple[int, int, int, int],
    source_no: int,
    question: str,
    answer: str,
    solution: str,
    unit_l2: str,
    unit_l3: str,
    scan_file: Optional[str] = None,
    note: str = "",
) -> ProblemRow:
    return ProblemRow(
        page_no=page_no,
        crop_box=crop_box,
        source_no=source_no,
        kind="subjective",
        question=question,
        choices=(),
        answer=answer,
        solution=solution,
        unit_l2=unit_l2,
        unit_l3=unit_l3,
        scan_file=scan_file,
        note=note,
    )


HN_ROWS: List[ProblemRow] = [
    obj(
        page_no=1,
        crop_box=(40, 180, 880, 450),
        source_no=1,
        question=_q(
            r"""
            $\sqrt[3]{3}\times\sqrt[3]{9}$을 간단히 하면?
            """
        ),
        choices=(r"$3$", r"$9$", r"$15$", r"$21$", r"$27$"),
        answer="①",
        solution=_q(
            r"""
            \[
            \sqrt[3]{3}\times\sqrt[3]{9}
            =\sqrt[3]{27}
            =3
            \]
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(40, 430, 880, 800),
        source_no=2,
        question=_q(
            r"""
            $\log_3 81$을 구하면?
            """
        ),
        choices=(r"$3$", r"$4$", r"$5$", r"$6$", r"$7$"),
        answer="②",
        solution=_q(
            r"""
            $81=3^4$이므로
            \[
            \log_3 81=4
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(40, 790, 880, 1200),
        source_no=3,
        question=_q(
            r"""
            $\sqrt[11]{\sqrt[3]{125^{11}}}-\sqrt[5]{-243}$을 간단히 하면?
            """
        ),
        choices=(r"$4$", r"$5$", r"$6$", r"$7$", r"$8$"),
        answer="⑤",
        solution=_q(
            r"""
            \[
            \sqrt[11]{\sqrt[3]{125^{11}}}
            =\sqrt[11]{125^{11/3}}
            =125^{1/3}
            =5
            \]
            이고,
            \[
            \sqrt[5]{-243}=-3
            \]
            이므로
            \[
            5-(-3)=8
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(40, 1180, 900, 1550),
        source_no=4,
        question=_q(
            r"""
            실수 $x$, $y$에 대하여 $3^x=30^y=100$일 때, $\dfrac{1}{x}-\dfrac{1}{y}$의 값은?
            """
        ),
        choices=(r"$-2$", r"$-1$", r"$-\dfrac{1}{2}$", r"$\dfrac{1}{2}$", r"$1$"),
        answer="③",
        solution=_q(
            r"""
            $3^x=100$이므로 $x=\log_3 100$이고, $30^y=100$이므로 $y=\log_{30}100$이다.

            따라서
            \[
            \frac{1}{x}=\log_{100}3,\qquad \frac{1}{y}=\log_{100}30
            \]
            이다.

            그러므로
            \[
            \frac{1}{x}-\frac{1}{y}
            =\log_{100}3-\log_{100}30
            =\log_{100}\frac{1}{10}
            =-\frac{1}{2}
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 90, 1790, 430),
        source_no=5,
        question=_q(
            r"""
            $\log_3 5\times\log_7 27\times\log_5 7$의 값은?
            """
        ),
        choices=(r"$\dfrac{3}{2}$", r"$2$", r"$\dfrac{5}{2}$", r"$3$", r"$\dfrac{7}{2}$"),
        answer="④",
        solution=_q(
            r"""
            \[
            \log_3 5\times\log_5 7=\log_3 7
            \]
            이므로
            \[
            \log_3 7\times\log_7 27=\log_3 27=3
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 400, 1790, 790),
        source_no=6,
        question=_q(
            r"""
            $\log\sqrt{10^3}\times\log\dfrac{1}{\sqrt[3]{100}}$의 값은?
            """
        ),
        choices=(r"$-\dfrac{5}{4}$", r"$-1$", r"$-\dfrac{3}{4}$", r"$-\dfrac{1}{2}$", r"$-\dfrac{1}{4}$"),
        answer="②",
        solution=_q(
            r"""
            \[
            \log\sqrt{10^3}=\log 10^{3/2}=\frac{3}{2}
            \]
            이고,
            \[
            \log\frac{1}{\sqrt[3]{100}}
            =\log 100^{-1/3}
            =\log 10^{-2/3}
            =-\frac{2}{3}
            \]
            이다.

            따라서
            \[
            \frac{3}{2}\times\left(-\frac{2}{3}\right)=-1
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 770, 1790, 1180),
        source_no=7,
        question=_q(
            r"""
            $a>1$, $b>1$일 때, $\left(\log_a b^2\right)^2+\left(\log_b a^2\right)^2$의 최솟값은?
            """
        ),
        choices=(r"$4$", r"$5$", r"$6$", r"$7$", r"$8$"),
        answer="⑤",
        solution=_q(
            r"""
            $t=\log_a b$라고 하면
            \[
            \log_a b^2=2t,\qquad \log_b a^2=\frac{2}{t}
            \]
            이다.

            따라서 주어진 식은
            \[
            4t^2+\frac{4}{t^2}=4\left(t^2+\frac{1}{t^2}\right)
            \]
            이다.

            $t^2+\dfrac{1}{t^2}\ge 2$이므로 최솟값은
            \[
            8
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 1160, 1790, 1600),
        source_no=8,
        question=_q(
            r"""
            정의역이 $\{x\mid -1\le x\le 2\}$일 때, 함수 $y=3^{x-1}+2$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M+9m$의 값은?
            """
        ),
        choices=(r"$23$", r"$24$", r"$25$", r"$26$", r"$27$"),
        answer="②",
        solution=_q(
            r"""
            함수 $y=3^{x-1}+2$는 증가함수이므로
            \[
            M=3+2=5,\qquad
            m=3^{-2}+2=\frac{1}{9}+2=\frac{19}{9}
            \]
            이다.

            따라서
            \[
            M+9m=5+19=24
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    obj(
        page_no=2,
        crop_box=(40, 90, 900, 590),
        source_no=9,
        question=_q(
            r"""
            어느 금융 상품에 $A$만원을 투자할 때 $t$년 후의 이익금은 $A\left(\dfrac{3}{2}\right)^{\frac{t}{4}}$만원이라고 한다. 이 금융 상품에 $1000$만원을 투자할 때, 이익금이 $3375$만원이 되는 것은 투자한 지 몇 년 후인가?
            """
        ),
        choices=("8년", "10년", "12년", "14년", "16년"),
        answer="③",
        solution=_q(
            r"""
            \[
            1000\left(\frac{3}{2}\right)^{t/4}=3375
            \]
            이므로
            \[
            \left(\frac{3}{2}\right)^{t/4}=\frac{3375}{1000}
            =\frac{27}{8}
            =\left(\frac{3}{2}\right)^3
            \]
            이다.

            따라서
            \[
            \frac{t}{4}=3,\qquad t=12
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    obj(
        page_no=2,
        crop_box=(40, 560, 900, 1380),
        source_no=10,
        question=_q(
            r"""
            오른쪽 그림은 함수 $y=2^x$, $y=\log_2 x$의 그래프와 직선 $y=x$이다. $b^{\frac{1}{a}}$의 값은?
            """
        )
        + _scan("HN-2022-G2-S1-MID-ALG-010 graph"),
        choices=(r"$1$", r"$\dfrac{3}{2}$", r"$2$", r"$\dfrac{5}{2}$", r"$3$"),
        answer="③",
        solution=_q(
            r"""
            그림에서 점 $(a,3)$가 함수 $y=2^x$ 위에 있으므로
            \[
            2^a=3
            \]
            이다.

            또 점 $(b,a)$가 함수 $y=\log_2 x$ 위에 있으므로
            \[
            a=\log_2 b
            \]
            이고, 따라서
            \[
            b=2^a=3
            \]
            이다.

            그러므로
            \[
            b^{1/a}=3^{1/\log_2 3}=3^{\log_3 2}=2
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
        scan_file="HN.2022.G2.S1.MID.ALG.010.png",
    ),
    obj(
        page_no=2,
        crop_box=(40, 1380, 900, 1920),
        source_no=11,
        question=_q(
            r"""
            $\log_{\frac{1}{3}}(x-1)^2\le \log_{\frac{1}{3}}(2x+1)$을 만족하는 $10$이하의 정수해의 개수는?
            """
        ),
        choices=(r"$5$", r"$6$", r"$7$", r"$8$", r"$9$"),
        answer="④",
        solution=_q(
            r"""
            로그의 진수 조건에서
            \[
            (x-1)^2>0,\qquad 2x+1>0
            \]
            이므로 $x\ne 1$, $x>-\dfrac12$이다.

            밑이 $\dfrac13$이므로 부등호 방향이 바뀌어
            \[
            (x-1)^2\ge 2x+1
            \]
            이다.

            정리하면
            \[
            x^2-4x\ge 0
            \]
            이므로
            \[
            x\le 0 \quad \text{또는} \quad x\ge 4
            \]
            이다.

            따라서 $10$ 이하의 정수해는
            \[
            0,4,5,6,7,8,9,10
            \]
            이므로 개수는 $8$개이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
    ),
    obj(
        page_no=2,
        crop_box=(930, 90, 1790, 500),
        source_no=12,
        question=_q(
            r"""
            함수 $y=2\cos 2x$의 주기를 $a$, 함수 $y=\tan 2x$의 주기를 $b$라고 할 때, $\dfrac{a}{b}$의 값은?
            """
        ),
        choices=(r"$\dfrac{1}{2}$", r"$1$", r"$\dfrac{3}{2}$", r"$2$", r"$\dfrac{5}{2}$"),
        answer="④",
        solution=_q(
            r"""
            $y=2\cos 2x$의 주기는
            \[
            a=\frac{2\pi}{2}=\pi
            \]
            이고, $y=\tan 2x$의 주기는
            \[
            b=\frac{\pi}{2}
            \]
            이다.

            따라서
            \[
            \frac{a}{b}=2
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-2. 삼각함수의 그래프",
    ),
    obj(
        page_no=2,
        crop_box=(930, 700, 1790, 1160),
        source_no=13,
        question=_q(
            r"""
            $0\le x<2\pi$일 때, 방정식 $\sin x=\dfrac{1}{3}$의 모든 근의 합은?
            """
        ),
        choices=(r"$\dfrac{\pi}{6}$", r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{3}$", r"$\dfrac{\pi}{2}$", r"$\pi$"),
        answer="⑤",
        solution=_q(
            r"""
            $\sin x=\dfrac13$을 만족하는 두 근을 $\alpha$, $\pi-\alpha$라 하면
            \[
            \alpha+(\pi-\alpha)=\pi
            \]
            이다.

            따라서 모든 근의 합은
            \[
            \pi
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
    ),
    obj(
        page_no=2,
        crop_box=(930, 1320, 1790, 1840),
        source_no=14,
        question=_q(
            r"""
            함수 $f(x)=a^x-a^{-x}\ (a>0,\ a\ne 1)$과 실수 $k$에 대하여 $f(k)=2$일 때, $f(2k)f(3k)$의 값은?
            """
        ),
        choices=(r"$56\sqrt{2}$", r"$28\sqrt{2}$", r"$14\sqrt{2}$", r"$14$", r"$7$"),
        answer="①",
        solution=_q(
            r"""
            $u=a^k$라고 하면
            \[
            u-\frac{1}{u}=2
            \]
            이다.

            따라서
            \[
            \left(u+\frac{1}{u}\right)^2
            =\left(u-\frac{1}{u}\right)^2+4
            =8
            \]
            이므로
            \[
            u+\frac{1}{u}=2\sqrt{2}
            \]
            이다.

            그러므로
            \[
            f(2k)=\left(u-\frac{1}{u}\right)\left(u+\frac{1}{u}\right)=4\sqrt{2}
            \]
            이고,
            \[
            u^2+\frac{1}{u^2}
            =\left(u+\frac{1}{u}\right)^2-2
            =6
            \]
            이므로
            \[
            f(3k)=\left(u-\frac{1}{u}\right)\left(u^2+1+\frac{1}{u^2}\right)=2(6+1)=14
            \]
            이다.

            따라서
            \[
            f(2k)f(3k)=56\sqrt{2}
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    obj(
        page_no=3,
        crop_box=(40, 80, 900, 620),
        source_no=15,
        question=_q(
            r"""
            세계 석유 소비량이 매년 $4\%$씩 감소된다고 할 때, 세계 석유 소비량이 처음으로 현재 소비량의 $\dfrac{1}{4}$ 이하가 되는 것은 몇 년 후인가? (단, $\log 2=0.3$, $\log 9.6=0.98$로 계산한다.)
            """
        ),
        choices=("20년", "30년", "40년", "50년", "60년"),
        answer="②",
        solution=_q(
            r"""
            \[
            0.96^n\le \frac14
            \]
            이므로
            \[
            n\log 0.96\le \log\frac14=-2\log 2=-0.6
            \]
            이다.

            또
            \[
            \log 0.96=\log 9.6-1=0.98-1=-0.02
            \]
            이므로
            \[
            -0.02n\le -0.6
            \]
            이다.

            따라서
            \[
            n\ge 30
            \]
            이므로 처음으로 조건을 만족하는 것은 $30$년 후이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=3,
        crop_box=(40, 620, 920, 1600),
        source_no=16,
        question=_q(
            r"""
            두 함수 $y=\log_2 x$, $y=3^x$의 그래프와 $y=-x+2$가 만나는 점을 각각 $P(x_1,y_1)$, $Q(x_2,y_2)$라 할 때, 옳은 것만을 보기에서 있는 대로 고른 것은?
            """
        )
        + _scan("HN-2022-G2-S1-MID-ALG-016 graph")
        + "\n\n"
        + _box(
            [
                "&lt;보기&gt;",
                "ㄱ. $x_2y_1<x_1y_2$",
                "ㄴ. $x_1^2+y_1^2<x_2^2+y_2^2$",
                "ㄷ. $x_1x_2<y_1y_2$",
            ]
        ),
        choices=("ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"),
        answer="⑤",
        solution=_q(
            r"""
            그래프에서 $P$에 대하여 $1<x_1<\dfrac32$, $0<y_1<1$이고, $Q$에 대하여 $0<x_2<\dfrac12$, $\dfrac32<y_2<2$이다.

            따라서
            \[
            x_2y_1<\frac12<x_1y_2
            \]
            이므로 ㄱ은 참이다.

            또 두 점 모두 직선 $y=-x+2$ 위에 있으므로
            \[
            x+y=2
            \]
            이고,
            \[
            x^2+y^2=2(x-1)^2+2
            \]
            이다.

            그런데
            \[
            (x_1-1)^2<\frac14<(x_2-1)^2
            \]
            이므로 ㄴ은 참이다.

            마지막으로
            \[
            x_1x_2<\frac32\cdot\frac12=\frac34
            \]
            이고
            \[
            y_1y_2>\frac12\cdot\frac32=\frac34
            \]
            이므로 ㄷ도 참이다.

            따라서 ㄱ, ㄴ, ㄷ이 모두 옳다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
        scan_file="HN.2022.G2.S1.MID.ALG.016.png",
    ),
    obj(
        page_no=3,
        crop_box=(930, 80, 1790, 1220),
        source_no=17,
        question=_q(
            r"""
            그림과 같이 선분 $AB$를 지름으로 하는 원 $O$ 위의 두 점 $C$, $D$에 대하여 $\overline{AB}=6$, $\overline{BC}=4$이다. $\angle ABC=\alpha$, $\angle BDC=\beta$라 할 때, $\cos(2\alpha+\beta)\tan(\alpha+2\beta)$의 값은?
            """
        )
        + _scan("HN-2022-G2-S1-MID-ALG-017 geometry"),
        choices=(r"$-\dfrac{4\sqrt{5}}{15}$", r"$-\dfrac{2}{3}$", r"$\dfrac{2}{3}$", r"$\dfrac{5}{6}$", r"$\dfrac{4\sqrt{5}}{15}$"),
        answer="④",
        solution=_q(
            r"""
            $AB$가 지름이므로 $\triangle ABC$는 $C$에서 직각이다.
            따라서
            \[
            AC=\sqrt{AB^2-BC^2}=\sqrt{36-16}=2\sqrt{5}
            \]
            이다.

            그러므로
            \[
            \cos\alpha=\frac{BC}{AB}=\frac{2}{3},\qquad
            \sin\alpha=\frac{AC}{AB}=\frac{\sqrt{5}}{3}
            \]
            이다.

            또 $\angle BAC$와 $\angle BDC$는 같은 호 $BC$를 보고 있으므로
            \[
            \beta=\frac{\pi}{2}-\alpha
            \]
            이다.

            따라서
            \[
            \cos(2\alpha+\beta)=\cos\left(\alpha+\frac{\pi}{2}\right)=-\sin\alpha=-\frac{\sqrt{5}}{3}
            \]
            이고
            \[
            \tan(\alpha+2\beta)=\tan(\pi-\alpha)=-\tan\alpha=-\frac{\sqrt{5}}{2}
            \]
            이다.

            그러므로
            \[
            \cos(2\alpha+\beta)\tan(\alpha+2\beta)=\frac{5}{6}
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
        scan_file="HN.2022.G2.S1.MID.ALG.017.png",
    ),
    sub(
        page_no=3,
        crop_box=(930, 1220, 1790, 1780),
        source_no=1,
        question=_q(
            r"""
            $\dfrac{\pi}{2}$를 육십분법으로 나타내시오.
            """
        ),
        answer=r"$90^\circ$",
        solution=_q(
            r"""
            \[
            \pi\ \text{rad}=180^\circ
            \]
            이므로
            \[
            \frac{\pi}{2}\ \text{rad}=90^\circ
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-1. 삼각함수",
    ),
    sub(
        page_no=4,
        crop_box=(40, 70, 890, 600),
        source_no=2,
        question=_q(
            r"""
            함수 $y=\left(\dfrac{1}{3}\right)^{-x+1}+k$의 그래프가 제2사분면을 지나지 않도록 하는 상수 $k$의 최댓값을 구하시오.
            """
        ),
        answer=r"$-\dfrac{1}{3}$",
        solution=_q(
            r"""
            \[
            y=\left(\frac13\right)^{-x+1}+k=3^{x-1}+k
            \]
            이다.

            제2사분면에서는 $x<0$이고, 이때
            \[
            0<3^{x-1}<\frac13
            \]
            이다.

            그래프가 제2사분면을 지나지 않으려면 $x<0$인 모든 $x$에 대하여
            \[
            3^{x-1}+k\le 0
            \]
            이어야 하므로
            \[
            \frac13+k\le 0
            \]
            이다.

            따라서 $k$의 최댓값은
            \[
            -\frac13
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    sub(
        page_no=4,
        crop_box=(40, 1440, 890, 1940),
        source_no=3,
        question=_q(
            r"""
            $\sin\theta\cos\theta<0$, $\cos\theta\tan\theta>0$을 만족시키는 각 $\theta$는 제 몇사분면의 각인지 구하시오.
            """
        ),
        answer="제2사분면",
        solution=_q(
            r"""
            \[
            \sin\theta\cos\theta<0
            \]
            이므로 $\sin\theta$와 $\cos\theta$의 부호가 반대이다.
            따라서 $\theta$는 제2사분면 또는 제4사분면의 각이다.

            또
            \[
            \cos\theta\tan\theta
            =\cos\theta\cdot\frac{\sin\theta}{\cos\theta}
            =\sin\theta>0
            \]
            이므로 $\theta$는 제2사분면의 각이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-1. 삼각함수",
    ),
    sub(
        page_no=4,
        crop_box=(930, 70, 1790, 890),
        source_no=4,
        question=_q(
            r"""
            지수가 정수일 때도 아래 주어진 지수법칙이 성립하는지 증명하는 과정을 서술하시오. (단, $a\ne 0$, $b\ne 0$이고 $m$, $n$이 음의 정수이다.)

            \[
            a^m\div a^n=a^{m-n},\qquad (ab)^n=a^n b^n
            \]
            """
        )
        + "\n\n"
        + _box(
            [
                "&lt;부분점수 기준&gt;",
                r"$a^m\div a^n=a^{m-n}$의 식을 증명했을 때 [3점]",
                r"$(ab)^n=a^n b^n$의 식을 증명했을 때 [3점]",
            ]
        ),
        answer="성립한다.",
        solution=_q(
            r"""
            $m=-p$, $n=-q$라 하자. 여기서 $p$, $q$는 자연수이다.

            먼저
            \[
            a^m\div a^n
            =a^{-p}\div a^{-q}
            =\frac{1}{a^p}\div \frac{1}{a^q}
            =\frac{1}{a^p}\cdot a^q
            =a^{q-p}
            =a^{-p-(-q)}
            =a^{m-n}
            \]
            이다.

            또
            \[
            (ab)^n=(ab)^{-q}=\frac{1}{(ab)^q}
            =\frac{1}{a^q b^q}
            =a^{-q}b^{-q}
            =a^n b^n
            \]
            이다.

            따라서 음의 정수 지수에서도 주어진 지수법칙은 성립한다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    sub(
        page_no=5,
        crop_box=(40, 60, 890, 920),
        source_no=5,
        question=_q(
            r"""
            그림과 같이 함수 $y=2^x$의 그래프 위의 점 $A(1,2)$에서 $x$축, $y$축에 내린 수선의 발을 각각 $B$, $C$라 하자. 점 $C$를 $y$축의 방향으로 $k$만큼 평행이동시킨 점을 $D$, 점 $D$를 지나고 $x$축과 평행한 직선이 함수 $y=2^x$의 그래프와 만나는 점을 $E$, 점 $E$에서 $x$축에 내린 수선의 발을 $F$라 하자. 사각형 $ACDE$, $ABFE$의 넓이의 합이 $22$일 때, 자연수 $k$의 값을 구하는 과정을 서술하시오.
            """
        )
        + "\n\n"
        + _box(
            [
                "&lt;부분점수 기준&gt;",
                "점 $D$, $E$, $F$의 좌표를 구했을 때 [각 1점]",
                "사각형 $ACDE$, $ABFE$의 넓이를 표현했을 때 [3점]",
                "$k$의 값을 구했을 때 [1점]",
            ]
        ),
        answer="6",
        solution=_q(
            r"""
            \[
            B(1,0),\quad C(0,2),\quad D(0,2+k)
            \]
            이다.

            점 $E$는 $y=2^x$ 위에 있고 $y$좌표가 $2+k$이므로
            \[
            E\bigl(\log_2(2+k),\,2+k\bigr)
            \]
            이고,
            \[
            F\bigl(\log_2(2+k),\,0\bigr)
            \]
            이다.

            사각형 $ACDE$의 넓이는
            \[
            \frac{k\{1+\log_2(2+k)\}}{2}
            \]
            이고,
            사각형 $ABFE$의 넓이는
            \[
            \frac{(4+k)\{\log_2(2+k)-1\}}{2}
            \]
            이다.

            두 넓이의 합이 $22$이므로 자연수 $k$를 대입해 보면 $k=6$일 때
            \[
            \log_2(2+k)=\log_2 8=3
            \]
            이고,
            \[
            \frac{6(1+3)}{2}+\frac{10(3-1)}{2}=12+10=22
            \]
            가 된다.

            따라서
            \[
            k=6
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    sub(
        page_no=5,
        crop_box=(930, 60, 1790, 920),
        source_no=6,
        question=_q(
            r"""
            그림과 같이 넓이가 $65\pi$인 부채꼴 $OAB$를 이용하여 꼭짓점이 $O$이고 호 $AB$가 밑면의 둘레인 원뿔을 만들었다. 원뿔의 밑면의 반지름의 길이를 $r$, 높이를 $h$라 할 때, $r:h=5:12$이다. 부채꼴의 둘레의 길이를 $a+b\pi$라 할 때 $ab$를 구하는 과정을 서술하시오. (단, $a$, $b$는 자연수이다.)
            """
        )
        + "\n\n"
        + _box(
            [
                "&lt;부분점수 기준&gt;",
                "부채꼴의 중심각을 구했을 때 [3점]",
                "부채꼴의 반지름을 구했을 때 [3점]",
                "$ab$의 값을 구했을 때 [1점]",
            ]
        ),
        answer="260",
        solution=_q(
            r"""
            $r:h=5:12$이므로 원뿔의 모선의 길이는 $13$의 비를 가진다.

            $r=5t$, $h=12t$라 하면 부채꼴의 반지름은 모선의 길이이므로
            \[
            13t
            \]
            이다.

            또 호의 길이는 원뿔의 밑면의 둘레이므로
            \[
            2\pi r=10\pi t
            \]
            이다.

            부채꼴의 넓이가 $65\pi$이므로
            \[
            \frac12\cdot 13t\cdot 10\pi t=65\pi
            \]
            이다.
            따라서
            \[
            65t^2=65,\qquad t=1
            \]
            이다.

            그러므로 부채꼴의 반지름은 $13$, 호의 길이는 $10\pi$이다.
            중심각의 크기를 $\theta$라 하면
            \[
            13\theta=10\pi
            \]
            이므로
            \[
            \theta=\frac{10\pi}{13}
            \]
            이다.

            부채꼴의 둘레의 길이는
            \[
            13+13+10\pi=26+10\pi
            \]
            이므로
            \[
            a=26,\quad b=10
            \]
            이다.

            따라서
            \[
            ab=260
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-1. 삼각함수",
    ),
]
JJ_ROWS: List[ProblemRow] = [
    obj(
        page_no=1,
        crop_box=(40, 80, 880, 960),
        source_no=1,
        question=_q(
            r"""
            다음 중 옳은 것은?
            """
        ),
        choices=(
            r"$-64$의 세제곱근 중에서 실수인 것은 $2$개이다.",
            r"$5$의 네제곱근 중에서 실수인 것은 $\sqrt[4]{5}$뿐이다.",
            r"$0$의 세제곱근은 없다.",
            r"$n$이 짝수일 때, $-1$의 $n$제곱근 중에서 실수인 것은 없다.",
            r"$n$이 홀수일 때, $2$의 $n$제곱근 중에서 실수인 것은 $2$개이다.",
        ),
        answer="④",
        solution=_q(
            r"""
            $-64$의 세제곱근 중 실수는 $-4$ 한 개뿐이므로 ①은 거짓이다.
            $5$의 네제곱근 중 실수는 $\pm\sqrt[4]{5}$ 두 개이므로 ②는 거짓이다.
            $0$의 세제곱근은 $0$이므로 ③은 거짓이다.
            짝수 차수의 근에서 $-1$을 만족하는 실수는 없으므로 ④는 참이다.
            홀수 차수의 근에서 $2$를 만족하는 실수는 한 개뿐이므로 ⑤는 거짓이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(40, 1050, 880, 1520),
        source_no=2,
        question=_q(
            r"""
            $2^{a+1}=6$, $3^{5b}=7$일 때, $7^{\frac{1}{ab}}$의 값은?
            """
        ),
        choices=(r"$32$", r"$28$", r"$25$", r"$22$", r"$20$"),
        answer="①",
        solution=_q(
            r"""
            $2^{a+1}=6$에서
            \[
            2^a=3
            \]
            이므로
            \[
            a=\log_2 3
            \]
            이다.

            또 $3^{5b}=7$에서
            \[
            b=\frac{1}{5}\log_3 7
            \]
            이다.

            따라서
            \[
            ab=\log_2 3\cdot \frac{1}{5}\log_3 7=\frac{1}{5}\log_2 7
            \]
            이므로
            \[
            \frac{1}{ab}=5\log_7 2
            \]
            이다.

            그러므로
            \[
            7^{1/(ab)}=7^{5\log_7 2}=2^5=32
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(40, 1530, 880, 2070),
        source_no=3,
        question=_q(
            r"""
            $\log\left(1+\dfrac{1}{1}\right)+\log\left(1+\dfrac{1}{2}\right)+\log\left(1+\dfrac{1}{3}\right)+\cdots+\log\left(1+\dfrac{1}{99}\right)$의 값은?
            """
        ),
        choices=(r"$2$", r"$3$", r"$4$", r"$5$", r"$6$"),
        answer="①",
        solution=_q(
            r"""
            \[
            \sum_{k=1}^{99}\log\left(1+\frac{1}{k}\right)
            =\log\prod_{k=1}^{99}\frac{k+1}{k}
            \]
            이다.

            곱은
            \[
            \frac{2}{1}\cdot\frac{3}{2}\cdot\frac{4}{3}\cdots\frac{100}{99}=100
            \]
            이므로
            \[
            \log 100=2
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 80, 1790, 970),
        source_no=4,
        question=_q(
            r"""
            자연수 $n$에 대하여 $\log a=\log b+\dfrac{64}{2^n}$를 만족시키는 $100$이하의 두 자연수 $a$, $b$의 순서쌍 $(a,b)$의 개수를 $f(n)$이라 할 때, $f(4)+f(5)+f(6)$의 값은?
            """
        ),
        choices=(r"$9$", r"$10$", r"$11$", r"$12$", r"$13$"),
        answer="③",
        solution=_q(
            r"""
            \[
            \log\frac{a}{b}=2^{6-n}
            \]
            이므로
            \[
            \frac{a}{b}=10^{2^{6-n}}
            \]
            이다.

            $n=4$이면 $\dfrac{a}{b}=10^4$이므로 가능한 순서쌍이 없다.
            따라서 $f(4)=0$이다.

            $n=5$이면 $\dfrac{a}{b}=100$이므로 $(a,b)=(100,1)$ 하나뿐이어서 $f(5)=1$이다.

            $n=6$이면 $\dfrac{a}{b}=10$이므로
            \[
            (a,b)=(10,1),(20,2),\ldots,(100,10)
            \]
            의 $10$개가 가능하다.

            따라서
            \[
            f(4)+f(5)+f(6)=0+1+10=11
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 920, 1790, 1440),
        source_no=5,
        question=_q(
            r"""
            부등식 $2^{-x+1}\ge \left(\dfrac{1}{2}\right)^x+\dfrac{1}{64}$을 만족시키는 자연수 $x$의 최댓값과 최솟값의 합은?
            """
        ),
        choices=(r"$6$", r"$7$", r"$8$", r"$9$", r"$10$"),
        answer="②",
        solution=_q(
            r"""
            $t=\left(\dfrac{1}{2}\right)^x$라 하면
            \[
            2^{-x+1}=2t
            \]
            이다.

            따라서 주어진 부등식은
            \[
            2t\ge t+\frac{1}{64}
            \]
            이므로
            \[
            t\ge \frac{1}{64}
            \]
            이다.

            즉
            \[
            \left(\frac{1}{2}\right)^x\ge \left(\frac{1}{2}\right)^6
            \]
            이므로
            \[
            x\le 6
            \]
            이다.

            자연수 $x$는 $1,2,3,4,5,6$이므로 최솟값과 최댓값의 합은
            \[
            1+6=7
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=1,
        crop_box=(930, 1500, 1790, 2040),
        source_no=6,
        question=_q(
            r"""
            함수 $f(x)=4^x-2^{x+3}+a$가 $x=b$에서 최솟값 $1$을 가질 때, 상수 $a-b$의 값은?
            """
        ),
        choices=(r"$23$", r"$21$", r"$19$", r"$17$", r"$15$"),
        answer="⑤",
        solution=_q(
            r"""
            $t=2^x\ (t>0)$라 하면
            \[
            f(x)=t^2-8t+a=(t-4)^2+a-16
            \]
            이다.

            최솟값이 $1$이므로
            \[
            a-16=1,\qquad a=17
            \]
            이다.

            또 최솟값은 $t=4$일 때이므로
            \[
            2^x=4,\qquad x=2
            \]
            이다.

            따라서
            \[
            a-b=17-2=15
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    obj(
        page_no=2,
        crop_box=(40, 90, 900, 1170),
        source_no=7,
        question=_q(
            r"""
            다음 그림과 같이 두 점 $(3,a)$, $(5,b)$는 함수 $y=\log_3 x$의 그래프 위의 점이다. 함수 $y=\log_3 x$의 그래프가 점 $\left(k,\dfrac{a+b}{2}\right)$를 지날 때, $k$의 값을 구하면?
            """
        )
        + _scan("JJ-2022-G2-S1-MID-ALG-007 graph"),
        choices=(r"$\sqrt{14}$", r"$\sqrt{15}$", r"$4$", r"$\sqrt{17}$", r"$3\sqrt{2}$"),
        answer="②",
        solution=_q(
            r"""
            $(3,a)$, $(5,b)$가 $y=\log_3 x$ 위의 점이므로
            \[
            a=\log_3 3=1,\qquad b=\log_3 5
            \]
            이다.

            또
            \[
            \log_3 k=\frac{a+b}{2}
            =\frac{1+\log_3 5}{2}
            =\frac{\log_3 15}{2}
            =\log_3 \sqrt{15}
            \]
            이므로
            \[
            k=\sqrt{15}
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
        scan_file="JJ.2022.G2.S1.MID.ALG.007.png",
    ),
    obj(
        page_no=2,
        crop_box=(40, 1200, 900, 1660),
        source_no=8,
        question=_q(
            r"""
            세계 석유 소비량이 매년 $4\%$씩 감소된다고 할 때, 세계 석유 소비량이 처음으로 현재 소비량의 $\dfrac{1}{2}$ 이하가 되는 것은 몇 년 후인가? (단, $\log 2=0.3$, $\log 3=0.48$로 계산한다.)
            """
        ),
        choices=("13년", "14년", "15년", "16년", "17년"),
        answer="③",
        solution=_q(
            r"""
            \[
            0.96^n\le \frac12
            \]
            이므로
            \[
            n\log 0.96\le -\log 2=-0.3
            \]
            이다.

            또
            \[
            \log 0.96=\log 3+5\log 2-2=0.48+1.5-2=-0.02
            \]
            이므로
            \[
            -0.02n\le -0.3
            \]
            이다.

            따라서
            \[
            n\ge 15
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    obj(
        page_no=2,
        crop_box=(40, 1640, 900, 2070),
        source_no=9,
        question=_q(
            r"""
            중심각의 크기가 $1$라디안이고 둘레의 길이가 $30$인 부채꼴의 넓이는?
            """
        ),
        choices=(r"$32$", r"$38$", r"$42$", r"$50$", r"$58$"),
        answer="④",
        solution=_q(
            r"""
            반지름을 $r$라 하면 부채꼴의 둘레의 길이는
            \[
            2r+r=3r
            \]
            이므로
            \[
            r=10
            \]
            이다.

            따라서 넓이는
            \[
            \frac12 r^2\theta=\frac12\cdot 10^2\cdot 1=50
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-1. 삼각함수",
    ),
    obj(
        page_no=2,
        crop_box=(930, 90, 1790, 650),
        source_no=10,
        question=_q(
            r"""
            함수 $y=\sin \pi x$의 그래프와 직선 $y=\dfrac{4}{21}x$의 교점의 개수는?
            """
        ),
        choices=(r"$7$", r"$8$", r"$9$", r"$10$", r"$11$"),
        answer="⑤",
        solution=_q(
            r"""
            함수
            \[
            f(x)=\sin\pi x-\frac{4}{21}x
            \]
            는 홀함수이므로 원점 대칭이다.

            $x>0$에서 $\sin\pi x$가 양수인 구간은 $(0,1)$, $(2,3)$, $(4,5)$이다.
            $(0,1)$에서는 원점을 제외한 교점이 한 개 있고, $(2,3)$과 $(4,5)$에서는 양 끝점에서 음수, 가운데에서 양수이므로 각각 두 개의 교점이 있다.

            따라서 양의 교점은 $5$개이고, 음의 교점도 $5$개이며 원점도 교점이다.
            그러므로 전체 교점의 개수는
            \[
            11
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-2. 삼각함수의 그래프",
    ),
    obj(
        page_no=2,
        crop_box=(930, 720, 1790, 1400),
        source_no=11,
        question=_q(
            r"""
            $0\le x<\dfrac{5}{2}\pi$일 때, 방정식 $3\sin x=2$를 만족시키는 $x$의 값을 작은 것부터 차례대로 $\alpha$, $\beta$, $\gamma$라고 하자. 이때 $\cos\left(\alpha+\dfrac{\beta+\gamma}{2}\right)$의 값은?
            """
        ),
        choices=(r"$\dfrac{2}{3}$", r"$\dfrac{1}{2}$", r"$\dfrac{2}{5}$", r"$\dfrac{1}{3}$", r"$\dfrac{3}{5}$"),
        answer="①",
        solution=_q(
            r"""
            \[
            \sin x=\frac{2}{3}
            \]
            이므로
            \[
            \beta=\pi-\alpha,\qquad \gamma=2\pi+\alpha
            \]
            이다.

            따라서
            \[
            \beta+\gamma=3\pi
            \]
            이고,
            \[
            \alpha+\frac{\beta+\gamma}{2}=\alpha+\frac{3\pi}{2}
            \]
            이다.

            그러므로
            \[
            \cos\left(\alpha+\frac{\beta+\gamma}{2}\right)=\cos\left(\alpha+\frac{3\pi}{2}\right)=\sin\alpha=\frac{2}{3}
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
    ),
    obj(
        page_no=2,
        crop_box=(930, 1510, 1790, 2050),
        source_no=12,
        question=_q(
            r"""
            함수 $f(x)=a\cos\dfrac{x}{3}+b$의 최댓값은 $4$이고 $f(2\pi)=-5$일 때, 상수 $a$, $b$에 대하여 $a-b$의 값은? (단, $a>0$)
            """
        ),
        choices=(r"$4$", r"$6$", r"$8$", r"$10$", r"$12$"),
        answer="③",
        solution=_q(
            r"""
            최댓값이 $4$이므로
            \[
            a+b=4
            \]
            이다.

            또
            \[
            f(2\pi)=a\cos\frac{2\pi}{3}+b=-\frac{a}{2}+b=-5
            \]
            이다.

            두 식을 연립하면
            \[
            a=6,\qquad b=-2
            \]
            이므로
            \[
            a-b=8
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-1. 삼각함수",
    ),
    obj(
        page_no=3,
        crop_box=(40, 60, 900, 1100),
        source_no=13,
        question=_q(
            r"""
            다음 그림과 같이 함수 $y=\sin\dfrac{\pi}{8}x$의 그래프와 $x$축으로 둘러싸인 부분에 직사각형 $ABCD$가 내접하고 있다. $\overline{BC}=4$일 때, 직사각형 $ABCD$의 넓이는?
            """
        )
        + _scan("JJ-2022-G2-S1-MID-ALG-013 graph"),
        choices=(r"$2$", r"$2\sqrt{2}$", r"$3$", r"$4\sqrt{2}$", r"$5\sqrt{2}$"),
        answer="②",
        solution=_q(
            r"""
            직사각형의 왼쪽 아래 꼭짓점의 $x$좌표를 $t$라 하면 오른쪽 아래 꼭짓점의 $x$좌표는 $t+4$이다.

            윗변의 양 끝점이 그래프 위에 있으므로
            \[
            \sin\frac{\pi t}{8}=\sin\frac{\pi(t+4)}{8}
            \]
            이다.

            $0\le t\le 4$에서 두 각은 서로 보각이므로
            \[
            \frac{\pi(t+4)}{8}=\pi-\frac{\pi t}{8}
            \]
            이고,
            \[
            t=2
            \]
            이다.

            따라서 직사각형의 높이는
            \[
            \sin\frac{\pi}{4}=\frac{\sqrt{2}}{2}
            \]
            이므로 넓이는
            \[
            4\cdot \frac{\sqrt{2}}{2}=2\sqrt{2}
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-2. 삼각함수의 그래프",
        scan_file="JJ.2022.G2.S1.MID.ALG.013.png",
    ),
    obj(
        page_no=3,
        crop_box=(40, 1160, 900, 1730),
        source_no=14,
        question=_q(
            r"""
            $0\le \alpha\le 2\pi$이고 $0\le \beta\le 2\pi$일 때, $\sin^2(\pi\cos\alpha)+\cos^2(\pi\sin\beta)=0$을 만족시키는 두 실수 $\alpha$, $\beta$의 순서쌍 $(\alpha,\beta)$의 개수는?
            """
        ),
        choices=(r"$12$", r"$14$", r"$16$", r"$18$", r"$20$"),
        answer="⑤",
        solution=_q(
            r"""
            두 제곱식의 합이 $0$이려면 각각이 모두 $0$이어야 한다.

            먼저
            \[
            \sin(\pi\cos\alpha)=0
            \]
            이고 $\cos\alpha\in[-1,1]$이므로
            \[
            \cos\alpha=-1,0,1
            \]
            이다.
            따라서 $\alpha$의 개수는 $5$개이다.

            또
            \[
            \cos(\pi\sin\beta)=0
            \]
            이고 $\sin\beta\in[-1,1]$이므로
            \[
            \sin\beta=\frac12 \quad \text{또는} \quad -\frac12
            \]
            이다.
            따라서 $\beta$의 개수는 $4$개이다.

            그러므로 순서쌍의 개수는
            \[
            5\times 4=20
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
    ),
    obj(
        page_no=3,
        crop_box=(930, 60, 1790, 840),
        source_no=15,
        question=_q(
            r"""
            모든 실수 $x$에 대하여 부등식 $\cos^2 x+3\sin x-a<0$이 항상 성립하도록 하는 실수 $a$의 값의 범위를 구하면?
            """
        ),
        choices=(r"$a\ge 4$", r"$a\ge 3$", r"$a>2$", r"$a>3$", r"$a>4$"),
        answer="④",
        solution=_q(
            r"""
            $t=\sin x$라 하면 $-1\le t\le 1$이고
            \[
            \cos^2 x=1-t^2
            \]
            이다.

            따라서
            \[
            \cos^2 x+3\sin x-a=-t^2+3t+1-a
            \]
            이다.

            함수 $-t^2+3t+1$은 구간 $[-1,1]$에서 증가하므로 최댓값은 $t=1$일 때의 값
            \[
            3
            \]
            이다.

            따라서 모든 실수 $x$에 대하여 부등식이 성립하려면
            \[
            a>3
            \]
            이어야 한다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
    ),
    sub(
        page_no=3,
        crop_box=(930, 980, 1790, 1460),
        source_no=1,
        question=_q(
            r"""
            세 양수 $x$, $y$, $z$에 대하여 $2^x=3^y=n^z$, $xy=yz+zx$일 때, 양수 $n$의 값을 구하시오.
            """
        ),
        answer="6",
        solution=_q(
            r"""
            $2^x=3^y=n^z=M$이라 하자.
            그러면
            \[
            x=z\log_2 n,\qquad y=z\log_3 n
            \]
            이다.

            이를 $xy=yz+zx$에 대입하면
            \[
            z^2\log_2 n\log_3 n=z^2(\log_3 n+\log_2 n)
            \]
            이다.

            $z>0$이므로
            \[
            \log_2 n\log_3 n=\log_3 n+\log_2 n
            \]
            이다.

            자연로그로 바꾸면
            \[
            \frac{\ln n}{\ln 2}\cdot\frac{\ln n}{\ln 3}
            =\frac{\ln n}{\ln 2}+\frac{\ln n}{\ln 3}
            \]
            이고, $\ln n>0$이므로
            \[
            \ln n=\ln 2+\ln 3=\ln 6
            \]
            이다.

            따라서
            \[
            n=6
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-1. 지수와 로그",
    ),
    sub(
        page_no=3,
        crop_box=(930, 1460, 1790, 2200),
        source_no=2,
        question=_q(
            r"""
            함수 $f(x)=3^{x+3}-5$에 대하여 곡선 $y=\lvert f(x)\rvert$와 직선 $y=k$가 오직 한 점에서 만나도록 하는 $16$보다 작은 정수 $k$의 개수를 구하시오.
            """
        ),
        answer="12",
        solution=_q(
            r"""
            함수 $f(x)=3^{x+3}-5$는 증가함수이므로 $y=\lvert f(x)\rvert$의 그래프는 왼쪽에서 감소하여 $0$까지 내려갔다가 다시 증가한다.

            왼쪽 가지의 값의 범위는
            \[
            0\le y<5
            \]
            이고, 오른쪽 가지의 값의 범위는
            \[
            y\ge 0
            \]
            이다.

            따라서 수평선 $y=k$가 그래프와 한 점에서만 만나는 경우는
            \[
            k=0,\quad k=5,\quad k>5
            \]
            일 때이다.

            $16$보다 작은 정수 $k$는
            \[
            0,5,6,7,8,9,10,11,12,13,14,15
            \]
            이므로 개수는
            \[
            12
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-2. 지수함수",
    ),
    sub(
        page_no=4,
        crop_box=(40, 80, 890, 650),
        source_no=3,
        question=_q(
            r"""
            $0\le x<2\pi$일 때, 부등식 $2\sin^2 x-\cos x-1<0$의 해를 구하시오.
            """
        ),
        answer=r"$[0,\dfrac{\pi}{3})\cup(\dfrac{5\pi}{3},2\pi)$",
        solution=_q(
            r"""
            $\sin^2 x=1-\cos^2 x$를 이용하면
            \[
            2(1-\cos^2 x)-\cos x-1<0
            \]
            이고,
            \[
            2\cos^2 x+\cos x-1>0
            \]
            이다.

            따라서
            \[
            (2\cos x-1)(\cos x+1)>0
            \]
            이다.

            $\cos x\in[-1,1]$이므로 가능한 것은
            \[
            \cos x>\frac12
            \]
            뿐이다.

            따라서 해는
            \[
            0\le x<\frac{\pi}{3}\quad \text{또는}\quad \frac{5\pi}{3}<x<2\pi
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-3. 삼각함수의 활용",
    ),
    sub(
        page_no=4,
        crop_box=(40, 900, 890, 1620),
        source_no=4,
        question=_q(
            r"""
            모든 실수 $x$에 대하여 $\log_{a-2}(x^2-2ax+8a)$의 값이 존재하도록 하는 모든 정수 $a$의 값의 합을 구하시오.
            """
        ),
        answer="22",
        solution=_q(
            r"""
            로그의 밑은
            \[
            a-2>0,\qquad a-2\ne 1
            \]
            이어야 하므로
            \[
            a>2,\qquad a\ne 3
            \]
            이다.

            또 진수
            \[
            x^2-2ax+8a=(x-a)^2+a(8-a)
            \]
            가 모든 실수 $x$에서 양수여야 한다.

            최솟값은 $x=a$일 때의 값 $a(8-a)$이므로
            \[
            a(8-a)>0
            \]
            이고,
            \[
            0<a<8
            \]
            이다.

            이를 모두 만족하는 정수 $a$는
            \[
            4,5,6,7
            \]
            이므로 합은
            \[
            22
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
    ),
    sub(
        page_no=4,
        crop_box=(930, 70, 1790, 800),
        source_no=5,
        question=_q(
            r"""
            함수 $y=\log_a x+m\ (a>1)$의 그래프와 그 역함수의 그래프가 두 점에서 만나고, 이 두 점의 $x$좌표가 각각 $1$, $3$일 때, $am$을 구하시오. (단, $m$은 상수이다.)
            """
        ),
        answer=r"$\sqrt{3}$",
        solution=_q(
            r"""
            함수와 그 역함수의 교점은 직선 $y=x$ 위에 있으므로 $(1,1)$, $(3,3)$이 함수
            \[
            y=\log_a x+m
            \]
            위에 있다.

            $(1,1)$을 대입하면
            \[
            1=\log_a 1+m=m
            \]
            이므로
            \[
            m=1
            \]
            이다.

            $(3,3)$을 대입하면
            \[
            3=\log_a 3+1
            \]
            이므로
            \[
            \log_a 3=2
            \]
            이다.

            따라서
            \[
            a^2=3,\qquad a=\sqrt{3}
            \]
            이고
            \[
            am=\sqrt{3}
            \]
            이다.
            """
        ),
        unit_l2="1. 지수함수와 로그함수",
        unit_l3="1-3. 로그함수",
    ),
    sub(
        page_no=4,
        crop_box=(930, 1060, 1790, 1820),
        source_no=6,
        question=_q(
            r"""
            $0\le x\le a$에서 함수 $f(x)=\tan x$의 그래프가 직선 $y=f\left(\dfrac{\pi}{5}\right)$ 또는 직선 $y=\dfrac{1}{f\left(\dfrac{\pi}{5}\right)}$과 만나는 점의 개수가 $7$개가 되도록 하는 $a$값의 범위가 $m\le a<M$일 때, $\dfrac{M}{m}$의 값을 구하시오.
            """
        ),
        answer=r"$\dfrac{33}{32}$",
        solution=_q(
            r"""
            \[
            f\left(\frac{\pi}{5}\right)=\tan\frac{\pi}{5}
            \]
            이고
            \[
            \frac{1}{f\left(\frac{\pi}{5}\right)}
            =\cot\frac{\pi}{5}
            =\tan\frac{3\pi}{10}
            \]
            이다.

            따라서 교점의 $x$좌표는
            \[
            x=\frac{\pi}{5}+k\pi,\qquad x=\frac{3\pi}{10}+k\pi
            \quad (k=0,1,2,\ldots)
            \]
            이다.

            이를 작은 것부터 나열하면
            \[
            \frac{\pi}{5},\ \frac{3\pi}{10},\ \frac{6\pi}{5},\ \frac{13\pi}{10},\ \frac{11\pi}{5},\ \frac{23\pi}{10},\ \frac{16\pi}{5},\ \frac{33\pi}{10},\ldots
            \]
            이다.

            교점의 개수가 $7$개가 되려면
            \[
            \frac{16\pi}{5}\le a<\frac{33\pi}{10}
            \]
            이어야 하므로
            \[
            m=\frac{16\pi}{5},\qquad M=\frac{33\pi}{10}
            \]
            이다.

            따라서
            \[
            \frac{M}{m}
            =\frac{33\pi/10}{16\pi/5}
            =\frac{33}{32}
            \]
            이다.
            """
        ),
        unit_l2="2. 삼각함수",
        unit_l3="2-2. 삼각함수의 그래프",
    ),
]


EXAMS: List[ExamSpec] = [
    ExamSpec(
        label="HN-2022-G2-S1-MID-ALG",
        school="HN",
        year=2022,
        grade=2,
        semester=1,
        exam="MID",
        subject="ALG",
        source_pdf="HN.2022.G2.S1.MID.ALG.pdf",
        rows=HN_ROWS,
    ),
    ExamSpec(
        label="JJ-2022-G2-S1-MID-ALG",
        school="JJ",
        year=2022,
        grade=2,
        semester=1,
        exam="MID",
        subject="ALG",
        source_pdf="JJ.2022.G2.S1.MID.ALG.pdf",
        rows=JJ_ROWS,
    ),
]


def _problem_number(row: ProblemRow) -> int:
    if row.kind == "subjective":
        return 100 + row.source_no
    return row.source_no


def _problem_id(spec: ExamSpec, row: ProblemRow) -> str:
    return (
        f"{spec.school}-{spec.year}-G{spec.grade}-S{spec.semester}-"
        f"{spec.exam}-{spec.subject}-{_problem_number(row):03d}"
    )


def _source_label(row: ProblemRow) -> str:
    if row.kind == "subjective":
        return f"서답{row.source_no}번"
    return str(row.source_no)


def _format_choices(choices: Sequence[str]) -> str:
    markers = ("①", "②", "③", "④", "⑤")
    return "\n".join(f"{marker} {choice}" for marker, choice in zip(markers, choices))


def _render_crop(doc: fitz.Document, page_no: int, crop_box: Tuple[int, int, int, int], out_path: Path) -> None:
    page = doc.load_page(page_no - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(PIXEL_SCALE, PIXEL_SCALE), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.crop(crop_box).save(out_path)


def _build_problem_md(
    spec: ExamSpec,
    row: ProblemRow,
    problem_id: str,
    assets: Sequence[str],
    level: int,
) -> str:
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(UNIT_L1, row.unit_l2, row.unit_l3, grade=spec.grade)
    source_label = _source_label(row)
    front = {
        "id": problem_id,
        "school": spec.school,
        "year": spec.year,
        "grade": spec.grade,
        "semester": spec.semester,
        "exam": spec.exam,
        "subject": spec.subject,
        "type": row.kind,
        "source_question_no": row.source_no,
        "source_question_kind": row.kind,
        "source_question_label": source_label,
        "difficulty": level,
        "level": level,
        "unit": f"{unit_l1}>{unit_l2}>{unit_l3}",
        "unit_l1": unit_l1,
        "unit_l2": unit_l2,
        "unit_l3": unit_l3,
        "source": SOURCE,
        "tags": [
            "수동생성",
            "PDF",
            row.kind,
            f"출제번호-{source_label}",
            "과목-대수",
            "생성일-2026-03-07",
        ],
        "assets": list(assets),
    }
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{row.question}\n\n"
        f"## Choices\n{_format_choices(row.choices)}\n\n"
        f"## Answer\n{row.answer}\n\n"
        f"## Solution\n{row.solution}\n"
    )
    return f"---\n{front_text}\n---\n\n{body}"


def _ingest_exam(spec: ExamSpec) -> Dict[str, object]:
    source_pdf = ORIGINAL / spec.source_pdf
    if not source_pdf.is_file():
        raise FileNotFoundError(f"missing source pdf: {source_pdf}")

    summary = {"created": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    duplicates: List[str] = []
    review_paths: List[str] = []

    doc = fitz.open(source_pdf)
    try:
        for row in spec.rows:
            pid = _problem_id(spec, row)
            problem_dir = PROBLEMS / pid
            problem_md = problem_dir / "problem.md"
            if problem_dir.exists():
                summary["skipped"] += 1
                duplicates.append(pid)
                results.append(f"{pid} | skipped | folder exists")
                continue

            assets_dir = problem_dir / "assets"
            original_dir = assets_dir / "original"
            original_dir.mkdir(parents=True, exist_ok=True)

            original_name = f"{pid}_original.png"
            _render_crop(doc, row.page_no, row.crop_box, original_dir / original_name)

            assets = ["assets/original/", f"assets/original/{original_name}"]
            if row.scan_file:
                scan_src = ORIGINAL / row.scan_file
                if scan_src.is_file():
                    shutil.copyfile(scan_src, assets_dir / "scan.png")
                    assets = ["assets/scan.png", *assets]
                else:
                    warnings.append(f"{pid}: missing scan source {row.scan_file}")

            classified = classify_unit_and_level(
                question_text=row.question,
                choices_text=_format_choices(row.choices),
                answer_text=row.answer,
                solution_text=row.solution,
                qtype=row.kind,
                grade=spec.grade,
                problem_no=_problem_number(row),
            )

            md = _build_problem_md(
                spec=spec,
                row=row,
                problem_id=pid,
                assets=assets,
                level=classified.level,
            )
            problem_md.write_text(md, encoding="utf-8")
            review_paths.append(str(problem_md.resolve()))
            summary["created"] += 1

            unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(UNIT_L1, row.unit_l2, row.unit_l3, grade=spec.grade)
            note = f" | note={row.note}" if row.note else ""
            results.append(
                f"{pid} | created | {unit_l1}>{unit_l2}>{unit_l3} | level={classified.level}{note}"
            )
            if row.note:
                warnings.append(f"{pid}: {row.note}")
                uncertain.append(pid)
    finally:
        doc.close()

    summary["warnings"] = len(warnings)
    return {
        "label": spec.label,
        "summary": summary,
        "results": results,
        "warnings": warnings,
        "uncertain": uncertain,
        "duplicates": duplicates,
        "review_paths": review_paths,
    }


def _report_block(report: Dict[str, object]) -> List[str]:
    return [
        f"[{report['label']}]",
        "created={created} skipped={skipped} warnings={warnings}".format(**report["summary"]),
        "",
        "[RESULTS]",
        *(report["results"] or ["(none)"]),
        "",
        "[DUPLICATE_FOLDERS]",
        *(report["duplicates"] or ["(none)"]),
        "",
        "[WARNINGS]",
        *(report["warnings"] or ["(none)"]),
        "",
        "[OCR_OR_FORMULA_UNCERTAIN]",
        *(report["uncertain"] or ["(none)"]),
        "",
        "[REVIEW_PATHS]",
        *(report["review_paths"] or ["(none)"]),
        "",
    ]


def main() -> None:
    reports = [_ingest_exam(spec) for spec in EXAMS]
    lines: List[str] = []
    total_created = sum(int(report["summary"]["created"]) for report in reports)
    total_skipped = sum(int(report["summary"]["skipped"]) for report in reports)
    total_warnings = sum(int(report["summary"]["warnings"]) for report in reports)
    lines.extend(
        [
            "[TOTAL]",
            f"created={total_created} skipped={total_skipped} warnings={total_warnings}",
            "",
        ]
    )
    for report in reports:
        lines.extend(_report_block(report))

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"report: {REPORT}")


if __name__ == "__main__":
    main()
