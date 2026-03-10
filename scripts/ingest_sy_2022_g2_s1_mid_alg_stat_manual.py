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
REPORT = ROOT / "_tmp_sy_2022_g2_s1_ingest_report.txt"
SOURCE = "user_upload_2026-03-06"
PIXEL_SCALE = 2.5


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
    unit_l1: str
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


ALG_L1 = "대수(2022개정)"
ALG_L2_EXP = "1. 지수함수와 로그함수"
ALG_L3_EXP = "1-1. 지수와 로그"
ALG_L2_TRI = "2. 삼각함수"
ALG_L3_TRI = "2-1. 삼각함수"

STAT_L1 = "확률과 통계(2022개정)"
STAT_L2_CASES = "1. 경우의 수"
STAT_L3_PERM = "1-1. 순열"
STAT_L3_COMB = "1-2. 조합"


ALG_ROWS: List[ProblemRow] = []
STAT_ROWS: List[ProblemRow] = []


ALG_ROWS.extend(
    [
        obj(
            page_no=1,
            crop_box=(40, 260, 860, 760),
            source_no=1,
            question=_q(
                r"""
                $16$의 네제곱근 중 양의 실수인 것을 $a$, $\dfrac{1}{27}$의 세제곱근 중 실수인 것을 $b$라 할 때, $ab$의 값은?
                """
            ),
            choices=(
                r"$\dfrac{1}{3}$",
                r"$\dfrac{2}{3}$",
                r"$1$",
                r"$\dfrac{4}{3}$",
                r"$\dfrac{5}{3}$",
            ),
            answer="②",
            solution=_q(
                r"""
                $a$는 $16$의 양의 네제곱근이므로
                \[
                a=2
                \]
                이고,
                \[
                b=\sqrt[3]{\frac{1}{27}}=\frac{1}{3}
                \]
                이다.

                따라서
                \[
                ab=2\times \frac{1}{3}=\frac{2}{3}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(40, 720, 860, 1240),
            source_no=2,
            question=_q(
                r"""
                $x>1$이고 $x+\dfrac{1}{x}=3$일 때, $x^{\frac{1}{2}}-x^{-\frac{1}{2}}$의 값은?
                """
            ),
            choices=(r"$1$", r"$\sqrt{2}$", r"$2$", r"$3$", r"$4$"),
            answer="①",
            solution=_q(
                r"""
                \[
                \left(\sqrt{x}-\frac{1}{\sqrt{x}}\right)^2
                =x+\frac{1}{x}-2
                =3-2
                =1
                \]
                이다.

                그런데 $x>1$이므로
                \[
                \sqrt{x}-\frac{1}{\sqrt{x}}>0
                \]
                이다.

                따라서
                \[
                \sqrt{x}-\frac{1}{\sqrt{x}}=1
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(40, 1190, 860, 1680),
            source_no=3,
            question=_q(
                r"""
                $15^x=16$, $3^y=2$일 때, $2^{\frac{4}{x}-\frac{1}{y}}$의 값은?
                """
            ),
            choices=(r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"),
            answer="⑤",
            solution=_q(
                r"""
                \[
                \frac{4}{x}
                =4\log_{16}15
                =\log_2 15
                \]
                이고,
                \[
                \frac{1}{y}=\log_2 3
                \]
                이다.

                따라서 지수는
                \[
                \log_2 15-\log_2 3=\log_2 5
                \]
                이므로
                \[
                2^{\frac{4}{x}-\frac{1}{y}}=2^{\log_2 5}=5
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(40, 1640, 860, 2460),
            source_no=4,
            question=_q(
                r"""
                $\log_{x-1}(-x^2+6x+7)$이 정의되도록 하는 모든 정수 $x$의 합은?
                """
            ),
            choices=(r"$12$", r"$15$", r"$18$", r"$21$", r"$24$"),
            answer="③",
            solution=_q(
                r"""
                로그의 밑과 진수의 조건은
                \[
                x-1>0,\quad x-1\ne 1,\quad -x^2+6x+7>0
                \]
                이다.

                진수 조건은
                \[
                -x^2+6x+7>0
                \iff (x+1)(x-7)<0
                \]
                이므로
                \[
                -1<x<7
                \]
                이다.

                이를 모두 만족하는 정수는
                \[
                x=3,4,5,6
                \]
                이다.

                따라서 합은
                \[
                3+4+5+6=18
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(900, 260, 1780, 760),
            source_no=5,
            question=_q(
                r"""
                $5^a=2$, $5^b=3$일 때, $\log_3 12$를 $a$, $b$로 나타내면?
                """
            ),
            choices=(
                r"$\dfrac{2a+b}{a}$",
                r"$\dfrac{a+2b}{a}$",
                r"$\dfrac{a+b}{b}$",
                r"$\dfrac{2a+b}{b}$",
                r"$\dfrac{a+2b}{b}$",
            ),
            answer="④",
            solution=_q(
                r"""
                \[
                a=\log_5 2,\qquad b=\log_5 3
                \]
                이므로
                \[
                \log_3 12=\frac{\log_5 12}{\log_5 3}
                =\frac{\log_5(2^2\cdot 3)}{\log_5 3}
                =\frac{2\log_5 2+\log_5 3}{b}
                =\frac{2a+b}{b}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(900, 720, 1780, 1250),
            source_no=6,
            question=_q(
                r"""
                이차방정식 $x^2-7x+5=0$의 두 근을 $\log_2 a$, $\log_2 b$라 할 때, $\log_a b+\log_b a$의 값은?
                """
            ),
            choices=(r"$7$", r"$\dfrac{36}{5}$", r"$\dfrac{37}{5}$", r"$\dfrac{38}{5}$", r"$\dfrac{39}{5}$"),
            answer="⑤",
            solution=_q(
                r"""
                두 근을
                \[
                p=\log_2 a,\qquad q=\log_2 b
                \]
                라 하면
                \[
                p+q=7,\qquad pq=5
                \]
                이다.

                또
                \[
                \log_a b=\frac{\log_2 b}{\log_2 a}=\frac{q}{p},\qquad
                \log_b a=\frac{p}{q}
                \]
                이므로
                \[
                \log_a b+\log_b a
                =\frac{p^2+q^2}{pq}
                =\frac{(p+q)^2-2pq}{pq}
                =\frac{49-10}{5}
                =\frac{39}{5}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=1,
            crop_box=(900, 1230, 1780, 2460),
            source_no=7,
            question=_q(
                rf"""
                옳은 것만을 <보기>에서 있는 대로 고른 것은?

                {_box([
                    "<strong>&lt;보기&gt;</strong>",
                    r"ㄱ. $2^{{\log_2 1+\log_2 2+\log_2 3+\cdots+\log_2 9}}=1\times2\times3\times\cdots\times9$",
                    r"ㄴ. $\log_2(2\times2^2\times2^3\times\cdots\times2^9)=90$",
                    r"ㄷ. $(\log_2 2)(\log_2 2^2)(\log_2 2^3)\cdots(\log_2 2^9)=45$",
                ])}
                """
            ),
            choices=("ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"),
            answer="②",
            solution=_q(
                r"""
                ㄱ. 로그의 성질로
                \[
                \log_2 1+\log_2 2+\cdots+\log_2 9
                =\log_2(1\times2\times\cdots\times9)
                \]
                이므로 참이다.

                ㄴ. 로그 안을 정리하면
                \[
                2\times2^2\times\cdots\times2^9=2^{1+2+\cdots+9}=2^{45}
                \]
                이므로
                \[
                \log_2(2^{45})=45
                \]
                이다. 따라서 거짓이다.

                ㄷ. 각 인수는
                \[
                \log_2 2=1,\ \log_2 2^2=2,\ \ldots,\ \log_2 2^9=9
                \]
                이므로 곱은
                \[
                1\times2\times\cdots\times9
                \]
                이다. 따라서 $45$가 아니므로 거짓이다.

                따라서 옳은 것은 ㄱ, ㄴ이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=2,
            crop_box=(40, 260, 860, 840),
            source_no=8,
            question=_q(
                r"""
                함수 $f(x)=\left(\dfrac{1}{5}\right)^{x^2-4x+1}$은 $x=a$에서 최댓값 $M$을 갖는다. $M-a$의 값은?
                """
            ),
            choices=(r"$123$", r"$125$", r"$129$", r"$131$", r"$133$"),
            answer="①",
            solution=_q(
                r"""
                밑이
                \[
                0<\frac{1}{5}<1
                \]
                이므로 지수
                \[
                x^2-4x+1=(x-2)^2-3
                \]
                가 가장 작을 때 함수값이 가장 크다.

                따라서
                \[
                a=2,\qquad M=\left(\frac{1}{5}\right)^{-3}=5^3=125
                \]
                이다.

                그러므로
                \[
                M-a=125-2=123
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
    ]
)

STAT_ROWS.extend(
    [
        obj(
            page_no=1,
            crop_box=(40, 260, 860, 760),
            source_no=1,
            question=_q(
                r"""
                부모와 $3$명의 자녀로 구성된 $5$명의 가족이 원탁에 둘러앉을 때, 부모가 이웃하게 앉는 경우의 수는?
                """
            ),
            choices=(r"$12$", r"$14$", r"$16$", r"$18$", r"$20$"),
            answer="①",
            solution=_q(
                r"""
                부모 $2$명을 한 묶음으로 보면 모두 $4$개를 원탁에 배열하는 경우의 수는
                \[
                (4-1)!=6
                \]
                이다.

                부모끼리의 자리바꿈은
                \[
                2!=2
                \]
                가지이므로 전체 경우의 수는
                \[
                6\times 2=12
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=1,
            crop_box=(40, 720, 860, 1180),
            source_no=2,
            question=_q(
                r"""
                같은 종류의 빵 $6$개를 같은 종류의 바구니 $3$개에 담는 방법의 수는? (단, 빈 바구니는 없다.)
                """
            ),
            choices=(r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"),
            answer="③",
            solution=_q(
                r"""
                같은 종류의 바구니이므로 $6$을 $3$개의 양의 정수의 합으로 나타내는 경우의 수를 구하면 된다.

                가능한 경우는
                \[
                4+1+1,\qquad 3+2+1,\qquad 2+2+2
                \]
                의 $3$가지이다.

                따라서 방법의 수는
                \[
                3
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        obj(
            page_no=1,
            crop_box=(40, 1130, 860, 1700),
            source_no=3,
            question=_q(
                r"""
                $2$, $3$, $4$, $5$, $6$ 다섯 개의 숫자 중에서 중복을 허용하여 $5$개를 뽑아 다섯 자리 자연수를 만들 때, 만의 자리의 수와 일의 자리의 수의 합이 $8$인 자연수의 개수는?
                """
            ),
            choices=(r"$125$", r"$250$", r"$400$", r"$625$", r"$875$"),
            answer="④",
            solution=_q(
                r"""
                만의 자리와 일의 자리의 합이 $8$이 되려면
                \[
                (2,6),\ (3,5),\ (4,4),\ (5,3),\ (6,2)
                \]
                의 $5$가지가 있다.

                나머지 세 자리는 각각 $5$가지씩 선택할 수 있으므로
                \[
                5^3=125
                \]
                가지이다.

                따라서 전체 개수는
                \[
                5\times 125=625
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=1,
            crop_box=(40, 1650, 860, 2460),
            source_no=4,
            question=_q(
                r"""
                `college`에 있는 $7$개의 문자를 일렬로 나열할 때, 양 끝에 $e$가 오도록 나열하는 방법의 수는?
                """
            ),
            choices=(r"$56$", r"$60$", r"$64$", r"$68$", r"$72$"),
            answer="②",
            solution=_q(
                r"""
                양 끝의 $e$는 고정된다.

                가운데에는
                \[
                c,\ o,\ l,\ l,\ g
                \]
                를 배열하면 되므로 경우의 수는
                \[
                \frac{5!}{2!}=60
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=1,
            crop_box=(900, 260, 1780, 760),
            source_no=5,
            question=_q(
                r"""
                $x$, $y$, $z$, $w$가 모두 자연수일 때, 방정식 $x+y+z+w=10$을 만족하는 해의 개수는?
                """
            ),
            choices=(r"$68$", r"$72$", r"$76$", r"$80$", r"$84$"),
            answer="⑤",
            solution=_q(
                r"""
                자연수 해의 개수이므로
                \[
                x'=x-1,\ y'=y-1,\ z'=z-1,\ w'=w-1
                \]
                라 두면
                \[
                x'+y'+z'+w'=6
                \]
                인 음이 아닌 정수해의 개수를 구하면 된다.

                따라서 경우의 수는
                \[
                {}_{4}H_{7}={}_{9}C_{3}=84
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        obj(
            page_no=1,
            crop_box=(900, 720, 1780, 1220),
            source_no=6,
            question=_q(
                r"""
                서우는 수민과 채원을 포함한 $5$명의 친구와 함께 모두 $6$명이 원탁에 둘러앉아 저녁을 먹으려고 한다. 서우와 수민은 마주보고, 서우와 채원은 이웃하게 앉는 경우의 수는?
                """
            ),
            choices=(r"$6$", r"$8$", r"$10$", r"$12$", r"$15$"),
            answer="④",
            solution=_q(
                r"""
                원탁이므로 서우의 자리를 고정한다.

                수민은 서우의 맞은편에만 앉을 수 있으므로 자리가 $1$가지이다.

                채원은 서우의 양옆 두 자리 중 한 곳에 앉을 수 있으므로
                \[
                2
                \]
                가지이다.

                나머지 $3$명은 남은 $3$자리에 배열하면 되므로
                \[
                3!=6
                \]
                가지이다.

                따라서 전체 경우의 수는
                \[
                1\times 2\times 6=12
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=1,
            crop_box=(900, 1180, 1780, 1780),
            source_no=7,
            question=_q(
                r"""
                오른쪽 그림은 같은 정육면체 $6$개를 쌓아 만든 직육면체이다. 정육면체의 모서리를 따라 꼭짓점 $A$에서 꼭짓점 $B$까지 최단 거리로 가는 경우의 수는?
                """
            )
            + _scan("정육면체 6개로 만든 직육면체"),
            choices=(r"$30$", r"$45$", r"$60$", r"$75$", r"$90$"),
            answer="③",
            solution=_q(
                r"""
                그림에서 $A$에서 $B$까지 최단 거리로 가려면 가로로 $2$칸, 깊이 방향으로 $1$칸, 세로로 $3$칸 이동해야 한다.

                따라서 이동 순서를 배열하는 경우의 수는
                \[
                \frac{6!}{2!\,1!\,3!}=60
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
            scan_file="SY.2022.G2.S1.MID2.STAT.007.png",
        ),
        obj(
            page_no=1,
            crop_box=(900, 1730, 1780, 2460),
            source_no=8,
            question=_q(
                r"""
                $7$가지 색으로 정사면체를 칠하는 방법의 수는? (단, 모든 면의 색은 다르다.)
                """
            ),
            choices=(r"$35$", r"$42$", r"$52$", r"$60$", r"$70$"),
            answer="⑤",
            solution=_q(
                r"""
                먼저 사용할 $4$가지 색을 고르는 방법은
                \[
                {}_{7}C_{4}=35
                \]
                가지이다.

                정해진 $4$가지 색으로 정사면체의 각 면을 모두 다르게 칠할 때, 한 면의 색을 바닥면으로 정하면 나머지 $3$면의 원형 배열만 따지면 되므로 경우의 수는
                \[
                (3-1)!=2
                \]
                가지이다.

                따라서 전체 방법의 수는
                \[
                35\times 2=70
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=2,
            crop_box=(40, 260, 860, 1070),
            source_no=9,
            question=_q(
                r"""
                남자 $4$명과 여자 $4$명이 각 변에 $2$명씩 앉는 정사각형 모양의 탁자에 둘러앉아 보드게임을 하려고 한다. 같은 모서리에 해당하는 두 좌석에는 반드시 남녀가 $1$명씩 앉도록 할 때, $8$명이 둘러앉는 방법의 수는?
                """
            ),
            choices=(r"$2304$", r"$2324$", r"$2348$", r"$2396$", r"$2456$"),
            answer="①",
            solution=_q(
                r"""
                정사각형의 네 모서리에 대응하는 좌석쌍마다 남자와 여자가 한 명씩 앉아야 한다.

                위쪽의 두 좌석과 아래쪽의 두 좌석에 남녀를 정하는 방법은 각각 $2$가지씩이므로, 전체 좌석의 성별 배치는
                \[
                2^4=16
                \]
                가지이다.

                성별 자리가 정해지면 남자 $4$명은 남자 자리 $4$곳에
                \[
                4!
                \]
                가지로, 여자 $4$명도
                \[
                4!
                \]
                가지로 앉는다.

                다만 정사각형 탁자는 $90^\circ$씩 회전한 경우가 같은 배치이므로 $4$로 나누어야 한다.

                따라서 경우의 수는
                \[
                \frac{16\times 4!\times 4!}{4}=2304
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=2,
            crop_box=(40, 1030, 860, 1620),
            source_no=10,
            question=_q(
                r"""
                ${}_{3}C_{0}+{}_{3}C_{1}+{}_{4}C_{2}+\cdots+{}_{10}C_{8}$의 값은?
                """
            ),
            choices=(r"$120$", r"$165$", r"$220$", r"$286$", r"$364$"),
            answer="②",
            solution=_q(
                r"""
                \[
                {}_{3}C_{0}={}_{2}C_{2},\quad
                {}_{3}C_{1}={}_{3}C_{2},\quad
                {}_{4}C_{2}={}_{4}C_{2},\ \ldots,\ 
                {}_{10}C_{8}={}_{10}C_{2}
                \]
                이므로
                \[
                {}_{2}C_{2}+{}_{3}C_{2}+{}_{4}C_{2}+\cdots+{}_{10}C_{2}
                \]
                와 같다.

                조합의 합의 성질에 의해
                \[
                {}_{2}C_{2}+{}_{3}C_{2}+\cdots+{}_{10}C_{2}={}_{11}C_{3}=165
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
    ]
)

STAT_ROWS.extend(
    [
        obj(
            page_no=2,
            crop_box=(40, 1580, 860, 2040),
            source_no=11,
            question=_q(
                r"""
                $21^{31}$을 $400$으로 나눈 나머지는?
                """
            ),
            choices=(r"$221$", r"$231$", r"$241$", r"$251$", r"$261$"),
            answer="①",
            solution=_q(
                r"""
                \[
                21=20+1
                \]
                이므로
                \[
                21^{31}=(20+1)^{31}
                \]
                이다.

                이항정리를 이용하면
                \[
                (20+1)^{31}=1+{}_{31}C_{1}20+{}_{31}C_{2}20^2+\cdots
                \]
                이다.

                그런데 $20^2=400$이므로 $20^2$ 이상이 포함된 항은 모두 $400$의 배수이다.

                따라서 나머지는
                \[
                1+31\times 20=621
                \]
                을 $400$으로 나눈 나머지와 같으므로
                \[
                621-400=221
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        obj(
            page_no=2,
            crop_box=(40, 1990, 860, 2460),
            source_no=12,
            question=_q(
                r"""
                $(1,\ 1,\ 1,\ 2,\ 2,\ 3)$ 여섯 개의 숫자 중에서 $4$개를 뽑아 네 자리 자연수를 만들려고 한다. 만들 수 있는 경우의 수는?
                """
            ),
            choices=(r"$38$", r"$39$", r"$40$", r"$41$", r"$42$"),
            answer="①",
            solution=_q(
                r"""
                사용할 숫자의 중복 형태를 나누어 세면 된다.

                \[
                (1,1,1,2),\ (1,1,1,3),\ (1,1,2,2),\ (1,1,2,3),\ (1,2,2,3)
                \]
                의 다섯 경우가 가능하다.

                각 경우의 배열 수는 차례로
                \[
                \frac{4!}{3!}=4,\quad
                \frac{4!}{3!}=4,\quad
                \frac{4!}{2!2!}=6,\quad
                \frac{4!}{2!}=12,\quad
                \frac{4!}{2!}=12
                \]
                이다.

                따라서 전체 개수는
                \[
                4+4+6+12+12=38
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=2,
            crop_box=(900, 260, 1780, 900),
            source_no=13,
            question=_q(
                r"""
                크기와 모양이 각각 같은 축구공 $6$개, 배구공 $11$개, 농구공 $11$개 중에서 $11$개의 공을 택하는 경우의 수는?
                """
            ),
            choices=(r"$56$", r"$60$", r"$63$", r"$68$", r"$77$"),
            answer="③",
            solution=_q(
                r"""
                축구공, 배구공, 농구공을 각각 $x$, $y$, $z$개 고른다고 하면
                \[
                x+y+z=11
                \]
                이고,
                \[
                0\le x\le 6,\qquad y\ge 0,\qquad z\ge 0
                \]
                이다.

                제한이 없다면 음이 아닌 정수해의 개수는
                \[
                {}_{3}H_{11}={}_{13}C_{2}=78
                \]
                이다.

                여기서 축구공을 $7$개 이상 고르는 경우를 빼야 한다.
                $x'=x-7$이라 두면
                \[
                x'+y+z=4
                \]
                의 음이 아닌 정수해 개수와 같으므로
                \[
                {}_{3}H_{4}={}_{6}C_{2}=15
                \]
                이다.

                따라서 구하는 경우의 수는
                \[
                78-15=63
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        obj(
            page_no=2,
            crop_box=(900, 860, 1780, 1710),
            source_no=14,
            question=_q(
                r"""
                하연을 포함하여 다섯 명의 학생이 전학을 와서 $A$반, $B$반, $C$반에 배정하려고 한다. 하연이 $A$반에 배정되었을 때, 나머지 네 명의 학생을 배정하는 방법의 수는? (단, 각 반에 적어도 한 명 이상 배정한다.)
                """
            ),
            choices=(r"$30$", r"$35$", r"$40$", r"$45$", r"$50$"),
            answer="⑤",
            solution=_q(
                r"""
                하연은 이미 $A$반에 배정되어 있다.

                나머지 $4$명은 각각 $A$, $B$, $C$반 중 한 반에 배정될 수 있으므로 전체 경우의 수는
                \[
                3^4=81
                \]
                이다.

                여기서 $B$반이 비는 경우는 $A$, $C$반에만 배정하는 경우이므로
                \[
                2^4=16
                \]
                가지이고, $C$반이 비는 경우도
                \[
                2^4=16
                \]
                가지이다.

                두 경우를 모두 빼면 $B$반과 $C$반이 모두 비는 경우를 두 번 뺀 것이므로
                \[
                1
                \]
                가지를 다시 더해 주어야 한다.

                따라서 구하는 경우의 수는
                \[
                81-16-16+1=50
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
        obj(
            page_no=2,
            crop_box=(900, 1660, 1780, 2460),
            source_no=15,
            question=_q(
                r"""
                $300000$보다 작은 여섯 자리 홀수 중 각 자리의 숫자의 합이 $11$인 모든 자연수의 개수는?
                """
            ),
            choices=(r"$670$", r"$685$", r"$700$", r"$715$", r"$730$"),
            answer="④",
            solution=_q(
                r"""
                첫째 자리를 $a$, 마지막 자리를 $b$라 하자.
                여섯 자리 수가 $300000$보다 작으므로
                \[
                a=1\ \text{또는}\ 2
                \]
                이다.

                또 홀수이므로
                \[
                b=1,3,5,7,9
                \]
                이다.

                1. $a=1$인 경우

                가운데 네 자리의 합은 $10-b$이므로 경우의 수는
                \[
                {}_{4}H_{10-b}
                \]
                이다.

                따라서
                \[
                {}_{4}H_{9}+{}_{4}H_{7}+{}_{4}H_{5}+{}_{4}H_{3}+{}_{4}H_{1}
                ={}_{12}C_{3}+{}_{10}C_{3}+{}_{8}C_{3}+{}_{6}C_{3}+{}_{4}C_{3}
                \]
                \[
                =220+120+56+20+4=420
                \]
                이다.

                2. $a=2$인 경우

                가운데 네 자리의 합은 $9-b$이므로 경우의 수는
                \[
                {}_{4}H_{8}+{}_{4}H_{6}+{}_{4}H_{4}+{}_{4}H_{2}+{}_{4}H_{0}
                \]
                이다.

                따라서
                \[
                {}_{11}C_{3}+{}_{9}C_{3}+{}_{7}C_{3}+{}_{5}C_{3}+{}_{3}C_{3}
                =165+84+35+10+1=295
                \]
                이다.

                그러므로 전체 개수는
                \[
                420+295=715
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        sub(
            page_no=3,
            crop_box=(40, 260, 860, 1430),
            source_no=1,
            question=_q(
                r"""
                다항식 $(a+b+c+d)^7$의 전개식에서 서로 다른 항의 개수를 구하시오.
                """
            ),
            answer=r"$120$",
            solution=_q(
                r"""
                전개식의 서로 다른 항은
                \[
                a^x b^y c^z d^w
                \]
                꼴에서
                \[
                x+y+z+w=7
                \]
                을 만족하는 음이 아닌 정수해의 개수와 같다.

                따라서 개수는
                \[
                {}_{4}H_{7}={}_{10}C_{3}=120
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        sub(
            page_no=3,
            crop_box=(40, 1400, 860, 2460),
            source_no=2,
            question=_q(
                r"""
                오른쪽 그림은 호수가 있는 어느 마을의 도로망이다. $A$지역에서 $B$지역까지 최단 거리로 가는 경우의 수를 구하시오.
                """
            )
            + _scan("호수가 있는 도로망"),
            answer=r"$30$",
            solution=_q(
                r"""
                오른쪽 또는 위쪽으로만 움직이며 각 교차점까지의 최단 경로 수를 적어 가면 된다.

                맨 아래 줄부터 차례로 적으면
                \[
                1,\ 1,\ 1,\ 1,\ 1,\ 1
                \]
                \[
                1,\ 2,\ 0,\ 1,\ 2,\ 3
                \]
                \[
                1,\ 3,\ 0,\ 0,\ 2,\ 5
                \]
                \[
                1,\ 4,\ 4,\ 4,\ 6,\ 11
                \]
                \[
                1,\ 5,\ 9,\ 13,\ 19,\ 30
                \]
                이다.

                따라서 $B$지역까지 최단 거리로 가는 경우의 수는
                \[
                30
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
            scan_file="SY.2022.G2.S1.MID2.STAT.서답2번.png",
        ),
        sub(
            page_no=3,
            crop_box=(900, 260, 1780, 2460),
            source_no=3,
            question=_q(
                r"""
                $(2x^3-3x)^6$의 전개식에서 $x^{14}$의 계수를 구하시오.
                """
            ),
            answer=r"$2160$",
            solution=_q(
                r"""
                전개식의 일반항은
                \[
                {}_{6}C_{r}(2x^3)^{6-r}(-3x)^r
                \]
                이다.

                이를 정리하면
                \[
                {}_{6}C_{r}2^{6-r}(-3)^r x^{18-2r}
                \]
                이다.

                $x^{14}$의 계수를 구해야 하므로
                \[
                18-2r=14
                \]
                에서
                \[
                r=2
                \]
                이다.

                따라서 계수는
                \[
                {}_{6}C_{2}\cdot 2^4\cdot (-3)^2
                =15\times 16\times 9
                =2160
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        sub(
            page_no=4,
            crop_box=(40, 260, 860, 2460),
            source_no=4,
            question=_q(
                r"""
                같은 종류의 볼펜 $4$개와 서로 다른 종류의 공책 $11$개 중 $5$개를 택하여 선물 세트를 만들려고 한다. 만들 수 있는 선물 세트의 종류의 개수를 구하시오.
                """
            ),
            answer=r"$1023$",
            solution=_q(
                r"""
                볼펜을 $k$개 넣는다고 하면 $k$는
                \[
                0,1,2,3,4
                \]
                이다.

                각 경우마다 공책은 $5-k$개를 골라야 하므로 경우의 수는
                \[
                {}_{11}C_{5}+{}_{11}C_{4}+{}_{11}C_{3}+{}_{11}C_{2}+{}_{11}C_{1}
                \]
                이다.

                따라서
                \[
                462+330+165+55+11=1023
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_COMB,
        ),
        sub(
            page_no=4,
            crop_box=(900, 260, 1780, 2460),
            source_no=5,
            question=_q(
                r"""
                네 개의 숫자 $1$, $2$, $3$, $4$에서 중복을 허용하여 $4$개를 뽑아 네 자리 자연수를 만들 때, $1$은 연속하여 사용하지 않고 만들 수 있는 자연수의 개수를 구하시오.
                """
            ),
            answer=r"$216$",
            solution=_q(
                r"""
                전체 네 자리 수의 개수는
                \[
                4^4=256
                \]
                이다.

                이제 $11$이 적어도 한 번 나타나는 경우를 뺀다.

                \[
                A_1=\text{앞의 두 자리가 }11,\quad
                A_2=\text{가운데 두 자리가 }11,\quad
                A_3=\text{뒤의 두 자리가 }11
                \]
                라 하자.

                그러면
                \[
                |A_1|=|A_2|=|A_3|=4^2=16
                \]
                이고,
                \[
                |A_1\cap A_2|=4,\quad |A_2\cap A_3|=4,\quad |A_1\cap A_3|=1
                \]
                이며,
                \[
                |A_1\cap A_2\cap A_3|=1
                \]
                이다.

                따라서 포함배제의 원리에 의해 $11$이 적어도 한 번 나타나는 경우의 수는
                \[
                16+16+16-4-4-1+1=40
                \]
                이다.

                그러므로 구하는 개수는
                \[
                256-40=216
                \]
                이다.
                """
            ),
            unit_l2=STAT_L2_CASES,
            unit_l3=STAT_L3_PERM,
        ),
    ]
)

ALG_ROWS.extend(
    [
        obj(
            page_no=2,
            crop_box=(40, 800, 860, 1390),
            source_no=9,
            question=_q(
                r"""
                함수 $f(x)=a^x\ (a>0,\ a\ne 1)$에 대하여 $f(t)=2$일 때, $f(2t)f\left(\dfrac{t}{2}\right)$의 값은?
                """
            ),
            choices=(r"$2$", r"$2\sqrt{2}$", r"$4$", r"$4\sqrt{2}$", r"$6$"),
            answer="④",
            solution=_q(
                r"""
                $f(t)=2$이므로
                \[
                a^t=2
                \]
                이다.

                따라서
                \[
                f(2t)f\left(\frac{t}{2}\right)=a^{2t}\cdot a^{t/2}
                =(a^t)^2\cdot (a^t)^{1/2}
                =2^2\cdot \sqrt{2}
                =4\sqrt{2}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=2,
            crop_box=(40, 1360, 860, 2460),
            source_no=10,
            question=_q(
                r"""
                다음 함수의 그래프 중에서 함수 $y=3^x$의 그래프를 평행이동하거나 대칭이동하여 포갤 수 없는 것은?
                """
            ),
            choices=(
                r"$y=\left(\dfrac{1}{3}\right)^x$",
                r"$y=3^x+2$",
                r"$y=\log_3 \dfrac{1}{x}$",
                r"$y=\log_{\frac{1}{3}}(x-2)$",
                r"$y=\log_3 \sqrt{x}$",
            ),
            answer="⑤",
            solution=_q(
                r"""
                \[
                y=\left(\frac{1}{3}\right)^x=3^{-x}
                \]
                는 $y=3^x$를 $y$축에 대하여 대칭이동한 그래프이다.

                \[
                y=3^x+2
                \]
                는 위로 평행이동한 그래프이다.

                \[
                y=\log_3 \frac{1}{x}=-\log_3 x
                \]
                는 $y=3^x$를 직선 $y=x$에 대하여 대칭이동한 뒤 다시 $x$축에 대하여 대칭이동한 그래프이다.

                \[
                y=\log_{\frac{1}{3}}(x-2)=-\log_3(x-2)
                \]
                도 대칭이동과 평행이동으로 얻을 수 있다.

                그러나
                \[
                y=\log_3 \sqrt{x}=\frac{1}{2}\log_3 x
                \]
                는 세로 방향의 확대와 축소가 필요하므로 평행이동이나 대칭이동만으로는 얻을 수 없다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=2,
            crop_box=(900, 260, 1780, 820),
            source_no=11,
            question=_q(
                r"""
                $x>0$, $y>0$일 때, $\log_4\left(x+\dfrac{1}{y}\right)+\log_4\left(y+\dfrac{9}{x}\right)$의 최솟값은?
                """
            ),
            choices=(r"$\dfrac{3}{2}$", r"$2$", r"$3$", r"$\dfrac{7}{2}$", r"$4$"),
            answer="②",
            solution=_q(
                r"""
                로그의 성질로
                \[
                \log_4\left(x+\frac{1}{y}\right)+\log_4\left(y+\frac{9}{x}\right)
                =\log_4\left\{\left(x+\frac{1}{y}\right)\left(y+\frac{9}{x}\right)\right\}
                \]
                이다.

                곱을 전개하면
                \[
                \left(x+\frac{1}{y}\right)\left(y+\frac{9}{x}\right)
                =xy+10+\frac{9}{xy}
                \]
                이다.

                $xy>0$이므로 산술평균과 기하평균의 관계에 의해
                \[
                xy+\frac{9}{xy}\ge 2\sqrt{9}=6
                \]
                이다.

                따라서
                \[
                xy+10+\frac{9}{xy}\ge 16
                \]
                이므로 최솟값은
                \[
                \log_4 16=2
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=2,
            crop_box=(900, 790, 1780, 1420),
            source_no=12,
            question=_q(
                r"""
                불순물을 포함한 어떤 물질이 여과기를 한 번 통과할 때마다 통과하기 전 불순물의 양의 $80\%$가 제거된다고 한다. 이 물질에 포함된 불순물의 양이 처음 불순물의 양의 $0.16\%$ 이하가 되도록 하려면 최소 몇 번 통과시켜야 하는가?
                """
            ),
            choices=("1번", "2번", "3번", "4번", "5번"),
            answer="④",
            solution=_q(
                r"""
                한 번 통과할 때마다 불순물의 양은 처음의
                \[
                1-0.8=0.2
                \]
                배가 된다.

                $n$번 통과시킨 뒤의 불순물의 양이 처음의 $0.16\%=0.0016$배 이하가 되어야 하므로
                \[
                (0.2)^n\le 0.0016
                \]
                이어야 한다.

                그런데
                \[
                (0.2)^4=0.0016
                \]
                이므로 최소 횟수는 $4$번이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        obj(
            page_no=2,
            crop_box=(900, 1400, 1780, 2460),
            source_no=13,
            question=_q(
                rf"""
                $\sin \theta \tan \theta <0$, $\cos \theta \tan \theta >0$을 만족시키는 각 $\theta$에 대하여 <보기>에서 옳은 것만을 있는 대로 고른 것은?

                {_box([
                    "<strong>&lt;보기&gt;</strong>",
                    r"ㄱ. $\sin \theta+\cos \theta>0$",
                    r"ㄴ. $\sin \theta-\tan \theta>0$",
                    r"ㄷ. $\cos \theta+\tan \theta<0$",
                ])}
                """
            ),
            choices=("ㄱ", "ㄴ", "ㄴ, ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"),
            answer="③",
            solution=_q(
                r"""
                \[
                \sin \theta \tan \theta
                =\sin \theta\cdot \frac{\sin \theta}{\cos \theta}
                =\frac{\sin^2 \theta}{\cos \theta}<0
                \]
                이므로
                \[
                \cos \theta<0
                \]
                이다.

                또
                \[
                \cos \theta \tan \theta
                =\cos \theta\cdot \frac{\sin \theta}{\cos \theta}
                =\sin \theta>0
                \]
                이므로
                \[
                \sin \theta>0
                \]
                이다.

                따라서 $\theta$는 제2사분면의 각이다.

                ㄱ. 제2사분면에서 $\sin \theta+\cos \theta$는 항상 양수가 아니므로 거짓이다.

                ㄴ. $\cos \theta<0$이므로
                \[
                \sin \theta-\tan \theta
                =\sin \theta\left(1-\frac{1}{\cos \theta}\right)>0
                \]
                이다.

                ㄷ. $\cos \theta<0$이고 $\tan \theta<0$이므로
                \[
                \cos \theta+\tan \theta<0
                \]
                이다.

                따라서 옳은 것은 ㄴ, ㄷ이다.
                """
            ),
            unit_l2=ALG_L2_TRI,
            unit_l3=ALG_L3_TRI,
        ),
        obj(
            page_no=3,
            crop_box=(40, 260, 860, 1120),
            source_no=14,
            question=_q(
                r"""
                $x$에 대한 이차방정식 $x^2-2ax-a^2=0$의 두 근이 $\sin \theta$, $\cos \theta$일 때, 양수 $a$의 값은?
                """
            ),
            choices=(
                r"$\dfrac{\sqrt{6}}{6}$",
                r"$\dfrac{\sqrt{5}}{6}$",
                r"$\dfrac{1}{3}$",
                r"$\dfrac{\sqrt{3}}{6}$",
                r"$\dfrac{\sqrt{2}}{6}$",
            ),
            answer="①",
            solution=_q(
                r"""
                근과 계수의 관계에 의해
                \[
                \sin \theta+\cos \theta=2a,\qquad
                \sin \theta \cos \theta=-a^2
                \]
                이다.

                또
                \[
                \sin^2 \theta+\cos^2 \theta=1
                \]
                이므로
                \[
                (\sin \theta+\cos \theta)^2-2\sin \theta \cos \theta=1
                \]
                이다.

                따라서
                \[
                (2a)^2-2(-a^2)=1
                \]
                이고,
                \[
                6a^2=1
                \]
                이다.

                양수 $a$는
                \[
                a=\frac{\sqrt{6}}{6}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_TRI,
            unit_l3=ALG_L3_TRI,
        ),
        obj(
            page_no=3,
            crop_box=(40, 1080, 860, 1700),
            source_no=15,
            question=_q(
                r"""
                **[문항 오류 의심]** 인쇄된 식 $\dfrac{\sqrt{\sin \theta}}{\sqrt{\cos \theta}}=-\sqrt{\dfrac{\sin \theta}{\cos \theta}}$는 실수 범위에서 그대로 해석하면 정의에 충돌이 있습니다. 아래 풀이는 출제 의도에 맞추어 $\sin \theta>0$, $\cos \theta<0$인 경우로 해석합니다.

                $\dfrac{\sqrt{\sin \theta}}{\sqrt{\cos \theta}}=-\sqrt{\dfrac{\sin \theta}{\cos \theta}}$를 만족시키는 각 $\theta$에 대하여 $\sin \theta+\cos \theta=\dfrac{1}{2}$일 때, $\sin^2 \theta-\cos^2 \theta$의 값을 구하면?
                """
            ),
            choices=(
                r"$-\dfrac{\sqrt{3}}{2}$",
                r"$-\dfrac{1}{2}$",
                r"$0$",
                r"$\dfrac{\sqrt{3}}{4}$",
                r"$\dfrac{\sqrt{7}}{4}$",
            ),
            answer="⑤",
            solution=_q(
                r"""
                문항의 식은 실수 범위에서 모호하지만, 출제 의도에 맞추어
                \[
                \sin \theta>0,\qquad \cos \theta<0
                \]
                로 해석하면 된다.

                \[
                \sin \theta+\cos \theta=\frac{1}{2}
                \]
                이므로
                \[
                (\sin \theta+\cos \theta)^2
                =\sin^2 \theta+2\sin \theta \cos \theta+\cos^2 \theta
                \]
                에서
                \[
                \frac{1}{4}=1+2\sin \theta \cos \theta
                \]
                이다.

                따라서
                \[
                \sin \theta \cos \theta=-\frac{3}{8}
                \]
                이다.

                이제
                \[
                (\sin \theta-\cos \theta)^2
                =1-2\sin \theta \cos \theta
                =1+\frac{3}{4}
                =\frac{7}{4}
                \]
                이므로
                \[
                \sin \theta-\cos \theta=\frac{\sqrt{7}}{2}
                \]
                이다.

                따라서
                \[
                \sin^2 \theta-\cos^2 \theta
                =(\sin \theta+\cos \theta)(\sin \theta-\cos \theta)
                =\frac{1}{2}\cdot \frac{\sqrt{7}}{2}
                =\frac{\sqrt{7}}{4}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_TRI,
            unit_l3=ALG_L3_TRI,
            note="인쇄된 제곱근 조건이 실수 범위에서 모호하여 출제 의도에 맞춰 풀이함",
        ),
        sub(
            page_no=3,
            crop_box=(40, 1680, 860, 2050),
            source_no=1,
            question=_q(
                r"""
                $\sqrt[4]{25}\times \sqrt[3]{\dfrac{1}{4}}\div \left(4^{\frac{1}{3}}\times 25^{-\frac{1}{2}}\right)^{\frac{1}{2}}$의 값을 구하시오.
                """
            ),
            answer=r"$\dfrac{5}{2}$",
            solution=_q(
                r"""
                \[
                \sqrt[4]{25}=5^{1/2},\qquad
                \sqrt[3]{\frac{1}{4}}=2^{-2/3}
                \]
                이고,
                \[
                \left(4^{1/3}\times 25^{-1/2}\right)^{1/2}
                =\left(2^{2/3}\times 5^{-1}\right)^{1/2}
                =2^{1/3}5^{-1/2}
                \]
                이다.

                따라서 구하는 값은
                \[
                \frac{5^{1/2}\cdot 2^{-2/3}}{2^{1/3}5^{-1/2}}
                =5\cdot 2^{-1}
                =\frac{5}{2}
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        sub(
            page_no=3,
            crop_box=(40, 1980, 860, 2460),
            source_no=2,
            question=_q(
                r"""
                $\log 5.2=0.716$일 때, $\log a=2.716$, $\log b=-0.284$를 만족하는 양의 실수 $a$, $b$에 대하여 $a+100b$의 값을 구하시오.
                """
            ),
            answer=r"$572$",
            solution=_q(
                r"""
                \[
                \log a=2.716=2+0.716=\log 100+\log 5.2=\log 520
                \]
                이므로
                \[
                a=520
                \]
                이다.

                또
                \[
                \log b=-0.284=0.716-1=\log 5.2-\log 10=\log 0.52
                \]
                이므로
                \[
                b=0.52
                \]
                이다.

                따라서
                \[
                a+100b=520+52=572
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        sub(
            page_no=3,
            crop_box=(900, 260, 1780, 1320),
            source_no=3,
            question=_q(
                r"""
                모든 실수 $x$에 대하여 부등식 $9^x-2k\times 3^x+4\ge 0$이 성립하도록 할 때, 실수 $k$의 최댓값을 구하시오.
                """
            ),
            answer=r"$2$",
            solution=_q(
                r"""
                \[
                t=3^x
                \]
                라 두면 $t>0$이고, 주어진 부등식은
                \[
                t^2-2kt+4\ge 0
                \]
                이다.

                이 식이 모든 $t>0$에 대하여 성립해야 한다.

                $k\ge 0$이면 꼭짓점의 $t$좌표는 $t=k$이고, 이때 최솟값은
                \[
                4-k^2
                \]
                이므로
                \[
                4-k^2\ge 0
                \]
                이어야 한다. 따라서
                \[
                0\le k\le 2
                \]
                이다.

                $k<0$이면 꼭짓점이 $t<0$에 있으므로 $t>0$에서 최솟값은 $t\to 0^+$일 때의 $4$에 가깝고 항상 양수이다.

                따라서 가능한 $k$는 모두
                \[
                k\le 2
                \]
                이고, 최댓값은
                \[
                2
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        sub(
            page_no=3,
            crop_box=(820, 900, 1800, 1800),
            source_no=4,
            question=_q(
                r"""
                $x$에 대한 로그부등식
                \[
                \log_3(x-1)\le \log_3\left(\frac{1}{2}x+k\right)
                \]
                를 만족시키는 모든 정수 $x$의 개수가 $5$일 때, 자연수 $k$의 값을 구하시오.
                """
            ),
            answer=r"$2$",
            solution=_q(
                r"""
                밑이 $3$으로 $1$보다 크므로
                \[
                x-1\le \frac{1}{2}x+k
                \]
                와 동치이다.

                정의역 조건은
                \[
                x-1>0,\qquad \frac{1}{2}x+k>0
                \]
                이다. 자연수 $k$에 대하여 두 번째 조건은 $x>1$보다 약하다.

                따라서
                \[
                x>1,\qquad x\le 2k+2
                \]
                이다.

                정수해는
                \[
                2,3,\ldots,2k+2
                \]
                이므로 개수는
                \[
                (2k+2)-2+1=2k+1
                \]
                이다.

                이것이 $5$이므로
                \[
                2k+1=5
                \]
                에서
                \[
                k=2
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
        sub(
            page_no=3,
            crop_box=(860, 1750, 1800, 2520),
            source_no=5,
            question=_q(
                r"""
                두 집합
                \[
                A=\left\{x\mid 2^{2x}+2^{x+2}-32<0\right\},\qquad
                B=\left\{x\mid (\log_2 x)^2-a\log_2 x+b\le 0\right\}
                \]
                에 대하여 $A\cap B=\varnothing$, $A\cup B=\{x\mid x\le 128\}$을 만족시킬 때, $a+b$의 값을 구하시오. (단, $a$, $b$는 상수이다.)
                """
            ),
            answer=r"$15$",
            solution=_q(
                r"""
                먼저 집합 $A$를 구하자.
                \[
                t=2^x\quad (t>0)
                \]
                라 두면
                \[
                t^2+4t-32<0
                \iff (t-4)(t+8)<0
                \]
                이다.

                $t>0$이므로
                \[
                0<t<4
                \]
                이고,
                \[
                x<2
                \]
                이다. 따라서
                \[
                A=\{x\mid x<2\}
                \]
                이다.

                또
                \[
                A\cap B=\varnothing,\qquad A\cup B=\{x\mid x\le 128\}
                \]
                이므로
                \[
                B=\{x\mid 2\le x\le 128\}
                \]
                이어야 한다.

                \[
                y=\log_2 x
                \]
                라 두면 $2\le x\le 128$은
                \[
                1\le y\le 7
                \]
                과 같다.

                따라서
                \[
                y^2-ay+b\le 0
                \]
                의 해가 $1\le y\le 7$이 되어야 하므로
                \[
                y^2-ay+b=(y-1)(y-7)=y^2-8y+7
                \]
                이다.

                따라서
                \[
                a=8,\qquad b=7
                \]
                이고,
                \[
                a+b=15
                \]
                이다.
                """
            ),
            unit_l2=ALG_L2_EXP,
            unit_l3=ALG_L3_EXP,
        ),
    ]
)


EXAMS: List[ExamSpec] = [
    ExamSpec(
        label="SY-2022-G2-S1-MID-ALG",
        school="SY",
        year=2022,
        grade=2,
        semester=1,
        exam="MID",
        subject="ALG",
        unit_l1=ALG_L1,
        source_pdf="SY.2022.G2.S1.MID.ALG.pdf",
        rows=ALG_ROWS,
    ),
    ExamSpec(
        label="SY-2022-G2-S1-MID2-STAT",
        school="SY",
        year=2022,
        grade=2,
        semester=1,
        exam="MID2",
        subject="STAT",
        unit_l1=STAT_L1,
        source_pdf="SY.2022.G2.S1.MID2.STAT.pdf",
        rows=STAT_ROWS,
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


def _render_rotated_crop(
    doc: fitz.Document,
    page_no: int,
    crop_box: Tuple[int, int, int, int],
    out_path: Path,
) -> None:
    page = doc.load_page(page_no - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(PIXEL_SCALE, PIXEL_SCALE), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    rotated = img.rotate(90, expand=True)
    rotated.crop(crop_box).save(out_path)


def _build_problem_md(
    spec: ExamSpec,
    row: ProblemRow,
    problem_id: str,
    assets: Sequence[str],
    level: int,
) -> str:
    unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
        spec.unit_l1,
        row.unit_l2,
        row.unit_l3,
        grade=spec.grade,
    )
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
            f"과목-{spec.subject}",
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
            _render_rotated_crop(doc, row.page_no, row.crop_box, original_dir / original_name)

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

            unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
                spec.unit_l1,
                row.unit_l2,
                row.unit_l3,
                grade=spec.grade,
            )
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
