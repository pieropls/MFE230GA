# v3 results: robustness battery for V2d (POST-HOC)

First run **2026-10-03T09:53:32+00:00** (regenerated 2026-10-04T09:55:17+00:00, outputs verified identical to the first run via v3_run_log.md). Spec `analysis/specs/study2_2_hq12_robustness.md` frozen at **2026-10-03T09:52:27+00:00** (sha256 `312aef1dd9551aa7044d37ccf8562a8e66cddfe741e0e1097c15cff18ed8bfde`). Deflated Sharpe ratios use N_trials = 132. Data: revised FRED values with fixed lags (`data_vintage.md`). Nothing here changes the confirmatory verdict (A3, Do not implement).

## Reading against the pre-declared rule (v3_spec.md section 3)

**fragile: R4**

| condition | holds |
|---|---|
| R1 hires-only and quits-only test Sharpe > 0 | True |
| R2 test 12m IC t >= 2 and 1m IC t < 2 | True |
| R3 holding 9 and 18 months test Sharpe > 0 | True |
| R4 both test halves Sharpe > 0 | False |
| R5 test break-even cost > 25 bp | True |
| R7 minimum drop-one test Sharpe > 0 | True |
| R9 90% interval excludes 0 (test or full) | True |

## R1 Components (held 12 months)

Source: `analysis/output/study2/tables/v3_r1_components.csv` (LaTeX `report/tables/v3_r1_components.tex`).

| Book (held 12 months) | Sharpe research | Sharpe test | Sharpe full | Test IC 12m (t) | Test alpha t |
|---|---|---|---|---|---|
| hires only | +0.41 | +0.19 | +0.27 | +0.093 (+2.90) | +0.79 |
| quits only | +0.18 | +0.16 | +0.15 | +0.085 (+1.75) | +0.81 |
| openings (contrast) | +0.10 | +0.42 | +0.29 | +0.082 (+1.38) | +1.48 |
| layoffs (contrast) | +0.11 | +0.16 | +0.13 | +0.032 (+0.87) | +0.69 |
| V2d = -(hires+quits)/2 | +0.50 | +0.29 | +0.35 | +0.096 (+2.43) | +1.37 |

## R2 Horizon profile: IC (t) of the V2d score

Source: `analysis/output/study2/tables/v3_r2_horizon_profile.csv` (LaTeX `report/tables/v3_r2_horizon_profile.tex`).

| Horizon | research | test | full |
|---|---|---|---|
| 1m | -0.016 (-0.59) | -0.020 (-0.87) | -0.019 (-1.08) |
| 3m | +0.005 (+0.18) | +0.007 (+0.18) | +0.005 (+0.21) |
| 6m | -0.004 (-0.11) | +0.017 (+0.40) | +0.006 (+0.20) |
| 9m | +0.023 (+0.48) | +0.069 (+1.98) | +0.046 (+1.52) |
| 12m | +0.047 (+0.90) | +0.096 (+2.43) | +0.071 (+2.06) |
| 18m | +0.038 (+0.59) | +0.085 (+2.00) | +0.059 (+1.41) |
| 24m | +0.009 (+0.11) | +0.063 (+1.86) | +0.034 (+0.72) |

## R3 Holding period: Sharpe by window

Source: `analysis/output/study2/tables/v3_r3_holding.csv` (LaTeX `report/tables/v3_r3_holding.tex`).

| Holding | research | test | full | post-2010 | last 18m | Test turnover |
|---|---|---|---|---|---|---|
| 6 months | +0.31 | +0.05 | +0.15 | +0.05 | +0.50 | 0.49 |
| 9 months | +0.43 | +0.14 | +0.24 | +0.16 | +0.29 | 0.40 |
| 12 months | +0.50 | +0.29 | +0.35 | +0.30 | +0.29 | 0.37 |
| 18 months | +0.58 | +0.30 | +0.38 | +0.34 | +0.31 | 0.28 |

## R4 Sub-periods

Source: `analysis/output/study2/tables/v3_r4_subperiods.csv` (LaTeX `report/tables/v3_r4_subperiods.tex`).

| Window | Months | Sharpe | Net p.a. | IC 12m (t) |
|---|---|---|---|---|
| test: first half | 71 | -0.21 | -1.4% | +0.097 (+1.75) |
| test: second half | 71 | +0.64 | +6.5% | +0.095 (+1.60) |
| test: excl. Mar 2020-Dec 2021 | 120 | +0.37 | +3.0% | +0.105 (+2.23) |
| test: pre-2020 | 62 | +0.14 | +0.8% | +0.114 (+1.92) |
| test: 2020 onward | 80 | +0.37 | +3.9% | +0.080 (+1.54) |
| full: first half | 134 | +0.33 | +2.0% | +0.038 (+0.73) |
| full: second half | 134 | +0.38 | +3.3% | +0.107 (+2.66) |
| full: excl. Mar 2020-Dec 2021 | 246 | +0.40 | +2.9% | +0.073 (+1.93) |
| full: pre-2020 | 188 | +0.36 | +2.2% | +0.068 (+1.57) |

## R5 Costs

Source: `analysis/output/study2/tables/v3_r5_costs.csv` (LaTeX `report/tables/v3_r5_costs.tex`).

| Window | 0 bp | 10 bp | 25 bp | 50 bp | Break-even (bp) |
|---|---|---|---|---|---|
| research | +0.58 | +0.50 | +0.39 | +0.20 | 76 |
| test | +0.34 | +0.29 | +0.22 | +0.09 | 68 |
| full | +0.41 | +0.35 | +0.26 | +0.11 | 69 |
| post-2010 | +0.35 | +0.30 | +0.21 | +0.07 | 63 |
| last 18m | +0.32 | +0.29 | +0.24 | +0.16 | 99 |

## R6 Factor regression, HAC 12 lags

Source: `analysis/output/study2/tables/v3_r6_alpha.csv` (LaTeX `report/tables/v3_r6_alpha.tex`).

| Factor | Test (HAC 12) | Full (HAC 12) |
|---|---|---|
| Alpha (per month) | +0.26% (+1.48) | +0.26% (+1.92) |
| Market | +0.03 (+0.58) | -0.00 (-0.08) |
| SMB | -0.17 (-2.24) | -0.02 (-0.31) |
| HML | +0.12 (+1.07) | +0.10 (+1.23) |
| RMW | -0.36 (-4.45) | -0.16 (-1.83) |
| CMA | -0.01 (-0.07) | -0.09 (-0.87) |
| Momentum | -0.12 (-1.14) | -0.03 (-0.51) |
| Industry momentum | +0.02 (+0.17) | +0.06 (+0.93) |

## R7 Drop one industry (summary)

Source: `analysis/output/study2/tables/v3_r7_dropone_summary.csv` (LaTeX `report/tables/v3_r7_dropone_summary.tex`).

| statistic | Test Sharpe | Full Sharpe |
|---|---|---|
| minimum | +0.18 | +0.23 |
| median | +0.30 | +0.34 |
| maximum | +0.48 | +0.54 |
| all 13 groups (V2d) | +0.29 | +0.35 |
| industry whose removal lowers test Sharpe most | Health care |  |
| industry whose removal raises test Sharpe most | Real estate |  |

## R8 Tightness moderator

Source: `analysis/output/study2/tables/v3_r8_tightness.csv` (LaTeX `report/tables/v3_r8_tightness.tex`).

| Window: regime | Months | Sharpe | Net p.a. | IC 12m (t) |
|---|---|---|---|---|
| test: T rising | 88 | -0.00 | -0.0% | +0.115 (+2.52) |
| test: T falling | 54 | +0.66 | +6.8% | +0.061 (+1.02) |
| test: V/U > 1 | 75 | +0.72 | +6.0% | +0.103 (+2.00) |
| test: V/U < 1 | 67 | -0.14 | -1.2% | +0.088 (+1.59) |
| full: T rising | 182 | +0.06 | +0.4% | +0.048 (+1.19) |
| full: T falling | 86 | +0.83 | +7.6% | +0.126 (+2.19) |
| full: V/U > 1 | 75 | +0.72 | +6.0% | +0.103 (+2.00) |
| full: V/U < 1 | 193 | +0.19 | +1.4% | +0.059 (+1.40) |

## R9 Block-bootstrap 90% interval

Source: `analysis/output/study2/tables/v3_r9_bootstrap.csv` (LaTeX `report/tables/v3_r9_bootstrap.tex`).

| Window | Sharpe | 90% interval | Months | Excludes 0 |
|---|---|---|---|---|
| test | +0.29 | [-0.07, +0.65] | 142 | no |
| full | +0.35 | [+0.05, +0.64] | 268 | yes |

## R10 As-known data

Source: `analysis/output/study2/tables/v3_r10_asknown.csv` (LaTeX `report/tables/v3_r10_asknown.tex`).

| check | status | note |
|---|---|---|
| R10 as-known (ALFRED vintage) rerun of V2a-V2d | not run: no key | analysis/.env has no FRED_API_KEY; historical v2/v3 results use revised data with fixed lags (data_vintage.md) |

## R11 Fundamental law (test window)

Source: `analysis/output/study2/tables/v3_r11_fundamental_law.csv` (LaTeX `report/tables/v3_r11_fundamental_law.tex`).

| Book (test window) | IC | Horizon | BR/yr | TC | Implied IR | Ceiling (TC=1) | Realised Sharpe |
|---|---|---|---|---|---|---|---|
| A3 primary | -0.021 | 1m | 156 | 0.80 | -0.21 | -0.27 | -0.58 |
| V2a wage growth | +0.049 | 1m | 156 | 0.91 | +0.56 | +0.62 | +0.16 |
| V2d -(hires+quits) 12m | +0.096 | 12m | 13 | 0.48 | +0.17 | +0.35 | +0.29 |

## Deflated Sharpe at 112 vs 132 trials

Source: `analysis/output/study2/tables/v3_dsr132.csv` (LaTeX `report/tables/v3_dsr132.tex`).

| Variant | Window | DSR (112 trials) | DSR (132 trials) | Benchmark Sharpe (132) |
|---|---|---|---|---|
| V2a | test | 0.02 | 0.02 | 0.76 |
| V2a | full | 0.03 | 0.03 | 0.56 |
| V2b | test | 0.00 | 0.00 | 0.76 |
| V2b | full | 0.00 | 0.00 | 0.56 |
| V2c | test | 0.09 | 0.08 | 0.76 |
| V2c | full | 0.16 | 0.15 | 0.56 |
| V2d | test | 0.06 | 0.05 | 0.76 |
| V2d | full | 0.18 | 0.16 | 0.56 |

## R7 full list

| industry | dropped_group | test_sharpe | full_sharpe |
|---|---|---|---|
| Mining & logging | 1 | 0.325 | 0.251 |
| Construction | 2 | 0.299 | 0.339 |
| Durable mfg | 3 | 0.299 | 0.304 |
| Nondurable mfg | 4 | 0.399 | 0.365 |
| Wholesale | 5 | 0.361 | 0.365 |
| Retail | 6 | 0.287 | 0.349 |
| Transport & utilities | 7 | 0.303 | 0.343 |
| Information | 8 | 0.408 | 0.539 |
| Finance & insurance | 9 | 0.23 | 0.231 |
| Real estate | 10 | 0.477 | 0.429 |
| Prof. & business svcs | 11 | 0.257 | 0.333 |
| Health care | 12 | 0.184 | 0.363 |
| Accommodation & food | 13 | 0.319 | 0.285 |

## Figures

- `report/figures/fig_horizon_profile.pdf` (R2), `fig_v2d_holding.pdf` (R3), `fig_v2d_dropone.pdf` (R7), `fig_v2d_tightness.pdf` (R8); V2d added to `fig_loadings.pdf` (R6).
