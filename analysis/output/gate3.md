# Gate 3

Run 2026-10-03T09:17:55+00:00 by analysis/run.ipynb. **Result: PASS**

| check | value | pass |
|---|---|---|
| v2 spec frozen before the v2 results | spec 2026-10-03T09:00:13+00:00 < first run 2026-10-03T09:01:55+00:00 | True |
| v2 spec unchanged since freezing | ca6582347904489b | True |
| Forward spec frozen before the book was built | spec 2026-10-03T09:03:56+00:00 < book 2026-10-03T09:17:55+00:00 | True |
| Forward spec unchanged since freezing | 735a8ffa9c9c23fd | True |
| Amendment 001 frozen after the v2 results and before the book | 2026-10-03T09:01:55+00:00 < 2026-10-03T09:16:11+00:00 < 2026-10-03T09:17:55+00:00 | True |
| Amendment 001 unchanged since freezing | c76cde86a85ff703 | True |
| No observation after the fixed-lag month used (full vs truncated vintage) | identical scores, 4 variants | True |
| V2a book weights net to zero | sum = +0.0e+00 | True |
| V2a book has 3 longs and 3 shorts | 3 long, 3 short | True |
| V2b book weights net to zero | sum = +1.1e-16 | True |
| V2b book has 3 longs and 3 shorts | 3 long, 3 short | True |
| V2c book weights net to zero | sum = +0.0e+00 | True |
| V2c book has 3 longs and 3 shorts | 3 long, 3 short | True |
| V2d book weights net to zero | sum = -1.1e-16 | True |
| V2d book has 3 longs and 3 shorts | 3 long, 3 short | True |
| Frozen repo unchanged at the end of the run | 3067 files, eb109be96917... | True |
