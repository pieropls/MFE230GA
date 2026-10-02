
- 2026-09-28T15:22:39.619836+00:00 · Stage 0: Preregistration verified; 125 selection months and 142 sealed months

- 2026-09-28T15:22:40.850570+00:00 · Stage 1: 169 pinned inputs; optional company data excluded for documented historical-evidence failures

- 2026-09-28T15:23:52.098284+00:00 · Stages 2–3: All four labor variants passed schema, calendar and publication-cutoff checks

- 2026-09-28T15:23:52.324166+00:00 · Stage 4: Private blinding map and 18 first prompts saved; no model calls made

- 2026-09-28T15:23:53.463254+00:00 · Stage 6: Synthetic tests passed; research return endpoint/schema checked; sealed returns remain unopened

- 2026-09-28T15:36:48.711752+00:00 · Validation: stable-source synthetic integration and all inline regressions passed; 12 synthetic figures and report rendered. No real experimental call or sealed opening. Next: resolve the pending agent transport choice, then P1/Stage 5/P4 and freeze. Reproduce preparation with run.ipynb under /opt/homebrew/bin/python3; rerun synthetic integration from the workspace with /opt/homebrew/bin/python3 work/validate_project.py.

- 2026-09-29T11:05:50.286421+00:00 · Protocol corrections:22 offline regression tests, inline checks and full synthetic workflow passed. Research remains paused; all earlier attempts retained. See guideline_alignment.md for unresolved prerequisites. No real research rerun or sealed opening.

- 2026-09-29T19:44:46.620200+00:00: Fresh research completed:108proposals/18reports/36judgedpairs, two selected features per arm; source bindings intact. P4 complete. Eight human judgments required before freeze. Sealed test unopened.

- 2026-10-02T06:00:09.557212+00:00: Stage 7: Freeze verified with 525 file hashes; all prerequisites passed. Starting the single authorized sealed evaluation.

- 2026-10-02T06:00:39.968409+00:00: Stage 8: Initial sealed evaluation completed successfully; saved outputs/sealed/initial/results.json. No rerun.

- 2026-10-02T06:00:41.050941+00:00: Stage 9: Registered figures and generated report saved. Final presentation and artifact checks remain; frozen inputs unchanged.

## Completed evaluation and reproduction record

The initial sealed evaluation completed once. Verdict: **Do not implement**, primary A3; G1 passes and G2–G5 fail. Core results, every diagnostic and12 figures are preserved. Human critique remains for students; migration judgment missingness,company-data exclusion,approximate industry mappings,technical restart and unverified capacity are disclosed.

Recorded execution from the workspace root:

```sh
/opt/homebrew/bin/python3 -u -W error work/finalize_study.py
/opt/homebrew/bin/python3 -W error work/assemble_final_delivery.py
```

Both completed successfully. They deliberately refuse to overwrite an existing initial evaluation/delivery. Do not rerun these commands over the delivered experiment. Reproduction with the same source can be checked without reopening returns:

```sh
cd outputs/follow_the_workers
/opt/homebrew/bin/python3 -c 'import data as D; print(len(D.verify_freeze()["hashes"]))'
```

Expected frozen-file count:525. The synthetic workflow uses generated fixtures rather than sealed returns, but `work/validate_project.py` also rewrites `outputs/integration_checks.json`. Do not run it in this frozen project. Any new validation run needs an isolated project copy with its paths configured to that copy. The delivered real experiment was executed through the notebook functions, not by re-executing the whole notebook from an empty cache after freeze. Such a new run is not authorized by these reproduction notes. Raw model outputs are retained for replay; live subscription inference is not deterministic.
