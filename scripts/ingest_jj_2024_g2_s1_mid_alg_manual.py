from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import shutil
import sys
from typing import Dict, List, Tuple

import fitz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
SOURCE_PDF = ROOT / "db" / "original" / "JJ.2024.G2.S1.MID1.ALG.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

UNIT_L1 = "대수(2022개정)"
UNIT_L2_MAP = {"1": "1. 지수함수와 로그함수", "2": "2. 삼각함수"}
UNIT_L3_MAP: Dict[int, str] = {
    1: "1-1. 지수와 로그",
    2: "1-1. 지수와 로그",
    3: "1-1. 지수와 로그",
    4: "1-1. 지수와 로그",
    5: "1-1. 지수와 로그",
    6: "1-2. 지수함수",
    7: "1-1. 지수와 로그",
    8: "1-3. 로그함수",
    9: "1-2. 지수함수",
    10: "1-3. 로그함수",
    11: "2-1. 삼각함수",
    12: "2-1. 삼각함수",
    13: "2-1. 삼각함수",
    14: "2-2. 삼각함수의 그래프",
    15: "2-1. 삼각함수",
    16: "1-1. 지수와 로그",
    17: "1-1. 지수와 로그",
    18: "2-3. 삼각함수의 활용",
    19: "1-1. 지수와 로그",
    20: "2-3. 삼각함수의 활용",
    21: "2-3. 삼각함수의 활용",
}

SCAN_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    10: (2, (515, 70, 708, 170)),
    11: (2, (515, 315, 705, 430)),
    14: (3, (210, 335, 352, 500)),
}

UNCERTAIN: Dict[int, str] = {
    10: "그림 기반 문자 배치 검수 권장",
}


@dataclass(frozen=True)
class Entry:
    exam_no: int
    qtype: str
    q: str
    choices: List[str]
    answer: str
    solution: str


def box(lines: List[str]) -> str:
    return '<div style="border:1px solid #000; padding:8px; margin:8px 0;">' + "<br/>".join(lines) + "</div>"


ENTRIES: List[Entry] = [
    Entry(
        1,
        "객관식",
        r"$a=\left(2^{\sqrt{3}}\right)^{3-\sqrt{3}},\ b=\left(2^{3+\sqrt{3}}\right)^{\sqrt{3}}$일 때, $\dfrac{a}{b}$의 값은?",
        [r"$\dfrac18$", r"$\dfrac1{16}$", r"$\dfrac1{32}$", r"$\dfrac1{64}$", r"$\dfrac1{128}$"],
        "④",
        (
            r"지수법칙을 이용하면"
            "\n$$\n"
            r"a=\left(2^{\sqrt{3}}\right)^{3-\sqrt{3}}=2^{\sqrt{3}(3-\sqrt{3})}=2^{3\sqrt{3}-3}"
            "\n$$\n"
            r"이고"
            "\n$$\n"
            r"b=\left(2^{3+\sqrt{3}}\right)^{\sqrt{3}}=2^{(3+\sqrt{3})\sqrt{3}}=2^{3\sqrt{3}+3}"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"\frac{a}{b}=2^{(3\sqrt{3}-3)-(3\sqrt{3}+3)}=2^{-6}=\frac{1}{64}"
            "\n$$\n"
            r"이므로 정답은 ④이다."
        ),
    ),
    Entry(
        2,
        "객관식",
        r"자연수 $n\;(n\ge2)$에 대하여 실수 $m$의 $n$제곱근 중에서 서로 다른 실수의 개수를 $f(m,n)$이라 할 때, $f(-2,2)+f(-1,3)+f(0,4)+f(1,5)+f(2,6)$의 값은?",
        ["3", "4", "5", "6", "7"],
        "③",
        (
            r"$f(-2,2)=0$, $f(-1,3)=1$, $f(0,4)=1$, $f(1,5)=1$, $f(2,6)=2$이다."
            "\n$$\n0+1+1+1+2=5\n$$"
        ),
    ),
    Entry(
        3,
        "객관식",
        r"$\log_3\left(2-\dfrac12\right)+\log_3\left(2-\dfrac23\right)+\log_3\left(2-\dfrac34\right)+\cdots+\log_3\left(2-\dfrac{52}{53}\right)$의 값은?",
        ["1", "2", "3", "4", "5"],
        "③",
        (
            r"각 항의 진수는 $\dfrac32,\dfrac43,\dfrac54,\ldots,\dfrac{54}{53}$이므로"
            "\n$$\n"
            r"\log_3\left(\frac32\cdot\frac43\cdot\frac54\cdots\frac{54}{53}\right)=\log_3 27=3"
            "\n$$"
        ),
    ),
    Entry(
        4,
        "객관식",
        r"$\log_4\{\log_3(\log_2 x)\}=0$을 만족시키는 $x$의 값은?",
        ["1", "2", "4", "8", "16"],
        "④",
        (
            r"$\log_4 A=0$이면 $A=1$이므로"
            "\n$$\n"
            r"\log_3(\log_2 x)=1 \Rightarrow \log_2 x=3 \Rightarrow x=8"
            "\n$$"
        ),
    ),
    Entry(
        5,
        "객관식",
        r"어느 출판사는 도서 판매량을 6개월에 $7\%$씩 증가시키려는 목표를 가지고 있다. 15년 후 도서 판매량은 현재 도서 판매량의 몇 배인가? (단, $\log 1.07=0.03$, $\log 2=0.3$)",
        ["3", "4", "5", "7", "8"],
        "⑤",
        (
            r"15년은 6개월 단위로 30번이므로 배수는 $(1.07)^{30}$이다."
            "\n"
            r"로그를 취하면"
            "\n$$\n"
            r"\log(1.07)^{30}=30\cdot 0.03=0.9"
            "\n$$\n"
            r"이다."
            "\n"
            r"$\log 8=3\log 2=0.9$이므로 $(1.07)^{30}=8$이다."
        ),
    ),
    Entry(
        6,
        "객관식",
        r"함수 $f(x)=a^{-x^2+2x+1}\;(a>0,\;a\ne1)$의 최댓값이 $4$일 때, $f(a)$의 값은?",
        ["1", "2", "3", "4", "5"],
        "②",
        (
            r"$-x^2+2x+1=-(x-1)^2+2$의 최댓값은 $2$이다."
            "\n"
            r"최댓값이 $4$로 유한하려면 $a>1$이고 $a^2=4$이므로 $a=2$이다."
            "\n$$\n"
            r"f(a)=f(2)=2^{-4+4+1}=2"
            "\n$$"
        ),
    ),
    Entry(
        7,
        "객관식",
        r"방정식 $(\log_3 x)^2-\log_3 x^3+1=0$의 두 근이 $\alpha$, $\beta$일 때 $\alpha\beta$의 값은?",
        ["1", "3", "9", "16", "27"],
        "⑤",
        (
            r"$t=\log_3 x$라 두면"
            "\n$$\n"
            r"t^2-3t+1=0"
            "\n$$\n"
            r"이다."
            "\n"
            r"두 근을 $t_1,t_2$라 하면 $t_1+t_2=3$이고, 원래 방정식의 두 근은 $3^{t_1},3^{t_2}$이므로"
            "\n$$\n"
            r"\alpha\beta=3^{t_1+t_2}=3^3=27"
            "\n$$"
        ),
    ),
    Entry(
        8,
        "객관식",
        (
            r"함수 $y=\log_2 x$의 그래프를 평행이동하거나 대칭이동하여 포갤 수 있는 함수를 <보기>에서 있는 대로 고른 것은?"
            "\n\n"
            + box(
                [
                    r"ㄱ. $y=\log_{\frac12}\dfrac{8}{x}$",
                    r"ㄴ. $y=\dfrac12\log_2(x-1)^2-1$",
                    r"ㄷ. $y=3\cdot\left(\dfrac12\right)^{x-1}-1$",
                ]
            )
        ),
        ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        "③",
        (
            r"ㄱ은 $\log_{\frac12}\dfrac{8}{x}=\log_2 x-3$이므로 평행이동으로 포갤 수 있다."
            "\n"
            r"ㄷ은 $y=\log_2 x$의 그래프를 직선 $y=x$에 대하여 대칭이동한 지수함수 그래프를 다시 평행이동한 것이므로 포갤 수 있다."
            "\n"
            r"ㄴ은 절댓값 때문에 두 갈래 그래프가 되어 원래 그래프 하나와 포개지지 않는다."
        ),
    ),
    Entry(
        9,
        "객관식",
        r"함수 $y=a^x+m\;(a>1)$의 그래프와 그 역함수의 그래프가 두 점에서 만나고, 이 두 점의 $x$좌표가 각각 $1$, $2$일 때, $am$의 값은?",
        ["-1", "1", "2", "3", "4"],
        "①",
        (
            r"교점은 직선 $y=x$ 위에 있으므로"
            "\n$$\n"
            r"a+m=1,\qquad a^2+m=2"
            "\n$$\n"
            r"이다."
            "\n"
            r"두 식을 빼면 $a^2-a=1$이므로"
            "\n$$\n"
            r"am=a(1-a)=-1"
            "\n$$"
        ),
    ),
    Entry(
        10,
        "객관식",
        (
            r"[그림 검수 필요] 오른쪽 그림은 함수 $y=\log_2 x$의 그래프와 직선 $y=x$이다. $x_3-x_1$의 값은?"
            "\n\n"
            '<img src="assets/scan.png" alt="로그함수와 직선" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        ["1", "2", "3", "4", "5"],
        "③",
        r"원본 그림의 표시를 따르면 $x_3-x_1=3$이다. 문자 배치는 원본 그림 검수를 권장한다.",
    ),
    Entry(
        11,
        "객관식",
        (
            r"오른쪽 그림과 같이 밑면의 반지름의 길이가 $2$, 모선의 길이가 $6$인 원뿔의 겉넓이는?"
            "\n\n"
            '<img src="assets/scan.png" alt="원뿔" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        [r"$13\pi$", r"$14\pi$", r"$15\pi$", r"$16\pi$", r"$17\pi$"],
        "④",
        (
            r"원뿔의 겉넓이는 밑면의 넓이와 옆넓이의 합이므로"
            "\n$$\n"
            r"\pi r^2+\pi rl=\pi\cdot 2^2+\pi\cdot 2\cdot 6=4\pi+12\pi=16\pi"
            "\n$$"
        ),
    ),
    Entry(
        12,
        "객관식",
        r"$\sin\theta+\cos\theta=\sqrt{2}$일 때, $\tan\theta+\dfrac{1}{\tan\theta}$의 값은?",
        ["1", "2", "3", "4", "5"],
        "②",
        (
            r"양변을 제곱하면 $\sin\theta\cos\theta=\dfrac12$이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"\tan\theta+\frac{1}{\tan\theta}=\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}=\frac{1}{1/2}=2"
            "\n$$"
        ),
    ),
    Entry(
        13,
        "객관식",
        r"$\theta$가 제3사분면의 각이고 $\tan\theta=\dfrac12$일 때, $\sin\theta+\cos\theta$의 값은?",
        [r"$-\dfrac{3\sqrt5}{5}$", r"$-\dfrac{\sqrt5}{5}$", r"$\dfrac{\sqrt5}{5}$", r"$\dfrac{2\sqrt5}{5}$", r"$\dfrac{3\sqrt5}{5}$"],
        "①",
        (
            r"제3사분면에서 $\tan\theta=\dfrac12$이므로"
            "\n$$\n"
            r"\sin\theta=-\frac{1}{\sqrt5},\qquad \cos\theta=-\frac{2}{\sqrt5}"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"\sin\theta+\cos\theta=-\frac{3}{\sqrt5}=-\frac{3\sqrt5}{5}"
            "\n$$"
        ),
    ),
    Entry(
        14,
        "객관식",
        (
            r"함수 $y=a\cos(bx+c\pi)+d$의 그래프가 다음 그림과 같을 때, 상수 $a$, $b$, $c$, $d$에 대하여 $\dfrac{ab}{cd}$의 값은? "
            r"(단, $a>0$, $b>0$, $-1<c<0$)"
            "\n\n"
            '<img src="assets/scan.png" alt="삼각함수 그래프" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        ["-6", "-3", "1", "3", "6"],
        "⑤",
        (
            r"원본 정답지의 그래프 판독값은 $a=3$, $b=2$, $c=-\dfrac12$, $d=-2$이다."
            "\n$$\n"
            r"\frac{ab}{cd}=\frac{3\cdot 2}{\left(-\frac12\right)(-2)}=6"
            "\n$$"
        ),
    ),
    Entry(
        15,
        "객관식",
        r"각 $\theta$를 나타내는 동경과 $5\theta$를 나타내는 동경이 $y$축 대칭일 때, 각 $\theta$의 크기는? (단, $\dfrac{\pi}{2}<\theta<\pi$)",
        [r"$\dfrac{2\pi}{3}$", r"$\dfrac{3\pi}{4}$", r"$\dfrac{4\pi}{5}$", r"$\dfrac{5\pi}{6}$", r"$\dfrac{6\pi}{7}$"],
        "④",
        (
            r"$y$축 대칭인 두 동경의 각의 크기는 합이 $\pi$가 되므로"
            "\n$$\n"
            r"5\theta=\pi-\theta+2n\pi"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"6\theta=(2n+1)\pi"
            "\n$$\n"
            r"이고 $\dfrac{\pi}{2}<\theta<\pi$를 만족시키려면 $6\theta=5\pi$이므로"
            "\n$$\n"
            r"\theta=\frac{5\pi}{6}"
            "\n$$"
        ),
    ),
    Entry(
        16,
        "단답형",
        r"두 수 $\sqrt{3m}$, $\sqrt[3]{4m}$이 모두 자연수가 되도록 하는 자연수 $m$의 최솟값을 구하시오.",
        [],
        r"$432$",
        (
            r"$m=2^a3^b$라 두면 $3m$이 제곱수여야 하므로 $a$는 짝수, $b+1$은 짝수여야 한다."
            "\n"
            r"또 $4m$이 세제곱수여야 하므로 $a+2$, $b$가 모두 $3$의 배수여야 한다."
            "\n"
            r"이를 만족하는 가장 작은 값은 $a=4$, $b=3$이므로"
            "\n$$\n"
            r"m=2^4\cdot 3^3=432"
            "\n$$"
        ),
    ),
    Entry(
        17,
        "단답형",
        r"$a>1$, $b>1$일 때, $\left(\log_a a^2b^3\right)\left(\log_b a^3b^2\right)$의 최솟값을 구하시오.",
        [],
        r"$25$",
        (
            r"$t=\log_a b$라 두면 $t>0$이고"
            "\n$$\n"
            r"\log_a a^2b^3=2+3t,\qquad \log_b a^3b^2=2+\frac{3}{t}"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 곱은"
            "\n$$\n"
            r"(2+3t)\left(2+\frac{3}{t}\right)=13+6\left(t+\frac1t\right)"
            "\n$$\n"
            r"이고, $t+\dfrac1t\ge2$이므로 최솟값은 $25$이다."
        ),
    ),
    Entry(
        18,
        "단답형",
        r"$0<x<2\pi$일 때, 방정식 $3|\cos x|^2-4|\cos x|+1=0$의 모든 해의 합을 구하시오.",
        [],
        r"$5\pi$",
        (
            r"$u=|\cos x|$라 두면"
            "\n$$\n"
            r"3u^2-4u+1=0 \Rightarrow (3u-1)(u-1)=0"
            "\n$$\n"
            r"이므로 $u=1$ 또는 $u=\dfrac13$이다."
            "\n"
            r"$|\cos x|=1$의 해는 $x=\pi$, $|\cos x|=\dfrac13$의 해는 네 개이고 그 합은 $4\pi$이다."
            "\n$$\n"
            r"\pi+4\pi=5\pi"
            "\n$$"
        ),
    ),
    Entry(
        19,
        "서술형",
        r"[오류문항] 거듭제곱근의 정의에 의하여 $n$은 $2$ 이상의 자연수여야 하므로 오류문항이다. 1이 아닌 양수 $a$, $b$, $c$에 대하여 $\sqrt[a]{\sqrt[b]{\sqrt[c]{2}}}=2$일 때, $\log_a b+\log_b a+\log_a c+\log_c a+\log_b c+\log_c b$의 값을 구하시오.",
        [],
        r"오류문항",
        r"거듭제곱근의 정의에 의하여 $n$은 $2$ 이상의 자연수여야 하므로 오류문항이다.",
    ),
    Entry(
        20,
        "서술형",
        r"함수 $y=\cos^2\left(\dfrac{\pi}{2}+x\right)+\sin(\pi+x)$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $Mm$의 값을 구하시오.",
        [],
        r"$-\dfrac12$",
        (
            r"$\cos\left(\dfrac{\pi}{2}+x\right)=-\sin x$, $\sin(\pi+x)=-\sin x$이므로"
            "\n$$\n"
            r"y=\sin^2 x-\sin x"
            "\n$$\n"
            r"이다."
            "\n"
            r"$t=\sin x$라 두면 $-1\le t\le1$에서"
            "\n$$\n"
            r"y=t^2-t=\left(t-\frac12\right)^2-\frac14"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 $m=-\dfrac14$, $M=2$이므로"
            "\n$$\n"
            r"Mm=2\cdot\left(-\frac14\right)=-\frac12"
            "\n$$"
        ),
    ),
    Entry(
        21,
        "서술형",
        r"$-\dfrac{\pi}{2}<x<\dfrac{\pi}{2}$일 때, 부등식 $\tan^2 x+(\sqrt{3}-1)\tan x-\sqrt{3}<0$의 해는 $\beta<x<\alpha$이다. 이때, $\alpha-\beta=\dfrac{p}{q}\pi$일 때, $p+q$의 값을 구하시오. (단, $p$, $q$는 서로소인 자연수이다.)",
        [],
        r"$19$",
        (
            r"$t=\tan x$라 두면"
            "\n$$\n"
            r"t^2+(\sqrt3-1)t-\sqrt3<0"
            "\n$$\n"
            r"이다."
            "\n"
            r"이를 인수분해하면"
            "\n$$\n"
            r"(t-1)(t+\sqrt3)<0"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"-\sqrt3<t<1"
            "\n$$\n"
            r"이다."
            "\n"
            r"$-\dfrac{\pi}{2}<x<\dfrac{\pi}{2}$에서 $\tan x$는 증가하므로"
            "\n$$\n"
            r"-\frac{\pi}{3}<x<\frac{\pi}{4}"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"\alpha-\beta=\frac{\pi}{4}-\left(-\frac{\pi}{3}\right)=\frac{7\pi}{12}"
            "\n$$\n"
            r"이므로 $p+q=19$이다."
        ),
    ),
]


def parse_meta() -> dict:
    return {"school": "JJ", "year": 2024, "grade": 2, "semester": 1, "exam": "MID", "subject": "ALG"}


def id_info(exam_no: int) -> Tuple[int, int, str, str]:
    if exam_no <= 15:
        return exam_no, exam_no, "objective", str(exam_no)
    source_no = exam_no - 15
    return 100 + source_no, source_no, "subjective", f"서답{source_no}번"


def export_crop(doc: fitz.Document, page_no: int, rect_vals: Tuple[float, float, float, float], out_path: Path) -> None:
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(*rect_vals), alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "")


def unit_triplet(exam_no: int) -> Tuple[str, str, str]:
    unit_l3 = UNIT_L3_MAP[exam_no]
    return UNIT_L1, UNIT_L2_MAP[unit_l3[0]], unit_l3


def build_markdown(
    *,
    pid: str,
    meta: dict,
    entry: Entry,
    source_no: int,
    source_kind: str,
    source_label: str,
    level: int,
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    original_asset_name: str,
    has_scan: bool,
) -> str:
    assets = []
    if has_scan:
        assets.append("assets/scan.png")
    assets.extend(["assets/original/", f"assets/original/{original_asset_name}"])
    lines = [
        "---",
        f"id: {pid}",
        f"school: {meta['school']}",
        f"year: {meta['year']}",
        f"grade: {meta['grade']}",
        f"semester: {meta['semester']}",
        f"exam: {meta['exam']}",
        f"subject: {meta['subject']}",
        f"type: {entry.qtype}",
        f"source_question_no: {source_no}",
        f"source_question_kind: {source_kind}",
        f"source_question_label: '{source_label}'",
        f"difficulty: {level}",
        f"level: {level}",
        f"unit: {unit_l1}>{unit_l2}>{unit_l3}",
        f"unit_l1: {unit_l1}",
        f"unit_l2: {unit_l2}",
        f"unit_l3: {unit_l3}",
        f"source: {SOURCE_TAG}",
        "tags:",
        "- 수동작성",
        "- PDF",
        f"- {entry.qtype}",
        f"- 출제번호-{source_label}",
        "- 과목-대수",
        "assets:",
    ]
    for asset in assets:
        lines.append(f"- {asset}")
    lines.extend(["---", "", "## Q", entry.q.strip(), "", "## Choices"])
    if entry.choices:
        for mark, choice in zip(["①", "②", "③", "④", "⑤"], entry.choices):
            lines.append(f"{mark} {choice}")
    lines.extend(["", "## Answer", entry.answer.strip(), "", "## Solution", entry.solution.strip(), ""])
    return "\n".join(lines)


def process(rewrite_existing: bool = False) -> None:
    meta = parse_meta()
    prefix = f"{meta['school']}-{meta['year']}-G{meta['grade']}-S{meta['semester']}-{meta['exam']}-{meta['subject']}"
    doc = fitz.open(SOURCE_PDF)
    created: List[str] = []
    updated: List[str] = []
    skipped_duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    results: List[Tuple[str, str, str]] = []
    review_paths: List[str] = []

    for entry in ENTRIES:
        pid_no, source_no, source_kind, source_label = id_info(entry.exam_no)
        pid = f"{prefix}-{pid_no:03d}"
        pdir = PROBLEMS / pid
        md_path = pdir / "problem.md"
        review_paths.append(str(md_path.resolve()))
        existed = pdir.exists()
        if existed and not rewrite_existing:
            skipped_duplicates.append(pid)
            results.append((pid, "SKIPPED_DUPLICATE", "existing folder kept as-is"))
            continue

        pdir.mkdir(parents=True, exist_ok=True)
        assets_original = pdir / "assets" / "original"
        assets_original.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_PDF, assets_original / SOURCE_PDF.name)

        has_scan = entry.exam_no in SCAN_CROPS
        scan_path = pdir / "assets" / "scan.png"
        if has_scan:
            page_no, rect_vals = SCAN_CROPS[entry.exam_no]
            export_crop(doc, page_no, rect_vals, scan_path)
        elif scan_path.exists():
            scan_path.unlink()

        cls = classify_unit_and_level(
            question_text=strip_html(entry.q),
            choices_text="\n".join(entry.choices),
            answer_text=entry.answer,
            solution_text=entry.solution,
            qtype=entry.qtype,
            grade=meta["grade"],
            problem_no=pid_no,
        )
        unit_l1, unit_l2, unit_l3 = unit_triplet(entry.exam_no)
        level = cls.level

        md_path.write_text(
            build_markdown(
                pid=pid,
                meta=meta,
                entry=entry,
                source_no=source_no,
                source_kind=source_kind,
                source_label=source_label,
                level=level,
                unit_l1=unit_l1,
                unit_l2=unit_l2,
                unit_l3=unit_l3,
                original_asset_name=SOURCE_PDF.name,
                has_scan=has_scan,
            ),
            encoding="utf-8",
            newline="\n",
        )

        if entry.exam_no in UNCERTAIN:
            uncertain.append(f"{pid}: {UNCERTAIN[entry.exam_no]}")

        if existed:
            updated.append(pid)
            results.append((pid, "UPDATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={level}"))
        else:
            created.append(pid)
            results.append((pid, "CREATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={level}"))

    doc.close()

    print("SUMMARY")
    print(f"created={len(created)}")
    print(f"updated={len(updated)}")
    print(f"skipped_duplicates={len(skipped_duplicates)}")
    print(f"warnings={len(warnings)}")
    print("")
    print("DUPLICATE_FOLDERS")
    if skipped_duplicates:
        for pid in skipped_duplicates:
            print(pid)
    else:
        print("(none)")
    print("")
    print("RESULTS")
    for pid, status, msg in results:
        print(f"{pid}\t{status}\t{msg}")
    print("")
    print("UNCERTAIN_OCR_OR_FORMULA")
    if uncertain:
        for row in uncertain:
            print(row)
    else:
        print("(none)")
    print("")
    print("WARNINGS")
    if warnings:
        for row in warnings:
            print(row)
    else:
        print("(none)")
    print("")
    print("REVIEW_PATHS")
    for path in review_paths:
        print(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual ingest for JJ 2024 G2 S1 MID ALG")
    parser.add_argument("--rewrite-existing", action="store_true")
    args = parser.parse_args()
    process(rewrite_existing=args.rewrite_existing)
