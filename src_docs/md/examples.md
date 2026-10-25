---
this_file: src_docs/md/examples.md
---

# Complete examples

These synthetic fonts contain `A` (U+0041) and a metric-only space (U+0020).
They are original examples under the repository's MIT license. No private font
or implementation is included. Each listing below comes from the downloadable
file itself.

| Example | Image representation | Storage | Scaled advance of A |
| --- | --- | --- | --- |
| [Embedded PNG](examples/embedded-png.phf) | Transparent 1×1 PNG, PPM 100 | MIME/Base64 | 600 font units |
| [External PNG](examples/external-png.phf) | Same PNG | `pixel.png` | 600 font units |
| [Embedded SVG](examples/embedded-svg.phf) | Red stylized A, PPM 1000 | SVG fragment | 650 font units |
| [External SVG](examples/external-svg.phf) | Same visible geometry | `A.svg` | 650 font units |

All four use UPM 1000 and a 250-unit space advance. The tiny PNG demonstrates
transport and metrics; it is transparent and is not intended as a visible letter.
The SVG examples put their top 700 units above the baseline. Their horizontal
shape positions match despite their different source coordinate systems.

## Embedded PNG

Download [embedded-png.phf](examples/embedded-png.phf). No additional files are
needed. PNG data is wrapped in MIME headers inside `data/photo/image`.

```xml
--8<-- "examples/embedded-png.phf"
```

## External PNG

Save [external-png.phf](examples/external-png.phf) and
[pixel.png](examples/pixel.png) in the same directory.

```xml
--8<-- "examples/external-png.phf"
```

## Embedded SVG

Download [embedded-svg.phf](examples/embedded-svg.phf). The glyph references an
SVG fragment in `data/image`; no nested SVG root or MIME wrapper is used.

```xml
--8<-- "examples/embedded-svg.phf"
```

## External SVG

Save [external-svg.phf](examples/external-svg.phf) and [A.svg](examples/A.svg)
in the same directory. The external image's baseline is at `y=700`.

```xml
--8<-- "examples/external-svg.phf"
```

The SVG resource is a standalone document:

```xml
--8<-- "examples/A.svg"
```

## Inspect the files

Download [photofont.py](examples/photofont.py), then run:

```sh
uv run photofont.py embedded-png.phf
uv run photofont.py external-svg.phf
uv run photofont.py --write new-demo.phf
uv run photofont.py new-demo.phf
```

The writer creates a new file and refuses to overwrite an existing one.
See [Python recipes](python.md) for the reader's scope and resource extraction.
