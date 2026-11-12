#!/usr/bin/env python3
"""Give the public Harika Fikirler CSS a content-addressed filename.

Browsers and CDNs may ignore a reused ?v=20261111 query. A new filename
guarantees that every modified CSS body has a distinct request URL.
Run only on staged deployment copies, without changing source files.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

LINK = re.compile(r'(?P<prefix>href="(?P<up>(?:\.\./)+)assets/)blog(?:-[a-f0-9]{12})?\.css(?:\?v=[^"]*)?"')


def version(root: Path) -> str:
    css = root / "assets/blog.css"
    if not css.is_file():
        raise ValueError("Staged blog.css missing; do not deploy")
    digest = hashlib.sha256(css.read_bytes()).hexdigest()[:12]
    versioned = css.with_name(f"blog-{digest}.css")
    versioned.write_bytes(css.read_bytes())
    pages = sorted((root / "blog").rglob("index.html"))
    if len(pages) < 4:
        raise ValueError(f"Expected at least 4 blog pages, got {len(pages)}")

    for page in pages:
        original = page.read_text(encoding="utf-8")
        if len(LINK.findall(original)) != 1:
            raise ValueError(f"Exactly one blog stylesheet expected in {page}")
        updated = LINK.sub(lambda m: f'{m.group("prefix")}blog-{digest}.css"', original, count=1)
        if updated == original or f"blog-{digest}.css" not in updated:
            raise ValueError(f"Could not fingerprint stylesheet on {page}")
        page.write_text(updated, encoding="utf-8")
        print(f"Cache-proof stylesheet linked in {page.relative_to(root)}")
    print(f"BLOG_CSS_FINGERPRINT={digest}")
    return digest


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--site-root", required=True, type=Path)
    args = p.parse_args()
    version(args.site_root)
