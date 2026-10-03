# Independent review, round 3 (grader's read of report/main.pdf built 3 Oct 2026 11:30)

Reviewer: fresh Claude subagent, no prior exposure to the project. Inputs read in order: `FinalProject.pdf`, `report/main.pdf` (19 pages, A4; cover + printed pages 1–18), `report/main.tex`, `results/claims.csv` (100 rows, all `verified=y`), then the source files named in the register. Nothing was modified. "The AI assistant" below means Claude, per the term's substitution for "ChatGPT" in the brief.

## A. Grade against the rubric

| Criterion | Score | |
|---|---|---|
| Strength and clarity of thesis | **32 / 40** | |
| Execution | **30 / 40** | |
| Originality | **18 / 20** | |
| **Total** | **80 / 100** | Estimate once the human items in §E are done: 87–89 |

**Thesis (32/40).** The thesis is stated as three hypotheses with mechanisms, citations and a diagram (Fig. 1), it is answered head-on in the "Answer to the thesis" box, and the conclusion "Do not implement" is unambiguous. Deductions: the strategy actually traded (H1 at one month) is not the thesis the report ends up believing (H2 at twelve months), and H2 appears in §2.1 with the same weight and citations as H1 although it was formulated after the test was opened, so the three-hypothesis frame reads as retrofitted; the motivation for a one-month demand effect from data published with a 1–2 month lag is thin and the report's own §3.3 says the preregistered signs of two of five signals were wrong and the one working signal was dropped "during the build", which is a design error, not bad luck; and the universe (13 groups, effectively 8–9) was known in advance to cap the Sharpe near 0.3–0.6, which makes the primary test underpowered by construction. The executive summary is one paragraph as required but at 15 printed lines and ~18 statistics it is hard to read cold.

**Execution (30/40).** The methodology is the strongest I have seen in a course project: ALFRED vintages with four data variants, hashed preregistration with five gates and a single opening, circular-shift placebo, Holm, deflated Sharpe with an explicit look count, Ledoit–Wolf, beta hedge, cost sensitivity and break-even, drop-one, block bootstrap, horizon profile, fundamental-law reconciliation of every result. Deductions, in order of weight: (i) the rubric's explicit item "Did you critically evaluate the AI?" is still empty in the document, with six red `[TODO: critique: ...]` cells in Table 8, a Reflection paragraph marked `draft`, and no Claude sentence in the executive summary; (ii) the brief requires AI transcripts in the appendix and Appendix A gives repository paths only, so a grader with the PDF alone cannot see any prompt output; (iii) eleven red TODO marks and a yellow `draft` pill are visible in the PDF; (iv) the post-hoc H2 result is labelled "supported" in the headline box although it fails the team's own pre-declared reading rule (DSR 0.05, one-month placebo 0.85); (v) §3 runs to ~4.5 pages against a 4-page limit and the body sits exactly at 10 pages before the TODO text is added; (vi) all post-hoc work uses revised data, the as-known rerun "was not run for lack of an API key", and as-known data pick a different top three in 58% of months.

**Originality (18/20).** Novel data (JOLTS and CES by industry, vintage-correct), a preregistered and hashed design, blinded LLM agents in two arms with a human-audited LLM judge, and a stronger-model replication are well beyond the brief. Deduction: the agent experiment is a study about agents attached to a strategy report (the report says so itself, App. F), and the prompt designs shown (P1, P2, P4) are good but short; the brief's "bonus for creative but well-structured" use is earned, the "unique insight" about the strategy is modest (the 12-month hiring reversal is Belo et al. 2014 at the industry level).

## B. Fifteen (plus five) numbers traced to source files

Every value below was read from the file named in `claims.csv`, not from the register's `file_value` column.

| # | Number as printed (where) | Claim ID | Source file | Value found | Match |
|---|---|---|---|---|---|
| 1 | Sharpe −0.58 (Exec. summary; Table 4) | C01 | `230ga-follow-the-workers/outputs/follow_the_workers/outputs/sealed/initial/results.json` → `variants.ASOF.A3.sharpe` | −0.58450 | yes |
| 2 | placebo p = 0.72 (Exec. summary) | C05 | same → `placebo.p` | 0.71579 | yes |
| 3 | F4 layoffs IC +0.028 (Table 1) | D02 | `analysis/output/tables/d1_signal_ic.csv` → `full_ic`, F4 | 0.028129 | yes |
| 4 | "same top-three groups in only 42% of months" (§2.2) | S02 | `analysis/output/data_vintage.md` table 0, ASOF, `same_top3_share` | 0.415 | yes (41.5 rounded up) |
| 5 | V/U > 1 in 75 test months (§2.2, Fig. 12) | D06 | `analysis/output/tables/d3_regime_balance.csv` → `V/U > 1`, test | 75 | yes |
| 6 | cap bound in 87% of A3 months; realised vol 7.8% (§2.3) | D13 | `analysis/output/tables/d9_risk_overlay.csv` → Sonnet/A3 `cap_binding_share`, `realised_vol` | 0.8662; 0.07849 | yes |
| 7 | ridge α = 1000 for every model (§2.3) | C18 | `.../outputs/selected_features.json` → `models.{A1,A1-T,A3,A4}.alpha` | 1000 ×4 | yes |
| 8 | A4 max drawdown −53.3% (Table 4) | none (comment cites `d4_test_performance.csv`) | `analysis/output/tables/d4_test_performance.csv` → `max_dd`, "A4 island agents"; also `results.json variants.ASOF.A4.max_drawdown` | −0.53290 | yes |
| 9 | RMW +0.19 (t 2.2), HML −0.15 (t −2.0) (§3.1) | C13 | `results.json` → `attribution.A3.coefficients/t_statistics` | 0.1942 / 2.156; −0.1464 / −2.014 | yes |
| 10 | V2d RMW −0.36, t −4.45 (§3.1) | R6b | `analysis/output/tables/v3_r6_alpha.csv` → test, RMW | −0.36232 / −4.4505 | yes |
| 11 | last-18-month IC t of 0.44 (§3.2) | none (comment cites `results.json windows.A3.last_18.IC.t`) | `results.json` → `windows.A3.last_18.IC.t` | 0.43686 | yes |
| 12 | A3 TC 0.80 → implied IR −0.21 (§3.3) | R11a | `analysis/output/tables/v3_r11_fundamental_law.csv` → A3 `tc`, `implied_ir` | 0.80281; −0.21393 | yes |
| 13 | health care cost 26 points; costs 13 (§3.3) | D09 | `analysis/output/tables/d5_industry_pnl.csv` → `contribution` | −0.26208; −0.13147 | yes |
| 14 | bootstrap 90% interval [−0.07, +0.65] test (Table 7) | R9a | `analysis/output/tables/v3_r9_bootstrap.csv` → test `low`, `high` | −0.06759; 0.64985 | yes |
| 15 | 199 and 294 logged calls (§3.4) | A06 | `.../outputs/agents/log.jsonl` (both studies), entries with `kind != evaluation` | 199 (109 candidate + 18 migration + 72 judge); 294 (108 + 18 + 168) | yes |
| 16 | Opus A4 test Sharpe +0.01 (App. F) | X01 | `.../follow_the_workers_opus55_xhigh/outputs/sealed/initial/results.json` → `variants.ASOF.A4.sharpe` | 0.00896 | yes (rounds to +0.01) |
| 17 | SHA-256 735a8ffa…, frozen 09:03:56Z (§3.3, App. G) | F08 | `analysis/forward/spec_frozen.sha256` | 735a8ffa9c9c…; `frozen_utc 2026-10-03T09:03:56+00:00` | yes |
| 18 | "25 findings" (Table 8, P1) | **no claim ID, no `% src`** | `.../outputs/p1_review.md` | 25 numbered items | yes |
| 19 | Holm-adjusted p = 1.0 for every pair (Table 4 note) | C16 | `results.json` → `comparisons[0..3].holm_p` | 1.0 ×4 | yes |
| 20 | "78 series" (§2.2) | none (comment cites frozen `report/report.md` §2b) | `.../follow_the_workers/report/report.md` line 17 | "all 78 core first-vintage dates" | soft: the source counts first-vintage *dates*, the report says *series*; reword or cite the manifest |

No numeric mismatch found. The register is unusually good. Three things a grader would still notice:

- Two deflated-Sharpe values for the same book appear on facing pages: Table 6 prints DSR 0.06 (112 looks) and the headline box and §3.3 say 0.05 (132 looks). Both are correct, but the headline should use one convention and say which.
- Numbers in the main body with no `% src` comment: "108 proposals", "two arms of three agents", "three repetitions" (§2.3, source would be `d10_agent_design.csv`); "25 findings" (Table 8); "DSR counts 112 looks" (Table 6 caption; source `analysis/v2_spec.md` line 89); "54 to 88 months per cell" (Fig. 12 caption; source `v3_r8_tightness.csv`); "medium effort" / "extra-high effort" (§3.4; A06 covers call counts, not the effort setting). The backtest constants (60/36 months, ±3, 24 months, grid 0.01–1000, 10 bp / 2 bp) are design parameters and acceptable without a claim row, but a one-line pointer to `params.py` would close the loop.
- Table 5 note: "A3's research and full-sample figures use the 88 months with a forecast (from June 2007)". The research figure uses 88 months; the full-sample figure (−0.44) uses 231 months from June 2007 (`course_windows.A3.full.n = 231`). The sentence as written says both use 88.

## C. Post-hoc read as confirmatory; sentences that undercut "Do not implement"; jargon; AI tells

**Post-hoc presented as confirmatory**

1. Headline box, §3 (main.tex 193): "H2, cost channel: *supported*, fragile in time". The result fails the pre-declared reading rule (DSR 0.05, one-month placebo 0.85, alpha t 1.37–1.48), and the rule that it "passes six of seven" of (Table 7) was itself frozen at 09:52 after the v2 results were seen at 09:01. "Supported" is a confirmatory verb. Suggest "consistent with H2; not established".
2. Executive summary (line 21): "which investment-based asset pricing would predict" is a theory fitted after the horizon profile was seen, and the sentence leads with "positive in every window (test Sharpe +0.29)" before the caveats. Lead with the caveat.
3. Figure 12 caption (line 454): "it earned its return when tightness was falling or V/U > 1" is a claim, while the text two lines above (line 301) promises the pattern is "recorded without a claim". The IC pattern is the opposite (12-month IC highest when T is *rising*, +0.115, t 2.52; `v3_r8_tightness.csv`), which the caption omits.
4. §3.3 "Why H1 failed, 1. Wrong signs" (line 269): the "right" signs are the in-sample signs, and layoffs' positive IC has t ≈ 0.9–1.4 in every window; "wrong" implies more certainty than the t-statistics carry. "Signs not supported by the data" is accurate.
5. §3.2 (line 233): "the post-hoc H2 book is the only one positive in every window" selects the one window definition (five overlapping windows) in which V2d looks uniformly good, while the halves split (−0.21 / +0.64) is deferred to Table 7.
6. §2.1 (lines 35, 39) and Fig. 1: H2 carries the same citations and box as H1. The "(tested post hoc)" tag is there, but the diagram presents all three as the design. State in one sentence whether H2's 6–24-month claim was written down before or after the horizon profile was seen; the current wording leaves it ambiguous.
7. Table 7 "Holds? yes (full)" for the bootstrap: the test interval includes zero; "yes (full)" is a reading allowed by the rule only because the rule says "test or full". Acceptable, but say so in the caption.

**Sentences that undercut "Do not implement"**

- Exec. summary (lines 21–23): the sequence "Do not implement ... A 12-month book on that sign is positive in every window (test Sharpe +0.29) ... It runs as paper books in a forward test" reads as "but this one works". Reorder so the deflation and first-half loss come before the Sharpe.
- Headline box (line 193): "a forward test is live" next to "supported".
- §3.3 heading and first sentence (line 301): "How robust is the H2 book? It fails one of the seven ... and passes the other six" is a scorecard that invites implementation.
- App. G (lines 485–489): full holdings for four books, ETF netting and hedge ratios read like a trade ticket. Fine for a paper test, but one line saying "no position of any size is recommended" would close the door the executive summary opened.

**Undefined or late-defined jargon**

- BR (breadth) is never defined; TC is used in §2.2 (line 105) and defined only in §3.3 (line 264).
- V2b is never defined in the report (its spec, "signs learned on research data", exists only in `analysis/v2_spec.md`); V2c is described only as "adding momentum" (line 279). Table 6 lists both.
- "seal opened" (Table 8, P4) and "sealed" are not introduced; the main text uses "frozen" and "opened once".
- "JSON-only rule" (Table 8, P3); "effort" as a model setting (§3.4); "migration reports" and "islands" are used before being explained (line 164 explains them in passing after Table 3 has used "communicating").
- "regime gate" is defined at line 272 but used earlier in Table 8 column 3 (which is read after, so acceptable) and in Figure 11.
- Typographic: the run-in heading renders as "How robust is the H2 book?." (question mark followed by the template's period) on printed page 8.

**AI-written tells** (no "delve/crucial/notably/furthermore", no em-dashes; the prose is clean at the word level, the tells are structural)

- A bold-label answer block: the "Answer to the thesis" key box is exactly the "**Answer:**" pattern.
- Aphoristic closers: "The fundamental law sizes every result." (line 264); "What protected us was mechanics: blinding, a fixed evaluator, hashed specifications and a test opened once." (line 340); "Thirteen groups bound what any signal can earn" (line 105); "One quarter has almost no power" (line 323).
- "X, not Y" contrast endings, five in nine pages: "post-hoc holdings, though not the conclusions" (111); "the cap, rather than the volatility target" (153); "quality and growth tilts rather than bets on labor news" (226); "shows up slowly, not within a month" (437); "evidence about agents, not about the strategy" (477).
- Parallel triplets for rhythm: "features that were artefacts of a regime gate, a judge that over-attributed, a red team that invented statistics" (340); "reproducing numbers, auditing code and timing" (340); "free and timely" (31).
- Colon-led explanations: "That is plausible: ..." (227); "Losses were concentrated: ..." (275).
- The Reflection paragraph (line 340) is abstract ("mechanics", "judgement about evidence") and is marked `draft`; Table 8 says Claude "draft[ed] this report" (P6), so the voice problem is literal and the team must own at least the executive summary, Reflection and critiques in their own words.
- Unsupported assertion in the thesis paragraph: "industry rotation rarely uses them" (line 31), no citation.

**Paragraphs longer than ~8 printed lines (main body)**

- Executive summary: 15 lines (one paragraph is required by the brief, but it carries ~18 numbers; cut to ≤ 11 lines).
- §2.2 "Universe, a design constraint": 9 lines (printed page 3).
- §2.2 "Point-in-time data": 8 lines (borderline).
- Appendix F single paragraph: 9 lines; Appendix G "Books" bullet: 10 lines (appendix, lower priority).

## D. Page budget (pdftotext -bbox; text block 59.5–782.4 pt on A4, 722.8 pt high)

| Item | Limit | Measured | Status |
|---|---|---|---|
| Executive summary | ≤ 225 words | 235 words as printed (excluding the red TODO placeholder; 249 with it); 225 by LaTeX source-word count | over by ~10 printed words, and the Claude sentence (~20 words) is still to come |
| Section 2 | ≤ 5 pages | starts printed p. 1 at y = 322 (0.64 of a page) + pp. 2–5 = **4.64 pages** | within |
| Section 3 | ≤ 4 pages | pp. 6–9 full + p. 10 to y = 442 (0.53) = **4.53 pages** | **over by ~0.5 page** (Table 8 spills onto p. 10) |
| Main body through references | ≤ 10 pages | References end at the bottom of printed p. 10 = **10.0 pages** | at the limit; six critique cells, the Reflection rewrite and the summary sentence will push it over unless something is cut |
| Appendices | – | printed pp. 11–18 (8 pages) | fine |

Visible draft artefacts in the PDF: 11 red TODO marks (exec. summary, honesty box, §3.4 ×2, Table 8 ×6 incl. the header-adjacent ones, App. A, App. B, App. G) and one yellow `draft` pill; `\drafttrue` is set in `preamble.tex`.

## E. Top 5 fixes by grade impact

1. **Write the critical evaluation of the AI, in the team's words** (Execution, ~5 points). Six "Our critique" cells in Table 8 (main.tex 350–359, ≤ 25 words each), the Reflection paragraph (line 340, remove `\prov{draft}`), the Claude sentence in the executive summary (line 24), the "6 astra" engineering-assistant vendor (line 333), the P1 disposition counts (line 374). Then build with `\draftfalse`. **Human** (Alex, Elouan, Al Yazid, Romain, Piero as assigned); the editor can only remove the marks.
2. **Put the transcripts in the appendix** (Execution, ~2–3 points). The brief says "Include ChatGPT transcripts"; Appendix A (lines 371–380) gives paths. For P1, P2 and P4 add the prompt, a half-page verbatim excerpt of the output and the disposition summary (`p1_review.md` has 25 numbered dispositions; `p4_review.md` likewise); for P2/P3 one agent turn and one judge verdict with the human label. **Editor** can assemble; a human should sign off that the excerpts are representative.
3. **Stop calling the post-hoc result "supported"** (Thesis and Execution, ~2 points). Line 193 "supported, fragile in time" → "consistent with H2; not established (fails the pre-declared rule)"; line 21 reorder so "post hoc, lost money in the first half, DSR 0.05" precedes "+0.29"; line 454 caption → "recorded without a claim; the 12-month IC is highest when T is rising"; line 301 drop the "six of seven" scorecard opening. **Editor**.
4. **Bring §3 under 4 pages and leave room for item 1** (Execution, ~1–2 points, and avoids a formal breach). Options in order of least damage: move Figure 6 (horizon profile) to Appendix D next to Figure 9, which shows the same thing; move Table 7 to Appendix D and keep the one-sentence summary at line 301; shrink Table 8 to `\tiny` or merge "What we changed" into "Our critique"; cut the executive summary to ≤ 225 printed words by dropping the parenthetical IC/t/p values (they reappear in the headline box). **Editor**; a human decides which figure goes.
5. **Make the thesis section self-contained and honest about sequencing** (Thesis, ~1–2 points). Define BR and TC at line 105; add one sentence at line 39 stating when H2's horizon claim was written down relative to the horizon profile; define V2b and V2c in one line each at line 277–279; fix the Table 5 note (88 vs 231 months, line 251); fix "?." at line 301; replace "industry rotation rarely uses them" with a citation or drop it; add `% src` comments for 108 / 25 / 112 / "54 to 88". **Editor**, except the H2 sequencing sentence, which a **human** who was there must write.

Secondary (no score change, but a grader will notice): the "78 series" vs "78 first-vintage dates" wording (line 108); the DSR 0.05/0.06 double convention (lines 193, 285, 301); the as-known rerun of V2a–V2d (R10) stays "not run" and should be stated once in §3.3 Limits as a known gap, which it is.
