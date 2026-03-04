from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile
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
        "--append-sheets-to-out",
        action="store_true",
        help="Append answer/solution sheets to the main exam PDF output as a single file.",
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
    parser.add_argument(
        "--show-unit-info",
        action="store_true",
        help="Show per-problem unit info line.",
    )
    parser.add_argument(
        "--teacher-view",
        action="store_true",
        help="Show inline answer under each problem in exam PDF (교사용 출력).",
    )
    return parser


def _merge_pdfs(out_pdf: Path, append_paths: List[Path]) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError(
            "pypdf is required to append answer/solution sheets into the main output PDF."
        ) from exc

    writer = PdfWriter()
    for source in [out_pdf, *append_paths]:
        reader = PdfReader(str(source))
        for page in reader.pages:
            writer.add_page(page)

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".pdf",
        prefix=f"{out_pdf.stem}_merged_",
        dir=str(out_pdf.parent),
        delete=False,
    )
    temp_path = Path(temp_file.name)
    temp_file.close()
    try:
        with temp_path.open("wb") as handle:
            writer.write(handle)
        temp_path.replace(out_pdf)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def _build_layout(
    paper: str,
    columns: int,
    font_size: float,
    title: str,
    show_meta: bool,
    show_source_info: bool,
    show_unit_info: bool,
    show_teacher_answer: bool,
) -> ExamLayout:
    paper_key = paper.upper()
    if columns < 1:
        raise ValueError("--columns must be >= 1")
    if font_size <= 0:
        raise ValueError("--font-size must be > 0")

    if paper_key == "A4":
        page_width_mm = 210
        page_height_mm = 297
        margin_top_mm = 10
        margin_right_mm = 8
        margin_bottom_mm = 10
        margin_left_mm = 8
        column_gap_mm = 9
    elif paper_key == "B4":
        page_width_mm = 257
        page_height_mm = 364
        margin_top_mm = 10
        margin_right_mm = 8
        margin_bottom_mm = 10
        margin_left_mm = 8
        column_gap_mm = 11
    else:
        raise ValueError(f"Unsupported paper type: {paper}")

    return ExamLayout(
        paper=paper_key,
        page_width_mm=page_width_mm,
        page_height_mm=page_height_mm,
        margin_top_mm=margin_top_mm,
        margin_right_mm=margin_right_mm,
        margin_bottom_mm=margin_bottom_mm,
        margin_left_mm=margin_left_mm,
        column_gap_mm=column_gap_mm,
        columns=columns,
        font_size_pt=font_size,
        title=title,
        show_meta=show_meta,
        show_source_info=show_source_info,
        show_unit_info=show_unit_info,
        show_teacher_answer=show_teacher_answer,
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
            show_unit_info=args.show_unit_info,
            show_teacher_answer=args.teacher_view,
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

    appended_paths: List[Path] = []
    temp_sheet_paths: List[Path] = []

    def _temp_sheet_path(prefix: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".pdf",
            prefix=f"{out_pdf.stem}_{prefix}_",
            dir=str(out_pdf.parent),
            delete=False,
        )
        path = Path(tmp.name)
        tmp.close()
        temp_sheet_paths.append(path)
        return path

    if answer_sheet_path:
        answer_target = _temp_sheet_path("answer") if args.append_sheets_to_out else answer_sheet_path
        try:
            render_answer_sheet_pdf(
                problems=parsed,
                out_pdf=answer_target,
                mathjax_bundle=mathjax_bundle,
                warnings=warnings,
            )
            if args.append_sheets_to_out:
                appended_paths.append(answer_target)
                print("Answer sheet generated (append target).")
            else:
                print(f"Answer Sheet PDF: {answer_sheet_path.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] Failed to render answer sheet PDF: {exc}", file=sys.stderr)
            for warning in warnings:
                print(f"[WARN] {warning}", file=sys.stderr)
            for temp_path in temp_sheet_paths:
                temp_path.unlink(missing_ok=True)
            return 1

    if solution_sheet_path:
        solution_target = _temp_sheet_path("solution") if args.append_sheets_to_out else solution_sheet_path
        try:
            render_solution_sheet_pdf(
                problems=parsed,
                out_pdf=solution_target,
                mathjax_bundle=mathjax_bundle,
                warnings=warnings,
            )
            if args.append_sheets_to_out:
                appended_paths.append(solution_target)
                print("Solution sheet generated (append target).")
            else:
                print(f"Solution Sheet PDF: {solution_sheet_path.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] Failed to render solution sheet PDF: {exc}", file=sys.stderr)
            for warning in warnings:
                print(f"[WARN] {warning}", file=sys.stderr)
            for temp_path in temp_sheet_paths:
                temp_path.unlink(missing_ok=True)
            return 1

    if args.append_sheets_to_out and appended_paths:
        try:
            _merge_pdfs(out_pdf=out_pdf, append_paths=appended_paths)
            print(f"Merged PDF (exam + selected sheets): {out_pdf.resolve()}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] Failed to merge PDFs: {exc}", file=sys.stderr)
            for warning in warnings:
                print(f"[WARN] {warning}", file=sys.stderr)
            for temp_path in temp_sheet_paths:
                temp_path.unlink(missing_ok=True)
            return 1

    for temp_path in temp_sheet_paths:
        temp_path.unlink(missing_ok=True)

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
