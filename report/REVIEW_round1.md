# Independent review, round 1: "Follow the Workers" (MFE 230GA final project)

Reviewer: independent grader, no prior exposure to the project. Files read, in order: `FinalProject.pdf`, `report/main.pdf` (19 PDF pages; printed page numbers run 1 behind the PDF index because the cover is unnumbered; I quote printed page numbers below), `report/main.tex`, `results/claims.csv`, and the source files the claims point to. Nothing was modified; `230ga-follow-the-workers/` was only read.

---

## A. Grade against the rubric

### Thesis, strength and clarity: 32 / 40

The thesis is well motivated and unusually honest. Two channels (demand news at 1-3 months, cost/investment news at 9-24 months) with opposite signs, a tightness moderator, and a clean statement of what was preregistered versus what the data later said (Table 1). The economics cite the right literature (Belo-Lin-Bazdresch, Kuehn-Simutin-Wang, Hong-Torous-Valkanov) and the "Do not implement" verdict follows from the data rather than fighting it. That is the strongest part of the report.

Deductions. (i) The thesis as traded contradicts the thesis as believed: the preregistered book traded the demand channel at one month, and the report ends by endorsing the cost channel at twelve months, which is a different thesis adopted after the test was opened; the executive summary blurs the two by stating the 12-month reversal as a finding ("industries that hire and lose workers fastest earn lower returns over the following 9 to 24 months, as investment-based asset pricing predicts") before the caveat. (ii) The one explanatory diagram, Figure 1, is broken: the "Demand news" and "Cost and investment news" boxes overlap and the "(1-3 months)" line is hidden, so the thesis figure a professor looks at first is unreadable. (iii) "Two of four preregistered signs were wrong" is generous: Table 1 shows F1 openings also carries the wrong sign in the full sample (-0.005 against a + prior); the precise statement is that F4 and F5 are wrong in both periods and F1 is wrong but negligible. (iv) The 13-group universe (effective width "closer to 8 or 9", Appendix C) is a design weakness the thesis should have confronted up front, not in a limits paragraph; with BR of 13 for the 12-month book, the thesis was never going to produce a tradable Sharpe, and the report says so only in Section 3.3.

### Execution: 30 / 40

What is here is rigorous: ALFRED vintages with four data variants, a preregistered risk model with hedge, volatility target, gross cap and costs, five pass/fail gates, a circular-shift placebo, Holm-adjusted comparisons, horizon analysis from 1 to 24 months, a hashed post-hoc battery with drop-one, holding-period, cost, bootstrap and deflated-Sharpe checks, and a fundamental-law decomposition that explains why realised Sharpes fall short of IC-implied ones. The course windows (full, post-2010, last 18 months) are all reported. This is well above the typical course project.

Deductions, in order of weight. (i) The rubric asks explicitly whether you "critically evaluated" the AI; the "Our critique" column of Table 7 is empty in all six rows (five TODOs) and the Reflection paragraph is marked "draft" and TODO. As submitted, the single most heavily weighted execution item is missing, and the P6 row admits the AI drafted the report itself, so a grader will ask who evaluated whom. (ii) Several numbers have no source or do not match their source: "607 calls" and "905 calls" (p. 9) appear in no file I could find (the call logs have 307 and 402 lines); the book-build time "09:17:55Z" (pp. 8, 18) appears in no source file, while `gate3.md` and the book files' timestamps say 10:00:17Z; "28 of 36 judge outputs were not valid JSON" and "guessed the engineering assistant was OpenAI Codex" (Table 7) have no supporting file. (iii) Internal inconsistencies: Opus features "7 passed the research filter" (p. 9) versus "6 of 6" failed (p. 7); V2d alpha t = 1.37 in Table 6 versus 1.48 in the text with no note that the lag count differs; "every selected feature failed the test" while two Opus selected features have positive test ICs (+0.022, +0.011 in `d7_selected_features.csv`), so "failed" needs a definition. (iv) The V2d placebo reported in Table 6 (p = 0.85) is a one-month placebo applied to a twelve-month signal; a horizon-matched placebo exists in the claims register (V09: p = 0.06 test, 0.04 full) and is not in the report. (v) The post-hoc work uses revised data; the as-known rerun "was not run for lack of an API key", which is an avoidable gap given that 42% top-three agreement is reported. (vi) Section 3 runs about 4.1 pages against a 4-page limit, before the critiques are written.

### Originality: 17 / 20

Genuinely original on three counts: JOLTS and CES flows by industry as a rotation signal with point-in-time vintages; a blinded two-arm LLM agent experiment with a mechanical selector, an LLM judge and a human audit of the judge; and a hashed, time-stamped forward test with a pre-committed data-release check that actually fired. The deflated Sharpe that counts every look, including diagnostic looks, is rare in student work. Deductions: the agent experiment consumes about a page and a half of the main body to conclude "capability is not alpha", which is a finding about tooling rather than about the strategy; and the surviving idea (hiring predicts lower returns at a year) is the industry-level version of a known effect rather than a new one.

### Total: 79 / 100 as submitted

With the TODOs filled, the unsourced numbers fixed and the inconsistencies reconciled (fixes 1-5 below), I would expect 86-89.

---

## B. Number trace (I opened each source file; claims.csv was used only to find the locator)

| # | Number as printed (page) | Claim ID | Source file :: locator | Value I found | Match |
|---|---|---|---|---|---|
| 1 | Sharpe -0.58 (p. 1, 5, 6) | C01 | `230ga-follow-the-workers/outputs/follow_the_workers/outputs/sealed/initial/results.json` :: variants.ASOF.A3.sharpe | -0.58450 | yes |
| 2 | placebo p = 0.72 (p. 1, 6) | C05 | same results.json :: placebo.p | 0.71579 | yes |
| 3 | IC -0.021, t = -1.08 (p. 1, 6) | C03 | same :: variants.ASOF.A3.IC.1.mean / .t | -0.02133 / -1.0771 | yes |
| 4 | F4 layoffs IC +0.028 (Table 1, p. 2) | D02 | `analysis/output/tables/d1_signal_ic.csv` :: full_ic, F4 | 0.028129 | yes |
| 5 | W t = 2.50 (Table 1 note, p. 2) | D01 | d1_signal_ic.csv :: full_t, W | 2.5023 | yes |
| 6 | pooled correlation 0.998 (p. 3) | S01 | `analysis/output/data_vintage.md` :: row FIXEDLAG, pooled_corr | 0.998 | yes |
| 7 | same top three in 42% of months (p. 3) | S02 | data_vintage.md :: row ASOF, same_top3_share | 0.415 | yes, but 41.5 printed as 42 is rounding a rounded value; the file shows 0.415 not the raw share |
| 8 | V/U > 1 in 75 test months, 0 research (p. 3) | D06 | `analysis/output/tables/d3_regime_balance.csv` :: V/U > 1 | 75 / 0 | yes |
| 9 | ridge alpha = 1000 for every model (p. 3) | C18 | `.../outputs/selected_features.json` :: models.{A1,A1-T,A3,A4}.alpha | 1000 x4 | yes |
| 10 | cap bound in 87% of months; realised vol 7.8% (p. 4) | D13 | `analysis/output/tables/d9_risk_overlay.csv` :: Sonnet, A3 | 0.86620 / 0.078489 | yes |
| 11 | break-even cost -32 bp (p. 5) | C06 | results.json :: cost_breakeven_bps | -31.837 | yes |
| 12 | costs 1.1% a year, gross loss 3.5% (p. 5) | C15 | `d4_test_performance.csv` :: cost_ann, A3; results.json :: variants.ASOF.A3.mean_gross_annual | 0.011110 / -0.034767 | yes |
| 13 | A4 max drawdown -53.3% (Table 4, p. 6) | C08 / d4 | d4_test_performance.csv :: max_dd, A4 island agents | -0.53290 | yes |
| 14 | A1-T -4.9% / 8.2% / -36.3% (Table 4, `\prov`) | none in register | results.json :: variants.ASOF.A1-T.{mean_net_annual, volatility, max_drawdown} | -0.048781 / 0.082248 / -0.36318 | yes; should be added to claims.csv and un-`\prov`ed |
| 15 | V2a HML -0.43 (t -4.4), Mom +0.22 (t 3.3) (p. 6) | V11 | `analysis/output/tables/v2a_factor_loadings_test.csv` | -0.43290 (-4.4327) / 0.21694 (3.3073) | yes |
| 16 | V2d RMW -0.36 (t -4.45) (p. 6) | R6b | `analysis/output/tables/v3_r6_alpha.csv` :: test, RMW | -0.36232 (-4.4505) | yes |
| 17 | last-18-month IC t of 0.44 (p. 6) | no claim ID (`% src` points at results.json directly) | results.json :: windows.A3.last_18.IC.t | 0.43686 | yes |
| 18 | health care -26, construction -19, finance -16, costs -13 points (p. 7) | D09 | `analysis/output/tables/d5_industry_pnl.csv` | -26.21 / -19.18 / -16.30 / -13.15 | yes |
| 19 | V2d alpha +0.26% a month, t 1.48 test, 1.92 full (p. 7) | R6a, R6a2 | v3_r6_alpha.csv :: intercept | 0.26095% (1.4807) / 0.26463% (1.9204) | yes |
| 20 | bootstrap [-0.07, +0.65] test, [+0.05, +0.64] full (p. 8) | R9a | `analysis/output/tables/v3_r9_bootstrap.csv` | -0.06759 / 0.64985; 0.05036 / 0.64145 | yes |
| 21 | DSR 0.05 test, 0.16 full at 132 looks (p. 8) | R12 | `analysis/output/tables/v3_dsr132.csv` :: V2d | 0.049379 / 0.16312 | yes |
| 22 | V2d TC 0.48 implies +0.17 (p. 7) | R11a | `analysis/output/tables/v3_r11_fundamental_law.csv` | 0.47927 / 0.16619 | yes |
| 23 | best IC 0.136 vs 0.059 (Opus), 0.049 vs 0.083 (Sonnet) (p. 9) | A05 | `.../agents/search_summary.json` :: metrics.best_so_far_ic | 0.13562/0.05940; 0.04886/0.08308 | yes |
| 24 | **607 calls / 905 calls (p. 9)** | **none** | not in any file; `agents/log.jsonl` has 307 and 402 lines, `agents/responses/` has 199 and 294 files | not found | **no: unverifiable** |
| 25 | A3 Sharpe by vintage -0.52 / -0.56 / -0.53 (p. 3, 12) | C20 | results.json :: variants.{FIRST,REVISED,FIXEDLAG}.A3.sharpe | -0.52183 / -0.56050 / -0.52628 | yes |
| 26 | Opus A4 +0.01, research -0.40, placebo 0.56, -0.19 at 25 bp (p. 17) | X01 | `.../follow_the_workers_opus55_xhigh/outputs/sealed/initial/results.json` and research_summary.json | 0.00896 / -0.40294 / 0.55789 / -0.19255 | yes |
| 27 | durable manufacturing +0.27 (p. 17) | X04 | `analysis/output/diagnostics.md` :: table=1 (zero-indexed; it is the second table), Durable mfg, A4 (Opus) | +0.273 | yes; the unit (fraction of cumulative gross return) is not stated in the report |
| 28 | SPY hedge -0.40 / -0.06 / -0.24 / -0.02 (p. 18) | F03 | `analysis/forward/book_2026Q4_hedge.csv` | -0.39661 / -0.05767 / -0.23914 / -0.02208 | yes |
| 29 | **book built 09:17:55Z (p. 8, 18)** | F05 | `analysis/output/gate3.md` says book 10:00:17Z; book files' mtimes are 10:00:17Z | 10:00:17Z | **no: 09:17:55Z appears only in claims.csv's own sentence, not in any source** |
| 30 | F2 hires 12m IC -0.062 (-2.08) (Table 9, p. 15) | d2 | `analysis/output/tables/d2_horizon_ic.csv` | -0.061770 (-2.0813) | yes |
| 31 | test first half: 71 months, -0.21, -1.4%, IC +0.097 (1.75) (Table 10, p. 15) | R4a | `analysis/output/tables/v3_r4_subperiods.csv` | 71 / -0.20857 / -1.418% / 0.097121 (1.7464) | yes |
| 32 | Oil 79%, Util 61%, Banks 51% (Table 8, p. 11) | none | `analysis/forward/etf_proxies.csv` :: group_composition_aug2026 | 79 / 61 / 51 | yes |

Rounding that changes meaning: none among the matched items. Two cosmetic ones: item 7 (41.5 -> 42) and "7 of 7" never appears but see the 7-vs-6 inconsistency below.

Numbers in the report with no `% src` comment at all (main.tex line numbers):
- l. 308: "607 calls", "905 calls" (also unverifiable, see item 24).
- l. 104: "78 series" (the `% src` on that line covers C20 only). `manifest.csv` has 80 admitted FRED/ALFRED rows (78 industry series plus JTSJOL and UNEMPLOY); `deviations.md` says 78. Pick one and say which.
- l. 318: "25 numbered findings" (I count 25 numbered items in `p1_response.md`, so it is right, but unsourced).
- l. 323: "28 of 36 judge outputs were not valid JSON": `migration_judgments.json` records 28 null `uses_claim` labels but no reason; no file says "invalid JSON".
- l. 326: "Guessed the engineering assistant was OpenAI Codex": not in `FINDINGS_AND_PROPOSAL.md`.
- l. 327: "Reproduced the sealed returns to 10^-16": claim S04 exists (1.51e-16) but the line has no `% src`.
- l. 249: BR 156 / 13 and the IR ceilings 0.6 / 0.35 (arithmetic, fine, but say so).
- l. 299: "a Q4 return anywhere between -10% and +10% is consistent with no skill (Appendix G)": the computation is in `analysis/forward/spec_frozen.md` l. 50, not in Appendix G, which contains no such statement.
- l. 283 (equation block): "60 months ending in m-2 (at least 36)"; l. 270: "12 HAC lags"; l. 274: "112 looks"; l. 285: "eleven checks", "132" (these are in `v2_spec.md` / `v3_spec.md`; add the src).
- Figure 3 text: "17 in the Opus study" (matches `human_review_submission.json`, items = 17).

Internal inconsistencies a grader will catch:
- l. 262 "6 of 6 Opus" (results.json `research_pass_sealed_failure_count` = 6) versus l. 333 "7 against 4" passed the research filter (`d7_agent_summary.csv` = 7). One of the two counts needs a footnote.
- Table 6 V2d "Alpha t +1.37" (6 lags, `v2_window_stats.csv`) versus text "t = 1.48 ... 12 HAC lags" (`v3_r6_alpha.csv`). Both correct; the table caption must state the lag.
- "every selected feature failed the test" (Table 7) versus `d7_selected_features.csv`, where Opus `islands_1_Temporal_4` and `islands_1_Temporal_6` have test ICs of +0.022 and +0.011. "Failed" means failed the sealed criterion; define it.
- Appendix A says the human audit is in `outputs/human_review_submission.md`; the file is `human_review_submission.json` (a `human_migration_review.md` also exists).
- Appendix F: "lost 1.41 over the last 18 months" is a Sharpe ratio, not a loss.

---

## C. Language and framing

### Post-hoc material that reads as confirmatory
- p. 1 (exec summary): "Across horizons the picture reverses: industries that hire and lose workers fastest earn lower returns over the following 9 to 24 months, as investment-based asset pricing predicts." Declarative finding stated before the "post hoc" caveat in the next sentence.
- p. 7, §3.3: "The variant that answers the thesis is V2d". `analysis/v2_spec.md` declared V2a the headline and V2b secondary; choosing V2d after the four results were seen is a second selection step and should be named as such.
- p. 8, Figure 4 caption: "The thesis result: the hiring score has no one-month IC and a positive IC from 9 to 24 months". It is a post-hoc horizon profile, and the pill says so, but the words say "thesis result".
- p. 7, §3.3: "Why the preregistered design failed. Four reasons, each visible in the data." These are post-hoc explanations; "visible in the data" asserts certainty that a four-explanation post-mortem on 142 months cannot have.
- p. 7, §3.3: "Its alpha is +0.26% a month (t = 1.48 ...)" stated as a property of the book, for a variant that fails the pre-declared reading rule.
- p. 8, §3.3: "We read this as a hypothesis with the right economics and too little data" ("right economics" was decided after the preregistered economics, traded at one month, failed).
- p. 6, §3.2: "the 12-month hiring book is the only one positive in every window" (true, labelled post-hoc in the table, but the sentence is a selling line).

### Where "Do not implement" is undercut
- p. 1: "A 12-month book on that sign is positive in every window (test Sharpe +0.29) ... a hypothesis under a live forward test (a Q4 2026 book frozen on 3 October)". The verdict is followed, within the same paragraph, by a Sharpe, a book and a trade date. Say explicitly that the forward books are paper books with no capital.
- p. 8, "Live forward test": four books (V2a-V2d) with ETF tickers and SPY hedges are described in trading detail; two of them (V2c, V2d) were added after the historical results were seen. This is implementing the post-hoc variants on paper, and the report should say in one sentence why that is consistent with "Do not implement".
- p. 8, "How robust is V2d?": four consecutive "not carried by" clauses before the one failure; the balance of the paragraph is promotional.
- p. 17, Appendix F: "lost 1.41 over the last 18 months" (a Sharpe).

### Jargon used without definition (first use)
- "IC" (p. 1, exec summary) before the definition in the Table 1 note (p. 2).
- "placebo test" (p. 1) and "circular-shift placebo with full refits" (p. 4): what is shifted, by how many months, how many shifts? (`results.json` has 95 shifts of 24-118 months; say so.)
- "Holm-adjusted bootstrap comparisons" (p. 4): which comparisons, how many?
- "blocked cross-validation" (p. 3).
- "Ledoit-Wolf covariance" (p. 4): no citation.
- "ALFRED vintages" (p. 2): never defined as the St. Louis Fed's archival database.
- "regime gate" / "gated on the 'low tightness' regime" (p. 7, 9).
- "HAC lags" (p. 7), "Newey-West" (figure axes): undefined.
- "looks" / "look count" (pp. 7-8): the DSR trial count; defined only by implication.
- "migration reports", "islands arm", "idea uptake" (pp. 4-5, 9): defined loosely in Figure 3.
- "Sonnet 5.5 at medium effort", "Opus 5.5 at extra-high effort" (p. 9): vendor settings, meaningless to a finance reader without one line.
- "tranche" (p. 4): defined by equation (3) only.
- "byte-reproducible", "hashed" (pp. 4, 9): fine for an engineer, one clause for a professor.

### Sounds AI-written
Good news first: no em-dashes, no "delve", "crucial", "notably", "furthermore", no bold "Answer:" label, "robust" only as a statistical term. The tells are structural rather than lexical:
- Aphoristic openers and closers: "Firms reveal their plans in the labor market before they reveal them in earnings." (p. 1); "Claude was a careful auditor and a poor source of out-of-sample signal." (p. 1); "the data were asking for no forecast at all." (p. 3); "capability is not alpha" (heading, p. 9).
- Repeated "X, not Y" antithesis: "a hypothesis ..., not a strategy" (p. 1); "the cap, not the volatility target" (p. 4); "mechanics, not prompts" (p. 9); "evidence about agents, not about the strategy" (p. 17); "a hypothesis with the right economics and too little data, not as alpha" (p. 8).
- Parallel triplets for rhythm: "free, timely and rarely used" (p. 1); "reproducing numbers, auditing code and timing, listing failure modes" set against "features that were artefacts of a regime gate, a judge that over-attributed, a red team that invented statistics" (p. 9); "blinding, a fixed evaluator, hashed specifications and a test opened once" (p. 9).
- Colon-led reveals: "Costs are not the explanation:" (p. 5); "The failure is informative:" (p. 1); "a DSR of 0.02: a value and momentum tilt that happened to work" (p. 7).
- The Reflection paragraph (p. 9) is the most AI-sounding passage and is already marked `\prov{draft}` with a TODO; Table 7 row P6 states that Claude "draft[ed] this report", so a grader will read the whole Claude-evaluation section as the AI grading itself unless the team's own words replace it.

---

## D. Page budget (measured with `pdftotext -bbox-layout`; text block spans y = 62 to about 790 pt on an A4 page)

| Item | Limit | Measured | Verdict |
|---|---|---|---|
| Executive summary | one paragraph, <= 230 words | 229 words counting each math expression as one token (LaTeX source); 239 words splitting the PDF text (e.g. "t = -1.08" counts as 3); plus one sentence still TODO | at the limit now, over once the Claude sentence is added |
| Section 2 | <= 5 pages | starts printed p. 1 at y = 322, ends p. 5 at y = 692: about 4.5 pages | OK |
| Section 3 | <= 4 pages | starts p. 5 at y = 692, ends p. 9 at y = 790: about 4.1 pages (0.13 + 3 + 1.0) | over by roughly 10 lines, and five critique cells plus the rewritten Reflection are still to be added |
| Main body through references | <= 10 pages | printed pp. 1-10 (references end about 40% down p. 10); PDF pages 2-11, cover excluded | at the limit |
| Appendices | - | printed pp. 11-18 (8 pages) | - |

---

## E. Top 10 fixes, ranked by expected effect on the grade

1. **Write the critiques.** Fill the five empty "Our critique" cells in Table 7 (`main.tex` ll. 318-327) and rewrite the Reflection (l. 338) in the team's words; remove `\prov{draft}`; add the exec-summary sentence (l. 23). This is the explicit "critically evaluate the AI" rubric item under Execution (40%). Needs humans (Alex, Elouan, Al Yazid, Romain, Piero as assigned).
2. **Fix Figure 1.** The tikz "Demand news" and "Cost and investment news" boxes overlap (`main.tex` ll. 38-56; increase the `yshift` on nodes `dem`/`cost` to about +-14 mm or shrink `text width`). First figure on page 2, currently unreadable. Editor.
3. **Rebalance the executive summary.** Keep "Do not implement" and its justification; compress the V2d and forward-test sentences into one that says "paper books, no capital, one quarter has no power"; cut to <= 230 words including the pending Claude sentence (ll. 17-23). Editor for the cut, human for the Claude sentence.
4. **Source or delete unsourced numbers.** 607/905 calls (l. 308: replace with the counts from `agents/log.jsonl`, 307 and 402, or have Alex supply the true call-log count and its file); 09:17:55Z (ll. 295, 464: the only file evidence is 10:00:17Z in `gate3.md` and the book files; either find the first-build log or change the time and say the book was rebuilt byte-identically at 10:00:17Z); "not valid JSON" (l. 323) and "OpenAI Codex" (l. 326) need a file or a softer wording; "78 series" (l. 104) versus 80 admitted FRED rows; add `% src` to l. 318 (25 findings), l. 327 (S04), l. 299 (spec_frozen.md l. 50). Editor, with Alex for the call logs.
5. **Reconcile the three internal inconsistencies.** 7 passed vs 6 of 6 failed (ll. 262, 333); Table 6 alpha t 1.37 vs text 1.48 (state "6 Newey-West lags" in the Table 6 caption, l. 274); define "failed the test" for agent features given two Opus features had positive test ICs (ll. 262, 320). Editor; confirm the 7-vs-6 definition with Alex.
6. **Bring Section 3 under 4 pages before adding the critiques.** Move the ETF/book composition sentences of "Live forward test" (ll. 296-298) to Appendix G where they already half-exist; replace the fundamental-law arithmetic sentence (l. 249) with a three-row table in Appendix D; trim the agents paragraph (l. 332-336), which repeats Table 7. Editor.
7. **Report the horizon-matched placebo for V2d.** Table 6 gives p = 0.85 from a one-month placebo for a twelve-month signal; claim V09 (`v2d_placebo_12m.csv`: 0.06 test, 0.04 full, 0.26 research) exists and is not in the report. Add it next to 0.85, labelled post-hoc and "added after v2". Editor.
8. **Reword the post-hoc-as-confirmatory sentences.** l. 269 "The variant that answers the thesis is V2d" -> "Of the four, V2d is the one whose sign tests the cost channel; it was not the declared headline (V2a was)"; Figure 4 caption (l. 281) "The thesis result" -> "Post-hoc horizon profile of the V2d score"; l. 253 "Four reasons, each visible in the data" -> "Four post-hoc explanations"; l. 21 exec summary reversal sentence -> conditional phrasing. Editor.
9. **Fix cross-references, paths and small errors.** "Appendix G" power statement (l. 299) is not in Appendix G: add one line there (10% annual vol -> about 5% quarterly s.d. -> +-10% is +-2 s.d.); `human_review_submission.md` -> `.json` (l. 352); "lost 1.41" -> "a Sharpe of -1.41" (l. 455); Figure 9 left title is clipped ("A3 test-period P&L by indus", `analysis/plots.py`); add A1-T to `claims.csv` and drop the `\prov` (l. 202); state the unit of "+0.27" (l. 456). Editor.
10. **Define jargon at first use and tighten the sign statement.** IC in the exec summary; circular-shift placebo (95 shifts of 24-118 months, full refits); Holm comparisons (four pairwise); blocked CV; HAC/Newey-West; "looks"; regime gate; cite Ledoit-Wolf (2004). Replace "two of four preregistered signs were wrong" (l. 20) with "F4 and F5 carry the wrong sign in both periods; F1 is wrong but near zero". Editor.

Remaining human TODOs that are not grade-critical but will be noticed if left: P1 disposition counts (l. 350, Alex), data-link access dates (l. 364, Elouan), freeze-hash confirmation against `FREEZE.json` / `evaluation_started.json` (l. 157, Alex; both files exist and are dated 2026-10-02T06:00:09Z), and the "6 astra" engineering-assistant name (l. 308, Alex). Build with `\draftfalse` for submission so no red TODO text or gold `\prov` boxes remain.
