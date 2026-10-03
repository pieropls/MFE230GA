# Open issues

Things found during the final pass (3 Oct 2026) that were **not** fixed because fixing them would change a frozen file or a recorded result. Rule from `docs/process/FINAL_PROMPT.md`: no result may change; log it here instead.

| # | Found in | Issue | Why not fixed | Owner |
|---|---|---|---|---|
| 1 | Stage 1 | `analysis/v2_spec.md` line 3 cites `FINDINGS_AND_PROPOSAL.md` at its old location (now `docs/FINDINGS_AND_PROPOSAL.md`). | The file is hashed (`analysis/v2_spec.sha256`, frozen 2026-10-03T09:00:13Z); editing it would break the freeze check in `run.ipynb`. | nobody (cosmetic) |
| 2 | Stage 1 | `analysis/output/diagnostics.md` (3 Oct baseline) and `docs/process/REVIEW_round*.md` quote paths as they were on 3 Oct. | Historical records; left as written. | nobody |
