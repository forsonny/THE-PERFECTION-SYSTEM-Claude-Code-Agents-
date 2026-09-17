#!/usr/bin/env python3
"""Offline checks for this repository, not a model or general YAML validator."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/the-perfection-system/SKILL.md")
STANDALONE = Path("THE-PERFECTION-SYSTEM.md")
REQUIRED = (
    SKILL,
    STANDALONE,
    Path("README.md"),
    Path("CHANGELOG.md"),
    SKILL.parent / "references/review-protocol.md",
    SKILL.parent / "references/examples.md",
    SKILL.parent / "assets/run-template.md",
    Path("tests/scenarios.json"),
)
STATUSES = {"accepted", "blocked", "budget_exhausted", "stalled", "stopped"}
HEADER = "<!-- Generated from skills/the-perfection-system/SKILL.md. Edit that file, then run python3 scripts/validate.py --sync. -->\n\n"
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")


def parse_skill(text: str) -> tuple[dict[str, str], str]:
    """Accept only this package's two-field, single-line YAML subset.

    The description is a JSON double-quoted string, also valid in YAML.
    Deliberately reject unfamiliar syntax rather than guess its meaning.
    """
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("SKILL.md must start with closed YAML frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    fields: dict[str, str] = {}
    for line in header.splitlines():
        key, separator, raw = line.partition(": ")
        if not separator or key not in {"name", "description"} or key in fields:
            raise ValueError("frontmatter must contain only unique name and description fields")
        if key == "description":
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError("description must be a JSON double-quoted string") from exc
            if not isinstance(value, str):
                raise ValueError("description must be a string")
        else:
            value = raw
        fields[key] = value
    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("name must be 1-64 lowercase alphanumeric/hyphen characters")
    description = fields.get("description", "")
    if not description.strip() or len(description) > 1024:
        raise ValueError("description must contain 1-1024 characters")
    if not body.strip():
        raise ValueError("skill body must not be empty")
    return fields, body.lstrip("\n")


def standalone_text(text: str) -> str:
    """Generate the original entry point with correctly rebased resource links."""
    _, body = parse_skill(text)
    body = re.sub(
        r"\]\((references|assets)/",
        r"](skills/the-perfection-system/\1/",
        body,
    )
    return HEADER + body.rstrip() + "\n"


def validate_scenarios(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, list) or not data:
        return ["scenarios must be a non-empty JSON array"]
    seen: set[str] = set()
    required = {"id", "mode", "prompt", "context", "expect", "reject"}
    for index, case in enumerate(data):
        prefix = f"scenario {index + 1}"
        if not isinstance(case, dict) or set(case) != required:
            errors.append(f"{prefix}: fields must be {sorted(required)}")
            continue
        for key in ("id", "mode", "prompt", "context"):
            if not isinstance(case[key], str) or not case[key].strip():
                errors.append(f"{prefix}: {key} must be non-empty text")
        identifier = case["id"]
        if isinstance(identifier, str):
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
                errors.append(f"{prefix}: invalid id")
            if identifier in seen:
                errors.append(f"{prefix}: duplicate id {identifier}")
            seen.add(identifier)
        for key in ("expect", "reject"):
            items = case[key]
            if not isinstance(items, list) or not items or any(
                not isinstance(item, str) or not item.strip() for item in items
            ):
                errors.append(f"{prefix}: {key} must be a non-empty list of non-empty strings")
    return errors


def validate(root: Path) -> list[str]:
    """Return actionable errors without making edits or network requests."""
    root = root.resolve()
    errors: list[str] = []
    for path in REQUIRED:
        target = root / path
        if not target.is_file():
            errors.append(f"missing required file: {path}")
        elif target.is_symlink() or root not in target.resolve().parents:
            errors.append(f"required file must be an in-repository regular file: {path}")
    if errors:
        return errors
    try:
        text = (root / SKILL).read_text(encoding="utf-8")
        fields, _ = parse_skill(text)
        if fields["name"] != SKILL.parent.name:
            errors.append("skill name must match its parent directory")
        if len(text.splitlines()) > 500:
            errors.append("keep the core skill at or below 500 lines")
        if (root / STANDALONE).read_text(encoding="utf-8") != standalone_text(text):
            errors.append("standalone copy is stale; run python3 scripts/validate.py --sync")
        for status in sorted(STATUSES):
            if f"`{status}`" not in text:
                errors.append(f"core skill is missing terminal status {status}")
        data = json.loads((root / "tests/scenarios.json").read_text(encoding="utf-8"))
        errors.extend(validate_scenarios(data))
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    for relative in [path for path in REQUIRED if path.suffix == ".md"]:
        path = root / relative
        try:
            content = path.read_text(encoding="utf-8")
            for target in LINK.findall(content):
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                destination = (path.parent / unquote(url.path)).resolve()
                if root not in destination.parents:
                    errors.append(f"{relative}: link leaves repository: {target}")
                elif not destination.exists():
                    errors.append(f"{relative}: broken relative link: {target}")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync", action="store_true", help="regenerate the standalone edition before checking")
    args = parser.parse_args()
    try:
        if args.sync:
            destination = ROOT / STANDALONE
            if destination.is_symlink():
                raise ValueError("refusing to replace a symlink at the standalone path")
            source = (ROOT / SKILL).read_text(encoding="utf-8")
            destination.write_text(standalone_text(source), encoding="utf-8")
        errors = validate(ROOT)
    except (OSError, UnicodeError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: package structure, links, standalone consistency, and scenario format.")
    print("Behavioral scenarios were NOT executed; no model or host compatibility is certified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
