# Web App Guide

## 1) Install dependencies

```powershell
cd D:\Math_Kichul
python -m pip install -r requirements.txt
```

Optional OCR setup:

1. Install Tesseract OCR on Windows.
2. Make sure `tesseract` command works in terminal.
3. Keep `Pillow` + `pytesseract` installed (`requirements.txt` already includes both).

## 2) Run app

```powershell
cd D:\Math_Kichul
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

## 3) Workflow

1. Upload images in the web page (`db/original` staging).
2. In DB auto generation:
   - choose `AI Provider` (`Gemini` or `Groq`)
   - set the provider API key and model
   - click `선택 AI 모델 목록 갱신` (refreshes models for the selected provider only)
3. Check/adjust detected DB numbers in the table.
4. Click `선택 이미지 DB 반영`.
5. Optionally click `선택 항목 삭제` to remove checked staged files.
6. Optionally generate exam/answer/solution PDFs from the same page.

## 4) API key input (optional env vars)

You can leave key fields empty if environment variables are set:

- Gemini: `GEMINI_API_KEY`
- Groq: `GROQ_API_KEY`

## 5) Filename rules

- `006.png` -> problem number `006` (objective by default)
- `서답5번.png` -> problem number `105` (subjective offset default = 100)
- `정답006.png` (or `answer006.png`) -> answer source for problem 006
- `해설006.png` (or `solution006.png`) -> solution source for problem 006

If detection is wrong, edit the DB number in the UI before ingestion.

## 6) OCR behavior

- If `OCR 사용` is enabled and OCR engine is unavailable (and AI is off), ingestion stops.
- RapidOCR is used first; if unavailable, Tesseract is used as fallback.

## 7) AI behavior

- `AI 자동 풀이` tries to generate question/choices/answer/solution from image.
- `AI 실패 시 OCR 대체 허용` enables OCR fallback when AI fails.
- Gemini and Groq calls include auto retry/backoff for transient errors and `429` rate limits.
- Groq includes request pacing by default (`GROQ_MIN_INTERVAL_SEC`, default `2.0` sec).
- If AI returns `401` (invalid API key/auth), remaining items skip AI in that run.
- If a selected model is decommissioned, remaining items skip AI in that run.
  Use `선택 AI 모델 목록 갱신` and pick another model.
- Deprecated Groq 3.2 vision model names are auto-switched to the current default model.

## 8) Asset rule

- `assets/scan.png`: inline figure image referenced inside Q/Choices.
- `assets/original/`: raw source image archive.
- Renderer ignores `assets/original/*` links by default, so full source scans do not appear in exam PDFs.
