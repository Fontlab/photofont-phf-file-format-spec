---
this_file: src_docs/md/document.md
---

# Document and header

The words **MUST**, **SHOULD** and **MAY** express requirements of this 2.0
profile. They do not retroactively describe every historical reader.

## XML envelope

A writer MUST produce a well-formed XML 1.0 document, encoded as UTF-8, with one
case-sensitive root `<PhF version="2.0">`. The XML declaration's version is the
XML language version; the root attribute is the Photofont format version.
`header/version` is a third, independent value: the font's own release string.

Photofont elements have no namespace. Do not put a default SVG namespace on
`PhF`, `glyphs`, or a data `image`. SVG descendants use the SVG namespace as
described in [resources](resources.md#embedded-svg).

The canonical section order and cardinality are:

| Element | Count | Contents |
| --- | --- | --- |
| `header` | 1 | Font properties, including `family` and `upm` |
| `globals` | 1 | One `unicode_mapping`, then optional `kerning` |
| `glyphs` | 1 | Zero or more `glyph` records |
| `data` | 0 or 1 | Optional `photo` container, then direct SVG `image` resources |

`data` MAY be omitted when all images are external or the font is empty.
Empty arrays and a font with no glyphs are valid. References may point forward
to `data`; readers SHOULD collect identifiers before resolving them.
Whitespace between elements and XML comments do not affect meaning. Escape XML
special characters in names and paths. Attribute order has no meaning in 2.0.
Writers MUST NOT emit a DTD or entity declarations.

## Property syntax

Header properties use `<property type="string|int|real">value</property>`.
The `type` describes the element's text, rather than an XML schema datatype.
Each recognized property MUST appear at most once. Strings are Unicode text;
identifiers elsewhere are case-sensitive, nonempty strings. Numeric text MUST
be finite decimal notation, using `.` for a fractional separator, without units.
`int` denotes signed decimal integers. Writers SHOULD use `int` for integral
values and `real` only for fractional header metrics.

```xml
<header>
  <family type="string">Example Colour</family>
  <full_name type="string">Example Colour Regular</full_name>
  <style type="string">Regular</style>
  <version type="string">1.2</version>
  <upm type="int">1000</upm>
  <ascender type="int">800</ascender>
  <descender type="int">200</descender>
  <external_leading type="int">100</external_leading>
</header>
```

## Header reference

| Property | Type | Requirement / meaning |
| --- | --- | --- |
| `family` | string | Required, nonempty family name |
| `upm` | int or real | Required, strictly positive units per em |
| `full_name` | string | Full font name; defaults to `family` |
| `style` | string | Style name; defaults to `Regular` |
| `version` | string | Font release description; no format-version semantics |
| `copyright` | string | Copyright notice |
| `source` | string | Source or designer information; no resource-resolution semantics |
| `face_name` | string | Legacy face identifier; distinct from `style` |
| `codepage` | string | Legacy descriptive codepage label; does not override Unicode mappings |
| `ascender` | int or real | Nonnegative height above the baseline, in font units |
| `descender` | int or real | Nonnegative depth below the baseline, in font units |
| `base_to_base` | int or real | Nonnegative baseline distance, in font units |
| `external_leading` | int or real | Additional nonnegative line gap, in font units |
| `xHeight` | int or real | Nonnegative lowercase height, in font units |
| `capHeight` | int or real | Nonnegative capital height, in font units |
| `italicAngle` | int or real | Slant angle in degrees; preserve the signed value |

`family` and `upm` were mandatory in the historical specification. The later
implementation reads/writes `face_name`, `source`, `external_leading`, `xHeight`,
`capHeight` and `italicAngle`. The reference samples also contain
`internal_leading`; its effect is not established by the supplied reader, so
2.0 readers MAY preserve it as opaque metadata but MUST NOT derive placement
from it.

### Baselines and descenders

Use `base_to_base` when present. Otherwise, this profile defines baseline
distance as `ascender + descender + external_leading`, with absent leading
treated as zero. The 1.0 specification's default was `ascender + descender`;
the added leading term is an explicit 2.0 profile rule. If either vertical metric
is absent and there is no explicit baseline distance, line spacing is unspecified
and the caller must supply a policy. Writers SHOULD include both metrics.

Do not write the negative descender convention used by many outline-font APIs
into this header: an API descender of `-200` is stored as depth `200`.
Header metrics are already in font units and MUST NOT be scaled by shape PPM.
