# Independent review, round 2: "Follow the Workers" (MFE 230GA final project)

Same reviewer and rules as round 1 (read-only; nothing imported from `230ga-follow-the-workers/`; files there were read as text or JSON only, with `python3 -B`). Report build checked: `report/main.pdf` and `report/main.tex` as of commit `dd9a851`, `results/claims.csv` with 100 claims. Printed page numbers are quoted (PDF index minus one).

Summary: the editor-level fixes landed and most are correct. The fix round also introduced one substantive regression (a sentence of Section 3.3 is now commented out of the PDF) and one silent loss (a human TODO no longer renders). Details below.

---

## 1. Re-grade

### Thesis, strength and clarity: 33 / 40 (was 32)

The executive summary now states the preregistered failure precisely (layoffs and hours, not "two of four"), frames the 12-month reversal as "consistent with" rather than a finding, and says the forward books carry no capital; Figure 1 renders correctly. The structural tension remains: the thesis that was tested (demand news at one month) is not the thesis the report ends up believing (cost news at a year), and the effective breadth of 8-9 groups is still introduced as a limit rather than as a design constraint.

### Execution: 31 / 40 (was 30)

The unsourced numbers are sourced or corrected (call counts 199/294 from the log, A1-T registered, 78 series and the 28 undefined judge labels cited to the frozen report), the 7-vs-6 and 1.37-vs-1.48 inconsistencies are resolved with definitions in the text, and the horizon-matched placebo now sits next to the one-month one. Two things hold the score: the "Our critique" column and the Reflection, the rubric's explicit AI-evaluation item, are still TODO; and the fix round commented out the fundamental-law comparison sentence (A3 implied -0.21 vs realised -0.58, V2a +0.56 vs +0.16, V2d +0.17 vs +0.29), so the claim that the overlay "cost the monthly books most of what their IC allowed" now has no numbers behind it in the PDF.

### Originality: 17 / 20 (unchanged)

Nothing in the fix round changes the originality case: industry-level JOLTS/CES flows with vintages, a blinded two-arm agent experiment with an audited judge, and a hashed forward test. The agent material still spends more main-body space than its conclusion earns.

### Total: 81 / 100 as it stands. With the regression fixed and the human items written, 87-89 is reachable.

---

## 2. Fixes re-checked, and ten further numbers traced

### Specific fixes from the coordinator's list

| Fix | Where | Verified? | Note |
|---|---|---|---|
| Call counts 607/905 -> 199/294 | p. 9, l. 307; claim A06 | yes | `agents/log.jsonl` kinds: Sonnet candidate 109 + migration 18 + judge 72 = 199; Opus 108 + 18 + 168 = 294; `evaluation` entries (108 each) excluded. Matches `agents/responses/` file counts. |
| "6 of 6" -> "6 of 7", "failed" defined | p. 7 item 4, l. 263; claim C19 | yes | Text now gives the criterion (t >= 1.5 and positive IC in both halves) and says the one Opus feature that passed was not selected. |
| Book first-build time 09:17:55Z | App. G, l. 462, 470; claim F09 | partly | See item 2 of the trace table: the cited file was written after the fact; git commit `9f4a50f` is the independent evidence. |
| Table 6 caption states 6 NW lags; text gives 12-lag alpha and says V2d fails the rule | p. 7-8, l. 271, 275 | yes | |
| Horizon-matched placebo added | p. 8, l. 293; claim V09 | yes | 0.06 test, 0.04 full, labelled "added after the run and outside the reading rule" and flagged optimistic for overlap. Good. |
| Figure 1 yshift 14 mm | p. 2 | yes | Boxes no longer overlap; "(1-3 months)" visible. |
| Exec summary rebalanced, IC defined, 224 words | p. 1 | yes | 224 by LaTeX tokens, 234 splitting PDF text; Claude sentence still pending. |
| "Four post-hoc explanations"; V2d "not the declared headline"; Fig. 4 "Post-hoc horizon profile" | p. 7-8 | yes | |
| Holdings moved to App. G with the power line | p. 8 / p. 18 | yes | Power line uses V2d test vol 8.7% ("about 9%"), claim V04. |
| "lost 1.41" -> Sharpe; ".md" -> ".json"; "+0.27" unit stated | App. F, App. A | yes | |
| A1-T registered, `\prov` removed | Table 4, claim C23 | yes | |
| Jargon defined at first use; Ledoit-Wolf cited | keybox p. 4, l. 150, l. 158, l. 262 | yes | Placebo, Holm, DSR/looks, blocked CV ("contiguous time blocks with a one-month purge"), tranche, regime gate, ALFRED, HAC all defined. |
| "78 series" sourced | l. 105 | yes | `230ga-follow-the-workers/outputs/follow_the_workers/report/report.md` l. 17: "all 78 core first-vintage dates". |
| Figure 9 title shortened | p. 14 | yes | "A3 P&L by industry, test" now fits. |

### Ten further numbers (none traced in round 1)

| # | Number as printed (page) | Claim ID | Source file :: locator | Value I found | Match |
|---|---|---|---|---|---|
| 1 | 199 / 294 logged calls (p. 9) | A06 | `230ga-follow-the-workers/outputs/{follow_the_workers,follow_the_workers_opus55_xhigh}/outputs/agents/log.jsonl` :: entries with kind != evaluation | 199 / 294 | yes |
| 2 | book first built 09:17:55Z (p. 18) | F09 | `analysis/forward/book_first_build.sha256` :: line 2 | 2026-10-03T09:17:55+00:00 | matches the cited file, **but** that file was created in the fix commit `dd9a851` (2026-10-03T03:36:55-07:00) and `gate3.md` was regenerated from it, so the claim verifies against a file the editor wrote. The independent evidence is commit `9f4a50f` (2026-10-03T02:18:29-07:00 = 09:18:29Z), which contains `book_2026Q4.csv` with the same SHA-256 (`857275...`) as today's file. Cite the commit. |
| 3 | horizon-matched placebo p = 0.06 test, 0.04 full (p. 8) | V09 | `analysis/output/tables/v2d_placebo_12m.csv` :: placebo_p_12m | 0.06316 / 0.03620 | yes |
| 4 | research Sharpes -0.44 / -0.54 / -0.55 / -0.13 / -0.18 over 88 months (Table 4) | C09 | `.../follow_the_workers/outputs/research_summary.json` :: strategies.*.sharpe, .n | -0.4409 / -0.5406 / -0.5481 / -0.1321 / -0.1813; n = 88 | yes |
| 5 | Opus A4 IC -0.002 (t -0.10), alpha t 0.05, last-18-month Sharpe -1.41 (p. 17) | X02 | `.../follow_the_workers_opus55_xhigh/outputs/sealed/initial/results.json` | -0.002477 / -0.1034 / 0.0524 / -1.4101 | yes |
| 6 | sealed returns reproduced to 10^-16 (Table 7, P6) | S04 | `analysis/output/validation.md` :: table rows "13 group returns vs 50 saved ledgers", "Sealed A0 net" | 1.51e-16; 9.97e-17 | yes |
| 7 | V2d test volatility "about 9%" (p. 18 power line) | V04 | `analysis/output/tables/v2_window_stats.csv` :: vol, V2d, test | 0.08733 | yes |
| 8 | "28 of 36 judge outputs broke the JSON-only rule" (Table 7, P3) | none (frozen report.md 3d) | `.../follow_the_workers/report/report.md` l. 129 | "Only 8 of 36 claim-uptake judgments passed the JSON-only output rule; the other 28 are undefined" | yes |
| 9 | A1-T -4.9% / 8.2% / -36.3% (Table 4) | C23 | `.../sealed/initial/results.json` :: variants.ASOF.A1-T | -4.878% / 8.225% / -36.32% | yes |
| 10 | hires alone +0.19, quits alone +0.16 (p. 8) | R1a | `analysis/output/tables/v3_r1_components.csv` :: sharpe, test | 0.18928 / 0.16038 | yes |
| 11 | break-even 68 bp; +0.22 at 25 bp; +0.09 at 50 (p. 8) | R5a | `analysis/output/tables/v3_r5_costs.csv` :: test | 68.30 / 0.21750 / 0.09172 | yes |
| 12 | V2d book long finance, real estate, accommodation; short mining, durable mfg, retail (p. 18) | F02 | `analysis/forward/book_2026Q4.csv` :: v2d_weight | +1/3 on groups 9, 10, 13; -1/3 on 1, 3, 6 | yes |
| 13 | placebo shifts "from 24 months up" (keybox, p. 4) | none | results.json :: placebo.shifts | shifts 24 to 118 (95 shifts) | yes |

All thirteen match their files. Items 2 and 8 are correct in value but item 2's cited source is not independent (see above).

---

## 3. Page budget (pdftotext -bbox-layout; text block y = 62 to about 790 pt)

| Item | Limit | Measured | Verdict |
|---|---|---|---|
| Executive summary | 1 paragraph, <= 230 words | 224 words (LaTeX tokens, math as one word); 234 splitting the PDF text; Claude sentence still TODO | OK now; the pending sentence must be <= 6 words or ~10 words must be cut elsewhere |
| Section 2 | <= 5 pages | printed p. 1 y = 322 to p. 6 y = 282: 0.64 + 4 + 0.30 = about 4.94 pages | OK, with 0.06 page to spare; about 0.3 page of that is blank space at the bottom of printed p. 2 (Table 1 ends at y = 553, Section 2.2 and Table 2 pushed to p. 3) |
| Section 3 | <= 4 pages | p. 6 y = 282 to p. 10 y = 252 (References heading): 0.69 + 3 + 0.26 = about 3.95 pages | OK by about four lines; five critique cells and the Reflection rewrite are still to come and will push it over unless Table 7 is tightened |
| Main body through references | <= 10 pages | printed pp. 1-10; references end on p. 10 at y = 564 | OK |
| Appendices | - | pp. 11-18 | - |

Round-1 comparison: Section 2 grew from 4.5 to 4.94 pages (definitions in the keybox and text, Ledoit-Wolf citation, wider Figure 2), Section 3 shrank from 4.1 to 3.95 (holdings moved to Appendix G). Net, the budget is tighter than before, not looser.

---

## 4. What remains, and what the fixes introduced

### Still reads post-hoc-as-confirmatory
- p. 1: "Read across horizons, the data are consistent with a slower, opposite effect: ... as investment-based asset pricing predicts." Much better; the trailing "as ... predicts" still lends theory's authority to a pattern found after the test was opened. Acceptable if kept, but "which investment-based asset pricing would predict" is the honest tense.
- p. 6, Section 3.2: "the 12-month hiring book is the only one positive in every window" remains a selling sentence for a book chosen after the fact.
- p. 8, "How robust is V2d?": four "not carried by" clauses before the one failed condition. Lead with the failure.
- p. 8 / Figure 11 caption: the tightness-regime pattern ("it earned its return when tightness was falling or V/U > 1") is now referenced from l. 295 without the round-1 disclaimer "recorded without a claim"; the caption narrates a conditional pattern on 54-88 months as fact.
- p. 9, heading "Agents: a stronger model followed the protocol, not the market": an aphorism in place of a finding.

### Remaining jargon without definition
- "block-bootstrap 90% interval" (p. 8): block length and draws not stated (file: 12-month blocks, 5000 draws).
- "pooled correlation of 0.998" (p. 2): pooled over what (groups x months).
- "medium effort" / "extra-high effort" (p. 9): vendor settings; one clause ("a setting that controls how long the model reasons before answering").
- "migration reports" (p. 4): defined only inside Figure 3.
- "winsorised at +-3", "z-scored" (p. 3): standard for the audience, but the brief's reader may not be the audience.
- "12 Newey-West lags for the overlap" (p. 7): fine for a quant, one clause for a professor ("because twelve-month returns overlap").

### New problems introduced by the fixes
1. **A sentence is commented out of the PDF.** `main.tex` l. 250 places `% src: claim R11a (breadth per year)` mid-line; LaTeX discards everything after `%` on that line, so "In the test, A3's IC of -0.021 and TC of 0.80 imply -0.21 against a realised -0.58; V2a's IC of +0.049 implies +0.56 against a realised +0.16; V2d's 12-month IC of +0.096 with a TC of 0.48 implies +0.17 against a realised +0.29." no longer appears (printed p. 6-7 jumps from "near 0.10 sqrt(13) ~ 0.35." to "A modest Sharpe ratio is the ceiling"). The next clause, "cost the monthly books most of what their IC allowed", is now an assertion without its numbers, and claim R11a is effectively orphaned.
2. **A human TODO silently disappeared.** l. 307 puts `\todo{Alex: exact name and vendor of the engineering assistant ... "6 astra" ...}` after `% src: claim A06`, so it is commented out. The PDF renders 12 TODO marks; the source has 13. Nobody reading the PDF will see that item.
3. **Orphaned token.** The P1 prompt box breaks across printed pp. 4-5 and leaves the single word "code]" at the top of p. 5.
4. **Blank third of a page.** Printed p. 2 ends at y = 553 after Table 1; Section 2.2 and Table 2 (both `[H]`) start a new page. Section 2's 4.94-page measure includes this whitespace.
5. **After-the-fact source for F09.** `analysis/forward/book_first_build.sha256` was written in the fix commit and `gate3.md` regenerated from it, so the register "verifies" the 09:17:55Z time against a file created to hold it. Commit `9f4a50f` (09:18:29Z) with a byte-identical book is the independent evidence and should be the cited source, with a note that the gate file was regenerated.
6. **Disclaimer dropped.** The round-1 sentence "One pattern is recorded without a claim" (tightness regimes) was replaced by a bare cross-reference to Figure 11 (l. 295); see the first list above.
7. **Budget headroom consumed.** Section 2 at 4.94 pages and Section 3 at 3.95 pages leave no room for the human additions that are still owed; Table 7 is already the tallest object in Section 3.

---

## 5. Top 5 remaining fixes

1. **(editor) Restore the two lines LaTeX is discarding.** l. 250: move `% src: claim R11a` to the end of the line so the fundamental-law comparison sentence returns to the PDF. l. 307: put the `\todo{...}` before the `% src: claim A06` comment. Then rebuild and confirm 13 TODO marks in the PDF and that "TC of 0.80" appears in `pdftotext` output. Add a one-line check to the build (`grep -c` on the PDF text) so a mid-line `%` cannot drop text again.
2. **(human) Write the owed text within the budget.** Five "Our critique" cells (Alex x2, Elouan, Al Yazid, Romain, Piero; each <= 25 words or Section 3 exceeds 4 pages), the Reflection in the team's words (l. 336, remove `\prov{draft}`), and the executive-summary Claude sentence (l. 24, <= 6 words of slack at 224 words; otherwise cut ~10 words elsewhere in the paragraph).
3. **(editor) Cite independent evidence for the first build.** In Appendix G (l. 470) and claim F09, cite commit `9f4a50f` (2026-10-03T09:18:29Z, book SHA-256 `857275...`) as the bound on the first build, and say that `book_first_build.sha256` and `gate3.md` were written or regenerated afterwards from the first run's record. Same hygiene for the regenerated `gate3.md` row "Forward spec frozen before the book was built".
4. **(editor) Recover layout slack.** Make the prompt boxes unbreakable (or `\needspace{6\baselineskip}` before each) so "code]" is not orphaned; let Table 2 float (`[t]`) or move Figure 2 after the Sample paragraph so the blank third of printed p. 2 is reused. This buys Section 2 roughly 0.3 page and removes two visible defects.
5. **(editor) Final wording pass on Section 3.** Reinstate a one-clause disclaimer on the tightness pattern (l. 295: "recorded, not claimed, on 54-88 months per cell"); re-order "How robust is V2d?" to lead with the failed condition; define the bootstrap (12-month blocks, 5000 draws), "pooled correlation" and model "effort"; replace the heading at l. 331 with a plain one ("Opus against Sonnet"); change "as investment-based asset pricing predicts" (l. 21) to "which investment-based asset pricing would predict".

Human items still open and unchanged from round 1, by design: P1 disposition counts (l. 348, Alex), data-link access dates (l. 362, Elouan), freeze-hash confirmation against `FREEZE.json` / `evaluation_started.json` (l. 159, Alex), weekly tracker (l. 471, Elouan). Build the submission with `\draftfalse` and re-run the page measurements after the critiques are in.
