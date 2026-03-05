from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(r"d:\Math_Kichul")
ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

META = {
    "school": "JEW",
    "year": 2023,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "source": "user_upload_2026-03-04",
    "subjective_offset": 100,
}

UNIT_MAP: Dict[str, Tuple[str, str, str]] = {
    "1-1. 다항식의 연산": ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산"),
    "1-2. 나머지정리": ("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리"),
    "1-3. 인수분해": ("공통수학1(2022개정)", "1. 다항식", "1-3. 인수분해"),
    "2-1. 복소수와 이차방정식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식"),
    "2-2. 이차방정식과 이차함수": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수"),
    "2-3. 여러 가지 방정식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식"),
    "2-4. 여러 가지 부등식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식"),
}


def q(text: str) -> str:
    return text.strip()


ROWS: List[Dict[str, Any]] = [
    {
        "filename": "005_2-1. 복소수와 이차방정식.png",
        "source_no": 5,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "2-1. 복소수와 이차방정식",
        "level": 2,
        "question": q(
            r"""
            \[
            \sqrt{-5}\sqrt{-5}+\sqrt{7}\sqrt{-7}+\frac{\sqrt{12}}{\sqrt{-3}}=a+bi
            \]
            일 때, 실수 \(a,\ b\)에 대하여 \(b-a\)의 값은?
            """
        ),
        "choices": ["① 6", "② 8", "③ 10", "④ 12", "⑤ 14"],
        "answer": "③",
        "solution": q(
            r"""
            \[
            \sqrt{-5}=i\sqrt{5},\quad \sqrt{-7}=i\sqrt{7},\quad \sqrt{-3}=i\sqrt{3}
            \]
            이므로
            \[
            \sqrt{-5}\sqrt{-5}=(i\sqrt{5})^2=-5,
            \]
            \[
            \sqrt{7}\sqrt{-7}=\sqrt{7}\cdot i\sqrt{7}=7i,
            \]
            \[
            \frac{\sqrt{12}}{\sqrt{-3}}
            =\frac{2\sqrt{3}}{i\sqrt{3}}
            =\frac{2}{i}
            =-2i.
            \]
            따라서
            \[
            -5+7i-2i=-5+5i=a+bi
            \]
            이고
            \[
            a=-5,\quad b=5
            \]
            이므로
            \[
            b-a=5-(-5)=10.
            \]
            정답은 ③이다.
            """
        ),
    },
    {
        "filename": "011_2-3. 여러 가지 방정식.png",
        "source_no": 11,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "2-3. 여러 가지 방정식",
        "level": 3,
        "question": q(
            r"""
            연립방정식
            \[
            \begin{cases}
            x+y=k\\
            x^2+y^2=4
            \end{cases}
            \]
            가 오직 한 쌍의 해를 갖도록 하는 양수 \(k\)의 값은?
            """
        ),
        "choices": ["① 1", r"② \(\sqrt{2}\)", r"③ \(\sqrt{3}\)", "④ 2", r"⑤ \(2\sqrt{2}\)"],
        "answer": "⑤",
        "solution": q(
            r"""
            \[
            x^2+y^2=4
            \]
            는 중심이 원점이고 반지름이 \(2\)인 원이고,
            \[
            x+y=k
            \]
            는 직선이다.

            해가 오직 한 쌍이라는 것은 직선이 원에 접한다는 뜻이다.

            원점에서 직선 \(x+y-k=0\)까지의 거리는
            \[
            \frac{|k|}{\sqrt{1^2+1^2}}=\frac{k}{\sqrt{2}}
            \]
            (양수 \(k\)) 이다.

            접할 조건은
            \[
            \frac{k}{\sqrt{2}}=2
            \]
            이므로
            \[
            k=2\sqrt{2}.
            \]
            정답은 ⑤이다.
            """
        ),
    },
    {
        "filename": "014_2-3. 여러 가지 부등식.png",
        "source_no": 14,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "2-4. 여러 가지 부등식",
        "level": 3,
        "question": q(
            r"""
            이차방정식
            \[
            ax^2+2ax-20=0
            \]
            의 한 근이 이차방정식
            \[
            x^2-3x+2=0
            \]
            의 두 근 사이에 존재하도록 하는 모든 자연수 \(a\)의 값의 합은?
            """
        ),
        "choices": ["① 12", "② 15", "③ 18", "④ 20", "⑤ 25"],
        "answer": "③",
        "solution": q(
            r"""
            \[
            x^2-3x+2=0
            \]
            의 두 근은 \(1,\ 2\)이므로, 첫째 방정식의 한 근이 \(1\)과 \(2\) 사이에 있어야 한다.

            \[
            ax^2+2ax-20=0\quad (a>0)
            \]
            의 근은
            \[
            x=-1\pm\sqrt{1+\frac{20}{a}}
            \]
            이고, 양의 근은
            \[
            -1+\sqrt{1+\frac{20}{a}}
            \]
            이다.

            조건은
            \[
            1<-1+\sqrt{1+\frac{20}{a}}<2
            \]
            이므로
            \[
            2<\sqrt{1+\frac{20}{a}}<3
            \]
            \[
            4<1+\frac{20}{a}<9
            \]
            \[
            3<\frac{20}{a}<8.
            \]
            따라서
            \[
            \frac{20}{8}<a<\frac{20}{3}
            \]
            이고 자연수 \(a\)는
            \[
            a=3,4,5,6.
            \]
            합은
            \[
            3+4+5+6=18.
            \]
            정답은 ③이다.
            """
        ),
    },
    {
        "filename": "015_1-2. 나머지정리.png",
        "source_no": 15,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "1-2. 나머지정리",
        "level": 3,
        "question": q(
            r"""
            두 다항식 \(A(x),\ B(x)\)에 대하여 \(A(x)\)를 \(x^2-1\)로 나눈 몫이 \(Q_1(x)\), 나머지가 \(2x+3\)이고,
            \(B(x)\)를 \(2(x^2-1)\)로 나눈 몫이 \(Q_2(x)\), 나머지가 \(x-2\)일 때,
            두 다항식의 곱 \(A(x)B(x)\)를 \(x^2-1\)로 나눈 나머지를 \(R(x)\)라 하자.
            \(R(-5)\)의 값은?
            """
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        "answer": "①",
        "solution": q(
            r"""
            \[
            A(x)\equiv 2x+3\pmod{x^2-1}
            \]
            이므로
            \[
            A(1)=5,\quad A(-1)=1.
            \]

            또
            \[
            B(x)=2(x^2-1)Q_2(x)+(x-2)
            \]
            이므로
            \[
            B(1)=-1,\quad B(-1)=-3.
            \]

            \(R(x)\)는 일차식이므로 \(R(x)=px+q\)라 두면
            \[
            R(1)=A(1)B(1)=5\cdot(-1)=-5,
            \]
            \[
            R(-1)=A(-1)B(-1)=1\cdot(-3)=-3.
            \]
            따라서
            \[
            p+q=-5,\quad -p+q=-3
            \]
            이고 이를 풀면
            \[
            p=-1,\quad q=-4.
            \]
            즉
            \[
            R(x)=-x-4.
            \]
            그러므로
            \[
            R(-5)=1.
            \]
            정답은 ①이다.
            """
        ),
    },
    {
        "filename": "016_2-1. 복소수와 이차방정식.png",
        "source_no": 16,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "2-1. 복소수와 이차방정식",
        "level": 4,
        "question": q(
            r"""
            \[
            \left(\frac{\sqrt{2}}{1+i}\right)^n+\left(\frac{-1+\sqrt{3}i}{2}\right)^n=2
            \]
            를 만족시키는 자연수 \(n\)의 최솟값은? (단, \(i=\sqrt{-1}\))
            """
        ),
        "choices": ["① 6", "② 12", "③ 15", "④ 18", "⑤ 24"],
        "answer": "⑤",
        "solution": q(
            r"""
            먼저
            \[
            \frac{\sqrt{2}}{1+i}
            =\frac{\sqrt{2}(1-i)}{(1+i)(1-i)}
            =\frac{1-i}{\sqrt{2}}
            =\cos\left(-\frac{\pi}{4}\right)+i\sin\left(-\frac{\pi}{4}\right),
            \]
            \[
            \frac{-1+\sqrt{3}i}{2}
            =\cos\left(\frac{2\pi}{3}\right)+i\sin\left(\frac{2\pi}{3}\right).
            \]

            두 수는 모두 절댓값이 \(1\)인 복소수이다.
            절댓값이 \(1\)인 복소수 두 개의 합이 \(2\)가 되려면 두 복소수가 모두 \(1\)이어야 한다.

            따라서
            \[
            \left(\frac{\sqrt{2}}{1+i}\right)^n=1,\quad
            \left(\frac{-1+\sqrt{3}i}{2}\right)^n=1.
            \]

            첫째 조건에서
            \[
            -\frac{n\pi}{4}=2m\pi
            \]
            이므로 \(n\)은 \(8\)의 배수이다.

            둘째 조건에서
            \[
            \frac{2n\pi}{3}=2\ell\pi
            \]
            이므로 \(n\)은 \(3\)의 배수이다.

            따라서 \(n\)의 최솟값은
            \[
            \mathrm{lcm}(8,3)=24.
            \]
            정답은 ⑤이다.
            """
        ),
    },
    {
        "filename": "017_2-2. 이차방정식과 이차함수.png",
        "source_no": 17,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "2-2. 이차방정식과 이차함수",
        "level": 4,
        "scan_filename": "017_2-2. 이차방정식과 이차함수_scan.png",
        "question": q(
            r"""
            그림과 같이 이차함수 \(y=x^2-8x+a\)의 그래프는 \(x\)축과 서로 다른 두 점 \(A,\ B\)에서 만나고,
            기울기가 양수인 직선 \(y=bx+c\)와 서로 다른 두 점 \(A,\ C\)에서 만난다.
            \(\overline{AB}=6\)이고 삼각형 \(ABC\)의 넓이가 \(21\)일 때, \(abc\)의 값은?
            (단, \(a,\ b,\ c\)는 상수이고 점 \(A\)의 \(x\)좌표는 점 \(B\)의 \(x\)좌표보다 작다.)

            <img src="assets/scan.png" alt="problem-017-figure" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ),
        "choices": ["① -28", "② -21", "③ -14", "④ -7", r"⑤ \(-\frac{7}{2}\)"],
        "answer": "④",
        "solution": q(
            r"""
            이차함수의 두 근을 \(r_1,\ r_2\)라 하면
            \[
            r_1+r_2=8,\quad r_2-r_1=6
            \]
            이다.
            따라서
            \[
            r_1=1,\quad r_2=7.
            \]
            즉
            \[
            A=(1,0),\ B=(7,0),\ a=r_1r_2=7.
            \]

            직선 \(y=bx+c\)가 \(A(1,0)\)를 지나므로
            \[
            0=b\cdot 1+c\Rightarrow c=-b.
            \]
            따라서 직선은
            \[
            y=b(x-1).
            \]

            점 \(C\)의 \(x\)좌표를 \(t\)라 하면
            \[
            t^2-8t+7=b(t-1)
            \]
            이고, 한 근이 \(t=1\)이므로 다른 근은 \(t=7+b\)이다.
            그러므로
            \[
            y_C=b(t-1)=b(6+b).
            \]

            삼각형 \(ABC\)의 밑변 길이는 \(\overline{AB}=6\), 높이는 \(y_C\)이므로
            \[
            \frac12\cdot 6\cdot y_C=21
            \Rightarrow y_C=7.
            \]
            따라서
            \[
            b(6+b)=7
            \Rightarrow b^2+6b-7=0
            \Rightarrow b=1\ \text{또는}\ -7.
            \]
            기울기가 양수이므로 \(b=1\), 따라서 \(c=-1\).

            \[
            abc=7\cdot 1\cdot(-1)=-7.
            \]
            정답은 ④이다.
            """
        ),
    },
    {
        "filename": "서답3번_1-3. 인수분해.png",
        "source_no": 3,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "unit_hint": "1-3. 인수분해",
        "level": 4,
        "question": q(
            r"""
            \(x\ne 0,\ 1,\ -1\)인 복소수 \(x\)에 대하여
            \[
            x^3-\frac{1}{x^3}=0
            \]
            이 성립한다.
            이때 \(x^4+x^2+3\)의 값을 구하시오.
            """
        ),
        "choices": [],
        "answer": "2",
        "solution": q(
            r"""
            \[
            x^3-\frac{1}{x^3}=0
            \Rightarrow x^6=1.
            \]
            \(y=x^2\)라 두면
            \[
            y^3=1.
            \]

            또 \(x\ne \pm1\)이므로 \(y\ne1\).
            따라서 \(y\)는 \(1\)이 아닌 세제곱근이므로
            \[
            y^2+y+1=0
            \Rightarrow y^2+y=-1.
            \]

            그러므로
            \[
            x^4+x^2+3=y^2+y+3=-1+3=2.
            \]
            """
        ),
    },
    {
        "filename": "서답4번_2-2. 이차방정식과 이차함수.png",
        "source_no": 4,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "unit_hint": "2-2. 이차방정식과 이차함수",
        "level": 4,
        "question": q(
            r"""
            \(1\le x\le 2\)에서 이차함수
            \[
            y=x^2-2ax+a^2+b
            \]
            의 최솟값이 \(4\)가 되도록 하는 두 실수 \(a,\ b\)에 대하여
            \(2a+b\)의 최댓값을 구하시오.
            """
        ),
        "choices": [],
        "answer": "9",
        "solution": q(
            r"""
            \[
            y=(x-a)^2+b
            \]
            이다.

            구간 \([1,2]\)에서의 최솟값은
            \[
            \min_{1\le x\le2}(x-a)^2+b=d^2+b
            \]
            이고, 여기서 \(d\)는 점 \(a\)와 구간 \([1,2]\) 사이의 거리이다.

            최솟값이 \(4\)이므로
            \[
            b=4-d^2.
            \]
            따라서
            \[
            2a+b=2a+4-d^2.
            \]

            경우를 나눈다.

            \[
            a<1\Rightarrow d=1-a,\quad
            2a+b=2a+4-(1-a)^2=-a^2+4a+3<6.
            \]

            \[
            1\le a\le2\Rightarrow d=0,\quad
            2a+b=2a+4\le8.
            \]

            \[
            a>2\Rightarrow d=a-2,\quad
            2a+b=2a+4-(a-2)^2=-(a-3)^2+9\le9.
            \]

            최댓값은 \(a=3\)일 때 \(9\)이다.
            (이때 \(b=3\), 실제 최솟값은 \(x=2\)에서 \(4\)가 된다.)
            """
        ),
    },
    {
        "filename": "서답5번_1-1. 다항식의 연산.png",
        "source_no": 5,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "unit_hint": "1-1. 다항식의 연산",
        "level": 5,
        "scan_filename": "서답5번_1-1. 다항식의 연산_scan.png",
        "question": q(
            r"""
            오른쪽 [그림 1]과 같이 물이 가득 담긴 직육면체 모양의 그릇에
            직육면체 모양의 막대를 밑면과 맞닿게 수직으로 넣었다.
            이때 남아 있는 물을 [그림 2]와 같은 직육면체 모양의 그릇에 옮겨 담았을 때,
            수면의 높이 \(h\)를 구하는 풀이 과정을 쓰고 답을 구하시오.
            (단, 막대의 길이는 \(x+4\)보다 길다.)

            <img src="assets/scan.png" alt="problem-105-figure" style="width:60% !important; max-width:60% !important; height:auto;" />

            (1) [그림 1]과 같이 물이 가득 담긴 직육면체 모양의 그릇의 물의 부피를 구하시오.

            (2) [그림 1]과 같이 물이 가득 담긴 직육면체 모양의 그릇에 직육면체 모양의 막대를 밑면과 맞닿게 수직으로 넣었을 때
            남아있는 물의 부피를 구하시오.

            (3) [그림 2]와 같은 직육면체 모양의 그릇으로 남아있는 물을 옮겨 담았을 때, 수면의 높이 \(h\)를 구하시오.
            """
        ),
        "choices": [],
        "answer": r"(1) \((x+2)^2(x+4)\), (2) \((x+1)(x+3)(x+4)\), (3) \(h=x+4\)",
        "solution": q(
            r"""
            [그림 1]에서 물이 가득 찬 그릇의 가로, 세로, 높이는 각각 \(x+2,\ x+2,\ x+4\)이므로

            \[
            \text{(1) 물의 부피}= (x+2)(x+2)(x+4)=(x+2)^2(x+4).
            \]

            막대의 밑면은 \(1\times1\), 길이는 \(x+4\)보다 길어서 그릇의 바닥부터 윗면까지를 모두 차지한다.
            따라서 물이 차지할 수 없는 막대 부분의 부피는
            \[
            1\cdot1\cdot(x+4)=x+4.
            \]
            그러므로 남아 있는 물의 부피는
            \[
            \text{(2) 남은 물의 부피}
            =(x+2)^2(x+4)-(x+4)
            =(x+4)\{(x+2)^2-1\}
            =(x+4)(x+1)(x+3).
            \]

            [그림 2] 그릇의 밑면은 \((x+3)\times(x+1)\)이고 수면 높이가 \(h\)이므로
            \[
            (x+3)(x+1)h=(x+4)(x+1)(x+3).
            \]
            따라서
            \[
            \text{(3) }h=x+4.
            \]
            """
        ),
    },
    {
        "filename": "서답6번_2-1. 복소수와 이차방정식.png",
        "source_no": 6,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "unit_hint": "2-1. 복소수와 이차방정식",
        "level": 5,
        "question": q(
            r"""
            은지와 주아가 이차방정식
            \[
            x^2+ax+b=0\quad (a,\ b\text{는 실수})
            \]
            의 근을 구하려고 한다.

            그런데 은지는 상수항을 잘못 보고 풀어 두 근 \(4+i,\ 4-i\)를 얻었고,
            주아는 \(x\)의 계수를 잘못 보고 풀어 두 근 \(3+\sqrt{3}i,\ 3-\sqrt{3}i\)를 얻었다.

            (1) 은지가 구한 두 수를 근으로 하는 이차방정식을 구하시오.

            (2) 주아가 구한 두 수를 근으로 하는 이차방정식을 구하시오.

            (3) 이차방정식 \(x^2+ax+b=0\)의 두 근을 바르게 구하시오.
            """
        ),
        "choices": [],
        "answer": r"(1) \(x^2-8x+17=0\), (2) \(x^2-6x+12=0\), (3) \(x=2,\ 6\)",
        "solution": q(
            r"""
            (1) \(4+i,\ 4-i\)를 근으로 하는 방정식은
            \[
            x^2-(\{4+i\}+\{4-i\})x+(4+i)(4-i)=0
            \]
            \[
            x^2-8x+17=0.
            \]

            은지는 상수항만 잘못 보았으므로 원래 식의 \(x\)의 계수는 그대로여서
            \[
            a=-8.
            \]

            (2) \(3+\sqrt{3}i,\ 3-\sqrt{3}i\)를 근으로 하는 방정식은
            \[
            x^2-(\{3+\sqrt{3}i\}+\{3-\sqrt{3}i\})x
            +(3+\sqrt{3}i)(3-\sqrt{3}i)=0
            \]
            \[
            x^2-6x+12=0.
            \]

            주아는 \(x\)의 계수만 잘못 보았으므로 원래 식의 상수항은 그대로여서
            \[
            b=12.
            \]

            (3) 따라서 원래 이차방정식은
            \[
            x^2-8x+12=0
            \]
            이고
            \[
            (x-2)(x-6)=0.
            \]
            그러므로 두 근은
            \[
            x=2,\ 6.
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
    level: int,
    unit_triplet: Tuple[str, str, str],
    source_label: str,
    source_tag_no: str,
    question: str,
    choices: List[str],
    answer: str,
    solution: str,
    assets: List[str],
) -> str:
    l1, l2, l3 = unit_triplet
    unit = f"{l1}>{l2}>{l3}"

    lines: List[str] = [
        "---",
        f"id: {pid}",
        f"school: {META['school']}",
        f"year: {META['year']}",
        f"grade: {META['grade']}",
        f"semester: {META['semester']}",
        f"exam: {META['exam']}",
        f'type: "{qtype}"',
        f"source_question_no: {source_no}",
        f"source_question_kind: {source_kind}",
        f'source_question_label: "{source_label}"',
        f"difficulty: {level}",
        f"level: {level}",
        f'unit: "{unit}"',
        f'unit_l1: "{l1}"',
        f'unit_l2: "{l2}"',
        f'unit_l3: "{l3}"',
        f'source: "{META["source"]}"',
        "tags:",
        "  - 수동작성",
        f"  - {qtype}",
        f"  - 출제번호-{source_tag_no}",
        "assets:",
    ]
    lines.extend([f"  - {asset}" for asset in assets])
    lines.extend(
        [
            "---",
            "",
            "## Q",
            question,
            "",
            "## Choices",
            "\n".join(choices),
            "",
            "## Answer",
            answer,
            "",
            "## Solution",
            solution,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []
    unmatched_units: List[str] = []

    for row in ROWS:
        filename = str(row["filename"])
        source_path = ORIGINAL / filename
        if not source_path.exists():
            warnings.append(f"{filename}: source image not found")
            continue

        source_no = int(row["source_no"])
        kind = str(row["kind"])
        problem_no = source_no if kind == "objective" else source_no + int(META["subjective_offset"])
        pid = f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{problem_no:03d}"
        pdir = PROBLEMS / pid

        if pdir.exists():
            summary["skipped"] += 1
            results.append(f"{filename} -> {pid} [skipped: folder exists]")
            continue

        unit_hint = str(row["unit_hint"])
        unit_triplet = UNIT_MAP.get(unit_hint)
        if unit_triplet is None:
            warnings.append(f"{filename}: unit mapping not found for hint '{unit_hint}'")
            unmatched_units.append(filename)
            continue

        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        copied_assets: List[str] = []
        copied_name = source_path.name
        shutil.copy2(source_path, original_dir / copied_name)
        copied_assets.append(f"assets/original/{copied_name}")

        scan_filename: Optional[str] = row.get("scan_filename")
        has_scan = False
        if scan_filename:
            scan_src = ORIGINAL / scan_filename
            if scan_src.exists():
                shutil.copy2(scan_src, assets_dir / "scan.png")
                shutil.copy2(scan_src, original_dir / scan_filename)
                copied_assets.append(f"assets/original/{scan_filename}")
                has_scan = True
            else:
                warnings.append(f"{filename}: scan source not found ({scan_filename})")

        source_label = str(source_no) if kind == "objective" else f"서답{source_no}"
        source_tag_no = str(source_no)
        assets_list: List[str] = []
        if has_scan:
            assets_list.append("assets/scan.png")
        assets_list.append("assets/original/")
        assets_list.extend(copied_assets)

        md = build_problem_md(
            pid=pid,
            qtype=str(row["type"]),
            source_no=source_no,
            source_kind=kind,
            level=int(row["level"]),
            unit_triplet=unit_triplet,
            source_label=source_label,
            source_tag_no=source_tag_no,
            question=str(row["question"]).strip(),
            choices=list(row["choices"]),
            answer=str(row["answer"]).strip(),
            solution=str(row["solution"]).strip(),
            assets=assets_list,
        )
        (pdir / "problem.md").write_text(md, encoding="utf-8")

        summary["created"] += 1
        scan_note = " +scan" if has_scan else ""
        results.append(f"{filename} -> {pid} [created]{scan_note}")

    # Report filename/unit label mismatch from source naming conventions.
    # The image name says "2-3. 여러 가지 부등식", but taxonomy is "2-4. 여러 가지 부등식".
    warnings.append("014_2-3. 여러 가지 부등식.png: filename unit label '2-3' mismatches taxonomy '2-4'.")

    summary["warnings"] = len(warnings)

    report_lines = [
        f"created={summary['created']} updated={summary['updated']} skipped={summary['skipped']} warnings={summary['warnings']}",
        "",
        "[RESULTS]",
    ]
    report_lines.extend(results)
    report_lines.append("")
    report_lines.append("[WARNINGS]")
    report_lines.extend(warnings)
    if unmatched_units:
        report_lines.append("")
        report_lines.append("[UNIT_UNMATCHED]")
        report_lines.extend(unmatched_units)

    report_path = ROOT / "_tmp_jew_2023_mid_ingest_report.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print("\n".join(report_lines))
    print(f"\nreport: {report_path}")


if __name__ == "__main__":
    main()
