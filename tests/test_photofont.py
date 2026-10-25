# this_file: tests/test_photofont.py
"""Executable recipes and original fixtures, independent of private sources."""

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from defusedxml.common import DefusedXmlException

EXAMPLES = Path(__file__).resolve().parents[1] / "src_docs/md/examples"
spec = importlib.util.spec_from_file_location("photofont", EXAMPLES / "photofont.py")
phf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phf)


class RecipeTests(unittest.TestCase):
    def test_documented_python_snippets_execute_as_written(self):
        snippets = re.findall(
            r"```python\n(.*?)```", (EXAMPLES.parent / "python.md").read_text(), re.DOTALL
        )
        with tempfile.TemporaryDirectory() as folder:
            for path in EXAMPLES.iterdir():
                if path.is_file():
                    shutil.copy(path, folder)
            for snippet in snippets:
                if "--8<--" not in snippet:
                    subprocess.run(
                        [sys.executable, "-c", snippet],
                        cwd=folder,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
            self.assertTrue((Path(folder) / "extracted.svg").is_file())
            self.assertEqual(phf.load_font(Path(folder) / "new-demo.phf").tag, "PhF")

    def test_all_four_storage_modes_resolve_original_resources(self):
        for name in ("embedded-png", "external-png", "embedded-svg", "external-svg"):
            with self.subTest(name=name):
                path = EXAMPLES / f"{name}.phf"
                font = phf.load_font(path)
                image = font.find("glyphs/glyph/image")
                raw = phf.resource_bytes(font, image, image.find("shape"), path.parent)
                if image.attrib["type"] == "photo":
                    self.assertEqual(raw, (EXAMPLES / "pixel.png").read_bytes())
                else:
                    svg = ET.fromstring(raw)
                    self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
                    self.assertIsNotNone(
                        svg.find(".//{http://www.w3.org/2000/svg}path")
                    )

    def test_shape_units_and_png_crop_are_not_font_units(self):
        shape = ET.fromstring(
            '<shape><ppm int="100"/><bbox x="-2" y="-3" '
            'width="6" height="8"/><base x="12" y="25"/>'
            '<delta x="60" y="-5"/></shape>'
        )
        self.assertEqual(phf.advance(shape, 1000), (600, -50))
        self.assertEqual(phf.png_crop(shape), (10, 20, 6, 8))

    def test_invalid_ppm_is_rejected(self):
        for value in ("0", "-1", "invalid"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                phf.advance(
                    ET.fromstring(
                        f'<shape><ppm int="{value}"/><delta x="1" y="0"/></shape>'
                    ),
                    1000,
                )

    def test_invalid_upm_is_rejected(self):
        shape = ET.fromstring('<shape><ppm int="100"/><delta x="1" y="0"/></shape>')
        for upm in (0, -1, float("inf"), float("nan")):
            with self.subTest(upm=upm), self.assertRaises(ValueError):
                phf.advance(shape, upm)

    def test_invalid_mime_or_png_signature_is_rejected(self):
        for text in (
            "",
            "Content-Type: text/plain\n\nx",
            "Content-Type: image/png\nContent-transfer-encoding: base64\n\n???",
            "Content-Type: image/png\nContent-transfer-encoding: base64\n\neA==",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                phf.decode_png(text)

    def test_mime_accepts_wrapping_indentation_and_header_case(self):
        font = phf.load_font(EXAMPLES / "embedded-png.phf")
        text = font.find("data/photo/image").text
        text = text.replace("Content-Type", "content-type").replace("\n", "\n  ")
        self.assertEqual(phf.decode_png(text), (EXAMPLES / "pixel.png").read_bytes())

    def test_external_paths_cannot_escape_or_use_urls(self):
        for location in (
            "../outside.png",
            "/tmp/file.png",
            "https://example.com/a.png",
            "a\\b.png",
            "pixel.png?x",
            "pixel.png#x",
            "",
        ):
            with self.subTest(location=location), self.assertRaises(ValueError):
                phf.local_resource(EXAMPLES, location)
        with tempfile.TemporaryDirectory() as folder:
            link = Path(folder) / "escape"
            link.symlink_to(EXAMPLES / "pixel.png")
            with self.assertRaises(ValueError):
                phf.local_resource(Path(folder), "escape")

    def test_missing_file_and_missing_embedded_resource_fail(self):
        with self.assertRaises(FileNotFoundError):
            phf.local_resource(EXAMPLES, "missing.png").read_bytes()
        font = phf.load_font(EXAMPLES / "embedded-png.phf")
        shape = font.find("glyphs/glyph/image/shape")
        shape.set("embedded", "missing")
        with self.assertRaises(ValueError):
            phf.resource_bytes(font, font.find("glyphs/glyph/image"), shape, EXAMPLES)

    def test_conflicting_locations_and_wrong_types_fail(self):
        font = phf.load_font(EXAMPLES / "embedded-png.phf")
        image = font.find("glyphs/glyph/image")
        shape = image.find("shape")
        shape.set("system", "pixel.png")
        with self.assertRaises(ValueError):
            phf.resource_bytes(font, image, shape, EXAMPLES)
        shape.attrib.pop("system")
        image.set("type", "svg")
        with self.assertRaises(ValueError):
            phf.resource_bytes(font, image, shape, EXAMPLES)

    def test_writer_saved_file_reopens_with_expected_svg(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "demo.phf"
            phf.write_svg_font(path)
            font = phf.load_font(path)
            self.assertEqual(font.findtext("header/family"), "Recipe Demo")
            self.assertEqual(
                font.find("globals/unicode_mapping/map").attrib["unc"], "65"
            )
            self.assertEqual(
                phf.advance(font.find("glyphs/glyph/image/shape"), 1000), (650, 0)
            )
            with self.assertRaises(FileExistsError):
                phf.write_svg_font(path)

    def test_loader_rejects_dtd_wrong_root_and_version(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.phf"
            for raw in (
                '<!DOCTYPE PhF><PhF version="2.0"/>',
                '<Other version="2.0"/>',
                '<PhF version="9.0"/>',
            ):
                path.write_text(raw)
                with (
                    self.subTest(raw=raw),
                    self.assertRaises((ValueError, DefusedXmlException)),
                ):
                    phf.load_font(path)

    def test_cli_reads_all_fixtures_and_writes_font(self):
        for path in EXAMPLES.glob("*.phf"):
            result = subprocess.run(
                [sys.executable, str(EXAMPLES / "photofont.py"), str(path)],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("bytes", result.stdout)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "new.phf"
            subprocess.run(
                [sys.executable, str(EXAMPLES / "photofont.py"), "--write", str(path)],
                check=True,
                capture_output=True,
            )
            self.assertEqual(phf.load_font(path).tag, "PhF")


if __name__ == "__main__":
    unittest.main()
