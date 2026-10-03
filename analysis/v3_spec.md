# v3 specification: robustness battery for V2d, frozen before running

**Label: POST-HOC.** Written on 3 Oct 2026 after the v2 results (`analysis/output/v2_results.md`) had been seen. Its purpose is to find out whether the V2d finding survives, not to raise its Sharpe ratio. It is hashed (`analysis/v3_spec.sha256`) and committed before any check runs. Every check is run once and reported whatever it shows. Nothing in this file changes after results exist.

The confirmatory verdict is unaffected: primary A3, test Sharpe −0.58, **Do not implement**.

## 0. Object under test

**V2d** as frozen in `analysis/v2_spec.md` §2: score s = −(z(F2) + z(F3))/2, where F2 is the 12-month change in the 3-month-average hires rate and F3 the same for the quits rate, each standardised as in `analysis/data.py::signals`; held in 12 monthly tranches; frozen-study portfolio construction (60-month beta hedge, 10% volatility target, gross cap 2, 10 bp industry costs, 2 bp hedge costs). Data: revised FRED values with fixed lags (`data_vintage.md`, option c); Ken French returns, CRSP 202608 build.

Windows as in v2: research (2004-05..2014-09), test (2014-11..2026-08), full (2004-05..2026-08), post-2010, last 18m. "Sharpe" means annualised net Sharpe at 10 bp unless stated.

## 1. Multiple-testing accounting

v2 used N_trials = 112. This battery adds **20 new portfolio variants** (R1: 4 single-signal books; R3: 3 holding periods other than 12; R7: 13 drop-one-industry books), so every deflated Sharpe ratio reported from here on uses **N_trials = 132**. Sub-period, cost, regime and horizon splits of the same V2d book are not counted as new variants. The trial variance stays 1/T as in v2.

## 2. The checks (exactly these)

| ID | Check | Output |
|---|---|---|
| R1 | **Components.** Four single-signal books, each −z(Fk) held 12 months like V2d: hires only (−z(F2)), quits only (−z(F3)); for contrast openings (−z(F1)) and layoffs (−z(F4)). Sharpe, 12-month IC with HAC t (lags 17), alpha t, for research, test and full. | `v3_r1_components.csv` |
| R2 | **Horizon profile.** Rank IC of the V2d score against the h-month compounded relative return for h = 1, 3, 6, 9, 12, 18, 24, with HAC t (lags h+5), for research, test and full. Months lacking a complete h-month return drop out. | `v3_r2_horizon_profile.csv`, `fig_horizon_profile.pdf` |
| R3 | **Holding period.** Same score and construction, held 6, 9, 12 and 18 months. Sharpe by window, test turnover. | `v3_r3_holding.csv`, `fig_v2d_holding.pdf` |
| R4 | **Sub-periods** of the V2d 10 bp ledger: test first half (71 months) and second half; test excluding Mar 2020–Dec 2021; pre-2020 (test months before Jan 2020) and post-2020 (Jan 2020 onward); plus the same splits of the full sample where defined. Sharpe, 12-month IC, months. | `v3_r4_subperiods.csv` |
| R5 | **Costs.** Sharpe at 0, 10, 25 and 50 bp industry costs (hedge 2 bp throughout), by window; break-even industry cost = 1e4 × Σ net(0 bp) / Σ industry turnover over the window. | `v3_r5_costs.csv` |
| R6 | **Factor alpha.** Regression of V2d 10 bp net returns on Mkt-RF, SMB, HML, RMW, CMA, Mom and the frozen group-momentum factor with **HAC lags = 12**, test and full: alpha with t, loadings with t. V2d is added to `fig_loadings.pdf`. | `v3_r6_alpha.csv` |
| R7 | **Drop one industry.** 13 runs, each removing one group before standardisation and before the portfolio (12 groups, top/bottom 3, otherwise unchanged; the frozen backtest requires ≥ 6 groups). Test and full Sharpe per run; minimum, median and maximum; the industry whose removal lowers the test Sharpe most, and the industry whose removal raises it most. | `v3_r7_dropone.csv`, `fig_v2d_dropone.pdf` |
| R8 | **Tightness moderator** (the original thesis). V2d monthly net return and 12-month IC conditioned on the regime at the decision: T rising vs falling over the previous 12 months; V/U > 1 vs < 1 (T > 0 vs ≤ 0). Sharpe of the conditional months, mean 12-month IC with HAC t, months, for test and full. | `v3_r8_tightness.csv`, `fig_v2d_tightness.pdf` |
| R9 | **Bootstrap interval.** Circular moving-block bootstrap of the V2d monthly net returns, block length 12, 5,000 draws, seed 230: 90% percentile interval (5th–95th) for the annualised Sharpe, test and full. | `v3_r9_bootstrap.csv` |
| R10 | **As-known data.** If `analysis/.env` contains `FRED_API_KEY`: rebuild the hires and quits panels from ALFRED vintages and rerun V2a–V2d for test and full. Otherwise write "not run: no key". | `v3_r10_asknown.csv` or the note |
| R11 | **Fundamental law** (Grinold–Kahn). For A3 (saved sealed scores and weights), V2a and V2d, test window: IC = mean monthly rank IC at the book's horizon (1 month for A3 and V2a; 12 months for V2d); breadth BR = 13 × 12 = 156 independent bets per year for the 1-month books and 13 for the 12-month book; transfer coefficient TC = mean monthly cross-sectional correlation between the realised industry weights and the cross-sectionally demeaned score; implied IR = IC × √BR × TC; compared with the realised net Sharpe. Also the ceiling IC × √BR (TC = 1). | `v3_r11_fundamental_law.csv` |

Every CSV goes to `analysis/output/tables/`; LaTeX fragments to `report/tables/`; figures to `report/figures/` in the house style.

## 3. Reading rule for the battery, fixed now

V2d is read as **"supported by the battery"** only if all of the following hold in the **test** window:
- R1: the hires-only and quits-only books both have positive test Sharpe (the finding is not carried by one component);
- R2: the 12-month IC is positive with t ≥ 2 and the 1-month IC is not significantly positive (t < 2), i.e. the horizon pattern the thesis predicts;
- R3: holding periods 9 and 18 months also give positive test Sharpe (not a 12-month artefact);
- R4: test Sharpe is positive in both halves;
- R5: break-even cost above 25 bp;
- R7: the minimum drop-one test Sharpe is above 0 (no single industry carries it);
- R9: the 90% bootstrap interval for the test Sharpe excludes 0 **or** the full-sample interval excludes 0.

If any condition fails, the battery is read as **"V2d is fragile in that dimension"** and the report names the dimension. Either way the result stays POST-HOC, is not an implementation recommendation, and the forward test (Q4 2026 book) remains the only clean out-of-sample evidence.

R6, R8, R10 and R11 are descriptive and do not enter the rule. R11 answers a different question: whether the realised Sharpe is in line with what a 13-group universe allows.

## 4. Outputs

- `analysis/output/v3_results.md`: every result and its reading against §3.
- Results Book and `results/claims.csv` updated with the v3 numbers.
- Gate 2: this file's timestamp is earlier than the first v3 output; `run.ipynb` runs top to bottom; the v2 result files stay byte-identical to `v2_run_log.md`.
