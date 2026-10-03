# STOP: forward-test data check failed (Part 3, step C)

**When:** 2026-10-03T09:06:57+00:00. The notebook halted in the cell "Forward test: data" of `analysis/run.ipynb`.

**Raw message:** `ALFRED vintage 2026-09-29 does not end at JOLTS 2026-07 / CES 2026-08 as the frozen forward spec requires: JOLTS {'2026-08'}, CES {'2026-08'}`

## What failed

`analysis/forward/spec_frozen.md` §2 was frozen at 2026-10-03T09:03:56Z (sha256 `735a8ffa…`, commit `45991d4`). It fixes the information set for the 30 Sep 2026 decision as "JOLTS rates through **July 2026**, CES through **August 2026**" and says: *"The notebook stops if any series carries an observation later than these months."*

The ALFRED vintage dated 29 Sep 2026 (`analysis/data/alfred_2026-09-29/`, 78 series) holds the following:

| Series | Last observation in the 29 Sep 2026 vintage | Spec expects |
|---|---|---|
| All 52 JOLTS industry rates and JTSJOL | **2026-08** | 2026-07 |
| All 24 CES hours/earnings series | 2026-08 | 2026-08 |
| UNEMPLOY | 2026-08 | (no limit stated) |

## Why

**August 2026 JOLTS was released on Tue 29 Sep 2026, the information-cutoff day itself.** ALFRED vintages of `JTU2300HIR` show it:

| Vintage date | Last observation |
|---|---|
| 2026-09-15 | 2026-07 |
| 2026-09-22 | 2026-07 |
| 2026-09-28 | 2026-07 |
| 2026-09-29 | **2026-08** |

The frozen study's as-known rule (`realtime_start ≤ d − 1 day`) treats a value published on 29 Sep as known at the 30 Sep decision. The forward spec instead took "JOLTS through July 2026" from ITERATION_PROMPT Part 3, assumed the release would come later, and pre-committed to stopping otherwise. The check did its job: the spec's assumption about the release calendar is wrong.

## Impact

- **V2a (headline) is not affected.** It uses only W, which comes from CES earnings (August 2026 in every option), so its Q4 book would be identical under any resolution.
- **V2b (secondary) is affected.** It uses the JOLTS signals F1–F4, so its inputs depend on which JOLTS information set you choose.
- **Nothing produced so far is affected:**
  - Parts 1 and 2: Gate 1 passed.
  - Part 3 step A: v2 spec frozen and committed (`d76fbb3`).
  - Part 3 step B: the v2 variants were run once at 09:01:55Z. A re-execution reproduced all five result files byte for byte (`v2_run_log.md`).
- **The frozen repo is unchanged:** 3,067 files, fingerprint `eb109be9…`, checked after the stop.

## Not done (because of this stop)

- Q4 2026 book (`analysis/forward/book_2026Q4.csv`), ETF proxies (`etf_proxies.csv`), tracker (`tracker.csv`).
- Gate 3. Its first condition holds already: v2 spec frozen at 09:00:13Z, before the first v2 run at 09:01:55Z. The book conditions cannot be checked until a book exists.

## Your decision (pick one; record it as a hashed amendment)

| Option | JOLTS information for V2b | Pros / cons |
|---|---|---|
| **A (recommended)** | Fixed-lag rule as in every v2 backtest: JOLTS month d−2 = **July 2026**, values as known on 29 Sep (the 29 Sep vintage, which includes July's revision published that day) | Same construction as the backtests that motivated the forward test. Uses only data published by the cutoff. Requires amending the stop condition to "no observation later than the fixed-lag month is *used*". |
| B | JOLTS **July 2026 as first published**, from the 28 Sep 2026 vintage | Matches the spec text literally. Discards a revision that was public at the cutoff. |
| C | As-known rule: **August 2026** JOLTS (latest published by 29 Sep) | Matches the frozen study's ASOF rule. Differs from the fixed-lag construction used in every v2 backtest. |

**To resume:**
1. Write `analysis/forward/spec_amendment_001.md` stating the option and the reason. Hash it and commit it.
2. Adjust the check in the "Forward test: data" cell to match (for option B, also add a 28 Sep vintage folder).
3. Delete this file.
4. Re-run `analysis/run.ipynb` from the top. The v2 run-log check guarantees the v2 results do not change.

Then let the remaining cells build the book, the ETF proxies, the tracker and Gate 3.
