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


def _collect_problem_dirs(
    root: Path,
    ids_arg: str | None,
    pattern: str | None,
    dirs_arg: List[str] | None,
    dirs_file_arg: str | None,
) -> List[Path]:
    selected: List[Path] = []

    if dirs_arg:
        for raw_dir in dirs_arg:
            token = str(raw_dir or "").strip()
            if not token:
                continue
            selected.append(Path(token))
    elif dirs_file_arg:
        dirs_file = Path(dirs_file_arg)
        for raw_line in dirs_file.read_text(encoding="utf-8").splitlines():
            token = raw_line.lstrip("\ufeff").strip()
            if not token or token.startswith("#"):
                continue
            selected.append(Path(token))
    elif ids_arg:
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
    selector.add_argument(
        "--dirs",
        nargs="+",
        help="Space-separated explicit problem folder paths.",
    )
    selector.add_argument(
        "--dirs-file",
        help="UTF-8 text file containing one explicit problem folder path per line.",
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
        "--problems-per-page",
        type=int,
        default=8,
        choices=[4, 6, 8],
        help="Target problem slots per page. Default: 8",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=10.0,
        help="Base font size in pt. Default: 10",
    )
    parser.add_argument(
        "--title",
        default="내신 기출",
        help="Document title shown in PDF header. Default: 내신 기출",
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
        "--outer-border-off",
        action="store_true",
        help="Hide the outer page border for the exam sheet.",
    )
    parser.add_argument(
        "--inner-dividers-off",
        action="store_true",
        help="Hide inner divider lines inside the exam sheet.",
    )
    parser.add_argument(
        "--teacher-view",
        action="store_true",
        help="Show inline answer under each problem in exam PDF (교사용 출력).",
    )
    parser.add_argument(
        "--reset-question-number-by-school",
        action="store_true",
        help="Reset displayed question number when school changes in selected order (학교별문항번호리셋).",
    )
    parser.add_argument(
        "--skip-exam",
        action="store_true",
        help="Skip main exam PDF rendering and generate only selected sheets.",
    )
    return parser


def _merge_pdfs(out_pdf: Path, append_paths: List[Path], include_out_pdf: bool = True) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError(
            "pypdf is required to append answer/solution sheets into the main output PDF."
        ) from exc

    writer = PdfWriter()
    sources: List[Path] = []
    if include_out_pdf:
        sources.append(out_pdf)
    sources.extend(append_paths)
    if not sources:
        raise RuntimeError("No PDF sources were provided for merge.")

    for source in sources:
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
    problems_per_page: int,
    font_size: float,
    title: str,
    show_meta: bool,
    show_source_info: bool,
    show_unit_info: bool,
    show_outer_border: bool,
    show_inner_dividers: bool,
    show_teacher_answer: bool,
    reset_question_number_by_school: bool,
) -> ExamLayout:
    paper_key = paper.upper()
    if columns < 1:
        raise ValueError("--columns must be >= 1")
    if problems_per_page < 1:
        raise ValueError("--problems-per-page must be >= 1")
    if problems_per_page % columns != 0:
        raise ValueError("--problems-per-page must be divisible by --columns")
    if font_size <= 0:
        raise ValueError("--font-size must be > 0")
    rows_per_column = problems_per_page // columns

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
        rows_per_column=rows_per_column,
        problems_per_page=problems_per_page,
        font_size_pt=font_size,
        title=title,
        show_meta=show_meta,
        show_source_info=show_source_info,
        show_unit_info=show_unit_info,
        show_outer_border=show_outer_border,
        show_inner_dividers=show_inner_dividers,
        show_teacher_answer=show_teacher_answer,
        reset_question_number_by_school=reset_question_number_by_school,
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
            problems_per_page=args.problems_per_page,
            font_size=args.font_size,
            title=args.title,
            show_meta=args.show_meta,
            show_source_info=args.show_source_info,
            show_unit_info=args.show_unit_info,
            show_outer_border=not args.outer_border_off,
            show_inner_dividers=not args.inner_dividers_off,
            show_teacher_answer=args.teacher_view,
            reset_question_number_by_school=args.reset_question_number_by_school,
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    warnings: List[str] = []

    using_explicit_dirs = bool(args.dirs or args.dirs_file)
    if not using_explicit_dirs and (not root.exists() or not root.is_dir()):
        print(f"[ERROR] Root directory not found: {root}", file=sys.stderr)
        return 1

    problem_dirs = _collect_problem_dirs(
        root=root,
        ids_arg=args.ids,
        pattern=args.pattern,
        dirs_arg=args.dirs,
        dirs_file_arg=args.dirs_file,
    )
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

    if args.skip_exam and not (answer_sheet_path or solution_sheet_path):
        print("[ERROR] --skip-exam requires --answer-sheet and/or --solution-sheet.", file=sys.stderr)
        return 1

    if not args.skip_exam:
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
    else:
        print("Exam PDF generation skipped (--skip-exam).")

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
                reset_question_number_by_school=layout.reset_question_number_by_school,
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
                reset_question_number_by_school=layout.reset_question_number_by_school,
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
            if args.skip_exam:
                if len(appended_paths) == 1:
                    appended_paths[0].replace(out_pdf)
                else:
                    _merge_pdfs(out_pdf=out_pdf, append_paths=appended_paths, include_out_pdf=False)
                print(f"Merged PDF (selected sheets): {out_pdf.resolve()}")
            else:
                _merge_pdfs(out_pdf=out_pdf, append_paths=appended_paths, include_out_pdf=True)
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
