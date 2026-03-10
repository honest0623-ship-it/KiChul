from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
import textwrap
from typing import Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

PROBLEMS = ROOT / "db" / "problems"
REPORT_PATH = ROOT / "_tmp_je_jew_2025_g2_s1_mid_alg_ingest_report.txt"

SOURCE = "user_upload_2026-03-03"
SUBJECT = "ALG"


def txt(raw: str) -> str:
    return textwrap.dedent(raw).strip()


@dataclass(frozen=True)
class Row:
    pid: str
    qtype: str
    crop: str
    q: str
    choices: List[str]
    answer: str
    solution: str
    uncertain: bool = False


EXPECTED_IDS = [
    *[f"JE-2025-G2-S1-MID-{i:03d}" for i in range(1, 17)],
    *[f"JE-2025-G2-S1-MID-{i:03d}" for i in range(101, 107)],
    *[f"JEW-2025-G2-S1-MID-{i:03d}" for i in range(1, 18)],
    *[f"JEW-2025-G2-S1-MID-{i:03d}" for i in range(101, 107)],
]

ROWS: List[Row] = [
    Row(
        pid="JE-2025-G2-S1-MID-001",
        qtype="객관식",
        crop="_tmp_je_missing/je_q1.png",
        q=txt(
            r"""
            복소수 $9+6i$의 실수부분과 허수부분을 각각 $a$, $b$라 할 때, $a-b$의 값은?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="③",
        solution=txt(
            r"""
            복소수 $9+6i$의 실수부분은 $9$, 허수부분은 $6$이므로
            $$
            a=9,
 b=6
            $$
            이다.

            따라서
            $$
            a-b=9-6=3
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-002",
        qtype="객관식",
        crop="_tmp_je_missing/je_q2.png",
        q=txt(
            r"""
            다항식 $f(x)=2x^3+4x^2-3x+7$을 일차식 $x+1$로 나누었을 때의 나머지를 $R$이라 할 때, $R$의 값은?
            """
        ),
        choices=["① 12", "② 14", "③ 16", "④ 18", "⑤ 20"],
        answer="①",
        solution=txt(
            r"""
            나머지정리에 의해
            $$
            R=f(-1)
            $$
            이다.

            $$
            f(-1)=2(-1)^3+4(-1)^2-3(-1)+7
            =-2+4+3+7=12
            $$

            따라서
            $$
            R=12
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-003",
        qtype="객관식",
        crop="_tmp_je_missing/je_q3.png",
        q=txt(
            r"""
            등식 $(3a-6)+(a-b)i=3+2i$를 만족시키는 두 실수 $a$, $b$에 대하여 $a+b$의 값은?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="④",
        solution=txt(
            r"""
            실수부분과 허수부분을 각각 비교하면
            $$
            3a-6=3,
 a-b=2
            $$
            이다.

            첫째 식에서 $a=3$이고,
            둘째 식에서 $3-b=2$이므로 $b=1$이다.

            따라서
            $$
            a+b=3+1=4
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-004",
        qtype="객관식",
        crop="_tmp_je_missing/je_q4.png",
        q=txt(
            r"""
            $x$의 값에 관계없이 등식
            $$
            (x-4)^2=a(x-2)^2+b(x-2)+c
            $$
            가 항상 성립할 때, $a-b+2c$의 값은? (단, $a,b,c$는 상수이다.)
            """
        ),
        choices=["① 11", "② 12", "③ 13", "④ 14", "⑤ 15"],
        answer="③",
        solution=txt(
            r"""
            좌변을 전개하면
            $$
            (x-4)^2=x^2-8x+16
            $$
            이다.

            우변을 전개하면
            $$
            a(x-2)^2+b(x-2)+c
            =ax^2+(-4a+b)x+(4a-2b+c)
            $$
            이다.

            계수를 비교하면
            $$
            a=1,
 -4a+b=-8,
 4a-2b+c=16
            $$
            이므로
            $$
            a=1,
 b=-4,
 c=4
            $$
            이다.

            따라서
            $$
            a-b+2c=1-(-4)+2\cdot4=13
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-005",
        qtype="객관식",
        crop="_tmp_je_missing/je_q5.png",
        q=txt(
            r"""
            이차방정식 $2x^2-5x+8=0$의 서로 다른 두 근을 $\alpha$, $\beta$라 할 때, $(\alpha+4)(\beta+4)$의 값은?
            """
        ),
        choices=["① 30", "② 32", "③ 34", "④ 36", "⑤ 38"],
        answer="①",
        solution=txt(
            r"""
            이차방정식 $2x^2-5x+8=0$에서 근과 계수의 관계를 쓰면
            $$
            \alpha+\beta=\frac{5}{2},
 \alpha\beta=\frac{8}{2}=4
            $$
            이다.

            $$
            (\alpha+4)(\beta+4)=\alpha\beta+4(\alpha+\beta)+16
            $$
            이므로
            $$
            (\alpha+4)(\beta+4)=4+4\cdot\frac{5}{2}+16=30
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-011",
        qtype="객관식",
        crop="_tmp_je_missing/je_q11.png",
        q=txt(
            r"""
            $-4\le x\le2$일 때, 이차함수 $y=x^2-2x+k$의 최댓값이 $30$이다. 이 함수의 최솟값을 $m$이라 할 때, $k+m$의 값은? (단, $k$는 상수이다.)
            """
        ),
        choices=["① 11", "② 12", "③ 13", "④ 14", "⑤ 15"],
        answer="①",
        solution=txt(
            r"""
            $$
            y=x^2-2x+k=(x-1)^2+k-1
            $$
            이다.

            꼭짓점은 $x=1$이고, 구간 $[-4,2]$에서 최솟값은
            $$
            m=k-1
            $$
            이다.

            최댓값은 꼭짓점에서 가장 먼 끝점 $x=-4$에서 얻으므로
            $$
            y(-4)=(-5)^2+k-1=24+k
            $$
            이다.

            최댓값이 $30$이므로
            $$
            24+k=30\Rightarrow k=6
            $$
            이다.

            따라서
            $$
            m=k-1=5,
 k+m=6+5=11
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-101",
        qtype="단답형",
        crop="_tmp_je_missing/je_s1.png",
        q=txt(
            r"""
            $x+y=5$, $xy=-4$일 때, $x^3+y^3$의 값을 구하시오.
            """
        ),
        choices=[],
        answer="185",
        solution=txt(
            r"""
            $$
            x^3+y^3=(x+y)^3-3xy(x+y)
            $$
            이므로
            $$
            x^3+y^3=5^3-3(-4)\cdot5=125+60=185
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JE-2025-G2-S1-MID-102",
        qtype="단답형",
        crop="_tmp_je_missing/je_s2.png",
        q=txt(
            r"""
            정의역이 $\{x\mid0\le x\le3\}$일 때, 함수
            $$
            y=\log_2(-x^2+2x+a)
            $$
            의 최댓값이 $3$일 때, 최솟값을 구하시오.
            """
        ),
        choices=[],
        answer="2",
        solution=txt(
            r"""
            안쪽 식을
            $$
            f(x)=-x^2+2x+a=-(x-1)^2+a+1
            $$
            라 두자.

            정의역 $0\le x\le3$에서 $f(x)$의 최댓값은 $x=1$일 때 $a+1$이다.
            또 $\log_2$는 증가함수이므로
            $$
            \log_2(a+1)=3
            $$
            이고, 따라서
            $$
            a+1=8\Rightarrow a=7
            $$
            이다.

            이제
            $$
            f(x)=-x^2+2x+7
            $$
            이고, $[0,3]$에서 최솟값은 끝점에서 비교하면
            $$
            f(0)=7,
 f(3)=4
            $$
            이므로 $4$이다.

            따라서 함수 $y$의 최솟값은
            $$
            \log_2 4=2
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-001",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q1.png",
        q=txt(
            r"""
            다음 값 중 옳지 않은 것은?
            """
        ),
        choices=[
            r"① $\log_2 32=5$",
            r"② $\log_5\sqrt{5}=\dfrac12$",
            r"③ $\log_{10}\dfrac{1}{1000}=-3$",
            r"④ $\log_{\frac12}8=-4$",
            r"⑤ $\log_{\frac13}9=-2$",
        ],
        answer="④",
        solution=txt(
            r"""
            각 보기의 참, 거짓을 확인하면
            $$
            \log_2 32=5,
 \log_5\sqrt{5}=\frac12,
 \log_{10}\frac1{1000}=-3,
 \log_{\frac13}9=-2
            $$
            는 모두 참이다.

            그런데
            $$
            \log_{\frac12}8=-3
            $$
            이므로 $\log_{\frac12}8=-4$는 거짓이다.

            따라서 옳지 않은 것은 ④이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-002",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q2.png",
        q=txt(
            r"""
            $$
            \log_2(4\sqrt{5})+\log_{\sqrt2}(\sqrt{10})-\frac32\log_2 5
            $$
            의 값은?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="③",
        solution=txt(
            r"""
            $$
            \log_2(4\sqrt5)=\log_2 4+\log_2\sqrt5=2+\frac12\log_2 5
            $$
            이고,
            $$
            \log_{\sqrt2}(\sqrt{10})
            =\frac{\log_2\sqrt{10}}{\log_2\sqrt2}
            =\frac{\frac12\log_2 10}{\frac12}
            =\log_2 10=1+\log_2 5
            $$
            이다.

            따라서 전체 값은
            $$
            \left(2+\frac12\log_2 5\right)+(1+\log_2 5)-\frac32\log_2 5=3
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-004",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q4.png",
        q=txt(
            r"""
            둘레의 길이가 $14$인 부채꼴의 중심각의 크기가 $\dfrac13$일 때, 호의 길이로 적절한 것은?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="②",
        solution=txt(
            r"""
            반지름을 $r$, 호의 길이를 $l$이라 하면
            $$
            l=r\theta=r\cdot\frac13=\frac r3
            $$
            이다.

            부채꼴의 둘레 길이는
            $$
            2r+l=14
            $$
            이므로
            $$
            2r+\frac r3=14
            \Rightarrow \frac{7r}{3}=14
            \Rightarrow r=6
            $$
            이다.

            따라서
            $$
            l=\frac r3=\frac63=2
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-005",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q5.png",
        q=txt(
            r"""
            각 $\theta$가 제3사분면의 각이고 $\cos\theta=-\dfrac{1}{\sqrt5}$일 때,
            $$
            \sqrt5\sin\theta+\tan\theta
            $$
            의 값은?
            """
        ),
        choices=["① 0", "② -1", "③ 1", "④ -2", "⑤ 2"],
        answer="①",
        solution=txt(
            r"""
            $$
            \sin^2\theta=1-\cos^2\theta=1-\frac15=\frac45
            $$
            이고, 제3사분면이므로
            $$
            \sin\theta=-\frac{2}{\sqrt5}
            $$
            이다.

            또
            $$
            \tan\theta=\frac{\sin\theta}{\cos\theta}
            =\frac{-2/\sqrt5}{-1/\sqrt5}=2
            $$
            이다.

            따라서
            $$
            \sqrt5\sin\theta+\tan\theta
            =\sqrt5\left(-\frac{2}{\sqrt5}\right)+2
            =-2+2=0
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-007",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q7.png",
        q=txt(
            r"""
            다음 보기 중 옳은 것을 모두 고르면?

            ㄱ. $2^{\log_2 1+\log_2 2+\log_2 4}=7$

            ㄴ. $\log_3(3\cdot3^2\cdot3^3\cdot3^4)=10$

            ㄷ. $\log\left(1-\dfrac12\right)+\log\left(1-\dfrac13\right)+\log\left(1-\dfrac14\right)+\cdots+\log\left(1-\dfrac1{10}\right)=-1$
            """
        ),
        choices=["① ㄱ", "② ㄴ", "③ ㄷ", "④ ㄱ, ㄷ", "⑤ ㄴ, ㄷ"],
        answer="⑤",
        solution=txt(
            r"""
            ㄱ에서
            $$
            2^{\log_2 1+\log_2 2+\log_2 4}
            =2^{0+1+2}=2^3=8
            $$
            이므로 거짓이다.

            ㄴ에서
            $$
            \log_3(3\cdot3^2\cdot3^3\cdot3^4)
            =\log_3\left(3^{1+2+3+4}\right)=\log_3(3^{10})=10
            $$
            이므로 참이다.

            ㄷ에서
            $$
            \sum_{k=2}^{10}\log\left(1-\frac1k\right)
            =\log\prod_{k=2}^{10}\left(1-\frac1k\right)
            =\log\prod_{k=2}^{10}\frac{k-1}{k}
            =\log\frac1{10}=-1
            $$
            이므로 참이다.

            따라서 옳은 것은 ㄴ, ㄷ이다.
            """
        ),
        uncertain=True,
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-009",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q9.png",
        q=txt(
            r"""
            함수 $y=a^x$($a>0$, $a\ne1$)의 그래프를 $y$축 대칭한 후, $x$축의 방향으로 $m$만큼, $y$축의 방향으로 $n$만큼 평행이동하면
            함수
            $$
            y=4\left(\frac12\right)^x+3
            $$
            의 그래프와 일치한다.

            이때 $a+m+n$의 값은? (단, $a,m,n$은 상수이다.)
            """
        ),
        choices=["① 9", "② 7", "③ 5", "④ 3", "⑤ 1"],
        answer="②",
        solution=txt(
            r"""
            $y=a^x$를 $y$축 대칭하면
            $$
            y=a^{-x}=\left(\frac1a\right)^x
            $$
            이다.

            이를 $x$축 방향으로 $m$, $y$축 방향으로 $n$만큼 평행이동하면
            $$
            y=\left(\frac1a\right)^{x-m}+n
            $$
            이다.

            문제 조건에 의해
            $$
            \left(\frac1a\right)^{x-m}+n=4\left(\frac12\right)^x+3
            $$
            이므로 밑을 비교하면
            $$
            \frac1a=\frac12\Rightarrow a=2
            $$
            이다.

            또
            $$
            \left(\frac1a\right)^{x-m}
            =\left(\frac12\right)^{x-m}
            =2^m\left(\frac12\right)^x
            $$
            이므로
            $$
            2^m=4\Rightarrow m=2,
 n=3
            $$
            이다.

            따라서
            $$
            a+m+n=2+2+3=7
            $$
            이다.
            """
        ),
        uncertain=True,
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-010",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q10.png",
        q=txt(
            r"""
            다음 중 함수 $y=3^{x-2}-2$의 설명으로 옳지 않은 것은?
            """
        ),
        choices=[
            "① 정의역은 실수 전체이다.",
            r"② 치역은 $\{y\mid y>-2\}$인 모든 실수이다.",
            "③ 점근선은 $y=-2$이다.",
            r"④ 이 함수는 $y=\log_3(x+2)+2$와 역함수 관계이다.",
            r"⑤ 정의역 $\{x\mid2\le x\le4\}$에서 최솟값은 $-2$이다.",
        ],
        answer="⑤",
        solution=txt(
            r"""
            함수
            $$
            y=3^{x-2}-2
            $$
            는 지수함수이므로 정의역은 실수 전체이고, 값의 범위는
            $$
            y>-2
            $$
            이다. 또한 수평점근선은 $y=-2$이다.

            역함수를 구하면
            $$
            x=3^{y-2}-2
            \Rightarrow y=\log_3(x+2)+2
            $$
            이므로 ④도 옳다.

            $2\le x\le4$에서
            $$
            y(2)=3^0-2=-1,
 y(4)=3^2-2=7
            $$
            이므로 최솟값은 $-1$이다.

            따라서 옳지 않은 것은 ⑤이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-011",
        qtype="객관식",
        crop="_tmp_jew_missing/jew_q11.png",
        q=txt(
            r"""
            부등식
            $$
            \left(\frac14\right)^{2x}\ge\left(\frac12\right)^{2x+6}
            $$
            을 만족하는 자연수 $x$의 개수는?
            """
        ),
        choices=["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        answer="③",
        solution=txt(
            r"""
            $$
            \left(\frac14\right)^{2x}=\left(\frac12\right)^{4x}
            $$
            이므로
            $$
            \left(\frac12\right)^{4x}\ge\left(\frac12\right)^{2x+6}
            $$
            이다.

            밑이 $\frac12$로 $1$보다 작으므로 지수의 대소가 반대로 되어
            $$
            4x\le2x+6
            \Rightarrow 2x\le6
            \Rightarrow x\le3
            $$
            이다.

            자연수 $x$는 $1,2,3$이므로 개수는 $3$이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-101",
        qtype="단답형",
        crop="_tmp_jew_missing/jew_s1.png",
        q=txt(
            r"""
            다음 식을 간단히 하여
            $$
            x^{\frac56}\times\sqrt[3]{y^4}\times\sqrt[6]{y}\div x^{-\frac23}\times x^{\frac32}\div\sqrt{y}=x^a y^b
            $$
            로 나타낼 때, 다음 물음에 답하시오.

            (1) 실수 $a$의 값

            (2) 실수 $b$의 값
            """
        ),
        choices=[],
        answer="$a=3, b=1$",
        solution=txt(
            r"""
            거듭제곱꼴로 바꾸면
            $$
            \sqrt[3]{y^4}=y^{\frac43},
 \sqrt[6]{y}=y^{\frac16},
 \sqrt y=y^{\frac12}
            $$
            이다.

            따라서 $x$의 지수는
            $$
            \frac56-\left(-\frac23\right)+\frac32
            =\frac56+\frac46+\frac96
            =\frac{18}{6}=3
            $$
            이고,

            $y$의 지수는
            $$
            \frac43+\frac16-\frac12
            =\frac86+\frac16-\frac36
            =\frac66=1
            $$
            이다.

            따라서
            $$
            a=3,
 b=1
            $$
            이다.
            """
        ),
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-102",
        qtype="단답형",
        crop="_tmp_jew_missing/jew_s2.png",
        q=txt(
            r"""
            함수
            $$
            y=\log_{\frac14}(x^2-ax+b)
            $$
            는 $x=2$일 때 최댓값 $-2$를 갖는다.

            다음 물음에 답하시오.

            (1) 실수 $a$의 값

            (2) 실수 $b$의 값
            """
        ),
        choices=[],
        answer="$a=4, b=20$",
        solution=txt(
            r"""
            안쪽 식을
            $$
            g(x)=x^2-ax+b
            $$
            라 하자.

            로그의 밑이 $\frac14$로 $1$보다 작으므로 $y$가 최댓값을 가지려면
            $g(x)$가 최솟값을 가져야 한다.

            $x=2$에서 최댓값이 나오므로 $x=2$는 $g(x)$의 꼭짓점 $x$좌표이다.
            따라서
            $$
            \frac{a}{2}=2\Rightarrow a=4
            $$
            이다.

            또 최댓값이 $-2$이므로
            $$
            \log_{\frac14}(g(2))=-2
            \Rightarrow g(2)=\left(\frac14\right)^{-2}=16
            $$
            이다.

            $a=4$를 대입하면
            $$
            g(2)=2^2-4\cdot2+b=b-4
            $$
            이므로
            $$
            b-4=16\Rightarrow b=20
            $$
            이다.

            따라서
            $$
            a=4,
 b=20
            $$
            이다.
            """
        ),
        uncertain=True,
    ),
    Row(
        pid="JEW-2025-G2-S1-MID-103",
        qtype="단답형",
        crop="_tmp_jew_missing/jew_s3.png",
        q=txt(
            r"""
            다음은 $\sin\theta=\dfrac35$일 때, $\cos\theta$의 값을 구하는 과정이다.
            다음 물음에 답하시오.

            $\sin\theta>0$이므로 각 $\theta$는 제1사분면의 각 또는 (가)의 각이다.

            i) 각 $\theta$가 제1사분면의 각이면 $\cos\theta=(\text{나})$

            ii) 각 $\theta$가 (가)의 각이면 $\cos\theta=(\text{다})$

            따라서 $\cos\theta=(\text{나})$ 또는 $\cos\theta=(\text{다})$

            (1) (가)에 알맞은 각의 위치를 $\alpha<\theta<\beta$라 할 때, $\alpha+\beta$의 값
            (단, $\alpha,\beta$는 실수이고 호도법으로 계산)

            (2) (나)에 알맞은 실수

            (3) (다)에 알맞은 실수
            """
        ),
        choices=[],
        answer=r"$\dfrac{3\pi}{2},\ \dfrac45,\ -\dfrac45$",
        solution=txt(
            r"""
            $\sin\theta=\frac35>0$이므로 $\theta$는 제1사분면 또는 제2사분면의 각이다.
            따라서 (가)는 제2사분면이고
            $$
            \frac{\pi}{2}<\theta<\pi
            $$
            이다.

            그러므로
            $$
            \alpha=\frac{\pi}{2},
 \beta=\pi,
 \alpha+\beta=\frac{3\pi}{2}
            $$
            이다.

            또
            $$
            \cos^2\theta=1-\sin^2\theta=1-\left(\frac35\right)^2=\frac{16}{25}
            $$
            이므로
            $$
            \cos\theta=\pm\frac45
            $$
            이다.

            제1사분면에서는 $\cos\theta>0$이므로
            $$
            (\text{나})=\frac45
            $$
            이고,

            제2사분면에서는 $\cos\theta<0$이므로
            $$
            (\text{다})=-\frac45
            $$
            이다.
            """
        ),
        uncertain=True,
    ),
]

UNIT_OVERRIDE: Dict[str, Tuple[str, str, str]] = {
    "JE-2025-G2-S1-MID-001": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-002": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-003": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-004": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-005": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-011": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-101": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JE-2025-G2-S1-MID-102": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수"),
    "JEW-2025-G2-S1-MID-001": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2025-G2-S1-MID-002": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2025-G2-S1-MID-004": ("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수"),
    "JEW-2025-G2-S1-MID-005": ("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수"),
    "JEW-2025-G2-S1-MID-007": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2025-G2-S1-MID-009": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "JEW-2025-G2-S1-MID-010": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수"),
    "JEW-2025-G2-S1-MID-011": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2025-G2-S1-MID-101": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    "JEW-2025-G2-S1-MID-102": ("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수"),
    "JEW-2025-G2-S1-MID-103": ("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수"),
}


def _pid_meta(pid: str) -> Tuple[str, int, str, int, str]:
    school, year, grade_token, sem_token, exam, num_token = pid.split("-")
    year_i = int(year)
    grade_i = int(grade_token[1:])
    semester_i = int(sem_token[1:])
    num = int(num_token)
    if num >= 100:
        source_no = num - 100
        source_kind = "subjective"
        source_label = f"서답{source_no}"
    else:
        source_no = num
        source_kind = "objective"
        source_label = str(source_no)
    return school, year_i, grade_i, semester_i, exam, source_kind, source_no, source_label


def _build_front(row: Row, unit: Tuple[str, str, str], level: int, source_no: int, source_kind: str, source_label: str, asset_name: str) -> Dict[str, object]:
    school, year_i, grade_i, sem_i, exam, *_ = _pid_meta(row.pid)
    l1, l2, l3 = unit
    tags = [row.qtype, f"출제번호-{source_label}"]
    return {
        "id": row.pid,
        "school": school,
        "year": year_i,
        "grade": grade_i,
        "semester": sem_i,
        "exam": exam,
        "subject": SUBJECT,
        "type": row.qtype,
        "source_question_no": source_no,
        "source_question_kind": source_kind,
        "source_question_label": source_label,
        "difficulty": int(level),
        "level": int(level),
        "unit": f"{l1}>{l2}>{l3}",
        "unit_l1": l1,
        "unit_l2": l2,
        "unit_l3": l3,
        "source": SOURCE,
        "tags": tags,
        "assets": [f"assets/original/{asset_name}"],
    }


def _write_problem(folder: Path, front: Dict[str, object], q: str, choices: str, answer: str, solution: str) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{q.strip()}\n\n"
        f"## Choices\n{choices.strip()}\n\n"
        f"## Answer\n{answer.strip()}\n\n"
        f"## Solution\n{solution.strip()}\n"
    )
    (folder / "problem.md").write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def main() -> int:
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: Dict[str, str] = {}
    warnings: List[str] = []
    uncertain: List[str] = []
    review_paths: List[str] = []

    # duplicate scan by expected ID set
    for pid in sorted(EXPECTED_IDS):
        if (PROBLEMS / pid).exists():
            summary["skipped"] += 1
            results[pid] = "skipped | duplicate-folder-exists"

    row_map = {row.pid: row for row in ROWS}

    for pid in sorted(EXPECTED_IDS):
        row = row_map.get(pid)
        target = PROBLEMS / pid

        if target.exists():
            continue

        if row is None:
            summary["warnings"] += 1
            warnings.append(f"{pid}: missing-manual-row-data")
            results[pid] = "warning | missing-manual-row-data"
            uncertain.append(pid)
            continue

        crop_path = ROOT / row.crop
        if not crop_path.exists():
            summary["warnings"] += 1
            warnings.append(f"{pid}: missing-crop-file ({row.crop})")
            results[pid] = "warning | missing-crop-file"
            uncertain.append(pid)
            continue

        school, year_i, grade_i, sem_i, exam, source_kind, source_no, source_label = _pid_meta(pid)

        choices_text = "\n".join(row.choices).strip() if row.choices else ""

        classified = classify_unit_and_level(
            question_text=row.q,
            choices_text=choices_text,
            answer_text=row.answer,
            solution_text=row.solution,
            qtype=row.qtype,
            grade=grade_i,
            problem_no=int(pid.rsplit("-", 1)[-1]),
        )
        unit_triplet = normalize_unit_triplet(
            classified.unit_l1,
            classified.unit_l2,
            classified.unit_l3,
            grade=grade_i,
        )
        unit_triplet = UNIT_OVERRIDE.get(pid, unit_triplet)

        asset_name = f"{pid}_original{crop_path.suffix.lower()}"
        assets_original = target / "assets" / "original"
        assets_original.mkdir(parents=True, exist_ok=False)
        shutil.copy2(crop_path, assets_original / asset_name)

        front = _build_front(
            row=row,
            unit=unit_triplet,
            level=classified.level,
            source_no=source_no,
            source_kind=source_kind,
            source_label=source_label,
            asset_name=asset_name,
        )
        _write_problem(target, front, row.q, choices_text, row.answer, row.solution)

        summary["created"] += 1
        reason = f"created | {crop_path.name}"
        if row.uncertain:
            reason += " | ocr-math-review-needed"
            uncertain.append(pid)
        results[pid] = reason
        review_paths.append(str((target / "problem.md").resolve()))

    # Include any manual rows not in expected set
    for pid in sorted(row_map):
        if pid not in EXPECTED_IDS:
            summary["warnings"] += 1
            warnings.append(f"{pid}: manual-row-not-in-expected-set")
            results[pid] = "warning | manual-row-not-in-expected-set"
            uncertain.append(pid)

    lines: List[str] = []
    lines.append("[요약]")
    lines.append(
        f"created={summary['created']}, updated={summary['updated']}, skipped={summary['skipped']}, warnings={summary['warnings']}"
    )
    lines.append("")
    lines.append("[파일별 결과]")
    for pid in sorted(results):
        lines.append(f"{pid} | {results[pid]}")

    lines.append("")
    lines.append("[중복 폴더]")
    dup_ids = [pid for pid in sorted(EXPECTED_IDS) if results.get(pid, "").startswith("skipped")]
    if not dup_ids:
        lines.append("(없음)")
    else:
        lines.extend(dup_ids)

    lines.append("")
    lines.append("[OCR/수식 불확실 문항]")
    if not uncertain:
        lines.append("(없음)")
    else:
        for pid in sorted(set(uncertain)):
            lines.append(pid)

    lines.append("")
    lines.append("[바로 검수할 파일 경로]")
    if not review_paths:
        lines.append("(없음)")
    else:
        for path in sorted(review_paths):
            lines.append(path)

    report_text = "\n".join(lines) + "\n"
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"[REPORT] {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
