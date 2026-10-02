# Audit: 10 Reasons These Results Could Be Spurious

**Framing.** None of these results is positive. All five variants have negative gross and net Sharpe ratios, from −0.40 to −0.55. Deflated Sharpe ratios are ≤ 0.001, and IC t-stats fall between −0.95 and +0.94. "Do not implement" is already the default. The real risks are:

- **Rescue by glimmer:** using the few favourable numbers to save a variant. These are A0's IR of +0.15, the positive ICs of A0 and A4, and A4 being "least bad".
- **Post-hoc sign flip:** inverting the signal after seeing it fail.
- **Pipeline errors:** problems that make the evaluation itself unreliable.

The reasons below are ranked by how likely each problem is to be present, given the numbers. Tests assume access to the monthly series behind these summaries. Where the summary alone is enough, I say so.

---

**1. Everything here is noise (insufficient power)**
- **Evidence:**
  - Monthly Sharpe × √88 gives t ≈ −1.09 (A4) to −1.48 (A1-T).
  - A0's IR of 0.15 over 7.3 years gives t ≈ 0.40.
  - The SE of the annual Sharpe is about 0.37, so the minimum detectable Sharpe is about 0.74.
  - Gaps between variants are at most 0.15 Sharpe, which is under 0.5 SE. Ranking the variants is meaningless.
- **Test:**
  - HAC (6-lag) t-stats and stationary block-bootstrap 95% confidence intervals for gross/net Sharpe and IC.
  - Memmel/Ledoit–Wolf tests for differences in Sharpe between variants.
- **Do not implement if:** no variant's gross-Sharpe confidence interval has a lower bound above 0, or no pairwise Sharpe difference is significant. Both are near-certain: A4's 95% interval is roughly −0.40 ± 0.72.

**2. P&L comes from a common construction or hedge drag, not the signal**
- **Evidence:**
  - All five variants lose 1.75–2.68% a year gross, while IC ranges from −0.030 to +0.027.
  - A0 (IC +0.012) and A4 (IC +0.027) still lose money gross.
  - A naive 5-point fit of gross return on IC implies about −2.2% a year at IC = 0, with a negligible slope.
- **Test:**
  - Placebo: run 500+ cross-sectionally shuffled signals through the identical construction, hedge and cost pipeline.
  - Regress each variant's monthly gross return on its own monthly IC and on hedge/benchmark returns.
  - Attribute P&L to the long book, the hedge leg and the residual.
- **Do not implement if:** the real variants sit below the 95th percentile of the placebo distribution, the return-on-own-IC slope is insignificant, or the hedge or residual beta explains most of the loss.
  - Even a pass here only justifies a redesign and a fresh out-of-sample test.

**3. A0's positive active return and IR are a benchmark artifact** *(summary suffices)*
- **Evidence:**
  - Net minus active return implies a benchmark of about −4.38% a year for A0, versus −1.02% to −1.21% for A1–A4.
  - A0 and A1 have the same net return (−3.48% vs −3.49%) but active returns of +0.89% vs −2.34%.
  - Benchmarks differ slightly even among A1–A4.
- **Test:** recompute active return, tracking error and IR for all variants against one fixed benchmark series over identical dates. Document what A0's benchmark is and why.
- **Do not implement if:** on the common benchmark A0's active return is ≤ 0 (arithmetic predicts about −2.3%, IR about −0.4), or A0's benchmark cannot be justified ex ante.

**4. The net figures are optimistic because the cost and financing model is a floor**
- **Evidence:**
  - Costs reverse-engineer exactly to 10 bp × turnover + 2 bp × hedge turnover per month. For A1: 0.001 × 0.8508 + 0.0002 × 0.0880 = 0.000868.
  - Borrow and financing are exactly 0.
  - Turnover is 66–85% a month, or roughly 8–10× a year.
- **Test:**
  - Compute break-even cost per unit of turnover (gross return ÷ annual turnover).
  - Rerun with impact scaled to average daily volume at target assets under management, plus real financing and borrow.
- **Do not implement if:** break-even cost is ≤ 0. This is already true for all five, since gross is negative, so no cost assumption rescues them.
  - For any future variant, also reject if break-even is below about 2× realistic modelled costs.

**5. Selection and trial accounting are understated; variants are near-clones**
- **Evidence:**
  - 41 trials were run but only 5 are reported, and A2 is missing.
  - A1 and A3 are near-identical: turnover 0.8508 vs 0.8510, cost 0.000868 vs 0.000869. Their agreement is not independent confirmation.
  - The DSR caveat says the adaptive search is not corrected for.
  - The DSR hurdle is 0.235 monthly. Passing DSR ≥ 0.95 would need an observed annual Sharpe of about 1.4. The best observed is −0.40.
- **Test:**
  - Assemble the full 41-trial return ledger, including A2.
  - Estimate the effective number of independent trials from the correlation matrix.
  - Run Hansen SPA and Romano–Wolf tests on the best trial versus zero.
- **Do not implement if:** the best trial has p > 0.05, the five shown are the top of the 41, or A2 was dropped for performance reasons.

**6. The IC sign is unstable, so neither the signal nor its inverse is reliable**
- **Evidence:**
  - A3's IC is −0.0285 and A4's is +0.0272: near mirror images, each with SE ≈ 0.03.
  - Flipping A1 or A3 "because both IC and returns are negative" would be an extra post-hoc trial.
  - Point 2 implies a flipped signal would not flip the P&L.
- **Test:**
  - Correlate the monthly IC series across variants.
  - Check the IC sign by half and by year.
  - Build the inverted A1/A3 portfolios through the same pipeline, log them as trials 42+, and recompute DSR.
- **Do not implement if:** the IC sign differs between halves or across most years, or the inverted portfolio loses money gross or has DSR < 0.95.

**7. Regime concentration and a hidden profitable stretch** *(summary partially suffices)*
- **Evidence:**
  - From the reported mean and volatility, A1's estimated end-to-end log loss is about −0.27, while its drawdown is −0.44 in log terms.
  - Drawdowns for A1, A1-T, A3 and A4 exceed their end-to-end losses by about 14–20 log points. Each must have had a sizeable profitable stretch.
  - A0's drawdown roughly equals its total loss, so A0 had no such stretch.
  - That stretch invites "it works since year X" cherry-picking. Clustered losses also imply autocorrelation, which distorts √12 annualisation.
- **Test:**
  - Find peak and trough dates.
  - Compute first-half vs second-half and calendar-year gross Sharpe.
  - Compute AR(1), Lo-adjusted Sharpe and a variance ratio.
- **Do not implement if:** the profitable stretch is confined to one window (under about 3 years) and does not recur in the other half, or any case for a variant depends on a start date chosen after seeing the curve.

**8. Outlier dependence: the typical month is worse than the mean**
- **Evidence:**
  - A1 had 34 of 88 months positive. A sign test gives p ≈ 0.04 versus 50%, which is stronger than its mean-based t of about −1.46.
  - With normal returns at A1's mean and volatility, the expected hit rate is about 44%; the observed rate is 38.6%.
- **Test:**
  - Median monthly return and a Wilcoxon signed-rank test.
  - Means with the best and worst 3 months trimmed.
  - Share of gross gains coming from the top 5 months.
- **Do not implement if:** the median gross return is negative for every variant, or more than about half of the gross gains come from 5 or fewer months.

**9. Timing or point-in-time misalignment between the signal, the IC and the traded portfolio**
- **Evidence:**
  - The sign of IC and the sign of P&L disagree for A0 and A4. This is consistent with a different lag, horizon or universe for the IC than for the portfolio.
  - Turnover of 66–85% a month with near-zero IC suggests the signal is stale or noisy at the trade date.
- **Test:**
  - Lag profile: compute IC and gross portfolio return with signal lags of −1, 0, +1, +2 and +3 months.
  - Recompute IC on the traded universe only.
  - Audit point-in-time timestamps and delisting-return coverage.
- **Do not implement if:** IC peaks at lag ≤ 0 (look-ahead or contemporaneous) and is about 0 at the first implementable lag, or the traded-universe IC has the opposite sign to the full-universe IC.

**10. Accounting basis mismatch: funded NAV vs the return series**
- **Evidence:**
  - Drawdown is reported on "funded NAV", while Sharpe is mean ÷ volatility on a return series. Net equals gross minus 12 × monthly cost exactly.
  - If capital and notional differ, the metrics describe different portfolios.
  - A0 reconciles approximately (24.1% drawdown vs about 24.3% estimated loss), but this is not proof.
- **Test:**
  - Compound the monthly net returns and compare the terminal NAV and drawdown with the reported figures.
  - Confirm the funded-capital versus notional basis and the treatment of hedge margin and cash.
- **Do not implement if:** the reconstruction differs by more than rounding (the pipeline is not decision-grade), or the drawdown on a funded basis breaches the risk budget. Drawdowns are already 3–5.5× annual volatility.

---

**Bottom line:** No test here can produce an "implement." The best possible outcomes come from points 2, 6 and 9: finding a fixable drag or misalignment. That would justify a redesign and a test on untouched data, with the trial count carried forward from 41.
