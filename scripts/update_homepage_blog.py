#!/usr/bin/env python3
"""Add Harika Fikirler to the *existing* Döşemealtı homepage without rebuilding it.

This stage runs AFTER update_homepage_navigation.py, against the downloaded live
index.html. It is deliberately idempotent and edits only header actions, one
footer navigation link, and an isolated style block.
"""
import argparse
import re
from pathlib import Path

BLOG_URL = "/dosemealti/blog/"
LINK = ('<a class="header-blog-link" href="' + BLOG_URL
        + '" aria-label="Harika Fikirler"><span class="blog-full">Harika Fikirler</span>'
        + '<span class="blog-short" aria-hidden="true">Blog</span></a>')
FOOTER_LINK = '<a class="footer-blog-link" href="' + BLOG_URL + '">Harika Fikirler</a>'
STYLE = """<style id="harika-fikirler-nav">
/* Local blog link sits next to the verified Instagram icon, separate from
   Dört dünya. The existing four-product navigation is untouched. */
.header .header-actions{gap:clamp(7px,1.2vw,16px)}
.header .header-blog-link{display:inline-flex;align-items:center;justify-content:center;min-height:40px;color:#132F25;font:700 clamp(.76rem,.9vw,.86rem)/1.3 var(--sans,Inter,Arial,sans-serif);white-space:nowrap;text-decoration:none;transition:color .2s ease}
.header .header-blog-link:hover,.header .header-blog-link:focus-visible{color:#a17d45}
.header .header-blog-link:focus-visible{outline:2px solid #b08b4b;outline-offset:4px}
.header .header-blog-link .blog-short{display:none}
@media(max-width:520px){
 .header .header-actions{gap:4px}
 .header .header-blog-link{min-height:34px;font-size:.78rem}
 .header .header-blog-link .blog-full{display:none}
 .header .header-blog-link .blog-short{display:inline}
}
@media(max-width:360px){
 .header{column-gap:3px!important}
 .header .header-blog-link{font-size:.73rem}
 .header .header-actions{gap:2px}
}
@media(prefers-reduced-motion:reduce){.header .header-blog-link{transition:none}}
</style>"""


def apply(source: str) -> str:
    if not all(token in source for token in ("<html", "</head>", "</body>", "</html>")):
        raise ValueError("Incomplete homepage: refusing update")
    if "harikaseylerdukkani.com/dosemealti/" not in source:
        raise ValueError("Not the expected Döşemealtı homepage")
    if '<nav class="story-dock"' not in source:
        raise ValueError("Homepage story layout missing: refusing update")

    header_match = re.search(r'<header\b[^>]*class="header"[^>]*>.*?</header>', source, re.S)
    footer_match = re.search(r'<footer\b[^>]*class="site-footer"[^>]*>.*?</footer>', source, re.S)
    if not header_match or not footer_match:
        raise ValueError("Expected homepage header/footer missing")
    header = header_match.group(0)
    footer = footer_match.group(0)
    if header.count('class="header-actions"') != 1 or header.count('class="header-instagram"') != 1:
        raise ValueError("Unexpected header controls")
    if header.count('class="desktop-nav"') != 1 or header.count('class="mobile-worlds-menu"') != 1:
        raise ValueError("Expected category navigation missing")
    if "Harika Fikirler" not in header:
        header = header.replace('<div class="header-actions">',
                                '<div class="header-actions">' + LINK, 1)
    if "Harika Fikirler" not in footer:
        if footer.count('<h3>Mağazamız</h3>') != 1:
            raise ValueError("Expected Mağazamız footer column missing")
        footer = footer.replace('<h3>Mağazamız</h3>',
                                '<h3>Mağazamız</h3>' + FOOTER_LINK, 1)

    # Replace from right to left to preserve original match offsets.
    edits = [(header_match.start(), header_match.end(), header),
             (footer_match.start(), footer_match.end(), footer)]
    for start, end, new in sorted(edits, reverse=True):
        source = source[:start] + new + source[end:]
    if 'id="harika-fikirler-nav"' in source:
        source, n = re.subn(r'<style id="harika-fikirler-nav">.*?</style>',
                            lambda _: STYLE, source, count=1, flags=re.S)
        if n != 1:
            raise ValueError("Failed to update existing blog link styles")
    else:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    assert source.count('class="header-blog-link"') == 1
    assert source.count('class="footer-blog-link"') == 1
    assert source.count('class="header-instagram"') == 1
    return source


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    args = p.parse_args()
    updated = apply(args.source.read_text(encoding="utf-8"))
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(updated, encoding="utf-8")
    print("Harika Fikirler: verified header link, mobile label and footer link.")
