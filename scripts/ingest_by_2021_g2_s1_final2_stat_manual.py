from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys
from typing import Dict, List, Tuple

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
SOURCE_PDF = ORIGINAL / "BY.2021.G2.S1.FINAL2.STAT.pdf"
SOURCE_TAG = "user_upload_2026-03-06"

# Coordinates are on 2x rendered page images rotated to upright orientation.
QUESTION_CROPS: Dict[int, Tuple[int, Tuple[int, int, int, int]]] = {
    1: (1, (70, 470, 725, 920)),
    2: (1, (70, 960, 725, 1385)),
    3: (1, (70, 1450, 725, 1940)),
    4: (1, (735, 260, 1395, 900)),
    5: (1, (735, 940, 1395, 1400)),
    6: (1, (735, 1460, 1395, 1940)),
    7: (2, (70, 250, 725, 820)),
    8: (2, (70, 820, 725, 1360)),
    9: (2, (70, 1360, 725, 1940)),
    10: (2, (735, 250, 1395, 820)),
    11: (2, (735, 820, 1395, 1360)),
    12: (2, (735, 1360, 1395, 1940)),
    13: (3, (70, 250, 725, 810)),
    14: (3, (70, 810, 725, 1360)),
    15: (3, (70, 1360, 725, 1940)),
    16: (3, (735, 250, 1395, 810)),
    17: (3, (735, 810, 1395, 1360)),
    18: (3, (735, 1360, 1395, 1940)),
    101: (4, (70, 250, 725, 620)),
    102: (4, (70, 620, 725, 910)),
    103: (4, (70, 1140, 725, 2045)),
    104: (4, (735, 250, 1395, 1820)),
}


@dataclass(frozen=True)
class Entry:
    exam_no: int
    qtype: str
    q: str
    choices: List[str]
    answer: str
    solution: str
    uncertain: bool = False


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
        q="$P(A)=\\dfrac{1}{3},\\ P(B^{c})=\\dfrac{3}{4},\\ P(A\\cup B)=\\dfrac{1}{2}$일 때, $P(A\\cap B)$는?",
        choices=[
            "$\\dfrac{1}{6}$",
            "$\\dfrac{1}{8}$",
            "$\\dfrac{1}{10}$",
            "$\\dfrac{1}{12}$",
            "$\\dfrac{1}{14}$",
        ],
        answer="④",
        solution=(
            "$P(B)=1-P(B^{c})=1-\\dfrac{3}{4}=\\dfrac{1}{4}$.\n"
            "따라서\n"
            "$$\n"
            "P(A\\cap B)=P(A)+P(B)-P(A\\cup B)\n"
            "=\\dfrac{1}{3}+\\dfrac{1}{4}-\\dfrac{1}{2}=\\dfrac{1}{12}\n"
            "$$\n"
            "이므로 정답은 ④이다."
        ),
    ),
    Entry(
        exam_no=2,
        qtype="객관식",
        q="사건 $A$, $B$가 서로 독립이고 $P(A)=\\dfrac{1}{3},\\ P(A\\cap B)=\\dfrac{1}{3}$일 때, $P(B)$의 값은?",
        choices=[
            "1",
            "$\\dfrac{3}{4}$",
            "$\\dfrac{2}{3}$",
            "$\\dfrac{1}{2}$",
            "$\\dfrac{1}{2}$",
        ],
        answer="①",
        solution=(
            "서로 독립이므로\n"
            "$$\n"
            "P(A\\cap B)=P(A)P(B)\n"
            "$$\n"
            "이다. 따라서\n"
            "$$\n"
            "\\dfrac{1}{3}=\\dfrac{1}{3}P(B)\n"
            "$$\n"
            "에서 $P(B)=1$이다."
        ),
    ),
    Entry(
        exam_no=3,
        qtype="객관식",
        q="$P(A)=\\dfrac{2}{3},\\ P(B)=\\dfrac{3}{5},\\ P(A\\cup B)=\\dfrac{13}{15}$일 때, $P(A\\mid B)$는?",
        choices=[
            "$\\dfrac{6}{7}$",
            "$\\dfrac{5}{6}$",
            "$\\dfrac{4}{5}$",
            "$\\dfrac{3}{4}$",
            "$\\dfrac{2}{3}$",
        ],
        answer="⑤",
        solution=(
            "$$\n"
            "P(A\\cap B)=P(A)+P(B)-P(A\\cup B)\n"
            "=\\dfrac{2}{3}+\\dfrac{3}{5}-\\dfrac{13}{15}=\\dfrac{2}{5}\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)}\n"
            "=\\dfrac{\\frac{2}{5}}{\\frac{3}{5}}=\\dfrac{2}{3}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=4,
        qtype="객관식",
        q="한 개의 주사위를 던져 홀수의 눈이 나왔을 때, 그 수가 소수일 확률은?",
        choices=[
            "$\\dfrac{1}{3}$",
            "$\\dfrac{1}{2}$",
            "$\\dfrac{2}{3}$",
            "$\\dfrac{3}{4}$",
            "1",
        ],
        answer="③",
        solution=(
            "홀수의 눈은 $\\{1,3,5\\}$의 3가지이고, 이 중 소수는 $3,5$의 2가지이다.\n"
            "따라서 구하는 확률은\n"
            "$$\n"
            "\\dfrac{2}{3}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=5,
        qtype="객관식",
        q="앞면과 뒷면이 나올 확률이 같은 동전을 5번 던졌을 때, 앞면이 3번 나올 확률은?",
        choices=[
            "$\\dfrac{1}{8}$",
            "$\\dfrac{3}{8}$",
            "$\\dfrac{5}{16}$",
            "$\\dfrac{7}{16}$",
            "$\\dfrac{11}{32}$",
        ],
        answer="③",
        solution=(
            "앞면이 정확히 3번 나오는 경우의 수는 ${}_{5}C_{3}=10$이고,\n"
            "전체 경우의 수는 $2^{5}=32$이다.\n"
            "따라서 확률은\n"
            "$$\n"
            "\\dfrac{10}{32}=\\dfrac{5}{16}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=6,
        qtype="객관식",
        q="흰 공 2개, 검은 공 3개, 붉은 공 4개가 들어 있는 주머니에서 2개의 공을 꺼낼 때, 2개가 모두 같은 색의 공일 확률은?",
        choices=[
            "$\\dfrac{5}{36}$",
            "$\\dfrac{5}{18}$",
            "$\\dfrac{5}{12}$",
            "$\\dfrac{5}{9}$",
            "$\\dfrac{5}{6}$",
        ],
        answer="②",
        solution=(
            "전체 경우의 수는 ${}_{9}C_{2}=36$이다.\n"
            "같은 색 2개를 뽑는 경우의 수는\n"
            "$$\n"
            "{}_{2}C_{2}+{}_{3}C_{2}+{}_{4}C_{2}=1+3+6=10\n"
            "$$\n"
            "이다.\n"
            "따라서 확률은\n"
            "$$\n"
            "\\dfrac{10}{36}=\\dfrac{5}{18}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=7,
        qtype="객관식",
        q=(
            "4개의 당첨 제비를 포함하여 12개의 제비가 들어 있는 주머니가 있다. "
            "$A$, $B$ 두 사람이 차례로 한 개씩 제비를 뽑을 때, 두 사람 모두 당첨 제비를 뽑을 확률은? "
            "(단, 뽑은 제비는 주머니에 다시 넣지 않는다.)"
        ),
        choices=[
            "$\\dfrac{4}{33}$",
            "$\\dfrac{3}{44}$",
            "$\\dfrac{1}{33}$",
            "$\\dfrac{1}{11}$",
            "$\\dfrac{2}{11}$",
        ],
        answer="④",
        solution=(
            "$A$가 당첨 제비를 뽑을 확률은 $\\dfrac{4}{12}$,\n"
            "그다음 $B$가 당첨 제비를 뽑을 확률은 $\\dfrac{3}{11}$이다.\n"
            "따라서\n"
            "$$\n"
            "\\dfrac{4}{12}\\times\\dfrac{3}{11}=\\dfrac{1}{11}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=8,
        qtype="객관식",
        q=(
            "주머니 $A$에는 노란 공 2개, 빨간 공 4개가 들어 있고, 주머니 $B$에는 노란 공 4개, 빨간 공 1개가 들어 있다. "
            "두 주머니 $A$, $B$ 중에서 한 주머니를 임의로 택하여 2개의 공을 임의로 꺼냈더니 노란 공 1개, 빨간 공 1개가 나왔을 때, "
            "꺼낸 공 2개가 주머니 $B$에서 나왔을 확률은?"
        ),
        choices=[
            "$\\dfrac{1}{7}$",
            "$\\dfrac{3}{7}$",
            "$\\dfrac{5}{17}$",
            "$\\dfrac{7}{17}$",
            "$\\dfrac{9}{23}$",
        ],
        answer="②",
        solution=(
            "사건 $E$를 \"노란 공 1개, 빨간 공 1개가 나온다\"로 두면\n"
            "$$\n"
            "P(E\\mid A)=\\dfrac{{}_{2}C_{1}{}_{4}C_{1}}{{}_{6}C_{2}}=\\dfrac{8}{15},\n"
            "\\quad\n"
            "P(E\\mid B)=\\dfrac{{}_{4}C_{1}{}_{1}C_{1}}{{}_{5}C_{2}}=\\dfrac{2}{5}\n"
            "$$\n"
            "이다. 또 $P(A)=P(B)=\\dfrac{1}{2}$이므로\n"
            "$$\n"
            "P(B\\mid E)\n"
            "=\\dfrac{P(E\\mid B)P(B)}{P(E\\mid A)P(A)+P(E\\mid B)P(B)}\n"
            "=\\dfrac{\\frac{2}{5}}{\\frac{8}{15}+\\frac{2}{5}}\n"
            "=\\dfrac{3}{7}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=9,
        qtype="객관식",
        q="길이가 $a,\\ 2a,\\ 3a,\\ \\cdots,\\ 6a$인 여섯 개의 막대가 있다. 이 중에서 세 개를 사용하여 삼각형을 만들 수 있는 확률은?",
        choices=[
            "$\\dfrac{3}{20}$",
            "$\\dfrac{1}{5}$",
            "$\\dfrac{1}{4}$",
            "$\\dfrac{3}{10}$",
            "$\\dfrac{7}{20}$",
        ],
        answer="⑤",
        solution=(
            "세 막대를 고르는 전체 경우의 수는 ${}_{6}C_{3}=20$이다.\n"
            "길이를 작은 순서로 $i a, j a, k a\\ (i<j<k)$라 하면 삼각형 조건은 $i+j>k$이다.\n"
            "이를 만족하는 경우를 세면 7가지이므로\n"
            "$$\n"
            "\\text{확률}=\\dfrac{7}{20}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=10,
        qtype="객관식",
        q=(
            "빨간색 주사위와 파란색 주사위 두 개를 동시에 던질 때 "
            "빨간색 주사위에서 나온 눈의 수를 $a$, 파란색 주사위에서 나온 눈의 수를 $b$라 하자. "
            "방정식 $x^{2}-(a+b)x+ab+1=0$의 근이 존재하지 않을 확률은?"
        ),
        choices=[
            "$\\dfrac{2}{9}$",
            "$\\dfrac{1}{3}$",
            "$\\dfrac{4}{9}$",
            "$\\dfrac{5}{9}$",
            "$\\dfrac{2}{3}$",
        ],
        answer="③",
        solution=(
            "근이 존재하지 않으려면 판별식이 음수여야 한다.\n"
            "$$\n"
            "D=(a+b)^{2}-4(ab+1)=(a-b)^{2}-4<0\n"
            "$$\n"
            "즉 $|a-b|<2$이므로 $|a-b|=0$ 또는 1이다.\n"
            "경우의 수는\n"
            "$$\n"
            "|a-b|=0:\\ 6\\text{가지},\\quad |a-b|=1:\\ 10\\text{가지}\n"
            "$$\n"
            "총 16가지.\n"
            "전체 36가지이므로\n"
            "$$\n"
            "\\dfrac{16}{36}=\\dfrac{4}{9}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=11,
        qtype="객관식",
        q=(
            "표본공간 $S$의 두 사건 $A$, $B$에 대하여 $P(A)=\\dfrac{2}{3},\\ P(B)=\\dfrac{3}{4}$일 때, "
            "$P(A\\cap B)$의 최댓값을 $M$, 최솟값을 $m$이라 하자. $M+m$의 값은?"
        ),
        choices=[
            "$\\dfrac{5}{12}$",
            "$\\dfrac{7}{12}$",
            "$\\dfrac{3}{4}$",
            "$\\dfrac{11}{12}$",
            "$\\dfrac{13}{12}$",
        ],
        answer="⑤",
        solution=(
            "$$\n"
            "M=\\min\\left(\\dfrac{2}{3},\\dfrac{3}{4}\\right)=\\dfrac{2}{3}\n"
            "$$\n"
            "$$\n"
            "m=\\max\\left(0,\\dfrac{2}{3}+\\dfrac{3}{4}-1\\right)=\\dfrac{5}{12}\n"
            "$$\n"
            "따라서\n"
            "$$\n"
            "M+m=\\dfrac{2}{3}+\\dfrac{5}{12}=\\dfrac{13}{12}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=12,
        qtype="객관식",
        q=(
            "5번의 경기 중에서 3번을 먼저 이기는 선수가 최종 우승하는 경기가 있다. "
            "$A$, $B$ 두 선수가 서로 이길 확률은 $\\dfrac{1}{2}$로 같으며 첫 번째 경기는 $A$선수가 이겼을 때, "
            "$A$선수가 최종 우승할 확률은?"
        ),
        choices=[
            "$\\dfrac{11}{16}$",
            "$\\dfrac{9}{16}$",
            "$\\dfrac{1}{2}$",
            "$\\dfrac{3}{8}$",
            "$\\dfrac{5}{16}$",
        ],
        answer="①",
        solution=(
            "첫 경기를 이미 이겼으므로 이후에 $A$가 우승하는 경우를 경기 수별로 센다.\n"
            "$$\n"
            "\\text{2연승으로 즉시 우승}:\\ \\left(\\dfrac12\\right)^{2}=\\dfrac14\n"
            "$$\n"
            "$$\n"
            "\\text{4번째 경기에서 우승}:\\ 2\\left(\\dfrac12\\right)^{3}=\\dfrac14\n"
            "$$\n"
            "$$\n"
            "\\text{5번째 경기에서 우승}:\\ 3\\left(\\dfrac12\\right)^{4}=\\dfrac{3}{16}\n"
            "$$\n"
            "따라서\n"
            "$$\n"
            "\\dfrac14+\\dfrac14+\\dfrac{3}{16}=\\dfrac{11}{16}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=13,
        qtype="객관식",
        q=(
            "건영이는 게임(LOL)을 할 때 두 종류의 캐릭터 티모 또는 가렌을 각각 40%, 60%로 선택하며 "
            "티모를 선택했을 때의 승률이 20%, 가렌을 선택했을 때의 승률이 70%라고 한다. "
            "건영이가 게임을 승리하였을 때, 티모로 승리하였을 확률은?"
        ),
        choices=[
            "$\\dfrac{1}{45}$",
            "$\\dfrac{2}{45}$",
            "$\\dfrac{1}{25}$",
            "$\\dfrac{2}{25}$",
            "$\\dfrac{4}{25}$",
        ],
        answer="⑤",
        solution=(
            "사건 $T$를 \"티모 선택\", $W$를 \"승리\"라 하면\n"
            "$$\n"
            "P(T)=\\dfrac{2}{5},\\quad P(W\\mid T)=\\dfrac{1}{5},\\quad P(W\\mid T^{c})=\\dfrac{7}{10}\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "P(T\\mid W)=\\dfrac{P(W\\mid T)P(T)}{P(W\\mid T)P(T)+P(W\\mid T^{c})P(T^{c})}\n"
            "=\\dfrac{\\frac{1}{5}\\cdot\\frac{2}{5}}{\\frac{1}{5}\\cdot\\frac{2}{5}+\\frac{7}{10}\\cdot\\frac{3}{5}}\n"
            "=\\dfrac{4}{25}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=14,
        qtype="객관식",
        q=(
            "비가 온 다음날에 비가 올 확률이 $\\dfrac{1}{2}$이고, 비가 오지 않은 날의 다음날에 비가 올 확률은 $\\dfrac{1}{3}$이다. "
            "이번 주 화요일에 비가 왔을 때, 같은 주 금요일에 비가 올 확률은?"
        ),
        choices=[
            "$\\dfrac{11}{36}$",
            "$\\dfrac{13}{48}$",
            "$\\dfrac{17}{48}$",
            "$\\dfrac{23}{72}$",
            "$\\dfrac{29}{72}$",
        ],
        answer="⑤",
        solution=(
            "화요일에 비가 왔으므로 $p_{0}=1$이라 두고,\n"
            "$p_{n}$을 $n$일 뒤 비가 올 확률이라 하자.\n"
            "$$\n"
            "p_{n+1}=\\dfrac12 p_{n}+\\dfrac13(1-p_{n})=\\dfrac13+\\dfrac16 p_{n}\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "p_{1}=\\dfrac12,\\quad p_{2}=\\dfrac{5}{12},\\quad p_{3}=\\dfrac{29}{72}\n"
            "$$\n"
            "이다.\n"
            "따라서 금요일에 비가 올 확률은 $\\dfrac{29}{72}$이다."
        ),
    ),
    Entry(
        exam_no=15,
        qtype="객관식",
        q="한 개의 주사위를 두 번 던지는 시행을 한다. 5가 한 번도 나오지 않았을 때, 나온 두 수의 합이 3의 배수일 확률은?",
        choices=[
            "$\\dfrac{6}{25}$",
            "$\\dfrac{8}{25}$",
            "$\\dfrac{11}{36}$",
            "$\\dfrac{13}{36}$",
            "$\\dfrac{17}{36}$",
        ],
        answer="②",
        solution=(
            "조건에 의해 각 눈은 $\\{1,2,3,4,6\\}$ 중에서 나온다.\n"
            "따라서 표본공간의 크기는 $5\\times 5=25$.\n"
            "합이 3의 배수가 되려면 나머지쌍이 $(0,0),(1,2),(2,1)$이어야 한다.\n"
            "가능한 경우 수는\n"
            "$$\n"
            "2\\times2+2\\times1+1\\times2=8\n"
            "$$\n"
            "이므로 확률은\n"
            "$$\n"
            "\\dfrac{8}{25}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=16,
        qtype="객관식",
        q=(
            "방정식 $a+b+c+d=11$을 만족시키는 자연수 $a,b,c,d$의 모든 순서쌍 $(a,b,c,d)$ 중에서 임의로 한 개를 선택한다. "
            "선택한 순서쌍 $(a,b,c,d)$가 $(a-2)(b+c-4)=0$을 만족시킬 확률은 $\\dfrac{k}{120}$이다. $k$의 값은?"
        ),
        choices=["29", "31", "37", "43", "47"],
        answer="④",
        solution=(
            "자연수 해의 전체 개수는\n"
            "$$\n"
            "{}_{10}C_{3}=120\n"
            "$$\n"
            "이다.\n"
            "$A: a=2$, $B: b+c=4$로 두고 합집합을 센다.\n"
            "$$\n"
            "|A|:\\ b+c+d=9\\Rightarrow {}_{8}C_{2}=28\n"
            "$$\n"
            "$$\n"
            "|B|:\\ (b,c)=(1,3),(2,2),(3,1)\\ \\text{3가지},\\ a+d=7\\ \\text{6가지}\n"
            "$$\n"
            "따라서 $|B|=18$.\n"
            "$$\n"
            "|A\\cap B|=3\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "|A\\cup B|=28+18-3=43\n"
            "$$\n"
            "따라서 $k=43$이다."
        ),
    ),
    Entry(
        exam_no=17,
        qtype="객관식",
        q=(
            "좌표평면 위를 움직이는 점 $P$가 있다. 주사위를 던져서 홀수의 눈이 나오면 $x$축의 양의 방향으로 1만큼 이동하고, "
            "짝수의 눈이 나오면 $y$축의 양의 방향으로 1만큼 이동한다. 원점 $O$에서 시작하여 주사위를 8회 던졌을 때, "
            "원점 $O$에서 $P$까지의 거리가 6 이하가 될 확률은 $\\dfrac{k}{2^{7}}$이다. 자연수 $k$의 값은?"
        ),
        choices=["70", "91", "103", "112", "182"],
        answer="②",
        solution=(
            "홀수의 눈이 나온 횟수를 $o$라 하면 짝수의 횟수는 $8-o$이고,\n"
            "최종 좌표는 $(o,8-o)$이다.\n"
            "거리 조건은\n"
            "$$\n"
            "o^{2}+(8-o)^{2}\\le 36\n"
            "$$\n"
            "이므로 풀면 $o=3,4,5$.\n"
            "따라서 경우의 수는\n"
            "$$\n"
            "{}_{8}C_{3}+{}_{8}C_{4}+{}_{8}C_{5}=56+70+56=182\n"
            "$$\n"
            "이고,\n"
            "$$\n"
            "P=\\dfrac{182}{2^{8}}=\\dfrac{91}{2^{7}}\n"
            "$$\n"
            "이므로 $k=91$이다."
        ),
    ),
    Entry(
        exam_no=18,
        qtype="객관식",
        q=(
            "집합 $X=\\{1,2,3,4,5,6,7\\}$에서 $k(2\\le k\\le 6)$개의 원소를 선택할 때, "
            "이 원소가 연속하는 자연수일 확률을 $P_{k}$라 한다. "
            "다음 <보기>에서 옳은 것을 모두 고르면?\n\n"
            + box(
                [
                    "ㄱ. $P_{2}=\\dfrac{2}{7}$",
                    "ㄴ. $P_{k}=P_{8-k}$",
                    "ㄷ. $P_{k}$ 중에서 최소값은 $P_{6}$이다.",
                ]
            )
        ),
        choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        answer="①",
        solution=(
            "$k$개의 연속한 수를 고르는 경우의 수는 시작값을 정하면 되므로 $8-k$가지이다.\n"
            "전체 경우의 수는 ${}_{7}C_{k}$이므로\n"
            "$$\n"
            "P_{k}=\\dfrac{8-k}{{}_{7}C_{k}}\n"
            "$$\n"
            "이다.\n"
            "ㄱ. $P_{2}=\\dfrac{6}{{}_{7}C_{2}}=\\dfrac{6}{21}=\\dfrac{2}{7}$ (참)\n"
            "ㄴ. 일반적으로 $\\dfrac{8-k}{{}_{7}C_{k}}\\ne\\dfrac{k}{{}_{7}C_{8-k}}$ (거짓)\n"
            "ㄷ. $P_{2}=\\dfrac{2}{7},\\ P_{3}=\\dfrac{1}{7},\\ P_{4}=\\dfrac{4}{35},\\ P_{5}=\\dfrac{1}{7},\\ P_{6}=\\dfrac{2}{7}$이므로 "
            "최소는 $P_{4}$ (거짓)\n"
            "따라서 옳은 것은 ㄱ만이다."
        ),
    ),
    Entry(
        exam_no=101,
        qtype="서답형(단답형)",
        q=(
            "두 집합 $X=\\{1,2,3,4\\},\\ Y=\\{1,2,3,4,5,6,7\\}$에 대하여 함수 $f:X\\to Y$가 "
            "$f(1)=1$이거나 $f(2)=2$일 확률이 $\\dfrac{q}{p}$일 때, $p+q$의 값을 구하여라. "
            "(단, $p,q$는 서로소인 자연수이다.)"
        ),
        choices=[],
        answer="62",
        solution=(
            "전체 함수의 개수는\n"
            "$$\n"
            "7^{4}\n"
            "$$\n"
            "이다.\n"
            "$A: f(1)=1$, $B: f(2)=2$로 두면\n"
            "$$\n"
            "|A|=7^{3},\\quad |B|=7^{3},\\quad |A\\cap B|=7^{2}\n"
            "$$\n"
            "이므로\n"
            "$$\n"
            "P(A\\cup B)=\\dfrac{7^{3}+7^{3}-7^{2}}{7^{4}}=\\dfrac{13}{49}\n"
            "$$\n"
            "따라서 $(p,q)=(49,13)$이고\n"
            "$$\n"
            "p+q=62\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=102,
        qtype="서답형(단답형)",
        q=(
            "두 직선 $y=x$와 $y=-x$ 위에 $x$좌표가 6 이하인 자연수인 점 3개를 선택하여 "
            "삼각형이 만들어질 때, 삼각형의 넓이가 6일 확률을 구하여라."
        ),
        choices=[],
        answer="$\\dfrac{2}{15}$",
        solution=(
            "점은 각 직선 위에 6개씩, 총 12개이다.\n"
            "삼각형이 만들어지는 경우의 수는 같은 직선 위 3점을 제외하므로\n"
            "$$\n"
            "{}_{12}C_{3}-{}_{6}C_{3}-{}_{6}C_{3}=220-20-20=180\n"
            "$$\n"
            "이다.\n"
            "한 직선에서 2점을 고르고 다른 직선에서 1점을 고르면 넓이는\n"
            "$$\n"
            "(\\text{인덱스 차})\\times(\\text{다른 직선 점의 인덱스})\n"
            "$$\n"
            "가 된다.\n"
            "넓이가 6이 되려면 가능한 차-인덱스 쌍은 $(1,6),(2,3),(3,2)$이고,\n"
            "각각의 경우 수는 $5,4,3$가지이므로 한 방향에서 12가지,\n"
            "두 방향 합쳐 24가지이다.\n"
            "따라서 확률은\n"
            "$$\n"
            "\\dfrac{24}{180}=\\dfrac{2}{15}\n"
            "$$\n"
            "이다."
        ),
        uncertain=True,
    ),
    Entry(
        exam_no=103,
        qtype="서답형(서술형)",
        q=(
            "상자에 동그라미, 세모, 네모 모양의 블록이 각각 3개, 4개, 6개 들어있다. "
            "이 상자에서 동시에 3개의 블록을 꺼낼 때, 두 가지 이상의 모양이 나올 확률을 구하여라.\n\n"
            "(1) 상자에서 동시에 3개의 블록을 꺼낼 때 모두 동그라미 모양의 블록이 나올 확률을 구하여라.\n\n"
            "(2) 상자에서 동시에 3개의 블록을 꺼낼 때 모두 세모 모양의 블록이 나올 확률을 구하여라.\n\n"
            "(3) 상자에서 동시에 3개의 블록을 꺼낼 때 모두 네모 모양의 블록이 나올 확률을 구하여라.\n\n"
            "(4) 상자에서 동시에 3개의 블록을 꺼낼 때, 두 가지 이상의 모양이 나올 확률을 구하여라."
        ),
        choices=[],
        answer="(1) $\\dfrac{1}{286}$, (2) $\\dfrac{2}{143}$, (3) $\\dfrac{10}{143}$, (4) $\\dfrac{261}{286}$",
        solution=(
            "전체 경우의 수는\n"
            "$$\n"
            "{}_{13}C_{3}=286\n"
            "$$\n"
            "이다.\n"
            "따라서\n"
            "$$\n"
            "(1)\\ \\dfrac{{}_{3}C_{3}}{{}_{13}C_{3}}=\\dfrac{1}{286}\n"
            "$$\n"
            "$$\n"
            "(2)\\ \\dfrac{{}_{4}C_{3}}{{}_{13}C_{3}}=\\dfrac{4}{286}=\\dfrac{2}{143}\n"
            "$$\n"
            "$$\n"
            "(3)\\ \\dfrac{{}_{6}C_{3}}{{}_{13}C_{3}}=\\dfrac{20}{286}=\\dfrac{10}{143}\n"
            "$$\n"
            "이고,\n"
            "$$\n"
            "(4)=1-\\left(\\dfrac{1}{286}+\\dfrac{2}{143}+\\dfrac{10}{143}\\right)\n"
            "=1-\\dfrac{25}{286}=\\dfrac{261}{286}\n"
            "$$\n"
            "이다."
        ),
    ),
    Entry(
        exam_no=104,
        qtype="서답형(서술형)",
        q=(
            "태은이와 민규는 체중감량을 위해 다음과 같은 규칙으로 가위바위보를 하여 계단을 오르는 게임을 한다.\n\n"
            + box(
                [
                    "이긴 사람은 위로 두 계단 올라간다.",
                    "진 사람은 아래로 한 계단 내려간다.",
                    "비기면 두 사람 모두 위로 한 계단 올라간다.",
                ]
            )
            + "\n\n가위바위보를 5번 한 후, 태은이가 처음 위치보다 세 계단 올라갔을 때, "
            "태은이가 가위바위보를 한 번도 이기지 못했을 확률을 구하여라.\n\n"
            "(1) 태은이가 세 계단을 올라가는 사건을 $A$, 태은이가 가위바위보를 한 번도 이기지 못하는 사건을 $B$라 할 때, "
            "문제에서 구하고자 하는 확률을 조건부확률을 이용하여 나타내어라.\n\n"
            "(2) 가위바위보를 5번 한 후 태은이가 세 계단을 올라가는 경우를 각각 구하고, $P(A)$를 구하여라.\n\n"
            "(3) $P(A\\cap B)$를 구하여라.\n\n"
            "(4) $P(B\\mid A)$를 구하여라."
        ),
        choices=[],
        answer="$\\dfrac{1}{7}$",
        solution=(
            "태은이 기준으로 1회 결과를 다음과 같이 둔다.\n"
            "이김 $W$ : $+2$, 짐 $L$ : $-1$, 비김 $D$ : $+1$.\n"
            "각 결과의 확률은 모두 $\\dfrac{1}{3}$이다.\n\n"
            "(1) 구하려는 값은\n"
            "$$\n"
            "P(B\\mid A)=\\dfrac{P(A\\cap B)}{P(A)}\n"
            "$$\n"
            "이다.\n\n"
            "(2) 5회 후 상승량이 3이 되려면\n"
            "$$\n"
            "2w-l+d=3,\\quad w+l+d=5\n"
            "$$\n"
            "을 만족해야 한다.\n"
            "해는 $(w,d,l)=(0,4,1),(2,1,2)$뿐이다.\n"
            "따라서 경우의 수는\n"
            "$$\n"
            "{}_{5}C_{1}+\\dfrac{5!}{2!1!2!}=5+30=35\n"
            "$$\n"
            "이고\n"
            "$$\n"
            "P(A)=\\dfrac{35}{3^{5}}=\\dfrac{35}{243}\n"
            "$$\n"
            "이다.\n\n"
            "(3) $A\\cap B$는 \"세 계단 상승\"이면서 \"한 번도 이기지 못함\"이므로 $(w,d,l)=(0,4,1)$뿐이다.\n"
            "따라서\n"
            "$$\n"
            "P(A\\cap B)=\\dfrac{{}_{5}C_{1}}{3^{5}}=\\dfrac{5}{243}\n"
            "$$\n"
            "이다.\n\n"
            "(4) 따라서\n"
            "$$\n"
            "P(B\\mid A)=\\dfrac{\\frac{5}{243}}{\\frac{35}{243}}=\\dfrac{1}{7}\n"
            "$$\n"
            "이다."
        ),
        uncertain=True,
    ),
]


def parse_pdf_meta(pdf_name: str) -> dict:
    parts = pdf_name.split(".")
    if len(parts) != 7 or parts[-1].lower() != "pdf":
        raise ValueError(f"unexpected pdf filename format: {pdf_name}")
    school, year, gtoken, stoken, exam, subject, _ = parts
    if not gtoken.upper().startswith("G") or not stoken.upper().startswith("S"):
        raise ValueError(f"unexpected grade/semester token in filename: {pdf_name}")
    return {
        "school": school.upper(),
        "year": int(year),
        "grade": int(gtoken[1:]),
        "semester": int(stoken[1:]),
        "exam": exam.upper(),
        "subject": subject.upper(),
    }


def id_info(exam_no: int) -> Tuple[int, int, str, str]:
    if exam_no < 100:
        source_no = exam_no
        pid_no = exam_no
        source_kind = "objective"
        source_label = str(source_no)
    else:
        source_no = exam_no - 100
        pid_no = exam_no
        source_kind = "subjective"
        source_label = f"서답{source_no}번"
    return pid_no, source_no, source_kind, source_label


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "")


def render_rotated_pages(doc: fitz.Document) -> Dict[int, Image.Image]:
    pages: Dict[int, Image.Image] = {}
    for idx, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        mode = "RGB" if pix.n < 4 else "RGBA"
        image = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
        if mode == "RGBA":
            image = image.convert("RGB")
        pages[idx] = image.rotate(-90, expand=True)
    return pages


def export_crop(
    rotated_pages: Dict[int, Image.Image],
    page_no: int,
    rect_vals: Tuple[int, int, int, int],
    out_path: Path,
) -> None:
    image = rotated_pages[page_no]
    crop = image.crop(rect_vals)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    crop.save(out_path)


def fallback_unit_for_entry(exam_no: int) -> Tuple[str, str]:
    conditional_set = {2, 3, 8, 11, 12, 13, 15, 104}
    if exam_no == 101:
        return ("1. 경우의 수", "1-2. 조합")
    if exam_no in conditional_set:
        return ("2. 확률", "2-2. 조건부 확률")
    return ("2. 확률", "2-1. 확률의 뜻과 활용")


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
) -> str:
    subject_ko = {
        "COM1": "공통수학1",
        "COM2": "공통수학2",
        "ALG": "대수",
        "CAL1": "미적분1",
        "STAT": "확률과통계",
    }.get(meta["subject"], meta["subject"])

    assets = [
        "assets/original/",
        f"assets/original/{original_asset_name}",
    ]

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


def process_range(start_idx: int, end_idx: int, rewrite_existing: bool = False) -> None:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"source PDF not found: {SOURCE_PDF}")

    meta = parse_pdf_meta(SOURCE_PDF.name)
    prefix = f"{meta['school']}-{meta['year']}-G{meta['grade']}-S{meta['semester']}-{meta['exam']}-{meta['subject']}"

    doc = fitz.open(SOURCE_PDF)
    rotated_pages = render_rotated_pages(doc)

    created: List[str] = []
    updated: List[str] = []
    skipped_duplicates: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []
    results: List[Tuple[str, str, str]] = []
    review_paths: List[str] = []

    if start_idx < 1 or end_idx > len(ENTRIES) or start_idx > end_idx:
        raise ValueError(f"invalid range: expected 1 <= start <= end <= {len(ENTRIES)}")
    target_entries = ENTRIES[start_idx - 1 : end_idx]

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
        original_asset_name = f"{SOURCE_PDF.stem}.q{pid_no:03d}.png"
        export_crop(rotated_pages, page_no, rect_vals, assets_original / original_asset_name)

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

        level = cls.level
        unit_l1 = cls.unit_l1
        unit_l2 = cls.unit_l2
        unit_l3 = cls.unit_l3

        if cls.unit_l1 != "확률과 통계(2022개정)":
            fallback_l2, fallback_l3 = fallback_unit_for_entry(entry.exam_no)
            unit_l1 = "확률과 통계(2022개정)"
            unit_l2 = fallback_l2
            unit_l3 = fallback_l3
            warnings.append(
                f"{pid}: classifier unit outside STAT -> {cls.unit_l1}>{cls.unit_l2}>{cls.unit_l3} ({cls.reason}); "
                f"fallback={unit_l2}>{unit_l3}"
            )

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
        )
        md_path.write_text(content, encoding="utf-8", newline="\n")

        if existed:
            updated.append(pid)
            results.append((pid, "UPDATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={level}"))
        else:
            created.append(pid)
            results.append((pid, "CREATED", f"exam_no={entry.exam_no}, unit={unit_l3}, level={level}"))

        if entry.uncertain:
            uncertain.append(f"{pid}: OCR/해석 확인 필요")

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
    parser = argparse.ArgumentParser(description="Manual ingest for BY 2021 G2 S1 FINAL2 STAT")
    parser.add_argument("--start-idx", type=int, default=1, help=f"start entry index (1~{len(ENTRIES)})")
    parser.add_argument("--end-idx", type=int, default=len(ENTRIES), help=f"end entry index (1~{len(ENTRIES)})")
    parser.add_argument(
        "--rewrite-existing",
        action="store_true",
        help="rewrite existing target folders instead of skipping duplicates",
    )
    args = parser.parse_args()

    process_range(args.start_idx, args.end_idx, rewrite_existing=args.rewrite_existing)
