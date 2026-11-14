#!/usr/bin/env python3
"""Build the public Döşemealtı sitemap from staged canonical pages."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree as XML

BASE = "https://harikaseylerdukkani.com/dosemealti/"
SITEMAP = "http://www.sitemaps.org/schemas/sitemap/0.9"
IMAGE = "http://www.google.com/schemas/sitemap-image/1.1"
HOME_IMAGES = (
    "bijuteri-taki-aksesuarlari.webp", "defter-kalem-kirtasiye-urunleri.webp",
    "harika-seyler-dukkani-logo.webp", "harika-seyler-dukkani-urun-seckisi.webp",
    "harika-seyler-dukkani-urun-vitrini.webp", "hediye-paketleri-ve-dekoratif-urunler.webp",
    "hediyelik-esya-hediye-kutusu.webp", "hediyelik-kupa.webp", "hediyelik-masa-lambasi.webp",
    "oyuncak-ayicik.webp", "oyuncak-tren-seti.webp",
)
CATEGORIES = ("bijuteri", "kirtasiye", "oyuncak", "hediyelik-esya")


class Metadata(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.canonicals = []
        self.indexable = True
        self.image = None
        self.inline_images = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "img" and attrs.get("src", "").startswith("../../assets/blog/"):
            self.inline_images.append(attrs["src"])
        if tag == "meta":
            if attrs.get("name", "").lower() in ("robots", "googlebot"):
                self.indexable &= "noindex" not in attrs.get("content", "").lower()
            if attrs.get("property") == "og:image":
                self.image = attrs.get("content")


def build(site):
    XML.register_namespace("", SITEMAP)
    XML.register_namespace("image", IMAGE)
    root = XML.Element(f"{{{SITEMAP}}}urlset")

    def add(url, images):
        entry = XML.SubElement(root, f"{{{SITEMAP}}}url")
        XML.SubElement(entry, f"{{{SITEMAP}}}loc").text = url
        for image in images:
            node = XML.SubElement(entry, f"{{{IMAGE}}}image")
            XML.SubElement(node, f"{{{IMAGE}}}loc").text = image

    add(BASE, [BASE + "assets/" + image for image in HOME_IMAGES])
    pages = [site / name / "index.html" for name in (*CATEGORIES, "blog")]
    pages.extend(sorted((site / "blog").glob("*/index.html")))
    for page in pages:
        expected = urljoin(BASE, page.parent.relative_to(site).as_posix() + "/")
        meta = Metadata(page.read_text(encoding="utf-8"))
        if not meta.indexable or meta.canonicals != [expected]:
            raise ValueError(f"Expected indexable page with canonical {expected}: {page}")
        images = [meta.image] if meta.image and meta.image.startswith(BASE + "assets/") else []
        images.extend(urljoin(expected, src) for src in meta.inline_images)
        add(expected, dict.fromkeys(images))

    XML.indent(root, space="  ")
    XML.ElementTree(root).write(site / "sitemap.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    build(parser.parse_args().site)

