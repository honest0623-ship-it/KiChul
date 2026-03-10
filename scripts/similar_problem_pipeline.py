from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import fnmatch
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any, Dict, Iterable, List, Sequence, Tuple
from difflib import SequenceMatcher

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from parser import ParsedProblem, parse_problem_file  # pylint: disable=wrong-import-position


DEFAULT_PROBLEMS_ROOT = BASE_DIR / "db" / "problems"
DEFAULT_GENERATED_ROOT = BASE_DIR / "db" / "generated_candidates"
PROBLEM_ID_RE = re.compile(
    r"^(?P<prefix>.+)-(?P<number>\d{3})$"
)
SECTION_NAMES = ("q", "choices", "answer", "solution")
DRAFT_TOKEN = "[DRAFT]"


@dataclass
class CandidateValidation:
    candidate_id: str
    ok: bool
    errors: List[str]
    warnings: List[str]
    similarity_ratio: float


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def sanitize_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return token.strip("_")


def parse_id_tokens(raw: str) -> List[str]:
    if not raw:
        return []
    tokens = re.split(r"[\s,]+", raw.strip())
    return [item for item in tokens if item]


def list_problem_ids(root: Path, pattern: str = "*") -> List[str]:
    if not root.is_dir():
        return []
    rows: List[str] = []
    for folder in sorted(root.iterdir(), key=lambda p: p.name):
        if not folder.is_dir():
            continue
        if not fnmatch.fnmatch(folder.name, pattern):
            continue
        if not (folder / "problem.md").is_file():
            continue
        if not PROBLEM_ID_RE.match(folder.name):
            continue
        rows.append(folder.name)
    return rows


def collect_seed_ids(root: Path, raw_seed_ids: str, pattern: str, limit: int) -> List[str]:
    if raw_seed_ids.strip():
        seeds = parse_id_tokens(raw_seed_ids)
        unique: List[str] = []
        seen = set()
        for seed in seeds:
            if seed in seen:
                continue
            seen.add(seed)
            unique.append(seed)
        return unique[:limit] if limit > 0 else unique

    ids = list_problem_ids(root, pattern=pattern or "*")
    if limit > 0:
        return ids[:limit]
    return ids


def load_problem(path: Path) -> ParsedProblem:
    return parse_problem_file(path / "problem.md")


def write_problem_md(path: Path, front: Dict[str, Any], parsed: Dict[str, str]) -> None:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    body = (
        f"## Q\n{parsed.get('q', '').strip()}\n\n"
        f"## Choices\n{parsed.get('choices', '').strip()}\n\n"
        f"## Answer\n{parsed.get('answer', '').strip()}\n\n"
        f"## Solution\n{parsed.get('solution', '').strip()}\n"
    )
    path.write_text(f"---\n{front_text}\n---\n\n{body}", encoding="utf-8")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def prompt_text(seed_id: str, variant_no: int, seed: ParsedProblem) -> str:
    return (
        "# Similar Problem Draft Task\n\n"
        f"- Seed Problem ID: `{seed_id}`\n"
        f"- Variant Index: `{variant_no}`\n\n"
        "## Constraints\n\n"
        "1. Keep same curriculum level and topic granularity.\n"
        "2. Create a new problem, not a paraphrase-only copy.\n"
        "3. Keep final answer and full solution internally consistent.\n"
        "4. Keep latex clean for markdown rendering.\n"
        "5. If objective, keep 5 options.\n\n"
        "## Seed Q\n\n"
        f"{seed.q.strip()}\n\n"
        "## Seed Choices\n\n"
        f"{seed.choices.strip()}\n\n"
        "## Seed Answer\n\n"
        f"{seed.answer.strip()}\n\n"
        "## Seed Solution\n\n"
        f"{seed.solution.strip()}\n"
    )


def source_snapshot_text(seed_id: str, seed: ParsedProblem) -> str:
    return (
        f"# Source Snapshot: {seed_id}\n\n"
        "## Q\n\n"
        f"{seed.q.strip()}\n\n"
        "## Choices\n\n"
        f"{seed.choices.strip()}\n\n"
        "## Answer\n\n"
        f"{seed.answer.strip()}\n\n"
        "## Solution\n\n"
        f"{seed.solution.strip()}\n"
    )


def objective_like(front: Dict[str, Any], problem_id: str) -> bool:
    kind = str(front.get("source_question_kind", "")).strip().lower()
    if kind in {"objective", "obj", "multiple"}:
        return True
    if kind in {"subjective", "subj", "essay"}:
        return False
    matched = PROBLEM_ID_RE.match(problem_id)
    if not matched:
        return True
    return int(matched.group("number")) < 100


def count_choice_lines(choices_text: str) -> int:
    lines = [line.strip() for line in choices_text.splitlines() if line.strip()]
    if not lines:
        return 0
    pattern = re.compile(r"^(?:[1-9][\).]|[①-⑩]|[-*])\s*")
    return sum(1 for line in lines if pattern.match(line))


def normalize_for_similarity(text: str) -> str:
    token = re.sub(r"\s+", " ", (text or "").strip())
    return token.lower()


def latex_balance_issues(text: str) -> List[str]:
    issues: List[str] = []
    dollar_count = len(re.findall(r"(?<!\\)\$", text or ""))
    if dollar_count % 2 != 0:
        issues.append("Unbalanced inline/display `$` delimiters.")
    if (text or "").count("\\(") != (text or "").count("\\)"):
        issues.append("Unbalanced `\\(` and `\\)` delimiters.")
    if (text or "").count("\\[") != (text or "").count("\\]"):
        issues.append("Unbalanced `\\[` and `\\]` delimiters.")
    return issues


def candidate_dirs(batch_dir: Path) -> List[Path]:
    if not batch_dir.is_dir():
        return []
    rows: List[Path] = []
    for child in sorted(batch_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if (child / "problem.md").is_file():
            rows.append(child)
    return rows


def load_candidate(candidate_dir: Path) -> Tuple[ParsedProblem, Dict[str, Any]]:
    parsed = parse_problem_file(candidate_dir / "problem.md")
    front = dict(parsed.front_matter or {})
    return parsed, front


def init_batch(args: argparse.Namespace) -> int:
    problems_root = Path(args.root).resolve()
    generated_root = Path(args.generated_root).resolve()
    ensure_dir(generated_root)

    batch_id = sanitize_token(args.batch_id) if args.batch_id else datetime.now().strftime("sim_%Y%m%d_%H%M%S")
    if not batch_id:
        print("[ERROR] Invalid batch_id.")
        return 1

    batch_dir = generated_root / batch_id
    if batch_dir.exists():
        if not args.overwrite:
            print(f"[ERROR] Batch already exists: {batch_dir}")
            return 1
        shutil.rmtree(batch_dir)
    ensure_dir(batch_dir)

    seeds = collect_seed_ids(
        root=problems_root,
        raw_seed_ids=args.seed_ids or "",
        pattern=args.pattern or "*",
        limit=max(int(args.limit), 0),
    )
    if not seeds:
        print("[ERROR] No seed problems selected.")
        return 1

    manifest: Dict[str, Any] = {
        "batch_id": batch_id,
        "created_at": now_iso(),
        "problems_root": str(problems_root),
        "generated_root": str(generated_root),
        "variants_per_seed": int(args.variants_per_seed),
        "similarity_type": args.similarity_type,
        "notes": args.notes or "",
        "seed_ids": seeds,
        "candidates": [],
    }

    for seed_id in seeds:
        seed_dir = problems_root / seed_id
        problem_md = seed_dir / "problem.md"
        if not problem_md.is_file():
            print(f"[WARN] Seed missing problem.md: {seed_id}")
            continue
        try:
            seed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[WARN] Failed to parse seed {seed_id}: {exc}")
            continue

        seed_front = dict(seed.front_matter or {})
        for variant_idx in range(1, int(args.variants_per_seed) + 1):
            cand_id = f"{seed_id}__SIM{variant_idx:02d}"
            cand_dir = batch_dir / cand_id
            ensure_dir(cand_dir)

            front = dict(seed_front)
            front["id"] = cand_id
            front["derived_from"] = seed_id
            front["similarity_type"] = args.similarity_type
            front["generation_batch_id"] = batch_id
            front["generation_model"] = "codex-agent-local"
            front["review_status"] = "pending"
            front["review_note"] = ""
            front["promoted_to"] = ""
            front["generated_at"] = now_iso()

            candidate_body = {
                "q": f"{DRAFT_TOKEN} Replace with a similar question derived from {seed_id}.",
                "choices": (
                    "1) \n2) \n3) \n4) \n5) "
                    if objective_like(front, seed_id)
                    else f"{DRAFT_TOKEN} Fill subjective answer space or conditions."
                ),
                "answer": f"{DRAFT_TOKEN} Fill final answer.",
                "solution": f"{DRAFT_TOKEN} Fill complete solution with valid math notation.",
            }
            write_problem_md(cand_dir / "problem.md", front, candidate_body)
            (cand_dir / "prompt.md").write_text(
                prompt_text(seed_id=seed_id, variant_no=variant_idx, seed=seed),
                encoding="utf-8",
            )
            (cand_dir / "source_snapshot.md").write_text(
                source_snapshot_text(seed_id=seed_id, seed=seed),
                encoding="utf-8",
            )

            manifest["candidates"].append(
                {
                    "candidate_id": cand_id,
                    "derived_from": seed_id,
                    "path": str(cand_dir),
                    "variant_index": variant_idx,
                }
            )
            print(f"[CREATED] {cand_id}")

    manifest_path = batch_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBatch created: {batch_dir}")
    print(f"Manifest: {manifest_path}")
    return 0


def validate_candidate(candidate_dir: Path, problems_root: Path, max_similarity: float) -> CandidateValidation:
    candidate_id = candidate_dir.name
    errors: List[str] = []
    warnings: List[str] = []

    try:
        parsed, front = load_candidate(candidate_dir)
    except Exception as exc:  # pylint: disable=broad-except
        return CandidateValidation(candidate_id, False, [f"Parse failed: {exc}"], [], 1.0)

    for section in SECTION_NAMES:
        text = str(getattr(parsed, section, "") or "").strip()
        if not text:
            errors.append(f"Section `{section}` is empty.")
        if DRAFT_TOKEN in text:
            errors.append(f"Section `{section}` still contains draft token.")
        for issue in latex_balance_issues(text):
            warnings.append(f"{section}: {issue}")

    objective = objective_like(front, str(front.get("derived_from", candidate_id)))
    if objective:
        choice_count = count_choice_lines(parsed.choices or "")
        if choice_count < 4:
            errors.append(f"Objective question has too few option-like lines ({choice_count}).")
        answer_token = (parsed.answer or "").strip()
        if not answer_token:
            errors.append("Objective answer is empty.")

    source_id = str(front.get("derived_from", "")).strip()
    similarity_ratio = 0.0
    if source_id:
        source_md = problems_root / source_id / "problem.md"
        if source_md.is_file():
            try:
                source = parse_problem_file(source_md)
                similarity_ratio = SequenceMatcher(
                    None,
                    normalize_for_similarity(source.q),
                    normalize_for_similarity(parsed.q),
                ).ratio()
                if similarity_ratio > max_similarity:
                    errors.append(
                        f"Q similarity too high vs source ({similarity_ratio:.3f} > {max_similarity:.3f})."
                    )
                elif similarity_ratio > max_similarity - 0.08:
                    warnings.append(f"Q similarity near threshold ({similarity_ratio:.3f}).")
            except Exception as exc:  # pylint: disable=broad-except
                warnings.append(f"Source parse failed for similarity check: {exc}")
        else:
            warnings.append(f"Source problem not found for similarity check: {source_id}")
    else:
        warnings.append("`derived_from` is missing.")

    ok = len(errors) == 0
    return CandidateValidation(candidate_id, ok, errors, warnings, similarity_ratio)


def validate_batch(args: argparse.Namespace) -> int:
    problems_root = Path(args.root).resolve()
    batch_dir = Path(args.generated_root).resolve() / args.batch_id
    if not batch_dir.is_dir():
        print(f"[ERROR] Batch folder not found: {batch_dir}")
        return 1

    targets = candidate_dirs(batch_dir)
    if args.candidate_ids:
        selected = set(parse_id_tokens(args.candidate_ids))
        targets = [path for path in targets if path.name in selected]

    if not targets:
        print("[ERROR] No candidate folders to validate.")
        return 1

    results: List[CandidateValidation] = []
    for cdir in targets:
        result = validate_candidate(cdir, problems_root, float(args.max_similarity))
        results.append(result)

    failed = [row for row in results if not row.ok]
    report = {
        "batch_id": args.batch_id,
        "validated_at": now_iso(),
        "max_similarity": float(args.max_similarity),
        "summary": {
            "total": len(results),
            "ok": len(results) - len(failed),
            "failed": len(failed),
        },
        "results": [
            {
                "candidate_id": row.candidate_id,
                "ok": row.ok,
                "similarity_ratio": row.similarity_ratio,
                "errors": row.errors,
                "warnings": row.warnings,
            }
            for row in results
        ],
    }
    report_path = batch_dir / "validation_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for row in results:
        status = "OK" if row.ok else "FAIL"
        print(f"[{status}] {row.candidate_id} | sim={row.similarity_ratio:.3f}")
        for err in row.errors:
            print(f"  - ERROR: {err}")
        for warn in row.warnings:
            print(f"  - WARN: {warn}")

    print(
        f"\nValidation summary: total={len(results)} ok={len(results) - len(failed)} failed={len(failed)}"
    )
    print(f"Report: {report_path}")
    return 0 if not failed else 2


def update_review(args: argparse.Namespace) -> int:
    batch_dir = Path(args.generated_root).resolve() / args.batch_id
    if not batch_dir.is_dir():
        print(f"[ERROR] Batch folder not found: {batch_dir}")
        return 1
    ids = parse_id_tokens(args.candidate_ids or "")
    if not ids:
        print("[ERROR] --candidate-ids is required.")
        return 1

    status = str(args.status).strip().lower()
    if status not in {"pending", "approved", "rejected"}:
        print("[ERROR] --status must be one of: pending, approved, rejected")
        return 1

    updated = 0
    for cid in ids:
        cdir = batch_dir / cid
        pmd = cdir / "problem.md"
        if not pmd.is_file():
            print(f"[WARN] Candidate not found: {cid}")
            continue
        parsed = parse_problem_file(pmd)
        front = dict(parsed.front_matter or {})
        front["review_status"] = status
        if args.note:
            front["review_note"] = args.note
        front["reviewed_at"] = now_iso()
        write_problem_md(
            pmd,
            front,
            {
                "q": parsed.q,
                "choices": parsed.choices,
                "answer": parsed.answer,
                "solution": parsed.solution,
            },
        )
        updated += 1
        print(f"[UPDATED] {cid} -> {status}")

    print(f"\nReview update completed: {updated} candidates")
    return 0


def next_problem_id(problems_root: Path, prefix: str, used_ids: Iterable[str]) -> str:
    used_numbers = set()
    used_ids_set = set(used_ids)
    for folder in problems_root.iterdir():
        if not folder.is_dir():
            continue
        token = folder.name
        matched = PROBLEM_ID_RE.match(token)
        if not matched:
            continue
        if matched.group("prefix") != prefix:
            continue
        used_numbers.add(int(matched.group("number")))
    for pid in used_ids_set:
        matched = PROBLEM_ID_RE.match(pid)
        if matched and matched.group("prefix") == prefix:
            used_numbers.add(int(matched.group("number")))
    if not used_numbers:
        return f"{prefix}-001"
    candidate = max(used_numbers) + 1
    if candidate > 999:
        raise ValueError(f"No available 3-digit number for prefix `{prefix}`.")
    return f"{prefix}-{candidate:03d}"


def promote_batch(args: argparse.Namespace) -> int:
    problems_root = Path(args.root).resolve()
    generated_root = Path(args.generated_root).resolve()
    batch_dir = generated_root / args.batch_id
    if not batch_dir.is_dir():
        print(f"[ERROR] Batch folder not found: {batch_dir}")
        return 1
    ensure_dir(problems_root)

    candidates = candidate_dirs(batch_dir)
    if args.candidate_ids:
        selected = set(parse_id_tokens(args.candidate_ids))
        candidates = [path for path in candidates if path.name in selected]
    if not candidates:
        print("[ERROR] No candidates selected for promotion.")
        return 1

    promoted: List[Tuple[str, str]] = []
    skipped = 0
    reserved_ids: List[str] = []
    for cdir in candidates:
        cid = cdir.name
        parsed, front = load_candidate(cdir)
        review_status = str(front.get("review_status", "")).strip().lower()
        if review_status != "approved" and not args.force:
            print(f"[SKIP] {cid} review_status={review_status!r} (need approved)")
            skipped += 1
            continue
        if any(DRAFT_TOKEN in (getattr(parsed, sec) or "") for sec in SECTION_NAMES):
            print(f"[SKIP] {cid} still contains {DRAFT_TOKEN}")
            skipped += 1
            continue

        derived_from = str(front.get("derived_from", "")).strip()
        matched = PROBLEM_ID_RE.match(derived_from)
        if not matched:
            print(f"[SKIP] {cid} invalid derived_from={derived_from!r}")
            skipped += 1
            continue
        prefix = matched.group("prefix")
        try:
            new_id = next_problem_id(problems_root, prefix, reserved_ids)
        except ValueError as exc:
            print(f"[SKIP] {cid} {exc}")
            skipped += 1
            continue
        reserved_ids.append(new_id)

        target_dir = problems_root / new_id
        if target_dir.exists():
            print(f"[SKIP] {cid} target already exists: {target_dir}")
            skipped += 1
            continue

        shutil.copytree(cdir, target_dir)
        for extra_name in ("prompt.md", "source_snapshot.md", "validation_report.json"):
            extra = target_dir / extra_name
            if extra.exists():
                if extra.is_dir():
                    shutil.rmtree(extra)
                else:
                    extra.unlink()

        front_new = dict(front)
        front_new["id"] = new_id
        front_new["promoted_from"] = cid
        front_new["promoted_at"] = now_iso()
        write_problem_md(
            target_dir / "problem.md",
            front_new,
            {
                "q": parsed.q,
                "choices": parsed.choices,
                "answer": parsed.answer,
                "solution": parsed.solution,
            },
        )

        front["promoted_to"] = new_id
        front["review_status"] = "promoted"
        front["promoted_at"] = now_iso()
        write_problem_md(
            cdir / "problem.md",
            front,
            {
                "q": parsed.q,
                "choices": parsed.choices,
                "answer": parsed.answer,
                "solution": parsed.solution,
            },
        )
        promoted.append((cid, new_id))
        print(f"[PROMOTED] {cid} -> {new_id}")

    report = {
        "batch_id": args.batch_id,
        "promoted_at": now_iso(),
        "promoted": [{"candidate_id": cid, "new_problem_id": nid} for cid, nid in promoted],
        "skipped": skipped,
    }
    report_path = batch_dir / "promotion_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nPromotion summary: promoted={len(promoted)} skipped={skipped}")
    print(f"Report: {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline similar-problem batch pipeline (init/validate/review/promote)."
    )
    parser.add_argument("--root", default=str(DEFAULT_PROBLEMS_ROOT), help="Path to db/problems")
    parser.add_argument(
        "--generated-root",
        default=str(DEFAULT_GENERATED_ROOT),
        help="Path to generated candidates root",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new candidate batch with draft files.")
    p_init.add_argument("--batch-id", default="", help="Custom batch ID (default: timestamp).")
    p_init.add_argument("--seed-ids", default="", help="Seed IDs separated by comma/space.")
    p_init.add_argument("--pattern", default="*", help="Glob-like pattern for auto seed selection.")
    p_init.add_argument("--limit", type=int, default=20, help="Max number of seed problems.")
    p_init.add_argument("--variants-per-seed", type=int, default=1, help="Draft variants per seed.")
    p_init.add_argument("--similarity-type", default="parameter_change", help="Similarity type label.")
    p_init.add_argument("--notes", default="", help="Free-form batch notes.")
    p_init.add_argument("--overwrite", action="store_true", help="Overwrite existing batch folder.")
    p_init.set_defaults(func=init_batch)

    p_validate = sub.add_parser("validate", help="Validate candidate files in a batch.")
    p_validate.add_argument("--batch-id", required=True, help="Batch ID to validate.")
    p_validate.add_argument("--candidate-ids", default="", help="Optional subset candidate IDs.")
    p_validate.add_argument(
        "--max-similarity",
        type=float,
        default=0.92,
        help="Maximum allowed question similarity ratio vs seed.",
    )
    p_validate.set_defaults(func=validate_batch)

    p_review = sub.add_parser("review", help="Set review status for candidate IDs.")
    p_review.add_argument("--batch-id", required=True, help="Batch ID.")
    p_review.add_argument("--candidate-ids", required=True, help="Candidate IDs separated by comma/space.")
    p_review.add_argument("--status", required=True, choices=["pending", "approved", "rejected"])
    p_review.add_argument("--note", default="", help="Optional review note.")
    p_review.set_defaults(func=update_review)

    p_promote = sub.add_parser("promote", help="Promote approved candidates to db/problems.")
    p_promote.add_argument("--batch-id", required=True, help="Batch ID.")
    p_promote.add_argument("--candidate-ids", default="", help="Optional subset candidate IDs.")
    p_promote.add_argument("--force", action="store_true", help="Promote even when review_status is not approved.")
    p_promote.set_defaults(func=promote_batch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
