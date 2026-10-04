# 230GA · Follow the Workers — build-and-run prompt

> **How to use this file.** Paste the whole file as the first message of a session with a model that can write and run code and reach the internet (for example Claude Code on your laptop), at the highest reasoning-effort setting available. Set `FRED_API_KEY` and `OPENAI_API_KEY` first. The model builds the codebase and runs Stages 0 to 9 in order in one go. It stops early only if a required key is missing.
>
> Team: Romain Almeida, Elouan Bahri, Piero Pelosi, Alex Roesler, Al Yazid Bensaid · UC Berkeley MFE · course 230GA · blueprint v4.

---

## 0. Your role

You are the lead research engineer for a five-person MFE team. In this session you will build, run and document the pre-registered research pipeline specified below, end to end, and deliver results, figures, logs and a draft report.

You are **the engineer, not the researcher**:

- Implement this specification exactly. Do not invent features, do not tune any parameter after seeing a result, and never look at sealed-period returns before the freeze in Stage 7.
- When reality forces a deviation (a series is missing, an API changed, a field has another name), first write it to `outputs/deviations.md` with the reason and a UTC timestamp, then choose the most conservative option and continue. Never make a deviation whose reason depends on performance.
- Do not ask the user questions. The only reason to stop early is a missing required API key (Section 3).
- After every stage, append a short plain-English status to `outputs/checkpoints.md` so a person can follow the run without reading code.
- Work carefully and verify as you go: this is a long task where one silent look-ahead bug invalidates everything. Prefer an explicit assert over an assumption.

---

## 1. The project

We test whether public labor-market data by industry predicts which US industries outperform. Every month, for 13 industry groups, we measure how job openings, hires, quits, layoffs, weekly hours and pay changed over the past year, exactly as those numbers were known on the decision date. We rank the groups, go long the top 3 and short the bottom 3, and hold each position 3 months through three overlapping monthly tranches. National labor tightness `T = log(job openings / unemployed)` is recorded as a conditioning variable.

Blinded ChatGPT research agents propose additional features on the research period only, in two architectures with equal budgets: three **island** agents that exchange short findings, and three **independent** agents that do not. A fixed evaluator scores everything. All choices are frozen, then the sealed test period is opened exactly once.

The report answers three questions:

| | Question | Where it is answered |
|---|---|---|
| **Q1** | Does public labor information predict industry returns? | Sealed test: A1 vs A0 and the gate. Judged on the **main effect**. |
| **Q2** | Do company-level recruiting and layoff data add to it? | Sealed test: A2 vs A1, only if the company data pass the Stage 1 gate. |
| **Q3** | Do agents that share findings **search better** than agents that do not? | **Research period**, with process metrics and dispersion across 3 seeds per arm. The sealed A4 vs A3 comparison is a single draw (one base algorithm, one opening of the seal) and is reported descriptively, never as a test. |

**Horizon.** The model target is the 1-month-ahead relative return, because that is where the data has enough independent observations to test honestly: about 142 sealed months if the sealed start S\* is October 2014, versus 47 non-overlapping 3-month periods and 23 non-overlapping 6-month periods. Positions are held 3 months through tranches. 3- and 6-month results are reported with overlap-robust errors and never decide anything.

**Expected outcome (pre-registered).** Given about 142 sealed months and a five-part gate, "Do not implement" is the expected outcome. The report is built so that three things carry the contribution whatever the verdict: the research-versus-sealed performance gap, the number of candidates that pass in research and fail in the sealed test, and the comparison of the two search architectures.

---

## 2. Non-negotiable rules

| # | Rule |
|---|---|
| R1 | **No look-ahead.** A value used at decision date `d` must have been published on or before `d − 1 day`. Primary results use ALFRED vintages. Today's revised values never enter primary results. |
| R2 | **Sealed test.** Returns after the research period are loaded only inside `final_evaluation()`. It refuses to run unless `outputs/FREEZE.json` exists and the SHA-256 of `params.py`, `data.py`, `stats.py`, `agents.py` and `outputs/selected_features.json` matches. It runs once. A rerun needs a written reason appended to `outputs/reruns.log`, and both results are reported. |
| R3 | **No tuning on results.** Every parameter lives in `params.py`, hashed at Stage 0 (`prereg_v0.json`) and at Stage 7 (`FREEZE.json`). Changes in between are allowed only for reasons unrelated to performance and are listed in `deviations.md`. |
| R4 | **Blinding.** Research agents never see company names, tickers, industry names, calendar dates, vendor names, series IDs, raw values, the data panel or this prompt. They see only an anonymized variable dictionary, anonymous group labels, a time index, the grammar and rounded research-period summaries. Call them through the OpenAI API with **no tools** (no browsing, no code execution). That is the security boundary, not a sentence in a prompt. |
| R5 | **Log everything.** Every download, every candidate (invalid ones included), every migration report, every model fit, every figure. Delete nothing. |
| R6 | **Small codebase.** Exactly these files: `params.py`, `data.py`, `stats.py`, `plots.py`, `agents.py`, `run.ipynb` (Section 4). No classes unless unavoidable, no frameworks, no test suite: inline asserts. |
| R7 | **Honest reporting.** Report every prespecified metric even when it is bad. State sample sizes, effective cross-sectional width and limits. |
| R8 | **Time-box the company data.** If LinkUp or WARN access is not working within 3 hours of wall time in Stage 1, drop it and A2 without further discussion (team decision). The evaluator and the as-of panels are what everything else waits on. |
| R9 | **No scope creep.** Do not build CRSP stock baskets or any other universe in this run. Name NAICS-based CRSP baskets as the recommended follow-up in the report's limits section. |

---

## 3. Environment

- Python 3.11 or later.
  `pip install pandas numpy scipy statsmodels scikit-learn matplotlib fredapi requests openai pyyaml pyarrow duckdb`
  Optional: `wrds`, `deweypy`, `lightgbm`.
- Environment variables:

| Variable | Required | Notes |
|---|---|---|
| `FRED_API_KEY` | yes | Free account at https://fredaccount.stlouisfed.org |
| `OPENAI_API_KEY` | yes for Stage 5, P1, P4 | The research agents are ChatGPT models; this also satisfies the course's ChatGPT requirement. |
| `OPENAI_MODEL` | no | Default `gpt-5`. Record the exact model id the API returns in every log line. |
| `WRDS_USERNAME` | no | Password via `~/.pgpass`. Needed only for Revelio WARN. |
| `DEWEY_API_KEY`, `DEWEY_PROJECT_ID` | no | Needed only for LinkUp. |

- If `FRED_API_KEY` is missing: stop and ask for it.
- If `OPENAI_API_KEY` is missing: run Stages 0 to 4 and 6, write every agent's first prompt to `outputs/agents/manual/` with paste instructions for ChatGPT, and stop before Stage 5.
- FRED allows 120 requests per minute: sleep 0.6 s between calls and cache every raw response under `data/cache/`.
- Seed every random process with 230.

---

## 4. Repository layout

| File | Contents |
|---|---|
| `params.py` | Every constant in this prompt, plus the pre-registration statements of Section 5 verbatim as `PREREG_NOTES`. |
| `data.py` | Downloads, vintage audit, as-of panels, crosswalk, features, returns, portfolio construction and backtest. |
| `stats.py` | Rank IC, Newey-West, stationary bootstrap, blocked ridge CV, reality check, deflated Sharpe, circular-shift placebo, factor regressions, process metrics. |
| `plots.py` | Every figure. |
| `agents.py` | Blinding, grammar parser, agent orchestration (both arms, all seeds), migration tracing, logging. |
| `run.ipynb` | Orchestrates Stages 0 to 9, with a short markdown cell before each stage explaining it. |
| `outputs/` | Manifest, panels, logs, candidates, freeze files, final results, figures, checkpoints, deviations. |
| `report/` | `report.md` and `chatgpt_log.md`. |

---

## 5. Stage 0 — Pre-registration (before any return file is read)

1. Write `params.py` with every constant in this prompt: dates, universe, series IDs, feature formulas, windows, thresholds, grammar, budgets, seeds, costs, comparison family, gate.
2. Include these statements verbatim in `PREREG_NOTES`:
   - **Tightness is extrapolated.** "V/U stays below 1 (T below 0) throughout the research period. Any feature × T interaction is therefore estimated outside the support observed in research and applied to a test period containing the 2021–23 tight regime. Q1 is judged on the main effect. The interaction model and the V/U above-versus-below-1 split are reported as descriptive, not as tests."
   - **Sealed boundary.** "The research/sealed boundary stays at S\*. Moving it earlier to capture tight-regime variation in research costs power where power is scarce: about 142 sealed months need an annualized Sharpe near 0.58 for t ≈ 2, 92 months about 0.72, 68 months about 0.84. No split solves both problems; this is a limitation of the data, not a design error."
   - **Seeds.** "Each agent arm is run with three seeds. Seed 1 is the only strategy-producing run: only its candidates may supply features to A3 and A4. Seeds 2 and 3 measure search behaviour and never enter selection."
   - **Trial count.** "The deflated Sharpe ratio and the reality check use the 36 candidates of seed 1 plus the strategies evaluated in research. Process-measurement seeds are excluded, since none of their candidates is eligible for selection."
   - **Comparison family.** "Holm correction applies to A1 vs A0, A2 vs A1 (if admitted) and A3 vs its base. A4 vs A3 is reported with its interval, outside the family, as descriptive."
   - **Expected outcome.** The paragraph in Section 1.
3. Save `outputs/prereg_v0.json` with the SHA-256 of `params.py` and a UTC timestamp.

---

## 6. Stage 1 — Download and audit (`outputs/manifest.csv`)

### 6.1 Returns and factors (Ken French, free)

| File | URL | Use |
|---|---|---|
| 49 industry portfolios | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip | Sections "Average Value Weighted Returns -- Monthly", "Number of Firms in Portfolios", "Average Firm Size" |
| Fama-French 5 factors | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip | Mkt-RF, SMB, HML, RMW, CMA, RF |
| Momentum | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip | Mom |
| Definitions | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes49.zip | Manifest documentation |
| SIC→NAICS concordance | https://www.census.gov/naics/concordances/1987_SIC_to_2002_NAICS.xls | Crosswalk check |

- Values are percent; `-99.99` and `-999` mean missing.
- Portfolio market cap = number of firms × average firm size, from the prior month.
- Group return = value-weighted mean of member portfolio returns using prior-month caps.
- Excess return = group return − RF. **Model target** = relative return = excess return minus the cross-sectional mean of the 13 groups that month.

### 6.2 Universe (fixed: do not add, split or merge)

| G | Group | JOLTS code | French members | CES code | Match |
|---|---|---|---|---|---|
| 1 | Mining and logging | 110099 | Gold Mines Coal Oil | 10000000 | exact |
| 2 | Construction | 2300 | Cnstr | 20000000 | exact |
| 3 | Durable manufacturing | 3200 | Toys BldMt Steel FabPr Mach ElcEq Autos Aero Ships Guns Hardw Chips LabEq MedEq | 31000000 | exact |
| 4 | Nondurable manufacturing | 3400 | Food Soda Beer Smoke Hshld Clths Drugs Chems Rubbr Txtls Paper | 32000000 | exact (Hshld approximate) |
| 5 | Wholesale trade | 4200 | Whlsl | 41420000 | exact |
| 6 | Retail trade | 4400 | Rtail | 42000000 | exact |
| 7 | Transportation, warehousing and utilities | 480099 | Trans Util | 43000000 | approximate (CES covers transportation and warehousing only) |
| 8 | Information | 5100 | Telcm | 50000000 | exact |
| 9 | Finance and insurance | 5200 | Banks Insur Fin | 55000000 | approximate (CES financial activities) |
| 10 | Real estate and rental and leasing | 5300 | RlEst | 55000000 | approximate (same CES series as group 9) |
| 11 | Professional and business services | 540099 | BusSv | 60000000 | exact |
| 12 | Health care and social assistance | 6200 | Hlth | 65000000 | approximate (CES private education and health) |
| 13 | Accommodation and food services | 7200 | Meals | 70000000 | approximate (CES leisure and hospitality) |

- Excluded French portfolios, with reasons recorded in the manifest: Agric (outside JOLTS nonfarm), Other, Boxes, Books, Softw, Fun, PerSv (SIC spans two NAICS sectors).
- Every strategy uses this same universe.
- Groups 9 and 10 share CES series and several groups use approximate supersectors, so the effective cross-sectional width is closer to 8–9 than 13. Never count shared series as independent evidence, and state this in the report.

### 6.3 JOLTS rates (FRED, not seasonally adjusted, monthly from December 2000)

- Series ID = `JTU` + JOLTS code + measure, with measure ∈ {`JOR` job openings rate, `HIR` hires rate, `QUR` quits rate, `LDR` layoffs and discharges rate}. Example: https://fred.stlouisfed.org/series/JTU480099JOR. All 52 IDs are listed in FRED's JOLTS release tables.
- Use NSA for every group because FRED carries seasonally adjusted JOLTS for only some industries. Every feature is a year-over-year change, which removes seasonality without seasonal-factor revisions.
- Tightness: `JTSJOL` (job openings, total nonfarm, SA, thousands) and `UNEMPLOY` (unemployment level, SA, thousands).

### 6.4 CES hours and earnings (FRED, production and nonsupervisory employees)

- Hours = `CEU` + CES code + `07`. Earnings = `CEU` + CES code + `08`.
- Exception: construction earnings = `CES2000000008` (seasonally adjusted; the NSA series is not on FRED; year-over-year changes make this acceptable). Note it in the manifest.

### 6.5 Output prices for F6 (optional)

Search FRED (API `fred/series/search`) for "Producer Price Index by Industry" series whose NAICS scope equals the group's JOLTS industry. Accept only exact scope matches (`PCUOMFGOMFG`, total manufacturing, is **not** a match for group 3 or 4 alone). Record the candidates and the decision per group. F6 enters models only if at least 9 of 13 groups have an accepted match with vintages; otherwise F6 is a diagnostic only.

### 6.6 Vintage audit and S\*

- For every series call `https://api.stlouisfed.org/fred/series/vintagedates` and store the first vintage date. Sanity values: `JTS2300JOR` first vintage 2010-08-11; `JTS3200JOR` 2014-10-07.
- A series is admitted if its first vintage is on or before 2015-06-30. A measure (for example `QUR`) is admitted if at least 11 of 13 groups have it admitted. A group missing an admitted measure gets 0 for that feature after cross-sectional standardization, flagged.
- **S\*** = the latest first-vintage date among admitted series. The first sealed decision is the last trading day of the month containing S\*.
- If fewer than 3 JOLTS measures are admitted, the primary switches to the FIXEDLAG variant (Stage 2) and every final result is labeled "pseudo-real-time".
- Before Stage 2, write to `checkpoints.md`: S\*, the number of research and sealed months, the non-overlapping counts at 1, 3 and 6 months, and the minimum detectable annualized Sharpe (`2 / sqrt(sealed years)`).

### 6.7 Company-level data gate (skip cleanly if access fails; see R8)

**LinkUp via Dewey** (https://www.deweydata.io/data-partners/linkup; `pip install deweypy`). Use raw postings with `created` (first observed), `delete_date`, `last_checked`, `company_id`, `ticker_symbol`, `naics_code` and the point-in-time company reference. Admit **Tier 1** (new-posting flows by `created`) only if all hold:

- records from 2008 with `created` timestamps;
- the `company_id` → ticker and NAICS mapping is point-in-time;
- scrape logs or coverage fields separate collection failures from inactivity;
- at least 20 cohort companies per group-month in at least 10 of 13 groups.

**Tier 2** (active postings, ages, removals, reappearances) is admitted only if historical snapshots exist, because postings can disappear and reappear. If raw data exceed 50 GB or 6 hours of processing, use Dewey's LinkUp company analytics only if their documentation confirms counts by first-observed date.

**WARN notices via WRDS**, schema `revelio_layoffs` (fields `notice_date`, `layoff_date`, `num_employees`, `state`, `rcid`). Map `rcid` to NAICS and public identifiers through Revelio's company reference tables. Information date = `notice_date` + 30 days unless a verified collection date exists. Treat amendments as versions of one event. Admit if the mapping covers at least 10 of 13 groups from 2008.

If any check fails, record why and continue with the public pipeline. Never substitute scraped current state WARN lists; they are not historical.

### 6.8 Manifest and P1

- Manifest: one row per series or dataset with source, ID or table, URL, group, measure, frequency, observation start and end, first vintage, admitted (yes/no), reason, mapping quality, flags.
- **P1 — ChatGPT data audit and coding.** Send ChatGPT (API, no tools) the manifest, the crosswalk table and the source code of your as-of function, with this prompt:

```text
Find mapping errors, timestamp or look-ahead errors, and code bugs in the material below.
For each problem, give the exact line or row, why it is wrong, and a test that would confirm it.
Do not report style issues.
```

Test every claim. Fix confirmed ones before Stage 2. Log the prompt, a summary of the output, what was wrong and what changed.

---

## 7. Stage 2 — As-of panels (`outputs/panel_asof.parquet` and variants)

- **Decision dates** `d`: the last trading day of each month. **Information cutoff**: `realtime_start ≤ d − 1 calendar day`.
- **Method**: `fredapi.get_series_all_releases` once per series; for each `d` and observation month `m`, take the value with the latest `realtime_start` at or before the cutoff (`pandas.merge_asof`).
- **Variants** from the same code path:

| Variant | Definition | Role |
|---|---|---|
| ASOF | Latest value known at `d` | Primary |
| FIRST | First release only (`get_series_first_release`) | Robustness |
| REVISED | Today's values | Hindsight diagnostic only |
| FIXEDLAG | Today's values; JOLTS months ≤ `d − 2`, CES and CPS months ≤ `d − 1` | Sensitivity |

- **Research period** (decisions before S\*): vintages do not exist, so use the vintage as of S\* with the FIXEDLAG availability rule. No revision published after S\* can reach the research period. Label it pseudo-real-time.
- **Periods** (returns are earned in month `d + 1`):
  - Research: first decision at the end of April 2004 through the last decision before S\*.
  - Sealed test: decisions from S\* through the latest month with French returns.
  - Last 18 months: the final 18 return months of the sealed test.
- **Checks**: assert that no row at `d` contains an observation month later than allowed. Write 5 random (series, `d`, value) triples to `checkpoints.md` for the team to verify by hand on the ALFRED website.

---

## 8. Stage 3 — Features (`outputs/features.parquet`)

Notation: `avg3(X, m)` = mean of `X(m)`, `X(m−1)`, `X(m−2)`. `m_J` = latest JOLTS month available at `d`; `m_C` = latest CES month available at `d`.

```text
F1 openings    = avg3(JOR, m_J) − avg3(JOR, m_J − 12)
F2 hires       = avg3(HIR, m_J) − avg3(HIR, m_J − 12)
F3 quits       = avg3(QUR, m_J) − avg3(QUR, m_J − 12)
F4 layoffs     = avg3(LDR, m_J) − avg3(LDR, m_J − 12)
F5 hours       = log avg3(H, m_C) − log avg3(H, m_C − 12)
F6 wage–price  = [log avg3(E, m_C) − log avg3(E, m_C − 12)] − [log avg3(P) − log avg3(P, −12)]   (only if admitted)
T              = log(JTSJOL / UNEMPLOY) at the latest month available for both at d (matched reference month)
A0 fixed rule  = mean(z1, z2, −z4, z5)   (no fitting; signs set by economics before any data)
```

- `T` is common to all groups: on its own it cannot rank them; it acts only through interactions, and every interaction is extrapolated (Section 5).
- **Standardization** at each `d`: divide each feature by its own group's expanding standard deviation (at least 24 observations, as-of `d`), then z-score across the 13 groups, winsorize at ±3, set missing to 0 (flagged).

**Company-level features** (only if admitted). Cohort at `d`: companies with at least 24 months of scrape history before `d` and no collection-failure flag. Compute company-level quantities first, then aggregate within group:

```text
N_i(m)  = postings of company i with created in month m;  Nbar_i = 3-month mean
H1 new-posting growth   = log( Σ_i Nbar_i(m) / Σ_i Nbar_i(m−12) )
H2 breadth              = share of cohort companies with Nbar_i(m) > Nbar_i(m−12)
H3 concentration        = share of Σ_i |ΔNbar_i| from the 5 largest contributors
W_i                     = 1 if company i has a WARN event with information date in (d − 3 months, d]
H4 notice intensity     = YoY change of Σ num_employees over the last 3 months / group employment (CEU + CES code + "01", as-of d)
H5 retrenchment         = mean_i [ W_i × 1(Nbar_i(m) < Nbar_i(m−12)) ]    (product per company, then average)
H6 reallocation         = mean_i [ W_i × 1(Nbar_i(m) > Nbar_i(m−12)) ]
H7 public–private gap   = z(H1) − z(F1), same reference month m_J
H7L leading version     = same with LinkUp's latest month (a separate feature; never mix with H7)
```

Save `(d, group, feature, value, variant, flags)`.

---

## 9. Stage 4 — Blinding (`outputs/blind_map.json` stays local and secret)

- Map variables to `V01…Vk`, groups to `G01…G13` in random order (seed 230), research decision dates to `t = 1…n`.
- The variable dictionary sent to agents lists, per variable: id, type (rate in percent of employment, hours, dollars per hour, count, share or index), stock or flow, monthly frequency, availability lag in months, coverage share, and whether it is common to all groups. Nothing else.
- Use the same blind map for every arm and every seed.

---

## 10. Stage 6 — Evaluator and portfolio (build and unit-test BEFORE Stage 5)

**Target and metrics.** Next-month relative return of each group. Per month: Spearman rank IC between score and target, and the long–short return.

**Models** (identical machinery for every strategy):

| Name | Features | Role |
|---|---|---|
| A0 | Fixed rule of Stage 3 | Benchmark, no fitting |
| A1 | Ridge on standardized main effects F1–F5 (+F6 if admitted) | Public model; Q1 |
| A1-T | A1 plus each feature × T | Descriptive only (extrapolated) |
| A2 | A1 plus admitted company-level features | Q2, overlap sample |
| A5 | LightGBM, `max_depth=2`, 200 trees, `learning_rate=0.03`, A1's features | Optional comparator, not tuned |

- Ridge is refit every month on an expanding window starting with the first research decision; first prediction after 36 months.
- The ridge penalty is chosen once on the research period by 5-fold blocked cross-validation (contiguous folds, 1-month purge) over `logspace(-2, 3, 11)`, then frozen.

**Portfolio** (identical for every strategy):

- Each month rank groups by score. New tranche: long the top 3, short the bottom 3, equal weight within legs, dollar-neutral. Book = average of the three most recent tranches (3-month holding). Sensitivities: 1-month and 6-month holding.
- Beta: each group's beta to Mkt-RF from the prior 60 months (at least 36). Hedge the book's ex-ante beta to zero with a Mkt-RF position.
- Volatility target 10% annualized using a Ledoit-Wolf covariance of group returns over the prior 60 months. Gross leverage cap 2.0 (sum of absolute weights). If the cap binds, accept lower volatility.
- Costs: `cost_t = c × Σ_g |w_target − w_pretrade|`, with pretrade weights after drift; `c` = 10 bp base, 0 and 25 bp sensitivities; no double counting. Hedge trades cost 2 bp. Borrow and financing reported separately (0 base, 25 bp per year sensitivity).
- Long-only version: equal-weight the top 3 groups against an equal-weight 13-group benchmark; report active return, tracking error and information ratio.

**Feedback returned to agents** (research period only, rounded to 2 decimals):

- coverage, mean IC, Newey-West t (6 lags);
- IC when T is in its lower versus upper expanding tercile (kept deliberately: it is not a selection criterion; note in the report that agents observed the thesis variable during search);
- maximum absolute correlation with the base features, rank autocorrelation, validity status.

**Never return the IC in each half of the research period.** Stage 7 selects on it; an agent that saw it could target it across six submissions.

**Unit check.** Before Stage 5, run the evaluator on a synthetic signal with a known IC and record the check in `checkpoints.md`.

---

## 11. Stage 5 — Agent research (research period only)

### 11.1 Design

| | Islands | Independent (control) |
|---|---|---|
| Agents | 3: Temporal, Composition, Interactions | 3: same emphases |
| Submissions per agent | 6 | 6 |
| Migration | After submissions 2 and 4, each island writes a ≤ 120-word report, including at least one failure, sent to the other two. Findings only: no specs, no formulas, no code. | None |
| Seeds | 3 (seed 1 strategy-producing; seeds 2–3 process only) | 3 (same) |
| Candidates per seed | 18 | 18 |

- Emphases: **Temporal** (changes, persistence, acceleration, recovery), **Composition** (breadth, concentration, dispersion across variables), **Interactions** (events, continuous regimes, disagreement between variables).
- Same model, same temperature (0.7 where supported), same starting prompts, same evaluator for every arm and seed. Pass the API `seed` parameter as 230 + seed number where supported, and record whether it was honoured.
- **Seed 1 is the only strategy-producing run.** Only its 36 candidates (18 per arm) are eligible for Stage 7. Seeds 2 and 3 measure search behaviour and never enter selection or the trial count.
- Invalid or unparseable submissions count against the budget. One retry is allowed for JSON syntax only; log both attempts.
- You, the engineer, must not propose, edit or rank features.

### 11.2 Submission format and grammar

Each submission is JSON only:

```json
{"name": "...", "hypothesis": "≤ 40 words", "falsified_if": "≤ 30 words", "expression": "..."}
```

Allowed operations (the parser rejects anything else, and any negative lag):

```text
lag(x,k)        k ∈ {1,2,3,6,12}
mavg(x,w)       w ∈ {3,6,12}
chg(x,k)        lchg(x,k)        yoy(x)
accel(x)        = chg(chg(x,3),3)
persist(x,k)    = share of the last k months with chg(x,1) > 0,  k ∈ {3,6}
tsz(x,w)        w ∈ {36, 60, "exp"}
csrank(x)       ratio(x,y)       spread(x,y) = z(x) − z(y)       mult(x,y)
withT(x)        = x × T
regime(x, s)    = x × 1(T in its lower or upper expanding tercile),  s ∈ {"low","high"}
Limits: at most 3 nested operations; at most 2 base variables plus T.
```

### 11.3 Prompts (use verbatim; fill the braces)

System prompt:

```text
You are a quantitative researcher. You will propose one feature per turn to predict which of {n} anonymous groups (G01 to G{n}) will have higher returns next month relative to the others. You see only the variable dictionary below, the allowed operations, and summary statistics of your previous submissions. You do not know what the groups, variables or time periods are. Do not guess them and do not use knowledge about any real industry, company or date.
Starting emphasis: {emphasis}.
Rules: return only JSON with keys name, hypothesis, falsified_if, expression; use only the allowed operations; state a hypothesis that the statistics could falsify.
Variable dictionary: {dictionary}
Allowed operations: {grammar}
```

Turn prompt:

```text
Submission {i} of 6. Your previous submissions and their development statistics: {history}.
{migration_reports}   ← islands only; empty for independent agents
Propose your next feature.
```

Migration prompt (islands, after submissions 2 and 4):

```text
In at most 120 words, report to the other researchers what you learned so far, including at least one thing that failed. Do not include formulas.
```

### 11.4 Process metrics for Q3 (pre-specified; computed per arm and seed)

| Metric | Definition |
|---|---|
| Best-so-far IC curve | For submission index i = 1…6, the best research-period mean IC among the arm's valid candidates submitted up to i |
| Median IC | Median research-period mean IC of the arm's valid candidates |
| Invalid rate | Share of submissions that failed parsing or validation |
| Diversity | 1 − mean pairwise Jaccard similarity of the candidates' token sets (operations + base variables) |

Q3 is answered on these metrics: arm means with the range across the 3 seeds, and whether the between-arm gap exceeds the between-seed range. The seeds give error bars on the search process only. They add no power on the sealed window (every seed would face the same 142 months), so they are never pooled into a sealed test.

### 11.5 Migration tracing

Trace every migration report forward (all seeds; seed 1 reported first):

1. Split the report into numbered claims.
2. For each later submission by the two receiving islands, ask a separate ChatGPT judge call (no tools) whether the submission uses or tests any claim. Input: the report and the submission's hypothesis and expression. Output JSON: `{"uses_claim": true|false, "claim_ids": [...]}`.
3. The team spot-checks 20% of the judgments; record agreement.
4. Report the uptake rate, and whether submissions that use a claim score better than the receiving island's own earlier best, compared with submissions that do not. Also record whether reported failures were avoided.

### 11.6 Logging

Log every call to `outputs/agents/log.jsonl`: arm, seed, agent, submission index, prompt, raw response, parsed spec, validity, evaluator feedback, tokens, model id, timestamp. Save the full library to `outputs/candidates.csv` with a `seed` column. Before Stage 7, grep the log to prove that no prompt contains a date, industry name, ticker or series ID, and record the result.

**P2** (blind hypothesis generation) = the first submissions of seed 1. **P3** (migration) = the seed-1 migration reports and their tracing.

---

## 12. Stage 7 — Selection, red team, freeze

**Selection rule per architecture** (seed 1 only; fixed): keep candidates with research-period Newey-West t ≥ 1.5, same-sign IC in both halves of the research period, and maximum absolute correlation below 0.8 with the base features and already-selected candidates. Take up to 3 by t. If none qualify, the architecture's strategy equals its base.

**Final strategy list** (no others):

| Strategy | Definition |
|---|---|
| A0 | Fixed rule (public) |
| A1 | Public ridge, main effects |
| A1-T | A1 + feature × T (descriptive) |
| A2 | A1 + admitted company-level features (only if admitted; overlap sample) |
| A3 | Base (A2 if admitted, else A1) + independent-arm features from seed 1 |
| A4 | Same base + island-arm features from seed 1 |
| A5 | Optional LightGBM comparator |

**Research-period multiple testing.** Stationary-bootstrap reality check (mean block 6 months, 5,000 draws) of the best candidate against the 36 seed-1 candidates; deflated Sharpe ratio for each strategy using the count of seed-1 candidates plus strategies evaluated in research. Seeds 2 and 3 are excluded from both.

**Primary strategy** for the implementation decision = the strategy among A0 to A4 with the highest research-period net Sharpe after costs (ties go to the simpler one). Record it now.

**P4 — ChatGPT red team** (API, no tools). Send the research-period tables (no dates, no names) with this prompt:

```text
Give 10 distinct reasons these results could be spurious, ranked by likelihood.
For each, name a test that can be run with this data and the result that would make us say "do not implement".
```

Add the specific, runnable tests to the prespecified diagnostics. Log accepted and rejected ones with reasons.

**Freeze.** Write `outputs/selected_features.json`, then `outputs/FREEZE.json` with the SHA-256 of `params.py`, `data.py`, `stats.py`, `agents.py` and `selected_features.json`, plus the UTC time. Nothing changes after this.

---

## 13. Stage 8 — Sealed final evaluation (run once)

Run every strategy of Stage 7 on the sealed period with the ASOF variant. For each, report:

- mean IC and Newey-West t at horizons 1, 3 and 6 months (overlapping horizons use h + 5 lags);
- gross and net long–short return, volatility, Sharpe, maximum drawdown, turnover, hit rate;
- long-only active return, tracking error and information ratio.

**Paired comparisons** (one-sided; stationary bootstrap, mean block 6 months, 5,000 draws; metrics: difference in mean IC and in net long–short return):

| Comparison | Status |
|---|---|
| A1 vs A0 | Test, Holm family |
| A2 vs A1 (overlap sample) | Test, Holm family, only if admitted |
| A3 vs its base | Test, Holm family |
| A4 vs A3 | **Descriptive**: report the interval; outside the Holm family |
| A1-T vs A1, V/U above vs below 1 | **Descriptive**: extrapolated tightness |

**Placebo.** Circular time shift of the frozen feature panel against returns, for every shift from 24 months to (number of sealed months − 24). p-value = share of shifted mean ICs at or above the actual one.

**Attribution.** Regress net long–short returns on Mkt-RF, SMB, HML, RMW, CMA, Mom and a group-momentum long–short (12-1 momentum of the 13 groups, top 3 minus bottom 3), Newey-West with 6 lags.

**Windows.** Whole sealed period; first and second half; excluding March–December 2020; last 18 months; T terciles.

**Variants.** FIRST, REVISED, FIXEDLAG. Report the as-known minus revised gap.

**Course windows** (label clearly): "post-2010" = January 2010 onward, pseudo-real-time before S\* and as-known after; "full" = May 2004 onward, same labeling.

**Drop-one-group.** Recompute with each group removed; flag any group contributing more than 50% of cumulative profit.

**Research-versus-sealed accounting.** For every seed-1 candidate and every strategy, the research-period statistic next to its sealed statistic; count the candidates that pass the Stage 7 filter in research and fail in the sealed test.

**Implementation.** Cost breakeven (the cost that sets net Sharpe to 0), turnover, capacity notes, and candidate ETF proxies per group (for example ITB or XHB construction, XRT retail, IYT transportation, XLU utilities, XLF, KBE or KIE financials, IYR real estate, PEJ leisure). Verify each exists, and state that French portfolios are research series, not tradable.

---

## 14. Stage 9 — Gate, decode, figures, report

**Gate.** Implement only if every criterion holds for the primary strategy on the sealed period:

| | Criterion |
|---|---|
| G1 | Timing: primary results use ASOF data and no audit flag is open. |
| G2 | Prediction: mean 1-month IC above 0 with Newey-West t ≥ 2.0. |
| G3 | Incremental: net long–short alpha after the attribution factors above 0 with Newey-West t ≥ 2.0. |
| G4 | Robust: positive mean IC in both halves; placebo p < 0.05; no single group above 50% of cumulative profit. |
| G5 | Implementable: net Sharpe above 0 at 25 bp; turnover and capacity documented. |

Otherwise write **"Do not implement"** and name the failed criteria. Always add the power statement: with about 142 sealed months, only an annualized Sharpe near 0.6 or higher reaches t ≈ 2, so a null result does not rule out a smaller effect. Recall that "Do not implement" was the expected outcome, and lead with what the study learned.

**Decode.** Only now open `blind_map.json` to interpret the selected features in economic terms. Nothing from this step goes back into selection.

**Figures** (`outputs/figures/`, from `plots.py`):

1. Pipeline diagram.
2. Sample-split timeline (research, S\*, sealed test, last 18 months).
3. Cumulative net long–short for every strategy.
4. IC by horizon with confidence intervals.
5. IC by T tercile.
6. As-known versus revised gap.
7. Placebo distribution.
8. Best-so-far IC curves by submission, islands versus independent, with the range across seeds.
9. Migration uptake and its effect on scores.
10. Research-versus-sealed scatter for all seed-1 candidates.
11. Factor loadings.
12. Drawdowns.

**Report** (`report/report.md`), in the course template:

1. Executive summary (one paragraph, verdict first)
2. What did you try: 2a Ideas; 2b Data (manifest summary, links, admission decisions); 2c Implementation (risk model, turnover and costs, ChatGPT prompts)
3. What did you learn: 3a Style and risk exposures; 3b Time patterns (full, post-2010, last 18 months); 3c Robustness and limits (effective width of 8–9 groups, extrapolated tightness, power, NAICS CRSP baskets as the recommended follow-up); 3d ChatGPT evaluation (P1–P4, Q3 process metrics, migration tracing)
4. Appendices (logs, tables, code snippets)

**ChatGPT log** (`report/chatgpt_log.md`): for P1, P2, P3 and P4, four fields (prompt, output summary, what was wrong, what we changed) plus a column "Team critique" left empty for the students.

---

## 15. Final checklist before you stop

- [ ] `prereg_v0.json` and `FREEZE.json` exist; `final_evaluation()` ran exactly once, or `reruns.log` explains why.
- [ ] The agent-log grep found no date, industry name, ticker or series ID.
- [ ] Only seed-1 candidates reached Stage 7 and the trial count.
- [ ] Agents never received the half-sample IC.
- [ ] Every number in the report comes from a saved file in `outputs/`.
- [ ] `deviations.md` lists every departure from this prompt, each with its reason.
- [ ] `run.ipynb` runs top to bottom from an empty cache.
- [ ] `checkpoints.md` ends with the verdict, the open limitations and the exact commands to reproduce the run.
