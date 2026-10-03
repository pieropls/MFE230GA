# Provenance of `230ga-follow-the-workers/` (the frozen study)

| | |
|---|---|
| Source repository | `https://github.com/Aroesler1/230ga-follow-the-workers.git` (private, Alex Roesler) |
| Commit imported | `c67c486d3eec759f07c85a03fd62a0f711b09140`, the tip of `main` on 3 Oct 2026 |
| How | `git subtree add --prefix=230ga-follow-the-workers <repo> c67c486` on 3 Oct 2026, **with history** (no `--squash`): Alex's commits are part of this repository's history and he appears as a contributor (`git shortlog -sne -- 230ga-follow-the-workers`) |
| Author | v1 pipeline, preregistration, sealed evaluation and both agent studies: **Alex Roesler**, with an engineering assistant he calls "6 astra" (name and vendor to be confirmed by Alex; not documented in the repository) |
| Status | **Read-only.** Nothing under this path is edited, rerun or retuned; our code imports it read-only (`analysis/data.py`, `frozen()`). Nothing is ever pushed back to Alex's repository |
| Integrity check | SHA-256 over every file path and content (excluding any `.git` entry): `eb109be969176412635ab80c03e0e37c6a006aedca740f671ed2908c371fbd9a`, 3,067 files, stored in `analysis/params.py` (`FROZEN_FINGERPRINT`) and checked by `analysis/run.ipynb` at Gate 1, Gate 3 and Gate 2 on every run; re-checked after the import (match) |
| Earlier form | Until 3 Oct 2026 the folder was an untracked clone, then briefly a git submodule pinned at the same commit (`402c92c`); the subtree import replaced it so that a plain `git clone` of this repository needs no access to Alex's private repository |
| Largest file | no file over 50 MB in the tree or in the imported history (largest blobs under 20 MB) |

To compare the imported tree with the source at any time: `git diff c67c486 HEAD:230ga-follow-the-workers` must be empty (the subtree root commit is reachable from `main`).
