#!/usr/bin/env python3
"""Read-only checks for this text-only public skill distribution (stdlib only)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL_NAME = "paper-ppt-cn"
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__"}
PRIVATE_DIRS = {"inputs", "outputs", "work", "private"}
EXCLUDED_SUFFIXES = {".pptx", ".pdf", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".ttf", ".otf", ".pem", ".key"}
PERSONAL_PATH = re.compile(r"\b[A-Za-z]:[\\/]Users[\\/][^\\/\s]+|/(?:Users|home)/[A-Za-z0-9_.-]+/", re.I)
TOKEN = re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")


def validate(root: Path) -> list[str]:
    """Return actionable errors without printing matched paths or credential values."""
    root = root.resolve()
    errors: list[str] = []
    entry = root / "skills" / SKILL_NAME / "SKILL.md"
    metadata = entry.parent / "agents" / "openai.yaml"
    if not entry.is_file():
        errors.append("Missing skill entrypoint")
    else:
        text = entry.read_text(encoding="utf-8-sig")
        front = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
        if not front:
            errors.append("Skill entrypoint needs YAML frontmatter")
        else:
            fields = front.group(1)
            name = re.search(r"(?m)^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", fields)
            if not name or name.group(1) != SKILL_NAME:
                errors.append("Skill name does not match installation directory")
            if not re.search(r"(?m)^description:\s*\S.+$", fields):
                errors.append("Missing skill description")
        if re.search(r"\bTODO\b|\[INSERT|\[PLACEHOLDER", text, re.I):
            errors.append("Unfinished skill scaffold")
    if not metadata.is_file():
        errors.append("Missing UI metadata")
    elif "$" + SKILL_NAME not in metadata.read_text(encoding="utf-8-sig"):
        errors.append("UI default prompt must use the installed skill name")

    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        label = relative.as_posix()
        if path.is_symlink():
            errors.append(f"Do not distribute symlinks: {label}")
            continue
        if not path.is_file():
            continue
        if any(part in PRIVATE_DIRS for part in relative.parts) or path.name.startswith(".env"):
            errors.append(f"Private/generated input in release: {label}")
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            errors.append(f"Third-party asset or binary is outside this text-only release: {label}")
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            errors.append(f"Unexpected non-text release file: {label}")
            continue
        if PERSONAL_PATH.search(text):
            errors.append(f"Personal absolute path in release: {label}")
        if TOKEN.search(text):
            errors.append(f"Credential-like material in release: {label}")
        if path.suffix.lower() != ".md":
            continue
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for link in MARKDOWN_LINK.findall(prose):
            link = link.strip().strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme == "file":
                errors.append(f"Local file URI in public documentation: {label}")
                continue
            if parsed.scheme or parsed.netloc or link.startswith("#"):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root):
                errors.append(f"Relative link escapes release directory: {label}")
            elif not target.exists():
                errors.append(f"Broken relative resource link in {label}: {parsed.path}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: skill entrypoint, metadata, resource links and public-package hygiene")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
