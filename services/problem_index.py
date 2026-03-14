from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Dict, List, Pattern


RowBuilder = Callable[..., Dict[str, str] | None]


@dataclass(frozen=True)
class _FolderSignature:
    folder_path: str
    has_problem_md: int
    mtime_ns: int
    size: int


class ProblemMetaIndex:
    def __init__(
        self,
        *,
        official_root: Path,
        generated_root: Path,
        problem_id_re: Pattern[str],
        batch_id_re: Pattern[str],
        extract_flat_batch_id: Callable[[Path], str],
        build_official_row: RowBuilder,
        build_generated_row: RowBuilder,
    ) -> None:
        self._official_root = official_root
        self._generated_root = generated_root
        self._problem_id_re = problem_id_re
        self._batch_id_re = batch_id_re
        self._extract_flat_batch_id = extract_flat_batch_id
        self._build_official_row = build_official_row
        self._build_generated_row = build_generated_row

        self._lock = Lock()
        self._official_cache: Dict[str, tuple[_FolderSignature, Dict[str, str]]] = {}
        self._generated_cache: Dict[str, tuple[_FolderSignature, Dict[str, str]]] = {}
        self._flat_batch_cache: Dict[str, tuple[_FolderSignature, str]] = {}

    def list_generated_batch_ids(self) -> List[str]:
        with self._lock:
            batch_candidates = self._scan_generated_candidates_unlocked()
            return sorted(batch_candidates.keys())

    def collect_batch_candidate_dirs(self, batch_id: str) -> Dict[str, Path]:
        token = str(batch_id or "").strip()
        if not token or not self._batch_id_re.match(token):
            return {}
        with self._lock:
            batch_candidates = self._scan_generated_candidates_unlocked()
            candidates = batch_candidates.get(token, {})
            return dict(candidates)

    def scan_problem_meta(
        self,
        *,
        data_sources: List[str] | None = None,
        generated_batches: List[str] | None = None,
    ) -> List[Dict[str, str]]:
        selected_sources = self._normalize_data_sources(data_sources or ["official"])
        include_official = "official" in selected_sources
        include_generated = "generated" in selected_sources

        with self._lock:
            rows: List[Dict[str, str]] = []
            if include_official:
                rows.extend(self._scan_official_rows_unlocked())
            if include_generated:
                rows.extend(self._scan_generated_rows_unlocked(generated_batches=generated_batches))

        return sorted(rows, key=lambda item: (str(item.get("root_kind", "")), str(item.get("batch_id", "")), str(item["id"])))

    def _normalize_data_sources(self, raw_values: List[str]) -> List[str]:
        normalized: List[str] = []
        seen = set()
        for value in raw_values:
            token = str(value or "").strip().lower()
            if token not in {"official", "generated"}:
                continue
            if token in seen:
                continue
            seen.add(token)
            normalized.append(token)
        if not normalized:
            return ["official"]
        return normalized

    def _signature_for_folder(self, folder: Path) -> _FolderSignature:
        try:
            folder_path = str(folder.resolve())
        except OSError:
            folder_path = str(folder)

        problem_md = folder / "problem.md"
        if not problem_md.is_file():
            return _FolderSignature(
                folder_path=folder_path,
                has_problem_md=0,
                mtime_ns=0,
                size=0,
            )

        try:
            stat = problem_md.stat()
            mtime_ns = int(stat.st_mtime_ns)
            size = int(stat.st_size)
        except OSError:
            mtime_ns = 0
            size = 0

        return _FolderSignature(
            folder_path=folder_path,
            has_problem_md=1,
            mtime_ns=mtime_ns,
            size=size,
        )

    def _scan_official_rows_unlocked(self) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        if not self._official_root.is_dir():
            self._official_cache.clear()
            return rows

        live_keys: set[str] = set()
        for folder in sorted(self._official_root.iterdir(), key=lambda p: p.name):
            if not folder.is_dir():
                continue
            matched = self._problem_id_re.match(folder.name)
            if not matched:
                continue

            cache_key = folder.name
            signature = self._signature_for_folder(folder)
            cached = self._official_cache.get(cache_key)
            if cached is not None and cached[0] == signature:
                row = cached[1]
            else:
                built = self._build_official_row(folder)
                if built is None:
                    continue
                row = built
                self._official_cache[cache_key] = (signature, row)

            live_keys.add(cache_key)
            rows.append(dict(row))

        stale = [key for key in self._official_cache if key not in live_keys]
        for key in stale:
            self._official_cache.pop(key, None)

        return rows

    def _scan_generated_candidates_unlocked(self) -> Dict[str, Dict[str, Path]]:
        rows: Dict[str, Dict[str, Path]] = {}
        if not self._generated_root.is_dir():
            self._flat_batch_cache.clear()
            return rows

        root_dirs = sorted((item for item in self._generated_root.iterdir() if item.is_dir()), key=lambda p: p.name)

        live_flat_cache_keys: set[str] = set()

        # Pass 1: flat layout (db/generated_candidates/<candidate_id>)
        for candidate_dir in root_dirs:
            if not (candidate_dir / "problem.md").is_file():
                continue

            signature = self._signature_for_folder(candidate_dir)
            flat_cache_key = signature.folder_path
            cached = self._flat_batch_cache.get(flat_cache_key)
            if cached is not None and cached[0] == signature:
                batch_id = cached[1]
            else:
                token = str(self._extract_flat_batch_id(candidate_dir) or "").strip()
                batch_id = token if token and self._batch_id_re.match(token) else ""
                self._flat_batch_cache[flat_cache_key] = (signature, batch_id)

            live_flat_cache_keys.add(flat_cache_key)
            if not batch_id:
                continue

            batch_rows = rows.setdefault(batch_id, {})
            batch_rows.setdefault(candidate_dir.name, candidate_dir)

        stale_flat = [key for key in self._flat_batch_cache if key not in live_flat_cache_keys]
        for key in stale_flat:
            self._flat_batch_cache.pop(key, None)

        # Pass 2: legacy nested layout (db/generated_candidates/<batch_id>/<candidate_id>)
        for batch_dir in root_dirs:
            if (batch_dir / "problem.md").is_file():
                continue
            batch_id = batch_dir.name
            if not self._batch_id_re.match(batch_id):
                continue
            if not batch_dir.is_dir():
                continue

            batch_rows = rows.setdefault(batch_id, {})
            for candidate_dir in sorted(batch_dir.iterdir(), key=lambda p: p.name):
                if not candidate_dir.is_dir():
                    continue
                if not (candidate_dir / "problem.md").is_file():
                    continue
                batch_rows.setdefault(candidate_dir.name, candidate_dir)

        return rows

    def _normalize_generated_batches(self, raw_values: List[str], available_batches: List[str]) -> List[str]:
        available_set = set(available_batches)
        normalized: List[str] = []
        seen = set()
        for value in raw_values:
            token = str(value or "").strip()
            if not token or token not in available_set:
                continue
            if token in seen:
                continue
            seen.add(token)
            normalized.append(token)
        return normalized

    def _scan_generated_rows_unlocked(self, *, generated_batches: List[str] | None) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        batch_candidates = self._scan_generated_candidates_unlocked()
        available_batches = sorted(batch_candidates.keys())
        selected_batches = (
            self._normalize_generated_batches(generated_batches or [], available_batches)
            if generated_batches is not None
            else list(available_batches)
        )
        if not selected_batches:
            selected_batches = list(available_batches)

        all_live_cache_keys: set[str] = set()
        for batch_id, candidates in batch_candidates.items():
            for candidate_id in candidates:
                all_live_cache_keys.add(f"{batch_id}::{candidate_id}")

        for batch_id in selected_batches:
            candidates = batch_candidates.get(batch_id, {})
            for candidate_id, folder in candidates.items():
                cache_key = f"{batch_id}::{candidate_id}"
                signature = self._signature_for_folder(folder)
                cached = self._generated_cache.get(cache_key)
                if cached is not None and cached[0] == signature:
                    row = cached[1]
                else:
                    built = self._build_generated_row(batch_id, folder)
                    if built is None:
                        continue
                    row = built
                    self._generated_cache[cache_key] = (signature, row)
                rows.append(dict(row))

        stale_generated = [key for key in self._generated_cache if key not in all_live_cache_keys]
        for key in stale_generated:
            self._generated_cache.pop(key, None)

        return rows
