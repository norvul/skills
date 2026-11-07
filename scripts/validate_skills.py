"""Validate published skills without executing their instructions or scripts."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject ambiguous frontmatter rather than silently overwriting fields."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise yaml.constructor.ConstructorError(
                    None, None, f"invalid or duplicate YAML key: {key!r}", key_node.start_mark
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def check_frontmatter(text: str, directory_name: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return ["SKILL.md must start with YAML frontmatter delimited by ---"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ["YAML frontmatter has no closing --- delimiter"]
    try:
        fields = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        return [f"invalid YAML frontmatter: {error}"]
    if not isinstance(fields, dict):
        return ["YAML frontmatter must be a mapping"]

    errors = []
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    unknown = fields.keys() - allowed
    if unknown:
        errors.append(f"put custom fields inside metadata: {', '.join(sorted(unknown))}")

    name = fields.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("name must contain lowercase ASCII letters, numbers, and single hyphens")
    elif len(name) > 64 or name != directory_name:
        errors.append("name must match the directory name and be at most 64 characters")

    for field, limit in (("description", 1024), ("compatibility", 500)):
        if field == "description" or field in fields:
            value = fields.get(field)
            if not isinstance(value, str) or not value.strip() or len(value) > limit:
                errors.append(f"{field} must be a nonempty string of at most {limit} characters")
    for field in ("license", "allowed-tools"):
        if field in fields and (
            not isinstance(fields[field], str) or not fields[field].strip()
        ):
            errors.append(f"{field} must be a nonempty string")
    if "metadata" in fields:
        metadata = fields["metadata"]
        if not isinstance(metadata, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in metadata.items()
        ):
            errors.append("metadata must map string keys to string values")
    if not "\n".join(lines[end + 1 :]).strip():
        errors.append("SKILL.md must contain instructions after its frontmatter")
    return errors


def check_file_links(text: str, source: Path, root: Path) -> list[str]:
    """Check Markdown links and images, ignoring code examples and remote URLs."""
    errors = []
    parser = MarkdownIt()
    # Inspect destinations for linting even when a renderer would refuse the URL.
    parser.validateLink = lambda _href: True
    for token in parser.parse(text):
        for child in token.children or []:
            attribute = {"link_open": "href", "image": "src"}.get(child.type)
            if not attribute:
                continue
            href = child.attrGet(attribute) or ""
            try:
                url = urlsplit(href)
            except ValueError:
                errors.append(f"invalid link: {href}")
                continue
            if re.match(r"^[a-zA-Z]:[\\/]", href) or url.scheme == "file":
                errors.append(f"use a portable relative file link: {href}")
                continue
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if path.startswith("/") or "\\" in path:
                errors.append(f"use a portable relative file link: {href}")
                continue
            target = (source.parent / path).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"file link leaves the repository: {href}")
            elif not target.exists():
                errors.append(f"missing linked file: {href}")
    return errors


def validate_repository(root: Path) -> tuple[int, list[str]]:
    skills = root / "skills"
    if not skills.is_dir() or skills.is_symlink():
        return 0, ["skills/ must be a real directory"]
    errors = []
    count = 0
    for directory in sorted(skills.iterdir()):
        relative = directory.relative_to(root)
        if directory.is_symlink():
            errors.append(f"{relative}: symbolic links are not supported")
            continue
        if directory.is_file():
            if directory.name != "README.md":
                errors.append(f"{relative}: put skill files in their own skill directory")
            continue
        count += 1
        files = list(directory.rglob("*"))
        symlinks = [path for path in files if path.is_symlink()]
        if symlinks:
            errors.extend(f"{path.relative_to(root)}: symbolic links are not supported" for path in symlinks)
            continue
        skill = directory / "SKILL.md"
        if not skill.is_file():
            errors.append(f"{relative}: missing SKILL.md")
            continue
        for path in files:
            if not path.is_file() or path.suffix.lower() != ".md":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                errors.append(f"{path.relative_to(root)}: cannot read UTF-8 text: {error}")
                continue
            problems = check_file_links(text, path, root)
            if path == skill:
                problems.extend(check_frontmatter(text, directory.name))
            errors.extend(f"{path.relative_to(root)}: {problem}" for problem in problems)
    return count, errors


def main() -> int:
    count, errors = validate_repository(Path(__file__).resolve().parents[1])
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {count} skill(s)." + (" No skills published yet." if count == 0 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
