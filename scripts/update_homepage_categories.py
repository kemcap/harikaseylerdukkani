#!/usr/bin/env python3
"""Safely link the 4 category pages from the existing Turhost homepage.

The current FTP homepage is the source of truth. Do not replace its design
with a prototype. Abort if the expected page structure is not present.
"""
import argparse
import re
from pathlib import Path

CATEGORIES = (
    ("bijuteri", "bijuteri", "Bijuteri & aksesuar sayfasını keşfet"),
    ("kirtasiye", "kirtasiye", "Kırtasiye sayfasını keşfet"),
    ("oyuncak", "oyuncak", "Oyuncak sayfasını keşfet"),
    ("hediye", "hediyelik-esya", "Hediyelik eşya sayfasını keşfet"),
)
STYLE = """<style id="category-link-styles">
/* Links to category landing pages, styled without changing existing CSS. */
.chapter-copy .category-details-link {
  display: inline-flex; align-items: center; justify-content: center;
  width: fit-content; max-width: 100%; gap: .75em;
  margin: 20px 0 10px; padding: 12px 20px;
  border: 1px solid currentColor; border-radius: 100px;
  color: inherit; background: transparent; text-align: center;
  font: 600 .91rem/1.35 var(--sans, Inter, sans-serif);
  text-decoration: none; transition: color .25s, background .25s, border-color .25s;
}
.chapter-copy .category-details-link:hover {
  background: #132F25; color: #faf6ed; border-color: #132F25;
}
.chapter-copy .category-details-link:focus-visible {
  outline: 2px solid #b08b4b; outline-offset: 4px;
}
@media (max-width: 480px) {
  .chapter-copy .category-details-link { padding: 12px 15px; font-size: .85rem; }
}
</style>"""

def patch_html(source):
    if not all(t in source for t in ("<html", "<head", "</head>", "</html>")):
        raise ValueError("Not a complete homepage; refusing deployment")
    if ("harikaseylerdukkani.com/dosemealti/" not in source
            or 'class="story-dock"' not in source):
        raise ValueError("Unexpected homepage version; refusing deployment")

    result = source
    inserted = 0
    for article_id, slug, label in CATEGORIES:
        chapter = re.search(
            rf'<article\b(?=[^>]*\bid\s*=\s*["\x27]{re.escape(article_id)}["\x27])[^>]*>',
            result, flags=re.I)
        if not chapter:
            raise ValueError(f"Missing chapter: {article_id}")
        end = result.find("</article>", chapter.end())
        if end < 0:
            raise ValueError(f"Unclosed chapter: {article_id}")
        section = result[chapter.end():end]
        url = f"/dosemealti/{slug}/"
        if 'class="category-details-link"' in section:
            if url not in section:
                raise ValueError(f"Wrong CTA destination: {article_id}")
            continue
        tags = re.search(r'<div\s+class\s*=\s*["\x27]chapter-tags["\x27]\s*>',
                         section, flags=re.I)
        if not tags:
            raise ValueError(f"No chapter tags: {article_id}")
        insert = (f'<a class="category-details-link" href="{url}">'
                  f'{label} <span aria-hidden="true">↗</span></a>\n')
        location = chapter.end() + tags.start()
        result = result[:location] + insert + result[location:]
        inserted += 1

    nav = re.search(
        r'<nav\b(?=[^>]*\baria-label\s*=\s*["\x27]Footer ürün dünyaları["\x27])[^>]*>.*?</nav>',
        result, flags=re.S | re.I)
    if not nav:
        raise ValueError("Missing footer category navigation")
    count = 0

    def replace_link(match):
        nonlocal count
        tag = match.group(0)
        ref = re.search(r'\bhref\s*=\s*(["\x27])(.*?)\1', tag, flags=re.S | re.I)
        if not ref:
            return tag
        old = ref.group(2)
        for article_id, slug, _ in CATEGORIES:
            new = f"/dosemealti/{slug}/"
            if old == new:
                count += 1
                return tag
            if old in (f"#{article_id}", f"/dosemealti/#{article_id}",
                       f"https://harikaseylerdukkani.com/dosemealti/#{article_id}"):
                count += 1
                return tag[:ref.start(2)] + new + tag[ref.end(2):]
        return tag

    footer = re.sub(r"<a\b[^>]*>", replace_link, nav.group(0), flags=re.I)
    if count != 4:
        raise ValueError(f"Expected exactly four footer links; got {count}")
    result = result[:nav.start()] + footer + result[nav.end():]
    if 'id="category-link-styles"' not in result:
        result = result.replace("</head>", STYLE + "\n</head>", 1)

    if result.count('class="category-details-link"') != 4:
        raise ValueError("Four category CTAs required")
    if not all(f"#{anchor}" in result for anchor, _, _ in CATEGORIES):
        raise ValueError("Original on-page chapter navigation must remain intact")
    if not all(f"/dosemealti/{slug}/" in result for _, slug, _ in CATEGORIES):
        raise ValueError("Missing landing-page destination")
    print(f"Validated 4 section CTAs and 4 footer links; {inserted} new CTAs.")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    original = args.source.read_text(encoding="utf-8")
    updated = patch_html(original)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(updated, encoding="utf-8")
    print(f"Original: {len(original)} chars, updated: {len(updated)} chars.")
