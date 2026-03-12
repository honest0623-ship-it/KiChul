from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import shutil

from PIL import Image
import yaml


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "db" / "problems"
ORIGINAL = ROOT / "db" / "original"
PAGE_DIR = ROOT / "output" / "bn2020_preview4x"
REPORT = ROOT / "_tmp_bn_2020_g2_s1_mid_alg_ingest_report.txt"

META = {
    "school": "BN",
    "year": 2020,
    "grade": 2,
    "semester": 1,
    "exam": "MID",
    "subject": "ALG",
    "source": "user_upload_2026-03-11",
}

# page index is 1-based for rotated page images
CROPS: Dict[int, Tuple[int, Tuple[int, int, int, int]]] = {
    1: (1, (90, 650, 1480, 1430)),
    2: (1, (90, 1180, 1480, 2420)),
    3: (1, (90, 2280, 1650, 3730)),
    4: (1, (1370, 430, 2830, 1530)),
    5: (1, (1370, 1380, 2830, 2440)),
    6: (1, (1370, 2280, 2830, 3730)),
    7: (2, (90, 430, 1480, 1460)),
    8: (2, (90, 1280, 1480, 2490)),
    9: (2, (90, 2320, 1480, 3690)),
    10: (2, (1370, 430, 2830, 1590)),
    11: (2, (1370, 1380, 2830, 2920)),
    12: (2, (1370, 2320, 2830, 3900)),
    13: (3, (90, 430, 1480, 1460)),
    14: (3, (90, 1280, 1480, 2410)),
    15: (3, (90, 2200, 1480, 3690)),
    16: (3, (1370, 430, 2830, 1600)),
    17: (3, (1370, 1360, 2830, 3690)),
    18: (4, (90, 430, 1480, 1630)),
    101: (4, (90, 1450, 1480, 2500)),
    102: (4, (90, 2390, 1480, 3690)),
    103: (4, (1370, 430, 2830, 2280)),
    104: (4, (1370, 2040, 2830, 3690)),
}


def _objective(
    q: str,
    choices: List[str],
    answer: str,
    solution: str,
) -> Dict[str, object]:
    return {
        "type": "객관식",
        "q": q,
        "choices": choices,
        "answer": answer,
        "solution": solution,
    }


def _subjective(
    qtype: str,
    q: str,
    answer: str,
    solution: str,
) -> Dict[str, object]:
    return {
        "type": qtype,
        "q": q,
        "choices": [],
        "answer": answer,
        "solution": solution,
    }


ENTRIES: Dict[int, Dict[str, object]] = {
    1: _objective(
        q=r"""$\sqrt{\sqrt{128}}\times\sqrt[4]{32}+\dfrac{\sqrt[3]{250}}{\sqrt[3]{2}}$의 값은?""",
        choices=[r"$11$", r"$12$", r"$13$", r"$14$", r"$15$"],
        answer="③",
        solution=r"""\[
\sqrt{\sqrt{128}}\times\sqrt[4]{32}
=128^{\frac14}\times 32^{\frac14}
=2^{\frac74}\times 2^{\frac54}
=2^3=8
\]
또,
\[
\dfrac{\sqrt[3]{250}}{\sqrt[3]{2}}
=\sqrt[3]{\dfrac{250}{2}}
=\sqrt[3]{125}=5
\]
따라서
\[
8+5=13
\]
이므로 정답은 ③이다.""",
    ),
    2: _objective(
        q=r"""$x$, $y$, $z$가 $1$이 아닌 양수일 때, 다음 중 옳지 않은 것은?""",
        choices=[
            r"$\log_x y\times\log_y z=\log_x z$",
            r"$\log_z xyz=1+\log_z xy$",
            r"$\log_x y^z=\dfrac{z}{\log_y x}$",
            r"$\log_z(xy)=\log_z x+\log_z y$",
            r"$\dfrac{\log_z y}{\log_z x}=\log_z y-\log_z x$",
        ],
        answer="⑤",
        solution=r"""①, ②, ③, ④는 로그의 기본 성질로 모두 성립한다.

⑤에서
\[
\dfrac{\log_z y}{\log_z x}=\log_x y
\]
이고,
\[
\log_z y-\log_z x=\log_z\left(\dfrac{y}{x}\right)
\]
이므로 일반적으로 같지 않다.

따라서 옳지 않은 것은 ⑤이다.""",
    ),
    3: _objective(
        q=r"""다음 중 함수 $y=\log_3(5-x)-3$의 그래프에 대한 설명으로 옳지 않은 것은?""",
        choices=[
            r"정의역은 $\{x\mid x<5\}$이다.",
            r"치역은 $\{y\mid y$는 모든 실수$\}$이다.",
            r"$x$의 값이 증가하면 $y$의 값은 감소한다.",
            r"점근선의 방정식은 $x=5$이다.",
            r"함수 $y=\log_{1/3}(5-x)-3$의 그래프와 $y$축에 대하여 대칭이다.",
        ],
        answer="⑤",
        solution=r"""$y=\log_3(5-x)-3$에서
\[
5-x>0\Rightarrow x<5
\]
이므로 ①은 옳다. 로그함수의 치역은 모든 실수이므로 ②도 옳다.

$5-x$는 $x$가 증가하면 감소하고, 밑이 $3(>1)$인 로그는 증가함수이므로 전체 함수는 감소한다. 따라서 ③은 옳다.

또한 $x=5$에서 수직점근선을 가지므로 ④도 옳다.

$y$축 대칭은 $x$를 $-x$로 바꾸는 것이므로
\[
y=\log_3(5+x)-3
\]
가 되어야 한다. ⑤의 함수는 이에 해당하지 않는다.

따라서 옳지 않은 것은 ⑤이다.""",
    ),
    4: _objective(
        q=r"""중심각의 크기가 $\dfrac{3\pi}{4}$이고, 둘레의 길이가 $8+3\pi$인 부채꼴의 넓이는?""",
        choices=[r"$6\pi$", r"$5\pi$", r"$4\pi$", r"$3\pi$", r"$2\pi$"],
        answer="①",
        solution=r"""반지름을 $r$이라 하면 부채꼴의 둘레는
\[
2r+r\cdot\frac{3\pi}{4}=8+3\pi
\]
이므로
\[
r\left(2+\frac{3\pi}{4}\right)=8+3\pi
\]
이고 $r=4$를 얻는다.

넓이는
\[
\frac12 r^2\theta
=\frac12\cdot 4^2\cdot\frac{3\pi}{4}
=6\pi
\]
이므로 정답은 ①이다.""",
    ),
    5: _objective(
        q=r"""방정식 $4^{x^2-3x}=2^{4x-12}$의 두 실근을 $\alpha$, $\beta$라 할 때, $\alpha\beta$의 값은?""",
        choices=[r"$2$", r"$6$", r"$10$", r"$14$", r"$18$"],
        answer="②",
        solution=r"""$4=2^2$이므로
\[
2^{2x^2-6x}=2^{4x-12}
\]
따라서
\[
2x^2-6x=4x-12
\]
\[
x^2-5x+6=0
\]
\[
(x-2)(x-3)=0
\]
이므로 두 근은 $2$, $3$이다.

따라서
\[
\alpha\beta=2\cdot 3=6
\]
이고 정답은 ②이다.""",
    ),
    6: _objective(
        q=r"""$\log_2 5=a$, $\log_5 3=b$일 때, $\log_5 12$를 $a$, $b$로 나타낸 것은?""",
        choices=[r"$\dfrac{b}{a}$", r"$\dfrac{a}{b}$", r"$\dfrac{1}{a}+b$", r"$a+\dfrac{1}{b}$", r"$\dfrac{2}{a}+b$"],
        answer="⑤",
        solution=r"""\[
\log_5 12=\log_5(3\cdot 4)=\log_5 3+\log_5 4
\]
\[
= b+2\log_5 2
\]
그런데
\[
\log_2 5=a\Rightarrow \log_5 2=\frac{1}{a}
\]
이므로
\[
\log_5 12=b+\frac{2}{a}
\]
이다.

따라서 정답은 ⑤이다.""",
    ),
    7: _objective(
        q=r"""$1<x<3$일 때, 세 수
\[
A=\log_{1/3}x,\quad B=\log_{1/3}\frac12,\quad C=\log_2\frac13
\]
의 대소 관계로 옳은 것은?""",
        choices=[
            r"$A<B<C$",
            r"$A<C<B$",
            r"$B<A<C$",
            r"$B<C<A$",
            r"$C<A<B$",
        ],
        answer="⑤",
        solution=r"""$1<x<3$이므로 $A=\log_{1/3}x$는
\[
-1<A<0
\]
이다(밑이 $1/3<1$이므로 감소함수).

또
\[
B=\log_{1/3}\frac12=\frac{\log(1/2)}{\log(1/3)}>0
\]
이고,
\[
C=\log_2\frac13<0
\]
이다.

또한
\[
A>-1,\quad C=\log_2\frac13\approx -1.58
\]
이므로 $C<A$이다. 따라서
\[
C<A<B
\]
이므로 정답은 ⑤이다.""",
    ),
    8: _objective(
        q=r"""$\sin\theta=-\dfrac{5}{13}$이고 $\cos\theta+\sin\theta\times\tan\theta<0$일 때, $\tan\theta$의 값은?""",
        choices=[r"$-\dfrac{12}{13}$", r"$-\dfrac{5}{12}$", r"$\dfrac{5}{12}$", r"$\dfrac{12}{13}$", r"$\dfrac{13}{5}$"],
        answer="③",
        solution=r"""주어진 부등식은
\[
\cos\theta+\sin\theta\tan\theta
=\cos\theta+\frac{\sin^2\theta}{\cos\theta}
=\frac{\cos^2\theta+\sin^2\theta}{\cos\theta}
=\frac{1}{\cos\theta}<0
\]
이므로 $\cos\theta<0$이다.

$\sin\theta=-\dfrac{5}{13}$이므로
\[
\cos\theta=-\frac{12}{13}
\]
(제3사분면)이고,
\[
\tan\theta=\frac{\sin\theta}{\cos\theta}
=\frac{-5/13}{-12/13}
=\frac{5}{12}
\]
이다.

따라서 정답은 ③이다.""",
    ),
    9: _objective(
        q=r"""함수 $y=\log_a x+m$의 그래프와 그 역함수의 그래프가 두 점에서 만난다. 두 교점의 $x$좌표가 각각 $1$, $3$일 때, 두 상수 $a$, $m$에 대하여 $a^2+m$의 값은? (단, $a>0$, $a\ne 1$)""",
        choices=[r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
        answer="④",
        solution=r"""함수와 역함수의 교점은 직선 $y=x$ 위에 있으므로
\[
\log_a x+m=x
\]
을 만족한다.

$x=1$을 대입하면
\[
\log_a1+m=1\Rightarrow m=1
\]
이다.

$x=3$을 대입하면
\[
\log_a3+m=3
\Rightarrow \log_a3=2
\Rightarrow a^2=3
\]
이다.

따라서
\[
a^2+m=3+1=4
\]
이므로 정답은 ④이다.""",
    ),
    10: _objective(
        q=r"""함수 $f(x)=a\cos bx+c$의 그래프는 그림과 같고,
$f(0)=5$, $f(2\pi)=1$일 때, $f\!\left(\dfrac{2\pi}{3}\right)$의 값은? (단, $a$, $b$, $c$는 상수이고 $a>0$, $b>0$이다.)

<img src="assets/scan.png" alt="문항 삽화" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        choices=[r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"],
        answer="④",
        solution=r"""그래프에서 최댓값이 $5$, 최솟값이 $1$이므로
\[
a=\frac{5-1}{2},\qquad c=\frac{5+1}{2}
\]
즉 $a=2$, $c=3$이다.

또 $x=0$에서 최댓값, $x=2\pi$에서 최솟값이므로 반주기가 $2\pi$이다.
따라서 주기는 $4\pi$, 즉
\[
\frac{2\pi}{b}=4\pi\Rightarrow b=\frac12
\]
이다.

그러므로
\[
f\!\left(\frac{2\pi}{3}\right)
=2\cos\left(\frac12\cdot\frac{2\pi}{3}\right)+3
=2\cos\frac\pi3+3
=2\cdot\frac12+3=4
\]
이므로 정답은 ④이다.""",
    ),
    11: _objective(
        q=r"""다음 &lt;보기&gt;의 함수의 그래프 중 함수 $y=3^x$의 그래프를 평행이동 또는 대칭이동하여 겹쳐지는 것만을 모두 고른 것은?

<div style="border:1px solid #222; padding:10px; margin:8px 0;">
<p>&lt;보기&gt;</p>
<p>ㄱ. $y=3^{x+1}-2$ &nbsp;&nbsp;&nbsp;&nbsp; ㄴ. $y=\left(\dfrac13\right)^x$</p>
<p>ㄷ. $y=3^{2x}+5$ &nbsp;&nbsp;&nbsp;&nbsp; ㄹ. $y=2\cdot 3^x+1$</p>
</div>""",
        choices=[r"ㄱ, ㄴ", r"ㄷ, ㄹ", r"ㄱ, ㄴ, ㄹ", r"ㄴ, ㄷ, ㄹ", r"ㄱ, ㄴ, ㄷ, ㄹ"],
        answer="①",
        solution=r"""ㄱ은 $y=3^x$를 왼쪽으로 $1$, 아래로 $2$만큼 평행이동한 그래프이므로 가능하다.

ㄴ은
\[
\left(\frac13\right)^x=3^{-x}
\]
이므로 $y=3^x$를 $y$축 대칭한 그래프이다.

ㄷ의 $3^{2x}$는 $x$방향의 축소(가로 변화)가 포함되어 평행이동/대칭이동만으로는 만들 수 없다.

ㄹ의 $2\cdot 3^x+1$은 세로 확대가 포함되어 평행이동/대칭이동만으로는 만들 수 없다.

따라서 ㄱ, ㄴ만 가능하므로 정답은 ①이다.""",
    ),
    12: _objective(
        q=r"""$a^{2x}=2$일 때,
\[
\frac{a^{3x}+a^{-3x}}{a^x-a^{-x}}
\]
의 값은? (단, $a>0$)""",
        choices=[r"$3$", r"$\dfrac72$", r"$4$", r"$\dfrac92$", r"$5$"],
        answer="④",
        solution=r"""$t=a^x$라 두면 $t>0$, $t^2=2$이므로 $t=\sqrt2$이다.

주어진 식은
\[
\frac{t^3+t^{-3}}{t-t^{-1}}
\]
이고,
\[
t^3=(\sqrt2)^3=2\sqrt2,\qquad t^{-3}=\frac{1}{2\sqrt2}=\frac{\sqrt2}{4}
\]
이므로 분자는
\[
2\sqrt2+\frac{\sqrt2}{4}=\frac{9\sqrt2}{4}
\]
이다.

또 분모는
\[
\sqrt2-\frac{1}{\sqrt2}=\frac{1}{\sqrt2}
\]
이므로
\[
\frac{\frac{9\sqrt2}{4}}{\frac1{\sqrt2}}
=\frac{9\sqrt2}{4}\cdot\sqrt2
=\frac{18}{4}
=\frac92
\]
이다.

따라서 정답은 ④이다.""",
    ),
    13: _objective(
        q=r"""모든 실수 $x$에 대하여 부등식
\[
25^x-4\cdot 5^x+a-1>0
\]
이 항상 성립하도록 하는 자연수 $a$의 최솟값은?""",
        choices=[r"$5$", r"$6$", r"$7$", r"$8$", r"$9$"],
        answer="②",
        solution=r"""$t=5^x(>0)$로 두면 부등식은
\[
t^2-4t+a-1>0
\]
즉
\[
(t-2)^2+a-5>0
\]
가 된다.

모든 $t>0$에 대해 항상 성립하려면 최소값에서도 양수여야 한다.
$(t-2)^2$의 최소값은 $0$이므로
\[
a-5>0\Rightarrow a>5
\]
이다.

자연수 $a$의 최솟값은 $6$이므로 정답은 ②이다.""",
    ),
    14: _objective(
        q=r"""다음
\[
2\sin^2\left(\frac\pi2-\theta\right)
+\cos\left(\frac\pi2+\theta\right)\sin(\pi-\theta)
+3\sin^2(2\pi+\theta)
\]
의 값은?""",
        choices=[r"$0$", r"$1$", r"$2$", r"$\sin^2\theta$", r"$\cos^2\theta$"],
        answer="③",
        solution=r"""삼각함수 항등식을 이용하면
\[
\sin\left(\frac\pi2-\theta\right)=\cos\theta,\quad
\cos\left(\frac\pi2+\theta\right)=-\sin\theta,\quad
\sin(\pi-\theta)=\sin\theta,\quad
\sin(2\pi+\theta)=\sin\theta
\]
이다.

따라서 식은
\[
2\cos^2\theta+(-\sin\theta)(\sin\theta)+3\sin^2\theta
\]
\[
=2\cos^2\theta+2\sin^2\theta
=2(\cos^2\theta+\sin^2\theta)=2
\]
가 된다.

정답은 ③이다.""",
    ),
    15: _objective(
        q=r"""$0<a<1<b<2$를 만족시키는 두 실수 $a$, $b$에 대하여 다음 &lt;보기&gt; 중 옳은 것만을 모두 고른 것은?

<div style="border:1px solid #222; padding:10px; margin:8px 0;">
<p>&lt;보기&gt;</p>
<p>ㄱ. $2^a<2^b$</p>
<p>ㄴ. $\log_a b>0$</p>
<p>ㄷ. $2^b<b^2$</p>
</div>""",
        choices=[r"ㄱ", r"ㄴ", r"ㄱ, ㄷ", r"ㄴ, ㄷ", r"ㄱ, ㄴ, ㄷ"],
        answer="①",
        solution=r"""조건이 $0<a<1<b<2$이므로

ㄱ. 밑이 $2>1$인 지수함수는 증가하므로 $a<b$에서 $2^a<2^b$가 성립한다. (참)

ㄴ. 밑이 $0<a<1$이고 진수가 $b>1$이면 $\log_a b<0$이므로 거짓이다.

ㄷ. $1<b<2$에서 $2^b$와 $b^2$를 비교하면 항상 $2^b<b^2$가 성립하지 않는다.
예를 들어 $b=\dfrac32$이면
\[
2^b=2^{3/2}=\sqrt8>\frac94=b^2
\]
이므로 거짓이다.

따라서 옳은 것은 ㄱ만이므로 정답은 ①이다.""",
    ),
    16: _objective(
        q=r"""$\sin\theta\times\sin\left(\dfrac\pi2-\theta\right)>0$이고 $\sin\theta=-\dfrac35$일 때,
\[
\tan(\pi-\theta)\times\cos(\pi+\theta)
\]
의 값은?""",
        choices=[r"$-\dfrac34$", r"$-\dfrac35$", r"$0$", r"$\dfrac35$", r"$\dfrac34$"],
        answer="②",
        solution=r"""조건
\[
\sin\theta\sin\left(\frac\pi2-\theta\right)
=\sin\theta\cos\theta>0
\]
이고 $\sin\theta=-\dfrac35<0$이므로 $\cos\theta<0$이다.

따라서
\[
\cos\theta=-\frac45,\qquad \tan\theta=\frac{\sin\theta}{\cos\theta}=\frac34
\]
이다.

이제
\[
\tan(\pi-\theta)=-\tan\theta=-\frac34,\qquad
\cos(\pi+\theta)=-\cos\theta=\frac45
\]
이므로
\[
\tan(\pi-\theta)\cos(\pi+\theta)
=-\frac34\cdot\frac45=-\frac35
\]
이다.

정답은 ②이다.""",
    ),
    17: _objective(
        q=r"""그림과 같이 직선 $y=\dfrac12x$ 위의 점 $P(a,b)$를 지나고 $x$축에 평행한 직선이 곡선 $y=2^x$와 만나는 점을 $A$, 점 $P$를 지나고 $y$축에 평행한 직선이 곡선 $y=\log_4x$와 만나는 점을 $B$라 하자. $\overline{PB}=5$일 때, $\overline{PA}$의 값은? (단, $a>1$)

<img src="assets/scan.png" alt="문항 삽화" style="width:60% !important; max-width:60% !important; height:auto;" />""",
        choices=[r"$10$", r"$11$", r"$12$", r"$13$", r"$14$"],
        answer="②",
        solution=r"""$P(a,b)$가 직선 $y=\dfrac12x$ 위의 점이므로
\[
b=\frac a2
\]
이다.

$B$는 $x=a$에서 $y=\log_4x$ 위의 점이므로
\[
B=(a,\log_4a)
\]
이고,
\[
\overline{PB}=b-\log_4a=5
\]
이므로
\[
\frac a2-\log_4a=5
\]
\[
a-\log_2a=10
\]
을 얻는다.

한편 $A$는 $y=b$와 $y=2^x$의 교점이므로
\[
A=(\log_2b,\ b)
\]
따라서
\[
\overline{PA}=a-\log_2b
\]
\[
=a-\log_2\left(\frac a2\right)
=a-(\log_2a-1)
=(a-\log_2a)+1
=10+1
=11
\]
이다.

정답은 ②이다.""",
    ),
    18: _objective(
        q=r"""$0\le x<2\pi$일 때, 방정식
\[
3\sin^2x-2\cos x+a=0
\]
이 실근을 가지도록 하는 정수 $a$의 개수는?""",
        choices=[r"$3$", r"$4$", r"$5$", r"$6$", r"$7$"],
        answer="④",
        solution=r"""$t=\cos x\ (-1\le t\le 1)$로 두고
\[
\sin^2x=1-\cos^2x=1-t^2
\]
를 대입하면
\[
a=3-3t^2-2t
\]
로 볼 수 있다.

함수
\[
f(t)=3-3t^2-2t
\]
는 아래로 열린 이차함수이다.

최댓값은 꼭짓점 $t=-\dfrac13$에서
\[
f\left(-\frac13\right)=\frac{10}{3}
\]
최솟값은 끝점 $t=1$에서
\[
f(1)=-2
\]
이다(또 $f(-1)=2$).

따라서 가능한 $a$의 범위는
\[
-2\le a\le \frac{10}{3}
\]
이고, 정수는
\[
-2,-1,0,1,2,3
\]
총 $6$개이다.

정답은 ④이다.""",
    ),
    101: _subjective(
        qtype="단답형",
        q=r"""원점 $O$와 점 $P(-1,2)$을 지나는 동경 $OP$가 나타내는 각의 크기를 $\theta$라 할 때,
\[
\frac{\cos\theta\cdot\sin\theta}{\tan\theta}
\]
의 값을 구하여라.""",
        answer=r"$\dfrac15$",
        solution=r"""점 $P(-1,2)$이므로
\[
r=\sqrt{(-1)^2+2^2}=\sqrt5
\]
\[
\cos\theta=\frac{-1}{\sqrt5},\qquad
\sin\theta=\frac{2}{\sqrt5},\qquad
\tan\theta=\frac{2/\sqrt5}{-1/\sqrt5}=-2
\]
이다.

따라서
\[
\frac{\cos\theta\sin\theta}{\tan\theta}
=\frac{\left(-\frac1{\sqrt5}\right)\left(\frac2{\sqrt5}\right)}{-2}
=\frac{-2/5}{-2}
=\frac15
\]
이다.""",
    ),
    102: _subjective(
        qtype="단답형",
        q=r"""$2\le n\le 100$인 자연수 $n$에 대하여
\[
\left(\sqrt{7^5}\right)^{\frac13}
\]
이 어떤 자연수의 $n$제곱근이 되도록 하는 $n$의 개수를 구하여라.""",
        answer=r"$16$",
        solution=r"""주어진 수를 정리하면
\[
\left(\sqrt{7^5}\right)^{1/3}
=\left(7^{5/2}\right)^{1/3}
=7^{5/6}
\]
이다.

이 수가 어떤 자연수의 $n$제곱근이 되려면
\[
\left(7^{5/6}\right)^n=7^{5n/6}
\]
이 자연수가 되어야 한다. 즉 지수 $\dfrac{5n}{6}$이 정수여야 하므로
\[
6\mid 5n
\]
이고, $\gcd(5,6)=1$이므로 $6\mid n$이다.

$2\le n\le 100$에서 $6$의 배수는
\[
6,12,18,\dots,96
\]
으로 총
\[
\frac{96-6}{6}+1=16
\]
개이다.

따라서 구하는 개수는 $16$이다.""",
    ),
    103: _subjective(
        qtype="서술형",
        q=r"""어느 국가의 국내 총생산은 매년 $5\%$씩 늘어난다고 한다. 이 국가의 국내 총생산이 현재의 $1.5$배 이상이 되는 해는 최소 $t$년 후일 때, $t$의 값을 구하는 풀이과정을 쓰고 답을 구하여라.

(단, $\log 1.5=0.18$, $\log 1.05=0.02$로 계산한다.)""",
        answer=r"$9$",
        solution=r"""현재 국내 총생산을 $G$라 하면 $t$년 후 국내 총생산은
\[
G(1.05)^t
\]
이다.

조건에 의해
\[
G(1.05)^t\ge 1.5G
\]
\[
(1.05)^t\ge 1.5
\]
이고, 상용로그를 취하면
\[
t\log 1.05\ge \log 1.5
\]
\[
t\cdot 0.02\ge 0.18
\]
\[
t\ge 9
\]
이다.

따라서 최소 정수 $t$는
\[
9
\]
이다.""",
    ),
    104: _subjective(
        qtype="서술형",
        q=r"""$0\le\theta<2\pi$일 때, 모든 실수 $x$에 대하여 부등식
\[
x^2-2\sin\theta\,x-\cos^2\theta-2\cos\theta+2\ge 0
\]
이 항상 성립하도록 하는 모든 $\theta$의 값의 범위는 $\alpha\le\theta\le\beta$이다. $\beta-2\alpha$의 값을 구하는 풀이과정을 쓰고 답을 구하여라.""",
        answer=r"$\pi$",
        solution=r"""이차식
\[
F(x)=x^2-2\sin\theta\,x-\cos^2\theta-2\cos\theta+2
\]
가 모든 실수 $x$에 대해 $F(x)\ge 0$이려면 판별식이 $0$ 이하이면 된다.

\[
\Delta=(-2\sin\theta)^2-4\cdot1\cdot(-\cos^2\theta-2\cos\theta+2)
\]
\[
=4\sin^2\theta+4(\cos^2\theta+2\cos\theta-2)
\]
\[
=4(\sin^2\theta+\cos^2\theta+2\cos\theta-2)
=4(2\cos\theta-1)
\]
따라서
\[
\Delta\le0\iff 2\cos\theta-1\le0\iff \cos\theta\le\frac12
\]
이다.

$0\le\theta<2\pi$에서
\[
\frac\pi3\le\theta\le\frac{5\pi}3
\]
이므로
\[
\alpha=\frac\pi3,\qquad \beta=\frac{5\pi}3
\]
이다.

따라서
\[
\beta-2\alpha
=\frac{5\pi}3-2\cdot\frac\pi3
=\pi
\]
이다.""",
    ),
}


def _pid(no: int) -> str:
    return f"{META['school']}-{META['year']}-G{META['grade']}-S{META['semester']}-{META['exam']}-{no:03d}"


def _build_choices(choices: List[str]) -> str:
    if not choices:
        return ""
    marks = ["①", "②", "③", "④", "⑤"]
    return "\n".join([f"{marks[idx]} {line}" for idx, line in enumerate(choices)])


def _source_fields(no: int) -> Tuple[int, str, str, str]:
    if no < 100:
        return no, "objective", str(no), f"BN.2020.G2.S1.MID.ALG.{no:03d}.question.png"
    idx = no - 100
    return idx, "subjective", f"서답{idx}", f"BN.2020.G2.S1.MID.ALG.SUB{idx:02d}.question.png"


def _copy_question_crop(no: int, out_path: Path) -> None:
    page_no, box = CROPS[no]
    page_img = Image.open(PAGE_DIR / f"page_{page_no}_rot.png")
    page_img.crop(box).save(out_path)


def _scan_asset_source(no: int) -> Path | None:
    if no == 10:
        return ORIGINAL / "BN.2020.G2.S1.MID.ALG.010.png"
    if no == 17:
        return ORIGINAL / "BN.2020.G2.S1.MID.ALG.017.png"
    return None


def main() -> int:
    results: List[Tuple[str, str, str]] = []
    warnings: List[str] = []

    numbers = list(range(1, 19)) + list(range(101, 105))
    for no in numbers:
        pid = _pid(no)
        pdir = PROBLEMS / pid
        entry = ENTRIES[no]

        pdir.mkdir(parents=True, exist_ok=True)
        assets_dir = pdir / "assets"
        original_dir = assets_dir / "original"
        original_dir.mkdir(parents=True, exist_ok=True)

        source_no, source_kind, source_label, q_asset_name = _source_fields(no)
        q_asset_rel = f"assets/original/{q_asset_name}"
        q_asset_path = original_dir / q_asset_name
        _copy_question_crop(no, q_asset_path)

        assets: List[str] = ["assets/original/", q_asset_rel]

        scan_src = _scan_asset_source(no)
        if scan_src is not None:
            if scan_src.exists():
                shutil.copy2(scan_src, assets_dir / "scan.png")
                shutil.copy2(scan_src, original_dir / scan_src.name)
                assets.insert(0, "assets/scan.png")
                assets.append(f"assets/original/{scan_src.name}")
            else:
                warnings.append(f"{pid}: supplemental-scan-missing: {scan_src.name}")

        qtype = str(entry["type"])
        tags = [
            "수동생성",
            "PDF",
            qtype,
            f"출제번호-{source_label}",
            f"과목-{META['subject']}",
            "생성일-2026-03-11",
        ]

        front = {
            "id": pid,
            "school": META["school"],
            "year": META["year"],
            "grade": META["grade"],
            "semester": META["semester"],
            "exam": META["exam"],
            "subject": META["subject"],
            "type": qtype,
            "source_question_no": source_no,
            "source_question_kind": source_kind,
            "source_question_label": source_label,
            "difficulty": 3,
            "level": 3,
            "unit": "",
            "unit_l1": "",
            "unit_l2": "",
            "unit_l3": "",
            "source": META["source"],
            "tags": tags,
            "assets": assets,
        }

        front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
        body = (
            f"## Q\n{str(entry['q']).strip()}\n\n"
            f"## Choices\n{_build_choices(list(entry['choices'])).strip()}\n\n"
            f"## Answer\n{str(entry['answer']).strip()}\n\n"
            f"## Solution\n{str(entry['solution']).strip()}\n"
        )
        md = f"---\n{front_text}\n---\n\n{body}"
        (pdir / "problem.md").write_text(md, encoding="utf-8")
        results.append((pid, "WRITTEN", q_asset_name))

    report_lines: List[str] = []
    report_lines.append("[SUMMARY]")
    report_lines.append(f"written={len(results)}")
    report_lines.append(f"warnings={len(warnings)}")
    report_lines.append("")
    report_lines.append("[DETAIL]")
    report_lines.extend([f"{pid} | {status} | {note}" for pid, status, note in results])
    report_lines.append("")
    report_lines.append("[WARNINGS]")
    if warnings:
        report_lines.extend(warnings)
    else:
        report_lines.append("(none)")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"[DONE] written={len(results)} warnings={len(warnings)}")
    print(f"[REPORT] {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
