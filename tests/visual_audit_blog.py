#!/usr/bin/env python3
"""Rendered browser audit: all blog pages across real mobile/tablet/desktop widths.

Run against the exact assembled static deployment using Playwright Chromium.
Screenshots and JSON diagnostics are saved under ui-audit/.
"""
from __future__ import annotations
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import threading
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "preview"
OUT = REPO / "ui-audit"
SLUGS = ("", "dogum-gunu-hediyesi-nasil-secilir/",
         "cocuklar-icin-oyuncak-secerken/", "kucuk-butceyle-anlamli-hediyeler/")
WIDTHS = (320, 375, 390, 430, 768, 1024, 1440)
MIN_GUTTER = 19

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)
    def log_message(self, format, *args):
        pass

def main():
    OUT.mkdir(exist_ok=True)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    th = threading.Thread(target=httpd.serve_forever, daemon=True)
    th.start()
    errors = []
    results = []
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
        # GitHub ubuntu-latest ships stable Chrome; local fallback uses Chromium.
        chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
        if chrome:
            launch["executable_path"] = chrome
        browser = p.chromium.launch(**launch)
        for slug in SLUGS:
            for width in WIDTHS:
                height = 860 if width <= 768 else 900
                ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
                page = ctx.new_page()
                url = f"http://127.0.0.1:{httpd.server_port}/dosemealti/blog/{slug}"
                row = {"page": slug or "archive", "width": width}
                try:
                    response = page.goto(url, wait_until="load", timeout=30000)
                    if not response or response.status >= 400:
                        raise AssertionError(f"HTTP {response.status if response else 'none'}")
                    # Lazy images below the fold are legitimately incomplete at load.
                    # Force their loading before measuring *failed* images.
                    page.evaluate("document.querySelectorAll('main img').forEach(img => img.loading = 'eager')")
                    page.wait_for_function(
                        "() => [...document.querySelectorAll('main img')].every(img => img.complete)",
                        timeout=4000)
                    row.update(page.evaluate("""() => {
                      const bb = sel => {
                        const el=document.querySelector(sel);
                        if(!el)return null;
                        const r=el.getBoundingClientRect();
                        return {x:+r.x.toFixed(1),left:+r.left.toFixed(1),
                          right:+r.right.toFixed(1),width:+r.width.toFixed(1),
                          height:+r.height.toFixed(1)};
                      };
                      const visible = sel => {
                        const el=document.querySelector(sel);
                        return !!el && getComputedStyle(el).display!=='none';
                      };
                      const images = [...document.querySelectorAll('main img')].filter(img=>{
                        const r=img.getBoundingClientRect();
                        return r.width>0 && r.height>0 && img.complete && img.naturalWidth===0;
                      }).map(img=>img.getAttribute('src'));
                      return {
                        screen: innerWidth,
                        documentWidth: document.documentElement.scrollWidth,
                        bodyWidth: document.body.scrollWidth,
                        hero: bb('.blog-hero-inner,.post-hero-inner'),
                        heroImage: bb('.blog-hero-photo,.post-hero-image'),
                        journal: bb('.blog-journal'),
                        pillar: bb('.blog-pillar-inner'),
                        pillarLinks: [...document.querySelectorAll('.blog-pillar-grid a')].map(a=>{const r=a.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,height:r.height}}),
                        articleContent: bb('.post-content'),
                        footer: bb('.site-footer'),
                        header: bb('.header'),
                        missingVisibleImages: images,
                        activeBlogLink: !!document.querySelector('.header-blog-link[aria-current="page"]'),
                        screenshotContent: document.querySelector('h1')?.innerText || '',
                        wrapperWidth: getComputedStyle(document.querySelector('.blog-page')).getPropertyValue('--blog-gutter').trim()
                      };
                    }"""))
                    if row["documentWidth"] > width + 1 or row["bodyWidth"] > width+1:
                        errors.append(f"{slug or 'archive'} {width}px: horizontal overflow document={row['documentWidth']} body={row['bodyWidth']}")
                    for name in ("hero", "heroImage", "journal", "pillar", "articleContent"):
                        rect = row.get(name)
                        if rect and width <= 768:
                            if rect["left"] < MIN_GUTTER:
                                errors.append(f"{slug or 'archive'} {width}px: {name} touches left edge ({rect['left']})")
                            if rect["right"] > width - MIN_GUTTER:
                                errors.append(f"{slug or 'archive'} {width}px: {name} touches right edge ({rect['right']})")
                    for link in row.get("pillarLinks", []):
                        if link["width"] < 100 or link["height"] < 44:
                            errors.append(f"archive {width}px: category tile too small {link}")
                        if link["left"] < MIN_GUTTER or link["right"] > width - MIN_GUTTER:
                            errors.append(f"archive {width}px: category tile out of safe margins {link}")
                    if row.get("missingVisibleImages"):
                        errors.append(f"{slug or 'archive'} {width}px: images failed to load: {row['missingVisibleImages']}")
                    if not row["activeBlogLink"]:
                        errors.append(f"{slug or 'archive'} {width}px: blog current nav state missing")
                    if width in (320,375,768,1440):
                        shot = f"{(slug[:-1] if slug else 'archive')}-{width}.png"
                        page.screenshot(path=str(OUT/shot), full_page=True, animations="disabled")
                except Exception as e:
                    errors.append(f"{slug or 'archive'} {width}px: {type(e).__name__}: {e}")
                results.append(row)
                ctx.close()
        browser.close()
    httpd.shutdown()
    report = {"tested": len(results), "errors": errors, "results": results}
    (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for row in results:
        print(f"{row['page']:46} {row['width']:4}px doc={row.get('documentWidth','?')} "
              f"hero={row.get('hero',{}).get('left','?') if row.get('hero') else '?'} "
              f"journal={row.get('journal',{}).get('left','?') if row.get('journal') else '?'} "
              f"pillar={row.get('pillar',{}).get('left','?') if row.get('pillar') else '?'}")
    if errors:
        print("UI_AUDIT_FAILURE: " + " | ".join(errors))
        raise SystemExit(1)
    print(f"UI_AUDIT_SUCCESS: {len(results)} viewport/page combinations; screenshots and JSON saved")

if __name__ == "__main__":
    main()
