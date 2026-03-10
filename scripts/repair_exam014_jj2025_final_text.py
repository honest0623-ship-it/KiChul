from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"


def s(text: str) -> str:
    return text.strip()


DATA = {
    "JJ-2025-G1-S1-Final-001": {
        "q": s(
            r"""
사차방정식 \(x^4+2x^3+2x^2-2x-3=0\)이 두 개의 실근과 두 개의 허근을 가질 때, 두 허근의 합은?
"""
        ),
        "choices": ["① -2", "② -1", "③ 0", "④ 1", "⑤ 2"],
    },
    "JJ-2025-G1-S1-Final-002": {
        "q": s(
            r"""
방정식 \(x^3+8=0\)의 한 허근을 \(\omega\)라 할 때,
\[
\omega^4+\omega^3+4\omega^2+9=a\omega+b
\]
이다. 이때 실수 \(a,\ b\)에 대하여 \(a+b\)의 값은?
"""
        ),
        "choices": ["① -15", "② -10", "③ -5", "④ 0", "⑤ 5"],
    },
    "JJ-2025-G1-S1-Final-003": {
        "q": s(
            r"""
삼차방정식 \(x^3+x-2=0\)의 세 근을 \(\alpha,\ \beta,\ \gamma\)라 할 때,
\[
\alpha^4\beta^4\gamma^4
\]
의 값은?
"""
        ),
        "choices": ["① 2", "② 4", "③ 8", "④ 16", "⑤ 32"],
    },
    "JJ-2025-G1-S1-Final-004": {
        "q": s(
            r"""
연립부등식
\[
2x-5<6(x+1)+1\le 2x+11
\]
을 만족시키는 정수 \(x\)의 개수는?
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "JJ-2025-G1-S1-Final-005": {
        "q": s(
            r"""
삼차방정식
\[
x^3-2x^2-(k+8)x-2k=0
\]
이 세 실근을 가질 때, 한 근은 \(0\)보다 작고 나머지 두 근은 모두 \(0\)보다 크도록 하는 모든 정수 \(k\)의 값의 합은?
"""
        ),
        "choices": ["① -10", "② -9", "③ -8", "④ -7", "⑤ -6"],
    },
    "JJ-2025-G1-S1-Final-006": {
        "q": s(
            r"""
두 부등식
\[
x^2+ax+b\ge 0,\qquad x^2+cx+d\le 0
\]
을 동시에 만족시키는 \(x\)의 값의 범위가
\[
-3\le x\le -1 \quad \text{또는} \quad x=2
\]
로 주어질 때, 상수 \(a,\ b,\ c,\ d\)에 대하여
\[
a^2+b^2+c^2+d^2
\]
의 값은?
"""
        ),
        "choices": ["① 34", "② 36", "③ 38", "④ 40", "⑤ 42"],
    },
    "JJ-2025-G1-S1-Final-007": {
        "q": s(
            r"""
부등식
\[
2|x-1|+|x+1|\le a
\]
를 만족하는 실수 \(x\)의 범위가
\[
-2\le x\le b
\]
가 되도록 하는 상수 \(a,\ b\)에 대하여 \(3ab\)의 값은?
"""
        ),
        "choices": ["① 54", "② 56", "③ 58", "④ 60", "⑤ 62"],
    },
    "JJ-2025-G1-S1-Final-008": {
        "q": s(
            r"""
여섯 개의 문자 \(a,\ b,\ c,\ d,\ e,\ f\)를 사전식으로 배열할 때, \(444\)번째로 배열된 문자는?
"""
        ),
        "choices": [
            "① `daefcb`",
            "② `dbcafe`",
            "③ `dcfabe`",
            "④ `deacfb`",
            "⑤ `debfca`",
        ],
    },
    "JJ-2025-G1-S1-Final-009": {
        "q": s(
            r"""
어느 지역에서 열린 배구 대회에 참가한 \(n\)개의 팀이 서로 다른 팀과 모두 한 번씩 경기하였더니 총 \(55\)번의 경기를 하였다. 이때 \(n\)의 값은?
"""
        ),
        "choices": ["① 10", "② 11", "③ 12", "④ 13", "⑤ 14"],
    },
    "JJ-2025-G1-S1-Final-010": {
        "q": s(
            r"""
서로 다른 \(4\)개의 상자에 공 \(3\)개를 넣으려고 한다. 각 상자에 많아야 공 \(1\)개씩만 넣을 때, 서로 다른 공 \(3\)개를 넣는 방법의 수를 \(a\), 똑같은 공 \(3\)개를 넣는 방법의 수를 \(b\)라 하자. 이때 \(a+b\)의 값은?
"""
        ),
        "choices": ["① 24", "② 28", "③ 32", "④ 36", "⑤ 40"],
    },
    "JJ-2025-G1-S1-Final-011": {
        "q": s(
            r"""
방정식
\[
x+2y+3z=12
\]
를 만족시키는 자연수 \(x,\ y,\ z\)의 순서쌍 \((x,\ y,\ z)\)의 개수를 구하면?
"""
        ),
        "choices": ["① 5", "② 6", "③ 7", "④ 8", "⑤ 9"],
    },
    "JJ-2025-G1-S1-Final-012": {
        "q": s(
            r"""
동근이와 재홍이를 포함한 남학생 \(5\)명과 주영이를 포함한 여학생 \(5\)명 중에서 남학생 \(2\)명, 여학생 \(3\)명을 뽑아 릴레이 선수로 출전시키고자 한다. 동근이와 주영이는 반드시 출전하고, 재홍이는 발목 부상으로 출전하지 않을 때, 릴레이 선수를 뽑아 달리는 순서를 정하는 경우의 수는?
"""
        ),
        "choices": ["① 2160", "② 2200", "③ 2240", "④ 2280", "⑤ 2320"],
    },
    "JJ-2025-G1-S1-Final-013": {
        "q": s(
            r"""
행렬
\[
A=\begin{pmatrix}2 & 0 \\ 6 & -1\end{pmatrix},\qquad
B=\begin{pmatrix}1 & -3 \\ 3 & -2\end{pmatrix}
\]
에 대하여 등식
\[
4A-X=2(X+B)
\]
를 만족시키는 행렬 \(X\)의 모든 성분의 합은?
"""
        ),
        "choices": ["① 8", "② 9", "③ 10", "④ 11", "⑤ 12"],
    },
    "JJ-2025-G1-S1-Final-014": {
        "q": s(
            r"""
다음 중 행렬의 곱셈이 불가능한 것은?
"""
        ),
        "choices": [
            r"① \(\begin{pmatrix}1 & -2 \\ 3 & 0\end{pmatrix}\begin{pmatrix}2 \\ -1\end{pmatrix}\)",
            r"② \(\begin{pmatrix}1 & 0 & -1\end{pmatrix}\begin{pmatrix}2 \\ 3 \\ -4\end{pmatrix}\)",
            r"③ \(\begin{pmatrix}1 \\ -2 \\ 3\end{pmatrix}\begin{pmatrix}4 & 0\end{pmatrix}\)",
            r"④ \(\begin{pmatrix}-1 \\ 2\end{pmatrix}\begin{pmatrix}3 & -4 \\ -5 & 1\end{pmatrix}\)",
            r"⑤ \(\begin{pmatrix}1 & -2\end{pmatrix}\begin{pmatrix}0 & 3 \\ 4 & -1\end{pmatrix}\)",
        ],
    },
    "JJ-2025-G1-S1-Final-015": {
        "q": s(
            r"""
행렬
\[
A=\begin{pmatrix}1 & 3 \\ -1 & -2\end{pmatrix}
\]
에 대하여
\[
X=2A^5-4A^2+A
\]
라 할 때, 행렬 \(X\)의 \((1,2)\)성분은?
"""
        ),
        "choices": ["① -4", "② -3", "③ 1", "④ 5", "⑤ 9"],
    },
    "JJ-2025-G1-S1-Final-101": {
        "q": s(
            r"""
삼차식
\[
f(x)=x^3+ax^2+bx+c
\]
이 다음 조건을 만족할 때, \(f(3)\)의 값을 작은 것부터 차례로 \(a_1,\ a_2,\ a_3,\ a_4,\ a_5\)라 하자. 이때 \(a_2+a_4\)의 값을 구하시오. (단, \(a,\ b,\ c\)는 실수이다.)

(가) 방정식 \(f(x)=0\)의 근 중 허근이 존재한다.

(나) \(f(x)=0\)이면 \(f(x^3)=0\)을 만족한다.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G1-S1-Final-102": {
        "q": s(
            r"""
서로 다른 \(6\)명을 한 줄로 세울 때, \(A\)와 \(B\)가 이웃하지 않고 \(A\)와 \(C\)도 이웃하지 않도록 세우는 경우의 수를 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G1-S1-Final-103": {
        "q": s(
            r"""
정사각행렬 \(A,\ B\)와 단위행렬 \(E\)가
\[
AB=O,\qquad A=B+2E
\]
를 만족시킨다. 이때
\[
A^6+B^6=kE
\]
가 되도록 하는 상수 \(k\)의 값을 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G1-S1-Final-104": {
        "q": s(
            r"""
연립방정식
\[
\begin{cases}
3x^2-y^2=-6,\\
2x-y=-1
\end{cases}
\]
의 해와 연립방정식
\[
\begin{cases}
3x+y^2=a,\\
x-y=b
\end{cases}
\]
의 해가 서로 같고 \(x<0\)일 때, \(a,\ b\)의 값을 각각 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G1-S1-Final-105": {
        "q": s(
            r"""
자연수
\[
A=4^k\times 5^2
\]
의 약수의 개수가 \(15\)개일 때, \(k\)의 값과 \(A\)의 약수의 총합을 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G1-S1-Final-106": {
        "q": s(
            r"""
두 행렬
\[
A=\begin{pmatrix}1 & 2 \\ 2 & 3\end{pmatrix},\qquad
B=\begin{pmatrix}1 & p \\ q & -1\end{pmatrix}
\]
에 대하여 \(AB=BA\)일 때, 상수 \(p,\ q\)의 값을 각각 구하시오.
"""
        ),
        "choices": [],
    },
}


def replace_section(text: str, section: str, body: str) -> str:
    pattern = re.compile(rf"(^## {re.escape(section)}\s*$\n)(.*?)(?=^## |\Z)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing section: {section}")
    body = body.rstrip()
    if body:
        replacement = match.group(1) + body + "\n\n"
    else:
        replacement = match.group(1) + "\n"
    return text[: match.start()] + replacement + text[match.end() :]


def update_problem(pid: str, q: str, choices: list[str]) -> None:
    path = PROBLEMS / pid / "problem.md"
    text = path.read_text(encoding="utf-8")
    text = replace_section(text, "Q", q)
    text = replace_section(text, "Choices", "\n".join(choices))
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for pid, item in DATA.items():
        update_problem(pid, item["q"], item["choices"])
        print(f"updated\t{pid}")


if __name__ == "__main__":
    main()
