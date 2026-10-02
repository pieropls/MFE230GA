Scope: only the supplied material. I did not verify live FRED data. I mark each item as confirmed (visible in the text) or as a question or limitation.

**Confirmed errors: mapping and manifest**

1. **Manifest rows for CEU5500000007 and CEU5500000008 with group 10 duplicate the group 9 rows.** The same series ID is mapped to two groups, and group 10 (Real estate) has no distinct CES series. The crosswalk repeats CES 55000000 for both groups.
   - Consequence: groups 9 and 10 get identical employment features, and the group 10 label overstates coverage. Financial activities (CES 55) includes real estate, rental and leasing, so group 9's "Finance and insurance" mapping is also approximate.
   - Test: group the manifest by `id` and assert one group per series. Compare the feature columns of groups 9 and 10, which will be identical.
   - Related: `series_map().drop_duplicates('series_id')` in `build_asof_panel` keeps only the first row, so group 10's CES series silently vanishes from the panel, or carries group 9's label. Test: count the distinct groups per series in the output panel.

2. **Group 10 rows have `mapping_quality` "exact" for the JOLTS series and flags "shared CES", while the crosswalk says `match` = "shared CES with group 9".** Group 9 CES rows are flagged "CES financial activities" but are not marked approximate. The `mapping_quality` column for the CES rows (groups 9 and 10) is "exact", which contradicts the flags. The same applies to these rows:
   - CEU4300000007/8 (group 7), flagged "CES excludes utilities" but marked "exact".
   - CEU6500000007/8 (group 12), flagged "includes private education" but marked "exact".
   - CEU7000000007/8 (group 13), flagged "includes leisure" but marked "exact".
   - CEU3200000007/8 (group 4), flagged "Hshld approximate" but marked "exact".
   - Consequence: any gate that filters on `mapping_quality == exact` will wrongly admit these.
   - Test: assert that `mapping_quality == 'exact'` implies flags contain no scope caveat.

3. **Group 7 CES code.** CEU4300000007 is Transportation and warehousing (CES 43), and utilities are CES 44. The crosswalk gives 43000000 for a "Transportation, warehousing and utilities" group. The JOLTS code 480099 is the correct combined series. Test: compare the CES series titles with the group name.

4. **Group 8 (Information) mapping.**
   - The manifest uses CES 50000000 for JOLTS 5100 (Information). Test: fetch the series titles and confirm they match.
   - The F6 note says Information has "partial scope".
   - The Census check gives Telcm as the only French portfolio for Information, so the mapping is partial although labeled "exact".

5. **Group 2 CES mismatch.** CES2000000008 is the seasonally adjusted series (prefix CES), while every other series in the file is not seasonally adjusted (CEU). Mixed seasonal treatment within a panel is a mapping error, and it is flagged only as an "exception".
   - Consequence: the adjusted series is revised, and the seasonal factors use future data.
   - Test: assert a uniform seasonal-adjustment status across all series.

6. **CES code 41420000 (group 5)** is Wholesale trade, but its dates and column meanings need checking. Also, group 4's CES code 32000000 and group 3's 31000000 use the pattern CEU3100000007 and CEU3200000007, which are fine. Nothing further to confirm here.

7. **Start dates.**
   - CEU3100000007/8 and CEU3200000007/8 start in 1939, and all the CES series start well before 1990, though `first_vintage` is 2011-03-04. First vintage is the publication date in ALFRED. The JOLTS `first_vintage` of 2010-08-11 is consistent with ALFRED's history, but the original JOLTS start of 2000-12 is not a vintage date.
   - The manifest lists `UNEMPLOY` first_vintage 1961-02-09 as "live confirmed". The reason field says "cached vintage audit; live first-vintage date confirmed". This is a claim I cannot verify, but the identical dates across all series (2010-08-11 for every JOLTS, 2011-03-04 for every CES) suggest the archive's coverage start rather than true first release dates.
   - Consequence: if the code treats `first_vintage` as the first release, it is a look-ahead source.
   - Test: compare the minimum `realtime_start` in each vintage file with the manifest value.

8. **Observation_end 2026-08-01 for CES and 2026-07-01 for JOLTS.** The Census check runs at 2026-09-29. A CES value for August 2026 would be released in early September, so this is plausible. But the manifest `observation_end` is an end date from the latest vintage, not a point-in-time property. Limitation, not a confirmed error.

9. **Ken French rows.** The `industry` row lists start 1926-07 and end 2026-08 with `first_vintage` empty. Ken French files are revised in place with no vintages, so these are not point-in-time (limitation). Their end date of 2026-08 is a data-library date, not a known-at date. Test: check the download date against the last return date.

10. **Ken French excluded portfolios.** Agric is excluded because it is outside nonfarm JOLTS. Other, Boxes, Books, Softw, Fun and PerSv are excluded as ambiguous. Note that the membership for group 5 (Whlsl) is "exact", but the Census check reports 73 of 285 correspondence rows as outside scope. This contradicts "exact". The Census assessment gives every group "Approximate SIC portfolio proxy", while the crosswalk marks most groups "exact". Test: compare the `match` column with the assessment field.

11. **The Census JSON `outside_scope_portfolios` lists every French portfolio for groups 2, 5, 6, 7, 8, 10, 11, 12 and 13.** For example, group 7 lists only "Trans", but the crosswalk's membership includes Util as well. Test: verify that every crosswalk French member appears in some Census row. Util is missing entirely, which suggests the check omitted it, and the group 7 "utilities" scope goes unchecked.

12. **Group 1 mapping.** French members "Gold Mines Coal Oil" appear in the crosswalk. Logging is not covered at all (there is no French portfolio for logging, and the Census check does not flag it), and JOLTS 110099 includes logging. Oil is also a poor match for mining and logging.

**Confirmed errors: code**

13. **`vintage_view(..., first=True)`** drops duplicates before filtering by cutoff. That is correct for first release, but the `first` variant compares `realtime_start <= cutoff` after picking the earliest row per observation, so observations whose first release comes after the cutoff are dropped. This is the desired behavior. However, the `first_release` view uses `bound = decision.to_period('M') - 1` for the observation month, which allows an observation that was not yet published. Because of the assertion `release_date <= cutoff`, this is caught only for rows that exist.

14. **The overlap check in `read_vintage`** uses `realtime_end >= next_start`. ALFRED intervals are inclusive, so the next `realtime_start` is typically the day after `realtime_end`. That is fine. But `realtime_end` of "9999-12-31" is compared as a string, which works. Limitation only.

15. **`replace('.', np.nan)`** on string dtype is correct. But `pd.PeriodIndex(frame.date, freq='M')` runs before the date-format validation, so malformed dates raise a different error first. Minor, and the check ordering is a bug only in error reporting.

16. **Research-period look-ahead.** In the research branch, `view = snapshot` uses the frozen snapshot, which contains revised values as of `P.RESEARCH_SNAPSHOT`. For decisions before `FIRST_SEALED_DECISION` the features use fixed-lag revised data, not as-known data. The label is "frozen_snapshot_fixed_lag", and that is disclosed. But `bound = decision.to_period('M') - item.lag` uses `item.lag` while the vintage branches use `-1`. Test: for a JOLTS series with a two-month real lag, confirm that `-1` admits an unpublished month in the ASOF, FIRST and REVISED variants.

17. **REVISED variant.** `view = latest` uses fully revised data for the whole history (intentional hindsight). The `bound` is derived from `actual.index.max()`, the last month known at the cutoff. That is coherent. But `latest` values for months at or before that bound carry a `release_date` from the latest vintage, so the research assertion is skipped for them. This is acceptable for a labeled hindsight variant.

18. **The research-branch assertion** `release_date <= P.RESEARCH_SNAPSHOT` compares strings. It holds only if `RESEARCH_SNAPSHOT` is an ISO string. If it is a `Timestamp`, this raises a TypeError. Test: run with the actual type.

19. **`cutoff = decision - pd.Timedelta(days=1)`** assumes `decision` is the month-end timestamp. If decisions are month-end dates, the cutoff is the day before, so data released on the decision day is excluded (conservative). But `decision.to_period('M')` then places the decision month at the same month as the observation bound, and `-1` allows the previous month, which has not been released for JOLTS (it lags about 5 weeks). The assertion would catch this for ASOF only if such rows exist; the view filter already prevents them.

20. **`vintage_view` for `first=False`** uses `realtime_end >= cutoff`. An observation revised on the cutoff day has two rows whose intervals do not overlap under the read-time check, so the result is one row. That is fine.

21. **Empty results.** If `result` is empty, `result.loc[known,'release_date'] <= ...` still works. Not a bug.

22. **`series_map().drop_duplicates('series_id')`** is the concrete code bug behind item 1: it discards the group 10 rows. If downstream code keys on group, group 10 has no CES series.

**Timestamps and PIT (optional PPI file)**

23. **`diagnostic`:** three PPI series have `first_vintage` 2015-04-14 with `known_at_research_snapshot` false. The BLS source notices are dated 2007 (new aggregate net output indexes). Group 8's `PCUAINFOAINFO` is listed in the diagnostics although its `exact_scope` is false. Likely an inconsistency: three diagnostic series but only two exact-scope groups. Test: confirm why Information appears.

24. **The PPI admission counts.** `exact_scope_groups` = 2 and `required_groups` = 9, consistent with F6. F6 says "two exact sector matches", also consistent.

25. **Timestamps.** The manifest and F6 refer to "research snapshot" first vintages, while the Census check and PPI audit are dated 2026-09-29. If the research snapshot predates these, no look-ahead arises. That cannot be confirmed without `P.RESEARCH_SNAPSHOT`.

**Questions and limitations**

- What are `P.FEATURE_START`, `P.LAST_RETURN`, `P.FIRST_SEALED_DECISION` and `P.RESEARCH_SNAPSHOT`? All three timing branches depend on them.
- `item.lag` is not defined in the supplied material.
- The `admitted` flag is True for group 9 and 10 CES series despite the caveats, so the manifest gate is not enforcing the mapping quality.
