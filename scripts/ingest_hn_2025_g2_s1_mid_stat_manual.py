from __future__ import annotations

from pathlib import Path
import shutil
import textwrap
from typing import Dict, List
import sys

import yaml

def txt(raw: str) -> str:
    return textwrap.dedent(raw).strip()


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level
from unit_taxonomy import normalize_unit_triplet

ORIGINAL = ROOT / "db" / "original"
PROBLEMS = ROOT / "db" / "problems"

META = {
    "school": "HN",
    "year": 2025,
    "grade": 2,
    "semester": 1,
    "exam": "MID2",
    "subject": "STAT",
    "source": "user_upload_2026-03-05",
}


ROWS: List[Dict[str, object]] = [
    {
        "source_no": 1,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            회장과 부회장을 포함한 6명의 회원이 원탁에 둘러앉을 때,
            회장과 부회장이 이웃하지 않게 앉는 경우의 수는?
            (단, 회전하여 일치하는 것은 같은 것으로 본다.)
            """
        ),
        "choices": ["① 36", "② 72", "③ 144", "④ 288", "⑤ 480"],
        "answer": "②",
        "solution": txt(
            """
            전체 원순열의 수는 $(6-1)!=120$이다.

            회장과 부회장이 이웃하여 앉는 경우는 두 사람을 한 묶음으로 보면
            5개를 원탁에 배치하는 경우이므로 $(5-1)!=24$가지이고,
            두 사람의 순서를 바꾸는 2가지를 곱해 $48$가지이다.

            따라서 구하는 경우의 수는
            $$
            120-48=72
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 2,
        "kind": "objective",
        "type": "객관식",
        "q": "네 개의 숫자 0, 1, 2, 3 중에서 중복을 허용하여 만들 수 있는 세 자리 자연수의 개수는?",
        "choices": ["① 12", "② 24", "③ 48", "④ 96", "⑤ 192"],
        "answer": "③",
        "solution": txt(
            """
            백의 자리는 0이 될 수 없으므로 $1,2,3$의 3가지이다.
            십의 자리와 일의 자리는 각각 4가지씩 가능하다.

            따라서 개수는
            $$
            3\\times 4\\times 4=48
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 3,
        "kind": "objective",
        "type": "객관식",
        "q": "크기와 모양이 같은 흰 공 2개, 검은 공 3개, 파란 공 1개를 일렬로 나열하는 경우의 수는?",
        "choices": ["① 12", "② 24", "③ 48", "④ 60", "⑤ 120"],
        "answer": "④",
        "solution": txt(
            """
            같은 색 공끼리는 서로 구별하지 않으므로 중복순열을 쓴다.

            전체 6개 중 흰 공 2개, 검은 공 3개, 파란 공 1개이므로
            $$
            \\frac{6!}{2!\\,3!\\,1!}=\\frac{720}{12}=60
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 4,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            3개의 숫자 4, 5, 6 중에서 중복을 허용하여 네 자리 자연수를 만들 때,
            4와 5를 모두 포함하는 자연수의 개수는?
            """
        ),
        "choices": ["① 30", "② 40", "③ 50", "④ 60", "⑤ 70"],
        "answer": "③",
        "solution": txt(
            """
            전체 경우는 $3^4=81$이다.

            4를 포함하지 않는 경우는 $\\{5,6\\}$만 쓰므로 $2^4=16$가지,
            5를 포함하지 않는 경우도 $16$가지이다.

            4와 5를 모두 포함하지 않는 경우(즉 6만 쓰는 경우)는 1가지이다.

            포함배제를 쓰면
            $$
            81-16-16+1=50
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 5,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            같은 종류의 빵 10개를 서로 다른 상자 3개에 넣으려고 한다.
            빈 상자가 없도록 빵을 모두 나누어 넣는 경우의 수는?
            """
        ),
        "choices": ["① 36", "② 46", "③ 56", "④ 66", "⑤ 76"],
        "answer": "①",
        "solution": txt(
            """
            각 상자에 들어가는 빵의 수를 $x,y,z$라 하면
            $$
            x+y+z=10\\quad(x,y,z\\ge 1)
            $$
            의 양의 정수해 개수를 구하면 된다.

            별과 막대 공식을 쓰면
            $$
            \\binom{10-1}{3-1}=\\binom{9}{2}=36
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 6,
        "kind": "objective",
        "type": "객관식",
        "q": "세 자리 자연수 중에서 각 자리의 수의 합이 7인 모든 자연수의 개수는?",
        "choices": ["① 24", "② 28", "③ 36", "④ 56", "⑤ 72"],
        "answer": "②",
        "solution": txt(
            """
            세 자리 수를 $\\overline{abc}$라 하면
            $$
            a+b+c=7,\\quad a\\ge 1,\\ b,c\\ge 0
            $$
            이다.

            $a'=a-1$로 두면
            $$
            a'+b+c=6\\quad(a',b,c\\ge 0)
            $$
            가 되고, 음이 아닌 정수해의 개수는
            $$
            \\binom{6+3-1}{3-1}=\\binom{8}{2}=28
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 7,
        "kind": "objective",
        "type": "객관식",
        "q": "다항식 $(a+b+c)^2(x+y)^3$의 전개식에서 서로 다른 항의 개수는?",
        "choices": ["① 6", "② 12", "③ 18", "④ 24", "⑤ 30"],
        "answer": "④",
        "solution": txt(
            """
            $(a+b+c)^2$의 서로 다른 항의 수는
            $$
            \\binom{2+3-1}{2}=\\binom{4}{2}=6
            $$
            이고, $(x+y)^3$의 서로 다른 항의 수는
            $$
            \\binom{3+2-1}{3}=\\binom{4}{3}=4
            $$
            이다.

            변수 집합이 서로 다르므로 곱의 서로 다른 항의 수는 곱으로 계산되어
            $$
            6\\times 4=24
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 8,
        "kind": "objective",
        "type": "객관식",
        "q": "$(x^3+\\frac{a}{x})^5$의 전개식에서 $x^3$의 계수가 $-80$일 때, 실수 $a$의 값은?",
        "choices": ["① 3", "② 2", "③ 1", "④ -1", "⑤ -2"],
        "answer": "⑤",
        "solution": txt(
            """
            일반항은
            $$
            \\binom{5}{k}(x^3)^{5-k}\\left(\\frac{a}{x}\\right)^k
            =\\binom{5}{k}a^k x^{15-4k}
            $$
            이다.

            $x$의 지수가 3이 되려면
            $$
            15-4k=3\\Rightarrow k=3
            $$
            이다.

            따라서 $x^3$의 계수는
            $$
            \\binom{5}{3}a^3=10a^3
            $$
            이므로
            $$
            10a^3=-80\\Rightarrow a^3=-8\\Rightarrow a=-2
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 9,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            철수를 포함한 6명의 친구들이 수학여행에서 기념사진을 찍으려고 한다.
            철수를 포함하여 최소한 2명이 나오도록 사진을 찍는 경우의 수는?
            """
        ),
        "choices": ["① 31", "② 32", "③ 57", "④ 63", "⑤ 64"],
        "answer": "①",
        "solution": txt(
            """
            철수는 반드시 포함되므로 나머지 5명의 포함 여부만 정하면 된다.

            철수만 나오는 경우(나머지 5명 모두 제외)는 조건을 만족하지 않으므로 제외한다.

            따라서 경우의 수는
            $$
            2^5-1=31
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 10,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            1부터 10까지의 자연수가 각각 하나씩 적힌 카드 10장 중 임의로 1장을 뽑는 시행에서,
            카드에 적힌 수가 10의 약수인 사건을 $A$, 8의 약수인 사건을 $B$라고 할 때,
            사건 $A$와는 배반이고 사건 $B$와는 배반이 아닌 사건의 개수는?
            """
        ),
        "choices": ["① 16", "② 32", "③ 48", "④ 64", "⑤ 80"],
        "answer": "③",
        "solution": txt(
            """
            표본공간을 $S=\\{1,2,\\dots,10\\}$라 하자.

            $A=\\{1,2,5,10\\}$, $B=\\{1,2,4,8\\}$이다.

            사건 $E$가 $A$와 배반이라는 것은 $E\\subseteq S\\setminus A$라는 뜻이다.
            따라서 가능한 원소는
            $$
            S\\setminus A=\\{3,4,6,7,8,9\\}
            $$
            의 6개이다.

            또 $E$가 $B$와 배반이 아니려면 $E\\cap B\\ne\\varnothing$이어야 한다.
            $S\\setminus A$ 안에서 $B$의 원소는 $\\{4,8\\}$이므로,
            $E$는 4 또는 8을 적어도 하나 포함해야 한다.

            전체 부분집합 수는 $2^6=64$,
            4와 8을 모두 포함하지 않는 부분집합 수는 나머지 4원소 부분집합 수 $2^4=16$이다.

            따라서
            $$
            64-16=48
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 11,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            다섯 개의 숫자 0, 1, 2, 3, 4 중에서 중복을 허용하여 만들 수 있는
            네 자리 자연수 중 임의로 하나의 수를 택할 때,
            택한 수가 2200보다 작을 확률은?
            """
        ),
        "choices": ["① $\\frac{1}{5}$", "② $\\frac{2}{5}$", "③ $\\frac{3}{10}$", "④ $\\frac{7}{20}$", "⑤ $\\frac{9}{20}$"],
        "answer": "④",
        "solution": txt(
            """
            전체 네 자리 수 개수는
            $$
            4\\times 5\\times 5\\times 5=500
            $$
            이다.

            $2200$보다 작은 경우를 센다.

            천의 자리가 1이면 나머지 3자리는 자유이므로 $5^3=125$개.

            천의 자리가 2이면 $2abc<2200$이어야 하므로
            백의 자리 $a$는 0 또는 1의 2가지이고,
            나머지 두 자리는 각각 5가지다.
            따라서 $2\\times 5\\times 5=50$개.

            유리한 경우는 $125+50=175$개이므로 확률은
            $$
            \\frac{175}{500}=\\frac{7}{20}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 12,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            어느 마을에 살고 있는 120가구 중에서 닭을 기르는 집은 72가구이고,
            돼지를 기르는 집은 54가구이다.
            또, 닭과 돼지를 모두 기르는 집은 24가구이다.
            이 마을에서 임의로 한 집을 택할 때,
            그 집에서 닭 또는 돼지를 기를 확률은?
            """
        ),
        "choices": ["① $\\frac{9}{20}$", "② $\\frac{11}{20}$", "③ $\\frac{13}{20}$", "④ $\\frac{3}{4}$", "⑤ $\\frac{17}{20}$"],
        "answer": "⑤",
        "solution": txt(
            """
            닭을 기르는 집의 집합을 $C$, 돼지를 기르는 집의 집합을 $P$라 하면
            $$
            |C\\cup P|=|C|+|P|-|C\\cap P|=72+54-24=102
            $$
            이다.

            따라서 구하는 확률은
            $$
            \\frac{102}{120}=\\frac{17}{20}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 13,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            남학생 4명과 여학생 5명으로 구성된 어느 모둠에서 청소 당번 3명을 뽑을 때,
            적어도 한 명의 여학생이 청소 당번으로 뽑힐 확률은?
            """
        ),
        "choices": ["① $\\frac{1}{21}$", "② $\\frac{5}{42}$", "③ $\\frac{1}{6}$", "④ $\\frac{37}{42}$", "⑤ $\\frac{20}{21}$"],
        "answer": "⑤",
        "solution": txt(
            """
            여학생이 한 명도 뽑히지 않는 경우를 여사건으로 계산한다.

            전체 경우의 수는
            $$
            \\binom{9}{3}
            $$
            이고, 남학생 4명 중 3명을 뽑는 경우의 수는
            $$
            \\binom{4}{3}
            $$
            이다.

            따라서 구하는 확률은
            $$
            1-\\frac{\\binom{4}{3}}{\\binom{9}{3}}
            =1-\\frac{4}{84}
            =1-\\frac{1}{21}
            =\\frac{20}{21}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 14,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            흰색 탁구공 8개와 주황색 탁구공 4개가 들어 있는 주머니에서
            탁구공을 임의로 한 개씩 두 번 꺼낼 때,
            두 공 모두 주황색 탁구공을 꺼낼 확률은?
            (단, 꺼낸 공은 다시 넣지 않는다.)
            """
        ),
        "choices": ["① $\\frac{1}{11}$", "② $\\frac{1}{9}$", "③ $\\frac{8}{33}$", "④ $\\frac{3}{11}$", "⑤ $\\frac{5}{11}$"],
        "answer": "①",
        "solution": txt(
            """
            두 공이 모두 주황색일 확률은
            $$
            \\frac{\\binom{4}{2}}{\\binom{12}{2}}
            =\\frac{6}{66}
            =\\frac{1}{11}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 15,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            어느 거짓말 탐지기는 참말을 '참'으로 판단할 확률이 0.9이고
            거짓말을 '거짓'으로 판단할 확률이 0.95라고 한다.
            거짓말을 할 확률이 0.9인 어떤 용의자의 답변을 거짓말 탐지기로 판단한 결과 중에서
            임의로 택한 결과가 '참'이었을 때,
            그 답변이 실제로 참이었을 확률은?
            """
        ),
        "choices": ["① $\\frac{1}{3}$", "② $\\frac{1}{2}$", "③ $\\frac{2}{3}$", "④ $\\frac{4}{5}$", "⑤ $\\frac{9}{10}$"],
        "answer": "③",
        "solution": txt(
            """
            사건을 다음과 같이 두자.

            $T$: 실제로 참말, $L$: 실제로 거짓말, $R$: 탐지 결과가 '참'

            문제에서
            $$
            P(T)=0.1,\\quad P(L)=0.9,
            $$
            $$
            P(R\\mid T)=0.9,\\quad P(R\\mid L)=1-0.95=0.05
            $$
            이다.

            베이즈 정리를 적용하면
            $$
            P(T\\mid R)=\\frac{P(R\\mid T)P(T)}{P(R\\mid T)P(T)+P(R\\mid L)P(L)}
            =\\frac{0.9\\cdot 0.1}{0.9\\cdot 0.1+0.05\\cdot 0.9}
            =\\frac{0.09}{0.135}
            =\\frac{2}{3}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 16,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            표본공간 $S$의 두 사건 $A, B$에 대하여 다음 <보기>에서 옳은 것의 개수는?
            (단, $0<P(A)<1$, $0<P(B)<1$)

            <보기>
            ㄱ. 서로 배반이 아닌 두 사건은 독립사건이다.
            ㄴ. 서로 배반인 두 사건은 종속사건이다.
            ㄷ. 서로 종속인 두 사건은 배반사건이 아니다.
            ㄹ. $A, B$가 서로 독립이면 $P(A\\mid B^c)=1-P(A^c\\mid B)$이다.
            ㅁ. $A\\cup B=S$이면 $P(A)+P(B)=1$이다.
            ㅂ. $A, B$가 서로 독립이면 $A^c, B^c$은 서로 종속이다.
            """
        ),
        "choices": ["① 1개", "② 2개", "③ 3개", "④ 4개", "⑤ 5개"],
        "answer": "②",
        "solution": txt(
            """
            각 문장을 판단한다.

            ㄱ. 배반이 아니어도 독립일 필요는 없으므로 거짓.

            ㄴ. 배반이면 $P(A\\cap B)=0$이고, $0<P(A),P(B)<1$에서 $P(A)P(B)>0$이므로
            독립이 아니고 종속이다. 참.

            ㄷ. 종속이라도 배반일 수 있다(ㄴ의 경우). 거짓.

            ㄹ. $A,B$가 독립이면 $A$와 $B^c$도 독립이므로
            $$
            P(A\\mid B^c)=P(A)
            $$
            또한 $A^c$와 $B$도 독립이므로
            $$
            P(A^c\\mid B)=P(A^c)=1-P(A)
            $$
            따라서
            $$
            1-P(A^c\\mid B)=P(A)=P(A\\mid B^c)
            $$
            이므로 참.

            ㅁ. 일반적으로
            $$
            P(A\\cup B)=P(A)+P(B)-P(A\\cap B)
            $$
            인데 $P(A\\cup B)=1$이므로 $P(A)+P(B)=1+P(A\\cap B)$이다.
            항상 1은 아니므로 거짓.

            ㅂ. 독립이면 여사건들 $A^c,B^c$도 독립이다. 종속이라는 말은 거짓.

            옳은 것은 ㄴ, ㄹ의 2개이다.
            """
        ),
    },
    {
        "source_no": 17,
        "kind": "objective",
        "type": "객관식",
        "q": txt(
            """
            어느 양궁 선수가 10점 과녁을 맞힐 확률은 $\\frac{2}{3}$이라고 한다.
            이 선수가 4발을 쏘았을 때, 적어도 두 발 이상은 10점 과녁을 맞힐 확률은?
            """
        ),
        "choices": ["① $\\frac{7}{9}$", "② $\\frac{8}{9}$", "③ $\\frac{25}{27}$", "④ $\\frac{26}{27}$", "⑤ $\\frac{79}{81}$"],
        "answer": "②",
        "solution": txt(
            """
            $X$를 10점 과녁을 맞힌 횟수라 하면
            $$
            X\\sim B\\left(4,\\frac{2}{3}\\right)
            $$
            이다.

            구하는 확률은
            $$
            P(X\\ge 2)=1-P(X=0)-P(X=1)
            $$
            이다.

            $$
            P(X=0)=\\left(\\frac{1}{3}\\right)^4=\\frac{1}{81}
            $$
            $$
            P(X=1)=\\binom{4}{1}\\left(\\frac{2}{3}\\right)\\left(\\frac{1}{3}\\right)^3=\\frac{8}{81}
            $$
            따라서
            $$
            P(X\\ge 2)=1-\\frac{1}{81}-\\frac{8}{81}=\\frac{72}{81}=\\frac{8}{9}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 1,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "q": "전체집합 $U=\\{1,2,3,4,5,6,7,8\\}$의 두 부분집합 $A,B$에 대하여 $A\\cap B=\\{1,3,5,7\\}$을 만족하는 두 집합 $A,B$를 정하는 경우의 수를 구하시오.",
        "choices": [],
        "answer": "81",
        "solution": txt(
            """
            $1,3,5,7$은 교집합에 반드시 있어야 하므로 각 원소는 $(A,B)$에 대해 $(1,1)$로 고정된다.

            나머지 원소 $2,4,6,8$은 교집합에 포함되면 안 되므로
            각 원소마다 가능한 포함 형태는
            $$
            (0,0),\\ (1,0),\\ (0,1)
            $$
            의 3가지이다.

            서로 독립적으로 4개 원소를 정하면 되므로
            $$
            3^4=81
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 2,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "q": "오늘부터 $98^7$일 후가 월요일일 때, 오늘부터 $100^7$일 후는 무슨 요일인지 구하시오.",
        "choices": [],
        "answer": "수요일",
        "solution": txt(
            """
            요일은 7일 주기이므로 7로 나눈 나머지를 본다.

            $$
            98\\equiv 0\\pmod 7\\Rightarrow 98^7\\equiv 0\\pmod 7
            $$
            이므로 $98^7$일 후의 요일은 오늘과 같다.
            따라서 오늘은 월요일이다.

            또
            $$
            100\\equiv 2\\pmod 7\\Rightarrow 100^7\\equiv 2^7\\equiv 2\\pmod 7
            $$
            이므로 $100^7$일 후는 오늘보다 2일 뒤이다.
            월요일에서 2일 뒤는 수요일이다.
            """
        ),
    },
    {
        "source_no": 3,
        "kind": "subjective",
        "type": "서답형(단답형)",
        "q": txt(
            """
            좌표평면의 원점에 점 $P$가 있다.
            주사위를 한 번 던져서 짝수의 눈이 나오면 $x$축의 방향으로 2만큼 평행이동하고,
            홀수의 눈이 나오면 $y$축의 방향으로 3만큼 평행이동한다.
            주사위를 6번 던질 때, 점 $P$가 직선 $y=2x-3$ 위에 있을 확률을 구하시오.
            """
        ),
        "choices": [],
        "answer": "$\\frac{5}{16}$",
        "solution": txt(
            """
            주사위를 6번 던져 짝수가 나온 횟수를 $e$, 홀수가 나온 횟수를 $o$라 하면
            $$
            e+o=6
            $$
            이다.

            이때 최종 좌표는
            $$
            (x,y)=(2e,\\ 3o)=(2e,\\ 3(6-e))=(2e,\\ 18-3e)
            $$
            이다.

            직선 $y=2x-3$ 위에 있으려면
            $$
            18-3e=2(2e)-3
            $$
            $$
            21=7e\\Rightarrow e=3
            $$
            이어야 한다.

            즉 6번 중 짝수가 정확히 3번 나올 확률이므로
            $$
            \\binom{6}{3}\\left(\\frac12\\right)^6=\\frac{20}{64}=\\frac{5}{16}
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 4,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "q": txt(
            """
            다음 조건을 만족시키는 음이 아닌 정수 $a,b,c,d$의 순서쌍 $(a,b,c,d)$의 개수를
            구하는 풀이 과정과 답을 쓰시오.

            (가) $a+b+c+d=6$
            (나) $a\\ne b$
            """
        ),
        "choices": [],
        "answer": "68",
        "solution": txt(
            """
            먼저 $a,b,c,d\\ge 0$에서
            $$
            a+b+c+d=6
            $$
            의 전체 해의 개수는
            $$
            \\binom{6+4-1}{4-1}=\\binom{9}{3}=84
            $$
            이다.

            이제 조건 $a\\ne b$를 반영하기 위해 $a=b$인 경우를 뺀다.
            $a=b=t$로 두면
            $$
            2t+c+d=6
            $$
            이다.

            $t=0,1,2,3$에 대해 $(c,d)$의 개수는 각각
            $$
            7,\\ 5,\\ 3,\\ 1
            $$
            이므로 합은 $16$이다.

            따라서 조건을 만족하는 개수는
            $$
            84-16=68
            $$
            이다.
            """
        ),
    },
    {
        "source_no": 5,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "q": txt(
            """
            $\\binom{20}{0}+\\binom{20}{2}\\cdot 3^2+\\binom{20}{4}\\cdot 3^4+\\binom{20}{6}\\cdot 3^6+\\cdots+\\binom{20}{20}\\cdot 3^{20}
            =2^m(2^{20}+1)$일 때, 자연수 $m$의 값을 구하는 풀이 과정과 답을 쓰시오.
            """
        ),
        "choices": [],
        "answer": "19",
        "solution": txt(
            """
            주어진 합을 $S$라 하자.

            짝수차 항의 합 공식으로
            $$
            S=\\frac{(1+3)^{20}+(1-3)^{20}}{2}
            $$
            이다.

            따라서
            $$
            S=\\frac{4^{20}+(-2)^{20}}{2}
            =\\frac{2^{40}+2^{20}}{2}
            =2^{39}+2^{19}
            =2^{19}(2^{20}+1)
            $$
            이 된다.

            그러므로 $m=19$이다.
            """
        ),
    },
    {
        "source_no": 6,
        "kind": "subjective",
        "type": "서답형(서술형)",
        "q": txt(
            """
            주머니 $A$에는 흰 구슬 3개, 검은 구슬 5개가 들어 있고,
            주머니 $B$에는 흰 구슬 3개, 검은 구슬 2개가 들어 있다.
            임의로 주머니 한 개를 택하여 꺼낸 두 개의 구슬이 흰 구슬 1개, 검은 구슬 1개이었을 때,
            그 구슬이 주머니 $A$에서 나왔을 확률은 $\\frac{q}{p}$($p,q$는 서로 소인 자연수)이다.
            이때 $p+q$의 값을 구하는 풀이 과정과 답을 쓰시오.
            (단, 각 주머니를 선택할 확률은 같다.)
            """
        ),
        "choices": [],
        "answer": "78",
        "solution": txt(
            """
            사건을 다음과 같이 두자.

            $E$: 꺼낸 2개의 구슬이 흰 1개, 검은 1개

            각 주머니를 선택할 확률은 $\\frac12$이다.

            $$
            P(E\\mid A)=\\frac{\\binom31\\binom51}{\\binom82}=\\frac{15}{28}
            $$
            $$
            P(E\\mid B)=\\frac{\\binom31\\binom21}{\\binom52}=\\frac{6}{10}=\\frac35
            $$

            베이즈 정리를 쓰면
            $$
            P(A\\mid E)
            =\\frac{P(E\\mid A)P(A)}{P(E\\mid A)P(A)+P(E\\mid B)P(B)}
            =\\frac{\\frac{15}{28}\\cdot\\frac12}{\\frac{15}{28}\\cdot\\frac12+\\frac35\\cdot\\frac12}
            =\\frac{15/28}{15/28+3/5}
            $$
            $$
            =\\frac{15/28}{159/140}
            =\\frac{25}{53}
            $$
            이다.

            따라서 $\\frac{q}{p}=\\frac{25}{53}$이므로
            $$
            p+q=53+25=78
            $$
            이다.
            """
        ),
    },
]


def problem_id(row: Dict[str, object]) -> str:
    source_no = int(row["source_no"])
    if row["kind"] == "subjective":
        source_no += 100
    return (
        f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-"
        f"{META['exam']}-{META['subject']}-{source_no:03d}"
    )


def main() -> int:
    pdfs = sorted(
        [p for p in ORIGINAL.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"],
        key=lambda p: p.name,
    )
    if not pdfs:
        print("[ERROR] db/original에 PDF가 없습니다.")
        return 1
    source_pdf = pdfs[0]

    planned = [problem_id(row) for row in ROWS]
    duplicates = [pid for pid in planned if (PROBLEMS / pid).exists()]
    if duplicates:
        print("[DUPLICATE] 이미 존재하는 폴더:")
        for pid in duplicates:
            print(f"- {pid}")
        print("[STOP] 중복이 있어 생성을 중단했습니다.")
        return 2

    created: List[str] = []
    warnings: List[str] = []
    uncertain: List[str] = []

    for row in ROWS:
        pid = problem_id(row)
        folder = PROBLEMS / pid
        folder.mkdir(parents=True, exist_ok=False)

        assets_original = folder / "assets" / "original"
        assets_original.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_pdf, assets_original / source_pdf.name)

        source_no = int(row["source_no"])
        source_kind = str(row["kind"])
        source_label = str(source_no) if source_kind == "objective" else f"서답{source_no}번"

        choices_lines = list(row["choices"])  # type: ignore[arg-type]
        choices_text = "\n".join(choices_lines).strip()
        q_text = str(row["q"]).strip()
        answer_text = str(row["answer"]).strip()
        solution_text = str(row["solution"]).strip()

        no_for_classifier = int(pid.rsplit("-", 1)[-1])
        classified = classify_unit_and_level(
            question_text=q_text,
            choices_text=choices_text,
            answer_text=answer_text,
            solution_text=solution_text,
            qtype=str(row["type"]),
            grade=int(META["grade"]),
            problem_no=no_for_classifier,
        )
        unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
            classified.unit_l1,
            classified.unit_l2,
            classified.unit_l3,
            grade=int(META["grade"]),
        )

        front = {
            "id": pid,
            "school": META["school"],
            "year": META["year"],
            "grade": META["grade"],
            "semester": META["semester"],
            "exam": META["exam"],
            "subject": META["subject"],
            "type": row["type"],
            "source_question_no": source_no,
            "source_question_kind": source_kind,
            "source_question_label": source_label,
            "difficulty": int(classified.level),
            "level": int(classified.level),
            "unit": f"{unit_l1}>{unit_l2}>{unit_l3}",
            "unit_l1": unit_l1,
            "unit_l2": unit_l2,
            "unit_l3": unit_l3,
            "source": META["source"],
            "tags": [
                "수동작성",
                str(row["type"]),
                f"출제번호-{source_label}",
                "과목-확률과통계",
            ],
            "assets": [
                "assets/original/",
                f"assets/original/{source_pdf.name}",
            ],
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

        created.append(pid)
        print(
            f"[CREATED] {pid} | kind={source_kind} source_no={source_no} | "
            f"unit={unit_l3} | level={classified.level}"
        )

        if str(row.get("ocr_uncertain", "")).strip().lower() in {"1", "true", "yes"}:
            uncertain.append(pid)

    print(
        f"[SUMMARY] created={len(created)} updated=0 skipped=0 warnings={len(warnings)}"
    )
    if warnings:
        print("[WARNINGS]")
        for msg in warnings:
            print(f"- {msg}")
    print("[OCR_UNCERTAIN]")
    if uncertain:
        for pid in uncertain:
            print(f"- {pid}")
    else:
        print("- none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
