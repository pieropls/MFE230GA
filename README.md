<div align="center">

# Follow the Workers

### Do labor-market flows predict which U.S. industries outperform?

**Piero Pelosi · Alex Roesler · Romain Almeida · Elouan Bahri · Al Yazid Bensaid**

MFE 230GA – Equity Markets · UC Berkeley Haas · Fall 2026 · Final project

[Report](report/main.pdf) · [Results Book](results/results_book.pdf) · [Verdict](results/VERDICT.md) · [Claims register](results/claims.csv)

</div>

---

## The answer in five lines

1. **H1, demand channel (preregistered, tested once): rejected.** Ranking 13 industry groups on the year-over-year change in openings, hires, layoffs and hours, as known at the time, lost 4.6% a year after costs over 142 untouched months (Sharpe −0.58, IC −0.021, placebo p 0.72). *Do not implement.*
2. **Why it failed:** two of the four preregistered signs (layoffs, hours) have the opposite sign in the data; the one stable one-month signal, wage growth, was dropped during the build; and the labor market never tightened in the research years, so the tightness moderator (H3) could not be tested.
3. **H2, cost and investment channel (post hoc): consistent with the data, not established.** Industries that hire and lose workers fastest earn lower returns over the following 9 to 24 months. A 12-month book on that sign (V2d) is positive in every window (test Sharpe +0.29, 12-month IC +0.096, t 2.43) but was designed after the test was opened, lost money in the first test half and has a deflated Sharpe of 0.05 after 132 looks.
4. **Forward test:** four paper books, frozen on 3 October 2026 for the 30 September decision and held to 31 December, with no capital behind them ([analysis/forward/](analysis/forward/)).
5. **Claude as research assistant:** a useful auditor and idea generator when a human checked every claim against the code and data and it could not change the rules after seeing results; all 25 P1 findings, 10 P4 concerns and 25 judge labels needed that check.

---

## Every strategy we ran

Net Sharpe ratios after 10 bp industry costs and 2 bp hedge costs, annualised. Source: [results/scoreboard.csv](results/scoreboard.csv), built by [results/build_results_book.py](results/build_results_book.py) from the frozen `results.json` and [analysis/output/tables/](analysis/output/tables/).

| Strategy | Label | Research | Test | Full | Last 18 m | IC (t) | DSR | Reading |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A3 primary (Sonnet agents) | CONFIRMATORY | −0.13 | **−0.58** | −0.44 | +0.85 | −0.021 (−1.08) | 0.00 | Do not implement |
| A0 fixed rule | CONFIRMATORY | −0.44 | −0.36 | −0.48 | −1.56 | −0.020 (−0.71) | 0.00 | negative |
| A1 ridge | CONFIRMATORY | −0.54 | −0.51 | −0.52 | +0.73 | −0.014 (−0.74) | 0.00 | negative |
| A1-T tightness | CONFIRMATORY | −0.55 | −0.59 | −0.58 | −0.37 | −0.029 (−1.42) | 0.00 | negative |
| A4 islands | CONFIRMATORY | −0.18 | −0.79 | −0.56 | +1.23 | −0.020 (−0.86) | 0.00 | negative |
| A4 primary (Opus follow-up) | EXPLORATORY | −0.40 | +0.01 | −0.13 | −1.41 | −0.002 (−0.10) | 0.00 | fails G2–G5 |
| V2a wage growth (declared headline) | POST-HOC | +0.09 | +0.16 | +0.15 | −1.71 | +0.049 (+2.04) | 0.02 | noise after the looks taken |
| V2b signed composite | POST-HOC | −0.06 | −0.15 | −0.11 | −1.34 | +0.042 (+1.65) | 0.00 | noise after the looks taken |
| V2c wage + momentum | POST-HOC | +0.27 | +0.35 | +0.32 | −0.78 | +0.032 (+1.21) | 0.09 | momentum supplies the return |
| V2d −(hires + quits), 12-month hold | POST-HOC | +0.50 | +0.29 | +0.35 | +0.29 | +0.096 (+2.43)\* | 0.06 | thesis result, fragile in time |

**Legend.** CONFIRMATORY: preregistered, frozen and hashed before the test period (Nov 2014–Aug 2026) was opened once. EXPLORATORY: the Opus follow-up, run after the test had been seen. POST-HOC: chosen on 3 Oct 2026 after the test was opened; specs were hashed before running and every variant is reported. DSR: deflated Sharpe ratio (Bailey and López de Prado), 41 nominal trials for the frozen study, 112 for v2. \*12-month IC; the one-month IC of V2d is −0.020.

<p align="center"><img src="docs/img/fig_cumulative.png" width="720" alt="Cumulative returns: every preregistered strategy lost money in the test"></p>
<p align="center"><em>Every preregistered H1 book lost money in the test; the post-hoc wage-growth book gained until 2024 and gave much of it back.</em></p>

<p align="center"><img src="docs/img/fig_horizon_profile.png" width="720" alt="Horizon profile of the H2 score"></p>
<p align="center"><em>The H2 score has no one-month IC and a positive IC from 9 to 24 months, peaking at 12 (post hoc).</em></p>

<p align="center"><img src="docs/img/fig_v2_windows.png" width="720" alt="Net Sharpe by window"></p>
<p align="center"><em>Only V2d is positive in every window; V2a and V2c lost heavily in the last 18 months.</em></p>

---

## How the pipeline fits together

```mermaid
flowchart LR
  A[Frozen study<br/>230ga-follow-the-workers<br/>sealed results.json] -->|read-only import| B[analysis/run.ipynb]
  D[Ken French 49 industries<br/>FRED + ALFRED labor series] --> B
  B --> G1{Gate 1<br/>reproduce sealed A0<br/>to 1e-16}
  G1 -->|pass| C[Diagnostics D1–D10]
  C --> S2[v2_spec.md<br/>hashed before run] --> V2[v2 variants, run once<br/>run log enforces byte identity]
  V2 --> S3[v3_spec.md<br/>hashed before run] --> V3[V2d robustness R1–R11]
  V2 --> F[forward/spec_frozen.md + amendment 001<br/>Q4 2026 book]
  F --> G3{Gate 3<br/>specs frozen before runs}
  V3 --> G2{Gate 2<br/>frozen folder fingerprint<br/>v2 outputs unchanged}
  G2 --> R[results/build_results_book.py<br/>claims.csv verified by locator]
  G3 --> R
  R --> P[report/main.tex<br/>every number has a % src comment]
  G1 -.fail.-> X[analysis/output/STOP.md]
  G2 -.fail.-> X
  G3 -.fail.-> X
```

The frozen study is never edited, rerun or retuned; its code is imported read-only and the sealed result (A3, Sharpe −0.58) stands. Every result carries exactly one label, CONFIRMATORY, POST-HOC or FORWARD TEST; post-hoc specs were written and hashed before they ran, every pre-declared variant is reported, and every look is counted in the deflated Sharpe ratio. [results/claims.csv](results/claims.csv) is the only source the report may quote; each claim has a machine-readable locator and is re-verified on every build (106 of 106 verified).

---

<details>
<summary><strong>Reproduce everything in three commands</strong></summary>

```bash
git clone https://github.com/pieropls/GA.git follow-the-workers
cd follow-the-workers
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
# 1. numbers, tables, figures (about 35 s); stops with analysis/output/STOP.md if any gate fails
jupyter nbconvert --to notebook --execute --inplace analysis/run.ipynb
# 2. claims register, scoreboard, Results Book
python3 -B results/build_results_book.py && (cd results && latexmk -pdf results_book.tex)
# 3. report
(cd report && python3 -B check_sources.py && latexmk -pdf main.tex)
```

Gates, in the order the notebook runs them: **Gate 1** rebuilds the 13 group returns and the preregistered A0 signal and matches the frozen study's 50 saved ledgers to 1.5e-16; **Gate 3** checks that every spec hash matches its file and that each freeze timestamp precedes its first run; **Gate 2** checks that the frozen folder still has 3,067 files with fingerprint `eb109be9…` and that the v2 and v3 outputs are byte-identical to their first runs. A failed gate writes `analysis/output/STOP.md` and the notebook stops; nothing downstream is regenerated. Use `python3 -B` (or `PYTHONDONTWRITEBYTECODE=1`) so no `__pycache__` lands in the frozen folder. Byte identity is expected in the recorded environment ([analysis/output/environment.txt](analysis/output/environment.txt)); another BLAS build may differ in the last bit.

</details>

<details>
<summary><strong>Repository map</strong></summary>

| Path | Contents |
|---|---|
| [README.md](README.md) | this page |
| [requirements.txt](requirements.txt) | Python packages (loose pins; recorded versions in the comment) |
| [230ga-follow-the-workers/](230ga-follow-the-workers/) | Alex's frozen preregistered study, imported with his git history at `c67c486`. Read-only ([provenance](docs/process/frozen_provenance.md)) |
| [analysis/](analysis/) | our iteration: `params.py`, `data.py`, `stats.py`, `plots.py`, `run.ipynb`; frozen specs; forward test; outputs ([README](analysis/README.md)) |
| [results/](results/) | claims register, scoreboard, Results Book (PDF + markdown), verdict ([README](results/README.md)) |
| [report/](report/) | LaTeX report on the house template: `main.tex`, `preamble.tex`, `refs.bib`, `figures/`, `tables/`, `code/` |
| [docs/](docs/) | [diagnosis of the frozen study](docs/FINDINGS_AND_PROPOSAL.md), [blueprint](docs/blueprint.html), [course sheet](docs/course/FinalProject.pdf), `img/`, [team inputs](docs/team_inputs/), [process](docs/process/) (project rules, prompts, brief, review rounds, code review, handoff, open issues) |

</details>

<details>
<summary><strong>How the results are protected: hashes, timestamps, commits</strong></summary>

| Artefact | SHA-256 (first 8) | Frozen (UTC, 3 Oct 2026) | First run | Commit |
|---|---|---|---|---|
| [analysis/v2_spec.md](analysis/v2_spec.md) (V2a–V2d, reading rule, 112 looks) | `ca658234` | 09:00:13 | 09:01:55 | `d76fbb3` |
| [analysis/forward/spec_frozen.md](analysis/forward/spec_frozen.md) | `735a8ffa` | 09:03:56 | book 09:17:55 | `45991d4` |
| [analysis/forward/spec_amendment_001.md](analysis/forward/spec_amendment_001.md) | `c76cde86` | 09:16:11 | book 09:17:55 | `96b828f` |
| [analysis/forward/book_2026Q4.csv](analysis/forward/book_2026Q4.csv) (first build) | `85727526` | 09:17:55 | | `9f4a50f` |
| [analysis/v3_spec.md](analysis/v3_spec.md) (R1–R11, 132 looks) | `312aef1d` | 09:52:27 | 09:53:32 | `8fd75ae` |
| Frozen study folder (3,067 files) | `eb109be9` | imported at `c67c486` with Alex's history | checked every run | [provenance](docs/process/frozen_provenance.md) |

- [analysis/output/v2_run_log.md](analysis/output/v2_run_log.md) and [v3_run_log.md](analysis/output/v3_run_log.md) hold the hashes of the first run; later runs must reproduce them or the notebook stops.
- [report/check_sources.py](report/check_sources.py) fails the build if a `% src:` comment swallows text.
- The forward test is evaluated once, on 31 December 2026, whatever it shows.
- Issues found and deliberately not fixed, because fixing them would change a frozen file or a recorded result: [docs/process/OPEN_ISSUES.md](docs/process/OPEN_ISSUES.md).

</details>

---

## How we used Claude

Claude did every AI job, which this term's course allows; the switch from the ChatGPT template is logged as preregistration amendments 001 and 002 in the frozen study. Confirmatory study: Claude Sonnet 5.5 at medium effort, 199 logged calls (P1 audit, P2 blinded signal agents, P3 migration judge, P4 red team). Follow-up: Claude Opus 5.5 at extra-high effort, 294 calls. Post-mortem review and this iteration: Claude Code (Opus 5.5, then Fable 5.1) under the [project rules](docs/process/project_rules.md); prompts in [docs/process/](docs/process/). The engineering assistant that wrote the frozen pipeline is not documented in the repository (open item for Alex). Section 3.4 and Appendix A of the [report](report/main.pdf) evaluate what Claude got right and wrong.

---

## Data sources and terms

- **Ken French Data Library**: 49 value-weighted industry portfolios, five factors and momentum (CRSP build 202608). Free for academic and non-commercial use with attribution. [analysis/data/french/](analysis/data/french/).
- **BLS JOLTS and CES via FRED**: industry openings, hires, quits and layoffs rates (not seasonally adjusted), average weekly hours and hourly earnings; `JTSJOL` and `UNEMPLOY` for tightness. BLS data are U.S. government works in the public domain; FRED and ALFRED redistribute them under the St. Louis Fed terms of use. Current values in [analysis/data/fred/](analysis/data/fred/), the 29 September 2026 vintage in [analysis/data/alfred_2026-09-29/](analysis/data/alfred_2026-09-29/).
- The frozen study's own ALFRED vintage files sit inside [230ga-follow-the-workers/](230ga-follow-the-workers/) and are not duplicated here.

---

## Team and contributions

| Who | Did |
|---|---|
| Piero Pelosi, Alex Roesler, Romain Almeida | idea |
| Elouan Bahri | data collection |
| Alex Roesler | v1 pipeline (the frozen preregistered study) |
| Piero Pelosi | v2 iteration and report v1 |
| Romain Almeida | report v2 |
| Al Yazid Bensaid | Claude evaluation |
| Elouan Bahri | references and data appendix |

Open items and who owns them: [docs/process/HANDOFF.md](docs/process/HANDOFF.md).
