# Study 2.3: additional robustness (POST-HOC)

First run **2026-10-04T09:26:27+00:00** (regenerated 2026-10-04T09:34:41+00:00); spec `analysis/specs/study2_3_robustness.md` frozen **2026-10-04T09:18:39+00:00** (sha256 `068a3e0396332514ee3b76677f31b9c1ff6bfea7362d9e91d69ecc013e791528`). Deflated Sharpe ratios here use N = 162 looks. Names: W, SC, W+MOM, HQ12 are the variants stored as V2a, V2b, V2c, V2d in the Study 2.1 and 2.2 result files. Nothing here changes the confirmatory verdict (A3, Do not implement).

## R1 As-known rerun

Validation: passed (`s23_r1_validation.csv`). Reading fixed in the spec: **as-known confirms the fixed-lag reading**.

| check | value | tolerance |
|---|---|---|
| raw F1-F5 rebuilt from panel_asof vs features_asof.raw_value: max abs difference | 0 | 1e-09 |
| rows without a counterpart or with a missing-value mismatch | 0 | 0.5 |
| A0 from features_asof vs saved ASOF_A0_scores.csv, test window: max abs difference | 4.441e-16 | 1e-09 |

Test window, fixed lag (Study 2.1) against as known (`s23_r1_variants.csv`, `s23_r1_overlap.csv`):

| Variant (test window) | Sharpe, fixed lag | Sharpe, as known | IC (t), fixed lag | IC (t), as known | Alpha t | Same top 3 | Same bottom 3 |
|---|---|---|---|---|---|---|---|
| W | +0.16 | +0.13 | +0.049 (+2.04) | +0.041 (+1.73) | +0.18 | 76% | 70% |
| SC | -0.15 | +0.24 | +0.042 (+1.65) | +0.021 (+0.75) | +0.71 | 0% | 0% |
| W+MOM | +0.35 | +0.46 | +0.032 (+1.21) | +0.036 (+1.40) | +1.93 | 84% | 74% |
| HQ12 | +0.29 | +0.20 | +0.096 (+2.43) | +0.085 (+2.26) | +0.92 | 39% | 51% |

Sharpe by window, as known:

| variant | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| W | 0.107 | 0.134 | 0.133 | 0.096 | -1.314 |
| SC | 0.335 | 0.235 | 0.275 | 0.121 | 1.378 |
| W+MOM | 0.248 | 0.458 | 0.373 | 0.314 | -0.942 |
| HQ12 | 0.543 | 0.204 | 0.312 | 0.231 | 0.136 |

HQ12 battery (`s23_r1_hq12_battery.csv`):

| check | fixed_lag | as_known |
|---|---|---|
| Test Sharpe (10 bp) | 0.293 | 0.204 |
| Full-sample Sharpe (10 bp) | 0.351 | 0.312 |
| 12-month IC, test | 0.096 | 0.085 |
| 12-month IC t, test | 2.425 | 2.256 |
| 1-month IC t, test | -0.868 | -0.422 |
| Component hires only, test Sharpe | 0.189 | 0.189 |
| Component quits only, test Sharpe | 0.16 | 0.168 |
| Holding 9 months, test Sharpe | 0.14 | 0.155 |
| Holding 18 months, test Sharpe | 0.302 | 0.108 |
| First test half, Sharpe | -0.209 | -0.231 |
| Second test half, Sharpe | 0.638 | 0.492 |
| Test Sharpe at 0 bp | 0.343 | 0.255 |
| Test Sharpe at 25 bp | 0.217 | 0.127 |
| Test Sharpe at 50 bp | 0.092 | -0.001 |
| Break-even cost, test (bp) | 68.3 | 49.81 |
| Drop one group, minimum test Sharpe | 0.184 | 0.048 |
| Drop one group, maximum test Sharpe | 0.477 | 0.361 |
| Bootstrap 90% interval, test: low | -0.068 | -0.145 |
| Bootstrap 90% interval, test: high | 0.65 | 0.567 |
| Alpha per month (%), test, HAC 12 | 0.261 | 0.156 |
| Alpha t, test, HAC 12 | 1.481 | 0.923 |
| Bootstrap 90% interval, full: low | 0.05 | 0.024 |
| Bootstrap 90% interval, full: high | 0.641 | 0.603 |
| Alpha per month (%), full, HAC 12 | 0.265 | 0.21 |
| Alpha t, full, HAC 12 | 1.92 | 1.812 |
| Deflated Sharpe, test (132 looks fixed lag; 162 as known) | 0.049 | 0.021 |

## R2 Risk overlay

Source: `s23_r2_risk_overlay.csv`, `s23_r2_distribution.csv`; figure `fig_s23_gross_needed.pdf`.

| Book | Cap | Sharpe | Realised vol | Mean gross | Cap binds | Max drawdown |
|---|---|---|---|---|---|---|
| A3 | 2 | -0.58 | 7.8% | 1.98 | 87% | -41.1% |
| A3 | 3 | -0.61 | 9.7% | 2.57 | 35% | -50.7% |
| A3 | none | -0.62 | 10.3% | 2.79 | 0% | -54.9% |
| HQ12 | 2 | +0.29 | 8.7% | 1.97 | 83% | -14.4% |
| HQ12 | 3 | +0.24 | 10.5% | 2.51 | 39% | -20.3% |
| HQ12 | none | +0.24 | 11.1% | 2.78 | 0% | -22.6% |

| book | unit_vol_p5 | unit_vol_p50 | unit_vol_p95 | gross_needed_p5 | gross_needed_p50 | gross_needed_p95 |
|---|---|---|---|---|---|---|
| A3 | 0.045 | 0.075 | 0.11 | 1.849 | 2.604 | 4.186 |
| HQ12 | 0.033 | 0.064 | 0.103 | 1.791 | 2.447 | 4.243 |

## R3 Rank-weighted books

Source: `s23_r3_rank_weighted.csv`.

| Book | Weights | Test Sharpe | TC | Turnover | Implied IR |
|---|---|---|---|---|---|
| A3 | top 3 / bottom 3 | -0.58 | 0.80 | 0.91 | -0.21 |
| A3 | rank-weighted | -0.49 | 0.83 | 0.86 | -0.22 |
| HQ12 | top 3 / bottom 3 | +0.29 | 0.48 | 0.37 | +0.17 |
| HQ12 | rank-weighted | +0.31 | 0.49 | 0.37 | +0.17 |

## R4 Agents: arm gap against seed spread

Source: `s23_r4_agents_by_seed.csv`, `s23_r4_permutation.csv`; figure `fig_s23_agents_seeds.pdf`.

| Study | Arm | Seed | Valid | Best IC | Mean IC | Eligible | Regime-gated |
|---|---|---|---|---|---|---|---|
| Study 1 (Sonnet) | independent | 1 | 17/18 | +0.101 | +0.014 | 2 | 29% |
| Study 1 (Sonnet) | independent | 2 | 17/18 | +0.102 | -0.006 |  | 24% |
| Study 1 (Sonnet) | independent | 3 | 13/18 | +0.046 | -0.014 |  | 15% |
| Study 1 (Sonnet) | islands | 1 | 16/18 | +0.052 | -0.003 | 2 | 25% |
| Study 1 (Sonnet) | islands | 2 | 17/18 | +0.058 | +0.005 |  | 6% |
| Study 1 (Sonnet) | islands | 3 | 18/18 | +0.037 | -0.008 |  | 22% |
| Study 1b (Opus) | independent | 1 | 18/18 | +0.088 | -0.002 | 1 | 28% |
| Study 1b (Opus) | independent | 2 | 18/18 | +0.045 | -0.006 |  | 11% |
| Study 1b (Opus) | independent | 3 | 18/18 | +0.045 | +0.002 |  | 6% |
| Study 1b (Opus) | islands | 1 | 17/18 | +0.125 | +0.026 | 6 | 6% |
| Study 1b (Opus) | islands | 2 | 18/18 | +0.191 | +0.049 |  | 39% |
| Study 1b (Opus) | islands | 3 | 17/18 | +0.091 | +0.009 |  | 47% |

| study | metric | islands_minus_independent | largest_seed_range_within_arm | gap_within_seed_range | perm_p_two_sided | relabelings |
|---|---|---|---|---|---|---|
| Study 1 (Sonnet) | best_ic | -0.034 | 0.056 | True | 0.3 | 20 |
| Study 1 (Sonnet) | mean_ic | -0.001 | 0.028 | True | 1 | 20 |
| Study 1b (Opus) | best_ic | 0.076 | 0.099 | True | 0.1 | 20 |
| Study 1b (Opus) | mean_ic | 0.03 | 0.04 | True | 0.1 | 20 |

## R5 Tokens

Source: `s23_r5_tokens.csv`, `s23_r5_tokens_ic.csv`.

| study | arm | calls_with_usage | tokens_total | tokens_per_call | output_tokens_per_call |
|---|---|---|---|---|---|
| Study 1 (Sonnet) | independent | 54 | 1.209e+05 | 2239 | 183 |
| Study 1 (Sonnet) | islands | 54 | 1.342e+05 | 2485 | 193 |
| Study 1b (Opus) | independent | 54 | 1.806e+05 | 3344 | 1257 |
| Study 1b (Opus) | islands | 54 | 2.14e+05 | 3963 | 1509 |

| study | n | spearman_output_tokens_vs_ic | spearman_output_tokens_vs_abs_ic |
|---|---|---|---|
| Study 1 (Sonnet) | 98 | 0.13 | 0.21 |
| Study 1b (Opus) | 106 | 0.41 | 0.24 |

## R6 Effective breadth

Source: `s23_r6_breadth.csv`.

| matrix | participation_ratio |
|---|---|
| 13 group excess returns | 1.96 |
| 13 group relative returns (group minus equal-weight mean) | 9.05 |
| z(W) across groups | 7.36 |
| HQ12 score across groups | 10.11 |

## Time patterns and costs (report tables)

| Strategy | Study | Test | Full sample | Post-2010 | Last 18 months |
|---|---|---|---|---|---|
| A0 fixed rule | Study 1 | -0.36 | -0.48 | -0.41 | -1.56 |
| A1 ridge | Study 1 | -0.51 | -0.52 | -0.66 | +0.73 |
| A1-T ridge x tightness | Study 1 | -0.59 | -0.58 | -0.73 | -0.37 |
| A3 agent features, independent (primary) | Study 1 | -0.58 | -0.44 | -0.62 | +0.85 |
| A4 agent features, communicating | Study 1 | -0.79 | -0.56 | -0.74 | +1.23 |
| W wage growth (declared headline) | Study 2 | +0.16 | +0.15 | +0.12 | -1.71 |
| SC signed composite | Study 2 | -0.15 | -0.11 | -0.16 | -1.34 |
| W+MOM wage growth + momentum | Study 2 | +0.35 | +0.32 | +0.24 | -0.78 |
| HQ12 hires + quits reversal, 12-month hold | Study 2 | +0.29 | +0.35 | +0.30 | +0.29 |

| Book (test window) | Turnover p.a. | Cost drag p.a. | Gross p.a. | Net p.a. | Break-even (bp) |
|---|---|---|---|---|---|
| A3 agent features, independent (primary) | 11.0x | 1.11% | -3.5% | -4.6% | -32 |
| W wage growth (declared headline) | 4.7x | 0.47% | +2.1% | +1.7% | +46 |
| SC signed composite | 8.7x | 0.88% | -0.5% | -1.3% | -5 |
| W+MOM wage growth + momentum | 5.8x | 0.59% | +3.6% | +3.1% | +62 |
| HQ12 hires + quits reversal, 12-month hold | 4.4x | 0.44% | +3.0% | +2.6% | +68 |
| A3 rank-weighted | 10.3x | 1.05% | -2.5% | -3.6% | -24 |
| HQ12 rank-weighted | 4.4x | 0.45% | +3.0% | +2.6% | +69 |

## R7 Capacity

| book | binding_etf | binding_adv_usd_m | monthly_trade_share_of_aum | aum_at_1pct_adv_usd_m | aum_at_5pct_adv_usd_m | spy_adv_usd_bn | smallest_etf_adv_usd_m | smallest_etf |
|---|---|---|---|---|---|---|---|---|
| A3 | PEJ | 3.151 | 0.063 | 0.497 | 2.487 | 47.01 | 3.151 | PEJ |
| HQ12 | PEJ | 3.151 | 0.027 | 1.174 | 5.872 | 47.01 | 3.151 | PEJ |

## R8 Judge fix

| study | judge | pairs | defined | agree | judge_yes | human_yes | false_yes | missed_yes |
|---|---|---|---|---|---|---|---|---|
| Study 1 (Sonnet) | original judge | 8 | 2 | 1 | 1 | 1 | 1 | 0 |
| Study 1 (Sonnet) | judge with verbatim quote | 8 | 8 | 7 | 2 | 1 | 1 | 0 |
| Study 1 (Sonnet) | with quote, fenced JSON accepted (supplementary) | 8 | 8 | 7 | 2 | 1 | 1 | 0 |
| Study 1b (Opus) | original judge | 17 | 17 | 10 | 10 | 3 | 7 | 0 |
| Study 1b (Opus) | judge with verbatim quote | 17 | 7 | 3 | 5 | 3 | 4 | 0 |
| Study 1b (Opus) | with quote, fenced JSON accepted (supplementary) | 17 | 17 | 9 | 11 | 3 | 8 | 0 |

## R9 Feedback ablation

| condition | seeds | proposals | valid | regime_proposals | regime_share | nonmissing_below_half_share | informative_below_half_share | best_ic |
|---|---|---|---|---|---|---|---|---|
| A_with_tercile_split | 3 | 54 | 48 | 4 | 0.083 | 0 | 0.083 | 0.07 |
| B_without_tercile_split | 3 | 54 | 50 | 3 | 0.06 | 0 | 0.06 | 0.07 |
