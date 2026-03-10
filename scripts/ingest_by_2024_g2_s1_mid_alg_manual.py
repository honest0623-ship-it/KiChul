from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import shutil
import sys
from typing import Dict, List, Optional, Tuple

import fitz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
SOURCE_PDF = ROOT / "db" / "original" / "BY.2024.G2.S1.MID1.ALG.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

UNIT_L1 = "대수(2022개정)"
UNIT_L2_MAP = {
    "1": "1. 지수함수와 로그함수",
    "2": "2. 삼각함수",
}

UNIT_L3_MAP: Dict[int, str] = {
    1: "1-1. 지수와 로그",
    2: "2-1. 삼각함수",
    3: "1-1. 지수와 로그",
    4: "1-1. 지수와 로그",
    5: "1-1. 지수와 로그",
    6: "2-1. 삼각함수",
    7: "2-2. 삼각함수의 그래프",
    8: "1-1. 지수와 로그",
    9: "2-1. 삼각함수",
    10: "1-1. 지수와 로그",
    11: "2-1. 삼각함수",
    12: "1-3. 로그함수",
    13: "2-1. 삼각함수",
    14: "2-3. 삼각함수의 활용",
    15: "1-2. 지수함수",
    16: "2-3. 삼각함수의 활용",
    17: "2-3. 삼각함수의 활용",
    18: "1-3. 로그함수",
    19: "1-1. 지수와 로그",
    20: "1-3. 로그함수",
    21: "1-1. 지수와 로그",
    22: "2-3. 삼각함수의 활용",
}

SCAN_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    11: (2, (412, 132, 558, 236)),
    16: (3, (40, 532, 168, 622)),
    18: (3, (414, 352, 558, 456)),
}

UNCERTAIN: Dict[int, str] = {
    15: "지수식의 원문 표기 확인 권장",
    17: "삼각식의 지수 표기 확인 권장",
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
    return (
        '<div style="border:1px solid #000; padding:8px; margin:8px 0;">'
        + body
        + "</div>"
    )


ENTRIES: List[Entry] = [
    Entry(
        exam_no=1,
        qtype="객관식",
        q=r"$\sqrt{2\sqrt{2\sqrt{2}}}=2^k$일 때, 유리수 $k$의 값은?",
        choices=[r"$\frac{1}{2}$", r"$\frac{3}{4}$", r"$\frac{7}{8}$", r"$\frac{11}{12}$", r"$\frac{25}{24}$"],
        answer="③",
        solution=(
            r"$\sqrt{2}=2^{\frac12}$이므로"
            "\n$$\n"
            r"\sqrt{2\sqrt{2\sqrt{2}}}"
            r"=\sqrt{2\sqrt{2\cdot 2^{\frac12}}}"
            r"=\sqrt{2\cdot 2^{\frac34}}"
            r"=\sqrt{2^{\frac74}}"
            r"=2^{\frac78}"
            "\n$$\n"
            r"이다. 따라서 $k=\frac78$이다."
        ),
    ),
    Entry(
        exam_no=2,
        qtype="객관식",
        q=(
            "다음 <보기>에서 옳은 것의 개수는?\n\n"
            + box(
                [
                    r"ㄱ. $30^\circ=\dfrac{\pi}{6}$",
                    r"ㄴ. $135^\circ=\dfrac{3\pi}{4}$",
                    r"ㄷ. $\dfrac{2\pi}{3}=150^\circ$",
                    r"ㄹ. $\dfrac{11\pi}{6}=330^\circ$",
                ]
            )
        ),
        choices=["0", "1", "2", "3", "4"],
        answer="④",
        solution=(
            r"$30^\circ=\dfrac{\pi}{6}$, $135^\circ=\dfrac{3\pi}{4}$, $\dfrac{11\pi}{6}=330^\circ$는 옳다."
            "\n"
            r"또 $\dfrac{2\pi}{3}=120^\circ$이므로 ㄷ은 옳지 않다."
            "\n"
            "따라서 옳은 것은 3개이다."
        ),
    ),
    Entry(
        exam_no=3,
        qtype="객관식",
        q=r"두 실수 $x$, $y$에 대하여 $x$는 $-81$의 세제곱근이고, $\sqrt{3}$은 $y$의 네제곱근일 때, $\dfrac{x^3}{y}$의 값은?",
        choices=["-9", "-3", "-1", "3", "9"],
        answer="①",
        solution=(
            r"$x$는 $-81$의 세제곱근이므로 $x^3=-81$이다."
            "\n"
            r"또 $\sqrt{3}$이 $y$의 네제곱근이므로 $y=\left(\sqrt{3}\right)^4=9$이다."
            "\n$$\n"
            r"\frac{x^3}{y}=\frac{-81}{9}=-9"
            "\n$$\n"
            "이므로 정답은 ①이다."
        ),
    ),
    Entry(
        exam_no=4,
        qtype="객관식",
        q=r"$\log_{x-2}\left(-x^2+3x+18\right)$이 정의되도록 하는 모든 정수 $x$의 합은?",
        choices=["8", "9", "10", "11", "12"],
        answer="②",
        solution=(
            r"로그가 정의되려면 밑에 대하여 $x-2>0$, $x-2\ne1$이고, 진수에 대하여 $-x^2+3x+18>0$이어야 한다."
            "\n"
            r"$-x^2+3x+18>0$은 $(x-6)(x+3)<0$과 같으므로 $-3<x<6$이다."
            "\n"
            r"이를 모두 합치면 $2<x<6$, $x\ne3$이므로 가능한 정수 $x$는 $4,5$이다."
            "\n$$\n4+5=9\n$$"
        ),
    ),
    Entry(
        exam_no=5,
        qtype="객관식",
        q=r"$\log 4.05=0.6075$일 때, $\log 4050=a$, $\log 0.0405=b$이다. 이때 $a-b$의 값은?",
        choices=["1", "2", "3", "4", "5"],
        answer="⑤",
        solution=(
            r"$4050=4.05\times 10^3$이므로 $a=\log 4.05+3=3.6075$이다."
            "\n"
            r"또 $0.0405=4.05\times 10^{-2}$이므로 $b=\log 4.05-2=-1.3925$이다."
            "\n$$\n"
            r"a-b=3.6075-(-1.3925)=5"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=6,
        qtype="객관식",
        q=r"$\sin\frac{7\pi}{6}-\cos\frac{11\pi}{3}+\tan\left(-\frac{9\pi}{4}\right)$의 값은?",
        choices=["-2", "-1", "0", "1", "2"],
        answer="①",
        solution=(
            r"$\sin\dfrac{7\pi}{6}=-\dfrac12$, $\cos\dfrac{11\pi}{3}=\cos\dfrac{5\pi}{3}=\dfrac12$, $\tan\left(-\dfrac{9\pi}{4}\right)=\tan\left(-\dfrac{\pi}{4}\right)=-1$이다."
            "\n$$\n"
            r"-\frac12-\frac12-1=-2"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=7,
        qtype="객관식",
        q=r"다음 중 함수 $f(x)=2\cos(4x-\pi)+3$에 대한 설명으로 옳지 않은 것은?",
        choices=[
            "최댓값은 5이다.",
            "최솟값은 1이다.",
            r"모든 실수 $x$에 대하여 $f\left(x+\dfrac{\pi}{2}\right)=f(x)$이다.",
            "그래프는 원점을 지나지 않는다.",
            r"그래프는 함수 $y=2\cos 4x$의 그래프를 $x$축의 방향으로 $-\dfrac{\pi}{4}$만큼, $y$축의 방향으로 3만큼 평행이동한 것이다.",
        ],
        answer="⑤",
        solution=(
            r"$f(x)=2\cos 4\left(x-\dfrac{\pi}{4}\right)+3$이므로 $y=2\cos 4x$의 그래프를 오른쪽으로 $\dfrac{\pi}{4}$만큼, 위로 $3$만큼 평행이동한 것이다."
            "\n"
            r"따라서 ⑤의 이동 방향 설명이 옳지 않다."
        ),
    ),
    Entry(
        exam_no=8,
        qtype="객관식",
        q=r"함수 $f(x)=\log_2\left(1+\dfrac{1}{x+3}\right)$에서 $f(1)+f(2)+f(3)+\cdots+f(n)=5$를 만족시키는 자연수 $n$의 값은?",
        choices=["28", "60", "124", "252", "508"],
        answer="③",
        solution=(
            r"$f(k)=\log_2\dfrac{k+4}{k+3}$이므로"
            "\n$$\n"
            r"\sum_{k=1}^{n} f(k)=\log_2\left(\frac54\cdot\frac65\cdot\frac76\cdots\frac{n+4}{n+3}\right)=\log_2\frac{n+4}{4}"
            "\n$$\n"
            r"이다. 따라서"
            "\n$$\n"
            r"\log_2\frac{n+4}{4}=5 \Rightarrow \frac{n+4}{4}=32 \Rightarrow n=124"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=9,
        qtype="객관식",
        q=r"$\dfrac{\pi}{2}<\theta<\pi$일 때, $\theta$를 나타내는 동경과 $6\theta$를 나타내는 동경이 서로 일치하는 $\theta$의 값은 $\dfrac{q}{p}\pi$이다. $p+q$의 값은? (단, $p$와 $q$는 서로소인 자연수이다.)",
        choices=["7", "9", "11", "13", "15"],
        answer="②",
        solution=(
            r"두 동경이 일치하므로 $6\theta-\theta=2n\pi$, 즉 $5\theta=2n\pi$이다."
            "\n"
            r"따라서 $\theta=\dfrac{2n\pi}{5}$인데, $\dfrac{\pi}{2}<\theta<\pi$를 만족하는 것은 $n=2$일 때뿐이므로"
            "\n$$\n"
            r"\theta=\frac{4\pi}{5}"
            "\n$$\n"
            r"이다. 따라서 $p=5$, $q=4$이므로 $p+q=9$이다."
        ),
    ),
    Entry(
        exam_no=10,
        qtype="객관식",
        q=(
            "단일 재료로 만들어진 벽면의 소음 차단 성능을 표시하기 위해 음향 투과 손실을 측정하려고 한다. "
            "어느 주파수 영역에서 벽의 단위 면적당 질량을 $m\\,\\mathrm{kg}/\\mathrm{m}^2$, 음향의 주파수를 $f\\,\\mathrm{Hz}$라고 하면 "
            "벽면의 음향 투과 손실 $L\\,\\mathrm{dB}$은 다음과 같다고 한다.\n\n"
            "$$\nL=20\\log(mf)-48\n$$\n\n"
            "주파수가 일정할 때, 벽의 단위 면적당 질량이 $200$배가 되면 음향 투과 손실은 $a\\,\\mathrm{dB}$만큼 늘어난다. "
            "이때 $a$의 값은? (단, $\\log 2=0.3$으로 계산한다.)"
        ),
        choices=["16", "26", "36", "46", "56"],
        answer="④",
        solution=(
            r"$m$이 $200m$이 되면 증가량은"
            "\n$$\n"
            r"20\log(200mf)-48-\left(20\log(mf)-48\right)=20\log 200"
            "\n$$\n"
            r"이다."
            "\n$$\n"
            r"20\log 200=20(\log 2+2)=20(0.3+2)=46"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=11,
        qtype="객관식",
        q=(
            r"다음 그림과 같이 중심각의 크기가 $\theta$이고 반지름의 길이가 $8$인 부채꼴 $PAB$가 있다. "
            r"반지름의 길이가 $1$인 원이 부채꼴의 둘레를 따라 $4$바퀴를 회전하면 정확히 본래 위치로 돌아온다고 할 때, "
            r"부채꼴 $PAB$의 중심각 $\theta$의 크기는?"
            "\n\n"
            '<img src="assets/scan.png" alt="부채꼴과 원" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices=[r"$\pi-3$", r"$\pi-\dfrac{5}{2}$", r"$\pi-2$", r"$\pi-\dfrac{3}{2}$", r"$\pi-1$"],
        answer="③",
        solution=(
            r"반지름이 $1$인 원이 $4$바퀴 굴러간 거리는"
            "\n$$\n"
            r"4\times 2\pi\times 1=8\pi"
            "\n$$\n"
            r"이다."
            "\n"
            r"부채꼴의 둘레의 길이는 $8+8+8\theta=16+8\theta$이므로"
            "\n$$\n"
            r"16+8\theta=8\pi"
            "\n$$\n"
            r"이다. 따라서"
            "\n$$\n"
            r"\theta=\pi-2"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=12,
        qtype="객관식",
        q=r"함수 $y=-2^x+p$의 그래프와 직선 $y=-1$이 한 점에서 만나고, 함수 $y=\log_{\frac13}(2x-p)$의 그래프와 직선 $x=2$가 한 점에서 만나도록 하는 정수 $p$의 개수는?",
        choices=["4", "5", "6", "7", "8"],
        answer="①",
        solution=(
            r"$y=-2^x+p$와 $y=-1$이 만나려면 $-2^x+p=-1$이어야 하므로 $2^x=p+1$이다."
            "\n"
            r"따라서 $p+1>0$, 즉 $p>-1$이면 한 점에서 만난다."
            "\n"
            r"또 $x=2$에서 로그함수가 정의되려면 $2\cdot 2-p>0$, 즉 $p<4$이어야 한다."
            "\n"
            r"따라서 정수 $p$는 $0,1,2,3$의 $4$개이다."
        ),
    ),
    Entry(
        exam_no=13,
        qtype="객관식",
        q=(
            r"직선 $y=mx$가 $x$축의 양의 방향과 이루는 각의 크기를 $\theta$라 할 때, 다음 <보기>가 성립한다. 양수 $m$의 값은?"
            "\n\n"
            + box([r"$\dfrac{\cos\theta}{1+\sin\theta}+\dfrac{1+\sin\theta}{\cos\theta}=6$"])
        ),
        choices=["1", r"$\sqrt{2}$", "2", r"$2\sqrt{2}$", "3"],
        answer="④",
        solution=(
            r"$\dfrac{\cos\theta}{1+\sin\theta}=\dfrac{1-\sin\theta}{\cos\theta}$이므로"
            "\n$$\n"
            r"\frac{\cos\theta}{1+\sin\theta}+\frac{1+\sin\theta}{\cos\theta}"
            r"=\frac{1-\sin\theta}{\cos\theta}+\frac{1+\sin\theta}{\cos\theta}"
            r"=\frac{2}{\cos\theta}=6"
            "\n$$\n"
            r"이다. 따라서 $\cos\theta=\dfrac13$이고,"
            "\n$$\n"
            r"\tan\theta=\frac{\sqrt{1-\left(\frac13\right)^2}}{\frac13}=2\sqrt{2}"
            "\n$$\n"
            r"이므로 $m=2\sqrt{2}$이다."
        ),
    ),
    Entry(
        exam_no=14,
        qtype="객관식",
        q=r"$\pi\le x\le 2\pi$일 때, 방정식 $\sin(\pi\cos x)=1$의 해는?",
        choices=[r"$\dfrac{\pi}{3}$", r"$\dfrac{\pi}{2}$", r"$\pi$", r"$\dfrac{3\pi}{2}$", r"$\dfrac{5\pi}{3}$"],
        answer="⑤",
        solution=(
            r"$\sin(\pi\cos x)=1$이려면"
            "\n$$\n"
            r"\pi\cos x=\frac{\pi}{2}+2n\pi"
            "\n$$\n"
            r"이어야 한다."
            "\n"
            r"따라서 $\cos x=\dfrac12+2n$인데, 가능한 값은 $\cos x=\dfrac12$뿐이다."
            "\n"
            r"$\pi\le x\le 2\pi$에서 이를 만족하는 값은 $x=\dfrac{5\pi}{3}$이다."
        ),
    ),
    Entry(
        exam_no=15,
        qtype="객관식",
        q=r"함수 $y=2^{-x+1}+1\;(0\le x\le 1)$의 그래프 위의 점 $P(x,y)$에 대하여 $\dfrac{y-1}{x+2}$의 최댓값, 최솟값을 각각 $M$, $m$이라 할 때, $M+m$의 값은?",
        choices=["1", r"$\dfrac{4}{3}$", r"$\dfrac{5}{3}$", "2", r"$\dfrac{7}{3}$"],
        answer="②",
        solution=(
            r"$y-1=2^{1-x}$이므로"
            "\n$$\n"
            r"\frac{y-1}{x+2}=\frac{2^{1-x}}{x+2}"
            "\n$$\n"
            r"이다."
            "\n"
            r"$0\le x\le 1$에서 분자는 감소하고 분모는 증가하므로 이 값은 감소한다."
            "\n"
            r"따라서"
            "\n$$\n"
            r"M=\frac{2^{1-0}}{0+2}=1,\qquad m=\frac{2^{1-1}}{1+2}=\frac13"
            "\n$$\n"
            r"이므로 $M+m=\dfrac43$이다."
        ),
    ),
    Entry(
        exam_no=16,
        qtype="객관식",
        q=(
            r"다음 그림과 같이 지면에서 출발하여 반지름의 길이가 $9$인 반원을 그리며 이동하는 모노레일을 설치하고자 한다. "
            r"모노레일 이동 경로의 $\dfrac{1}{18}$지점마다 지면과 수직인 지지대를 설치한다고 할 때, 설치하는 모든 지지대 길이의 제곱의 합은? "
            r"(단, 지지대의 폭은 고려하지 않는다.)"
            "\n\n"
            '<img src="assets/scan.png" alt="모노레일 반원" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices=["153", "507", "668", "729", "930"],
        answer="④",
        solution=(
            r"반원의 중심을 원점으로 두고, 반원의 호를 $18$등분하면 $k$번째 지지대의 길이를 $h_k$라 할 때"
            "\n$$\n"
            r"h_k=9\sin\frac{k\pi}{18}\qquad (k=1,2,\ldots,17)"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 지지대 길이의 제곱의 합은"
            "\n$$\n"
            r"\sum_{k=1}^{17} h_k^2=81\sum_{k=1}^{17}\sin^2\frac{k\pi}{18}=81\times 9=729"
            "\n$$\n"
            r"이다."
        ),
    ),
    Entry(
        exam_no=17,
        qtype="객관식",
        q=r"방정식 $2\cos^2 x+\sin x-1=k$가 $0\le x<2\pi$에서 서로 다른 네 개의 실근을 갖도록 하는 정수 $k$의 개수는?",
        choices=["1", "2", "3", "4", "5"],
        answer="①",
        solution=(
            r"$t=\sin x$라 두면 $-1\le t\le 1$이고"
            "\n$$\n"
            r"2(1-t^2)+t-1=k \Rightarrow 2t^2-t+(k-1)=0"
            "\n$$\n"
            r"이다."
            "\n"
            r"서로 다른 네 개의 실근을 가지려면 $t$에 대한 이차방정식이 $(-1,1)$ 안에서 서로 다른 두 근을 가져야 한다."
            "\n"
            r"$k=1$이면 $2t^2-t=0$이므로 $t=0,\dfrac12$가 되어 각각 서로 다른 두 근씩 주어 총 네 개의 실근을 갖는다."
            "\n"
            r"$k=0,-1,-2$에서는 가능한 $t$값의 개수가 하나이거나 $t=1$이 포함되어 네 개가 되지 않으므로 조건을 만족하는 정수 $k$는 하나뿐이다."
        ),
    ),
    Entry(
        exam_no=18,
        qtype="객관식",
        q=(
            r"그림과 같이 두 함수 $y=\log_{\frac12}x$, $y=\left(\dfrac12\right)^x$의 그래프의 교점을 $A$라 하고, "
            r"이 두 함수의 그래프와 함수 $y=\log_2(x-1)$의 그래프의 교점을 각각 $B$, $C$라 하자. "
            r"<보기>에서 옳은 것만을 있는 대로 고른 것은?"
            "\n\n"
            '<img src="assets/scan.png" alt="세 함수의 그래프" style="width:60% !important; max-width:60% !important; height:auto;" />'
            "\n\n"
            + box(
                [
                    r"ㄱ. 원점 $O$에 대하여 $\overline{OA}>\dfrac{\sqrt{2}}{2}$이다.",
                    r"ㄴ. 점 $B$의 $x$좌표를 $b$라 하면 $\dfrac32<b<2$이다.",
                    r"ㄷ. 점 $C$와 직선 $y=x$ 사이의 거리는 $\sqrt{2}$보다 크다.",
                ]
            )
        ),
        choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        answer="②",
        solution=(
            r"점 $B$는 $\log_{\frac12}x=\log_2(x-1)$에서 정해지므로"
            "\n$$\n"
            r"-\log_2 x=\log_2(x-1)\Rightarrow \log_2\frac{1}{x}=\log_2(x-1)"
            r"\Rightarrow x^2-x-1=0"
            "\n$$\n"
            r"이다. 따라서"
            "\n$$\n"
            r"b=\frac{1+\sqrt5}{2}"
            "\n$$\n"
            r"이므로 $\dfrac32<b<2$이다."
            "\n\n"
            r"점 $A$는 $y=\log_{\frac12}x$와 $y=\left(\dfrac12\right)^x$의 교점이므로 $x=y$인 제1사분면의 점이며, 수치적으로 $A\approx(0.641,0.641)$이다."
            r" 따라서"
            "\n$$\n"
            r"\overline{OA}\approx \sqrt{2}\times 0.641 > \frac{\sqrt2}{2}"
            "\n$$\n"
            r"이어서 ㄱ은 참이다."
            "\n\n"
            r"또 점 $C$는 대략 $C\approx(2.167,0.223)$이므로 직선 $y=x$와의 거리는"
            "\n$$\n"
            r"\frac{|2.167-0.223|}{\sqrt2}<\sqrt2"
            "\n$$\n"
            r"가 되어 ㄷ은 거짓이다. 따라서 옳은 것은 ㄱ, ㄴ이다."
        ),
    ),
    Entry(
        exam_no=19,
        qtype="단답형",
        q=r"방정식 $2^{3x}\times 9^{x^2-3}=24^x$의 모든 실근의 곱을 구하시오.",
        choices=[],
        answer=r"$-3$",
        solution=(
            r"$24^x=2^{3x}\cdot 3^x$이므로 양변에서 $2^{3x}$를 약분하면"
            "\n$$\n"
            r"9^{x^2-3}=3^x"
            "\n$$\n"
            r"이다."
            "\n"
            r"$9=3^2$이므로"
            "\n$$\n"
            r"3^{2x^2-6}=3^x \Rightarrow 2x^2-x-6=0"
            "\n$$\n"
            r"이다. 따라서"
            "\n$$\n"
            r"(2x+3)(x-2)=0"
            "\n$$\n"
            r"이므로 실근은 $2$, $-\dfrac32$이다."
            "\n$$\n"
            r"2\times\left(-\frac32\right)=-3"
            "\n$$"
        ),
    ),
    Entry(
        exam_no=20,
        qtype="단답형",
        q=(
            r"$a-1\le x\le a+1$에서 함수"
            "\n$$\n"
            r"f(x)=\begin{cases}\left(\dfrac12\right)^{x-2} & (x<2)\\[4pt]\log_2 x & (x\ge 2)\end{cases}"
            "\n$$\n"
            r"의 최댓값과 최솟값의 합이 $3$이 되도록 하는 모든 실수 $a$의 값의 곱을 구하시오."
        ),
        choices=[],
        answer=r"$6$",
        solution=(
            r"$x<2$에서는 $f(x)=2^{2-x}$로 감소하고, $x\ge2$에서는 $f(x)=\log_2 x$로 증가하며, $f(2)=1$이다."
            "\n"
            r"따라서 구간이 $x=2$를 포함하면 최솟값은 $1$이다."
            "\n\n"
            r"1. $a<1$이면 구간 전체가 $x<2$에 있으므로 최댓값과 최솟값의 합은 $3$이 될 수 없다."
            "\n"
            r"2. $1\le a<3$이면 구간이 $x=2$를 포함하므로 최솟값은 $1$이고, 최댓값은 양 끝점 값 중 큰 값이다."
            r" 이때 합이 $3$이 되려면 최댓값이 $2$여야 하므로 $a=2$이다."
            "\n"
            r"3. $a\ge3$이면 구간 전체가 $x\ge2$에 있으므로"
            "\n$$\n"
            r"\log_2(a-1)+\log_2(a+1)=3"
            r"\Rightarrow \log_2(a^2-1)=3"
            r"\Rightarrow a^2=9"
            "\n$$\n"
            r"이어서 $a=3$이다."
            "\n"
            r"따라서 가능한 $a$는 $2,3$이고, 그 곱은 $6$이다."
        ),
    ),
    Entry(
        exam_no=21,
        qtype="서술형",
        q=r"모든 실수 $x$에 대하여 $\sqrt[3]{x^2-2(a-1)x+5(a-1)}$이 양수가 되기 위한 자연수 $a$의 개수를 구하는 풀이과정을 쓰고 답을 구하시오.",
        choices=[],
        answer=r"$4$",
        solution=(
            r"세제곱근의 값이 양수이려면 근호 안의 값이 양수여야 하므로,"
            "\n$$\n"
            r"x^2-2(a-1)x+5(a-1)>0"
            "\n$$\n"
            r"가 모든 실수 $x$에 대하여 성립해야 한다."
            "\n"
            r"이차식의 계수는 양수이므로 판별식이 음수이면 된다."
            "\n$$\n"
            r"D=\{-2(a-1)\}^2-4\cdot 1\cdot 5(a-1)=4(a-1)(a-6)<0"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"1<a<6"
            "\n$$\n"
            r"이다."
            "\n"
            r"자연수 $a$는 $2,3,4,5$의 네 개이다."
        ),
    ),
    Entry(
        exam_no=22,
        qtype="서술형",
        q=r"실수 $p$, $q$에 대하여 함수 $f(x)=\sin^2\left(x+\dfrac{\pi}{3}\right)-2\sin\left(x-\dfrac{\pi}{6}\right)+p$는 $x=q\pi$일 때 최댓값 $5$를 갖는다. $p+q$의 값을 구하는 풀이과정을 쓰고 답을 구하시오. (단, $0\le x<2\pi$)",
        choices=[],
        answer=r"$\dfrac{14}{3}$",
        solution=(
            r"$t=x-\dfrac{\pi}{6}$이라 두면"
            "\n$$\n"
            r"\sin^2\left(x+\frac{\pi}{3}\right)=\sin^2\left(t+\frac{\pi}{2}\right)=\cos^2 t"
            "\n$$\n"
            r"이므로"
            "\n$$\n"
            r"f(x)=\cos^2 t-2\sin t+p=1-\sin^2 t-2\sin t+p"
            r"=-(\sin t+1)^2+p+2"
            "\n$$\n"
            r"이다."
            "\n"
            r"따라서 최댓값은 $p+2$이고, 이것이 $5$이므로 $p=3$이다."
            "\n"
            r"최댓값은 $\sin t=-1$일 때 이루어지므로"
            "\n$$\n"
            r"x-\frac{\pi}{6}=-\frac{\pi}{2}+2n\pi"
            "\n$$\n"
            r"이다."
            "\n"
            r"$0\le x<2\pi$에서 이를 만족하는 값은 $x=\dfrac{5\pi}{3}$이므로 $q=\dfrac53$이다."
            "\n$$\n"
            r"p+q=3+\frac53=\frac{14}{3}"
            "\n$$"
        ),
    ),
]


def parse_meta() -> dict:
    return {
        "school": "BY",
        "year": 2024,
        "grade": 2,
        "semester": 1,
        "exam": "MID",
        "subject": "ALG",
    }


def id_info(exam_no: int) -> Tuple[int, int, str, str]:
    if exam_no <= 18:
        return exam_no, exam_no, "objective", str(exam_no)
    source_no = exam_no - 18
    return 100 + source_no, source_no, "subjective", f"서답{source_no}번"


def export_crop(doc: fitz.Document, page_no: int, rect_vals: Tuple[float, float, float, float], out_path: Path) -> None:
    page = doc[page_no - 1]
    rect = fitz.Rect(*rect_vals)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "")


def unit_triplet(exam_no: int) -> Tuple[str, str, str]:
    unit_l3 = UNIT_L3_MAP[exam_no]
    unit_l2 = UNIT_L2_MAP[unit_l3[0]]
    return UNIT_L1, unit_l2, unit_l3


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

    lines: List[str] = [
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
        marks = ["①", "②", "③", "④", "⑤"]
        for mark, choice in zip(marks, entry.choices):
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

        original_asset_name = SOURCE_PDF.name
        shutil.copy2(SOURCE_PDF, assets_original / original_asset_name)

        has_scan = entry.exam_no in SCAN_CROPS
        scan_path = pdir / "assets" / "scan.png"
        if has_scan:
            page_no, rect_vals = SCAN_CROPS[entry.exam_no]
            export_crop(doc, page_no, rect_vals, scan_path)
        elif scan_path.exists():
            scan_path.unlink()

        q_for_cls = strip_html(entry.q)
        choices_for_cls = "\n".join(entry.choices)
        cls = classify_unit_and_level(
            question_text=q_for_cls,
            choices_text=choices_for_cls,
            answer_text=entry.answer,
            solution_text=entry.solution,
            qtype=entry.qtype,
            grade=meta["grade"],
            problem_no=pid_no,
        )
        unit_l1, unit_l2, unit_l3 = unit_triplet(entry.exam_no)
        level = cls.level

        content = build_markdown(
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
            original_asset_name=original_asset_name,
            has_scan=has_scan,
        )
        md_path.write_text(content, encoding="utf-8", newline="\n")

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
    parser = argparse.ArgumentParser(description="Manual ingest for BY 2024 G2 S1 MID ALG")
    parser.add_argument("--rewrite-existing", action="store_true")
    args = parser.parse_args()
    process(rewrite_existing=args.rewrite_existing)
