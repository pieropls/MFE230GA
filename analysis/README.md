# analysis/: v2 iteration code (post-hoc and forward test)

Layout follows `../CLAUDE.md`: small and flat. `run.ipynb` regenerates every number, table and figure top to bottom.

| File | Contents |
|---|---|
| `params.py` | Paths, windows, lags, portfolio settings (checked equal to the frozen study), variant registry |
| `data.py` | French group returns, FRED/ALFRED labor signals, read-only import of the frozen backtest |
| `stats.py` | Rank IC, Newey–West regression, performance, factor attribution, placebo, deflated Sharpe |
| `plots.py` | Every figure (vector PDF to `../report/figures/`), plus booktabs and markdown table writers |
| `run.ipynb` | Orchestration: data → Gate 1 → diagnostics D1–D10 → v2 variants → forward test |
| `v2_spec.md`, `v2_spec.sha256` | Post-hoc variants, frozen (hashed, timestamped, committed) before they were run |
| `forward/` | Forward-test spec and amendment 001 (both hashed), Q4 2026 book for V2a–V2d (`book_2026Q4.csv`, plus scores, hedge and netted-ETF versions), `etf_proxies.csv`. The weekly tracker is deferred. |
| `output/` | `validation.md` (Gate 1), `data_vintage.md`, `diagnostics_v2.md`, `v2_results.md`, `v2_run_log.md`, `gate3.md` (Gate 3), `tables/*.csv` |
| `data/` | Ken French files (CRSP 202608 build), FRED current values and ALFRED vintage, downloaded Oct 2026 |

How to run: `cd analysis` and open `run.ipynb` (pandas, numpy, scipy, scikit-learn, matplotlib). The frozen study in `../230ga-follow-the-workers/` is only read.

`output/diagnostics.md` is the 3 Oct baseline behind `docs/FINDINGS_AND_PROPOSAL.md`. It was produced by the earlier `diagnostics.py`, which you can recover with `git show 771e482:analysis/diagnostics.py` (it has since been folded into the notebook).
