---
this_file: WORK.md
---

# Issue 101 work record

## 2026-11-24 local verification

The worktree uses fly-january 0.2.1 with FontLab chrome labelled “Photofont 2.0”.
The theme migration passed the Python 3.13 strict build with zero warnings and
all 16 tests in `bash test.sh`. The latest check ran against the existing
`docs/` output and passed all 16 tests.

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python -m unittest discover -s tests -v
```

The original publication, browser checks and file comparisons are documented
in the [October 25 work record](https://github.com/Fontlab/photofont-phf-file-format-spec/blob/5afb1839ddd51e044d0c1b153dd9a012c84034f2/WORK.md).
