# analysis/: v2 iteration code (post-hoc and forward test)

Layout: small and flat. `run.ipynb` regenerates every number, table and figure top to bottom in about 35 s and stops with `output/STOP.md` if a gate fails.

| File | Contents |
|---|---|
| `params.py` | Paths, windows, lags, portfolio settings (checked equal to the frozen study), the frozen folder's fingerprint, variant registry |
| `data.py` | French group returns, FRED/ALFRED labor signals with fixed publication lags, read-only import of the frozen backtest |
| `stats.py` | Rank IC, Newey–West regression, performance, factor attribution, circular-shift placebo, deflated Sharpe, block bootstrap |
| `plots.py` | Every figure (vector PDF to `../report/figures/`), plus booktabs and markdown table writers |
| `run.ipynb` | Orchestration: data → Gate 1 → diagnostics D1–D10 → v2 variants → forward test → Gate 3 → v3 battery → Gate 2 |
| `v2_spec.md`, `v2_spec.sha256` | Four post-hoc variants and the reading rule, frozen (hashed, timestamped, committed) before they were run |
| `v3_spec.md`, `v3_spec.sha256` | V2d robustness battery R1–R11, frozen before it was run |
| `forward/` | Forward-test spec and amendment 001 (both hashed), Q4 2026 book for V2a–V2d (`book_2026Q4.csv`, plus scores, hedge and netted-ETF versions), `etf_proxies.csv`, `book_first_build.sha256`. The weekly tracker is deferred. |
| `output/` | `validation.md` (Gate 1), `data_vintage.md`, `diagnostics_v2.md`, `v2_results.md`, `v2_run_log.md`, `v3_results.md`, `v3_run_log.md`, `gate2.md`, `gate3.md`, `tables/*.csv` |
| `data/` | Ken French files (CRSP 202608 build), FRED current values and the ALFRED vintage of 29 Sep 2026, downloaded Oct 2026 |

How to run: from the project root, `jupyter nbconvert --to notebook --execute --inplace analysis/run.ipynb`, or open the notebook and run all cells (kernel `python3`, packages in `../requirements.txt`). Use `python3 -B` or `PYTHONDONTWRITEBYTECODE=1` so no `__pycache__` is written into the frozen folder, whose file count is part of Gate 2. The frozen study in `../230ga-follow-the-workers/` is only read.

Run logs: `output/v2_run_log.md` and `output/v3_run_log.md` record the SHA-256 of each output at its first run; the notebook recomputes them every run and stops if any differs. `forward/book_first_build.sha256` does the same for the Q4 book.

`output/diagnostics.md` is the 3 Oct baseline behind `../docs/FINDINGS_AND_PROPOSAL.md`. It was produced by the earlier `diagnostics.py`, which you can recover with `git show f6c95ef:analysis/diagnostics.py` (it has since been folded into the notebook).
