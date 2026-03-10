당신은 한국 고등학교 수학 문항 제작자다.
아래 원문항을 바탕으로 유사하지만 새로운 문항 1개를 생성하라.
반드시 대한민국 고등학교 교육과정 기호를 사용하고, 수식은 markdown LaTeX로 작성하라.
답과 해설은 문항과 일치해야 한다.

출력 형식은 반드시 JSON 객체 하나만 출력한다. 다른 텍스트를 절대 붙이지 마라.
JSON keys: q, choices, answer, solution

제약:
- 학년: 고1
- 단원: 공통수학1(2022개정) > 2. 방정식과 부등식 > 2-1. 복소수와 이차방정식
- 변형유형: parameter_change
- 변형번호: 1
- 문제/정답/해설 모두 한국어로 작성.
- `solution`은 중간 계산을 간결하게 포함하고 최종 결론을 명확히 제시.
- 객관식 문항으로 만들고, `choices`에는 5개 선택지(①~⑤)를 줄바꿈으로 제공한다.
- 벡터/미적분 등 해당 학년·단원을 벗어나는 풀이 기호는 사용하지 않는다.

[원본 ID] JJ-2025-G1-S1-MID-011
[원본 Q]
이차방정식 $x^2+2x-3=0$의 두 근을 $\alpha,\beta$라고 할 때, 두 수 $\dfrac{\alpha}{1+\alpha}$, $\dfrac{\beta}{1+\beta}$를 두 근으로 하고 $x^2$의 계수가 4인 이차방정식을 구하면?

[원본 Choices]
① $4x^2-8x+1=0$
② $4x^2-8x+3=0$
③ $4x^2+8x-1=0$
④ $4x^2+8x+1=0$
⑤ $4x^2+8x+3=0$

[원본 Answer]
②

[원본 Solution]
$\alpha,\beta$에 대해
            $$
            \alpha+\beta=-2,\quad \alpha\beta=-3.
            $$
            새 근을
            $$
            u=\frac{\alpha}{1+\alpha},\quad v=\frac{\beta}{1+\beta}
            $$
            라 두면
            $$
            u+v=\frac{\alpha(1+\beta)+\beta(1+\alpha)}{(1+\alpha)(1+\beta)}
            =\frac{(\alpha+\beta)+2\alpha\beta}{1+(\alpha+\beta)+\alpha\beta}
            =\frac{-2-6}{1-2-3}=2,
            $$
            $$
            uv=\frac{\alpha\beta}{(1+\alpha)(1+\beta)}
            =\frac{-3}{1-2-3}=\frac34.
            $$
            따라서 새 이차방정식은
            $$
            x^2-2x+\frac34=0.
            $$
            $x^2$의 계수를 4로 맞추면
            $$
            4x^2-8x+3=0.
            $$
