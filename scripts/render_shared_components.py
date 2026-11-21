#!/usr/bin/env python3
"""Build one shared Header/Footer into each Döşemealtı HTML page.

The canonical markup lives in dosemealti/components/{header,footer}.html.
Source HTML keeps a last-built fallback shell for direct GitHub Pages viewing;
only the rendered deployment copy is authoritative. All replacement happens
before FTPS, so bots and visitors get complete HTML without client-side fetches.

Examples:
    python3 scripts/render_shared_components.py --site-root deploy/dosemealti --min-pages 8
    python3 scripts/render_shared_components.py --site-root deploy/dosemealti --page deploy/dosemealti/index.html
    python3 scripts/render_shared_components.py --site-root deploy/dosemealti --min-pages 8 --check
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = REPO_ROOT / "dosemealti" / "components"
SHELL_HEADER = re.compile(r'<header\b[^>]*\bclass="header"[^>]*>[\s\S]*?</header>', re.I)
SHELL_FOOTER = re.compile(r'<footer\b[^>]*\bclass="site-footer"[^>]*>[\s\S]*?</footer>', re.I)
HOMEPAGE_MENU_STYLE = """<style id="main-category-header-menu">
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
BASE_MENU = re.compile(r'<style id="main-category-header-menu">.*?</style>', re.S)
GLOBAL_MENU_STYLE = """<style id="shared-navigation-style">
.header .mobile-worlds-panel .mobile-blog-link {
    margin-top: 6px;
    border-top: 1px solid #d7c5a4;
    color: #132f25;
    background: #f3eddf;
}
.header .mobile-worlds-panel .mobile-blog-link span {color: #93703b}
.header .mobile-worlds-panel .mobile-blog-link[aria-current="page"] {
    background: #132f25;
    color: #faf6ed;
}
.header .mobile-worlds-panel .mobile-blog-link:hover,
.header .mobile-worlds-panel .mobile-blog-link:focus-visible {text-decoration: underline}
@media (max-width: 1060px) {
    .header .header-actions .header-blog-link {display: none}
    .header .mobile-worlds-menu {position: static}
    .header .mobile-worlds-panel {
        top: calc(100% + 8px);
        inset-inline-end: clamp(12px, 4vw, 30px);
        max-height: calc(100dvh - 100px);
        overflow-y: auto;
    }
}
</style>
"""
SHARED_MENU = re.compile(r'<style id="shared-navigation-style">.*?</style>\s*', re.S)
CATEGORY_SLUGS = ("bijuteri", "kirtasiye", "oyuncak", "hediyelik-esya")
BLOG_SLUGS = (
    ("blog", "index.html"),
    ("blog", "dogum-gunu-hediyesi-nasil-secilir", "index.html"),
    ("blog", "cocuklar-icin-oyuncak-secerken", "index.html"),
    ("blog", "kucuk-butceyle-anlamli-hediyeler", "index.html"),
)


def template(path: Path, pattern: re.Pattern[str]) -> str:
    source = path.read_text(encoding="utf-8")
    match = pattern.search(source)
    if match is None or len(pattern.findall(source)) != 1:
        raise ValueError(f"Invalid shared component: {path}")
    return match.group(0)


def page_type(relative: Path) -> str:
    parts = relative.parts
    if parts == ("index.html",):
        return "home"
    if len(parts) == 2 and parts[1] == "index.html" and parts[0] in CATEGORY_SLUGS:
        return parts[0]
    if parts[0] == "blog" and parts[-1] == "index.html" and len(parts) in (2, 3):
        return "blog"
    raise ValueError(f"Unapproved target (no shell replacement): {relative}")



# Shared, server-rendered link previews and favicon for all public pages.
SOCIAL_ICON = '<link rel="icon" type="image/svg+xml" href="/dosemealti/assets/favicon.svg">'
SOCIAL_IMAGE_PREFIX = "https://harikaseylerdukkani.com/dosemealti/assets/"


def _social_pattern(name: str) -> re.Pattern[str]:
    return re.compile(
        r'<meta\b(?=[^>]*\b(?:property|name)\s*=\s*["\']'
        + re.escape(name) + r'["\'])[^>]*>', re.I
    )


def _read_social(source: str, name: str) -> str:
    head = source.split("</head>", 1)[0]
    matches = _social_pattern(name).findall(head)
    if len(matches) != 1:
        raise ValueError(f"Expected one {name} meta tag, found {len(matches)}")
    value = re.search(r'\bcontent\s*=\s*"([^"]*)"', matches[0], re.I)
    if not value:
        raise ValueError(f"Missing content value for {name}")
    return value.group(1)


def _set_social(source: str, name: str, value: str) -> str:
    pattern = _social_pattern(name)
    matches = list(pattern.finditer(source.split("</head>", 1)[0]))
    if len(matches) > 1:
        raise ValueError(f"Duplicate {name} meta tags")
    attr = "property" if name.startswith("og:") else "name"
    tag = f'<meta {attr}="{name}" content="{value}">'
    if matches:
        match = matches[0]
        return source[:match.start()] + tag + source[match.end():]
    return source.replace("</head>", tag + "\n</head>", 1)


def ensure_social_metadata(source: str, relative: Path) -> str:
    """Normalize native OG/Twitter metadata without touching visible page content.

    Requires each published page to have its own image, title, and description.
    Runs at build time, so WhatsApp/Facebook crawlers see tags in raw HTML.
    """
    page_type(relative)  # Whitelist only homepage, categories and blog.
    if source.count("</head>") != 1:
        raise ValueError(f"Invalid HTML head on {relative}")
    image = _read_social(source, "og:image")
    title = _read_social(source, "og:title")
    description = _read_social(source, "og:description")
    if not (image.startswith(SOCIAL_IMAGE_PREFIX) and image.endswith(".webp")):
        raise ValueError(f"Unapproved social preview image URL on {relative}: {image}")
    existing_alt = _social_pattern("og:image:alt").search(source.split("</head>", 1)[0])
    alt = _read_social(source, "og:image:alt") if existing_alt else title

    for name, value in (
        ("og:site_name", "Harika Şeyler Dükkanı"),
        ("og:image:secure_url", image),
        ("og:image:type", "image/webp"),
        ("og:image:alt", alt),
        ("twitter:card", "summary_large_image"),
        ("twitter:title", title),
        ("twitter:description", description),
        ("twitter:image", image),
        ("twitter:image:alt", alt),
    ):
        source = _set_social(source, name, value)

    head = source.split("</head>", 1)[0]
    icons = list(re.finditer(
        r'<link\b(?=[^>]*\brel\s*=\s*["\']icon["\'])[^>]*>', head, re.I
    ))
    if len(icons) > 1:
        raise ValueError(f"Duplicate favicon links on {relative}")
    if icons:
        source = source[:icons[0].start()] + SOCIAL_ICON + source[icons[0].end():]
    else:
        source = source.replace("</head>", SOCIAL_ICON + "\n</head>", 1)
    return source

def render(source: str, relative: Path, header_template: str, footer_template: str) -> str:
    kind = page_type(relative)
    if not all(token in source for token in ("<html", "</head>", "</body>", "</html>")):
        raise ValueError(f"Incomplete HTML: {relative}")
    if kind == "home" and ('class="story-dock"' not in source
                           or 'harikaseylerdukkani.com/dosemealti/' not in source):
        raise ValueError(f"Homepage identity check failed: {relative}")
    if kind in CATEGORY_SLUGS and 'category-seo-h1' not in source:
        raise ValueError(f"Category identity check failed: {relative}")
    if kind == "blog" and 'class="blog-page"' not in source:
        raise ValueError(f"Blog identity check failed: {relative}")
    headers = list(SHELL_HEADER.finditer(source))
    footers = list(SHELL_FOOTER.finditer(source))
    if len(headers) != 1 or len(footers) != 1 or headers[0].end() > footers[0].start():
        raise ValueError(f"Expected one complete header and footer: {relative}")

    header = header_template
    # Active state is applied on both category links (desktop and mobile) or
    # on the dedicated Harika Fikirler link, never on another page.
    if kind in CATEGORY_SLUGS:
        dest = f'href="/dosemealti/{kind}/"'
        if header.count(dest) != 2:
            raise ValueError(f"Missing desktop/mobile destination for {kind}")
        header = header.replace(dest, dest + ' aria-current="page"')
    elif kind == "blog":
        for link_class in ("header-blog-link", "mobile-blog-link"):
            fragment = f'<a class="{link_class}"'
            if header.count(fragment) != 1:
                raise ValueError(f"Missing blog navigation link: {link_class}")
            header = header.replace(fragment, fragment + ' aria-current="page"', 1)

    if (header.count('class="desktop-nav"') != 1
        or header.count('class="mobile-worlds-menu"') != 1
        or header.count('class="header-instagram"') != 1
        or header.count('class="header-blog-link"') != 1
        or header.count('class="brand-logo"') != 1
        or footer_template.count('class="footer-blog-link"') != 1):
        raise ValueError("Shared shell is missing required elements")
    if header.count('href="/dosemealti/') != 11:
        # 4 desktop + 4 mobile category destinations + brand + 2 blog links
        raise ValueError("Unexpected navigation count in shared header")

    # Preserve every byte of page-specific content, metadata and JavaScript.
    output = (source[:headers[0].start()] + header
              + source[headers[0].end():footers[0].start()]
              + footer_template + source[footers[0].end():])

    if kind in ("home", "blog"):
        if BASE_MENU.search(output):
            output = BASE_MENU.sub(lambda _: HOMEPAGE_MENU_STYLE, output, count=1)
        else:
            output = output.replace("</head>", HOMEPAGE_MENU_STYLE + "\n</head>", 1)
    output = ensure_social_metadata(output, relative)
    output = SHARED_MENU.sub("", output).replace("</head>", GLOBAL_MENU_STYLE + "</head>", 1)

    if (len(SHELL_HEADER.findall(output)) != 1
        or len(SHELL_FOOTER.findall(output)) != 1
        or output.count('class="header-blog-link"') != 1
        or output.count('class="footer-blog-link"') != 1):
        raise ValueError(f"Shared shell verification failed: {relative}")
    return output


def target_paths(root: Path, explicit: Path | None) -> list[Path]:
    if explicit is not None:
        path = explicit.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("Explicit page must exist below --site-root")
        return [path]
    targets = sorted(p for p in root.rglob("index.html") if p.is_file())
    # Every staged page is validated. New blog articles are discovered
    # automatically, with no need to update a list of slugs.
    for path in targets:
        page_type(path.relative_to(root))
    return targets


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--site-root", required=True, type=Path)
    cli.add_argument("--page", type=Path,
                     help="Only render this exact page (for the protected homepage workflow)")
    cli.add_argument("--expect-pages", type=int,
                     help="Abort if the count is not exactly this number")
    cli.add_argument("--min-pages", type=int,
                     help="At least this many pages must be present (supports new posts)")
    cli.add_argument("--check", action="store_true",
                     help="Fail when checked-in/deployed markup differs; do not write")
    cli.add_argument("--dry-run", action="store_true",
                     help="Validate rendering without writing")
    args = cli.parse_args()
    root = args.site_root.resolve()
    if not root.is_dir():
        cli.error(f"Site directory does not exist: {root}")

    header = template(COMPONENT_ROOT / "header.html", SHELL_HEADER)
    footer = template(COMPONENT_ROOT / "footer.html", SHELL_FOOTER)
    targets = target_paths(root, args.page)
    if not targets:
        cli.error("No pages selected for rendering")
    if args.expect_pages is not None and len(targets) != args.expect_pages:
        cli.error(f"Expected {args.expect_pages} pages; found {len(targets)}")
    if args.min_pages is not None and len(targets) < args.min_pages:
        cli.error(f"Expected at least {args.min_pages} pages; found {len(targets)}")
    if args.page is None:
        required = {Path(slug) / "index.html" for slug in CATEGORY_SLUGS}
        required.add(Path("blog/index.html"))
        present = {p.relative_to(root) for p in targets}
        if not required.issubset(present):
            cli.error(f"Missing mandatory category/blog archive pages: {required - present}")

    rendered: list[tuple[Path, str, str]] = []
    for path in targets:
        original = path.read_text(encoding="utf-8")
        result = render(original, path.relative_to(root), header, footer)
        rendered.append((path, original, result))

    for path, original, result in rendered:
        if args.check and original != result:
            raise SystemExit(f"Shared shell drift: {path}")
        if not args.check and not args.dry_run and original != result:
            path.write_text(result, encoding="utf-8")
        state = "current" if original == result else ("validated" if args.dry_run else "rendered")
        print(f"{state}: {path.relative_to(root)}")
    print(f"Harika shared components: {len(rendered)} pages validated; no client-side loading.")


if __name__ == "__main__":
    main()
