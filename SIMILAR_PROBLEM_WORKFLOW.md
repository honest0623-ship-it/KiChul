# Similar Problem Workflow (Offline, No API)

This workflow creates similar-problem drafts from existing DB items without calling external AI APIs.

The pipeline is script-based and safe-by-default:

1. Create draft batch in `db/generated_candidates/<batch_id>`
2. Edit candidate `problem.md` files manually (or with Codex agent)
3. Validate drafts
4. Mark review status
5. Promote approved candidates into `db/problems`

## Script

- `scripts/similar_problem_pipeline.py`

## 1) Create batch

```powershell
python scripts/similar_problem_pipeline.py `
  --root db/problems `
  --generated-root db/generated_candidates `
  init `
  --pattern "BY-2021-G1-S1-Final-*" `
  --limit 5 `
  --variants-per-seed 2 `
  --similarity-type "parameter_change"
```

Notes:

- Candidate folders are created under `db/generated_candidates/<batch_id>/`.
- Each candidate contains:
  - `problem.md` (draft placeholder sections)
  - `prompt.md` (generation prompt context)
  - `source_snapshot.md` (source Q/Choices/Answer/Solution)

## 2) Edit draft content

Replace `[DRAFT]` sections in each candidate `problem.md`.

Required sections:

- `## Q`
- `## Choices`
- `## Answer`
- `## Solution`

## 3) Validate

```powershell
python scripts/similar_problem_pipeline.py `
  --root db/problems `
  --generated-root db/generated_candidates `
  validate `
  --batch-id sim_20260309_130000 `
  --max-similarity 0.92
```

Validation report:

- `db/generated_candidates/<batch_id>/validation_report.json`

## 4) Review status update

```powershell
python scripts/similar_problem_pipeline.py `
  --generated-root db/generated_candidates `
  review `
  --batch-id sim_20260309_130000 `
  --candidate-ids "BY-2021-G1-S1-Final-001__SIM01 BY-2021-G1-S1-Final-002__SIM01" `
  --status approved `
  --note "checked by teacher"
```

## 5) Promote approved candidates

```powershell
python scripts/similar_problem_pipeline.py `
  --root db/problems `
  --generated-root db/generated_candidates `
  promote `
  --batch-id sim_20260309_130000
```

Promotion report:

- `db/generated_candidates/<batch_id>/promotion_report.json`

Promoted IDs are auto-assigned under the same prefix as `derived_from`.

## Metadata fields used

Candidates use/add these front-matter fields:

- `derived_from`
- `similarity_type`
- `generation_batch_id`
- `generation_model`
- `review_status`
- `review_note`
- `promoted_to`
- `promoted_from` (on promoted copies)
- `promoted_at`

## Operational recommendation

- Keep `review_status=approved` as mandatory before promotion.
- Do not promote candidates containing `[DRAFT]`.
- Keep generated candidates in staging (`db/generated_candidates`) until reviewed.

