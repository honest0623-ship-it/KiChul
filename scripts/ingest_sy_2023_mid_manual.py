from __future__ import annotations

import shutil
from pathlib import Path
import sys
import textwrap
from typing import Any, Dict, List

ROOT = Path(r"d:\Math_Kichul")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level


ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

META = {
    "school": "SY",
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "source": "user_upload_2026-03-04",
    "subjective_offset": 100,
}


def q(text: str) -> str:
    return textwrap.dedent(text).strip()


ROWS: List[Dict[str, Any]] = [
    {
        "source_no": 1,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            두 다항식
            \[
            A=x^2+xy+4y^2,\quad B=2x^2-2xy+y^2
            \]
            에 대하여 \(2A+B\)의 값은?
            """
        ),
        "choices": [
            r"① \(3x^2+9y^2\)",
            r"② \(4x^2+9y^2\)",
            r"③ \(3x^2-xy+5y^2\)",
            r"④ \(3x^2+xy+9y^2\)",
            r"⑤ \(4x^2+xy+9y^2\)",
        ],
        "answer": "②",
        "solution": q(
            r"""
            \[
            2A=2x^2+2xy+8y^2
            \]
            이므로
            \[
            2A+B=(2x^2+2xy+8y^2)+(2x^2-2xy+y^2)=4x^2+9y^2.
            \]
            따라서 정답은 ②이다.
            """
        ),
    },
    {
        "source_no": 2,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            다항식
            \[
            (3x^2-4xy+y^2)(x^2+2xy)
            \]
            의 전개식에서 \(x^3y\)의 계수는?
            """
        ),
        "choices": ["① -4", "② -2", "③ 0", "④ 2", "⑤ 4"],
        "answer": "④",
        "solution": q(
            r"""
            \(x^3y\) 항만 모으면
            \[
            3x^2\cdot 2xy=6x^3y,\quad
            (-4xy)\cdot x^2=-4x^3y
            \]
            이다.
            따라서 계수는
            \[
            6+(-4)=2.
            \]
            정답은 ④이다.
            """
        ),
    },
    {
        "source_no": 3,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            모든 실수 \(x\)에 대하여 등식
            \[
            3x^2+x-1=a(x+1)^2+b(x+1)+c
            \]
            이 성립할 때, 상수 \(a,\ b,\ c\)에 대하여 \(a+b+c\)의 값은?
            """
        ),
        "choices": ["① -1", "② 0", "③ 1", "④ 2", "⑤ 3"],
        "answer": "①",
        "solution": q(
            r"""
            양변을 전개하여 계수를 비교하면
            \[
            a=3,\quad 2a+b=1,\quad a+b+c=-1
            \]
            이다.

            먼저
            \[
            a=3,\quad b=1-2a=1-6=-5
            \]
            이고
            \[
            a+b+c=-1
            \]
            이므로 구하는 값은 바로
            \[
            a+b+c=-1.
            \]
            정답은 ①이다.
            """
        ),
    },
    {
        "source_no": 4,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            다음 <보기> 중 옳은 것만을 있는 대로 고른 것은?

            <보기>

            ㄱ.
            \[
            (2x+3y)^3=8x^3+36x^2y+54xy^2+27y^3
            \]
            ㄴ.
            \[
            (3x+1)(x^2-2x-1)=3x^3+5x^2-5x-1
            \]
            ㄷ.
            \[
            (x-1)(x-2)(x-3)=x^3-6x^2+11x-6
            \]
            ㄹ.
            \[
            (x+2)(x-2)(x+3)(x-3)=x^4-13x^2+36
            \]
            """
        ),
        "choices": ["① ㄱ", "② ㄴ", "③ ㄱ, ㄷ", "④ ㄱ, ㄷ, ㄹ", "⑤ ㄱ, ㄴ, ㄷ, ㄹ"],
        "answer": "④",
        "solution": q(
            r"""
            ㄱ은 \((a+b)^3\) 전개식으로 참이다.

            ㄴ의 좌변을 전개하면
            \[
            (3x+1)(x^2-2x-1)=3x^3-5x^2-5x-1
            \]
            이므로 거짓이다.

            ㄷ은 직접 전개하면 맞다.

            ㄹ은
            \[
            (x+2)(x-2)(x+3)(x-3)=(x^2-4)(x^2-9)=x^4-13x^2+36
            \]
            이므로 참이다.

            따라서 옳은 것은 ㄱ, ㄷ, ㄹ이므로 정답은 ④이다.
            """
        ),
    },
    {
        "source_no": 5,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            \(-1\le x\le 3\)에서 이차함수
            \[
            y=x^2-2x+k
            \]
            의 최솟값이 \(3\)이다. 상수 \(k\)의 값은?
            """
        ),
        "choices": ["① 2", "② 3", "③ 4", "④ 5", "⑤ 6"],
        "answer": "③",
        "solution": q(
            r"""
            \[
            y=x^2-2x+k=(x-1)^2+k-1
            \]
            이고, 꼭짓점 \(x=1\)은 구간 \([-1,3]\) 안에 있다.
            따라서 최솟값은
            \[
            k-1.
            \]
            문제 조건에 의해
            \[
            k-1=3
            \]
            이므로
            \[
            k=4.
            \]
            정답은 ③이다.
            """
        ),
    },
    {
        "source_no": 6,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            다음 중 \(x\)축과의 교점의 개수가 \(2\)개인 이차함수는?
            """
        ),
        "choices": [
            r"① \(y=2x^2-x+5\)",
            r"② \(y=x^2-x+2\)",
            r"③ \(y=x^2+3x+1\)",
            r"④ \(y=x^2-3x+3\)",
            r"⑤ \(y=-4x^2+4x-1\)",
        ],
        "answer": "③",
        "solution": q(
            r"""
            \(x\)축과의 교점이 2개이려면 판별식 \(D>0\)이어야 한다.

            ① \(D=1-40<0\)

            ② \(D=1-8<0\)

            ③ \(D=3^2-4\cdot 1\cdot 1=5>0\)

            ④ \(D=9-12<0\)

            ⑤ \(D=16-16=0\)

            따라서 정답은 ③이다.
            """
        ),
    },
    {
        "source_no": 7,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            이차방정식
            \[
            x^2-4x+2=0
            \]
            의 두 근 \(\alpha,\ \beta\)에 대하여 이차방정식
            \[
            4x^2-ax+b=0
            \]
            의 두 근이 \(\frac{\alpha}{2},\ \frac{\beta}{2}\)일 때,
            상수 \(a,\ b\)에 대하여 \(a+b\)의 값은?
            """
        ),
        "choices": ["① 10", "② 12", "③ 14", "④ 16", "⑤ 18"],
        "answer": "①",
        "solution": q(
            r"""
            \[
            \alpha+\beta=4,\quad \alpha\beta=2
            \]
            이다.

            새 방정식의 근은 \(\frac{\alpha}{2},\ \frac{\beta}{2}\)이므로
            \[
            \frac{\alpha}{2}+\frac{\beta}{2}=2,\quad
            \frac{\alpha\beta}{4}=\frac12.
            \]

            한편 \(4x^2-ax+b=0\)에서
            \[
            \text{근의 합}=\frac{a}{4},\quad
            \text{근의 곱}=\frac{b}{4}.
            \]
            따라서
            \[
            \frac{a}{4}=2\Rightarrow a=8,\quad
            \frac{b}{4}=\frac12\Rightarrow b=2.
            \]
            \[
            a+b=10.
            \]
            정답은 ①이다.
            """
        ),
    },
    {
        "source_no": 8,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            방정식
            \[
            x^2-2x-2=0
            \]
            을 만족하는 두 근 \(\alpha,\ \beta\ (\alpha>\beta)\)에 대하여
            \(\alpha^3-\beta^3\)의 값은?
            """
        ),
        "choices": [
            r"① \(4\sqrt{3}\)",
            r"② \(6\sqrt{3}\)",
            r"③ \(8\sqrt{3}\)",
            r"④ \(10\sqrt{3}\)",
            r"⑤ \(12\sqrt{3}\)",
        ],
        "answer": "⑤",
        "solution": q(
            r"""
            \[
            \alpha+\beta=2,\quad \alpha\beta=-2
            \]
            이고
            \[
            \alpha-\beta=\sqrt{(\alpha+\beta)^2-4\alpha\beta}
            =\sqrt{4+8}=2\sqrt{3}.
            \]

            또한
            \[
            \alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=4+4=8
            \]
            이므로
            \[
            \alpha^2+\alpha\beta+\beta^2=8-2=6.
            \]
            따라서
            \[
            \alpha^3-\beta^3
            =(\alpha-\beta)(\alpha^2+\alpha\beta+\beta^2)
            =2\sqrt{3}\cdot 6
            =12\sqrt{3}.
            \]
            정답은 ⑤이다.
            """
        ),
    },
    {
        "source_no": 9,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            정수 \(a,\ b,\ c,\ d\)에 대하여
            \[
            (x+1)(x+2)(x-3)(x-4)+4=(x^2+ax+b)(x^2+cx+d)
            \]
            일 때, \(a+b+c+d\)의 값은?
            """
        ),
        "choices": ["① -19", "② -18", "③ -17", "④ -16", "⑤ -15"],
        "answer": "⑤",
        "solution": q(
            r"""
            좌변을 전개하면
            \[
            (x+1)(x+2)(x-3)(x-4)+4
            =x^4-4x^3-7x^2+22x+28.
            \]

            \[
            (x^2+ax+b)(x^2+cx+d)
            \]
            에서 계수 비교를 하면
            \[
            a+c=-4,\quad
            ac+b+d=-7,\quad
            ad+bc=22,\quad
            bd=28.
            \]

            대칭성을 보고 \(a=c=-2\)를 대입하면
            \[
            b+d=-11,\quad bd=28
            \]
            이고
            \[
            b,\ d=-7,\ -4
            \]
            (순서 바뀜 가능)이다.

            따라서
            \[
            a+b+c+d=-2-7-2-4=-15.
            \]
            정답은 ⑤이다.
            """
        ),
    },
    {
        "source_no": 10,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            다항식 \(Q(x)\)와 \(0\)이 아닌 상수 \(k\)에 대하여 등식
            \[
            2x^3+19x^2-4x-1=(2x-1)Q(x)+kx+1
            \]
            이 \(x\)에 대한 항등식일 때, \(Q(k)\)의 값은?
            """
        ),
        "choices": ["① 26", "② 32", "③ 38", "④ 44", "⑤ 52"],
        "answer": "①",
        "solution": q(
            r"""
            \(x=\frac12\)를 대입하면 \((2x-1)Q(x)\)가 사라져서
            \[
            2\left(\frac12\right)^3+19\left(\frac12\right)^2-4\left(\frac12\right)-1
            =k\left(\frac12\right)+1
            \]
            \[
            2=\frac{k}{2}+1
            \]
            이므로
            \[
            k=2.
            \]

            이제
            \[
            2x^3+19x^2-4x-1-(2x+1)=2x^3+19x^2-6x-2
            \]
            이고
            \[
            2x^3+19x^2-6x-2=(2x-1)Q(x).
            \]
            나눗셈을 하면
            \[
            Q(x)=x^2+10x+2.
            \]
            따라서
            \[
            Q(k)=Q(2)=2^2+10\cdot 2+2=26.
            \]
            정답은 ①이다.
            """
        ),
    },
    {
        "source_no": 11,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            복소수
            \[
            z=(a+1)+(a-9)i
            \]
            에 대하여
            \[
            z^2+(\overline{z})^2\le 0
            \]
            을 만족하는 자연수 \(a\)의 개수는?
            """
        ),
        "choices": ["① 2", "② 3", "③ 4", "④ 5", "⑤ 6"],
        "answer": "③",
        "solution": q(
            r"""
            \[
            z=x+yi\quad (x=a+1,\ y=a-9)
            \]
            로 두면
            \[
            z^2+(\overline{z})^2
            =(x+yi)^2+(x-yi)^2
            =2(x^2-y^2).
            \]
            따라서 조건은
            \[
            x^2-y^2\le 0
            \]
            즉
            \[
            (a+1)^2\le (a-9)^2.
            \]
            이를 정리하면
            \[
            (a+1)^2-(a-9)^2\le 0
            \]
            \[
            20(a-4)\le 0
            \]
            \[
            a\le 4.
            \]
            자연수 \(a\)는 \(1,2,3,4\)이므로 개수는 \(4\)개이다.
            정답은 ③이다.
            """
        ),
    },
    {
        "source_no": 12,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            다항식
            \[
            x^{10}-x^7+5
            \]
            를 다항식 \(x^2+x+1\)으로 나누었을 때 나머지를 \(ax+b\)라 할 때,
            \(a+b\)의 값은? (단, \(a,\ b\)는 실수)
            """
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        "answer": "⑤",
        "solution": q(
            r"""
            \[
            x^2+x+1=0
            \]
            의 근을 \(\omega\)라 하면 \(\omega^3=1,\ \omega\ne 1\)이다.

            나머지를 \(R(x)=ax+b\)라 하면
            \[
            R(\omega)=\omega^{10}-\omega^7+5.
            \]
            \(\omega^3=1\)이므로
            \[
            \omega^{10}=\omega,\quad \omega^7=\omega
            \]
            이고
            \[
            R(\omega)=5.
            \]
            같은 방식으로 \(\omega^2\)를 넣어도 \(R(\omega^2)=5\)이다.

            따라서 \(R(x)\)는 상수 \(5\)여야 하므로
            \[
            a=0,\quad b=5.
            \]
            \[
            a+b=5.
            \]
            정답은 ⑤이다.
            """
        ),
    },
    {
        "source_no": 13,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            이차함수
            \[
            f(x)=-x^2+mx+n
            \]
            에 대하여 \(f(-2)=f(4)\)이고, 함수 \(f(x)\)의 최댓값이 \(4\)일 때,
            \[
            f(|f(x)|)=0
            \]
            을 만족하는 서로 다른 실근의 합은?
            """
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        "answer": "④",
        "solution": q(
            r"""
            \(f(-2)=f(4)\)이므로 축의 \(x\)좌표는 \(\frac{-2+4}{2}=1\)이다.
            \[
            \frac{m}{2}=1\Rightarrow m=2.
            \]

            최댓값이 \(4\)이므로
            \[
            f(1)=4
            \]
            에서
            \[
            -1+2+n=4\Rightarrow n=3.
            \]
            따라서
            \[
            f(x)=-x^2+2x+3.
            \]

            이제 \(t=|f(x)|\ge 0\)로 두면
            \[
            f(t)=0\Rightarrow -t^2+2t+3=0
            \]
            \[
            t^2-2t-3=0
            \]
            이고 \(t=3\)만 가능하다.
            즉
            \[
            |f(x)|=3.
            \]

            1) \(f(x)=3\):
            \[
            -x^2+2x+3=3\Rightarrow x=0,\ 2
            \]

            2) \(f(x)=-3\):
            \[
            -x^2+2x+3=-3\Rightarrow x^2-2x-6=0
            \]
            \[
            x=1\pm\sqrt{7}
            \]

            서로 다른 실근의 합은
            \[
            0+2+(1+\sqrt{7})+(1-\sqrt{7})=4.
            \]
            정답은 ④이다.
            """
        ),
    },
    {
        "source_no": 14,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            이차함수
            \[
            y=x^2-x+1
            \]
            의 그래프와 직선
            \[
            y=x+n
            \]
            의 그래프가 만나는 서로 다른 두 점의 \(x\)좌표를 각각 \(\alpha,\ \beta\)라 하자.
            \[
            |\alpha|+|\beta|
            \]
            의 값이 자연수가 되도록 하는 \(50\) 이하의 자연수 \(n\)의 합은?
            """
        ),
        "choices": ["① 140", "② 138", "③ 136", "④ 134", "⑤ 132"],
        "answer": "①",
        "solution": q(
            r"""
            교점의 \(x\)좌표는
            \[
            x^2-x+1=x+n
            \]
            \[
            x^2-2x+(1-n)=0
            \]
            의 근이다.
            따라서
            \[
            \alpha=1+\sqrt{n},\quad \beta=1-\sqrt{n}
            \]
            (\(n>0\)에서 서로 다른 두 점)이다.

            \(n=1\)이면 \(\alpha=2,\ \beta=0\)이므로
            \[
            |\alpha|+|\beta|=2
            \]
            는 자연수이다.

            \(n>1\)이면 \(\beta<0\)이므로
            \[
            |\alpha|+|\beta|=(1+\sqrt{n})+(\sqrt{n}-1)=2\sqrt{n}.
            \]
            이 값이 자연수가 되려면 \(\sqrt{n}\)이 정수여야 하므로
            \(n\)은 완전제곱수이다.

            \(50\) 이하의 완전제곱수:
            \[
            1,\ 4,\ 9,\ 16,\ 25,\ 36,\ 49.
            \]
            합은
            \[
            1+4+9+16+25+36+49=140.
            \]
            정답은 ①이다.
            """
        ),
    },
    {
        "source_no": 15,
        "kind": "objective",
        "type": "객관식",
        "question": q(
            r"""
            두 이차함수
            \[
            y=x^2+mx+3,\quad y=-x^2+2x+n
            \]
            의 그래프가 만나지 않을 때,
            자연수 \(m,\ n\)의 순서쌍 \((m,n)\)의 개수는?
            """
        ),
        "choices": ["① 8", "② 9", "③ 10", "④ 11", "⑤ 12"],
        "answer": "②",
        "solution": q(
            r"""
            두 그래프가 만나지 않으려면
            \[
            x^2+mx+3=-x^2+2x+n
            \]
            \[
            2x^2+(m-2)x+(3-n)=0
            \]
            이 실근을 가지지 않아야 하므로 판별식이 음수:
            \[
            (m-2)^2-8(3-n)<0.
            \]
            즉
            \[
            8n<24-(m-2)^2.
            \]

            자연수 \(m\)에 대해 경우를 보면

            \(m=1:\ 8n<23\Rightarrow n=1,2\) (2개)

            \(m=2:\ 8n<24\Rightarrow n=1,2\) (2개)

            \(m=3:\ 8n<23\Rightarrow n=1,2\) (2개)

            \(m=4:\ 8n<20\Rightarrow n=1,2\) (2개)

            \(m=5:\ 8n<15\Rightarrow n=1\) (1개)

            \(m\ge 6\)에서는 가능한 \(n\)이 없다.

            따라서 개수는
            \[
            2+2+2+2+1=9.
            \]
            정답은 ②이다.
            """
        ),
    },
    {
        "source_no": 1,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "question": q(
            r"""
            \[
            \left(\frac{4-3i}{3+4i}\right)^{2023}
            \]
            의 값을 구하시오.
            """
        ),
        "choices": [],
        "answer": "i",
        "solution": q(
            r"""
            먼저
            \[
            \frac{4-3i}{3+4i}
            =\frac{(4-3i)(3-4i)}{(3+4i)(3-4i)}
            =\frac{-25i}{25}
            =-i.
            \]
            따라서
            \[
            \left(\frac{4-3i}{3+4i}\right)^{2023}=(-i)^{2023}.
            \]

            \(2023=4\cdot 505+3\)이므로
            \[
            (-i)^{2023}=(-i)^3=i.
            \]
            따라서 정답은
            \[
            i
            \]
            이다.
            """
        ),
    },
    {
        "source_no": 2,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "question": q(
            r"""
            이차함수
            \[
            f(x)=-x^2+2x+48
            \]
            위의 두 점 \(A(k,f(k))\), \(B(k+6,f(k+6))\)와
            \(x\)축 위의 두 점 \(C(k,0)\), \(D(k+6,0)\)에 대하여
            사각형 \(ABDC\)의 넓이의 최댓값과 그때 \(k\)의 값을 구하시오.
            \(( -6<k<0 )\)
            """
        ),
        "choices": [],
        "answer": "최댓값 240, k=-2",
        "solution": q(
            r"""
            사각형 \(ABDC\)는 서로 평행한 두 변 \(AC,\ BD\)를 갖는 사다리꼴이다.
            \[
            AC=f(k),\quad BD=f(k+6),\quad AC\text{와 }BD\text{ 사이 거리}=6.
            \]
            따라서 넓이 \(S\)는
            \[
            S=\frac{f(k)+f(k+6)}{2}\cdot 6=3\{f(k)+f(k+6)\}.
            \]

            \[
            f(k)=-k^2+2k+48,
            \]
            \[
            f(k+6)=-(k+6)^2+2(k+6)+48=-k^2-10k+24.
            \]
            그러므로
            \[
            S=3(-2k^2-8k+72)
            =-6k^2-24k+216
            \]
            \[
            =-6(k+2)^2+240.
            \]
            따라서 최댓값은
            \[
            240
            \]
            이고, 그때
            \[
            k=-2
            \]
            이다.
            """
        ),
    },
    {
        "source_no": 3,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "question": q(
            r"""
            이차방정식
            \[
            x^2+3x+1=0
            \]
            의 두 근을 \(\alpha,\ \beta\)라 할 때,
            \[
            (\sqrt{\alpha}+\sqrt{\beta})^2
            \]
            의 값을 구하시오.
            (단, 이차방정식의 근과 계수의 관계를 이용하여 풀 것)
            """
        ),
        "choices": [],
        "answer": "-5",
        "solution": q(
            r"""
            근과 계수의 관계로
            \[
            \alpha+\beta=-3,\quad \alpha\beta=1.
            \]

            주어진 식은
            \[
            (\sqrt{\alpha}+\sqrt{\beta})^2
            =\alpha+\beta+2\sqrt{\alpha}\sqrt{\beta}.
            \]
            이차방정식 \(x^2+3x+1=0\)의 두 근은 모두 음수이므로
            \[
            \sqrt{\alpha}=i\sqrt{|\alpha|},\quad
            \sqrt{\beta}=i\sqrt{|\beta|}
            \]
            이고
            \[
            \sqrt{\alpha}\sqrt{\beta}
            =i^2\sqrt{|\alpha||\beta|}
            =-\sqrt{\alpha\beta}
            =-1.
            \]
            따라서
            \[
            (\sqrt{\alpha}+\sqrt{\beta})^2
            =(\alpha+\beta)+2(-1)
            =-3-2=-5.
            \]
            """
        ),
    },
    {
        "source_no": 4,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "question": q(
            r"""
            이차방정식
            \[
            x^2+mx+n=0
            \]
            의 한 근이 \(-2+ai\)이다.
            \(10\) 이하의 두 정수 \(m,\ n\)에 대하여 \(mn\)의 최댓값과 최솟값을 구하시오.
            (단, \(a\ne 0\)인 실수)
            """
        ),
        "choices": [],
        "answer": "40, 20",
        "solution": q(
            r"""
            계수가 실수이므로 다른 한 근은
            \[
            -2-ai
            \]
            이다.

            따라서 두 근의 합과 곱은
            \[
            (-2+ai)+(-2-ai)=-4,\quad
            (-2+ai)(-2-ai)=4+a^2.
            \]
            근과 계수의 관계로
            \[
            -m=-4\Rightarrow m=4,\quad
            n=4+a^2.
            \]

            \(a\ne 0\)이므로 \(a^2>0\), 따라서
            \[
            n>4.
            \]
            또 \(n\)은 \(10\) 이하의 정수이므로
            \[
            n=5,6,7,8,9,10.
            \]
            그러면
            \[
            mn=4n
            \]
            이므로
            \[
            \min mn=4\cdot 5=20,\quad
            \max mn=4\cdot 10=40.
            \]
            """
        ),
    },
    {
        "source_no": 5,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "question": q(
            r"""
            이차함수
            \[
            y=-x^2+kx+2k+5
            \]
            의 그래프는 실수 \(k\)값에 관계없이 항상 점 \(A\)를 지난다.
            점 \(A\)가 이차함수 \(y=-x^2+kx+2k+5\)의 꼭짓점일 때,
            이차함수의 \(x\)절편과 점 \(A\)를 꼭짓점으로 하는 삼각형의 넓이를 구하시오.
            """
        ),
        "choices": [],
        "answer": "[x절편: -3, -1], [삼각형의 넓이=1]",
        "solution": q(
            r"""
            식을
            \[
            y=-x^2+5+k(x+2)
            \]
            로 보면, \(k\)와 무관한 공통점은 \(x+2=0\), 즉 \(x=-2\)일 때이다.
            이때
            \[
            y=-(-2)^2+5=1
            \]
            이므로
            \[
            A(-2,1).
            \]

            점 \(A\)가 꼭짓점이려면 꼭짓점의 \(x\)좌표
            \[
            \frac{k}{2}
            \]
            가 \(-2\)여야 하므로
            \[
            k=-4.
            \]
            따라서 함수는
            \[
            y=-x^2-4x-3.
            \]

            \(x\)절편은
            \[
            -x^2-4x-3=0
            \]
            \[
            x^2+4x+3=0
            \]
            \[
            (x+1)(x+3)=0
            \]
            이므로
            \[
            x=-3,\ -1.
            \]

            삼각형의 꼭짓점은 \((-3,0),\ (-1,0),\ A(-2,1)\)이고,
            밑변 길이 \(2\), 높이 \(1\)이므로 넓이는
            \[
            \frac12\cdot 2\cdot 1=1.
            \]
            """
        ),
    },
]


def build_problem_md(
    *,
    pid: str,
    qtype: str,
    source_no: int,
    source_kind: str,
    source_label: str,
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    level: int,
    question: str,
    choices: List[str],
    answer: str,
    solution: str,
    assets: List[str],
) -> str:
    unit_path = f"{unit_l1}>{unit_l2}>{unit_l3}"
    source_tag = f"출제번호-{source_no}" if source_kind == "objective" else f"출제번호-서답{source_no}"
    lines: List[str] = [
        "---",
        f"id: {pid}",
        f"school: {META['school']}",
        f"year: {META['year']}",
        f"grade: {META['grade']}",
        f"semester: {META['semester']}",
        f"exam: {META['exam']}",
        f"type: {qtype}",
        f"source_question_no: {source_no}",
        f"source_question_kind: {source_kind}",
        f"source_question_label: \"{source_label}\"",
        f"difficulty: {level}",
        f"level: {level}",
        f"unit: \"{unit_path}\"",
        f"unit_l1: \"{unit_l1}\"",
        f"unit_l2: \"{unit_l2}\"",
        f"unit_l3: \"{unit_l3}\"",
        f"source: \"{META['source']}\"",
        "tags:",
        "  - 수동작성",
        f"  - {qtype}",
        f"  - {source_tag}",
        "assets:",
    ]
    lines.extend([f"  - {item}" for item in assets])
    lines.extend(
        [
            "---",
            "",
            "## Q",
            question.strip(),
            "",
            "## Choices",
            "\n".join(choices).strip(),
            "",
            "## Answer",
            answer.strip(),
            "",
            "## Solution",
            solution.strip(),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    originals = sorted(
        [p for p in ORIGINAL.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".webp"}],
        key=lambda p: p.name,
    )

    if not originals:
        raise FileNotFoundError(f"No source files found in {ORIGINAL}")

    target_pdf = None
    for src in originals:
        if src.suffix.lower() == ".pdf":
            target_pdf = src
            break
    if target_pdf is None:
        raise FileNotFoundError("Expected at least one PDF in db/original for this ingest task.")

    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    review_paths: List[str] = []

    for row in ROWS:
        source_no = int(row["source_no"])
        kind = str(row["kind"])
        qtype = str(row["type"])
        problem_no = source_no if kind == "objective" else source_no + int(META["subjective_offset"])
        pid = f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{problem_no:03d}"
        pdir = PROBLEMS / pid

        if pdir.exists():
            summary["skipped"] += 1
            results.append(f"{target_pdf.name} -> {pid} [skipped: folder exists]")
            continue

        question = str(row["question"]).strip()
        choices = [str(item).strip() for item in row["choices"]]
        answer = str(row["answer"]).strip()
        solution = str(row["solution"]).strip()
        choices_text = "\n".join(choices)

        classified = classify_unit_and_level(
            question_text=question,
            choices_text=choices_text,
            answer_text=answer,
            solution_text=solution,
            qtype=qtype,
            grade=int(META["grade"]),
            problem_no=problem_no,
        )

        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)
        copied_name = target_pdf.name
        shutil.copy2(target_pdf, original_dir / copied_name)

        source_label = str(source_no) if kind == "objective" else f"서답{source_no}번"
        md = build_problem_md(
            pid=pid,
            qtype=qtype,
            source_no=source_no,
            source_kind=kind,
            source_label=source_label,
            unit_l1=classified.unit_l1,
            unit_l2=classified.unit_l2,
            unit_l3=classified.unit_l3,
            level=int(classified.level),
            question=question,
            choices=choices,
            answer=answer,
            solution=solution,
            assets=["assets/original/", f"assets/original/{copied_name}"],
        )
        (pdir / "problem.md").write_text(md, encoding="utf-8")

        summary["created"] += 1
        results.append(
            f"{target_pdf.name} -> {pid} [created] "
            f"unit={classified.unit_l3}, level={classified.level}, reason={classified.reason}"
        )
        review_paths.append(str((pdir / "problem.md").resolve()))

    summary["warnings"] = len(warnings)

    report_lines = [
        f"created={summary['created']} updated={summary['updated']} skipped={summary['skipped']} warnings={summary['warnings']}",
        "",
        "[RESULTS]",
    ]
    report_lines.extend(results)
    report_lines.append("")
    report_lines.append("[WARNINGS]")
    report_lines.extend(warnings if warnings else ["(none)"])
    report_lines.append("")
    report_lines.append("[OCR_UNCERTAIN]")
    report_lines.extend(uncertain if uncertain else ["(none)"])
    report_lines.append("")
    report_lines.append("[REVIEW_PATHS]")
    report_lines.extend(review_paths if review_paths else ["(none)"])

    report_path = ROOT / "_tmp_sy_2023_mid_ingest_report.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n".join(report_lines))
    print(f"\nreport: {report_path}")


if __name__ == "__main__":
    main()
