from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import re

import yaml


FRONT_MATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)
SECTION_RE = re.compile(r"(?m)^##\s+([^\n#]+?)\s*$")


@dataclass
class ParsedProblem:
    folder_id: str
    source_path: Path
    front_matter: Dict[str, Any]
    q: str
    choices: str
    answer: str
    solution: str
    warnings: List[str] = field(default_factory=list)

    @property
    def display_id(self) -> str:
        front_id = self.front_matter.get("id")
        if front_id is None:
            return self.folder_id
        return str(front_id)


def _read_text_with_fallback(path: Path) -> Tuple[str, str]:
    errors: List[str] = []
    for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError as exc:
            errors.append(f"{encoding}: {exc}")

    joined = "; ".join(errors)
    raise ValueError(f"Failed to decode file {path}: {joined}")


def _split_front_matter(text: str, path: Path, warnings: List[str]) -> Tuple[Dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        warnings.append(f"{path}: YAML front-matter not found.")
        return {}, text

    yaml_text = match.group(1)
    body = text[match.end() :]
    try:
        parsed = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as exc:
        warnings.append(f"{path}: Failed to parse YAML front-matter ({exc}).")
        parsed = {}

    if not isinstance(parsed, dict):
        warnings.append(f"{path}: Front-matter is not a mapping object.")
        parsed = {}

    return parsed, body


def _normalize_section_name(name: str) -> str | None:
    token = re.sub(r"[^a-z]", "", name.lower())
    if token in {"q", "question", "problem"}:
        return "q"
    if token.startswith("choice"):
        return "choices"
    if token in {"answer", "ans"}:
        return "answer"
    if token in {"solution", "sol", "explanation"}:
        return "solution"
    return None


def _extract_sections(body: str, path: Path, warnings: List[str]) -> Dict[str, str]:
    matches = list(SECTION_RE.finditer(body))
    if not matches:
        warnings.append(f"{path}: Section headings not found. Entire body treated as Q.")
        return {"q": body.strip("\n"), "choices": "", "answer": "", "solution": ""}

    raw_sections: Dict[str, str] = {}
    for idx, match in enumerate(matches):
        heading = match.group(1).strip()
        key = _normalize_section_name(heading)
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        content = body[start:end].strip("\n")

        if key is None:
            warnings.append(f"{path}: Unknown section heading '## {heading}' ignored.")
            continue

        if key in raw_sections and raw_sections[key]:
            warnings.append(f"{path}: Duplicate section '{key}' merged.")
            merged = raw_sections[key].rstrip()
            if content:
                merged = f"{merged}\n\n{content.lstrip()}"
            raw_sections[key] = merged
        else:
            raw_sections[key] = content

    for required in ("q", "choices", "answer", "solution"):
        if required not in raw_sections:
            warnings.append(f"{path}: Missing section '{required}'.")
            raw_sections[required] = ""

    return raw_sections


def parse_problem_file(problem_md_path: Path) -> ParsedProblem:
    warnings: List[str] = []
    text, encoding = _read_text_with_fallback(problem_md_path)
    if encoding != "utf-8-sig":
        warnings.append(f"{problem_md_path}: Decoded using fallback encoding '{encoding}'.")

    front_matter, body = _split_front_matter(text, problem_md_path, warnings)
    sections = _extract_sections(body, problem_md_path, warnings)

    return ParsedProblem(
        folder_id=problem_md_path.parent.name,
        source_path=problem_md_path,
        front_matter=front_matter,
        q=sections["q"],
        choices=sections["choices"],
        answer=sections["answer"],
        solution=sections["solution"],
        warnings=warnings,
    )
