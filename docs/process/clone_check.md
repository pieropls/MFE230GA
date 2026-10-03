# Fresh-clone check (3 Oct 2026, final)

A plain clone of the public repository, run from a temporary folder on the same machine and deleted afterwards. No submodule, no access to Alex's private repository: his study is part of this repository's history (`frozen_provenance.md`).

```
git clone https://github.com/pieropls/GA.git gh_clone        # commit 0d05ba4
```

| Check | Result |
|---|---|
| Authors in `git log` | `pieropls` (31 commits) and `Aroesler1 <183014507+Aroesler1@users.noreply.github.com>` (2 commits: `8a520b0`, `c67c486`) |
| Frozen tree | `230ga-follow-the-workers/` has 3,067 files; `git diff c67c486 HEAD:230ga-follow-the-workers` is empty |
| Fingerprint in the clone | `eb109be96917…`, 3,067 files (Gate 2 row "Frozen repo unchanged": True) |
| `analysis/run.ipynb` top to bottom (nbclient, `python3 -B`) | 34 s, no `STOP.md`; Gate 1 PASS, Gate 3 PASS, Gate 2 PASS |
| v2 / v3 tables, placebo, signs and the four Q4 book files | 25 of 25 byte-identical to the pushed tree (the run logs check every v2/v3 table on each run) |
| `results/build_results_book.py` | 106 claims, 0 unverified |
| `report/check_sources.py`, `latexmk -pdf main.tex` | clean; `main.pdf` 22 pages, 0 errors |
| `results/results_book.tex` | builds |
| Files the run modifies in a clean clone | `analysis/run.ipynb` outputs, `report/figures/*.pdf` (PDF timestamps), `analysis/output/*.md` (run timestamps); no table, CSV or book changes |
| Left behind | no `__pycache__` (use `python3 -B`) |

Environment: Python 3.12.5, packages as in `analysis/output/environment.txt`. Byte identity of the run logs is expected in that environment; a different BLAS build may differ in the last bit (OPEN_ISSUES.md #7).

Earlier check (same day, superseded): a local clone with `--recurse-submodules` when the frozen study was still a submodule; it passed the same checks.
