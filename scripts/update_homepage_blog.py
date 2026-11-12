#!/usr/bin/env python3
"""Preserve homepage blog link styling before global shell rendering.

The component templates in dosemealti/components/ define the canonical
header and footer. This step only prepares the matching CSS on the downloaded
live homepage; scripts/render_shared_components.py inserts shared HTML.
"""
import argparse
import re
from pathlib import Path

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

    if not re.search(r'<header\b[^>]*class="header"[^>]*>.*?</header>', source, re.S):
        raise ValueError("Original homepage header missing")
    if not re.search(r'<footer\b[^>]*class="site-footer"[^>]*>.*?</footer>', source, re.S):
        raise ValueError("Original homepage footer missing")
    if 'id="harika-fikirler-nav"' in source:
        source, n = re.subn(r'<style id="harika-fikirler-nav">.*?</style>',
                            lambda _: STYLE, source, count=1, flags=re.S)
        if n != 1:
            raise ValueError("Failed to update existing blog link styles")
    else:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    print("Blog navigation CSS prepared; shared renderer inserts the single link.")
    return source


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    args = p.parse_args()
    updated = apply(args.source.read_text(encoding="utf-8"))
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(updated, encoding="utf-8")
    print("Harika Fikirler: shared navigation styles prepared (markup via component renderer).")
