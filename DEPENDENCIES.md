---
this_file: DEPENDENCIES.md
---

# Dependencies

Exact resolved versions are in `uv.lock`.

| Package | Purpose |
| --- | --- |
| ProperDocs | Build the static site from Markdown and YAML. |
| mkdocs-materialx | Documentation navigation, search and code presentation. |
| pymdown-extensions | Highlighted fenced code and Markdown snippets. |
| defusedxml | Parse XML examples while rejecting DTD/entity declarations. |

Python's standard library supplies XML writing, MIME header parsing, strict
Base64 decoding, paths, argument parsing and unit tests. No font rasterizer is
needed for the recipes. The website loads the versioned fltheme26 CSS/JS assets
from `i.fontlab.com`, following the neighbouring FontLab documentation sites.
