#!/usr/bin/env python3
"""Inventory the major repo surfaces so a comprehensive audit can prove coverage."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".turbo",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "tmp",
    "venv",
}

LANGUAGE_EXTENSIONS = {
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".css": "css",
    ".go": "go",
    ".h": "c",
    ".hpp": "cpp",
    ".html": "html",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript-react",
    ".kt": "kotlin",
    ".mjs": "javascript",
    ".php": "php",
    ".pl": "perl",
    ".py": "python",
    ".rb": "ruby",
    ".rs": "rust",
    ".sass": "sass",
    ".scss": "scss",
    ".sh": "shell",
    ".sql": "sql",
    ".svelte": "svelte",
    ".swift": "swift",
    ".ts": "typescript",
    ".tsx": "typescript-react",
    ".vue": "vue",
}

SURFACE_HINTS = {
    "docs": {
        "dirs": {"docs"},
        "files": {"readme.md", "contributing.md", "architecture.md", "adr.md"},
    },
    "ci_cd": {
        "dirs": {".github", ".circleci"},
        "files": {
            ".gitlab-ci.yml",
            "jenkinsfile",
            "azure-pipelines.yml",
            "buildkite.yml",
        },
    },
    "scripts": {
        "dirs": {"bin", "hack", "ops", "script", "scripts", "tool", "tools", "tooling"},
        "files": set(),
    },
    "tests": {
        "dirs": {"__tests__", "e2e", "spec", "test", "tests"},
        "files": set(),
    },
    "frontend": {
        "dirs": {"components", "pages", "public"},
        "files": set(),
    },
    "infra": {
        "dirs": {"helm", "infra", "k8s", "terraform"},
        "files": {
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            "terragrunt.hcl",
        },
    },
    "data_db": {
        "dirs": {"alembic", "db", "migrations", "prisma", "sql"},
        "files": {"schema.prisma"},
    },
    "observability": {
        "dirs": {"grafana", "monitoring", "observability", "prometheus"},
        "files": {"otel-collector-config.yaml", "sentry.properties"},
    },
    "config": {
        "dirs": set(),
        "files": {
            ".env",
            ".env.example",
            ".env.sample",
            ".pre-commit-config.yaml",
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "poetry.lock",
            "pnpm-lock.yaml",
            "yarn.lock",
            "go.mod",
            "cargo.toml",
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
            "composer.json",
        },
    },
}

FRONTEND_EXTENSIONS = {
    ".css",
    ".html",
    ".jsx",
    ".sass",
    ".scss",
    ".svelte",
    ".tsx",
    ".vue",
}

MAX_SAMPLE_PATHS = 8


@dataclass
class SurfaceRecord:
    paths: set[str] = field(default_factory=set)

    def add(self, rel_path: str) -> None:
        self.paths.add(rel_path)

    def sample(self) -> list[str]:
        return sorted(self.paths)[:MAX_SAMPLE_PATHS]


def suggested_review_passes(languages: Counter[str], surfaces: dict[str, SurfaceRecord]) -> list[str]:
    passes: list[str] = []

    passes.append("references/change-safety-harness.md")

    if languages:
        passes.append("references/performance-optimization-guide.md")

    if languages.get("python"):
        passes.append("references/python-review-guide.md")

    js_like = {
        "javascript",
        "javascript-react",
        "typescript",
        "typescript-react",
    }
    if any(languages.get(name) for name in js_like):
        passes.append("references/javascript-review-guide.md")

    html_like = {"html", "vue", "svelte"}
    if any(languages.get(name) for name in html_like):
        passes.append("references/html-review-guide.md")

    if surfaces["frontend"].paths:
        passes.append("references/frontend-clean-code-extension.md")

    if surfaces["tests"].paths:
        passes.append("references/testing-validation-guide.md")

    if surfaces["scripts"].paths:
        passes.append("scripts/find_stale_scripts.py")

    return passes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory the major surfaces of a repository for comprehensive audits."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text.",
    )
    return parser.parse_args()


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


def detect_surfaces(root: Path, files: list[Path]) -> dict[str, SurfaceRecord]:
    surfaces = {name: SurfaceRecord() for name in SURFACE_HINTS}
    for path in files:
        rel_path = path.relative_to(root).as_posix()
        lower_name = path.name.lower()
        lower_parts = {part.lower() for part in path.relative_to(root).parts[:-1]}

        for name, hints in SURFACE_HINTS.items():
            if lower_name in hints["files"] or lower_parts & hints["dirs"]:
                surfaces[name].add(rel_path)

        if path.suffix.lower() in FRONTEND_EXTENSIONS:
            surfaces["frontend"].add(rel_path)

    return surfaces


def detect_languages(files: list[Path]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in files:
        language = LANGUAGE_EXTENSIONS.get(path.suffix.lower())
        if language:
            counts[language] += 1
    return counts


def print_text(root: Path, surfaces: dict[str, SurfaceRecord], languages: Counter[str]) -> None:
    print(f"Repo surface inventory for {root}")
    if languages:
        language_summary = ", ".join(
            f"{name}={count}" for name, count in sorted(languages.items())
        )
        print(f"Languages: {language_summary}")
    else:
        print("Languages: none detected")

    print()
    print("Surfaces:")
    for name in sorted(surfaces):
        record = surfaces[name]
        label = name.replace("_", " ")
        if not record.paths:
            print(f"- {label}: not present")
            continue
        print(f"- {label}: {len(record.paths)} paths")
        print(f"  sample: {', '.join(record.sample())}")

    review_passes = suggested_review_passes(languages, surfaces)
    print()
    print("Suggested review passes:")
    if not review_passes:
        print("- none")
    else:
        for item in review_passes:
            print(f"- {item}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")

    files = iter_repo_files(root)
    surfaces = detect_surfaces(root, files)
    languages = detect_languages(files)

    if args.json:
        review_passes = suggested_review_passes(languages, surfaces)
        payload = {
            "root": str(root),
            "languages": dict(sorted(languages.items())),
            "surfaces": {
                name: {
                    "count": len(record.paths),
                    "sample_paths": record.sample(),
                }
                for name, record in sorted(surfaces.items())
            },
            "suggested_review_passes": review_passes,
        }
        print(json.dumps(payload, indent=2))
        return 0

    print_text(root, surfaces, languages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
