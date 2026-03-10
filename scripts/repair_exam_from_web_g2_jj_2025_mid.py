from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"
IMAGE_TAG = '<img src="assets/scan.png" alt="문항 도형" style="width:100% !important; max-width:100% !important; height:auto;" />'


def s(text: str) -> str:
    return text.strip()


DATA = {
    "JJ-2025-G2-S1-MID-002": {
        "use_scan": False,
        "q": s(
            r"""
\[
3^{2-\sqrt{2}}\times 3^{2+\sqrt{2}}
\]
의 값은?
"""
        ),
        "choices": ["① 81", "② 27", "③ 9", "④ 3", "⑤ 1"],
    },
    "JJ-2025-G2-S1-MID-003": {
        "use_scan": False,
        "q": s(
            r"""
\[
a=\log 15.7,\qquad b=\log 0.0244
\]
일 때, \(a-b\)의 값은? (단, \(\log 1.57=0.1959,\ \log 2.44=0.3874\)로 계산한다.)
"""
        ),
        "choices": ["① -1.6126", "② -1.4167", "③ 0.7792", "④ 1.1915", "⑤ 2.8085"],
    },
    "JJ-2025-G2-S1-MID-004": {
        "use_scan": False,
        "q": s(
            r"""
\[
\sin\theta\cos\theta<0,\qquad \sin\theta\tan\theta>0
\]
를 만족시키는 각 \(\theta\)는 제 몇 사분면의 각인가?
"""
        ),
        "choices": ["① 제1사분면", "② 제2사분면", "③ 제3사분면", "④ 제4사분면", "⑤ 없음"],
    },
    "JJ-2025-G2-S1-MID-005": {
        "use_scan": False,
        "q": s(
            r"""
다음 함수의 그래프 중에서 함수 \(y=3^x\)의 그래프를 평행이동하거나 대칭이동하여 포갤 수 없는 것은?
"""
        ),
        "choices": [
            r"① \(y=3^{-x}\)",
            r"② \(y=3^x+2\)",
            r"③ \(y=\log_3\sqrt{x}\)",
            r"④ \(y=\log_3(x-2)\)",
            r"⑤ \(y=-\log_3 x\)",
        ],
    },
    "JJ-2025-G2-S1-MID-006": {
        "use_scan": False,
        "q": s(
            r"""
다음 <보기>의 각 중에서 각 \(-420^\circ\)와 같은 사분면에 속하는 각을 고른 것은?

ㄱ. \(\dfrac{4\pi}{3}\)

ㄴ. \(-\dfrac{9\pi}{4}\)

ㄷ. \(300^\circ\)
"""
        ),
        "choices": ["① ㄱ", "② ㄴ", "③ ㄷ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"],
    },
    "JJ-2025-G2-S1-MID-007": {
        "use_scan": False,
        "q": s(
            r"""
다음 중에서 옳은 것은?
"""
        ),
        "choices": [
            r"① \(0\)의 세제곱근은 없다.",
            r"② \(-64\)의 세제곱근 중에서 실수인 것은 \(2\)개다.",
            r"③ \(n\)이 홀수일 때, \(2\)의 \(n\)제곱근 중에서 실수인 것은 하나뿐이다.",
            r"④ \(n\)이 짝수일 때, \(-1\)의 \(n\)제곱근 중에서 실수인 것은 \(2\)개다.",
            r"⑤ \(5\)의 네제곱근 중에서 실수인 것은 \(\sqrt5\)뿐이다.",
        ],
    },
    "JJ-2025-G2-S1-MID-008": {
        "use_scan": True,
        "q": s(
            r"""
다음 그림은 함수
\[
y=-\left(\frac12\right)^{{x+a}}+b
\]
의 그래프이다. 상수 \(a,\ b\)에 대하여 \(a+b\)의 값은?
"""
            + "\n\n"
            + IMAGE_TAG
        ),
        "choices": ["① -3", "② -1", "③ 1", "④ 3", "⑤ 5"],
    },
    "JJ-2025-G2-S1-MID-009": {
        "use_scan": False,
        "q": s(
            r"""
다음 중 함수
\[
y=\log_3(-x+1)-2
\]
에 대한 설명으로 옳지 않은 것은?
"""
        ),
        "choices": [
            r"① 그래프는 점 \((0,-2)\)를 지난다.",
            r"② 그래프의 점근선은 직선 \(x=1\)이다.",
            r"③ \(x\)의 값이 증가하면 \(y\)의 값은 감소한다.",
            r"④ 정의역은 \(\{x\mid x<1\}\)이다.",
            r"⑤ 치역은 \(\{y\mid y<-2\}\)이다.",
        ],
    },
    "JJ-2025-G2-S1-MID-010": {
        "use_scan": False,
        "q": s(
            r"""
다음은 \(a>0,\ a\ne1,\ M>0\)일 때
\[
\log_a(M^k)=k\log_a M
\]
이 성립함을 보이는 과정이다. (가), (나), (다)에 알맞은 것을 차례대로 나열한 것은?

\[
\log_a M=m
\]
으로 놓으면
\[
M=(\text{가})
\]
이므로 지수법칙에 의하여
\[
M^k=(\text{나})
\]
이다. 따라서 로그의 정의에 의하여
\[
\log_a(\text{다})=mk=k\log_a M
\]
이다.
"""
        ),
        "choices": [
            r"① \((\text{가})=kM,\ (\text{나})=a^{mk},\ (\text{다})=kM\)",
            r"② \((\text{가})=a^{mk},\ (\text{나})=kM,\ (\text{다})=M^k\)",
            r"③ \((\text{가})=a^m,\ (\text{나})=M^k,\ (\text{다})=a^{mk}\)",
            r"④ \((\text{가})=a^m,\ (\text{나})=a^{mk},\ (\text{다})=M^k\)",
            r"⑤ \((\text{가})=M^k,\ (\text{나})=a^m,\ (\text{다})=a^{mk}\)",
        ],
    },
    "JJ-2025-G2-S1-MID-011": {
        "use_scan": False,
        "q": s(
            r"""
\(x,\ y,\ z\)는 실수이고 \(a\)가 \(1\)이 아닌 양수라 하자.
\[
2^x=5^y=a^z,\qquad \frac1z=\frac1x+\frac1y
\]
를 만족시킬 때, \(a\)의 값은?
"""
        ),
        "choices": ["① 10", "② 5", "③ \(\dfrac52\)", "④ 2", "⑤ \(\dfrac25\)"],
    },
    "JJ-2025-G2-S1-MID-013": {
        "use_scan": True,
        "q": s(
            r"""
다음 그림과 같이 중심각의 크기가 \(\dfrac{\pi}{6}\)인 부채꼴 \(OAB\)가 있다. 선분 \(OA\) 위의 점 \(P\)에 대하여 선분 \(PA\)를 지름으로 하고 선분 \(OB\)에 접하는 반원을 \(C\)라 하자. 부채꼴 \(OAB\)의 넓이를 \(S_1\), 반원 \(C\)의 넓이를 \(S_2\)라 할 때,
\[
S_1-S_2=16\pi
\]
이다. 이때 부채꼴 \(OAB\)의 호 \(AB\)의 길이는?
"""
            + "\n\n"
            + IMAGE_TAG
        ),
        "choices": [r"① \(2\pi\)", r"② \(4\pi\)", r"③ \(6\pi\)", r"④ \(8\pi\)", r"⑤ \(10\pi\)"],
    },
    "JJ-2025-G2-S1-MID-014": {
        "use_scan": False,
        "q": s(
            r"""
함수
\[
f(x)=\log_a(bx+c)+d
\]
가
\[
f(10)=10,\qquad f(100)=100
\]
을 만족시키는 두 실수 \(p,\ q\)에 대하여 \(f(p)=q\)라 하자. (단, \(0<a<1\)이고 \(a,\ b,\ c,\ d,\ p,\ q\)는 실수이다.)

옳은 것만을 <보기>에서 있는 대로 고른 것은?

ㄱ. \(\dfrac{c}{b}<0\)

ㄴ. \(ca^d<1\)

ㄷ. \(q<p\)
"""
        ),
        "choices": ["① ㄱ", "② ㄴ", "③ ㄱ, ㄴ", "④ ㄱ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"],
    },
    "JJ-2025-G2-S1-MID-101": {
        "use_scan": False,
        "q": s(
            r"""
\(\dfrac{\pi}{2}<\theta<\pi\)이고 \(\sin\theta=\dfrac35\)일 때,
\[
\frac{\cos\theta}{1+\sin\theta}-\tan\theta
\]
의 값을 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G2-S1-MID-102": {
        "use_scan": False,
        "q": s(
            r"""
반지름의 길이가 \(10\)인 원의 둘레를 \(10\)등분하여 \(10\)개의 합동인 부채꼴을 그리고, 그 중 \(4\)개를 잘라내고 남은 부분이 원뿔의 옆면이 되도록 원뿔을 만들었다. 이 원뿔의 부피를 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G2-S1-MID-103": {
        "use_scan": False,
        "q": s(
            r"""
\(1000\) 이하의 자연수 \(n\)에 대하여
\[
3\log_{81}\left(\frac{2^2}{(3n+15)^2}\right)
\]
의 값이 정수가 되도록 하는 \(n\)의 최댓값을 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G2-S1-MID-104": {
        "use_scan": False,
        "q": s(
            r"""
함수
\[
f(x)=\log_a x+m\qquad (a>1)
\]
의 그래프와 그 역함수의 그래프가 두 점에서 만나고, 이 두 점의 \(x\)좌표가 각각 \(1,\ 3\)일 때, \(am\)의 값을 구하시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G2-S1-MID-105": {
        "use_scan": False,
        "q": s(
            r"""
\(1\)이 아닌 네 양수 \(a,\ b,\ x,\ y\)가
\[
a^x=\left(\frac{b}{a}\right)^y
\]
를 만족시킬 때,
\[
\frac{y}{x+y}
\]
를 \(a,\ b\)로 나타내시오.
"""
        ),
        "choices": [],
    },
    "JJ-2025-G2-S1-MID-106": {
        "use_scan": False,
        "q": s(
            r"""
\[
\sqrt[4]{2^3}
\]
이 어떤 자연수의 \(n\)제곱근일 때, 자연수 \(n\)의 개수를 \(k\)라 하자.
\[
\frac{1}{2^{-k}+1}+\frac{1}{2^{-(k-2)}+1}+\cdots+\frac{1}{2^{k-2}+1}+\frac{1}{2^k+1}
\]
의 값을 구하시오. (단, \(2\le n\le 75,\ n\)은 자연수이다.)
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
    replacement = match.group(1) + (body + "\n\n" if body else "\n")
    return text[: match.start()] + replacement + text[match.end() :]


def set_scan_asset(text: str, use_scan: bool) -> str:
    has_scan_asset = "- assets/scan.png\n" in text
    if use_scan and not has_scan_asset:
        text = text.replace("assets:\n", "assets:\n- assets/scan.png\n", 1)
    if not use_scan and has_scan_asset:
        text = text.replace("- assets/scan.png\n", "", 1)
    return text


def update_problem(pid: str, item: dict[str, object]) -> None:
    path = PROBLEMS / pid / "problem.md"
    text = path.read_text(encoding="utf-8")
    text = set_scan_asset(text, bool(item["use_scan"]))
    text = replace_section(text, "Q", str(item["q"]))
    text = replace_section(text, "Choices", "\n".join(item["choices"]))
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for pid, item in DATA.items():
        update_problem(pid, item)
        print(f"updated\t{pid}")


if __name__ == "__main__":
    main()
