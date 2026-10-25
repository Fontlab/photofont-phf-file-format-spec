---
this_file: src_docs/md/conformance.md
---

# Conformance and compatibility

## A 2.0 writer

A conforming writer MUST meet the document, identifier, numeric, mapping,
kerning and resource rules in this specification. In particular:

1. Emit UTF-8 XML, `<PhF version="2.0">`, one header with nonempty family and
   positive UPM, one globals and one glyphs section.
2. Write explicit image types, positive shape PPM and complete `delta` metrics.
   PNG records include bbox and base. Metric-only shapes have no location and
   zero bbox dimensions.
3. Keep glyph IDs unique, image IDs unique within glyphs and resource IDs unique
   across `data`. Resolve all mapping, kerning and embedded-resource references.
4. Serialize PNG as MIME/Base64 in `data/photo/image`, or as external PNG;
   serialize embedded SVG as graphics in direct `data/image type="svg"`, or as
   an external SVG document. Do not confuse the storage forms.
5. Use valid Unicode scalars and unambiguous kerning. Keep resource paths local
   and portable. Include every required external file when distributing a font.

These additional restrictions make 2.0 exchange predictable. They are not
claims that all historical files obey them. There is no supplied authoritative
XSD or DTD; the rules here are the conformance contract.

## A 2.0 reader

A reader claiming full 2.0 support MUST accept both PNG and SVG, both embedded
and external storage, arbitrary XML attribute order and the documented numeric
and reference forms. It MUST distinguish invalid input from unsupported
features. A PNG-only implementation MUST identify itself as a subset reader.

Readers MUST reject zero/negative UPM or PPM, invalid numeric values, duplicate
identifiers, dangling references, invalid Unicode scalars, ambiguous kerning,
conflicting locations, resource-type mismatches and crops outside PNG bounds.
Missing files and corrupt image payloads are errors, even if metrics are valid.
They MUST reject DTD/entity declarations and prevent resource resolution from
escaping the chosen font directory, including through symlinks.
Implementations SHOULD impose documented input/image-size limits appropriate
to their environment. XML parsing alone does not validate a PNG or render SVG.

Unknown metadata MAY be preserved for round-trip purposes. Unknown image types
and graphics features MUST be reported as unsupported; they MUST NOT be silently
discarded. Readers should retain enough information to avoid rewriting a
partially supported font as though conversion were lossless.

### Rendering and layout policies

The caller must state image/shape selection, unsupported SVG handling,
missing-character behaviour and line spacing when metrics are absent. These
choices are outside the portable file contract. The Python recipes intentionally
inspect resources without selecting or rendering them.

## Legacy compatibility

| Feature | Original 1.0 specification | Later observed usage | 2.0 profile |
| --- | --- | --- | --- |
| Root version | `1.0` | Still `1.0`, even with SVG | `2.0` |
| PNG glyph images | Yes | Yes | Required reader support |
| SVG glyph images | **Not supported** | `type="svg"` implemented | Required reader support |
| Embedded PNG | MIME/Base64 in `data/photo/image` | Same structure | Same structure |
| External image path | `bitmap_placement` in prose | `system`; C++ reader also accepts `file` | Canonical `system` |
| Embedded SVG | Absent | Direct `data/image type="svg"` | Same structure |
| Shape PPM scaling | Described | Explicitly implemented | Required |
| Image-specific/vertical kerning | Described | Only a subset implemented by C++ reader | Defined, with overlap rule |
| Attribute order | XML implies no semantics | Some C++ routines depend on order | No order dependence |

### Reading existing fonts

A compatibility mode MAY accept root `1.0` with SVG, identifying it as an
extended legacy file. It MAY normalize `file` to `system`. Older
`bitmap_placement` examples include both paths and URLs; do not enable network
access merely because the attribute appears. Preserve or report unsupported
locations rather than silently changing their meaning.

The supplied C++ reader has order-dependent parsing for maps, pairs and shape
locations; put `id` before `unc`, use `left`, `right`, `x` for simple pairs, and
put the location first when targeting it. A mixed PNG/SVG legacy writer can
repeat image IDs; a 2.0 writer must assign distinct IDs and update qualifiers.
Do not infer full specification conformance from successful loading in one app.

### Writing for an old application

Confirm the target application's capabilities with a small test font. Merely
changing the root version to `1.0` does not make SVG a feature of the original
1.0 format. A strict original-1.0 target requires PNG resources, rasterization
of SVG if needed, and supported metrics/kerning. A legacy SVG-capable target
may accept the older extended dialect, but this must be tested separately.

The GlyphsSDK sample focuses on embedded PNG background images and should not
be treated as a full SVG-capable reader. The private C++ implementation was
read as evidence; it has not been compiled or used to certify these examples.
