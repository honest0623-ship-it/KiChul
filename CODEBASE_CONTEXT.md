# CODEBASE_CONTEXT.md

This file is the quick context snapshot for this repository.
Read this first before making changes.

## 1) Project Summary

- Current project scope: render exam PDFs from existing markdown DB entries.
- Web app role: filter/select problems and call `build_exam.py`.
- Ingest/upload/auto-DB-generation workflows were removed on 2026-03-04.

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
- `templates/admin.html`: Web admin page (render-only controls).
- `build_exam.py`: CLI entry point for exam/answer/solution PDF generation.
- `parser.py`: Parses `problem.md` (front-matter + sections).
- `renderer.py`: HTML/MathJax render and Playwright PDF output.
- `templates/exam.html`: print layout template.

## 4) Request Flow

### 4.1 Web render (`POST /render`)

1. Load metadata from `db/problems/*/problem.md`.
2. Apply filter options (school/year/grade/semester/exam/unit/level/source no).
3. Build selected problem ID list.
4. Run `build_exam.py` as subprocess with selected IDs.
5. Save output PDF in `output/`.
6. Optionally generate answer/solution sheets and append to the main output.

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
