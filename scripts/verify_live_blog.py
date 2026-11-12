#!/usr/bin/env python3
"""Verify the actual public Turhost blog HTML and versioned CSS after FTP deploy.

This checks HTTP responses, not GitHub's success status or a local preview.
A failed public check must not be reported as a confirmed live update.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = "https://harikaseylerdukkani.com/dosemealti/"
SLUGS = (
    "blog/",
    "blog/dogum-gunu-hediyesi-nasil-secilir/",
    "blog/cocuklar-icin-oyuncak-secerken/",
    "blog/kucuk-butceyle-anlamli-hediyeler/",
)


def get(url: str) -> tuple[bytes, dict[str, str]]:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; HarikaDeployVerifier/1.0)",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    })
    with urlopen(req, timeout=22) as res:
        if res.status != 200:
            raise RuntimeError(f"HTTP {res.status} for {url}")
        headers = {k.lower(): v for k, v in res.headers.items()}
        return res.read(), headers


def check(css: bytes, expected_digest: str, token: str) -> None:
    css_url = ROOT + f"assets/blog-{expected_digest}.css?verify={token}"
    content, headers = get(css_url)
    if content != css:
        raise AssertionError(
            f"Public CSS content differs: expected sha256={hashlib.sha256(css).hexdigest()} "
            f"got sha256={hashlib.sha256(content).hexdigest()}"
        )
    print("Verified public content-hashed CSS:", css_url,
          "length=", len(content),
          "cache-control=", headers.get("cache-control", "(not set)"),
          "age=", headers.get("age", "(not set)"))

    for slug in SLUGS:
        # Two URL forms: ordinary and deliberately fresh query string. Both
        # must serve the new markup, otherwise a CDN may still be stale.
        for extra in ("", f"?verify={token}"):
            url = ROOT + slug + extra
            body, head = get(url)
            html = body.decode("utf-8")
            expected_link = f"blog-{expected_digest}.css"
            if expected_link not in html:
                raise AssertionError(
                    f"OLD HTML: new CSS link {expected_link!r} missing from {url}"
                )
            if 'class="blog-page"' not in html:
                raise AssertionError(f"Not the expected blog page: {url}")
            if slug == "blog/":
                if 'class="blog-pillar-inner wrap"' not in html:
                    raise AssertionError(f"New compact category tiles missing: {url}")
                if 'class="blog-local"' in html:
                    raise AssertionError(f"Obsolete duplicate promotional section remains: {url}")
                if html.count('class="blog-pillar-number"') != 4:
                    raise AssertionError(f"Not all four compact category tiles present: {url}")
            print("Verified public HTML:", url, "length=", len(body),
                  "cache-control=", head.get("cache-control", "(not set)"),
                  "age=", head.get("age", "(not set)"))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--site-root", required=True, type=Path)
    p.add_argument("--sha", required=True, help="GitHub commit SHA for unique query")
    args = p.parse_args()
    css = (args.site_root / "assets/blog.css").read_bytes()
    digest = hashlib.sha256(css).hexdigest()[:12]
    if not (args.site_root / f"assets/blog-{digest}.css").is_file():
        raise ValueError("Staged fingerprinted stylesheet missing")

    for attempt in range(1, 6):
        try:
            check(css, digest, args.sha[:12] + f"-{attempt}")
            print("PUBLIC_LIVE_BLOG_VERIFIED")
            return
        except (URLError, HTTPError, TimeoutError, AssertionError, RuntimeError) as exc:
            print(f"Public check attempt {attempt}/5 failed: {exc}", flush=True)
            if attempt < 5:
                time.sleep(8)
    raise SystemExit("PUBLIC_LIVE_BLOG_NOT_VERIFIED: do not claim site is updated")


if __name__ == "__main__":
    main()
