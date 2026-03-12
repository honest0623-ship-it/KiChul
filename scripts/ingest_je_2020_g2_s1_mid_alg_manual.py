from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import shutil
import sys

import fitz
from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unit_level_classifier import classify_unit_and_level

PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
REPORT = ROOT / "_tmp_je_2020_g2_s1_mid_alg_ingest_report.txt"

SOURCE_PDF = ORIGINAL / "JE.2020.G2.S1.MID.ALG.pdf"
SUPPLEMENT_SCANS: Dict[int, Path] = {
    13: ORIGINAL / "JE.2020.G2.S1.MID.ALG.013.png",
    105: ORIGINAL / "JE.2020.G2.S1.MID.ALG.105.png",
    106: ORIGINAL / "JE.2020.G2.S1.MID.ALG.106.png",
}

META = {
    "school": "JE",
    "year": 2020,
    "grade": 2,
    "semester": 1,
    "exam": "MID",
    "subject": "ALG",
    "source": "user_upload_2026-03-12",
    "created_date": "2026-03-12",
}


@dataclass
class Entry:
    qtype: str
    q: str
    choices: List[str]
    answer: str
    solution: str


def _objective(q: str, choices: List[str], answer: str, solution: str) -> Entry:
    return Entry(qtype="객관식", q=q, choices=choices, answer=answer, solution=solution)


def _subjective(q: str, answer: str, solution: str) -> Entry:
    return Entry(qtype="서술형", q=q, choices=[], answer=answer, solution=solution)


ENTRIES: Dict[int, Entry] = {
    1: _objective(
        q=r"1의 네제곱근 중 실수인 것은?",
        choices=[
            r"$-1$",
            r"$1$",
            r"$-1,\ 1$",
            r"$-1,\ 0,\ 1$",
            r"$-1,\ 0,\ 1,\ 2$",
        ],
        answer="③",
        solution=r"""방정식 \(x^4=1\)의 근은
\[
x=\pm1,\ \pm i
\]
이다. 이 중 실수는 \(-1,\ 1\)이다.""",
    ),
    2: _objective(
        q=r"다음 중 값이 다른 것 하나는?",
        choices=[
            r"$\sqrt[4]{16}$",
            r"$\sqrt[3]{\sqrt[4]{2^6}}$",
            r"방정식 \(x^2=4\)의 근",
            r"8의 세제곱근 중 실수",
            r"$\left(\sqrt[4]{3}-1\right)\left(\sqrt[4]{3}+1\right)\left(\sqrt3+1\right)$",
        ],
        answer="③",
        solution=r"""①, ④, ⑤는 모두 값이 \(2\)가 된다.
\[
\sqrt[4]{16}=2,\quad \sqrt[3]{8}=2
\]
\[
\left(\sqrt[4]{3}-1\right)\left(\sqrt[4]{3}+1\right)=\sqrt3-1,\ 
(\sqrt3-1)(\sqrt3+1)=2
\]

③은 방정식 \(x^2=4\)의 근 전체로 \(x=\pm2\)를 뜻하므로 다른 항과 성격이 다르다.""",
    ),
    3: _objective(
        q=r"""식
\[
\frac{\sqrt[3]{3}}{\sqrt[3]{81}}
\times\left(\sqrt[4]{9}\right)^2
\div\sqrt[4]{\sqrt{6^8}}
\]
을 간단히 한 것은?""",
        choices=[r"$\dfrac16$", r"$\dfrac13$", r"$2$", r"$3$", r"$6$"],
        answer="①",
        solution=r"""\[
\frac{\sqrt[3]{3}}{\sqrt[3]{81}}
=\frac{3^{1/3}}{3^{4/3}}=\frac13,\quad
\left(\sqrt[4]{9}\right)^2=3
\]
\[
\sqrt[4]{\sqrt{6^8}}
\;=\;(6^8)^{1/2\cdot1/4}=6
\]
따라서
\[
\frac13\times3\div6=\frac16
\]
이다.""",
    ),
    4: _objective(
        q=r"다음 중 틀린 것은?",
        choices=[
            r"$a\ne0$일 때, $a^0=1$",
            r"$a\ne0,\ b\ne0$일 때, $(ab)^{-2}=a^{-2}b^{-2}$",
            r"$a\ne0$일 때, $(a^2)^{-3/2}=a^{-3}$",
            r"$a>0,\ b>0$일 때, $a^{2/3}\times a^{-1/3}=a^{1/3}$",
            r"$a>0,\ b>0$일 때, $(a^{\sqrt2})^{\sqrt5}=a^{\sqrt{10}}$",
        ],
        answer="③",
        solution=r"""③에서
\[
(a^2)^{-3/2}=\frac{1}{(a^2)^{3/2}}=\frac{1}{|a|^3}
\]
이므로 일반적으로 \(a^{-3}\)와 같지 않다. (예: \(a<0\)일 때)
따라서 틀린 것은 ③이다.""",
    ),
    5: _objective(
        q=r"""<span style="color:red">[오류 문항]</span> ③과 ⑤가 동시에 거짓이므로 정답이 하나로 정해지지 않습니다.

다음 로그의 성질 중 틀린 것은?""",
        choices=[
            r"$\log_2 3+\log_2 5=\log_2 15$",
            r"$\log_2 3\cdot\log_5 2=\log_5 3$",
            r"$\log_2 21\div\log_2 7=\log_2 3$",
            r"$\log_8 27=\log_2 3$",
            r"$\log_4 25=\dfrac{\log_5 25}{\log_2 4}$",
        ],
        answer="문항 오류 (③, ⑤ 동시 오답)",
        solution=r"""③:
\[
\frac{\log_2 21}{\log_2 7}=\log_7 21\ne\log_2 3
\]
이므로 거짓이다.

⑤:
\[
\frac{\log_5 25}{\log_2 4}=\frac{2}{2}=1,\quad
\log_4 25\ne1
\]
이므로 거짓이다.

따라서 오답이 둘이라 문항 자체에 오류가 있다.""",
    ),
    6: _objective(
        q=r"""다음은 \(1\)이 아닌 세 양수 \(a,b,c\)에 대하여
\[
a^{\log_b c}=(\text{다})
\]
가 성립함을 보이는 과정이다. 물음에 답하여라.

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
\[
a^{\log_b c}=x\ \text{로 놓으면 로그의 정의에 따라}\ \log_a x=\log_b c
\]
\[
\text{양변을 각각 }c\text{를 밑으로 하는 로그로 나타내면}\ 
\frac{\log_c x}{\log_c a}=(\text{가})
\]
\[
\text{즉, }\log_c x=(\text{나})\ \text{이므로 로그의 정의에 따라}\ x=(\text{다})
\]
\[
\therefore\ a^{\log_b c}=(\text{다})
\]
</div>

빈칸에 들어갈 식 \((\text{가})\)와 \((\text{나})\)에 대하여
\[
f(a,b,c)=(\text{가})+(\text{나})
\]
라 할 때, \(f(2,4,8)\)의 값을 구하면?""",
        choices=[r"$\dfrac56$", r"$\dfrac76$", r"$\dfrac32$", r"$\dfrac{11}{6}$", r"$2$"],
        answer="⑤",
        solution=r"""변환 공식으로
\[
\log_a x=\log_b c
\Rightarrow
\frac{\log_c x}{\log_c a}=\frac{\log_c c}{\log_c b}
\]
이므로
\[
(\text{가})=\frac{1}{\log_c b},\quad
(\text{나})=\frac{\log_c a}{\log_c b}=\log_b a
\]
이다.

따라서
\[
f(2,4,8)=\frac{1}{\log_8 4}+\log_4 2
=\frac{1}{2/3}+\frac12
=\frac32+\frac12=2
\]
이다.""",
    ),
    7: _objective(
        q=r"""6번의 과정에서 빈칸에 들어갈 식 \((\text{다})\)는?""",
        choices=[
            r"$a^{\log_c b}$",
            r"$b^{\log_a c}$",
            r"$b^{\log_c a}$",
            r"$c^{\log_a b}$",
            r"$c^{\log_b a}$",
        ],
        answer="⑤",
        solution=r"""6번에서
\[
\log_c x=\log_b a
\]
이므로 로그의 정의에 의해
\[
x=c^{\log_b a}
\]
이다. 따라서 \((\text{다})=c^{\log_b a}\)이다.""",
    ),
    8: _objective(
        q=r"""외부 자극의 세기를 \(I\), 감각의 세기를 \(S\)라고 하면
\[
S=k\log I\quad(k\text{는 상수})
\]
인 관계가 성립한다고 한다. 어느 자극의 세기가 \(2000\)일 때 감각의 세기가 \(0.660\)이라고 한다.
\[
\log2=0.3
\]
으로 계산할 때, 상수 \(k\)는?""",
        choices=[r"$\dfrac13$", r"$\dfrac14$", r"$\dfrac15$", r"$\dfrac16$", r"$\dfrac17$"],
        answer="③",
        solution=r"""\[
0.660=k\log2000=k(\log2+\log1000)=k(0.3+3)=3.3k
\]
이므로
\[
k=\frac{0.660}{3.3}=0.2=\frac15
\]
이다.""",
    ),
    9: _objective(
        q=r"""8번의 관계식에서 감각의 세기가 \(0.580\)이 되는 자극의 세기는 얼마인가?""",
        choices=[r"$400$", r"$600$", r"$800$", r"$1000$", r"$1200$"],
        answer="③",
        solution=r"""8번에서 \(k=\dfrac15\)이므로
\[
0.580=\frac15\log I
\Rightarrow \log I=2.9
\]
이다.
\[
I=10^{2.9}=10^2\cdot10^{0.9}
\]
이고 \(\log2=0.3\)이므로 \(10^{0.9}=8\).
따라서
\[
I=100\times8=800
\]
이다.""",
    ),
    10: _objective(
        q=r"""함수
\[
y=2^{x-1}-3
\]
의 그래프에 대한 설명으로 옳은 것은?""",
        choices=[
            r"감소함수이다.",
            r"점 \((1,-3)\)을 지난다.",
            r"치역은 \(\{y\mid y\ge-3\}\)이다.",
            r"점근선의 방정식은 \(y=-3\)이다.",
            r"함수 \(y=2^x\)의 그래프를 \(x\)축의 방향으로 \(-1\)만큼, \(y\)축의 방향으로 \(-3\)만큼 평행이동한 그래프이다.",
        ],
        answer="④",
        solution=r"""지수함수 \(2^{x-1}\)은 항상 양수이므로
\[
y=2^{x-1}-3>-3
\]
이고 수평점근선은 \(y=-3\)이다.
따라서 옳은 것은 ④이다.""",
    ),
    11: _objective(
        q=r"""지수함수
\[
y=(a^2-3)^x
\]
와 로그함수
\[
y=\log_{(a+2)}(x+1)
\]
은 \(x\)의 값이 증가하면 \(y\)값은 감소한다. 이때 실수 \(a\)의 값의 범위는?""",
        choices=[
            r"$-2<a<-\sqrt3$",
            r"$-2<a<-1$",
            r"$\sqrt3<a<2$",
            r"$-1<a<2$",
            r"$-2<a<-\sqrt3,\ \sqrt3<a<2$",
        ],
        answer="①",
        solution=r"""지수함수가 감소하려면
\[
0<a^2-3<1
\Rightarrow 3<a^2<4
\Rightarrow -2<a<-\sqrt3\ \text{또는}\ \sqrt3<a<2
\]
이다.

로그함수가 감소하려면 밑이 \(0\)과 \(1\) 사이여야 하므로
\[
0<a+2<1
\Rightarrow -2<a<-1
\]
이다.

교집합은
\[
-2<a<-\sqrt3
\]
이므로 정답은 ①이다.""",
    ),
    12: _objective(
        q=r"""어떤 박테리아는 10분이 지날 때마다 그 수가 2배가 된다. 처음에 20마리였던 박테리아가 2560마리 이상이 되려면 최소 몇 분이 걸리는가?""",
        choices=[r"$60$분", r"$70$분", r"$80$분", r"$90$분", r"$100$분"],
        answer="②",
        solution=r"""시간을 \(t\)분이라 하면
\[
20\cdot2^{t/10}\ge2560
\Rightarrow 2^{t/10}\ge128=2^7
\]
이므로
\[
\frac{t}{10}\ge7,\quad t\ge70
\]
이다. 최소 시간은 \(70\)분이다.""",
    ),
    13: _objective(
        q=r"""오른쪽 그래프는 로그함수
\[
y=\log_a(x+b)+c
\]
의 그래프이다. 그래프가 점 \((4,1)\)을 지날 때, \(a+b-c\)의 값은?

<img src="assets/scan.png" alt="JE-2020-G2-S1-MID-013 graph" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        choices=[r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
        answer="②",
        solution=r"""그래프에서 점근선이 \(x=1\)이므로
\[
x+b=0\Rightarrow -b=1\Rightarrow b=-1
\]
이다.

\((2,0)\)을 지나므로
\[
0=\log_a(2+b)+c=\log_a1+c=c
\Rightarrow c=0
\]
이다.

\((4,1)\)을 지나므로
\[
1=\log_a(4+b)+c=\log_a3
\Rightarrow a=3
\]
이다.

따라서
\[
a+b-c=3+(-1)-0=2
\]
이다.""",
    ),
    14: _objective(
        q=r"다음 중 제2사분면의 각은?",
        choices=[r"$375^\circ$", r"$520^\circ$", r"$800^\circ$", r"$-154^\circ$", r"$-770^\circ$"],
        answer="②",
        solution=r"""\[
520^\circ-360^\circ=160^\circ
\]
이고 \(160^\circ\)는 제2사분면의 각이다.
나머지 선택지는 각각 제1, 제3, 제4사분면에 해당한다.""",
    ),
    15: _objective(
        q=r"""다음 보기 중 옳은 것을 모두 고르면?

<div style="border:1px solid #000; padding:8px; margin:8px 0;">
\[
\text{ㄱ. }72^\circ=\frac{2}{5}\pi,\quad
\text{ㄴ. }-105^\circ=-\frac{5}{12}\pi
\]
\[
\text{ㄷ. }\frac{4}{3}\pi=240^\circ,\quad
\text{ㄹ. }-\frac{5}{6}\pi=-150^\circ
\]
</div>""",
        choices=[r"ㄱ", r"ㄷ", r"ㄱ, ㄴ", r"ㄴ, ㄹ", r"ㄱ, ㄷ, ㄹ"],
        answer="⑤",
        solution=r"""라디안-도 변환으로 확인하면
\[
72^\circ=\frac{72\pi}{180}=\frac{2\pi}{5}\ (\text{참})
\]
\[
-105^\circ=\frac{-105\pi}{180}=-\frac{7\pi}{12}\ (\text{거짓})
\]
\[
\frac{4\pi}{3}=240^\circ\ (\text{참}),\qquad
-\frac{5\pi}{6}=-150^\circ\ (\text{참})
\]
        이므로 옳은 것은 ㄱ, ㄷ, ㄹ이다.""",
    ),
    16: _objective(
        q=r"반지름의 길이가 \(12\)이고 호의 길이가 \(8\pi\)인 부채꼴의 중심각의 크기는?",
        choices=[r"$\dfrac{\pi}{6}$", r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{3}$", r"$\dfrac{2\pi}{3}$", r"$\dfrac{3\pi}{4}$"],
        answer="④",
        solution=r"""부채꼴에서
\[
\text{호의 길이}=r\theta
\]
이므로
\[
8\pi=12\theta
\Rightarrow \theta=\frac{8\pi}{12}=\frac{2\pi}{3}
\]
이다.""",
    ),
    17: _objective(
        q=r"\(\theta=\dfrac{7\pi}{6}\)일 때, \(\cos\theta\)의 값은?",
        choices=[r"$-\dfrac{\sqrt3}{2}$", r"$-\dfrac12$", r"$\dfrac12$", r"$\dfrac{\sqrt2}{2}$", r"$\dfrac{\sqrt3}{2}$"],
        answer="①",
        solution=r"""\[
\theta=\frac{7\pi}{6}=\pi+\frac{\pi}{6}
\]
이므로 제3사분면의 각이다.
\[
\cos\left(\pi+\alpha\right)=-\cos\alpha
\]
를 이용하면
\[
\cos\frac{7\pi}{6}=-\cos\frac{\pi}{6}=-\frac{\sqrt3}{2}
\]
이다.""",
    ),
    18: _objective(
        q=r"\(\sin\theta+\cos\theta=-\dfrac14\)일 때, \(\sin\theta\cos\theta\)의 값은?",
        choices=[r"$-\dfrac{15}{32}$", r"$-\dfrac{15}{16}$", r"$-\dfrac{15}{8}$", r"$-\dfrac{7}{16}$", r"$-\dfrac{7}{8}$"],
        answer="①",
        solution=r"""\[
(\sin\theta+\cos\theta)^2=\sin^2\theta+\cos^2\theta+2\sin\theta\cos\theta
\]
이므로
\[
\left(-\frac14\right)^2=1+2\sin\theta\cos\theta
\]
\[
\frac1{16}=1+2\sin\theta\cos\theta
\Rightarrow 2\sin\theta\cos\theta=-\frac{15}{16}
\]
\[
\sin\theta\cos\theta=-\frac{15}{32}
\]
이다.""",
    ),
    101: _subjective(
        q=r"""식
\[
\left(\frac13\log_4 25\right)\left(\log_{\frac15}\sqrt2\right)
\]
의 값을 구하시오.""",
        answer=r"$-\dfrac16$",
        solution=r"""\[
\log_4 25=\frac{\log_2 25}{\log_2 4}
=\frac{2\log_2 5}{2}
=\log_2 5
\]
\[
\log_{\frac15}\sqrt2
=\frac{\log_5\sqrt2}{\log_5\frac15}
=-\log_5\sqrt2
=-\frac12\log_5 2
\]
따라서
\[
\left(\frac13\log_4 25\right)\left(\log_{\frac15}\sqrt2\right)
=\frac13\log_2 5\cdot\left(-\frac12\log_5 2\right)
=-\frac16
\]
이다.""",
    ),
    102: _subjective(
        q=r"""\[
\sin\theta\tan\theta<0,\quad \cos\theta\tan\theta<0
\]
일 때, 각 \(\theta\)는 제 몇 사분면의 각인지 쓰시오.""",
        answer="제3사분면",
        solution=r"""\[
\sin\theta\tan\theta
=\sin\theta\cdot\frac{\sin\theta}{\cos\theta}
=\frac{\sin^2\theta}{\cos\theta}<0
\]
이므로 \(\cos\theta<0\)이다.

또
\[
\cos\theta\tan\theta
=\cos\theta\cdot\frac{\sin\theta}{\cos\theta}
=\sin\theta<0
\]
이므로 \(\sin\theta<0\)이다.

\(\sin\theta<0,\ \cos\theta<0\)이므로 \(\theta\)는 제3사분면의 각이다.""",
    ),
    103: _subjective(
        q=r"""지적 능력을 측정하는 방법 중 하나는 뇌의 무게를 뇌의 크기로 나누어 구하는 것이다.
이 때 뇌의 크기는 몸무게가 \(a\text{kg}\)일 때
\[
\left(\frac{b}{0.12}\right)^3=a^2
\]
를 만족시키는 \(b\)의 값으로 추정한다고 한다.
무게가 \(8\)톤하는 코끼리의 뇌의 크기를 구하시오.""",
        answer=r"$48$",
        solution=r"""코끼리의 몸무게가 \(8\)톤이므로
\[
a=8000
\]
이다.

\[
\left(\frac{b}{0.12}\right)^3=a^2
\]
에서 양변에 세제곱근을 취하면
\[
\frac{b}{0.12}=a^{2/3}
\Rightarrow b=0.12\cdot a^{2/3}
\]
이다.

\[
8000=20^3
\Rightarrow 8000^{2/3}=20^2=400
\]
이므로
\[
b=0.12\cdot400=48
\]
이다.""",
    ),
    104: _subjective(
        q=r"""함수
\[
f(x)=\log_x(x+1)
\]
에서
\[
f(2)\cdot f(3)\cdots f(n)=6
\]
을 만족시키는 자연수 \(n\)의 값을 구하시오.""",
        answer=r"$63$",
        solution=r"""밑변환을 이용하면
\[
f(k)=\log_k(k+1)=\frac{\log(k+1)}{\log k}
\]
이다.

따라서
\[
f(2)f(3)\cdots f(n)
=\frac{\log3}{\log2}\cdot\frac{\log4}{\log3}\cdots\frac{\log(n+1)}{\log n}
=\frac{\log(n+1)}{\log2}
=\log_2(n+1)
\]
이다.

\[
\log_2(n+1)=6
\Rightarrow n+1=2^6=64
\Rightarrow n=63
\]
이다.""",
    ),
    105: _subjective(
        q=r"""아래 그래프는 일차함수 \(y=f(x)\)의 그래프이다. 다음 조건을 만족한다.
\[
(1)\ f(-6)=0
\]
\[
(2)\ \text{부등식 }3^{f(x)}\le81\text{의 해가 }x\le-3\text{이다.}
\]
\(f(1)\)의 값을 구하시오.

<img src="assets/scan.png" alt="JE-2020-G2-S1-MID-105 graph" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        answer=r"$\dfrac{28}{3}$",
        solution=r"""\[
3^{f(x)}\le81=3^4
\]
이고 \(3^t\)는 증가함수이므로
\[
f(x)\le4
\]
와 같다.

해가 \(x\le-3\)이므로 직선 \(y=f(x)\)에서 \(x=-3\)일 때 \(f(x)=4\)이다.
또 \(f(-6)=0\)이므로 두 점 \((-6,0),(-3,4)\)를 지난다.

기울기는
\[
m=\frac{4-0}{-3-(-6)}=\frac43
\]
이고,
\[
f(1)=0+\frac43\{1-(-6)\}=\frac43\cdot7=\frac{28}{3}
\]
이다.""",
    ),
    106: _subjective(
        q=r"""아래 그래프는 로그함수 \(y=\log_2 x\)의 그래프이다.
상수 \(c\)에 대하여 \(c^8\)은 몇 자리의 정수인지 구하시오.
\[
\text{(단, 점선은 }x\text{축, }y\text{축에 평행하고, }\log2=0.301\text{로 계산한다.)}
\]

<img src="assets/scan.png" alt="JE-2020-G2-S1-MID-106 graph" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        answer=r"$10$자리",
        solution=r"""그래프의 점선 관계에서
\[
\log_2 a=1,\quad \log_2 b=a,\quad \log_2 c=b
\]
를 읽을 수 있다.

따라서
\[
a=2,\quad b=2^a=4,\quad c=2^b=16
\]
이다.

\[
c^8=16^8=(2^4)^8=2^{32}
\]
이므로
\[
\log(c^8)=\log(2^{32})=32\log2=32\times0.301=9.632
\]
이다.

따라서 \(c^8\)의 자릿수는
\[
\lfloor9.632\rfloor+1=10
\]
자리이다.""",
    ),
}


# Crop rectangles on 3x, -90 rotated pages (x0, y0, x1, y1).
CROPS: Dict[int, Tuple[int, Tuple[int, int, int, int]]] = {
    1: (1, (60, 700, 1085, 1180)),
    2: (1, (60, 1080, 1085, 1900)),
    3: (1, (60, 1460, 1085, 2180)),
    4: (1, (60, 2100, 1085, 3010)),
    5: (1, (1010, 450, 2140, 1370)),
    6: (1, (1010, 1300, 2140, 2490)),
    7: (1, (1010, 2420, 2140, 3010)),
    8: (2, (60, 200, 1085, 850)),
    9: (2, (60, 780, 1085, 1380)),
    10: (2, (60, 1300, 1085, 1950)),
    11: (2, (60, 1870, 1085, 3010)),
    12: (2, (1020, 200, 2140, 930)),
    13: (2, (1020, 900, 2140, 1620)),
    14: (2, (1020, 1680, 2140, 2260)),
    15: (2, (1020, 2080, 2140, 3010)),
    16: (4, (30, 60, 1065, 660)),
    17: (4, (30, 615, 1065, 1095)),
    18: (4, (30, 1050, 1065, 2122)),
    101: (4, (30, 2122, 1065, 3052)),
    102: (4, (1095, 60, 2152, 900)),
    103: (4, (1095, 825, 2152, 1900)),
    104: (4, (1000, 1660, 2200, 2300)),
    105: (3, (50, 120, 1085, 2100)),
    106: (3, (1040, 120, 2140, 2100)),
}

UNCERTAIN_NOTES: Dict[int, str] = {
    2: "선지 ②의 중첩근호 인덱스(4제곱근 표기) OCR 판독 재확인 권장",
    3: "분모 근호의 인덱스/중첩근호 판독 재확인 권장",
}


def _pid(no: int) -> str:
    return f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{no:03d}"


def _source_fields(no: int) -> Tuple[int, str, str, str]:
    if no < 100:
        return (
            no,
            "objective",
            str(no),
            f"{META['school']}.{META['year']}.G{META['grade']}.S{META['semester']}.{META['exam']}.{META['subject']}.{no:03d}.question.png",
        )
    idx = no - 100
    return (
        idx,
        "subjective",
        f"서답{idx}",
        f"{META['school']}.{META['year']}.G{META['grade']}.S{META['semester']}.{META['exam']}.{META['subject']}.SUB{idx:02d}.question.png",
    )


def _build_choices(choices: List[str]) -> str:
    if not choices:
        return ""
    marks = ["①", "②", "③", "④", "⑤"]
    return "\n".join(f"{marks[i]} {txt}" for i, txt in enumerate(choices))


def _render_rotated_pages() -> Dict[int, Image.Image]:
    pages: Dict[int, Image.Image] = {}
    doc = fitz.open(SOURCE_PDF)
    try:
        for page_no in range(1, doc.page_count + 1):
            page = doc[page_no - 1]
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # This source set is consistently clockwise-rotated in PDF pages.
            img = img.rotate(-90, expand=True)
            pages[page_no] = img
    finally:
        doc.close()
    return pages


def _write_question_crop(pages: Dict[int, Image.Image], no: int, out_path: Path) -> None:
    page_no, box = CROPS[no]
    x0, y0, x1, y1 = box
    page_img = pages[page_no]
    x0 = max(0, min(x0, page_img.width - 1))
    y0 = max(0, min(y0, page_img.height - 1))
    x1 = max(x0 + 1, min(x1, page_img.width))
    y1 = max(y0 + 1, min(y1, page_img.height))
    page_img.crop((x0, y0, x1, y1)).save(out_path)


def main() -> int:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"source-pdf-not-found: {SOURCE_PDF}")

    numbers = list(range(1, 19)) + list(range(101, 107))
    pages = _render_rotated_pages()

    results: List[Tuple[str, str, str]] = []
    duplicate_dirs: List[str] = []
    warnings: List[str] = []
    review_paths: List[str] = []
    uncertain_rows: List[str] = []

    for no in numbers:
        pid = _pid(no)
        pdir = PROBLEMS / pid
        md_path = pdir / "problem.md"

        if pdir.exists():
            results.append((pid, "SKIPPED_DUPLICATE", "existing-folder"))
            duplicate_dirs.append(str(pdir))
            if no in UNCERTAIN_NOTES:
                uncertain_rows.append(f"{pid} | {UNCERTAIN_NOTES[no]}")
            continue

        pdir.mkdir(parents=True, exist_ok=True)
        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        source_no, source_kind, source_label, q_asset_name = _source_fields(no)
        q_asset_rel = f"assets/original/{q_asset_name}"
        q_asset_path = original_dir / q_asset_name
        _write_question_crop(pages=pages, no=no, out_path=q_asset_path)

        assets: List[str] = ["assets/original/", q_asset_rel]

        sup = SUPPLEMENT_SCANS.get(no)
        if sup is not None:
            if sup.exists():
                shutil.copy2(sup, assets_dir / "scan.png")
                shutil.copy2(sup, original_dir / sup.name)
                assets.insert(0, "assets/scan.png")
                assets.append(f"assets/original/{sup.name}")
            else:
                warnings.append(f"{pid}: supplemental-scan-missing: {sup.name}")

        entry = ENTRIES[no]
        q_text = entry.q.strip()
        choices_text = _build_choices(entry.choices).strip()
        answer_text = entry.answer.strip()
        solution_text = entry.solution.strip()

        cls = classify_unit_and_level(
            question_text=q_text,
            choices_text=choices_text,
            answer_text=answer_text,
            solution_text=solution_text,
            qtype=entry.qtype,
            grade=META["grade"],
            problem_no=no,
        )

        tags = [
            "수동생성",
            "PDF",
            entry.qtype,
            f"출제번호-{source_label}",
            f"과목-{META['subject']}",
            f"생성일-{META['created_date']}",
        ]

        front = {
            "id": pid,
            "school": META["school"],
            "year": META["year"],
            "grade": META["grade"],
            "semester": META["semester"],
            "exam": META["exam"],
            "subject": META["subject"],
            "type": entry.qtype,
            "source_question_no": source_no,
            "source_question_kind": source_kind,
            "source_question_label": source_label,
            "difficulty": cls.level,
            "level": cls.level,
            "unit": cls.unit_path,
            "unit_l1": cls.unit_l1,
            "unit_l2": cls.unit_l2,
            "unit_l3": cls.unit_l3,
            "source": META["source"],
            "tags": tags,
            "assets": assets,
        }

        front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
        body = (
            f"## Q\n{q_text}\n\n"
            f"## Choices\n{choices_text}\n\n"
            f"## Answer\n{answer_text}\n\n"
            f"## Solution\n{solution_text}\n"
        )
        md = f"---\n{front_text}\n---\n\n{body}"
        md_path.write_text(md, encoding="utf-8")

        results.append((pid, "CREATED", q_asset_name))
        review_paths.append(str(md_path))

        if no in UNCERTAIN_NOTES:
            uncertain_rows.append(f"{pid} | {UNCERTAIN_NOTES[no]}")

        if no == 5:
            uncertain_rows.append(f"{pid} | 오류 문항 처리: ③,⑤ 동시 오답")

    created = sum(1 for _, status, _ in results if status == "CREATED")
    skipped = sum(1 for _, status, _ in results if status == "SKIPPED_DUPLICATE")

    lines: List[str] = []
    lines.append("[SUMMARY]")
    lines.append(f"created={created}")
    lines.append("updated=0")
    lines.append(f"skipped={skipped}")
    lines.append(f"warnings={len(warnings)}")
    lines.append("")
    lines.append("[DUPLICATE_DIRS]")
    if duplicate_dirs:
        lines.extend(duplicate_dirs)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[DETAIL]")
    lines.extend([f"{pid} | {status} | {note}" for pid, status, note in results])
    lines.append("")
    lines.append("[UNCERTAIN_OCR_OR_MATH]")
    if uncertain_rows:
        lines.extend(uncertain_rows)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[WARNINGS]")
    if warnings:
        lines.extend(warnings)
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("[REVIEW_PATHS]")
    if review_paths:
        lines.extend(review_paths)
    else:
        lines.append("(none)")
    lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"[DONE] created={created} skipped={skipped} warnings={len(warnings)}")
    print(f"[DUPLICATES] {len(duplicate_dirs)}")
    print(f"[UNCERTAIN] {len(uncertain_rows)}")
    print(f"[REPORT] {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
