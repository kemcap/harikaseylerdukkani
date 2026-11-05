#!/usr/bin/env python3
"""Replace only the header navigation of the existing Turhost homepage.

Preserves all other content/animations and supports repeated idempotent runs.
Desktop shows four direct category links; mobile uses the "Dört dünya"
disclosure with only four category links.
"""
import argparse
import re
from pathlib import Path

CATEGORIES = (
    ("bijuteri", "Bijuteri & Aksesuar"),
    ("kirtasiye", "Kırtasiye"),
    ("oyuncak", "Oyuncak"),
    ("hediyelik-esya", "Hediyelik Eşya"),
)

STYLE = """<style id="main-category-header-menu">
/* Harika unified primary navigation: 4 links on desktop; dropdown on mobile. */
.header .desktop-nav{margin-left:auto;justify-content:flex-end;gap:clamp(14px,2vw,38px)}
.header .desktop-nav a{font-size:clamp(.77rem,.95vw,.89rem);font-weight:600;letter-spacing:.012em}
.mobile-worlds-menu{display:none}
@media(min-width:761px){.header .desktop-nav{display:flex!important}}
@media(max-width:760px){
 .header .desktop-nav{display:none!important}
 .header .mobile-worlds-menu{display:block;position:relative;margin-left:auto;color:inherit;z-index:90}
 .header .mobile-worlds-menu summary{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:40px;padding:6px 12px;list-style:none;cursor:pointer;white-space:nowrap;font-size:.9rem;font-weight:700;letter-spacing:.01em;border:1px solid currentColor;border-radius:4px}
 .header .mobile-worlds-menu summary::-webkit-details-marker{display:none}
 .header .mobile-worlds-menu summary::marker{content:""}
 .header .mobile-worlds-menu summary:focus-visible{outline:2px solid #c2a268;outline-offset:4px}
 .header .mobile-worlds-menu .mobile-chevron{display:inline-block;font-size:1.2rem;line-height:1;transition:transform .2s ease}
 .header .mobile-worlds-menu[open] .mobile-chevron{transform:rotate(180deg)}
 .header .mobile-worlds-panel{display:flex;flex-direction:column;position:absolute;right:0;top:calc(100% + 10px);width:min(330px,calc(100vw - 28px));padding:10px;background:#faf6ed;color:#132F25;border:1px solid #d7c5a4;border-radius:9px;box-shadow:0 18px 46px rgba(9,29,21,.26);z-index:100}
 .header .mobile-worlds-panel a{display:flex;align-items:center;gap:14px;padding:14px 12px;min-height:48px;font-size:.93rem;font-weight:600;border-radius:5px;text-decoration:none}
 .header .mobile-worlds-panel a+a{border-top:1px solid rgba(19,47,37,.10)}
 .header .mobile-worlds-panel a:hover,.header .mobile-worlds-panel a:focus-visible{background:#e9ebe1}
 .header .mobile-worlds-panel .world-index{font-size:.72rem;letter-spacing:.09em;color:#a58852;font-weight:700}
 .story-dock{display:none!important}
}
@media(prefers-reduced-motion:reduce){.mobile-worlds-menu .mobile-chevron{transition:none!important}}
</style>"""

BEHAVIOR = """<script id="main-category-header-behavior">
(() => {
  const menu = document.querySelector('.mobile-worlds-menu');
  if (!menu) return;
  document.addEventListener('pointerdown', event => {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary')?.focus();
    }
  });
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => { menu.open = false; });
  });
  window.matchMedia('(min-width: 761px)').addEventListener?.('change', event => {
    if (event.matches) menu.open = false;
  });
})();
</script>"""

def apply(source):
    if not all(x in source for x in ("<html", "</head>", "</body>", "</html>")):
        raise ValueError("Not a complete HTML page: upload blocked")
    if "harikaseylerdukkani.com/dosemealti/" not in source:
        raise ValueError("Unexpected canonical: upload blocked")
    if '<nav class="story-dock"' not in source:
        raise ValueError("Unrecognized homepage: upload blocked")
    header_match = re.search(r'<header\b[^>]*class="header"[^>]*>.*?</header>', source, re.S)
    if header_match is None:
        raise ValueError("Existing header not found: upload blocked")
    old_header = header_match.group(0)
    brand_match = re.search(r'<a class="brand"[^>]*>.*?</a>', old_header, re.S)
    if not brand_match:
        raise ValueError("Original brand/logo link not found: upload blocked")
    brand = brand_match.group(0)
    desktop = "".join(
        f'<a href="/dosemealti/{slug}/">{label}</a>'
        for slug, label in CATEGORIES
    )
    mobile = "".join(
        f'<a href="/dosemealti/{slug}/"><span class="world-index">{idx:02d}</span>{label}</a>'
        for idx, (slug, label) in enumerate(CATEGORIES, 1)
    )
    new_header = (
        '<header class="header">'
        + brand
        + '<nav class="desktop-nav" aria-label="Ürün kategorileri">'
        + desktop + '</nav>'
        + '<details class="mobile-worlds-menu"><summary>Dört dünya '
        + '<span class="mobile-chevron" aria-hidden="true">⌄</span></summary>'
        + '<nav class="mobile-worlds-panel" aria-label="Ürün kategorileri">'
        + mobile + '</nav></details></header>'
    )
    html = source[:header_match.start()] + new_header + source[header_match.end():]
    if 'id="main-category-header-menu"' in html:
        html, count = re.subn(r'<style id="main-category-header-menu">.*?</style>',
                              lambda _: STYLE, html, count=1, flags=re.S)
        if count != 1:
            raise ValueError("Cannot replace existing menu CSS")
    else:
        html = html.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="main-category-header-behavior"' in html:
        html, count = re.subn(r'<script id="main-category-header-behavior">.*?</script>',
                              lambda _: BEHAVIOR, html, count=1, flags=re.S)
        if count != 1:
            raise ValueError("Cannot replace existing menu JS")
    else:
        html = html.replace("</body>", BEHAVIOR + "\n</body>", 1)

    match = re.search(r'<header\b[^>]*class="header"[^>]*>.*?</header>', html, re.S)
    result_header = match.group(0)
    assert result_header.count('<nav class="desktop-nav"') == 1
    assert result_header.count('<details class="mobile-worlds-menu"') == 1
    assert result_header.count('<a href="/dosemealti/') == 8
    assert "Yakından bak" not in result_header
    assert "Sık sorulanlar" not in result_header
    assert "Döşemealtı Ana Sayfa" not in result_header
    assert "Online-Mağazamız" not in result_header
    assert 'href="#dunyalar"' not in result_header
    for slug, _ in CATEGORIES:
        assert result_header.count(f'href="/dosemealti/{slug}/"') == 2
    print("Validated: 4 desktop links, 4 mobile links, preserved brand and story.")
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    result = apply(args.source.read_text(encoding="utf-8"))
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(result, encoding="utf-8")
