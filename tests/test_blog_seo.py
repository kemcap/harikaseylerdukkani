"""SEO regression checks: crawlable links between blog clusters and pillar categories.

Run with: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dosemealti"
CATEGORIES = ("bijuteri", "kirtasiye", "oyuncak", "hediyelik-esya")
ARTICLES = ("dogum-gunu-hediyesi-nasil-secilir",
            "cocuklar-icin-oyuncak-secerken",
            "kucuk-butceyle-anlamli-hediyeler", "okul-kirtasiye-listesi",
            "gunluk-taki-kombinleri", "yeni-ev-hediyesi-fikirleri")
ANCHORS = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>', re.I)
SCRIPT = re.compile(r'<script\s+type="application/ld\+json"[^>]*>([\s\S]*?)</script>', re.I)


def local_links(section: str, page: Path):
    links = []
    for href in ANCHORS.findall(section):
        if href.startswith(("https:", "http:", "tel:", "mailto:", "#")):
            continue
        clean = urlsplit(href).path
        dest = (page.parent / clean).resolve()
        if not dest.is_relative_to(SITE.resolve()):
            raise AssertionError(f"{page} links outside local site: {href}")
        target = dest / "index.html" if clean.endswith("/") else dest
        if not target.is_file():
            raise AssertionError(f"Broken internal link from {page}: {href}")
        links.append((href, target))
    return links


class BlogSEOTests(unittest.TestCase):
    def test_articles_link_to_pillars_and_other_guides(self):
        for slug in ARTICLES:
            page = SITE / "blog" / slug / "index.html"
            html = page.read_text(encoding="utf-8")
            article = html.split('<article class="post-content">', 1)[1].split('</article>', 1)[0]
            related = html.split('<aside class="post-related', 1)[1].split('</aside>', 1)[0]
            links = local_links(article, page)
            self.assertTrue(any((SITE / cat / "index.html") == target
                                for _, target in links for cat in CATEGORIES), slug)
            self.assertTrue(any("/blog/" in str(target) and target != page
                                for _, target in links), slug)
            self.assertEqual(len(local_links(related, page)), 2, slug)
            self.assertIn('rel="canonical"', html, slug)
            self.assertIn('name="description"', html, slug)
            self.assertIn('class="post-intro"', article, slug)
            self.assertGreaterEqual(article.count('<h2 '), 5, slug)
            self.assertGreaterEqual(article.count('<summary>'), 5, slug)

            structured = [json.loads(block) for block in SCRIPT.findall(html)]
            article_types = [s.get("@type") for s in structured]
            self.assertIn("BlogPosting", article_types, slug)
            self.assertIn("BreadcrumbList", article_types, slug)
            breadcrumb = next(s for s in structured if s.get("@type") == "BreadcrumbList")
            self.assertEqual(len(breadcrumb["itemListElement"]), 3, slug)
            self.assertTrue(all(c["item"].startswith("https://harikaseylerdukkani.com/dosemealti/")
                                for c in breadcrumb["itemListElement"]), slug)

    def test_category_pillars_link_back_to_guides(self):
        for slug in CATEGORIES:
            page = SITE / slug / "index.html"
            html = page.read_text(encoding="utf-8")
            self.assertEqual(html.count('class="category-reading wrap"'), 1, slug)
            section = html.split('<section class="category-reading', 1)[1].split('</section>', 1)[0]
            links = local_links(section, page)
            blog_guides = [target for _, target in links if "/blog/" in str(target)]
            self.assertGreaterEqual(len(blog_guides), 2, slug)
            self.assertTrue(any(target.name == "index.html" and target.parent.name == "blog"
                                for target in blog_guides), slug)

    def test_blog_archive_links_to_all_four_pillars(self):
        page = SITE / "blog" / "index.html"
        html = page.read_text(encoding="utf-8")
        cluster = html.split('<section class="blog-pillar', 1)[1].split('</section>', 1)[0]
        links = local_links(cluster, page)
        targets = {target for _, target in links}
        for cat in CATEGORIES:
            self.assertIn(SITE / cat / "index.html", targets)
        structured = [json.loads(block) for block in SCRIPT.findall(html)]
        self.assertIn("BreadcrumbList", {s.get("@type") for s in structured})

    def test_no_duplicate_canonical_and_unique_h1(self):
        for slug in ARTICLES:
            page = SITE / "blog" / slug / "index.html"
            html = page.read_text(encoding="utf-8")
            self.assertEqual(html.count('rel="canonical"'), 1, slug)
            self.assertEqual(len(re.findall(r"<h1\b", html)), 1, slug)


if __name__ == "__main__":
    unittest.main()

