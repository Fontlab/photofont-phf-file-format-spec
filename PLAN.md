---
this_file: PLAN.md
---

# Issue 101 plan

Deliver an original Photofont 2.0 XML specification, executable examples, and a
ProperDocs/MaterialX website using fltheme26, then publish and check the live site.

1. Read the historical specification, both implementations and representative
   PNG/SVG fonts. Separate historical evidence from new 2.0 interoperability rules.
2. Specify document structure, header, mappings, kerning, metrics, resource storage,
   PNG and SVG coordinates, version compatibility and reader/writer requirements.
3. Supply synthetic embedded/external PNG/SVG examples and tested Python recipes.
4. Configure `src_docs/mkdocs.yml`, Markdown in `src_docs/md/`, output in `docs/`.
   Reuse neighbouring sites' MaterialX and versioned fltheme26 configuration.
5. Run examples, tests, strict site build, link/privacy checks and browser checks.
6. Review and simplify directly; commit only public deliverables, push, verify
   GitHub Pages deployment and the actual HTTPS site including its downloads.

Acceptance evidence is recorded in WORK.md. No private implementation or sample
font is redistributed. Existing owner changes remain intact.

Steps 1–5 are complete. Step 6 has passed direct review and awaits publication
and verification of the deployed content.
