---
this_file: src_docs/md/metrics.md
---

# Glyphs and metrics

## Records and identifier scopes

```xml
<glyphs>
  <glyph id="A">
    <image id="colour" type="photo" shift_x="0" shift_y="0">
      <shape embedded="a-pixels">
        <ppm int="100" />
        <bbox x="2" y="0" width="6" height="8" />
        <base x="-2" y="8" />
        <delta x="10" y="0" />
      </shape>
    </image>
  </glyph>
</glyphs>
```

This is a fragment; its `a-pixels` resource must be supplied in `data`.

| Record | Meaning |
| --- | --- |
| `glyph/@id` | Required, unique across the font; used in mapping and kerning |
| `glyph/image/@id` | Required, unique within that glyph |
| `glyph/image/@type` | Required, `photo` for PNG or `svg` for SVG |
| `glyph/image/@shift_x`, `@shift_y` | Optional signed integers, default 0, in font units |
| `image/shape` | One or more uses of resources with independent metrics |

A glyph MAY contain no image records. This represents no drawable image and
does not supply an advance; use a metric-only shape for a space glyph.
An image record MUST contain at least one shape. A resource ID is independent
of an image-record ID. Multiple glyphs or shapes MAY share a resource.

Historical image records have been used as alternate pictures and as editor
layers. No universal selection/compositing algorithm is established by those
implementations. A 2.0 application MUST state how it selects image records and
shapes (for example, select an explicit image ID and a resolution). Writers
SHOULD use one image and one shape per glyph for portable exchange. Additional
image records MUST NOT be assumed to be PNG fallbacks for an SVG image.

## Shape fields

| Element / attribute | Requirement / meaning |
| --- | --- |
| `shape/@embedded` | Embedded resource ID; mutually exclusive with `system` |
| `shape/@system` | Relative path to an external PNG/SVG file |
| `ppm/@int` | Required positive integer: shape units per em |
| `bbox/@x`, `@y`, `@width`, `@height` | Required for PNG; signed offsets and nonnegative extents |
| `base/@x`, `@y` | Required for PNG; baseline origin in source-image coordinates |
| `delta/@x`, `@y` | Required signed integers: horizontal and vertical advance components |

Write children in order `ppm`, `bbox`, `base`, `delta`; omit `bbox` and `base`
for origin-aligned embedded SVG. All shape numbers are integers. `bbox`, `base`
and `delta` are measured in the shape's PPM units, not header UPM units.
SVG external coordinates are described [separately](resources.md#external-svg).

A drawable shape MUST have exactly one nonempty location attribute. A
metric-only PNG shape MAY omit both, but MUST have zero bbox width and height.
Its positive PPM and `delta` still define spacing. An empty location string is
not a substitute for omitting the attribute.

## PPM and advance conversion

Let `U` be header UPM, `P` shape PPM, and `E` requested em size in display pixels:

```text
shape-to-font scale = U / P
font advance X      = delta.x * U / P
font advance Y      = delta.y * U / P
shape-to-pixel scale = E / P
font-to-pixel scale  = E / U
```

For `U=1000`, `P=100`, `delta.x=60`, the font advance is 600 font units.
At a 50-pixel em it is 30 pixels. Do not assume `ppm == upm`.
The `delta` values are pen movement, not an image offset, and MUST NOT be
summed over shapes used to draw one glyph. To avoid reader-dependent spacing,
all shapes and images of a glyph SHOULD yield the same scaled advances.
The legacy FontGate reader takes the maximum nonnegative scaled advance across
shapes; this loses negative advances and is not a 2.0 requirement.

## PNG crop and placement

Use a source PNG coordinate system with origin at its top-left, X rightward and
Y downward. Font coordinates have X rightward, Y upward and origin on the
baseline. `bbox.y` is the **bottom** of the glyph in upward shape coordinates.
This resolves an inconsistent “top border” description in the older prose.

For `bbox=(x, y, w, h)` and `base=(bx, by)`, the top-left of the source crop is:

```text
crop_x = bx + x
crop_y = by - y - h
crop_width = w
crop_height = h
```

For a point `(u, v)` measured from the top-left of that crop:

```text
font_x = (x + u) * U/P + shift_x
font_y = (y + h - v) * U/P + shift_y
```

The crop MUST lie inside the source PNG. Base coordinates themselves can be
negative or outside the image. A shared atlas uses different base/bbox values
for each glyph; do not crop the whole atlas to every glyph.

In the fragment above, a 6×8 source PNG has `crop=(0,0,6,8)`. At `U=1000` and
`P=100`, its left edge is 20 font units right of the origin, its top is 80 units
above the baseline, and its advance is 100 units. Image shifts apply after
scaling and MUST be applied once, even when an image has multiple shapes.

## Metric-only space

```xml
<glyph id="space">
  <image id="v0" type="photo">
    <shape>
      <ppm int="1000" />
      <bbox x="0" y="0" width="0" height="0" />
      <base x="0" y="0" />
      <delta x="250" y="0" />
    </shape>
  </image>
</glyph>
```
