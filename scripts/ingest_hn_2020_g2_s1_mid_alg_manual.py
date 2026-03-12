from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import shutil
import sys

import fitz
from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
REPORT = ROOT / "_tmp_hn_2020_g2_s1_mid_alg_ingest_report.txt"

SOURCE_PDF = ORIGINAL / "HN.2020.G2.S1.MID.ALG.pdf"
SUPPLEMENT_SCAN_103 = ORIGINAL / "HN.2020.G2.S1.MID.ALG.103.png"

META = {
    "school": "HN",
    "year": 2020,
    "grade": 2,
    "semester": 1,
    "exam": "MID",
    "subject": "ALG",
    "source": "user_upload_2026-03-11",
    "created_date": "2026-03-11",
}

# Upright page render policy:
# - page 1,3: rotate -90 deg
# - page 2,4: rotate +90 deg
ROTATE_BY_PAGE: Dict[int, int] = {
    1: -90,
    2: 90,
    3: -90,
    4: 90,
}

# Crop rectangles on upright 3x-rendered pages (x0, y0, x1, y1).
CROPS: Dict[int, Tuple[int, Tuple[int, int, int, int]]] = {
    1: (1, (80, 220, 1085, 1170)),
    2: (1, (80, 1100, 1085, 1560)),
    3: (1, (80, 1480, 1085, 2150)),
    4: (1, (80, 2110, 1085, 3010)),
    5: (1, (1040, 210, 2140, 990)),
    6: (1, (1040, 930, 2140, 1540)),
    7: (1, (1040, 1430, 2140, 2050)),
    8: (1, (1040, 2010, 2140, 3010)),
    9: (2, (80, 220, 1085, 790)),
    10: (2, (80, 720, 1085, 1270)),
    11: (2, (80, 1200, 1085, 1930)),
    12: (2, (80, 1860, 1085, 3010)),
    13: (2, (1040, 220, 2140, 1340)),
    14: (2, (1040, 1250, 2140, 2020)),
    15: (2, (1040, 1940, 2140, 3010)),
    16: (3, (80, 220, 1085, 1250)),
    17: (3, (80, 1160, 1085, 3010)),
    101: (3, (1040, 220, 2140, 980)),
    102: (3, (1040, 900, 2140, 1480)),
    103: (3, (1040, 1400, 2140, 3010)),
    104: (4, (80, 220, 1085, 1500)),
    105: (4, (80, 1430, 1085, 3010)),
    106: (4, (1030, 220, 2160, 3010)),
}

UNCERTAIN_NOTES: Dict[int, str] = {
    6: "선지 ③의 계수(필기 겹침) 판독 불확실",
    103: "그래프의 x축 표기(3π 위치) 해석에 따른 정답 재검토 필요 가능성",
}


def _objective(q: str, choices: List[str], answer: str, solution: str) -> Dict[str, object]:
    return {
        "type": "객관식",
        "q": q,
        "choices": choices,
        "answer": answer,
        "solution": solution,
    }


def _subjective(qtype: str, q: str, answer: str, solution: str) -> Dict[str, object]:
    return {
        "type": qtype,
        "q": q,
        "choices": [],
        "answer": answer,
        "solution": solution,
    }


ENTRIES: Dict[int, Dict[str, object]] = {
    1: _objective(
        q=r"""다음 식의 값이 잘못된 것은? (단, $a\ne0$, $b\ne0$)""",
        choices=[
            r"$a^2a^3=a^5$",
            r"$ab^2\times a^4b^3=a^5b^5$",
            r"$\left(\dfrac{b^2}{a}\right)^3=\dfrac{b^6}{a^3}$",
            r"$a^4b^3\div(ab)^6=\dfrac{1}{a^2b^3}$",
            r"$(ab^2)^{-3}=\dfrac{1}{ab^6}$",
        ],
        answer="⑤",
        solution=r"""⑤에서
\[
(ab^2)^{-3}=a^{-3}b^{-6}=\frac{1}{a^3b^6}
\]
이므로 제시된 식
\[
(ab^2)^{-3}=\frac{1}{ab^6}
\]
은 잘못되었다.

따라서 정답은 ⑤이다.""",
    ),
    2: _objective(
        q=r"""$\sqrt[5]{-243}$의 값을 구하면?""",
        choices=[r"$-1$", r"$-2$", r"$-3$", r"$3i$", r"$i$"],
        answer="③",
        solution=r"""$-243=(-3)^5$이므로
\[
\sqrt[5]{-243}=-3
\]
이다.

따라서 정답은 ③이다.""",
    ),
    3: _objective(
        q=r"""다음 중에서 옳은 것은?""",
        choices=[
            r"$5$의 제곱근은 없다.",
            r"$256$의 네제곱근 중에서 실수인 것은 $4$이다.",
            r"$-64$의 세제곱근은 $-4$뿐이다.",
            r"$n$이 홀수일 때, $-3$의 $n$제곱근 중에서 실수인 것은 $1$개이다.",
            r"$n$이 짝수일 때, $3$의 $n$제곱근 중에서 실수인 것은 없다.",
        ],
        answer="④",
        solution=r"""① $5$의 제곱근은 $\pm\sqrt5$가 있으므로 거짓이다.

② $256$의 네제곱근 중 실수는 $4$, $-4$ 두 개이므로 거짓이다.

③ 세제곱근은 복소수 범위에서 $3$개이므로 거짓이다.

④ $n$이 홀수일 때 $-3$의 $n$제곱근 중 실수는 정확히 $1$개이므로 참이다.

⑤ $n$이 짝수일 때 $3$의 $n$제곱근 중 실수는 $\pm\sqrt[n]{3}$ 두 개이므로 거짓이다.

따라서 정답은 ④이다.""",
    ),
    4: _objective(
        q=r"""$\log_6(3\sqrt2)-\log_6\sqrt3$을 계산하면?""",
        choices=[r"$-1$", r"$0$", r"$\dfrac12$", r"$1$", r"$2$"],
        answer="③",
        solution=r"""\[
\log_6(3\sqrt2)-\log_6\sqrt3
=\log_6\left(\frac{3\sqrt2}{\sqrt3}\right)
=\log_6\sqrt6
\]
\[
=\log_6(6^{1/2})=\frac12
\]
이므로 정답은 ③이다.""",
    ),
    5: _objective(
        q=r"""세기가 $A\ \mathrm{W}$인 전파가 어떤 벽을 통과하면 세기가 $B\ \mathrm{W}$가 될 때, 그 벽의 전파 감소비 $f\ \mathrm{dB}$는
\[
f=10\log\frac{B}{A}
\]
라고 한다. 세기가 $1\ \mathrm{W}$인 전파가 어떤 벽을 통과하면 세기가 $0.302\ \mathrm{W}$가 될 때, 그 벽의 전파 감소비를 구하면? (단, $\log 3.02=0.4800$으로 계산한다.)""",
        choices=[r"$-4.6$", r"$-4.8$", r"$-5.0$", r"$-5.2$", r"$-5.4$"],
        answer="④",
        solution=r"""주어진 식에 $A=1$, $B=0.302$를 대입하면
\[
f=10\log(0.302)
\]
이다.

\[
0.302=3.02\times10^{-1}
\]
이므로
\[
\log(0.302)=\log3.02-1=0.4800-1=-0.5200
\]
따라서
\[
f=10\times(-0.5200)=-5.2
\]
이다.

정답은 ④이다.""",
    ),
    6: _objective(
        q=r"""두 수의 대소 관계가 잘못된 것은?""",
        choices=[
            r"$\sqrt[3]{4}>\sqrt[5]{8}$",
            r"$\left(\dfrac{1}{\sqrt2}\right)^{\frac25}<\left(\dfrac{1}{32}\right)^{\frac14}$",
            r"$2\log_3 5<5\log_9 4$",
            r"$2\log_{\frac13}4<\dfrac13\log_{\frac13}64$",
            r"$\log_2 11<2\log_2(2\sqrt3)$",
        ],
        answer="②",
        solution=r"""①
\[
\sqrt[3]{4}=2^{2/3},\quad \sqrt[5]{8}=2^{3/5}
\]
이고 $2/3>3/5$이므로 참이다.

②
\[
\left(\frac{1}{\sqrt2}\right)^{2/5}=2^{-1/5},\quad
\left(\frac{1}{32}\right)^{1/4}=2^{-5/4}
\]
인데 $-1/5>-5/4$이므로
\[
2^{-1/5}>2^{-5/4}
\]
이다. 따라서 제시 부등식은 거짓이다.

③
\[
2\log_3 5\approx2.93,\quad 5\log_9 4\approx3.15
\]
이므로 참이다.

④
\[
\frac13\log_{\frac13}64
=\frac13\log_{\frac13}(4^3)
=\log_{\frac13}4
\]
이고 $\log_{\frac13}4<0$이므로
\[
2\log_{\frac13}4<\log_{\frac13}4
\]
가 되어 참이다.

⑤
\[
2\log_2(2\sqrt3)=\log_2(12)
\]
이고 $11<12$이므로
\[
\log_2 11<\log_2 12
\]
가 되어 참이다.

따라서 잘못된 것은 ②이다.""",
    ),
    7: _objective(
        q=r"""방정식
\[
0.2^{x-1}=\frac{1}{\sqrt[3]{25}}
\]
의 해를 구하면?""",
        choices=[r"$\dfrac13$", r"$\dfrac23$", r"$\dfrac53$", r"$\dfrac34$", r"$\dfrac15$"],
        answer="③",
        solution=r"""\[
0.2=\frac15=5^{-1}
\]
이므로
\[
0.2^{x-1}=5^{1-x}
\]
이다.

또
\[
\frac{1}{\sqrt[3]{25}}=25^{-1/3}=5^{-2/3}
\]
이므로
\[
5^{1-x}=5^{-2/3}
\Rightarrow 1-x=-\frac23
\Rightarrow x=\frac53
\]
이다.

정답은 ③이다.""",
    ),
    8: _objective(
        q=r"""부등식
\[
\log_{\frac15}(2x+1)\ge\log_{\frac15}(3x-2)
\]
의 해를 구하면?""",
        choices=[
            r"$x\ge3$",
            r"$x\le-3$",
            r"$x\ge-2$",
            r"$x\ge1$",
            r"$x\le1$",
        ],
        answer="①",
        solution=r"""정의역 조건은
\[
2x+1>0,\quad 3x-2>0
\]
이므로
\[
x>-\frac12,\quad x>\frac23
\Rightarrow x>\frac23
\]
이다.

밑이 $\dfrac15(<1)$이므로 로그함수는 감소함수이다.
따라서
\[
\log_{\frac15}(2x+1)\ge\log_{\frac15}(3x-2)
\Rightarrow 2x+1\le3x-2
\Rightarrow x\ge3
\]
이다.

정의역과 합치면 $x\ge3$.
정답은 ①이다.""",
    ),
    9: _objective(
        q=r"""함수 $f(x)=a^x-a^{-x}$ ($a>0$, $a\ne1$)과 실수 $k$에 대하여
\[
f(k)=2
\]
일 때, $f(2k)$를 구하면?""",
        choices=[r"$\sqrt2$", r"$2\sqrt2$", r"$3\sqrt2$", r"$4\sqrt2$", r"$5\sqrt2$"],
        answer="④",
        solution=r"""$u=a^k$라 두면 $u>0$이고
\[
u-\frac1u=2
\]
이다.

따라서
\[
u^2-2u-1=0
\]
이고 $u=1+\sqrt2$ (양수이므로)이다.
그러면
\[
\frac1u=\sqrt2-1
\]
이다.

\[
f(2k)=a^{2k}-a^{-2k}
=u^2-\frac1{u^2}
=\left(u-\frac1u\right)\left(u+\frac1u\right)
\]
\[
=2\left((1+\sqrt2)+(\sqrt2-1)\right)
=2(2\sqrt2)=4\sqrt2
\]
이므로 정답은 ④이다.""",
    ),
    10: _objective(
        q=r"""부등식
\[
3^{2x+1}-28\times3^x+9\le0
\]
을 만족시키는 정수 $x$의 값으로 옳지 않은 것은?""",
        choices=[r"$-2$", r"$-1$", r"$0$", r"$1$", r"$2$"],
        answer="①",
        solution=r"""$t=3^x$ ($t>0$)라 두면
\[
3t^2-28t+9\le0
\]
이다.

방정식 $3t^2-28t+9=0$의 근은
\[
t=\frac{28\pm\sqrt{28^2-4\cdot3\cdot9}}{6}
=\frac{28\pm26}{6}
\]
이므로
\[
t=\frac13,\ 9
\]
이다.

따라서
\[
\frac13\le t\le9
\Rightarrow \frac13\le3^x\le9
\Rightarrow -1\le x\le2
\]
이다.

정수해는 $-1,0,1,2$이고, 옳지 않은 값은 $-2$이다.
정답은 ①이다.""",
    ),
    11: _objective(
        q=r"""반지름의 길이가 $6\ \mathrm{cm}$, 중심각의 크기가 $\dfrac{\pi}{3}$인 부채꼴의 호의 길이와 넓이를 구하면?""",
        choices=[
            r"호의 길이: $2\pi\ \mathrm{cm}$, 넓이: $3\pi\ \mathrm{cm}^2$",
            r"호의 길이: $2\pi\ \mathrm{cm}$, 넓이: $6\pi\ \mathrm{cm}^2$",
            r"호의 길이: $3\pi\ \mathrm{cm}$, 넓이: $3\pi\ \mathrm{cm}^2$",
            r"호의 길이: $3\pi\ \mathrm{cm}$, 넓이: $6\pi\ \mathrm{cm}^2$",
            r"호의 길이: $6\pi\ \mathrm{cm}$, 넓이: $3\pi\ \mathrm{cm}^2$",
        ],
        answer="②",
        solution=r"""호의 길이는
\[
\ell=r\theta=6\cdot\frac{\pi}{3}=2\pi\ (\mathrm{cm})
\]
이고,

넓이는
\[
S=\frac12r^2\theta
=\frac12\cdot36\cdot\frac{\pi}{3}
=6\pi\ (\mathrm{cm}^2)
\]
이다.

따라서 정답은 ②이다.""",
    ),
    12: _objective(
        q=r"""\[
\pi<\theta<\frac{3\pi}{2}
\]
이고 $\cos\theta=-\dfrac{5}{13}$일 때, $\sin\theta$, $\tan\theta$의 값을 구하면?""",
        choices=[
            r"$\sin\theta=-\dfrac{13}{12},\ \tan\theta=\dfrac{12}{5}$",
            r"$\sin\theta=\dfrac{12}{13},\ \tan\theta=\dfrac{12}{5}$",
            r"$\sin\theta=-\dfrac{12}{13},\ \tan\theta=\dfrac{5}{12}$",
            r"$\sin\theta=-\dfrac{12}{13},\ \tan\theta=-\dfrac{12}{5}$",
            r"$\sin\theta=-\dfrac{12}{13},\ \tan\theta=\dfrac{12}{5}$",
        ],
        answer="⑤",
        solution=r"""$\pi<\theta<\dfrac{3\pi}{2}$이므로 제3사분면에서
\[
\sin\theta<0,\ \cos\theta<0,\ \tan\theta>0
\]
이다.

\[
\sin\theta
=-\sqrt{1-\cos^2\theta}
=-\sqrt{1-\left(-\frac5{13}\right)^2}
=-\sqrt{\frac{144}{169}}
=-\frac{12}{13}
\]
이다.

\[
\tan\theta=\frac{\sin\theta}{\cos\theta}
=\frac{-12/13}{-5/13}
=\frac{12}{5}
\]
이므로 정답은 ⑤이다.""",
    ),
    13: _objective(
        q=r"""$0\le x<2\pi$일 때, 부등식
\[
\sqrt2\sin x<1
\]
을 풀면?""",
        choices=[
            r"$0\le x<\dfrac{\pi}{4}$ 또는 $\dfrac{3\pi}{4}<x<2\pi$",
            r"$0\le x\le\dfrac{\pi}{4}$ 또는 $\dfrac{7\pi}{4}\le x<2\pi$",
            r"$0\le x<\dfrac{\pi}{4}$ 또는 $\dfrac{5\pi}{4}\le x<2\pi$",
            r"$0\le x\le\dfrac{\pi}{4}$ 또는 $\dfrac{3\pi}{4}<x<2\pi$",
            r"$0\le x<\dfrac{\pi}{4}$ 또는 $\dfrac{7\pi}{4}<x<2\pi$",
        ],
        answer="①",
        solution=r"""부등식은
\[
\sin x<\frac{1}{\sqrt2}=\frac{\sqrt2}{2}
\]
와 같다.

$0\le x<2\pi$에서
\[
\sin x=\frac{\sqrt2}{2}
\]
가 되는 점은
\[
x=\frac{\pi}{4},\ \frac{3\pi}{4}
\]
이다.

\[
\sin x\ge\frac{\sqrt2}{2}
\]
인 구간이
\[
\frac{\pi}{4}\le x\le\frac{3\pi}{4}
\]
이므로, 이를 제외하면
\[
0\le x<\frac{\pi}{4}
\quad\text{또는}\quad
\frac{3\pi}{4}<x<2\pi
\]
이다.

정답은 ①이다.""",
    ),
    14: _objective(
        q=r"""$0\le x<2\pi$일 때, 방정식
\[
\cos x=\frac13
\]
의 모든 근의 합을 구하면?""",
        choices=[r"$\dfrac{\pi}{2}$", r"$\pi$", r"$\dfrac{3\pi}{2}$", r"$2\pi$", r"$3\pi$"],
        answer="④",
        solution=r"""$\cos x=\dfrac13$의 해를
\[
x=\alpha,\ 2\pi-\alpha
\]
($0<\alpha<\pi$)라 두면 두 근의 합은
\[
\alpha+(2\pi-\alpha)=2\pi
\]
이다.

따라서 정답은 ④이다.""",
    ),
    15: _objective(
        q=r"""$0$이 아닌 두 실수 $x$, $y$에 대하여
\[
2^x+2^y=3-p,\quad x+y=0
\]
일 때,
\[
\left(1+p\times2^x+2^{2x}\right)\left(1+p\times2^y+2^{2y}\right)
\]
의 값은? (단, $p$는 상수이다.)""",
        choices=[r"$6$", r"$7$", r"$8$", r"$9$", r"$10$"],
        answer="④",
        solution=r"""$a=2^x$라 두면 $a>0$이고, $x+y=0$에서
\[
2^y=2^{-x}=\frac1a
\]
이다.

또
\[
a+\frac1a=3-p
\Rightarrow p=3-\left(a+\frac1a\right)
\]
이다.

첫째 괄호는
\[
1+pa+a^2
=1+a\left(3-\left(a+\frac1a\right)\right)+a^2
=1+3a-a^2-1+a^2
=3a
\]
이고,

둘째 괄호는
\[
1+\frac{p}{a}+\frac1{a^2}
=3\cdot\frac1a
\]
이다.

따라서 전체 값은
\[
3a\cdot\frac3a=9
\]
이므로 정답은 ④이다.""",
    ),
    16: _objective(
        q=r"""정의역 $\{x\mid1\le x\le4\}$인 함수
\[
f(x)=9\times x^{-4+\log_3 x^2}
\]
의 최댓값을 $M$, 최솟값을 $m$이라 할 때, $M-m$의 값은?""",
        choices=[r"$4$", r"$5$", r"$6$", r"$7$", r"$8$"],
        answer="⑤",
        solution=r"""$x=3^t$라 두면 $t=\log_3x$이고
\[
0\le t\le\log_34
\]
이다.

\[
\log_3x^2=2\log_3x=2t
\]
이므로
\[
f(x)=9(3^t)^{-4+2t}
=3^2\cdot3^{-4t+2t^2}
=3^{2(t-1)^2}
\]
이다.

따라서 $f(x)$의 최소는 $(t-1)^2$가 최소일 때이며 $t=1$에서
\[
m=3^0=1
\]
이다.

최대는 구간 끝점에서 비교하면
\[
t=0\Rightarrow f=3^2=9,\quad
t=\log_34\Rightarrow f<9
\]
이므로
\[
M=9
\]
이다.

따라서
\[
M-m=9-1=8
\]
이고 정답은 ⑤이다.""",
    ),
    17: _objective(
        q=r"""실수 전체의 집합에서 정의된 함수 $f(x)$가 모든 실수 $x$에 대하여
\[
f(\sin x)=\cos4x
\]
를 만족시킬 때,
\[
f(\sin x)+f(\cos x)=1
\]
을 만족시키는 양수 $x$의 최솟값은?""",
        choices=[r"$\dfrac{\pi}{8}$", r"$\dfrac{\pi}{12}$", r"$\dfrac{\pi}{16}$", r"$\dfrac{\pi}{20}$", r"$\dfrac{\pi}{24}$"],
        answer="②",
        solution=r"""모든 실수 $u$에 대하여
\[
f(u)=1-8u^2+8u^4
\]
로 둘 수 있다. (왜냐하면 $\cos4x=1-8\sin^2x+8\sin^4x$)

따라서
\[
f(\sin x)=\cos4x
\]
이고,
\[
f(\cos x)=1-8\cos^2x+8\cos^4x=\cos4x
\]
이다.

주어진 식은
\[
2\cos4x=1
\Rightarrow \cos4x=\frac12
\]
가 된다.

따라서
\[
4x=\frac{\pi}{3},\ \frac{5\pi}{3},\dots
\]
이므로 양의 최소값은
\[
x=\frac{\pi}{12}
\]
이다.

정답은 ②이다.""",
    ),
    101: _subjective(
        qtype="단답형",
        q=r"""\[
\left(\sqrt[6]{27}\right)^2
\]
의 식을 간단히 하시오.""",
        answer=r"$3$",
        solution=r"""\[
\left(\sqrt[6]{27}\right)^2
=(27^{1/6})^2
=27^{1/3}
=3
\]
이다.""",
    ),
    102: _subjective(
        qtype="단답형",
        q=r"""\[
\sin\theta=\frac35,\quad \cos\theta=\frac45
\]
일 때,
\[
\tan\left(\frac{\pi}{2}-\theta\right)
\]
의 값을 구하시오.""",
        answer=r"$\dfrac{4}{3}$",
        solution=r"""\[
\tan\left(\frac{\pi}{2}-\theta\right)=\cot\theta=\frac{\cos\theta}{\sin\theta}
\]
이므로
\[
\tan\left(\frac{\pi}{2}-\theta\right)
=\frac{4/5}{3/5}
=\frac43
\]
이다.""",
    ),
    103: _subjective(
        qtype="단답형",
        q=r"""다음 그림은
\[
y=a\cos(bx+c)-1
\]
의 그래프이다. 주기를 $p\pi$라 할 때,
\[
\frac{p}{abc}
\]
의 값을 구하여라. (단, $a>0$, $b>0$, $0<c<\pi$)

<img src="assets/scan.png" alt="문항 삽화" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        answer=r"$\dfrac{24}{\pi}$",
        solution=r"""그래프의 최댓값이 $1$, 최솟값이 $-3$이므로
\[
a=2
\]
이다.

그래프에서
\[
x=\frac{\pi}{3}\ \text{에서 }y=0,\qquad x=3\pi\ \text{에서 }y=0
\]
이며 두 점에서 기울기 부호가 반대이므로
\[
b\left(3\pi-\frac{\pi}{3}\right)=\frac{4\pi}{3}
\Rightarrow b=\frac12
\]
이다.

또 $x=-\dfrac{\pi}{3}$에서 꼭댓점을 가지므로
\[
b\left(-\frac{\pi}{3}\right)+c=0
\Rightarrow c=\frac{\pi}{6}
\]
이다.

주기 $T$는
\[
T=\frac{2\pi}{b}=4\pi
\]
이므로 $p=4$.

따라서
\[
\frac{p}{abc}
=\frac{4}{2\cdot\frac12\cdot\frac{\pi}{6}}
=\frac{24}{\pi}
\]
이다.""",
    ),
    104: _subjective(
        qtype="서술형",
        q=r"""\[
\log 4.28=0.6314
\]
일 때, 다음 값을 구하시오.

(1) $\log 4280$

(2) $\log 42.8$

(3) $\log x=-1.3686$인 $x$의 값""",
        answer=r"""$(1)\ 3.6314,\ (2)\ 1.6314,\ (3)\ 0.0428$""",
        solution=r"""(1)
\[
\log4280=\log(4.28\times10^3)=\log4.28+\log10^3
=0.6314+3=3.6314
\]

(2)
\[
\log42.8=\log(4.28\times10)
=\log4.28+\log10
=0.6314+1=1.6314
\]

(3)
\[
\log x=-1.3686
\Rightarrow x=10^{-1.3686}
=10^{-2}\cdot10^{0.6314}
=0.01\cdot4.28
=0.0428
\]
이다.""",
    ),
    105: _subjective(
        qtype="서술형",
        q=r"""\[
\sin\theta+\cos\theta=\sqrt2
\]
일 때, 다음 식의 값을 구하시오.

(1) $\sin\theta\cos\theta$

(2) $\tan\theta+\dfrac{1}{\tan\theta}$

(3) $\sin^3\theta+\cos^3\theta$""",
        answer=r"""$(1)\ \dfrac12,\ (2)\ 2,\ (3)\ \dfrac{\sqrt2}{2}$""",
        solution=r"""주어진 식을 제곱하면
\[
(\sin\theta+\cos\theta)^2=2
\]
\[
\sin^2\theta+\cos^2\theta+2\sin\theta\cos\theta=2
\]
\[
1+2\sin\theta\cos\theta=2
\Rightarrow \sin\theta\cos\theta=\frac12
\]

(1)
\[
\sin\theta\cos\theta=\frac12
\]

(2)
\[
\tan\theta+\frac1{\tan\theta}
=\frac{\sin\theta}{\cos\theta}+\frac{\cos\theta}{\sin\theta}
=\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}
=\frac{1}{1/2}=2
\]

(3)
\[
\sin^3\theta+\cos^3\theta
=(\sin\theta+\cos\theta)^3-3\sin\theta\cos\theta(\sin\theta+\cos\theta)
\]
\[
=(\sqrt2)^3-3\cdot\frac12\cdot\sqrt2
=2\sqrt2-\frac{3\sqrt2}{2}
=\frac{\sqrt2}{2}
\]
이다.""",
    ),
    106: _subjective(
        qtype="서술형",
        q=r"""$x>0$에 대한 방정식
\[
(\log_2 x)^2-\log_2 x^2+a=0
\]
의 한 근이 방정식
\[
4x^2-9x+2=0
\]
의 두 근 사이에 존재할 때, 상수 $a$의 값의 범위를 구하여라.""",
        answer=r"""$-8<a<1$""",
        solution=r"""먼저
\[
4x^2-9x+2=0
\]
의 근은
\[
x=\frac{9\pm\sqrt{81-32}}{8}
=\frac{9\pm7}{8}
\]
이므로
\[
\frac14,\ 2
\]
이다.

주어진 조건은 첫 번째 방정식의 근 중 하나가
\[
\frac14<x<2
\]
를 만족한다는 뜻이다.

$t=\log_2x$로 두면
\[
\log_2x^2=2\log_2x=2t
\]
이므로 식은
\[
t^2-2t+a=0
\]
가 된다.

또
\[
\frac14<x<2
\]
는
\[
-2<t<1
\]
와 같다.

이차방정식의 근은
\[
t=1\pm\sqrt{1-a}
\]
인데, $1+\sqrt{1-a}>1$이므로 구간 $(-2,1)$ 안에 들어갈 수 있는 근은
\[
t_1=1-\sqrt{1-a}
\]
뿐이다.

따라서
\[
-2<t_1<1
\]
이어야 하므로
\[
-2<1-\sqrt{1-a}
\Rightarrow \sqrt{1-a}<3
\Rightarrow a>-8
\]
그리고
\[
1-\sqrt{1-a}<1
\Rightarrow \sqrt{1-a}>0
\Rightarrow a<1
\]
이다.

따라서
\[
-8<a<1
\]
이다.""",
    ),
}


def _pid(no: int) -> str:
    return f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{META['subject']}-{no:03d}"


def _source_fields(no: int) -> Tuple[int, str, str, str]:
    if no < 100:
        return no, "objective", str(no), f"{META['school']}.{META['year']}.G{META['grade']}.S{META['semester']}.{META['exam']}.{META['subject']}.{no:03d}.question.png"
    idx = no - 100
    return idx, "subjective", f"서답{idx}", f"{META['school']}.{META['year']}.G{META['grade']}.S{META['semester']}.{META['exam']}.{META['subject']}.SUB{idx:02d}.question.png"


def _build_choices(choices: List[str]) -> str:
    if not choices:
        return ""
    marks = ["①", "②", "③", "④", "⑤"]
    return "\n".join([f"{marks[idx]} {line}" for idx, line in enumerate(choices)])


def _render_upright_pages() -> Dict[int, Image.Image]:
    pages: Dict[int, Image.Image] = {}
    doc = fitz.open(SOURCE_PDF)
    try:
        for page_no in range(1, doc.page_count + 1):
            page = doc[page_no - 1]
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            rot = ROTATE_BY_PAGE.get(page_no, 0)
            if rot:
                img = img.rotate(rot, expand=True)
            pages[page_no] = img
    finally:
        doc.close()
    return pages


def _write_question_crop(pages: Dict[int, Image.Image], no: int, out_path: Path) -> None:
    page_no, box = CROPS[no]
    x0, y0, x1, y1 = box
    page_img = pages[page_no]
    x0 = max(0, min(x0, page_img.width - 1))
    y0 = max(0, min(y0, page_img.height - 1))
    x1 = max(x0 + 1, min(x1, page_img.width))
    y1 = max(y0 + 1, min(y1, page_img.height))
    page_img.crop((x0, y0, x1, y1)).save(out_path)


def main() -> int:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"source-pdf-not-found: {SOURCE_PDF}")

    numbers = list(range(1, 18)) + list(range(101, 107))
    pages = _render_upright_pages()

    results: List[Tuple[str, str, str]] = []
    duplicate_dirs: List[str] = []
    warnings: List[str] = []
    review_paths: List[str] = []
    uncertain_rows: List[str] = []

    for no in numbers:
        pid = _pid(no)
        pdir = PROBLEMS / pid
        md_path = pdir / "problem.md"
        if pdir.exists():
            results.append((pid, "SKIPPED_DUPLICATE", "existing-folder"))
            duplicate_dirs.append(str(pdir))
            if no in UNCERTAIN_NOTES:
                uncertain_rows.append(f"{pid} | {UNCERTAIN_NOTES[no]}")
            continue

        pdir.mkdir(parents=True, exist_ok=True)
        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        source_no, source_kind, source_label, q_asset_name = _source_fields(no)
        q_asset_rel = f"assets/original/{q_asset_name}"
        q_asset_path = original_dir / q_asset_name
        _write_question_crop(pages=pages, no=no, out_path=q_asset_path)

        assets: List[str] = ["assets/original/", q_asset_rel]

        if no == 103:
            if SUPPLEMENT_SCAN_103.exists():
                shutil.copy2(SUPPLEMENT_SCAN_103, assets_dir / "scan.png")
                shutil.copy2(SUPPLEMENT_SCAN_103, original_dir / SUPPLEMENT_SCAN_103.name)
                assets.insert(0, "assets/scan.png")
                assets.append(f"assets/original/{SUPPLEMENT_SCAN_103.name}")
            else:
                warnings.append(f"{pid}: supplemental-scan-missing: {SUPPLEMENT_SCAN_103.name}")

        entry = ENTRIES[no]
        qtype = str(entry["type"])
        q_text = str(entry["q"]).strip()
        choices_list = list(entry["choices"])
        choices_text = _build_choices(choices_list).strip()
        answer_text = str(entry["answer"]).strip()
        solution_text = str(entry["solution"]).strip()

        cls = classify_unit_and_level(
            question_text=q_text,
            choices_text=choices_text,
            answer_text=answer_text,
            solution_text=solution_text,
            qtype=qtype,
            grade=META["grade"],
            problem_no=no,
        )

        tags = [
            "수동생성",
            "PDF",
            qtype,
            f"출제번호-{source_label}",
            f"과목-{META['subject']}",
            f"생성일-{META['created_date']}",
        ]

        front = {
            "id": pid,
            "school": META["school"],
            "year": META["year"],
            "grade": META["grade"],
            "semester": META["semester"],
            "exam": META["exam"],
            "subject": META["subject"],
            "type": qtype,
            "source_question_no": source_no,
            "source_question_kind": source_kind,
            "source_question_label": source_label,
            "difficulty": cls.level,
            "level": cls.level,
            "unit": cls.unit_path,
            "unit_l1": cls.unit_l1,
            "unit_l2": cls.unit_l2,
            "unit_l3": cls.unit_l3,
            "source": META["source"],
            "tags": tags,
            "assets": assets,
        }

        front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
        body = (
            f"## Q\n{q_text}\n\n"
            f"## Choices\n{choices_text}\n\n"
            f"## Answer\n{answer_text}\n\n"
            f"## Solution\n{solution_text}\n"
        )
        md = f"---\n{front_text}\n---\n\n{body}"
        md_path.write_text(md, encoding="utf-8")

        results.append((pid, "CREATED", q_asset_name))
        review_paths.append(str(md_path))
        if no in UNCERTAIN_NOTES:
            uncertain_rows.append(f"{pid} | {UNCERTAIN_NOTES[no]}")

    created = sum(1 for _, status, _ in results if status == "CREATED")
    skipped = sum(1 for _, status, _ in results if status == "SKIPPED_DUPLICATE")

    lines: List[str] = []
    lines.append("[SUMMARY]")
    lines.append(f"created={created}")
    lines.append("updated=0")
    lines.append(f"skipped={skipped}")
    lines.append(f"warnings={len(warnings)}")
    lines.append("")
    lines.append("[DUPLICATE_DIRS]")
    if duplicate_dirs:
        lines.extend(duplicate_dirs)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[DETAIL]")
    lines.extend([f"{pid} | {status} | {note}" for pid, status, note in results])
    lines.append("")
    lines.append("[UNCERTAIN_OCR_OR_MATH]")
    if uncertain_rows:
        lines.extend(uncertain_rows)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[WARNINGS]")
    if warnings:
        lines.extend(warnings)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[REVIEW_PATHS]")
    if review_paths:
        lines.extend(review_paths)
    else:
        lines.append("(none)")
    lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"[DONE] created={created} skipped={skipped} warnings={len(warnings)}")
    print(f"[DUPLICATES] {len(duplicate_dirs)}")
    print(f"[UNCERTAIN] {len(uncertain_rows)}")
    print(f"[REPORT] {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
