---
this_file: src_docs/md/mapping.md
---

# Encoding and kerning

## Unicode mapping

```xml
<globals>
  <unicode_mapping type="array" subtype="map_unicode">
    <map id="A" unc="65" />
    <map id="A" unc="97" />
    <map id="V" unc="86" />
    <map id="smile" unc="128578" />
  </unicode_mapping>
  <kerning type="array" subtype="kerning_pair">
    <pair left="A" right="V" x="-60" />
  </kerning>
</globals>
```

Each `map` MUST have `id`, referring to an existing glyph, and `unc`, a decimal
Unicode scalar value in `0..1114111`, excluding the surrogate range
`55296..57343`. Supplementary-plane characters are supported by this profile;
the old GlyphsSDK sample's 16-bit character handling is not a format limit.

Multiple codepoints MAY map to one glyph. A glyph MAY have no mapping. Within
this profile, one codepoint MUST NOT map to different glyphs, and duplicate
identical mapping rows SHOULD be omitted. An empty `unicode_mapping` is valid.
Glyph names do not imply codepoints. The format does not specify Unicode
normalization, variation sequences, ligature substitution, bidi processing or
missing-glyph selection. Applications must define these separately.

Write decimal `unc` values. A historical C++ reader accepts C-style numeric
prefixes, but hexadecimal or octal input is not canonical 2.0 syntax.

## Kerning pairs

| Attribute | Requirement / meaning |
| --- | --- |
| `left` | Required glyph ID preceding the pair boundary |
| `right` | Required glyph ID following the pair boundary |
| `left_image` | Optional image-record ID within the left glyph |
| `right_image` | Optional image-record ID within the right glyph |
| `x` | Signed decimal integer horizontal adjustment, default 0 |
| `y` | Signed decimal integer vertical adjustment, default 0 |

Both referenced glyphs MUST exist. Image qualifiers, when supplied, MUST resolve
within their respective glyphs. Omitting an image qualifier makes that side of
the pair match all images of its glyph.

Kerning is in **font units**, independent of the selected shape's PPM. A negative
`x` reduces horizontal separation. In the 2.0 profile, positive `y` moves the
following glyph upward in font coordinates. The pair adjustment is applied once
to the following glyph's origin and subsequent pen position, not once per shape.

```xml
<pair left="A" left_image="colour" right="V" x="-40" y="0" />
```

### Overlap rule (2.0 profile)

Choose the matching pair with the most explicit image qualifiers. A pair
qualifying both images takes precedence over a one-sided pair; a one-sided pair
takes precedence over a glyph-wide pair. Equally specific matching entries are
ambiguous and MUST be rejected, including duplicate pairs. Do not sum broad and
specific adjustments. This rule resolves a case the 1.0 prose did not define.

For a 600-unit advance of `A` and `x="-60"`, the origin of `V` is 540 units after
the origin of `A`. With `upm=1000` and a requested 50-pixel em, that is 27 pixels.

The supplied C++ implementation only reads/writes unqualified horizontal pairs
with attributes ordered `left`, `right`, `x`. Readers supporting the full 2.0
pair model must not copy that limitation. For legacy exchange, use simple pairs
and that attribute order. See [compatibility](conformance.md#legacy-compatibility).
