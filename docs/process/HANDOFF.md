# Handoff (final pass, 3 Oct 2026)

Written for the team by Claude Code (Fable 5.1) at the end of `FINAL_PROMPT.md`. Supersedes the TODO table in `MORNING_BRIEF.md`.

## Repository

No GitHub URL was supplied, so nothing has been pushed. The local repository is at commit `HEAD` of `main` with the frozen study as a submodule. To publish, from the project root:

```bash
git remote add origin <GITHUB_URL>
git push -u origin main
# then verify from a clean directory:
git clone --recurse-submodules <GITHUB_URL> ftw && cd ftw
jupyter nbconvert --to notebook --execute --inplace analysis/run.ipynb   # ~35 s, must not write analysis/output/STOP.md
python3 -B results/build_results_book.py                                # 106 claims, 0 unverified
cd report && python3 -B check_sources.py && latexmk -pdf main.tex
```

Whoever clones needs read access to Alex's private repository `Aroesler1/230ga-follow-the-workers` (the submodule, pinned to `c67c486`). A local fresh-clone check passed end to end: `clone_check.md`.

Deliverables: `report/main.pdf` (21 pages, draft marks on), `results/results_book.pdf`, `results/VERDICT.md`, `README.md`.

## What changed in this pass (stages 1 to 5, one commit each)

1. **Layout.** `docs/` holds the diagnosis (`FINDINGS_AND_PROPOSAL.md`), the blueprint, the course sheet, `img/`, `team_inputs/` and `process/` (prompts, brief, review rounds, code review, open issues, this file). Every moved path was repointed (claims register, `% src` comments, notebook, scripts, CLAUDE.md). `requirements.txt` added; `build.log`, caches and dead code removed.
2. **Code review** (`CODE_REVIEW.md`). One MAJOR finding: the fixed-lag rule assumes the normal BLS calendar, which the Oct–Nov 2025 shutdown broke, so two post-hoc earning months use data released after the decision. Not corrected (it would change v2/v3 numbers after the run logs were frozen); disclosed in `data_vintage.md`, report §2.2 and `OPEN_ISSUES.md` #3. Result-neutral fixes applied: Results Book call counts 199/294, slice-vs-cold-start note, unused helpers removed, `code_hashes.md` and `environment.txt` added.
3. **Report.** Al's Claude section integrated (Table 8, judge paragraph, Reflection, Appendix A, summary sentence); V2d provenance stated; v2 test columns labelled post hoc; power line extended; six new claims (A07–A10, V13, V14), 106 verified. Summary 230 printed words; main body 10 pages; §3 about 4.4 pages (the Claude table is half a page; the window figure and table moved to Appendix D). 9 `\todo` marks remain (below).
4. **README** front page, `analysis/README.md`, `results/README.md`.
5. **Submodule** pinned at `c67c486`; fingerprint re-checked (`eb109be9…`, 3,067 files); fresh-clone check recorded.

No result changed at any stage: every v2/v3 table and the Q4 book are byte-identical to their first runs (checked by the notebook on every run), the sealed result stands, and the fingerprint is unchanged.

## Corrections to Al's section

Every number in `docs/team_inputs/al_claude_section.md` checked out against the frozen files (25 P1 findings with 5 unsupported and 1 metadata fix; 584 shared rows; 98 of 108; 199 calls; 11 of 18 reports, 10 over 120 words; 10 of 17, 3 human yes, 7 judge-only yes; 28 of 36; 6 of 10 and 4 rejected; 3 of 142; −1.71; 25 + 25 + 10 human checks; 14 grammar operations; amendments 001–002). Edits made in the report, not corrections:

- The reason for using Claude is now "this term's course allows it; the switch from the ChatGPT template is logged as amendments 001–002", everywhere. Al's "no OpenAI API key was available" was dropped (3b of the prompt).
- Table cells were condensed to 20 words or fewer; Al's P2 critique line was shortened and its recommendation (keep regime splits out of agent feedback, or require a minimum share of active months) moved to Appendix A.
- The post-mortem row names the model (Opus 5.5) and points to `docs/FINDINGS_AND_PROPOSAL.md`.
- The blinding audit is cited from `agents/blinding_audit.json` (108 candidate calls, 18 migration calls, 1 syntax repair, total 199).

## Remaining `\todo` marks in `report/main.tex` (line numbers at this commit)

| Owner | Item | Line |
|---|---|---|
| Alex | Confirm the freeze hashes and the single opening against `FREEZE.json` / `evaluation_started.json` | 159 |
| Alex | Exact name and vendor of the engineering assistant that wrote the pipeline code ("6 astra"); not documented in the repository, do not guess | 310 |
| Alex | Critique cells for P1 and P6 in Table 8 | 331, 349 |
| Elouan | Critique cell for P3 (judge) | 339 |
| Romain | Critique cell for P4 (red team); final prose pass on the whole report | 343 |
| Piero | Critique cell for P5 (post-mortem) | 347 |
| Elouan | Check every data link and add access dates; verify every `refs.bib` entry | 413 |
| Elouan | Weekly forward-test tracker, if the team wants one (deferred) | 544 |

Al's P2 critique is in (Table 8, row P2). Build with `\draftfalse` (`preamble.tex`) for the submission so no red TODO text remains; `check_sources.py` must still pass.

## Open issues

`OPEN_ISSUES.md` has eight entries. The ones that need a decision:

- **#3 shutdown exception** (Piero, next iteration): apply the ALFRED availability rule or carry Aug/Sep 2025 forward, then re-freeze a new run log; expect marginal changes to v2/v3 numbers.
- **§3 length**: about 4.4 pages against the 4-page target in CLAUDE.md; the Claude table alone is half a page. Romain can decide whether Table 6 (v2 results) or the robustness table goes to Appendix D.
- **Course compliance**: the brief asks for ChatGPT; every AI role used Claude. The report states this once with the amendment reference; confirm with the instructors if needed.

## Answer to Al's V2d question

V2d was not read off the test. Its sign is the one the investment channel predicts (Belo, Lin and Bazdresch 2014): firms that hire and lose workers fastest earn lower returns later. Its 12-month horizon, though, was chosen from a horizon profile that included the test period, so the horizon is fitted on the test and the book is post hoc through and through. On the research years alone the 12-month IC is +0.047 (t 0.90) with a horizon-matched placebo p of 0.26 (claim V13): a researcher with only the research sample would not have selected it. That is why the report calls H2 "consistent with the data, not established", keeps V2d under the post-hoc label, and lets the forward test speak.

## Overleaf

Upload `report/` (`main.tex`, `preamble.tex`, `refs.bib`, `figures/`, `tables/`, `code/`). Compiler pdfLaTeX, main document `main.tex`; the bibliography runs automatically (natbib, plainnat). Locally: `cd report && latexmk -pdf main.tex`. The Results Book builds the same way from `results/results_book.tex` (it `\input`s `../report/preamble`). Regenerate numbers, tables and figures with `analysis/run.ipynb`; it stops with `analysis/output/STOP.md` if any gate fails.
