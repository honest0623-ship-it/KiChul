from __future__ import annotations

import shutil
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"d:\Math_Kichul")
ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

META = {
    "school": "BY",
    "year": 2025,
    "grade": 1,
    "semester": 1,
    "exam": "Final",
    "source": "user_upload_2026-03-01",
}

UNIT_MAP: Dict[str, Tuple[str, str, str]] = {
    "행렬과 그 연산": ("공통수학1(2022개정)", "4. 행렬", "4-1. 행렬과 그 연산"),
    "여러 가지 부등식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식"),
    "합의 법칙과 곱의 법칙": ("공통수학1(2022개정)", "3. 경우의 수", "3-1. 합의 법칙과 곱의 법칙"),
    "여러 가지 방정식": ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식"),
    "순열과 조합": ("공통수학1(2022개정)", "3. 경우의 수", "3-2. 순열과 조합"),
}


def q(text: str) -> str:
    return text.strip()


ROWS: List[Dict[str, object]] = [
    {
        "filename": "006_행렬과 그 연산.png",
        "source_no": 6,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "행렬과 그 연산",
        "level": 3,
        "question": q(
            """
            $3\\times 2$ 행렬 $A$의 $(i,j)$ 성분 $a_{ij}\\,(i=1,2,3,\\ j=1,2)$가
            $$
            a_{ij}=3ij-i+k
            $$
            일 때, $a_{12}+a_{31}=7$이다. $k$의 값은?
            """
        ),
        "choices": ["① $-2$", "② $-1$", "③ $0$", "④ $1$", "⑤ $2$"],
        "answer": "①",
        "solution": q(
            """
            $$
            a_{12}=3\\cdot1\\cdot2-1+k=5+k,\\qquad
            a_{31}=3\\cdot3\\cdot1-3+k=6+k
            $$
            이므로
            $$
            (5+k)+(6+k)=7\\Rightarrow 11+2k=7\\Rightarrow 2k=-4\\Rightarrow k=-2.
            $$
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "007_여러 가지 부등식.png",
        "source_no": 7,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "여러 가지 부등식",
        "level": 3,
        "question": q(
            """
            이차부등식
            $$
            x^2-(k-1)x+k+2<0
            $$
            의 해가 존재하지 않도록 하는 정수 $k$의 최댓값은?
            """
        ),
        "choices": ["① $4$", "② $5$", "③ $6$", "④ $7$", "⑤ $8$"],
        "answer": "④",
        "solution": q(
            """
            포물선 $y=x^2-(k-1)x+k+2$는 아래로 볼록이므로, 부등식의 해가 없으려면 판별식이 $0$ 이하이다.
            $$
            \\Delta=(k-1)^2-4(k+2)=k^2-6k-7=(k-7)(k+1)\\le 0
            $$
            따라서 $-1\\le k\\le 7$이고, 정수 $k$의 최댓값은 $7$이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "009_합의 법칙과 곱의 법칙.png",
        "source_no": 9,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "합의 법칙과 곱의 법칙",
        "level": 3,
        "question": "1부터 100까지의 자연수 중에서 3과 7로 모두 나누어 떨어지지 않는 자연수의 개수는?",
        "choices": ["① $51$", "② $53$", "③ $55$", "④ $57$", "⑤ $59$"],
        "answer": "④",
        "solution": q(
            """
            포함배제를 이용하면,
            $$
            |3의\\ 배수|=\\left\\lfloor\\frac{100}{3}\\right\\rfloor=33,\\quad
            |7의\\ 배수|=\\left\\lfloor\\frac{100}{7}\\right\\rfloor=14,\\quad
            |21의\\ 배수|=\\left\\lfloor\\frac{100}{21}\\right\\rfloor=4.
            $$
            따라서 3 또는 7의 배수는
            $$
            33+14-4=43
            $$
            개이므로, 원하는 개수는
            $$
            100-43=57.
            $$
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "010_행렬과 그 연산.png",
        "source_no": 10,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "행렬과 그 연산",
        "level": 3,
        "question": q(
            """
            두 이차정사각행렬 $A,B$에 대하여
            $$
            A+B=\\begin{pmatrix}2 & 1 \\\\ 4 & 3\\end{pmatrix},\\qquad
            A-B=\\begin{pmatrix}0 & -1 \\\\ 2 & 1\\end{pmatrix}
            $$
            일 때, 행렬 $AB-BA$의 $(1,2)$ 성분은?
            """
        ),
        "choices": ["① $-2$", "② $-1$", "③ $0$", "④ $1$", "⑤ $2$"],
        "answer": "②",
        "solution": q(
            """
            $$
            A=\\frac{(A+B)+(A-B)}{2}=\\begin{pmatrix}1 & 0 \\\\ 3 & 2\\end{pmatrix},\\qquad
            B=\\frac{(A+B)-(A-B)}{2}=\\begin{pmatrix}1 & 1 \\\\ 1 & 1\\end{pmatrix}.
            $$
            따라서
            $$
            AB=\\begin{pmatrix}1 & 1 \\\\ 5 & 5\\end{pmatrix},\\quad
            BA=\\begin{pmatrix}4 & 2 \\\\ 4 & 2\\end{pmatrix},
            $$
            $$
            AB-BA=\\begin{pmatrix}-3 & -1 \\\\ 1 & 3\\end{pmatrix}.
            $$
            $(1,2)$ 성분은 $-1$이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "012_여러 가지 부등식.png",
        "source_no": 12,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "여러 가지 부등식",
        "level": 3,
        "question": q(
            """
            부등식
            $$
            |x+1|+|x-3|\\le 4
            $$
            를 만족시키는 정수 $x$의 개수는?
            """
        ),
        "choices": ["① $3$", "② $4$", "③ $5$", "④ $6$", "⑤ $7$"],
        "answer": "③",
        "solution": q(
            """
            $|x+1|+|x-3|$는 수직선에서 점 $-1,3$까지의 거리의 합이다.
            거리의 합이 최소가 되는 구간은 $-1\\le x\\le 3$이고, 그 값이 $4$이다.
            따라서 부등식을 만족하는 실수해는
            $$
            -1\\le x\\le 3
            $$
            이고 정수는 $-1,0,1,2,3$으로 $5$개이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "013_여러 가지 부등식.png",
        "source_no": 13,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "여러 가지 부등식",
        "level": 4,
        "question": q(
            """
            $x$에 대한 이차부등식
            $$
            x^2-2ax-2a\\le 0
            $$
            의 해는 한 개이고, $x$에 대한 이차부등식
            $$
            ax^2-4x+3a+b>0
            $$
            은 해를 갖지 않을 때, 두 실수 $a,b$에 대하여 $a+b$의 최댓값은? (단, $a\\ne 0$)
            """
        ),
        "choices": ["① $-2$", "② $-1$", "③ $0$", "④ $1$", "⑤ $2$"],
        "answer": "⑤",
        "solution": q(
            """
            첫 번째 부등식의 해가 한 개이려면 이차식이 중근을 가져야 하므로
            $$
            (-2a)^2-4\\cdot1\\cdot(-2a)=4a(a+2)=0
            $$
            에서 $a=0$ 또는 $a=-2$. 조건 $a\\ne0$이므로 $a=-2$.

            두 번째 부등식은
            $$
            -2x^2-4x-6+b>0
            $$
            즉
            $$
            -2(x+1)^2+(b-4)>0.
            $$
            좌변의 최댓값은 $b-4$이므로 해가 없으려면 $b-4\\le0$, 즉 $b\\le4$.
            따라서
            $$
            a+b=-2+b\\le2
            $$
            최댓값은 $2$이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "014_여러 가지 부등식.png",
        "source_no": 14,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "여러 가지 부등식",
        "level": 4,
        "question": q(
            """
            연립이차부등식
            $$
            \\begin{cases}
            x^2<x+12 \\\\
            x^2-(2k+3)x+k^2+3k+2>0
            \\end{cases}
            $$
            을 만족시키는 정수해의 개수가 4가 되도록 하는 모든 정수 $k$의 값의 합은?
            """
        ),
        "choices": ["① $-5$", "② $-4$", "③ $-3$", "④ $-2$", "⑤ $-1$"],
        "answer": "①",
        "solution": q(
            """
            첫째 부등식은
            $$
            (x-4)(x+3)<0\\Rightarrow -3<x<4
            $$
            이므로 정수해 후보는 $\\{-2,-1,0,1,2,3\\}$ (6개)이다.

            둘째 부등식은
            $$
            (x-(k+1))(x-(k+2))>0
            $$
            이므로 $x=k+1,\\ k+2$에서는 성립하지 않는다.
            정수해가 4개가 되려면 후보 6개 중 정확히 2개가 제외되어야 하므로
            $k+1,\\ k+2$가 모두 후보 집합 안에 있어야 한다.
            즉
            $$
            -2\\le k+1\\le3,\\quad -2\\le k+2\\le3
            $$
            에서 $k=-3,-2,-1,0,1$.
            합은
            $$
            -3-2-1+0+1=-5.
            $$
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "015_여러 가지 방정식.png",
        "source_no": 15,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "여러 가지 방정식",
        "level": 4,
        "question": q(
            """
            삼차방정식 $x^3=1$의 한 허근을 $\\omega$라 할 때, 다음 중에서 옳은 것만을 있는 대로 고른 것은?

            ㄱ. $\\dfrac{1}{\\omega}+\\dfrac{1}{\\overline{\\omega}}=-1$

            ㄴ. $\\omega(\\overline{\\omega})^2+\\omega^2\\overline{\\omega}=-1$

            ㄷ. $1+\\omega^4+\\omega^5+\\omega^{40}+\\omega^{50}=(\\overline{\\omega})^3+(\\overline{\\omega})^{30}-1$
            """
        ),
        "choices": ["① ㄱ", "② ㄴ", "③ ㄱ, ㄴ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"],
        "answer": "③",
        "solution": q(
            """
            $\\omega^3=1$, $\\omega\\ne1$, $1+\\omega+\\omega^2=0$, $\\overline{\\omega}=\\omega^2$를 이용한다.

            ㄱ.
            $$
            \\frac1\\omega+\\frac1{\\overline\\omega}=\\omega^2+\\omega=-1
            $$
            이므로 참.

            ㄴ.
            $$
            \\omega(\\overline\\omega)^2+\\omega^2\\overline\\omega
            =\\omega(\\omega^2)^2+\\omega^2\\omega^2
            =\\omega^5+\\omega^4=\\omega^2+\\omega=-1
            $$
            이므로 참.

            ㄷ.
            좌변은
            $$
            1+\\omega+\\omega^2+\\omega+\\omega^2=(1+\\omega+\\omega^2)+(\\omega+\\omega^2)=-1.
            $$
            우변은
            $$
            (\\overline\\omega)^3+(\\overline\\omega)^{30}-1=1+1-1=1.
            $$
            좌변과 우변이 달라 거짓.

            따라서 옳은 것은 ㄱ, ㄴ이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "016_행렬과 그 연산.png",
        "source_no": 16,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "행렬과 그 연산",
        "level": 4,
        "question": q(
            """
            이차정사각행렬 $A$가
            $$
            A^2-4A+8E=O
            $$
            를 만족시킨다.
            $$
            A\\begin{pmatrix}1\\\\-1\\end{pmatrix}=\\begin{pmatrix}2\\\\3\\end{pmatrix},\\qquad
            A\\begin{pmatrix}2\\\\3\\end{pmatrix}=\\begin{pmatrix}a\\\\b\\end{pmatrix}
            $$
            일 때, $a+b$의 값은? (단, $E$는 단위행렬이고, $O$는 영행렬이다.)
            """
        ),
        "choices": ["① $16$", "② $17$", "③ $18$", "④ $19$", "⑤ $20$"],
        "answer": "⑤",
        "solution": q(
            """
            다항식 관계식에 벡터 $\\begin{pmatrix}1\\\\-1\\end{pmatrix}$를 곱하면
            $$
            (A^2-4A+8E)\\begin{pmatrix}1\\\\-1\\end{pmatrix}=\\begin{pmatrix}0\\\\0\\end{pmatrix}.
            $$
            여기서
            $$
            A\\begin{pmatrix}1\\\\-1\\end{pmatrix}=\\begin{pmatrix}2\\\\3\\end{pmatrix},\\qquad
            A^2\\begin{pmatrix}1\\\\-1\\end{pmatrix}=A\\begin{pmatrix}2\\\\3\\end{pmatrix}=\\begin{pmatrix}a\\\\b\\end{pmatrix}.
            $$
            따라서
            $$
            \\begin{pmatrix}a\\\\b\\end{pmatrix}-4\\begin{pmatrix}2\\\\3\\end{pmatrix}+8\\begin{pmatrix}1\\\\-1\\end{pmatrix}=\\begin{pmatrix}0\\\\0\\end{pmatrix}
            $$
            이므로
            $$
            \\begin{pmatrix}a\\\\b\\end{pmatrix}=\\begin{pmatrix}0\\\\20\\end{pmatrix}.
            $$
            따라서 $a+b=20$이다.
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "017_순열과 조합.png",
        "source_no": 17,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "순열과 조합",
        "level": 4,
        "question": q(
            """
            두 쌍의 부부를 포함한 남자 5명, 여자 2명이 졸업식에 참여해 아래 그림과 같은 좌석에 앉으려고 한다.
            각각의 부부는 이웃해 앉고, 두 쌍의 부부는 같은 열에 앉는다.
            부부에 속한 남자를 제외한 남자 3명은 서로 이웃하지 않도록 앉는 방법의 수는?

            <img src="assets/scan.png" alt="seat-figure" style="width:56% !important; max-width:56% !important; height:auto;" />
            """
        ),
        "choices": ["① $1968$", "② $2016$", "③ $2064$", "④ $2112$", "⑤ $2160$"],
        "answer": "②",
        "solution": q(
            """
            두 쌍의 부부가 같은 열에 앉으므로, 먼저 부부가 앉을 열을 정한다.

            1) 부부가 앉는 열 선택: A열 또는 B열, $2$가지.

            2) 한 열(좌석 5칸)에서 길이 2인 자리 블록 2개를 겹치지 않게 잡는 방법:
            $([1,2],[3,4]),([1,2],[4,5]),([2,3],[4,5])$의 $3$가지.

            3) 두 부부를 두 블록에 배치: $2!$가지, 각 블록에서 부부 자리 바꾸기 $2^2$가지.

            따라서 부부 배치는
            $$
            2\\times3\\times2!\\times2^2=48
            $$
            가지.

            이제 남은 남자 3명을 배치한다.
            부부가 앉은 열에는 빈칸 1개, 다른 열에는 빈칸 5개가 남는다.
            남자 3명이 서로 이웃하지 않게 앉는 경우는

            - 5칸 열에 3명 모두 배치: 비인접 자리 선택 1가지, 사람 배치 $3!$로 $6$가지
            - 5칸 열에 2명, 1칸 열에 1명 배치: 5칸에서 비인접 2자리 선택 $6$가지, 사람 배치 $3\\times2!=6$가지

            합하여
            $$
            6+6\\times6=42
            $$
            가지.

            전체는
            $$
            48\\times42=2016.
            $$
            """
        ),
        "use_scan": True,
    },
    {
        "filename": "018_행렬과 그 연산.png",
        "source_no": 18,
        "kind": "objective",
        "type": "객관식",
        "unit_hint": "행렬과 그 연산",
        "level": 4,
        "question": q(
            """
            $$
            x^2y^2+x^2+4y^2+12xy+16=0
            $$
            을 만족하는 두 실수 $x,y$에 대하여 $x^2=a,\\ y^2=b$라 하자.
            행렬
            $$
            A=\\begin{pmatrix}a & b \\\\ 0 & 1\\end{pmatrix}
            $$
            일 때, 행렬 $A$의 모든 성분의 합은?
            """
        ),
        "choices": ["① $8$", "② $9$", "③ $10$", "④ $11$", "⑤ $12$"],
        "answer": "④",
        "solution": q(
            """
            식은 $x$에 대한 이차식으로 보면
            $$
            (y^2+1)x^2+12yx+(4y^2+16)=0.
            $$
            실수해가 존재하려면 판별식이 0 이상이어야 하므로
            $$
            \\Delta=144y^2-4(y^2+1)(4y^2+16)=-16(y^2-2)^2\\ge0.
            $$
            따라서 $y^2=2$, 즉 $b=2$.
            이때 원식을 만족하는 $x$는 $x=-2y$이므로
            $$
            a=x^2=4y^2=8.
            $$
            행렬 성분의 합은
            $$
            a+b+0+1=8+2+1=11.
            $$
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "서답2번_순열과 조합.png",
        "source_no": 2,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "unit_hint": "순열과 조합",
        "level": 4,
        "question": q(
            """
            학생 5명에게 서로 다른 빵 3개와 서로 다른 과자 4개를 나누어 주려고 한다.
            빵을 받지 않는 학생에게만 과자를 1개씩 나누어 줄 수 있으며 나누어 준 후 빵은 남지 않고, 과자는 남는다.
            학생 5명에게 빵과 과자를 나누어 주는 방법의 수를 구하시오.
            (단, 한 학생이 빵을 2개 이상 받을 수 있다.)
            """
        ),
        "choices": [],
        "answer": "2160",
        "solution": q(
            """
            빵 3개를 분배하는 경우를 빵을 받지 않는 학생 수로 나눈다.

            - 빵을 3명이 받는 경우(각 1개씩):
            $$
            \\binom{5}{3}\\cdot 3!=60
            $$
            이때 빵을 받지 않는 2명에게 서로 다른 과자 2개를 배정하는 방법은
            $$
            {}_4P_2=4\\cdot3=12
            $$
            이므로 $60\\cdot12=720$가지.

            - 빵을 2명이 받는 경우(2개, 1개):
            $$
            5\\cdot4\\cdot\\binom{3}{2}=60
            $$
            이때 빵을 받지 않는 3명에게 서로 다른 과자 3개를 배정하는 방법은
            $$
            {}_4P_3=4\\cdot3\\cdot2=24
            $$
            이므로 $60\\cdot24=1440$가지.

            - 빵을 1명이 모두 받는 경우는 빵을 받지 않는 학생이 4명이라 과자가 남지 않으므로 제외.

            따라서 전체 방법 수는
            $$
            720+1440=2160.
            $$
            """
        ),
        "use_scan": False,
    },
    {
        "filename": "서답4번_여러 가지 부등식.png",
        "source_no": 4,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "unit_hint": "여러 가지 부등식",
        "level": 5,
        "question": q(
            """
            이차부등식 $f(x)<0$의 해가 $x<-2$ 또는 $x>6$일 때,
            부등식 $f(2x)>0$을 만족시키는 모든 정수 $x$의 값의 합을 구하는 풀이과정을 쓰고 답을 구하시오.
            """
        ),
        "choices": [],
        "answer": "3",
        "solution": q(
            """
            $f(x)<0$의 해가 $x<-2$ 또는 $x>6$이므로,
            이차함수 $f(x)$는 근이 $-2,6$이고 아래로 볼록이다.
            따라서
            $$
            f(x)=a(x+2)(x-6)\\quad(a<0).
            $$
            그러면
            $$
            f(2x)=a(2x+2)(2x-6)=4a(x+1)(x-3).
            $$
            $a<0$이므로 $f(2x)>0$은
            $$
            (x+1)(x-3)<0
            $$
            와 동치이다.
            따라서
            $$
            -1<x<3.
            $$
            정수해는 $x=0,1,2$이고 그 합은
            $$
            0+1+2=3.
            $$
            """
        ),
        "use_scan": False,
    },
]


def make_scan_017(path: Path) -> None:
    img = Image.new("RGB", (1200, 320), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_big = ImageFont.truetype("malgun.ttf", 44)
        font = ImageFont.truetype("malgun.ttf", 36)
    except Exception:
        font_big = ImageFont.load_default()
        font = ImageFont.load_default()

    left = 170
    top1 = 60
    top2 = 200
    width = 180
    height = 70

    draw.text((35, top1 + 10), "A열", fill="black", font=font_big)
    draw.text((35, top2 + 10), "B열", fill="black", font=font_big)

    for row, top in enumerate([top1, top2]):
        for i in range(5):
            x = left + i * width
            draw.rectangle([x, top, x + width, top + height], outline="black", width=3)
            label = f"{'A' if row == 0 else 'B'}{i + 1}"
            bbox = draw.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((x + (width - tw) / 2, top + (height - th) / 2 - 2), label, fill="black", font=font)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def canonical_original_name(source_no: int, kind: str) -> str:
    if kind == "objective":
        return f"{source_no:03d}.png"
    return f"서답{source_no - 100}번.png"


def build_problem_md(
    pid: str,
    source_no: int,
    source_kind: str,
    qtype: str,
    level: int,
    unit_triplet: Tuple[str, str, str],
    question: str,
    choices: List[str],
    answer: str,
    solution: str,
    original_asset_name: str,
    use_scan: bool,
) -> str:
    l1, l2, l3 = unit_triplet
    unit_path = f"{l1}>{l2}>{l3}"
    source_label = f"서답{source_no - 100}번" if source_kind == "subjective" else str(source_no)

    assets = ["assets/original/", f"assets/original/{original_asset_name}"]
    if use_scan:
        assets.insert(0, "assets/scan.png")

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
        f"source_question_label: '{source_label}'",
        f"difficulty: '{level}'",
        f"level: {level}",
        f"unit: {unit_path}",
        f"unit_l1: {l1}",
        f"unit_l2: {l2}",
        f"unit_l3: {l3}",
        f"source: {META['source']}",
        "tags:",
        f"- {qtype}",
        f"- 출제번호-{source_label}",
        "assets:",
    ]
    lines.extend([f"- {item}" for item in assets])
    lines.extend(
        [
            "---",
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
    summary = {"created": 0, "updated": 0, "skipped": 0, "warnings": 0}
    results: List[str] = []
    warnings: List[str] = []

    for row in ROWS:
        filename = str(row["filename"])
        source_path = ORIGINAL / filename
        if not source_path.exists():
            warnings.append(f"{filename}: source image not found")
            continue

        source_no = int(row["source_no"])
        kind = str(row["kind"])
        problem_no = source_no if kind == "objective" else source_no + 100
        pid = f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{problem_no:03d}"
        pdir = PROBLEMS / pid
        existed = pdir.exists()

        unit_hint = str(row["unit_hint"])
        unit_triplet = UNIT_MAP[unit_hint]

        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        original_name = canonical_original_name(problem_no, kind)
        dest_original = original_dir / original_name
        shutil.copy2(source_path, dest_original)

        if bool(row["use_scan"]):
            make_scan_017(assets_dir / "scan.png")

        md_text = build_problem_md(
            pid=pid,
            source_no=problem_no,
            source_kind=kind,
            qtype=str(row["type"]),
            level=int(row["level"]),
            unit_triplet=unit_triplet,
            question=str(row["question"]),
            choices=list(row["choices"]),  # type: ignore[arg-type]
            answer=str(row["answer"]),
            solution=str(row["solution"]),
            original_asset_name=original_name,
            use_scan=bool(row["use_scan"]),
        )
        md_path = pdir / "problem.md"
        md_path.write_text(md_text, encoding="utf-8")

        if existed:
            summary["updated"] += 1
            status = "updated"
        else:
            summary["created"] += 1
            status = "created"
        scan_flag = " scan.png" if bool(row["use_scan"]) else ""
        results.append(f"{filename} -> {pid} [{status}]{scan_flag}")

    summary["warnings"] = len(warnings)

    report = ROOT / "_tmp_by_final_ingest_report.txt"
    lines = [
        f"created={summary['created']} updated={summary['updated']} skipped={summary['skipped']} warnings={summary['warnings']}"
    ]
    lines.extend(results)
    if warnings:
        lines.append("")
        lines.append("[WARNINGS]")
        lines.extend(warnings)
    report.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"report: {report}")


if __name__ == "__main__":
    main()
