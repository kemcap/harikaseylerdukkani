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
        fragment = '<a class="header-blog-link"'
        if header.count(fragment) != 1:
            raise ValueError("Missing one Harika Fikirler top navigation link")
        header = header.replace(fragment, fragment + ' aria-current="page"', 1)

    if (header.count('class="desktop-nav"') != 1
        or header.count('class="mobile-worlds-menu"') != 1
        or header.count('class="header-instagram"') != 1
        or header.count('class="header-blog-link"') != 1
        or header.count('class="brand-logo"') != 1
        or footer_template.count('class="footer-blog-link"') != 1):
        raise ValueError("Shared shell is missing required elements")
    if header.count('href="/dosemealti/') != 10:
        # 4 desktop + 4 mobile category destinations + brand + blog
        raise ValueError("Unexpected navigation count in shared header")

    # Preserve every byte of page-specific content, metadata and JavaScript.
    output = (source[:headers[0].start()] + header
              + source[headers[0].end():footers[0].start()]
              + footer_template + source[footers[0].end():])

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
