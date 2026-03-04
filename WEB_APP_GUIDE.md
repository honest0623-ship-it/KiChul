# Web App Guide

## 1) Install dependencies

```powershell
cd D:\Math_Kichul
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## 2) Run app

```powershell
cd D:\Math_Kichul
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

## 3) What the web app does now

- The web app is render-only.
- It reads existing markdown problems from `db/problems`.
- It filters and selects problems, then generates PDF outputs.

Removed from web app:

- image upload workflow
- DB auto-generation (ingest) workflow

## 4) Render workflow

1. Choose filters (school/year/grade/semester/exam/unit/level/source no).
2. Optionally set pattern, explicit IDs, and manual order.
3. Set output options (paper, columns, title, file names).
4. Click `PDF 생성 실행`.

## 5) Output

- Main PDF: `output/<out_name>.pdf`
- Optional answer sheet: `output/<answer_name>.pdf`
- Optional solution sheet: `output/<solution_name>.pdf`

## 6) CLI equivalent

```powershell
python build_exam.py --root db/problems --ids HN-2025-G1-S1-MID-006,HN-2025-G1-S1-MID-008 --out output/exam_test.pdf
```
