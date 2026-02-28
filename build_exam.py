from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import List

from parser import ParsedProblem, parse_problem_file
from renderer import (
    ExamLayout,
    render_answer_sheet_pdf,
    render_exam_pdf,
    render_solution_sheet_pdf,
)


def _parse_ids(ids_arg: str) -> List[str]:
    return [item.strip() for item in ids_arg.split(",") if item.strip()]


def _collect_problem_dirs(root: Path, ids_arg: str | None, pattern: str | None) -> List[Path]:
    selected: List[Path] = []

    if ids_arg:
        for problem_id in _parse_ids(ids_arg):
            selected.append(root / problem_id)
    elif pattern:
        selected.extend(sorted([p for p in root.glob(pattern) if p.is_dir()], key=lambda p: p.name))

    deduped: List[Path] = []
    seen = set()
    for item in selected:
        resolved = item.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(item)
    return deduped


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build exam PDF from problem markdown DB.")
    parser.add_argument(
        "--root",
        default="db/problems",
        help="Problem root directory. Default: db/problems",
    )

    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument(
        "--ids",
        help="Comma-separated folder IDs. Example: A-001,A-002,A-003",
    )
    selector.add_argument(
        "--pattern",
        help='Glob pattern for selecting folders. Example: "JEHS-2025-G1-S1-MID-*"',
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output exam PDF path. Example: output/exam.pdf",
    )
    parser.add_argument(
        "--answer-sheet",
        help="Optional answer sheet PDF output path.",
    )
    parser.add_argument(
        "--solution-sheet",
        help="Optional solution sheet PDF output path (answer + solution).",
    )
    parser.add_argument(
        "--template",
        default="templates/exam.html",
        help="HTML template path. Default: templates/exam.html",
    )
    parser.add_argument(
        "--mathjax-bundle",
        default="vendor/mathjax/tex-svg.js",
        help="Local MathJax bundle path. Default: vendor/mathjax/tex-svg.js",
    )
    parser.add_argument(
        "--paper",
        default="A4",
        choices=["A4", "B4", "a4", "b4"],
        help="Paper size: A4 (210x297mm) or JIS B4 (257x364mm). Default: A4",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=2,
        help="Number of columns for exam body. Default: 2",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=10.0,
        help="Base font size in pt. Default: 10",
    )
    parser.add_argument(
        "--title",
        default="Exam",
        help="Document title shown in PDF header. Default: Exam",
    )
    parser.add_argument(
        "--show-meta",
        action="store_true",
        help="Show generated timestamp/paper/column meta line in header. Default: hidden",
    )
    parser.add_argument(
        "--show-source-info",
        action="store_true",
        help="Show per-problem source info line (school/year/grade/semester/exam/source-no/ID).",
    )
    return parser


def _build_layout(
    paper: str,
    columns: int,
    font_size: float,
    title: str,
    show_meta: bool,
    show_source_info: bool,
) -> ExamLayout:
    paper_key = paper.upper()
    if columns < 1:
        raise ValueError("--columns must be >= 1")
    if font_size <= 0:
        raise ValueError("--font-size must be > 0")

    if paper_key == "A4":
        page_width_mm = 210
        page_height_mm = 297
        margin_mm = 13
        column_gap_mm = 9
    elif paper_key == "B4":
        page_width_mm = 257
        page_height_mm = 364
        margin_mm = 13
        column_gap_mm = 11
    else:
        raise ValueError(f"Unsupported paper type: {paper}")

    return ExamLayout(
        paper=paper_key,
        page_width_mm=page_width_mm,
        page_height_mm=page_height_mm,
        margin_mm=margin_mm,
        column_gap_mm=column_gap_mm,
        columns=columns,
        font_size_pt=font_size,
        title=title,
        show_meta=show_meta,
        show_source_info=show_source_info,
    )


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()

    root = Path(args.root)
    out_pdf = Path(args.out)
    template_path = Path(args.template)
    mathjax_bundle = Path(args.mathjax_bundle)
    answer_sheet_path = Path(args.answer_sheet) if args.answer_sheet else None
    solution_sheet_path = Path(args.solution_sheet) if args.solution_sheet else None
    try:
        layout = _build_layout(
            paper=args.paper,
            columns=args.columns,
            font_size=args.font_size,
            title=args.title,
            show_meta=args.show_meta,
            show_source_info=args.show_source_info,
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    warnings: List[str] = []

    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Root directory not found: {root}", file=sys.stderr)
        return 1

    problem_dirs = _collect_problem_dirs(root=root, ids_arg=args.ids, pattern=args.pattern)
    if not problem_dirs:
        print("[ERROR] No problem folders matched the selector.", file=sys.stderr)
        return 1

    parsed: List[ParsedProblem] = []
    for folder in problem_dirs:
        if not folder.exists() or not folder.is_dir():
            warnings.append(f"{folder}: Folder does not exist. Skipped.")
            continue

        problem_md = folder / "problem.md"
        if not problem_md.exists():
            warnings.append(f"{folder}: problem.md not found. Skipped.")
            continue

        try:
            item = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            warnings.append(f"{problem_md}: Failed to parse ({exc}). Skipped.")
            continue

        warnings.extend(item.warnings)
        parsed.append(item)

    if not parsed:
        print("[ERROR] No valid problem documents were parsed.", file=sys.stderr)
        for warning in warnings:
            print(f"[WARN] {warning}", file=sys.stderr)
        return 1

    try:
        render_exam_pdf(
            problems=parsed,
            out_pdf=out_pdf,
            template_path=template_path,
            mathjax_bundle=mathjax_bundle,
            layout=layout,
            warnings=warnings,
        )
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[ERROR] Failed to render exam PDF: {exc}", file=sys.stderr)
        for warning in warnings:
            print(f"[WARN] {warning}", file=sys.stderr)
        return 1

    print(f"Exam PDF: {out_pdf.resolve()}")

    if answer_sheet_path:
        try:
            render_answer_sheet_pdf(
                problems=parsed,
                out_pdf=answer_sheet_path,
                mathjax_bundle=mathjax_bundle,
                warnings=warnings,
            )
            print(f"Answer Sheet PDF: {answer_sheet_path.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] Failed to render answer sheet PDF: {exc}", file=sys.stderr)
            for warning in warnings:
                print(f"[WARN] {warning}", file=sys.stderr)
            return 1

    if solution_sheet_path:
        try:
            render_solution_sheet_pdf(
                problems=parsed,
                out_pdf=solution_sheet_path,
                mathjax_bundle=mathjax_bundle,
                warnings=warnings,
            )
            print(f"Solution Sheet PDF: {solution_sheet_path.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] Failed to render solution sheet PDF: {exc}", file=sys.stderr)
            for warning in warnings:
                print(f"[WARN] {warning}", file=sys.stderr)
            return 1

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
