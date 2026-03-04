# Math_Kichul 작업 재개용 컨텍스트

이 문서는 다음 작업을 시작할 때 가장 먼저 읽는 기준 문서다.  
목표: 코드를 다시 전부 훑지 않아도 구조/흐름/주의점을 빠르게 복원하기.

## 1. 프로젝트 한 줄 요약

- 이미지 기반 수학 문항을 `db/problems/<문항ID>/problem.md`로 적재(ingest)하고, 선택 조건으로 시험지 PDF를 생성하는 Flask + Python 파이프라인.

## 2. 빠른 시작

```powershell
cd d:\Math_Kichul
python -m pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

- 웹: `http://127.0.0.1:5000`
- 업로드 스테이징 폴더: `db/original`
- 결과 PDF 폴더: `output`

## 3. 디렉토리 맵

- `app.py`: 웹 UI 라우트, ingest/render 오케스트레이션
- `ingest_pipeline.py`: 이미지 후보 감지, AI/OCR 추출, `problem.md` 생성
- `gemini_solver.py`, `groq_solver.py`: Vision 모델 호출 + 재시도 + JSON 정규화
- `parser.py`: `problem.md` 파싱(YAML front-matter + `##` 섹션)
- `renderer.py`: Markdown/MathJax/이미지 경로 처리 + Playwright PDF 렌더
- `build_exam.py`: CLI 시험지 빌더(`--ids` 또는 `--pattern`)
- `unit_taxonomy.py`: 단원 트리/정규화/노드 확장
- `unit_level_classifier.py`: 키워드 기반 단원/난이도 추정
- `backfill_unit_level.py`: 기존 `problem.md`에 단원/난이도 보강
- `templates/admin.html`: 관리자 웹 UI
- `templates/exam.html`: 시험지 레이아웃 템플릿(2열/4박스 배치)

## 4. 핵심 실행 흐름

### 4.1 Ingest (웹 `POST /ingest`)

1. `db/original` 파일 목록에서 문제 후보 탐지 (`build_candidates`)
2. 파일명 기반 문항번호 추정 + 필요 시 사용자 오버라이드 적용
3. `db/problems/<ID>/assets/original`로 원본 아카이브 복사
4. AI 사용 시 Gemini/Groq로 Q/Choices/Answer/Solution 추출
5. AI 실패 + 허용 시 OCR fallback 수행
6. 단원/난이도 분류(`classify_unit_and_level`) 후 front-matter 생성
7. `problem.md` 작성(또는 overwrite 비활성 시 스킵)
8. `move_after_ingest`가 켜져 있으면 `db/original` 원본 삭제

### 4.2 Render (웹 `POST /render`)

1. 메타 필터(학교/학년/시험/단원/난이도/출제번호)로 문항 선택
2. `build_exam.py`를 서브프로세스로 호출
3. `build_exam.py` -> `parser.py`로 문항 파싱
4. `renderer.py`가 HTML 렌더 + MathJax 완료 대기 + PDF 출력
5. 옵션으로 답안지/해설지 생성 및 본 PDF에 병합 가능

## 5. `problem.md` 사실상 표준 스키마

필수에 가까운 필드:

- `id`, `school`, `year`, `grade`, `semester`, `exam`
- `type`, `level`(또는 `difficulty`)
- `unit`, `unit_l1`, `unit_l2`, `unit_l3`
- `source_question_no`, `source_question_kind`, `source_question_label`
- `tags`, `assets`

본문 섹션:

- `## Q`
- `## Choices`
- `## Answer`
- `## Solution`

파서(`parser.py`)는 섹션명이 다소 달라도 정규화하지만, 위 표준을 유지하는 편이 안전하다.

## 6. 파일명 규칙(중요)

`ingest_pipeline.py` 기준:

- 일반 숫자: `006.png` -> 6번
- 주관/서답 패턴: `서답5번.png` -> `subjective_offset`(기본 100) 더해 105번
- `_scan` 접미사: 보조 이미지로 인식(문제 본문이 아니라 `scan.png` 후보)
- `answer/정답/ans` 포함 파일명: 답안 보조 파일
- `solution/해설/sol` 포함 파일명: 해설 보조 파일
- `<번호>_<단원힌트>.png` 형식이면 단원 자동 힌트 매핑 시도

## 7. AI/OCR 로직 요약

- AI provider: `gemini` 또는 `groq`
- 모델 목록 새로고침 액션 존재 (`action=refresh_models`)
- Groq deprecated 모델은 기본 모델로 자동 대체
- AI 인증 실패(401류) 또는 모델 폐기 에러가 한 번 나면, 같은 실행에서 나머지 문항은 AI 스킵
- OCR 엔진 우선순위: RapidOCR -> Tesseract
- OCR 전처리(OpenCV): 색 마킹 제거 + 이진화
- `allow_ocr_fallback_if_ai_fails` 체크 시 AI 실패 문항에 OCR fallback 적용

## 8. 렌더링 로직 주의점

- `renderer.py`는 `assets/original/*` 이미지를 의도적으로 렌더링에서 제외한다.
- 본문에 들어갈 이미지는 `assets/scan.png` 참조가 권장 규칙.
- Markdown -> HTML 변환 시 수식(LaTeX) 보존용 placeholder 처리 있음.
- 시험지 레이아웃은 템플릿 JS가 페이지 배치를 계산한다(2열, 페이지당 최대 4박스).

## 9. 자주 쓰는 명령

### 웹 서버

```powershell
python app.py
```

### ID 지정으로 시험지 생성

```powershell
python build_exam.py `
  --root db/problems `
  --ids HN-2025-G1-S1-MID-006,HN-2025-G1-S1-MID-008 `
  --out output/exam_test.pdf `
  --paper A4 `
  --columns 2 `
  --title "HN 2025 G1 S1 MID"
```

### 패턴으로 시험지 생성

```powershell
python build_exam.py `
  --root db/problems `
  --pattern "HN-2025-G2-S1-MID-*" `
  --out output/hn_g2_mid.pdf
```

### 단원/난이도 백필(쓰기 없이 미리보기)

```powershell
python backfill_unit_level.py --root db/problems --pattern "HN-2025-G2-S1-MID-*" --dry-run
```

## 10. 수정 시 체크포인트

- AI 관련 수정은 `gemini_solver.py`와 `groq_solver.py` 둘 다 반영해야 일관성이 맞다.
- `copy_to_scan_png` 옵션은 현재 경고만 남기고 실질 복사를 하지 않도록 되어 있다(의도된 동작).
- `problem.md` overwrite 기본값은 꺼져 있으므로, 이미지 아카이브만 갱신되고 본문은 스킵될 수 있다.
- `assets/original`은 아카이브 용도다. 렌더에 보일 이미지는 `scan.png`를 써야 한다.
- 자동 테스트 스위트는 현재 없다. 변경 후 최소 수동 검증은 다음 2가지를 수행:
  - 웹 ingest 1건 (AI 또는 OCR)
  - `build_exam.py`로 PDF 1건 생성

## 11. 현재 코드베이스에서 눈에 띄는 상태

- `PROJECT_ANALYSIS.md`는 현재 인코딩이 깨져 있어 실무 참조 용도로 부적합.
- `WEB_APP_GUIDE.md`는 실행 절차 참고용으로 유효.
- 저장소 핵심 파일은 루트에 평평하게 모여 있고, 모듈 분리는 아직 최소 수준.

## 12. 다음 작업 시작 루틴(권장)

1. 이 파일(`CODEBASE_CONTEXT.md`) 먼저 읽기
2. 이번 작업과 직접 관련된 파일만 추가로 열기
3. 변경 후 `build_exam.py` 또는 웹 경로로 최소 1회 검증
4. 결과/주의점은 이 문서에 짧게 누적 업데이트


## 13. Recent Optimization Updates (2026-03-03)

- Added shared retry helper module: `ai_solver_utils.py`
  - `parse_retry_after_seconds`
  - `should_retry_status`
- `gemini_solver.py` and `groq_solver.py` now import retry helpers from `ai_solver_utils.py`.
- Ingest path now scans `db/original` once per run and reuses the list for:
  - candidate detection
  - answer/solution companion indexing
  - scan companion indexing
- Removed unused renderer precompute:
  - deleted `_chunk_problem_pages`
  - removed unused `problem_pages` template argument
- Detailed staged log is tracked in `OPTIMIZATION_PROGRESS.md`.

- Additional low-risk optimization batch completed (Stage 6):
  - Shared JSON extraction helper moved to `ai_solver_utils.py`.
  - `gemini_solver.py` and `groq_solver.py` now use shared JSON extraction and shared retry helpers.
  - Ingest companion indexing (scan/answer/solution) merged into one pass.
  - Removed unused `_build_problem_markdown` parameter (`problem_no`).
  - Regression checks passed (compile/import/CLI render smoke).
- Workspace hygiene: `.gitignore` now excludes `output/` and Python cache files.

## 14. VSCode Agent용 DB 워크플로우 CLI (2026-03-03)

- 브라우저 없이 터미널/에이전트에서 DB 업로드 배치를 돌리기 위한 스크립트:
  - `scripts/db_workflow_cli.py`
- 프로필 설정 파일:
  - `scripts/db_workflow_profiles.json`
- 런타임 상태 파일(자동 생성):
  - `scripts/.db_workflow_state.json`
- 작업계획서(자동 갱신):
  - `scripts/DB_WORKFLOW_PLAN.md`

### 기본 사용

```powershell
python scripts/db_workflow_cli.py start
```

- 위 한 줄로 `사전점검(plan) -> 중복 확인 -> chunk 실행 -> 결과 요약` 순서 수행.
- 프로필 기본값은 `scripts/db_workflow_profiles.json`의 `active_profile`.
- 기본 chunk/rpm/중복정책은 `defaults`의 `chunk_size=2`, `rpm=4`, `on_duplicate=ask`.
- 메타를 한 줄로 바로 주는 방법:

```powershell
python scripts/db_workflow_cli.py start --meta "JE,2025,2,1,MID"
```

- `--meta` 형식: `school,year,grade,semester,exam`
- `source_label`이 비어 있으면 `user_upload_YYYY-MM-DD`(오늘 날짜)로 자동 채움.

### 소스 메타 자동 반영 (`db/original/_meta.json`)

- `db/original`에 `_meta.json`(또는 `meta.json`)을 두면, 실행 시 프로필보다 우선 적용된다.
- 따라서 ID 접두/연도/학년/학기/시험/출처가 배치마다 자동 변경된다.
- 예시:

```json
{
  "school": "JE",
  "year": 2025,
  "grade": 2,
  "semester": 1,
  "exam": "MID",
  "source": "user_upload_2026-03-03",
  "subjective_offset": 100
}
```

- `source` 또는 `source_label` 둘 다 사용 가능하며 내부적으로 `source_label`로 반영된다.
- 필요 시 CLI 인자로 최종 오버라이드 가능:
  - `--school --year --grade --semester --exam --source-label --subjective-offset`

### 중복 폴더가 있는 경우(ask 모드)

- 중복이 있으면 실행을 멈추고 decision을 요구:
  - `python scripts/db_workflow_cli.py resume --decision skip`
  - `python scripts/db_workflow_cli.py resume --decision overwrite`

### 중단 후 이어서 실행

```powershell
python scripts/db_workflow_cli.py resume
```

### 검수 경로만 출력

```powershell
python scripts/db_workflow_cli.py report --review-only
```

## 15. Workflow Update (2026-03-03)

- `python scripts/db_workflow_cli.py start ...` now runs an automatic pre-clean step before preflight.
- Pre-clean target: question images in `db/original` (excluding `_scan`, answer, solution companions).
- It removes top-right footnote-like number marks (examples: `(16)`, `17)`) when detected by OCR boxes.
- If OCR/OpenCV dependency is unavailable, the workflow prints pre-clean warnings and continues.

## 16. AI Provider Update (2026-03-04)

- Added `openai` as a third AI provider option across web UI and workflow CLI.
- New runtime fields:
  - `openai_api_key` (or `OPENAI_API_KEY` environment variable)
  - `openai_model` (default: `gpt-4.1`)
- Web ingest panel now supports:
  - provider select: `Gemini / Groq / OpenAI`
  - OpenAI model list refresh
- Ingest runtime now routes AI solve by provider:
  - `gemini` -> `gemini_solver.py`
  - `groq` -> `groq_solver.py`
  - `openai` -> `openai_solver.py`
