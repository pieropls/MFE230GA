# Study 1 robustness: A3 (agent features, independent; primary) and A0 (fixed rule)

Regenerated 2026-10-04T09:55:48+00:00 by analysis/run.ipynb. Rows labelled CONFIRMATORY are read from Study 1's saved `results.json` and `research_summary.json` and are unchanged; rows labelled POST-HOC are diagnostics added in Study 2.3 (spec `analysis/specs/study2_3_robustness.md`, section 1) and cannot change the verdict: **Do not implement**.

## Consolidated table

Source: `analysis/output/study1/tables/d11_study1_robustness.csv`.

| item | A3 | A0 | label | source |
|---|---|---|---|---|
| Test Sharpe, data as known | -0.58 | -0.36 | CONFIRMATORY | results.json variants.ASOF |
| Test Sharpe, data first release | -0.52 | -0.16 | CONFIRMATORY | results.json variants.FIRST |
| Test Sharpe, data revised | -0.56 | -0.26 | CONFIRMATORY | results.json variants.REVISED |
| Test Sharpe, data fixed lag | -0.53 | -0.27 | CONFIRMATORY | results.json variants.FIXEDLAG |
| Net return p.a. | -4.6% | -3.5% | CONFIRMATORY | results.json variants.ASOF |
| IC, one month (t) | -0.021 (-1.08) | -0.020 (-0.71) | CONFIRMATORY | results.json variants.ASOF.IC.1 |
| Factor alpha per month (t) | -0.38% (-1.86) | -0.25% (-0.92) | CONFIRMATORY | results.json attribution |
| Placebo p (circular shift) | 0.72 | n/a (primary only) | CONFIRMATORY | results.json placebo |
| Holm-adjusted p, IC and return | 1.00, 1.00 (A3 vs A1) | 1.00, 1.00 (A1 vs A0) | CONFIRMATORY | results.json comparisons |
| Deflated Sharpe, research (41 trials) | 0.003 | 0.000 | CONFIRMATORY | research_summary.json |
| Sharpe at 0 / 10 / 25 bp | -0.45 / -0.58 / -0.79 | n/a / -0.36 / n/a | CONFIRMATORY | results.json sensitivities (primary only) |
| Sharpe, first test half | -0.72 | -0.55 | CONFIRMATORY | results.json windows.first_half |
| Sharpe, second test half | -0.49 | -0.20 | CONFIRMATORY | results.json windows.second_half |
| Sharpe, excluding Mar-Dec 2020 | -0.51 | -0.18 | CONFIRMATORY | results.json windows.ex_pandemic |
| Sharpe, last 18 months | +0.85 | -1.56 | CONFIRMATORY | results.json windows.last_18 |
| Drop one group, Sharpe range | -0.70 (Wholesale) to -0.24 (Durable mfg) | n/a (primary only) | CONFIRMATORY | results.json drop_one_group |
| Gates G1 timing / G2 prediction / G3 alpha / G4 robustness / G5 implementable | pass / fail / fail / fail / fail | n/a (primary only) | CONFIRMATORY | results.json gate |
| Verdict | Do not implement | not primary | CONFIRMATORY | results.json gate |
| Block-bootstrap 90% interval, test Sharpe | [-0.99, -0.16] | [-0.91, +0.20] | POST-HOC | saved ledgers; 12-month blocks, 5,000 draws, seed 230 |
| A3 score IC at 1 / 6 / 12 / 24 months (t) | -0.021 (-1.08) / -0.004 (-0.09) / -0.013 (-0.22) / -0.000 (-0.00) | n/a | POST-HOC | d11_a3_horizon_profile.csv |
| A3 Sharpe with cap 2 / cap 3 / no cap | -0.58 / -0.61 / -0.62 | n/a | POST-HOC | s23_r2_risk_overlay.csv |
| A3 Sharpe, rank-weighted book | -0.49 | n/a | POST-HOC | s23_r3_rank_weighted.csv |

## Horizon profile of the A3 score (POST-HOC)

Source: `d11_a3_horizon_profile.csv`; figure `report/figures/fig_s1_horizon.pdf`.

| book | h | ic | se | t | months |
|---|---|---|---|---|---|
| A3 agent features (Study 1 primary) | 1 | -0.0213 | 0.0198 | -1.077 | 142 |
| HQ12 (Study 2, post-hoc) | 1 | -0.02 | 0.023 | -0.8684 | 142 |
| A3 agent features (Study 1 primary) | 3 | -0.0292 | 0.027 | -1.083 | 140 |
| HQ12 (Study 2, post-hoc) | 3 | 0.0068 | 0.0373 | 0.1809 | 140 |
| A3 agent features (Study 1 primary) | 6 | -0.0044 | 0.0479 | -0.0912 | 137 |
| HQ12 (Study 2, post-hoc) | 6 | 0.0168 | 0.0417 | 0.4037 | 137 |
| A3 agent features (Study 1 primary) | 9 | -0.0155 | 0.057 | -0.2714 | 134 |
| HQ12 (Study 2, post-hoc) | 9 | 0.069 | 0.0348 | 1.981 | 134 |
| A3 agent features (Study 1 primary) | 12 | -0.0132 | 0.0591 | -0.2228 | 131 |
| HQ12 (Study 2, post-hoc) | 12 | 0.0962 | 0.0397 | 2.425 | 131 |
| A3 agent features (Study 1 primary) | 18 | 0.0059 | 0.0448 | 0.1314 | 125 |
| HQ12 (Study 2, post-hoc) | 18 | 0.0852 | 0.0426 | 2.001 | 125 |
| A3 agent features (Study 1 primary) | 24 | -0 | 0.055 | -0.0008 | 119 |
| HQ12 (Study 2, post-hoc) | 24 | 0.0628 | 0.0337 | 1.861 | 119 |

## Freeze record (CONFIRMATORY)

Source: `d11_freeze_check.csv`, computed from `FREEZE.json`, `evaluation_started.json` and the files in `study1_preregistered/`.

| check | ok | value |
|---|---|---|
| SHA-256 of FREEZE.json equals evaluation_started.freeze_sha256 | True | 60ea05294ffc856e |
| Freeze recorded (UTC) | True | 2026-10-02T06:00:09.537758+00:00 |
| Test opened (UTC) | True | 2026-10-02T06:00:09.578162+00:00 |
| Test opened after the freeze | True | 0.040 s later |
| Files in the freeze inventory | True | 525 |
| of which present in the repository | True | 338 |
| present files whose hash matches the inventory | True | 337 |
| present files that differ | True | outputs/human_migration_review.md |
| First test decision in the freeze record | True | 2014-10-31 |
