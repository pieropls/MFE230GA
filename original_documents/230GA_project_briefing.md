# 230GA Final Project: Catch-Up Briefing

*Prepared Saturday 26 Sep 2026 for Al. Sources: the team chat (13 to 24 Sep), the project artifact "230GA - Project" (blueprint v4, dated 24 Sep), the build-and-run prompt (`230GA_build-and-run_prompt.md`) and the course assignment sheet.*

**Team:** Romain Almeida, Elouan Bahri, Piero Pelosi, Alex Roesler, Al Yazid Bensaid.

---

## 0. The 60-second version

- **The assignment.** Design and test an active investment strategy. Use ChatGPT as a research assistant along the way. Write a group report in the course template.
- **Our strategy: "Follow the Workers."** Every month we look at public labor data for 13 US industry groups: job openings, hires, quits, layoffs, weekly hours, wages. We rank the groups. We go long the top 3, short the bottom 3, and hold each position 3 months.
- **The ChatGPT twist.** Blinded ChatGPT "agents" propose extra signals without knowing what the data is. We compare two setups: agents that share notes ("islands") and agents that work alone ("independent").
- **The discipline.** Every rule is written down and locked (hashed) before we look at test results. The test period (Nov 2014 to Aug 2026) is opened once.
- **Expected answer: "Do not implement."** We said so in advance. The grade comes from rigor and what we learn, not from finding alpha.
- **Where we are.** The plan is finished (Piero's artifact + the prompt file). At the last chat message (Thu 24 Sep, about 5 PM): the code had not been run, nobody had an OpenAI API key, and the work split had not been sent.
- **Deadline.** Sunday 27 Sep (tomorrow), per Romain. Confirm on bCourses.
- **Your open item.** Piero asked you or Elouan to download all the data into one zip and email it to the team. Elouan replied. Check who is doing it.

---

## 1. What the professor asks for

### 1.1 Goal

Pick an active strategy built on industry/factor returns, emissions data, or broker/alpha signals. Evaluate it critically. Use ChatGPT for ideas, coding help and robustness checks.

### 1.2 Report template

| Section | Length | What goes in it |
|---|---|---|
| 1. Executive summary | 1 paragraph | The strategy. If no alpha, say "Do not implement" and why. |
| 2. What did you try? | 2 to 5 pages | a. Ideas (where the strategy comes from). b. Data (sources). c. Implementation: risk model, turnover and costs, at least 3 good ChatGPT prompts. |
| 3. What did you learn? | 1 to 4 pages | a. Style and risk factor exposures. b. Performance over time: full sample, post-2010, last 12 to 18 months. c. Robustness and limits. d. ChatGPT evaluation: usefulness, flaws, how we adapted. |
| 4. Appendices | as needed | ChatGPT transcripts, tables, plots, code snippets. |

### 1.3 Grading

- **Thesis, 40%.** Well motivated, consistent with the data, clearly explained.
- **Execution, 40%.** Risk control, horizon analysis, robustness checks, a critical look at ChatGPT's role.
- **Originality, 20%.** New data use, prompt design, unique insights. Bonus for creative but well-structured ChatGPT use.

### 1.4 ChatGPT rules

1. At least 3 substantial interactions (idea generation, coding support, robustness design).
2. Document each one: prompt, summary of the output, our critical evaluation.
3. Reflect on ChatGPT's strengths and limits as an investment research assistant.

The sheet links this to HW01 (ChatGPT generated two emissions strategy ideas) and HW02 (ChatGPT critiqued alpha assumptions). Same critical mindset expected here.

### 1.5 Two things to watch

- The sheet says "Deadline: September 10th, 2025". That is last year's date. The team is working to **Sunday 27 Sep 2026**.
- At the 21 Sep meeting you noted extra framing: **US equities, 3 months from 1 Oct to 31 Dec, maximize Q4 P&L, watch the midterm elections.** It is not on the sheet. Section 11.3 covers how the plan handles it.

---

## 2. Our project in plain words

### 2.1 The idea

Workers give a live read on an industry. When an industry posts more openings, hires more, and its workers quit more (they have options), it is usually growing. When layoffs rise and hours get cut, it is shrinking. The BLS publishes these numbers by industry every month. Equity investors mostly treat them as macro headlines, not as a way to rank industries.

The open question: is strong hiring **good news** (demand is growing) or **bad news** (labor costs squeeze margins)? The answer may depend on how tight the whole labor market is. We measure that with:

> **T = log(job openings ÷ unemployed people)**

When T is above 0, there are more openings than unemployed people. That is a tight market, like 2021 to 2023.

### 2.2 The three research questions

| | Question | How we answer it |
|---|---|---|
| **Q1** | Does public labor data predict which industries outperform? | Main test, on the sealed period. Model A1 vs simple rule A0, plus the gate. |
| **Q2** | Does company-level data (job postings, layoff notices) add anything? | Only if we get access to that data on day 1. Likely dropped (see 11.2). |
| **Q3** | Do ChatGPT agents that share findings search better than agents that don't? | On the research period, using process metrics across 3 runs (seeds). |

### 2.3 Why "Do not implement" is expected, and why that's fine

- The test period has about 142 months. To reach a t-stat near 2 in 142 months, you need an annualized Sharpe near 0.58. That is a high bar for a 13-industry rotation.
- The 13 groups are not fully independent (some share data series). The real width is closer to 8 or 9 groups. Fewer independent bets means weaker evidence.
- The gate has 5 conditions. All must pass.

So the report is built to be useful whatever the verdict. It leads with three findings:

1. The gap between research-period performance and sealed-test performance.
2. How many candidate signals looked good in research and then failed in the test.
3. The comparison of the two agent setups (islands vs independent).

The assignment explicitly accepts "Do not implement" with a justification.

---

## 3. How the strategy works

### 3.1 Universe: 13 industry groups

Returns come from Ken French's 49 industry portfolios. We merge them into 13 groups that match BLS industry codes. 7 portfolios are dropped because they don't map cleanly to one BLS industry: Agric, Other, Boxes, Books, Softw, Fun, PerSv.

| # | Group | French portfolios inside | Hours/wages match |
|---|---|---|---|
| 1 | Mining and logging | Gold, Mines, Coal, Oil | exact |
| 2 | Construction | Cnstr | exact |
| 3 | Durable manufacturing | Toys, BldMt, Steel, FabPr, Mach, ElcEq, Autos, Aero, Ships, Guns, Hardw, Chips, LabEq, MedEq | exact |
| 4 | Nondurable manufacturing | Food, Soda, Beer, Smoke, Hshld, Clths, Drugs, Chems, Rubbr, Txtls, Paper | exact (Hshld approximate) |
| 5 | Wholesale trade | Whlsl | exact |
| 6 | Retail trade | Rtail | exact |
| 7 | Transport, warehousing, utilities | Trans, Util | approximate (covers transport only) |
| 8 | Information | Telcm | exact |
| 9 | Finance and insurance | Banks, Insur, Fin | approximate (financial activities) |
| 10 | Real estate | RlEst | approximate (same series as group 9) |
| 11 | Professional and business services | BusSv | exact |
| 12 | Health care | Hlth | approximate (education and health) |
| 13 | Accommodation and food | Meals | approximate (leisure and hospitality) |

JOLTS data always matches the group's own industry code. Only the hours/wages series (CES) are sometimes a wider sector.

- **Group return** = value-weighted average of its portfolios (weights = last month's market cap).
- **Target** = next month's return **relative** to the average of all 13 groups. We predict the ranking, not the market direction.

### 3.2 The signals

Every signal is a **change over the past year of a 3-month average**:

- The 3-month average smooths monthly noise.
- The year-over-year change removes seasonality (retail always hires in December). This lets us use not-seasonally-adjusted data, which FRED has for every industry. Seasonally adjusted JOLTS is missing for several industries.

| Signal | What it measures | Source | Sign in rule A0 |
|---|---|---|---|
| F1 Openings | change in job openings rate | JOLTS | + |
| F2 Hires | change in hires rate | JOLTS | + |
| F3 Quits | change in quits rate | JOLTS | not in A0 |
| F4 Layoffs | change in layoffs and discharges rate | JOLTS | minus (more layoffs = bad) |
| F5 Hours | log change in average weekly hours | CES | + |
| F6 Wage-price | wage growth minus output price growth (margin pressure) | CES + PPI | used only if 9+ groups have a clean price match |
| T | national tightness, log(openings ÷ unemployed) | JOLTS total + CPS | same for all groups, works only through interactions |

**Standardization, every month:** divide each signal by its group's own historical volatility (at least 24 months), z-score across the 13 groups, cap at ±3, set missing to 0.

**A0 fixed rule** = average of z(F1), z(F2), minus z(F4), z(F5). Signs set by economic logic before seeing any data. No fitting at all.

### 3.3 The models

| Name | What it is | Role |
|---|---|---|
| A0 | Fixed rule above | Benchmark. Nothing to overfit. |
| A1 | Ridge regression on F1 to F5 (+F6 if admitted) | Main public model. Answers Q1. |
| A1-T | A1 plus each signal × T | Tests "tightness decides". Descriptive only (see 4.4). |
| A2 | A1 plus company-level features | Q2. Only if that data is admitted. |
| A3 | Base model + features from the independent agents | Control arm of the agent experiment |
| A4 | Base model + features from the island agents | Sharing arm of the agent experiment |
| A5 | Small LightGBM (depth 2, 200 trees), not tuned | Optional comparison |

- Ridge is refit every month on all data up to that month (expanding window, "walk-forward"). First prediction after 36 months.
- The ridge penalty is picked once, on research data only (5-fold blocked cross-validation), then frozen.
- The **primary strategy**, the one the gate judges, is the best research-period net Sharpe among A0 to A4. It is chosen before the test opens.

### 3.4 The portfolio (same for every model)

- **Rank** the 13 groups each month by the model score.
- **New tranche:** long top 3, short bottom 3, equal weights, dollar-neutral (same dollars long and short).
- **3-month hold:** the book is the average of the last 3 tranches. Each month one third of the book is replaced.
- **Beta hedge:** estimate each group's market beta (60 months). Offset the book's beta with a market position. We bet on industries, not on the market.
- **Volatility target:** scale to 10% annualized (Ledoit-Wolf covariance, 60 months). Gross leverage capped at 2×.
- **Costs:** 10 bp per unit of traded weight (also 0 and 25 bp). Hedge trades 2 bp. Borrow and financing reported separately.
- **Long-only version:** equal-weight top 3 vs equal-weight all 13. Report active return, tracking error, information ratio.
- **Sensitivities:** 1-month and 6-month holding.

### 3.5 Horizon: predict 1 month, hold 3 months

The trading horizon is 3 months, which matches the Oct to Dec framing. But we train and test on 1-month returns because that gives far more independent data points:

| Horizon | Research (2004 to 2014) | Sealed test (2014 to 2026) |
|---|---|---|
| 1 month | 126 | 142 |
| 3 months (non-overlapping) | 42 | 47 |
| 6 months (non-overlapping) | 21 | 23 |

23 data points can't prove anything. So 3- and 6-month results are reported, but they never decide.

---

## 4. The "no cheating" machinery

This is the core of the Execution grade. Five ideas.

### 4.1 No look-ahead: use data as it was known

Economic data gets revised. The JOLTS number you download today for March 2012 is not what investors saw in April 2012. Using today's numbers in a backtest is look-ahead bias.

The fix is **ALFRED**, the St. Louis Fed archive. It stores every past version ("vintage") of each series. For each decision date d (last trading day of the month), we use only values published by d minus 1 day.

Publication lags also matter:

| Source | Released | Latest month usable at month-end d |
|---|---|---|
| JOLTS | about 5 weeks after month end | d minus 2 months |
| CES hours and wages | first Friday of the next month | d minus 1 month |
| Unemployment (CPS) | same day as CES | d minus 1 (T uses the matched month, d minus 2) |

### 4.2 Research period vs sealed test, split at S*

**Problem:** ALFRED vintages for industry JOLTS start late. Construction openings: 11 Aug 2010. Durable goods: 7 Oct 2014. Before that, no as-known history exists.

**Solution:** S* = the date by which all admitted series have vintages. The audit sets it, and it is expected around Oct 2014.

```
May 2004 ............ RESEARCH ............ S* (~Oct 2014) ............ SEALED TEST ............ Aug 2026
  pseudo-real-time data                     |   as-known data, opened ONCE
  agents and selection happen here          |   last 18 months = Mar 2025 to Aug 2026
  includes the 2008-09 crisis               |   includes COVID and the 2021-23 tight market
```

- **Research period** (returns May 2004 to Oct 2014). Uses the S* vintage with fixed publication lags. Called "pseudo-real-time". We build and select everything here.
- **Sealed test** (returns Nov 2014 to Aug 2026). True as-known data. Returns load only inside one function, `final_evaluation()`. It refuses to run until the freeze file exists and the hashes match. It runs once.

### 4.3 Pre-registration and freeze

- **Stage 0:** every constant goes in `params.py`. Its SHA-256 hash (a digital fingerprint) is saved in `prereg_v0.json` before any return is loaded.
- Any later change goes in `deviations.md`, with a reason that is not about performance.
- **Stage 7 freeze:** hash of code + params + selected features saved in `FREEZE.json`. Nothing changes after that.
- Why it matters: it proves we did not tweak the strategy after peeking at results.

### 4.4 Tightness is "extrapolated"

In the research period, openings never exceed unemployed people (T stays below 0). Tight markets only appear from 2018, and especially 2021 to 2023, inside the test. So any "signal × T" effect is learned without ever seeing a tight market. That is why Q1 is judged on main effects only (A1), and A1-T is descriptive.

### 4.5 Overfitting controls

| Tool | Plain-English meaning |
|---|---|
| Reality check (stationary bootstrap) | Is the best of our 36 candidates better than what luck alone would give the best of 36? |
| Deflated Sharpe ratio | Shrinks a Sharpe ratio for the number of things we tried. |
| Holm correction | Adjusts p-values because we run several tests (A1 vs A0, A2 vs A1, A3 vs base). |
| Circular time-shift placebo | Slide the signals against returns by 24+ months, many times. If the real IC is not in the top 5% of shifted ICs, it is probably noise. |
| Newey-West t | A t-stat corrected for autocorrelation and overlapping returns. |
| Drop-one-group | Check that no single industry makes more than 50% of the profit. |
| Data variants (FIRST, REVISED, FIXEDLAG) | Rerun with first-release data, today's data, fixed lags. The as-known minus revised gap shows how much look-ahead would have flattered us. |

---

## 5. The ChatGPT part

### 5.1 The four documented interactions (P1 to P4)

The course needs at least 3. We have 4. Each is logged with: prompt, output summary, what was wrong, what we changed. There is also a **"Team critique" column that the model leaves empty for us to fill.**

| | Name | Stage | What ChatGPT does |
|---|---|---|---|
| P1 | Data audit and coding | 1 | Reviews our data list, industry mapping and as-of code. Finds mapping errors, look-ahead bugs and code bugs, each with a test. |
| P2 | Blind hypothesis generation | 5 | The agents' first feature ideas (seed 1), from anonymized data. |
| P3 | Migration | 5 | The notes island agents send each other (seed 1), and whether the others used them. |
| P4 | Red team | 7 | Gives 10 reasons our research results could be spurious, each with a runnable test. Useful tests are added before the freeze. |

This covers the three course categories: idea generation (P2, P3), coding support (P1), robustness design (P4).

### 5.2 The agent experiment (Q3)

This is the island-migration idea from the agent research-loop paper you wanted to apply to the ChatGPT part.

- **Blinding.** Agents never see industry names, tickers, dates, series IDs or raw values. Variables become V01..Vk, groups G01..G13, time t = 1..n. They are called through the OpenAI API with no tools (no browsing, no code). This stops ChatGPT from using what it "knows" about history.
- **Two arms, same budget:**
  - *Islands:* 3 agents with different starting focus (Temporal, Composition, Interactions). 6 submissions each. After submissions 2 and 4, each writes a note of 120 words max (findings, at least one failure, no formulas) to the other two.
  - *Independent:* same 3 focuses, same budget, no notes.
- **Each submission** is JSON: a name, a hypothesis (40 words max), what would falsify it (30 words max), and a formula written in a fixed grammar of 14 operations (lag, moving average, change, yoy, rank, ratio, × T, etc.). Max 3 nested operations, max 2 variables plus T. Invalid submissions still use up the budget.
- **Feedback** after each submission (research period only, rounded): coverage, mean IC, Newey-West t, IC in low vs high T, max correlation with base features, rank persistence. **Never the IC in each half of the sample**, because selection uses it and an agent could game it.
- **Seeds.** Each arm runs 3 times. Only seed 1 can feed a strategy (36 candidates, 18 per arm). Seeds 2 and 3 only measure how the search behaves (error bars). Total: 108 candidates.
- **Q3 metrics, per arm:** best-so-far IC by submission number, median IC, invalid rate, diversity (how different the ideas are). Q3 answer = is the gap between arms bigger than the spread between seeds?
- **Migration tracing.** Each note is split into claims. A separate ChatGPT "judge" call checks which later submissions used which claim. The team spot-checks 20% of those judgments by hand.
- **Selection (Stage 7, seed 1 only).** Keep a candidate if research t ≥ 1.5, its IC has the same sign in both halves, and its correlation with base features and already-picked ones is below 0.8. Up to 3 per arm. A3 gets the independent picks, A4 the island picks.

### 5.3 Why this scores well

The rubric rewards "creative but well-structured ChatGPT use". Here ChatGPT is not just used, it is tested: blinded, budgeted, compared against a control, and red-teamed.

---

## 6. The pipeline, stage by stage

Stage 6 (the evaluator) is built and tested **before** Stage 5 (the agents). That way the agents can't shape how they are scored.

| Stage | What happens | Main output |
|---|---|---|
| 0 Pre-register | Write all constants and 6 pre-registration statements, then hash | `params.py`, `prereg_v0.json` |
| 1 Download and audit | Download data, check every series ID, find first vintages, set S*, admit or reject series, try company data (3-hour limit), run P1 | `manifest.csv` |
| 2 As-of panels | Build "what was known on date d" tables in 4 variants. 5 values listed for hand-checking on ALFRED | `panel_asof.parquet` |
| 3 Features | Compute F1 to F6, T, A0, then standardize | `features.parquet` |
| 4 Blinding | Anonymize variables, groups, dates | `blind_map.json` (kept secret) |
| 6 Evaluator | Build models, portfolio, costs, feedback. Test on a fake signal with a known IC | check in `checkpoints.md` |
| 5 Agents | Run islands and independent agents, 3 seeds, full logging, migration tracing | `agents/log.jsonl`, `candidates.csv` |
| 7 Select, red team, freeze | Pick features, reality check, deflated Sharpe, choose primary strategy, run P4, freeze | `selected_features.json`, `FREEZE.json` |
| 8 Sealed evaluation | Run all strategies on the test period once: tests, placebo, factor attribution, time windows, data variants, drop-one-group, ETF proxies | `outputs/final/` |
| 9 Gate, decode, report | Apply the gate. Only now decode what the selected features mean. 12 figures, draft report, ChatGPT log | `report/report.md`, `report/chatgpt_log.md`, `outputs/figures/` |

Code files, and only these: `params.py`, `data.py`, `stats.py`, `plots.py`, `agents.py`, `run.ipynb`.

---

## 7. The gate: when would we say "Implement"?

All 5 must hold for the primary strategy on the sealed test.

| | Criterion | Plain English |
|---|---|---|
| G1 | Timing | Primary results use as-known data. No open audit flag. |
| G2 | Prediction | Mean 1-month IC above 0 with t ≥ 2. |
| G3 | Incremental | Alpha after FF5 + momentum + industry momentum above 0 with t ≥ 2. |
| G4 | Robust | Positive IC in both halves. Placebo p < 0.05. No group above 50% of profit. |
| G5 | Implementable | Net Sharpe above 0 at 25 bp costs. Turnover and capacity documented. |

If any fails: write "Do not implement", name the failed criteria, and add the power statement (about 142 months can only detect a Sharpe near 0.6 or higher, so a null result does not rule out a smaller effect).

French portfolios are research series, not tradable. The report lists ETF proxies per group, for example ITB or XHB (construction), XRT (retail), IYT (transport), XLU (utilities), XLF, KBE or KIE (financials), IYR (real estate), PEJ (leisure).

---

## 8. Documents and what each one is for

| Document | What it is | Role | Made by |
|---|---|---|---|
| Assignment sheet ("MFE 230G - Final Project Assignment") | Course brief | Rules, template, grading, ChatGPT requirement | Professor |
| Artifact "230GA - Project", final version ([link](https://claude.ai/artifact/L4NCwGaTNio12ZLLcdmdvC)) | Web page | Human-readable blueprint: recap, review changes, horizon, all data links, pipeline, diagram, 5-day plan, rubric mapping, sources, prompt download | Piero (with a change from Romain's work) |
| Your copy "230GA - Project (Copy)" ([link](https://claude.ai/code/artifact/20de004a-314a-4b78-aea5-2bc97e33ce19)) | Same page, v4 dated 24 Sep | What this briefing is based on | Copy of Piero's |
| Earlier draft ([link](https://claude.ai/artifact/5nc3prvApe8CPLJfM8VChx)) | First draft, posted 23 Sep 4:37 PM | Superseded. Ignore. | Piero |
| `230GA_build-and-run_prompt.md` | About 6,100-word instruction file | Paste into a coding AI that can run code and reach the internet. It writes the code and runs Stages 0 to 9 in one go. Stops early only for a missing API key. | Piero |
| Data zip (to be made) | All downloadable data in one file | Lets the runner start fast. Shared by email. | You or Elouan |
| Run outputs (after the run) | Code + `outputs/` + `report/` | The real results and the draft report | Whoever runs it (Alex offered) |

**Files to read first once the run finishes:**

1. `outputs/checkpoints.md`: plain-English status after each stage. Ends with the verdict, limits and how to reproduce.
2. `outputs/deviations.md`: every place the run departed from the plan, and why.
3. `report/report.md`: draft report in the course template.
4. `report/chatgpt_log.md`: P1 to P4 logs with the empty "Team critique" column.
5. `outputs/figures/`: the 12 figures.

---

## 9. What's been done so far

### 9.1 Timeline

| Date | What happened |
|---|---|
| 13 Sep | Last homework submitted by Alex (not this project). Elouan said the contribution statement was only needed once, at the start. |
| 20 Sep | Romain: GA project due "next Sunday" (27 Sep). Piero sets a team meeting. |
| 21 Sep, 7:30 PM | Meeting (in person in Chou Hall, or online). You joined online and noted: US equities, 3 months Oct 1 to Dec 31, maximize Q4 P&L, watch the midterms. Piero set a follow-up for Wed 6:30 PM. |
| 21 Sep, night | Romain found a paper that "doesn't look overly complicated" and said he'd try a similar pipeline. |
| 23 Sep, afternoon | Everyone but Elouan was at Haas, so the rest of the team met early instead of waiting for the evening slot. |
| 23 Sep, 4:37 to 6:15 PM | Piero posted two artifact links, then the "FINAL VERSION" (strategy, horizon, data, pipeline, diagram, full prompt). Asked you and Elouan to review it, then split the work. |
| 24 Sep | Piero added "a slight change from Romain's work" (same link). Blueprint v4 is dated 24 Sep. |
| 24 Sep, 3:39 PM | Alex: no OpenAI API key. He'd look for a fix and split the work, with each person doing a part "by Sat or something". |
| 24 Sep, 3:56 PM | Piero: only one person needs to run the prompt, ideally before the weekend. Then the team splits the report revision. Alex offered to run it with Opus 5.5. |
| 24 Sep, 4:01 PM | Piero asked you or Elouan to build a data zip for Alex. Romain: "not even sure we need the best version". |
| 24 Sep, 4:55 to 4:59 PM | Elouan asked where to put the data. Piero: zip it and email it to the team. **Chat ends here.** |

### 9.2 Who's doing what

- **Piero:** built the blueprint and the prompt. Organizes meetings.
- **Romain:** flagged the deadline. Said he'd try a pipeline based on a paper. Piero then added a change from Romain's work to the final version.
- **Alex:** offered to run the pipeline. Flagged the missing OpenAI key. Said he'd send the work split.
- **Elouan:** asked to help with the data zip and replied.
- **You:** noted the meeting constraints. Asked (with Elouan) to build the data zip.

### 9.3 Status board

| Item | Status |
|---|---|
| Strategy idea and thesis | Done |
| Blueprint (two review rounds, v4) | Done |
| Data sources identified, links checked (23 Sep) | Done |
| Build-and-run prompt | Done |
| Data zip | Asked of you or Elouan on 24 Sep. Unknown. |
| OpenAI API key | Missing as of 24 Sep. Alex looking into it. |
| Work split | Promised by Alex. Not in the chat. |
| Pipeline run | Not started as of 24 Sep. Target was "before the weekend". |
| Report revision | Not started. Split after the run. |
| Submission | Due Sun 27 Sep. Submitter not chosen. |

---

## 10. What you need to do

In order:

1. **Get a status update today.** Ask the group: Was the zip sent? Did Alex run the pipeline? Is there an OpenAI key? Where is the work split?
2. **Build the data zip** if Elouan hasn't (10.1).
3. **Help unblock the OpenAI key** (11.1).
4. **Take your report piece.** If no split exists yet, the artifact's 5-day plan has 4 roles, each ending in a report section:
   - *Data and timestamps* → Data section (2b) and appendix.
   - *Features and mappings* → economic interpretation of the results.
   - *Portfolio and evaluation* → tables, figures, Section 3.
   - *Agents and reporting* → Section 3d (ChatGPT evaluation) and the team critique.
5. **Fill in the "Team critique" column** of the ChatGPT log, at least for your part. The course grades our own critical view of ChatGPT.
6. **Run the checklist in 10.2** before submitting.

### 10.1 The data zip

Suggested layout (all links are in the artifact, "1 · Data" section):

```
230GA_data/
  french/
    49_Industry_Portfolios_CSV.zip
    F-F_Research_Data_5_Factors_2x3_CSV.zip
    F-F_Momentum_Factor_CSV.zip
    Siccodes49.zip
  census/
    1987_SIC_to_2002_NAICS.xls
  fred/                      (CSV, current values)
    jolts/      52 series: JTU + code + JOR/HIR/QUR/LDR
                codes: 110099 2300 3200 3400 4200 4400 480099 5100 5200 5300 540099 6200 7200
    ces/        24 series: CEU + code + 07 (hours) and 08 (earnings)
                codes: 10000000 20000000 31000000 32000000 41420000 42000000
                       43000000 50000000 55000000 60000000 65000000 70000000
                construction earnings = CES2000000008 (not CEU2000000008)
    tightness/  JTSJOL, UNEMPLOY
  README.txt                 (file, source URL, download date)
```

**Important caveat to tell the team:** FRED CSVs downloaded today hold **today's revised values**. Rule R1 forbids those in primary results. The pipeline pulls the historical vintages from ALFRED through the FRED API, so whoever runs it **still needs a free FRED API key**. The zip is still useful: the French and Census files need no key, and the FRED CSVs work as a backup and as the "REVISED" diagnostic.

### 10.2 Pre-submission checklist

- [ ] Executive summary: one paragraph, verdict first.
- [ ] Section 2 is 2 to 5 pages. Section 3 is 1 to 4 pages.
- [ ] At least 3 ChatGPT interactions, each with prompt, output summary and critique (P1 to P4).
- [ ] Section 3d reflects on ChatGPT's strengths and limits in our own words.
- [ ] Time windows: full sample, post-2010, last 12 to 18 months (pseudo-real-time parts labeled).
- [ ] Factor exposures reported (FF5 + momentum).
- [ ] Limits stated: effective width of 8 to 9 groups, extrapolated tightness, low power, CRSP stock baskets as the follow-up.
- [ ] Appendices: transcripts, tables, plots, code snippets.
- [ ] Every number traces to a file in `outputs/`.
- [ ] Q4 2026 / midterm point handled, if the team keeps it (11.3).
- [ ] Contribution statement: confirm whether the final project needs one.
- [ ] Submitter chosen.

---

## 11. Open issues to raise with the team

### 11.1 No OpenAI API key (biggest blocker)

- The agents, P1, P4 and the migration judge all call ChatGPT through the API. A ChatGPT subscription is billed separately from the API and does not come with a key.
- Without a key, the prompt's fallback runs Stages 0 to 4 and 6, saves the agents' first prompts in `outputs/agents/manual/`, and stops before Stage 5.
- Doing Stage 5 by hand by tomorrow is not realistic: 108 submissions (2 arms × 3 agents × 6 × 3 seeds), each waiting on evaluator feedback, plus 18 migration notes and the judge calls.
- Options, best first:
  1. **Someone creates an OpenAI API key** (pay-as-you-go, card on file). Keeps the plan intact.
  2. **Key, but short on time:** run seed 1 only (36 submissions). Log it in `deviations.md` with a time reason. Keeps the strategy, P2 and P3. Loses the Q3 error bars.
  3. **No key at all:** do P1, P4 and a small P2 by hand in ChatGPT. Report Q3 as not run. Meets the course minimum but loses much of the originality.
- Keep the agents on ChatGPT, since the course requires it. The coding model that runs the pipeline (Opus 5.5 or another) can be anything. It is the "engineer", not the researcher.

### 11.2 Time

- The plan was a 5-day build. As of Thursday nothing had run. A full run can take many hours (rate-limited downloads, 108 agent calls in sequence, 5,000-draw bootstraps).
- Expect company data (LinkUp, WARN) to be dropped under the 3-hour rule (R8). Then Q2 and A2 disappear. The team agreed to this in advance. The report should say so.
- The model's draft report will need a human pass: length limits, tone, and the critique column.

### 11.3 The Q4 2026 and midterm framing

You noted: US equities, 3 months from 1 Oct to 31 Dec, maximize Q4 P&L, watch the midterms.

- **Covered by the plan:** US equities, 3-month holding.
- **Not covered:** any live position for Q4 2026, and the midterm elections (Tue 3 Nov 2026). The sealed test ends Aug 2026.
- **If this framing came from the professor, raise it now.** A light fix: a short section showing the book the frozen model would hold at the 30 Sep 2026 decision date, plus one line in the limits on election risk (the model has no political variable). Keep it outside the sealed test so it doesn't touch the pre-registration.

### 11.4 Deadline and logistics

- The sheet's date is stale (Sept 10, 2025). Team target: Sun 27 Sep 2026. Confirm on bCourses.
- Choose who submits.

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **IC (information coefficient)** | Correlation between our scores and next month's actual relative returns across the 13 groups. **Rank IC** uses ranks (Spearman). |
| **Newey-West t** | t-stat corrected for autocorrelation and overlapping returns. |
| **Sharpe ratio** | Average excess return ÷ volatility, annualized. |
| **Alpha** | Return left after removing exposure to known factors. |
| **Fama-French factors** | Mkt-RF (market), SMB (size), HML (value), RMW (profitability), CMA (investment). Plus **Mom** (momentum). |
| **Ridge regression** | Linear regression with a penalty that shrinks coefficients. Less overfitting. |
| **Walk-forward / expanding window** | Refit each month on all data up to that month, predict the next month. |
| **Blocked cross-validation** | Cross-validation with contiguous time blocks (and a 1-month gap), so the future doesn't leak into training. |
| **Tranche** | One month's batch of positions. Three live tranches = 3-month holding. |
| **Dollar-neutral** | Same dollar amount long and short. |
| **Beta hedge** | A market position that cancels the book's market exposure. |
| **Volatility target** | Scale positions so expected volatility is 10% a year. |
| **Ledoit-Wolf** | A more stable way to estimate a covariance matrix. |
| **Turnover / bp** | How much of the book trades each month. 1 bp = 0.01%. |
| **z-score / winsorize** | Standardize to mean 0 and std 1. Cap extreme values (here at ±3). |
| **Vintage / ALFRED** | A past version of a data series as published on a given date. ALFRED is the archive of vintages. |
| **As-of / ASOF** | The value known on a given date, using vintages. |
| **Pseudo-real-time** | Old data with fixed lags applied, used where no vintages exist (our research period). |
| **JOLTS** | BLS Job Openings and Labor Turnover Survey: openings, hires, quits, layoffs by industry. |
| **CES** | BLS Current Employment Statistics: hours and earnings by industry. |
| **CPS** | BLS household survey. Source of the unemployment count. |
| **SA / NSA** | Seasonally adjusted / not seasonally adjusted. |
| **V/U, T** | Job openings ÷ unemployed. T = log(V/U). Above 0 means a tight labor market. |
| **S*** | The research/sealed-test boundary, set by when vintages start. |
| **Pre-registration** | Writing every rule down before seeing results. |
| **SHA-256 hash** | A fingerprint of a file. Any change to the file changes the hash. |
| **Seed** | One independent run of the agent experiment. |
| **Jaccard similarity** | Overlap between two sets. Used to measure how similar two ideas are. |
| **Reality check** | Bootstrap test: is the best of many strategies better than luck? |
| **Deflated Sharpe ratio** | Sharpe adjusted for the number of trials. |
| **Holm correction** | Adjustment for running several tests at once. |
| **Stationary bootstrap** | Resampling in random-length blocks to keep time dependence. |
| **Placebo (circular shift)** | Shift signals in time against returns to see what "no real link" looks like. |
| **LinkUp / Dewey** | Company job-postings data, accessed through the Dewey platform. |
| **WARN / Revelio / WRDS** | Legally required mass-layoff notices, compiled by Revelio Labs, accessed through WRDS. |
| **SIC / NAICS** | Two industry classification systems. French uses SIC, BLS uses NAICS. |
| **CRSP baskets** | Stock-level industry portfolios built from CRSP. Named as the follow-up, not built here. |

---

## 13. Useful links

- Final artifact (Piero): https://claude.ai/artifact/L4NCwGaTNio12ZLLcdmdvC
- Ken French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- FRED API key (free): https://fred.stlouisfed.org/docs/api/api_key.html
- ALFRED: https://alfred.stlouisfed.org/
- FRED JOLTS release tables: https://fred.stlouisfed.org/release/tables?rid=192&eid=6614
- fredapi (Python): https://github.com/mortada/fredapi
- Background paper cited in the artifact: Belo, Lin and Bazdresch, "Labor hiring and returns", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1267462
- Suggested readings from the sheet: Zarattini and Antonacci, "A Century of Profitable Industry Trends" (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4857230); NBER w30217, ML in asset pricing (https://www.nber.org/system/files/working_papers/w30217/w30217.pdf).
