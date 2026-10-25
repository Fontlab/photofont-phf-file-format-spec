---
this_file: src_docs/md/sources.md
---

# Sources and specification status

This document combines historical format documentation with observations from
later readers, writers and sample files. It is original prose. Reference source
code and third-party sample fonts are not redistributed with the public site.

## Evidence and decisions

| Topic | Evidence | Treatment in this specification |
| --- | --- | --- |
| Four sections, names, UPM, mapping, kerning, PNG MIME | June 2003 Photofont 1.0 draft and older developer tutorial | Retained, with explicit validity rules |
| Original 1.0 has no SVG | Historical text specifies photo/PNG images only | Explicit compatibility boundary |
| SVG with root 1.0 | Later C++ reader/writer and external-SVG sample fonts | Documented as extended legacy usage |
| SVG fragments outside `photo` | Later C++ writer and reader | Retained as canonical embedded representation |
| PNG bbox/base and scaling | Reader's crop equations, writer's inverse placement and GlyphsSDK crop/position | Equations stated explicitly; ambiguous older wording corrected |
| External SVG baseline | Later reader uses base offsets and Y conversion; its SVG parser internals are outside the supplied collection | Explicit 2.0 equation; legacy viewport/import behaviour requires target testing |
| Extra header properties and image shifts | Later reader/writer | Listed with units and defaults |
| 2.0 version marker, path policy, unique IDs and pair precedence | Interoperability decisions made for this document | New profile requirements, not historical claims |

No separate ratified Photofont 2.0 document was present in the supplied reference
collection. “2.0” here names the explicit profile written for this project.
Application support must be established independently. The specification does
not promise that an existing FontLab or Glyphs release imports the new marker.

## Public references

- [Project repository](https://github.com/Fontlab/photofont-phf-file-format-spec)
  — Markdown sources, runnable examples, tests and build instructions.
- [Historical Photofont developer page (Internet Archive)](https://web.archive.org/web/20090206082057/http://www.photofont.com/photofont/devel/)
  — the 1.0 draft, revision June 2003.
- [GlyphsSDK Photofont sample, pinned revision](https://github.com/schriftgestalt/GlyphsSDK/blob/569244a7181e08fc7c5230bcdfad6b9f7e5ea11f/Xcode%20Samples/Photofont/Photofont/GSPhotoFont.m)
  — independent PNG importer/exporter, useful for cross-checking crop and baseline
  interpretation; not a complete implementation of this profile.
- [XML 1.0](https://www.w3.org/TR/xml/) and [SVG 1.1](https://www.w3.org/TR/SVG11/)
  — underlying document and vector-graphics languages.
- [PNG specification](https://www.w3.org/TR/png/) and
  [MIME transfer encodings](https://www.rfc-editor.org/rfc/rfc2045#section-6)
  — image representation and Base64 transport.

The implementation evidence includes private FontGate material reviewed locally.
Its source and the reference fonts retain their own rights and are intentionally
absent from this website. All downloadable example fonts here are synthetic,
created for this specification, and covered by the repository's MIT license.

## Website tooling

The website follows the FontLab Marketing and VFJ documentation sites:
[ProperDocs](https://properdocs.org/user-guide/configuration/),
[MaterialX](https://pypi.org/project/mkdocs-materialx/) and versioned
[fltheme26](https://i.fontlab.com/fltheme26/1.0.0/theme.css) styles and scripts.
Markdown and configuration are maintained separately from generated HTML.
