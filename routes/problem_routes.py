from __future__ import annotations

from typing import Any, Dict

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
    _serialize_problem_meta = deps["_serialize_problem_meta"]
    _serialize_problem_sections = deps["_serialize_problem_sections"]

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
    
    
