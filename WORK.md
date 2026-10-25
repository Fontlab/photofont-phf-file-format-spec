---
this_file: WORK.md
---

# Issue 101 work record

## Research and baseline

- Initial public tree contained only a title README and license; no test suite or
  documentation build existed. Owner changes: private-directory ignore rule,
  issue brief, local CodeGraph index and Finder metadata.
- Read historical June 2003 specification and older tutorial, FontGate reader,
  writer and records, GlyphsSDK importer/exporter, and embedded PNG/external SVG
  samples. CodeGraph had no relevant indexed implementation symbols.
- SVG resources occur in legacy documents declaring 1.0. No supplied standalone
  historical 2.0 standard establishes a new root version. The new spec must
  explicitly identify its 2.0 profile and distinguish it from implementation facts.
- Confirmed PNG crop and PPM scaling in reader/writer; SVG uses downward Y and
  external base offsets. Header descender is a positive depth. Older prose is
  ambiguous about bbox orientation; implementation equations take precedence here.
- Consulted official ProperDocs configuration, MaterialX package documentation,
  Python ElementTree/email documentation and both requested neighbouring sites.
- GitHub Pages already targets `main:/docs`. Publication is explicitly authorized.
- Native Codex goal is active. OMC story ledger tracks this work; no separate
  Claude goal is created in this Codex session.

## Verification and cleanup plan

- Keep the recipe API and four storage-mode fixtures fixed; use the 14 passing
  unit/integration/site tests as the regression lock.
- Bound the ai-slop-cleaner pass to new Python, build configuration and prose:
  remove dead/duplicated code if found; retain existing platform/MIME/XML helpers;
  add no abstraction or dependency for cleanup. Review the whole public file set
  directly for unsupported claims, incomplete snippets and privacy leaks.
- First fixture test run failed because fixtures did not yet exist. After adding
  them, a MIME indentation regression failed and was fixed with standard-library
  dedent. PNG was independently decoded/verified as 1×1 transparent RGBA.
- Site audit caught copied __pycache__ bytecode with an absolute source path.
  Added build exclusions and disabled bytecode writes during tests; the full
  14-test suite, link/fragment audit and privacy scan now pass.
- Native browser check initially used an over-specific heading name (the theme
  appends a permalink character); corrected the browser assertion. Preview port
  collision was avoided with a dedicated localhost static server.

## Final local verification and direct review

- `bash test.sh`: strict ProperDocs build and all 16 tests passed. Tests execute
  the documented Python snippets verbatim, inspect all four storage forms,
  reopen saved output, reject unsafe paths/entities and invalid numeric/MIME
  input, audit all site links/fragments, compare downloadable source bytes and
  exclude private material and Python caches from every generated file.
- `uv run --with ruff ruff check src_docs/md/examples/photofont.py tests`: passed.
- `uv run --with coverage coverage run --source=src_docs/md/examples -m unittest
  discover -s tests -v`, then `coverage report -m`: 83% recipe coverage; subprocess
  CLI tests also pass (their execution is outside that coverage percentage).
- Direct ai-slop-cleaner pass: no speculative wrapper/classes or dependencies
  added. Removed the optional repository-statistics widget, which requested a
  nonexistent release; retained a plain project-source link. Source inclusions
  keep the prose listings and downloadable examples identical.
- Direct code review: APPROVE; no remaining correctness/privacy blockers.
  Reviewed specification provenance, PNG equations and units, SVG baseline
  conventions, error paths, exact snippets, build exclusions and private-source
  boundary. Existing application compatibility is explicitly unclaimed.
- Chromium acceptance: all nine pages render; Pagefind search for "kerning"
  returns the mapping page; navigation, both theme toggles and mobile menu pass.
  Desktop 1440×1000 and mobile 390×844 have no horizontal page overflow, no
  JavaScript errors and no HTTP failures. Screenshots visually inspected.
- Local browser receipts and screenshots are retained in the ignored task
  ledger directory. 53 generated website files are ready for publication.
- The existing private-directory ignore rule is retained and will be committed
  with ignores for local task state, CodeGraph data and Finder metadata.

Publication remains pending until the pushed commit is served at the HTTPS URL.
