# analysis/: Study 2 (the post-hoc iteration) and the diagnostics of Study 1

Small and flat. `run.ipynb` regenerates every number, table and figure top to bottom in about one minute and stops with `output/STOP.md` if a gate fails. Names: Study 1 is Alex's preregistered study in `../study1_preregistered/` (read-only); Study 2.1 is the four variants W, SC, W+MOM and HQ12 (stored as V2a to V2d inside the older result files), Study 2.2 the HQ12 battery, Study 2.3 the additional robustness.

| File | Contents |
|---|---|
| `params.py` | Paths, windows, lags, portfolio settings (checked equal to Study 1's), the Study 1 folder's fingerprint, names |
| `data.py` | French group returns, FRED/ALFRED labor signals with fixed publication lags, as-known features from Alex's panel, read-only import of Study 1's backtest, and a variant engine (gross cap, rank weights) that reproduces it |
| `stats.py` | Rank IC, Newey-West regression, performance, factor attribution, circular-shift placebo, deflated Sharpe, block bootstrap |
| `plots.py` | Every figure (vector PDF to `../report/figures/`), plus booktabs and markdown table writers |
| `run.ipynb` | Data, Gate 1, Study 1 diagnostics D1-D10, Study 2.1, forward test, Gate 3, Study 2.2, Gate 2, Study 1 robustness, Study 2.3 (R1-R9), report tables, Gate 4 |
| `llm_runs.py` | The model calls of Study 2.3 (R8 judge with a quote, R9 feedback ablation); run once, logged, read by the notebook |
| `specs/` | Every specification, hashed before it ran: `study2_1_variants`, `study2_2_hq12_robustness`, `study2_3_robustness`, `forward_spec`, `forward_amendment_001` (each `.md` with its `.sha256`) |
| `output/study1/` | `validation.md` (Gate 1), `data_vintage.md`, `diagnostics_v2.md`, `robustness.md`, `tables/d*.csv` |
| `output/study2/` | `v2_results.md` and `v3_results.md` (Studies 2.1 and 2.2), `robustness_2_3.md`, the three run logs, `gate2.md`, `gate4.md`, `asknown_features.csv`, `llm/` call logs, `tables/*.csv` |
| `output/forward/` | Q4 2026 book for W, SC, W+MOM and HQ12 (`book_2026Q4.csv`, plus scores, hedge and netted-ETF versions), `etf_proxies.csv`, `book_first_build.sha256`, `gate3.md` |
| `data/` | Ken French files (CRSP 202608 build), FRED current values and the ALFRED vintage of 29 Sep 2026 |
| `data/alex_package/` | Alex Roesler's data package (as-known panels, full ALFRED vintages, saved outputs of both of his studies; 1,191 files verified against his `DATA_INVENTORY.json`). Read-only and optional: when it is absent the notebook reads the as-known features saved in `output/study2/asknown_features.csv` |

How to run: from the project root, `jupyter nbconvert --to notebook --execute --inplace analysis/run.ipynb`, or open the notebook and run all cells (kernel `python3`, packages in `../requirements.txt`). Use `python3 -B` or `PYTHONDONTWRITEBYTECODE=1` so no `__pycache__` is written into the Study 1 folder, whose file count is part of Gates 2 and 4.

Run logs: `output/study2/v2_run_log.md`, `v3_run_log.md` and `study2_3_run_log.md` record the SHA-256 of each result table at its first run; the notebook recomputes them every run and stops if any differs. `output/forward/book_first_build.sha256` does the same for the Q4 book.

`output/study1/diagnostics.md` is the 3 Oct baseline behind `../docs/FINDINGS_AND_PROPOSAL.md`. It was produced by the earlier `diagnostics.py`, which you can recover with `git show f6c95ef:analysis/diagnostics.py` (it has since been folded into the notebook).
