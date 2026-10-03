# Exploratory analysis (post-hoc)

These scripts rebuild the study's inputs from public sources so the team can extend the analysis without Alex's data zip. They read the frozen study outputs in `../230ga-follow-the-workers/` read-only.

| File | Purpose |
|---|---|
| `french.py` | Parses Ken French 49-industry, FF5 and momentum CSVs, and builds the 13 group returns exactly as the study did. The study's saved test ledgers are reproduced to 1e-16. |
| `signals.py` | Builds F1–F5 and wage growth W from **current (revised)** FRED data with fixed lags: JOLTS at d−2, CES at d−1. This approximates the study's FIXEDLAG variant, not ASOF. |
| `diagnostics.py` | Produces every **[exploratory]** number in `../FINDINGS_AND_PROPOSAL.md`, written to `output/diagnostics.md`. |
| `data/` | Downloads from 3 Oct 2026: French files (CRSP 202608 build) and FRED CSVs from `fredgraph.csv`. |

To run: `python3 diagnostics.py` (pandas, numpy).

Everything here uses a sample that has already been seen. It is for interpretation and forward-test hypotheses only, never confirmatory evidence.
