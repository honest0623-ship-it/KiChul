from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class UnitLevelResult:
    unit_l1: str
    unit_l2: str
    unit_l3: str
    level: int
    reason: str

    @property
    def unit_path(self) -> str:
        parts = [self.unit_l1.strip(), self.unit_l2.strip(), self.unit_l3.strip()]
        return " > ".join([item for item in parts if item])


@dataclass(frozen=True)
class UnitRule:
    unit_l1: str
    unit_l2: str
    unit_l3: str
    keywords: Sequence[str]
    grades: Optional[Sequence[int]] = None
    weight: int = 1
    min_hits: int = 1


# Practical taxonomy table for high-school math DB tagging.
# This is intentionally concise and can be extended as data grows.
STANDARD_TAXONOMY: Dict[int, Dict[str, Dict[str, Sequence[str]]]] = {
    1: {
        "공통수학1": {
            "다항식": ("다항식의 연산", "나머지정리/인수정리", "인수분해"),
            "방정식과 부등식": ("복소수", "이차방정식", "이차방정식과 이차함수"),
            "경우의 수": ("순열", "조합"),
            "행렬": ("행렬의 뜻", "행렬의 연산"),
        },
        "공통수학2": {
            "함수": ("함수의 뜻", "이차함수", "합성함수/역함수"),
            "도형의 방정식": ("직선", "원", "도형의 이동"),
            "집합과 명제": ("집합의 연산", "명제", "조건의 활용"),
        },
    },
    2: {
        "대수": {
            "지수함수와 로그함수": ("지수", "로그", "지수/로그함수"),
            "삼각함수": ("삼각함수의 정의", "삼각함수의 그래프", "삼각함수의 활용"),
            "수열": ("등차/등비수열", "수열의 합", "점화식"),
        },
        "미적분": {
            "극한과 연속": ("함수의 극한", "함수의 연속"),
            "미분법": ("도함수", "미분계수", "도함수의 활용"),
            "적분법": ("부정적분", "정적분", "적분의 활용"),
        },
        "확률과통계": {
            "경우의 수": ("순열과 조합", "중복조합"),
            "확률": ("확률의 뜻", "조건부확률", "독립시행"),
            "통계": ("확률분포", "통계적 추정"),
        },
        "기하": {
            "이차곡선": ("포물선", "타원", "쌍곡선"),
            "평면벡터": ("벡터의 연산", "벡터의 내적"),
            "공간도형과 공간좌표": ("직선과 평면", "공간좌표"),
        },
    },
    3: {
        "미적분": {
            "극한과 연속": ("극한의 활용", "연속조건"),
            "미분법": ("매개변수 미분", "접선/법선", "최적화"),
            "적분법": ("치환적분", "부분적분", "정적분의 응용"),
        },
        "확률과통계": {
            "확률": ("조건부확률 심화", "확률분포 심화"),
            "통계": ("추정과 검정 기초",),
        },
        "기하": {
            "벡터": ("공간벡터", "벡터 방정식"),
            "공간좌표": ("공간도형의 방정식",),
        },
        "대수": {
            "수열": ("귀납적 정의", "수열의 극한적 해석"),
            "삼각함수": ("삼각함수 방정식/부등식"),
        },
    },
}


RULES: List[UnitRule] = [
    # Grade 1: common math
    UnitRule("공통수학1", "다항식", "나머지정리/인수정리", ("나머지", "인수정리", "x-1", "x^2", "x^3"), grades=(1,), weight=3),
    UnitRule("공통수학1", "다항식", "인수분해", ("인수분해", "인수인", "곱셈공식"), grades=(1,), weight=3),
    UnitRule("공통수학1", "방정식과 부등식", "복소수", ("복소수", "허수", "켤레복소수", "허수부", "실수부", "i"), grades=(1,), weight=3),
    UnitRule("공통수학1", "방정식과 부등식", "이차방정식", ("이차방정식", "판별식", "중근", "두 근", "근과 계수"), grades=(1,), weight=3),
    UnitRule("공통수학1", "경우의 수", "순열", ("순열", "경우의 수"), grades=(1, 2), weight=2),
    UnitRule("공통수학1", "경우의 수", "조합", ("조합", "경우의 수"), grades=(1, 2), weight=2),
    UnitRule("공통수학1", "방정식과 부등식", "이차방정식과 이차함수", ("이차함수", "그래프", "최댓값", "최솟값", "축"), grades=(1,), weight=3),
    UnitRule("공통수학2", "도형의 방정식", "직선", ("직선", "기울기", "거리"), grades=(1,), weight=2),
    UnitRule("공통수학2", "도형의 방정식", "원", ("원", "반지름", "원점", "중심"), grades=(1,), weight=2),
    UnitRule("공통수학2", "집합과 명제", "명제", ("명제", "필요조건", "충분조건", "참", "거짓"), grades=(1,), weight=2),
    UnitRule("공통수학2", "행렬", "행렬의 연산", ("행렬", "det", "역행렬"), grades=(1,), weight=2),

    # Grade 2~3: algebra / calculus / probability-statistics / geometry
    UnitRule("대수", "지수함수와 로그함수", "지수/로그", ("지수", "로그", "log", "밑"), grades=(2, 3), weight=3),
    UnitRule("대수", "삼각함수", "삼각함수", ("삼각함수", "sin", "cos", "tan", "라디안"), grades=(2, 3), weight=3),
    UnitRule("대수", "수열", "등차/등비수열", ("수열", "등차", "등비", "점화식", "시그마"), grades=(2, 3), weight=3),

    UnitRule("미적분", "극한과 연속", "함수의 극한", ("극한", "lim", "수렴"), grades=(2, 3), weight=3),
    UnitRule("미적분", "극한과 연속", "함수의 연속", ("연속", "불연속"), grades=(2, 3), weight=3),
    UnitRule("미적분", "미분법", "도함수", ("미분", "도함수", "미분계수", "접선", "법선"), grades=(2, 3), weight=3),
    UnitRule("미적분", "미분법", "도함수의 활용", ("증가", "감소", "극대", "극소", "최적화"), grades=(2, 3), weight=2),
    UnitRule("미적분", "적분법", "정적분/부정적분", ("적분", "정적분", "부정적분", "넓이"), grades=(2, 3), weight=3),

    UnitRule("확률과통계", "경우의 수", "순열과 조합", ("경우의 수", "순열", "조합", "중복조합"), grades=(2, 3), weight=3),
    UnitRule("확률과통계", "확률", "조건부확률", ("확률", "조건부확률", "독립", "사건"), grades=(2, 3), weight=3),
    UnitRule("확률과통계", "통계", "확률분포/통계적 추정", ("확률분포", "기댓값", "분산", "표준편차", "정규분포"), grades=(2, 3), weight=3),

    UnitRule("기하", "이차곡선", "포물선/타원/쌍곡선", ("이차곡선", "포물선", "타원", "쌍곡선"), grades=(2, 3), weight=3),
    UnitRule("기하", "평면벡터", "벡터의 연산/내적", ("벡터", "내적", "벡터의 크기"), grades=(2, 3), weight=3),
    UnitRule("기하", "공간도형과 공간좌표", "공간좌표", ("공간좌표", "평면", "직선", "공간"), grades=(2, 3), weight=2),
]


def _normalize_text(*chunks: str) -> str:
    merged = "\n".join([chunk for chunk in chunks if chunk])
    merged = merged.lower().strip()
    merged = re.sub(r"\s+", " ", merged)
    return merged


def _grade_fallback(grade: Optional[int]) -> Tuple[str, str, str]:
    if grade == 1:
        return ("공통수학1", "기타", "미분류")
    if grade in {2, 3}:
        return ("대수", "기타", "미분류")
    return ("공통수학", "기타", "미분류")


def _is_subjective(problem_no: Optional[int], qtype: str, choices_text: str) -> bool:
    if problem_no is not None and problem_no >= 100:
        return True
    qtoken = (qtype or "").lower().strip()
    if any(token in qtoken for token in ("subjective", "short", "descriptive", "서답", "단답", "서술")):
        return True
    # No choices usually means short-answer/descriptive.
    if not (choices_text or "").strip():
        return True
    return False


def _score_rule(rule: UnitRule, text: str, grade: Optional[int]) -> Tuple[int, int]:
    hits = sum(1 for keyword in rule.keywords if keyword.lower() in text)
    if hits < rule.min_hits:
        return (0, hits)

    score = hits * rule.weight
    if grade is not None and rule.grades:
        if grade in rule.grades:
            score += 2
        else:
            score -= 1
    return (max(score, 0), hits)


def _estimate_level(
    text: str,
    qtype: str,
    choices_text: str,
    solution_text: str,
    problem_no: Optional[int],
) -> int:
    level = 3

    if _is_subjective(problem_no=problem_no, qtype=qtype, choices_text=choices_text):
        level += 1

    hard_tokens = (
        "증명",
        "항상",
        "모든",
        "범위",
        "조건을 만족",
        "매개변수",
        "극한",
        "미분",
        "적분",
    )
    hard_hit = sum(1 for token in hard_tokens if token in text)
    if hard_hit >= 2:
        level += 1

    easy_tokens = ("인수분해", "나머지", "기본 계산", "단순 계산")
    if any(token in text for token in easy_tokens):
        level -= 1

    if len(solution_text) > 550:
        level += 1

    # Very short objective stems tend to be easier.
    if len(text) < 120 and not _is_subjective(problem_no, qtype, choices_text):
        level -= 1

    return max(1, min(5, level))


def classify_unit_and_level(
    question_text: str,
    choices_text: str,
    answer_text: str,
    solution_text: str,
    qtype: str = "",
    grade: Optional[int] = None,
    problem_no: Optional[int] = None,
) -> UnitLevelResult:
    text = _normalize_text(question_text, choices_text, answer_text, solution_text)
    if not text:
        l1, l2, l3 = _grade_fallback(grade)
        return UnitLevelResult(unit_l1=l1, unit_l2=l2, unit_l3=l3, level=3, reason="empty-text-fallback")

    best_rule: Optional[UnitRule] = None
    best_score = 0
    best_hits = 0

    for rule in RULES:
        score, hits = _score_rule(rule=rule, text=text, grade=grade)
        if score > best_score:
            best_score = score
            best_hits = hits
            best_rule = rule

    level = _estimate_level(
        text=text,
        qtype=qtype,
        choices_text=choices_text,
        solution_text=solution_text,
        problem_no=problem_no,
    )

    if best_rule is None:
        l1, l2, l3 = _grade_fallback(grade)
        return UnitLevelResult(
            unit_l1=l1,
            unit_l2=l2,
            unit_l3=l3,
            level=level,
            reason="keyword-fallback",
        )

    return UnitLevelResult(
        unit_l1=best_rule.unit_l1,
        unit_l2=best_rule.unit_l2,
        unit_l3=best_rule.unit_l3,
        level=level,
        reason=f"rule-score:{best_score},hits:{best_hits}",
    )
