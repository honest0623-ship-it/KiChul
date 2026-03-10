from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys
from typing import Dict, List, Tuple

import fitz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "JJ.2024.G2.S1.MID2.STAT.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

QUESTION_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    1: (1, (20, 170, 355, 250)),
    2: (1, (20, 380, 355, 470)),
    3: (1, (20, 620, 355, 900)),
    4: (1, (372, 45, 710, 150)),
    5: (1, (372, 340, 710, 415)),
    6: (1, (372, 625, 710, 745)),
    7: (2, (20, 45, 355, 130)),
    8: (2, (20, 325, 355, 445)),
    9: (2, (20, 605, 355, 785)),
    10: (2, (372, 45, 710, 130)),
    11: (2, (372, 330, 710, 430)),
    12: (2, (372, 610, 710, 690)),
    13: (3, (20, 60, 360, 240)),
    14: (3, (20, 375, 320, 465)),
    15: (3, (20, 640, 360, 745)),
    16: (3, (372, 60, 710, 155)),
    17: (3, (372, 465, 710, 760)),
    18: (4, (20, 45, 355, 120)),
    19: (4, (20, 450, 355, 620)),
    20: (4, (372, 45, 710, 150)),
}

SCAN_CROPS: Dict[int, Tuple[int, Tuple[float, float, float, float]]] = {
    3: (1, (100, 715, 305, 807)),
    17: (3, (455, 560, 700, 735)),
}

STAT_FALLBACK_UNIT_L3: Dict[int, str] = {
    1: "1-1. 순열",
    2: "1-1. 순열",
    3: "1-1. 순열",
    4: "1-1. 순열",
    5: "1-2. 조합",
    6: "1-2. 조합",
    7: "1-1. 순열",
    8: "1-1. 순열",
    9: "1-2. 조합",
    10: "1-2. 조합",
    11: "1-2. 조합",
    12: "1-2. 조합",
    13: "1-1. 순열",
    14: "1-2. 조합",
    15: "1-2. 조합",
    16: "1-1. 순열",
    17: "1-1. 순열",
    18: "1-2. 조합",
    19: "1-1. 순열",
    20: "1-2. 조합",
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
        q="$ {}_{2}H_{5}+{}_{2}\\Pi_{5}$의 값은?",
        choices=["31", "35", "38", "42", "57"],
        answer="③",
        solution=(
            "$ {}_{2}H_{5}={}_{6}C_{5}=6$이고, $ {}_{2}\\Pi_{5}=2^{5}=32$이다.\n"
            "따라서 구하는 값은\n"
            "$$\n"
            "6+32=38\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=2,
        qtype="객관식",
        q="0, 1, 2, 3, 4, 5에서 중복을 허용하여 3개를 뽑아 만들 수 있는 세 자리 자연수의 개수는?",
        choices=["60", "100", "120", "180", "216"],
        answer="④",
        solution=(
            "천의 자리는 0이 될 수 없으므로 5가지,\n"
            "백의 자리와 십의 자리는 각각 6가지이다.\n"
            "따라서 곱의 법칙에 의해\n"
            "$$\n"
            "5\\times 6\\times 6=180\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=3,
        qtype="객관식",
        q=(
            "다음 그림은 중심이 같은 두 원 사이를 4등분 한 도형이다. 서로 다른 5개의 색을 모두 사용하여 "
            "이 도형의 각 영역을 칠하는 경우의 수는? (단, 한 영역에는 한 가지 색만 칠하고, 회전하여 일치하는 것은 같은 것으로 본다.)\n\n"
            '<img src="assets/scan.png" alt="원형 도형" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices=["30", "36", "60", "90", "120"],
        answer="①",
        solution=(
            "가운데 원의 색을 정하는 방법은 5가지이다.\n"
            "바깥의 4영역은 서로 다른 4색을 원형으로 배열하는 경우와 같으므로\n"
            "원순열의 수는 $(4-1)!=6$이다.\n"
            "따라서 전체 경우의 수는\n"
            "$$\n"
            "5\\times 6=30\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=4,
        qtype="객관식",
        q="7개의 문자 $a,a,a,b,b,b,c$를 모두 일렬로 나열할 때, 3개의 문자 $b$가 모두 문자 $c$보다 왼쪽에 있는 경우의 수는?",
        choices=["20", "35", "60", "75", "120"],
        answer="②",
        solution=(
            "서로 같은 문자를 고려한 전체 배열 수는\n"
            "$$\n"
            "\\frac{7!}{3!3!}=140\n"
            "$$\n"
            "이다.\n"
            "$b,b,b,c$의 상대적 순서에서 $c$의 위치는 4곳이 대칭적으로 같게 나타나므로,\n"
            "조건 \"$b$가 모두 $c$의 왼쪽\"인 경우는 전체의 $\\dfrac{1}{4}$이다.\n"
            "따라서\n"
            "$$\n"
            "140\\div 4=35\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=5,
        qtype="객관식",
        q="$ {}_{n-1}C_{8}+{}_{n-1}C_{9}={}_{n}C_{7}$를 만족시키는 $n$의 값은?",
        choices=["10", "11", "13", "15", "16"],
        answer="⑤",
        solution=(
            "조합의 성질\n"
            "$$\n"
            "{}_{n-1}C_{r-1}+{}_{n-1}C_{r}={}_{n}C_{r}\n"
            "$$\n"
            "을 이용하면\n"
            "$$\n"
            "{}_{n-1}C_{8}+{}_{n-1}C_{9}={}_{n}C_{9}\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "{}_{n}C_{9}={}_{n}C_{7}\n"
            "$$\n"
            "이다.\n"
            "조합의 대칭성으로 $9=n-7$이어서 $n=16$이다."
        ),
    ),
    Entry(
        exam_no=6,
        qtype="객관식",
        q=(
            "세 종류의 카드가 각각 3장씩 총 9장의 카드가 들어 있는 주머니에서 5장의 카드를 동시에 꺼낼 때, "
            "세 종류의 카드가 적어도 1장씩 포함되도록 하는 경우의 수는? (단, 같은 종류의 카드는 구별하지 않는다.)"
        ),
        choices=["3", "4", "6", "8", "9"],
        answer="③",
        solution=(
            "세 종류에서 뽑힌 장수를 $(x,y,z)$라 하면\n"
            "$$\n"
            "x+y+z=5,\\quad 1\\le x,y,z\\le 3\n"
            "$$\n"
            "이다.\n"
            "가능한 분배는\n"
            "$$\n"
            "(3,1,1)\\text{의 순열 3가지},\\quad (2,2,1)\\text{의 순열 3가지}\n"
            "$$\n"
            "뿐이다.\n"
            "따라서 조합적 분배 경우의 수는\n"
            "$$\n"
            "3+3=6\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=7,
        qtype="객관식",
        q="일곱 개의 숫자 $0,1,1,2,2,2,3$을 모두 사용하여 만들 수 있는 일곱 자리의 자연수 중에서 짝수의 개수는?",
        choices=["120", "150", "180", "210", "240"],
        answer="④",
        solution=(
            "끝자리가 0인 경우:\n"
            "남은 6자리 배열 수는\n"
            "$$\n"
            "\\frac{6!}{2!3!}=60\n"
            "$$\n"
            "이다.\n\n"
            "끝자리가 2인 경우:\n"
            "남은 배열 수는\n"
            "$$\n"
            "\\frac{6!}{2!2!}=180\n"
            "$$\n"
            "인데, 맨 앞이 0인 경우\n"
            "$$\n"
            "\\frac{5!}{2!2!}=30\n"
            "$$\n"
            "을 빼면 $150$이다.\n\n"
            "따라서 전체는\n"
            "$$\n"
            "60+150=210\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=8,
        qtype="객관식",
        q=(
            "현재 자물쇠 비밀번호는 1010이다. 네 개의 숫자 0, 1, 2, 3에서 중복을 허용하여 4개를 뽑아 "
            "비밀번호를 바꾸려고 한다. 바꿀 수 있는 비밀번호의 개수는? (단, 자물쇠 비밀번호는 네 자리이다.)"
        ),
        choices=["23", "127", "128", "255", "256"],
        answer="④",
        solution=(
            "4자리 비밀번호 전체 개수는\n"
            "$$\n"
            "4^{4}=256\n"
            "$$\n"
            "가지이다.\n"
            "현재 비밀번호 1010은 제외해야 하므로\n"
            "$$\n"
            "256-1=255\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=9,
        qtype="객관식",
        q=(
            "<보기>에서 옳은 것만 있는 대로 고른 것은?\n\n"
            + box(
                [
                    "ㄱ. $ {}_{5}C_{0}+{}_{5}C_{1}+\\cdots+{}_{5}C_{5}=2^{5}$",
                    "ㄴ. $ {}_{11}C_{0}+{}_{11}C_{1}+\\cdots+{}_{11}C_{5}=2^{10}$",
                    "ㄷ. $ {}_{3n}C_{0}+{}_{3n}C_{1}+\\cdots+{}_{3n}C_{3n}=6^{n}$",
                ]
            )
        ),
        choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        answer="②",
        solution=(
            "ㄱ. 이항정리에 의해\n"
            "$$\n"
            "(1+1)^{5}=\\sum_{k=0}^{5} {}_{5}C_{k}=2^{5}\n"
            "$$\n"
            "이므로 참이다.\n\n"
            "ㄴ. $11$은 홀수이므로 조합의 대칭성에 의해\n"
            "$$\n"
            "{}_{11}C_{0}+{}_{11}C_{1}+\\cdots+{}_{11}C_{5}=2^{10}\n"
            "$$\n"
            "이어서 참이다.\n\n"
            "ㄷ. 왼쪽은 전체 합이므로\n"
            "$$\n"
            "\\sum_{k=0}^{3n} {}_{3n}C_{k}=2^{3n}=8^{n}\n"
            "$$\n"
            "이다. 따라서 $6^{n}$이 아니므로 거짓이다.\n"
            "정답은 ㄱ, ㄴ이다."
        ),
    ),
    Entry(
        exam_no=10,
        qtype="객관식",
        q=(
            "100 이하의 자연수 $n$ 중에서 $ {}_{n}C_{1}+{}_{n}C_{2}+{}_{n}C_{3}+\\cdots+{}_{n}C_{n}$의 값이 "
            "5의 배수가 되도록 하는 자연수 $n$의 개수는?"
        ),
        choices=["20", "21", "22", "24", "25"],
        answer="⑤",
        solution=(
            "이항정리로\n"
            "$$\n"
            "{}_{n}C_{1}+{}_{n}C_{2}+\\cdots+{}_{n}C_{n}=2^{n}-1\n"
            "$$\n"
            "이다.\n"
            "따라서 $2^{n}$을 5로 나누었을 때 나머지가 1이어야 한다.\n"
            "$2^{1},2^{2},2^{3},2^{4}$를 5로 나눈 나머지는 차례로 $2,4,3,1$이고,\n"
            "이 패턴이 4번마다 반복된다.\n"
            "그러므로 $n$은 4의 배수여야 한다.\n"
            "1부터 100까지 4의 배수는\n"
            "$$\n"
            "100\\div 4=25\n"
            "$$\n"
            "개이다."
        ),
    ),
    Entry(
        exam_no=11,
        qtype="객관식",
        q="$\\left(ax+\\dfrac{1}{x^{2}}\\right)^{6}$의 전개식에서 상수항과 $\\dfrac{1}{x^{3}}$의 계수가 서로 같을 때, $3a$의 값은? (단, $a>0$)",
        choices=["3", "4", "5", "6", "7"],
        answer="②",
        solution=(
            "전개식의 일반항은\n"
            "$$\n"
            "{}_{6}C_{k}(ax)^{6-k}\\left(\\frac{1}{x^{2}}\\right)^{k}\n"
            "={}_{6}C_{k}a^{6-k}x^{6-3k}\n"
            "$$\n"
            "이다.\n"
            "상수항은 $6-3k=0$이므로 $k=2$에서 계수 $15a^{4}$,\n"
            "$\\dfrac{1}{x^{3}}$항은 $6-3k=-3$이므로 $k=3$에서 계수 $20a^{3}$이다.\n"
            "두 계수가 같아야 하므로\n"
            "$$\n"
            "15a^{4}=20a^{3}\n"
            "$$\n"
            "$a>0$에서 $a=\\dfrac{4}{3}$.\n"
            "따라서\n"
            "$$\n"
            "3a=4\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=12,
        qtype="객관식",
        q="$\\left(x^{2}+1\\right)^{3}\\left(x+\\dfrac{1}{x}\\right)^{5}$의 전개식에서 $x^{9}$의 계수는?",
        choices=["8", "11", "14", "17", "20"],
        answer="①",
        solution=(
            "$\\left(x^{2}+1\\right)^{3}$의 항을 ${}_{3}C_{i}x^{2i}$,\n"
            "$\\left(x+\\dfrac{1}{x}\\right)^{5}$의 항을 ${}_{5}C_{j}x^{5-2j}$로 두면\n"
            "지수 조건은\n"
            "$$\n"
            "2i+5-2j=9\n"
            "$$\n"
            "즉 $i-j=2$이다.\n"
            "가능한 쌍은 $(i,j)=(2,0),(3,1)$이므로 계수는\n"
            "$$\n"
            "{}_{3}C_{2}{}_{5}C_{0}+{}_{3}C_{3}{}_{5}C_{1}=3+5=8\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=13,
        qtype="객관식",
        q=(
            "네 명의 학생 $A,B,C,D$를 포함한 8명의 학생이 원탁에 둘러앉을 때, 다음 조건을 모두 만족시키는 경우의 수는?\n\n"
            + box(
                [
                    "(가) $A$와 $C$는 이웃하게 앉는다.",
                    "(나) $B$와 $C$는 이웃하게 앉는다.",
                    "(다) $B$와 $D$는 이웃하지 않게 앉는다.",
                ]
            )
        ),
        choices=["120", "144", "168", "192", "216"],
        answer="④",
        solution=(
            "$A,C,B$를 붙어 있는 하나의 블록으로 보면(방향 2가지),\n"
            "나머지 5명과 함께 총 6개 대상을 원탁에 배열하는 경우이다.\n"
            "따라서 먼저\n"
            "$$\n"
            "2\\times (6-1)!=2\\times 120=240\n"
            "$$\n"
            "가지이다.\n"
            "여기서 $B$와 $D$가 이웃한 경우를 뺀다.\n"
            "$D$를 $B$ 옆에 붙인 블록으로 보면 대상 수는 5개이고,\n"
            "방향 2가지를 고려하면\n"
            "$$\n"
            "2\\times (5-1)!=2\\times 24=48\n"
            "$$\n"
            "가지이다.\n"
            "따라서 구하는 경우의 수는\n"
            "$$\n"
            "240-48=192\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=14,
        qtype="객관식",
        q="$102^{20}$을 200으로 나누었을 때의 나머지는?",
        choices=["80", "104", "128", "152", "176"],
        answer="⑤",
        solution=(
            "$102^{2}=10404$이므로 200으로 나눈 나머지는 4이다.\n"
            "따라서\n"
            "$$\n"
            "102^{4}\\text{의 나머지}=4^{2}=16\n"
            "$$\n"
            "$$\n"
            "102^{8}\\text{의 나머지}=16^{2}=256\\text{의 나머지}=56\n"
            "$$\n"
            "$$\n"
            "102^{16}\\text{의 나머지}=56^{2}=3136\\text{의 나머지}=136\n"
            "$$\n"
            "이다.\n"
            "그러므로\n"
            "$$\n"
            "102^{20}=102^{16}\\cdot 102^{4}\n"
            "$$\n"
            "의 나머지는\n"
            "$$\n"
            "136\\times 16=2176\\text{의 나머지}=176\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=15,
        qtype="객관식",
        q=(
            "방정식 $a+b+c+4d=e\\,(13\\le e\\le 16)$을 만족시키는 자연수 $a,b,c,d,e$의 모든 순서쌍 "
            "$(a,b,c,d,e)$의 개수와 같은 것은?"
        ),
        choices=["$ {}_{11}C_{3}$", "$ {}_{11}C_{4}$", "$ {}_{12}C_{3}$", "$ {}_{12}C_{4}$", "$ {}_{13}C_{3}$"],
        answer="③",
        solution=(
            "$e$를 고정하고 $d$를 나누어 센다.\n"
            "$e=13$일 때는 $(d,a+b+c)=(1,9),(2,5)$여서\n"
            "$$\n"
            "{}_{8}C_{2}+{}_{4}C_{2}=28+6=34\n"
            "$$\n"
            "이다.\n"
            "같은 방식으로\n"
            "$$\n"
            "e=14:\\ 36+10=46\n"
            "$$\n"
            "$$\n"
            "e=15:\\ 45+15+1=61\n"
            "$$\n"
            "$$\n"
            "e=16:\\ 55+21+3=79\n"
            "$$\n"
            "이다.\n"
            "전체는\n"
            "$$\n"
            "34+46+61+79=220\n"
            "$$\n"
            "이고, 보기에서\n"
            "$$\n"
            "{}_{12}C_{3}=220\n"
            "$$\n"
            "이므로 정답은 ③이다."
        ),
    ),
    Entry(
        exam_no=16,
        qtype="서답형(단답형)",
        q=(
            "좌표평면 위에서 좌우 방향 또는 상하 방향으로 한 번에 한 칸씩 움직이는 점 $A$가 있다. "
            "원점 $O$에서 출발한 점 $A$가 5번 움직여서 점 $B(1,2)$의 위치에 오는 경우의 수를 구하시오."
        ),
        choices=[],
        answer="50",
        solution=(
            "오른쪽, 왼쪽, 위, 아래 이동 횟수를 각각 $R,L,U,D$라 하면\n"
            "$$\n"
            "R-L=1,\\quad U-D=2,\\quad R+L+U+D=5\n"
            "$$\n"
            "이다.\n"
            "$R=L+1$, $U=D+2$를 대입하면\n"
            "$$\n"
            "2L+2D+3=5\\Rightarrow L+D=1\n"
            "$$\n"
            "이므로 경우는 두 가지이다.\n\n"
            "1. $(L,D)=(0,1)$이면 $(R,U)=(1,3)$\n"
            "$$\n"
            "\\frac{5!}{1!3!1!}=20\n"
            "$$\n"
            "2. $(L,D)=(1,0)$이면 $(R,U)=(2,2)$\n"
            "$$\n"
            "\\frac{5!}{2!2!1!}=30\n"
            "$$\n"
            "따라서 전체 경우의 수는\n"
            "$$\n"
            "20+30=50\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=17,
        qtype="서답형(단답형)",
        q=(
            "다음 그림과 같은 도로망이 있다. $A$지점에서 출발하여 $B$지점을 지나 $C$지점에 도착하는 "
            "최단 경로의 수를 구하시오. (단, 한 번 지나온 길은 다시 돌아가지 않는다.)\n\n"
            '<img src="assets/scan.png" alt="도로망" style="width:60% !important; max-width:60% !important; height:auto;" />'
        ),
        choices=[],
        answer="235",
        solution=(
            "$A$에서 $B$까지 가는 경우의 수는 15가지이다.\n"
            "이를 두 경우로 나누어 센다.\n"
            "1. $B$를 지나는 세로선의 일부를 이미 지나온 경우: 10가지\n"
            "이때마다 $B$에서 $C$까지는 11가지\n"
            "2. 위 경우가 아닌 경우: 5가지\n"
            "이때마다 $B$에서 $C$까지는 25가지\n"
            "따라서 전체 경우의 수는\n"
            "$$\n"
            "10\\times 11+5\\times 25=235\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=18,
        qtype="서답형(단답형)",
        q="집합 $X=\\{1,2,3,4,5\\}$에서 집합 $Y=\\{a,b\\}$로의 함수 중에서 치역과 공역이 서로 같은 것의 개수를 구하시오.",
        choices=[],
        answer="30",
        solution=(
            "$X$의 각 원소는 $a,b$ 중 하나로 대응되므로 전체 함수 수는\n"
            "$$\n"
            "2^{5}=32\n"
            "$$\n"
            "이다.\n"
            "치역이 공역과 같지 않은 경우는\n"
            "모든 원소가 $a$로 가는 경우, 모든 원소가 $b$로 가는 경우의 2가지뿐이다.\n"
            "따라서 구하는 개수는\n"
            "$$\n"
            "32-2=30\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=19,
        qtype="서답형(서술형)",
        q=(
            "두 단계로 구성된 $A,B,C$ 미션이 있다. 각 미션은 1단계를 통과해야 2단계 미션을 통과할 수 있다. 예를 들어,\n\n"
            + box([
                "$A(1\\text{단계}) \\rightarrow B(1\\text{단계}) \\rightarrow A(2\\text{단계})$",
                "$\\rightarrow C(1\\text{단계}) \\rightarrow B(2\\text{단계}) \\rightarrow C(2\\text{단계})$",
            ])
            + "\n\n6개의 미션을 모두 수행하는 경우의 수를 구하시오."
        ),
        choices=[],
        answer="90",
        solution=(
            "수행 순서를 $A_{1},A_{2},B_{1},B_{2},C_{1},C_{2}$의 배열로 보면\n"
            "전체 순열 수는\n"
            "$$\n"
            "6!\n"
            "$$\n"
            "이다.\n"
            "각 미션마다 1단계가 2단계보다 먼저 와야 하므로\n"
            "각 쌍에서 절반만 허용된다.\n"
            "세 쌍을 반영하면\n"
            "$$\n"
            "\\frac{6!}{2^{3}}=\\frac{720}{8}=90\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=20,
        qtype="서답형(서술형)",
        q=(
            "다음 조건을 만족시키는 자연수 $N$의 개수를 구하시오.\n\n"
            + box([
                "(가) $N$은 4자리의 자연수이며, 짝수이다.",
                "(나) $N$의 각 자리의 수의 합은 6이다.",
            ])
        ),
        choices=[],
        answer="34",
        solution=(
            "천, 백, 십, 일의 자리를 $a,b,c,d$라 하면\n"
            "$$\n"
            "a+b+c+d=6,\\quad a\\ge 1,\\quad d\\text{는 짝수}\n"
            "$$\n"
            "이다.\n"
            "$d=0,2,4,6$으로 나누어 센다.\n\n"
            "1. $d=0$: $a-1+b+c=5$\n"
            "$$\n"
            "{}_{7}C_{2}=21\n"
            "$$\n"
            "2. $d=2$: $a-1+b+c=3$\n"
            "$$\n"
            "{}_{5}C_{2}=10\n"
            "$$\n"
            "3. $d=4$: $a-1+b+c=1$\n"
            "$$\n"
            "{}_{3}C_{2}=3\n"
            "$$\n"
            "4. $d=6$: 불가능\n\n"
            "따라서 전체 개수는\n"
            "$$\n"
            "21+10+3=34\n"
            "$$\n"
            "이다."
        ),
    ),
]


def parse_pdf_meta(pdf_name: str) -> dict:
    parts = pdf_name.split(".")
    if len(parts) != 7 or parts[-1].lower() != "pdf":
        raise ValueError(f"unexpected pdf filename format: {pdf_name}")
    school, year, gtoken, stoken, exam, subject, _ = parts
    if not gtoken.upper().startswith("G") or not stoken.upper().startswith("S"):
        raise ValueError(f"unexpected grade/semester token in filename: {pdf_name}")
    meta = {
        "school": school.upper(),
        "year": int(year),
        "grade": int(gtoken[1:]),
        "semester": int(stoken[1:]),
        "exam": exam.upper(),
        "subject": subject.upper(),
    }
    return meta


def id_info(exam_no: int) -> Tuple[int, int, str, str]:
    if exam_no <= 15:
        pid_no = exam_no
        source_no = exam_no
        source_kind = "objective"
        source_label = str(source_no)
    else:
        source_no = exam_no - 15
        pid_no = 100 + source_no
        source_kind = "subjective"
        source_label = f"서답{source_no}번"
    return pid_no, source_no, source_kind, source_label


def export_crop(doc: fitz.Document, page_no: int, rect_vals: Tuple[float, float, float, float], out_path: Path) -> None:
    rect = fitz.Rect(*rect_vals)
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "")


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
    subject_ko = {
        "COM1": "공통수학1",
        "COM2": "공통수학2",
        "ALG": "대수",
        "CAL1": "미적분1",
        "STAT": "확률과통계",
    }.get(meta["subject"], meta["subject"])

    assets = []
    if has_scan:
        assets.append("assets/scan.png")
    assets.extend([
        "assets/original/",
        f"assets/original/{original_asset_name}",
    ])

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
        f"- 과목-{subject_ko}",
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


def process_range(start_no: int, end_no: int, rewrite_existing: bool = False) -> None:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"source PDF not found: {SOURCE_PDF}")

    meta = parse_pdf_meta(SOURCE_PDF.name)
    prefix = f"{meta['school']}-{meta['year']}-G{meta['grade']}-S{meta['semester']}-{meta['exam']}-{meta['subject']}"

    doc = fitz.open(SOURCE_PDF)

    created: List[str] = []
    updated: List[str] = []
    skipped_duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    results: List[Tuple[str, str, str]] = []
    review_paths: List[str] = []

    target_entries = [e for e in ENTRIES if start_no <= e.exam_no <= end_no]

    for entry in target_entries:
        if entry.exam_no not in QUESTION_CROPS:
            warnings.append(f"exam_no {entry.exam_no}: question crop is not defined")
            continue

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

        page_no, rect_vals = QUESTION_CROPS[entry.exam_no]
        original_asset_name = f"{SOURCE_PDF.stem}_q{entry.exam_no:03d}.png"
        export_crop(doc, page_no, rect_vals, assets_original / original_asset_name)

        has_scan = entry.exam_no in SCAN_CROPS
        if has_scan:
            scan_page, scan_rect = SCAN_CROPS[entry.exam_no]
            export_crop(doc, scan_page, scan_rect, pdir / "assets" / "scan.png")
        else:
            scan_path = pdir / "assets" / "scan.png"
            if scan_path.exists():
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

        unit_l1 = cls.unit_l1
        unit_l2 = cls.unit_l2
        unit_l3 = cls.unit_l3

        if cls.unit_l1 != "확률과 통계(2022개정)":
            unit_l1 = "확률과 통계(2022개정)"
            unit_l2 = "1. 경우의 수"
            unit_l3 = STAT_FALLBACK_UNIT_L3.get(entry.exam_no, "1-2. 조합")
            warnings.append(
                f"{pid}: classifier unit outside STAT -> {cls.unit_l1}>{cls.unit_l2}>{cls.unit_l3} ({cls.reason}); "
                f"fallback={unit_l3}"
            )

        content = build_markdown(
            pid=pid,
            meta=meta,
            entry=entry,
            source_no=source_no,
            source_kind=source_kind,
            source_label=source_label,
            level=cls.level,
            unit_l1=unit_l1,
            unit_l2=unit_l2,
            unit_l3=unit_l3,
            original_asset_name=original_asset_name,
            has_scan=has_scan,
        )
        md_path.write_text(content, encoding="utf-8", newline="\n")

        if existed:
            updated.append(pid)
            results.append((pid, "UPDATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={cls.level}"))
        else:
            created.append(pid)
            results.append((pid, "CREATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={cls.level}"))

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
    parser = argparse.ArgumentParser(description="Manual ingest for JJ 2024 G2 S1 MID2 STAT")
    parser.add_argument("--start", type=int, default=1, help="start exam number (1~20)")
    parser.add_argument("--end", type=int, default=20, help="end exam number (1~20)")
    parser.add_argument(
        "--rewrite-existing",
        action="store_true",
        help="rewrite existing JJ-2024 target folders instead of skipping duplicates",
    )
    args = parser.parse_args()

    if args.start < 1 or args.end > 20 or args.start > args.end:
        raise ValueError("invalid range: expected 1 <= start <= end <= 20")

    process_range(args.start, args.end, rewrite_existing=args.rewrite_existing)
