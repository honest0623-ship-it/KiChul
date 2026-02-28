from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import yaml

from parser import parse_problem_file
from unit_level_classifier import classify_unit_and_level


def _collect_problem_files(root: Path, pattern: str | None) -> List[Path]:
    if pattern:
        folders = sorted([p for p in root.glob(pattern) if p.is_dir()], key=lambda p: p.name)
    else:
        folders = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name)
    return [folder / "problem.md" for folder in folders if (folder / "problem.md").exists()]


def _build_front_matter(front: Dict[str, object], classified) -> Dict[str, object]:
    updated = dict(front)
    updated["difficulty"] = str(classified.level)
    updated["level"] = int(classified.level)
    updated["unit"] = classified.unit_path
    updated["unit_l1"] = classified.unit_l1
    updated["unit_l2"] = classified.unit_l2
    updated["unit_l3"] = classified.unit_l3
    return updated


def _rewrite_problem_md(path: Path, front: Dict[str, object], parsed) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{parsed.q.strip()}\n\n"
        f"## Choices\n{parsed.choices.strip()}\n\n"
        f"## Answer\n{parsed.answer.strip()}\n\n"
        f"## Solution\n{parsed.solution.strip()}\n"
    )
    text = f"---\n{front_text}\n---\n\n{body}"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill unit hierarchy and level into problem.md files.")
    parser.add_argument("--root", default="db/problems", help="Problems root directory.")
    parser.add_argument("--pattern", default="", help="Optional folder glob pattern, e.g. HN-2025-G1-S1-MID-*")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing unit/level values.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] Root not found: {root}")
        return 1

    files = _collect_problem_files(root, args.pattern.strip() or None)
    if not files:
        print("[INFO] No problem.md files found.")
        return 0

    updated = 0
    skipped = 0
    for path in files:
        try:
            parsed = parse_problem_file(path)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[WARN] {path}: parse failed ({exc})")
            skipped += 1
            continue

        front = dict(parsed.front_matter or {})
        has_unit = bool(str(front.get("unit_l1", "")).strip()) and bool(str(front.get("unit_l2", "")).strip())
        has_level = str(front.get("level", "")).strip().isdigit() or str(front.get("difficulty", "")).strip().isdigit()
        if not args.overwrite and has_unit and has_level:
            skipped += 1
            continue

        folder_no = None
        tail = parsed.folder_id.rsplit("-", 1)[-1]
        if tail.isdigit():
            folder_no = int(tail)

        classified = classify_unit_and_level(
            question_text=parsed.q,
            choices_text=parsed.choices,
            answer_text=parsed.answer,
            solution_text=parsed.solution,
            qtype=str(front.get("type", "")),
            grade=int(str(front.get("grade", "0") or "0") or 0) or None,
            problem_no=folder_no,
        )
        next_front = _build_front_matter(front, classified)

        if args.dry_run:
            print(f"[DRY] {parsed.folder_id}: {classified.unit_path} | level {classified.level}")
            updated += 1
            continue

        _rewrite_problem_md(path, next_front, parsed)
        print(f"[OK] {parsed.folder_id}: {classified.unit_path} | level {classified.level}")
        updated += 1

    print(f"[DONE] updated={updated}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

