#!/usr/bin/env python3
"""Update the SEO copy and guide links on the existing Döşemealtı homepage."""
import argparse
from html import escape
import json
from pathlib import Path
import re

HOME = "https://harikaseylerdukkani.com/dosemealti/"
TITLE = "Harika Şeyler Dükkanı | Döşemealtı, Antalya"
DESCRIPTION = ("Antalya Döşemealtı Yeniköy’de takı, kırtasiye, oyuncak ve hediyelik eşya. "
               "Harika Şeyler Dükkanı’nın adresini, çalışma saatlerini ve yol tarifini bul.")
GUIDES = {
    "bijuteri": ("gunluk-taki-kombinleri", "Günlük takı kombinleri rehberi"),
    "kirtasiye": ("okul-kirtasiye-listesi", "Okul kırtasiye alışveriş listesi"),
    "oyuncak": ("cocuklar-icin-oyuncak-secerken", "Yaşa uygun oyuncak seçme rehberi"),
    "hediye": ("yeni-ev-hediyesi-fikirleri", "Yeni ev hediyesi fikirleri"),
}


def replace_single(source, pattern, replacement):
    result, count = re.subn(pattern, replacement, source, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one homepage match for {pattern!r}, found {count}")
    return result


def apply(source):
    if f'<link rel="canonical" href="{HOME}"' not in source:
        raise ValueError("The input must be the live Döşemealtı homepage")
    source = replace_single(source, r"<title>[^<]*</title>", f"<title>{escape(TITLE)}</title>")
    for attribute, value in (
        ('name="description"', DESCRIPTION),
        ('property="og:title"', TITLE),
        ('property="og:description"', DESCRIPTION),
        ('name="twitter:title"', TITLE),
        ('name="twitter:description"', DESCRIPTION),
    ):
        source = replace_single(source, rf'(<meta {attribute} content=")[^"]*(")',
                                lambda match: match[1] + escape(value, quote=True) + match[2])

    def update_webpage(match):
        data = json.loads(match[2])
        for node in data.get("@graph", []):
            if node.get("@type") == "WebPage" and node.get("url") == HOME:
                node.update(name=TITLE, description=DESCRIPTION)
                return match[1] + json.dumps(data, ensure_ascii=False) + match[3]
        return match[0]

    source = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',
                    update_webpage, source, flags=re.S)

    for chapter, (slug, label) in GUIDES.items():
        guide = (f'<p class="chapter-guide">Harika Fikirler · <a href="/dosemealti/blog/{slug}/" '
                 f'style="text-decoration:underline;text-underline-offset:.18em">{label}</a></p>')
        pattern = (rf'(<article class="chapter [^"]+" id="{chapter}"[^>]*>.*?'
                   r'<div class="category-description">.*?)(?:<p class="chapter-guide">.*?</p>)?(</div>)')
        source = replace_single(source, pattern, lambda match: match[1] + guide + match[2])
    return source


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("page", type=Path)
    args = parser.parse_args()
    source = args.page.read_text(encoding="utf-8")
    updated = apply(source)
    if apply(updated) != updated:
        raise ValueError("Homepage SEO update must be idempotent")
    args.page.write_text(updated, encoding="utf-8")
