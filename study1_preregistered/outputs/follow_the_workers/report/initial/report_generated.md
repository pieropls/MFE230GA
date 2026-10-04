# Follow the Workers

## 1. Executive summary

**Do not implement**. The prespecified primary is A3. Failed criteria: G2, G3, G4, G5. 142 sealed months require roughly 0.6 annualized Sharpe for IID t≈2; a null does not rule out a smaller effect. This study separates public labor prediction, optional company data, and agent search behavior.

## 2. What did you try

### 2a. Ideas

Predict next-month relative returns across 13 fixed industry groups using public labor changes. Compare independent and communicating agent searches with equal budgets; only seed 1 supplies strategy features.

### 2b. Data

FRED/ALFRED labor vintages and Ken French industry returns and factors, pinned by file hash. Research uses the October 30, 2014 snapshot with fixed publication lags. Sealed results use information available before each decision. Selection ends September 2014; October is purged. LinkUp and WARN failed timing/evidence gates and are excluded. F6 and A5 are omitted; Q2 cannot be answered with these inputs. See manifest.csv and deviations.md.

### 2c. Implementation

Expanding ridge fits require 36 fully available training months. Penalties are fixed using five chronological folds with a one-month purge. Portfolios rank the top and bottom three, average three monthly tranches, hedge lagged market beta, target 10% volatility and cap gross exposure at 2. Costs use drift-adjusted one-way turnover; industry trades cost 10 bp and market-hedge trades 2 bp. The registered volatility target and leverage cap also apply during startup.

The target is an industry's excess return less the equal-weight mean excess return of the fixed group universe. This focuses the prediction exercise on relative performance. National tightness is common to every group and cannot change a cross-sectional ranking on its own; it enters the interaction comparator, while the main public model answers the primary labor-information question. The fixed benchmark averages standardized openings, hires, negative layoffs and hours with signs specified before observing results.

Each industry return combines its assigned French portfolios using prior-month market capitalizations, computed as number of firms times average firm size. Missing required members or factors cause a validation failure rather than a smaller, changing universe. The French files are current historical research series. Their use does not establish point-in-time constituent availability or the tradability of an identical basket. Exact source bytes and observation endpoints are retained in the input inventory.

The labor pipeline distinguishes reference months from publication dates. A value observed for an earlier month is not usable merely because its reference month precedes the portfolio decision. ASOF uses the vintage interval in force by the previous calendar day. FIRST keeps the earliest archived vintage, which is not necessarily the original release for observations predating archive coverage. REVISED is a hindsight diagnostic and FIXEDLAG applies publication lags to revised values. Research history uses a single frozen snapshot with fixed lags, so it is explicitly pseudo-real-time. No later revision enters that research snapshot. National openings and unemployment use the latest jointly available reference month, with staleness recorded. Construction earnings use the prescribed seasonally adjusted exception, explicitly flagged in the manifest.

Public signals compare three-month averages with their year-earlier counterparts; hours use log growth. Each signal is divided by its own expanding historical standard deviation, then standardized across groups and winsorized. Insufficient current coverage does not become an apparently valid all-zero signal. Permitted missing groups are flagged before imputation. Shared series and broad supersector matches reduce the effective diversity of the information, even when the portfolio has distinct return columns.

Training labels obey the same timing rule as predictors. For a return earned in month m, the decision is at the previous month-end and the most recent fully available monthly return is m minus two. The October boundary return therefore cannot choose the first sealed portfolio's model, and the same restriction applies to its risk estimates. Cross-validation keeps entire months together and uses chronological training followed by purged validation blocks. Penalties and selected feature definitions remain fixed in the sealed test, while coefficients update using newly available historical labels.

Agent leaves are decision-time levels, evaluated privately; agents receive their anonymous dictionary, permitted operations and rounded development summaries. Temporal operators retain the information known at each previous decision rather than retrospectively revising the feature history. A whitelist parser rejects arbitrary code, arithmetic outside the grammar, negative lags and excess depth or variable counts. Constructed candidates receive the registered standardization. Missing candidate model inputs are zero-imputed with coverage reported separately; undefined candidate IC is never presented as zero.

Both search architectures receive equal submission budgets and starting emphases. Migration occurs only after all participating islands finish the designated submission, preventing an ordering advantage within a round. Invalid submissions consume their slots. Syntax repair is limited and is distinct from revising an invalid hypothesis. Only the first seed can contribute selected features; the remaining seeds characterize search variation. The engineer does not propose, manually edit or rank experimental candidates.

Portfolio membership stays fixed within each tranche. Each month's target combines the remaining tranches, estimates group market betas from prior returns, adds a market hedge and uses a joint covariance estimate for risk scaling. Both hedge exposure and industry exposure count toward the gross cap. Empty startup or abstention slots contribute zero tranches; the aggregate book is scaled to the registered volatility target subject to the leverage cap. If tranches cancel, the book can become flat and pays any required liquidation costs. Weight drift uses funded account returns, while performance Sharpe uses net excess returns.

Transaction charges are applied once to absolute changes from drifted pretrade weights. Industry and hedge rates are distinct, and borrow/financing sensitivities are reported separately. Candidate portfolio diagnostics use the common research comparison calendar; missing or constant signals create no new tranche while existing holdings age normally. The long-only comparator uses the same top-group membership against an equal-weight group benchmark. Its active return, tracking error and information ratio supplement the long–short results.

Monthly IC inference uses calendar-aware Newey–West errors. Overlapping horizons compound total returns before cross-sectional demeaning, with longer HAC lags. Paired comparisons resample the same calendar positions and center the null distribution; the prespecified inferential endpoints share a Holm adjustment. The reality-check diagnostic preserves the joint IC/missingness calendar, and unavailable full-family calculations are reported explicitly. Deflated Sharpe uses monthly units and the nominal search budget; neither diagnostic completely removes dependence or adaptive-search bias.

Before opening sealed returns, feature choices, code, inputs, review evidence and the implementation-capacity assessment are hashed. A start marker precedes the sealed read. Any later rerun needs a written reason and a separate output directory. Readiness rejects stale audit stamps whose underlying files changed. The notebook source is protected independently of execution outputs, while append-only operational logs remain available to document the run.

## 3. What did you learn

### 3a. Style and risk exposures

| Strategy | Research Sharpe | Sealed Sharpe | Sealed IC | HAC t |
|---|---:|---:|---:|---:|
| A0 | -0.441 | -0.359 | -0.020 | -0.713 |
| A1 | -0.541 | -0.507 | -0.014 | -0.743 |
| A1-T | -0.548 | -0.593 | -0.029 | -1.422 |
| A3 | -0.132 | -0.584 | -0.021 | -1.077 |
| A4 | -0.181 | -0.786 | -0.020 | -0.859 |

Primary factor alpha (monthly): -0.004; HAC t: -1.856. See the saved factor table and figure.

### 3b. Time patterns

The results file contains whole-period, half-period, pandemic-excluded, last-18-month and expanding-tightness-tercile results. Course-window series combine pseudo-real-time research and as-known sealed data and are descriptive.

| Primary window | Months | Net Sharpe | Mean IC | HAC t |
|---|---:|---:|---:|---:|
| whole | 142 | -0.584 | -0.021 | -1.077 |
| first_half | 71 | -0.724 | -0.028 | -0.901 |
| second_half | 71 | -0.486 | -0.015 | -0.594 |
| ex_pandemic | 132 | -0.514 | -0.012 | -0.565 |
| last_18 | 18 | 0.846 | 0.033 | 0.437 |
| T_low | 3 | -16.850 | unavailable | unavailable |
| T_middle | 6 | -0.072 | unavailable | unavailable |
| T_high | 133 | -0.542 | -0.017 | -0.828 |
| VU_below_1 | 67 | -0.635 | -0.026 | -0.853 |
| VU_above_1 | 75 | -0.554 | -0.017 | -0.672 |

Funded drawdown is not computed for disconnected conditional months: concatenating isolated regimes would not describe a continuous account. The full and post-2010 windows state their actual first observation after model burn-in. Their research segment is descriptive because the same research sample supplied model choices. It is not additional sealed evidence.

### 3c. Robustness and limits

Effective cross-sectional width is approximately 8–9 because some groups share CES series or use approximate supersectors. Tightness interactions and A4 versus A3 are descriptive. Company-data exclusion limits the study to Q1 and Q3. Research bootstrap and DSR diagnostics cannot fully correct adaptive model search. French industry portfolios are research series, not directly tradable. NAICS-based CRSP stock baskets are the recommended follow-up. ETF proxies require verified mapping and capacity analysis before trading.

Primary placebo p: 0.716. Fixed-path industry-cost breakeven: -31.837 bp. All prespecified sensitivity values, candidate failures, Holm-adjusted comparisons and exclusion reasons remain in the output files regardless of sign.

| Primary sensitivity | Net Sharpe | Mean turnover |
|---|---:|---:|
| holding_1 | -0.900 | 1.431 |
| holding_6 | -0.187 | 0.602 |
| cost_0 | -0.445 | 0.913 |
| cost_25 | -0.793 | 0.915 |
| borrow_25 | -0.615 | 0.914 |

Candidates that passed research eligibility but failed the sealed predictive criterion: 4. The saved definition requires the research t/correlation/half-sample filter and checks sealed t plus positive IC in each half; it does not reselect features on test outcomes. Every original seed-1 slot remains accounted for, including invalid proposals.

Circular-shift tests refit the frozen algorithm causally under every registered displacement. They do not merely shift already-fitted predictions. Drop-one-group diagnostics recompute cross-sectional transforms, target ranks, coefficients and portfolio risk while retaining the selected specifications and penalties. Revised-data comparisons measure the difference between available information and hindsight. These checks expose sensitivity; passing them does not prove an executable trading edge.

### 3d. AI evaluation

The experimental researchers, migration judges and P1/P4 reviewers use Claude Sonnet 5.5 through a subscription. The user approved Claude for all agent usage before research began; the provider amendment and actual interaction evidence are retained. Run indices 1–3 label independent repetitions; the CLI does not honor requested model seeds or temperature. Only run 1 supplies strategy features. Agents saw tightness-tercile feedback but never half-sample IC. Study calls receive no calendar dates or project context; the verified transport removes the CLI’s injected environment reminders.

Migration reports admitted: 7 of 18. Only admitted reports were delivered; report rejection and undefined judgments separately.

| Search metric | Independent mean | Islands mean | Islands minus independent | Absolute gap exceeds seed range? |
|---|---:|---:|---:|---|
| best_so_far_ic | 0.083 | 0.049 | -0.034 | False |
| median_ic | 0.005 | -0.002 | -0.007 | False |
| invalid_rate | 0.130 | 0.056 | -0.074 | False |
| diversity | 0.827 | 0.798 | -0.029 | False |

These comparisons describe the search process. Claim uptake is evaluated per report–receiving-submission pair; a later hypothesis can be associated with several earlier reports. Improvements over a receiving agent’s earlier best are therefore descriptive associations, not causal estimates of communication. Failure avoidance and the sampled human agreement are retained separately. Students must critically assess the proposals and audit findings rather than treating a syntactically valid response as economic evidence.

## 4. Appendices

All reported results originate in saved research_summary.json, agent summary files or sealed results.json. Full code, input hashes, inference tables, frozen selections, call logs and figure hashes accompany this report. Team critique remains for the students.

### Selected feature interpretation, decoded after evaluation

- independent, independent_1_Temporal_3: `regime(yoy(E),"low")`. Groups with higher year-over-year change in V05 (dollars per hour) will have higher next-month returns in low-T regimes, because accelerating compensation signals stronger conditions not yet fully priced in. The effect should vanish in high T.
- independent, independent_1_Interactions_4: `regime(spread(tsz(LDR,60),tsz(HIR,60)),"low")`. Groups whose V04 rate is unusually high versus their own history, relative to V02 (cross-sectionally standardized spread of time-series z-scores), earn lower next-month relative returns, especially when T is in its low regime, since stretched flows mean-revert.
- islands, islands_1_Composition_5: `spread(chg(LDR,6),chg(JOR,6))`. Groups whose V04 flow rate rose more than their V06 stock rate over the last 6 months (standardized across groups) have higher next-month returns, extending the 3-month version that showed positive IC. Expect positive IC in both T regimes.
- islands, islands_1_Composition_2: `spread(chg(LDR,3),chg(JOR,3))`. Groups whose V04 flow rate rose more than their V06 stock rate over the last 3 months (cross-sectionally standardized) have higher next-month returns, because flow-versus-stock composition shifts signal improving conditions ahead of the stock.
