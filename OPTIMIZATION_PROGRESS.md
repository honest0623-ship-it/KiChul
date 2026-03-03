# Optimization Progress Log

## Goal

- Keep all current features and outputs.
- Improve code efficiency and maintainability.
- Remove obvious duplication/dead paths with low regression risk.

## Stage Plan

1. Baseline validation and optimization target discovery
2. AI solver deduplication (shared utility extraction)
3. Ingest path micro-optimization (reduce repeated directory scans)
4. Renderer/app cleanup (remove dead or redundant compute)
5. Regression checks and handoff notes

## Stage Log

### Stage 1 - Baseline validation

Status: Completed

Actions:
- Ran compile check for major Python modules.
- Verified `build_exam.py --help` works.
- Confirmed `app.py --help` is not a valid CLI mode (server run path; timeout expected).
- Identified safe optimization targets:
  - duplicated normalization/JSON helpers in `gemini_solver.py` and `groq_solver.py`
  - repeated `db/original` directory scans in ingest path
  - unused `problem_pages` precompute in renderer flow

Next:
- Execute Stage 2 with behavior-preserving utility extraction.

### Stage 2 - AI solver deduplication (safe scope)

Status: Completed

Actions:
- Added shared helper module: `ai_solver_utils.py`.
- Consolidated retry helpers used by both providers:
  - `parse_retry_after_seconds`
  - `should_retry_status`
- Updated both solver modules to import shared retry helpers:
  - `gemini_solver.py`
  - `groq_solver.py`

Notes:
- Kept provider-specific prompt/response/normalization logic unchanged to avoid encoding-related regression risk.

### Stage 3 - Ingest path micro-optimization

Status: Completed

Actions:
- Reduced repeated `db/original` scans during ingest by scanning once and reusing the list.
- Updated internal helpers to accept preloaded image sequences:
  - `_companion_indexes(images, subjective_offset)`
  - `_scan_companion_index(images, subjective_offset)`
  - `build_candidates(..., images=...)`
- `ingest_images` now calls `list_original_images` once and reuses the result for:
  - candidate detection
  - answer/solution companion indexing
  - scan companion indexing

Expected impact:
- Lower filesystem I/O during ingest runs (especially with large staging directories).
- No functional change in selection/order logic.

### Stage 4 - Renderer cleanup

Status: Completed

Actions:
- Removed unused precompute path in `renderer.py`:
  - deleted `_chunk_problem_pages`
  - removed unused `problem_pages` generation and template argument

Expected impact:
- Small CPU/memory reduction in exam render preparation.
- No change in rendered layout (template performs client-side layouting).

### Stage 5 - Regression checks

Status: Completed

Checks run:
- `python -m compileall app.py ingest_pipeline.py build_exam.py renderer.py parser.py gemini_solver.py groq_solver.py ai_solver_utils.py unit_taxonomy.py unit_level_classifier.py backfill_unit_level.py make_scaffold.py`
- import smoke test:
  - `import app, ingest_pipeline, renderer, build_exam`
- end-to-end CLI render smoke:
  - `python build_exam.py --root db/problems --ids HN-2025-G2-S1-MID-006 --out output/_tmp_opt_check.pdf --paper A4 --columns 2 --title "opt-check"`

Result:
- All checks passed.

### Stage 7 - Workspace cleanup

Status: Completed

Actions:
- Added `.gitignore` to keep local artifacts out of VCS:
  - `__pycache__/`
  - `*.pyc`
  - `*.pyo`
  - `output/`

Result:
- Working tree now shows code/doc changes only (no output artifact noise).

## Resume Notes

- If work stops mid-way later, resume from this file and append next stage entries.
- Keep optimization edits low-risk first; run the Stage 5 check set after each batch.

### Stage 6 - Additional low-risk optimization batch

Status: Completed

Actions:
- Expanded shared AI utility module (`ai_solver_utils.py`):
  - added `extract_json_object`
- Removed duplicated JSON extraction function bodies from:
  - `gemini_solver.py`
  - `groq_solver.py`
- Further optimized ingest indexing:
  - merged scan/answer/solution companion indexing into a single pass in `_companion_indexes`
  - removed separate scan index pass
- Removed unused parameter from markdown builder flow:
  - dropped `problem_no` arg in `_build_problem_markdown` and call site

Checks run:
- `python -m compileall ai_solver_utils.py gemini_solver.py groq_solver.py ingest_pipeline.py renderer.py build_exam.py app.py parser.py`
- import smoke test:
  - `import ai_solver_utils, gemini_solver, groq_solver, ingest_pipeline`
- CLI render smoke:
  - `python build_exam.py --root db/problems --ids HN-2025-G2-S1-MID-006 --out output/_tmp_opt_check2.pdf --paper A4 --columns 2 --title "opt-check-2"`
- ingest candidate smoke:
  - `build_candidates(Path("db/original"), subjective_offset=100)`

Result:
- All checks passed.
