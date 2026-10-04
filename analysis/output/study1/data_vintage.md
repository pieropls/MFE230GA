# Data vintage used in this iteration

Written by analysis/run.ipynb on 2026-10-04T10:22:02+00:00.

**Choice: option (c)** of the iteration task, Part 1 step 2.

- (a) As-known (ASOF) panels saved in the frozen repo: **not available**. The repo contains 0 parquet files; its package_manifest.json lists the panels as omitted.
- (b) ALFRED vintages with `analysis/.env` FRED_API_KEY: **not available** (no key file).
- (c) Revised FRED data downloaded 3 Oct 2026 from fredgraph.csv, with fixed publication lags (JOLTS month d-2, CES month d-1, tightness month d-2): **used** for every historical result in this iteration.

**Known exception, found in the 3 Oct 2026 code review and left uncorrected.** The fixed lags assume the usual BLS release calendar, which the federal shutdown of 1 Oct to 12 Nov 2025 broke. Checked against ALFRED vintages by the reviewer: at the 31 Oct 2025 decision the latest published CES month was Aug 2025 (the rule assumes Sep); at the 28 Nov 2025 decision the latest CES month was Sep 2025 and the latest JOLTS month Aug 2025 (the rule assumes Oct and Sep). Earning months Nov 2025 (W, F5) and Dec 2025 (F1-F5, W, T) therefore use values released after the decision. The frozen study's as-known (ASOF) variant handled this correctly; its FIXEDLAG diagnostic shares the issue. Correcting it would change v2/v3 numbers after their run logs were frozen, so it is logged in docs/OPEN_ISSUES.md instead; any future run should apply the ALFRED availability rule.

The forward-test book (Part 3) does not use (c). It uses ALFRED values *as published on 2026-09-29*, downloaded without a key from alfredgraph.csv, so it only contains data known before the 30 Sep 2026 decision.

## How close is (c) to the frozen study's own signals?

Our rebuilt A0 composite (same transforms) against the frozen study's saved sealed A0 scores, Nov 2014 to Aug 2026:

| saved A0 variant | pooled_corr | mean_monthly_rank_corr | same_top3_share |
|---|---|---|---|
| FIXEDLAG | 0.998 | 0.992 | 0.908 |
| ASOF | 0.918 | 0.863 | 0.415 |
| REVISED | 0.991 | 0.979 | 0.859 |
| FIRST | 0.851 | 0.78 | 0.239 |

Our data is the FIXEDLAG construction (revised values, fixed lags), and it reproduces the frozen FIXEDLAG scores almost exactly. As-known (ASOF) data picks the same top three industries in only 42% of months, so revisions do change portfolio membership. The frozen study's primary A3 had the same test IC under ASOF (-0.0213) and FIXEDLAG (-0.0213) and a test Sharpe of -0.58 against -0.53 (results.json), so the verdict is not sensitive to this choice, but monthly holdings and the size of the loss are. Every historical number in this iteration is therefore labelled as computed on revised data.
