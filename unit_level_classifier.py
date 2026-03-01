from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List, Optional, Sequence, Tuple

from unit_taxonomy import normalize_unit_triplet


@dataclass(frozen=True)
class UnitLevelResult:
    unit_l1: str
    unit_l2: str
    unit_l3: str
    level: int
    reason: str

    @property
    def unit_path(self) -> str:
        return ">".join([self.unit_l1.strip(), self.unit_l2.strip(), self.unit_l3.strip()])


@dataclass(frozen=True)
class UnitRule:
    unit_l1: str
    unit_l2: str
    unit_l3: str
    keywords: Sequence[str]
    grades: Optional[Sequence[int]] = None
    weight: int = 1
    min_hits: int = 1


def _rule(
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    keywords: Sequence[str],
    grades: Optional[Sequence[int]] = None,
    weight: int = 1,
    min_hits: int = 1,
) -> UnitRule:
    l1, l2, l3 = normalize_unit_triplet(unit_l1, unit_l2, unit_l3)
    return UnitRule(
        unit_l1=l1,
        unit_l2=l2,
        unit_l3=l3,
        keywords=keywords,
        grades=grades,
        weight=weight,
        min_hits=min_hits,
    )


RULES: List[UnitRule] = [
    # 공통수학1(2022개정)
    _rule("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산", ("다항식", "항", "계수", "전개", "정리"), grades=(1,), weight=2),
    _rule("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리", ("나머지", "인수정리", "f(", "x-a", "다항식의 나눗셈"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "1. 다항식", "1-3. 인수분해", ("인수분해", "곱셈공식", "완전제곱", "인수"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식", ("복소수", "허수", "켤레", "이차방정식", "판별식", "근과 계수", "실근"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수", ("이차함수", "포물선", "축", "최댓값", "최솟값", "그래프"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "2. 방정식과 부등식", "2-3. 여러 가지 방정식", ("삼차방정식", "사차방정식", "연립방정식", "여러 가지 방정식"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "2. 방정식과 부등식", "2-4. 여러 가지 부등식", ("부등식", "절댓값", "연립부등식", "여러 가지 부등식"), grades=(1,), weight=3),
    _rule("공통수학1(2022개정)", "2. 방정식과 부등식", "2-5. 여러 가지 방정식(교육과정 외)", ("교육과정 외",), grades=(1,), weight=5),
    _rule("공통수학1(2022개정)", "3. 경우의 수", "3-1. 합의 법칙과 곱의 법칙", ("합의 법칙", "곱의 법칙", "경우의 수"), grades=(1, 2), weight=2),
    _rule("공통수학1(2022개정)", "3. 경우의 수", "3-2. 순열과 조합", ("순열", "조합", "중복순열", "중복조합", "이항계수"), grades=(1, 2), weight=3),
    _rule("공통수학1(2022개정)", "4. 행렬", "4-1. 행렬과 그 연산", ("행렬", "역행렬", "행렬식", "det", "성분", "AB=BA"), grades=(1,), weight=4),
    # 공통수학2(2022개정)
    _rule("공통수학2(2022개정)", "1. 도형의 방정식", "1-1. 평면좌표", ("평면좌표", "좌표평면", "거리", "중점"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식", ("직선의 방정식", "직선", "기울기"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식", ("원의 방정식", "반지름", "중심", "원"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "1. 도형의 방정식", "1-4. 도형의 이동", ("도형의 이동", "평행이동", "대칭이동", "회전"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "2. 집합과 명제", "2-1. 집합", ("집합", "합집합", "교집합", "차집합", "원소"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "2. 집합과 명제", "2-2. 명제", ("명제", "필요조건", "충분조건", "대우", "역"), grades=(1,), weight=3),
    _rule("공통수학2(2022개정)", "3. 함수", "3-1. 함수", ("함수", "정의역", "치역", "함숫값", "합성함수", "역함수"), grades=(1,), weight=2),
    _rule("공통수학2(2022개정)", "3. 함수", "3-2. 유리함수", ("유리함수",), grades=(1,), weight=4),
    _rule("공통수학2(2022개정)", "3. 함수", "3-3. 무리함수", ("무리함수",), grades=(1,), weight=4),
    _rule("공통수학2(2022개정)", "3. 함수", "3-4. 여러 가지 함수의 그래프(교육과정 외)", ("교육과정 외", "여러 가지 함수의 그래프"), grades=(1,), weight=5),
    # 대수(2022개정)
    _rule("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그", ("지수", "로그", "log", "밑", "지수법칙", "로그법칙"), grades=(2, 3), weight=3),
    _rule("대수(2022개정)", "1. 지수함수와 로그함수", "1-2. 지수함수", ("지수함수",), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "1. 지수함수와 로그함수", "1-3. 로그함수", ("로그함수",), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수", ("삼각함수", "sin", "cos", "tan", "라디안"), grades=(2, 3), weight=3),
    _rule("대수(2022개정)", "2. 삼각함수", "2-2. 삼각함수의 그래프", ("삼각함수의 그래프", "주기", "위상"), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "2. 삼각함수", "2-3. 삼각함수의 활용", ("삼각함수의 활용", "삼각방정식", "삼각부등식"), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "3. 수열", "3-1. 등차수열", ("등차수열",), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "3. 수열", "3-2. 등비수열", ("등비수열",), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "3. 수열", "3-3. 수열의 합", ("수열의 합", "시그마", "Σ"), grades=(2, 3), weight=4),
    _rule("대수(2022개정)", "3. 수열", "3-4. 수학적귀납법", ("수학적귀납법", "귀납"), grades=(2, 3), weight=4),
    # 미적분 I(2022개정)
    _rule("미적분 I(2022개정)", "1. 함수의 극한과 연속", "1-1. 함수의 극한", ("극한", "lim", "수렴"), grades=(2, 3), weight=4),
    _rule("미적분 I(2022개정)", "1. 함수의 극한과 연속", "1-2. 함수의 연속", ("연속", "불연속"), grades=(2, 3), weight=4),
    _rule("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수", ("미분계수", "도함수", "미분"), grades=(2, 3), weight=3),
    _rule("미적분 I(2022개정)", "2. 미분", "2-2. 도함수의 활용", ("도함수의 활용", "접선", "증가", "감소", "극대", "극소"), grades=(2, 3), weight=4),
    _rule("미적분 I(2022개정)", "3. 적분", "3-1. 부정적분", ("부정적분",), grades=(2, 3), weight=4),
    _rule("미적분 I(2022개정)", "3. 적분", "3-2. 정적분", ("정적분",), grades=(2, 3), weight=3),
    _rule("미적분 I(2022개정)", "3. 적분", "3-3. 정적분의 활용", ("정적분의 활용", "면적", "속도", "거리"), grades=(2, 3), weight=4),
    # 확률과 통계(2022개정)
    _rule("확률과 통계(2022개정)", "1. 경우의 수", "1-1. 순열", ("순열",), grades=(2, 3), weight=4),
    _rule("확률과 통계(2022개정)", "1. 경우의 수", "1-2. 조합", ("조합", "이항정리"), grades=(2, 3), weight=4),
    _rule("확률과 통계(2022개정)", "2. 확률", "2-1. 확률의 뜻과 활용", ("확률", "사건", "표본공간", "여사건", "독립"), grades=(2, 3), weight=3),
    _rule("확률과 통계(2022개정)", "2. 확률", "2-2. 조건부 확률", ("조건부확률", "베이즈"), grades=(2, 3), weight=4),
    _rule("확률과 통계(2022개정)", "3. 통계", "3-1. 확률분포", ("확률분포", "기댓값", "분산", "표준편차", "정규분포"), grades=(2, 3), weight=4),
    _rule("확률과 통계(2022개정)", "3. 통계", "3-2. 통계적 추정", ("통계적 추정", "신뢰구간", "모평균", "가설검정", "추정"), grades=(2, 3), weight=4),
]


def _normalize_text(*chunks: str) -> str:
    merged = "\n".join([chunk for chunk in chunks if chunk])
    merged = merged.lower().strip()
    return re.sub(r"\s+", " ", merged)


def _grade_fallback(grade: Optional[int]) -> Tuple[str, str, str]:
    return normalize_unit_triplet("", "", "", grade=grade)


def _is_subjective(problem_no: Optional[int], qtype: str, choices_text: str) -> bool:
    if problem_no is not None and problem_no >= 100:
        return True
    qtoken = (qtype or "").lower().strip()
    if any(token in qtoken for token in ("subjective", "short", "descriptive", "서답", "단답", "서술")):
        return True
    return not bool((choices_text or "").strip())


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

    hard_tokens = ("증명", "항상", "모든", "범위", "조건을 만족", "극한", "미분", "적분")
    if sum(1 for token in hard_tokens if token in text) >= 2:
        level += 1

    easy_tokens = ("인수분해", "나머지", "기본 계산", "단순 계산")
    if any(token in text for token in easy_tokens):
        level -= 1

    if len(solution_text) > 550:
        level += 1

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
