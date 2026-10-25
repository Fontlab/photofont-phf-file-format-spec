#!/usr/bin/env bash
# this_file: test.sh
set -euo pipefail
cd "$(dirname "$0")"
bash build.sh
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python -m unittest discover -s tests -v
