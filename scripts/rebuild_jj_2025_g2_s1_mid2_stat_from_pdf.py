from __future__ import annotations

from pathlib import Path
import shutil
from textwrap import dedent

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"
PDF_SRC = ROOT / "db" / "original" / "JJ.2025.G2.S1.MID2.STAT.pdf"

PREFIX = "JJ-2025-G2-S1-MID2-STAT"
UNIT_L1 = "확률과 통계(2022개정)"
UNIT_L2 = "1. 경우의 수"
SOURCE = "user_upload_2026-03-06"


def box(lines: list[str]) -> str:
    body = "<br/>".join(lines)
    return (
        '<div style="border:1px solid #000; padding:8px; margin:8px 0;">'
        f"{body}"
        "</div>"
    )


QUESTIONS = [
    {
        "num": 1,
        "level": 2,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "2명의 주연 배우를 포함하여 한 영화에 출연한 5명의 배우가 시상식에 참석해 원탁에 둘러앉았을 때, 2명의 주연 배우가 이웃하게 앉는 경우의 수는?",
        "choices": ["6", "9", "12", "15", "18"],
        "answer": "③",
        "solution": dedent(
            """
            주연 배우 2명을 한 덩어리로 보면 원탁에 앉는 대상은 4개이다.
            따라서 경우의 수는
            $$
            (4-1)!\\times 2 = 3!\\times 2 = 12
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 2,
        "level": 2,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "0, 1, 2, 3, 4에서 중복을 허용하여 5개를 뽑아 다섯 자리 자연수를 만들 때, 홀수의 개수는?",
        "choices": ["500", "1000", "1500", "2000", "2500"],
        "answer": "②",
        "solution": dedent(
            """
            천의 자리는 0이 될 수 없으므로 4가지이고,
            일의 자리는 홀수이므로 2가지이다.
            가운데 세 자리는 각각 5가지씩 가능하다.
            $$
            4\\times 5^3\\times 2 = 1000
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 3,
        "level": 3,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "0, 1, 2, 3에서 중복을 허락하여 4개의 수를 뽑아 네 자리 자연수를 만들 때, 4의 배수의 개수는?",
        "choices": ["24", "30", "36", "42", "48"],
        "answer": "⑤",
        "solution": dedent(
            """
            4의 배수 판정은 끝의 두 자리로 한다.
            사용할 수 있는 끝의 두 자리(00~33 중 4의 배수)는
            $$
            00,\\ 12,\\ 20,\\ 32
            $$
            의 4가지이다.

            천의 자리는 1,2,3 중 하나이므로 3가지,
            백의 자리는 0,1,2,3 중 하나이므로 4가지이다.
            따라서 전체 개수는
            $$
            3\\times 4\\times 4 = 48
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 4,
        "level": 3,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": dedent(
            """
            아래 그림과 같은 도로망에서 A 지점에서 C 지점을 거치지 않고 B 지점까지 최단 거리로 가는 경우의 수는?

            <img src="assets/scan.png" alt="도로망 그림" style="width:60% !important; max-width:60% !important; height:auto;" />
            """
        ).strip(),
        "choices": ["60", "66", "72", "78", "84"],
        "answer": "②",
        "solution": dedent(
            """
            그림에서 A에서 B까지 최단 거리로 가려면
            오른쪽으로 5번, 위로 4번 이동하므로 전체 경우의 수는
            $$
            {}_{9}C_{4}=126
            $$
            이다.

            C를 거치는 최단 경로 수를 구하면,
            A에서 C까지는 오른쪽 3번, 위로 2번이므로
            $$
            {}_{5}C_{2}=10
            $$
            C에서 B까지는 오른쪽 2번, 위로 2번이므로
            $$
            {}_{4}C_{2}=6
            $$
            이다.

            따라서 C를 거치지 않는 경우의 수는
            $$
            126-10\\times 6=66
            $$
            이다.
            """
        ).strip(),
        "has_scan": True,
    },
    {
        "num": 5,
        "level": 3,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": (
            "전체집합 $U=\\{1,2,3,4,5,6\\}$의 두 부분집합 $A, B$에 대하여 다음 조건을 만족하는 "
            "$A, B$의 순서쌍 $(A, B)$의 개수는?\n\n"
            + box(
                [
                    "(가) $A\\cup B=U$",
                    "(나) $A\\cap B=\\varnothing$",
                    "(다) $A\\ne\\varnothing,\\ B\\ne\\varnothing$",
                ]
            )
        ),
        "choices": ["56", "58", "60", "62", "64"],
        "answer": "④",
        "solution": dedent(
            """
            각 원소를 A에 넣거나 B에 넣는 두 가지 선택을 하므로
            기본 경우의 수는 $2^6$이다.
            이때 $A=\\varnothing$ 또는 $B=\\varnothing$인 경우 2가지를 빼면
            $$
            2^6-2=62
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 6,
        "level": 3,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "0, 1, 2, 3, 4, 5에서 중복을 허락하여 4개를 뽑아 네 자리 자연수를 만들 때, 천의 자리의 숫자와 일의 자리의 숫자의 합이 5의 배수인 자연수의 개수는?",
        "choices": ["216", "224", "232", "240", "248"],
        "answer": "①",
        "solution": dedent(
            """
            천의 자리를 $a$, 일의 자리를 $d$라 하면
            $a\\in\\{1,2,3,4,5\\}$, $d\\in\\{0,1,2,3,4,5\\}$이고
            $a+d$가 5의 배수여야 한다.

            가능한 $(a,d)$는
            $$
            (1,4),(2,3),(3,2),(4,1),(5,0),(5,5)
            $$
            의 6가지이다.
            가운데 두 자리는 각각 6가지이므로
            $$
            6\\times 6\\times 6=216
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 7,
        "level": 3,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "네 문자 $a,b,c,d$ 중에서 중복을 허락하여 5개를 택해 일렬로 나열할 때, 문자 $a$가 세 번만 나오는 경우의 수는?",
        "choices": ["75", "80", "85", "90", "95"],
        "answer": "④",
        "solution": dedent(
            """
            5자리 중 $a$가 놓일 위치 3자리를 고르는 방법은
            $$
            {}_{5}C_{3}=10
            $$
            이다.
            나머지 2자리는 $b,c,d$ 중 하나이므로
            $$
            3^2=9
            $$
            가지.
            따라서 경우의 수는
            $$
            10\\times 9=90
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 8,
        "level": 2,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": "방정식 $x+y+z=9$를 만족하는 $x,y,z$가 모두 양의 정수인 해의 개수는?",
        "choices": ["20", "24", "28", "32", "36"],
        "answer": "③",
        "solution": dedent(
            """
            $x'=x-1,\\ y'=y-1,\\ z'=z-1$로 두면
            $x',y',z'\\ge 0$이고
            $$
            x'+y'+z'=6
            $$
            이다.
            음이 아닌 정수해의 개수는
            $$
            {}_{8}C_{2}=28
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 9,
        "level": 2,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": "$(x^2-2x)^4$의 전개식에서 $x^6$의 계수는?",
        "choices": ["-36", "-24", "-12", "12", "24"],
        "answer": "⑤",
        "solution": dedent(
            """
            일반항은
            $$
            {}_{4}C_{k}(x^2)^{4-k}(-2x)^k
            ={}_{4}C_{k}(-2)^k x^{8-k}
            $$
            이다.
            $x^6$항이 되려면 $8-k=6$이므로 $k=2$.
            따라서 계수는
            $$
            {}_{4}C_{2}(-2)^2=6\\times 4=24
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 10,
        "level": 4,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": "집합 $X=\\{1,2,3,4,5\\}$에 대하여 $X$에서 $X$로의 함수 중에서 임의로 하나를 선택할 때, $f(1)+f(2)+f(3)=6$을 만족시키고 집합 $\\{y\\mid y=f(x),\\ x\\in X\\}$의 원소의 개수가 2개인 함수 $f$의 개수는?",
        "choices": ["16", "18", "20", "22", "24"],
        "answer": "⑤",
        "solution": dedent(
            """
            $(f(1),f(2),f(3))=(a,b,c)$라 하자.
            $a+b+c=6$이고 각 값은 1부터 5까지이다.

            가능한 순서쌍 형태는
            $$
            (2,2,2),\\quad (1,1,4)\\text{의 순열},\\quad (1,2,3)\\text{의 순열}
            $$
            이다.

            1. $(2,2,2)$인 경우  
            첫 세 값의 상은 $\\{2\\}$이다. 전체 상의 개수가 2가 되려면
            $f(4),f(5)$는 $2$와 어떤 값 $t(\\ne 2)$만 사용해야 하고,
            둘 다 2인 경우는 제외한다.
            $t$ 선택 4가지, 각 $t$마다 $(f(4),f(5))$는 3가지이므로 12가지.

            2. $(1,1,4)$의 순열인 경우  
            순열은 3가지.
            이미 상이 $\\{1,4\\}$이므로 $f(4),f(5)$는 각각 1 또는 4여야 한다.
            각 순열마다 $2^2=4$가지이므로 12가지.

            3. $(1,2,3)$의 순열인 경우  
            이미 상의 개수가 3이므로 불가능.

            따라서 전체 개수는
            $$
            12+12=24
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 11,
        "level": 3,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": (
            "집합 $X=\\{1,2,3\\},\\ Y=\\{0,1,2,3,4\\}$가 있다. $X$에서 $Y$로의 함수 중 다음 조건을 만족하는 함수 $f$의 개수는?\n\n"
            + box(["집합 $X$의 어떤 두 원소 $a,b(a<b)$에 대하여 $f(a)<f(b)$이다."])
        ),
        "choices": ["60", "70", "80", "90", "100"],
        "answer": "④",
        "solution": dedent(
            """
            전체 함수의 개수는
            $$
            5^3=125
            $$
            이다.

            조건을 만족하지 않는 경우는
            $f(1)\\ge f(2)\\ge f(3)$인 경우와 같다.
            이는 0,1,2,3,4 중에서 중복을 허용해 3개를 뽑아 내림차순으로 놓는 것과 같으므로
            $$
            {}_{7}C_{3}=35
            $$
            가지.

            따라서 조건을 만족하는 함수의 개수는
            $$
            125-35=90
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 12,
        "level": 2,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": "$ {}_{10}C_{0}+{}_{10}C_{1}\\times 3+{}_{10}C_{2}\\times 3^{2}+\\cdots+{}_{10}C_{10}\\times 3^{10}=p$일 때, $\\log_{2}p$의 값은?",
        "choices": ["18", "20", "22", "24", "26"],
        "answer": "②",
        "solution": dedent(
            """
            이항정리에 의해
            $$
            p=(1+3)^{10}=4^{10}=2^{20}
            $$
            이므로
            $$
            \\log_{2}p=\\log_{2}(2^{20})=20
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 13,
        "level": 3,
        "unit_l3": "1-1. 순열",
        "qtype": "객관식",
        "q": "자연수 $n$을 순서를 고려하여 2 이하의 자연수의 합으로 나타내는 경우의 수를 $N(n)$이라고 하자. 예를 들어 $4=1+1+1+1=1+1+2=1+2+1=2+1+1=2+2$이므로 $N(4)=5$이다. 이때 $N(8)$의 값은?",
        "choices": ["34", "36", "38", "40", "42"],
        "answer": "①",
        "solution": dedent(
            """
            마지막 항이 1인 경우와 2인 경우로 나누면
            $$
            N(n)=N(n-1)+N(n-2)
            $$
            이다.
            또한
            $$
            N(1)=1,\\ N(2)=2
            $$
            이므로
            $$
            N(3)=3,\\ N(4)=5,\\ N(5)=8,\\ N(6)=13,\\ N(7)=21,\\ N(8)=34
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 14,
        "level": 4,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": (
            "네 명의 학생 $A,B,C,D$에게 같은 종류의 사과 5개와 같은 종류의 배 2개를 다음 조건을 만족하도록 남김없이 나누어 주는 방법의 수는?\n\n"
            + box(["모든 학생이 사과 또는 배를 1개 이상씩 받도록 한다."])
        ),
        "choices": ["120", "130", "140", "150", "160"],
        "answer": "⑤",
        "solution": dedent(
            """
            조건 없이 나누는 방법은
            $$
            {}_{8}C_{3}\\times {}_{5}C_{3}=56\\times 10=560
            $$
            이다.

            이제 포함배제를 쓴다.

            한 학생이 아무것도 받지 않는 경우(예: A)는
            $$
            {}_{7}C_{2}\\times {}_{4}C_{2}=21\\times 6=126
            $$
            이고 학생 선택 4가지이므로 $4\\times 126=504$.

            두 학생이 아무것도 받지 않는 경우는
            $$
            {}_{6}C_{1}\\times {}_{3}C_{1}=6\\times 3=18
            $$
            이고 학생쌍 선택 6가지이므로 $6\\times 18=108$.

            세 학생이 아무것도 받지 않는 경우는 4가지.

            따라서
            $$
            560-504+108-4=160
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 15,
        "level": 3,
        "unit_l3": "1-2. 조합",
        "qtype": "객관식",
        "q": (
            "다음 식의 값을 만족하는 모든 자연수 $r$의 값의 합은?\n\n"
            + box(["$ {}_{2}C_{0}+{}_{3}C_{1}+{}_{4}C_{2}+\\cdots+{}_{10}C_{8}={}_{11}C_{r}$"])
        ),
        "choices": ["9", "10", "11", "12", "13"],
        "answer": "③",
        "solution": dedent(
            """
            왼쪽은
            $$
            \\sum_{k=0}^{8} {}_{k+2}C_{k}
            =\\sum_{i=2}^{10} {}_{i}C_{2}
            $$
            이고 항등식
            $$
            \\sum_{i=2}^{10} {}_{i}C_{2} = {}_{11}C_{3}
            $$
            을 이용하면
            $$
            {}_{11}C_{r}={}_{11}C_{3}
            $$
            이다.
            따라서
            $$
            r=3,\\ 8
            $$
            이고 구하는 합은
            $$
            3+8=11
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 101,
        "level": 4,
        "unit_l3": "1-1. 순열",
        "qtype": "서답형(단답형)",
        "q": (
            "네 명의 남학생 $A,B,C,D$와 네 명의 여학생 $E,F,G,H$가 있다. "
            "이 8명의 학생이 일정한 간격을 두고 원 모양의 탁자에 다음 조건을 만족하도록 모두 둘러앉는 경우의 수는?\n\n"
            + box(
                [
                    "(가) $A$와 $B$는 서로 이웃한다.",
                    "(나) $E$는 여학생과 이웃하지 않는다.",
                ]
            )
        ),
        "choices": None,
        "answer": "288",
        "solution": dedent(
            """
            원순열이므로 $E$의 자리를 고정한다.
            그러면 $E$의 양옆 두 자리는 남학생이어야 한다.

            1. $E$의 양옆이 $C,D$인 경우(순서 고려 2가지)  
            남은 5자리(일렬)에는 $A,B,F,G,H$를 배치한다.
            이때 $A,B$가 이웃해야 하므로
            $$
            2\\times 4!=48
            $$
            가지.
            따라서
            $$
            2\\times 48=96
            $$
            가지.

            2. $E$의 양옆에 $A$ 또는 $B$가 정확히 하나 있는 경우  
            (양옆이 $A,B$인 경우는 $A,B$가 서로 이웃하지 않으므로 제외)
            경우의 수는
            $$
            2\\ (\uC120\uD0DD: A \uB610\uB294 B)\\times
            2\\ (\uC704\uCE58: \uC67C\uCABD/\uC624\uB978\uCABD)\\times
            2\\ (\uB2E4\uB978 \uC606\uC790\uB9AC: C \uB610\uB294 D)
            =8
            $$
            가지.
            남은 한 명($A$ 또는 $B$)의 자리는 이웃 조건 때문에 자동으로 정해지고,
            나머지 4명은 자유롭게 배치되므로 $4!=24$가지.
            따라서
            $$
            8\\times 24=192
            $$
            가지.

            전체 경우의 수는
            $$
            96+192=288
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 102,
        "level": 4,
        "unit_l3": "1-1. 순열",
        "qtype": "서답형(단답형)",
        "q": "1에서 10까지의 자연수가 하나씩 적힌 10장의 카드 중에서 한 장의 카드를 뽑아서 숫자를 확인하는 시행을 세 번 반복한다. 세 번 반복한 결과 얻은 세 수를 차례대로 $x,y,z$라고 할 때, 세 수 $x,y,z$의 합이 3으로 나누어 떨어지는 경우의 수를 구하여라.",
        "choices": None,
        "answer": "334",
        "solution": dedent(
            """
            1부터 10까지를 3으로 나눈 나머지별 개수는
            $$
            0\\text{인 수 }3\\text{개},\\quad
            1\\text{인 수 }4\\text{개},\\quad
            2\\text{인 수 }3\\text{개}
            $$
            이다.

            합이 3의 배수가 되는 나머지 조합은
            $$
            (0,0,0),\\ (1,1,1),\\ (2,2,2),\\ (0,1,2)\uC758 \uC21C\uC5F4
            $$
            이다.

            따라서 경우의 수는
            $$
            3^3 + 4^3 + 3^3 + 6\\times 3\\times 4\\times 3
            =27+64+27+216=334
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 103,
        "level": 3,
        "unit_l3": "1-2. 조합",
        "qtype": "서답형(단답형)",
        "q": "자연수 $n$에 대하여 $\\left(x^{n}+\\dfrac{2}{x}\\right)^{n}$의 전개식에서 $\\dfrac{1}{x^{n}}$의 계수를 $f(n)$이라 하자. 방정식 $\\log_{\\sqrt{2}} f(n)=20$을 만족하는 자연수 $n$의 값을 구하여라.",
        "choices": None,
        "answer": "10",
        "solution": dedent(
            """
            전개식의 일반항은
            $$
            {}_{n}C_{k}(x^n)^{n-k}\\left(\\frac{2}{x}\\right)^k
            ={}_{n}C_{k}2^k x^{n^2-(n+1)k}
            $$
            이다.
            $\\dfrac{1}{x^n}$항이 되려면
            $$
            n^2-(n+1)k=-n
            $$
            이어야 하므로 $k=n$.
            따라서
            $$
            f(n)=2^n
            $$
            이다.

            주어진 식은
            $$
            \\log_{\\sqrt{2}}(2^n)=20
            $$
            이고 $\\sqrt{2}=2^{1/2}$이므로
            $$
            2n=20
            $$
            따라서
            $$
            n=10
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 104,
        "level": 3,
        "unit_l3": "1-2. 조합",
        "qtype": "서답형(서술형)",
        "q": (
            "다음 조건을 만족시키는 두 자연수 $a,b$의 순서쌍 $(a,b)$의 개수는?\n\n"
            + box(
                [
                    "(가) 두 수 $a,b$의 곱은 짝수이다.",
                    "(나) $5\\le a\\le b\\le 15$",
                ]
            )
        ),
        "choices": None,
        "answer": "45",
        "solution": dedent(
            """
            $5\\le a\\le b\\le 15$를 만족하는 $(a,b)$의 전체 개수는
            11개에서 중복조합 2개를 뽑는 것과 같으므로
            $$
            {}_{12}C_{2}=66
            $$
            이다.

            곱이 짝수가 아니려면 $a,b$가 모두 홀수여야 한다.
            5부터 15까지의 홀수는
            $$
            5,7,9,11,13,15
            $$
            로 6개.
            따라서 $a\\le b$인 홀수쌍의 개수는
            $$
            {}_{7}C_{2}=21
            $$
            이다.

            구하는 개수는
            $$
            66-21=45
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 105,
        "level": 5,
        "unit_l3": "1-2. 조합",
        "qtype": "서답형(서술형)",
        "q": (
            "흰공 4개, 검은공 5개와 서로 다른 네 상자가 있다. 이 9개의 공을 4개의 상자에 다음 조건을 만족하도록 남김없이 나누어 넣는 경우의 수를 구하여라. "
            "(단, 같은 색의 공끼리는 서로 구별하지 않는다.)\n\n"
            + box(
                [
                    "(가) 흰 공만 들어있는 상자의 수는 2이다.",
                    "(나) 검은 공만 들어있는 상자의 수는 1이다.",
                    "(다) 모든 상자에는 적어도 하나의 공이 들어 있다.",
                ]
            )
        ),
        "choices": None,
        "answer": "144",
        "solution": dedent(
            """
            조건 (가), (나), (다)에 의해 4개의 상자 유형은
            $$
            \\text{흰공 전용 2개, 검은공 전용 1개, 섞인 상자 1개}
            $$
            로 정해진다.

            먼저 상자 유형 배정:
            섞인 상자를 고르는 방법 4가지,
            남은 3개 중 검은공 전용 상자를 고르는 방법 3가지.
            따라서
            $$
            4\\times 3=12
            $$
            가지.

            흰공 4개는 (흰공 전용 2상자 + 섞인 상자)로, 모두 1개 이상이므로
            $$
            w_1+w_2+w_3=4\\ (w_i\\ge 1)
            $$
            의 해의 수는
            $$
            {}_{3}C_{2}=3
            $$
            가지.

            검은공 5개는 (검은공 전용 1상자 + 섞인 상자)로, 모두 1개 이상이므로
            $$
            b_1+b_2=5\\ (b_i\\ge 1)
            $$
            의 해의 수는
            $$
            {}_{4}C_{1}=4
            $$
            가지.

            따라서 전체 경우의 수는
            $$
            12\\times 3\\times 4=144
            $$
            이다.
            """
        ).strip(),
    },
    {
        "num": 106,
        "level": 2,
        "unit_l3": "1-1. 순열",
        "qtype": "서답형(서술형)",
        "q": "1, 2, 3에서 중복을 허락하여 3개를 뽑아 만들 수 있는 모든 세 자리 자연수의 합을 구하시오.",
        "choices": None,
        "answer": "5994",
        "solution": dedent(
            """
            세 자리 수의 개수는
            $$
            3^3=27
            $$
            이다.

            각 자리(백의 자리, 십의 자리, 일의 자리)에
            1,2,3은 각각 $3^2=9$번씩 나온다.
            따라서 각 자리에서의 숫자합 기여는
            $$
            (1+2+3)\\times 9 = 54
            $$
            이다.

            전체 합은
            $$
            54\\times 100 + 54\\times 10 + 54
            =5400+540+54=5994
            $$
            이다.
            """
        ).strip(),
    },
]


def build_markdown(item: dict) -> str:
    qnum = item["num"]
    qid = f"{PREFIX}-{qnum:03d}"
    source_no = qnum if qnum < 100 else qnum - 100
    kind = "objective" if qnum < 100 else "subjective"
    label = str(source_no) if qnum < 100 else f"서답{source_no}번"

    assets = [
        "assets/original/",
        f"assets/original/{PDF_SRC.name}",
    ]
    if item.get("has_scan"):
        assets.append("assets/scan.png")

    lines: list[str] = [
        "---",
        f"id: {qid}",
        "school: JJ",
        "year: 2025",
        "grade: 2",
        "semester: 1",
        "exam: MID2",
        "subject: STAT",
        f"type: {item['qtype']}",
        f"source_question_no: {source_no}",
        f"source_question_kind: {kind}",
        f"source_question_label: '{label}'",
        f"difficulty: {item['level']}",
        f"level: {item['level']}",
        f"unit: {UNIT_L1}>{UNIT_L2}>{item['unit_l3']}",
        f"unit_l1: {UNIT_L1}",
        f"unit_l2: {UNIT_L2}",
        f"unit_l3: {item['unit_l3']}",
        f"source: {SOURCE}",
        "tags:",
        "- 수동작성",
        f"- {item['qtype']}",
        f"- 출제번호-{label}",
        "- 과목-확률과통계",
        "assets:",
    ]
    for a in assets:
        lines.append(f"- {a}")

    lines.extend(["---", "", "## Q", item["q"].strip(), "", "## Choices"])

    if item["choices"]:
        for no, choice in zip(["①", "②", "③", "④", "⑤"], item["choices"]):
            lines.append(f"{no} {choice}")

    lines.extend(
        [
            "",
            "## Answer",
            str(item["answer"]).strip(),
            "",
            "## Solution",
            item["solution"].strip(),
            "",
        ]
    )
    return "\n".join(lines)


def make_q4_scan(out_path: Path) -> None:
    cols, rows = 5, 4
    cell = 140
    margin = 60

    width = margin * 2 + cols * cell
    height = margin * 2 + rows * cell

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    x0, y0 = margin, margin

    for c in range(cols + 1):
        x = x0 + c * cell
        draw.line([(x, y0), (x, y0 + rows * cell)], fill="black", width=3)
    for r in range(rows + 1):
        y = y0 + r * cell
        draw.line([(x0, y), (x0 + cols * cell, y)], fill="black", width=3)

    # A: bottom-left, B: top-right, C: interior node
    ax, ay = x0, y0 + rows * cell
    bx, by = x0 + cols * cell, y0
    cx, cy = x0 + 3 * cell, y0 + 2 * cell

    dot_r = 5
    draw.ellipse((ax - dot_r, ay - dot_r, ax + dot_r, ay + dot_r), fill="black")
    draw.ellipse((bx - dot_r, by - dot_r, bx + dot_r, by + dot_r), fill="black")
    draw.ellipse((cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r), fill="black")

    draw.text((ax - 28, ay + 10), "A", fill="black")
    draw.text((bx + 10, by - 10), "B", fill="black")
    draw.text((cx + 10, cy - 12), "C", fill="black")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def main() -> None:
    if not PDF_SRC.exists():
        raise FileNotFoundError(f"source PDF not found: {PDF_SRC}")

    target_ids = {f"{PREFIX}-{q['num']:03d}" for q in QUESTIONS}
    deleted_extra: list[str] = []
    created: list[str] = []
    updated: list[str] = []
    warnings: list[str] = []
    results: list[tuple[str, str, str]] = []

    # Remove wrong leftovers (for example, non-existent problem numbers from previous runs).
    for pdir in sorted(PROBLEMS.glob(f"{PREFIX}-*")):
        if not pdir.is_dir():
            continue
        if pdir.name not in target_ids:
            shutil.rmtree(pdir)
            deleted_extra.append(pdir.name)

    for item in QUESTIONS:
        qnum = item["num"]
        qid = f"{PREFIX}-{qnum:03d}"
        pdir = PROBLEMS / qid
        existed = pdir.exists()

        (pdir / "assets" / "original").mkdir(parents=True, exist_ok=True)
        shutil.copy2(PDF_SRC, pdir / "assets" / "original" / PDF_SRC.name)

        # Clean old scan when this question has no figure.
        scan_path = pdir / "assets" / "scan.png"
        if item.get("has_scan"):
            if qnum == 4:
                make_q4_scan(scan_path)
            else:
                warnings.append(f"{qid}: has_scan=True but no scan builder")
        else:
            if scan_path.exists():
                scan_path.unlink()

        md_path = pdir / "problem.md"
        md_path.write_text(build_markdown(item), encoding="utf-8", newline="\n")

        if existed:
            updated.append(qid)
            results.append((qid, "UPDATED", "problem.md rewritten from PDF transcription"))
        else:
            created.append(qid)
            results.append((qid, "CREATED", "new problem folder from PDF transcription"))

    print("SUMMARY")
    print(f"created={len(created)}")
    print(f"updated={len(updated)}")
    print(f"deleted_extra={len(deleted_extra)}")
    print(f"warnings={len(warnings)}")
    print("")
    print("DELETED_EXTRA")
    for qid in deleted_extra:
        print(qid)
    print("")
    print("RESULTS")
    for qid, status, msg in results:
        print(f"{qid}\t{status}\t{msg}")
    print("")
    print("WARNINGS")
    for w in warnings:
        print(w)


if __name__ == "__main__":
    main()

