---
this_file: src_docs/md/resources.md
---

# PNG and SVG resources

## Locations and resource IDs

`shape embedded="resource-id"` resolves to a data image with the same ID.
IDs MUST be unique across both PNG and SVG data resources. The resource's type
MUST match the glyph image's type. File extensions in IDs are optional and do
not determine the resource type.

`shape system="images/A.png"` or `system="images/A.svg"` resolves relative to the
directory containing the `.phf` file. A 2.0 writer MUST use portable relative
paths with `/` separators. This profile excludes absolute paths, URI schemes,
backslashes, query/fragment suffixes and `..` path components. Readers MUST NOT
silently fetch network resources. These are explicit 2.0 resource policies;
older prose also described remote locations.

Embedded and external resources MAY coexist in one document. Distributing an
external-resource font requires distributing its resource directory as well.
Missing, malformed or incorrectly typed resources MUST be reported; silently
converting them into empty glyphs loses information.

## Embedded PNG

PNG data images are children of `data/photo`. Their XML text contains MIME
headers, a blank line and a Base64-encoded PNG, rather than a `data:` URL.

```xml
<data>
  <photo>
    <image id="pixel">
Content-Type: image/png
Content-transfer-encoding: base64

iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGNgAAIAAAUA
AXpeqz8AAAAASUVORK5CYII=
    </image>
  </photo>
</data>
```

The [complete PNG example](examples.md#embedded-png) supplies glyph metrics and
uses this transparent 1×1 PNG. `data/photo/image/@type`, if present, MUST be
`photo`; `photo` is otherwise implied by its container.

Writers MUST emit `Content-Type: image/png` and
`Content-transfer-encoding: base64` (MIME header names are case-insensitive).
Optional MIME parameters such as `name` or historical `charset=US-ASCII` do not
change the decoded image. `image/@id`, not MIME `name`, is the reference key.
Base64 MAY be wrapped across lines; whitespace is ignored. XML formatting
indentation and an initial newline before the headers are harmless.

Readers MUST decode Base64, check the PNG format and reject invalid image data.
The signature alone does not prove a complete PNG. Canonical files include the
blank line separating headers from the body; compatibility readers MAY accept
historical files without it. PNG transparency is supported; RGBA PNG is
recommended, while legal PNG colour types remain PNG. Shape bbox dimensions
describe a crop, so they need not equal the whole image's dimensions.

## External PNG

An external PNG is an ordinary binary PNG file. It has no MIME wrapper and no
entry in `data` is needed. Use `type="photo"` in the glyph image and `system`
in its shape. The same crop, baseline and PPM rules apply to embedded and
external PNGs.

## Embedded SVG

An embedded SVG resource is a **direct child of `data`**, outside `photo`, with
`type="svg"`. Its children are SVG graphics elements, not MIME or Base64 text.

```xml
<data>
  <image id="a-vector" type="svg">
    <g xmlns="http://www.w3.org/2000/svg" fill="#d13b42">
      <path d="M0 0 L300 -700 L600 0 L450 0 L300 -400 L150 0 Z" />
    </g>
  </image>
</data>
```

The Photofont data `image` acts as the container; do not replace it with SVG's
`image` element. A consumer can reconstruct a standalone SVG by placing its
children inside `<svg xmlns="http://www.w3.org/2000/svg">…</svg>`.
There is no required nested `<svg>` document or viewBox in the embedded form.

Use SVG user coordinates with positive Y downward. Embedded fragments are
baseline-origin graphics: a point 700 shape units above the baseline has
`y=-700`. For a fragment point `(sx, sy)` after its SVG transforms:

```text
font_x =  sx * U/P + shift_x
font_y = -sy * U/P + shift_y
```

For portable embedded SVG, writers SHOULD omit `bbox` and `base` and encode
placement in the fragment itself. A legacy reader ignores embedded SVG `base`;
this profile does not use it for embedded placement. SVG `bbox` metadata MUST
NOT implicitly crop the graphic.

### SVG feature expectations

Writers SHOULD use self-contained paths, groups, fills and transforms, with
explicit `Z` commands for closed contours. Colour and opacity belong to SVG
graphics/style attributes. Generic SVG applications support more than some
historical Photofont importers; there is no evidence that every reader supports
all SVG filters, masks, clipping, patterns, gradients, text or referenced images.
Readers MUST document unsupported features and report losses. They MUST NOT
execute scripts or follow external resource references while importing a font.

## External SVG

An external SVG resource is a complete SVG document with the SVG namespace and
its own viewport, for example `viewBox="0 0 600 700"`. Its matching Photofont
record uses `type="svg"` and `shape system="images/A.svg"`.
The shape's `base` identifies the glyph origin in SVG user units after viewport
mapping; when omitted, this profile uses `(0,0)`.

For SVG point `(sx, sy)` and base `(bx, by)`:

```text
font_x =  (sx - bx) * U/P + shift_x
font_y = -(sy - by) * U/P + shift_y
```

For an upright 600×700 graphic with its baseline at the bottom, use
`base x="0" y="700"`, `ppm int="1000"`, and header UPM 1000. The top then appears
700 font units above the baseline. The [external SVG example](examples.md#external-svg)
demonstrates this exact placement. Use a 1:1 viewport/viewBox mapping and unitless
geometry for portability; legacy viewport handling varies. Do not treat `bbox`
as a PNG crop when loading SVG.
