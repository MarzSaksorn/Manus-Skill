#!/usr/bin/env python3
"""Localize Google Font imports in a copied CSS bundle."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

FONT_URL_RE = re.compile(r"url\(\s*[\"']?(https://[^)\"']+\.(?:woff2?|ttf|otf)(?:\?[^)\"']*)?)[\"']?\s*\)")
GOOGLE_IMPORT_RE = re.compile(
    r"@import\s*[\"'](https://fonts\.googleapis\.com/[^\"']+)[\"']\s*;?",
    re.IGNORECASE,
)


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(request, timeout=30).read().decode("utf-8")


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(request, timeout=30).read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("css", type=Path, help="Copied CSS bundle to update")
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=None,
        help="Directory for fonts.css and fonts/; defaults to the CSS file directory",
    )
    parser.add_argument(
        "--font-css-name",
        default="fonts.css",
        help="Generated local font stylesheet filename",
    )
    args = parser.parse_args()

    css_path = args.css.resolve()
    asset_dir = (args.asset_dir or css_path.parent).resolve()
    asset_dir.mkdir(parents=True, exist_ok=True)
    font_dir = asset_dir / "fonts"

    bundle = css_path.read_text(encoding="utf-8")
    imports = GOOGLE_IMPORT_RE.findall(bundle)
    if not imports:
        print("No Google Font import found; nothing to localize.")
        return 0

    source_css = "\n".join(fetch_text(url) for url in imports)
    urls = list(dict.fromkeys(FONT_URL_RE.findall(source_css)))
    if not urls:
        print("Google Font import found, but no downloadable font files were discovered.", file=sys.stderr)
        return 1

    font_dir.mkdir(parents=True, exist_ok=True)
    local_css = source_css
    for index, url in enumerate(urls, start=1):
        source_name = url.rsplit("/", 1)[-1].split("?", 1)[0]
        filename = f"{index:02d}-{source_name}"
        target = font_dir / filename
        if not target.exists():
            target.write_bytes(fetch_bytes(url))
        relative = os.path.relpath(target, asset_dir).replace(os.sep, "/")
        local_css = local_css.replace(url, f"./{relative}")

    font_css_path = asset_dir / args.font_css_name
    font_css_path.write_text(local_css, encoding="utf-8")
    relative_import = os.path.relpath(font_css_path, css_path.parent).replace(os.sep, "/")
    replacement = f'@import "./{relative_import}";'
    updated, count = GOOGLE_IMPORT_RE.subn(replacement, bundle, count=1)
    if count != 1:
        print("Failed to replace the Google Font import.", file=sys.stderr)
        return 1
    css_path.write_text(updated, encoding="utf-8")
    print(f"Localized {len(urls)} font files into {font_dir}")
    print(f"Updated {css_path} to import {font_css_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
