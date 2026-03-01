from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class UnitL2:
    label: str
    l3: Sequence[str]


@dataclass(frozen=True)
class UnitSubject:
    label: str
    l2: Sequence[UnitL2]


UNIT_TAXONOMY: Sequence[UnitSubject] = (
    UnitSubject(
        label="공통수학1(2022개정)",
        l2=(
            UnitL2("1. 다항식", ("1-1. 다항식의 연산", "1-2. 나머지정리", "1-3. 인수분해")),
            UnitL2(
                "2. 방정식과 부등식",
                (
                    "2-1. 복소수와 이차방정식",
                    "2-2. 이차방정식과 이차함수",
                    "2-3. 여러 가지 방정식",
                    "2-4. 여러 가지 부등식",
                    "2-5. 여러 가지 방정식(교육과정 외)",
                ),
            ),
            UnitL2("3. 경우의 수", ("3-1. 합의 법칙과 곱의 법칙", "3-2. 순열과 조합")),
            UnitL2("4. 행렬", ("4-1. 행렬과 그 연산",)),
        ),
    ),
    UnitSubject(
        label="공통수학2(2022개정)",
        l2=(
            UnitL2(
                "1. 도형의 방정식",
                ("1-1. 평면좌표", "1-2. 직선의 방정식", "1-3. 원의 방정식", "1-4. 도형의 이동"),
            ),
            UnitL2("2. 집합과 명제", ("2-1. 집합", "2-2. 명제")),
            UnitL2(
                "3. 함수",
                ("3-1. 함수", "3-2. 유리함수", "3-3. 무리함수", "3-4. 여러 가지 함수의 그래프(교육과정 외)"),
            ),
        ),
    ),
    UnitSubject(
        label="대수(2022개정)",
        l2=(
            UnitL2("1. 지수함수와 로그함수", ("1-1. 지수와 로그", "1-2. 지수함수", "1-3. 로그함수")),
            UnitL2("2. 삼각함수", ("2-1. 삼각함수", "2-2. 삼각함수의 그래프", "2-3. 삼각함수의 활용")),
            UnitL2("3. 수열", ("3-1. 등차수열", "3-2. 등비수열", "3-3. 수열의 합", "3-4. 수학적귀납법")),
        ),
    ),
    UnitSubject(
        label="미적분 I(2022개정)",
        l2=(
            UnitL2("1. 함수의 극한과 연속", ("1-1. 함수의 극한", "1-2. 함수의 연속")),
            UnitL2("2. 미분", ("2-1. 미분계수와 도함수", "2-2. 도함수의 활용")),
            UnitL2("3. 적분", ("3-1. 부정적분", "3-2. 정적분", "3-3. 정적분의 활용")),
        ),
    ),
    UnitSubject(
        label="확률과 통계(2022개정)",
        l2=(
            UnitL2("1. 경우의 수", ("1-1. 순열", "1-2. 조합")),
            UnitL2("2. 확률", ("2-1. 확률의 뜻과 활용", "2-2. 조건부 확률")),
            UnitL2("3. 통계", ("3-1. 확률분포", "3-2. 통계적 추정")),
        ),
    ),
)


LEGACY_ALIASES: Dict[Tuple[str, str, str], Tuple[str, str, str]] = {
    ("공통수학1", "다항식", "나머지정리/인수정리"): ("공통수학1(2022개정)", "1. 다항식", "1-2. 나머지정리"),
    ("공통수학1", "다항식", "인수분해"): ("공통수학1(2022개정)", "1. 다항식", "1-3. 인수분해"),
    ("공통수학1", "다항식", "다항식의 연산"): ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산"),
    ("공통수학1", "방정식과 부등식", "복소수"): ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식"),
    ("공통수학1", "방정식과 부등식", "이차방정식"): ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-1. 복소수와 이차방정식"),
    ("공통수학1", "방정식과 부등식", "이차방정식과 이차함수"): ("공통수학1(2022개정)", "2. 방정식과 부등식", "2-2. 이차방정식과 이차함수"),
    ("공통수학1", "경우의 수", "순열"): ("공통수학1(2022개정)", "3. 경우의 수", "3-2. 순열과 조합"),
    ("공통수학1", "경우의 수", "조합"): ("공통수학1(2022개정)", "3. 경우의 수", "3-2. 순열과 조합"),
    ("공통수학1", "행렬", "행렬의 연산"): ("공통수학1(2022개정)", "4. 행렬", "4-1. 행렬과 그 연산"),
    ("공통수학2", "도형의 방정식", "직선"): ("공통수학2(2022개정)", "1. 도형의 방정식", "1-2. 직선의 방정식"),
    ("공통수학2", "도형의 방정식", "원"): ("공통수학2(2022개정)", "1. 도형의 방정식", "1-3. 원의 방정식"),
    ("공통수학2", "도형의 방정식", "도형의 이동"): ("공통수학2(2022개정)", "1. 도형의 방정식", "1-4. 도형의 이동"),
    ("공통수학2", "집합과 명제", "집합"): ("공통수학2(2022개정)", "2. 집합과 명제", "2-1. 집합"),
    ("공통수학2", "집합과 명제", "명제"): ("공통수학2(2022개정)", "2. 집합과 명제", "2-2. 명제"),
    ("공통수학2", "함수", "함수의 뜻"): ("공통수학2(2022개정)", "3. 함수", "3-1. 함수"),
    ("공통수학2", "함수", "이차함수"): ("공통수학2(2022개정)", "3. 함수", "3-1. 함수"),
    ("공통수학2", "함수", "합성함수/역함수"): ("공통수학2(2022개정)", "3. 함수", "3-1. 함수"),
    ("대수", "지수함수와 로그함수", "지수/로그"): ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    ("대수", "지수함수와 로그함수", "지수"): ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    ("대수", "지수함수와 로그함수", "로그"): ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그"),
    ("대수", "삼각함수", "삼각함수"): ("대수(2022개정)", "2. 삼각함수", "2-1. 삼각함수"),
    ("대수", "삼각함수", "삼각함수의 그래프"): ("대수(2022개정)", "2. 삼각함수", "2-2. 삼각함수의 그래프"),
    ("대수", "삼각함수", "삼각함수의 활용"): ("대수(2022개정)", "2. 삼각함수", "2-3. 삼각함수의 활용"),
    ("대수", "수열", "등차/등비수열"): ("대수(2022개정)", "3. 수열", "3-1. 등차수열"),
    ("대수", "수열", "수열의 합"): ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    ("대수", "수열", "점화식"): ("대수(2022개정)", "3. 수열", "3-3. 수열의 합"),
    ("미적분", "극한과 연속", "함수의 극한"): ("미적분 I(2022개정)", "1. 함수의 극한과 연속", "1-1. 함수의 극한"),
    ("미적분", "극한과 연속", "함수의 연속"): ("미적분 I(2022개정)", "1. 함수의 극한과 연속", "1-2. 함수의 연속"),
    ("미적분", "미분법", "도함수"): ("미적분 I(2022개정)", "2. 미분", "2-1. 미분계수와 도함수"),
    ("미적분", "미분법", "도함수의 활용"): ("미적분 I(2022개정)", "2. 미분", "2-2. 도함수의 활용"),
    ("미적분", "적분법", "정적분/부정적분"): ("미적분 I(2022개정)", "3. 적분", "3-2. 정적분"),
    ("미적분", "적분법", "적분의 활용"): ("미적분 I(2022개정)", "3. 적분", "3-3. 정적분의 활용"),
    ("확률과통계", "경우의 수", "순열과 조합"): ("확률과 통계(2022개정)", "1. 경우의 수", "1-1. 순열"),
    ("확률과통계", "확률", "조건부확률"): ("확률과 통계(2022개정)", "2. 확률", "2-2. 조건부 확률"),
    ("확률과통계", "통계", "확률분포/통계적 추정"): ("확률과 통계(2022개정)", "3. 통계", "3-2. 통계적 추정"),
}


def _compact(text: str) -> str:
    token = (text or "").strip()
    token = token.replace("Ⅰ", "I")
    token = re.sub(r"\s+", "", token)
    return token


def make_unit_path(unit_l1: str, unit_l2: str, unit_l3: str) -> str:
    return ">".join([unit_l1.strip(), unit_l2.strip(), unit_l3.strip()])


def iter_leaf_units() -> List[Tuple[str, str, str]]:
    rows: List[Tuple[str, str, str]] = []
    for subject in UNIT_TAXONOMY:
        for l2 in subject.l2:
            for l3 in l2.l3:
                rows.append((subject.label, l2.label, l3))
    return rows


LEAF_TRIPLETS = iter_leaf_units()
LEAF_PATHS = [make_unit_path(l1, l2, l3) for l1, l2, l3 in LEAF_TRIPLETS]
LEAF_SET = set(LEAF_PATHS)
LEAF_BY_COMPACT = {make_unit_path(_compact(l1), _compact(l2), _compact(l3)): (l1, l2, l3) for l1, l2, l3 in LEAF_TRIPLETS}


def _subject_node_id(subject: str) -> str:
    return f"S::{subject}"


def _l2_node_id(subject: str, l2: str) -> str:
    return f"L2::{subject}>{l2}"


def _l3_node_id(subject: str, l2: str, l3: str) -> str:
    return f"L3::{make_unit_path(subject, l2, l3)}"


def subject_node_ids() -> List[str]:
    return [_subject_node_id(subject.label) for subject in UNIT_TAXONOMY]


def unit_tree_for_ui() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for subject in UNIT_TAXONOMY:
        l2_rows: List[Dict[str, object]] = []
        for l2 in subject.l2:
            l3_rows = []
            for l3 in l2.l3:
                path = make_unit_path(subject.label, l2.label, l3)
                l3_rows.append(
                    {
                        "id": _l3_node_id(subject.label, l2.label, l3),
                        "label": l3,
                        "path": path,
                    }
                )
            l2_rows.append(
                {
                    "id": _l2_node_id(subject.label, l2.label),
                    "label": l2.label,
                    "children": l3_rows,
                }
            )
        rows.append(
            {
                "id": _subject_node_id(subject.label),
                "label": subject.label,
                "children": l2_rows,
            }
        )
    return rows


NODE_TO_LEAF_PATHS: Dict[str, List[str]] = {}
for subject in UNIT_TAXONOMY:
    subject_leafs: List[str] = []
    for l2 in subject.l2:
        l2_leafs: List[str] = []
        for l3 in l2.l3:
            path = make_unit_path(subject.label, l2.label, l3)
            l2_leafs.append(path)
            NODE_TO_LEAF_PATHS[_l3_node_id(subject.label, l2.label, l3)] = [path]
        NODE_TO_LEAF_PATHS[_l2_node_id(subject.label, l2.label)] = l2_leafs
        subject_leafs.extend(l2_leafs)
    NODE_TO_LEAF_PATHS[_subject_node_id(subject.label)] = subject_leafs


def expand_unit_nodes_to_leaf_paths(selected_nodes: Iterable[str]) -> List[str]:
    rows: List[str] = []
    seen = set()
    for node in selected_nodes:
        for path in NODE_TO_LEAF_PATHS.get(str(node).strip(), []):
            if path in seen:
                continue
            seen.add(path)
            rows.append(path)
    return rows


def default_selected_unit_nodes() -> List[str]:
    return subject_node_ids()


def normalize_unit_triplet(
    unit_l1: str,
    unit_l2: str,
    unit_l3: str,
    unit_path: str = "",
    grade: Optional[int] = None,
) -> Tuple[str, str, str]:
    l1 = (unit_l1 or "").strip()
    l2 = (unit_l2 or "").strip()
    l3 = (unit_l3 or "").strip()

    if l1 and l2 and l3:
        direct = make_unit_path(l1, l2, l3)
        if direct in LEAF_SET:
            return (l1, l2, l3)
        alias = LEGACY_ALIASES.get((l1, l2, l3))
        if alias:
            return alias

        compact_key = make_unit_path(_compact(l1), _compact(l2), _compact(l3))
        matched = LEAF_BY_COMPACT.get(compact_key)
        if matched:
            return matched

    token = (unit_path or "").strip()
    if token:
        pieces = [item.strip() for item in token.split(">") if item.strip()]
        if len(pieces) == 3:
            return normalize_unit_triplet(pieces[0], pieces[1], pieces[2], "", grade=grade)

    # Grade fallback always returns one of fixed taxonomy leaves.
    if grade == 1:
        return ("공통수학1(2022개정)", "1. 다항식", "1-1. 다항식의 연산")
    if grade == 2:
        return ("대수(2022개정)", "1. 지수함수와 로그함수", "1-1. 지수와 로그")
    if grade == 3:
        return ("미적분 I(2022개정)", "1. 함수의 극한과 연속", "1-1. 함수의 극한")
    return LEAF_TRIPLETS[0]


def normalize_unit_path(unit_path: str, grade: Optional[int] = None) -> str:
    l1, l2, l3 = normalize_unit_triplet("", "", "", unit_path=unit_path, grade=grade)
    return make_unit_path(l1, l2, l3)
