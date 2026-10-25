# this_file: tests/test_site.py
"""Audit the complete generated site, including fragment links and downloads."""

import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
PREFIX = "/photofont-phf-file-format-spec/"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


class SiteTests(unittest.TestCase):
    def test_every_local_link_asset_and_fragment_resolves(self):
        pages = {p: Page(p.read_text()) for p in SITE.rglob("*.html")}
        self.assertGreaterEqual(
            len(pages), 10, "Build the complete site before testing"
        )
        for path, page in pages.items():
            for link in page.links:
                target = urlsplit(link)
                if target.scheme or target.netloc:
                    continue
                relative = unquote(target.path)
                if relative.startswith(PREFIX):
                    dest = SITE / relative.removeprefix(PREFIX)
                elif relative.startswith("/"):
                    self.fail(f"Unexpected absolute site path: {link}")
                else:
                    dest = path.parent / relative if relative else path
                dest = dest.resolve()
                if dest.is_dir():
                    dest /= "index.html"
                self.assertTrue(
                    dest.is_file(), f"{path.relative_to(SITE)}: broken {link}"
                )
                if target.fragment and dest.suffix == ".html":
                    self.assertIn(
                        unquote(target.fragment),
                        pages[dest].ids,
                        f"{path.relative_to(SITE)}: broken anchor {link}",
                    )

    def test_downloads_are_exact_source_bytes(self):
        for path in (ROOT / "src_docs/md/examples").iterdir():
            if path.is_file():
                self.assertEqual(
                    (SITE / "examples" / path.name).read_bytes(),
                    path.read_bytes(),
                    f"Stale downloadable file: {path.name}",
                )

    def test_public_site_excludes_private_inputs_and_local_paths(self):
        forbidden = (
            b"/Users/",
            b"_private/",
            b"phf_read.cpp",
            b"phf_write.cpp",
            b"Trees24",
            b"arturaliev-ClipBlank01",
            b"dvarg DisplayBoard",
        )
        for path in SITE.rglob("*"):
            if path.is_file():
                self.assertNotIn("__pycache__", path.parts, "Do not publish Python caches")
                self.assertNotEqual(path.suffix, ".pyc", "Do not publish Python bytecode")
                raw = path.read_bytes()
                for token in forbidden:
                    self.assertFalse(
                        token in raw, f"Private source leak in {path.relative_to(SITE)}"
                    )


if __name__ == "__main__":
    unittest.main()
