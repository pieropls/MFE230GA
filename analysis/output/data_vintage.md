# Data vintage used in this iteration

Written by analysis/run.ipynb on 2026-10-03T10:33:38+00:00.

**Choice: option (c)** of ITERATION_PROMPT Part 1 step 2.

- (a) As-known (ASOF) panels saved in the frozen repo: **not available**. The repo contains 0 parquet files; its package_manifest.json lists the panels as omitted.
- (b) ALFRED vintages with `analysis/.env` FRED_API_KEY: **not available** (no key file).
- (c) Revised FRED data downloaded 3 Oct 2026 from fredgraph.csv, with fixed publication lags (JOLTS month d-2, CES month d-1, tightness month d-2): **used** for every historical result in this iteration.

The forward-test book (Part 3) does not use (c). It uses ALFRED values *as published on 2026-09-29*, downloaded without a key from alfredgraph.csv, so it only contains data known before the 30 Sep 2026 decision.

## How close is (c) to the frozen study's own signals?

Our rebuilt A0 composite (same transforms) against the frozen study's saved sealed A0 scores, Nov 2014 to Aug 2026:

| saved A0 variant | pooled_corr | mean_monthly_rank_corr | same_top3_share |
|---|---|---|---|
| FIXEDLAG | 0.998 | 0.992 | 0.908 |
| ASOF | 0.918 | 0.863 | 0.415 |
| REVISED | 0.991 | 0.979 | 0.859 |
| FIRST | 0.851 | 0.78 | 0.239 |

Our data is the FIXEDLAG construction (revised values, fixed lags), and it reproduces the frozen FIXEDLAG scores almost exactly. As-known (ASOF) data picks the same top three industries in only 42% of months, so revisions do change portfolio membership. The frozen study's primary A3 had the same test IC under ASOF (-0.0213) and FIXEDLAG (-0.0213) (results.json), so the conclusions are not sensitive to this choice, but monthly holdings are. Every historical number in this iteration is therefore labelled as computed on revised data.
