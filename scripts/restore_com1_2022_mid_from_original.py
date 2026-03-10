from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PROBLEM_ROOT = ROOT / "db" / "problems"
PDF_ROOT = ROOT / "db" / "original"

TARGET_SCHOOLS = ("JEW", "JJ", "SY")
TARGET_ID_RE = re.compile(r"^(JEW|JJ|SY)-2022-G1-S1-MID-(\d{3})$")
IMAGE_HTML = '<img src="assets/scan.png" alt="문항 원본" style="width:100% !important; max-width:100% !important; height:auto;" />'

QUESTION_START_PATTERNS = {
    "JEW": [
        (re.compile(r"^(\d+)\."), "objective"),
        (re.compile(r"^서(\d+)\."), "subjective"),
    ],
    "JJ": [
        (re.compile(r"^(\d+)\."), "objective"),
        (re.compile(r"^(?:서답형|서술형)(\d+)\)"), "subjective"),
    ],
    "SY": [
        (re.compile(r"^(\d+)\."), "objective"),
        (re.compile(r"^\[(?:서답형|서술형)(\d+)\]"), "subjective"),
    ],
}

OBJECTIVE_ANSWERS = {
    "JEW": {
        "001": "③",
        "002": "④",
        "003": "⑤",
        "004": "②",
        "005": "③",
        "006": "①",
        "007": "④",
        "008": "①",
        "009": "③",
        "010": "②",
        "011": "④",
        "012": "⑤",
        "013": "①",
        "014": "②",
        "015": "②",
        "016": "⑤",
        "017": "③",
    },
    "JJ": {
        "001": "②",
        "002": "③",
        "003": "④",
        "004": "①",
        "005": "①",
        "006": "③",
        "007": "②",
        "008": "⑤",
        "009": "②",
        "010": "②",
        "011": "①",
        "012": "⑤",
        "013": "④",
        "014": "③",
        "015": "①",
    },
    "SY": {
        "001": "④",
        "002": "④",
        "003": "④",
        "004": "②",
        "005": "③",
        "006": "②",
        "007": "⑤",
        "008": "②",
        "009": "④",
        "010": "②",
        "011": "①",
        "012": "①",
        "013": "⑤",
        "014": "③",
        "015": "①",
    },
}

SPECIAL_ANSWERS = {
    "JEW-2022-G1-S1-MID-106": (
        "(1) 가격: $600+x$, 판매량: $800-x$\n\n"
        "(2) 하루 판매액: $R(x)=(600+x)(800-x)=-x^2+200x+480000$\n\n"
        "(3) 최대가 되는 가격: $700$원\n\n"
        "(4) 최대 하루 판매액: $490000$원"
    ),
}

SPECIAL_SOLUTIONS = {
    "JJ-2022-G1-S1-MID-104": (
        "$x\\ge 0$일 때\n"
        "\\[\n"
        "y=x^2-2|x|-1=x^2-2x-1=(x-1)^2-2\n"
        "\\]\n"
        "$x<0$일 때\n"
        "\\[\n"
        "y=x^2-2|x|-1=x^2+2x-1=(x+1)^2-2\n"
        "\\]\n"
        "\\[\n"
        "0\\le x\\le 3 \\text{ 에서 최솟값은 } -2, \\text{ 최댓값은 } 2\n"
        "\\]\n"
        "\\[\n"
        "-2\\le x<0 \\text{ 에서 최솟값은 } -2, \\text{ 최댓값은 } 1\n"
        "\\]\n"
        "따라서 전체 범위에서\n"
        "\\[\n"
        "\\alpha=2,\\qquad \\beta=-2\n"
        "\\]\n"
        "이므로\n"
        "\\[\n"
        "\\alpha-\\beta=2-(-2)=4\n"
        "\\]\n"
        "이다.\n\n"
        "따라서 답은 $4$이다."
    ),
    "JJ-2022-G1-S1-MID-105": (
        "(1) 한 근이 $2$이므로\n"
        "\\[\n"
        "4(\\alpha-1)-2(\\alpha^2+1)+2(\\alpha+1)=0\n"
        "\\]\n"
        "\\[\n"
        "\\alpha^2-3\\alpha+2=0\n"
        "\\]\n"
        "\\[\n"
        "\\alpha=1 \\text{ 또는 } 2\n"
        "\\]\n"
        "$\\alpha\\ne 1$이므로 $\\alpha=2$이다.\n"
        "따라서\n"
        "\\[\n"
        "x^2-5x+6=0\n"
        "\\]\n"
        "이므로 다른 한 근은 $3$이다.\n\n"
        "(2)\n"
        "\\[\n"
        "a\\star a=a^2-2a,\\qquad 2\\star a=2a-2-a=a-2\n"
        "\\]\n"
        "이므로\n"
        "\\[\n"
        "a^2-2a=|a-2|\n"
        "\\]\n"
        "\\[\n"
        "a(a-2)=|a-2|\n"
        "\\]\n"
        "$a\\ge 2$일 때\n"
        "\\[\n"
        "a(a-2)=a-2\n"
        "\\]\n"
        "\\[\n"
        "(a-2)(a-1)=0\n"
        "\\]\n"
        "이므로 $a=2$이다.\n"
        "$a<2$일 때\n"
        "\\[\n"
        "a(a-2)=2-a=-(a-2)\n"
        "\\]\n"
        "\\[\n"
        "(a-2)(a+1)=0\n"
        "\\]\n"
        "이므로 $a=-1$이다.\n"
        "따라서 답은 다음과 같다.\n\n"
        "(1) $3$\n\n"
        "(2) $-1,\\ 2$"
    ),
}


@dataclass
class QuestionRegion:
    problem_id: str
    page_index: int
    x0: float
    y0: float
    x1: float
    y1: float


def normalize_block_text(text: str) -> str:
    return " ".join(text.strip().split())


def detect_problem_id(school: str, text: str) -> str | None:
    sample = normalize_block_text(text)
    for pattern, kind in QUESTION_START_PATTERNS[school]:
        match = pattern.match(sample)
        if not match:
            continue
        no = int(match.group(1))
        if kind == "objective":
            return f"{school}-2022-G1-S1-MID-{no:03d}"
        return f"{school}-2022-G1-S1-MID-{100 + no:03d}"
    return None


def collect_question_regions(school: str) -> dict[str, QuestionRegion]:
    pdf_path = PDF_ROOT / f"{school}.2022.G1.S1.MID.COM1.pdf"
    doc = fitz.open(pdf_path)
    regions: dict[str, QuestionRegion] = {}

    for page_index, page in enumerate(doc):
        blocks = []
        for raw in page.get_text("blocks"):
            x0, y0, x1, y1, text, *_ = raw
            sample = normalize_block_text(text)
            if not sample:
                continue
            problem_id = detect_problem_id(school, sample)
            blocks.append(
                {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "text": sample,
                    "problem_id": problem_id,
                }
            )

        footer_y = page.rect.height - 20
        for block in blocks:
            if block["text"].startswith("- ") and block["y0"] > page.rect.height * 0.9:
                footer_y = min(footer_y, block["y0"] - 8)

        starts = [b for b in blocks if b["problem_id"]]
        by_column = {"left": [], "right": []}
        mid = page.rect.width / 2
        for start in starts:
            side = "left" if start["x0"] < mid else "right"
            by_column[side].append(start)

        for side, items in by_column.items():
            items.sort(key=lambda item: item["y0"])
            for idx, item in enumerate(items):
                next_y = items[idx + 1]["y0"] - 10 if idx + 1 < len(items) else footer_y
                x0 = 15 if side == "left" else mid + 5
                x1 = mid - 5 if side == "left" else page.rect.width - 10
                regions[item["problem_id"]] = QuestionRegion(
                    problem_id=item["problem_id"],
                    page_index=page_index,
                    x0=x0,
                    y0=max(0, item["y0"] - 8),
                    x1=x1,
                    y1=min(page.rect.height - 10, next_y),
                )

    return regions


def ensure_scan_asset(text: str) -> str:
    match = re.search(r"(?ms)^assets:\n((?:- .*\n)+)", text)
    if not match:
        return text
    items = [line.rstrip() for line in match.group(1).splitlines() if line.strip()]
    if "- assets/scan.png" not in items:
        items.insert(0, "- assets/scan.png")
    replacement = "assets:\n" + "\n".join(items) + "\n"
    return text[: match.start()] + replacement + text[match.end() :]


def ensure_answer_section(text: str, answer: str) -> str:
    if "## Answer\n" in text:
        return replace_section(text, "Answer", answer, ["Solution"])
    marker = "\n## Solution\n"
    if marker not in text:
        return text.rstrip() + f"\n\n## Answer\n{answer}\n"
    return text.replace(marker, f"\n## Answer\n{answer}\n{marker}", 1)


def replace_section(text: str, section: str, new_body: str, next_sections: list[str]) -> str:
    if next_sections:
        next_pattern = "|".join(re.escape(f"\n## {name}") for name in next_sections)
        regex = re.compile(rf"(?s)(## {re.escape(section)}\n)(.*?)(?={next_pattern}|\Z)")
    else:
        regex = re.compile(rf"(?s)(## {re.escape(section)}\n)(.*)\Z")
    return regex.sub(lambda m: m.group(1) + new_body.rstrip() + "\n", text, count=1)


def clean_inline_line(line: str) -> str:
    prefix_match = re.match(r"\s*(\d+\.)", line)
    prefix = prefix_match.group(1) + " " if prefix_match else ""
    formulas = re.findall(r"\$[^$]+\$", line)
    if formulas:
        return prefix + " ".join(formulas)
    return ""


def clean_solution(solution: str, answer: str, is_objective: bool) -> str:
    lines = solution.splitlines()
    cleaned: list[str] = []
    in_display = False

    for line in lines:
        stripped = line.rstrip()
        plain = stripped.strip()
        if not plain:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        if plain.startswith(r"\["):
            in_display = True
            cleaned.append(stripped)
            continue
        if in_display:
            cleaned.append(stripped)
            if plain.endswith(r"\]") or plain == r"\]":
                in_display = False
            continue

        if plain.startswith("<") and plain.endswith(">") and "?" not in plain:
            cleaned.append(stripped)
            continue

        if "?" in plain:
            recovered = clean_inline_line(stripped)
            if recovered:
                cleaned.append(recovered)
            continue

        cleaned.append(stripped)

    normalized: list[str] = []
    for line in cleaned:
        if line == "" and (not normalized or normalized[-1] == ""):
            continue
        normalized.append(line)

    while normalized and normalized[-1] == "":
        normalized.pop()

    body = "\n".join(normalized).strip()

    if is_objective:
        tail = f"따라서 정답은 {answer.strip()}이다."
    else:
        ans = answer.strip()
        if "\n" in ans or ans.startswith("(1)"):
            tail = f"따라서 답은 다음과 같다.\n\n{ans}"
        else:
            tail = f"따라서 답은 {ans}이다."

    if not body:
        return tail
    return body + "\n\n" + tail


def resolve_answer(problem_id: str, text: str, kind: str) -> str:
    if problem_id in SPECIAL_ANSWERS:
        return SPECIAL_ANSWERS[problem_id]
    answer_match = re.search(r"(?s)## Answer\n(.*?)(?=\n## Solution|\Z)", text)
    answer = answer_match.group(1).strip() if answer_match else ""
    if answer:
        return answer
    if kind == "objective":
        school = problem_id.split("-", 1)[0]
        numeric = problem_id.rsplit("-", 1)[-1]
        return OBJECTIVE_ANSWERS[school][numeric]
    return ""


def render_question_images() -> None:
    region_map = {school: collect_question_regions(school) for school in TARGET_SCHOOLS}

    for problem_dir in sorted(PROBLEM_ROOT.iterdir()):
        if not problem_dir.is_dir():
            continue
        problem_id = problem_dir.name
        match = TARGET_ID_RE.match(problem_id)
        if not match:
            continue
        school = match.group(1)
        if school not in region_map:
            continue
        region = region_map[school].get(problem_id)
        if not region:
            continue

        pdf_path = PDF_ROOT / f"{school}.2022.G1.S1.MID.COM1.pdf"
        doc = fitz.open(pdf_path)
        page = doc[region.page_index]
        rect = fitz.Rect(region.x0, region.y0, region.x1, region.y1)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect, alpha=False)

        assets_dir = problem_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        pix.save(assets_dir / "scan.png")


def rewrite_problem_files() -> None:
    for problem_dir in sorted(PROBLEM_ROOT.iterdir()):
        if not problem_dir.is_dir():
            continue
        problem_id = problem_dir.name
        match = TARGET_ID_RE.match(problem_id)
        if not match:
            continue
        school = match.group(1)

        path = problem_dir / "problem.md"
        text = path.read_text(encoding="utf-8")
        text = ensure_scan_asset(text)
        front_match = re.match(r"(?s)\A---\n.*?\n---\n*", text)
        if not front_match:
            continue
        front = front_match.group(0).rstrip() + "\n"
        kind_match = re.search(r"^source_question_kind:\s*(objective|subjective)\s*$", text, re.M)
        kind = kind_match.group(1) if kind_match else ("subjective" if problem_id.endswith(tuple(f"{i:03d}" for i in range(101, 200))) else "objective")
        is_objective = kind == "objective"
        answer = resolve_answer(problem_id, text, kind)

        solution_match = re.search(r"(?s)## Solution\n(.*)$", text)
        solution = solution_match.group(1).strip() if solution_match else ""
        solution = re.split(r"\n\s*따라서 (?:정답은|답은)", solution, 1)[0].strip()

        cleaned_solution = clean_solution(solution, answer, is_objective)
        if problem_id in SPECIAL_SOLUTIONS:
            cleaned_solution = SPECIAL_SOLUTIONS[problem_id]
        body = (
            "## Q\n"
            f"{IMAGE_HTML}\n\n"
            "## Choices\n\n"
            "## Answer\n"
            f"{answer.strip()}\n\n"
            "## Solution\n"
            f"{cleaned_solution.strip()}\n"
        )
        path.write_text(front + body, encoding="utf-8")


def main() -> None:
    render_question_images()
    rewrite_problem_files()


if __name__ == "__main__":
    main()
