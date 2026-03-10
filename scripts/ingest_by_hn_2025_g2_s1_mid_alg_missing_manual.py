# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import shutil
import textwrap
from typing import Any, Dict, List
import sys

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

PROBLEMS = ROOT / "db" / "problems"
CROPS = ROOT / "_tmp_alg_q_final"
SOURCE = "user_upload_2026-03-06"


def txt(raw: str) -> str:
    return textwrap.dedent(raw).strip()


def restore_controls(s: str) -> str:
    """
    Recover backslash-initiated LaTeX commands if a Python string literal
    accidentally interpreted escape sequences such as \\f, \\t, \\r, ...
    """
    return (
        s.replace("\x0c", r"\f")
        .replace("\t", r"\t")
        .replace("\r", r"\r")
        .replace("\x08", r"\b")
        .replace("\x07", r"\a")
        .replace("\x0b", r"\v")
    )


ROWS: List[Dict[str, Any]] = [
    {
        "school": "BY",
        "source_no": 1,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_001.png",
        "q": txt(
            r"""
            $\log_{x-2}(6-x)$의 값이 존재하도록 하는 모든 자연수 $x$의 값의 합은?
            """
        ),
        "choices": ["① 6", "② 9", "③ 12", "④ 15", "⑤ 18"],
        "answer": "②",
        "solution": txt(
            r"""
            로그의 조건은
            $$
            x-2>0,\quad x-2\ne1,\quad 6-x>0
            $$
            이다.

            따라서 $x>2,\ x\ne3,\ x<6$이므로 가능한 자연수는 $x=4,5$이다.
            합은 $4+5=9$이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 2,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_002.png",
        "q": txt(
            r"""
            16의 세제곱근 중 실수인 것을 $a$, 64의 네제곱근 중 양의 실수인 것을 $b$라고 할 때,
            $\left(\frac{b}{a}\right)^6$의 값은?
            """
        ),
        "choices": ["① $\sqrt[6]{2}$", "② $\sqrt[4]{2}$", "③ $\sqrt[3]{2}$", "④ $\sqrt{2}$", "⑤ $2$"],
        "answer": "⑤",
        "solution": txt(
            r"""
            $a=\sqrt[3]{16}=2^{\frac43}$, $b=\sqrt[4]{64}=2^{\frac32}$이므로
            $$
            \frac{b}{a}=2^{\frac32-\frac43}=2^{\frac16}
            $$
            이다.
            따라서
            $$
            \left(\frac{b}{a}\right)^6=\left(2^{\frac16}\right)^6=2
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 3,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_003.png",
        "q": txt(
            r"""
            다음 표에 대하여 $\sin(abcd)^\circ$의 값은?

            | 육십분법 | $30^\circ$ | $a^\circ$ | $60^\circ$ | $b^\circ$ |
            | --- | --- | --- | --- | --- |
            | 호도법 | $c\pi$ | $\frac{\pi}{4}$ | $d\pi$ | $\frac{\pi}{2}$ |
            """
        ),
        "choices": [
            "① $-\frac{\sqrt{3}}{2}$",
            "② $-\frac{\sqrt{2}}{2}$",
            "③ $\frac{1}{2}$",
            "④ $\frac{\sqrt{2}}{2}$",
            "⑤ $\frac{\sqrt{3}}{2}$",
        ],
        "answer": "②",
        "solution": txt(
            r"""
            표에서
            $$
            c=\frac16,\quad a=45,\quad d=\frac13,\quad b=90
            $$
            이다.

            따라서
            $$
            abcd=45\times90\times\frac16\times\frac13=225
            $$
            이고
            $$
            \sin(abcd)^\circ=\sin225^\circ=-\frac{\sqrt2}{2}
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 4,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_004.png",
        "q": txt(
            r"""
            $-2\le x\le1$일 때, 함수 $y=3^x\times2^{-x}$의 최댓값과 최솟값의 합은?
            """
        ),
        "choices": [
            "① $\frac{29}{18}$",
            "② $\frac{31}{18}$",
            "③ $\frac{11}{6}$",
            "④ $\frac{35}{18}$",
            "⑤ $\frac{37}{18}$",
        ],
        "answer": "④",
        "solution": txt(
            r"""
            $$
            y=3^x\cdot2^{-x}=\left(\frac32\right)^x
            $$
            이다. 밑이 1보다 크므로 증가함수이다.

            $$
            y_{\min}=\left(\frac32\right)^{-2}=\frac49,\quad
            y_{\max}=\left(\frac32\right)^1=\frac32
            $$
            이고, 합은
            $$
            \frac49+\frac32=\frac{35}{18}
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 5,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_005.png",
        "q": "함수 $y=\\log_2(x-1)+\\log_2(5-x)$의 최댓값은?",
        "choices": ["① 2", "② 3", "③ 4", "④ 5", "⑤ 6"],
        "answer": "①",
        "solution": txt(
            r"""
            정의역은 $1<x<5$이다.
            $$
            y=\log_2\{(x-1)(5-x)\}=\log_2\{-x^2+6x-5\}
            $$
            이다.

            $-x^2+6x-5=-(x-3)^2+4$의 최댓값은 4이므로
            $$
            y_{\max}=\log_2 4=2
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 6,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_006.png",
        "q": "$\\sqrt{6+2^{\\frac52}}\\times\\sqrt{6-2^{\\frac52}}$의 값은?",
        "choices": ["① 1", "② $\\sqrt{2}$", "③ 2", "④ $2\\sqrt{2}$", "⑤ 4"],
        "answer": "③",
        "solution": txt(
            r"""
            $$
            \sqrt{6+2^{\frac52}}\sqrt{6-2^{\frac52}}
            =\sqrt{36-\left(2^{\frac52}\right)^2}
            =\sqrt{36-32}
            =2
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 7,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_007.png",
        "q": txt(
            r"""
            각 $\theta$가 제3사분면의 각이고 $\sin\theta=-\frac45$일 때,
            $\left(1-\cos^2\theta\right)\left(1+\tan^2\theta\right)$의 값은?
            """
        ),
        "choices": ["① $\\frac{10}{9}$", "② $\\frac{4}{3}$", "③ $\\frac{14}{9}$", "④ $\\frac{16}{9}$", "⑤ $\\frac{1}{2}$"],
        "answer": "④",
        "solution": txt(
            r"""
            제3사분면이므로 $\cos\theta<0$이다.
            $\sin\theta=-\frac45$에서 $\cos\theta=-\frac35$, $\tan\theta=\frac43$.

            $$
            (1-\cos^2\theta)(1+\tan^2\theta)
            =\sin^2\theta\sec^2\theta
            =\tan^2\theta
            =\left(\frac43\right)^2
            =\frac{16}{9}
            $$
            이다.
            """
        ),
    },
    {
        "school": "BY",
        "source_no": 8,
        "kind": "objective",
        "type": "객관식",
        "crop": "BY_008.png",
        "q": txt(
            r"""
            $\sin\theta\cos\theta<0$, $\tan\theta\cos\theta<0$을 동시에 만족시키는 각 $\theta$에 대하여
            $$
            \frac{\sin\theta}{\sqrt{\sin^2\theta}}+\frac{\sqrt{\cos^2\theta}}{\cos\theta}+\frac{\tan\theta}{\sqrt{\tan^2\theta}}
            $$
            를 간단히 한 것은?
            """
        ),
        "choices": ["① $-3$", "② $-1$", "③ $1$", "④ $\\sin\\theta$", "⑤ $\\tan\\theta$"],
        "answer": "②",
        "solution": txt(
            r"""
            $\tan\theta\cos\theta=\sin\theta<0$이므로 $\sin\theta<0$.
            또 $\sin\theta\cos\theta<0$이므로 $\cos\theta>0$이고, 따라서 $\tan\theta<0$.

            $$
            \frac{\sin\theta}{|\sin\theta|}=-1,\quad
            \frac{|\cos\theta|}{\cos\theta}=1,\quad
            \frac{\tan\theta}{|\tan\theta|}=-1
            $$
            이므로 합은 $-1$이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 1,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_001.png",
        "q": "다음 중에서 옳은 것은?",
        "choices": [
            "① $-2$의 제곱근 중에서 실수인 것은 2개이다.",
            "② 4의 세제곱근 중에서 실수인 것은 3개이다.",
            "③ 세제곱근 2와 2의 세제곱근은 같다.",
            "④ 지수가 정수이고 밑이 음수이면 지수법칙을 쓸 수 있다.",
            "⑤ 지수가 유리수이고 밑이 음수이면 지수법칙을 쓸 수 있다.",
        ],
        "answer": "④",
        "solution": txt(
            r"""
            ① $x^2=-2$는 실근이 없다.
            ② 4의 세제곱근 중 실수는 1개이다.
            ③ 세제곱근 2($\sqrt[3]{2}$)와 2의 세제곱근 전체는 같은 뜻이 아니다.
            ⑤ 유리수 지수에서 밑이 음수이면 실수 범위에서 정의되지 않는 경우가 있다.

            따라서 옳은 것은 ④이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 2,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_002.png",
        "q": txt(
            r"""
            $3^x=5$일 때
            $$
            \frac{3^{2x}-3^{-2x}}{3^x-3^{-x}}\times3^x
            $$
            의 값은?
            """
        ),
        "choices": ["① 6", "② 11", "③ 16", "④ 21", "⑤ 26"],
        "answer": "⑤",
        "solution": txt(
            r"""
            $$
            \frac{3^{2x}-3^{-2x}}{3^x-3^{-x}}
            =3^x+3^{-x}
            $$
            이므로 식은
            $$
            (3^x+3^{-x})3^x=3^{2x}+1
            $$
            이다.

            $3^x=5$이므로 $3^{2x}=25$, 따라서 값은 26이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 3,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_003.png",
        "q": "$\\sqrt[3]{a^3}+\\sqrt[3]{27}=0$을 만족하는 실수 $a$의 값은?",
        "choices": ["① $-5$", "② $-3$", "③ $1$", "④ $3$", "⑤ $5$"],
        "answer": "②",
        "solution": txt(
            r"""
            $\sqrt[3]{a^3}=a$, $\sqrt[3]{27}=3$이므로
            $$
            a+3=0\Rightarrow a=-3
            $$
            이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 4,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_004.png",
        "q": "$\\log_4(\\log_3 x)=1$을 만족시키는 $x$의 값은?",
        "choices": ["① 1", "② 3", "③ $3^2$", "④ $3^3$", "⑤ $3^4$"],
        "answer": "⑤",
        "solution": txt(
            r"""
            $$
            \log_4(\log_3 x)=1\Rightarrow \log_3 x=4\Rightarrow x=3^4
            $$
            이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 5,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_005.png",
        "q": txt(
            r"""
            다음 <조건>을 만족시키는 정수 $n$에 대하여 $2^n$의 최댓값과 최솟값의 합은?

            <조건>

            (1) $\log_2 a+\log_2 b=n$

            (2) $a,b\in\{1,2,4\}$
            """
        ),
        "choices": ["① 5", "② 8", "③ 11", "④ 14", "⑤ 17"],
        "answer": "⑤",
        "solution": txt(
            r"""
            $$
            n=\log_2 a+\log_2 b=\log_2(ab)
            $$
            이다.

            $ab$는 $1,2,4,8,16$이 가능하므로
            $$
            n\in\{0,1,2,3,4\},\quad 2^n\in\{1,2,4,8,16\}
            $$
            이다.

            따라서 최솟값 1, 최댓값 16이므로 합은 17이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 13,
        "kind": "objective",
        "type": "객관식",
        "crop": "HN_013.png",
        "q": txt(
            r"""
            원점 $O$와 점 $P(1,\sqrt3)$에 대하여 동경 $OP$가 나타내는 각의 크기를 $\theta$라고 할 때,
            $\sin\theta+\sin3\theta+\sin4\theta+\sin11\theta$의 값은?
            """
        ),
        "choices": [
            "① $-\frac{\sqrt{3}}{2}$",
            "② $-\frac{1}{2}$",
            "③ 0",
            "④ $\frac{1}{2}$",
            "⑤ $\frac{\sqrt{3}}{2}$",
        ],
        "answer": "①",
        "solution": txt(
            r"""
            $\tan\theta=\sqrt3$이고 제1사분면이므로 $\theta=\frac\pi3$.

            $$
            \sin\theta=\frac{\sqrt3}{2},\ 
            \sin3\theta=\sin\pi=0,\ 
            \sin4\theta=\sin\frac{4\pi}{3}=-\frac{\sqrt3}{2},\ 
            \sin11\theta=\sin\frac{11\pi}{3}=-\frac{\sqrt3}{2}
            $$
            이다.

            합은 $-\frac{\sqrt3}{2}$이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 1,
        "kind": "subjective",
        "type": "단답형",
        "crop": "HN_101.png",
        "q": "$\\left(\\frac{1}{32}\\right)^{\\frac{2}{n}}$이 자연수가 되도록 하는 정수 $n$의 개수를 구하시오.",
        "choices": [],
        "answer": "4",
        "solution": txt(
            r"""
            $$
            \left(\frac{1}{32}\right)^{\frac{2}{n}}
            =(2^{-5})^{\frac{2}{n}}
            =2^{-\frac{10}{n}}
            $$
            이다.

            자연수가 되려면 지수 $-\frac{10}{n}$이 양의 정수여야 한다.
            따라서 $n$은 $-10$의 음의 약수:
            $$
            n=-1,-2,-5,-10
            $$
            이고 개수는 4이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 2,
        "kind": "subjective",
        "type": "단답형",
        "crop": "HN_102.png",
        "q": txt(
            r"""
            기울기가 $-\frac13$인 직선이 두 함수 $y=4^x$, $y=4^{x+3}+1$의 그래프와 만나는 점을 각각 $A$, $B$라 하자.
            선분 $AB$의 중점의 좌표가 $\left(a,\frac{33}{2}\right)$일 때, 상수 $a$의 값을 구하시오.
            """
        ),
        "choices": [],
        "answer": "$\\frac{1}{2}$",
        "solution": txt(
            r"""
            $A=(t,4^t)$라 두면, 기울기 조건 때문에 $B=(t-3,4^t+1)$가 된다.
            실제로
            $$
            \frac{(4^t+1)-4^t}{(t-3)-t}=\frac{1}{-3}=-\frac13
            $$
            이다.

            중점의 $y$좌표가 $\frac{33}{2}$이므로
            $$
            \frac{4^t+(4^t+1)}2=\frac{33}{2}
            \Rightarrow 4^t=16
            \Rightarrow t=2
            $$
            이다.

            따라서
            $$
            a=\frac{t+(t-3)}2=\frac{1}{2}
            $$
            이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 3,
        "kind": "subjective",
        "type": "단답형",
        "crop": "HN_103.png",
        "q": txt(
            r"""
            $-\pi\le\theta\le\frac\pi4$일 때
            $$
            (x-\cos\theta)^2+(y-\sin\theta)^2=\frac14
            $$
            을 만족하는 점 $(x,y)$에 대하여 $y-x$의 최댓값과 $y+x$의 최댓값을 각각 구하시오.
            """
        ),
        "choices": [],
        "answer": "$1+\\frac{\\sqrt2}{2},\\ \\frac{3\\sqrt2}{2}$",
        "solution": txt(
            r"""
            중심 $(\cos\theta,\sin\theta)$, 반지름 $\frac12$인 원이다.

            고정된 $\theta$에서
            $$
            \max(y-x)=\sin\theta-\cos\theta+\frac{\sqrt2}{2}
            $$
            이고
            $$
            \sin\theta-\cos\theta=\sqrt2\sin\left(\theta-\frac\pi4\right)
            $$
            의 최댓값은 1이므로
            $$
            \max(y-x)=1+\frac{\sqrt2}{2}.
            $$

            또
            $$
            \max(y+x)=\sin\theta+\cos\theta+\frac{\sqrt2}{2},
            \quad
            \sin\theta+\cos\theta=\sqrt2\sin\left(\theta+\frac\pi4\right)
            $$
            의 최댓값은 $\sqrt2$이므로
            $$
            \max(y+x)=\frac{3\sqrt2}{2}.
            $$
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 4,
        "kind": "subjective",
        "type": "서술형",
        "crop": "HN_104.png",
        "q": txt(
            r"""
            $A=10^{1.18}$, $B=10^{2.28}$인 두 양수 $A, B$에 대하여 부등식
            $$
            (x-A)(x-B)<0
            $$
            을 만족시키는 자연수 $x$의 개수를 구하고 풀이 과정을 쓰시오.

            (단, $\log 1.51=0.18$, $\log 1.91=0.28$)
            """
        ),
        "choices": [],
        "answer": "175",
        "solution": txt(
            r"""
            $$
            A=10^{1.18}=10\cdot10^{0.18}=10\cdot1.51=15.1,
            \quad
            B=10^{2.28}=100\cdot10^{0.28}=100\cdot1.91=191
            $$
            이다.

            $A<x<B$를 만족하는 자연수는 $16,17,\dots,190$.
            개수는
            $$
            190-16+1=175
            $$
            이다.
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 5,
        "kind": "subjective",
        "type": "서술형",
        "crop": "HN_105.png",
        "scan_box": (110, 430, 760, 1230),
        "q": txt(
            r"""
            그림과 같이 $a>1$인 상수 $a$와 $b>a+1$인 상수 $b$에 대하여
            직선 $y=-x+b$가 두 곡선 $y=a^x$, $y=\log_a(x-1)-1$와 만나는 점을 각각 $A$, $B$라 하고,
            직선 $y=-x+\frac{10}{3}b$가 두 곡선 $y=a^x$, $y=\log_a(x-1)-1$와 만나는 점을 각각 $C$, $D$라 하자.
            직선 $y=x$가 두 직선 $y=-x+b$, $y=-x+\frac{10}{3}b$와 만나는 점을 각각 $E$, $F$라 할 때,
            $$
            \overline{FD}=\sqrt2(b+1),\quad \overline{AE}=\frac{\sqrt2}{6}b
            $$
            이다. $\overline{EB}\times\overline{CF}$의 값을 구하시오.

            <img src="assets/scan.png" style="width: 60%; max-width: 60%;">
            """
        ),
        "choices": [],
        "answer": "24",
        "solution": txt(
            r"""
            $E=(\frac b2,\frac b2)$, $F=(\frac{5b}{3},\frac{5b}{3})$.

            $\overline{AE}=\frac{\sqrt2}{6}b$에서
            $$
            \left|x_A-\frac b2\right|=\frac b6
            $$
            이고, 그림에서 $A$는 왼쪽이므로 $x_A=\frac b3$, $y_A=\frac{2b}{3}$.
            따라서
            $$
            a^{\frac b3}=\frac{2b}{3}\quad\cdots(1)
            $$

            $\overline{FD}=\sqrt2(b+1)$에서
            $$
            \left|x_D-\frac{5b}{3}\right|=b+1
            $$
            이고, 그림에서 $D$는 오른쪽이므로
            $$
            x_D=\frac{8b}{3}+1,\quad y_D=\frac{2b}{3}-1.
            $$
            $D$가 로그곡선 위이므로
            $$
            \log_a\!\left(\frac{8b}{3}\right)=\frac{2b}{3}\quad\cdots(2)
            $$

            (1)을 제곱하면 $a^{\frac{2b}{3}}=\frac{4b^2}{9}$,
            (2)에서 $a^{\frac{2b}{3}}=\frac{8b}{3}$.
            따라서
            $$
            \frac{4b^2}{9}=\frac{8b}{3}\Rightarrow b=6,\quad a=2.
            $$

            그러면
            $$
            A=(2,4),\ E=(3,3),\ F=(10,10).
            $$
            직선 $y=-x+6$과 로그곡선 교점은 $B=(5,1)$,
            직선 $y=-x+20$과 지수곡선 교점은 $C=(4,16)$.

            $$
            \overline{EB}=2\sqrt2,\quad \overline{CF}=6\sqrt2
            $$
            이므로
            $$
            \overline{EB}\times\overline{CF}
            =(2\sqrt2)(6\sqrt2)=24.
            $$
            """
        ),
    },
    {
        "school": "HN",
        "source_no": 6,
        "kind": "subjective",
        "type": "서술형",
        "crop": "HN_106.png",
        "scan_box": (90, 430, 760, 1230),
        "q": txt(
            r"""
            그림과 같이 두 양수 $a$, $b$에 대하여 함수 $y=a\cos(b\pi x)$의 그래프가 $x$축과 만나는 점을 $A$, $B$라 하고,
            함수 $y=a\cos(b\pi x)$의 그래프와 직선 $y=-a$가 만나는 점을 $C$라 할 때,
            $\angle ACB=\frac\pi2$이고 삼각형 $ABC$의 넓이는 4이다.
            자연수 $n$에 대하여 $0\le x\le\frac{2}{b}$일 때, 방정식
            $$
            a\cos(bn\pi x)=\frac{2}{n}
            $$
            의 모든 실근의 합을 $f(n)$이라 하자.
            부등식 $20\le f(n)\le 40$을 만족시키는 모든 자연수 $n$의 값의 합을 구하시오.

            <img src="assets/scan.png" style="width: 60%; max-width: 60%;">
            """
        ),
        "choices": [],
        "answer": "12",
        "solution": txt(
            r"""
            좌표를
            $$
            A\!\left(\frac{1}{2b},0\right),\ 
            B\!\left(\frac{3}{2b},0\right),\ 
            C\!\left(\frac1b,-a\right)
            $$
            로 둔다.

            $\angle ACB=\frac\pi2$이므로
            $$
            \overrightarrow{CA}\cdot\overrightarrow{CB}=0
            \Rightarrow a=\frac{1}{2b}\quad\cdots(1)
            $$

            넓이 조건
            $$
            \frac12\cdot\overline{AB}\cdot a
            =\frac12\cdot\frac1b\cdot a=4
            \Rightarrow a=8b\quad\cdots(2)
            $$

            (1), (2)에서 $b=\frac14$, $a=2$.
            따라서
            $$
            2\cos\left(\frac{n\pi x}{4}\right)=\frac2n
            \Rightarrow \cos\left(\frac{n\pi x}{4}\right)=\frac1n.
            $$

            $t=\frac{n\pi x}{4}$로 두면 $0\le t\le 2n\pi$.
            $\alpha=\arccos\frac1n$이라 하면 해는
            $$
            t=2k\pi+\alpha,\quad t=2k\pi+(2\pi-\alpha)\ (k=0,\dots,n-1)
            $$
            이고, 같은 $k$의 합은 $4k\pi+2\pi$이다.

            따라서 전체 $t$의 합은
            $$
            \sum_{k=0}^{n-1}(4k\pi+2\pi)=2\pi n^2
            $$
            이므로
            $$
            f(n)=\frac{4}{n\pi}\cdot2\pi n^2=8n.
            $$

            $20\le8n\le40$에서 $n=3,4,5$.
            합은 $3+4+5=12$이다.
            """
        ),
    },
]

UNIT_OVERRIDES: Dict[str, tuple[str, str, str]] = {
    "BY-2025-G2-S1-MID-004": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "HN-2025-G2-S1-MID-005": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "HN-2025-G2-S1-MID-102": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "HN-2025-G2-S1-MID-103": ("대수(2022개정)", "2. 삼각함수", "2-3. 삼각함수의 활용"),
    "HN-2025-G2-S1-MID-106": ("대수(2022개정)", "2. 삼각함수", "2-2. 삼각함수의 그래프"),
}


def problem_id(row: Dict[str, Any]) -> str:
    no = int(row["source_no"])
    if row["kind"] == "subjective":
        no += 100
    return f"{row['school']}-2025-G2-S1-MID-{no:03d}"


def main() -> int:
    created: List[str] = []
    updated: List[str] = []
    warnings: List[str] = []

    for row in ROWS:
        pid = problem_id(row)
        folder = PROBLEMS / pid

        if folder.exists():
            shutil.rmtree(folder)
            updated.append(pid)

        folder.mkdir(parents=True, exist_ok=True)
        assets_original = folder / "assets" / "original"
        assets_original.mkdir(parents=True, exist_ok=True)

        crop = CROPS / row["crop"]
        if not crop.exists():
            warnings.append(f"{pid}: missing crop {row['crop']}")
            continue

        original_name = f"{pid}_original.png"
        shutil.copy2(crop, assets_original / original_name)

        assets = [f"assets/original/{original_name}"]
        if "scan_box" in row:
            scan = Image.open(crop).crop(tuple(row["scan_box"]))
            scan.save(folder / "assets" / "scan.png")
            assets.append("assets/scan.png")

        source_no = int(row["source_no"])
        kind = str(row["kind"])
        no_for_classifier = source_no + (100 if kind == "subjective" else 0)
        label = str(source_no) if kind == "objective" else f"서답{source_no}"

        choices_list = [restore_controls(str(c)) for c in row["choices"]]
        choices_text = "\n".join(choices_list).strip()
        q_text = restore_controls(str(row["q"]).strip())
        answer_text = restore_controls(str(row["answer"]).strip())
        solution_text = restore_controls(str(row["solution"]).strip())

        cls = classify_unit_and_level(
            question_text=q_text,
            choices_text=choices_text,
            answer_text=answer_text,
            solution_text=solution_text,
            qtype=str(row["type"]),
            grade=2,
            problem_no=no_for_classifier,
        )
        unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
            cls.unit_l1,
            cls.unit_l2,
            cls.unit_l3,
            grade=2,
        )
        if pid in UNIT_OVERRIDES:
            unit_l1, unit_l2, unit_l3 = UNIT_OVERRIDES[pid]

        front = {
            "id": pid,
            "school": row["school"],
            "year": 2025,
            "grade": 2,
            "semester": 1,
            "exam": "MID",
            "type": row["type"],
            "source_question_no": source_no,
            "source_question_kind": kind,
            "source_question_label": label,
            "difficulty": int(cls.level),
            "level": int(cls.level),
            "unit": f"{unit_l1}>{unit_l2}>{unit_l3}",
            "unit_l1": unit_l1,
            "unit_l2": unit_l2,
            "unit_l3": unit_l3,
            "source": SOURCE,
            "tags": [row["type"], f"출제번호-{label}"],
            "assets": assets,
        }

        front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
        body = (
            f"## Q\n{q_text}\n\n"
            f"## Choices\n{choices_text}\n\n"
            f"## Answer\n{answer_text}\n\n"
            f"## Solution\n{solution_text}\n"
        )
        doc = f"---\n{front_text}\n---\n\n{body}"
        (folder / "problem.md").write_text(doc, encoding="utf-8")

        if pid not in updated:
            created.append(pid)

    print(f"[SUMMARY] created={len(created)} updated={len(updated)} warnings={len(warnings)}")
    for pid in created:
        print(f"[CREATED] {pid}")
    for pid in updated:
        print(f"[UPDATED] {pid}")
    for w in warnings:
        print(f"[WARN] {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
