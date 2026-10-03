# Independent code review: analysis/ (v2, v3, forward test) and results/

Reviewer: Claude (Fable 5.1), 3 Oct 2026. Scope: `analysis/{params,data,stats,plots}.py`, `analysis/run.ipynb` (83 cells), `results/build_results_book.py`, `results/v3_claims.py`, the frozen specs and run logs. The frozen study was read, never run or written; all checks ran with `python3 -B` / `PYTHONDONTWRITEBYTECODE=1` from the scratchpad (`check1.py` .. `check4.py`). The frozen-folder fingerprint is unchanged after the review (3067 files, `eb109be969176412...`). Nothing in the project was modified.

Findings are ordered most severe first. "Changes a reported number" follows the project rule that result-changing fixes are logged, not applied.

---

## 1. Fixed-lag rule uses labor data that had not been published at two decision dates (Oct and Nov 2025 shutdown)

- **(a) Where:** `analysis/data.py:179-211` (`signals`, `to_decision` with `JOLTS_LAG=2`, `CES_LAG=1`; `params.py:62-63`); documented in `analysis/v2_spec.md` §1 and `analysis/output/data_vintage.md`.
- **(b) What the code does:** for every decision month d it assumes JOLTS month d−2 and CES month d−1 are known at the end of d. Historical values are revised FRED data (option c), so there is no per-month availability check.
- **(c) Why it is wrong:** the Oct–Nov 2025 federal shutdown delayed BLS releases. Verified from ALFRED vintages (read-only web queries, `alfredgraph.csv?vintage_date=...`):

  | Decision (end of) | Rule assumes | Latest actually published (ALFRED vintage) | Status |
  |---|---|---|---|
  | 30 Oct 2025 | CES Sep 2025 | CES (CEU0500000007) latest = **Aug 2025** at 2025-10-30 | **not yet published** |
  | 28 Nov 2025 | CES Oct 2025 | CES latest = **Sep 2025** at 2025-11-28 | **not yet published** |
  | 28 Nov 2025 | JOLTS Sep 2025 | JTSJOL latest = **Aug 2025** at 2025-11-28 | **not yet published** |
  | 30 Dec 2025 | JOLTS Oct 2025 / CES Nov 2025 | Oct 2025 / Nov 2025 | fine |
  | 30 Jan 2026 | JOLTS Nov 2025 | Nov 2025 | fine |
  | 31 Oct 2013 (control, 2013 shutdown) | JOLTS Aug 2013 | Aug 2013 | fine |

  So the scores for earning months **Nov 2025 (W, F5) and Dec 2025 (F1–F5, W, and T)** use observations released after the decision. These two months sit in the `test`, `full`, `post-2010` and `last 18m` windows, so they enter every v2/v3 table, the forward-looking V2d `last 18m` Sharpe (2 of 18 months), and the D1–D3/R8 regime splits. The frozen study's primary ASOF variant handled this correctly (vintage view bounded at the cutoff); the frozen FIXEDLAG variant shares the issue, and `data_vintage.md` reports that v2 reproduces FIXEDLAG. No file in `analysis/`, `docs/` or `report/main.tex` mentions the shutdown or release delays (grep for "shutdown", "delay", "not yet published" returns nothing).
- **(d) Severity:** MAJOR (a documented "known at the decision" claim is false for two months; the effect on point estimates is small because it is 2 of 142 test months).
- **(e) Changes a reported number:** YES (small) for every v2/v3 statistic whose window contains Nov–Dec 2025; the confirmatory numbers are untouched.
- **(f) Fix:** do not re-run. Log it: add a dated paragraph to `data_vintage.md` and the report's limits ("Fixed-lag construction; at the Oct and Nov 2025 decisions the fixed-lag months were released late; the as-known rule would have carried Aug/Sep 2025 values forward for 2 of 142 test months"). For any future re-run, implement the frozen ASOF availability rule (latest month with `realtime_start <= cutoff`, via ALFRED vintages per month-end) or, at minimum, hard-code the two exceptions. Note: the same caveat applies to the warm-up months Apr 2002–mid 2002 (JOLTS was first published in 2002) but those only feed the expanding s.d. before the research window, exactly as in the frozen pseudo-real-time research period.

## 2. Test-window statistics of V2a–V2d are slices of a continuous May 2004 run; the confirmatory A3 ledger starts cold in Nov 2014

- **(a) Where:** `run.ipynb` cell 38 (`D.backtest(score.reindex(full_months), ...)`), cell 39 (`LEDGERS[(v,10)].loc[idx]`), cell 20 (D4 table), cell 76 (R11), `results/build_results_book.py:359-368` (scoreboard).
- **(b) What it does:** one backtest per variant over 2004-05..2026-08; windows are `.loc` slices. The sealed frozen ledgers were produced by running `backtest` on the test months only, so the first H−1 months ramp up from zero (1/3, 2/3 of the book) and pretrade weights start at zero.
- **(c) Why it matters:** in the test slice the book is already fully invested and carries drift from Oct 2014. Verified with the frozen backtest (scratchpad `check4.py`): V2d test Sharpe **+0.293 (slice) vs +0.277 (cold start, frozen sealed convention)**, net p.a. 2.56% vs 2.41%, 12 months differ; V2a +0.164 vs +0.163 (3 months differ). The scoreboard, D4 and R11 put the two conventions side by side without saying so (D4's note does say the momentum run is continuous).
- **(d) Severity:** MINOR. It is exactly what `v2_spec.md` §4 pre-declared ("windows are slices of that one ledger"), so it is a disclosure point, not a bug.
- **(e) Changes a reported number:** NO (fix is a footnote). Switching to cold starts would change V2d test Sharpe by −0.016.
- **(f) Fix:** add one sentence to the scoreboard caption and the report's method section: "A3 test figures start from an empty book in Nov 2014; v2 figures are the test slice of a continuous run (V2d: +0.29 vs +0.28 if started cold)".

## 3. `v2_spec.md` points at module hashes that no longer match the working tree

- **(a) Where:** `analysis/v2_spec.md` lines "Code at freeze (commit a56e6ce): params.py sha256 1d9617..., data.py 5275fe..., stats.py 8e02fc..." and "Signals (exactly `analysis/data.py::signals` at the commit above)".
- **(b) What happened:** `git diff a56e6ce HEAD -- analysis/{params,data,stats}.py` shows 20 insertions / 4 deletions made for the v3 battery (commit 925fdee): `signals(..., groups=None)` plus one line inside the loop, `P.SEED`, `factor_attribution(..., lags=P.HAC_LAGS)`, and new `block_bootstrap_sharpe`. Current hashes: params `4a73bed2...`, data `5f178457...`, stats `942fa12f...`. All three differ from the spec.
- **(c) Why it matters:** the spec's code pointer is the only link between "what was frozen" and "what ran". The v2 outputs still byte-match `v2_run_log.md` (verified), so the results did not change, and the diff is additive, but a reader cannot verify this from the spec alone; the notebook does not assert module hashes.
- **(d) Severity:** MINOR (reproducibility/documentation).
- **(e) Changes a reported number:** NO.
- **(f) Fix:** append to `v3_run_log.md` (or a new `analysis/output/code_hashes.md`) the module hashes at 925fdee and at HEAD with the one-paragraph diff summary above; optionally have cell 36/54 print the three hashes so each run records them. Do not edit `v2_spec.md` (it is hashed).

## 4. Results Book hard-codes the retracted "607 / 905 calls" figures, contradicting its own verified claim A06

- **(a) Where:** `results/build_results_book.py:502` and `:531` (literal text "(607 calls)" / "(905 calls)"); rendered in `results/RESULTS_BOOK.md:164` and `results/results_book.tex:111`. Also the A06 note at `:233` says "docs/process/project_rules.md states 607 and 905", which is stale (docs/process/project_rules.md now says 199/294 and explains the double count).
- **(b) What it does:** claim A06 counts 199 and 294 from `agents/log.jsonl` and is marked verified, while section 5 of the same book prints 607/905 from docs/process/project_rules.md's old text.
- **(c) Why it matters:** a number in the Results Book without a `% src` that is known to be wrong. `report/main.tex` does not contain 607/905 (checked), so the report itself is clean.
- **(d) Severity:** MINOR (report-facing, not analytical).
- **(e) Changes a reported number:** NO analysis number; yes for the Results Book text.
- **(f) Fix:** replace the literals with the `counts` already computed for A06 (e.g. f-string), update the A06 note, rebuild `results_book.pdf`.

## 5. Deflated Sharpe uses a null trial variance (1/T), not the Bailey–López de Prado cross-trial variance

- **(a) Where:** `analysis/stats.py:97-109`; `v2_spec.md` §5 item 11; `v3_spec.md` §1.
- **(b) What it does:** `sr0 = sqrt(1/T) * [(1−γ) Φ⁻¹(1−1/N) + γ Φ⁻¹(1−1/(Ne))]`, N = 112 (v2) or 132 (v3), then DSR = Φ[(SR−SR0)·√(T−1)/√(1 − γ₃SR + (γ₄−1)SR²/4)]. The formula, Euler constant, raw-kurtosis convention and √(T−1) placement were checked against an independent implementation (identical to 1e-8: V2d test DSR 0.0556; benchmark annual Sharpe 0.75 at N=112, 0.76 at N=132). The frozen `stats.deflated_sharpe` instead uses `std(trial Sharpes)`.
- **(c) Why it may mislead:** V[SR] in BLdP is the dispersion of the trials' estimated Sharpe ratios; 1/T is its value only if every trial has zero true Sharpe and trials are independent. With correlated trials (the 108 looks are mostly ICs of nested signals on the same sample) the effective N is smaller and 1/T overstates the dispersion; with heterogeneous true Sharpes it understates it. The choice is documented and pre-declared, so this is an interpretation caveat. Also: because var = 1/T, the `last 18m` benchmark uses T = 18 and the DSR there is not meaningful (spec already says not to interpret the 18-month alpha; say the same for DSR).
- **(d) Severity:** MINOR.
- **(e) Changes a reported number:** NO (keep as declared); any alternative would be a new look.
- **(f) Fix:** one sentence in the report: "trial variance set to its null value 1/T because the earlier looks were ICs; the benchmark is therefore a convention, not an estimate of the family's dispersion."

## 6. `perf()` has no contiguity guard; max drawdown would be wrong on gapped windows

- **(a) Where:** `analysis/stats.py:53-63`; callers `run.ipynb` cell 54 `perf_window` (R4 `test_idx.difference(pandemic)`, R8 regime months via `reindex(sel)`).
- **(b) What it does:** `wealth = (1+total_net.dropna()).cumprod()` compounds whatever months are present. The frozen `performance()` returns NaN for `max_drawdown` when the index is not a consecutive monthly range.
- **(c) Why it matters:** latent only. R4 and R8 do not print `max_dd`, and the Sharpe/mean on gapped months is a descriptive statistic the spec asked for. If someone later adds `max_dd` to those tables it would be silently wrong.
- **(d) Severity:** MINOR (latent).
- **(e) Changes a reported number:** NO.
- **(f) Fix:** mirror the frozen guard: `max_dd = ... if ledger.index.equals(pd.period_range(min,max,'M')) else np.nan`.

## 7. Byte-identity run logs and the fingerprint are brittle across machines

- **(a) Where:** `run.ipynb` cells 39, 50, 80, 82 (`sha256(csv) == recorded`), cell 7 (`frozen_fingerprint` counts every file), `requirements.txt` (loose pins), `data.py:133-150` (`download_alfred` called on every run, cell 46).
- **(b)/(c):** the CSVs are written with full float repr, so a different BLAS (Accelerate vs OpenBLAS) or scikit-learn version can change `LedoitWolf` output in the last bits and trip `stop()` even though nothing material changed; `requirements.txt` has no upper bounds and does not list `requests` (imported by the frozen `data.py`, present here only transitively via jupyter); the fingerprint fails if a `.DS_Store` or `__pycache__` appears in the frozen folder (none present now; that strictness is deliberate and good, but should be stated); `download_alfred()` touches the network when a vintage file is missing (all 78 present). The notebook-level matmul `RuntimeWarning` filter in cell 2 is justified by the Gate 1 match but hides any future genuine overflow.
- **(d) Severity:** MINOR.
- **(e) Changes a reported number:** NO.
- **(f) Fix:** record the exact environment (`pip freeze`) next to the run logs; add `requests` to `requirements.txt`; state in the README that the byte-identity check is expected to pass only in the recorded environment and that a mismatch in the 1e-15 range should be investigated, not worked around.

## 8. Readability and dead code (NIT)

- `run.ipynb` cell 78: `'sharpe': 12 * dsr['monthly_sharpe'] * np.sqrt(12) / 12` is `np.sqrt(12) * monthly_sharpe`.
- `run.ipynb` cells 46 and 48 import `shutil`, `tempfile`, `Path`, `LedoitWolf` mid-notebook, against the "first section is Imports" convention.
- `run.ipynb` cell 48 re-implements the frozen tranche / beta / Ledoit–Wolf / scale logic (`tranche()`, `BETAS`, `cov`, `scale`). Necessary, because the frozen `backtest` needs realised returns for the earning month, but it should say so in a comment and ideally compare one historical month against the frozen weights as a self-test.
- `analysis/data.py:51` `saved_json`, `:218` `cszscore`, `analysis/stats.py:112` `window` are never called (checked against the notebook source).
- `analysis/data.py:206-207` comment says T uses "the latest month <= d−2 with both V and U observed (frozen rule)"; the frozen ASOF rule is "latest month with both observed as known at the cutoff", which is d−2 in practice. Fine, but say "fixed-lag analogue of the frozen rule".
- `results/build_results_book.py:544`: `open(TAB / 'd10_agent_design.csv').read().replace(',', ' | ')[:0]` evaluates to `''` (dead expression).
- `analysis/output/data_vintage.md`: "the same test IC under ASOF (−0.0213) and FIXEDLAG (−0.0213) ... so the conclusions are not sensitive" — true for the IC; the Sharpe differs (−0.58 vs −0.53, claim C20). Say "IC identical, Sharpe −0.58 vs −0.53".
- `analysis/README.md` says `run.ipynb` is "data → Gate 1 → diagnostics D1–D10 → v2 variants → forward test"; it now also runs the v3 battery and Gate 2.

---

## Checked and found correct

- **Signal timing** (`check1.py`): for earning month m = 2019-07, F2 equals the standardised 12-month change of the 3-month-average hires rate at JOLTS observation month 2019-04 (= d−2 with d = 2019-06), and W uses CES 2019-05 (= d−1). The signal index runs from earning month 2002-05; first non-NaN W is 2004-04 (24-month s.d. warm-up), one month before the research window.
- **Tightness T**: UNEMPLOY has exactly one gap (Oct 2025). `np.log(V/U).ffill()` then lag 2 gives T(earning Jan 2026) = ratio(Sep 2025), i.e. the latest earlier month with both series, as the frozen rule; no forward value leaks.
- **`horizon_target(h)`** at m covers m..m+h−1 (verified for h=3); **`industry_momentum`** at m covers m−12..m−2 (verified); the forward `mom_formula` reproduces `F['IndMom']` for 2026-08 (asserted in cell 48).
- **Windows**: research 125, test 142, full 268, post-2010 200, last 18m 18 months; Oct 2014 excluded from research and test, as in the frozen study.
- **Backtest wrapper**: `D.backtest` passes only `holding` and `cost_bps`; longs/shorts 3, 60-month window, 36-month minimum, 10% target, gross cap 2, 2 bp hedge all come from the frozen `params.PORTFOLIO` (asserted equal in Gate 1). `signal_available` semantics match the frozen `score.loc[usable]` convention. The wrapper reproduces `v2_monthly_net.csv` exactly for V2a and V2d; Gate 1 reproduces the sealed A0 ledger to 1e-16 and 50 saved ledgers' gross returns to 1.5e-16.
- **`hac`**: identical to statsmodels OLS with `cov_type='HAC', maxlags=6, use_correction=True` on both the IC series (t = 2.035563) and the 7-factor regression (alpha t = −1.855802); the calendar zero-fill for gapped windows matches the frozen `hac_regression`.
- **`rank_ic`** equals `scipy.stats.spearmanr` month by month.
- **`perf`**: Sharpe = √12·mean/sd on net excess returns; drawdown on funded wealth with peak floored at 1, as frozen.
- **`placebo`**: `np.roll(s, k)` moves row 0 to row k (verified); shifts 24..n−24 inclusive (95 for the test window), same range as the frozen `circular_placebo`; actual IC computed with the same estimator as the shifted ones.
- **`block_bootstrap_sharpe`**: blocks are contiguous and wrap modulo n (first block of draw 0: indices 84..95 then 1); deterministic under seed 230; 5,000 draws; interval [−0.068, +0.650] matches `v3_r9_bootstrap.csv`.
- **Deflated Sharpe** formula matches an independent implementation (see finding 5).
- **Forward book**: decision Sep 2026 → earning Oct 2026; JOLTS Jul 2026, CES Aug 2026, from the ALFRED 2026-09-29 vintage; truncated-vintage equality check is a genuine test that no later observation is used; beta/LW window Sep 2021–Aug 2026 (60 months ending m−2); momentum Oct 2025–Aug 2026. Spec, amendment and book hashes match their `.sha256` records; timestamps order spec < v2 run < amendment < book.
- **Hashes and logs**: all 5 v2 and 14 v3 table hashes match their run logs; `v2_spec`, `v3_spec`, `spec_frozen`, `spec_amendment_001` hashes match; frozen fingerprint (3067 files) unchanged; no `__pycache__`/`.pyc` in the frozen folder.
- **Drop-one (R7)**: `signals(groups=...)` standardises on 12 groups with the 11-group minimum, matching the frozen `drop_group_diagnostic`; reduced `relative` returns are recomputed on 12 groups.
- **V2b signs** are learned on research months only and held fixed under the placebo shift.
- **Reading rules** in cells 39 and 78 implement v2_spec §6 and v3_spec §3 literally.
- **Figures**: ±2 s.e. bars use the HAC s.e.; colours follow docs/process/project_rules.md; no custom fonts.

## Overall assessment

The analysis code is small, faithful to the frozen study (every estimator and the backtest reproduce the sealed outputs to machine precision) and unusually well guarded by hashes, run logs and gates. The one substantive problem is that the fixed-lag rule silently assumes publication dates that the Oct–Nov 2025 shutdown broke, so two test months use data released after the decision; this changes v2/v3 numbers only marginally but must be disclosed, and the comparability of continuous-run slices with the cold-start confirmatory ledger should be stated once. Everything else found is documentation drift (spec code hashes, 607/905 calls) or minor hygiene, none of which alters a reported result.
