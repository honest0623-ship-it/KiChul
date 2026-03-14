from __future__ import annotations

import fnmatch
from typing import Any, Dict, List

from flask import abort, jsonify, request, send_from_directory


def register_problem_routes(app, deps: Dict[str, Any]) -> None:
    # Explicit dependency binding keeps this module import-light and testable.
    VENDOR_DIR = deps["VENDOR_DIR"]
    normalize_unit_triplet = deps["normalize_unit_triplet"]
    parse_problem_file = deps["parse_problem_file"]
    shutil = deps["shutil"]

    _build_preview_payload = deps["_build_preview_payload"]
    _extract_level_from_front_matter = deps["_extract_level_from_front_matter"]
    _extract_source_kind = deps["_extract_source_kind"]
    _extract_source_no_from_front_matter = deps["_extract_source_no_from_front_matter"]
    _fallback_source_no = deps["_fallback_source_no"]
    _id_groups_for_problem_meta = deps["_id_groups_for_problem_meta"]
    _invalidate_front_matter_cache_for_folder = deps["_invalidate_front_matter_cache_for_folder"]
    _normalize_subject_code = deps["_normalize_subject_code"]
    _open_path_in_file_manager = deps["_open_path_in_file_manager"]
    _parse_generated_problem_ui_id = deps["_parse_generated_problem_ui_id"]
    _refresh_problem_meta_row = deps["_refresh_problem_meta_row"]
    _resolve_problem_folder = deps["_resolve_problem_folder"]
    _resolve_problem_folder_any = deps["_resolve_problem_folder_any"]
    _resolve_similar_candidate_folder = deps["_resolve_similar_candidate_folder"]
    _rewrite_problem_md = deps["_rewrite_problem_md"]
    _rewrite_problem_md_sections = deps["_rewrite_problem_md_sections"]
    _safe_int_token = deps["_safe_int_token"]
    _scan_problem_meta = deps["_scan_problem_meta"]
    _serialize_problem_meta = deps["_serialize_problem_meta"]
    _serialize_problem_sections = deps["_serialize_problem_sections"]

    def _split_tokens(raw: str) -> List[str]:
        token = str(raw or "").strip()
        if not token:
            return []
        rows: List[str] = []
        for part in token.replace(",", " ").split():
            item = part.strip()
            if item:
                rows.append(item)
        return rows

    def _query_values(name: str) -> List[str]:
        rows: List[str] = []
        for raw in request.args.getlist(name):
            rows.extend(_split_tokens(raw))
        if rows:
            return rows
        return _split_tokens(request.args.get(name, ""))

    def _normalize_source_selector(raw: str) -> List[str] | None:
        token = str(raw or "official").strip().lower()
        if token in {"official", "generated"}:
            return [token]
        if token in {"all", "both", "*"}:
            return ["official", "generated"]
        return None

    def _safe_positive_int(raw: Any, *, default: int, minimum: int = 1, maximum: int = 500) -> int:
        try:
            value = int(raw)
        except (TypeError, ValueError):
            value = default
        if value < minimum:
            return minimum
        if value > maximum:
            return maximum
        return value

    def _meta_row_for_client(row: Dict[str, Any]) -> Dict[str, str]:
        keys = (
            "id",
            "problem_id",
            "display_id",
            "root_kind",
            "batch_id",
            "school",
            "year",
            "grade",
            "semester",
            "exam",
            "subject",
            "number",
            "source_no",
            "source_kind",
            "source_label",
            "unit",
            "level",
        )
        return {key: str(row.get(key, "") or "") for key in keys}

    def _match_filter_value(row: Dict[str, Any], key: str, selected: set[str]) -> bool:
        if not selected:
            return True
        token = str(row.get(key, "") or "").strip()
        return token in selected

    @app.get("/vendor-assets/<path:asset_rel>")
    def vendor_asset(asset_rel: str):
        rel_path = (asset_rel or "").replace("\\", "/").strip()
        if not rel_path:
            abort(404)
    
        target = (VENDOR_DIR / rel_path).resolve()
        try:
            target.relative_to(VENDOR_DIR.resolve())
        except ValueError:
            abort(403)
        if not target.is_file():
            abort(404)
    
        return send_from_directory(str(VENDOR_DIR), rel_path)
    
    
    @app.get("/api/problem-asset/<problem_id>/<path:asset_rel>")
    def problem_asset(problem_id: str, asset_rel: str):
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            abort(404)
    
        rel_path = (asset_rel or "").replace("\\", "/").strip()
        if not rel_path:
            abort(404)
    
        target = (folder / rel_path).resolve()
        try:
            target.relative_to(folder.resolve())
        except ValueError:
            abort(403)
    
        if not target.is_file():
            abort(404)
    
        return send_from_directory(str(folder), rel_path)
    
    
    @app.get("/api/similar-asset/<batch_id>/<candidate_id>/<path:asset_rel>")
    def similar_asset(batch_id: str, candidate_id: str, asset_rel: str):
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            abort(404)
    
        rel_path = (asset_rel or "").replace("\\", "/").strip()
        if not rel_path:
            abort(404)
    
        target = (folder / rel_path).resolve()
        try:
            target.relative_to(folder.resolve())
        except ValueError:
            abort(403)
        if not target.is_file():
            abort(404)
        return send_from_directory(str(folder), rel_path)
    
    
    @app.get("/api/problem-preview")
    def problem_preview():
        problem_id = request.args.get("id", "").strip()
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404
    
        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500
    
        preview = _build_preview_payload(
            problem_id=problem_id,
            q=parsed.q,
            choices=parsed.choices,
            answer=parsed.answer,
            solution=parsed.solution,
        )
        preview["id"] = parsed.display_id
        preview["warnings"] = parsed.warnings
        return jsonify(preview)
    
    
    @app.get("/api/problem-content")
    def problem_content():
        problem_id = request.args.get("id", "").strip()
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404
    
        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500
    
        return jsonify(
            {
                "id": parsed.display_id,
                **_serialize_problem_sections(parsed),
                "warnings": parsed.warnings,
            }
        )
    
    
    @app.post("/api/problem-preview-render")
    def problem_preview_render():
        payload = request.get_json(silent=True) or {}
        problem_id = str(payload.get("id", "")).strip()
        if _resolve_problem_folder_any(problem_id) is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        q = str(payload.get("q", "") or "")
        choices = str(payload.get("choices", "") or "")
        answer = str(payload.get("answer", "") or "")
        solution = str(payload.get("solution", "") or "")
    
        preview = _build_preview_payload(
            problem_id=problem_id,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
        preview["id"] = problem_id
        return jsonify(preview)
    
    
    @app.post("/api/problem-content")
    def update_problem_content():
        payload = request.get_json(silent=True) or {}
        problem_id = str(payload.get("id", "")).strip()
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404
    
        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500
    
        front = dict(parsed.front_matter or {})
        parsed_generated = _parse_generated_problem_ui_id(problem_id)
        if parsed_generated is None:
            front["id"] = problem_id
        else:
            _, candidate_id = parsed_generated
            existing_id = str(front.get("id", "")).strip()
            if existing_id:
                front["id"] = existing_id
            elif candidate_id:
                front["id"] = candidate_id
    
        q = str(payload.get("q", "") or "")
        choices = str(payload.get("choices", "") or "")
        answer = str(payload.get("answer", "") or "")
        solution = str(payload.get("solution", "") or "")
    
        try:
            _rewrite_problem_md_sections(
                problem_md,
                front,
                q=q,
                choices=choices,
                answer=answer,
                solution=solution,
            )
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "write-failed", "detail": str(exc)}), 500
    
        preview = _build_preview_payload(
            problem_id=problem_id,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
        return jsonify(
            {
                "ok": True,
                "id": problem_id,
                "sections": {
                    "q": q,
                    "choices": choices,
                    "answer": answer,
                    "solution": solution,
                },
                "preview": preview,
            }
        )
    
    
    @app.get("/api/problem-meta")
    def problem_meta():
        problem_id = request.args.get("id", "").strip()
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404
    
        try:
            parsed = parse_problem_file(problem_md)
            front = dict(parsed.front_matter or {})
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500
    
        payload = _serialize_problem_meta(problem_id, front)
        return jsonify({"id": problem_id, "meta": payload})


    @app.get("/api/problem-meta-list")
    def problem_meta_list():
        source_raw = request.args.get("source", "official")
        data_sources = _normalize_source_selector(source_raw)
        if data_sources is None:
            return jsonify({"error": "invalid-query", "detail": "source must be official|generated|all"}), 400

        generated_batches = _query_values("generated_batch")
        if not generated_batches:
            generated_batches = _query_values("generated_batches")
        generated_batches_arg = generated_batches if generated_batches else None

        rows = _scan_problem_meta(
            data_sources=data_sources,
            generated_batches=generated_batches_arg,
        )

        schools = set(_query_values("school"))
        years = set(_query_values("year"))
        grades = set(_query_values("grade"))
        semesters = set(_query_values("semester"))
        exams = {item.upper() for item in _query_values("exam")}
        subjects = {item.upper() for item in _query_values("subject")}
        levels = set(_query_values("level"))
        source_labels = set(_query_values("source_label"))
        pattern = str(request.args.get("pattern", "")).strip()
        unit_keyword = str(request.args.get("unit_keyword", "")).strip().lower()
        selector_ids = _query_values("selector_id")
        if not selector_ids:
            selector_ids = _query_values("selector_ids")
        if not selector_ids:
            selector_ids = _query_values("id")
        selector_id_order: Dict[str, int] = {}
        selector_id_set = set()
        for token in selector_ids:
            item = str(token or "").strip()
            if not item or item in selector_id_set:
                continue
            selector_id_order[item] = len(selector_id_order)
            selector_id_set.add(item)

        filtered: List[Dict[str, str]] = []
        for row in rows:
            row_id = str(row.get("id", "") or "")
            row_display_id = str(row.get("display_id", "") or "")
            row_problem_id = str(row.get("problem_id", "") or "")
            if selector_id_set and row_id not in selector_id_set and row_display_id not in selector_id_set and row_problem_id not in selector_id_set:
                continue
            if not _match_filter_value(row, "school", schools):
                continue
            if not _match_filter_value(row, "year", years):
                continue
            if not _match_filter_value(row, "grade", grades):
                continue
            if not _match_filter_value(row, "semester", semesters):
                continue
            exam_token = str(row.get("exam", "") or "").strip().upper()
            if exams and exam_token not in exams:
                continue
            subject_token = str(row.get("subject", "") or "").strip().upper()
            if subjects and subject_token not in subjects:
                continue
            if not _match_filter_value(row, "level", levels):
                continue
            if not _match_filter_value(row, "source_label", source_labels):
                continue
            if unit_keyword and unit_keyword not in str(row.get("unit", "") or "").strip().lower():
                continue
            if pattern:
                pattern_token = pattern.strip()
                id_candidates = (
                    row_id,
                    row_display_id,
                    row_problem_id,
                )
                lowered = pattern_token.lower()
                if any(char in pattern_token for char in "*?[]"):
                    matched = any(fnmatch.fnmatch(candidate, pattern_token) for candidate in id_candidates if candidate)
                else:
                    matched = any(lowered in candidate.lower() for candidate in id_candidates if candidate)
                if not matched:
                    continue
            filtered.append(_meta_row_for_client(row))

        if selector_id_order:
            missing_rank = len(selector_id_order) + 1

            def selector_sort_key(item: Dict[str, str]) -> tuple[int, str]:
                candidates = (
                    str(item.get("id", "") or ""),
                    str(item.get("display_id", "") or ""),
                    str(item.get("problem_id", "") or ""),
                )
                rank = min((selector_id_order.get(candidate, missing_rank) for candidate in candidates), default=missing_rank)
                return (rank, str(item.get("id", "") or ""))

            filtered.sort(key=selector_sort_key)

        page = _safe_positive_int(request.args.get("page"), default=1, minimum=1, maximum=500000)
        page_size = _safe_positive_int(request.args.get("page_size"), default=120, minimum=1, maximum=500)
        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        items = filtered[start:end] if start < total else []
        has_more = end < total

        return jsonify(
            {
                "ok": True,
                "source": data_sources[0] if len(data_sources) == 1 else "all",
                "page": page,
                "page_size": page_size,
                "total": total,
                "has_more": has_more,
                "items": items,
            }
        )


    @app.get("/api/problem-meta-filter-options")
    def problem_meta_filter_options():
        source_raw = request.args.get("source", "official")
        data_sources = _normalize_source_selector(source_raw)
        if data_sources is None:
            return jsonify({"error": "invalid-query", "detail": "source must be official|generated|all"}), 400

        rows = _scan_problem_meta(data_sources=data_sources)

        def distinct(key: str, *, numeric: bool = False, upper: bool = False) -> List[str]:
            values = set()
            for row in rows:
                token = str(row.get(key, "") or "").strip()
                if not token:
                    continue
                if upper:
                    token = token.upper()
                values.add(token)
            if not numeric:
                return sorted(values)
            return sorted(values, key=lambda item: (0, int(item)) if item.isdigit() else (1, item))

        return jsonify(
            {
                "ok": True,
                "source": data_sources[0] if len(data_sources) == 1 else "all",
                "schools": distinct("school", upper=True),
                "years": distinct("year", numeric=True),
                "grades": distinct("grade", numeric=True),
                "semesters": distinct("semester", numeric=True),
                "exams": distinct("exam", upper=True),
                "subjects": distinct("subject", upper=True),
                "levels": distinct("level", numeric=True),
            }
        )
    
    
    @app.post("/api/problem-meta")
    def update_problem_meta():
        payload = request.get_json(silent=True) or {}
        problem_id = str(payload.get("id", "")).strip()
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404
    
        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500
    
        front = dict(parsed.front_matter or {})
        from_id = _id_groups_for_problem_meta(problem_id, front)
        parsed_generated = _parse_generated_problem_ui_id(problem_id)
    
        def _pick(name: str, fallback: str = "") -> str:
            if name not in payload:
                return fallback
            return str(payload.get(name, "")).strip()
    
        try:
            school = _pick("school", str(front.get("school") or from_id.get("school") or "")).upper().strip()
            year = _pick("year", str(front.get("year") or from_id.get("year") or "").strip())
            grade = _pick("grade", str(front.get("grade") or from_id.get("grade") or "").strip())
            semester = _pick("semester", str(front.get("semester") or from_id.get("semester") or "").strip())
            exam = _pick("exam", str(front.get("exam") or from_id.get("exam") or "").strip()).upper()
            raw_subject = _pick("subject", str(front.get("subject") or from_id.get("subject") or "").strip())
            qtype = _pick("type", str(front.get("type", "")).strip())
    
            source_no = _pick(
                "source_question_no",
                _extract_source_no_from_front_matter(front) or _fallback_source_no(str(from_id.get("number", "")), front),
            )
            source_kind = _pick(
                "source_question_kind",
                _extract_source_kind(front, str(from_id.get("number", ""))),
            ).lower()
            source_label = _pick("source_question_label", str(front.get("source_question_label", "")).strip())
            level_token = _pick("level", _extract_level_from_front_matter(front))
            difficulty_token = _pick("difficulty", str(front.get("difficulty", "")).strip())
    
            if not school:
                raise ValueError("'school' is required.")
            year_value = _safe_int_token(year, "year")
            grade_value = _safe_int_token(grade, "grade")
            semester_value = _safe_int_token(semester, "semester")
            source_no_value = _safe_int_token(source_no, "source_question_no")
            if source_kind not in {"objective", "subjective"}:
                raise ValueError("'source_question_kind' must be objective or subjective.")
    
            if not source_label:
                source_label = f"서답{source_no_value}번" if source_kind == "subjective" else str(source_no_value)
    
            parsed_level = None
            if level_token:
                parsed_level = _safe_int_token(level_token, "level")
            elif difficulty_token:
                parsed_level = _safe_int_token(difficulty_token, "difficulty")
            if parsed_level is None:
                parsed_level = 3
            parsed_level = max(1, min(5, int(parsed_level)))
    
            unit_l1_input = _pick("unit_l1", str(front.get("unit_l1", "")).strip())
            unit_l2_input = _pick("unit_l2", str(front.get("unit_l2", "")).strip())
            unit_l3_input = _pick("unit_l3", str(front.get("unit_l3", "")).strip())
            if not unit_l1_input or not unit_l2_input or not unit_l3_input:
                raise ValueError("'unit_l1', 'unit_l2', 'unit_l3' are required.")
            unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
                unit_l1_input,
                unit_l2_input,
                unit_l3_input,
                grade=grade_value,
            )
            subject = _normalize_subject_code(raw_subject, unit_l1=unit_l1, fallback=from_id.get("subject") or "")
        except ValueError as exc:
            return jsonify({"error": "invalid-payload", "detail": str(exc)}), 400
    
        if parsed_generated is None:
            front["id"] = problem_id
        else:
            _, candidate_id = parsed_generated
            existing_id = str(front.get("id", "")).strip()
            if existing_id:
                front["id"] = existing_id
            elif candidate_id:
                front["id"] = candidate_id
        front["school"] = school
        front["year"] = year_value
        front["grade"] = grade_value
        front["semester"] = semester_value
        front["exam"] = exam
        front["subject"] = subject
        front["type"] = qtype
        front["source_question_no"] = source_no_value
        front["source_question_kind"] = source_kind
        front["source_question_label"] = source_label
        front["difficulty"] = parsed_level
        front["level"] = parsed_level
        front["unit_l1"] = unit_l1
        front["unit_l2"] = unit_l2
        front["unit_l3"] = unit_l3
        front["unit"] = f"{unit_l1}>{unit_l2}>{unit_l3}"
    
        try:
            _rewrite_problem_md(problem_md, front, parsed)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "write-failed", "detail": str(exc)}), 500
    
        refreshed = _refresh_problem_meta_row(problem_id)
        if refreshed is None:
            refreshed = _serialize_problem_meta(problem_id, front)
        return jsonify({"ok": True, "id": problem_id, "row": refreshed})
    
    
    @app.post("/api/problem-delete")
    def delete_problem():
        payload = request.get_json(silent=True) or {}
        problem_id = str(payload.get("id", "")).strip()
        if not problem_id:
            return jsonify({"error": "invalid-payload", "detail": "'id' is required."}), 400
    
        folder = _resolve_problem_folder(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        try:
            _invalidate_front_matter_cache_for_folder(folder)
            shutil.rmtree(folder)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "delete-failed", "detail": str(exc)}), 500
    
        return jsonify({"ok": True, "id": problem_id})
    
    
    @app.post("/api/problem-open-folder")
    def open_problem_folder():
        payload = request.get_json(silent=True) or {}
        problem_id = str(payload.get("id", "")).strip()
        if not problem_id:
            return jsonify({"error": "invalid-payload", "detail": "'id' is required."}), 400
    
        folder = _resolve_problem_folder_any(problem_id)
        if folder is None:
            return jsonify({"error": "problem-not-found"}), 404
    
        try:
            _open_path_in_file_manager(folder)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "open-failed", "detail": str(exc)}), 500
    
        return jsonify({"ok": True, "id": problem_id, "path": str(folder)})
    
    
