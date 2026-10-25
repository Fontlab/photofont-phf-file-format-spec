---
this_file: src_docs/md/python.md
---

# Python recipes

[Download photofont.py](examples/photofont.py). It requires Python 3.12 or later.
Its inline dependency declaration lets `uv run photofont.py …` install
`defusedxml` without setting up a project. In this repository, use
`uv run python src_docs/md/examples/photofont.py …`.

The recipe parses the XML envelope, reports scaled advances and reads PNG/SVG
resources. It also writes a minimal embedded-SVG font using ElementTree. It
accepts both 2.0 and extended legacy 1.0 envelopes; it does not certify either.

## Read glyph metrics

```python
from pathlib import Path
from photofont import load_font, advance, png_crop

font = load_font(Path("embedded-png.phf"))
upm = float(font.findtext("header/upm"))
shape = font.find("glyphs/glyph/image/shape")
print(advance(shape, upm))  # (600.0, 0.0)
print(png_crop(shape))      # (0, 0, 1, 1)
```

## Read resource bytes

```python
from pathlib import Path
from photofont import load_font, resource_bytes

path = Path("embedded-svg.phf")
font = load_font(path)
image = font.find("glyphs/glyph/image")
raw = resource_bytes(font, image, image.find("shape"), path.parent)
# Embedded SVG becomes a standalone <svg> wrapper; external files stay unchanged.
with Path("extracted.svg").open("xb") as output:
    output.write(raw)
```

For PNG input, `raw` is decoded PNG bytes. Metric-only shapes have no resource;
do not pass them to `resource_bytes`. This function does not render SVG or choose
a viewport for the reconstructed baseline-origin fragment. Its graphics may
extend into negative coordinates; a previewer must supply a suitable viewBox.

## Write a new font

```python
from pathlib import Path
from photofont import write_svg_font, load_font

path = Path("new-demo.phf")
write_svg_font(path)  # Raises FileExistsError if the path already exists.
font = load_font(path)
print(font.findtext("header/family"))  # Recipe Demo
```

## Scope of the checks

The recipe rejects DTDs/entities, unsupported root versions, unsafe local paths,
conflicting locations, missing/duplicate requested embedded resources, resource
type mismatches, invalid Base64 and incorrect embedded PNG signatures. It checks
UPM/PPM when computing advances. Missing external files raise `FileNotFoundError`;
malformed XML and invalid numeric text raise parsing errors.

**It is not a complete conformance validator.** It assumes the requested glyph
and metric elements exist, and does not validate all IDs, mappings, kerning,
crop bounds, PNG chunks or SVG features. External resources are read as bytes,
without decoding or executing them. Use a PNG decoder and an SVG-aware importer
before rendering; apply the [full conformance rules](conformance.md) at an
application's input boundary. The recipe has no font renderer or layout engine.

## Complete runnable source

```python
--8<-- "examples/photofont.py"
```

The implementation uses Python's [ElementTree writer](https://docs.python.org/3/library/xml.etree.elementtree.html),
[MIME parser](https://docs.python.org/3/library/email.parser.html) and
[strict Base64 decoder](https://docs.python.org/3/library/base64.html).
