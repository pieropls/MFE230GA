# Follow the Workers: where the project stands, what is wrong with it, and how to fix it

*Prepared 3 Oct 2026 for Piero, the team, and the Claude chat where the blueprint was written. Based on a full read of Alex's repository ([230ga-follow-the-workers/](230ga-follow-the-workers/), commit `c67c486`, 2 Oct), the blueprint artifact ([230GA - Project.html](230GA%20-%20Project.html), v4, 24 Sep), the build-and-run prompt, the catch-up briefing and the assignment sheet ([FinalProject.pdf](FinalProject.pdf)).*

*Source of the numbers. Unmarked numbers come from the saved outputs of the two completed studies. Numbers marked **[exploratory]** come from my own diagnostics, which are post-hoc and use revised public data. Those diagnostics are in [analysis/diagnostics.py](analysis/diagnostics.py), with output in [analysis/output/diagnostics.md](analysis/output/diagnostics.md). They change nothing in either study.*

---

## 0. Summary

**Where we are.** Alex ran the blueprint end to end twice. An AI coding agent was the engineer (possibly OpenAI Codex, see §4.1), and Claude did every research role, called through the Claude Code CLI:
- an original study whose research agents were Claude **Sonnet 5.5**;
- an exploratory follow-up with Claude **Opus 5.5** at extra-high effort, requested after the first study's test results had been seen.

Both studies conclude **"Do not implement"**. The engineering discipline is excellent: point-in-time ALFRED vintages, a sealed test opened once, and hash-pinned code and inputs. The deliverable is not usable as a course submission.

**Why it cannot be submitted as it is.** Six reasons, in order of severity:

1. **Zero ChatGPT interactions.**
   - The assignment requires at least 3 documented ChatGPT interactions and a reflection on ChatGPT. Every AI role ran on Claude.
   - The report leaves this as an open "team submission consideration".
2. **The thesis is never answered.**
   - The question was: is hiring demand news or cost news, and does labor-market tightness decide which?
   - The report shows no results for individual signals, no signs and no literature.
   - The tightness test cannot work as designed: 133 of the 142 test months fall in a single tightness bin (Figure 05 is literally one dot per strategy).
3. **The report reads like an audit log, not an investment report.**
   - It runs to about 4,000 words of compliance prose ("transport attestation", "amendment chain", "technical restart").
   - The "Style/risk factor exposures" section has one sentence of interpretation.
   - Two studies are interleaved, and several figures carry no information.
4. **Design flaws make parts of the result meaningless, not just negative.**
   - The agent features selected for A3 are active in only 3 of the 142 test months, so A3 is effectively A1.
   - One selected feature was chosen on 15 research months.
   - The ridge penalty landed on the upper edge of its grid in every model.
   - The primary strategy was picked from five strategies that all lost money in research.
5. **The analysis a grader expects is missing.** There are no signal-level ICs or decay profiles, no industry-momentum benchmark (it is the assignment's own suggested reading), no interpretation of factor loadings, and no P&L by industry.
6. **Loose ends.**
   - The "Team critique" columns are empty.
   - The Opus run was launched after a look at the results ("this is horrible, can't we do better?", amendment 005).
   - Its near-zero Sharpe comes almost entirely from being long Durable Manufacturing, a group that was 55% semiconductors by market cap in 2024. The gains are spread over 2016–2024.

**What I propose (detail in §6).**
- Keep the preregistered Sonnet study as the confirmatory core, with its verdict unchanged.
- Around it, build four things:
  1. a clearly labelled diagnostic layer that explains *why* it failed, which is where the thesis and execution marks are earned;
  2. a ChatGPT layer: I prepare the prompt packets and the team runs them;
  3. a full rewrite of the report in the course template, with a new figure set;
  4. a genuine forward test: a v2 specification frozen *now*, whose 30 Sep 2026 book is held for Oct–Dec 2026 (only 2 trading days of that window have passed). That book also delivers the "Q4 2026, maximize P&L" framing from the 21 Sep meeting.

**Decisions needed from you:** §8.

---

## 1. What is in this folder

| Path | What it is | Owner |
|---|---|---|
| [FINDINGS_AND_PROPOSAL.md](FINDINGS_AND_PROPOSAL.md) | This document | Claude |
| [230GA - Project.html](230GA%20-%20Project.html) | Blueprint v4 artifact (design, data links, pipeline, rubric map) | Piero |
| [FinalProject.pdf](FinalProject.pdf) | Course assignment sheet | Professor |
| [230ga-follow-the-workers/](230ga-follow-the-workers/) | Clone of Alex's private repo, left untouched (`git pull` updates it) | Alex |
| [analysis/](analysis/) | My exploratory rebuild from public data, plus `diagnostics.py`. Independent of the frozen pipeline. | Claude |

Inside the team repo, read these first:
- [README.md](230ga-follow-the-workers/README.md), [handoff.md](230ga-follow-the-workers/handoff.md) and [TEAM_REVIEW.md](230ga-follow-the-workers/TEAM_REVIEW.md): Alex's summary and the remaining team tasks.
- [original_documents/](230ga-follow-the-workers/original_documents/): the briefing and build prompt, unchanged.
- [outputs/follow_the_workers/](230ga-follow-the-workers/outputs/follow_the_workers/): the original Sonnet study (source code, `report/`, `outputs/`).
- [outputs/follow_the_workers_opus55_xhigh/](230ga-follow-the-workers/outputs/follow_the_workers_opus55_xhigh/): the Opus follow-up, with the same layout.

Within each study, the important files are:
- `report/report.md` and `report/chatgpt_log.md`;
- `outputs/deviations.md` and `outputs/checkpoints.md`;
- `outputs/research_summary.json` and `outputs/selected_features.json`;
- `outputs/sealed/initial/results.json`, with the monthly ledgers, weights, scores and ICs beside it;
- `outputs/prereg_amendments/` and `outputs/agents/`.

Raw data and intermediate panels are **not** in the repo. I verified that the public Ken French files reproduce the study's industry-group returns exactly: the saved sealed ledgers match to a maximum absolute error of 1e-16 ([diagnostics §1](analysis/output/diagnostics.md)). So the return side can be rebuilt without Alex's data zip. Rebuilding the labor side exactly needs ALFRED vintages (see §8, decision 6).

---

## 2. What happened

### 2.1 Timeline

| Date (2026) | Event |
|---|---|
| 23–24 Sep | Blueprint v4 and build prompt finished (Piero). The plan called for ChatGPT agents through the OpenAI API, but nobody had an API key. |
| 26 Sep | Catch-up briefing for Al. The deadline was believed to be **Sun 27 Sep** (still to be confirmed on bCourses). |
| 28 Sep | Stages 0–4 and 6 run. **Amendment 001**: no OpenAI key, so the agents switch to Claude Sonnet 5.5 through Alex's Claude subscription. |
| 29 Sep | **Amendment 002**: Claude for every AI role, including the P1 audit and P4 red team. The first research run was paused when 23 of 70 proposals and 0 of 12 migration reports had passed validation. **Amendments 003–004**: fixes, the whole run discarded, a fresh run started. Fresh research completed the same day. |
| 2 Oct, 06:00 UTC | Freeze (525 file hashes), single sealed evaluation, verdict **Do not implement** (primary A3). |
| 2 Oct, 06:12 UTC | **Amendment 005**: "this is horrible, cant we do better? ... lets try it with all opus 5.5 agents". Opus follow-up run, verdict **Do not implement** (primary A4). |
| 2 Oct | Private repo published. Team critique and course submission still outstanding. |

### 2.2 Where the implementation departs from the blueprint

| Blueprint | Implemented | Consequence |
|---|---|---|
| ChatGPT agents through the API (P2, P3), ChatGPT P1 and P4 | Claude Sonnet 5.5 (and Opus 5.5 in the follow-up) through the Claude Code CLI. The model's seed and temperature parameters are not supported. | Course compliance risk (§4.1). The "seeds" are independent repetitions, not seeded runs. |
| S\* set by the vintage audit | Fixed first test decision on 31 Oct 2014, with October 2014 purged. Core vintages actually start in March 2011. | 125 selection months and 142 test months, as planned. |
| LinkUp and WARN gated on day 1 | Acquired, then failed the evidence gates (no collection-failure history, no point-in-time mapping) | Q2 (company data) is unanswered and A2 does not exist. |
| F6 wage–price, if at least 9 groups have an exact PPI match | Only 2 exact matches, so F6 was dropped | **Wage growth was dropped with it** (see §4.2). |
| A5 LightGBM (optional) | Not installed, omitted | Minor. |
| One run | First run discarded, fresh restart (amendment 004) | Disclosed. |
| — | Opus follow-up after the sealed results were seen | Exploratory only. Not a second holdout. |

---

## 3. Results as they stand

### 3.1 Strategies: research period vs test period (net Sharpe; mean 1-month rank IC with HAC t)

The research comparison covers 88 months (Jun 2007 to Sep 2014). The test covers 142 months (Nov 2014 to Aug 2026).

| Strategy | What it is | Research Sharpe | Test Sharpe | Test IC (t) |
|---|---|---:|---:|---:|
| A0 | Fixed rule: mean(z openings, z hires, −z layoffs, z hours) | −0.44 | −0.36 | −0.020 (−0.71) |
| A1 | Ridge on F1–F5 | −0.54 | −0.51 | −0.014 (−0.74) |
| A1-T | A1 plus feature × tightness interactions | −0.55 | −0.59 | −0.029 (−1.42) |
| A3, Sonnet (**primary**) | A1 plus 2 independent-agent features | −0.13 | −0.58 | −0.021 (−1.08) |
| A4, Sonnet | A1 plus 2 island-agent features | −0.18 | −0.79 | −0.020 (−0.86) |
| A3, Opus | A1 plus 1 independent-agent feature | −0.48 | −0.46 | +0.001 (+0.05) |
| A4, Opus (**primary**) | A1 plus 3 island-agent features | −0.40 | +0.01 | −0.003 (−0.10) |

Gate results for both primaries: **G1 passes; G2 to G5 fail.** For the Sonnet primary (A3):
- placebo p = 0.72;
- factor alpha −0.38% a month (t −1.86);
- Sharpe at 25 bp costs −0.79;
- cost breakeven −32 bp, meaning it loses money even with zero trading costs.

All four Holm-family comparisons have adjusted p = 1.0 in Sonnet, and the smallest is 0.80 in Opus.

### 3.2 The agent experiment (Q3)

| | Sonnet study | Opus study |
|---|---|---|
| Valid proposals | 98 / 108 | 106 / 108 |
| Migration reports admitted | 7 / 18 | 15 / 18 |
| Usable machine uptake labels | 8 / 36 (the other 28 responses were not bare JSON) | 84 / 88 |
| Best-so-far IC, islands vs independent | 0.049 vs 0.083 | 0.136 vs 0.059 |
| Gap between arms larger than the spread across seeds? | No (all four metrics) | No (all four metrics) |
| Human spot check of uptake labels | 8 pairs, 2 comparable | 17 pairs: human yes 3, machine yes 10, agreement 10/17. All 7 disagreements are machine-yes / human-no. |
| Features passing research selection that failed in the test | 4 / 4 | 6 / 6 |

The P4 red team, run on research tables only before the seal was opened, already concluded: *"Overall verdict: do not implement. Every variant has a negative net Sharpe, an insignificant IC, and a DSR near zero."* ([p4_response.md](230ga-follow-the-workers/outputs/follow_the_workers/outputs/p4_response.md))

---

## 4. Assessment: why this cannot be submitted as it is

Organised by the grading rubric: Thesis 40%, Execution 40%, Originality 20%. Course compliance comes first.

### 4.1 Course compliance

| Requirement (assignment sheet) | Status | Problem |
|---|---|---|
| "Integrate ChatGPT as your AI research assistant" | ✗ | No ChatGPT at all. The report says the acceptability of Claude "remains a team submission consideration". Nobody has asked the professor. |
| At least 3 substantial **ChatGPT** interactions (ideas, coding, robustness) | ✗ | P1, P2 and P4 exist, but on Claude. None of P4's ten suggestions led to a new test (each was marked "covered by" an existing diagnostic or "no additional test adopted"), so "how we adapted" reads as "we didn't". |
| Document each one: prompt, summarised output, critical evaluation | Partial | [chatgpt_log.md](230ga-follow-the-workers/outputs/follow_the_workers/report/chatgpt_log.md) has four rows that link to JSON files. **The Team critique column is empty.** |
| Reflect on ChatGPT's strengths and limits | ✗ | Section 3d describes the Claude transport and process, with no reflection in our own words. |
| Template: Section 2 is 2–5 pages, Section 3 is 1–4 pages | ✗ | Section 2c is about 1,000 words of unbroken prose with no equations or tables. Section 3a has one sentence about factors. |
| Time windows: full, post-2010, last 12–18 months | ✓ | Present, but mixes research and test segments without saying so clearly. |
| Factor exposures | Weak | Table present, no interpretation. |
| Briefing checklist §10.2 | Open | Team critique, Q4/midterm point, contribution statement and submitter choice are all still open. |

One thing to check with Alex: [agents.py](230ga-follow-the-workers/outputs/follow_the_workers/agents.py) sandboxes the agent calls so they cannot read `/Users/alex/.codex` ("cannot read study inputs or Codex context"). That suggests **the engineering agent that wrote and ran the pipeline may have been OpenAI Codex**. If so, the coding-support interaction was with an OpenAI model and can be documented, which partly addresses the requirement.

### 4.2 Thesis (40%): the central question is never actually tested

The thesis in the blueprint was: *"Is hiring demand news or cost news, and does tightness decide?"* The report only ever tests combined models (A0, A1, and so on). It never says which labor signals point which way. My exploratory check (revised data, fixed publication lags, the same universe and target) shows why that matters:

**[exploratory] Single-signal rank IC against next-month relative return**

| Signal | Sign assumed in A0 | Research 2004–14 | Test 2014–26 | Full sample |
|---|---|---:|---:|---:|
| F1 Openings | + | +0.001 | −0.011 | −0.005 (t −0.3) |
| F2 Hires | + | +0.012 | +0.013 | +0.013 (t +0.7) |
| F3 Quits | (not in A0) | +0.014 | +0.002 | +0.009 (t +0.5) |
| F4 Layoffs | **−** | **+0.033** | **+0.026** | **+0.028 (t +1.4)** |
| F5 Hours | **+** | −0.015 | −0.009 | −0.012 (t −0.8) |
| W Wage growth (dropped with F6) | — | **+0.039** | **+0.041** | **+0.040 (t +2.4)** |
| A0 as preregistered | | −0.018 | −0.006 | −0.011 (t −0.6) |
| Industry momentum (12-1) | | +0.050 | +0.017 | +0.034 (t +1.7) |

What this suggests:

1. **A0 assumed the wrong sign for two of its four inputs.**
   - Layoffs: more layoffs predicted *higher* next-month relative returns, in both the research and the test period.
   - Hours: the sign is also reversed.
   - A0 therefore combined two near-zero signals with two signals of the wrong sign. That is enough to explain why the "economics-signed" benchmark had a negative IC.
2. **Horizon matters, and it speaks directly to "demand news vs cost news".** At a 12-month horizon, all four JOLTS flow signals turn negative. Hires go to −0.062 (t −2.1) and quits to −0.065 (t −1.7) ([diagnostics §4](analysis/output/diagnostics.md)).
   - This is the investment (q-theory) channel of **Belo, Lin and Bazdresch (2014, JPE)**: firms that hire a lot earn *lower* subsequent returns, and in our data the same pattern shows up across industries.
   - That is the paper the blueprint cites as background. Its prediction is the opposite of A0's sign, and the report never mentions it.
3. **Wage growth is the most consistent single signal**, with the same sign and size in research and test.
   - It was never a public feature, because F6 (wage growth minus price growth) failed on the price side and the wage half was thrown out with it.
   - **Both agent runs rediscovered it blind.** Sonnet proposed `regime(yoy(V05),"low")` and Opus proposed `tsz(lchg(lag(V05,1),12),36)`, where V05 is hourly earnings.
   - It is *not* significant once you count how many signals and windows I looked at. It is a hypothesis, not a result.
4. **The tightness half of the thesis cannot be tested with the design as it stands** ([diagnostics §5](analysis/output/diagnostics.md)).

   | Tightness split | Research months | Test months |
   |---|---|---|
   | Expanding terciles (low / middle / high) | 55 / 29 / 41 | **3 / 6 / 132** |
   | V/U above 1 | **0** | 75 |
   | 12-month change in T (rising / falling) | 93 / 32 | 88 / 53 |

   - T rose from −1.9 to +0.7 over 2009–2022. Expanding terciles therefore label almost every test month "high", which is why Figure 05 is a single dot per strategy.
   - A split on whether T is rising or falling (tightening vs loosening) is balanced in both periods and has a clear economic meaning.

Literature the report should engage with, and currently does not:
- Belo, Lin and Bazdresch (2014, JPE): hiring and returns;
- Moskowitz and Grinblatt (1999, JF): industry momentum;
- Hong, Torous and Valkanov (2007, JFE): industries lead the market;
- Kuehn, Simutin and Wang (2017, JF): labor-market tightness priced in the cross-section;
- Donangelo, Gourio, Kehrig and Palacios (2019, JFE): labor leverage;
- Zarattini and Antonacci: the course's own suggested reading on industry trends.

### 4.3 Execution (40%): design and implementation findings

Each finding below is verifiable from saved outputs. Items marked † come from my diagnostics.

| # | Finding | Evidence | Consequence | Severity |
|---|---|---|---|---|
| E1 | **Agent features gated on a tightness regime cannot work out of sample.** The `regime(x,"low")` operator uses expanding terciles of T. T trends upward, so "low" almost never happens after 2014. | Sonnet A3's two features: research n = 48 and 43, **test n = 3**. Opus's best island feature (t = 3.56): test n = 3. | Sonnet's primary A3 equals A1 in 139 of 142 test months. The "agent contribution" is an artifact. | High |
| E2 | **No minimum coverage rule in feature selection.** | Opus `independent_1_Interactions_6` was selected on **15** research months. | Selection on noise. | High |
| E3 | **The ridge penalty sits on the upper edge of its grid (α = 1000) in every model.** | `selected_features.json`, both studies. | Cross-validation is saying "shrink toward predicting nothing", and the grid stopped before it could. That signals no predictive content, and nobody acted on it. | Medium |
| E4 | **There is no stop rule at the research stage.** All strategies lost money in research (Sharpe −0.13 to −0.55, IC t ≤ 1.23), and the primary was simply the least bad. | `research_summary.json`. P4's verdict before the seal. | The single look at the test period was spent confirming a null the research data had already shown. A pre-test gate ("no primary with research Sharpe above 0 means stop") would have been better design and a better story. | Medium |
| E5 | **The volatility target is almost never reached.** The 2× gross cap binds in 80–93% of months. Ex-ante volatility averages 7.3–8.0% against a 10% target. A0's realised volatility (9.7%) exceeds its ex-ante estimate (8.0%). | † [diagnostics §1](analysis/output/diagnostics.md) | The risk overlay is mis-calibrated and the report does not mention it. | Low–medium |
| E6 | **The research window is short and dominated by the financial crisis.** 125 selection months shrink to 88 prediction months (Jun 2007 to Sep 2014). Warm-up eats the rest: 12 months for year-on-year changes, 24 for standardisation and 36 for the ridge burn-in. | `research_A0_ledger.csv` | Strategy selection rests on about 7 years that contain one recession. | Structural |
| E7 | **The industry mapping dilutes the labor signal.** "Durable manufacturing" is a value-weighted blend of 14 portfolios dominated by Chips (55% of the group's market cap in mid-2024). "Information" is Telcm only, because Software is excluded. Health-care labor data includes social assistance. | † Opus A4's industry positions net to only +0.04 in total, while Durable mfg alone contributed +0.27 (held long in 64% of months). Without it, the industry book loses about 0.23. The rest of its +0.14 gross came from the market hedge (+0.11). | Labor data and stock returns describe different firms. The one "near-positive" result is exposure to the semiconductor boom. | High (for interpretation) |
| E8 | **Losses are concentrated in a few industries.** Health care is the largest loser for A1 and A3 (−0.26 cumulative) and the second largest for A0 (−0.13, after Durable mfg at −0.14). Construction and Finance follow for A1 and A3. | † [diagnostics §2](analysis/output/diagnostics.md) | Not discussed. This is the material for the "why it failed" section. | Medium |
| E9 | **Factor exposures are reported but not interpreted.** A1 and A3 load on RMW (+0.19 to +0.21, t ≈ 2.2) and HML (−0.15, t ≈ −2.0), with intercepts of −0.35 to −0.38% a month (t ≈ −1.8). A0 loads +0.22 on industry momentum (t 1.9). | `results.json` → `attribution` | The "labor" tilts are partly quality and growth tilts. That is an interpretable finding that goes unused. | Medium |
| E10 | **Costs are not the problem.** Costs run 1.0–1.35% a year against gross returns of −2.5% to −4.8% a year. | Ledgers | The signal is the problem. The report should say so plainly. | Low |
| E11 | **The second study was chosen after the first study's results were seen.** | Amendment 005 | The Opus primary's +0.01 Sharpe is not evidence. The repo labels this correctly, but the two studies are interleaved in the narrative. | Medium |
| E12 | **The LLM judge over-attributes idea uptake.** Agreement with the human is 10/17, and all 7 disagreements are machine-yes. In Sonnet, 28 of 36 judge outputs were unusable (not bare JSON). | `human_review_submission.md` | A good finding for Section 3d that is currently buried. | Positive (if surfaced) |

**What is genuinely good, and should be kept and showcased:**
- point-in-time vintages with the ASOF, FIRST, REVISED and FIXEDLAG variants (the revision gap is real evidence);
- a freeze and a single sealed opening, with every result reported whatever its sign;
- a causal circular-shift placebo with refits, drop-one-group, and paired bootstrap with Holm correction;
- the blinded agent design with matched budgets, three repetitions and a human audit of the judge;
- honest disclosure of the restart and the follow-up.

These are execution strengths a grader will reward, *once they can be read*.

### 4.4 Originality (20%): strong raw material, poorly surfaced

The project already contains insights a grader would call original. None of them is stated in the report:
1. **Blinded agents rediscovered wage growth**, the most consistent labor signal, without knowing what V05 was.
2. **Regime conditioning was the agents' best research tool and their worst out-of-sample one.**
   - The operator the design handed them produced the highest research t-statistics (3.56) and features that then vanished in the test.
   - This is a clean case study of how overfitting enters through conditioning.
3. **A more capable model improved compliance, not alpha.**
   - Opus produced 106 valid proposals out of 108, against Sonnet's 98.
   - It got 15 of 18 migration reports admitted, against 7, and 84 of 88 usable judge labels, against 8 of 36.
   - Neither found signal that survived the test.
4. **Communication raised research search scores in one model and not the other, and never carried over to the test.** Islands vs independent best-so-far IC was 0.136 vs 0.059 with Opus and 0.049 vs 0.083 with Sonnet.
5. **The LLM judge is systematically generous about attribution** (E12).
6. **The AI red team called "Do not implement" from research tables alone**, before the seal was opened.

### 4.5 Presentation

- **Jargon.** "Sealed capability", "transport attestation", "amendment chain", "technical restart", "within-run diagnostics". None of it belongs in a course report except in an appendix.
- **No equations.** None for signals, model, portfolio or risk model. Section 2c is prose.
- **Codes without a legend.** A0–A4, F1–F5 and G1–G5 are used without a table explaining them. The executive summary uses "HAC t" and "funded drawdown" without definition.
- **Two studies interleaved.** The Opus report copies the Sonnet methods text, and the comparison table sits in an appendix of the wrong report.
- **Figures.**
  - 01 (pipeline): an arrow runs through a box and most of the canvas is empty.
  - 03 (cumulative returns): no benchmark line.
  - 05 (IC by tightness tercile): one bin.
  - 10 (research vs test scatter): unlabelled points, with no marking of which features were selected or regime-gated.
  - No thesis diagram, no timeline showing the T path, no P&L by industry, no signal-level figure.

---

## 5. What I ran to check all this

1. **Reproduced the return side** from public Ken French data (CRSP 202608 build). My group returns reproduce every saved sealed ledger to 1e-16 ([diagnostics §1](analysis/output/diagnostics.md)). The team can therefore extend the analysis without Alex's data zip.
2. **Rebuilt the labor signals** F1–F5 and W from current FRED data, with the study's fixed lags (JOLTS at d−2, CES at d−1) and the study's standardisation. These are *revised* values, so they approximate the FIXEDLAG variant, not ASOF. In the frozen study, FIXEDLAG and ASOF results were close: the A3 test IC was −0.021 under both.
3. **Computed** single-signal ICs by window and horizon, tightness-regime balance, P&L by industry, use of the risk overlay, test-period coverage of the selected agent features, and the ridge penalties chosen.

Caveats:
- All of this is post-hoc, on a sample everyone has already seen, across about 9 signals × 4 horizons × 3 windows.
- Nothing here is a confirmatory result. Its uses are interpretation ("why did it fail?") and hypotheses for a forward test.

---

## 6. Improvement proposal

### 6.1 Principles

1. **Do not touch the preregistered result.**
   - The Sonnet study is the confirmatory core and "Do not implement" stands.
   - No rerun of the sealed evaluation, no retuning, and no promotion of Opus A4.
2. **Label everything new as either "post-hoc diagnostic" or "forward test".** The report should make this distinction visually, for example with a coloured tag on every table and figure.
3. **The Opus study is evidence for the AI evaluation, not a strategy result.** It answers "does a stronger model search better?", not "does the strategy work?".
4. **Write for the grader.** Lead with the thesis, the answer and what we learned. Move the integrity machinery to one methods box and an appendix.
5. **Every number traces to a file**, as the blueprint already required.

### 6.2 Work packages

| ID | Work package | Rubric target | Who | Needs |
|---|---|---|---|---|
| **WP1** | **ChatGPT layer.** I write 4 prompt packets (exact prompt plus attached context); the team runs them in ChatGPT and saves share links. (C1) Idea critique: given the thesis and the single-signal table, what are the mechanisms and expected signs, and what does BLB predict? (C2) Coding support: review `backtest()`, `select_candidates()` and the `regime()` operator for bugs and design flaws. Does it find E1, E2 and E3 on its own? (C3) Red team on the *sealed* results. (C4) The same P4 prompt as Claude got, for a ChatGPT vs Claude comparison. The result is at least 3 real ChatGPT interactions plus a model-comparison table for Section 3d, which turns the compliance gap into originality. | Compliance, 3d, Originality | Claude prepares, team runs | A ChatGPT account (any member) |
| **WP2** | **Exact as-known data rebuild** (ALFRED vintages for 78 series), validated by reproducing the frozen A0 test scores. All diagnostics then run on as-known data, not revised data. | Execution | Claude | A free FRED API key (2 minutes). Fallback: ALFRED CSV per vintage date, which is slower but needs no key. |
| **WP3** | **Diagnostic layer, "Why it didn't work"** (each item gets a table or figure). D1: single-signal ICs and signs, research vs test, ASOF. D2: IC decay over 1–12 months for each signal, which tests "predict 1, hold 3". D3: demand vs cost channel, sign by horizon, linked to BLB. D4: tightness done properly (T rising vs falling, rolling 60-month terciles, interaction ICs). D5: is the labor signal just industry momentum? (benchmark and orthogonalisation). D6: P&L attribution by industry and by factor, including the Durable mfg / semiconductor story. D7: effective breadth (eigenvalues of the signal correlation; shared CES series). D8: risk-overlay audit (cap binding, ex-ante vs realised volatility). D9: agent-feature autopsy (regime-gated vs ungated, coverage, research→test). D10: human vs LLM-judge confusion matrix. | Thesis, Execution, Originality | Claude | WP2 for the exact versions; D5–D10 can start now |
| **WP4** | **Report rewrite** in the course template with page budgets (§6.3). Sonnet is the main study; Opus goes to 3d and an appendix. A new set of about 12 figures, consistent and print-ready. The ChatGPT log is rebuilt with real transcripts and summaries, plus a worksheet so each member writes their own critique. | All | Claude drafts, team edits | Decisions in §8 |
| **WP5** | **Forward test and Q4 2026 book.** Freeze a v2 specification immediately. Today is 3 Oct, so only two trading days of the holding period have passed; record that in the freeze note. Publish the book for the 30 Sep 2026 decision (held Oct–Dec). Track it live with ETF proxies, because French's October data only arrives in late November. Add a midterm-election note (no political variable; event-risk discussion). | Thesis, Execution ("implementable") | Claude | Decision 5 |
| **WP6** | **A clean analysis package** beside the frozen pipeline: `analysis/` with a single figure and table script and a README. Alex's repo is not modified. Optionally a branch and pull request if Alex agrees. | Execution | Claude | Decision 8 |
| WP7 | *(Optional)* A results page that complements the blueprint artifact: a readable web version of the findings for the team and for the presentation. | Presentation | Claude | Ask |

### 6.3 Proposed report outline (about 9–10 pages plus appendices)

1. **Executive summary** (1 paragraph).
   - Strategy, then "Do not implement" and why, in plain words.
   - Then three things we learned:
     - the labor signal signs, and wage growth;
     - why the design could not test tightness;
     - what the AI agents did well and badly.
2. **What we tried** (about 4.5 pages)
   - 2a *Idea and thesis.* The two channels (demand news vs cost and investment news), with tightness as the moderator. The literature. A hypothesis table with the expected sign of each signal and the reason. A one-figure thesis diagram.
   - 2b *Data.* One table of sources, series, frequency, publication lag and vintage handling. The universe and mapping table with its caveats. A timeline figure showing the research/test split and the T path.
   - 2c *Implementation.*
     - Signal equations and the models table (A0–A4).
     - The portfolio and risk model, as equations: tranches, beta hedge, volatility target, costs.
     - The integrity design in **one** box: vintages, freeze, a single opening.
     - The AI research design, with a figure.
     - Three boxed ChatGPT prompts.
3. **What we learned** (about 4 pages)
   - 3a *Style and risk exposures.* A loadings table and figure, with interpretation (quality and growth tilt; momentum link).
   - 3b *Performance over time.* Full sample, post-2010 and last 18 months, as a table plus a cumulative chart with the momentum benchmark and rolling IC. Mixed windows labelled clearly.
   - 3c *Robustness and limits.* The gate table. Diagnostics D1–D8: why it failed, which signals carry information, horizon, tightness, industry concentration, breadth, the revision gap, costs. Limits.
   - 3d *AI evaluation.* A ChatGPT vs Claude interaction table with our critique. The agent experiment (Q3) result. Judge vs human. "Capability ≠ alpha". What we would change.
4. **Appendices.** Transcripts; the full results tables; code snippets (as-of function, backtest); deviations and amendments; the Opus follow-up; the forward-test specification and Q4 book.

### 6.4 Forward-test (v2) specification: candidates for discussion

These are *hypotheses* drawn from the diagnostics, frozen before new data arrives. They are not findings.
- **Signals.** Keep F1–F5. Add W (wage growth). Let the model learn signs on all data through Aug 2026 instead of imposing priors. Add industry momentum as a control so the labor signal is measured beyond momentum.
- **Tightness.** Replace expanding terciles with a T-rising / T-falling interaction, which is balanced historically.
- **Agent features.** Require a minimum coverage, for example at least 60 research months and active in at least 50% of months. Allow no regime gates without that.
- **Risk.** Either target the volatility the gross cap can actually deliver (about 7%) or document that the cap is the effective constraint.
- **Model.** Widen the ridge grid, or use a sign-constrained, equal-weighted composite. Simpler is better given the CV result.
- **Universe.** Keep the 13 groups, given the time available. Name NAICS-based CRSP baskets as the main extension, since E7 shows the mapping is a first-order problem.

### 6.5 What we will not do

- Reopen or rerun the sealed evaluation, or present any post-hoc variant as if it had passed a holdout.
- Claim W, the layoffs sign flip or anything else in §4.2 as significant.
- Invent ChatGPT transcripts, team critiques or individual contributions.
- Push to Alex's repo without his agreement.

---

## 7. Overnight plan (once the improvements are agreed)

| Step | Output | Gate before the next step |
|---|---|---|
| 1 | Rebuild the as-known panels from ALFRED (WP2) | Must reproduce the frozen A0 test scores and IC exactly. If not, stop and report. |
| 2 | Diagnostics D1–D10 (WP3): tables in `analysis/output/`, figures in `analysis/figures/` | Each number traceable to a script line |
| 3 | v2 specification frozen (hash and timestamp), 30 Sep 2026 book, tracking stub (WP5) | Frozen immediately, disclosing which October trading days were already known |
| 4 | Report v2 draft (Markdown plus PDF or DOCX, whichever you choose), page-budgeted, with the new figure set (WP4) | Checked against the template and rubric |
| 5 | ChatGPT prompt packets and a team-critique worksheet (WP1) | Ready to paste |
| 6 | Morning handover note: what is done, what needs humans, open risks | — |

What I need before starting: answers to §8, especially decisions 1, 2, 5 and 6.

---

## 8. Decisions and questions for you (and for the other chat)

1. **Deadline and deliverables.** The briefing said 27 Sep. What are the "future deliverables": a final report, slides, a presentation? What is the page limit?
2. **ChatGPT.**
   - Will someone ask the professor whether Claude is acceptable?
   - Either way, will the team run the WP1 packets in ChatGPT? I recommend yes: it removes the compliance risk and adds a model comparison.
3. **Main study.** Present the Sonnet study as primary and confirmatory, and Opus as AI-evaluation evidence? I recommend yes.
4. **Post-hoc diagnostics in the report**, clearly labelled? I recommend yes. This is where the thesis and execution marks are.
5. **Forward test and Q4 2026 book.** I recommend yes. It is the only clean holdout left and it matches the meeting's Q4 framing.
6. **FRED API key** for the exact as-known rebuild: free, at https://fredaccount.stlouisfed.org. Without it I use the slower ALFRED CSV route.
7. **Output format.** Markdown plus PDF? Word? A Google Doc for joint editing?
8. **Repo etiquette.** Work locally in `analysis/`, or on a branch of Alex's repo with a pull request?
9. **For Alex.** Was the engineering agent Codex (see §4.1)? Are there any ChatGPT logs from the build?
10. **Team critique.** Who writes which rows of the AI-interaction log? The course grades *our* critique.

---

## Appendix A: Numbers at a glance

| Item | Value | Source |
|---|---|---|
| Selection months / research prediction months / test months | 125 / 88 / 142 | `checkpoints.md`, research ledgers |
| Test window | Nov 2014 to Aug 2026 | `params.py` |
| Primary (Sonnet): Sharpe, IC (t), alpha per month (t) | −0.58; −0.021 (−1.08); −0.38% (−1.86) | `results.json` |
| Primary (Opus): Sharpe, IC (t), alpha per month (t) | +0.01; −0.003 (−0.10); +0.01% (+0.05) | `results.json` |
| Placebo p (Sonnet / Opus) | 0.72 / 0.56 | `results.json` |
| Cost breakeven (Sonnet / Opus) | −32 bp / +11 bp | `results.json` |
| Ridge α, all models | 1000, the grid maximum | `selected_features.json` |
| Months where the gross cap binds | 80–93% | † diagnostics §1 |
| Test months in the expanding-tercile "high" bin | 132 of 141 (my rebuild) / 133 of 142 (study) | † §5 / `report.md` |
| Selected agent features active in the test (Sonnet A3) | 3 of 142 months | † §6 |
| Human vs machine uptake agreement (Opus) | 10/17, with all disagreements machine-yes | `human_review_submission.md` |
| Minimum detectable Sharpe for t ≈ 2 over 142 months | about 0.58 | Blueprint |

## Appendix B: References to verify and cite

- Belo, F., Lin, X., and Bazdresch, S. (2014). "Labor Hiring, Investment, and Stock Return Predictability in the Cross Section." *Journal of Political Economy* 122(1).
- Moskowitz, T., and Grinblatt, M. (1999). "Do Industries Explain Momentum?" *Journal of Finance* 54(4).
- Hong, H., Torous, W., and Valkanov, R. (2007). "Do Industries Lead Stock Markets?" *Journal of Financial Economics* 83(2).
- Kuehn, L.-A., Simutin, M., and Wang, J. (2017). "A Labor Capital Asset Pricing Model." *Journal of Finance* 72(5).
- Donangelo, A., Gourio, F., Kehrig, M., and Palacios, M. (2019). "The Cross-Section of Labor Leverage and Equity Returns." *Journal of Financial Economics* 132(2).
- Zarattini, C., and Antonacci, G. "A Century of Profitable Industry Trends." SSRN 4857230 (course reading).
- Bailey, D., and López de Prado, M. (2014). "The Deflated Sharpe Ratio." *Journal of Portfolio Management* (already used in the pipeline).
