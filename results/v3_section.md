### 4b. V2d robustness battery (v3, POST-HOC)

Spec `analysis/v3_spec.md` frozen 2026-10-03T09:52:27Z (sha256 `312aef1d…`), first run 09:53:32Z; results in `analysis/output/v3_results.md`; N_trials raised to 132. **Reading against the pre-declared rule: fragile in one dimension (R4): V2d lost money in the first half of the test (Sharpe −0.21) and made it in the second (+0.64). The other six conditions hold.**

| ID | Table | Figure | One-line result |
|---|---|---|---|
| R1 | `v3_r1_components` | — | Hires alone +0.19 and quits alone +0.16 test Sharpe; openings +0.42 and layoffs +0.16 with the same sign. Not carried by one component. |
| R2 | `v3_r2_horizon_profile` | `fig_horizon_profile.pdf` | IC −0.020 at 1 month, +0.069 at 9, +0.096 at 12 (t 2.43), +0.085 at 18, +0.063 at 24. The thesis horizon pattern. |
| R3 | `v3_r3_holding` | `fig_v2d_holding.pdf` | Test Sharpe +0.05 (6m), +0.14 (9m), +0.29 (12m), +0.30 (18m). |
| R4 | `v3_r4_subperiods` | — | Test halves −0.21 / +0.64; ex-pandemic +0.37; pre-2020 +0.14; 2020 onward +0.37. The 12-month IC is positive in both halves (+0.097, +0.095). |
| R5 | `v3_r5_costs` | — | Test Sharpe +0.34 / +0.29 / +0.22 / +0.09 at 0 / 10 / 25 / 50 bp; break-even 68 bp. |
| R6 | `v3_r6_alpha` | `fig_loadings.pdf` (V2d added) | Alpha +0.26%/month, t 1.48 test and 1.92 full (HAC 12). Loads against RMW (−0.36, t −4.45). |
| R7 | `v3_r7_dropone(_summary)` | `fig_v2d_dropone.pdf` | Drop-one test Sharpe from +0.18 (no health care) to +0.48 (no real estate), median +0.30. |
| R8 | `v3_r8_tightness` | `fig_v2d_tightness.pdf` | Sharpe −0.00 when T rose, +0.66 when it fell; +0.72 when V/U > 1, −0.14 when V/U < 1. The IC is highest when T rises (+0.115). |
| R9 | `v3_r9_bootstrap` | — | 90% interval [−0.07, +0.65] test (includes 0), [+0.05, +0.64] full (excludes 0). |
| R10 | `v3_r10_asknown` | — | Not run: no FRED key. |
| R11 | `v3_r11_fundamental_law` | — | Implied IR: A3 −0.21 (realised −0.58), V2a +0.56 (realised +0.16), V2d +0.17 with ceiling +0.35 (realised +0.29). |
| — | `v3_dsr132` | — | V2d DSR at 132 trials: 0.05 test, 0.16 full. |
