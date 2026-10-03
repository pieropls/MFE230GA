# Morning brief, Sat 4 Oct 2026

> Superseded on 3 Oct 2026 (evening) by `docs/process/HANDOFF.md`: TODO table, line numbers, open issues and push instructions live there now.

Deliverables: `results/results_book.pdf` (27 pp.), `results/VERDICT.md`, `report/main.pdf` (19 pp., draft marks on), `docs/process/REVIEW.md`. Everything is committed; the frozen repo is untouched (3,067 files, fingerprint unchanged).

## Verdict in three lines
1. The preregistered strategy fails: A3 test Sharpe −0.58, IC t −1.08, placebo p 0.72, gates G2–G5 failed. **Do not implement** stands. [CONF]
2. Labor flows carry industry information as slow cost news, not fast demand news: the hiring/quits score has no one-month IC and a positive IC from 9 to 24 months (12-month IC +0.096, t 2.43); the 12-month book V2d is positive in every window (+0.29 test) but fails one pre-declared check (first test half −0.21), its test bootstrap interval includes zero and its DSR is 0.05. A hypothesis, not alpha. [POST-HOC]
3. Four paper books (V2a headline, V2b, V2c, V2d) are frozen for Q4 2026 and will be evaluated whatever they show. [FWD]

## Scoreboard (net Sharpe; IC one-month except V2d at 12 months; source `results/scoreboard.csv`)

| Strategy | Label | Research | Test | Full | Last 18m | IC (t) | α/m (t) | Placebo | DSR | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| A3 primary (Sonnet) | CONF | −0.13 | −0.58 | −0.44 | +0.85 | −0.021 (−1.08) | −0.38% (−1.86) | 0.72 | 0.00 | Do not implement |
| A0 / A1 / A1-T / A4 | CONF | −0.44 / −0.54 / −0.55 / −0.18 | −0.36 / −0.51 / −0.59 / −0.79 | | | | | | | negative |
| A4 primary (Opus follow-up) | expl. | −0.40 | +0.01 | −0.13 | −1.41 | −0.002 (−0.10) | +0.01% (+0.05) | 0.56 | 0.00 | exploratory, fails G2–G5 |
| V2a wage growth (headline) | POST-HOC | +0.09 | +0.16 | +0.15 | −1.71 | +0.049 (+2.04) | +0.06% (+0.29) | 0.02 | 0.02 | noise after looks |
| V2b signed composite | POST-HOC | −0.06 | −0.15 | −0.11 | −1.34 | +0.042 (+1.65) | −0.18% (−0.84) | 0.05 | 0.00 | noise after looks |
| V2c wage + momentum | POST-HOC | +0.27 | +0.35 | +0.32 | −0.78 | +0.032 (+1.21) | +0.22% (+1.36) | 0.26 | 0.09 | noise after looks |
| V2d −(hires+quits), 12m | POST-HOC | +0.50 | +0.29 | +0.35 | +0.29 | +0.096 (+2.43) | +0.26% (+1.37) | 0.85 (1m); 0.06 (12m, post-hoc) | 0.06 (112) / 0.05 (132) | fragile in time (R4) |

## What changed overnight
- **Results Book** (`results/`): scoreboard, every figure and table with source, agent experiment, AI inventory, 100-claim register verified by locator (`claims.csv`), known issues. Built by `results/build_results_book.py`.
- **v3 robustness battery for V2d** (`analysis/v3_spec.md`, frozen 09:52Z, run once 09:53Z): R1–R11. Holds on components, horizon, holding period, costs (break-even 68 bp), drop-one (min +0.18), full-sample bootstrap; fails R4 (test halves −0.21 / +0.64). N_trials raised to 132. Gate 2 PASS.
- **VERDICT.md** and the verdict page in the Results Book.
- **Report v1** on the house template: 10-page main body (summary 225 words, §2 ≈ 4.6 pp., §3 ≈ 4.5 pp. after iteration 1), appendices A–G, zero build errors, references resolved. Three review rounds by independent subagents (79, 81, then 80/100 after the presentation iteration; 87–89 estimated once the human items are written); see `docs/process/REVIEW.md`. Round 2 caught a regression I had introduced (two mid-line `% src` comments swallowed a sentence and a TODO); fixed, and `report/check_sources.py` now guards against it.
- **Corrections made on the reviewer's findings:** call counts are 199 (Sonnet) and 294 (Opus) from the logs, not 607/905; "6 of 6" Opus features became "6 of 7" (one research-passing feature passed the sealed criterion but was not selected); the forward book's first-build time (09:17:55Z) is now recorded in `analysis/forward/book_first_build.sha256` and enforced; horizon-matched placebo for V2d added next to the pre-declared one; Figure 1 overlap fixed; A1-T numbers registered (no `\prov`); Codex guess removed from `docs/FINDINGS_AND_PROPOSAL.md`.
- **Incident:** a Gate 1 run failed once because a `__pycache__/*.pyc` file had been written inside the frozen folder (a bytecode cache from the reviewer importing `params.py`). The frozen sources were untouched; the cache was removed and the fingerprint matches the baseline again (`eb109be9…`, 3,067 files).

## Five best figures
`report/figures/fig_horizon_profile.pdf` (the thesis horizon profile), `fig_ic_signals.pdf` (wrong signs, wage growth), `fig_timeline.pdf` (no tight market in research), `fig_v2_windows.pdf` (all four variants by window against A3), `fig_v2d_dropone.pdf` (no single industry carries V2d).

## Remaining `\todo` marks in `report/main.tex`, with owners (line numbers after iteration 1)
| Owner | Item | Line |
|---|---|---|
| Al Yazid | One sentence on Claude in the executive summary; rewrite the Reflection in the team's words and remove `\prov{draft}`; own Table 8 (AI evaluation) and the judge-disagreement review; critique row P3 | 24, 340, 356 |
| Alex | Confirm freeze hashes and the single opening against `FREEZE.json` / `evaluation_started.json`; exact name and vendor of the engineering assistant ("6 astra"); P1 disposition counts; critique rows P1 and P6 | 160, 333, 374, 350, 359 |
| Elouan | References (verify every `refs.bib` entry, incl. Ledoit–Wolf 2004); data-link access dates; weekly tracker if wanted; critique row P2 | 402, 506, 353 |
| Romain | Critique row P4; final prose pass; decide whether Figure 6 or Table 7 moves to the appendix to bring Section 3 under 4 pages (it is about 4.5 after the added figures) | 357 |
| Piero | Critique row P5; decide on the headline-box wording for H2 (round 3 asked for "consistent with the data, not established" instead of "supported"; applied) | 358 |

Build with `\draftfalse` (preamble.tex, line 74) for the submission so no red TODO text or gold `\prov` boxes remain.

## Open risks
- **`CLAUDE.md` says 607 and 905 logged calls; the logs hold 199 and 294** (candidate + migration + judge calls; `agents/responses/` has the same counts). The report uses the log counts. Please check where 607/905 came from before anyone quotes them.
- **Course compliance:** the brief asks for ChatGPT; every AI role used Claude. Confirm with the instructors or document the substitution clearly (the report already states the models from the logs).
- **Post-hoc data:** every v2/v3 number uses revised FRED data with fixed lags; as-known data pick the same top-3 groups in only 42% of months. The as-known rerun (R10) needs a FRED key.
- **V2c's ETF book has four legs** (two positions cancel in XLI); track V2c on French group returns.
- **One quarter of forward test has almost no power**; say so whenever the Q4 result is discussed.
- **Section 3 is about 4.5 pages** (CLAUDE.md allows 4) after iteration 1 put `fig_cumulative`, `fig_v2_windows` and the robustness table in the body; the main body is exactly 10 pages before the critiques are written. Options: move Figure 6 (horizon profile) or Table 7 to Appendix D. The executive summary is 225 printed words with the Claude sentence still to add, so cut elsewhere when it goes in.

## How to build on Overleaf
Upload the `report/` folder (main.tex, preamble.tex, refs.bib, figures/, tables/, code/). Compiler: pdfLaTeX; main document `main.tex`; the bibliography runs automatically (natbib + plainnat). Locally: `cd report && latexmk -pdf main.tex`. The Results Book builds the same way from `results/results_book.tex` (it `\input`s `../report/preamble`). Regenerate numbers, tables and figures with `analysis/run.ipynb` (about 35 s); it stops with `analysis/output/STOP.md` if any gate fails.
