"""Regression tests for the global Döşemealtı header/footer build stage.

The live homepage is downloaded over FTPS and patched separately; tests use
its versioned design source to guarantee that the shared renderer preserves
story interactions and never removes page-specific content.
"""
from __future__ import annotations

from pathlib import Path
import re
import unittest

from scripts import render_shared_components as shared

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    Path("index.html"): ROOT / "sticky-discovery" / "index.html",
    **{Path(slug) / "index.html": ROOT / "dosemealti" / slug / "index.html"
       for slug in (*shared.CATEGORY_SLUGS, shared.ATELIER_SLUG)},
    **{Path(*parts): ROOT / "dosemealti" / Path(*parts)
       for parts in shared.BLOG_SLUGS},
}


class SharedComponentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.header = shared.template(
            shared.COMPONENT_ROOT / "header.html", shared.SHELL_HEADER)
        cls.footer = shared.template(
            shared.COMPONENT_ROOT / "footer.html", shared.SHELL_FOOTER)

    def test_public_page_types_have_one_identical_shell(self):
        self.assertEqual(len(SAMPLES), 10)  # homepage + 4 categories + atelier + 4 blog pages
        for relative, path in SAMPLES.items():
            with self.subTest(page=str(relative)):
                source = path.read_text(encoding="utf-8")
                result = shared.render(source, relative, self.header, self.footer)
                self.assertEqual(
                    result, shared.render(result, relative, self.header, self.footer),
                    "Re-rendering must be idempotent")
                self.assertEqual(result.count('class="header-blog-link"'), 1)
                self.assertEqual(result.count('class="footer-blog-link"'), 1)
                self.assertEqual(result.count('class="header-instagram"'), 1)
                self.assertEqual(result.count('class="header-atelier-link"'), 1)
                self.assertEqual(result.count('class="mobile-atelier-link"'), 1)
                self.assertEqual(result.count('class="home-sound-atelier"'), int(relative == Path("index.html")))
                self.assertIn("/dosemealti/assets/harika-seyler-dukkani-logo.webp", result)
                def page_content(html):
                    html = shared.SHARED_MENU.sub("", html)
                    html = shared.BASE_MENU.sub("", html)
                    html = shared.HOME_ATELIER.sub("", html)
                    html = shared.SHELL_HEADER.sub("<SHARED_HEADER>", html)
                    return shared.SHELL_FOOTER.sub("<SHARED_FOOTER>", html)

                self.assertEqual(page_content(shared.ensure_social_metadata(source, relative)), page_content(result))
                rendered_header = shared.SHELL_HEADER.search(result).group(0)
                if relative.parts[0] in (*shared.CATEGORY_SLUGS, shared.ATELIER_SLUG):
                    self.assertEqual(rendered_header.count('aria-current="page"'), 2)
                elif relative.parts[0] == "blog":
                    self.assertEqual(rendered_header.count('aria-current="page"'), 2)
                    self.assertIn('class="mobile-blog-link" aria-current="page"', rendered_header)
                else:
                    self.assertNotIn('aria-current="page"', rendered_header)

    def test_all_public_pages_have_valid_social_previews_and_shared_favicon(self):
        public_root = ROOT / "dosemealti"
        pages = sorted((public_root / "blog").rglob("index.html"))
        pages.extend(public_root / slug / "index.html"
                     for slug in (*shared.CATEGORY_SLUGS, shared.ATELIER_SLUG))
        pages.append(ROOT / "sticky-discovery" / "index.html")
        self.assertEqual(len(pages), 16)  # 9 articles + blog index + 4 categories + homepage + atelier
        for path in pages:
            relative = (Path("index.html") if path.parent.name == "sticky-discovery"
                        else path.relative_to(public_root))
            with self.subTest(page=str(relative)):
                source = path.read_text(encoding="utf-8")
                updated = shared.ensure_social_metadata(source, relative)
                self.assertEqual(updated, shared.ensure_social_metadata(updated, relative))
                self.assertIn(shared.SOCIAL_ICON, updated)
                self.assertEqual(updated.count('name="twitter:image"'), 1)
                self.assertEqual(updated.count('name="twitter:card"'), 1)
                image = shared._read_social(updated, "og:image")
                self.assertEqual(image, shared._read_social(updated, "twitter:image"))
                file_name = image.removeprefix(
                    "https://harikaseylerdukkani.com/dosemealti/"
                )
                self.assertTrue((public_root / file_name).is_file(), image)
        self.assertTrue((public_root / "assets/favicon.svg").is_file())

    def test_fails_on_unknown_or_incomplete_page(self):
        with self.assertRaises(ValueError):
            shared.page_type(Path("unrelated/index.html"))
        source = (ROOT / "dosemealti" / "bijuteri" / "index.html").read_text(encoding="utf-8")
        with self.assertRaises(ValueError):
            shared.render(source.replace("<footer", "<unused-footer", 1),
                          Path("bijuteri/index.html"), self.header, self.footer)
        with self.assertRaises(ValueError):
            shared.render(source.replace('category-seo-h1', 'unknown-title'),
                          Path("bijuteri/index.html"), self.header, self.footer)

    def test_deploy_subpages_are_whitelisted(self):
        public_sections = (*shared.CATEGORY_SLUGS, shared.ATELIER_SLUG)
        paths = [Path(slug) / "index.html" for slug in public_sections]
        paths.extend(Path(*parts) for parts in shared.BLOG_SLUGS)
        self.assertEqual(len(paths), 9)
        self.assertEqual(shared.page_type(Path("blog/yeni-yazi/index.html")), "blog")
        for path in paths:
            self.assertIn(shared.page_type(path),
                          (*public_sections, "blog"))


if __name__ == "__main__":
    unittest.main()
