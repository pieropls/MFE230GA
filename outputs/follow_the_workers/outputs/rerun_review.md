# Research rerun review

Reviewed September 29, 2026. Recommendation only: research remains paused. No production source changes, model calls, performance-based selection, or sealed evaluation occurred during this review.

## Verified problems

- Of 70 proposals, 47 were rejected. The primary reason for 28 was the legitimate statistical acronym `HAC`, which the identifier filter disallows even though evaluator feedback includes `hac_t`.
- Twelve proposals failed the 40-word hypothesis or 30-word falsification limits. Those limits appear in the supplied plan but are absent from its verbatim prompt template, copied into `params.py`. The implementation should have reconciled this inconsistency before running. Additional name/expression length constraints are also undisclosed in the prompt.
- All 12 migration reports exceeded the explicit 120-word cap: 131–174 words. Screening fixes alone would admit none. Separate screening false positives include Markdown asterisks, prose parentheticals, and ordinary statistical uses of industry-name words.
- Rejection feedback is too generic to explain repeated errors; migration records lack structured rejection reasons. Migration tracing excludes all invalid proposals, narrowing the population requested by the plan.

Evidence: `work/claude_audit_setup/rerun_protocol_diagnosis.json` at the workspace root; saved candidate/report records; `agents.py`, `params.py`, and `stats.py`; independent read-only protocol review. Rejection categories were inspected without using performance values to choose corrections.

## Required before a corrected run

1. Preserve the partial run, its original sources/parameters, and all 83 successful call journals. Keep the existing pause guard and sealed-data guard in place.
2. Record a new protocol amendment before further research. State every enforced output constraint and the exact counting rules, permitted statistical vocabulary, migration format, safe rejection feedback, and treatment of invalid submissions in migration tracing. Preserve fixed budgets; do not add repair attempts merely to rescue responses.
3. Correct screening without weakening identity/date blinding or admitting actual formulas into findings-only reports. Add regression cases for the observed false positives, boundary lengths, genuine prohibited content, and unavailable selection-only feedback.
4. Validate a complete mocked schedule for both arms, including both migration barriers, delivery, tracing, fresh contexts, budget enforcement, pause/resume, and cache separation. Any live format preflight should have a fixed budget and synthetic feedback only. Passing tests cannot guarantee that every future model response will comply.
5. Declare prior-search accounting before rerunning. Both original first-run arms completed all 36 strategy-producing slots. A new experiment adds another 36. Preserve and disclose both libraries and predeclare conservative trial accounting or sensitivity analysis; do not silently retain the original claim of only 36 attempts. Other repetitions remain process-only.
6. Bind the corrected source, prompts, evaluation rules, and transport evidence to a new run identity. Rerun both arms under identical corrected rules, using fresh journals and output paths. Do not cherry-pick the original 23 accepted proposals, replenish invalid slots, or mix caches.

## Current limits and next action

No complete line-by-line certification of the entire project is claimed. The original run is an incomplete protocol run, not evidence that communication is ineffective. The sealed period remains unopened; prior research feedback and the subsequent amendment must still be disclosed.

Next: implement and validate these protocol corrections, finalize the amendment and trial-accounting rule, then explicitly resume a fresh research run. Nothing has restarted.
