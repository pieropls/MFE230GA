# Iteration prompt: "Follow the Workers" v2 and report v1

---

## 0. How to run this (Piero)

- **Where:** open Claude Code in `project/`, so it reads `docs/process/project_rules.md` automatically.
- **Baseline first:** in `project/`, run `git init && git add -A && git commit -m baseline`. Every part can then be rolled back.
- **Two sessions.** Claude Code cannot change its own model, so the work is split.

| Session | Parts | Model | Effort | Paste this to start |
|---|---|---|---|---|
| A | 1–3 (code, numbers, figures, v2) | Opus 5.5 | high | `Read docs/process/project_rules.md and ITERATION_PROMPT.md. Execute Parts 1, 2 and 3 end to end without asking me questions. Commit after each part. Stop only if a gate fails (write analysis/output/STOP.md).` |
| B (new session) | 4–5 (report v1, review, handoff) | Fable 5.1 if available, else Opus 5.5 | high (Opus: xhigh) | `Read docs/process/project_rules.md and ITERATION_PROMPT.md. Parts 1–3 are done. Execute Parts 4 and 5 end to end without asking me questions. Commit when done.` |

- **Effort:** don't use max. It is slow and burns limits for no gain. Haiku and Sonnet are not needed, because nothing here reruns the agents.
- **Timing:** expect about 3h for session A and 2–3h for session B. Between sessions, open `analysis/output/v2_results.md` and the figures in `report/figures/` for 5 minutes.
- **If something breaks:** read `analysis/output/STOP.md`, then fix it or skip that item. Never tell it to push through a failed gate.

---

## 1. Context (for Claude)

**The study.** We test whether public labor-market flows predict which of 13 U.S. industry groups outperform over 1–3 months, and whether labor-market tightness changes the answer.
- Data: JOLTS openings, hires, quits and layoffs; CES hours and earnings; and V/U tightness.
- Alex built a preregistered pipeline (`230ga-follow-the-workers/`):
  - research period May 2004–Sep 2014, test period Nov 2014–Aug 2026 (142 months), opened once;
  - strategies A0–A4, with blinded LLM agents proposing features for A3 and A4.
- **Result:** the primary, A3 (Sonnet study), has a test Sharpe of −0.58 and the verdict is "Do not implement". That stays the confirmatory result. The Opus study was launched after the test was opened, so it is exploratory and counts as evidence about AI agents.

**Why it failed** (`FINDINGS_AND_PROPOSAL.md`, `analysis/output/diagnostics.md`):
- The A0 signs for layoffs and hours are contradicted by the data.
- Wage growth W was dropped during the build. It was part of F6 in the blueprint, and it is the only stable signal: rank IC +0.039 in research and +0.041 in test.
- Hiring predicts returns with the q-theory (Belo–Lin–Bazdresch) negative sign at 12 months, not at 1 month.
- The expanding tightness terciles put 132 of 141 test months in one bin.
- The A3 agent features were regime-gated and active in only 3 of 142 test months.
- Ridge chose α=1000, the edge of the grid.
- The gross-exposure cap bound in 80–93% of months.
- Losses were concentrated in health care, construction and finance.

**Goal of this iteration:** the best *honest* result, plus a beautiful report v1 that Romain takes over in the morning.
- "Better results" means a small set of v2 strategies fixed now from economics and the diagnostics, run once and all reported.
- It also means a live forward test, and a report that explains the thesis, the failure and what survives.
- It never means searching until the test looks good.

---

## Part 1: Rebuild the analysis core (session A)

1. Build `analysis/` in the layout from `docs/process/project_rules.md`: `params.py`, `data.py`, `stats.py`, `plots.py` and `run.ipynb` in the notebook format given there.
   - Reuse `french.py`, `signals.py` and `diagnostics.py`.
   - Keep it small and flat.
2. **Data vintage.** Use the best of these that is available, and record which one in `analysis/output/data_vintage.md`:
   - (a) as-known (ASOF) panels saved inside the frozen repo;
   - (b) ALFRED vintages, if `analysis/.env` contains `FRED_API_KEY`;
   - (c) revised FRED data with fixed publication lags (JOLTS d−2, CES d−1). This is what `analysis/data/` holds now. In the frozen study, revised data with fixed lags gave the same A3 test IC as the as-known data (−0.021).
3. **Backtest.** It must equal the frozen study's portfolio construction. Locate the backtest in `230ga-follow-the-workers/outputs/follow_the_workers/` and import it read-only rather than rewriting it if you can.
   - 3-month tranches.
   - Beta hedge using 60-month betas.
   - 10% volatility target using a 60-month covariance matrix (minimum 36 months).
   - Gross exposure capped at 2.
   - Costs of 10 bp, plus 2 bp on the hedge.
4. **GATE 1.**
   - Using the study's own A0 scores or weights, reproduce the sealed A0 net monthly returns in `outputs/follow_the_workers/outputs/sealed/initial/` to within 1e-6.
   - Confirm that the 13 group returns still match the saved ledgers.
   - Write the result to `analysis/output/validation.md`.
5. Write the score-to-weight mapping as a LaTeX equation in `report/tables/portfolio_equation.tex`.

## Part 2: Diagnostics, tables and figures (session A)

Every item below gets a CSV in `analysis/output/tables/`. Items marked "fig" also get a figure. Each table also gets a booktabs `tabular` fragment in `report/tables/`, with no float wrapper, so `main.tex` can `\input` it. Everything is POST-HOC unless marked CONFIRMATORY.

| ID | Content | Figure |
|---|---|---|
| D1 | Single-signal rank IC (F1–F5, W, A0, industry momentum 12-1) for research, test and the full sample, with Newey–West t | `fig_ic_signals.pdf`: dot plot, research vs test, ±2 s.e. |
| D2 | IC by horizon h = 1, 3, 6, 12 for each signal | `fig_horizon.pdf`: annotated heatmap |
| D3 | Tightness T path with research/test shading and the V/U = 1 line; IC per signal in T-rising vs T-falling (12-month) months | `fig_timeline.pdf`, `fig_tightness.pdf` |
| D4 | CONFIRMATORY: cumulative net returns of A0, A1, A3 and A4 from the saved ledgers, plus industry momentum 12-1 through the same backtest | `fig_cumulative.pdf` (v2 is added in Part 3) |
| D5 | P&L by industry for A3 | `fig_industry_pnl.pdf` |
| D6 | CONFIRMATORY: factor loadings (FF5, momentum and group momentum, with NW t) for A0, A1 and A3 from `results.json` → `attribution` | `fig_loadings.pdf`: coefficient plot |
| D7 | Agent features: research IC vs test IC for every candidate in both studies, marking selected and regime-gated ones | `fig_agents_scatter.pdf` |
| D8 | CONFIRMATORY: A3 course windows (full test, halves, ex-pandemic, last 18 months) from `results.json` → `windows` | — |
| D9 | Risk overlay: months with the cap binding, ex-ante vs realised volatility | — |
| D10 | Agent-experiment design diagram: 2 arms × 3 agents × 3 repetitions, migration reports, mechanical selection, LLM judge with human audit | `fig_agents.pdf` |

Open every figure as an image. Check that it is readable at its print width, has no overlaps and follows the style in `docs/process/project_rules.md`. Fix anything that fails. Write `analysis/output/diagnostics_v2.md`, listing every number and the file it came from.

## Part 3: The v2 iteration (session A)

**Step A: freeze before computing.**
1. Write `analysis/v2_spec.md` with exactly the variants below and every reported statistic.
2. Write its SHA-256 and a UTC timestamp to `analysis/v2_spec.sha256`.
3. Commit.

All variants use the frozen study's portfolio construction and costs. The same windows apply to every variant: research, test, full sample, post-2010 and the last 18 months.

| Variant | Score | Why (decided now, from economics and the diagnostics) |
|---|---|---|
| **V2a (headline)** | Cross-sectional rank of W | Restores the wage signal the blueprint preregistered and the build dropped |
| V2b | Equal-weight composite of z(F1…F5, W), each signed by its **research-period** IC (2004-05 to 2014-09, computed inside the script) | Signs learned only from research data, not imposed |
| V2c | Equal-rank composite of W and industry momentum 12-1 | Is the labor signal additive to price momentum? |
| V2d | −(z(F2)+z(F3))/2, held 12 months (12 tranches) | Thesis test of the long-horizon investment channel |

**Reported statistics for every variant:**
- Sharpe, net return, volatility, max drawdown, hit rate, IC with t;
- factor alpha with t (FF5, momentum and group momentum);
- costs at 0, 10 and 25 bp;
- turnover;
- circular-shift placebo p-value;
- deflated Sharpe with N_trials = 112 (about 108 looks already taken in the diagnostics, plus these 4);
- P&L by industry.

**Step B: run once.** Write `analysis/output/v2_results.md` and `report/tables/v2_results.tex`.
- Report every variant whatever it shows. No edits after results.
- For reference only, so you don't tune towards it: a rough check on 3 Oct (no hedge, no vol target) gave V2a Sharpe ≈ +0.36 research, +0.23 test, +0.28 full, negative over the last 18 months.
- Add V2a to `fig_cumulative.pdf` (dashed, post-hoc colour) and to `fig_loadings.pdf`.
- Add `fig_v2_windows.pdf`: Sharpe by window for V2a–V2d, with the A3 confirmatory bar for contrast.

**Step C: forward test.** Write `analysis/forward/spec_frozen.md` (V2a headline, V2b secondary), hash it and timestamp it. Note that the 1–2 Oct 2026 returns already existed when it was frozen.
- Build the **Q4 2026 book**: decision 30 Sep 2026, using only data published by then (JOLTS through July 2026, CES through August 2026).
- Write `analysis/forward/book_2026Q4.csv` (group, V2a weight, V2b weight).
- Write `analysis/forward/etf_proxies.csv`: one liquid sector ETF per group, with a caveat column.
- Write `analysis/forward/tracker.csv`: weekly rows for Elouan to fill in.

**GATE 3:** the spec timestamp is earlier than the results file, and every book's weights net to zero.

## Part 4: Report v1 (session B)

Turn `report/main.tex` into a complete, beautifully presented first draft. The skeleton already has the title page with all five names, the course template, the colour labels and macros, a thesis diagram, and the verified sealed numbers. Keep its look.

**Section by section:**
1. **Executive summary.** One paragraph, at most 230 words, in this order: the strategy, then "Do not implement" and why, then what survives (V2a, honestly sized and labelled post-hoc), then the forward test, then one line on what Claude did well and badly.
2. **What we tried** (at most 5 pages).
   - 2a, Idea: the thesis and its two channels, with tightness as moderator, the literature, and Table 1.
   - 2b, Data: Table 2, the universe and its mapping caveat, the point-in-time handling, and `fig_timeline`.
   - 2c, Implementation:
     - equations for signals, ridge and portfolio (`\input{tables/portfolio_equation}`);
     - the models table;
     - the "How we kept the test honest" box;
     - the agent experiment with `fig_agents`;
     - **at least 3 Claude prompt boxes**, each a short exact excerpt: P1 source and code review (`outputs/p1_request.json`), P2 the signal-search agent prompt (template in `params.py`, calls in `outputs/agents/log.jsonl`), and P4 the robustness red team (`outputs/p4_request.json`). These paths are relative to `230ga-follow-the-workers/outputs/follow_the_workers/`.
3. **What we learned** (at most 4 pages).
   - 3a: exposures with `fig_loadings`. The labor book is partly a quality/growth tilt; say why that is plausible.
   - 3b: time patterns. One table covering A3 (confirmatory) and V2a (post-hoc) over the full sample, post-2010 and the last 18 months, plus `fig_cumulative`. Explain that A3's test starts in Nov 2014, so for A3 "post-2010" is the whole test.
   - 3c: robustness and limits, in this order:
     - why it failed: wrong signs (`fig_ic_signals`), wrong horizon (`fig_horizon`), untestable moderator (`fig_tightness`), fragile agent features (`fig_agents_scatter`), concentrated losses (`fig_industry_pnl`), and over-shrinkage plus the binding cap;
     - **what survives**: `v2_results` and `fig_v2_windows`, stated plainly as modest, not significant after deflation, and negative recently if that is what the results show;
     - the forward test and Q4 2026 book;
     - limits: power of about 0.6 Sharpe, and mapping dilution.
   - 3d: **Claude evaluation.**
     - A table with one row per interaction: role, what we asked, what it got right, what it got wrong, what we changed, and our critique.
     - Rows: P1–P4 from the build (summaries and "what was wrong" are in `230ga-follow-the-workers/outputs/follow_the_workers/report/chatgpt_log.md`; the Opus study has its own copy), P5 the post-mortem review (`FINDINGS_AND_PROPOSAL.md`), and P6 this iteration.
     - Leave the critique cells as `\todo{critique: <name>}`, spread over the five members.
     - Then the agent experiment: capability is not alpha (Opus vs Sonnet compliance vs out-of-sample results); the judge vs human audit (10/17, with all 7 disagreements machine-yes); communication effects within the seed spread.
     - End with a reflection on strengths and limits, drafted and marked `\prov`.
4. **Appendices:**
   - interaction transcripts (condensed, with file links);
   - data links;
   - industry mapping;
   - full results (vintage variants, cost sensitivity, gate table);
   - code snippets of 15–25 lines each (as-of lookup, signal construction, backtest core);
   - the Opus follow-up (exploratory; its +0.01 Sharpe comes from being long durable manufacturing, i.e. semiconductors);
   - the forward-test specification with its hash.

**Rules:**
- Every figure gets a caption that states the finding in one sentence, plus its label tag.
- Every number gets a `% src`. Remove `\prov` only once a number is verified. Keep `\todo` only where a human is needed.
- Follow the writing style in `docs/process/project_rules.md` strictly, especially "must not read as AI-written".

**Build and look:**
- `latexmk -pdf`, with zero errors, zero undefined references and no overfull box above 5pt.
- Render every page to PNG and inspect it.
- Fix float placement, tables running past the margins, widows, and figures that are too small to read.
- The main body must be at most 10 pages.

## Part 5: Self-review and handoff (session B)

1. Act as the grader, using the rubric in `FinalProject.pdf` (Thesis 40, Execution 40, Originality 20).
   - Trace 15 random numbers to their `% src` files and fix any mismatch.
   - Check that nothing post-hoc reads as confirmatory and that "Do not implement" is clear and justified.
   - Score the report and apply every fix that needs no human input. Rebuild and inspect the pages again.
2. Write `report/REVIEW.md`: scores, fixes applied, and fixes left.
3. Write `report/HANDOFF_ROMAIN.md`:
   - what is done;
   - every remaining `\todo`, with an owner suggestion: critiques go to all five members; citations, the literature paragraph and the forward tracker go to Elouan; the Claude evaluation table and the judge-disagreement review go to Al Yazid; number checks against the ledgers and the integrity box go to Alex;
   - open risks;
   - how to build, including an Overleaf note: upload the `report/` folder and compile with pdfLaTeX.
4. Commit.
