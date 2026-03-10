당신은 한국 고등학교 수학 문항 제작자다.
아래 원문항을 바탕으로 유사하지만 새로운 문항 1개를 생성하라.
반드시 대한민국 고등학교 교육과정 기호를 사용하고, 수식은 markdown LaTeX로 작성하라.
답과 해설은 문항과 일치해야 한다.

출력 형식은 반드시 JSON 객체 하나만 출력한다. 다른 텍스트를 절대 붙이지 마라.
JSON keys: q, choices, answer, solution

제약:
- 학년: 고1
- 단원: 공통수학1(2022개정) > 2. 방정식과 부등식 > 2-2. 이차방정식과 이차함수
- 변형유형: parameter_change
- 변형번호: 1
- 문제/정답/해설 모두 한국어로 작성.
- `solution`은 중간 계산을 간결하게 포함하고 최종 결론을 명확히 제시.
- 객관식 문항으로 만들고, `choices`에는 5개 선택지(①~⑤)를 줄바꿈으로 제공한다.
- 벡터/미적분 등 해당 학년·단원을 벗어나는 풀이 기호는 사용하지 않는다.

[원본 ID] HN-2025-G1-S1-MID-018
[원본 Q]
오른쪽 그림의 직사각형 $ABCD$에서 두 점 $A$와 $B$는 $x$축 위에 있고,
두 점 $C$와 $D$는 이차함수
$$
y=-2x^2+6x
$$
의 그래프 위에 있다.  
이때 직사각형 $ABCD$의 둘레의 길이의 최댓값을 $\alpha$,
그때의 직사각형의 넓이를 $\beta$라 할 때, $\alpha+\beta$의 값은?

(단, 두 점 $C,D$는 제1사분면 위의 점이다.) (4.5점)

<img src="assets/scan.png" alt="figure" style="width:66% !important; max-width:66% !important; height:auto;" />

[원본 Choices]
① 8  
② 10  
③ 12  
④ 14  
⑤ 16

[원본 Answer]
④

[원본 Solution]
함수
$$
f(x)=-2x^2+6x=-2(x-\tfrac{3}{2})^2+\tfrac{9}{2}
$$
는 $x=\tfrac{3}{2}$에 대해 대칭이므로, 직사각형의 윗변이 닿는 점을
$$
x=\tfrac{3}{2}\pm t \quad (t>0)
$$
로 두면 폭은 $2t$.

높이는
$$
h=f(\tfrac{3}{2}-t)=-2t^2+\tfrac{9}{2}.
$$

둘레
$$
P(t)=2(2t+h)=2\!\left(2t-2t^2+\tfrac{9}{2}\right)=-4t^2+4t+9
$$
이므로 최댓값은 꼭짓점에서,
$$
t=\frac{-4}{2(-4)}=\frac{1}{2}.
$$
따라서
$$
\alpha=P(\tfrac12)=-4\cdot \tfrac14+4\cdot \tfrac12+9=10.
$$

넓이
$$
A(t)=(2t)\,h=2t\!\left(-2t^2+\tfrac{9}{2}\right)=-4t^3+9t
$$
이므로
$$
\beta=A(\tfrac12)=-4\cdot \tfrac18+9\cdot \tfrac12=-\tfrac12+\tfrac{9}{2}=4.
$$
따라서 $\alpha+\beta=10+4=14$ (정답 ④).
