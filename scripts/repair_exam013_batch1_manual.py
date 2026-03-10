from __future__ import annotations

import ast
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parser import _read_text_with_fallback, parse_problem_file

PROBLEMS = ROOT / "db" / "problems"

Q_PATTERN = re.compile(r"(?ms)^## Q\n.*?(?=^## Choices\n)")
CHOICES_PATTERN = re.compile(r"(?ms)^## Choices\n.*?(?=^## Answer\n)")
ANSWER_PATTERN = re.compile(r"(?ms)^## Answer\n.*?(?=^## Solution\n)")
SOLUTION_PATTERN = re.compile(r"(?ms)^## Solution\n.*\Z")
ANSWER_FROM_SOLUTION_RE = re.compile(r"정답은\s*\$?([①-⑤0-9\-\+\(\)a-zA-Z]+)\$?")


def _load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_fix_2024_data() -> dict[str, dict[str, str]]:
    src = (ROOT / "scripts" / "fix_2024_manual_quality.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "DATA" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise RuntimeError("DATA not found in fix_2024_manual_quality.py")


def _pid_from_meta(meta: dict[str, Any], source_no: int, kind: str) -> str:
    number = source_no + (int(meta["subjective_offset"]) if kind == "subjective" else 0)
    return (
        f"{meta['school']}-{meta['year']}-G{meta['grade']}-S{meta['semester']}-"
        f"{meta['exam']}-{number:03d}"
    )


def _normalize_choices(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw.strip()
    return "\n".join(str(item).strip() for item in raw).strip()


def _extract_answer_from_solution(solution: str) -> str:
    match = ANSWER_FROM_SOLUTION_RE.search(solution)
    return match.group(1).strip() if match else ""


def _rewrite_problem(pid: str, q: str, choices: str, answer: str, solution: str) -> None:
    path = PROBLEMS / pid / "problem.md"
    text, _ = _read_text_with_fallback(path)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("- assets/scan.png\n", "")
    text = Q_PATTERN.sub(lambda _m: f"## Q\n{q.strip()}\n\n", text)
    text = CHOICES_PATTERN.sub(lambda _m: f"## Choices\n{choices.strip()}\n\n", text)
    text = ANSWER_PATTERN.sub(lambda _m: f"## Answer\n{answer.strip()}\n\n", text)
    text = SOLUTION_PATTERN.sub(lambda _m: f"## Solution\n{solution.strip()}\n", text)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    targets: dict[str, dict[str, str]] = {}

    sy2023 = _load_module("sy2023_mid_manual", "scripts/ingest_sy_2023_mid_manual.py")
    for row in sy2023.ROWS:
        pid = _pid_from_meta(sy2023.META, int(row["source_no"]), str(row["kind"]))
        targets[pid] = {
            "q": str(row["question"]).strip(),
            "choices": _normalize_choices(row["choices"]),
            "answer": str(row["answer"]).strip(),
            "solution": str(row["solution"]).strip(),
        }

    jj25 = _load_module("jj2025_mid_manual", "scripts/ingest_jj_2025_g1_mid_com1_manual_missing.py")
    for row in jj25.ROWS:
        pid = _pid_from_meta(jj25.META, int(row.source_no), str(row.kind))
        targets[pid] = {
            "q": str(row.q).strip(),
            "choices": _normalize_choices(row.choices),
            "answer": str(row.answer).strip(),
            "solution": str(row.solution).strip(),
        }

    mid2023 = _load_module(
        "jj_jew_2023_mid_manual", "scripts/ingest_jj_jew_2023_mid_com1_missing_manual.py"
    )
    for item in mid2023.DATA:
        if item.pid == "JJ-2023-G1-S1-MID-106":
            targets[item.pid] = {
                "q": str(item.question).strip(),
                "choices": str(item.choices).strip(),
                "answer": str(item.answer).strip(),
                "solution": str(item.solution).strip(),
            }

    data2024 = _load_fix_2024_data()
    for pid in [
        "JJ-2024-G1-S1-MID-002",
        "JJ-2024-G1-S1-MID-003",
        "JJ-2024-G1-S1-MID-005",
        "JJ-2024-G1-S1-MID-008",
    ]:
        parsed = parse_problem_file(PROBLEMS / pid / "problem.md")
        solution = str(data2024[pid]["Solution"]).strip()
        answer = parsed.answer.strip() or _extract_answer_from_solution(solution)
        targets[pid] = {
            "q": str(data2024[pid]["Q"]).strip(),
            "choices": _normalize_choices(data2024[pid].get("Choices")),
            "answer": answer,
            "solution": solution,
        }

    ordered_pids = [
        *[f"SY-2023-G1-S1-MID-{n:03d}" for n in range(1, 16)],
        *[f"SY-2023-G1-S1-MID-{n:03d}" for n in range(101, 106)],
        "JJ-2023-G1-S1-MID-106",
        "JJ-2024-G1-S1-MID-002",
        "JJ-2024-G1-S1-MID-003",
        "JJ-2024-G1-S1-MID-005",
        "JJ-2024-G1-S1-MID-008",
        "JJ-2025-G1-S1-MID-002",
        "JJ-2025-G1-S1-MID-003",
        "JJ-2025-G1-S1-MID-004",
        "JJ-2025-G1-S1-MID-005",
        "JJ-2025-G1-S1-MID-006",
        "JJ-2025-G1-S1-MID-007",
        "JJ-2025-G1-S1-MID-011",
        "JJ-2025-G1-S1-MID-012",
        "JJ-2025-G1-S1-MID-105",
    ]

    for pid in ordered_pids:
        payload = targets[pid]
        _rewrite_problem(
            pid=pid,
            q=payload["q"],
            choices=payload["choices"],
            answer=payload["answer"],
            solution=payload["solution"],
        )
        print(f"updated {pid}")


if __name__ == "__main__":
    main()
