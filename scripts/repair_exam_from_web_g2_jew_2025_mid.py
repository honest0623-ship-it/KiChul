from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"
IMAGE_TAG = '<img src="assets/scan.png" alt="문항 도형" style="width:100% !important; max-width:100% !important; height:auto;" />'


def s(text: str) -> str:
    return text.strip()


DATA = {
    "JEW-2025-G2-S1-MID-002": {
        "use_scan": False,
        "q": s(
            r"""
\[
\log_2(4\sqrt{5})+\log_{\sqrt{2}}(\sqrt{10})-\frac{3}{2}\log_2 5
\]
의 값은?
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "JEW-2025-G2-S1-MID-003": {
        "use_scan": False,
        "q": s(
            r"""
\[
\log 761=2.8814
\]
일 때, 다음 중 옳지 않은 것은?
"""
        ),
        "choices": [
            r"① \(\log 76.1=1.8814\)",
            r"② \(\log 7610=3.8814\)",
            r"③ \(\log 7.61=0.8814\)",
            r"④ \(\log 0.0761=-2.1186\)",
            r"⑤ \(\log 0.000761=-4+0.8814\)",
        ],
    },
    "JEW-2025-G2-S1-MID-004": {
        "use_scan": False,
        "q": s(
            r"""
둘레의 길이가 \(14\)인 부채꼴의 중심각의 크기가 \(\dfrac{1}{3}\)일 때, 호의 길이로 적절한 것은?
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "JEW-2025-G2-S1-MID-005": {
        "use_scan": False,
        "q": s(
            r"""
각 \(\theta\)가 제3사분면의 각이고 \(\cos\theta=-\dfrac{1}{\sqrt{5}}\)일 때,
\[
\sqrt{5}\sin\theta+\tan\theta
\]
의 값은?
"""
        ),
        "choices": ["① 0", "② -1", "③ 1", "④ -2", "⑤ 2"],
    },
    "JEW-2025-G2-S1-MID-006": {
        "use_scan": False,
        "q": s(
            r"""
\(2\) 이상의 자연수 \(n\)에 대하여 \(n-5\)의 \(n\)제곱근 중 실수인 것의 개수를 \(f(n)\)이라 하자. 이때
\[
f(2)+f(3)+f(4)+f(5)+f(6)+f(7)+f(8)
\]
의 값은?
"""
        ),
        "choices": ["① 4", "② 5", "③ 6", "④ 7", "⑤ 8"],
    },
    "JEW-2025-G2-S1-MID-007": {
        "use_scan": False,
        "q": s(
            r"""
다음 보기 중 옳은 것을 모두 고르면?

ㄱ. \(2^{\log_2 1+\log_2 2+\log_2 4}=7\)

ㄴ. \(\log_3(3\cdot 3^2\cdot 3^3\cdot 3^4)=10\)

ㄷ. \(\log\left(1-\dfrac12\right)+\log\left(1-\dfrac13\right)+\log\left(1-\dfrac14\right)+\cdots+\log\left(1-\dfrac1{10}\right)=-1\)
"""
        ),
        "choices": ["① ㄱ", "② ㄴ", "③ ㄷ", "④ ㄱ, ㄷ", "⑤ ㄴ, ㄷ"],
    },
    "JEW-2025-G2-S1-MID-008": {
        "use_scan": False,
        "q": s(
            r"""
\(x\)에 대한 이차방정식
\[
x^2-2ax-a^2=0
\]
의 두 근이 \(\sin\theta,\ \cos\theta\)일 때, 양수 \(a\)의 값은?
"""
        ),
        "choices": [
            r"① \(\dfrac{\sqrt5}{5}\)",
            r"② \(\dfrac{1}{\sqrt5}\)",
            r"③ \(\dfrac{\sqrt6}{6}\)",
            r"④ \(\dfrac{\sqrt7}{7}\)",
            r"⑤ \(\dfrac{\sqrt8}{8}\)",
        ],
    },
    "JEW-2025-G2-S1-MID-009": {
        "use_scan": False,
        "q": s(
            r"""
함수 \(y=a^x\,(a>0,\ a\ne1)\)의 그래프를 \(y\)축 대칭한 후, \(x\)축의 방향으로 \(m\)만큼, \(y\)축의 방향으로 \(n\)만큼 평행이동하면 함수
\[
y=4\left(\frac12\right)^x+3
\]
의 그래프와 일치한다. 이때 \(a+m+n\)의 값은? (단, \(a,\ m,\ n\)은 상수이다.)
"""
        ),
        "choices": ["① 9", "② 7", "③ 5", "④ 3", "⑤ 1"],
    },
    "JEW-2025-G2-S1-MID-010": {
        "use_scan": False,
        "q": s(
            r"""
다음 중 함수
\[
y=3^{x-2}-2
\]
의 설명으로 옳지 않은 것은?
"""
        ),
        "choices": [
            "① 정의역은 실수 전체이다.",
            r"② 치역은 \(\{y\mid y>-2\}\)인 모든 실수이다.",
            r"③ 점근선은 \(y=-2\)이다.",
            r"④ 이 함수는 \(y=\log_3(x+2)+2\)와 역함수 관계이다.",
            r"⑤ 정의역 \(\{x\mid 2\le x\le 4\}\)에서 최솟값은 \(-2\)이다.",
        ],
    },
    "JEW-2025-G2-S1-MID-011": {
        "use_scan": False,
        "q": s(
            r"""
부등식
\[
\left(\frac14\right)^{2x}\ge\left(\frac12\right)^{2x+6}
\]
을 만족하는 자연수 \(x\)의 개수는?
"""
        ),
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "JEW-2025-G2-S1-MID-012": {
        "use_scan": False,
        "q": s(
            r"""
양수 \(x,\ y\)가
\[
5^{2x}=k,\qquad 64^y=k
\]
를 만족시킬 때,
\[
\frac{1}{x}+\frac{1}{3y}=2
\]
가 성립한다. 상수 \(k\)의 값은?
"""
        ),
        "choices": ["① 10", "② 15", "③ 20", "④ 25", "⑤ 30"],
    },
    "JEW-2025-G2-S1-MID-013": {
        "use_scan": False,
        "q": s(
            r"""
다음 방정식
\[
\log_3(x-3)+\log_3(x+5)=2
\]
를 만족하는 실수 \(x\)의 값은?
"""
        ),
        "choices": ["① 2", "② 4", "③ 6", "④ 8", "⑤ 10"],
    },
    "JEW-2025-G2-S1-MID-014": {
        "use_scan": False,
        "q": s(
            r"""
다음 부등식
\[
\log_{\frac12}(x-2)+\log_{\frac12}(x-3)>-1
\]
을 만족하는 실수 \(x\)의 값의 범위를 \(\alpha<x<\beta\)라 할 때, \(\alpha+\beta\)의 값은?
"""
        ),
        "choices": ["① 5", "② 7", "③ 9", "④ 11", "⑤ 13"],
    },
    "JEW-2025-G2-S1-MID-015": {
        "use_scan": False,
        "q": s(
            r"""
\[
\frac{\cos\theta}{1+\sin\theta}+\tan\theta=5
\]
일 때, \(\cos\theta\)의 값은?
"""
        ),
        "choices": [
            r"① \(\dfrac15\)",
            r"② \(\dfrac25\)",
            r"③ \(\dfrac35\)",
            r"④ \(\dfrac45\)",
            r"⑤ \(1\)",
        ],
    },
    "JEW-2025-G2-S1-MID-016": {
        "use_scan": False,
        "q": s(
            r"""
어느 공장의 생산 라인을 시험 가동해 보니 초기 불량률이 \(12.8\%\)이었다. 매달 불량률이 절반으로 감소한다고 할 때, 이 생산 라인의 불량률이 \(0.1\%\)가 되는 것은 가동을 시작한 때로부터 몇 개월 후인가?
"""
        ),
        "choices": ["① 4", "② 5", "③ 6", "④ 7", "⑤ 8"],
    },
    "JEW-2025-G2-S1-MID-017": {
        "use_scan": True,
        "q": s(
            rf"""
오른쪽 그림과 같이 두 곡선 \(y=\log_2 x\)와 \(y=\log_{{\frac14}}x\)가 만나는 점을 \(P\), 직선 \(x=k\,(k>1)\)가 두 곡선과 만나는 점을 각각 \(A,\ B\)라 하자. \(\triangle PAB\)의 넓이가 \(45\)일 때, 정수 \(k\)의 값은?

{IMAGE_TAG}
"""
        ),
        "choices": ["① 14", "② 15", "③ 16", "④ 17", "⑤ 18"],
    },
    "JEW-2025-G2-S1-MID-101": {
        "use_scan": False,
        "q": s(
            r"""
다음 식을 간단히 하여
\[
x^{\frac56}\times\sqrt[3]{{y^4}}\times\sqrt[6]{y}\div x^{-\frac23}\times x^{\frac32}\div\sqrt{y}=x^a y^b
\]
로 나타낼 때, 다음 물음에 답하시오.

(1) 실수 \(a\)의 값

(2) 실수 \(b\)의 값
"""
        ),
        "choices": [],
    },
    "JEW-2025-G2-S1-MID-102": {
        "use_scan": False,
        "q": s(
            r"""
함수
\[
y=\log_{\frac14}(x^2-ax+b)
\]
는 \(x=2\)일 때 최댓값 \(-2\)를 갖는다. 다음 물음에 답하시오.

(1) 실수 \(a\)의 값

(2) 실수 \(b\)의 값
"""
        ),
        "choices": [],
    },
    "JEW-2025-G2-S1-MID-103": {
        "use_scan": False,
        "q": s(
            r"""
다음은 \(\sin\theta=\dfrac35\)일 때, \(\cos\theta\)의 값을 구하는 과정이다. 다음 물음에 답하시오.

\(\sin\theta>0\)이므로 각 \(\theta\)는 제1사분면의 각 또는 (가)의 각이다.

i) 각 \(\theta\)가 제1사분면의 각이면 \(\cos\theta=(\text{나})\)

ii) 각 \(\theta\)가 (가)의 각이면 \(\cos\theta=(\text{다})\)

따라서 \(\cos\theta=(\text{나})\) 또는 \(\cos\theta=(\text{다})\)

(1) (가)에 알맞은 각의 위치를 \(\alpha<\theta<\beta\)라 할 때, \(\alpha+\beta\)의 값

(2) (나)에 알맞은 실수

(3) (다)에 알맞은 실수
"""
        ),
        "choices": [],
    },
    "JEW-2025-G2-S1-MID-104": {
        "use_scan": False,
        "q": s(
            r"""
함수
\[
f(x)=\frac{9^x+9^{-x}}{2}
\]
의 역함수를 \(g(x)\)라 할 때, \(g\!\left(\dfrac52\right)=k\)라 하자. 이때
\[
\frac{3^{6k}+1}{3^{4k}+3^{2k}}
\]
의 값을 구하는 과정과 답을 쓰시오. (단, \(k\)는 실수이다.)
"""
        ),
        "choices": [],
    },
    "JEW-2025-G2-S1-MID-105": {
        "use_scan": False,
        "q": s(
            r"""
어떤 미생물의 개체 수는 매시간 \(r\%\)씩 일정하게 증가하여 \(n\)시간 후의 개체 수는 처음의 \(\left(1+\dfrac{r}{100}\right)^n\)배가 된다고 한다. 이 미생물의 개체 수가 매시간 \(40\%\)씩 일정하게 증가할 때, \(19\)시간 후의 개체 수는 처음의 약 몇 배가 되는지 구하는 과정과 답을 쓰시오.

(단, \(\log 1.4=0.1461,\ \log 5.97=0.7759\)로 계산한다.)
"""
        ),
        "choices": [],
    },
    "JEW-2025-G2-S1-MID-106": {
        "use_scan": False,
        "q": s(
            r"""
다음 이차방정식
\[
x^2-4x-9=0
\]
의 두 근이 \(\log_2 a,\ \log_2 b\)일 때,
\[
\log_a b-\log_b a=\frac{n\sqrt{13}}{m}
\]
이다. 이때 \(m\times n\)의 값을 구하는 과정과 답을 쓰시오.

(단, \(a,\ b,\ m,\ n\)은 실수이고 \(b>a\)이다.)
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
