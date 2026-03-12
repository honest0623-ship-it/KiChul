# CODEBASE_CONTEXT.md

This file is the quick context snapshot for this repository.
Read this first before making changes.

## 1) Project Summary

- Current project scope: render exam PDFs from existing markdown DB entries, edit per-problem metadata/body (`Q/Choices/Answer/Solution`) in web admin, and review offline-generated similar-problem candidates.
- Manual one-off DB ingest scripts for specific source sets still exist under `scripts/` and may be used for repository maintenance.
- Web app role: filter/select problems and call `build_exam.py`, plus review generated candidates under `db/generated_candidates`.
- Web app ingest/upload/auto-DB-generation workflows were removed on 2026-03-04.
- Repository-level maintenance may still use standalone manual ingest scripts; these are not part of the Flask UI flow.

## 2) Quick Start

```powershell
cd d:\Math_Kichul
python -m pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

- Web URL: `http://127.0.0.1:5000`
- Problem root: `db/problems`
- Output folder: `output`

## 3) Key Files

- `app.py`: Flask web UI for filtering/selecting problems and PDF generation.
- `routes/problem_routes.py`: Problem asset/preview/content/meta/edit/delete/open-folder API route registration.
- `routes/similar_routes.py`: AI runtime config + similar candidate generation/review/validation/promotion API route registration.
- `routes/render_routes.py`: Output-folder open + PDF render route registration.
- `templates/admin.html`: Web admin page shell/template (UI markup + bootstrap payload).
- `static/admin.js`: Main admin frontend logic (filters/sorting/editor/similar-candidate workflows).
- `build_exam.py`: CLI entry point for exam/answer/solution PDF generation.
- `parser.py`: Parses `problem.md` (front-matter + sections).
- `renderer.py`: HTML/MathJax render and Playwright PDF output.
- `services/ai_runtime.py`: AI provider model catalog + generation API call/parsing utilities.
- `templates/exam.html`: print layout template.

## 4) Request Flow

### 4.1 Web render (`POST /render`)

1. Load metadata from both DBs:
   - official DB: `db/problems/*/problem.md`
   - generated candidates DB (flat): `db/generated_candidates/<candidate_id>/problem.md` with `generation_batch_id=<batch_id>`
   - generated candidates DB (legacy nested, read-only compatibility): `db/generated_candidates/<batch>/*/problem.md`
2. Apply filter options (school/year/grade/semester/exam/unit/level/source no).
3. Filter by chosen source DB (`official` or `generated`) and build selected problem ID list.
4. Run `build_exam.py` as subprocess with explicit selected problem folder paths (`--dirs`).
5. Save output PDF in `output/`.
6. Optionally generate answer/solution sheets and append to the main output.

### 4.2 Problem metadata edit (`GET/POST /api/problem-meta`, `POST /api/problem-delete`, `POST /api/similar-delete`)

1. Select problem from filtered manual-order list.
2. Open metadata editor modal from the row's `수정` button.
3. Supported targets for metadata update are both official DB rows and generated candidate rows.
4. Update source metadata (`school/year/grade/semester/exam/subject/source info`) and unit triplet (`unit_l1/l2/l3`).
5. Save to rewrite front-matter in the target `problem.md`.
6. UI metadata cache is refreshed so filtering/sorting uses updated values.
7. Optional folder shortcut action opens the target problem folder (the directory containing `problem.md`) in the file manager.
8. Optional delete action removes the target folder from the source DB:
   - official row: delete via `POST /api/problem-delete` (`db/problems/<id>`)
   - generated row: delete via `POST /api/similar-delete` (`db/generated_candidates/.../<candidate_id>`)
9. Subject values are normalized to subject codes (`COM1/COM2/ALG/CAL1/STAT`) when scanning/saving.

### 4.3 Problem body edit (`GET/POST /api/problem-content`, `POST /api/problem-preview-render`)

1. Select problem from manual-order list.
2. Load raw section text (`Q/Choices/Answer/Solution`) into in-page editor.
3. Render draft preview from editor text via preview-render API.
4. Save writes updated body sections back to `problem.md` while preserving front-matter.
5. Saved-preview and draft-preview panes refresh for immediate verification.

### 4.4 Similar candidate review (`/api/similar-*`)

1. Load batch IDs from `db/generated_candidates`.
2. Load candidate list with review/validation state for the selected batch.
3. Open candidate preview/content, edit sections, and save updates to candidate `problem.md`.
4. Update review status (`pending|approved|rejected`) and note per candidate.
5. Optional delete action (via candidate `수정` -> metadata modal `삭제`) removes the target candidate folder (including `problem.md`) from `db/generated_candidates`.
6. Run batch validation for candidate quality checks.
7. Promotion to `db/problems` is policy-disabled to keep official DB and generated DB strictly separated.

### 4.4.1 Similar auto-generation (`POST /api/similar-generate`)

1. Accept seed problem IDs selected via similar-tab filter/search result checkboxes.
2. Use configured AI runtime provider/key/model (Gemini, Groq, or OpenAI) to generate candidate `Q/Choices/Answer/Solution`.
3. Save candidate folders directly under `db/generated_candidates/` and tag each candidate with `generation_batch_id=<batch_id>`.
4. Save prompt/source snapshot/manifest and return per-candidate success/failure summary.

### 4.5 AI runtime config (`GET/POST /api/ai-config`)

1. Store provider/model plus provider-scoped API keys for generation in server runtime memory.
2. API key is not persisted to repo files and is cleared when app restarts.

## 5) `problem.md` Shape

Expected front-matter fields include (non-exhaustive):

- `id`, `school`, `year`, `grade`, `semester`, `exam`
- `type`, `level` (or `difficulty`)
- `unit`, `unit_l1`, `unit_l2`, `unit_l3`
- `source_question_no`, `source_question_kind`, `source_question_label`
- `tags`, `assets`

Expected body sections:

- `## Q`
- `## Choices`
- `## Answer`
- `## Solution`

## 6) Common Commands

Run web app:

```powershell
python app.py
```

Build by IDs:

```powershell
python build_exam.py `
  --root db/problems `
  --ids HN-2025-G1-S1-MID-006,HN-2025-G1-S1-MID-008 `
  --out output/exam_test.pdf `
  --paper A4 `
  --columns 2 `
  --title "HN 2025 G1 S1 MID"
```

Build by pattern:

```powershell
python build_exam.py `
  --root db/problems `
  --pattern "HN-2025-G2-S1-MID-*" `
  --out output/hn_g2_mid.pdf
```

Build by explicit directories (mixed roots allowed):

```powershell
python build_exam.py `
  --dirs `
  db/problems/HN-2025-G1-S1-MID-006 `
  db/generated_candidates/HN-2025-G1-S1-MID-006-sim001 `
  --out output/mixed_exam.pdf
```

Backfill unit/level:

```powershell
python backfill_unit_level.py --root db/problems --pattern "HN-2025-G2-S1-MID-*" --dry-run
```

## 7) Validation Checklist for Changes

- `python -m compileall app.py build_exam.py parser.py renderer.py`
- Run `python app.py` and verify render page loads.
- Run one `build_exam.py` command and verify output PDF is generated.

## 8) Notes

- `PROJECT_ANALYSIS.md` and `OPTIMIZATION_PROGRESS.md` may contain historical ingest references.
- For current behavior, trust code first, then update docs if mismatch appears.
- Offline similar-problem staging workflow is documented in `SIMILAR_PROBLEM_WORKFLOW.md` and implemented by `scripts/similar_problem_pipeline.py`.
