from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Sequence
from urllib.parse import urlparse
import re

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from parser import ParsedProblem


IMG_TAG_RE = re.compile(
    r"<img\b(?P<before>[^>]*?)\bsrc=(?P<quote>[\"'])(?P<src>.*?)(?P=quote)(?P<after>[^>]*)>",
    re.IGNORECASE,
)
RAW_ORIGINAL_MARKER = "assets/original/"
MATH_PLACEHOLDER_RE = re.compile(r"@@MATH_BLOCK_(\d+)@@")
MATH_SEGMENT_RE = re.compile(
    r"(\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|\$(?:\\.|[^$\n\\])+\$)",
    re.DOTALL,
)
CURRICULUM_SUFFIX_RE = re.compile(r"\s*\(2022개정\)\s*")


@dataclass(frozen=True)
class ExamLayout:
    paper: str
    page_width_mm: int
    page_height_mm: int
    margin_top_mm: int
    margin_right_mm: int
    margin_bottom_mm: int
    margin_left_mm: int
    column_gap_mm: int
    columns: int
    font_size_pt: float
    title: str
    show_meta: bool
    show_source_info: bool
    show_teacher_answer: bool


PROBLEM_ID_RE = re.compile(
    r"^(?P<school>[^-]+)-(?P<year>\d{4})-G(?P<grade>\d+)-S(?P<semester>\d+)-(?P<exam>[^-]+)-(?P<number>\d{3})$"
)
SOURCE_NO_TAG_RE = re.compile(r"異쒖젣踰덊샇-(\d+)")

MATHJAX_BOOTSTRAP = """
<script>
window.__MATHJAX_DONE = false;
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  },
  svg: {
    fontCache: 'none'
  },
  startup: {
    pageReady: () => {
      return MathJax.startup.defaultPageReady().then(() => {
        window.__MATHJAX_DONE = true;
      });
    }
  }
};
window.addEventListener('load', () => {
  setTimeout(() => {
    if (!window.MathJax) {
      window.__MATHJAX_DONE = true;
    }
  }, 500);
});
</script>
"""

PDF_EMPTY_HEADER_TEMPLATE = "<div></div>"

PDF_FOOTER_TEMPLATE = """
<div style="width:100%; font-size:10px; color:#111; text-align:center; line-height:1.1; padding-top:2px;">
  <span class="pageNumber"></span>/<span class="totalPages"></span>
</div>
"""

ANSWER_SHEET_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Answer Sheet</title>
  <style>
    @page { size: A4; margin: 18mm 16mm 18mm 16mm; }
    body {
      font-family: "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      font-size: 12pt;
      line-height: 1.6;
      color: #111;
    }
    h1 {
      font-size: 16pt;
      margin: 0 0 8mm 0;
    }
    ol {
      margin: 0;
      padding-left: 7mm;
    }
    li {
      margin: 0 0 1.8mm 0;
      break-inside: avoid;
    }
    .meta {
      color: #666;
      margin-left: 2mm;
      font-size: 10pt;
    }
  </style>
  {{ mathjax_bootstrap | safe }}
  <script defer src="{{ mathjax_bundle_uri }}"></script>
</head>
<body>
  <h1>Answer Sheet</h1>
  <ol>
    {% for row in rows %}
      <li>{{ row.answer_text }} <span class="meta">({{ row.problem_id }})</span></li>
    {% endfor %}
  </ol>
</body>
</html>
"""

SOLUTION_SHEET_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Solution Sheet</title>
  <style>
    @page { size: A4; margin: 10mm 9mm 10mm 9mm; }
    body {
      font-family: "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      font-size: 10.2pt;
      line-height: 1.3;
      color: #111;
      margin: 0;
    }
    h1 {
      font-size: 15pt;
      margin: 0 0 3mm 0;
    }
    .sheet {
      column-count: 2;
      column-gap: 4mm;
      column-fill: auto;
    }
    .item {
      border: 0.8pt solid #cfd6dd;
      border-radius: 4px;
      padding: 1.4mm 1.8mm;
      margin: 0 0 1.6mm 0;
      break-inside: avoid;
      page-break-inside: avoid;
      -webkit-column-break-inside: avoid;
    }
    .head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin: 0 0 0.9mm 0;
      border-bottom: 0.5pt solid #e5e7eb;
      padding-bottom: 0.7mm;
    }
    .num {
      font-weight: 700;
      font-size: 10.4pt;
    }
    .pid {
      color: #667085;
      font-size: 8.2pt;
    }
    .label {
      font-size: 8.8pt;
      color: #475467;
      margin: 0 0 0.4mm 0;
      font-weight: 700;
    }
    .answer,
    .solution {
      margin-bottom: 0.7mm;
    }
    .answer p,
    .solution p {
      margin: 0;
      line-height: 1.26;
    }
    .answer p + p,
    .solution p + p {
      margin-top: 0.25mm;
    }
    .answer .MathJax_Display,
    .solution .MathJax_Display,
    .answer mjx-container[display="true"],
    .solution mjx-container[display="true"] {
      margin-top: 0.35mm !important;
      margin-bottom: 0.35mm !important;
    }
    .answer img,
    .solution img {
      max-width: 78%;
      height: auto;
      display: block;
      margin: 0.5mm auto;
    }
  </style>
  {{ mathjax_bootstrap | safe }}
  <script defer src="{{ mathjax_bundle_uri }}"></script>
</head>
<body>
  <h1>Solution Sheet</h1>
  <main class="sheet">
    {% for row in rows %}
      <section class="item">
        <div class="head">
          <span class="num">{{ row.number }}\ubc88</span>
          <span class="pid">{{ row.problem_id }}</span>
        </div>
        <div class="answer">
          <p class="label">\uc815\ub2f5</p>
          {{ row.answer_html }}
        </div>
        <div class="solution">
          <p class="label">\ud574\uc124</p>
          {{ row.solution_html }}
        </div>
      </section>
    {% endfor %}
  </main>
</body>
</html>
"""


def _is_external_src(src: str) -> bool:
    parsed = urlparse(src)
    return bool(parsed.scheme) or src.startswith("//")


def _rewrite_img_sources(
    html_text: str, base_dir: Path, problem_id: str, warnings: List[str]
) -> str:
    # IMPORTANT:
    # - Only images explicitly referenced in markdown (Q/Choices) are rendered.
    # - Front-matter "assets" list is metadata only and is not auto-rendered.
    # - Project convention: assets/scan.png is for inline figure crops, while
    #   raw originals should be stored under assets/original/.
    def replace(match: re.Match[str]) -> str:
        before = match.group("before")
        quote = match.group("quote")
        src = match.group("src")
        after = match.group("after")
        source = src.strip()
        if not source or _is_external_src(source):
            return match.group(0)

        normalized = source.replace("\\", "/")
        lowered = normalized.lower().lstrip("./")
        if lowered.startswith(RAW_ORIGINAL_MARKER) or f"/{RAW_ORIGINAL_MARKER}" in lowered:
            warnings.append(
                f"{problem_id}: Raw original image reference ignored ('{source}'). "
                "Use assets/scan.png for inline figures."
            )
            return ""

        candidate = (base_dir / normalized).resolve()
        if candidate.exists():
            return f"<img{before}src={quote}{candidate.as_uri()}{quote}{after}>"

        warnings.append(
            f"{problem_id}: Referenced image not found: '{source}' (resolved: {candidate})"
        )
        # Drop broken local image tags so alt text is not rendered.
        return ""

    return IMG_TAG_RE.sub(replace, html_text)


def _markdown_to_html(md_text: str) -> str:
    # Preserve TeX segments before markdown conversion.
    # Python-Markdown consumes backslashes in normal text, which breaks
    # matrix/cases syntax (e.g., "\\\\", "\\begin{...}") used by MathJax.
    saved_math: List[str] = []

    def stash_math(match: re.Match[str]) -> str:
        saved_math.append(match.group(1))
        return f"@@MATH_BLOCK_{len(saved_math) - 1}@@"

    protected = MATH_SEGMENT_RE.sub(stash_math, md_text)
    converter = markdown.Markdown(extensions=["extra", "sane_lists", "nl2br"])
    html_text = converter.convert(protected)

    def restore_math(match: re.Match[str]) -> str:
        index = int(match.group(1))
        if index < 0 or index >= len(saved_math):
            return match.group(0)
        return escape(saved_math[index], quote=False)

    return MATH_PLACEHOLDER_RE.sub(restore_math, html_text)


def _extract_source_question_no(front_matter: Dict[str, object]) -> str:
    raw = front_matter.get("source_question_no")
    if isinstance(raw, int):
        return str(raw)
    if isinstance(raw, str):
        token = raw.strip()
        if token.isdigit():
            return token

    tags = front_matter.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            match = SOURCE_NO_TAG_RE.search(str(tag))
            if match:
                return match.group(1)
    return ""


def _extract_source_question_label(
    front_matter: Dict[str, object], id_number_text: str
) -> str:
    raw_label = str(front_matter.get("source_question_label", "")).strip()
    if raw_label:
        return raw_label

    source_no = _extract_source_question_no(front_matter).strip()
    qkind = str(front_matter.get("source_question_kind", "")).strip().lower()
    id_number = int(id_number_text) if id_number_text.isdigit() else None

    if not source_no and id_number is not None:
        if id_number >= 100:
            source_no = str(id_number - 100)
        else:
            source_no = str(id_number)
    if not source_no:
        return ""

    subj_prefix = "\uc11c\ub2f5"
    if qkind == "subjective":
        return f"{subj_prefix}{source_no}"
    if qkind == "objective":
        return source_no

    if id_number is not None and id_number >= 100:
        return f"{subj_prefix}{source_no}"
    return source_no


def _build_source_info(problem: ParsedProblem) -> str:
    front = problem.front_matter
    matched = PROBLEM_ID_RE.match(problem.display_id)
    from_id = matched.groupdict() if matched else {}

    school = str(front.get("school") or from_id.get("school") or "").strip().upper()
    year = str(front.get("year") or from_id.get("year") or "").strip()
    grade = str(front.get("grade") or from_id.get("grade") or "").strip()
    semester = str(front.get("semester") or from_id.get("semester") or "").strip()
    exam = str(front.get("exam") or from_id.get("exam") or "").strip().upper()
    source_label = _extract_source_question_label(front, str(from_id.get("number", "")))

    unit_l1 = str(front.get("unit_l1") or "").strip()
    unit_l2 = str(front.get("unit_l2") or "").strip()
    unit_l3 = str(front.get("unit_l3") or "").strip()
    unit_path = ""
    if unit_l1 and unit_l2 and unit_l3:
        unit_path = ">".join([CURRICULUM_SUFFIX_RE.sub("", unit_l1).strip(), unit_l2, unit_l3])
    else:
        raw_unit = str(front.get("unit") or "").strip()
        if raw_unit:
            unit_parts = [token.strip() for token in raw_unit.split(">") if token.strip()]
            if unit_parts:
                if unit_parts:
                    unit_parts[0] = CURRICULUM_SUFFIX_RE.sub("", unit_parts[0]).strip()
                unit_path = ">".join(unit_parts)

    parts: List[str] = []
    if school:
        parts.append(school)
    if year:
        parts.append(year)
    if grade:
        parts.append(f"G{grade}")
    if semester:
        parts.append(f"S{semester}")
    if exam:
        parts.append(exam)
    if source_label:
        parts.append(f"출제번호 {source_label}")
    if unit_path:
        parts.append(f"단원 {unit_path}")
    return " | ".join(parts)


def _extract_unit_path(front_matter: Dict[str, object]) -> str:
    unit_l1 = str(front_matter.get("unit_l1") or "").strip()
    unit_l2 = str(front_matter.get("unit_l2") or "").strip()
    unit_l3 = str(front_matter.get("unit_l3") or "").strip()
    if unit_l1 and unit_l2 and unit_l3:
        return " > ".join([CURRICULUM_SUFFIX_RE.sub("", unit_l1).strip(), unit_l2, unit_l3])

    raw_unit = str(front_matter.get("unit") or "").strip()
    if not raw_unit:
        return ""
    unit_parts = [token.strip() for token in raw_unit.split(">") if token.strip()]
    if unit_parts:
        unit_parts[0] = CURRICULUM_SUFFIX_RE.sub("", unit_parts[0]).strip()
    return " > ".join(unit_parts)


def _build_source_header_meta(problem: ParsedProblem) -> Dict[str, str]:
    front = problem.front_matter
    matched = PROBLEM_ID_RE.match(problem.display_id)
    from_id = matched.groupdict() if matched else {}

    school = str(front.get("school") or from_id.get("school") or "").strip().upper()
    year = str(front.get("year") or from_id.get("year") or "").strip()
    grade = str(front.get("grade") or from_id.get("grade") or "").strip()
    semester = str(front.get("semester") or from_id.get("semester") or "").strip()
    exam = str(front.get("exam") or from_id.get("exam") or "").strip().upper()
    source_label = _extract_source_question_label(front, str(from_id.get("number", "")))

    exam_parts: List[str] = []
    if school:
        exam_parts.append(school)
    if year:
        exam_parts.append(year)
    if grade:
        exam_parts.append(f"G{grade}")
    if semester:
        exam_parts.append(f"S{semester}")
    if exam:
        exam_parts.append(exam)
    if source_label:
        exam_parts.append(str(source_label))

    return {
        "source_exam_info": " ".join(exam_parts),
        "source_unit_info": _extract_unit_path(front),
    }


def _extract_subject_name(front_matter: Dict[str, object]) -> str:
    unit_l1 = str(front_matter.get("unit_l1", "")).strip()
    if unit_l1:
        return CURRICULUM_SUFFIX_RE.sub("", unit_l1).strip()
    unit = str(front_matter.get("unit", "")).strip()
    if not unit:
        return ""
    return CURRICULUM_SUFFIX_RE.sub("", unit.split(">", 1)[0].strip()).strip()


def _build_exam_summary(problems: Sequence[ParsedProblem]) -> Dict[str, str]:
    schools: set[str] = set()
    years: set[str] = set()
    subjects: set[str] = set()

    for problem in problems:
        front = problem.front_matter
        matched = PROBLEM_ID_RE.match(problem.display_id)
        from_id = matched.groupdict() if matched else {}

        school = str(front.get("school") or from_id.get("school") or "").strip().upper()
        year = str(front.get("year") or from_id.get("year") or "").strip()
        subject = _extract_subject_name(front)

        if school:
            schools.add(school)
        if year:
            years.add(year)
        if subject:
            subjects.add(subject)

    sorted_schools = sorted(schools)
    sorted_years = sorted(years, key=lambda token: int(token) if token.isdigit() else 9999)
    sorted_subjects = sorted(subjects)

    return {
        "schools_text": ", ".join(sorted_schools) if sorted_schools else "-",
        "years_text": ", ".join(sorted_years) if sorted_years else "-",
        "subjects_text": ", ".join(sorted_subjects) if sorted_subjects else "-",
    }


def _problem_to_template_context(
    problem: ParsedProblem, number: int, warnings: List[str], show_teacher_answer: bool
) -> Dict[str, object]:
    base_dir = problem.source_path.parent
    q_html = _rewrite_img_sources(
        _markdown_to_html(problem.q), base_dir, problem.display_id, warnings
    )
    choices_html = _rewrite_img_sources(
        _markdown_to_html(problem.choices), base_dir, problem.display_id, warnings
    )
    teacher_answer_html = ""
    if show_teacher_answer:
        answer_md = (problem.answer or "").strip()
        if not answer_md:
            answer_md = "(정답 누락)"
            warnings.append(f"{problem.display_id}: Answer section is empty.")
        teacher_answer_md = f"**정답 : {answer_md}**"
        teacher_answer_html = _rewrite_img_sources(
            _markdown_to_html(teacher_answer_md), base_dir, problem.display_id, warnings
        )

    header_meta = _build_source_header_meta(problem)
    return {
        "number": number,
        "problem_id": problem.display_id,
        "source_info": _build_source_info(problem),
        "source_exam_info": header_meta["source_exam_info"],
        "source_unit_info": header_meta["source_unit_info"],
        "question_html": Markup(q_html),
        "choices_html": Markup(choices_html),
        "teacher_answer_html": Markup(teacher_answer_html),
    }


def _render_html_to_pdf(
    html_content: str,
    out_pdf: Path,
    warnings: List[str],
    wait_for_mathjax: bool = True,
) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(prefix="exam_build_") as tmpdir:
        html_path = Path(tmpdir) / "render.html"
        html_path.write_text(html_content, encoding="utf-8")

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")

            if wait_for_mathjax:
                try:
                    page.wait_for_function(
                        "() => window.__MATHJAX_DONE === true", timeout=40000
                    )
                except PlaywrightTimeoutError:
                    warnings.append(
                        "MathJax rendering wait timed out. PDF was generated anyway."
                    )

            # Run optional client-side layout hook after MathJax render.
            try:
                has_layout_hook = bool(
                    page.evaluate(
                        "() => typeof window.__layoutProblemPages === 'function' || typeof window.__adjustProblemSpacing === 'function'"
                    )
                )
                if has_layout_hook:
                    page.evaluate(
                        "() => { if (typeof window.__layoutProblemPages === 'function') window.__layoutProblemPages(); else if (typeof window.__adjustProblemSpacing === 'function') window.__adjustProblemSpacing(); }"
                    )
                    page.wait_for_timeout(60)
                    page.evaluate(
                        "() => { if (typeof window.__layoutProblemPages === 'function') window.__layoutProblemPages(); else if (typeof window.__adjustProblemSpacing === 'function') window.__adjustProblemSpacing(); }"
                    )
                    page.wait_for_timeout(40)
            except Exception as exc:  # pylint: disable=broad-except
                warnings.append(f"Client-side layout hook skipped: {exc}")

            page.pdf(
                path=str(out_pdf),
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template=PDF_EMPTY_HEADER_TEMPLATE,
                footer_template=PDF_FOOTER_TEMPLATE,
            )
            browser.close()


def render_exam_pdf(
    problems: Sequence[ParsedProblem],
    out_pdf: Path,
    template_path: Path,
    mathjax_bundle: Path,
    layout: ExamLayout,
    warnings: List[str],
) -> None:
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    if not mathjax_bundle.exists():
        raise FileNotFoundError(f"MathJax bundle not found: {mathjax_bundle}")

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template(template_path.name)

    items = [
        _problem_to_template_context(
            problem,
            idx,
            warnings,
            show_teacher_answer=layout.show_teacher_answer,
        )
        for idx, problem in enumerate(problems, start=1)
    ]
    exam_summary = _build_exam_summary(problems)

    html_content = template.render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        mathjax_bundle_uri=mathjax_bundle.resolve().as_uri(),
        mathjax_bootstrap=Markup(MATHJAX_BOOTSTRAP),
        title=layout.title,
        show_meta=layout.show_meta,
        show_source_info=layout.show_source_info,
        show_teacher_answer=layout.show_teacher_answer,
        paper=layout.paper,
        page_width_mm=layout.page_width_mm,
        page_height_mm=layout.page_height_mm,
        margin_top_mm=layout.margin_top_mm,
        margin_right_mm=layout.margin_right_mm,
        margin_bottom_mm=layout.margin_bottom_mm,
        margin_left_mm=layout.margin_left_mm,
        column_gap_mm=layout.column_gap_mm,
        columns=layout.columns,
        font_size_pt=layout.font_size_pt,
        exam_summary=exam_summary,
        problems=items,
    )
    _render_html_to_pdf(html_content=html_content, out_pdf=out_pdf, warnings=warnings)


def render_answer_sheet_pdf(
    problems: Sequence[ParsedProblem],
    out_pdf: Path,
    mathjax_bundle: Path,
    warnings: List[str],
) -> None:
    if not mathjax_bundle.exists():
        raise FileNotFoundError(f"MathJax bundle not found: {mathjax_bundle}")

    env = Environment(autoescape=select_autoescape(["html"]))
    template = env.from_string(ANSWER_SHEET_TEMPLATE)

    rows = []
    for idx, problem in enumerate(problems, start=1):
        answer_text = (problem.answer or "").strip()
        if not answer_text:
            answer_text = "(Answer missing)"
            warnings.append(f"{problem.display_id}: Answer section is empty.")

        rows.append(
            {
                "number": idx,
                "problem_id": problem.display_id,
                "answer_text": answer_text,
            }
        )

    html_content = template.render(
        rows=rows,
        mathjax_bootstrap=Markup(MATHJAX_BOOTSTRAP),
        mathjax_bundle_uri=mathjax_bundle.resolve().as_uri(),
    )
    _render_html_to_pdf(html_content=html_content, out_pdf=out_pdf, warnings=warnings)


def render_solution_sheet_pdf(
    problems: Sequence[ParsedProblem],
    out_pdf: Path,
    mathjax_bundle: Path,
    warnings: List[str],
) -> None:
    if not mathjax_bundle.exists():
        raise FileNotFoundError(f"MathJax bundle not found: {mathjax_bundle}")

    env = Environment(autoescape=select_autoescape(["html"]))
    template = env.from_string(SOLUTION_SHEET_TEMPLATE)

    rows = []
    for idx, problem in enumerate(problems, start=1):
        base_dir = problem.source_path.parent

        answer_md = (problem.answer or "").strip()
        if not answer_md:
            answer_md = "(Answer missing)"
            warnings.append(f"{problem.display_id}: Answer section is empty.")

        solution_md = (problem.solution or "").strip()
        if not solution_md:
            solution_md = "(Solution missing)"
            warnings.append(f"{problem.display_id}: Solution section is empty.")

        answer_html = _rewrite_img_sources(
            _markdown_to_html(answer_md), base_dir, problem.display_id, warnings
        )
        solution_html = _rewrite_img_sources(
            _markdown_to_html(solution_md), base_dir, problem.display_id, warnings
        )

        rows.append(
            {
                "number": idx,
                "problem_id": problem.display_id,
                "answer_html": Markup(answer_html),
                "solution_html": Markup(solution_html),
            }
        )

    html_content = template.render(
        rows=rows,
        mathjax_bootstrap=Markup(MATHJAX_BOOTSTRAP),
        mathjax_bundle_uri=mathjax_bundle.resolve().as_uri(),
    )
    _render_html_to_pdf(html_content=html_content, out_pdf=out_pdf, warnings=warnings)

