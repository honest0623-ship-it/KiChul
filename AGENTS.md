# AGENTS.md

## Startup Rule

- At the start of every task, read `CODEBASE_CONTEXT.md` first.
- If `CODEBASE_CONTEXT.md` conflicts with current code, trust code and update the document immediately.

## Operator Shortcut

- If the user says `DB작업시작해줘` (or equivalent short command), run:
  1) Ask one short question first (if not explicitly provided in same message):
     - `메타 5개를 입력해줘: school,year,grade,semester,exam (예: JE,2025,2,1,MID)`
  2) Then run:
     - `python scripts/db_workflow_cli.py start --meta "<사용자입력>" --review-only`
- This command performs:
  - pre-clean of `db/original` question images (remove top-right footnote-like numbers such as `(16)` / `17)` when detected)
  - preflight scan
  - duplicate check (`ask` policy by default)
  - chunked ingest (`chunk_size=2` default profile)
  - final output with review paths
- If `db/original/_meta.json` exists, use it as runtime fixed-meta override
  (`school/year/grade/semester/exam/source/source_label/subjective_offset`).
- If duplicate decision is needed, continue with:
  - `python scripts/db_workflow_cli.py resume --decision skip --review-only`
  - or `python scripts/db_workflow_cli.py resume --decision overwrite --review-only`
