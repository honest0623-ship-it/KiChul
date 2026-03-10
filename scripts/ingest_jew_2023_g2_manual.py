from __future__ import annotations

import inspect
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from unit_level_classifier import classify_unit_and_level


ROOT = REPO_ROOT
ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

ALG_PDF = ORIGINAL / "JEW.2023.G2.S1.MID1.ALG.pdf"
CAL1_PDF = ORIGINAL / "JEW.2023.G2.S1.MID2.CAL1.pdf"

SOURCE_META = {
    "school": "JEW",
    "year": 2023,
    "grade": 2,
    "semester": 1,
    "source": "user_upload_2026-03-06",
    "subjective_offset": 100,
}


@dataclass(frozen=True)
class ProblemRow:
    exam: str
    subject: str
    subject_label: str
    page_no: int
    crop_box: Tuple[int, int, int, int]
    source_no: int
    kind: str
    qtype: str
    question: str
    choices: Sequence[str]
    answer: str
    solution: str
    scan_builder: Optional[Callable[[Path], None]] = None
    note: str = ""

    @property
    def problem_no(self) -> int:
        if self.kind == "objective":
            return self.source_no
        return self.source_no + int(SOURCE_META["subjective_offset"])

    @property
    def problem_id(self) -> str:
        return (
            f"{SOURCE_META['school']}-{SOURCE_META['year']}-G{SOURCE_META['grade']}"
            f"-S{SOURCE_META['semester']}-{self.exam}-{self.subject}-{self.problem_no:03d}"
        )

    @property
    def source_label(self) -> str:
        if self.kind == "objective":
            return str(self.source_no)
        return f"서답{self.source_no}번"

    @property
    def source_tag(self) -> str:
        if self.kind == "objective":
            return str(self.source_no)
        return f"서답{self.source_no}번"


def _q(text: str) -> str:
    return inspect.cleandoc(text).strip()


def build_q8_scan(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 3.3), dpi=200)
    xs = [2 + 10 ** (t / 40) for t in range(-80, 90)]
    ys = [math.log(x - 2, 3) - 1 for x in xs]

    ax.plot(xs, ys, color="black", linewidth=2)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.axvline(2, color="black", linestyle="--", linewidth=1)
    ax.text(2, 0.18, "2", ha="center", va="bottom", fontsize=10)
    ax.text(5, 0.18, "5", ha="center", va="bottom", fontsize=10)
    ax.text(-0.15, -0.15, "O", ha="right", va="top", fontsize=10)
    ax.text(6.1, -0.08, "x", ha="left", va="center", fontsize=10)
    ax.text(-0.08, 2.3, "y", ha="center", va="bottom", fontsize=10)
    ax.set_xlim(-0.2, 6.0)
    ax.set_ylim(-2.2, 2.4)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)


ALG_ROWS: List[ProblemRow] = []
ALG_ROWS.extend(
    [
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=1,
            crop_box=(80, 520, 980, 1120),
            source_no=1,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                $\log_3 \dfrac{1}{7}+\log_3 63$의 값은?
                """
            ),
            choices=("① 1", "② 2", "③ 3", "④ 4", "⑤ 5"),
            answer="②",
            solution=_q(
                r"""
                로그의 성질을 이용하면
                $$
                \log_3 \dfrac{1}{7}+\log_3 63
                =\log_3 \left(\dfrac{1}{7}\times 63\right)
                =\log_3 9
                =2
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=1,
            crop_box=(80, 1120, 980, 1880),
            source_no=2,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                다음 수열이 주어진 순서대로 등차수열을 이룰 때, $x$의 값은?

                $$
                4,\ x,\ 12
                $$
                """
            ),
            choices=("① 6", "② 7", "③ 8", "④ 9", "⑤ 10"),
            answer="③",
            solution=_q(
                r"""
                등차수열에서는 가운데 항이 양 끝 항의 평균이므로
                $$
                x=\dfrac{4+12}{2}=8
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=1,
            crop_box=(80, 1880, 980, 2740),
            source_no=3,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                자연수 $m,\ n$에 대하여
                $$
                a^3\times a^{-2}\div \sqrt[3]{a^2}=\sqrt[m]{a^n}
                $$
                일 때, $m+n$의 값은? $(a>0)$
                """
            ),
            choices=("① 2", "② 3", "③ 4", "④ 5", "⑤ 6"),
            answer="③",
            solution=_q(
                r"""
                왼쪽 식을 지수법칙으로 정리하면
                $$
                a^3\times a^{-2}\div \sqrt[3]{a^2}
                =a^{3-2-\frac{2}{3}}
                =a^{\frac13}
                $$
                이다.

                또
                $$
                \sqrt[m]{a^n}=a^{\frac{n}{m}}
                $$
                이므로
                $$
                \frac{n}{m}=\frac13
                $$
                이다. 자연수 $m,\ n$은 $m=3,\ n=1$이므로
                $$
                m+n=4
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=1,
            crop_box=(1120, 430, 2080, 1050),
            source_no=4,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                정의역이 $\left\{x\mid -1\le x\le 5\right\}$인 함수
                $$
                f(x)=\log_2 (x+3)-2
                $$
                의 최댓값은?
                """
            ),
            choices=("① $-2$", "② $-1$", "③ $0$", "④ $1$", "⑤ $2$"),
            answer="④",
            solution=_q(
                r"""
                로그함수 $y=\log_2 (x+3)$은 밑이 $2$이므로 증가한다.
                따라서 주어진 구간에서 최댓값은 $x=5$일 때이다.

                $$
                f(5)=\log_2 8-2=3-2=1
                $$

                따라서 최댓값은 $1$이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=1,
            crop_box=(1060, 1200, 2080, 2500),
            source_no=5,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                다음 학생들의 말 중 옳지 않은 것은?

                (단, $a_n$은 일반항, $a$는 첫째항, $n$은 자연수, $d$는 공차, $r$은 공비, $l$은 제 $n$항, $S_n$은 첫째항부터 제 $n$항까지의 합이다.)
                """
            ),
            choices=(
                "① 민서 : 등차수열 $\\{a_n\\}$의 일반항은 $a_n=a+(n-1)d$야.",
                "② 채린 : 등차수열 $\\{a_n\\}$의 첫째항부터 제 $n$항까지의 합은 $S_n=\\dfrac{n(a+l)}{2}$라고 할 수 있어.",
                "③ 하연 : 등비수열 $\\{a_n\\}$의 일반항은 $a_n=ar^{n-1}$이야.",
                "④ 경민 : 등비수열 $\\{a_n\\}$의 첫째항부터 제 $n$항까지의 합은 $S_n=\\dfrac{a(r^n-1)}{r-1}=\\dfrac{a(1-r^n)}{1-r}$이야. $(r\\ne 1)$",
                "⑤ 가현 : $0$이 아닌 세 수 $a,b,c$가 차례로 등비수열을 이룰 때, $b$는 기하평균인 $\\sqrt{ac}$뿐이야.",
            ),
            answer="⑤",
            solution=_q(
                r"""
                ①, ②, ③, ④는 모두 등차수열과 등비수열의 기본 성질이다.

                세 수 $a,b,c$가 차례로 등비수열을 이루면
                $$
                b^2=ac
                $$
                이므로
                $$
                b=\pm \sqrt{ac}
                $$
                이다.

                따라서 $b$가 반드시 $\sqrt{ac}$ 하나로만 정해진다고 한 ⑤가 옳지 않다.
                """
            ),
        ),
    ]
)
ALG_ROWS.extend(
    [
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=2,
            crop_box=(70, 260, 1040, 1050),
            source_no=6,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합 $S_n$이
                $$
                S_n=3^n-1
                $$
                일 때, 이 수열의 일반항 $a_n$은?
                """
            ),
            choices=(r"① $2\cdot 3^{n-1}$", "② $3^{n-1}$", "③ $3^n$", r"④ $2\cdot 3^n$", "⑤ $3^{n+1}$"),
            answer="①",
            solution=_q(
                r"""
                $n\ge 2$일 때
                $$
                a_n=S_n-S_{n-1}
                $$
                이므로
                $$
                a_n=(3^n-1)-(3^{n-1}-1)=3^n-3^{n-1}=2\cdot 3^{n-1}
                $$
                이다.

                첫째항도
                $$
                a_1=S_1=3-1=2
                $$
                이므로 일반항은
                $$
                a_n=2\cdot 3^{n-1}
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=2,
            crop_box=(70, 930, 1040, 1690),
            source_no=7,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                $$
                \sqrt[3]{-8}+\sqrt[4]{(-3)^4}\times \sqrt{\dfrac{\sqrt[3]{128}}{\sqrt[3]{2}}}
                $$
                의 값은?
                """
            ),
            choices=("① $-10$", "② $-8$", "③ $-4$", "④ $-2$", "⑤ $4$"),
            answer="⑤",
            solution=_q(
                r"""
                각 부분을 계산하면
                $$
                \sqrt[3]{-8}=-2,\qquad \sqrt[4]{(-3)^4}=3
                $$
                이고,
                $$
                \sqrt{\dfrac{\sqrt[3]{128}}{\sqrt[3]{2}}}
                =\sqrt{\sqrt[3]{64}}
                =\sqrt{4}=2
                $$
                이다.

                따라서
                $$
                -2+3\times 2=4
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=2,
            crop_box=(70, 1680, 1040, 2820),
            source_no=8,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                함수
                $$
                y=\log_3 (x-a)+b
                $$
                의 그래프가 아래의 그림과 같을 때, $ab$의 값은?
                (단, $a,\ b$는 상수이고 직선 $x=2$는 점근선이다.)

                <img src="assets/scan.png" alt="JEW-2023-G2-S1-MID-ALG-008 graph" style="width:60% !important; max-width:60% !important; height:auto;" />
                """
            ),
            choices=("① $-3$", "② $-2$", "③ $-1$", "④ $1$", "⑤ $2$"),
            answer="②",
            solution=_q(
                r"""
                점근선이 $x=2$이므로
                $$
                x-a=0
                $$
                에서 점근선이 생긴다. 따라서
                $$
                a=2
                $$
                이다.

                또 그래프가 $x$축과 만나는 점의 $x$좌표가 $5$이므로
                $$
                0=\log_3 (5-2)+b=\log_3 3+b=1+b
                $$
                이다. 따라서
                $$
                b=-1
                $$
                이다.

                그러므로
                $$
                ab=2\times (-1)=-2
                $$
                이다.
                """
            ),
            scan_builder=build_q8_scan,
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=2,
            crop_box=(1070, 350, 2080, 1280),
            source_no=9,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                비행기의 엔진 소리의 세기 $I\ \mathrm{W/m^2}$와 소리의 크기 $D\ \mathrm{dB}$ 사이에는
                $$
                D=10\log \dfrac{I}{10^{-12}}
                $$
                가 성립한다. 비행기 $A$의 엔진 소리의 세기가 비행기 $B$의 엔진 소리의 세기의 $10$배일 때, 비행기 $A$와 비행기 $B$의 엔진 소리 크기의 차이는?
                """
            ),
            choices=("① $10$", "② $20$", "③ $30$", "④ $40$", "⑤ $50$"),
            answer="①",
            solution=_q(
                r"""
                비행기 $A,\ B$의 소리 크기를 각각 $D_A,\ D_B$라 하면
                $$
                D_A-D_B
                =10\log \dfrac{I_A}{10^{-12}}-10\log \dfrac{I_B}{10^{-12}}
                =10\log \dfrac{I_A}{I_B}
                $$
                이다.

                $I_A=10I_B$이므로
                $$
                D_A-D_B=10\log 10=10
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=2,
            crop_box=(1070, 1500, 2080, 2500),
            source_no=10,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                첫째항부터 제 $3$항까지의 합이 $3$, 첫째항부터 제 $6$항까지의 합이 $33$인 등차수열의 첫째항부터 제 $9$항까지의 합은?
                """
            ),
            choices=("① $62$", "② $70$", "③ $80$", "④ $90$", "⑤ $100$"),
            answer="④",
            solution=_q(
                r"""
                첫째항을 $a$, 공차를 $d$라 하면
                $$
                S_3=\frac{3}{2}(2a+2d)=3(a+d)=3
                $$
                이므로
                $$
                a+d=1
                $$
                이다.

                또
                $$
                S_6=\frac{6}{2}(2a+5d)=3(2a+5d)=33
                $$
                이므로
                $$
                2a+5d=11
                $$
                이다.

                두 식을 풀면
                $$
                a=-2,\quad d=3
                $$
                이다.

                따라서
                $$
                S_9=\frac{9}{2}(2a+8d)=\frac{9}{2}\times 20=90
                $$
                이다.
                """
            ),
        ),
    ]
)
ALG_ROWS.extend(
    [
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=3,
            crop_box=(80, 250, 1040, 1200),
            source_no=11,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                다음 중 지수함수
                $$
                y=-\left(\frac{1}{2}\right)^{x-1}+1
                $$
                에 대한 설명으로 옳지 않은 것은?
                """
            ),
            choices=(
                "① 정의역은 실수 전체 집합이다.",
                "② 그래프의 점근선은 $y=1$이다.",
                "③ $x$의 값이 증가하면 $y$의 값도 증가한다.",
                "④ 로그함수 $y=-\\log_2 (x-1)+1$과 역함수 관계이다.",
                "⑤ 그래프는 $y=2^{x-1}+1$의 그래프와 점 $(1,1)$에 대하여 대칭이다.",
            ),
            answer="④",
            solution=_q(
                r"""
                역함수를 구하면
                $$
                y=-\left(\frac12\right)^{x-1}+1
                $$
                에서
                $$
                1-y=\left(\frac12\right)^{x-1}
                $$
                이고,
                $$
                x=\log_{\frac12}(1-y)+1=-\log_2 (1-y)+1
                $$
                이다.

                따라서 원래 함수의 역함수는
                $$
                y=-\log_2 (1-x)+1
                $$
                이므로 ④가 옳지 않다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=3,
            crop_box=(80, 1250, 1040, 2350),
            source_no=12,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                방정식
                $$
                \log_2 (x-1)+\frac{1}{2}=\log_4 (x^2-2x+5)
                $$
                을 만족하는 실수 $x$의 값은?
                """
            ),
            choices=("① $-3$", "② $-1$", "③ $1$", "④ $2$", "⑤ $3$"),
            answer="⑤",
            solution=_q(
                r"""
                정의역은
                $$
                x-1>0
                $$
                이므로
                $$
                x>1
                $$
                이다.

                또
                $$
                \log_4 (x^2-2x+5)=\frac12 \log_2 (x^2-2x+5)
                $$
                이므로 주어진 식에 양변에 $2$를 곱하면
                $$
                2\log_2 (x-1)+1=\log_2 (x^2-2x+5)
                $$
                이다.

                따라서
                $$
                \log_2 \left(2(x-1)^2\right)=\log_2 (x^2-2x+5)
                $$
                이므로
                $$
                2(x-1)^2=x^2-2x+5
                $$
                이다.

                정리하면
                $$
                x^2-2x-3=0
                $$
                이고,
                $$
                (x-3)(x+1)=0
                $$
                이다.

                정의역을 만족하는 값은
                $$
                x=3
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=3,
            crop_box=(1100, 250, 2080, 1200),
            source_no=13,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                등차수열 $\{a_n\}$의 공차가 $0$이 아닐 때, 세 수 $a_2,\ a_5,\ a_9$이 순서대로 등비수열을 이룬다.
                $\dfrac{a_{13}}{a_3}$의 값은?
                """
            ),
            choices=("① $2$", "② $3$", "③ $4$", "④ $5$", "⑤ $6$"),
            answer="①",
            solution=_q(
                r"""
                첫째항을 $a$, 공차를 $d$라 하면
                $$
                a_2=a+d,\quad a_5=a+4d,\quad a_9=a+8d
                $$
                이다.

                세 수가 순서대로 등비수열이므로
                $$
                (a+4d)^2=(a+d)(a+8d)
                $$
                이다.

                전개하면
                $$
                a^2+8ad+16d^2=a^2+9ad+8d^2
                $$
                이므로
                $$
                ad=8d^2
                $$
                이다. 공차가 $0$이 아니므로 $d\ne 0$이고,
                $$
                a=8d
                $$
                이다.

                따라서
                $$
                a_{13}=a+12d=20d,\quad a_3=a+2d=10d
                $$
                이므로
                $$
                \dfrac{a_{13}}{a_3}=2
                $$
                이다.
                """
            ),
            note="OCR로 $a_9$를 판독하여 작성함",
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=3,
            crop_box=(1090, 1030, 2080, 2200),
            source_no=14,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                두 실수 $a,\ b$가
                $$
                ab=\log_5 \sqrt{7},\qquad b-a=\log_2 7
                $$
                을 만족시킬 때,
                $$
                2^{\frac1a}\div 2^{\frac1b}
                $$
                의 값은?
                """
            ),
            choices=("① $\\dfrac{25}{2}$", "② $4$", "③ $5$", "④ $25$", "⑤ $32$"),
            answer="④",
            solution=_q(
                r"""
                $$
                2^{\frac1a}\div 2^{\frac1b}=2^{\frac1a-\frac1b}
                =2^{\frac{b-a}{ab}}
                $$
                이다.

                따라서
                $$
                \frac{b-a}{ab}
                =\frac{\log_2 7}{\log_5 \sqrt{7}}
                =\frac{\log_2 7}{\frac12 \log_5 7}
                =2\cdot \frac{\log_2 7}{\log_5 7}
                $$
                이다.

                밑변환을 이용하면
                $$
                \frac{\log_2 7}{\log_5 7}=\log_2 5
                $$
                이므로
                $$
                \frac{b-a}{ab}=2\log_2 5=\log_2 25
                $$
                이다.

                따라서
                $$
                2^{\frac1a}\div 2^{\frac1b}=2^{\log_2 25}=25
                $$
                이다.
                """
            ),
        ),
    ]
)
ALG_ROWS.extend(
    [
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=4,
            crop_box=(70, 250, 1040, 1200),
            source_no=15,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                첫째항이 $10$인 등차수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 하면
                $$
                S_5=S_6
                $$
                이 성립한다. 부등식
                $$
                S_n>S_{n+1}
                $$
                을 만족시키는 $n$의 최솟값은?
                """
            ),
            choices=("① $4$", "② $5$", "③ $6$", "④ $7$", "⑤ $8$"),
            answer="③",
            solution=_q(
                r"""
                $$
                S_6-S_5=a_6
                $$
                이므로
                $$
                a_6=0
                $$
                이다.

                첫째항이 $10$인 등차수열이므로
                $$
                a_6=10+5d=0
                $$
                에서
                $$
                d=-2
                $$
                이다.

                또
                $$
                S_{n+1}-S_n=a_{n+1}
                $$
                이므로 $S_n>S_{n+1}$이려면
                $$
                a_{n+1}<0
                $$
                이어야 한다.

                $$
                a_{n+1}=10+n(-2)=10-2n<0
                $$
                이므로
                $$
                n>5
                $$
                이다.

                따라서 최솟값은
                $$
                6
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=4,
            crop_box=(70, 980, 1040, 1900),
            source_no=16,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                정의역이 $\{x\mid x\ge 3\}$일 때, 함수
                $$
                y=\log_2 \dfrac{4x-10}{x-2}
                $$
                의 치역은?
                """
            ),
            choices=(
                "① $\\{y\\mid y\\ge 1\\}$",
                "② $\\{y\\mid y\\ge 2\\}$",
                "③ $\\{y\\mid 1\\le y<2\\}$",
                "④ $\\{y\\mid 1\\le y\\le 2\\}$",
                "⑤ 양의 실수 전체 집합",
            ),
            answer="③",
            solution=_q(
                r"""
                로그 안의 식을 정리하면
                $$
                \dfrac{4x-10}{x-2}=4-\dfrac{2}{x-2}
                $$
                이다.

                정의역이 $x\ge 3$이므로 $x-2\ge 1$이다.
                따라서
                $$
                0<\dfrac{2}{x-2}\le 2
                $$
                이고,
                $$
                2\le 4-\dfrac{2}{x-2}<4
                $$
                이다.

                그러므로
                $$
                1\le y=\log_2 \dfrac{4x-10}{x-2}<2
                $$
                이다.

                따라서 치역은
                $$
                \{y\mid 1\le y<2\}
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=4,
            crop_box=(1100, 250, 2080, 1500),
            source_no=17,
            kind="objective",
            qtype="객관식",
            question=_q(
                r"""
                자연수 $m\ (m\ge 2)$에 대하여 $2^m$의 $n$제곱근 중에서 정수가 존재하도록 하는 $2$ 이상의 자연수 $n$의 개수를 $f(m)$이라 하자.
                $f(m)=1$을 만족하는 $10$ 이하의 자연수 $m$의 값의 합은?
                """
            ),
            choices=("① $15$", "② $17$", "③ $25$", "④ $26$", "⑤ $30$"),
            answer="②",
            solution=_q(
                r"""
                $2^m$의 $n$제곱근이 정수라고 하자. 그러면 그 정수를 $2^k$라 놓을 수 있고
                $$
                (2^k)^n=2^m
                $$
                이므로
                $$
                2^{kn}=2^m
                $$
                이다. 따라서
                $$
                kn=m
                $$
                이므로 $m$은 $n$의 배수이다.

                따라서 $f(m)$은 $m$의 약수 중 $2$ 이상인 것의 개수와 같다.

                $f(m)=1$이 되려면 $m$의 약수가 $1$과 자기 자신뿐이어야 하므로 $m$은 소수이다.
                $10$ 이하의 자연수 중 $2$ 이상인 소수는
                $$
                2,\ 3,\ 5,\ 7
                $$
                이다.

                따라서 그 합은
                $$
                2+3+5+7=17
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=5,
            crop_box=(40, 180, 1020, 900),
            source_no=1,
            kind="subjective",
            qtype="서답형(단답형)",
            question=_q(
                r"""
                $\log 2=a$일 때, $\log 800$을 $a$로 나타내시오.
                """
            ),
            choices=(),
            answer=r"$3a+2$",
            solution=_q(
                r"""
                $$
                \log 800=\log (8\times 100)=\log 8+\log 100
                $$
                이다.

                또
                $$
                \log 8=\log 2^3=3\log 2=3a,\qquad \log 100=2
                $$
                이므로
                $$
                \log 800=3a+2
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=5,
            crop_box=(40, 900, 1020, 1500),
            source_no=2,
            kind="subjective",
            qtype="서답형(단답형)",
            question=_q(
                r"""
                부등식
                $$
                8^x\le \left(\frac12\right)^{-x+4}
                $$
                을 푸시오.
                """
            ),
            choices=(),
            answer=r"$x\le -2$",
            solution=_q(
                r"""
                양변을 밑이 $2$인 거듭제곱으로 나타내면
                $$
                8^x=2^{3x},\qquad \left(\frac12\right)^{-x+4}=2^{x-4}
                $$
                이다.

                따라서
                $$
                2^{3x}\le 2^{x-4}
                $$
                이므로
                $$
                3x\le x-4
                $$
                이다.

                정리하면
                $$
                2x\le -4
                $$
                이므로
                $$
                x\le -2
                $$
                이다.
                """
            ),
        ),
    ]
)
ALG_ROWS.extend(
    [
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=5,
            crop_box=(30, 1250, 1050, 2400),
            source_no=3,
            kind="subjective",
            qtype="서답형(단답형)",
            question=_q(
                r"""
                첫째항이 양수이고 공비가 음수인 등비수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 하자.
                $$
                a_4a_6=1,\qquad S_3=3a_3
                $$
                일 때, $a_3$의 값을 구하시오.
                """
            ),
            choices=(),
            answer=r"$4$",
            solution=_q(
                r"""
                첫째항을 $a$, 공비를 $r$이라 하면 $a>0,\ r<0$이고
                $$
                a_3=ar^2,\quad a_4=ar^3,\quad a_6=ar^5
                $$
                이다.

                먼저
                $$
                a_4a_6=a^2r^8=1
                $$
                이다.

                또
                $$
                S_3=a+ar+ar^2=a(1+r+r^2)
                $$
                이고
                $$
                S_3=3a_3=3ar^2
                $$
                이므로
                $$
                1+r+r^2=3r^2
                $$
                이다.

                따라서
                $$
                2r^2-r-1=0
                $$
                이고,
                $$
                (2r+1)(r-1)=0
                $$
                이다.

                공비가 음수이므로
                $$
                r=-\frac12
                $$
                이다.

                이제
                $$
                a^2\left(-\frac12\right)^8=1
                $$
                에서
                $$
                a^2\cdot \frac{1}{256}=1
                $$
                이므로
                $$
                a=16
                $$
                이다.

                따라서
                $$
                a_3=ar^2=16\cdot \frac14=4
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=5,
            crop_box=(1040, 180, 2080, 2100),
            source_no=4,
            kind="subjective",
            qtype="서답형(단답형)",
            question=_q(
                r"""
                양의 실수 전체 집합에서 정의된 함수 $f(x)$가 다음을 만족시킨다.

                <div style="border:1px solid #000; padding:8px; margin:8px 0;">
                (가)
                $$
                f(x)=
                \begin{cases}
                3^x-1 & (0\le x\le 1)\\
                3-3^{x-1} & (1< x\le 2)
                \end{cases}
                $$
                (나) 자연수 $n$에 대하여
                $$
                3^n f(x)=f(x-2n)\qquad (2n<x\le 2n+2)
                $$
                </div>

                함수 $y=f(x)\ (2n<x\le 2n+2)$의 그래프와 $x$축으로 둘러싸인 부분의 넓이를 $a_n$이라 하자.
                수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n$이라 할 때, $S_3$의 값을 구하시오.
                """
            ),
            choices=(),
            answer=r"$\dfrac{26}{27}$",
            solution=_q(
                r"""
                먼저 $0\le x\le 2$에서 그래프와 $x$축으로 둘러싸인 넓이를 $A$라 하자.

                $0\le x\le 1$에서
                $$
                f(x)=3^x-1
                $$
                이고, $1< x\le 2$에서 $t=x-1$로 놓으면 $0<t\le 1$이므로
                $$
                f(x)=3-3^{x-1}=3-3^t
                $$
                이다.

                이때
                $$
                (3^t-1)+(3-3^t)=2
                $$
                이므로 구간 $0\le x\le 1$의 그래프와 구간 $1< x\le 2$의 그래프는 직선 $y=1$에 대하여 서로 대칭이다.
                따라서 두 부분의 넓이의 합은 가로의 길이가 $1$, 세로의 길이가 $2$인 직사각형의 넓이와 같으므로
                $$
                A=2
                $$
                이다.

                또
                $$
                3^n f(x)=f(x-2n)\qquad (2n<x\le 2n+2)
                $$
                이므로
                $$
                f(x)=\frac{1}{3^n}f(x-2n)
                $$
                이다.
                즉, $0\le x\le 2$에서의 그래프를 오른쪽으로 $2n$만큼 옮기고 높이를 $\dfrac{1}{3^n}$배 한 것이 구간 $2n<x\le 2n+2$에서의 그래프이다.
                따라서 넓이도 $\dfrac{1}{3^n}$배가 되어
                $$
                a_n=\frac{A}{3^n}=\frac{2}{3^n}
                $$
                이다.

                그러므로
                $$
                S_3=a_1+a_2+a_3
                =\frac{2}{3}+\frac{2}{9}+\frac{2}{27}
                =\frac{26}{27}
                $$
                이다.
                """
            ),
            note="인덱스 해석에 따른 계산 결과를 반영함",
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=6,
            crop_box=(60, 250, 1040, 2700),
            source_no=5,
            kind="subjective",
            qtype="서답형(서술형)",
            question=_q(
                r"""
                세 수 $-8,\ a,\ b$는 이 순서대로 등차수열을 이루고, 세 수 $a,\ 8,\ b$는 이 순서대로 등비수열을 이룬다.
                다음 과정에 따라 $a,\ b$의 값을 구하시오. (단, $a\ne b$)

                1. 등차중항을 이용하여 세 수 $-8,\ a,\ b$의 관계를 나타내시오.
                2. 등비중항을 이용하여 세 수 $a,\ 8,\ b$의 관계를 나타내시오.
                3. 위에서 구한 두 식을 연립하여 $a$에 대한 이차식으로 나타내시오.
                4. 위에서 구한 식을 풀어 $a,\ b$의 값을 구하시오.
                """
            ),
            choices=(),
            answer=r"$a=4,\ b=16$",
            solution=_q(
                r"""
                등차중항의 성질에 의해
                $$
                2a=-8+b
                $$
                이므로
                $$
                b=2a+8
                $$
                이다.

                또 등비중항의 성질에 의해
                $$
                8^2=ab
                $$
                이므로
                $$
                ab=64
                $$
                이다.

                $b=2a+8$을 $ab=64$에 대입하면
                $$
                a(2a+8)=64
                $$
                이고,
                $$
                a^2+4a-32=0
                $$
                이다.

                인수분해하면
                $$
                (a-4)(a+8)=0
                $$
                이므로
                $$
                a=4\quad \text{또는}\quad a=-8
                $$
                이다.

                그런데 $a\ne b$이므로 $a=-8$이면 $b=-8$이 되어 조건에 맞지 않는다.
                따라서
                $$
                a=4
                $$
                이고,
                $$
                b=2a+8=16
                $$
                이다.
                """
            ),
        ),
        ProblemRow(
            exam="MID",
            subject="ALG",
            subject_label="대수",
            page_no=6,
            crop_box=(1070, 150, 2080, 2650),
            source_no=6,
            kind="subjective",
            qtype="서답형(서술형)",
            question=_q(
                r"""
                함수
                $$
                f(x)=-x^2+ax+3
                $$
                일 때, 함수
                $$
                y=\left(\frac14\right)^{f(x)}
                $$
                는 $x=1$일 때 최솟값 $k$를 갖는다.
                이때
                $$
                2^{|f(x)+n|}=\frac{1}{k}
                $$
                을 만족하는 실근이 $3$개가 되도록 하는 자연수 $n$의 값을 구하시오. (단, $a,\ k$는 실수)
                """
            ),
            choices=(),
            answer=r"$4$",
            solution=_q(
                r"""
                밑이 $\dfrac14$이므로
                $$
                y=\left(\frac14\right)^{f(x)}
                $$
                가 최솟값을 가질 때는 $f(x)$가 최댓값을 가진다.

                $f(x)=-x^2+ax+3$의 꼭짓점의 $x$좌표는 $\dfrac{a}{2}$이므로
                $$
                \frac{a}{2}=1
                $$
                에서
                $$
                a=2
                $$
                이다.

                따라서
                $$
                f(x)=-x^2+2x+3=-(x-1)^2+4
                $$
                이고,
                $$
                k=\left(\frac14\right)^4=\frac{1}{256}
                $$
                이다.

                그러므로
                $$
                \frac{1}{k}=256=2^8
                $$
                이므로 주어진 방정식은
                $$
                |f(x)+n|=8
                $$
                과 같다.

                즉
                $$
                f(x)+n=8
                $$
                또는
                $$
                f(x)+n=-8
                $$
                이다.

                첫째 식은
                $$
                -x^2+2x+3+n=8
                $$
                이므로
                $$
                x^2-2x-(n-5)=0
                $$
                이다.
                이 방정식이 중근을 가지려면
                $$
                (-2)^2-4\cdot 1\cdot (-(n-5))=0
                $$
                이고,
                $$
                4+4(n-5)=0
                $$
                에서
                $$
                n=4
                $$
                이다.

                둘째 식은
                $$
                -x^2+2x+3+n=-8
                $$
                이므로
                $$
                x^2-2x-(n+11)=0
                $$
                이다. 이 방정식은 항상 서로 다른 두 실근을 가진다.

                따라서 전체 실근의 개수가 $3$개가 되려면 첫째 식이 중근을 가져야 하므로
                $$
                n=4
                $$
                이다.
                """
            ),
        ),
    ]
)
CAL1_ROWS: List[ProblemRow] = []

UNIT_OVERRIDES: Dict[str, Tuple[str, str, str]] = {
    "JEW-2023-G2-S1-MID-ALG-001": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-002": ("대수(2022개정)", "3. 수열", "3-1. 등차수열"),
    "JEW-2023-G2-S1-MID-ALG-003": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-004": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-005": ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    "JEW-2023-G2-S1-MID-ALG-006": ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    "JEW-2023-G2-S1-MID-ALG-007": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-008": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수"),
    "JEW-2023-G2-S1-MID-ALG-009": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-010": ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    "JEW-2023-G2-S1-MID-ALG-011": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "JEW-2023-G2-S1-MID-ALG-012": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-013": ("대수(2022개정)", "3. 수열", "3-1. 등차수열"),
    "JEW-2023-G2-S1-MID-ALG-014": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-015": ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    "JEW-2023-G2-S1-MID-ALG-016": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수"),
    "JEW-2023-G2-S1-MID-ALG-017": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-101": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-102": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2023-G2-S1-MID-ALG-103": ("대수(2022개정)", "3. 수열", "3-2. 등비수열"),
    "JEW-2023-G2-S1-MID-ALG-104": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "JEW-2023-G2-S1-MID-ALG-105": ("대수(2022개정)", "3. 수열", "3-2. 등비수열"),
    "JEW-2023-G2-S1-MID-ALG-106": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
}


def render_crop(src_pdf: Path, page_no: int, crop_box: Tuple[int, int, int, int], out_path: Path) -> None:
    doc = fitz.open(src_pdf)
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
    doc.close()
    out_path.write_bytes(pix.tobytes("png"))
    with Image.open(out_path) as img:
        img.crop(crop_box).save(out_path)


def build_problem_md(row: ProblemRow, assets: List[str], unit_l1: str, unit_l2: str, unit_l3: str, level: int) -> str:
    unit = f"{unit_l1}>{unit_l2}>{unit_l3}"
    lines: List[str] = [
        "---",
        f"id: {row.problem_id}",
        f"school: {SOURCE_META['school']}",
        f"year: {SOURCE_META['year']}",
        f"grade: {SOURCE_META['grade']}",
        f"semester: {SOURCE_META['semester']}",
        f"exam: {row.exam}",
        f"subject: {row.subject}",
        f"type: {row.qtype}",
        f"source_question_no: {row.source_no}",
        f"source_question_kind: {row.kind}",
        f"source_question_label: {row.source_label}",
        f"difficulty: {level}",
        f"level: {level}",
        f"unit: {unit}",
        f"unit_l1: {unit_l1}",
        f"unit_l2: {unit_l2}",
        f"unit_l3: {unit_l3}",
        f"source: {SOURCE_META['source']}",
        "tags:",
        "- 수동작성",
        f"- {row.qtype}",
        f"- 출제번호-{row.source_tag}",
        f"- 과목-{row.subject_label}",
        f"- 생성일-{SOURCE_META['source'][-10:]}",
        "assets:",
    ]
    lines.extend([f"- {asset}" for asset in assets])
    lines.extend(
        [
            "---",
            "",
            "## Q",
            row.question,
            "",
            "## Choices",
            "\n".join(row.choices),
            "",
            "## Answer",
            row.answer,
            "",
            "## Solution",
            row.solution,
            "",
        ]
    )
    return "\n".join(lines)


def ingest_rows(rows: Sequence[ProblemRow], src_pdf: Path) -> Dict[str, object]:
    summary = {"created": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []

    for row in rows:
        problem_dir = PROBLEMS / row.problem_id
        if problem_dir.exists():
            summary["skipped"] += 1
            results.append(f"{row.problem_id} | skipped | folder exists")
            continue

        assets_dir = problem_dir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        original_name = f"{row.problem_id}_original.png"
        render_crop(src_pdf=src_pdf, page_no=row.page_no, crop_box=row.crop_box, out_path=original_dir / original_name)

        assets = ["assets/original/", f"assets/original/{original_name}"]
        if row.scan_builder is not None:
            row.scan_builder(assets_dir / "scan.png")
            assets.insert(0, "assets/scan.png")

        classified = classify_unit_and_level(
            question_text=row.question,
            choices_text="\n".join(row.choices),
            answer_text=row.answer,
            solution_text=row.solution,
            qtype=row.qtype,
            grade=int(SOURCE_META["grade"]),
            problem_no=row.problem_no,
        )

        unit_l1, unit_l2, unit_l3 = UNIT_OVERRIDES.get(
            row.problem_id,
            (classified.unit_l1, classified.unit_l2, classified.unit_l3),
        )

        md = build_problem_md(
            row=row,
            assets=assets,
            unit_l1=unit_l1,
            unit_l2=unit_l2,
            unit_l3=unit_l3,
            level=classified.level,
        )
        (problem_dir / "problem.md").write_text(md, encoding="utf-8")

        summary["created"] += 1
        note = f" | note={row.note}" if row.note else ""
        results.append(f"{row.problem_id} | created | {unit_l1}>{unit_l2}>{unit_l3} | level={classified.level}{note}")
        if row.note:
            uncertain.append(f"{row.problem_id} | {row.note}")

    summary["warnings"] = len(warnings)
    return {"summary": summary, "results": results, "warnings": warnings, "uncertain": uncertain}


def make_report_block(title: str, report: Dict[str, object]) -> List[str]:
    lines = [
        f"[{title}]",
        "created={created} skipped={skipped} warnings={warnings}".format(**report["summary"]),
        "",
        "[RESULTS]",
        *report["results"],
        "",
        "[WARNINGS]",
        *(report["warnings"] or ["(none)"]),
        "",
        "[OCR_OR_FORMULA_UNCERTAIN]",
        *(report["uncertain"] or ["(none)"]),
        "",
    ]
    return lines


def main() -> None:
    report_lines: List[str] = []

    if ALG_ROWS:
        if not ALG_PDF.is_file():
            raise FileNotFoundError(f"missing source pdf: {ALG_PDF}")
        report_lines.extend(make_report_block("ALG", ingest_rows(ALG_ROWS, ALG_PDF)))

    if CAL1_ROWS:
        if not CAL1_PDF.is_file():
            raise FileNotFoundError(f"missing source pdf: {CAL1_PDF}")
        report_lines.extend(make_report_block("CAL1", ingest_rows(CAL1_ROWS, CAL1_PDF)))

    if not report_lines:
        report_lines.append("No rows configured.")

    report_path = ROOT / "_tmp_jew_2023_g2_ingest_report.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print(f"\nreport: {report_path}")


if __name__ == "__main__":
    main()
