# Code hashes of the analysis modules at each freeze and run

Written 3 Oct 2026 during the final pass (code review finding 3). `analysis/v2_spec.md` points to the module code "at the commit above" (44ae263); the modules were extended for the v3 battery (`signals(groups=)`, `factor_attribution(lags=)`, `block_bootstrap_sharpe`, `P.SEED`) after the v2 run, and two unused helpers were removed in the final pass. The v2 outputs are byte-identical across all of these versions (`v2_run_log.md`, checked on every notebook run), so no result changed; this file makes the code pointer verifiable again.

| commit | event | params.py | data.py | stats.py | plots.py |
|---|---|---|---|---|---|
| `44ae263` | v2 spec frozen | `1d9617fef447c312` | `5275fe7ef82bc563` | `8e02fce7b80c099d` | `083a28666d5ab9a3` |
| `60126f3` | v2 first run | `1d9617fef447c312` | `5275fe7ef82bc563` | `8e02fce7b80c099d` | `eb8ca243e94bcc2c` |
| `c7014d9` | v3 spec frozen | `1d9617fef447c312` | `5275fe7ef82bc563` | `8e02fce7b80c099d` | `eb8ca243e94bcc2c` |
| `925fdee` | v3 first run | `4a73bed2e26603f7` | `5f178457c3fb35c7` | `942fa12f865fd298` | `6321acd7e7168104` |
| `final pass` | 3 Oct 2026 Stage 2 hygiene (two unused helpers removed, one comment) | `4a73bed2e26603f7` | `0a12100fa04388d5` | `77288610a67a171e` | `f6c37860be1d55b2` |

SHA-256, first 16 hex digits, of the file blobs. Reproduce with `git show <commit>:analysis/<module> | shasum -a 256`; the "final pass" row is the working tree of the Stage 2 commit.

Diff between the v2 first run (60126f3) and the v3 first run (925fdee):

```
analysis/data.py   |  3 ++-
 analysis/params.py |  1 +
 analysis/plots.py  | 79 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 analysis/stats.py  | 20 +++++++++++---
 4 files changed, 99 insertions(+), 4 deletions(-)
```
