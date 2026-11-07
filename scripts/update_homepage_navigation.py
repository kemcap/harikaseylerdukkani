#!/usr/bin/env python3
"""Update the header navigation and hero accents of the existing Turhost homepage.

Preserves the homepage structure and supports repeated idempotent runs.
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

ACTIONS = """<div class="header-actions"><a class="header-instagram" href="https://www.instagram.com/_harikaseylerdukkani/" target="_blank" rel="noopener noreferrer" aria-label="Harika Şeyler Dükkanı – Instagram"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a></div>"""

STYLE = """<style id="main-category-header-menu">
/* Harika unified primary navigation: 4 links on desktop; dropdown on mobile. */
.header .desktop-nav{margin-left:auto;justify-content:flex-end;gap:clamp(14px,2vw,38px)}
.header .desktop-nav a{font-size:clamp(.77rem,.95vw,.89rem);font-weight:600;letter-spacing:.012em}
.mobile-worlds-menu{display:none}
@media(min-width:1061px){.header .desktop-nav{display:flex!important}}
@media(max-width:1060px){
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
}
@media(max-width:760px){.story-dock{display:none!important}}
@media(prefers-reduced-motion:reduce){.mobile-worlds-menu .mobile-chevron{transition:none!important}}

/* Center category menu; restore verified Instagram social link to the right. */
@media(min-width:1061px){
 .header{display:grid;grid-template-columns:minmax(120px,1fr) max-content minmax(120px,1fr);align-items:center;gap:16px}
 .header .brand{grid-column:1;justify-self:start}
 .header .desktop-nav{grid-column:2;justify-self:center;margin:0;justify-content:center;gap:clamp(15px,1.65vw,32px)}
 .header .header-actions{grid-column:3;justify-self:end;display:flex;align-items:center}
 .header .mobile-worlds-menu{display:none!important}
}
@media(max-width:1060px){
 .header{display:grid;grid-template-columns:minmax(80px,1fr) auto auto;align-items:center;gap:clamp(6px,2vw,15px)}
 .header .brand{grid-column:1;justify-self:start;min-width:0}
 .header .desktop-nav{display:none!important}
 .header .mobile-worlds-menu{display:block!important;grid-column:2;margin:0;justify-self:end}
 .header .header-actions{display:flex;grid-column:3;justify-self:end;align-items:center;margin:0}
 .header .header-instagram{display:inline-flex;width:40px;min-width:40px;min-height:40px;align-items:center;justify-content:center}
 .header .mobile-worlds-panel{right:0}
}
@media(max-width:420px){
 .header{gap:6px}
 .header .header-instagram{width:34px;min-width:34px;min-height:36px}
 .header .header-instagram svg{width:24px;height:24px}
 .header .mobile-worlds-menu summary{gap:6px;padding:6px 9px;font-size:.79rem}
}


/* Slim evergreen Dört dünya trigger, with vertical breathing room in the compact header. */
@media(max-width:1060px){
 .header .mobile-worlds-menu summary{
   gap:7px;min-height:34px;padding:7px 11px;
   border:0;border-radius:5px;box-shadow:none;
   background:#132F25;color:#fff;
   font-size:.82rem;font-weight:650;line-height:1.2;
   transition:background-color .2s ease;
 }
 .header .mobile-worlds-menu summary:hover{background:#1b4032}
 .header .mobile-worlds-menu summary:focus-visible{outline:2px solid #c2a268;outline-offset:3px}
 .header .mobile-worlds-menu .mobile-chevron{color:inherit;font-size:1rem}
 .header-compact .header .mobile-worlds-menu summary{
   min-height:28px;padding:4px 9px;font-size:.77rem;
 }
 .header-compact .header .header-instagram{min-height:28px}
}
@media(max-width:420px){
 .header .mobile-worlds-menu summary{padding:6px 9px;gap:5px}
 .header-compact .header .mobile-worlds-menu summary{padding:4px 8px;min-height:28px}
}
@media(prefers-reduced-motion:reduce){.header .mobile-worlds-menu summary{transition:none}}

.hero-stamp span{
  display:inline-block;color:#93703b;
  transform:rotate(var(--home-star-angle,0deg));
}
@media(prefers-reduced-motion:reduce){.hero-stamp span{transform:none}}

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
  window.matchMedia('(min-width: 1061px)').addEventListener?.('change', event => {
    if (event.matches) menu.open = false;
  });
})();
(() => {
  const star = document.querySelector('.hero-stamp span');
  if (!star) return;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  const update = () => {
    frame = 0;
    const angle = motion.matches ? 0 : Math.min(Math.max(window.scrollY, 0), window.innerHeight) * .105;
    star.style.setProperty('--home-star-angle', angle + 'deg');
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('pageshow', schedule);
  motion.addEventListener?.('change', schedule);
  schedule();
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
        + mobile + '</nav></details>' + ACTIONS + '</header>'
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

    # CSS hides these photos on narrow screens. Lazy loading avoids fetching
    # them there while leaving the main hero image high-priority.
    html = re.sub(r'(<figure class="hero-float float-(?:one|two)"[^>]*><img )(?!loading=)',
                  r'\1loading="lazy" ', html)
    html = html.replace("Bir dükkan, dört dünya.", "Bir dükkân, dört dünya.")

    match = re.search(r'<header\b[^>]*class="header"[^>]*>.*?</header>', html, re.S)
    result_header = match.group(0)
    assert result_header.count('<nav class="desktop-nav"') == 1
    assert result_header.count('<details class="mobile-worlds-menu"') == 1
    assert result_header.count('<a href="/dosemealti/') == 8
    assert result_header.count('class="header-instagram"') == 1
    assert result_header.count('https://www.instagram.com/_harikaseylerdukkani/') == 1
    assert "Yakından bak" not in result_header
    assert "Sık sorulanlar" not in result_header
    assert "Döşemealtı Ana Sayfa" not in result_header
    assert "Online-Mağazamız" not in result_header
    assert 'href="#dunyalar"' not in result_header
    for slug, _ in CATEGORIES:
        assert result_header.count(f'href="/dosemealti/{slug}/"') == 2
    print("Validated: 4 centered desktop links, 4 mobile links, Instagram right; brand and story preserved.")
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    result = apply(args.source.read_text(encoding="utf-8"))
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(result, encoding="utf-8")
