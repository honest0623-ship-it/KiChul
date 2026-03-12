from __future__ import annotations

from typing import Any, Dict, List

from flask import flash, redirect, request, url_for


def register_render_routes(app, deps: Dict[str, Any]) -> None:
    BASE_DIR = deps["BASE_DIR"]
    DEFAULT_EXAM_TITLE = deps["DEFAULT_EXAM_TITLE"]
    DEFAULT_SORT_FIELD_SLOTS = deps["DEFAULT_SORT_FIELD_SLOTS"]
    OUTPUT_DIR = deps["OUTPUT_DIR"]
    Path = deps["Path"]
    default_selected_unit_nodes = deps["default_selected_unit_nodes"]
    expand_unit_nodes_to_leaf_paths = deps["expand_unit_nodes_to_leaf_paths"]
    subprocess = deps["subprocess"]
    sys = deps["sys"]
    tempfile = deps["tempfile"]

    _apply_manual_order = deps["_apply_manual_order"]
    _current_defaults = deps["_current_defaults"]
    _effective_sort_fields = deps["_effective_sort_fields"]
    _extract_ids = deps["_extract_ids"]
    _matches_pattern_for_row = deps["_matches_pattern_for_row"]
    _normalize_data_source = deps["_normalize_data_source"]
    _normalize_paper = deps["_normalize_paper"]
    _normalize_problems_per_page = deps["_normalize_problems_per_page"]
    _normalize_sort_field_slots = deps["_normalize_sort_field_slots"]
    _normalize_sort_order = deps["_normalize_sort_order"]
    _normalize_title = deps["_normalize_title"]
    _normalize_values = deps["_normalize_values"]
    _open_path_in_file_manager = deps["_open_path_in_file_manager"]
    _parse_int = deps["_parse_int"]
    _resolve_unique_pdf_path = deps["_resolve_unique_pdf_path"]
    _scan_problem_meta = deps["_scan_problem_meta"]
    _sort_selected_problem_ids = deps["_sort_selected_problem_ids"]

    @app.get("/open-output")
    def open_output_folder():
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        try:
            _open_path_in_file_manager(OUTPUT_DIR)
            flash(f"출력 폴더를 열었습니다: {OUTPUT_DIR}", "success")
        except Exception as exc:  # pylint: disable=broad-except
            flash(f"출력 폴더 열기 실패: {exc}", "warning")
        return redirect(url_for("index", **_current_defaults()))


    @app.post("/render")
    def render_pdf():
        def _first_or(values: List[str], fallback: str) -> str:
            return values[0] if values else fallback

        defaults = _current_defaults()
        schools = _normalize_values(request.form.getlist("schools"), upper=True)
        years = _normalize_values(request.form.getlist("years"))
        grades = _normalize_values(request.form.getlist("grades"))
        semesters = _normalize_values(request.form.getlist("semesters"))
        exams = _normalize_values(request.form.getlist("exams"), upper=True)
        unit_nodes = _normalize_values(request.form.getlist("unit_nodes"))
        if not unit_nodes:
            unit_nodes = default_selected_unit_nodes()
        units = expand_unit_nodes_to_leaf_paths(unit_nodes)
        levels = _normalize_values(request.form.getlist("levels"))
        source_numbers = _normalize_values(request.form.getlist("source_numbers"))
        selected_data_source = _normalize_data_source(request.form.get("data_source", "official"))

        selector_ids = _extract_ids(request.form.get("selector_ids", ""))
        manual_order_ids = _extract_ids(request.form.get("manual_order_ids", ""))
        manual_selected_supplied = "manual_selected_ids" in request.form
        manual_selected_ids = _extract_ids(request.form.get("manual_selected_ids", ""))
        pattern = request.form.get("selector_pattern", "").strip()
        legacy_sort_field = request.form.get("sort_field", "")
        sort_field_slots = _normalize_sort_field_slots(
            [
                request.form.get("sort_field_1", legacy_sort_field or DEFAULT_SORT_FIELD_SLOTS[0]),
                request.form.get("sort_field_2", DEFAULT_SORT_FIELD_SLOTS[1]),
                request.form.get("sort_field_3", DEFAULT_SORT_FIELD_SLOTS[2]),
            ]
        )
        effective_sort_fields = _effective_sort_fields(sort_field_slots)
        primary_sort_field = sort_field_slots[0]
        sort_order = _normalize_sort_order(request.form.get("sort_order", "asc"))
        paper = _normalize_paper(request.form.get("paper", "A4"))
        problems_per_page = _normalize_problems_per_page(request.form.get("problems_per_page", "8"))
        question_count = max(_parse_int(request.form.get("question_count", "0"), 0), 0)
        show_source_info = bool(request.form.get("show_source_info"))
        show_unit_info = bool(request.form.get("show_unit_info"))
        show_outer_border = bool(request.form.get("show_outer_border"))
        show_inner_dividers = bool(request.form.get("show_inner_dividers"))
        teacher_view = bool(request.form.get("teacher_view"))
        reset_question_number_by_school = bool(request.form.get("reset_question_number_by_school"))
        include_exam_sheet = bool(request.form.get("exam_sheet"))
        append_answer_sheet = bool(request.form.get("answer_sheet"))
        append_solution_sheet = bool(request.form.get("solution_sheet"))
        title = _normalize_title(request.form.get("title"), default=DEFAULT_EXAM_TITLE)

        problem_meta = _scan_problem_meta(
            data_sources=[selected_data_source],
        )
        meta_by_id = {item["id"]: item for item in problem_meta}
        available_ids = {item["id"] for item in problem_meta}
        manual_selected_ids = [item for item in manual_selected_ids if item in available_ids]
        manual_selection_active = manual_selected_supplied and (primary_sort_field == "manual" or bool(manual_order_ids))
        selected_problem_ids: List[str] = []

        if selector_ids:
            selected_problem_ids = [item for item in selector_ids if item in available_ids]
            missing_ids = [item for item in selector_ids if item not in available_ids]
            if missing_ids:
                flash(f"존재하지 않는 ID 제외: {', '.join(missing_ids[:10])}", "warning")
        else:
            for item in problem_meta:
                if schools and item["school"] not in schools:
                    continue
                if years and item["year"] not in years:
                    continue
                if grades and item["grade"] not in grades:
                    continue
                if semesters and item["semester"] not in semesters:
                    continue
                if exams and item["exam"] not in exams:
                    continue
                if units and item.get("unit", "") not in units:
                    continue
                if levels and item.get("level", "") not in levels:
                    continue
                if source_numbers and str(item.get("source_label", "")) not in source_numbers:
                    continue
                selected_problem_ids.append(item["id"])

        if pattern:
            selected_problem_ids = [
                item
                for item in selected_problem_ids
                if _matches_pattern_for_row(meta_by_id.get(item, {}), pattern)
            ]

        if manual_selection_active:
            selected_manual_set = set(manual_selected_ids)
            selected_problem_ids = [item for item in selected_problem_ids if item in selected_manual_set]

        if primary_sort_field == "manual":
            manual_reference_ids = (
                manual_selected_ids
                if manual_selection_active
                else (manual_order_ids if manual_order_ids else selector_ids)
            )
            selected_problem_ids, missing_manual_ids = _apply_manual_order(
                selected_problem_ids=selected_problem_ids,
                manual_order_ids=manual_reference_ids,
            )
            if not manual_reference_ids and not (manual_selection_active and not manual_selected_ids):
                flash("수동 정렬 기준(ID 목록)이 비어 있어 현재 선택 순서를 유지합니다.", "warning")
            if missing_manual_ids:
                flash(f"수동 정렬 목록에서 제외된 ID: {', '.join(missing_manual_ids[:10])}", "warning")
        else:
            selected_problem_ids = _sort_selected_problem_ids(
                selected_problem_ids=selected_problem_ids,
                problem_meta=problem_meta,
                sort_fields=effective_sort_fields,
                sort_order=sort_order,
            )

        if question_count > 0:
            selected_problem_ids = selected_problem_ids[:question_count]

        if not selected_problem_ids:
            flash("선택 조건에 해당하는 문항이 없습니다.", "warning")
            next_defaults = {
                "school": _first_or(schools, defaults["school"]),
                "year": _first_or(years, defaults["year"]),
                "grade": _first_or(grades, defaults["grade"]),
                "semester": _first_or(semesters, defaults["semester"]),
                "exam": _first_or(exams, defaults["exam"]),
                "data_source": selected_data_source,
                "schools": schools,
                "years": years,
                "grades": grades,
                "semesters": semesters,
                "exams": exams,
                "unit_nodes": unit_nodes,
                "levels": levels,
                "source_numbers": source_numbers,
                "selector_pattern": pattern,
                "sort_field_1": sort_field_slots[0],
                "sort_field_2": sort_field_slots[1],
                "sort_field_3": sort_field_slots[2],
                "sort_order": sort_order,
                "paper": paper,
                "problems_per_page": str(problems_per_page),
                "manual_order_ids": " ".join(manual_order_ids),
                "manual_selected_ids": " ".join(manual_selected_ids),
                "question_count": str(question_count),
                "show_source_info": "1" if show_source_info else "0",
                "show_unit_info": "1" if show_unit_info else "0",
                "show_outer_border": "1" if show_outer_border else "0",
                "show_inner_dividers": "1" if show_inner_dividers else "0",
                "teacher_view": "1" if teacher_view else "0",
                "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
                "exam_sheet": "1" if include_exam_sheet else "0",
                "answer_sheet": "1" if append_answer_sheet else "0",
                "solution_sheet": "1" if append_solution_sheet else "0",
            }
            return redirect(url_for("index", **next_defaults))

        selected_problem_dirs: List[str] = []
        seen_problem_dirs = set()
        missing_problem_dirs: List[str] = []
        for problem_id in selected_problem_ids:
            row = meta_by_id.get(problem_id)
            folder_path = str(row.get("folder_path", "")).strip() if row else ""
            if not folder_path:
                missing_problem_dirs.append(problem_id)
                continue
            normalized_folder_path = str(Path(folder_path))
            if normalized_folder_path in seen_problem_dirs:
                continue
            seen_problem_dirs.add(normalized_folder_path)
            selected_problem_dirs.append(normalized_folder_path)

        if missing_problem_dirs:
            flash(f"문항 폴더를 찾을 수 없는 ID 제외: {', '.join(missing_problem_dirs[:10])}", "warning")

        if not selected_problem_dirs:
            flash("선택된 문항 폴더를 찾을 수 없습니다.", "warning")
            next_defaults = {
                "school": _first_or(schools, defaults["school"]),
                "year": _first_or(years, defaults["year"]),
                "grade": _first_or(grades, defaults["grade"]),
                "semester": _first_or(semesters, defaults["semester"]),
                "exam": _first_or(exams, defaults["exam"]),
                "data_source": selected_data_source,
                "schools": schools,
                "years": years,
                "grades": grades,
                "semesters": semesters,
                "exams": exams,
                "unit_nodes": unit_nodes,
                "levels": levels,
                "source_numbers": source_numbers,
                "selector_pattern": pattern,
                "sort_field_1": sort_field_slots[0],
                "sort_field_2": sort_field_slots[1],
                "sort_field_3": sort_field_slots[2],
                "sort_order": sort_order,
                "paper": paper,
                "problems_per_page": str(problems_per_page),
                "manual_order_ids": " ".join(manual_order_ids),
                "manual_selected_ids": " ".join(manual_selected_ids),
                "question_count": str(question_count),
                "show_source_info": "1" if show_source_info else "0",
                "show_unit_info": "1" if show_unit_info else "0",
                "show_outer_border": "1" if show_outer_border else "0",
                "show_inner_dividers": "1" if show_inner_dividers else "0",
                "teacher_view": "1" if teacher_view else "0",
                "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
                "exam_sheet": "1" if include_exam_sheet else "0",
                "answer_sheet": "1" if append_answer_sheet else "0",
                "solution_sheet": "1" if append_solution_sheet else "0",
                "selector_ids": " ".join(selector_ids),
            }
            return redirect(url_for("index", **next_defaults))

        if not include_exam_sheet and not append_answer_sheet and not append_solution_sheet:
            flash("문제지/답안지/해설지 중 하나 이상 선택해 주세요.", "warning")
            next_defaults = {
                "school": _first_or(schools, defaults["school"]),
                "year": _first_or(years, defaults["year"]),
                "grade": _first_or(grades, defaults["grade"]),
                "semester": _first_or(semesters, defaults["semester"]),
                "exam": _first_or(exams, defaults["exam"]),
                "data_source": selected_data_source,
                "schools": schools,
                "years": years,
                "grades": grades,
                "semesters": semesters,
                "exams": exams,
                "unit_nodes": unit_nodes,
                "levels": levels,
                "source_numbers": source_numbers,
                "selector_pattern": pattern,
                "sort_field_1": sort_field_slots[0],
                "sort_field_2": sort_field_slots[1],
                "sort_field_3": sort_field_slots[2],
                "sort_order": sort_order,
                "paper": paper,
                "problems_per_page": str(problems_per_page),
                "manual_order_ids": " ".join(manual_order_ids),
                "manual_selected_ids": " ".join(manual_selected_ids),
                "question_count": str(question_count),
                "show_source_info": "1" if show_source_info else "0",
                "show_unit_info": "1" if show_unit_info else "0",
                "show_outer_border": "1" if show_outer_border else "0",
                "show_inner_dividers": "1" if show_inner_dividers else "0",
                "teacher_view": "1" if teacher_view else "0",
                "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
                "exam_sheet": "1" if include_exam_sheet else "0",
                "answer_sheet": "1" if append_answer_sheet else "0",
                "solution_sheet": "1" if append_solution_sheet else "0",
                "selector_ids": " ".join(selector_ids),
                "title": title,
            }
            return redirect(url_for("index", **next_defaults))

        out_name = Path(request.form.get("out_name", "").strip() or "exam_from_web.pdf").name
        if not out_name.lower().endswith(".pdf"):
            out_name = f"{out_name}.pdf"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = _resolve_unique_pdf_path(OUTPUT_DIR / out_name)

        dirs_manifest = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            prefix="build_exam_dirs_",
            dir=str(OUTPUT_DIR),
            delete=False,
            encoding="utf-8",
            newline="\n",
        )
        dirs_manifest_path = Path(dirs_manifest.name)
        try:
            for problem_dir in selected_problem_dirs:
                dirs_manifest.write(f"{problem_dir}\n")
        finally:
            dirs_manifest.close()

        cmd = [
            sys.executable,
            "build_exam.py",
            "--out",
            str(out_path),
            "--paper",
            paper,
            "--problems-per-page",
            str(problems_per_page),
            "--title",
            title,
            "--dirs-file",
            str(dirs_manifest_path),
        ]

        if show_source_info:
            cmd.append("--show-source-info")
        if show_unit_info:
            cmd.append("--show-unit-info")
        if not show_outer_border:
            cmd.append("--outer-border-off")
        if not show_inner_dividers:
            cmd.append("--inner-dividers-off")
        if teacher_view:
            cmd.append("--teacher-view")
        if reset_question_number_by_school:
            cmd.append("--reset-question-number-by-school")
        if not include_exam_sheet:
            cmd.append("--skip-exam")

        if append_answer_sheet:
            answer_path = _resolve_unique_pdf_path(OUTPUT_DIR / "answer_sheet_web.pdf")
            cmd.extend(["--answer-sheet", str(answer_path)])

        if append_solution_sheet:
            solution_path = _resolve_unique_pdf_path(OUTPUT_DIR / "solution_sheet_web.pdf")
            cmd.extend(["--solution-sheet", str(solution_path)])

        if append_answer_sheet or append_solution_sheet:
            cmd.append("--append-sheets-to-out")

        try:
            completed = subprocess.run(
                cmd,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
        finally:
            dirs_manifest_path.unlink(missing_ok=True)

        if completed.returncode != 0:
            flash("PDF 생성 실패", "error")
            if completed.stderr.strip():
                for line in completed.stderr.strip().splitlines()[:20]:
                    flash(line, "warning")
            if completed.stdout.strip():
                for line in completed.stdout.strip().splitlines()[:20]:
                    flash(line, "info")
        else:
            flash(f"PDF 생성 완료: {out_path}", "success")
            flash(f"출제 문항 수: {len(selected_problem_ids)}", "info")
            if append_answer_sheet or append_solution_sheet:
                flash("체크한 답안지/해설지를 본문 PDF에 병합해 단일 파일로 생성했습니다.", "info")
            if completed.stdout.strip():
                for line in completed.stdout.strip().splitlines()[:20]:
                    flash(line, "info")
            if completed.stderr.strip():
                for line in completed.stderr.strip().splitlines()[:20]:
                    flash(line, "warning")

        next_defaults = {
            "school": _first_or(schools, defaults["school"]),
            "year": _first_or(years, defaults["year"]),
            "grade": _first_or(grades, defaults["grade"]),
            "semester": _first_or(semesters, defaults["semester"]),
            "exam": _first_or(exams, defaults["exam"]),
            "data_source": selected_data_source,
            "schools": schools,
            "years": years,
            "grades": grades,
            "semesters": semesters,
            "exams": exams,
            "unit_nodes": unit_nodes,
            "levels": levels,
            "source_numbers": source_numbers,
            "selector_pattern": pattern,
            "sort_field_1": sort_field_slots[0],
            "sort_field_2": sort_field_slots[1],
            "sort_field_3": sort_field_slots[2],
            "sort_order": sort_order,
            "paper": paper,
            "problems_per_page": str(problems_per_page),
            "manual_order_ids": " ".join(manual_order_ids),
            "manual_selected_ids": " ".join(manual_selected_ids),
            "question_count": str(question_count),
            "show_source_info": "1" if show_source_info else "0",
            "show_unit_info": "1" if show_unit_info else "0",
            "show_outer_border": "1" if show_outer_border else "0",
            "show_inner_dividers": "1" if show_inner_dividers else "0",
            "teacher_view": "1" if teacher_view else "0",
            "reset_question_number_by_school": "1" if reset_question_number_by_school else "0",
            "exam_sheet": "1" if include_exam_sheet else "0",
            "answer_sheet": "1" if append_answer_sheet else "0",
            "solution_sheet": "1" if append_solution_sheet else "0",
            "selector_ids": " ".join(selector_ids),
            "title": title,
        }
        return redirect(url_for("index", **next_defaults))

