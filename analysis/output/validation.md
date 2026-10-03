# Gate 1 validation

Run 2026-10-03T22:21:06+00:00 by analysis/run.ipynb. **Result: PASS**

Every check uses the frozen study's saved files in `230ga-follow-the-workers/` (read-only) and public Ken French data (CRSP 202608 build) in `analysis/data/french/`. The backtest is the frozen `data.backtest`, imported read-only.

| check | value | threshold | pass |
|---|---|---|---|
| Frozen repo unchanged (SHA-256 over all files) | 3067 files, eb109be96917... | 3067 files, eb109be96917... | True |
| Portfolio parameters equal frozen params.PORTFOLIO | {'longs': 3, 'shorts': 3, 'holding': 3, 'risk_window': 60, 'risk_min_months': 36, 'vol_target': 0.1, 'gross_cap': 2.0, 'cost_bps': 10, 'hedge_cost_bps': 2} | identical | True |
| Sealed A0 net: max |ours - saved| over 142 months | 9.97e-17 | < 1e-6 | True |
| Sealed A0 gross: max |ours - saved| over 142 months | 9.71e-17 | < 1e-6 | True |
| Sealed A0 cost: max |ours - saved| over 142 months | 9.94e-17 | < 1e-6 | True |
| Sealed A0 turnover: max |ours - saved| over 142 months | 2.22e-16 | < 1e-6 | True |
| 13 group returns vs 50 saved ledgers (both studies, sealed + research) | 1.51e-16 | < 1e-6 | True |
| Estimators vs results.json (IC, IC t, Sharpe, factor coefs and t; A0-A4) | 3.55e-15 | < 1e-8 | True |

## Informational: rebuilt labor signals vs the frozen study's saved A0 scores

Not part of the gate (our labor data is revised FRED, not the frozen as-known panels). See `data_vintage.md`.

| saved A0 variant | pooled_corr | mean_monthly_rank_corr | same_top3_share |
|---|---|---|---|
| FIXEDLAG | 0.9983 | 0.9922 | 0.9085 |
| ASOF | 0.9181 | 0.8635 | 0.4155 |
| REVISED | 0.9912 | 0.9793 | 0.8592 |
| FIRST | 0.8506 | 0.7796 | 0.2394 |
