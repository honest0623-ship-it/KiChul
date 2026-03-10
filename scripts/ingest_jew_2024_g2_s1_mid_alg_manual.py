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
SOURCE_PDF = ROOT / "db" / "original" / "JEW.2024.G2.S1.MID1.ALG.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

UNIT_L1 = "대수(2022개정)"
UNIT_L2_MAP = {"1": "1. 지수함수와 로그함수", "2": "2. 삼각함수"}
UNIT_L3_MAP: Dict[int, str] = {
    1: "1-1. 지수와 로그",
    2: "1-1. 지수와 로그",
    3: "1-1. 지수와 로그",
    4: "1-1. 지수와 로그",
    5: "1-1. 지수와 로그",
    6: "1-1. 지수와 로그",
    7: "1-2. 지수함수",
    8: "2-1. 삼각함수",
    9: "1-1. 지수와 로그",
    10: "2-1. 삼각함수",
    11: "2-1. 삼각함수",
    12: "1-1. 지수와 로그",
    13: "1-2. 지수함수",
    14: "1-1. 지수와 로그",
    15: "1-3. 로그함수",
    16: "1-3. 로그함수",
    17: "1-2. 지수함수",
    18: "1-1. 지수와 로그",
    19: "1-2. 지수함수",
    20: "1-1. 지수와 로그",
    21: "1-1. 지수와 로그",
    22: "1-1. 지수와 로그",
    23: "1-2. 지수함수",
}

SCAN_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    19: (4, (20, 460, 352, 760)),
}

UNCERTAIN: Dict[int, str] = {
    19: "그림 기반 좌표 판독 검수 필요",
    21: "문제 OCR과 정답지 값이 상충함",
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
    Entry(1, "객관식", r"$\log_5(x-1)=2$의 해를 구하면?", ["3", "10", "11", "25", "26"], "⑤", r"$x-1=5^2=25$이므로 $x=26$이다."),
    Entry(
        2,
        "객관식",
        r"$\sqrt{3\sqrt[3]{9\sqrt[4]{27}}}$을 $3^k$의 꼴로 나타내었을 때, 상수 $k$의 값을 구하면?",
        [r"$\dfrac{23}{24}$", r"$\dfrac{25}{24}$", r"$\dfrac{7}{12}$", r"$\dfrac73$", r"$\dfrac12$"],
        "①",
        (
            r"$27^{1/4}=3^{3/4}$이므로"
            "\n$$\n"
            r"\sqrt{3\sqrt[3]{9\sqrt[4]{27}}}"
            r"=\left(3\cdot (3^2\cdot 3^{3/4})^{1/3}\right)^{1/2}"
            r"=\left(3^{1+\frac{11}{12}}\right)^{1/2}=3^{23/24}"
            "\n$$"
        ),
    ),
    Entry(
        3,
        "객관식",
        r"다음 거듭제곱근에 대한 설명 중 옳은 것은?",
        [
            r"$9$의 세제곱근은 $\sqrt[3]{9}$뿐이다.",
            r"$3$의 네제곱근은 $-\sqrt[4]{3}$, $\sqrt[4]{3}$이다.",
            r"$-3$의 세제곱근 중 실수인 것은 없다.",
            r"$n$이 홀수이고 $a$가 음수일 때, $\sqrt[n]{a^n}=-a$이다.",
            r"$n$이 짝수일 때, $4$의 $n$제곱근 중 실수인 것은 $2$개다.",
        ],
        "⑤",
        (
            r"짝수 $n$에 대하여 $x^n=4$의 실근은 $x=\sqrt[n]{4}$와 $x=-\sqrt[n]{4}$의 두 개이다."
            "\n"
            r"따라서 옳은 것은 ⑤이다."
        ),
    ),
    Entry(
        4,
        "객관식",
        r"$\sqrt{(-3)^2}+\sqrt[3]{(-4)^3}+\sqrt[4]{(-5)^4}+\sqrt[5]{(-6)^5}$의 값을 구하면?",
        ["-2", "-1", "0", "1", "2"],
        "①",
        r"$3-4+5-6=-2$이다.",
    ),
    Entry(
        5,
        "객관식",
        r"부등식 $3^{3x}<9^{2x-1}$의 해를 구하면 $x>a$이다. 이때 상수 $a$의 값을 구하면?",
        ["2", "3", "4", "5", "6"],
        "①",
        (
            r"$9^{2x-1}=3^{4x-2}$이므로"
            "\n$$\n"
            r"3x<4x-2 \Rightarrow x>2"
            "\n$$\n"
            r"이다."
        ),
    ),
    Entry(
        6,
        "객관식",
        r"다음 중 옳지 않은 것은?",
        [
            r"$\log_3 5\cdot \log_5 3=1$",
            r"$2\log_2 \sqrt{6}-\log_2 \dfrac32=2$",
            r"$\log_3 \sqrt{2}+\log_3 \dfrac13-\dfrac32\log_3(\sqrt[3]{6})=\dfrac32$",
            r"$\log_2 4\cdot \log_4 5\cdot \log_5 8=3$",
            r"$2^{\log_5 3}=3^{\log_5 2}$",
        ],
        "③",
        (
            r"③의 왼쪽은"
            "\n$$\n"
            r"\frac12\log_3 2-1-\frac32\cdot \frac13\log_3 6"
            r"=\frac12\log_3 2-1-\frac12(\log_3 2+1)=-\frac32"
            "\n$$\n"
            r"이므로 옳지 않다."
        ),
    ),
    Entry(
        7,
        "객관식",
        r"정의역이 $\{x\mid -1\le x\le2\}$인 함수 $y=\left(\dfrac12\right)^{x-1}+2$의 최댓값을 $a$, 최솟값을 $b$라 할 때, $ab$의 값을 구하면?",
        [r"$\dfrac{51}{8}$", "9", r"$\dfrac{85}{8}$", "15", "20"],
        "④",
        (
            r"함수는 감소함수이므로"
            "\n$$\n"
            r"a=\left(\frac12\right)^{-2}+2=6,\qquad b=\left(\frac12\right)^1+2=\frac52"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"ab=6\cdot \frac52=15"
            "\n$$"
        ),
    ),
    Entry(
        8,
        "객관식",
        r"두 상수 $a$, $b$에 대하여 $135^\circ=a\pi$, $-70^\circ=b\pi$일 때, $ab$의 값을 구하면?",
        [r"$-\dfrac13$", r"$-\dfrac{7}{24}$", r"$-\dfrac14$", r"$-\dfrac{5}{24}$", r"$-\dfrac16$"],
        "②",
        (
            r"$a=\dfrac{135}{180}=\dfrac34$, $b=-\dfrac{70}{180}=-\dfrac{7}{18}$이므로"
            "\n$$\n"
            r"ab=-\frac{7}{24}"
            "\n$$"
        ),
    ),
    Entry(
        9,
        "객관식",
        r"부등식 $2\log_3(x+1)\le 1-\log_{\frac13}(x+7)$을 만족시키는 정수 $x$의 최솟값을 구하면?",
        ["4", "0", "-1", "-5", "-7"],
        "②",
        (
            r"$\log_{\frac13}(x+7)=-\log_3(x+7)$이므로"
            "\n$$\n"
            r"2\log_3(x+1)\le 1+\log_3(x+7)=\log_3(3x+21)"
            "\n$$\n"
            r"이다."
            "\n"
            r"$x>-1$에서 밑이 3이므로"
            "\n$$\n"
            r"(x+1)^2\le 3x+21 \Rightarrow x^2-x-20\le0"
            "\n$$\n"
            r"이고, 따라서 $-1<x\le5$이다. 정수의 최솟값은 $0$이다."
        ),
    ),
    Entry(
        10,
        "객관식",
        r"$\pi<\theta<2\pi$인 $\theta$에 대하여 $\cos\theta=-\dfrac{2}{3}$일 때, $\tan\theta$의 값은?",
        [
            r"$\dfrac{\sqrt{5}}{2}$",
            r"$\dfrac{\sqrt{5}}{3}$",
            r"$1$",
            r"$-\dfrac{\sqrt{5}}{3}$",
            r"$-\dfrac{\sqrt{5}}{2}$",
        ],
        "①",
        (
            r"$\pi<\theta<2\pi$이고 $\cos\theta<0$이므로 $\theta$는 제3사분면의 각이다."
            "\n"
            r"따라서 $\sin\theta<0$이고"
            "\n$$\n"
            r"\sin\theta=-\sqrt{1-\cos^2\theta}"
            r"\n=-\sqrt{1-\left(-\frac{2}{3}\right)^2}"
            r"\n=-\frac{\sqrt{5}}{3}"
            "\n$$\n"
            r"이다."
            "\n"
            r"그러므로"
            "\n$$\n"
            r"\tan\theta=\frac{\sin\theta}{\cos\theta}"
            r"\n=\frac{-\frac{\sqrt{5}}{3}}{-\frac{2}{3}}"
            r"\n=\frac{\sqrt{5}}{2}"
            "\n$$\n"
            r"이다."
        ),
    ),
    Entry(
        11,
        "객관식",
        r"반지름의 길이가 $6$이고 넓이가 $15\pi$인 부채꼴의 중심각의 크기를 구하면?",
        [r"$\dfrac{\pi}{3}$", r"$\dfrac{\pi}{2}$", r"$\dfrac{2\pi}{3}$", r"$\dfrac{5\pi}{6}$", r"$\dfrac{7\pi}{6}$"],
        "④",
        (
            r"부채꼴의 넓이는 $\dfrac12 r^2\theta$이므로"
            "\n$$\n"
            r"\frac12\cdot 6^2\theta=15\pi \Rightarrow 18\theta=15\pi"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"\theta=\frac{5\pi}{6}"
            "\n$$"
        ),
    ),
    Entry(
        12,
        "객관식",
        r"어느 나라의 물가지수가 매년 $5\%$씩 상승할 때, 소비자 물가지수가 현재의 2배 이상이 되는 것은 최소 몇 년 후인가? (단, $\log 2=0.3$, $\log 1.05=0.02$)",
        ["6", "8", "10", "13", "15"],
        "⑤",
        (
            r"$(1.05)^n\ge2$가 되는 최소의 $n$을 구하면 된다."
            "\n"
            r"로그를 취하면"
            "\n$$\n"
            r"0.02n\ge 0.3 \Rightarrow n\ge 15"
            "\n$$"
        ),
    ),
    Entry(
        13,
        "객관식",
        r"$k\le10$인 자연수 $k$에 대하여 $x$에 대한 방정식 $|5^x-3|=k$가 오직 하나의 실근을 갖는 $k$의 값의 개수를 구하면?",
        ["5", "6", "7", "8", "9"],
        "④",
        (
            r"$t=5^x\;(>0)$라 두면 $|t-3|=k$이다."
            "\n"
            r"$k=1,2$이면 $t=3\pm k$가 모두 양수이므로 실근이 2개이고, $k=3$이면 $t=6,0$에서 $t=0$은 불가능하므로 실근이 1개이다."
            "\n"
            r"$k>3$이면 $3-k<0$이어서 실근은 1개이다."
            "\n"
            r"따라서 $k=3,4,5,6,7,8,9,10$의 8개이다."
        ),
    ),
    Entry(
        14,
        "객관식",
        r"$\log_{x-1}(-x^2+7x-6)$가 정의되도록 하는 모든 정수 $x$의 값의 합을 구하면?",
        ["11", "12", "13", "14", "15"],
        "②",
        (
            r"밑에 대하여 $x-1>0$, $x-1\ne1$이고, 진수에 대하여 $-x^2+7x-6>0$이어야 한다."
            "\n"
            r"$-x^2+7x-6>0$은 $(x-1)(x-6)<0$과 같으므로 $1<x<6$이다."
            "\n"
            r"이를 모두 합치면 가능한 정수는 $3,4,5$이고 합은 $12$이다."
        ),
    ),
    Entry(
        15,
        "객관식",
        (
            r"함수 $y=|\log_3 x^2|$의 그래프에 대하여 옳은 것만을 <보기>에서 있는 대로 고른 것은?"
            "\n\n"
            + box(
                [
                    r"ㄱ. $y$축에 대하여 대칭이다.",
                    r"ㄴ. $y=|2\log_3 x|$와 같은 그래프이다.",
                    r"ㄷ. 양수 $k$에 대하여 방정식 $|\log_3 x^2|=k$의 서로 다른 실근의 개수는 4이다.",
                ]
            )
        ),
        ["ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        "③",
        (
            r"$x^2$가 들어 있으므로 그래프는 $y$축 대칭이어서 ㄱ은 참이다."
            "\n"
            r"ㄴ은 $x<0$에서 정의되지 않는 $y=|2\log_3 x|$와 다르므로 거짓이다."
            "\n"
            r"또 $|\log_3 x^2|=k$는 $x^2=3^k$ 또는 $x^2=3^{-k}$가 되어 서로 다른 실근이 4개이므로 ㄷ은 참이다."
        ),
    ),
    Entry(
        16,
        "객관식",
        r"$n\ge2$인 자연수 $n$에 대하여 두 곡선 $y=\log_n x$, $y=-\log_n(x+3)+1$이 만나는 점의 $x$좌표가 $1$보다 크고 $2$보다 작도록 하는 모든 $n$의 값의 합을 구하면?",
        ["31", "32", "33", "34", "35"],
        "⑤",
        (
            r"두 식을 같게 두면"
            "\n$$\n"
            r"\log_n x+\log_n(x+3)=1 \Rightarrow \log_n\{x(x+3)\}=1"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"x^2+3x=n"
            "\n$$\n"
            r"이다."
            "\n"
            r"$1<x<2$이므로 $4<n<10$이어서 $n=5,6,7,8,9$이다."
            "\n$$\n5+6+7+8+9=35\n$$"
        ),
    ),
    Entry(
        17,
        "객관식",
        r"$a>1$인 상수 $a$와 $n\ge2$인 자연수 $n$에 대하여 곡선 $y=a^x$와 직선 $y=n$이 만나는 점을 $P_n$이라 하자. 선분 $P_nP_{n+1}$을 대각선으로 하고 모든 변이 $x$축 또는 $y$축과 평행한 직사각형의 넓이를 $f(n)$이라 할 때, $f(4)+f(5)+f(6)+f(7)+f(8)=2$이다. $a$의 값을 구하시오.",
        [r"$\dfrac12$", "1", r"$\dfrac32$", "2", r"$\dfrac52$"],
        "③",
        (
            r"$P_n=(\log_a n,n)$이므로 직사각형의 높이는 1, 너비는 $\log_a(n+1)-\log_a n$이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"f(n)=\log_a\frac{n+1}{n}"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"\sum_{n=4}^{8} f(n)=\log_a\frac94=2"
            "\n$$\n"
            r"이므로 $a^2=\dfrac94$, $a>1$에서"
            "\n$$\n"
            r"a=\frac32"
            "\n$$"
        ),
    ),
    Entry(18, "단답형", r"$\sqrt[4]{256}$을 간단히 하시오.", [], r"$4$", r"$256=4^4$이므로 $\sqrt[4]{256}=4$이다."),
    Entry(
        19,
        "단답형",
        (
            r"[그림 검수 필요] 함수 $y=3^{x-a}+b$의 그래프가 다음 그림과 같을 때, $ab$의 값을 구하시오. "
            r"(단, $a$, $b$는 상수이고 직선 $y=-1$은 점근선이다.)"
            "\n\n"
            '<img src="assets/scan.png" alt="지수함수 그래프" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        [],
        r"$1$",
        (
            r"점근선이 $y=-1$이므로 $b=-1$이다."
            "\n"
            r"또 그래프의 표시를 따르면 점 $(0,2)$를 지나므로"
            "\n$$\n"
            r"3^{-a}-1=2 \Rightarrow 3^{-a}=3 \Rightarrow a=-1"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"ab=(-1)(-1)=1"
            "\n$$"
        ),
    ),
    Entry(
        20,
        "단답형",
        (
            r"$\log 2=0.3$, $\log 3=0.5$일 때, 다음 물음에 답하시오."
            "\n\n"
            r"1) $\log 5$의 값을 구하시오."
            "\n\n"
            r"2) $A=\log 150-\log \dfrac{12}{5}+\log 24$일 때, $100A$의 값을 구하시오."
        ),
        [],
        "1) $0.7$\n\n2) $320$",
        (
            r"1) $\log 5=\log 10-\log 2=1-0.3=0.7$이다."
            "\n\n"
            r"2) 로그의 성질로"
            "\n$$\n"
            r"A=\log\left(150\cdot 24\cdot \frac{5}{12}\right)=\log 1500"
            "\n$$\n"
            r"이다."
            "\n"
            r"$1500=15\times 10^2$이므로"
            "\n$$\n"
            r"A=\log 15+2=\log 3+\log 5+2=0.5+0.7+2=3.2"
            "\n$$\n"
            r"이다. 따라서 $100A=320$이다."
        ),
    ),
    Entry(
        21,
        "단답형",
        r"$10000$의 모든 양의 약수를 $a_1,a_2,a_3,\ldots,a_{25}$라 할 때, $\log a_1+\log a_2+\log a_3+\cdots+\log a_{25}$의 값을 구하시오.",
        [],
        r"$50$",
        (
            r"$10000=10^4$이므로 양의 약수들을 짝지으면 각 쌍의 곱은 모두 $10000$이다."
            "\n"
            r"또 $10000$은 제곱수이므로 짝이 없는 약수는"
            "\n$$\n"
            r"\sqrt{10000}=100"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 모든 양의 약수의 곱은"
            "\n$$\n"
            r"10000^{12}\cdot 100=10^{48}\cdot 10^2=10^{50}"
            "\n$$\n"
            r"이다."
            "\n"
            r"그러므로"
            "\n$$\n"
            r"\log a_1+\log a_2+\log a_3+\cdots+\log a_{25}"
            r"\n=\log(a_1a_2a_3\cdots a_{25})"
            r"\n=\log 10^{50}"
            "\n=50"
            "\n$$\n"
            r"이다."
        ),
    ),
    Entry(
        22,
        "서술형",
        r"$1<a<b$일 때, 직선 $x=k$가 세 함수 $f(x)=\log_a x$, $g(x)=\log_b x$, $h(x)=-\log_a x$의 그래프와 만나는 점을 각각 $P,Q,R$라 하자. $\overline{PQ}:\overline{PR}=2:5$일 때, $f(b)$의 값을 구하시오. (단, $a,b,k$는 상수이고, $k>1$)",
        [],
        r"$5$",
        (
            r"$x=k$일 때"
            "\n$$\n"
            r"P(k,\log_a k),\quad Q(k,\log_b k),\quad R(k,-\log_a k)"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"\overline{PQ}=\log_a k-\log_b k,\qquad \overline{PR}=2\log_a k"
            "\n$$\n"
            r"이고,"
            "\n$$\n"
            r"\frac{\overline{PQ}}{\overline{PR}}=\frac{2}{5}"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"\frac{\frac1{\log a}-\frac1{\log b}}{\frac{2}{\log a}}=\frac25"
            "\n$$\n"
            r"에서 $\log b=5\log a$를 얻는다."
            "\n"
            r"따라서 $b=a^5$이고"
            "\n$$\n"
            r"f(b)=\log_a b=\log_a a^5=5"
            "\n$$"
        ),
    ),
    Entry(
        23,
        "서술형",
        r"$\dfrac13\le x\le 9$에서 함수 $y=kx^{-4+\log_3 x}$의 최댓값이 $9$이고, $x=\alpha$에서 최솟값 $m$을 가질 때, $\dfrac{\alpha k}{m}$의 값을 구하시오. (단, $k>0$)",
        [],
        r"$729$",
        (
            r"$t=\log_3 x$라 두면 $x=3^t$이고, $\dfrac13\le x\le9$에서 $-1\le t\le2$이다."
            "\n"
            r"또"
            "\n$$\n"
            r"x^{-4+\log_3 x}=(3^t)^{-4+t}=3^{t^2-4t}=3^{(t-2)^2-4}"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"y=k\cdot 3^{(t-2)^2-4}"
            "\n$$\n"
            r"이다."
            "\n"
            r"구간 $-1\le t\le2$에서 $(t-2)^2$의 최댓값은 $9$이므로 최댓값은 $243k$이다."
            "\n$$\n"
            r"243k=9 \Rightarrow k=\frac1{27}"
            "\n$$\n"
            r"이다."
            "\n"
            r"최솟값은 $(t-2)^2$가 가장 작을 때, 즉 $t=2$일 때 얻으므로 $\alpha=9$이고"
            "\n$$\n"
            r"m=\frac1{27}\cdot 3^{-4}=3^{-7}"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"\frac{\alpha k}{m}=\frac{9\cdot \frac1{27}}{3^{-7}}=729"
            "\n$$"
        ),
    ),
]


def parse_meta() -> dict:
    return {"school": "JEW", "year": 2024, "grade": 2, "semester": 1, "exam": "MID", "subject": "ALG"}


def id_info(exam_no: int) -> Tuple[int, int, str, str]:
    if exam_no <= 17:
        return exam_no, exam_no, "objective", str(exam_no)
    source_no = exam_no - 17
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
    parser = argparse.ArgumentParser(description="Manual ingest for JEW 2024 G2 S1 MID ALG")
    parser.add_argument("--rewrite-existing", action="store_true")
    args = parser.parse_args()
    process(rewrite_existing=args.rewrite_existing)
