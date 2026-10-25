#!/usr/bin/env bash
# this_file: build.sh
set -euo pipefail
cd "$(dirname "$0")"
uv run --frozen properdocs build --strict --config-file src_docs/mkdocs.yml
touch docs/.nojekyll
