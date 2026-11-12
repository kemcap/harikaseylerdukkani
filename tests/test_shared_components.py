"""Regression tests for the global Döşemealtı header/footer build stage.

The live homepage is downloaded over FTPS and patched separately; tests use
its versioned design source to guarantee that the shared renderer preserves
story interactions and never removes page-specific content.
"""
from __future__ import annotations

from pathlib import Path
import unittest

from scripts import render_shared_components as shared

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    Path("index.html"): ROOT / "sticky-discovery" / "index.html",
    **{Path(slug) / "index.html": ROOT / "dosemealti" / slug / "index.html"
       for slug in shared.CATEGORY_SLUGS},
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

    def test_nine_pages_have_one_identical_shell(self):
        self.assertEqual(len(SAMPLES), 9)  # homepage + 4 categories + 4 blog pages
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
                self.assertIn("/dosemealti/assets/harika-seyler-dukkani-logo.webp", result)
                before = shared.SHELL_FOOTER.sub(
                    "<SHARED_FOOTER>", shared.SHELL_HEADER.sub("<SHARED_HEADER>", source))
                after = shared.SHELL_FOOTER.sub(
                    "<SHARED_FOOTER>", shared.SHELL_HEADER.sub("<SHARED_HEADER>", result))
                self.assertEqual(before, after, "Page content outside shell must not change")
                rendered_header = shared.SHELL_HEADER.search(result).group(0)
                if relative.parts[0] in shared.CATEGORY_SLUGS:
                    self.assertEqual(rendered_header.count('aria-current="page"'), 2)
                elif relative.parts[0] == "blog":
                    self.assertEqual(rendered_header.count('aria-current="page"'), 1)
                else:
                    self.assertNotIn('aria-current="page"', rendered_header)

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

    def test_all_eight_deploy_subpages_are_whitelisted(self):
        paths = [Path(slug) / "index.html" for slug in shared.CATEGORY_SLUGS]
        paths.extend(Path(*parts) for parts in shared.BLOG_SLUGS)
        self.assertEqual(len(paths), 8)
        for path in paths:
            self.assertIn(shared.page_type(path),
                          (*shared.CATEGORY_SLUGS, "blog"))


if __name__ == "__main__":
    unittest.main()
