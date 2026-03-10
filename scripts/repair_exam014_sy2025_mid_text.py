from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"
IMAGE_TAG = '<img src="assets/scan.png" alt="문항 원본" style="width:100% !important; max-width:100% !important; height:auto;" />'


def s(text: str) -> str:
    return text.strip()


DATA = {
    "SY-2025-G1-S1-MID-002": {
        "q": s(
            r"""
복소수 \(z\)에 대하여
\[
z+\overline{z}=4,\qquad z\overline{z}=5
\]
이다. \(z^2\)의 실수부분은? (단, \(\overline{z}\)는 \(z\)의 켤레복소수이다.)
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "SY-2025-G1-S1-MID-003": {
        "q": s(
            r"""
\(0\le x\le 3\)일 때, \(y=x^2-6x+5\)의 최댓값을 \(M\), 최솟값을 \(m\)이라 하자. 이때 \(M+m\)의 값은?
"""
        ),
        "choices": ["① 1", "② 3", "③ 5", "④ 7", "⑤ 9"],
    },
    "SY-2025-G1-S1-MID-004": {
        "q": s(
            r"""
이차방정식 \(x^2+3x+6=0\)의 두 근을 \(\alpha,\ \beta\)라 할 때,
\[
\frac{\alpha}{\beta}+\frac{\beta}{\alpha}
\]
의 값은?
"""
        ),
        "choices": [r"① \(-1\)", r"② \(-\frac12\)", r"③ \(0\)", r"④ \(\frac12\)", r"⑤ \(1\)"],
    },
    "SY-2025-G1-S1-MID-005": {
        "q": s(
            r"""
이차함수 \(y=-2x^2+5x+k\)의 그래프와 \(x\)축이 서로 다른 두 점에서 만날 때, 정수 \(k\)의 최솟값은?
"""
        ),
        "choices": ["① -7", "② -6", "③ -5", "④ -4", "⑤ -3"],
    },
    "SY-2025-G1-S1-MID-006": {
        "q": s(
            r"""
등식
\[
x^2+3x+2=ax(x-1)+b(x-1)+c
\]
가 \(x\)의 값에 관계없이 항상 성립할 때, \(a-b+c\)의 값은?
"""
        ),
        "choices": ["① 0", "② 1", "③ 2", "④ 3", "⑤ 4"],
    },
    "SY-2025-G1-S1-MID-007": {
        "q": s(
            r"""
이차방정식
\[
kx^2-2(k-2)x+k-2=0
\]
이 서로 다른 두 실근을 갖도록 하는 정수 \(k\)의 최댓값은?
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "SY-2025-G1-S1-MID-008": {
        "q": s(
            r"""
실수 \(x\)에 대하여 등식
\[
(x^2+x-1)^5=c_0+c_1x+c_2x^2+\cdots+c_{10}x^{10}
\]
이 성립할 때,
\[
c_0+c_2+c_4+\cdots+c_{10}
\]
의 값은?
"""
        ),
        "choices": ["① -10", "② 0", "③ 10", "④ 20", "⑤ 30"],
    },
    "SY-2025-G1-S1-MID-009": {
        "q": s(
            r"""
다음 값은?
\[
\frac{2025^3-1}{2025^2-1}-\frac{1}{2026}-1
\]
"""
        ),
        "choices": ["① 2021", "② 2022", "③ 2023", "④ 2024", "⑤ 2025"],
    },
    "SY-2025-G1-S1-MID-010": {
        "q": s(
            r"""
다음 값은?
\[
\sqrt{-3}\left(\sqrt{-27}+\frac{\sqrt{-4}}{\sqrt{3}}\right)
\]
"""
        ),
        "choices": ["① -11", "② -1", "③ 1", "④ 11", "⑤ 13"],
    },
    "SY-2025-G1-S1-MID-011": {
        "q": s(
            r"""
다항식 \(ax^4+bx^3+8\)이 \(x^2-3x+2\)로 나누어떨어질 때, 실수 \(a,\ b\)에 대하여 \(a-b\)의 값은?
"""
        ),
        "choices": ["① -22", "② -12", "③ 2", "④ 12", "⑤ 22"],
    },
    "SY-2025-G1-S1-MID-012": {
        "q": s(
            r"""
유리수 \(m,\ n\)에 대하여 이차함수 \(y=x^2+mx+4\)의 그래프와 직선 \(y=-3x+n\)이 서로 다른 두 점에서 만나고, 두 교점 중 한 교점의 \(x\)좌표가 \(3-\sqrt{3}\)이다. 이때 \(mn\)의 값은?
"""
        ),
        "choices": ["① 15", "② 18", "③ 21", "④ 24", "⑤ 27"],
    },
    "SY-2025-G1-S1-MID-013": {
        "q": s(
            r"""
이차방정식 \(x^2+2x-2=0\)의 두 근을 \(\alpha,\ \beta\)라 하자. 두 수
\[
\frac{1}{2\alpha^2+6\alpha-1},\qquad \frac{1}{2\beta^2+6\beta-1}
\]
을 근으로 하고 \(x^2\)의 계수가 \(1\)인 이차방정식을 \(f(x)=0\)이라 할 때, \(f(1)\)의 값은?
"""
        ),
        "choices": [
            r"① \(\frac{8}{11}\)",
            r"② \(\frac{9}{11}\)",
            r"③ \(\frac{10}{11}\)",
            r"④ \(1\)",
            r"⑤ \(\frac{12}{11}\)",
        ],
    },
    "SY-2025-G1-S1-MID-014": {
        "q": s(
            r"""
이차함수
\[
y=x^2-2(a+k)x+k^2-4k-b
\]
의 그래프가 실수 \(k\)의 값에 관계없이 항상 \(x\)축에 접할 때, 상수 \(a,\ b\)에 대하여 \(a+b\)의 값은?
"""
        ),
        "choices": ["① -6", "② -3", "③ 0", "④ 3", "⑤ 6"],
    },
    "SY-2025-G1-S1-MID-015": {
        "q": s(
            rf"""
오른쪽 그림과 같이 \(x\)축 위의 두 점 \(A,\ B\)와 이차함수 \(y=-x^2+6x\)의 그래프 위의 두 점 \(C,\ D\)를 네 꼭짓점으로 하는 직사각형 \(ABCD\)의 둘레의 길이의 최댓값은?

{IMAGE_TAG}
"""
        ),
        "choices": ["① 8", "② 16", "③ 20", "④ 28", "⑤ 36"],
    },
    "SY-2025-G1-S1-MID-016": {
        "q": s(
            r"""
삼차식 \(f(x)\)에 대하여 다항식 \(f(x)+8\)이 \((x+2)^2\)으로 나누어떨어지고, 다항식 \(10-f(x)\)가 \(x^2-1\)로 나누어떨어진다. \(f(x)\)를 \(x+3\)으로 나누었을 때의 나머지는?
"""
        ),
        "choices": ["① 10", "② 16", "③ 22", "④ 26", "⑤ 34"],
    },
    "SY-2025-G1-S1-MID-017": {
        "q": s(
            r"""
삼각형의 세 변의 길이 \(a,\ b,\ c\)에 대하여
\[
a^3-c^3+a^2c-ac^2+b^2(a+c)=0
\]
이 성립한다. 이 삼각형의 넓이가 \(15\)일 때, \(ab\)의 값은?
"""
        ),
        "choices": ["① 15", "② 20", "③ 30", "④ 40", "⑤ 45"],
    },
    "SY-2025-G1-S1-MID-018": {
        "q": s(
            r"""
실수 \(p\)에 대하여 이차방정식
\[
x^2-px+p+19=0
\]
이 서로 다른 두 허근을 갖는다. 한 허근의 허수부분이 \(2\)일 때, 음의 실수 \(p\)의 값은?
"""
        ),
        "choices": ["① -12", "② -6", "③ -4", "④ -2", "⑤ -1"],
    },
    "SY-2025-G1-S1-MID-019": {
        "q": s(
            r"""
등식
\[
\frac{1}{i}-\frac{1}{i^2}+\frac{1}{i^3}-\cdots+\frac{(-1)^{n+1}}{i^n}=1
\]
이 성립하도록 하는 \(100\) 이하의 자연수 \(n\)의 개수는?
"""
        ),
        "choices": ["① 23", "② 24", "③ 25", "④ 26", "⑤ 27"],
    },
    "SY-2025-G1-S1-MID-020": {
        "q": s(
            r"""
부피가
\[
\pi(x^3+7x^2+16x+12)
\]
이고 겉넓이가
\[
2\pi(x+a)(bx+5)
\]
인 원기둥이 있다. 이 원기둥의 높이와 밑면의 반지름의 길이가 각각 계수가 \(1\)인 일차식일 때, 상수 \(a,\ b\)에 대하여 \(2a+b\)의 값은?
"""
        ),
        "choices": ["① 2", "② 3", "③ 4", "④ 5", "⑤ 6"],
    },
    "SY-2025-G1-S1-MID-101": {
        "q": s(
            r"""
방정식
\[
3x^2+8x+a=0
\]
의 두 실근의 차가 \(\frac{10}{3}\)일 때, 실수 \(a\)의 값을 구하시오.
"""
        ),
        "choices": [],
    },
    "SY-2025-G1-S1-MID-102": {
        "q": s(
            r"""
최고차항의 계수가 양수인 다항식 \(P(x)\)가 모든 실수 \(x\)에 대하여
\[
\{P(x)\}^2=-P(x)+4x^4-4x^3+11x^2-5x+6
\]
을 만족시킬 때, \(P(x)\)를 구하시오.
"""
        ),
        "choices": [],
    },
    "SY-2025-G1-S1-MID-103": {
        "q": s(
            r"""
함수 \(y=-x^2+5x-3\)이 구간 \([a,4]\)에서 최댓값이 \(3\), 최솟값이 \(b\)일 때, \(a,\ b\)의 값을 각각 구하시오.
"""
        ),
        "choices": [],
    },
    "SY-2025-G1-S1-MID-104": {
        "q": s(
            r"""
어느 상품의 가격과 하루 판매량이 각각
\[
5000-100x,\qquad 100+10x
\]
로 주어진다. \(x\)일 후의 하루 판매 금액을 \(f(x)\)라 할 때, 다음을 구하시오. (단, \(0\le x\le 30\))

(1) \(f(x)\)

(2) \(f(x)\)의 최댓값과 최솟값
"""
        ),
        "choices": [],
    },
    "SY-2025-G1-S1-MID-105": {
        "q": s(
            r"""
다항식
\[
x^7+ax^6+bx^5
\]
를 \((x-2)^2\)로 나눈 나머지가 \(32(x-2)\)일 때, \(b-a\)의 값을 구하시오.
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
