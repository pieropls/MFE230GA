# Independent review of report v1: two rounds (3–4 Oct 2026)

Reviewer: a fresh Claude subagent that had not seen the project, given `FinalProject.pdf`, `report/main.pdf`, `report/main.tex` and `results/claims.csv`, with read-only access to the rest. Full write-ups: `report/REVIEW_round1.md`, `report/REVIEW_round2.md`. Rubric: Thesis 40, Execution 40, Originality 20.

## Scores

| | Thesis | Execution | Originality | Total |
|---|---|---|---|---|
| Round 1 (commit `ad1dec3`) | 32 | 30 | 17 | 79 |
| Round 2 (commit `dd9a851`) | 33 | 31 | 17 | 81 |
| Reviewer's estimate once the human items are written | | | | 87–89 |

The reviewer's reading of the deductions: the thesis as traded (demand news at one month) is not the thesis the report ends up believing (cost news at a year), and the 13-group universe is introduced as a limit rather than a design constraint; under Execution, the rubric's explicit "critically evaluate the AI" item is still TODO in six places (critique cells and the Reflection).

## Numbers traced
Round 1: 32 numbers; 30 matched their source file at the printed precision; 2 did not (607/905 calls not in any file; the book build time 09:17:55Z not in any file at the time). Round 2: 13 further numbers; all matched.

## Fixes applied by the editor (Claude) between and after the rounds
- Call counts replaced by the log counts (199 Sonnet, 294 Opus; claim A06); CLAUDE.md's 607/905 flagged in `MORNING_BRIEF.md`.
- "6 of 6" Opus features corrected to "6 of 7"; "failed the test" defined as the frozen sealed criterion (t ≥ 1.5 and positive IC in both halves); claim C19 rewritten.
- The Q4 book's first build (09:17:55Z) recorded in `analysis/forward/book_first_build.sha256` and enforced by the notebook; commit `9f4a50f` cited as the independent evidence; `gate3.md` shows the first-build time again.
- Horizon-matched placebo for V2d (claim V09) added next to the pre-declared one-month placebo; Table 6 caption states the one-month statistics and 6 Newey–West lags; the 12-lag alpha is labelled.
- Figure 1 box overlap fixed; Figure 9 title shortened; A1-T numbers registered (claim C23) and the `\prov` marks removed; "78 series" and the "28 undefined judge labels" cited to the frozen report.
- Executive summary rebalanced: IC defined, the sign statement tightened (layoffs and hours), the 12-month reversal framed as "consistent with ... would predict", "paper books ... no capital"; 225 words by LaTeX token count.
- Post-hoc framing: "Four post-hoc explanations"; "Of the four, V2d is the one whose sign tests the cost channel; it was not the declared headline (V2a was)"; Figure 4 caption "Post-hoc horizon profile"; "How robust is V2d?" now leads with the failed condition; the tightness pattern is "recorded without a claim"; heading "Agents: Opus against Sonnet".
- Jargon defined at first use: Newey–West/HAC, circular-shift placebo, Holm correction, DSR and "looks", blocked cross-validation, tranche, regime gate, ALFRED, block bootstrap (12-month blocks, 5,000 draws), "effort"; Ledoit–Wolf (2004) cited.
- Appendix fixes: `.md` → `.json`, "lost 1.41" → Sharpe, unit of "+0.27", book holdings and the power line moved to Appendix G.
- Layout: Section 3 starts on a fresh page; Tables 2 and 5 float; the P1 prompt box is unbreakable.
- Regression caught in round 2 and fixed: two `% src:` comments placed mid-line had swallowed a sentence (the fundamental-law comparison) and one TODO. `report/check_sources.py` now fails the build step if a `% src:` comment is followed by LaTeX on the same line.

## Fixes left (need a human)
- Five "Our critique" cells in Table 7 (P1 Alex, P2 Elouan, P3 Al Yazid, P4 Romain, P5 Piero, P6 Alex), at most ~25 words each so Section 3 stays within four pages.
- The Reflection paragraph in the team's words (Al Yazid); remove `\prov{draft}`.
- One sentence on Claude in the executive summary (Al Yazid); the summary has about 5 words of slack, so cut elsewhere if needed.
- Alex: name and vendor of the engineering assistant ("6 astra"); confirm the freeze hashes and the single opening against `FREEZE.json` and `evaluation_started.json`; P1 disposition counts; check where CLAUDE.md's 607/905 call counts came from.
- Elouan: verify every `refs.bib` entry (including the added Ledoit–Wolf 2004); data-link access dates; weekly tracker if wanted.
- Romain: final prose pass; the reviewer still flags a few aphoristic sentences.
- Build the submission with `\draftfalse` and re-measure the page budget after the critiques are in.
