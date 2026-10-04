# Claude interaction log

All study roles used Claude Sonnet 5.5 through the approved subscription amendment. The filename preserves the assignment template. Team critique cells are intentionally empty for the students.

| Phase | Actual prompt/transcript | Output summary | What was wrong | What changed | Team critique |
|---|---|---|---|---|---|
| P1 | [Prompt](../outputs/p1_request.json) / [Findings](../outputs/p1_review.md) | 25 source/code findings | Several alleged errors were not supported; French-scope descriptions needed qualification | Tested findings; corrected mapping metadata; numeric mapping/timing unchanged |  |
| P2 | [Call log](../outputs/agents/log.jsonl) / [Candidates](../outputs/candidates.csv) | 108 proposals; two selected per arm from repetition 1 | Some submissions violated rules or failed research eligibility | Invalid submissions consumed slots; mechanical selection; no engineer rewriting |  |
| P3 | [Reports](../outputs/agents/migrations.json) / [Human review](../outputs/human_review_submission.json) | 7/18 reports delivered; 8/36 usable uptake labels | 28 uptake outputs not JSON-only; no defined failure-avoidance labels; one match among two comparable human/machine labels | Preserved missing labels and full responses; no extra calls or repair parsing; qualified all migration claims |  |
| P4 | [Prompt](../outputs/p4_request.json) / [Decisions](../outputs/p4_review.md) | 10 ranked robustness concerns | Some asserted results were uncomputed; several proposed thresholds were unregistered | Retained registered diagnostics; no post-hoc feature or threshold changes |  |
