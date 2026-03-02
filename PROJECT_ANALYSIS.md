# Math Kichul (수학 기출) 프로젝트 분석 및 개선 가이드

이 문서는 `Math_Kichul` 프로젝트의 현재 코드베이스를 분석하고, 향후 유지보수 및 개선을 위한 가이드를 제공합니다.

## 1. 프로젝트 개요 및 아키텍처

본 프로젝트는 수학 시험지(이미지)를 관리하고 조판하는 종합 워크플로우 시스템입니다.

### 핵심 워크플로우
1. **업로드 및 Ingest (DB화)**: 
   - `app.py`(Flask) 웹 인터페이스를 통해 원본 이미지를 업로드합니다.
   - `ingest_pipeline.py`가 이미지를 분석하여 문제 번호를 추출합니다.
   - `gemini_solver.py` 또는 `groq_solver.py`를 통해 VLM(Vision-Language Model) API를 호출하여 문제, 선지, 정답, 해설을 마크다운 형식으로 추출합니다. AI 실패 시 `RapidOCR` 또는 `Tesseract`를 통한 Fallback을 제공합니다.
   - `unit_level_classifier.py`의 휴리스틱/키워드 기반 룰 엔진을 통해 단원과 난이도를 추정합니다.
   - 추출된 데이터는 `db/problems/{ID}/problem.md` 형태로 저장됩니다.
2. **조판 및 렌더링 (PDF 생성)**:
   - 사용자가 문제를 선택하고 PDF 생성을 요청합니다.
   - `build_exam.py` 및 `renderer.py`가 실행됩니다.
   - `parser.py`를 통해 마크다운 파일을 파싱하고, Jinja2 HTML 템플릿(`templates/exam.html` 등)에 데이터를 렌더링합니다.
   - `Playwright`(Chromium)를 Headless 모드로 띄워 MathJax로 수식을 렌더링한 후 PDF로 최종 출력합니다.

### 주요 파일 역할
- `app.py`: Flask 기반 웹 서버. 라우팅, 설정 관리, 파이프라인 트리거.
- `ingest_pipeline.py`: 이미지 파일에서 마크다운 DB를 생성하는 핵심 로직.
- `build_exam.py` & `renderer.py`: 마크다운 DB를 읽어 PDF로 컴파일하는 엔진.
- `parser.py`: `problem.md`의 YAML Front-matter 및 마크다운 섹션 파서.
- `unit_taxonomy.py` & `unit_level_classifier.py`: 수학 교육과정 단원 분류 체계 및 키워드 기반 분류기.
- `gemini_solver.py` & `groq_solver.py`: 외부 AI 모델 연동 모듈 (Prompting, Retry, JSON 파싱 로직 포함).
- `backfill_unit_level.py`: 기존 DB의 단원/난이도를 재분류하는 유틸리티.
- `make_scaffold.py`: 수동으로 문제 폴더 구조를 생성하는 유틸리티.

---

## 2. 코드 개선 제안 (Refactoring & Improvements)

프로젝트가 훌륭하게 작동하지만, 앞으로 코드가 더 커질 것을 대비해 다음과 같은 부분들을 개선할 수 있습니다.

### A. 중복 코드 제거 (DRY - Don't Repeat Yourself)
`gemini_solver.py`와 `groq_solver.py`에는 매우 유사한 유틸리티 함수들이 중복되어 있습니다.
- **중복 함수**: `_strip_score_tokens`, `_extract_json_object`, `_normalize_qtype`, `_normalize_choice_symbol`, `_normalize_choices`, `_normalize_answer`, `_should_retry_status` 등
- **개선 방법**: `ai_utils.py` (또는 `utils/ai_utils.py`) 모듈을 새로 만들어 공통 로직을 분리하면 유지보수가 훨씬 쉬워집니다.

### B. 재시도(Retry) 로직의 추상화
현재 API 호출 실패 시 자체적인 `for` 루프와 `time.sleep()`을 사용하여 Retry 로직을 구현하고 있습니다. (`_post_generate_content_with_retry` 등)
- **개선 방법**: 파이썬의 `tenacity` 라이브러리를 도입하면 데코레이터(`@retry(wait=wait_exponential...)`) 한 줄로 훨씬 견고하고 가독성 좋은 재시도 로직을 구현할 수 있습니다.

### C. 설정(Configuration) 관리 분리
`app.py` 상단에 `DEFAULTS` 딕셔너리로 하드코딩된 설정들이 있습니다.
- **개선 방법**: `.env` 파일과 `python-dotenv` (또는 `pydantic-settings`)를 사용하여 환경 변수로 설정을 관리하도록 분리하면, 다양한 환경(개발, 배포 등)에서 코드를 수정하지 않고 설정만 변경하여 실행하기 좋습니다.

### D. 아키텍처 및 계층 분리 (Separation of Concerns)
현재 `app.py` 내의 라우트 함수(`index`, `ingest`, `render_pdf`) 안에 비즈니스 로직(데이터 필터링, 폴더 스캔 등)이 다소 혼재되어 있습니다.
- **개선 방법**: `services/` 폴더를 만들어 비즈니스 로직(예: `scan_problem_meta()`, `pdf_filter_options` 빌드 등)을 분리하면 Flask 라우트 코드가 훨씬 간결해집니다.

### E. 오류 처리(Error Handling) 세분화
OCR 및 AI 파싱 실패 시 `Exception`을 광범위하게 잡는(`except Exception as exc:`) 부분이 있습니다.
- **개선 방법**: 예외를 세분화하여(NetworkError, ParseError 등) 잡으면, 예기치 않은 버그를 놓치는 일을 방지할 수 있습니다.

### F. 자동화된 테스트(Testing) 도입
AI 모델의 프롬프트를 변경하거나 정규식(Regex)을 수정할 때 기존 로직이 깨지지 않는지 보장하기 어렵습니다.
- **개선 방법**: `pytest`를 도입하여 `parser.py`의 파싱 로직, `unit_level_classifier.py`의 분류 로직, `ai_utils.py`의 JSON 추출 로직 등에 대한 단위 테스트(Unit Test)를 작성하면 시스템 안정성이 크게 향상됩니다.

---

## 3. 향후 개발 시 참고 사항

- **PDF 렌더링 성능**: `Playwright`는 매우 강력하고 렌더링 품질이 좋지만 무겁습니다. 한 번에 수백 페이지의 시험지를 생성해야 하는 상황이 온다면, 렌더링 워커를 비동기(Async) 또는 큐(Celery 등)로 빼는 아키텍처를 고려해야 할 수 있습니다.
- **Prompt Engineering**: AI에 의존하는 파이프라인 특성상 `system_prompt` 및 `user_text`의 미세한 변화가 결과에 큰 영향을 미칩니다. 모델 변경 시 프롬프트 튜닝 결과를 기록해두는 것이 좋습니다.
- **JSON 파싱 견고성**: 현재 AI의 응답에서 JSON을 강제로 추출해 내는 로직(`_extract_json_object`, `_repair_json_with_*`)이 매우 방어적으로 잘 짜여 있습니다. 향후 OpenAI의 `Structured Outputs` 기능이나 Gemini의 더 엄격한 Schema 모드가 정착되면 이 부분을 간소화할 수 있습니다.
