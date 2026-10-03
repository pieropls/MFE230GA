# v2 results (POST-HOC)

First run at **2026-10-03T09:01:55+00:00** (this file regenerated at 2026-10-03T22:21:18+00:00; outputs verified identical to the first run, see v2_run_log.md). Specification `analysis/v2_spec.md` was frozen at **2026-10-03T09:00:13+00:00** (sha256 `ca6582347904489bdb6fac1496f895fd18c91eba47ca2bc8566e35cdf44a5832`, commit d76fbb3) before this run. All four variants are reported. Labor data are revised FRED values with fixed lags (`data_vintage.md`); returns and portfolio construction are the frozen study's (Gate 1).

The confirmatory verdict is unchanged: primary A3, test Sharpe -0.58, **Do not implement**.

## Reading rule (v2_spec.md section 6), test window

Source: `analysis/output/tables/v2_reading_rule.csv`.

| variant | sharpe_25bp_positive | ic_t_ge_2 | alpha_t_ge_2 | ic_positive_both_halves | placebo_p_lt_0.05 | dsr_gt_0.95 | reading |
|---|---|---|---|---|---|---|---|
| V2a | True | True | False | True | True | False | not distinguishable from noise after the looks already taken |
| V2b | False | False | False | True | False | False | not distinguishable from noise after the looks already taken |
| V2c | True | False | False | True | False | False | not distinguishable from noise after the looks already taken |
| V2d | True | False | False | False | False | False | not distinguishable from noise after the looks already taken |

## Sharpe ratio by window (10 bp)

Source: `analysis/output/tables/v2_window_stats.csv` (column `sharpe`).

| variant | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| V2a | 0.093 | 0.164 | 0.147 | 0.125 | -1.709 |
| V2b | -0.055 | -0.153 | -0.11 | -0.158 | -1.344 |
| V2c | 0.274 | 0.345 | 0.325 | 0.239 | -0.775 |
| V2d | 0.503 | 0.293 | 0.351 | 0.297 | 0.286 |

## A3 contrast (CONFIRMATORY)

Sources: research_summary.json (research, 88 months Jun 2007-Sep 2014); results.json windows (test, last 18m) and course_windows (full, post-2010; descriptive mix of research and test).

| index | A3 Sharpe |
|---|---|
| research | -0.132 |
| test | -0.584 |
| full | -0.438 |
| post-2010 | -0.615 |
| last 18m | 0.846 |

## All statistics, every variant and window

Source: `analysis/output/tables/v2_window_stats.csv`. Net return, volatility, drawdown and hit rate in decimals; alpha per month; DSR uses N_trials = 112 and trial variance 1/T.

### V2a: Cross-sectional rank of W (headline)

| index | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| months | 125 | 142 | 268 | 200 | 18 |
| sharpe | 0.0927 | 0.1637 | 0.1473 | 0.1246 | -1.709 |
| net_ann | 0.0063 | 0.0167 | 0.0129 | 0.0114 | -0.121 |
| vol | 0.0681 | 0.102 | 0.0877 | 0.0918 | 0.0708 |
| max_dd | -0.1443 | -0.2115 | -0.2115 | -0.2115 | -0.1502 |
| hit | 0.48 | 0.5282 | 0.5075 | 0.515 | 0.3333 |
| ic | 0.0293 | 0.0493 | 0.0394 | 0.0378 | -0.0295 |
| ic_t | 1.537 | 2.036 | 2.502 | 1.892 | -0.9054 |
| ic_hold | 0.0263 | 0.043 | 0.0368 | 0.0392 | -0.0334 |
| ic_hold_t | 1.061 | 1.352 | 1.769 | 1.457 | -0.9857 |
| alpha_month | 0.0005 | 0.0006 | 0.0007 | 0.0004 | -0.0179 |
| alpha_t | 0.2812 | 0.2873 | 0.5086 | 0.2472 | -6.58 |
| sharpe_0bp | 0.1592 | 0.2093 | 0.1997 | 0.1749 | -1.637 |
| sharpe_10bp | 0.0927 | 0.1637 | 0.1473 | 0.1246 | -1.709 |
| sharpe_25bp | -0.0079 | 0.0953 | 0.0683 | 0.049 | -1.817 |
| turnover | 0.3802 | 0.3877 | 0.3844 | 0.3854 | 0.453 |
| placebo_p | 0.0897 | 0.0211 | 0 | 0.1242 |  |
| dsr | 0.0116 | 0.0231 | 0.0308 | 0.0202 | 0 |

### V2b: Equal-weight composite of z(F1..F5, W), each signed by its research-period IC

| index | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| months | 125 | 142 | 268 | 200 | 18 |
| sharpe | -0.0551 | -0.1528 | -0.1099 | -0.1577 | -1.344 |
| net_ann | -0.0041 | -0.0134 | -0.0089 | -0.0125 | -0.1171 |
| vol | 0.0736 | 0.0875 | 0.081 | 0.0791 | 0.0871 |
| max_dd | -0.2215 | -0.2175 | -0.2215 | -0.2175 | -0.1373 |
| hit | 0.456 | 0.5282 | 0.4963 | 0.51 | 0.3333 |
| ic | 0.0372 | 0.0422 | 0.04 | 0.0363 | -0.0644 |
| ic_t | 1.309 | 1.651 | 2.091 | 1.64 | -1.096 |
| ic_hold | 0.0246 | 0.0286 | 0.0275 | 0.024 | -0.1387 |
| ic_hold_t | 0.6573 | 0.7718 | 1.025 | 0.7576 | -3.835 |
| alpha_month | 0.0003 | -0.0018 | -0.0012 | -0.0016 | -0.0192 |
| alpha_t | 0.1691 | -0.8404 | -0.8184 | -0.9546 | -3.944 |
| sharpe_0bp | 0.0617 | -0.0531 | -0.003 | -0.0496 | -1.219 |
| sharpe_10bp | -0.0551 | -0.1528 | -0.1099 | -0.1577 | -1.344 |
| sharpe_25bp | -0.2308 | -0.3025 | -0.2706 | -0.3199 | -1.531 |
| turnover | 0.7169 | 0.7267 | 0.7215 | 0.7125 | 0.9259 |
| placebo_p | 0.0513 | 0.0526 | 0.0452 | 0.0392 |  |
| dsr | 0.003 | 0.0009 | 0.0009 | 0.0006 | 0 |

### V2c: Equal-rank composite of W and industry momentum 12-1

| index | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| months | 125 | 142 | 268 | 200 | 18 |
| sharpe | 0.2741 | 0.3452 | 0.3247 | 0.2386 | -0.775 |
| net_ann | 0.0249 | 0.0305 | 0.029 | 0.0189 | -0.0748 |
| vol | 0.0908 | 0.0884 | 0.0894 | 0.079 | 0.0965 |
| max_dd | -0.1773 | -0.1293 | -0.1773 | -0.1576 | -0.0884 |
| hit | 0.552 | 0.5563 | 0.556 | 0.53 | 0.3889 |
| ic | 0.0459 | 0.0324 | 0.0397 | 0.0339 | -0.0828 |
| ic_t | 2.042 | 1.211 | 2.232 | 1.632 | -1.566 |
| ic_hold | 0.0333 | 0.045 | 0.0406 | 0.0351 | -0.031 |
| ic_hold_t | 0.9191 | 1.482 | 1.736 | 1.412 | -1.106 |
| alpha_month | 0.0004 | 0.0022 | 0.0015 | 0.0013 | -0.0131 |
| alpha_t | 0.2946 | 1.361 | 1.228 | 0.9958 | -4.485 |
| sharpe_0bp | 0.3408 | 0.4112 | 0.3911 | 0.3123 | -0.7086 |
| sharpe_10bp | 0.2741 | 0.3452 | 0.3247 | 0.2386 | -0.775 |
| sharpe_25bp | 0.1737 | 0.2462 | 0.2249 | 0.1276 | -0.8748 |
| turnover | 0.5071 | 0.485 | 0.4952 | 0.4868 | 0.5333 |
| placebo_p | 0.0513 | 0.2632 | 0 | 0.0458 |  |
| dsr | 0.0562 | 0.088 | 0.1608 | 0.0574 | 0.0001 |

### V2d: -(z(F2)+z(F3))/2, held 12 months (12 tranches)

| index | research | test | full | post-2010 | last 18m |
|---|---|---|---|---|---|
| months | 125 | 142 | 268 | 200 | 18 |
| sharpe | 0.5033 | 0.2928 | 0.3514 | 0.2974 | 0.2865 |
| net_ann | 0.0313 | 0.0256 | 0.0269 | 0.0237 | 0.0364 |
| vol | 0.0621 | 0.0873 | 0.0765 | 0.0797 | 0.1269 |
| max_dd | -0.082 | -0.1439 | -0.2172 | -0.2172 | -0.0837 |
| hit | 0.576 | 0.5493 | 0.5597 | 0.56 | 0.5556 |
| ic | -0.0158 | -0.02 | -0.019 | -0.0125 | 0.0543 |
| ic_t | -0.591 | -0.8684 | -1.084 | -0.5897 | 0.9345 |
| ic_hold | 0.0471 | 0.0962 | 0.0711 | 0.0807 |  |
| ic_hold_t | 0.8965 | 2.425 | 2.064 | 2.131 |  |
| alpha_month | 0.0017 | 0.0026 | 0.0026 | 0.0022 | 0.0001 |
| alpha_t | 1.042 | 1.372 | 1.956 | 1.369 | 0.014 |
| sharpe_0bp | 0.5799 | 0.343 | 0.4108 | 0.353 | 0.3186 |
| sharpe_10bp | 0.5033 | 0.2928 | 0.3514 | 0.2974 | 0.2865 |
| sharpe_25bp | 0.3885 | 0.2175 | 0.2622 | 0.2139 | 0.2383 |
| turnover | 0.3944 | 0.3656 | 0.3789 | 0.3697 | 0.3401 |
| placebo_p | 0.6026 | 0.8526 | 0.8552 | 0.7974 |  |
| dsr | 0.1761 | 0.0556 | 0.1777 | 0.0837 | 0.0158 |

## V2b signs, learned on research months only (May 2004-Sep 2014)

Source: `analysis/output/tables/v2b_signs.csv`.

| index | research_ic | sign |
|---|---|---|
| F1 | 0.0006 | 1 |
| F2 | 0.012 | 1 |
| F3 | 0.0139 | 1 |
| F4 | 0.0326 | 1 |
| F5 | -0.0118 | -1 |
| W | 0.0293 | 1 |

## P&L by industry (sum of monthly contributions, 10 bp)

Source: `analysis/output/tables/v2_pnl_by_industry.csv`.

| component | V2a test | V2a full | V2b test | V2b full | V2c test | V2c full | V2d test | V2d full |
|---|---|---|---|---|---|---|---|---|
| Mining & logging | -0.482 | -0.444 | -0.106 | -0.28 | -0.135 | -0.183 | 0.092 | 0.391 |
| Construction | 0.229 | 0.171 | 0.005 | -0.098 | 0.129 | 0.095 | 0.085 | 0.009 |
| Durable mfg | 0.194 | 0.109 | 0.072 | 0.171 | 0.21 | -0.012 | 0.052 | 0.119 |
| Nondurable mfg | 0.116 | 0.054 | 0.103 | -0.013 | 0.046 | 0.05 | -0.009 | 0.142 |
| Wholesale | 0.043 | 0.232 | -0.028 | 0.039 | 0.024 | 0.237 | 0.085 | 0.045 |
| Retail | 0.248 | 0.389 | 0.014 | 0.059 | 0.194 | 0.351 | 0.043 | 0.091 |
| Transport & utilities | -0.211 | -0.376 | -0.107 | -0.288 | -0.149 | -0.245 | -0.03 | -0.192 |
| Information | 0.186 | 0.195 | -0.062 | 0.302 | 0.131 | 0.199 | 0.069 | -0.278 |
| Finance & insurance | 0.141 | 0.351 | 0.051 | 0.126 | 0.062 | 0.308 | 0.057 | 0.159 |
| Real estate | 0.21 | 0.345 | 0.153 | 0.111 | 0.028 | 0.143 | -0.167 | -0.117 |
| Prof. & business svcs | -0.113 | -0.173 | -0.211 | -0.172 | 0.125 | 0.047 | 0.11 | 0.176 |
| Health care | -0.099 | 0.011 | 0.049 | 0.157 | -0.066 | -0.076 | 0.052 | -0.025 |
| Accommodation & food | -0.191 | -0.384 | 0.027 | -0.093 | -0.141 | -0.174 | -0.032 | 0.095 |
| Market hedge | -0.016 | -0.087 | -0.014 | -0.023 | -0.025 | 0.043 | -0.05 | 0.09 |
| Trading costs | -0.056 | -0.105 | -0.105 | -0.197 | -0.07 | -0.135 | -0.053 | -0.103 |

## Files

- `analysis/output/tables/v2_window_stats.csv`, `v2_reading_rule.csv`, `v2b_signs.csv`, `v2_monthly_net.csv`, `v2_pnl_by_industry.csv`, `v2a_factor_loadings_test.csv`
- `report/tables/v2_results.tex`
- `report/figures/fig_v2_windows.pdf`; V2a added to `fig_cumulative.pdf` and `fig_loadings.pdf`

## Additional check added after the run (POST-HOC, not part of the reading rule)

Added on 3 Oct 2026 after the v2 results above had been seen, at the team's request. It does **not** replace the pre-declared placebo: V2d's pre-declared test-window placebo p (1-month IC) stays 0.85, as reported in the tables above and in the reading rule.

V2d is held 12 months, so this check uses its 12-month IC: the rank IC between the score and the 12-month compounded relative return (months m to m+11). The score panel is rolled circularly against that target within each window by every shift from 24 to n-24 months; p is the share of shifted mean ICs at or above the actual one. Months at the end of the sample without a complete 12-month return drop out. The 12-month returns overlap, which the circular shift preserves but does not correct.

Source: `analysis/output/tables/v2d_placebo_12m.csv`.

| window | ic_12m | placebo_p_12m | shifts | placebo_p_1m_predeclared |
|---|---|---|---|---|
| research | 0.0471 | 0.2564 | 78 | 0.6026 |
| test | 0.0962 | 0.0632 | 95 | 0.8526 |
| full | 0.0711 | 0.0362 | 221 | 0.8552 |
| post-2010 | 0.0807 | 0 | 153 | 0.7974 |
