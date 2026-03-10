from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import fitz
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PROBLEM_ROOT = REPO_ROOT / "db" / "problems"
ORIGINAL_ROOT = REPO_ROOT / "db" / "original"


PUA_MAP = {
    "\ue000": "A",
    "\ue001": "B",
    "\ue002": "C",
    "\ue003": "D",
    "\ue004": "E",
    "\ue005": "F",
    "\ue006": "G",
    "\ue007": "H",
    "\ue00f": "P",
    "\ue010": "Q",
    "\ue011": "R",
    "\ue034": "1",
    "\ue035": "2",
    "\ue036": "3",
    "\ue037": "4",
    "\ue038": "5",
    "\ue039": "6",
    "\ue03a": "7",
    "\ue03b": "8",
    "\ue03c": "9",
    "\ue03d": "0",
    "\ue044": "(",
    "\ue045": ")",
    "\ue046": "-",
    "\ue047": "=",
    "\ue048": "+",
    "\ue04b": "{",
    "\ue04c": "}",
    "\ue04f": ":",
    "\ue052": ",",
    "\ue056": ">",
    "\ue05c": "sqrt",
    "\ue06d": "/",
    "\ue09d": "alpha",
    "\ue09e": "beta",
    "\ue0e5": "a",
    "\ue0e6": "b",
    "\ue0e7": "c",
    "\ue0ea": "f",
    "\ue0eb": "g",
    "\ue0ed": "i",
    "\ue0ef": "k",
    "\ue0f1": "m",
    "\ue0f2": "n",
    "\ue0f4": "p",
    "\ue0f5": "q",
    "\ue0f8": "t",
    "\ue0fc": "x",
    "\ue0fd": "y",
    "\ue0fe": "z",
    "\ue101": "|",
}

CHOICE_MARKERS = "①②③④⑤"
EXAM_CODES = ("JEW", "JJ", "SY")


@dataclass(frozen=True)
class ExamConfig:
    school: str
    pdf_path: Path
    start_patterns: tuple[str, ...]
    skip_last_page: bool


CONFIGS = {
    "JEW": ExamConfig(
        school="JEW",
        pdf_path=ORIGINAL_ROOT / "JEW.2022.G1.S1.MID.COM1.pdf",
        start_patterns=(r"^\d+\.", r"^서\d+\."),
        skip_last_page=False,
    ),
    "JJ": ExamConfig(
        school="JJ",
        pdf_path=ORIGINAL_ROOT / "JJ.2022.G1.S1.MID.COM1.pdf",
        start_patterns=(r"^\d+\.", r"^서(?:답형|술형)\d+\)"),
        skip_last_page=True,
    ),
    "SY": ExamConfig(
        school="SY",
        pdf_path=ORIGINAL_ROOT / "SY.2022.G1.S1.MID.COM1.pdf",
        start_patterns=(r"^\d+\.", r"^\[서(?:답형|술형)\d+\]"),
        skip_last_page=True,
    ),
}

MANUAL_SECTIONS: dict[str, dict[str, str]] = {
    "JEW-2022-G1-S1-MID-002": {
        "q": "이차방정식 $x^2-3x+5=0$의 두 근을 $\\alpha$, $\\beta$라 할 때, $(\\alpha-1)(\\beta-1)$의 값은?",
    },
    "JEW-2022-G1-S1-MID-005": {
        "q": "다음 등식 $(2x-y)+(x+y-6)i=0$을 만족시키는 실수 $x, y$에 대하여 $xy$의 값은? (단, $i=\\sqrt{-1}$)",
    },
    "JEW-2022-G1-S1-MID-008": {
        "q": "$x$에 대한 사차식 $x^4-8x^2+4$이 $(x^2+ax+b)(x^2-ax+b)$로 인수분해될 때 $ab$의 값은? (단, $a>0$)",
    },
    "JEW-2022-G1-S1-MID-010": {
        "q": "이차함수 $y=3x^2-x+2$의 그래프가 직선 $y=ax-3$과 두 점 $(x_1,y_1)$, $(x_2,y_2)$에서 만난다. $x_1+x_2=3$일 때, 실수 $a$의 값은?",
    },
    "JEW-2022-G1-S1-MID-015": {
        "q": "$a+b+c=-2$, $\\dfrac{1}{a}+\\dfrac{1}{b}+\\dfrac{1}{c}=1$, $\\dfrac{1}{a^2}+\\dfrac{1}{b^2}+\\dfrac{1}{c^2}=5$일 때, $a^2+b^2+c^2$의 값은? (단, $abc\\ne 0$)",
    },
    "JEW-2022-G1-S1-MID-017": {
        "q": "$0\\le x\\le 4$일 때, 이차함수 $f(x)=x^2-2kx+4k$의 최솟값이 $-5$가 되도록 하는 모든 실수 $k$의 값의 합은?",
        "choices": "\n".join(
            [
                "① $-\\dfrac{5}{4}$",
                "② $-\\dfrac{1}{4}$",
                "③ $4$",
                "④ $\\dfrac{25}{4}$",
                "⑤ $9$",
            ]
        ),
    },
    "JEW-2022-G1-S1-MID-101": {
        "q": "$x$에 대한 이차방정식 $x^2-(k+1)x+k^2=0$이 중근을 갖도록 하는 실수 $k$의 값의 합을 구하시오.",
    },
    "JEW-2022-G1-S1-MID-102": {
        "q": "$x$에 대한 이차식 $x^2+2x+5$를 복소수 범위에서 인수분해 하시오.",
    },
    "JEW-2022-G1-S1-MID-103": {
        "q": "$z=\\dfrac{1-i}{\\sqrt{2}}$일 때, $z^2-z^4-z^6+z^8$의 값을 구하시오.",
    },
    "JEW-2022-G1-S1-MID-104": {
        "q": "다항식 $x^3-2kx^2-(3k^2+k+1)x+3k^2+3k$를 인수분해한 것이 $(x-a)^2(x-b)$꼴이 되도록 하는 모든 실수 $k$값의 합을 구하시오.",
    },
    "JEW-2022-G1-S1-MID-105": {
        "q": "\n".join(
            [
                "$x^3$의 계수가 $1$인 삼차식 $P(x)$에 대하여 $P(1)=1$, $P(2)=2$, $P(3)=3$일 때, $P(x)$를 $x-5$로 나누었을 때의 나머지를 구하려 한다. 다음 물음에 답하시오.",
                "",
                "(1) $P(x)=x$의 근을 구하시오. [3점]",
                "(2) (1)의 결과를 이용하여 $f(x)=P(x)-x$라 두고, $P(x)$를 구하시오. [4점]",
                "(3) $P(x)$를 $x-5$로 나누었을 때의 나머지를 구하시오. [3점]",
            ]
        ),
    },
    "JEW-2022-G1-S1-MID-106": {
        "q": "\n".join(
            [
                "어느 꽃가게에서 백합 한 송이의 가격이 $600$원일 때 하루에 $800$송이씩 팔린다고 한다. 백합 한 송이의 가격을 $x$원 올리면 하루 판매량은 $x$개 감소한다고 한다. 다음 물음에 답하시오.",
                "",
                "(1) 백합 한 송이의 가격과 하루 판매량을 $x$를 사용한 식으로 나타내시오. [2점]",
                "(2) 백합의 하루 판매액을 함수로 나타내시오. [3점]",
                "(3) 이차함수의 최대, 최소를 이용하여 백합 하루 판매액이 최대가 되는 백합 한 송이의 가격을 구하시오. [3점]",
                "(4) 백합의 최대 하루 판매액을 구하시오. [2점]",
            ]
        ),
    },
    "JJ-2022-G1-S1-MID-003": {
        "q": "등식 $(x^2+x-3)^3=a_0+a_1x+\\cdots+a_5x^5+a_6x^6$이 $x$에 대한 항등식일 때, $a_0+a_2+a_4+a_6$의 값은? (단, $a_0, a_1, a_2, \\ldots, a_6$은 상수이다.)",
    },
    "JJ-2022-G1-S1-MID-001": {
        "q": "세 다항식 $A$, $B$, $C$가 $A=x^2+xy-3y^2$, $B=y^2-xy+2x^2$, $C=3x^2+5y^2$일 때, $A-(B-C)$를 계산하면?",
    },
    "JJ-2022-G1-S1-MID-002": {
        "q": "$a-b=6$, $b-c=-2$일 때, $a^2+b^2+c^2-ab-bc-ca$의 값은?",
    },
    "JJ-2022-G1-S1-MID-004": {
        "q": "이차방정식 $x^2-(k-2)x-a(2k+1)+b=0$이 $k$의 값에 관계없이 $1$을 근으로 가질 때, $a+b$의 값은?",
    },
    "JJ-2022-G1-S1-MID-005": {
        "q": "다항식 $2x^3-x^2+2x+1$을 $2x-1$로 나누었을 때의 몫을 $Q(x)$라 하고 나머지를 $R$이라 할 때, $Q(2)+R$의 값은?",
    },
    "JJ-2022-G1-S1-MID-006": {
        "q": "다항식 $f(x)$를 $x^2-2$로 나눈 나머지가 $x+1$이다. 이때, $\\{f(x)\\}^2$을 $x^2-2$로 나눈 나머지를 $ax+b$라 할 때, $ab$의 값은?",
    },
    "JJ-2022-G1-S1-MID-007": {
        "q": "두 자리 자연수 $n$에 대하여 $z=\\dfrac{1-i}{1+i}$라 할 때, $z^{4n}+z^{2n}+z^n$의 값이 실수가 되도록 하는 자연수 $n$의 개수는?",
    },
    "JJ-2022-G1-S1-MID-008": {
        "q": "$x=\\dfrac{-1+\\sqrt{3}i}{2}$일 때, $x^3+x^2+5x-1$의 값을 $p+qi$라 할 때, $\\sqrt{3}pq$의 값은? (단, $p, q$는 실수이다.)",
    },
    "JJ-2022-G1-S1-MID-009": {
        "q": "복소수 $z=(1+i)x+(1-i)y-2+4i$일 때, $z\\overline{z}=0$이 성립하도록 하는 두 실수 $x, y$에 대하여 $x^2+y^2$의 값을 구하면?",
    },
    "JJ-2022-G1-S1-MID-010": {
        "q": "\n".join(
            [
                "세 변의 길이가 $a$, $b$, $c$인 삼각형 $ABC$가 다음 조건을 만족한다.",
                "",
                "(가) $x$에 관한 다항식",
                "$f(x)=x^3-(b+c)x^2-(b^2+c^2)x+b^3+c^3+b^2c+bc^2$",
                "은 $x-a$로 나누어 떨어진다.",
                "(나) $2b=3(a-c)$",
                "(다) 삼각형 $ABC$의 넓이는 $30$이다.",
                "",
                "삼각형 $ABC$의 둘레의 길이를 구하시오.",
            ]
        ),
    },
    "JJ-2022-G1-S1-MID-011": {
        "q": "다음 중 $(x^2+2x-5)(x^2+2x-13)-20$의 인수가 아닌 것은?",
    },
    "JJ-2022-G1-S1-MID-012": {
        "q": "다항식 $f(x)=x^3+2x^2-(k+3)x+k$가 $x$의 계수와 상수항이 정수인 세 일차식의 곱으로 인수분해될 때, $400$ 이하의 자연수 $k$의 개수는?",
    },
    "JJ-2022-G1-S1-MID-013": {
        "q": "어느 극단의 공연 관람권의 가격을 $x$만원, 한 달 동안의 공연 이익금을 $y$만원이라고 하면 $x$와 $y$ 사이에는 $y=-5x^2+80x-200$인 관계가 성립한다고 한다. 관람권의 가격을 $6$만원 이상 $9$만원 이하로 정할 때, 한 달 동안의 공연 이익금의 최댓값과 최솟값의 차이는? (단위는 만원이다.)",
    },
    "JJ-2022-G1-S1-MID-014": {
        "q": "$\\dfrac{\\sqrt{x+4}}{\\sqrt{x-1}}=-\\sqrt{\\dfrac{x+4}{x-1}}$를 만족하는 $x$의 범위에서 이차함수 $f(x)=2x^2+4x+1$의 최댓값과 최솟값의 합은?",
    },
    "JJ-2022-G1-S1-MID-015": {
        "q": "\n".join(
            [
                "최고차항의 계수가 $1$인 삼차다항식 $f(x)$가 다음 조건을 만족한다.",
                "",
                "(가) $f(1)=1+k$",
                "(나) $f(2)=2+k$",
                "(다) $f(3)=3+k$",
                "",
                "$f(x)$를 $x-5$로 나누었을 때, 나누어 떨어지도록 상수 $k$의 값을 구하면?",
            ]
        ),
    },
    "JJ-2022-G1-S1-MID-101": {
        "q": "$z$가 복소수이고 $z+\\overline{z}=4$, $z\\overline{z}=7$일 때, $\\dfrac{\\overline{z}}{z}-\\dfrac{z}{\\overline{z}}$의 값을 구하시오. (단, $z$의 허수부분은 음수이다.)",
    },
    "JJ-2022-G1-S1-MID-102": {
        "q": "다항식 $f(x)=x^4+mx^3+nx^2+8$가 $(x-a)(x-b)$를 인수로 가질 때, $m^2+n^2$의 값을 구하시오. (단, $a, b$는 서로 다른 자연수이고, $m, n$은 정수이다.)",
    },
    "JJ-2022-G1-S1-MID-103": {
        "q": "실수 $t$에 대하여 $t\\le x\\le t+2$인 함수 $f(x)=x^2-4x+6$의 최솟값을 $g(t)$라고 하자. 방정식 $g(t)=6$의 서로 다른 두 실근을 $\\alpha$, $\\beta$라 할 때, $(\\alpha-\\beta)^2$의 값을 구하시오.",
    },
    "JJ-2022-G1-S1-MID-104": {
        "q": "\n".join(
            [
                "최고차항의 계수가 $1$인 삼차식 $f(x)$가 다음 조건을 만족한다.",
                "",
                "(가) $f(x)$를 $x-1$로 나눈 나머지가 $2$이다.",
                "(나) 모든 실수 $x$에 대하여 $f(2+x)=-f(2-x)$이 성립한다.",
                "",
                "다항식 $f(x)$를 $x^2-4x+3$로 나눈 나머지를 구하시오.",
            ]
        ),
    },
    "JJ-2022-G1-S1-MID-105": {
        "q": "이차함수 $y=x^2+(a+1)x+b-1$의 그래프가 직선 $y=2x-1$과 점 $(1,1)$에서 접할 때, 실수 $a, b$의 값을 구하시오.",
    },
    "SY-2022-G1-S1-MID-003": {
        "q": "다항식 $P(x)$를 $5x+1$로 나누었을 때 몫을 $Q(x)$, 나머지를 $R$이라고 하자. 다항식 $P(x)$를 $x+\\dfrac{1}{5}$로 나누었을 때, 몫과 나머지는?",
        "choices": "\n".join(
            [
                "① 몫: $\\dfrac{1}{5}Q(x)$, 나머지: $5R$",
                "② 몫: $Q(x)$, 나머지: $R$",
                "③ 몫: $Q(x)$, 나머지: $5R$",
                "④ 몫: $5Q(x)$, 나머지: $R$",
                "⑤ 몫: $5Q(x)$, 나머지: $5R$",
            ]
        ),
    },
    "SY-2022-G1-S1-MID-004": {
        "q": "$x+y=2$를 만족하는 모든 실수 $x, y$에 대하여 등식 $ax^2+xy+by^2+x+y-4=0$이 성립할 상수 $a, b$의 값은?",
        "choices": "\n".join(
            [
                "① $a=0$, $b=\\dfrac{1}{2}$",
                "② $a=\\dfrac{1}{2}$, $b=\\dfrac{1}{2}$",
                "③ $a=\\dfrac{1}{2}$, $b=1$",
                "④ $a=1$, $b=\\dfrac{1}{2}$",
                "⑤ $a=1$, $b=1$",
            ]
        ),
    },
    "SY-2022-G1-S1-MID-006": {
        "q": "$\\displaystyle \\frac{127^3-123^3}{127^2+127\\times123+123^2}$의 값은?",
    },
    "SY-2022-G1-S1-MID-001": {
        "q": "\n".join(
            [
                "세 다항식 $A$, $B$, $C$에 대하여",
                "$A=4x^3-3x^2+2x-1$",
                "$B=2x^3-6x+8$",
                "$C=-2x^3+7x^2+3x-6$",
                "일 때, $A-2(A+B)+2(A-C)$를 계산하면?",
            ]
        ),
    },
    "SY-2022-G1-S1-MID-002": {
        "q": "$x$에 대한 다항식 $(3x^2+ax+1)(2x^2-5x-1)$의 전개식에서 $x^2$의 계수가 $-6$일 때, 상수 $a$의 값은?",
    },
    "SY-2022-G1-S1-MID-005": {
        "q": "다음 중 다항식을 인수분해한 것으로 옳지 않은 것은?",
    },
    "SY-2022-G1-S1-MID-007": {
        "q": "삼각형 $ABC$의 세 변의 길이를 각각 $a$, $b$, $c$라고 하자. 등식 $a^3+b^3+a^2b+ab^2-ac^2-bc^2=0$이 성립할 때, 삼각형 $ABC$는 어떤 삼각형인가?",
    },
    "SY-2022-G1-S1-MID-008": {
        "q": "상수 $a_0, a_1, a_2, \\cdots, a_{10}$에 대하여 등식 $(2x^2+x-4)^5=a_0+a_1x+a_2x^2+\\cdots+a_{10}x^{10}$이 $x$에 대한 항등식일 때, $a_0+a_2+a_4+a_6+a_8+a_{10}$의 값을 구하면?",
    },
    "SY-2022-G1-S1-MID-009": {
        "q": "\n".join(
            [
                "두 복소수 $z_1$, $z_2$와 각각의 켤레복소수 $\\overline{z_1}$, $\\overline{z_2}$에 대하여 다음 보기 중 항상 성립하는 것을 모두 고르면?",
                "",
                "<보기>",
                "ㄱ. $\\overline{z_1+z_2}=\\overline{z_1}+\\overline{z_2}$",
                "ㄴ. $z_1, z_2$가 모두 실수이면 $\\overline{z_1}+z_2=z_1+\\overline{z_2}$이다.",
                "ㄷ. $\\overline{z_1}=z_2$이면 $z_1+z_2$는 허수이다.",
                "ㄹ. $z_1\\overline{z_1}=0$이면 $z_1=\\overline{z_1}$이다.",
            ]
        ),
    },
    "SY-2022-G1-S1-MID-010": {
        "q": "등식 $\\sqrt{-2}\\sqrt{-8}+\\dfrac{\\sqrt{18}}{\\sqrt{-2}}-\\sqrt{-3}\\sqrt{27}=a+bi$를 만족시키는 실수 $a, b$에 대하여 $a+b$의 값은?",
    },
    "SY-2022-G1-S1-MID-011": {
        "q": "다음 그림과 같이 밑변의 길이가 $30$, 높이가 $10$인 직각삼각형 $ABC$에 내접하는 직사각형 $BFDE$를 그렸다. $\\square BFDE$의 넓이가 최대일 때, $\\square BFDE$의 둘레의 길이는?",
    },
    "SY-2022-G1-S1-MID-012": {
        "q": "실수 $x, y$에 대하여 $\\dfrac{1}{i}+\\dfrac{2}{i^2}+\\dfrac{3}{i^3}+\\dfrac{4}{i^4}+\\cdots+\\dfrac{20}{i^{20}}=x+yi$일 때, $x+y$의 값은?",
    },
    "SY-2022-G1-S1-MID-014": {
        "q": "복소수 $z=a+bi$가 $z^2=2i$를 만족시킬 때, $z+\\dfrac{2}{z}$의 값은? (단, $a, b$는 실수, $a>0$)",
    },
    "SY-2022-G1-S1-MID-015": {
        "q": "오른쪽 그림과 같이 직사각형 $ABCD$의 두 꼭짓점 $A, B$는 $x$축 위에 있고, 두 꼭짓점 $C, D$는 이차함수 $y=-x^2+8x$의 그래프 위에 있다. 직사각형 $ABCD$의 둘레의 길이의 최댓값을 구하면?",
    },
    "SY-2022-G1-S1-MID-102": {
        "q": "오른쪽 그림과 같이 한 변의 길이가 $8$인 정사각형 $ABCD$에 내접하는 정사각형 $EFGH$가 있다. 이때 점 $E, F, G, H$는 각각 변 $AB, BC, CD, DA$ 위에 있다. 정사각형 $EFGH$의 넓이의 최솟값을 구하시오.",
    },
    "SY-2022-G1-S1-MID-101": {
        "q": "이차함수 $y=x^2-2(a+k)x+k^2+2k+b$의 그래프가 실수 $k$에 관계없이 항상 $x$축과 접할 때, 실수 $a, b$의 값을 구하시오.",
    },
    "SY-2022-G1-S1-MID-103": {
        "q": "최고차항의 계수가 양수인 다항식 $f(x)$가 임의의 실수 $x$에 대하여 $\\{f(x)\\}^3=4x^2f(x)-8x^2+6x-1$을 만족시킬 때, 다항식 $\\{f(x)\\}^3$을 $x^2-1$로 나눈 나머지를 $R(x)$라 할 때, $R(1)$의 값을 구하시오.",
    },
    "SY-2022-G1-S1-MID-104": {
        "q": "$-2\\le x\\le 3$에서 함수 $y=x^2-2|x|-1$의 최댓값과 최솟값을 각각 $\\alpha$, $\\beta$라고 할 때, $\\alpha-\\beta$를 구하시오. (풀이과정에 반드시 그래프를 활용하시오.)",
    },
    "SY-2022-G1-S1-MID-105": {
        "q": "\n".join(
            [
                "(1)~(2) 문항에 대하여 서술하시오.",
                "",
                "(1) $x$에 대한 이차방정식 $(\\alpha-1)x^2-(\\alpha^2+1)x+2(\\alpha+1)=0$의 한 근이 $2$일 때, 다른 한 근을 구하시오. (단, $\\alpha$는 상수) [3점]",
                "(2) 임의의 두 실수 $A, B$에 대하여 연산 $\\star$를 $A\\star B=AB-A-B$라 할 때, $a$에 대한 방정식 $a\\star a=|2\\star a|$의 해를 구하시오. [4점]",
            ]
        ),
    },
}

SOLUTION_OVERRIDES = {
    "JEW-2022-G1-S1-MID-101": "\n".join(
        [
            "중근을 가지려면 판별식이 $0$이어야 하므로",
            "\\[",
            "(k+1)^2-4k^2=0",
            "\\]",
            "\\[",
            "3k^2-2k-1=0",
            "\\]",
            "\\[",
            "(3k+1)(k-1)=0",
            "\\]",
            "따라서",
            "\\[",
            "k=1,\\qquad k=-\\frac{1}{3}",
            "\\]",
            "이므로 그 합은",
            "\\[",
            "1-\\frac{1}{3}=\\frac{2}{3}",
            "\\]",
            "이다.",
        ]
    ),
    "JEW-2022-G1-S1-MID-104": "\n".join(
        [
            "인수분해한 식이 $(x-a)^2(x-b)$꼴이 되려면 중근을 가져야 하므로 $k$는 다음 방정식을 만족한다.",
            "\\[",
            "(k+2)^2(3k-1)^2(4k+1)^2=0",
            "\\]",
            "따라서",
            "\\[",
            "k=-2,\\qquad k=\\frac{1}{3},\\qquad k=-\\frac{1}{4}",
            "\\]",
            "이다. 실제로",
            "\\[",
            "k=-2 \\Rightarrow (x-1)^2(x+6),",
            "\\]",
            "\\[",
            "k=\\frac{1}{3} \\Rightarrow (x-1)^2\\left(x+\\frac{4}{3}\\right),",
            "\\]",
            "\\[",
            "k=-\\frac{1}{4} \\Rightarrow \\left(x+\\frac{3}{4}\\right)^2(x-1)",
            "\\]",
            "이므로 모두 조건을 만족한다. 따라서 구하는 합은",
            "\\[",
            "-2+\\frac{1}{3}-\\frac{1}{4}=-\\frac{23}{12}",
            "\\]",
            "이다.",
        ]
    ),
    "JEW-2022-G1-S1-MID-105": "\n".join(
        [
            "$P(1)=1$, $P(2)=2$, $P(3)=3$이므로 $P(x)-x$는 $x=1,2,3$을 근으로 갖는다.",
            "따라서",
            "\\[",
            "f(x)=P(x)-x=(x-1)(x-2)(x-3)",
            "\\]",
            "이고",
            "\\[",
            "P(x)=x+(x-1)(x-2)(x-3)",
            "\\]",
            "\\[",
            "=x+x^3-6x^2+11x-6=x^3-6x^2+12x-5",
            "\\]",
            "이다. 나머지정리에 의해 $P(x)$를 $x-5$로 나누었을 때의 나머지는 $P(5)$이므로",
            "\\[",
            "P(5)=5+(5-1)(5-2)(5-3)=5+4\\cdot3\\cdot2=29",
            "\\]",
            "이다.",
            "",
            "따라서 답은 다음과 같다.",
            "",
            "(1) $1, 2, 3$",
            "(2) $P(x)=x+(x-1)(x-2)(x-3)=x^3-6x^2+12x-5$",
            "(3) $29$",
        ]
    ),
    "JEW-2022-G1-S1-MID-106": "\n".join(
        [
            "(1) 백합 한 송이의 가격은 $600+x$원, 하루 판매량은 $800-x$송이이다.",
            "",
            "(2) 하루 판매액을 $R(x)$라 하면",
            "\\[",
            "R(x)=(600+x)(800-x)=-x^2+200x+480000",
            "\\]",
            "이다.",
            "",
            "(3) $R(x)$는 아래로 볼록한 이차함수이므로 최대값은 꼭짓점에서 갖는다.",
            "\\[",
            "x=-\\frac{200}{2\\cdot(-1)}=100",
            "\\]",
            "따라서 최대가 되는 가격은",
            "\\[",
            "600+100=700",
            "\\]",
            "원이다.",
            "",
            "(4) 최대 하루 판매액은",
            "\\[",
            "R(100)=700\\cdot700=490000",
            "\\]",
            "원이므로 $490000$원이다.",
        ]
    ),
    "JJ-2022-G1-S1-MID-101": "\n".join(
        [
            "$z=a+bi$라 두면",
            "\\[",
            "z+\\overline{z}=2a=4",
            "\\]",
            "이므로 $a=2$이다. 또",
            "\\[",
            "z\\overline{z}=a^2+b^2=7",
            "\\]",
            "이므로",
            "\\[",
            "4+b^2=7 \\Rightarrow b^2=3",
            "\\]",
            "이다. $z$의 허수부분이 음수이므로 $b=-\\sqrt{3}$, 즉",
            "\\[",
            "z=2-\\sqrt{3}i,\\qquad \\overline{z}=2+\\sqrt{3}i",
            "\\]",
            "이다. 따라서",
            "\\[",
            "\\frac{\\overline{z}}{z}=\\frac{(2+\\sqrt{3}i)^2}{7}=\\frac{1+4\\sqrt{3}i}{7},\\qquad",
            "\\frac{z}{\\overline{z}}=\\frac{(2-\\sqrt{3}i)^2}{7}=\\frac{1-4\\sqrt{3}i}{7}",
            "\\]",
            "이므로",
            "\\[",
            "\\frac{\\overline{z}}{z}-\\frac{z}{\\overline{z}}=\\frac{8\\sqrt{3}}{7}i",
            "\\]",
            "이다.",
        ]
    ),
    "JJ-2022-G1-S1-MID-102": "\n".join(
        [
            "$(x-a)(x-b)$가 인수이므로",
            "\\[",
            "f(x)=(x-a)(x-b)(x^2+px+q)",
            "\\]",
            "로 둘 수 있다. 전개하면",
            "\\[",
            "f(x)=x^4+(p-a-b)x^3+(q-p(a+b)+ab)x^2+\\{-q(a+b)+abp\\}x+abq",
            "\\]",
            "이다. 상수항이 $8$이고 $x$의 계수가 $0$이므로",
            "\\[",
            "abq=8,\\qquad -q(a+b)+abp=0",
            "\\]",
            "를 만족한다.",
            "서로 다른 자연수 $a, b$에 대해 $ab$는 $8$의 약수이므로 가능한 경우를 조사하면 $(a,b)=(1,2)$일 때만 정수 $p, q$가 존재한다.",
            "이때 $ab=2$이므로 $q=4$,",
            "\\[",
            "-4(1+2)+2p=0 \\Rightarrow p=6",
            "\\]",
            "이다. 따라서",
            "\\[",
            "f(x)=(x-1)(x-2)(x^2+6x+4)=x^4+3x^3-12x^2-8x+8",
            "\\]",
            "이므로 $m=3$, $n=-12$이다. 따라서",
            "\\[",
            "m^2+n^2=3^2+(-12)^2=153",
            "\\]",
            "이다.",
        ]
    ),
    "JJ-2022-G1-S1-MID-103": "\n".join(
        [
            "\\[",
            "f(x)=x^2-4x+6=(x-2)^2+2",
            "\\]",
            "이므로 꼭짓점은 $(2,2)$이다.",
            "구간 $[t, t+2]$에서의 최솟값 $g(t)$를 생각하면",
            "",
            "- $t\\le 0$이면 구간이 꼭짓점의 왼쪽에 있으므로 $g(t)=f(t+2)=t^2+2$",
            "- $0\\le t\\le 2$이면 구간 안에 $x=2$가 포함되므로 $g(t)=2$",
            "- $t\\ge 2$이면 구간이 꼭짓점의 오른쪽에 있으므로 $g(t)=f(t)=(t-2)^2+2$",
            "",
            "이제 $g(t)=6$을 풀면",
            "\\[",
            "t^2+2=6 \\Rightarrow t=-2,\\qquad (t-2)^2+2=6 \\Rightarrow t=4",
            "\\]",
            "이다. 따라서 $\\alpha=-2$, $\\beta=4$이고",
            "\\[",
            "(\\alpha-\\beta)^2=(-2-4)^2=36",
            "\\]",
            "이다.",
        ]
    ),
    "JJ-2022-G1-S1-MID-104": "\n".join(
        [
            "조건 $f(2+x)=-f(2-x)$는 그래프가 점 $(2,0)$에 대하여 점대칭임을 뜻하므로",
            "\\[",
            "f(x)=(x-2)^3+p(x-2)",
            "\\]",
            "로 둘 수 있다.",
            "또 $f(x)$를 $x-1$로 나눈 나머지가 $2$이므로 $f(1)=2$이다. 따라서",
            "\\[",
            "(-1)^3-p=2 \\Rightarrow -1-p=2 \\Rightarrow p=-3",
            "\\]",
            "이므로",
            "\\[",
            "f(x)=(x-2)^3-3(x-2)=x^3-6x^2+9x-2",
            "\\]",
            "이다.",
            "이제 $x^2-4x+3=(x-1)(x-3)$로 나눈 나머지를 $R(x)=ax+b$라 하면",
            "\\[",
            "R(1)=f(1)=2,\\qquad R(3)=f(3)=-2",
            "\\]",
            "이다. 두 점 $(1,2)$, $(3,-2)$를 지나는 일차식은",
            "\\[",
            "R(x)=-2x+4",
            "\\]",
            "이므로 구하는 나머지는 $-2x+4$이다.",
        ]
    ),
    "JJ-2022-G1-S1-MID-105": "\n".join(
        [
            "직선 $y=2x-1$이 이차함수 $y=x^2+(a+1)x+b-1$에 점 $(1,1)$에서 접하므로",
            "\\[",
            "1^2+(a+1)\\cdot1+b-1=1",
            "\\]",
            "에서",
            "\\[",
            "a+b=0",
            "\\]",
            "을 얻는다.",
            "또 접점에서의 기울기가 같아야 하므로",
            "\\[",
            "\\frac{d}{dx}\\left(x^2+(a+1)x+b-1\\right)\\Big|_{x=1}=2",
            "\\]",
            "\\[",
            "2\\cdot1+(a+1)=2 \\Rightarrow a=-1",
            "\\]",
            "이다. 따라서 $b=1$이다.",
        ]
    ),
    "SY-2022-G1-S1-MID-104": "\n".join(
        [
            "$x\\ge 0$일 때",
            "\\[",
            "y=x^2-2|x|-1=x^2-2x-1=(x-1)^2-2",
            "\\]",
            "$x<0$일 때",
            "\\[",
            "y=x^2-2|x|-1=x^2+2x-1=(x+1)^2-2",
            "\\]",
            "따라서 최솟값은 $-2$, 최댓값은 $2$이므로",
            "\\[",
            "\\alpha-\\beta=2-(-2)=4",
            "\\]",
            "따라서 답은 $4$이다.",
        ]
    ),
    "SY-2022-G1-S1-MID-101": "\n".join(
        [
            "$x$축과 접하려면 판별식이 $0$이어야 하므로",
            "\\[",
            "\\{2(a+k)\\}^2-4(k^2+2k+b)=0",
            "\\]",
            "\\[",
            "8(a-1)k+4(a^2-b)=0",
            "\\]",
            "이 식이 모든 실수 $k$에 대하여 성립해야 하므로",
            "\\[",
            "a-1=0,\\qquad a^2-b=0",
            "\\]",
            "이다. 따라서",
            "\\[",
            "a=1,\\qquad b=1",
            "\\]",
            "이다.",
        ]
    ),
    "SY-2022-G1-S1-MID-102": "\n".join(
        [
            "정사각형 $EFGH$의 한 변의 길이를 $s$, 변 $AD$와 이루는 각을 $\\theta$라 하자.",
            "정사각형 $ABCD$의 한 변의 길이가 $8$이므로",
            "\\[",
            "s\\cos\\theta+s\\sin\\theta=8",
            "\\]",
            "이고 따라서",
            "\\[",
            "s=\\frac{8}{\\sin\\theta+\\cos\\theta}",
            "\\]",
            "이다. 정사각형 $EFGH$의 넓이를 $S$라 하면",
            "\\[",
            "S=s^2=\\frac{64}{(\\sin\\theta+\\cos\\theta)^2}",
            "\\]",
            "이다. 그런데",
            "\\[",
            "(\\sin\\theta+\\cos\\theta)^2=1+\\sin2\\theta\\le 2",
            "\\]",
            "이므로",
            "\\[",
            "S\\ge \\frac{64}{2}=32",
            "\\]",
            "이다. 따라서 넓이의 최솟값은 $32$이다.",
        ]
    ),
    "SY-2022-G1-S1-MID-105": "\n".join(
        [
            "(1) 한 근이 $2$이므로",
            "\\[",
            "4(\\alpha-1)-2(\\alpha^2+1)+2(\\alpha+1)=0",
            "\\]",
            "\\[",
            "\\alpha^2-3\\alpha+2=0",
            "\\]",
            "\\[",
            "(\\alpha-1)(\\alpha-2)=0",
            "\\]",
            "$\\alpha=1$ 또는 $2$인데, $\\alpha=1$이면 이차방정식이 성립하지 않으므로 $\\alpha=2$이다.",
            "따라서",
            "\\[",
            "x^2-5x+6=0",
            "\\]",
            "이므로 다른 한 근은 $3$이다.",
            "",
            "(2) 연산의 정의에 따라",
            "\\[",
            "a\\star a=a^2-2a,\\qquad 2\\star a=a-2",
            "\\]",
            "이므로 방정식은",
            "\\[",
            "a^2-2a=|a-2|",
            "\\]",
            "가 된다. 경우를 나누면 해는 $a=-1,\\ 2$이다.",
            "",
            "따라서 답은 다음과 같다.",
            "",
            "(1) $3$",
            "(2) $-1,\\ 2$",
        ]
    ),
}

ANSWER_OVERRIDES = {
    "JJ-2022-G1-S1-MID-101": "$\\dfrac{8\\sqrt{3}}{7}i$",
    "JJ-2022-G1-S1-MID-102": "$153$",
    "JJ-2022-G1-S1-MID-103": "$36$",
    "JJ-2022-G1-S1-MID-104": "$-2x+4$",
    "JJ-2022-G1-S1-MID-105": "$a=-1$, $b=1$",
}

JJ_106_FRONT_MATTER = {
    "id": "JJ-2022-G1-S1-MID-106",
    "school": "JJ",
    "year": 2022,
    "grade": 1,
    "semester": 1,
    "exam": "MID",
    "subject": "COM1",
    "type": "subjective",
    "source_question_no": 6,
    "source_question_kind": "subjective",
    "source_question_label": "서6",
    "difficulty": 5,
    "level": 5,
    "unit": "공통수학1(2022개정)>2. 방정식과 부등식>2-1. 복소수와 이차방정식",
    "unit_l1": "공통수학1(2022개정)",
    "unit_l2": "2. 방정식과 부등식",
    "unit_l3": "2-1. 복소수와 이차방정식",
    "source": "user_upload_2026-03-06",
    "tags": [
        "수동생성",
        "PDF",
        "subjective",
        "출제번호-서6",
        "과목-COM1",
        "생성일-2026-03-07",
    ],
    "assets": [
        "assets/original/",
        "assets/original/JJ.2022.G1.S1.MID.COM1.pdf",
    ],
}

JJ_106_Q = "\n".join(
    [
        "이차항의 계수가 $1$인 이차함수 $f(x)$는 다음과 같은 조건을 만족한다.",
        "",
        "(가) $f(0)>1$",
        "(나) 이차방정식 $f(x)=0$의 두 근의 합은 $2$이다.",
        "(다) 이차방정식 $x^2-2x+3=0$의 두 근 $\\alpha$, $\\beta$에 대하여 $f(\\alpha)\\times f(\\beta)=4$이다.",
        "",
        "$f(4)$의 값을 구하시오.",
    ]
)

JJ_106_ANSWER = "$13$"

JJ_106_SOLUTION = "\n".join(
    [
        "이차항의 계수가 $1$이고 두 근의 합이 $2$이므로",
        "\\[",
        "f(x)=x^2-2x+c",
        "\\]",
        "로 둘 수 있다.",
        "이차방정식 $x^2-2x+3=0$의 근 $\\alpha$, $\\beta$에 대하여",
        "\\[",
        "\\alpha^2-2\\alpha+3=0,\\qquad \\beta^2-2\\beta+3=0",
        "\\]",
        "이므로",
        "\\[",
        "f(\\alpha)=\\alpha^2-2\\alpha+c=c-3,\\qquad f(\\beta)=c-3",
        "\\]",
        "이다. 따라서",
        "\\[",
        "(c-3)^2=f(\\alpha)f(\\beta)=4",
        "\\]",
        "\\[",
        "c-3=\\pm 2",
        "\\]",
        "이므로 $c=1$ 또는 $5$이다. 그런데 $f(0)=c>1$이므로 $c=5$이다.",
        "따라서",
        "\\[",
        "f(4)=4^2-2\\cdot4+5=13",
        "\\]",
        "이다.",
    ]
)


def translate_pua(text: str) -> str:
    for src, dst in PUA_MAP.items():
        text = text.replace(src, dst)
    return text


def read_exam_text(config: ExamConfig) -> str:
    pdf = fitz.open(config.pdf_path)
    pages = list(pdf)
    if config.skip_last_page:
        pages = pages[:-1]
    return "\n".join(translate_pua(page.get_text()) for page in pages)


def extract_blocks(config: ExamConfig) -> list[str]:
    text = read_exam_text(config)
    starts: list[int] = []
    for pattern in config.start_patterns:
        starts.extend(match.start() for match in re.finditer(pattern, text, re.M))
    starts = sorted(set(starts))
    blocks: list[str] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        block = text[start:end].strip()
        if block:
            blocks.append(block)
    return blocks


def block_problem_ids(school: str, block_count: int) -> list[str]:
    if school == "JEW":
        return [f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(1, 18)] + [
            f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(101, 107)
        ]
    if school == "JJ":
        return [f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(1, 16)] + [
            f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(101, 107)
        ]
    if school == "SY":
        return [f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(1, 16)] + [
            f"{school}-2022-G1-S1-MID-{index:03d}" for index in range(101, 106)
        ]
    raise ValueError(f"Unsupported school: {school}")


def extract_sections(problem_text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^##\s+(Q|Choices|Answer|Solution)\s*$", problem_text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(problem_text)
        sections[match.group(1)] = problem_text[start:end].strip("\n")
    return sections


def remove_scan_asset(front_matter_text: str) -> str:
    return re.sub(r"(?m)^- assets/scan\.png\s*\n?", "", front_matter_text)


def cleanup_existing_solution(problem_id: str, solution: str, answer: str, front_matter: dict[str, Any]) -> str:
    if problem_id in SOLUTION_OVERRIDES:
        return SOLUTION_OVERRIDES[problem_id].strip()

    solution = solution.replace("\x07lpha", r"\alpha")
    solution = solution.replace("\x08eta", r"\beta")
    solution = solution.replace("\x07", "\\")
    solution = solution.replace("\x08", "\\")
    solution = re.sub(r"(?m)^(따라서 정답은 .+이다\.)\n+\1$", r"\1", solution.strip())

    if str(front_matter.get("type", "")).strip().lower() == "objective":
        answer_text = answer.strip() or "(정답 미기재)"
        return f"정답은 {answer_text}이다."

    return solution.strip()


def cleanup_source_block(block: str) -> str:
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", stripped):
            continue
        if re.fullmatch(r"\d+\)", stripped):
            continue
        if stripped.startswith("시험지에 이름을 꼭 써주세요"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def collapse_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def flatten_preserving_wrap(text: str) -> str:
    text = cleanup_source_block(text).replace("\n", "")
    text = re.sub(r"(?<=[0-9])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=\))(?=\([가-힣]\))", " ", text)
    text = re.sub(r"(?<=[0-9A-Za-z])(?=□)", " ", text)
    return collapse_whitespace(text)


def latexize_math(expr: str) -> str:
    expr = expr.strip()
    if not expr:
        return expr
    expr = expr.replace("alpha", r"\alpha")
    expr = expr.replace("beta", r"\beta")
    expr = expr.replace("⋯", r"\cdots")
    expr = expr.replace("...", r"\cdots")
    expr = expr.replace("×", r"\times")
    expr = expr.replace("⋆", r"\star")
    expr = expr.replace("≤", r"\le ")
    expr = expr.replace("≥", r"\ge ")
    expr = expr.replace("≠", r"\ne ")
    expr = re.sub(r"sqrt/([\-]?\d+)", r"\\sqrt{\1}", expr)
    expr = re.sub(r"sqrt/([A-Za-z])", r"\\sqrt{\1}", expr)
    expr = re.sub(r"/([A-Za-z]\d*)", lambda m: rf"\overline{{{m.group(1)}}}", expr)
    expr = re.sub(r"([A-Za-z\)\}])(\d+)", lambda m: f"{m.group(1)}^{m.group(2)}", expr)
    expr = expr.replace(r"\alpha^2", r"\alpha^2")
    expr = re.sub(r"\s+", " ", expr)
    return expr.strip()


def wrap_math_chunks(text: str) -> str:
    parts = re.split(r"([가-힣]+)", text)
    rendered: list[str] = []
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"[가-힣]+", part):
            rendered.append(part)
            continue
        if not re.search(r"[A-Za-z0-9]", part):
            rendered.append(part)
            continue

        leading = re.match(r"^\s*", part).group(0)
        trailing = re.search(r"\s*$", part).group(0)
        core = part[len(leading) : len(part) - len(trailing) if trailing else len(part)]
        if not core:
            rendered.append(part)
            continue
        suffix_match = re.search(r"([,.:;?]+)$", core)
        suffix = suffix_match.group(1) if suffix_match else ""
        math_core = core[: -len(suffix)] if suffix else core
        if not math_core or math_core.startswith("[") and math_core.endswith("]"):
            rendered.append(part)
            continue
        rendered.append(f"{leading}${latexize_math(math_core)}${suffix}{trailing}")
    return "".join(rendered)


def cleanup_wrapped_question(text: str) -> str:
    text = re.sub(r"\s*\[\d+(?:\.\d+)?\$?점\$?\]\s*\d+\)\$?", "", text)
    text = re.sub(r"\s*\[\d+(?:\.\d+)?\$?점\$?\]\s*$", "", text)
    replacements = {
        "$?": "?",
        "$.": ".",
        "$,": ",",
        "$)": ")",
        "$]": "]",
        "($": "(",
        "[$": "[",
        "<서술형$>": "<서술형>",
        "서답형$": "서답형",
        "서술형$": "서술형",
        "[서답형$": "[서답형",
        "[서술형$": "[서술형",
        "점$]": "점]",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"\$\s+", "$ ", text)
    text = re.sub(r"\s+\$", " $", text)
    return text.strip()


def generic_question_markdown(problem_id: str, stem_text: str) -> str:
    override = MANUAL_SECTIONS.get(problem_id, {}).get("q")
    if override is not None:
        return override.strip()

    stem_text = cleanup_source_block(stem_text)
    stem_text = re.sub(r"^\d+\.\s*", "", stem_text)
    stem_text = flatten_preserving_wrap(stem_text)
    stem_text = re.sub(r"\s*\[\d+(?:\.\d+)?점\]\s*$", "", stem_text)
    return cleanup_wrapped_question(wrap_math_chunks(stem_text).strip())


def generic_choices_markdown(problem_id: str, choices: list[tuple[str, str]]) -> str:
    override = MANUAL_SECTIONS.get(problem_id, {}).get("choices")
    if override is not None:
        return override.strip()

    rendered = []
    for marker, raw_choice in choices:
        choice_text = flatten_preserving_wrap(raw_choice)
        rendered.append(f"{marker} {wrap_math_chunks(choice_text).strip()}")
    return "\n".join(rendered).strip()


def split_objective_block(block: str) -> tuple[str, list[tuple[str, str]]]:
    matches = list(re.finditer(f"[{CHOICE_MARKERS}]", block))
    if not matches:
        return block, []

    stem = block[: matches[0].start()].strip()
    choices: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        choices.append((match.group(0), block[start:end].strip()))
    return stem, choices


def render_body(problem_id: str, current_text: str, block_text: str) -> str:
    front_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", current_text, re.S)
    if not front_match:
        raise ValueError(f"{problem_id}: front matter not found.")

    front_matter_text = remove_scan_asset(front_match.group(1))
    body_text = current_text[front_match.end() :]
    front_matter = yaml.safe_load(front_matter_text) or {}
    sections = extract_sections(body_text)

    q_md = ""
    choices_md = ""
    problem_type = str(front_matter.get("type", "")).strip().lower()
    if problem_type == "objective":
        stem, choices = split_objective_block(block_text)
        q_md = generic_question_markdown(problem_id, stem)
        choices_md = generic_choices_markdown(problem_id, choices)
    else:
        q_md = generic_question_markdown(problem_id, block_text)
        choices_md = ""

    answer_md = ANSWER_OVERRIDES.get(problem_id, sections.get("Answer", "").strip())
    solution_md = cleanup_existing_solution(
        problem_id,
        sections.get("Solution", ""),
        answer_md,
        front_matter,
    )

    body = "\n".join(
        [
            "## Q",
            q_md.strip(),
            "",
            "## Choices",
            choices_md.strip(),
            "",
            "## Answer",
            answer_md,
            "",
            "## Solution",
            solution_md,
            "",
        ]
    )
    return f"---\n{front_matter_text.strip()}\n---\n{body}"


def write_existing_problem(problem_id: str, block_text: str) -> None:
    problem_path = PROBLEM_ROOT / problem_id / "problem.md"
    current_text = problem_path.read_text(encoding="utf-8")
    rendered = render_body(problem_id, current_text, block_text)
    problem_path.write_text(rendered, encoding="utf-8")


def write_jj_106(block_text: str) -> None:
    problem_dir = PROBLEM_ROOT / "JJ-2022-G1-S1-MID-106"
    problem_dir.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(
        JJ_106_FRONT_MATTER,
        allow_unicode=True,
        sort_keys=False,
    ).strip()
    body = "\n".join(
        [
            "## Q",
            JJ_106_Q,
            "",
            "## Choices",
            "",
            "## Answer",
            JJ_106_ANSWER,
            "",
            "## Solution",
            JJ_106_SOLUTION,
            "",
        ]
    )
    (problem_dir / "problem.md").write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")
    original_dir = problem_dir / "assets" / "original"
    original_dir.mkdir(parents=True, exist_ok=True)
    target_pdf = original_dir / "JJ.2022.G1.S1.MID.COM1.pdf"
    source_pdf = ORIGINAL_ROOT / "JJ.2022.G1.S1.MID.COM1.pdf"
    if not target_pdf.exists():
        target_pdf.write_bytes(source_pdf.read_bytes())


def restore_exam(school: str) -> None:
    config = CONFIGS[school]
    blocks = extract_blocks(config)
    ids = block_problem_ids(school, len(blocks))
    if len(blocks) != len(ids):
        raise ValueError(f"{school}: expected {len(ids)} blocks, got {len(blocks)}.")

    for problem_id, block in zip(ids, blocks, strict=True):
        if problem_id == "JJ-2022-G1-S1-MID-106":
            write_jj_106(block)
        else:
            write_existing_problem(problem_id, block)


def main() -> None:
    for school in EXAM_CODES:
        restore_exam(school)
        print(f"{school}: restored")


if __name__ == "__main__":
    main()
