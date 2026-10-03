# Audit of the Supplied JOLTS/CES/French Material

"Confirmed" means the problem can be shown from the supplied material alone. "Likely" items need an outside check. "Question" items depend on code or config that was not supplied (`series_map`, `month_end_decisions`, `P.*`).

---

## A. Confirmed errors

**1. Research-period rows are revised data, labelled with the requested variant (look-ahead).**
- **Where:** code lines `if research: view = snapshot; bound = decision.to_period('M') - item.lag` and `rows.append((decision, …, variant, label, …))`.
- **Why it is wrong:**
  - For every decision before `FIRST_SEALED_DECISION`, all variants use the vintage as of `P.RESEARCH_SNAPSHOT`. This includes `ASOF` and `FIRST`.
  - A decision in 2005 therefore uses values that include later revisions and benchmarks. Its `release_date` can be years after its `cutoff`.
  - The `variant` column still says `ASOF`. Only the `timing` column reveals the substitution.
  - The research-period assertion `release_date <= P.RESEARCH_SNAPSHOT` cannot fail, because `vintage_view` already filters on `realtime_start <= snapshot`. Nothing compares research rows to their own cutoff.
- **Test:**
  - Build the panel and select rows with `timing == 'frozen_snapshot_fixed_lag'`. Check `(r.release_date > r.cutoff).sum() > 0`.
  - For research decisions on or after the first vintage, compare snapshot values with `vintage_view(history, cutoff)` values.
  - Confirm that research rows in `panel_asof` and `panel_revised` are identical.

**2. Rows labelled "first release" (and as-of rows) for early months are actually the series' first ALFRED vintage.**
- **Where:** `vintage_view(..., first=True)`, line `frame.drop_duplicates('observation_month', keep='first')`, together with the manifest `first_vintage` values (2010-08-11 for JOLTS, 2011-03-04 for CES).
- **Why it is wrong:**
  - For observation months from 2000-12 to about mid-2010 (JOLTS) or early 2011 (CES), the earliest row's `realtime_start` is the series' first vintage date.
  - Those values had already been through years of revisions. For JTSJOL, UNEMPLOY's peers and CES2000000008, they had also been through seasonal re-estimation.
  - They still pass the `release_date <= cutoff` assertion and receive the label `first_release`.
- **Test:**
  - Run `h = read_vintage('JTU2300JOR'); f = vintage_view(h, '2016-01-30', first=True)`.
  - Count `f.realtime_start.eq(h.realtime_start.min())`. Expect about 115 censored months for JOLTS.
  - Repeat for a CEU series.

**3. Manifest row `CES2000000008` (group 2, E) is seasonally adjusted inside an unadjusted panel.**
- **Why it is wrong:**
  - All other sector series are JTU or CEU, which are not seasonally adjusted. Group 2 therefore pairs unadjusted hours (`CEU2000000007`) with adjusted earnings.
  - The row is still labelled `mapping_quality = exact`.
  - In the `latest`, snapshot, REVISED and FIXEDLAG views, adjusted values carry seasonal factors estimated with later data. The unadjusted sibling series have no such look-ahead channel.
  - Its `first_vintage` (2011-03-04) matches the unadjusted rows exactly, which suggests it was copied.
- **Test:**
  - Check that `manifest.query("group>0 and measure in ['H','E']").id.str.startswith('CEU').all()`. It fails on this row.
  - In the cached vintage files, compare how often February vintages revise observations more than 24 months old: CES2000000008 versus CEU2000000007.
  - Check that `min(realtime_start)` in the file matches the manifest.

**4. The `prescribed_match` and `mapping_quality` labels contradict the scope audit.**
- **Where:** crosswalk groups 1, 2, 3, 5, 6, 8 and 11 are marked `exact`. Yet:
  - Every group has `verified_French_scope = Approximate`.
  - The Census audit finds out-of-scope rows in all 13 groups. Examples: group 1 has 3 of 4 portfolios out of scope; group 3 has 9 of 14; group 11 has 77 of 162 rows.
  - The manifest copies `exact` onto the JOLTS and CES series.
- **Group 4 is wrong in the other direction:**
  - It is labelled only `Hshld approximate`, but the audit flags 7 portfolios.
  - That French-side caveat is stamped on `CEU3200000007/08`, even though CES 32000000 is an exact match for nondurables.
  - The group-4 JTU rows meanwhile say `exact`.
  - In short, one column is mixing the JOLTS↔CES match with the JOLTS↔French match.
- **Test:**
  - `cw[(cw.prescribed_match=='exact') & (cw.outside_scope_rows>0)]` should be empty. It returns 7 groups.
  - Derive a CES-only quality label from `CES_code` versus `JOLTS_code` and compare it with the manifest.

**5. Groups 9 and 10 share the same CES series, and the code drops the duplicate.**
- **Where:** the manifest IDs `CEU5500000007` and `CEU5500000008` each appear twice (groups 9 and 10). In the code, `series_map().drop_duplicates('series_id')` keeps only the first occurrence, along with its `lag` and group attributes.
- **Why it is wrong:**
  - The hours and earnings features for groups 9 and 10 are identical, so CES adds no information to separate them.
  - CES 55000000 combines NAICS 52 and 53, so each group is contaminated by the other.
  - Group 10's CES rows survive only if the downstream code rejoins through the full manifest.
- **Test:**
  - `manifest.id.duplicated().sum()` should be 0. It is 2.
  - After the downstream join, count rows for (group 10, H) and (group 10, E).
  - The correlation between group 9 and group 10 features should equal 1.

**6. Vintage-interval validation catches overlaps but not gaps or unterminated final intervals.**
- **Where:** `read_vintage`, line `(next_start.notna() & (ordered.realtime_end >= next_start))`.
- **Why it is wrong:**
  - The code never checks that `realtime_end + 1 day == next realtime_start`.
  - It never checks that each month's last interval ends `9999-12-31`.
  - If there is a gap, the observation silently disappears from the as-of view on cutoffs inside the gap.
  - If the final interval is closed, `latest` (`keep='last'`) returns a withdrawn value.
- **Test:** feed a synthetic file with intervals [2012-01-06, 2012-02-02] and [2012-02-10, 9999-12-31]. It currently passes; it should raise. Also assert that `groupby('observation_month').realtime_end.last() == '9999-12-31'` for every month.

**7. The duplicate-key check uses the wrong key (low severity).**
- **Where:** `frame.duplicated(['date','realtime_start'])`.
- **Why it is wrong:**
  - All downstream logic is keyed on `observation_month`.
  - The date regex does not require the day to be `01`.
  - Two dates in the same month would pass this check. They would then be treated as successive vintages of one month, or raise later with a misleading "overlapping" message.
- **Test:** assert `frame.date.str.endswith('-01').all()` and check `duplicated(['observation_month','realtime_start'])`.

**8. The French archives are called "pinned" but nothing pins them.**
- **Where:** manifest rows `industry`, `ff5` and `momentum`.
- **Why it is wrong:**
  - The URLs point to the live, mutable files. French restates history when CRSP data are updated.
  - No checksum or download date is recorded, unlike the Census files.
  - "Date fields checked without parsing return values" means missing-value codes (-99.99, -999) and table boundaries (value-weighted, equal-weighted, annual) are never validated.
- **Test:**
  - Record a SHA-256 and a download date for each file.
  - Parse the returns and assert none are ≤ -99.
  - Assert the monthly value-weighted table has 1,202 rows (1926-07 to 2026-08).

---

## B. Likely errors that need an outside check

**9. Fixed lags can include data not yet published (timing look-ahead, not just revisions).**
- **Where:** the research and FIXEDLAG branches, line `bound = decision.to_period('M') - item.lag`.
- **Why it is likely wrong:**
  - The REVISED branch sets its bound from actual availability. These two branches do not.
  - Delayed releases break a fixed lag of 1 (CES) or 2 (JOLTS). By my recollection, during the 2025 shutdown the September 2025 jobs report slipped to 2025-11-20, and the September/October JOLTS releases to December 2025. The 2013 shutdown caused similar delays.
  - JOLTS needs a lag of at least 2 with month-end decisions. The lag values were not supplied.
  - The label `fixed_lag_revised` does not disclose this.
- **Test:**
  - For each decision on or after the first vintage, assert `bound <= vintage_view(h, cutoff).dropna().index.max()`.
  - Inspect the 2025-10-31 and 2025-11-30 decisions in particular.

**10. Finer CES series probably exist for several groups.**
- **Where:** groups 9 and 10 (`55000000`), 12 (`65000000`) and 13 (`70000000`).
- **Why it is likely wrong:** CES publishes sector codes 55520000, 55530000, 65620000 and 70720000. For group 7, it also publishes 44220000 (utilities), which could be combined with 43000000. If production-worker hours and earnings exist for these codes with comparable vintages, the supersector mappings are unnecessary approximations.
- **Test:** check ALFRED for `CEU5552000007/08`, `CEU5553000007/08`, `CEU6562000007/08`, `CEU7072000007/08` and `CEU4422000007/08`, and compare their first vintages.

**11. The first-vintage dates are suspiciously uniform.**
- **Where:** all JOLTS rows (including JTSJOL) show 2010-08-11, and all CES rows (including the adjusted CES2000000008) show 2011-03-04. All are marked "confirmed".
- **Test:** compute `min(realtime_start)` from each cached file and compare it with the manifest.

**12. The PPI search evidence has gaps (the decision is unaffected).**
- **Group 1:**
  - The representative series is `PCU212212` (mining except oil and gas).
  - A total-mining series (likely `PCUOMINOMIN`) may exist, which would make the reason "excludes oil/gas" an artifact of the choice.
  - Logging would still be missing, so `exact_scope = false` stands.
- **Group 2:**
  - The decision text says "nonresidential", but the selected series is warehouse construction.
  - `unique_candidates = 200` exactly, which may mean results were capped at one page.
- **Overall:** the gate result (2 of 9 groups) does not change.
- **Test:** re-run the searches with pagination and search for `PCUOMINOMIN`.

---

## C. Questions that depend on unseen code or config

**13. The final `else` branch accepts any variant.**
- **Where:** the line `label = 'as_known' if variant=='ASOF' else 'first_release'`.
- **Issue:** any member of `P.VARIANTS` other than the four named ones is computed as an as-of view but labelled `first_release`.
- **Test:** `assert set(P.VARIANTS) == {'ASOF','FIRST','REVISED','FIXEDLAG'}`.

**14. Some comparisons are fragile to input types.**
- **Snapshot comparison:**
  - The line `release_date <= P.RESEARCH_SNAPSHOT` compares strings without normalising the snapshot value.
  - A `Timestamp` would raise `TypeError`.
  - A `'YYYY-MM'` value would fail even when correct (`'2014-06-01' <= '2014-06'` is False).
- **Lag type:**
  - `Period - item.lag` fails if `lag` is a float.
  - The manifest's `group` column (`1.0`) suggests such columns get converted to floats.
- **Test:**
  - Run with `pd.Timestamp(...)` and with `'2014-06'` as the snapshot.
  - Assert that `series_map().lag` has an integer dtype.

**15. Snapshot coverage is unchecked.**
- **Research decisions after the snapshot date:** if any research decision falls after `RESEARCH_SNAPSHOT`, its features silently stop at the snapshot's last month.
- **Snapshot older than the first vintage:** the PPI diagnostic implies the snapshot is before 2015-04-14. If it is also before 2010-08-11 or 2011-03-04, the snapshot is empty for JOLTS or CES, with no error raised.
- **Window between first vintages:** decisions between 2010-08-11 and 2011-03-04 would have JOLTS data but no CES data.
- **Test:**
  - For each research decision, compare the maximum observation month with `bound`.
  - Assert the snapshot is non-empty for every admitted series.

---

## D. Limitations (disclosed or design choices, not errors)

**16. Seasonal adjustment is mixed across levels.** The national series JTSJOL and UNEMPLOY are seasonally adjusted, while the sector JTU and CEU series are not. The adjusted series also carry the look-ahead from seasonal re-estimation described in item 3.

**17. The Census scope audit only measures one direction.**
- It counts portfolio rows that fall outside a group's scope. It does not measure how much of the group's own scope is missing. Examples:
  - Logging (SIC 2411) sits in BldMt, which is mapped to group 3, so group 1 has no logging.
  - Information's publishing and software activity sits in the excluded Books and Softw portfolios.
- It uses 2002 NAICS, while JOLTS and CES now use NAICS 2022.
- The excluded `Aux → 551114` rows belong to group 11's scope.
- **Test:** compute, for each group, the share of in-scope NAICS rows covered by the assigned portfolios.

**18. Several approximations are already disclosed.**
- Group 7: CES excludes utilities.
- Group 12: CES includes private education.
- Group 13: CES includes all of leisure and hospitality.
