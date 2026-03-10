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
SOURCE_PDF = ROOT / "db" / "original" / "SY.2024.G2.S1.MID1.ALG.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

UNIT_L1 = "대수(2022개정)"
UNIT_L2_MAP = {"1": "1. 지수함수와 로그함수", "2": "2. 삼각함수"}
UNIT_L3_MAP: Dict[int, str] = {
    1: "1-1. 지수와 로그",
    2: "1-3. 로그함수",
    3: "2-1. 삼각함수",
    4: "1-1. 지수와 로그",
    5: "1-2. 지수함수",
    6: "2-1. 삼각함수",
    7: "1-1. 지수와 로그",
    8: "1-1. 지수와 로그",
    9: "1-1. 지수와 로그",
    10: "1-3. 로그함수",
    11: "1-2. 지수함수",
    12: "2-1. 삼각함수",
    13: "1-3. 로그함수",
    14: "1-2. 지수함수",
    15: "1-1. 지수와 로그",
    16: "2-1. 삼각함수",
    17: "1-2. 지수함수",
    18: "1-1. 지수와 로그",
    19: "1-3. 로그함수",
    20: "1-1. 지수와 로그",
}

SCAN_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    3: (1, (245, 705, 355, 825)),
    10: (2, (425, 92, 705, 270)),
}

UNCERTAIN: Dict[int, str] = {
    10: '원본 정답지에 "② or 3"으로 표기됨',
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
    body = "<br/>".join(lines)
    return '<div style="border:1px solid #000; padding:8px; margin:8px 0;">' + body + "</div>"


ENTRIES: List[Entry] = [
    Entry(
        1,
        "객관식",
        r"다음 중 옳지 않은 것은?",
        [
            r"$\sqrt[4]{27}\times\sqrt[4]{3}=3$",
            r"$\dfrac{\sqrt[3]{128}}{\sqrt[3]{2}}=4$",
            r"$3^4\times 3^{-6}=\dfrac{1}{9}$",
            r"$3\sqrt{6}+\dfrac{2}{3\sqrt{6}}=9$",
            r"$\left\{\left(\dfrac14\right)^{\sqrt{2}+1}\right\}^{\sqrt{2}-1}=\dfrac{1}{256}$",
        ],
        "⑤",
        (
            r"⑤의 왼쪽은 지수의 곱을 이용하면"
            "\n$$\n"
            r"\left(\frac14\right)^{(\sqrt2+1)(\sqrt2-1)}=\left(\frac14\right)^1=\frac14"
            "\n$$\n"
            r"이므로 $\dfrac{1}{256}$이 아니다."
        ),
    ),
    Entry(
        2,
        "객관식",
        r"다음 중 로그함수 $y=\log_3(-x+2)$의 그래프에 대한 설명으로 옳지 않은 것은?",
        [
            r"정의역은 $\{x\mid x<2\}$이다.",
            "치역은 실수 전체의 집합이다.",
            r"그래프의 점근선의 방정식은 $x=2$이다.",
            r"$y=\log_2 x$의 그래프를 $x$축에 대하여 대칭이동하고 $x$축 방향으로 $2$만큼 평행이동하여 얻어진다.",
            r"$x$의 값이 증가하면 $y$의 값은 감소한다.",
        ],
        "④",
        (
            r"$y=\log_3(-x+2)$는 $y=\log_3 x$의 그래프를 $y$축에 대하여 대칭이동한 뒤 오른쪽으로 $2$만큼 평행이동한 그래프이다."
            "\n"
            r"따라서 ④는 기준 함수의 밑과 이동 설명이 맞지 않다."
        ),
    ),
    Entry(
        3,
        "객관식",
        (
            r"시초선 $OX$와 동경 $OP$의 위치가 오른쪽 그림과 같을 때, 다음 중 동경 $OP$가 나타내는 각이 될 수 없는 것은?"
            "\n\n"
            '<img src="assets/scan.png" alt="동경 OP" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        [r"$-670^\circ$", r"$-330^\circ$", r"$-1030^\circ$", r"$410^\circ$", r"$770^\circ$"],
        "②",
        (
            r"$-670^\circ$, $-1030^\circ$, $410^\circ$, $770^\circ$는 모두 $50^\circ$와 동경이 같다."
            "\n"
            r"반면 $-330^\circ$는 $30^\circ$와 동경이 같으므로 그림의 동경과 일치하지 않는다."
        ),
    ),
    Entry(
        4,
        "객관식",
        (
            "서영여자고등학교 학생회가 축제 기간에 운영하는 먹거리 장터에서 수학 동아리가 다음과 같은 차림표를 마련하였다.\n\n"
            "| 품명 | 단위 | 가격 |\n| --- | --- | --- |\n"
            "| 영화 떡볶이 | 접시 | $1000\\times\\sqrt[3]{27}$ |\n"
            "| 세경 김밥 | 줄 | $1000\\times\\log_3 81$ |\n"
            "| 희재 튀김 | 접시 | $500\\times 6^{\\log_6 7}$ |\n"
            "| 명영 어묵 | 그릇 | $1000\\times\\log 1000$ |\n\n"
            "영화 떡볶이 1접시와 세경 김밥 1줄, 명영 어묵 1그릇을 먹었을 때 지불해야 하는 금액은?"
        ),
        ["10000원", "11000원", "12000원", "13000원", "14000원"],
        "①",
        (
            r"영화 떡볶이는 $1000\times\sqrt[3]{27}=3000$원, 세경 김밥은 $1000\times\log_3 81=4000$원, 명영 어묵은 $1000\times\log 1000=3000$원이다."
            "\n$$\n3000+4000+3000=10000\n$$"
        ),
    ),
    Entry(
        5,
        "객관식",
        r"함수 $y=2^x$의 그래프를 $x$축 방향으로 $2$만큼, $y$축의 방향으로 $m$만큼 평행이동한 그래프가 점 $(3,5)$를 지날 때, 상수 $m$의 값은?",
        ["1", r"$\dfrac32$", "2", r"$\dfrac52$", "3"],
        "⑤",
        (
            r"평행이동한 그래프의 식은 $y=2^{x-2}+m$이다."
            "\n"
            r"점 $(3,5)$를 지나므로"
            "\n$$\n"
            r"5=2^{3-2}+m=2+m"
            "\n$$\n"
            r"이어서 $m=3$이다."
        ),
    ),
    Entry(
        6,
        "객관식",
        r"호의 길이가 $3\pi$이고, 넓이가 $6\pi$인 부채꼴의 중심각의 크기는?",
        [r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{3}$", r"$\dfrac{\pi}{2}$", r"$\dfrac{2\pi}{3}$", r"$\dfrac{3\pi}{4}$"],
        "⑤",
        (
            r"호의 길이가 $3\pi$이므로 $r\theta=3\pi$이고, 넓이가 $6\pi$이므로"
            "\n$$\n"
            r"\frac12 r^2\theta=6\pi"
            "\n$$\n"
            r"이다."
            "\n"
            r"여기서 $\frac12 r(r\theta)=6\pi$에 $r\theta=3\pi$를 대입하면 $r=4$이다."
            "\n$$\n"
            r"\theta=\frac{3\pi}{4}"
            "\n$$"
        ),
    ),
    Entry(
        7,
        "객관식",
        r"$\log_{x-3}(-x^2+9x-14)$가 정의되도록 하는 정수 $x$의 값들의 합은?",
        ["11", "15", "18", "22", "25"],
        "①",
        (
            r"밑에 대하여 $x-3>0$, $x-3\ne1$이어야 하고, 진수에 대하여 $-x^2+9x-14>0$이어야 한다."
            "\n"
            r"$-x^2+9x-14>0$은 $(x-7)(x-2)<0$과 같으므로 $2<x<7$이다."
            "\n"
            r"이를 모두 합치면 $3<x<7$, $x\ne4$이므로 가능한 정수는 $5,6$이다."
            "\n$$\n5+6=11\n$$"
        ),
    ),
    Entry(
        8,
        "객관식",
        r"두 양수 $x$, $y$가 $\log_2(3x+2y)=4$, $\log_2 x+\log_2 y=3$을 만족시킬 때, $9x^2+4y^2$의 값은?",
        ["60", "128", "160", "180", "256"],
        "③",
        (
            r"$3x+2y=16$, $xy=8$이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"9x^2+4y^2=(3x+2y)^2-12xy=16^2-12\cdot 8=160"
            "\n$$"
        ),
    ),
    Entry(
        9,
        "객관식",
        r"부등식 $3^{x-8}>\left(\dfrac{1}{27}\right)^x$를 만족시키는 실수 $x$의 값의 범위는?",
        [r"$x>2$", r"$x>4$", r"$x<2$", r"$x<4$", r"$2<x<4$"],
        "①",
        (
            r"$\left(\dfrac{1}{27}\right)^x=3^{-3x}$이므로"
            "\n$$\n"
            r"3^{x-8}>3^{-3x}"
            "\n$$\n"
            r"이다."
            "\n"
            r"밑이 $3>1$이므로 지수끼리 비교하면"
            "\n$$\n"
            r"x-8>-3x \Rightarrow 4x>8 \Rightarrow x>2"
            "\n$$"
        ),
    ),
    Entry(
        10,
        "객관식",
        (
            r"[정답지 표기 검수 필요] 원본 정답지에 `② or 3`으로 표기되어 있다."
            "\n\n"
            r"다음 그림은 함수 $y=2^x$, $y=\log_2 x$의 그래프와 직선 $y=x$이다. $a$, $b$, $c$의 곱인 $abc$의 값은? "
            r"(단, $a$, $b$, $c$는 상수)"
            "\n\n"
            '<img src="assets/scan.png" alt="지수함수와 로그함수의 그래프" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        [r"$-\sqrt{3}$", r"$-\sqrt{2}$", "1", r"$\sqrt{2}$", r"$\sqrt{3}$"],
        "② 또는 ③",
        (
            r"원본 정답지의 표기가 `② or 3`으로 남아 있어 그래프의 문자 배치에 대한 원본 검수가 필요하다."
            "\n"
            r"현재 DB에는 원본 정답지 표기를 그대로 반영하였다."
        ),
    ),
    Entry(
        11,
        "객관식",
        r"함수 $f(x)=4^x-2^{x+2}+a$가 $x=b$에서 최솟값 $2$를 가질 때, 상수 $a$, $b$의 합 $a+b$의 값은?",
        ["6", "7", "8", "9", "10"],
        "②",
        (
            r"$t=2^x$라 두면 $t>0$이고"
            "\n$$\n"
            r"f(x)=t^2-4t+a=(t-2)^2+a-4"
            "\n$$\n"
            r"이다."
            "\n"
            r"최솟값이 $2$이므로 $a-4=2$, 즉 $a=6$이고, 이때 $t=2$이므로 $x=1$이다."
            "\n"
            r"따라서 $a+b=6+1=7$이다."
        ),
    ),
    Entry(
        12,
        "객관식",
        r"반지름의 길이가 $r$이고 중심각의 크기가 $\theta\;(0<\theta<\dfrac{2\pi}{3})$인 부채꼴이 있다. 이 부채꼴의 중심각의 크기를 $3$배, 반지름의 길이를 $\dfrac12$배 하였을 때, 호의 길이는 $a$배, 넓이는 $b$배가 된다. $a\times b=\dfrac{p}{q}$일 때, $p+q$의 값은? (단, $p$, $q$는 서로소인 자연수)",
        ["11", "13", "17", "25", "35"],
        "③",
        (
            r"호의 길이는 $r\theta$에 비례하므로"
            "\n$$\n"
            r"a=\frac{\frac12 r\cdot 3\theta}{r\theta}=\frac32"
            "\n$$\n"
            r"이다."
            "\n"
            r"넓이는 $\frac12 r^2\theta$에 비례하므로"
            "\n$$\n"
            r"b=\frac{\frac12\left(\frac12 r\right)^2\cdot 3\theta}{\frac12 r^2\theta}=\frac34"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"a b=\frac32\cdot \frac34=\frac98"
            "\n$$\n"
            r"이므로 $p+q=17$이다."
        ),
    ),
    Entry(
        13,
        "객관식",
        r"1보다 큰 양수 $a$에 대하여 두 곡선 $y=a^{-x-2}$과 $y=\log_a(x-2)$가 직선 $y=1$과 만나는 두 점을 각각 $A$, $B$라 하자. $\overline{AB}=10$일 때, $a$의 값은?",
        ["2", "4", "6", "8", "10"],
        "③",
        (
            r"$y=1$과 $y=a^{-x-2}$의 교점은 $a^{-x-2}=1$이므로 $x=-2$이다."
            "\n"
            r"또 $y=1$과 $y=\log_a(x-2)$의 교점은 $\log_a(x-2)=1$이므로 $x=a+2$이다."
            "\n"
            r"두 점은 모두 $y=1$ 위에 있으므로"
            "\n$$\n"
            r"\overline{AB}=|(a+2)-(-2)|=a+4=10"
            "\n$$\n"
            r"이다. 따라서 $a=6$이다."
        ),
    ),
    Entry(
        14,
        "객관식",
        r"두 함수 $y=2^x$, $y=-\left(\dfrac12\right)^x+k$의 그래프가 서로 다른 두 점 $A$, $B$에서 만난다. 선분 $AB$의 중점의 좌표가 $\left(0,\dfrac54\right)$일 때, 상수 $k$의 값은?",
        ["1", r"$\dfrac32$", "2", r"$\dfrac52$", "3"],
        "④",
        (
            r"교점의 $x$좌표를 $x_1$, $x_2$라 하면"
            "\n$$\n"
            r"2^x+\left(\frac12\right)^x=k"
            "\n$$\n"
            r"를 만족한다."
            "\n"
            r"이 식은 $x$와 $-x$에 대하여 같은 값을 가지므로 두 교점의 $x$좌표는 서로 부호가 반대이고, 중점의 $x$좌표가 $0$인 것과도 일치한다."
            "\n"
            r"각 교점의 $y$좌표의 합은 $k$이므로 중점의 $y$좌표는 $\dfrac{k}{2}$이다."
            "\n$$\n"
            r"\frac{k}{2}=\frac54 \Rightarrow k=\frac52"
            "\n$$"
        ),
    ),
    Entry(
        15,
        "객관식",
        r"세계 석유 소비량이 매년 $4\%$씩 감소된다고 할 때, 세계 석유 소비량이 처음으로 현재 소비량의 $\dfrac13$ 이하가 되는 것은 몇 년 후인가? (단, $\log 2=0.30$, $\log 3=0.48$, $\log 9.6=0.98$)",
        ["15년", "18년", "21년", "24년", "27년"],
        "④",
        (
            r"$0.96^n\le \dfrac13$이 되는 최소의 자연수 $n$을 구하면 된다."
            "\n"
            r"$\log 0.96=\log 9.6-2=0.98-2=-0.02$이므로"
            "\n$$\n"
            r"n(-0.02)\le -\log 3=-0.48"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"n\ge 24"
            "\n$$\n"
            r"이므로 처음으로 $\dfrac13$ 이하가 되는 것은 24년 후이다."
        ),
    ),
    Entry(
        16,
        "단답형",
        r"$\sin\theta+\cos\theta=\sqrt{2}$일 때, $\sin^3\theta+\cos^3\theta$의 값을 구하시오.",
        [],
        r"$\dfrac{\sqrt{2}}{2}$",
        (
            r"양변을 제곱하면"
            "\n$$\n"
            r"\sin^2\theta+\cos^2\theta+2\sin\theta\cos\theta=2"
            "\n$$\n"
            r"이므로 $\sin\theta\cos\theta=\dfrac12$이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"\sin^3\theta+\cos^3\theta=(\sin\theta+\cos\theta)^3-3\sin\theta\cos\theta(\sin\theta+\cos\theta)"
            r"=\frac{\sqrt2}{2}"
            "\n$$"
        ),
    ),
    Entry(
        17,
        "단답형",
        r"함수 $y=\left(\dfrac12\right)^{x-2}+k$의 그래프가 제3사분면을 지나도록 하는 정수 $k$의 최댓값을 구하시오.",
        [],
        r"$-5$",
        (
            r"제3사분면을 지나려면 어떤 $x<0$에서 $y<0$이어야 한다."
            "\n"
            r"$x<0$일 때 $\left(\dfrac12\right)^{x-2}=2^{2-x}>4$이므로"
            "\n$$\n"
            r"2^{2-x}+k<0"
            "\n$$\n"
            r"가 되려면 $k<-4$여야 한다."
            "\n"
            r"따라서 가능한 정수의 최댓값은 $-5$이다."
        ),
    ),
    Entry(
        18,
        "서술형",
        r"실수 $x$, $y$에 대하여 $27^x=2^y=6$일 때, $\dfrac{2}{x}+\dfrac{6}{y}$의 값을 풀이 과정과 함께 쓰시오.",
        [],
        r"$6$",
        (
            r"$27^x=6$이므로 $3^{3x}=6$이고, 따라서"
            "\n$$\n"
            r"x=\frac{\log_3 6}{3}"
            "\n$$\n"
            r"이다."
            "\n"
            r"또 $2^y=6$이므로"
            "\n$$\n"
            r"y=\log_2 6"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"\frac{2}{x}+\frac{6}{y}=\frac{6}{\log_3 6}+\frac{6}{\log_2 6}"
            r"=6\log_6 3+6\log_6 2=6"
            "\n$$"
        ),
    ),
    Entry(
        19,
        "서술형",
        r"정의역이 $\{x\mid 1\le x\le 243\}$인 함수 $y=(\log_3 x)(\log_{\frac13}x)+4\log_3 x+10$의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M+m$의 값을 풀이 과정과 함께 쓰시오.",
        [],
        r"$19$",
        (
            r"$t=\log_3 x$라 두면 $1\le x\le243=3^5$이므로 $0\le t\le5$이다."
            "\n"
            r"또 $\log_{\frac13}x=-t$이므로"
            "\n$$\n"
            r"y=-t^2+4t+10=-(t-2)^2+14"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 최댓값은 $t=2$일 때의 $14$이고, 최솟값은 구간 끝에서 비교하여 $t=5$일 때의 $5$이다."
            "\n$$\n"
            r"M+m=14+5=19"
            "\n$$"
        ),
    ),
    Entry(
        20,
        "서술형",
        r"부등식 $\log_3(10-x)+\log_3(10+x)<4$를 만족시키는 정수 $x$의 개수를 풀이 과정과 함께 쓰시오.",
        [],
        "10개",
        (
            r"정의역은 $-10<x<10$이다."
            "\n"
            r"로그의 성질을 이용하면"
            "\n$$\n"
            r"\log_3\{(10-x)(10+x)\}<4"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"100-x^2<3^4=81"
            r"\Rightarrow x^2>19"
            "\n$$\n"
            r"이다."
            "\n"
            r"$-10<x<10$인 정수 중 $x^2>19$를 만족하는 것은"
            "\n$$\n"
            r"\pm5,\pm6,\pm7,\pm8,\pm9"
            "\n$$\n"
            r"의 10개이다."
        ),
    ),
]


def parse_meta() -> dict:
    return {"school": "SY", "year": 2024, "grade": 2, "semester": 1, "exam": "MID", "subject": "ALG"}


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
    parser = argparse.ArgumentParser(description="Manual ingest for SY 2024 G2 S1 MID ALG")
    parser.add_argument("--rewrite-existing", action="store_true")
    args = parser.parse_args()
    process(rewrite_existing=args.rewrite_existing)
