# Verdict (3 Oct 2026)

Labels: CONF = confirmatory (frozen study), POST-HOC = chosen after seeing the data, FWD = forward test. Claim IDs refer to `results/claims.csv`.

## 1. Verdict on each strategy

| Strategy | Label | Verdict |
|---|---|---|
| A3 (Study 1 primary) | CONF | **Do not implement.** Test Sharpe −0.58, IC −0.021 (t −1.08), placebo p 0.72, fails gates G2–G5. This verdict stands and nothing below changes it. [C01–C07] |
| A0, A1, A1-T, A4 | CONF | Negative in the test (−0.36 to −0.79); not primary; no claim. [C08] |
| Study 1b (Opus follow-up) (A4) | exploratory | Launched after the test was seen. Sharpe +0.01 but IC t −0.10, alpha t 0.05, fails G2–G5; its gross came from one long industry. Evidence about agents, not about the strategy. [X01, X02, X04] |
| W wage growth (declared headline) | POST-HOC | Modest and fragile: test Sharpe +0.16, IC +0.049 (t 2.04), placebo p 0.02, but alpha t 0.29, a value/momentum tilt (HML −0.43, Mom +0.22), Sharpe −1.71 in the last 18 months, DSR 0.02. Not distinguishable from noise after the looks taken. Forward-tested. [V_V2a_SR, V01, V11] |
| SC signed composite | POST-HOC | Negative (test −0.15). Learned signs did not help. [V_V2b_SR, V06] |
| W+MOM wage + momentum | POST-HOC | Test +0.35, alpha t 1.36, placebo p 0.26, DSR 0.09; momentum supplies the return. Noise after the looks taken. Its ETF book has four legs. [V_V2c_SR, V05, F04] |
| **HQ12 −(hires + quits), 12-month hold** | POST-HOC | **The thesis result, fragile in time.** Positive in every window (+0.50 research, +0.29 test, +0.35 full, +0.29 last 18m); 12-month IC +0.096 (t 2.43) against a 1-month IC of −0.02; alpha +0.26%/month (t 1.5 test, 1.9 full); survives components, holding 9–18 months, 50 bp costs (break-even 68 bp) and every drop-one run (min +0.18). It fails one pre-declared condition: the first test half is −0.21 (second +0.64), and the test bootstrap interval includes zero. DSR 0.05 at 132 trials. Post-hoc, not tradeable on this evidence; the forward test is live. [V_V2d_SR, V02, V03, R1a–R9a, R12, R13] |

## 2. The story in one paragraph

Public labor flows do carry information about industry returns, but as slow cost news rather than fast demand news. The preregistered strategy traded the fast channel: it bet that industries with rising openings, hires and hours would outperform next month, and it lost money in a one-time test on 142 untouched months (Sharpe −0.58). Two of its four signs were wrong and the one stable short-horizon signal, wage growth, had been dropped during the build. When we look at horizons instead of months, the picture inverts: industries that hire and lose workers fastest earn lower returns over the following 9 to 24 months, as investment-based asset pricing predicts, and a 12-month book built on that sign (HQ12) is positive in every window we have. That book was designed after the test was opened, it was negative in the first half of the test, and its deflated Sharpe is near zero, so it is a hypothesis with a live forward test, not an implementable strategy. Our verdict is still "Do not implement".

## 3. What we can claim

- The preregistered strategy fails cleanly and we know why: wrong signs [D03], wrong horizon [D04, R2a], an untestable moderator [D06, D07], agent features active in 3 test months [D12], over-shrinkage and a binding risk cap [C18, D13], concentrated losses [D09]. Costs were not the cause [C15].
- Wage growth is the only short-horizon labor signal whose IC exceeds 1.5 standard errors in both periods [D01]; both blinded agent runs rediscovered it [D7b table].
- Hiring and quits predict returns with a negative sign at 9–24 months and not at 1 month [R2a, R2b]; hires alone carry most of it [R1a, R1b].
- HQ12's return is not carried by one industry [R7a], survives realistic costs [R5a], longer holding periods [R3a], and is not a factor tilt that FF5 + momentum explains (alpha t 1.5–1.9) [R6a], but it loads against profitability [R6b].
- The 13-group universe caps what any IC can deliver: a 0.1 twelve-month IC with breadth 13 implies an IR near 0.35 at best [R11a]; W realised far less than its IC implied because of the hedge, the cap and turnover [R11a].
- A stronger model followed the protocol better but found no more out-of-sample signal; the LLM judge over-attributed idea uptake [A01, A02, A03, D10].
- The forward test is frozen and the Q4 2026 books are dollar-neutral [F01–F05].

## 4. What we cannot claim

- That any post-hoc variant "passed": none met the v2 reading rule [V07]; HQ12 fails R4 and its test bootstrap interval includes zero [R9a, R13]; every DSR is below 0.2 [V08, R12].
- That HQ12 is tradeable, or that the tightness pattern in R8 (returns only when T falls or V/U > 1) is more than one draw with 54–88 months per cell [R8a].
- That Studies 2.1 and 2.2 as first run reflect real-time data: those numbers use revised data with fixed lags [S02]; the as-known rerun came later, in Study 2.3 (section 6) [T02].
- That the Opus study's +0.01 is evidence for the strategy [X01].
- Alpha from the labor signal beyond quality/growth exposure for A3 or W [C13, V11].

## 5. Figure plan for the report (10 figures)

| # | Figure | Claims it supports | Where |
|---|---|---|---|
| 1 | `fig_timeline.pdf` | D06 (no tight market in research) | 2b Data |
| 2 | `fig_agents.pdf` | A01, A02 (design) | 2c Implementation |
| 3 | `fig_loadings.pdf` | C13, V11, R6b (quality/growth tilts) | 3a Exposures |
| 4 | `fig_cumulative.pdf` | C08, V_V2a_SR (every preregistered book lost; W dashed) | 3b Time patterns |
| 5 | `fig_ic_signals.pdf` | D01–D03 (wrong signs, wage growth) | 3c Why it failed |
| 6 | `fig_horizon.pdf` | D04, D05 (sign flips with horizon) | 3c Why it failed |
| 7 | `fig_agents_scatter.pdf` | D10–D12 (fragile agent features) | 3c Why it failed |
| 8 | `fig_horizon_profile.pdf` | R2a, R2b (the thesis figure) | 3c What survives |
| 9 | `fig_v2_windows.pdf` | V_*_SR (all four variants by window) | 3c What survives |
| 10 | `fig_v2d_dropone.pdf` | R7a (no single industry) | 3c What survives |
| appendix | `fig_tightness.pdf`, `fig_v2d_tightness.pdf`, `fig_industry_pnl.pdf`, `fig_v2d_holding.pdf` | D07, R8a, D09, R3a | appendices |

## 6. Study 2.3: what changed in the reading

Run on 4 October 2026 from a spec hashed before running (`analysis/specs/study2_3_robustness.md`, 162 looks). Nothing changes in the verdict: Study 1's primary A3 stays "Do not implement" and HQ12 stays a post-hoc hypothesis that fails its reading rule. What the new runs add:

- **As-known data (R1).** The four variants were rerun on data as known at each decision date, after the as-known inputs were validated to machine precision against Study 1's saved features and A0 scores. HQ12 keeps its sign and most of its size: test Sharpe +0.20 against +0.29 with fixed lags, 12-month IC +0.085 (t 2.26) against +0.096; its first test half is still negative (-0.23), its break-even cost falls to 50 bp, its drop-one minimum to +0.05 and its deflated Sharpe is 0.02 at 162 looks. W earns +0.13 and W+MOM +0.46. SC flips from -0.15 to +0.24 because three of its six learned signs change with the data version, so SC is not a stable object. As-known and fixed-lag HQ12 scores pick the same top three groups in only 39% of test months. The reading fixed in the spec is "as-known confirms the fixed-lag reading"; the months affected by the 2025 shutdown are handled correctly in this rerun. [T01-T09]
- **Risk overlay (R2).** Reaching the 10% volatility target would need a median gross exposure of 2.6 for A3 and 2.4 for HQ12, so the cap of 2 binds in 87% and 83% of test months. With the cap at 3 or removed, realised volatility rises to about 10% and the Sharpe ratio does not improve (A3 -0.61 and -0.62; HQ12 +0.24). The cap explains the volatility shortfall, not the losses. [B05, T10, T11]
- **Rank-weighted books (R3).** Holding all 13 groups in proportion to their rank changes little: A3 -0.49 (transfer coefficient 0.83) against -0.58; HQ12 +0.31 against +0.29. Portfolio construction is not what failed. [B06, T12]
- **Study 1 diagnostics.** The block-bootstrap 90% interval of A3's test Sharpe is [-0.99, -0.16], and the A3 score has no IC at any horizon from 1 to 24 months. Study 1's freeze record checks out: the hash of FREEZE.json equals the one stored when the test was opened, 0.04 seconds later. [B01-B04]
- **Agents (R4, R5).** In both agent studies the gap between the communicating and independent arms is within the spread across seeds (permutation p 0.30 and 0.10, the smallest value 20 relabelings allow), and tokens per call are similar across arms. [T13, T15]
- **Breadth and capacity (R6, R7).** The 13 groups behave like about 9 independent bets (participation ratio of relative returns 9.1). With the proxy ETFs of the forward test, monthly trading reaches 1% of one day's volume in the least liquid ETF at about $0.5 million of AUM for A3 and $1.2 million for HQ12; gate G5 stays failed. [T16, T17]
- **Judge fix (R8).** Requiring a verbatim quote made the Sonnet judge's answers usable (8 of 8, 7 in agreement with the human) but did not reduce the Opus judge's false yes (8 of 17 against 7). [T18, T19]
- **Feedback ablation (R9).** On research data only, 4 of 48 valid proposals used a regime gate when the feedback showed IC by tightness tercile and 3 of 50 when it did not. The rerun does not support the explanation that the tercile feedback caused the gates, and it produced fewer gates than the original run (15% to 29% of proposals per seed). [T14, T20, T21]
