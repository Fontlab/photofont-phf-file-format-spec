---
this_file: src_docs/md/index.md
---

# Photofont 2.0 XML format

Photofont stores a font as an XML document whose glyphs refer to PNG or SVG
images. The document carries names, font metrics, Unicode mappings, kerning and
per-image placement and advance metrics. Image resources can be embedded or
stored beside the `.phf` file.

**Photofont 1.0 specified PNG bitmap glyphs and did not support SVG.** Later
implementations added SVG while continuing to write `version="1.0"`.
This specification defines an explicit **2.0 interoperability profile** for both
PNG and SVG, retaining the established XML vocabulary.

!!! note "Specification status"
    This is a reconstructed specification and a proposed 2.0 profile, dated
    25 October 2026. Historical behaviour and new profile requirements are
    distinguished throughout. It does not establish that existing applications
    recognize a `version="2.0"` document. See [sources and status](sources.md).

## Read the format

| Section | Contents |
| --- | --- |
| [Document and header](document.md) | XML syntax, versions, font names and global metrics |
| [Encoding and kerning](mapping.md) | Unicode scalar values and pair adjustments |
| [Glyphs and metrics](metrics.md) | Images, shapes, advances, PPM scaling and crop coordinates |
| [PNG and SVG resources](resources.md) | Embedded MIME PNGs, SVG fragments and external files |
| [Conformance](conformance.md) | Required checks and legacy interoperability limits |
| [Examples](examples.md) | Complete original fonts covering both formats and storage modes |
| [Python recipes](python.md) | Read resources, inspect metrics and write an SVG font |

## Document at a glance

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PhF version="2.0">
  <header><!-- Font names and UPM --></header>
  <globals><!-- Unicode mappings and optional kerning --></globals>
  <glyphs><!-- Glyph image records and their metrics --></glyphs>
  <data><!-- Embedded PNG and/or SVG resources --></data>
</PhF>
```

This skeleton shows the four sections; the [complete examples](examples.md)
supply their required contents. A glyph image record describes the use of a
resource. A data image stores the resource itself. These two uses of `<image>`
are distinct and have separate identifier scopes.

Photofont is an interchange format. It does not define a browser font-loading
API, OpenType shaping engine, variable font model or SVG font element. A `.phf`
file cannot be used directly as a standard CSS webfont.
