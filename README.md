---
this_file: README.md
---

# Photofont 2.0 XML specification

Specification and original examples for Photofont XML fonts with PNG and SVG
glyphs. The original Photofont 1.0 specification supported PNG, without SVG;
this site distinguishes later SVG-capable legacy files from the explicit 2.0
profile defined here.

Read the [published specification](https://fontlab.dev/photofont-phf-file-format-spec/)
or start at [the Markdown overview](src_docs/md/index.md).

## Build and test

Install [uv](https://docs.astral.sh/uv/), then run with Python 3.12 or later:

```sh
bash test.sh
```

This runs a strict documentation build and the Python recipe/site tests.
`bash build.sh` only builds the website. Preview with:

```sh
uv run --frozen properdocs serve --config-file src_docs/mkdocs.yml
```

| Path | Purpose |
| --- | --- |
| `src_docs/mkdocs.yml` | ProperDocs configuration with MaterialX and fltheme26 |
| `src_docs/md/` | Markdown source and downloadable original examples |
| `docs/` | Generated static website, published by GitHub Pages from `main:/docs` |
| `tests/` | Executable recipe and resource checks |

The site is built with ProperDocs; the config filename remains `mkdocs.yml`.
Exact dependencies are locked in `uv.lock`. Run `bash build.sh` before committing
documentation changes, and commit the resulting `docs/` directory with sources.

Private research material is excluded from publication. Public examples are
synthetic and covered by [MIT](LICENSE). See
[sources and status](src_docs/md/sources.md) for the specification's evidence and
the limits of legacy application compatibility.
