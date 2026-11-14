#!/usr/bin/env python3
"""Preserve homepage navigation behavior and styling before global shell rendering.

The header and footer markup is exclusively authored in dosemealti/components/.
This script adds the existing responsive navigation CSS and interactions to the
downloaded live homepage, while the final build stage injects canonical markup.
"""
import argparse
import re
from pathlib import Path

from render_shared_components import HOMEPAGE_MENU_STYLE as STYLE

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

def apply(source: str) -> str:
    if not all(x in source for x in ("<html", "</head>", "</body>", "</html>")):
        raise ValueError("Not a complete homepage: upload blocked")
    if "harikaseylerdukkani.com/dosemealti/" not in source:
        raise ValueError("Unexpected canonical: upload blocked")
    if '<nav class="story-dock"' not in source:
        raise ValueError("Unrecognized homepage: upload blocked")
    original_header = re.search(
        r'<header\b[^>]*class="header"[^>]*>.*?</header>', source, flags=re.S)
    if original_header is None or 'class="brand"' not in original_header.group(0):
        raise ValueError("Original homepage header/brand not found")
    if not re.search(r'<footer\b[^>]*class="site-footer"[^>]*>.*?</footer>',
                     source, flags=re.S):
        raise ValueError("Original homepage footer not found")

    html = source
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

    # Preserve the live story, add lazy loading to decorative floating photos.
    html = re.sub(r'(<figure class="hero-float float-(?:one|two)"[^>]*><img )(?!loading=)',
                  r'\1loading="lazy" ', html)
    html = html.replace("Bir dükkan, dört dünya.", "Bir dükkân, dört dünya.")
    print("Homepage nav CSS/behavior ready; global renderer supplies all markup.")
    return html


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    result = apply(args.source.read_text(encoding="utf-8"))
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(result, encoding="utf-8")
