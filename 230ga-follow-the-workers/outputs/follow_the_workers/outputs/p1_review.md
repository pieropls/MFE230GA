# P1 audit disposition

Current-source Sonnet audit; each finding checked without investment return analysis. The team critique remains for the students.

1. **documented_design:** Shared CES is explicitly prescribed; panel is keyed by series_id and downstream features map to both groups.584 nonmissing shared H/E pairs verified in ASOF and FIRST.
2. **claim_not_supported:** Current JOLTS flags are not shared-CES flags; CES mapping_quality contains the actual scope descriptions, not exact. Checked affected manifest rows.
3. **documented_limitation:** CES transport excludes utilities as specified and flagged. Keep prescribed series rather than invent a substitute.
4. **documented_limitation:** CES50000000 is the prescribed Information series. French Telcm is an approximate proxy; PPI Information has separately documented partial scope.
5. **documented_design:** Construction SA earnings exception is explicitly prescribed. Vintage filtering controls publication availability; seasonal adjustment alone does not establish sealed lookahead.
6. **checked_question:** Prescribed IDs, schema, dates, archive hashes and live first-vintage metadata verified. Finding identifies no concrete conflicting value.
7. **documented_limitation:** All78 live archive-inception dates match pinned minima. FIRST means earliest archived vintage, not a recovered original historical publication. Frozen research snapshot is explicitly pseudo-real-time.
8. **documented_limitation:** Manifest observation_end describes pinned file coverage; row-level release_date and cutoff control availability.
9. **documented_limitation:** French returns are a pinned current historical snapshot, not vintage returns. Numeric sealed rows remain guarded.
10. **fixed_metadata:** Crosswalk now separates prescribed_match from verified_French_scope and correspondence counts. All13 baskets are approximate; membership unchanged.
11. **claim_not_supported:** outside_scope_portfolios lists only portfolios with spillovers. Detail audit contains every prescribed member, including Util; all13 memberships checked.
12. **documented_limitation:** Fixed French industry proxies do not replicate the full JOLTS scope. Oil includes upstream extraction but also spillovers; logging coverage incomplete. No silent remapping.
13. **claim_not_supported:** Both FIRST and ASOF filter publication dates before applying the observation-month bound. No observed future-release row is admitted.
14. **checked_no_error:** Inclusive interval disjointness and ISO string comparison are checked; malformed/reversed/overlapping dates fail.
15. **nonblocking_error_message:** Period parsing may reject malformed observation dates before the explicit ISO validation. It still rejects input; no incorrect value admitted. No numerical change needed.
16. **documented_design:** Snapshot research branch is prescribed and labeled. ASOF/FIRST vintage filtering precedes month bound, so a minus-one bound cannot admit unpublished values.
17. **documented_design:** REVISED is intentionally a labeled hindsight diagnostic. It is not the ASOF strategy.
18. **claim_not_supported:** Actual RESEARCH_SNAPSHOT is an ISO string; verified value and type.
19. **checked_no_error:** Day-minus-one cutoff is the approved rule; release filter prevents unpublished JOLTS observations regardless of upper month bound.
20. **checked_no_error:** Nonoverlapping inclusive vintage intervals yield one active row; schema self-tests exercise the filter.
21. **checked_no_error:** Empty subsets are not evidence of a timestamp error; explicit model coverage gates still apply.
22. **claim_not_supported:** Same keyed-series versus group distinction as finding1. Both groups retain nonmissing H/E values downstream.
23. **documented_diagnostic:** Information is retained as a rejected-scope coverage diagnostic, not counted as an exact match or supplied to a model. Earliest archive date is not index inception.
24. **checked_no_error:** Two exact-scope groups are below the fixed nine-group model threshold.
25. **documented_design:** Snapshot2014-10-30, first sealed decision2014-10-31, feature start2002-04, endpoint2026-08; fixed source selection and vintage availability rules apply. Audit timestamp is not an economic observation date.
