# Verdict (3 Oct 2026)

Labels: CONF = confirmatory (frozen study), POST-HOC = chosen after seeing the data, FWD = forward test. Claim IDs refer to `results/claims.csv`.

## 1. Verdict on each strategy

| Strategy | Label | Verdict |
|---|---|---|
| A3 (preregistered primary) | CONF | **Do not implement.** Test Sharpe −0.58, IC −0.021 (t −1.08), placebo p 0.72, fails gates G2–G5. This verdict stands and nothing below changes it. [C01–C07] |
| A0, A1, A1-T, A4 | CONF | Negative in the test (−0.36 to −0.79); not primary; no claim. [C08] |
| Opus follow-up (A4) | exploratory | Launched after the test was seen. Sharpe +0.01 but IC t −0.10, alpha t 0.05, fails G2–G5; its gross came from one long industry. Evidence about agents, not about the strategy. [X01, X02, X04] |
| V2a wage growth (declared headline) | POST-HOC | Modest and fragile: test Sharpe +0.16, IC +0.049 (t 2.04), placebo p 0.02, but alpha t 0.29, a value/momentum tilt (HML −0.43, Mom +0.22), Sharpe −1.71 in the last 18 months, DSR 0.02. Not distinguishable from noise after the looks taken. Forward-tested. [V_V2a_SR, V01, V11] |
| V2b signed composite | POST-HOC | Negative (test −0.15). Learned signs did not help. [V_V2b_SR, V06] |
| V2c wage + momentum | POST-HOC | Test +0.35, alpha t 1.36, placebo p 0.26, DSR 0.09; momentum supplies the return. Noise after the looks taken. Its ETF book has four legs. [V_V2c_SR, V05, F04] |
| **V2d −(hires + quits), 12-month hold** | POST-HOC | **The thesis result, fragile in time.** Positive in every window (+0.50 research, +0.29 test, +0.35 full, +0.29 last 18m); 12-month IC +0.096 (t 2.43) against a 1-month IC of −0.02; alpha +0.26%/month (t 1.5 test, 1.9 full); survives components, holding 9–18 months, 50 bp costs (break-even 68 bp) and every drop-one run (min +0.18). It fails one pre-declared condition: the first test half is −0.21 (second +0.64), and the test bootstrap interval includes zero. DSR 0.05 at 132 trials. Post-hoc, not tradeable on this evidence; the forward test is live. [V_V2d_SR, V02, V03, R1a–R9a, R12, R13] |

## 2. The story in one paragraph

Public labor flows do carry information about industry returns, but as slow cost news rather than fast demand news. The preregistered strategy traded the fast channel: it bet that industries with rising openings, hires and hours would outperform next month, and it lost money in a one-time test on 142 untouched months (Sharpe −0.58). Two of its four signs were wrong and the one stable short-horizon signal, wage growth, had been dropped during the build. When we look at horizons instead of months, the picture inverts: industries that hire and lose workers fastest earn lower returns over the following 9 to 24 months, as investment-based asset pricing predicts, and a 12-month book built on that sign (V2d) is positive in every window we have. That book was designed after the test was opened, it was negative in the first half of the test, and its deflated Sharpe is near zero, so it is a hypothesis with a live forward test, not an implementable strategy. Our verdict is still "Do not implement".

## 3. What we can claim

- The preregistered strategy fails cleanly and we know why: wrong signs [D03], wrong horizon [D04, R2a], an untestable moderator [D06, D07], agent features active in 3 test months [D12], over-shrinkage and a binding risk cap [C18, D13], concentrated losses [D09]. Costs were not the cause [C15].
- Wage growth is the only short-horizon labor signal whose IC exceeds 1.5 standard errors in both periods [D01]; both blinded agent runs rediscovered it [D7b table].
- Hiring and quits predict returns with a negative sign at 9–24 months and not at 1 month [R2a, R2b]; hires alone carry most of it [R1a, R1b].
- V2d's return is not carried by one industry [R7a], survives realistic costs [R5a], longer holding periods [R3a], and is not a factor tilt that FF5 + momentum explains (alpha t 1.5–1.9) [R6a], but it loads against profitability [R6b].
- The 13-group universe caps what any IC can deliver: a 0.1 twelve-month IC with breadth 13 implies an IR near 0.35 at best [R11a]; V2a realised far less than its IC implied because of the hedge, the cap and turnover [R11a].
- A stronger model followed the protocol better but found no more out-of-sample signal; the LLM judge over-attributed idea uptake [A01, A02, A03, D10].
- The forward test is frozen and the Q4 2026 books are dollar-neutral [F01–F05].

## 4. What we cannot claim

- That any post-hoc variant "passed": none met the v2 reading rule [V07]; V2d fails R4 and its test bootstrap interval includes zero [R9a, R13]; every DSR is below 0.2 [V08, R12].
- That V2d is tradeable, or that the tightness pattern in R8 (returns only when T falls or V/U > 1) is more than one draw with 54–88 months per cell [R8a].
- Anything about as-known data for v2/v3: all historical v2/v3 numbers use revised data with fixed lags; the as-known rerun was not run [R10, S02].
- That the Opus study's +0.01 is evidence for the strategy [X01].
- Alpha from the labor signal beyond quality/growth exposure for A3 or V2a [C13, V11].

## 5. Figure plan for the report (10 figures)

| # | Figure | Claims it supports | Where |
|---|---|---|---|
| 1 | `fig_timeline.pdf` | D06 (no tight market in research) | 2b Data |
| 2 | `fig_agents.pdf` | A01, A02 (design) | 2c Implementation |
| 3 | `fig_loadings.pdf` | C13, V11, R6b (quality/growth tilts) | 3a Exposures |
| 4 | `fig_cumulative.pdf` | C08, V_V2a_SR (every preregistered book lost; V2a dashed) | 3b Time patterns |
| 5 | `fig_ic_signals.pdf` | D01–D03 (wrong signs, wage growth) | 3c Why it failed |
| 6 | `fig_horizon.pdf` | D04, D05 (sign flips with horizon) | 3c Why it failed |
| 7 | `fig_agents_scatter.pdf` | D10–D12 (fragile agent features) | 3c Why it failed |
| 8 | `fig_horizon_profile.pdf` | R2a, R2b (the thesis figure) | 3c What survives |
| 9 | `fig_v2_windows.pdf` | V_*_SR (all four variants by window) | 3c What survives |
| 10 | `fig_v2d_dropone.pdf` | R7a (no single industry) | 3c What survives |
| appendix | `fig_tightness.pdf`, `fig_v2d_tightness.pdf`, `fig_industry_pnl.pdf`, `fig_v2d_holding.pdf` | D07, R8a, D09, R3a | appendices |
