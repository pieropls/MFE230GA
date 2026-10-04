# 230GA: Follow the Workers

Private team review package, prepared October 2, 2026. Both experiments are complete. **Neither passes the implementation gate.** The team's own critique and final course-submission review remain.

## Start here

- [Original project briefing](original_documents/230GA_project_briefing.md) and [original build-and-run specification](original_documents/230GA_build-and-run_prompt.md), preserved exactly as supplied. These are historical instructions; read the recorded amendments before comparing them with the implementation.
- [Original Sonnet study report](outputs/follow_the_workers/report/report.md).
- [Opus follow-up report and comparison](outputs/follow_the_workers_opus55_xhigh/report/report.md).
- [Human review with all 17 rationales](outputs/follow_the_workers_opus55_xhigh/outputs/human_review_submission.md).
- [Team review checklist](TEAM_REVIEW.md) and [reproducibility and data notes](REPRODUCIBILITY.md).

## Results

The test covers November 2014 through August 2026, 142 months. Each study selected its primary strategy using research data, before that study's test evaluation.

| Study | Research-selected primary | Net Sharpe | Annualized mean net excess return | Maximum funded drawdown | Verdict |
|---|---|---:|---:|---:|---|
| Original, Claude Sonnet 5.5 | A3, independent agents | -0.58 | -4.59% | -41.06% | Do not implement |
| Follow-up, Claude Opus 5.5 at extra-high effort | A4, communicating agents | 0.01 | +0.07% | -25.25% | Do not implement |

The annualized return is twelve times the monthly arithmetic mean, not CAGR. The two rows use different research-selected primary strategies. Comparing the same communicating strategy, A4's Sharpe changed from -0.79 to 0.01.

**The Opus comparison is exploratory.** It was requested after the original test results were seen. Fresh agents received no earlier research outputs, but the historical period was already known to the user and engineer. Model and effort changed together, alongside two disclosed preflight corrections to formatting instructions and a narrow language screen. The comparison does not isolate a model or communication effect. Both studies and their failures remain available.

The human marked 3 of 17 sampled report/proposal pairs as using a specific result from the paired report; the automated judge marked 10. Agreement was 10/17, with all seven disagreements machine yes/human no. Formatting compliance did not resolve attribution reliability. Ambiguous human answers remain recorded as submitted.

## What is included

- The five Python modules and notebook for each completed study, without changing their frozen source.
- Reports, all registered figures, saved monthly strategy ledgers, weights, predictions, candidate results and inference tables.
- Preregistration, amendments, selection and freeze records, data-source manifests, human judgments and audit dispositions.
- Experimental prompts, responses, migration reports, machine judgments and bounded call evidence. Rejected attempts remain recorded.
- Portable copies of the 28 follow-up regression tests and an offline package/result verifier.

The review export is about 41 MB before Git compression. The largest file is a model-fit log of about 8 MB. Raw data archives, vendor downloads, intermediate Parquet panels, credentials, login sessions, local caches and abandoned technical-run directories are not included. Omissions and source/export hashes are listed in [package_manifest.json](package_manifest.json). Disclosures of technical failures remain in the completed studies.

## Verify without running the experiment

From the repository root, with Python 3.11 or later:

```sh
python3 tools/verify_review_package.py
```

This uses only the standard library and saved artifacts. It verifies export hashes, preserved source, local report links, human-label integrity and saved performance accounting. It makes no network request, model call or new backtest.

For the synthetic regression suite, use the recorded numerical environment described in [REPRODUCIBILITY.md](REPRODUCIBILITY.md):

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

Do not rerun the study notebook as a way to inspect results. This is a bounded review export, not a complete raw-data archive or a new preregistered experiment.
