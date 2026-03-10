from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_ROOT = ROOT / "db" / "problems"


DATA: dict[str, dict[str, object]] = {
    "JEW-2023-G1-S1-MID-005": {
        "q": r"""\(\sqrt{-5}\sqrt{-5}+\sqrt{7}\sqrt{-7}+\frac{\sqrt{12}}{\sqrt{-3}}=a+bi\)일 때, 실수 \(a,\ b\)에 대하여 \(b-a\)의 값은?""",
        "choices": ["① 6", "② 8", "③ 10", "④ 12", "⑤ 14"],
    },
    "JEW-2023-G1-S1-MID-011": {
        "q": r"""연립방정식
\[
\begin{cases}
x+y=k \\
x^2+y^2=4
\end{cases}
\]
가 오직 한 쌍의 해를 갖도록 하는 양수 \(k\)의 값은?""",
        "choices": [r"① 1", r"② \(\sqrt{2}\)", r"③ \(\sqrt{3}\)", r"④ 2", r"⑤ \(2\sqrt{2}\)"],
    },
    "JEW-2023-G1-S1-MID-014": {
        "q": r"""이차방정식 \(ax^2+2ax-20=0\)의 한 근이 이차방정식 \(x^2-3x+2=0\)의 두 근 사이에 존재하도록 하는 모든 자연수 \(a\)의 값의 합은?""",
        "choices": ["① 12", "② 15", "③ 18", "④ 20", "⑤ 25"],
    },
    "JEW-2023-G1-S1-MID-015": {
        "q": r"""두 다항식 \(A(x),\ B(x)\)에 대하여 \(A(x)\)를 \(x^2-1\)로 나눈 몫이 \(Q_1(x)\), 나머지가 \(2x+3\)이고, \(B(x)\)를 \(2(x^2-1)\)로 나눈 몫이 \(Q_2(x)\), 나머지가 \(x-2\)일 때, 두 다항식의 곱 \(A(x)B(x)\)를 \(x^2-1\)로 나눈 나머지를 \(R(x)\)라 할 때, \(R(-5)\)의 값은?""",
        "choices": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
    },
    "JEW-2023-G1-S1-MID-016": {
        "q": r"""\[
\left(\frac{\sqrt{2}}{1+i}\right)^n+\left(\frac{-1+\sqrt{3}i}{2}\right)^n=2
\]
를 만족시키는 자연수 \(n\)의 최솟값은? (단, \(i=\sqrt{-1}\))""",
        "choices": ["① 6", "② 12", "③ 15", "④ 18", "⑤ 24"],
    },
    "JEW-2023-G1-S1-MID-103": {
        "q": r"""\(x\ne 0,\ 1,\ -1\)인 복소수 \(x\)에 대하여
\[
x^3-\frac{1}{x^3}=0
\]
이 성립한다. 이때 \(x^4+x^2+3\)의 값을 구하시오.""",
        "choices": [],
    },
    "JEW-2023-G1-S1-MID-104": {
        "q": r"""\(1\le x\le 2\)에서 이차함수 \(y=x^2-2ax+a^2+b\)의 최솟값이 \(4\)가 되도록 하는 두 실수 \(a,\ b\)에 대하여 \(2a+b\)의 최댓값을 구하시오.""",
        "choices": [],
    },
    "JEW-2023-G1-S1-MID-106": {
        "q": r"""은지와 주아가 이차방정식 \(x^2+ax+b=0\) (\(a,\ b\)는 실수)의 근을 구하려고 한다. 그런데 은지는 상수항을 잘못 보고 풀어 두 근 \(4+i,\ 4-i\)를 얻었고, 주아는 \(x\)의 계수를 잘못 보고 풀어 두 근 \(3+\sqrt{3}i,\ 3-\sqrt{3}i\)를 얻었다. 다음 물음에 답하시오.

1. 은지가 구한 두 수를 근으로 하는 이차방정식을 구하시오.
2. 주아가 구한 두 수를 근으로 하는 이차방정식을 구하시오.
3. 이차방정식 \(x^2+ax+b=0\)의 두 근을 바르게 구하시오.""",
        "choices": [],
    },
    "JEW-2024-G1-S1-MID-008": {
        "q": r"""다항식 \(256x^8-1\)을 \((2x-1)^2\)으로 나누었을 때의 나머지를 \(R(x)\)라고 할 때, \(R(10)\)의 값은?""",
        "choices": ["① 149", "② 150", "③ 151", "④ 152", "⑤ 153"],
    },
    "JEW-2024-G1-S1-MID-009": {
        "q": r"""\(n^4-63n^2+49\)의 값이 소수가 되도록 하는 자연수 \(n\)의 값을 \(a\), 그때의 소수를 \(p\)라 할 때, \(a+p\)의 값은?""",
        "choices": ["① 117", "② 118", "③ 119", "④ 120", "⑤ 121"],
    },
    "JEW-2024-G1-S1-MID-010": {
        "q": r"""실수 \(a,\ b\)에 대하여 \(a>0,\ b<0\)일 때, 다음 보기의 설명 중 옳은 것을 모두 고른 것은?

<보기>

ㄱ. \(\sqrt{(-2)^2}+\sqrt{-3}\sqrt{-4}=2+2\sqrt{3}\)
ㄴ. \(\sqrt{a}\sqrt{b}=\sqrt{ab}i\)
ㄷ. \(\sqrt{-a}\sqrt{-b}=-\sqrt{ab}\)
ㄹ. \(\frac{\sqrt{a}}{\sqrt{b}}=-\sqrt{\frac{a}{b}}\)""",
        "choices": ["① ㄱ", "② ㄴ, ㄷ", "③ ㄹ", "④ ㄴ, ㄹ", "⑤ ㄷ, ㄹ"],
    },
    "JEW-2024-G1-S1-MID-012": {
        "q": r"""이차함수 \(y=x^2-2kx+k+2\)의 그래프는 \(x\)축과 한 점에서 만나고, 이차함수 \(y=-x^2+x+k\)의 그래프는 \(x\)축과 만나지 않도록 하는 실수 \(k\)의 값은?""",
        "choices": [r"① \(-2\)", r"② \(-1\)", "③ 0", "④ 1", "⑤ 2"],
    },
    "JEW-2024-G1-S1-MID-013": {
        "q": r"""이차함수 \(f(x)=x^2+ax+b\)가 다음 조건을 모두 만족시킬 때, \(-1\le x\le 4\)에서의 \(f(x)\)의 최댓값은? (단, \(a,\ b\)는 상수이다.)

(가) \(f(-2)=f(4)\)
(나) 함수 \(f(x)\)의 최솟값은 \(-3\)이다.""",
        "choices": ["① 0", "② 2", "③ 4", "④ 6", "⑤ 8"],
    },
    "JEW-2024-G1-S1-MID-014": {
        "q": r"""다음 방정식 \(x^4-3x^3+x^2-x-6=0\)의 두 허근의 합을 \(m\), 두 허근의 곱을 \(n\)이라 할 때, \(mn\)의 값은?""",
        "choices": [r"① \(-2\)", r"② \(-1\)", "③ 0", "④ 1", "⑤ 2"],
    },
    "JEW-2024-G1-S1-MID-016": {
        "q": r"""삼차방정식 \(x^3-4x^2+6x-4=0\)의 한 허근을 \(w\)라 할 때,
\[
\left\{w(\overline{w}-1)\right\}^n=256
\]
을 만족시키는 자연수 \(n\)의 값은? (단, \(\overline{w}\)는 \(w\)의 켤레복소수이다.)""",
        "choices": ["① 4", "② 9", "③ 16", "④ 25", "⑤ 36"],
    },
    "JEW-2024-G1-S1-MID-103": {
        "q": r"""다음은 이차방정식 \(x^2-px+q=0\)의 두 근이 \(\alpha,\ \beta\)일 때, 다음 조건을 모두 만족시키는 실수 \(p,\ q\)의 값을 구하는 과정이다. 다음 물음에 답하여라.

(가) \(\alpha,\ \beta,\ p,\ q\)는 \(50\) 이하의 서로 다른 자연수이다.
(나) \(\alpha,\ \beta\)는 각각 \(3\)개의 약수를 갖는다.

먼저 \(\alpha,\ \beta\)는 조건 (가), (나)에 의하여 \(3\)개의 약수를 가지는 \(50\) 이하의 서로 다른 자연수이므로 \(\alpha,\ \beta\)가 될 수 있는 수는 ①, ②, \(25\), \(49\)뿐이다. 한편, 이차방정식 \(x^2-px+q=0\)의 두 근이 \(\alpha,\ \beta\)이고 근과 계수의 관계와 조건 (가)에 의해 \(p=\)③, \(q=\)④이다.

1. ①에 들어갈 자연수를 쓰시오.
2. ②에 들어갈 자연수를 쓰시오.
3. ③에 알맞은 \(p\)의 값을 쓰시오.
4. ④에 알맞은 \(q\)의 값을 쓰시오.""",
        "choices": [],
    },
}


Q_PATTERN = re.compile(r"(?ms)^## Q\n.*?(?=^## Choices\n)")
CHOICES_PATTERN = re.compile(r"(?ms)^## Choices\n.*?(?=^## Answer\n)")


def rewrite_problem(pid: str, payload: dict[str, object]) -> None:
    path = PROBLEMS_ROOT / pid / "problem.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("- assets/scan.png\n", "")

    q = str(payload["q"]).strip()
    choices = "\n".join(payload["choices"]).strip()

    text = Q_PATTERN.sub(lambda _m: f"## Q\n{q}\n\n", text)
    if choices:
        text = CHOICES_PATTERN.sub(lambda _m: f"## Choices\n{choices}\n\n", text)
    else:
        text = CHOICES_PATTERN.sub(lambda _m: "## Choices\n\n", text)

    if '<img src="assets/scan.png"' in text:
        raise RuntimeError(f"{pid}: image reference still present after rewrite")

    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for pid, payload in DATA.items():
        rewrite_problem(pid, payload)
        print(f"updated {pid}")


if __name__ == "__main__":
    main()
