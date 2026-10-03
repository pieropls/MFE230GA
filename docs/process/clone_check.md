# Fresh-clone check (Stage 5, 3 Oct 2026)

Done from a temporary directory on the same machine, from the local repository at commit `05e73fa` (no GitHub remote was configured; see HANDOFF.md for the push commands). The temporary clone was deleted afterwards.

```
git clone --recurse-submodules <local repo> clone_check      # 2.3 s
```

| Check | Result |
|---|---|
| Submodule `230ga-follow-the-workers` resolved from `https://github.com/Aroesler1/230ga-follow-the-workers.git` and pinned at `c67c486` | yes (`git submodule status`: ` c67c486d3eec759f07c85a03fd62a0f711b09140 230ga-follow-the-workers (heads/main)`) |
| Frozen fingerprint in the clone | 3,067 files, `eb109be96917...` (Gate 2 row "Frozen repo unchanged": True) |
| `analysis/run.ipynb` top to bottom (nbclient, `python3 -B`) | 32 s, no `STOP.md`; Gate 1, Gate 3 and Gate 2 PASS |
| v2 / v3 tables and the Q4 book byte-identical to the committed files | yes (`cmp` on `v2_window_stats.csv`, `v3_r9_bootstrap.csv`, `book_2026Q4.csv`; the run logs check all 19 tables) |
| `results/build_results_book.py` | 106 claims, 0 unverified |
| `report/check_sources.py` and `latexmk -pdf main.tex` | clean; `main.pdf` 21 pages |
| Files the run modifies in a clean clone | `analysis/run.ipynb` (outputs), `report/figures/*.pdf` (PDF timestamps), `analysis/output/*.md` (run timestamps); no table, CSV or book changes |

Environment: Python 3.12.5, packages as in `analysis/output/environment.txt`. Not tested: a machine without cached GitHub credentials for Alex's private repository (the submodule clone needs read access to it), and a different BLAS build (byte identity of the run logs is expected only in the recorded environment; see OPEN_ISSUES.md #7).
