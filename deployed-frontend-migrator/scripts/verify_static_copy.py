#!/usr/bin/env python3
"""Verify that a static frontend copy has no missing local asset paths."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

URL_RE = re.compile(r"url\(\s*[\"']?([^)'\"]+)[\"']?\s*\)")
IMPORT_RE = re.compile(r"@import\s*[\"']([^\"']+)[\"']")
HTML_REF_RE = re.compile(r"(?:src|href)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
JS_ASSET_RE = re.compile(r"(?:/assets/|assets/)[^\"'`\\ )]+")


def is_remote(value: str) -> bool:
    return value.startswith(("http://", "https://", "//", "data:", "blob:", "#"))


def local_path(root: Path, source: Path, ref: str) -> Path | None:
    ref = unquote(ref.split("?", 1)[0].split("#", 1)[0])
    if not ref or is_remote(ref):
        return None
    if ref.startswith("/") or ref.startswith("assets/"):
        return root / ref.lstrip("/")
    return source.parent / ref


def add_ref(missing: list[Path], root: Path, source: Path, ref: str) -> None:
    path = local_path(root, source, ref)
    if path is not None and not path.exists():
        missing.append(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Standalone frontend root")
    args = parser.parse_args()
    root = args.root.resolve()
    index = root / "index.html"
    if not index.exists():
        print(f"Missing {index}", file=sys.stderr)
        return 1

    missing: list[Path] = []
    external: set[str] = set()
    html = index.read_text(encoding="utf-8", errors="ignore")
    for ref in HTML_REF_RE.findall(html):
        if is_remote(ref):
            external.add(ref)
        else:
            add_ref(missing, root, index, ref)

    for css in root.rglob("*.css"):
        text = css.read_text(encoding="utf-8", errors="ignore")
        for ref in IMPORT_RE.findall(text) + URL_RE.findall(text):
            if is_remote(ref):
                external.add(ref)
            else:
                add_ref(missing, root, css, ref)

    for js in root.rglob("*.js"):
        text = js.read_text(encoding="utf-8", errors="ignore")
        for ref in JS_ASSET_RE.findall(text):
            add_ref(missing, root, js, ref)
        external.update(re.findall(r"https?://[^\"'` ]+", text))

    unique_missing = sorted(set(path.resolve() for path in missing))
    print(f"Checked {len(list(root.rglob('*')))} paths under {root}")
    print(f"External URLs retained: {len(external)}")
    if unique_missing:
        print("Missing local assets:", file=sys.stderr)
        for path in unique_missing:
            print(f"- {path}", file=sys.stderr)
        return 1
    print("Static copy asset check: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
