# Final pass: clean repo, final code review, complete report v1, push to GitHub

Read `CLAUDE.md` and this file. Then work through Stages 1–6 in order without asking questions. Commit after every stage.

**Golden rule.** No result may change. If any fix would change a number in `results/claims.csv`, a table or a figure, do not apply it. Write it to `docs/process/OPEN_ISSUES.md` and carry on.

`GITHUB_URL` is given in the kickoff message.

---

## Stage 1: Organise the repository

Target layout. The frozen study keeps its path, because the code references it.

```
README.md                    ← new: the front page (Stage 4)
CLAUDE.md                    ← stays at root (Claude Code rules)
requirements.txt             ← new: loose pins (pandas>=2, numpy, matplotlib, scipy, statsmodels, jupyter …)
.gitignore
230ga-follow-the-workers/    ← Alex's frozen study, as a git SUBMODULE pinned to commit c67c486 (Stage 5)
analysis/                    ← params.py, data.py, stats.py, plots.py, run.ipynb, specs + hashes, forward/, output/, data/
results/                     ← results_book.tex/.pdf, RESULTS_BOOK.md, VERDICT.md, claims.csv, scoreboard.csv, build script
report/                      ← main.tex, preamble.tex, refs.bib, figures/, tables/, code/, check_sources.py, main.pdf
docs/
  FINDINGS_AND_PROPOSAL.md   ← post-mortem of the frozen study
  blueprint.html             ← "230GA - Project.html"
  course/FinalProject.pdf
  img/                       ← PNG exports of key figures for the README
  team_inputs/               ← team_inputs/* (Al's Claude section, and later contributions)
  process/                   ← ITERATION_PROMPT.md, OVERNIGHT_PROMPT.md, FINAL_PROMPT.md, MORNING_BRIEF.md,
                               REVIEW*.md, STOP/amendment history notes, OPEN_ISSUES.md
```

1. Move the files with `git mv`. **Update every reference to a moved path** in `claims.csv` locators, `% src` comments, `main.tex`, the results book, the notebook and the scripts.
2. Remove clutter:
   - the tracked `build.log`, `__pycache__`, `.DS_Store` and LaTeX build files;
   - any absolute or personal path (`/Users/...`, user names) in any file, including notebook outputs;
   - dead code, commented-out blocks and unused imports.
3. Keep Piero's layout convention (`params` / `data` / `stats` / `plots` + `run.ipynb`, in his notebook format). Use short docstrings, consistent names and no new abstraction layers.
4. **Gate 1:**
   - `run.ipynb` restarts and runs top to bottom, with Gates 1–3 passing;
   - every v2/v3 result file is byte-identical to before;
   - `claims.csv` re-verifies 100% by locator;
   - `check_sources.py` passes;
   - the report and the results book both build cleanly;
   - the frozen repo fingerprint is unchanged.

## Stage 2: Final code review (independent)

1. Spawn a fresh reviewer subagent. Ask it to review `analysis/`, `results/build_results_book.py` and `report/check_sources.py` for:
   - look-ahead or timing errors (publication lags, as-of dates, the tranche and holding logic);
   - backtest correctness against the frozen study;
   - statistics: Newey–West lags, deflated Sharpe trial counts, placebo construction, bootstrap;
   - reproducibility: seeds, paths, determinism;
   - readability.
2. It returns a ranked list. Apply only fixes that leave every result unchanged. Log anything that would change a number in `OPEN_ISSUES.md`, with its expected effect.
3. **Gate 2:** same checks as Gate 1.

## Stage 3: Complete report v1 (so Romain has very little left)

**3a. Integrate Al Yazid's section** (`docs/team_inputs/al_claude_section.md`, his words).
- Verify every number in it against the files. Add each one to `claims.csv`. Correct any that do not match, and list the corrections in the handoff.
- **Table 7 (section 3.4):** use Al's content for P1, P2, the judge row (P3), P4 and P5. Condense each cell to at most about 20 words. Keep Fable's P6 row.
- **Al's critique line goes in the P2 row**, since it is about agent feedback. Leave `\todo{critique: <name>}` placeholders for P1 (Alex), P3 (Elouan), P4 (Romain), P5 (Piero) and P6 (Alex).
- **Judge disagreements:** replace the paragraph with Al's analysis, shortened to at most about 90 words. It comes from the Opus follow-up, so cite `follow_the_workers_opus55_xhigh/outputs/human_review_submission.md`.
- **Reflection:** rewrite it from Al's "good at / bad at" points and his bottom line, in at most about 120 words, and remove `\prov{draft}`. His full section, condensed, goes in Appendix A as "Detailed evaluation of Claude".
- **Executive summary:** replace the Claude TODO with one sentence built from Al's bottom line. Stay within 230 words.

**3b. Make the reason for using Claude consistent.**
- Al's draft says "no OpenAI API key was available". The report says this term's course allows Claude.
- Use one statement: *this term's course allows Claude; the switch from the ChatGPT template is logged as amendments 001–002 (`deviations.md`)*.
- Drop the API-key reason unless a file supports it.

**3c. V2d provenance (Al asked: "were V2d's signs and 12-month hold picked on research data only?").**
- The answer is no. State it plainly in 3.3, in one or two sentences:
  - the negative sign comes from theory (Belo–Lin–Bazdresch);
  - the 12-month horizon was chosen from diagnostics that included the test period (the full-sample horizon table);
  - on research data alone, V2d's 12-month IC is +0.047 with a horizon-matched placebo p of 0.26.
- That is why V2d is post-hoc and why the Q4 2026 forward test is the only clean test. Add the claim to the register.

**3d. Check the rest of what Al raised.**
- V2a stays the declared headline.
- The v2 test columns are labelled post-hoc everywhere.
- The best post-hoc test Sharpe of about 0.35 implies t ≈ 1.2 over 142 months; say so once, next to the power line.
- `FINDINGS_AND_PROPOSAL.md` is now in `docs/`. Point to it from row P5.

**3e. Page budget and build.**
- Executive summary at most 230 words. Section 3 at most 4 pages: Figure 5 (`fig_v2_windows`) goes to the appendix if it isn't there already. Main body at most 10 pages.
- Run `check_sources.py`. Build with zero errors, zero undefined references and no overfull box above 5pt. Render every page and fix the layout.
- Keep `\drafttrue` so the remaining human TODOs stay visible.
- The remaining TODOs should be only: Alex ("6 astra", freeze hashes, P1 counts), Elouan (references, link dates), the five critique cells, and Romain's final pass.

## Stage 4: README.md, the front page of the repo

Write a beautiful, clean README in plain English. It is the first thing graders and the team see.

1. **Header.** Title, one-line question, team (all five names), course (MFE 230GA – Active Equity Management, Fall 2026; instructors Raffaele Savi and Gerald Garvey, BlackRock), and links to `report/main.pdf` and `results/results_book.pdf`.
2. **The answer in five lines.** H1 rejected (confirmatory); H2 consistent with the data but not established (post-hoc, fragile in time); H3 untestable as designed; the verdict, "Do not implement"; the forward test is live.
3. **Scoreboard.** One table with every strategy, Alex's and ours: label, research / test / full / last-18-month Sharpe, verdict. Below it, a legend for CONFIRMATORY / POST-HOC / FORWARD TEST.
4. **Key figures.** Export 2–3 figures to `docs/img/*.png`: the horizon profile, the cumulative returns, the timeline. Embed them.
5. **Repository map.** A tree with one line per folder and per important file, saying what it is and what produces it. Cover every file a reader might open.
6. **Pipeline diagram.** A Mermaid flowchart (GitHub renders it): data, then signals, then the frozen study (v1) and the v2/v3 specs, then results, the results book and the report.
7. **Reproduce.** Clone with `--recurse-submodules`, `pip install -r requirements.txt`, run `analysis/run.ipynb` (about 35s), build the report with `latexmk -pdf`. Explain what each gate checks and what `STOP.md` means.
8. **Integrity design.**
   - Freeze order and hashes: the v2 spec, v3 spec, forward spec and amendment 001, each with its timestamp and commit.
   - The rule that nothing post-hoc is presented as confirmatory.
   - The claims register.
9. **AI use.** The models and call counts from the logs. What Claude did in each phase. Pointers to Table 7 and Appendix A.
10. **Data sources and licences**, with links.
11. **Team and roles**, as stated by Piero:
    - Alex, Romain and Piero: the idea.
    - Elouan: data collection.
    - Alex: v1 pipeline and frozen study.
    - Piero: v2 iteration and report v1.
    - Romain: report v2.
    - Al Yazid: Claude evaluation.
    - Elouan: references and data appendix.
    - Do not add anything else.

Also add a short `analysis/README.md` and a short `results/README.md`: what each file is and how it is produced.

## Stage 5: Push to GitHub

1. **Make the frozen study a submodule.** Remove `230ga-follow-the-workers/` from `.gitignore`. Add it as a submodule (`https://github.com/Aroesler1/230ga-follow-the-workers.git`) pinned to `c67c486`, at the same path. Keep the frozen files byte-identical, and check the fingerprint again.
2. **Push.** Run `git remote add origin GITHUB_URL`, then push `main`. If authentication fails, stop and print the exact commands for Piero to run.
3. **Verify from a fresh clone.** Clone `GITHUB_URL` with `--recurse-submodules` into a temp folder, then:
   - run `analysis/run.ipynb` there (the gates pass, and the v2/v3 outputs match the original byte for byte);
   - build `report/main.tex` there;
   - delete the temp folder.
   Record the result in `docs/process/clone_check.md`, commit it and push.

## Stage 6: Handoff

1. Write `docs/process/HANDOFF.md`:
   - the repo URL;
   - what changed today;
   - corrections made to Al's numbers, if any;
   - the remaining TODOs, with owner and line number;
   - open issues from Stage 2;
   - how to build on Overleaf (upload `report/`).
2. Commit and push.
3. Print, ready to paste into the team chat:
   - the repo URL;
   - one line on where the PDF is;
   - the remaining items with owners;
   - the answer to Al's V2d question (from 3c).
