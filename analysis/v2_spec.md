# v2 specification: frozen before any v2 result was computed

**Label: POST-HOC.** These variants were chosen on 3 Oct 2026. By then the frozen study's test period had been opened and about 108 diagnostic looks had been taken on the same sample (`FINDINGS_AND_PROPOSAL.md`, `analysis/output/diagnostics.md`, `analysis/output/diagnostics_v2.md`).

The rules for this file:
- It is hashed (SHA-256, in `analysis/v2_spec.sha256`) and committed before the variants run.
- Each variant runs once. All four are reported, whatever they show.
- Nothing in this file changes after results exist.

No post-hoc result can change the confirmatory verdict. That verdict stays: primary A3, test Sharpe −0.58, **Do not implement**.

Code at freeze (commit `a0bdff3`):
- `analysis/params.py` sha256 `1d9617fef447c3121e6a106e17ab62878b12cc094f7bc709f177fa6ae868724e`;
- `analysis/data.py` `5275fe7ef82bc563605a1e6a94af883f8a5beeff3bef6b5d122b379ec5c6cad3`;
- `analysis/stats.py` `8e02fce7b80c099d8fbd4765e6a0373958e08e6a0aa22fca352cf79e362eee70`.

The variant cells are added to `analysis/run.ipynb` after this commit. They may only implement what is written here.

## 1. Data

- **Returns.** Ken French 49 industry portfolios, CRSP 202608 build (`analysis/data/french/`), aggregated into the frozen study's 13 groups with prior-month market-cap weights. Gate 1 showed these equal the frozen study's group returns to 1e-16. The target is the group excess return minus the cross-sectional mean (relative return).
- **Labor data.** Current (revised) FRED values downloaded 3 Oct 2026 (`analysis/data/fred/`), with fixed publication lags:
  - JOLTS observation month d−2 at decision month d;
  - CES observation month d−1;
  - tightness from month d−2, using the latest month in which both series are observed.
  - See `analysis/output/data_vintage.md`. This is the frozen study's FIXEDLAG construction, not as-known (ASOF) data.
- **Signals** (exactly `analysis/data.py::signals` at the commit above), at decision month d, known at the end of month d:
  - F1 openings, F2 hires, F3 quits, F4 layoffs: avg3(rate, m_J) − avg3(rate, m_J−12);
  - F5 hours: log avg3(H, m_C) − log avg3(H, m_C−12);
  - **W wage growth**: log avg3(E, m_C) − log avg3(E, m_C−12), with E the CES average hourly earnings (construction uses CES2000000008, as in the frozen study).
  - Each raw signal is divided by its group's expanding standard deviation (at least 24 months, history from decision month Apr 2002), z-scored across the 13 groups and winsorised at ±3. A missing group is set to 0 only when at least 11 groups are observed; otherwise the month has no signal.
  - z(·) denotes this standardised value.
- **Industry momentum 12-1** (Mom): compounded total return of each group over months m−12 to m−2. This skips month m−1, matching the frozen information rule (latest full return month m−2).
- csrank(·) is the cross-sectional percentile rank (average ranks for ties).

## 2. The four variants (score s_{m,g} for earning month m, group g)

| Variant | Score | Holding |
|---|---|---|
| **V2a (headline)** | s = csrank(z(W)) | 3 tranches (3 months) |
| V2b | s = (1/6) Σ_k sign(IC_k^res) · z_k over k ∈ {F1, F2, F3, F4, F5, W} | 3 tranches |
| V2c | s = ( csrank(z(W)) + csrank(Mom) ) / 2 | 3 tranches |
| V2d | s = −( z(F2) + z(F3) ) / 2 | **12 tranches (12 months)** |

- **IC_k^res** is the mean monthly rank IC of z_k against next-month relative returns over earning months May 2004 to Sep 2014. It is computed inside the script, once, from research-period data only. The six signs are written into the results; a sign of exactly zero would map to +1.
- **Ties** (groups 9 and 10 share their CES series, so their W is identical) are broken by the frozen backtest's stable ordering of group IDs.

## 3. Portfolio (identical for every variant)

The frozen study's `data.backtest`, imported read-only:
- each month, a new tranche goes long the top 3 and short the bottom 3 groups by score, at ±1/3 each;
- the book is the average of the last H tranches (H = 3 for V2a–V2c, H = 12 for V2d);
- market beta hedge from 60 months ending in m−2 (at least 36);
- 10% annual volatility target using a Ledoit–Wolf covariance over the same window, with gross exposure capped at 2;
- costs of 10 bp per unit of traded industry weight and 2 bp on hedge trades; borrow and financing 0.

A month whose score is missing or constant across groups opens no new tranche.

## 4. Backtest runs and windows

- **One run per variant and cost level.** A single continuous backtest runs over earning months May 2004 to Aug 2026, at industry costs of 0, 10 and 25 bp (hedge 2 bp in all). The 10 bp run is the base case.
- **Windows are slices of that one ledger:**

| Window | Earning months | Months |
|---|---|---|
| research | 2004-05 .. 2014-09 | 125 |
| test | 2014-11 .. 2026-08 | 142 |
| full | 2004-05 .. 2026-08 | 268 |
| post-2010 | 2010-01 .. 2026-08 | 200 |
| last 18m | 2025-03 .. 2026-08 | 18 |

  October 2014 belongs to full and post-2010, but to neither research nor test, as in the frozen study.

## 5. Statistics reported for every variant (all five windows unless noted)

1. **Sharpe ratio**: 12 × mean monthly net excess return ÷ (√12 × s.d.).
2. **Net return**: 12 × mean monthly net excess return.
3. **Volatility**: √12 × s.d. of monthly net excess returns.
4. **Maximum drawdown** of funded wealth (risk-free rate + net), within the window.
5. **Hit rate**: share of months with positive net excess return.
6. **IC**: mean monthly 1-month rank IC with Newey–West t (6 lags). Also the IC at the holding horizon, with t from h + 5 lags: h = 3 for V2a–V2c, h = 12 for V2d, using the h-month compounded relative return.
7. **Factor alpha**: intercept, per month, with Newey–West t (6 lags). From regressing 10 bp net returns on Mkt-RF, SMB, HML, RMW, CMA, Mom and the frozen group-momentum factor. In the 18-month window it is reported but not interpreted.
8. **Cost sensitivity**: Sharpe at 0, 10 and 25 bp.
9. **Turnover**: mean monthly traded industry weight (10 bp run).
10. **Placebo**: circular-shift p-value for the 1-month mean IC.
    - Scores are rolled against returns within the window by every shift from 24 to n−24 months; p is the share of shifted mean ICs at or above the actual one.
    - Definitions and V2b signs stay fixed under the shift.
    - Undefined for last 18m (no admissible shift).
11. **Deflated Sharpe ratio** (Bailey and López de Prado, 2014) on 10 bp monthly net returns, with **N_trials = 112**.
    - The trial variance of the monthly Sharpe ratio is set to 1/T (its null sampling variance over the window's T months), because most earlier looks were ICs, not Sharpe ratios.
    - Skewness and kurtosis are adjusted as in the frozen `stats.deflated_sharpe`.
12. **P&L by industry**: sum of monthly contributions w_g · r^e_g for each group, plus the market hedge and costs, for the test and full windows.

**Contrast bars** in `fig_v2_windows.pdf` are the frozen A3 primary (CONFIRMATORY). They come from:
- research: `research_summary.json`, 88 months, Jun 2007 to Sep 2014;
- test and last 18m: `results.json` → windows;
- full and post-2010: `results.json` → course_windows, a descriptive mix of research and test.

## 6. Reading rule, fixed now

A variant is called **"consistent with a real effect, to be forward-tested"** only if, in the **test** window, it meets all of:
- net Sharpe above 0 at 25 bp;
- 1-month IC t ≥ 2.0;
- factor-alpha t ≥ 2.0;
- positive mean IC in both halves of the test window;
- placebo p < 0.05;
- deflated Sharpe ratio above 0.95.

These mirror the frozen gate (prediction, incremental alpha, robustness, implementability), plus deflation.

Otherwise it is reported as **"not distinguishable from noise after the looks already taken"**, whatever its point estimates.

Passing would **not** change the verdict to "Implement". This is post-hoc work, and the only clean holdout left is the future (Part 3, step C).

## 7. Outputs

- `analysis/output/v2_results.md`: every statistic above, with the source file of each.
- `analysis/output/tables/v2_*.csv`.
- `report/tables/v2_results.tex`: compact summary with Sharpe by window, plus test-window IC (t), alpha t, placebo p and DSR.
- `report/figures/fig_v2_windows.pdf`.
- V2a (10 bp, test window) added to `fig_cumulative.pdf` (dashed, post-hoc colour) and to `fig_loadings.pdf`.

## 8. Forward test, decided now and independent of the v2 results

The forward test uses **V2a as headline and V2b as secondary**, with the V2b signs computed under §2.
- It is frozen in `analysis/forward/spec_frozen.md` before any return of the holding period beyond those already printed on 1–2 Oct 2026 is known.
- The decision date is 30 Sep 2026. It uses ALFRED values as published on 29 Sep 2026: JOLTS through July 2026, CES through August 2026.
