#!/usr/bin/env -S uv run -s
# /// script
# requires-python = ">=3.12"
# dependencies = ["defusedxml==0.7.1"]
# ///
# this_file: src_docs/md/examples/photofont.py
"""Read Photofont resources or write a synthetic SVG font; not a full validator."""

import argparse
import base64
import copy
import textwrap
from email import policy
from email.parser import Parser
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

from defusedxml import ElementTree as SafeET

SVG = "http://www.w3.org/2000/svg"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def load_font(path: Path) -> ET.Element:
    """Parse XML without DTDs/entities; accept 2.0 and extended legacy 1.0."""
    root = SafeET.parse(path, forbid_dtd=True).getroot()
    if root.tag != "PhF" or root.get("version") not in {"1.0", "2.0"}:
        raise ValueError("Expected PhF version 1.0 or 2.0")
    return root


def decode_png(text: str) -> bytes:
    """Decode a MIME PNG; a PNG decoder must still check chunks and pixels."""
    message = Parser(policy=policy.default).parsestr(textwrap.dedent(text).strip())
    if message.get_content_type() != "image/png":
        raise ValueError("Expected image/png")
    if message.get("Content-Transfer-Encoding", "").lower() != "base64":
        raise ValueError("Expected Base64 transfer encoding")
    raw = base64.b64decode("".join(message.get_payload().split()), validate=True)
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError("Invalid PNG signature")
    return raw


def local_resource(directory: Path, location: str) -> Path:
    """Resolve a portable local resource without escaping the font directory."""
    relative = PurePosixPath(location)
    if (
        not location
        or relative.is_absolute()
        or ".." in relative.parts
        or any(char in location for char in "\\:?#")
    ):
        raise ValueError("Expected a relative local resource path")
    path = (directory / location).resolve()
    if not path.is_relative_to(directory.resolve()):
        raise ValueError("Resource escapes the font directory")
    return path


def resource_bytes(
    root: ET.Element, image: ET.Element, shape: ET.Element, directory: Path
) -> bytes:
    """Return PNG bytes or a standalone SVG wrapper without rendering graphics."""
    locations = [key for key in ("embedded", "system") if key in shape.attrib]
    if len(locations) != 1:
        raise ValueError(
            "Expected one resource location (metric-only shapes have none)"
        )
    kind = image.attrib["type"]
    if kind not in {"photo", "svg"}:
        raise ValueError("Unsupported image type")
    if locations[0] == "system":
        return local_resource(directory, shape.attrib["system"]).read_bytes()
    identifier = shape.attrib["embedded"]
    candidates = list(root.findall("data/photo/image")) + list(
        root.findall("data/image")
    )
    matches = [item for item in candidates if item.get("id") == identifier]
    if len(matches) != 1:
        raise ValueError("Missing or duplicate embedded resource")
    resource = matches[0]
    png_container = resource in root.findall("data/photo/image")
    resource_kind = resource.get("type", "photo" if png_container else "")
    if resource_kind != kind or png_container != (kind == "photo"):
        raise ValueError("Resource type does not match glyph image")
    if kind == "photo":
        return decode_png(resource.text or "")
    svg = ET.Element(f"{{{SVG}}}svg")
    svg.extend(copy.deepcopy(list(resource)))
    return ET.tostring(svg, encoding="utf-8", xml_declaration=True)


def advance(shape: ET.Element, upm: float) -> tuple[float, float]:
    """Convert shape advances from PPM units to font units."""
    ppm = int(shape.find("ppm").attrib["int"])
    if ppm <= 0 or not 0 < upm < float("inf"):
        raise ValueError("UPM and PPM must be positive and finite")
    delta = shape.find("delta")
    return tuple(int(delta.attrib[axis]) * upm / ppm for axis in ("x", "y"))


def png_crop(shape: ET.Element) -> tuple[int, int, int, int]:
    """Return source-image crop (x, y, width, height); see spec for bounds checks."""
    box, base = shape.find("bbox"), shape.find("base")
    x, y, width, height = (
        int(box.attrib[key]) for key in ("x", "y", "width", "height")
    )
    return int(base.attrib["x"]) + x, int(base.attrib["y"]) - y - height, width, height


def write_svg_font(path: Path) -> None:
    """Write a minimal original font with one embedded SVG glyph; never overwrite."""
    root = ET.Element("PhF", version="2.0")
    header = ET.SubElement(root, "header")
    for name, kind, text in (
        ("family", "string", "Recipe Demo"),
        ("upm", "int", "1000"),
    ):
        ET.SubElement(header, name, type=kind).text = text
    globals_node = ET.SubElement(root, "globals")
    mapping = ET.SubElement(
        globals_node, "unicode_mapping", type="array", subtype="map_unicode"
    )
    ET.SubElement(mapping, "map", id="A", unc="65")
    glyph = ET.SubElement(ET.SubElement(root, "glyphs"), "glyph", id="A")
    image = ET.SubElement(glyph, "image", id="v0", type="svg")
    shape = ET.SubElement(image, "shape", embedded="a-vector")
    ET.SubElement(shape, "ppm", int="1000")
    ET.SubElement(shape, "delta", x="650", y="0")
    resource = ET.SubElement(
        ET.SubElement(root, "data"), "image", id="a-vector", type="svg"
    )
    ET.SubElement(
        resource, f"{{{SVG}}}path", d="M0 0 L300 -700 L600 0 Z", fill="#d13b42"
    )
    ET.indent(root)
    with path.open("xb") as stream:
        ET.ElementTree(root).write(stream, encoding="utf-8", xml_declaration=True)


def main() -> None:
    """Inspect each shape or create an example font at an unused path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path)
    parser.add_argument(
        "--write", action="store_true", help="write a synthetic SVG font"
    )
    args = parser.parse_args()
    if args.write:
        write_svg_font(args.font)
        return
    root = load_font(args.font)
    upm = float(root.findtext("header/upm"))
    for glyph in root.findall("glyphs/glyph"):
        for image in glyph.findall("image"):
            for shape in image.findall("shape"):
                raw = (
                    resource_bytes(root, image, shape, args.font.parent)
                    if any(key in shape.attrib for key in ("embedded", "system"))
                    else b""
                )
                print(
                    glyph.attrib["id"],
                    image.attrib["type"],
                    advance(shape, upm),
                    len(raw),
                    "bytes",
                )


if __name__ == "__main__":
    main()
