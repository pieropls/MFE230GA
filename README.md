# 230GA Final Project: Follow the Workers

Start with **[docs/FINDINGS_AND_PROPOSAL.md](docs/FINDINGS_AND_PROPOSAL.md)**. It covers where the project stands, what is wrong with it, and the improvement plan.

| Path | Contents |
|---|---|
| `docs/FINDINGS_AND_PROPOSAL.md` | Review of both completed studies, and the proposal (3 Oct 2026) |
| `docs/blueprint.html` | Blueprint v4 artifact (Piero) |
| `docs/course/FinalProject.pdf` | Course assignment sheet |
| `230ga-follow-the-workers/` | Clone of Alex's private repo `Aroesler1/230ga-follow-the-workers`, unmodified. Run `git pull` inside it to update. |
| `analysis/` | Exploratory diagnostics on public data. Independent of the frozen studies; writes nothing into the team repo. |

## Morning deliverables (4 Oct 2026)
- `docs/process/MORNING_BRIEF.md`: verdict, scoreboard, what changed, remaining todos with owners, risks, how to build.
- `results/`: `results_book.pdf`, `VERDICT.md`, `claims.csv` (every number the report may use, verified by locator), `scoreboard.csv`.
- `report/main.pdf`: report v1 (draft marks on); `docs/process/REVIEW.md`: two independent review rounds.

## Overnight rebuild (3 Oct 2026)
- `docs/process/ITERATION_PROMPT.md`: the Claude Code task for the v2 iteration and report v1, including how to run it (model, effort, kickoff lines).
- `CLAUDE.md`: rules Claude Code follows in this folder.
- `report/`: LaTeX report skeleton (`main.tex`, `refs.bib`). Build with `latexmk -pdf main.tex`.
