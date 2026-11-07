#!/usr/bin/env python3
"""Surface likely stale scripts by checking how strongly they are referenced."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "temp",
    "tmp",
    "venv",
}

SCRIPT_DIR_NAMES = {
    "bin",
    "ci",
    "hack",
    "ops",
    "script",
    "scripts",
    "tool",
    "tools",
    "tooling",
}

SCRIPT_EXTENSIONS = {
    ".bash",
    ".fish",
    ".js",
    ".pl",
    ".ps1",
    ".py",
    ".rb",
    ".sh",
    ".ts",
    ".zsh",
}

MAX_SCAN_BYTES = 1_000_000
MAX_REF_SAMPLES = 5


@dataclass
class ScriptRecord:
    rel_path: str
    path_refs: set[str] = field(default_factory=set)
    name_refs: set[str] = field(default_factory=set)
    last_commit_date: str | None = None

    @property
    def basename(self) -> str:
        return Path(self.rel_path).name

    @property
    def status(self) -> str:
        if not self.path_refs and not self.name_refs:
            return "likely-stale"
        if len(self.path_refs) >= 2:
            return "referenced"
        if len(self.path_refs) >= 1 and len(self.name_refs) >= 1:
            return "referenced"
        if len(self.name_refs) >= 3:
            return "referenced"
        return "needs-review"

    def sample_refs(self) -> list[str]:
        refs = sorted(self.path_refs | self.name_refs)
        return refs[:MAX_REF_SAMPLES]

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.rel_path,
            "status": self.status,
            "last_commit_date": self.last_commit_date,
            "path_ref_count": len(self.path_refs),
            "name_ref_count": len(self.name_refs),
            "sample_refs": self.sample_refs(),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Identify candidate stale scripts by scanning for repo references."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include referenced scripts in text output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text.",
    )
    return parser.parse_args()


def is_probably_text(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(4096)
    except OSError:
        return False
    return b"\0" not in chunk


def has_shebang(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            first_line = handle.readline(256)
    except OSError:
        return False
    return first_line.startswith(b"#!")


def is_candidate_script(root: Path, path: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    parent_parts = {part.lower() for part in rel_parts[:-1]}
    in_script_dir = bool(parent_parts & SCRIPT_DIR_NAMES)
    extension = path.suffix.lower()
    # Windows X_OK does not distinguish an ordinary module from a CLI script.
    executable = os.name != "nt" and os.access(path, os.X_OK)
    shebang = has_shebang(path)

    if in_script_dir and (extension in SCRIPT_EXTENSIONS or executable or shebang):
        return True
    if shebang:
        return True
    if executable and (extension in SCRIPT_EXTENSIONS or shebang):
        return True
    return False


def iter_repo_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current_root, dirnames, filenames in os.walk(root):
        current_dir = Path(current_root)
        dirnames[:] = [
            name for name in dirnames
            if name not in IGNORE_DIRS and not (current_dir / name).is_symlink()
        ]
        for filename in filenames:
            path = current_dir / filename
            if not path.is_symlink():
                files.append(path)
    return files


def collect_candidates(root: Path, files: list[Path]) -> list[ScriptRecord]:
    candidates: list[ScriptRecord] = []
    for path in files:
        if not path.is_file() or not is_probably_text(path):
            continue
        if is_candidate_script(root, path):
            rel_path = path.relative_to(root).as_posix()
            candidates.append(ScriptRecord(rel_path=rel_path))
    return sorted(candidates, key=lambda record: record.rel_path)


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_SCAN_BYTES:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def scan_references(root: Path, files: list[Path], candidates: list[ScriptRecord]) -> None:
    patterns = []
    for record in candidates:
        rel_path = record.rel_path
        basename_pattern = re.compile(
            rf"(?<![A-Za-z0-9_./\\\\-]){re.escape(record.basename)}(?![A-Za-z0-9_./\\\\-])"
        )
        patterns.append(
            (
                record,
                rel_path,
                rel_path.replace("/", "\\"),
                basename_pattern,
            )
        )

    for file_path in files:
        if not file_path.is_file() or not is_probably_text(file_path):
            continue
        rel_path = file_path.relative_to(root).as_posix()
        content = read_text(file_path)
        if not content:
            continue

        for record, posix_path, windows_path, basename_pattern in patterns:
            if rel_path == record.rel_path:
                continue
            if posix_path in content or windows_path in content:
                record.path_refs.add(rel_path)
                continue
            if basename_pattern.search(content):
                record.name_refs.add(rel_path)


def git_available(root: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0


def populate_git_dates(root: Path, candidates: list[ScriptRecord]) -> None:
    if not git_available(root):
        return

    for record in candidates:
        result = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%cs", "--", record.rel_path],
            capture_output=True,
            text=True,
            check=False,
        )
        date_text = result.stdout.strip()
        if result.returncode == 0 and date_text:
            record.last_commit_date = date_text


def sort_records(records: list[ScriptRecord]) -> list[ScriptRecord]:
    status_rank = {"likely-stale": 0, "needs-review": 1, "referenced": 2}
    return sorted(
        records,
        key=lambda record: (
            status_rank[record.status],
            len(record.path_refs) + len(record.name_refs),
            record.last_commit_date or "",
            record.rel_path,
        ),
    )


def print_text(records: list[ScriptRecord], include_all: bool) -> None:
    buckets = {"likely-stale": [], "needs-review": [], "referenced": []}
    for record in records:
        buckets[record.status].append(record)

    print(f"Scanned {len(records)} candidate scripts.")
    print("Heuristic only: treat this as a shortlist for manual confirmation.")

    ordered_statuses = ["likely-stale", "needs-review"]
    if include_all:
        ordered_statuses.append("referenced")

    for status in ordered_statuses:
        print()
        print(status.upper())
        if not buckets[status]:
            print("- none")
            continue

        for record in buckets[status]:
            last_commit = record.last_commit_date or "unknown"
            print(
                f"- {record.rel_path} | last_commit={last_commit} "
                f"| path_refs={len(record.path_refs)} | name_refs={len(record.name_refs)}"
            )
            refs = record.sample_refs()
            if refs:
                print(f"  refs: {', '.join(refs)}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")

    files = iter_repo_files(root)
    candidates = collect_candidates(root, files)
    scan_references(root, files, candidates)
    populate_git_dates(root, candidates)
    ordered = sort_records(candidates)

    if args.json:
        payload = {
            "root": str(root),
            "candidate_count": len(ordered),
            "results": [record.as_dict() for record in ordered],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print_text(ordered, include_all=args.all)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
