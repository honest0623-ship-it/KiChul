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

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from unit_level_classifier import classify_unit_and_level


ROOT = REPO_ROOT
ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"
SOURCE_PDF = ORIGINAL / "JEW.2023.G2.S1.MID2.CAL1.pdf"

SOURCE_META = {
    "school": "JEW",
    "year": 2023,
    "grade": 2,
    "semester": 1,
    "exam": "MID2",
    "subject": "CAL1",
    "source": "user_upload_2026-03-06",
    "subjective_offset": 100,
}


@dataclass(frozen=True)
class ProblemRow:
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
            f"-S{SOURCE_META['semester']}-{SOURCE_META['exam']}-{SOURCE_META['subject']}-{self.problem_no:03d}"
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


def _closed_point(ax, x: float, y: float) -> None:
    ax.plot(x, y, "o", color="black", markersize=5)


def _open_point(ax, x: float, y: float) -> None:
    ax.plot(
        x,
        y,
        marker="o",
        markersize=6,
        markerfacecolor="white",
        markeredgecolor="black",
        linewidth=1.5,
    )


def _setup_axes(ax, xlim: Tuple[float, float], ylim: Tuple[float, float]) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def build_q3_scan(out_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), dpi=200)

    ax = axes[0]
    _setup_axes(ax, (-2.4, 2.3), (-1.4, 1.5))
    ax.plot([-2, 0], [1, -1], color="black", linewidth=2)
    ax.plot([0, 1], [0, 1], color="black", linewidth=2)
    ax.plot([1, 2], [-1, 0], color="black", linewidth=2)
    _open_point(ax, -2, 1)
    _open_point(ax, 0, -1)
    _closed_point(ax, 0, 0)
    _open_point(ax, 1, 1)
    _closed_point(ax, 1, 0)
    _open_point(ax, 1, -1)
    _closed_point(ax, 2, 0)
    ax.text(0.55, 1.15, r"$y=f(x)$", fontsize=11)
    ax.text(-2, -0.18, r"$-2$", ha="center", va="top", fontsize=9)
    ax.text(1, -0.18, r"$1$", ha="center", va="top", fontsize=9)
    ax.text(2, -0.18, r"$2$", ha="center", va="top", fontsize=9)
    ax.text(-0.12, 1, r"$1$", ha="right", va="center", fontsize=9)
    ax.text(-0.12, -1, r"$-1$", ha="right", va="center", fontsize=9)
    ax.text(0.08, -0.08, r"$O$", ha="left", va="top", fontsize=9)
    ax.text(2.18, -0.04, r"$x$", fontsize=10)
    ax.text(0.06, 1.38, r"$y$", fontsize=10)

    ax = axes[1]
    _setup_axes(ax, (-2.4, 2.3), (-1.4, 1.5))
    ax.plot([-2, 0], [-1, 1], color="black", linewidth=2)
    ax.plot([0, 2], [1, -1], color="black", linewidth=2)
    _open_point(ax, -2, -1)
    _open_point(ax, 0, 1)
    _open_point(ax, 2, -1)
    _closed_point(ax, 0, 0)
    ax.text(0.45, 0.9, r"$y=g(x)$", fontsize=11)
    ax.text(-2, 0.18, r"$-2$", ha="center", va="bottom", fontsize=9)
    ax.text(-1, 0.18, r"$-1$", ha="center", va="bottom", fontsize=9)
    ax.text(1, -0.18, r"$1$", ha="center", va="top", fontsize=9)
    ax.text(2, 0.18, r"$2$", ha="center", va="bottom", fontsize=9)
    ax.text(-0.12, 1, r"$1$", ha="right", va="center", fontsize=9)
    ax.text(-0.12, -1, r"$-1$", ha="right", va="center", fontsize=9)
    ax.text(0.08, -0.08, r"$O$", ha="left", va="top", fontsize=9)
    ax.text(2.18, -0.04, r"$x$", fontsize=10)
    ax.text(0.06, 1.38, r"$y$", fontsize=10)

    fig.tight_layout(pad=0.5)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def build_q13_scan(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    _setup_axes(ax, (-4.8, 4.8), (-2.8, 4.7))
    r = 4.0
    thetas = [math.pi / 2 + t * (math.pi / 2) / 200 for t in range(201)]
    xs = [r * math.cos(t) for t in thetas]
    ys = [r * math.sin(t) for t in thetas]
    ax.plot(xs, ys, color="black", linewidth=2)

    p_x = -r / math.sqrt(5)
    p_y = 2 * r / math.sqrt(5)
    ax.plot([4, -4], [2, -2], color="black", linewidth=1.6)
    ax.plot([4, p_x], [2, p_y], color="black", linewidth=1.6)
    ax.plot([-4, p_x], [-2, p_y], color="black", linewidth=1.6)
    ax.plot([0, 4], [2, 2], color="black", linewidth=1, linestyle="--")
    ax.plot([4, 4], [0, 2], color="black", linewidth=1, linestyle="--")
    _closed_point(ax, 4, 2)
    _closed_point(ax, -4, -2)
    _closed_point(ax, p_x, p_y)
    ax.text(4.08, 2.08, r"$A$", fontsize=10)
    ax.text(-4.55, -2.3, r"$A'$", fontsize=10)
    ax.text(p_x - 0.35, p_y + 0.18, r"$P$", fontsize=10)
    ax.text(-3.45, 2.35, r"$C$", fontsize=10)
    ax.text(0.06, -0.08, r"$O$", ha="left", va="top", fontsize=9)
    ax.text(4, -0.18, r"$4$", ha="center", va="top", fontsize=9)
    ax.text(-4, -0.18, r"$-4$", ha="center", va="top", fontsize=9)
    ax.text(-0.14, 2, r"$2$", ha="right", va="center", fontsize=9)
    ax.text(-0.14, -2, r"$-2$", ha="right", va="center", fontsize=9)
    ax.text(0.08, 4.28, r"$r$", fontsize=10)
    ax.text(4.55, -0.04, r"$x$", fontsize=10)
    ax.text(0.06, 4.55, r"$y$", fontsize=10)
    fig.tight_layout(pad=0.4)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def build_s1_scan(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(3.6, 3.4), dpi=200)
    _setup_axes(ax, (-1.5, 2.4), (-0.8, 3.6))
    ax.plot([-1.3, 2.0], [-0.3, 3.0], color="black", linewidth=2)
    _open_point(ax, 0, 1)
    _closed_point(ax, 0, 3)
    ax.text(0.75, 2.7, r"$y=f(x)$", fontsize=11)
    ax.text(-1, -0.16, r"$-1$", ha="center", va="top", fontsize=9)
    ax.text(-0.12, 1, r"$1$", ha="right", va="center", fontsize=9)
    ax.text(-0.12, 3, r"$3$", ha="right", va="center", fontsize=9)
    ax.text(0.08, -0.08, r"$O$", ha="left", va="top", fontsize=9)
    ax.text(2.22, -0.04, r"$x$", fontsize=10)
    ax.text(0.06, 3.4, r"$y$", fontsize=10)
    fig.tight_layout(pad=0.3)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def build_s4_scan(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.8), dpi=200)
    _setup_axes(ax, (-0.2, 4.4), (-0.3, 3.5))
    ax.plot([0, 1, 2], [0, 1, 0], color="black", linewidth=2)
    ax.plot([2, 3, 4], [2, 3, 2], color="black", linewidth=2)
    ax.plot([0, 4.2], [1.5, 3.6], color="black", linewidth=1.6)
    _closed_point(ax, 0, 0)
    _closed_point(ax, 1, 1)
    _closed_point(ax, 2, 0)
    _open_point(ax, 2, 2)
    _closed_point(ax, 3, 3)
    _closed_point(ax, 4, 2)
    ax.text(-0.08, 2, r"$2$", ha="right", va="center", fontsize=9)
    ax.text(-0.08, 3, r"$3$", ha="right", va="center", fontsize=9)
    for value in (1, 2, 3, 4):
        ax.text(value, -0.16, f"${value}$", ha="center", va="top", fontsize=9)
    ax.text(2.65, 3.08, r"$y=f(x)$", fontsize=11)
    ax.text(-0.08, 1.45, r"$\ell_m$", ha="right", va="center", fontsize=10)
    ax.text(4.18, -0.04, r"$x$", fontsize=10)
    ax.text(0.06, 3.3, r"$y$", fontsize=10)
    fig.tight_layout(pad=0.3)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


ROWS: List[ProblemRow] = [
    ProblemRow(
        page_no=0,
        crop_box=(12, 140, 350, 400),
        source_no=1,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            다음은 함수
            $$
            f(x)=
            \begin{cases}
            3x-1 & (x<2)\\
            k & (x=2)\\
            x^2+1 & (x>2)
            \end{cases}
            $$
            가 $x=2$에서 연속이 되게 하는 상수 $k$의 값은?
            """
        ),
        choices=("① 1", "② 2", "③ 3", "④ 4", "⑤ 5"),
        answer="⑤",
        solution=_q(
            r"""
            $x<2$에서의 식으로 구한 왼쪽 극한은
            $$
            \lim_{x\to 2^-}f(x)=3\cdot 2-1=5
            $$
            이다.

            또 $x>2$에서의 식으로 구한 오른쪽 극한은
            $$
            \lim_{x\to 2^+}f(x)=2^2+1=5
            $$
            이다.

            함수가 $x=2$에서 연속이 되려면
            $$
            k=f(2)=5
            $$
            이어야 한다.
            """
        ),
    ),
    ProblemRow(
        page_no=0,
        crop_box=(12, 350, 350, 631),
        source_no=2,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            $$
            \lim_{x\to 1}\frac{x^2+2x-3}{x-1}
            $$
            의 값은?
            """
        ),
        choices=("① 1", "② 2", "③ 3", "④ 4", "⑤ 5"),
        answer="④",
        solution=_q(
            r"""
            분자를 인수분해하면
            $$
            x^2+2x-3=(x-1)(x+3)
            $$
            이다.

            따라서
            $$
            \frac{x^2+2x-3}{x-1}=x+3 \quad (x\ne 1)
            $$
            이므로
            $$
            \lim_{x\to 1}\frac{x^2+2x-3}{x-1}=1+3=4
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=0,
        crop_box=(12, 594, 350, 962),
        source_no=3,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            두 함수 $y=f(x)$, $y=g(x)$의 그래프가 다음과 같을 때,
            $$
            \lim_{x\to 0^-}f(x)+g(0)
            $$
            의 값은?

            <img src="assets/scan.png" alt="JEW-2023-G2-S1-MID2-CAL1-003 graph" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ),
        choices=("① $-2$", "② $-1$", "③ $0$", "④ $1$", "⑤ $2$"),
        answer="②",
        solution=_q(
            r"""
            그래프에서
            $$
            \lim_{x\to 0^-}f(x)=-1
            $$
            이고, $x=0$에서의 함수값은
            $$
            g(0)=0
            $$
            이다.

            따라서
            $$
            \lim_{x\to 0^-}f(x)+g(0)=-1+0=-1
            $$
            이다.
            """
        ),
        scan_builder=build_q3_scan,
    ),
    ProblemRow(
        page_no=0,
        crop_box=(350, 112, 712, 350),
        source_no=4,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            함수
            $$
            f(x)=\frac{1}{12}x^3+\frac{1}{3}x^2-\frac{1}{6}x+1
            $$
            라 할 때, $x=1$에서 $f(x)$의 순간변화율의 값은?
            """
        ),
        choices=(r"① $\dfrac{1}{2}$", r"② $\dfrac{3}{4}$", r"③ $1$", r"④ $\dfrac{5}{4}$", r"⑤ $2$"),
        answer="②",
        solution=_q(
            r"""
            순간변화율은 미분계수이므로
            $$
            f'(x)=\frac{1}{4}x^2+\frac{2}{3}x-\frac{1}{6}
            $$
            이다.

            따라서
            $$
            f'(1)=\frac{1}{4}+\frac{2}{3}-\frac{1}{6}
            =\frac{3+8-2}{12}
            =\frac{3}{4}
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=0,
        crop_box=(350, 312, 712, 619),
        source_no=5,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            다음 중 $x=2$에서 미분가능한 함수는?
            """
        ),
        choices=(
            r"① $y=x-2$",
            r"② $y=\left|x-2\right|$",
            r"③ $y=\dfrac{1}{x-2}$",
            r"④ $y=\dfrac{1}{\left|x-2\right|}$",
            r"⑤ $y=\dfrac{x-2}{\left|x-2\right|}$",
        ),
        answer="①",
        solution=_q(
            r"""
            ①의 함수 $y=x-2$는 일차함수이므로 모든 실수에서 미분가능하다.

            ②는 $x=2$에서 뾰족한 점이 생겨 미분가능하지 않다.
            ③, ④는 $x=2$에서 정의되지 않는다.
            ⑤도 $x=2$에서 정의되지 않는다.

            따라서 $x=2$에서 미분가능한 함수는
            $$
            y=x-2
            $$
            뿐이다.
            """
        ),
    ),
    ProblemRow(
        page_no=0,
        crop_box=(350, 581, 712, 962),
        source_no=6,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            다음 중 $A,B,C$를 큰 순서대로 올바르게 나열한 것은?

            $$
            A=\lim_{x\to\infty}\frac{3x^2+x+3}{4x^2+3x+4},\quad
            B=\lim_{x\to 3}\frac{x^2-4}{3x-6},\quad
            C=\lim_{x\to 1}\frac{2x+2}{x^2+x+2}
            $$
            """
        ),
        choices=("① A-B-C", "② A-C-B", "③ B-A-C", "④ B-C-A", "⑤ C-A-B"),
        answer="④",
        solution=_q(
            r"""
            $$
            A=\lim_{x\to\infty}\frac{3x^2+x+3}{4x^2+3x+4}=\frac{3}{4}
            $$
            이다.

            또
            $$
            B=\lim_{x\to 3}\frac{x^2-4}{3x-6}=\frac{9-4}{9-6}=\frac{5}{3}
            $$
            이고,
            $$
            C=\lim_{x\to 1}\frac{2x+2}{x^2+x+2}=\frac{4}{4}=1
            $$
            이다.

            따라서
            $$
            B>C>A
            $$
            이므로 큰 순서대로 나열하면
            $$
            B-C-A
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=1,
        crop_box=(12, 19, 362, 294),
        source_no=7,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            실수 전체의 집합에서 연속인 함수 $f(x)$가
            $$
            (x-2)f(x)=x^2-3x+2
            $$
            를 만족시킬 때,
            $$
            \lim_{x\to 2}f(x)
            $$
            의 값은?
            """
        ),
        choices=("① 1", "② 2", "③ 3", "④ 4", "⑤ 5"),
        answer="①",
        solution=_q(
            r"""
            $$
            x^2-3x+2=(x-1)(x-2)
            $$
            이므로 $x\ne 2$에서
            $$
            f(x)=x-1
            $$
            이다.

            따라서
            $$
            \lim_{x\to 2}f(x)=\lim_{x\to 2}(x-1)=1
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=1,
        crop_box=(12, 237, 362, 513),
        source_no=8,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            함수 $f(x)$가 모든 실수 $x$에 대하여
            $$
            2x\le f(x)\le 2x+1
            $$
            을 만족시킬 때,
            $$
            \lim_{x\to\infty}\frac{x f(x)}{x^2+5}
            $$
            의 값은?
            """
        ),
        choices=(r"① $\dfrac{1}{2}$", r"② $1$", r"③ $0$", r"④ $2$", r"⑤ $3$"),
        answer="④",
        solution=_q(
            r"""
            주어진 부등식에 $x>0$를 곱하면
            $$
            2x^2\le x f(x)\le 2x^2+x
            $$
            이다.

            따라서
            $$
            \frac{2x^2}{x^2+5}\le \frac{x f(x)}{x^2+5}\le \frac{2x^2+x}{x^2+5}
            $$
            이다.

            이때
            $$
            \lim_{x\to\infty}\frac{2x^2}{x^2+5}=2,\qquad
            \lim_{x\to\infty}\frac{2x^2+x}{x^2+5}=2
            $$
            이므로 샌드위치 정리에 의하여
            $$
            \lim_{x\to\infty}\frac{x f(x)}{x^2+5}=2
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=1,
        crop_box=(12, 456, 362, 969),
        source_no=9,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            함수 $f(x)$, $g(x)$에 대하여
            $$
            \lim_{x\to 1}f(x),\quad \lim_{x\to 1}g(x)
            $$
            가 존재할 때, $x=1$에서 극한값이 항상 존재하는 것을 <보기>에서 있는 대로 고른 것은?

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            <보기><br />
            ㄱ. $2f(x)+g(x)+1$<br />
            ㄴ. $f(x)g(x)$<br />
            ㄷ. $\dfrac{g(x)}{f(x)-g(x)}$<br />
            ㄹ. $\dfrac{g(x)}{\{f(x)\}^2+1}$
            </div>
            """
        ),
        choices=("① ㄱ, ㄴ", "② ㄴ, ㄷ", "③ ㄱ, ㄴ, ㄷ", "④ ㄱ, ㄴ, ㄹ", "⑤ ㄱ, ㄴ, ㄷ, ㄹ"),
        answer="④",
        solution=_q(
            r"""
            ㄱ은 극한의 합과 실수배를 이용하면 항상 극한값이 존재한다.

            ㄴ은 두 함수의 극한값이 각각 존재하므로 곱의 극한값도 항상 존재한다.

            ㄷ은
            $$
            \lim_{x\to 1}\{f(x)-g(x)\}=0
            $$
            이 될 수 있으므로 항상 존재한다고 할 수 없다.

            ㄹ은
            $$
            \{f(x)\}^2+1>0
            $$
            이므로 분모의 극한값이 0이 될 수 없다. 따라서 항상 극한값이 존재한다.

            그러므로 옳은 것은 ㄱ, ㄴ, ㄹ이다.
            """
        ),
    ),
    ProblemRow(
        page_no=1,
        crop_box=(362, 12, 715, 513),
        source_no=10,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            곡선
            $$
            y=x^3-2x
            $$
            위의 점 $A(p,q)$에서의 접선이 직선
            $$
            y=-x+3
            $$
            에 수직일 때, $p+q$의 값은?
            (단, $A$는 제2사분면 위의 점이다.)
            """
        ),
        choices=("① $-1$", "② $0$", "③ $1$", "④ $2$", "⑤ $3$"),
        answer="②",
        solution=_q(
            r"""
            직선 $y=-x+3$의 기울기는 $-1$이므로, 이에 수직인 접선의 기울기는
            $$
            1
            $$
            이다.

            곡선 $y=x^3-2x$의 도함수는
            $$
            y'=3x^2-2
            $$
            이므로
            $$
            3p^2-2=1
            $$
            이다.

            따라서
            $$
            p^2=1
            $$
            이고, 제2사분면 위의 점이므로
            $$
            p=-1
            $$
            이다.

            이때
            $$
            q=p^3-2p=-1+2=1
            $$
            이므로
            $$
            p+q=0
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=1,
        crop_box=(362, 450, 715, 956),
        source_no=11,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            함수
            $$
            f(x)=\frac{2x+1}{mx^2+mx+3-m}
            $$
            가 모든 실수에서 연속이 되기 위한 정수 $m$의 개수는?
            """
        ),
        choices=("① 0개", "② 1개", "③ 2개", "④ 3개", "⑤ 4개"),
        answer="④",
        solution=_q(
            r"""
            모든 실수에서 연속이 되려면 분모가 0이 되는 실수가 없어야 한다.

            먼저 $m=0$이면 분모가
            $$
            3
            $$
            이므로 조건을 만족한다.

            이제 $m\ne 0$이라 하면 분모는 이차식
            $$
            mx^2+mx+3-m
            $$
            이다. 이 식이 실근을 가지지 않으려면 판별식이 음수이어야 하므로
            $$
            D=m^2-4m(3-m)<0
            $$
            이다.

            정리하면
            $$
            D=5m^2-12m=m(5m-12)<0
            $$
            이므로
            $$
            0<m<\frac{12}{5}
            $$
            이다.

            정수 $m$은
            $$
            1,\ 2
            $$
            이고, 여기에 $m=0$도 가능하므로 모두
            $$
            3\text{개}
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=2,
        crop_box=(12, 19, 350, 387),
        source_no=12,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            다음 중 주어진 구간에서 최댓값과 최솟값을 모두 가지는 함수를 있는 대로 고른 것은?

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            <보기><br />
            ㄱ. $y=x^2+2x-4,\ [0,2]$<br />
            ㄴ. $y=x^2-4x+2,\ [0,3)$<br />
            ㄷ. $y=\sqrt{x+1},\ [0,5)$<br />
            ㄹ. $y=\dfrac{3x+1}{x},\ [-1,1]$
            </div>
            """
        ),
        choices=("① ㄱ, ㄴ", "② ㄴ, ㄷ", "③ ㄱ, ㄹ", "④ ㄱ, ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄹ"),
        answer="①",
        solution=_q(
            r"""
            ㄱ은 닫힌구간 $[0,2]$에서 연속이므로 최댓값과 최솟값을 모두 가진다.

            ㄴ은
            $$
            y=x^2-4x+2=(x-2)^2-2
            $$
            이므로 최솟값은 $x=2$에서 $-2$이고, 최댓값은 $x=0$에서 $2$이다.

            ㄷ은 증가함수이지만 구간의 오른쪽 끝 $5$가 포함되지 않으므로 최댓값이 없다.

            ㄹ은 $x=0$에서 정의되지 않으므로 주어진 구간 전체에서의 함수가 아니다.

            따라서 옳은 것은 ㄱ, ㄴ이다.
            """
        ),
    ),
    ProblemRow(
        page_no=2,
        crop_box=(350, 19, 715, 450),
        source_no=14,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            두 실수 $a(a<1)$, $b$에 대하여 함수
            $$
            f(x)=
            \begin{cases}
            \dfrac{1-a}{x-1}+2 & (x\le a)\\
            b(x-a)+1 & (x>a)
            \end{cases}
            $$
            라 하자. 다음 중 옳은 것을 있는 대로 고른 것은?

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            <보기><br />
            ㄱ. $\lim_{x\to a^+}f(x)=1$<br />
            ㄴ. $f(x)$는 $x=a$에서 연속이다.<br />
            ㄷ. $\lim_{x\to\infty}f(x)$의 값이 존재하면, $f(a)=f(1)$이다.
            </div>
            """
        ),
        choices=("① ㄱ", "② ㄱ, ㄴ", "③ ㄴ, ㄷ", "④ ㄱ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"),
        answer="⑤",
        solution=_q(
            r"""
            ㄱ. $x>a$에서의 식은
            $$
            f(x)=b(x-a)+1
            $$
            이므로
            $$
            \lim_{x\to a^+}f(x)=1
            $$
            이다.

            ㄴ. $x=a$일 때
            $$
            f(a)=\frac{1-a}{a-1}+2=-1+2=1
            $$
            이다. 왼쪽 극한과 오른쪽 극한도 모두 1이므로 $x=a$에서 연속이다.

            ㄷ. $\lim_{x\to\infty}f(x)$의 값이 존재하려면
            $$
            b=0
            $$
            이어야 한다. 그러면 $x>a$에서 $f(x)=1$이고, $a<1$이므로
            $$
            f(1)=1
            $$
            이다. 또한 $f(a)=1$이므로
            $$
            f(a)=f(1)
            $$
            이다.

            따라서 ㄱ, ㄴ, ㄷ이 모두 옳다.
            """
        ),
    ),
    ProblemRow(
        page_no=2,
        crop_box=(12, 387, 350, 962),
        source_no=13,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            > 오류문항: 보기 중 정답이 없습니다. 실제 값은 $2\sqrt{5}$입니다.

            다음 그림과 같이 $r>2$에 대하여, 좌표평면 위에 사분원의 호
            $$
            C:x^2+y^2=r^2 \quad (x\le 0,\ y\ge 0)
            $$
            과 점 $A(4,2)$가 있다. 점 $A$를 원점에 대하여 대칭이동한 점인 $A'$과, $C$를 움직이는 점 $P$에 대하여 삼각형 $AA'P$의 넓이의 최댓값을 $n(r)$이라 할 때,
            $$
            \lim_{r\to\infty}\frac{n(r)}{r}
            $$
            의 값은?

            <img src="assets/scan.png" alt="JEW-2023-G2-S1-MID2-CAL1-013 geometry" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ),
        choices=(r"① $\dfrac{1}{\sqrt{5}}$", r"② $1$", r"③ $2$", r"④ $\sqrt{5}$", r"⑤ $3$"),
        answer="오류문항(보기에 없음)",
        solution=_q(
            r"""
            점 $P$를
            $$
            P(x,y)
            $$
            라 하자. 그러면 $x\le 0$, $y\ge 0$, $x^2+y^2=r^2$이다.

            좌표를 이용한 삼각형의 넓이 공식으로 삼각형 $AA'P$의 넓이 $S$를 구하면
            $$
            S=\frac12\left|4(-2-y)+(-4)(y-2)+x\{2-(-2)\}\right|
            $$
            이다.

            정리하면
            $$
            S=2|x-2y|
            $$
            이고, $x\le 0$, $y\ge 0$이므로
            $$
            S=2(2y-x)
            $$
            이다.

            또
            $$
            (2y-x)^2=5(x^2+y^2)-(2x+y)^2
            $$
            이므로
            $$
            (2y-x)^2\le 5r^2
            $$
            이다.

            따라서
            $$
            2y-x\le \sqrt{5}\,r
            $$
            이고, 최댓값은
            $$
            \sqrt{5}\,r
            $$
            이다.

            그러므로
            $$
            n(r)=2\sqrt{5}\,r
            $$
            이고,
            $$
            \lim_{r\to\infty}\frac{n(r)}{r}=2\sqrt{5}
            $$
            이다.

            즉, 원래 보기에는 정답이 없다.
            """
        ),
        scan_builder=build_q13_scan,
        note="오류문항: 보기 중 정답 없음, 실제 값은 2√5",
    ),
    ProblemRow(
        page_no=2,
        crop_box=(350, 462, 715, 962),
        source_no=15,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            실수 전체에서 정의된 함수 $f(x)$에 대하여 다음 중 옳은 것을 있는 대로 고른 것은?

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            <보기><br />
            ㄱ. $\lim_{x\to 1}\dfrac{f(x)-f(1)}{x-1}=0$이면, $f(1)=\lim_{x\to 1}f(x)$이다.<br />
            ㄴ. $\lim_{h\to 0}\dfrac{f(1+h)-f(1-h)}{2h}=2$이면, 미분계수 $f'(1)$가 존재하고, 그 값은 $1$이다.<br />
            ㄷ. $f'(1)$이 존재하고, 모든 실수 $x$에 대하여 $f(x)=f(-x)$이면, $f'(-1)=-f'(1)$이다.
            </div>
            """
        ),
        choices=("① ㄱ", "② ㄱ, ㄴ", "③ ㄱ, ㄷ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"),
        answer="③",
        solution=_q(
            r"""
            ㄱ. 주어진 식에서
            $$
            \lim_{x\to 1}\frac{f(x)-f(1)}{x-1}=0
            $$
            이면 분자
            $$
            f(x)-f(1)\to 0
            $$
            이므로
            $$
            \lim_{x\to 1}f(x)=f(1)
            $$
            이다. 따라서 참이다.

            ㄴ. 식
            $$
            \frac{f(1+h)-f(1-h)}{2h}
            $$
            의 극한은 좌우에서 대칭으로 본 평균변화율이다. 이 값이 2라고 해서 미분계수가 반드시 존재하는 것은 아니며, 미분가능하다 하더라도 그 값은 2가 된다. 따라서 거짓이다.

            ㄷ. 모든 실수 $x$에 대하여 $f(x)=f(-x)$이므로 $f$는 짝함수이다. 짝함수의 도함수는 홀함수가 되므로
            $$
            f'(-1)=-f'(1)
            $$
            이다. 따라서 참이다.

            그러므로 옳은 것은 ㄱ, ㄷ이다.
            """
        ),
    ),
    ProblemRow(
        page_no=3,
        crop_box=(12, 12, 350, 537),
        source_no=16,
        kind="objective",
        qtype="객관식",
        question=_q(
            r"""
            함수 $f(x)$에 대하여 $x=1$에서
            $$
            \lim_{x\to 1^+}f(x)=\lim_{x\to 1^-}f(x)
            $$
            이고,
            $$
            \lim_{x\to 1}\frac{f(x)-1}{x^2-3f(1)}=1
            $$
            이다. 다음 중 옳은 것을 있는 대로 고른 것은?

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            <보기><br />
            ㄱ. $f(1)=\dfrac{1}{3}$이면, 함수 $g(x)=\{f(x)\}^2-\dfrac{4}{3}f(x)$는 $x=1$에서 연속이다.<br />
            ㄴ. $f(x)$가 $x=1$에서 불연속이면, $3f(1)+\lim_{x\to 1^+}f(x)=2$이다.<br />
            ㄷ. $f(x)$가 $x=1$에서 연속이면, $f(1)=\dfrac{1}{2}$이다.
            </div>
            """
        ),
        choices=("① ㄱ", "② ㄴ", "③ ㄱ, ㄷ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"),
        answer="⑤",
        solution=_q(
            r"""
            공통된 극한값을
            $$
            L=\lim_{x\to 1}f(x)
            $$
            라 하자.

            ㄱ. $f(1)=\dfrac13$이면 분모는
            $$
            x^2-1
            $$
            이 되어 $x\to 1$일 때 0으로 간다. 주어진 극한값이 1이므로 분자도 0으로 가야 하여
            $$
            L=1
            $$
            이다. 따라서
            $$
            \lim_{x\to 1}g(x)=L^2-\frac43L=1-\frac43=-\frac13
            $$
            이고,
            $$
            g(1)=\left(\frac13\right)^2-\frac43\cdot \frac13=-\frac13
            $$
            이므로 $g(x)$는 $x=1$에서 연속이다.

            ㄴ. $f(x)$가 $x=1$에서 불연속이면 $L\ne f(1)$이다. 이때 주어진 식에서
            $$
            L-1=1-3f(1)
            $$
            이므로
            $$
            3f(1)+L=2
            $$
            이다. 또한 $L=\lim_{x\to 1^+}f(x)$이므로 ㄴ은 참이다.

            ㄷ. $f(x)$가 $x=1$에서 연속이면
            $$
            L=f(1)
            $$
            이다. 따라서
            $$
            f(1)-1=1-3f(1)
            $$
            이고,
            $$
            4f(1)=2
            $$
            이므로
            $$
            f(1)=\frac12
            $$
            이다. 따라서 ㄷ도 참이다.

            그러므로 ㄱ, ㄴ, ㄷ이 모두 옳다.
            """
        ),
    ),
    ProblemRow(
        page_no=3,
        crop_box=(350, 0, 715, 350),
        source_no=1,
        kind="subjective",
        qtype="서답형(단답형)",
        question=_q(
            r"""
            함수 $f(x)$의 그래프가 다음과 같을 때, $x=0$에서의 극한값
            $$
            \lim_{x\to 0}f(x)
            $$
            을 구하시오.

            <img src="assets/scan.png" alt="JEW-2023-G2-S1-MID2-CAL1-101 graph" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ),
        choices=(),
        answer=r"$1$",
        solution=_q(
            r"""
            그래프에서 $x=0$의 왼쪽과 오른쪽에서 모두 함수값이
            $$
            1
            $$
            에 가까워진다.

            따라서
            $$
            \lim_{x\to 0}f(x)=1
            $$
            이다.
            """
        ),
        scan_builder=build_s1_scan,
    ),
    ProblemRow(
        page_no=3,
        crop_box=(350, 325, 715, 662),
        source_no=2,
        kind="subjective",
        qtype="서답형(단답형)",
        question=_q(
            r"""
            곡선
            $$
            y=x^3-2x+3
            $$
            위의 점 $(1,2)$에서의 접선의 방정식을 구하시오.
            """
        ),
        choices=(),
        answer=r"$y=x+1$",
        solution=_q(
            r"""
            도함수는
            $$
            y'=3x^2-2
            $$
            이므로 $x=1$에서의 기울기는
            $$
            3\cdot 1^2-2=1
            $$
            이다.

            따라서 점 $(1,2)$를 지나고 기울기가 1인 접선의 방정식은
            $$
            y-2=x-1
            $$
            이고,
            $$
            y=x+1
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=3,
        crop_box=(350, 644, 715, 1000),
        source_no=3,
        kind="subjective",
        qtype="서답형(단답형)",
        question=_q(
            r"""
            $$
            \lim_{x\to -a}\frac{x^2-a^2}{x^3+a^3}=2,\qquad
            \lim_{x\to\infty}\left(\frac{\sqrt{x^2+2x+x}}{bx+1}\right)=1
            $$
            일 때, $a+b$의 값을 구하시오.
            (단, $a,b$는 상수)
            """
        ),
        choices=(),
        answer=r"$\dfrac{2}{3}$",
        solution=_q(
            r"""
            먼저
            $$
            x^2-a^2=(x+a)(x-a),\qquad
            x^3+a^3=(x+a)(x^2-ax+a^2)
            $$
            이므로
            $$
            \frac{x^2-a^2}{x^3+a^3}=\frac{x-a}{x^2-ax+a^2}
            $$
            이다.

            따라서
            $$
            \lim_{x\to -a}\frac{x^2-a^2}{x^3+a^3}
            =\frac{-a-a}{(-a)^2-(-a)a+a^2}
            =\frac{-2a}{3a^2}
            =-\frac{2}{3a}
            $$
            이다.

            이 값이 2이므로
            $$
            -\frac{2}{3a}=2
            $$
            에서
            $$
            a=-\frac13
            $$
            이다.

            또
            $$
            \sqrt{x^2+2x+x}=\sqrt{x^2+3x}
            $$
            이고, $x\to\infty$일 때 분자와 분모를 $x$로 나누어 생각하면
            $$
            \lim_{x\to\infty}\frac{\sqrt{x^2+3x}}{bx+1}
            =\lim_{x\to\infty}\frac{x\sqrt{1+\frac{3}{x}}}{x\left(b+\frac{1}{x}\right)}
            =\frac{1}{b}
            $$
            이다.

            이 값이 1이므로
            $$
            b=1
            $$
            이다.

            따라서
            $$
            a+b=-\frac13+1=\frac23
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=4,
        crop_box=(12, 0, 350, 575),
        source_no=4,
        kind="subjective",
        qtype="서답형(단답형)",
        question=_q(
            r"""
            임의의 실수 $m$에 대하여 $\ell_m$은 점 $(1,2)$를 지나는 기울기 $m$인 직선이다. 닫힌구간 $[0,4]$에서 정의된 함수 $f(x)$의 그래프가 다음과 같을 때, 함수 $y=f(x)$와 직선 $\ell_m$이 만나는 점의 개수를 $g(m)$이라 하자. $m=\dfrac12$에서 함수 $g(m)$의 우극한과 좌극한을 각각 $a,b$라 할 때, $a,b,g(a),g(b)$의 값을 각각 순서대로 구하시오.

            <img src="assets/scan.png" alt="JEW-2023-G2-S1-MID2-CAL1-104 graph" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ),
        choices=(),
        answer=r"$0,\ 2,\ 1,\ 1$",
        solution=_q(
            r"""
            직선 $\ell_m$의 방정식은
            $$
            y=m(x-1)+2
            $$
            이다.

            그래프의 위쪽 왼편 선분은
            $$
            y=x \quad (2<x\le 3)
            $$
            이므로, 이 선분과의 교점의 $x$좌표는
            $$
            x=m(x-1)+2
            $$
            에서
            $$
            x=\frac{2-m}{1-m}
            $$
            이다. 이 값이 $2<x\le 3$이 되려면
            $$
            0<m\le \frac12
            $$
            이어야 한다.

            또 위쪽 오른편 선분은
            $$
            y=-x+6 \quad (3\le x\le 4)
            $$
            이므로, 이 선분과의 교점의 $x$좌표는
            $$
            -x+6=m(x-1)+2
            $$
            에서
            $$
            x=\frac{m+4}{m+1}
            $$
            이다. 이 값이 $3\le x\le 4$가 되려면
            $$
            0\le m\le \frac12
            $$
            이어야 한다.

            따라서 $m<\dfrac12$에서 $\dfrac12$에 아주 가까우면 교점이 2개이고, $m>\dfrac12$에서 $\dfrac12$에 아주 가까우면 교점이 없다.
            그러므로
            $$
            a=0,\qquad b=2
            $$
            이다.

            이제
            $$
            g(0)
            $$
            을 구하면, 직선은 $y=2$가 되고 그래프와는 점 $(4,2)$에서만 만나므로
            $$
            g(0)=1
            $$
            이다.

            또
            $$
            g(2)
            $$
            를 구하면, 직선은 $y=2x$가 되고 그래프와는 점 $(0,0)$에서만 만나므로
            $$
            g(2)=1
            $$
            이다.

            따라서 구하는 값은
            $$
            0,\ 2,\ 1,\ 1
            $$
            이다.
            """
        ),
        scan_builder=build_s4_scan,
    ),
    ProblemRow(
        page_no=4,
        crop_box=(350, 0, 715, 637),
        source_no=5,
        kind="subjective",
        qtype="서답형(서술형)",
        question=_q(
            r"""
            함수
            $$
            f(x)=x^2+3x+1
            $$
            에 대하여 $x$의 값이 $1$에서 $a$까지 변할 때의 평균변화율이 $3f'(a)$와 같다. 다음 물음에 대하여 풀이과정과 함께 답안을 서술하시오.
            (단, $a$는 $a\ne 1$인 상수이다.)

            1. $x$의 값이 $1$에서 $a$까지 변할 때의 평균변화율을 구하시오.
            2. $x=a$에서 $f(x)$의 미분계수 $f'(a)$를 구하시오.
            3. $a$와 $f(a)$의 값을 각각 구하시오.
            """
        ),
        choices=(),
        answer=r"$a=-1,\ f(a)=-1$",
        solution=_q(
            r"""
            먼저
            $$
            f(1)=1+3+1=5
            $$
            이다.

            1. 평균변화율은
            $$
            \frac{f(a)-f(1)}{a-1}
            =\frac{(a^2+3a+1)-5}{a-1}
            =\frac{a^2+3a-4}{a-1}
            $$
            이다.
            $$
            a^2+3a-4=(a+4)(a-1)
            $$
            이므로
            $$
            \frac{f(a)-f(1)}{a-1}=a+4
            $$
            이다.

            2. 도함수는
            $$
            f'(x)=2x+3
            $$
            이므로
            $$
            f'(a)=2a+3
            $$
            이다.

            3. 조건에 따라
            $$
            a+4=3(2a+3)
            $$
            이다.
            정리하면
            $$
            a+4=6a+9
            $$
            이므로
            $$
            a=-1
            $$
            이다.

            따라서
            $$
            f(a)=f(-1)=(-1)^2+3(-1)+1=-1
            $$
            이다.
            """
        ),
    ),
    ProblemRow(
        page_no=4,
        crop_box=(350, 575, 715, 962),
        source_no=6,
        kind="subjective",
        qtype="서답형(서술형)",
        question=_q(
            r"""
            실수 전체에서 정의된 함수
            $$
            g(x)=|x-1|+1
            $$
            에 대하여 다음 물음에 답하시오.

            1. 함수 $g(x)$의 $x=1$에서의 연속성을 조사하시오.
            2. 함수 $g(x)$의 $x=1$에서의 미분가능성을 조사하시오.
            """
        ),
        choices=(),
        answer="(1) 연속이다. (2) 미분가능하지 않다.",
        solution=_q(
            r"""
            절댓값의 정의에 따라
            $$
            g(x)=
            \begin{cases}
            -(x-1)+1=-x+2 & (x<1)\\
            x-1+1=x & (x\ge 1)
            \end{cases}
            $$
            이다.

            1. $x\to 1$일 때 왼쪽에서나 오른쪽에서나 함수값은 모두
            $$
            1
            $$
            로 가까워지고,
            $$
            g(1)=|1-1|+1=1
            $$
            이다. 따라서 $x=1$에서 연속이다.

            2. 왼쪽에서의 기울기는
            $$
            -1
            $$
            이고, 오른쪽에서의 기울기는
            $$
            1
            $$
            이다. 왼쪽 미분계수와 오른쪽 미분계수가 서로 다르므로 $x=1$에서 미분가능하지 않다.
            """
        ),
    ),
    ProblemRow(
        page_no=5,
        crop_box=(12, 0, 375, 562),
        source_no=7,
        kind="subjective",
        qtype="서답형(서술형)",
        question=_q(
            r"""
            이차함수 $y=f(x)$가 다음을 만족할 때, 다음 물음에 대하여 풀이과정과 함께 답안을 서술하시오.

            <div style="border:1px solid #000; padding:8px; margin:8px 0;">
            $$
            \lim_{x\to 2}\frac{f(x)-1}{x-2}=3,\qquad
            \lim_{x\to 1}\frac{x-1}{f(x)+f(2)}=1
            $$
            </div>

            1. $\lim_{x\to 2}f(x)$와 $f(2)$를 구하시오.
            2. $f(x)$의 $x=2$에서의 미분계수 $f'(2)$를 구하시오.
            3. $f(1)$을 구하시오.
            4. $f(x)$를 구하시오.
            5. 연속함수의 성질을 이용하여 열린구간 $(1,2)$에서 방정식 $f(x)=0$이 적어도 하나의 실근을 가짐을 보이시오.
            """
        ),
        choices=(),
        answer=r"$f(x)=x^2-x-1$",
        solution=_q(
            r"""
            이차함수는 연속함수이므로 차례로 구해 보자.

            1.
            $$
            \lim_{x\to 2}\frac{f(x)-1}{x-2}=3
            $$
            이 유한한 값이므로 분자도 0으로 가야 한다. 따라서
            $$
            \lim_{x\to 2}f(x)=1
            $$
            이다.
            이차함수는 연속이므로
            $$
            f(2)=1
            $$
            이다.

            2.
            $$
            \lim_{x\to 2}\frac{f(x)-1}{x-2}
            =\lim_{x\to 2}\frac{f(x)-f(2)}{x-2}
            =f'(2)
            $$
            이므로
            $$
            f'(2)=3
            $$
            이다.

            3.
            $$
            \lim_{x\to 1}\frac{x-1}{f(x)+f(2)}=1
            $$
            이고 $f(2)=1$이므로, 분모가 0으로 가야 한다. 따라서
            $$
            f(1)+1=0
            $$
            이고
            $$
            f(1)=-1
            $$
            이다.

            4. 이차함수를
            $$
            f(x)=ax^2+bx+c
            $$
            라 하자.
            $$
            f(2)=1,\qquad f'(2)=3,\qquad f(1)=-1
            $$
            이므로
            $$
            4a+2b+c=1,\qquad 4a+b=3,\qquad a+b+c=-1
            $$
            이다.

            첫째 식에서 셋째 식을 빼면
            $$
            3a+b=2
            $$
            이고, 이것을
            $$
            4a+b=3
            $$
            와 연립하면
            $$
            a=1,\qquad b=-1
            $$
            이다.
            다시
            $$
            a+b+c=-1
            $$
            에 대입하면
            $$
            c=-1
            $$
            이다.

            따라서
            $$
            f(x)=x^2-x-1
            $$
            이다.

            5.
            $$
            f(1)=-1,\qquad f(2)=1
            $$
            이므로
            $$
            f(1)<0<f(2)
            $$
            이다.
            함수 $f(x)$는 연속이므로 연속함수의 성질에 의하여 열린구간 $(1,2)$에서 방정식
            $$
            f(x)=0
            $$
            은 적어도 하나의 실근을 가진다.
            """
        ),
    ),
]

UNIT_OVERRIDES: Dict[str, Tuple[str, str, str]] = {
    "JEW-2023-G2-S1-MID2-CAL1-004": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-005": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-010": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-012": ("미적분 I(2022개정)", "2. 미분", "2-2. 도함수의 활용"),
    "JEW-2023-G2-S1-MID2-CAL1-015": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-102": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-104": ("미적분 I(2022개정)", "2. 미분", "2-2. 도함수의 활용"),
    "JEW-2023-G2-S1-MID2-CAL1-105": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-106": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    "JEW-2023-G2-S1-MID2-CAL1-107": ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
}


def render_crop(src_pdf: Path, page_no: int, crop_box: Tuple[int, int, int, int], out_path: Path) -> None:
    doc = fitz.open(src_pdf)
    try:
        page = doc.load_page(page_no)
        rect = fitz.Rect(*crop_box)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.4, 2.4), clip=rect, alpha=False)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(out_path)
    finally:
        doc.close()


def build_problem_md(row: ProblemRow, assets: List[str], unit_l1: str, unit_l2: str, unit_l3: str, level: int) -> str:
    unit = f"{unit_l1}>{unit_l2}>{unit_l3}"
    lines: List[str] = [
        "---",
        f"id: {row.problem_id}",
        f"school: {SOURCE_META['school']}",
        f"year: {SOURCE_META['year']}",
        f"grade: {SOURCE_META['grade']}",
        f"semester: {SOURCE_META['semester']}",
        f"exam: {SOURCE_META['exam']}",
        f"subject: {SOURCE_META['subject']}",
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
        "- 과목-미적분 I",
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
    duplicates: List[str] = []
    review_paths: List[str] = []

    for row in rows:
        problem_dir = PROBLEMS / row.problem_id
        problem_md = problem_dir / "problem.md"
        if problem_dir.exists():
            summary["skipped"] += 1
            duplicates.append(row.problem_id)
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
        problem_md.write_text(md, encoding="utf-8")
        review_paths.append(str(problem_md.resolve()))

        summary["created"] += 1
        note = f" | note={row.note}" if row.note else ""
        results.append(
            f"{row.problem_id} | created | {unit_l1}>{unit_l2}>{unit_l3} | level={classified.level}{note}"
        )
        if row.note:
            warnings.append(f"{row.problem_id}: {row.note}")

    summary["warnings"] = len(warnings)
    return {
        "summary": summary,
        "results": results,
        "warnings": warnings,
        "uncertain": uncertain,
        "duplicates": duplicates,
        "review_paths": review_paths,
    }


def make_report_block(report: Dict[str, object]) -> List[str]:
    return [
        "[CAL1]",
        "created={created} skipped={skipped} warnings={warnings}".format(**report["summary"]),
        "",
        "[RESULTS]",
        *report["results"],
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
    if not SOURCE_PDF.is_file():
        raise FileNotFoundError(f"missing source pdf: {SOURCE_PDF}")

    report = ingest_rows(ROWS, SOURCE_PDF)
    report_lines = make_report_block(report)
    report_path = ROOT / "_tmp_jew_2023_g2_s1_mid2_cal1_ingest_report.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print(f"report: {report_path}")


if __name__ == "__main__":
    main()
