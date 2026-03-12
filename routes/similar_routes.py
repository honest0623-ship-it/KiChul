from __future__ import annotations

from typing import Any, Dict, List

from flask import jsonify, request


def register_similar_routes(app, deps: Dict[str, Any]) -> None:
    AI_CONFIG_LOCK = deps["AI_CONFIG_LOCK"]
    AI_RUNTIME_CONFIG = deps["AI_RUNTIME_CONFIG"]
    AI_SUPPORTED_PROVIDERS = deps["AI_SUPPORTED_PROVIDERS"]
    DB_GENERATED_CANDIDATES_DIR = deps["DB_GENERATED_CANDIDATES_DIR"]
    DB_PROBLEMS_DIR = deps["DB_PROBLEMS_DIR"]
    DRAFT_TOKEN = deps["DRAFT_TOKEN"]
    PROBLEM_ID_RE = deps["PROBLEM_ID_RE"]
    SIMILAR_GENERATION_MAX_ATTEMPTS = deps["SIMILAR_GENERATION_MAX_ATTEMPTS"]
    SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST = deps["SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST"]
    SIMILAR_PROMOTION_ENABLED = deps["SIMILAR_PROMOTION_ENABLED"]
    SequenceMatcher = deps["SequenceMatcher"]
    datetime = deps["datetime"]
    json = deps["json"]
    normalize_unit_triplet = deps["normalize_unit_triplet"]
    parse_problem_file = deps["parse_problem_file"]
    shutil = deps["shutil"]

    _as_positive_int = deps["_as_positive_int"]
    _batch_report_path = deps["_batch_report_path"]
    _build_similar_candidate_id = deps["_build_similar_candidate_id"]
    _build_similar_generation_prompt = deps["_build_similar_generation_prompt"]
    _build_similar_preview_payload = deps["_build_similar_preview_payload"]
    _call_ai_model_text = deps["_call_ai_model_text"]
    _collect_batch_candidate_dirs = deps["_collect_batch_candidate_dirs"]
    _count_choice_lines = deps["_count_choice_lines"]
    _current_ai_runtime_secret = deps["_current_ai_runtime_secret"]
    _default_ai_model = deps["_default_ai_model"]
    _extract_ids = deps["_extract_ids"]
    _invalidate_front_matter_cache_for_folder = deps["_invalidate_front_matter_cache_for_folder"]
    _is_generation_retryable_error = deps["_is_generation_retryable_error"]
    _is_timeout_generation_error = deps["_is_timeout_generation_error"]
    _latex_balance_issues = deps["_latex_balance_issues"]
    _list_generated_batch_ids = deps["_list_generated_batch_ids"]
    _model_allowed_for_provider = deps["_model_allowed_for_provider"]
    _next_problem_id_for_prefix = deps["_next_problem_id_for_prefix"]
    _normalize_ai_provider = deps["_normalize_ai_provider"]
    _normalize_for_similarity = deps["_normalize_for_similarity"]
    _normalize_runtime_config_unlocked = deps["_normalize_runtime_config_unlocked"]
    _now_iso = deps["_now_iso"]
    _objective_like_candidate = deps["_objective_like_candidate"]
    _parse_generated_sections = deps["_parse_generated_sections"]
    _parse_int = deps["_parse_int"]
    _provider_display_name = deps["_provider_display_name"]
    _resolve_problem_folder = deps["_resolve_problem_folder"]
    _resolve_similar_candidate_folder = deps["_resolve_similar_candidate_folder"]
    _rewrite_problem_md_sections = deps["_rewrite_problem_md_sections"]
    _save_source_snapshot = deps["_save_source_snapshot"]
    _seed_ids_from_payload = deps["_seed_ids_from_payload"]
    _serialize_ai_runtime_config = deps["_serialize_ai_runtime_config"]
    _serialize_problem_sections = deps["_serialize_problem_sections"]
    _unique_batch_id = deps["_unique_batch_id"]

    @app.get("/api/ai-config")
    def get_ai_config():
        return jsonify(_serialize_ai_runtime_config())


    @app.post("/api/ai-config")
    def update_ai_config():
        payload = request.get_json(silent=True) or {}

        provider_input = str(payload.get("provider", "gemini") or "gemini").strip().lower()
        if provider_input and provider_input not in AI_SUPPORTED_PROVIDERS:
            return jsonify({"error": "invalid-payload", "detail": f"Unsupported provider: {provider_input}"}), 400
        provider = _normalize_ai_provider(provider_input)

        model = str(payload.get("model", "") or "").strip() or _default_ai_model(provider)
        if not _model_allowed_for_provider(provider, model):
            return (
                jsonify(
                    {
                        "error": "invalid-payload",
                        "detail": f"Unsupported model for provider `{provider}`: {model}",
                    }
                ),
                400,
            )
        clear_api_key = bool(payload.get("clear_api_key"))
        api_key_raw = payload.get("api_key", None)

        changed = False
        with AI_CONFIG_LOCK:
            current_provider, _, keys, _ = _normalize_runtime_config_unlocked()
            if current_provider != provider:
                AI_RUNTIME_CONFIG["provider"] = provider
                changed = True

            if str(AI_RUNTIME_CONFIG.get("model", "")).strip() != model:
                AI_RUNTIME_CONFIG["model"] = model
                changed = True

            if clear_api_key:
                if str(keys.get(provider, "")).strip():
                    keys[provider] = ""
                    changed = True
            elif api_key_raw is not None:
                token = str(api_key_raw or "").strip()
                if token and token != str(keys.get(provider, "")).strip():
                    keys[provider] = token
                    changed = True

            if changed:
                AI_RUNTIME_CONFIG["updated_at"] = _now_iso()

        summary = _serialize_ai_runtime_config()
        return jsonify({"ok": True, **summary})


    @app.post("/api/similar-generate")
    def generate_similar_candidates():
        payload = request.get_json(silent=True) or {}
        seed_ids = _seed_ids_from_payload(payload)
        if not seed_ids:
            return jsonify({"error": "invalid-payload", "detail": "seed_ids is required."}), 400
        if len(seed_ids) > SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST:
            return (
                jsonify(
                    {
                        "error": "too-many-seeds",
                        "detail": (
                            f"seed_ids can contain up to {SIMILAR_GENERATION_MAX_SEEDS_PER_REQUEST} items per request. "
                            "Split into smaller chunks and retry."
                        ),
                    }
                ),
                400,
            )

        variants_per_seed = _as_positive_int(payload.get("variants_per_seed"), 1, min_value=1, max_value=5)
        similarity_type = str(payload.get("similarity_type", "parameter_change") or "parameter_change").strip()
        requested_batch_id = str(payload.get("batch_id", "") or "").strip()
        temperature_raw = payload.get("temperature", 0.45)
        try:
            temperature = float(temperature_raw)
        except (TypeError, ValueError):
            temperature = 0.45
        if temperature < 0.0:
            temperature = 0.0
        if temperature > 1.0:
            temperature = 1.0

        ai = _current_ai_runtime_secret()
        provider = _normalize_ai_provider(ai.get("provider", "gemini"))
        if provider not in AI_SUPPORTED_PROVIDERS:
            return jsonify({"error": "provider-not-supported", "detail": f"Unsupported provider: {provider}"}), 400
        api_key = ai.get("api_key", "")
        if not api_key:
            provider_label = _provider_display_name(provider)
            return jsonify({"error": "ai-not-configured", "detail": f"{provider_label} API key is not set."}), 400

        model_from_payload = str(payload.get("model", "") or "").strip()
        model = model_from_payload or ai.get("model", _default_ai_model(provider))
        if not model:
            model = _default_ai_model(provider)
        if not _model_allowed_for_provider(provider, model):
            return (
                jsonify(
                    {
                        "error": "invalid-payload",
                        "detail": f"Unsupported model for provider `{provider}`: {model}",
                    }
                ),
                400,
            )

        DB_GENERATED_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        batch_id = _unique_batch_id(requested_batch_id)

        created_rows: List[Dict[str, Any]] = []
        failed_rows: List[Dict[str, Any]] = []
        skipped_rows: List[Dict[str, Any]] = []

        for seed_id in seed_ids:
            seed_folder = _resolve_problem_folder(seed_id)
            if seed_folder is None:
                skipped_rows.append({"seed_id": seed_id, "reason": "seed-not-found"})
                continue
            seed_md = seed_folder / "problem.md"
            if not seed_md.is_file():
                skipped_rows.append({"seed_id": seed_id, "reason": "seed-problem-md-not-found"})
                continue

            try:
                seed_parsed = parse_problem_file(seed_md)
            except Exception as exc:  # pylint: disable=broad-except
                skipped_rows.append({"seed_id": seed_id, "reason": f"seed-parse-failed: {exc}"})
                continue

            seed_front = dict(seed_parsed.front_matter or {})
            objective = _objective_like_candidate(seed_front, seed_id)
            grade = str(seed_front.get("grade", "") or "").strip()
            raw_unit = str(seed_front.get("unit", "") or "").strip()
            unit_l1, unit_l2, unit_l3 = normalize_unit_triplet(
                str(seed_front.get("unit_l1", "")).strip(),
                str(seed_front.get("unit_l2", "")).strip(),
                str(seed_front.get("unit_l3", "")).strip(),
                unit_path=raw_unit,
                grade=_parse_int(grade, 0) or None,
            )

            for variant_index in range(1, variants_per_seed + 1):
                candidate_id = _build_similar_candidate_id(
                    seed_id=seed_id,
                    variant_index=variant_index,
                    variants_per_seed=variants_per_seed,
                    batch_dir=DB_GENERATED_CANDIDATES_DIR,
                )
                candidate_dir = DB_GENERATED_CANDIDATES_DIR / candidate_id
                candidate_dir.mkdir(parents=True, exist_ok=False)

                prompt = _build_similar_generation_prompt(
                    seed_id=seed_id,
                    seed_q=seed_parsed.q,
                    seed_choices=seed_parsed.choices,
                    seed_answer=seed_parsed.answer,
                    seed_solution=seed_parsed.solution,
                    grade=grade or "?",
                    unit_l1=unit_l1 or "?",
                    unit_l2=unit_l2 or "?",
                    unit_l3=unit_l3 or "?",
                    similarity_type=similarity_type,
                    objective=objective,
                    variant_index=variant_index,
                )
                (candidate_dir / "prompt.md").write_text(prompt, encoding="utf-8")
                _save_source_snapshot(
                    candidate_dir,
                    seed_id=seed_id,
                    q=seed_parsed.q,
                    choices=seed_parsed.choices,
                    answer=seed_parsed.answer,
                    solution=seed_parsed.solution,
                )

                front = dict(seed_front)
                front["id"] = candidate_id
                front["derived_from"] = seed_id
                front["similarity_type"] = similarity_type
                front["generation_batch_id"] = batch_id
                front["generation_model"] = f"{provider}:{model}"
                front["review_status"] = "pending"
                front["review_note"] = ""
                front["promoted_to"] = ""
                front["generated_at"] = _now_iso()

                generated_sections: Dict[str, str] | None = None
                last_error = ""
                attempt_prompt = prompt
                active_model = model
                model_used_for_candidate = model
                fallback_downgraded = False
                for attempt in range(1, SIMILAR_GENERATION_MAX_ATTEMPTS + 1):
                    try:
                        text = _call_ai_model_text(
                            provider=provider,
                            api_key=api_key,
                            model=active_model,
                            prompt=attempt_prompt,
                            temperature=temperature,
                        )
                        candidate_sections = _parse_generated_sections(text)
                        if objective and _count_choice_lines(candidate_sections.get("choices", "")) < 4:
                            raise ValueError("Generated objective choices are insufficient.")
                        if any(DRAFT_TOKEN in candidate_sections.get(key, "") for key in ("q", "choices", "answer", "solution")):
                            raise ValueError("Generated output still contains draft token.")
                        generated_sections = candidate_sections
                        model_used_for_candidate = active_model
                        break
                    except Exception as exc:  # pylint: disable=broad-except
                        last_error = str(exc).strip() or exc.__class__.__name__
                        if provider == "openai" and (not fallback_downgraded) and _is_timeout_generation_error(last_error):
                            fallback_model = _default_ai_model("openai")
                            if fallback_model and fallback_model != active_model:
                                active_model = fallback_model
                                fallback_downgraded = True
                                continue
                        should_retry = (
                            attempt < SIMILAR_GENERATION_MAX_ATTEMPTS
                            and _is_generation_retryable_error(last_error)
                        )
                        if not should_retry:
                            break
                        attempt_prompt = (
                            f"{prompt}\n\n"
                            "직전 출력은 형식 검증에 실패했다. 아래 오류를 반영해 JSON만 다시 출력하라.\n"
                            f"- 오류: {last_error}\n"
                        )
                        continue

                front["generation_model"] = f"{provider}:{model_used_for_candidate}"

                if generated_sections is None:
                    failed_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "seed_id": seed_id,
                            "reason": last_error or "unknown-generation-error",
                        }
                    )
                    generated_sections = {
                        "q": f"{DRAFT_TOKEN} generation failed. seed={seed_id}",
                        "choices": "1) \n2) \n3) \n4) \n5) " if objective else "",
                        "answer": f"{DRAFT_TOKEN} generation failed",
                        "solution": f"{DRAFT_TOKEN} generation failed",
                    }
                    front["review_note"] = f"auto-generation failed: {last_error}".strip()

                try:
                    _rewrite_problem_md_sections(
                        candidate_dir / "problem.md",
                        front,
                        q=generated_sections["q"],
                        choices=generated_sections["choices"],
                        answer=generated_sections["answer"],
                        solution=generated_sections["solution"],
                    )
                except Exception as exc:  # pylint: disable=broad-except
                    failed_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "seed_id": seed_id,
                            "reason": f"write-failed: {exc}",
                        }
                    )
                    continue

                created_rows.append(
                    {
                        "candidate_id": candidate_id,
                        "seed_id": seed_id,
                        "objective": objective,
                        "status": "generated" if DRAFT_TOKEN not in generated_sections["q"] else "draft-fallback",
                    }
                )

        manifest = {
            "batch_id": batch_id,
            "created_at": _now_iso(),
            "provider": provider,
            "model": model,
            "similarity_type": similarity_type,
            "variants_per_seed": variants_per_seed,
            "seed_ids": seed_ids,
            "summary": {
                "requested_seed_count": len(seed_ids),
                "created": len(created_rows),
                "failed": len(failed_rows),
                "skipped": len(skipped_rows),
            },
            "created": created_rows,
            "failed": failed_rows,
            "skipped": skipped_rows,
        }
        manifest_path = _batch_report_path(batch_id, "manifest")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        return jsonify(
            {
                "ok": True,
                "batch_id": batch_id,
                "batch_path": str(DB_GENERATED_CANDIDATES_DIR),
                "manifest_path": str(manifest_path),
                "summary": manifest["summary"],
                "created": created_rows,
                "failed": failed_rows,
                "skipped": skipped_rows,
            }
        )


    @app.get("/api/similar-batches")
    def similar_batches():
        rows: List[Dict[str, Any]] = []
        if not DB_GENERATED_CANDIDATES_DIR.is_dir():
            return jsonify({"batches": rows})

        for batch_id in sorted(_list_generated_batch_ids(), reverse=True):
            candidate_dirs = _collect_batch_candidate_dirs(batch_id)
            if not candidate_dirs:
                continue
            validation_summary = {"total": 0, "ok": 0, "failed": 0}
            report_path = _batch_report_path(batch_id, "validation_report")
            legacy_report_path = DB_GENERATED_CANDIDATES_DIR / batch_id / "validation_report.json"
            if not report_path.is_file() and legacy_report_path.is_file():
                report_path = legacy_report_path

            if report_path.is_file():
                try:
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                    if isinstance(report, dict):
                        raw_summary = report.get("summary", {})
                        if isinstance(raw_summary, dict):
                            validation_summary = {
                                "total": int(raw_summary.get("total", 0) or 0),
                                "ok": int(raw_summary.get("ok", 0) or 0),
                                "failed": int(raw_summary.get("failed", 0) or 0),
                            }
                except Exception:
                    validation_summary = {"total": 0, "ok": 0, "failed": 0}

            latest_mtime = 0.0
            for candidate_dir in candidate_dirs.values():
                try:
                    latest_mtime = max(latest_mtime, candidate_dir.stat().st_mtime)
                except Exception:
                    continue

            rows.append(
                {
                    "batch_id": batch_id,
                    "candidate_count": len(candidate_dirs),
                    "created_at": datetime.fromtimestamp(latest_mtime).isoformat(timespec="seconds") if latest_mtime else "",
                    "validation": validation_summary,
                }
            )
        return jsonify({"batches": rows})


    @app.get("/api/similar-candidates")
    def similar_candidates():
        batch_id = request.args.get("batch_id", "").strip()
        candidate_dirs = _collect_batch_candidate_dirs(batch_id)
        if not candidate_dirs:
            return jsonify({"error": "batch-not-found"}), 404

        validation_index: Dict[str, Dict[str, Any]] = {}
        report_path = _batch_report_path(batch_id, "validation_report")
        legacy_report_path = DB_GENERATED_CANDIDATES_DIR / batch_id / "validation_report.json"
        if not report_path.is_file() and legacy_report_path.is_file():
            report_path = legacy_report_path
        if report_path.is_file():
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                for row in report.get("results", []) if isinstance(report, dict) else []:
                    candidate_id = str(row.get("candidate_id", "")).strip()
                    if candidate_id:
                        validation_index[candidate_id] = row
            except Exception:
                validation_index = {}

        rows: List[Dict[str, Any]] = []
        for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
            candidate_id = cdir.name
            try:
                parsed = parse_problem_file(cdir / "problem.md")
            except Exception as exc:  # pylint: disable=broad-except
                rows.append(
                    {
                        "candidate_id": candidate_id,
                        "review_status": "parse-failed",
                        "review_note": str(exc),
                        "derived_from": "",
                    }
                )
                continue

            front = dict(parsed.front_matter or {})
            has_draft = any(
                DRAFT_TOKEN in str(section or "")
                for section in (parsed.q, parsed.choices, parsed.answer, parsed.solution)
            )
            review_note = str(front.get("review_note", "")).strip()
            validation = validation_index.get(candidate_id, {})
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "derived_from": str(front.get("derived_from", "")).strip(),
                    "similarity_type": str(front.get("similarity_type", "")).strip(),
                    "review_status": str(front.get("review_status", "pending") or "pending").strip().lower(),
                    "review_note": review_note,
                    "has_draft": has_draft,
                    "auto_failed": review_note.lower().startswith("auto-generation failed"),
                    "promoted_to": str(front.get("promoted_to", "")).strip(),
                    "generation_batch_id": str(front.get("generation_batch_id", "")).strip(),
                    "warnings": parsed.warnings,
                    "validation": {
                        "ok": bool(validation.get("ok", False)) if validation else None,
                        "error_count": len(validation.get("errors", [])) if isinstance(validation, dict) else 0,
                        "warning_count": len(validation.get("warnings", [])) if isinstance(validation, dict) else 0,
                        "similarity_ratio": validation.get("similarity_ratio") if isinstance(validation, dict) else None,
                    },
                }
            )
        return jsonify({"batch_id": batch_id, "candidates": rows})


    @app.get("/api/similar-preview")
    def similar_preview():
        batch_id = request.args.get("batch_id", "").strip()
        candidate_id = request.args.get("candidate_id", "").strip()
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404

        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

        preview = _build_similar_preview_payload(
            batch_id=batch_id,
            candidate_id=candidate_id,
            q=parsed.q,
            choices=parsed.choices,
            answer=parsed.answer,
            solution=parsed.solution,
        )
        preview["batch_id"] = batch_id
        preview["candidate_id"] = candidate_id
        preview["warnings"] = parsed.warnings
        return jsonify(preview)


    @app.get("/api/similar-content")
    def similar_content():
        batch_id = request.args.get("batch_id", "").strip()
        candidate_id = request.args.get("candidate_id", "").strip()
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404

        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

        front = dict(parsed.front_matter or {})
        return jsonify(
            {
                "batch_id": batch_id,
                "candidate_id": candidate_id,
                **_serialize_problem_sections(parsed),
                "review_status": str(front.get("review_status", "pending") or "pending").strip().lower(),
                "review_note": str(front.get("review_note", "")).strip(),
                "derived_from": str(front.get("derived_from", "")).strip(),
                "warnings": parsed.warnings,
            }
        )


    @app.post("/api/similar-preview-render")
    def render_similar_preview_draft():
        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_id = str(payload.get("candidate_id", "")).strip()
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404

        q = str(payload.get("q", "") or "")
        choices = str(payload.get("choices", "") or "")
        answer = str(payload.get("answer", "") or "")
        solution = str(payload.get("solution", "") or "")

        preview = _build_similar_preview_payload(
            batch_id=batch_id,
            candidate_id=candidate_id,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
        return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "preview": preview})


    @app.post("/api/similar-content")
    def update_similar_content():
        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_id = str(payload.get("candidate_id", "")).strip()
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404

        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

        front = dict(parsed.front_matter or {})
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

        preview = _build_similar_preview_payload(
            batch_id=batch_id,
            candidate_id=candidate_id,
            q=q,
            choices=choices,
            answer=answer,
            solution=solution,
        )
        return jsonify(
            {
                "ok": True,
                "batch_id": batch_id,
                "candidate_id": candidate_id,
                "sections": {"q": q, "choices": choices, "answer": answer, "solution": solution},
                "preview": preview,
            }
        )


    @app.post("/api/similar-review")
    def update_similar_review():
        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_id = str(payload.get("candidate_id", "")).strip()
        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404
        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return jsonify({"error": "problem-file-not-found"}), 404

        status = str(payload.get("review_status", "")).strip().lower()
        if status not in {"pending", "approved", "rejected"}:
            return jsonify({"error": "invalid-payload", "detail": "review_status must be pending|approved|rejected"}), 400
        note = str(payload.get("review_note", "") or "").strip()

        try:
            parsed = parse_problem_file(problem_md)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "problem-parse-failed", "detail": str(exc)}), 500

        front = dict(parsed.front_matter or {})
        front["id"] = candidate_id
        front["review_status"] = status
        front["review_note"] = note
        front["reviewed_at"] = _now_iso()

        try:
            _rewrite_problem_md_sections(
                problem_md,
                front,
                q=parsed.q,
                choices=parsed.choices,
                answer=parsed.answer,
                solution=parsed.solution,
            )
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "write-failed", "detail": str(exc)}), 500

        return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "review_status": status, "review_note": note})


    @app.post("/api/similar-delete")
    def delete_similar_candidate():
        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_id = str(payload.get("candidate_id", "")).strip()
        if not batch_id or not candidate_id:
            return jsonify({"error": "invalid-payload", "detail": "batch_id and candidate_id are required"}), 400

        folder = _resolve_similar_candidate_folder(batch_id, candidate_id)
        if folder is None:
            return jsonify({"error": "candidate-not-found"}), 404

        try:
            resolved_folder = folder.resolve()
        except Exception:
            resolved_folder = folder

        try:
            resolved_folder.relative_to(DB_GENERATED_CANDIDATES_DIR.resolve())
        except ValueError:
            return jsonify({"error": "candidate-not-found"}), 404

        if not resolved_folder.is_dir():
            return jsonify({"error": "candidate-not-found"}), 404

        try:
            _invalidate_front_matter_cache_for_folder(resolved_folder)
            shutil.rmtree(resolved_folder)
        except Exception as exc:  # pylint: disable=broad-except
            return jsonify({"error": "delete-failed", "detail": str(exc)}), 500

        legacy_batch_dir = DB_GENERATED_CANDIDATES_DIR / batch_id
        if legacy_batch_dir.is_dir():
            try:
                if resolved_folder.parent.resolve() == legacy_batch_dir.resolve() and not any(legacy_batch_dir.iterdir()):
                    legacy_batch_dir.rmdir()
            except Exception:
                # Empty legacy batch folder cleanup is best-effort only.
                pass

        return jsonify({"ok": True, "batch_id": batch_id, "candidate_id": candidate_id, "deleted_path": str(resolved_folder)})


    @app.post("/api/similar-validate")
    def validate_similar_batch():
        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_dirs = _collect_batch_candidate_dirs(batch_id)
        if not candidate_dirs:
            return jsonify({"error": "batch-not-found"}), 404

        candidate_ids_raw = str(payload.get("candidate_ids", "") or "").strip()
        selected_ids = set(_extract_ids(candidate_ids_raw))
        max_similarity = payload.get("max_similarity", 0.92)
        try:
            max_similarity_value = float(max_similarity)
        except (TypeError, ValueError):
            return jsonify({"error": "invalid-payload", "detail": "max_similarity must be numeric"}), 400

        results: List[Dict[str, Any]] = []
        for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
            candidate_id = cdir.name
            if selected_ids and candidate_id not in selected_ids:
                continue

            errors: List[str] = []
            warnings: List[str] = []
            similarity_ratio = 0.0
            try:
                parsed = parse_problem_file(cdir / "problem.md")
            except Exception as exc:  # pylint: disable=broad-except
                results.append(
                    {
                        "candidate_id": candidate_id,
                        "ok": False,
                        "similarity_ratio": 1.0,
                        "errors": [f"Parse failed: {exc}"],
                        "warnings": [],
                    }
                )
                continue

            front = dict(parsed.front_matter or {})
            for section_name in ("q", "choices", "answer", "solution"):
                value = str(getattr(parsed, section_name, "") or "").strip()
                if not value:
                    errors.append(f"Section `{section_name}` is empty.")
                if DRAFT_TOKEN in value:
                    errors.append(f"Section `{section_name}` still contains draft token.")
                for issue in _latex_balance_issues(value):
                    warnings.append(f"{section_name}: {issue}")

            if _objective_like_candidate(front, candidate_id):
                count = _count_choice_lines(parsed.choices)
                if count < 4:
                    errors.append(f"Objective question has too few option-like lines ({count}).")

            derived_from = str(front.get("derived_from", "")).strip()
            if derived_from:
                source_md = DB_PROBLEMS_DIR / derived_from / "problem.md"
                if source_md.is_file():
                    try:
                        source = parse_problem_file(source_md)
                        similarity_ratio = SequenceMatcher(
                            None,
                            _normalize_for_similarity(source.q),
                            _normalize_for_similarity(parsed.q),
                        ).ratio()
                        if similarity_ratio > max_similarity_value:
                            errors.append(
                                f"Q similarity too high vs source ({similarity_ratio:.3f} > {max_similarity_value:.3f})."
                            )
                        elif similarity_ratio > max_similarity_value - 0.08:
                            warnings.append(f"Q similarity near threshold ({similarity_ratio:.3f}).")
                    except Exception as exc:  # pylint: disable=broad-except
                        warnings.append(f"Source parse failed for similarity check: {exc}")
                else:
                    warnings.append(f"Source problem not found: {derived_from}")
            else:
                warnings.append("`derived_from` is missing.")

            results.append(
                {
                    "candidate_id": candidate_id,
                    "ok": len(errors) == 0,
                    "similarity_ratio": similarity_ratio,
                    "errors": errors,
                    "warnings": warnings,
                }
            )

        failed = [row for row in results if not row.get("ok")]
        report = {
            "batch_id": batch_id,
            "validated_at": _now_iso(),
            "max_similarity": max_similarity_value,
            "summary": {"total": len(results), "ok": len(results) - len(failed), "failed": len(failed)},
            "results": results,
        }
        report_path = _batch_report_path(batch_id, "validation_report")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return jsonify({"ok": True, "batch_id": batch_id, "summary": report["summary"], "results": results, "report_path": str(report_path)})


    @app.post("/api/similar-promote")
    def promote_similar_candidates():
        if not SIMILAR_PROMOTION_ENABLED:
            return jsonify(
                {
                    "error": "policy-disabled",
                    "detail": "Promotion is disabled by policy. Official DB and generated candidates DB must remain separated.",
                }
            ), 403

        payload = request.get_json(silent=True) or {}
        batch_id = str(payload.get("batch_id", "")).strip()
        candidate_dirs = _collect_batch_candidate_dirs(batch_id)
        if not candidate_dirs:
            return jsonify({"error": "batch-not-found"}), 404

        selected_ids = set(_extract_ids(str(payload.get("candidate_ids", "") or "").strip()))
        force = bool(payload.get("force"))

        promoted: List[Dict[str, str]] = []
        skipped: List[Dict[str, str]] = []

        for cdir in sorted(candidate_dirs.values(), key=lambda p: p.name):
            candidate_id = cdir.name
            if selected_ids and candidate_id not in selected_ids:
                continue
            try:
                parsed = parse_problem_file(cdir / "problem.md")
            except Exception as exc:  # pylint: disable=broad-except
                skipped.append({"candidate_id": candidate_id, "reason": f"parse-failed: {exc}"})
                continue
            front = dict(parsed.front_matter or {})
            status = str(front.get("review_status", "")).strip().lower()
            if status != "approved" and not force:
                skipped.append({"candidate_id": candidate_id, "reason": f"review_status={status or 'none'}"})
                continue
            if any(DRAFT_TOKEN in str(getattr(parsed, sec, "") or "") for sec in ("q", "choices", "answer", "solution")):
                skipped.append({"candidate_id": candidate_id, "reason": "contains-draft-token"})
                continue

            derived_from = str(front.get("derived_from", "")).strip()
            source_match = PROBLEM_ID_RE.match(derived_from)
            if not source_match:
                skipped.append({"candidate_id": candidate_id, "reason": "invalid-derived_from"})
                continue

            prefix = derived_from.rsplit("-", 1)[0]
            try:
                new_id = _next_problem_id_for_prefix(prefix)
            except ValueError as exc:
                skipped.append({"candidate_id": candidate_id, "reason": str(exc)})
                continue

            target_dir = DB_PROBLEMS_DIR / new_id
            if target_dir.exists():
                skipped.append({"candidate_id": candidate_id, "reason": "target-already-exists"})
                continue

            try:
                shutil.copytree(cdir, target_dir)
                for extra_name in ("prompt.md", "source_snapshot.md", "validation_report.json"):
                    extra = target_dir / extra_name
                    if extra.exists():
                        if extra.is_dir():
                            shutil.rmtree(extra)
                        else:
                            extra.unlink()

                promoted_front = dict(front)
                promoted_front["id"] = new_id
                promoted_front["promoted_from"] = candidate_id
                promoted_front["promoted_at"] = _now_iso()
                _rewrite_problem_md_sections(
                    target_dir / "problem.md",
                    promoted_front,
                    q=parsed.q,
                    choices=parsed.choices,
                    answer=parsed.answer,
                    solution=parsed.solution,
                )

                front["promoted_to"] = new_id
                front["review_status"] = "promoted"
                front["promoted_at"] = _now_iso()
                _rewrite_problem_md_sections(
                    cdir / "problem.md",
                    front,
                    q=parsed.q,
                    choices=parsed.choices,
                    answer=parsed.answer,
                    solution=parsed.solution,
                )
                promoted.append({"candidate_id": candidate_id, "new_problem_id": new_id})
            except Exception as exc:  # pylint: disable=broad-except
                skipped.append({"candidate_id": candidate_id, "reason": f"promote-failed: {exc}"})

        report = {
            "batch_id": batch_id,
            "promoted_at": _now_iso(),
            "promoted": promoted,
            "skipped": skipped,
        }
        report_path = _batch_report_path(batch_id, "promotion_report")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return jsonify(
            {
                "ok": True,
                "batch_id": batch_id,
                "promoted": promoted,
                "skipped": skipped,
                "report_path": str(report_path),
            }
        )

