# Section: Evaluating Claude as a research assistant (Al)

The course asks for ChatGPT. No OpenAI API key was available, so every AI role used Claude: Sonnet 5.5 for the main study and Opus 5.5 (extra-high effort) for the follow-up run. The switch was logged as pre-registration amendments 001 and 002. The log file keeps the template name `chatgpt_log.md`, but its content is Claude.

## 1. Where Claude was used

| Use | What we asked | What Claude got right | What it got wrong | What we changed |
|---|---|---|---|---|
| **P1: data and code audit** (Sonnet 5.5) | Find mapping, look-ahead and code bugs in the manifest, crosswalk and as-of code, with the row, the reason and a test. | Flagged every real scope gap: transport without utilities, Telcm for Information, groups 9 and 10 sharing CES, French returns that are not vintaged. | Called design choices "confirmed errors". 5 of 25 findings were wrong, e.g. that group 10's CES series "silently vanishes" (584 shared rows were present). No real look-ahead bug. | Tested all 25. One metadata fix (crosswalk now separates prescribed match from verified French scope). No change to any number or timing rule. |
| **P2: signal agents** (Sonnet 5.5; 3 islands + 3 independent, 3 seeds) | Blind to names and dates, propose 6 features each in a fixed 14-operation grammar, using research-period feedback only. | 98 of 108 proposals passed validation. The blinding audit of all 199 calls passed. Best research IC about 0.08 (independent) and 0.05 (islands). | Both features picked for the independent arm (wage growth; layoffs vs hires) only switch on when T is in its low tercile. 11 of 18 migration reports broke the rules, 10 by exceeding 120 words. | Invalid proposals used up their slot. Selection was mechanical: 2 per arm, seed 1 only. No engineer edits to any proposal. |
| **Judge: migration tracing** (Sonnet 5.5; Opus 5.5 in follow-up) | Say whether a later island proposal uses or tests a claim from an earlier report, in JSON. | Follow-up: agreed with the human on 10 of 17 pairs and caught all 3 human "yes" cases. | Main run: 28 of 36 answers were not clean JSON, leaving 8 usable labels. Follow-up: all 7 disagreements were false "yes" (see part 3). | Undefined labels kept as missing. No repair parsing or extra calls. Migration uptake reported as descriptive only. |
| **P4: red team** (Sonnet 5.5) | From anonymous research tables, give 10 reasons the results could be spurious, each with a test and a "do not implement" trigger. | Read the tables correctly: no IC t-stat above 1.3, negative Sharpes, nothing to implement. 6 of 10 concerns matched tests we had already registered. | Stated results it never computed (a permutation p-value "already" above 0.10). Proposed new thresholds after seeing results (95th percentile, DSR ≥ 0.95, rolling 24-month). | Kept the registered diagnostics. Rejected the 4 new tests and every new threshold as post-hoc. |
| **Post-mortem review** (Claude, after the sealed test) | Explain why the frozen strategies lost money. | Found that the agent features were almost never active in the test (about 3 of 142 months). This fits the low-T gate: T stayed high for most of 2014 to 2026, so the gate rarely switched on. | Its fixes (re-adding wage growth, flipping two A0 signs) come from the sealed results, which our pre-registration rules out. It called wage growth "the only stable signal", yet V2a's last-18-month Sharpe is −1.71. | v2: four variants fixed before running and all reported, with wage growth (V2a) as the declared headline. Reported as a post-hoc follow-up next to the pre-registered v1. |

## 2. Prompt excerpts (copied exactly)

**P1, data and code audit** (`outputs/p1_request.json`)

> System: "You are a careful data and code auditor. Inspect only the supplied material. Use no tools. Return specific numbered findings and distinguish confirmed errors from limitations or questions."
>
> Prompt: "Find mapping errors, timestamp or look-ahead errors, and code bugs in the material below.
> For each problem, give the exact line or row, why it is wrong, and a test that would confirm it.
> Do not report style issues."

Followed by the manifest, the crosswalk and the as-of code (about 38,700 characters).

**Signal agents** (`params.py`, `SYSTEM_PROMPT`)

> "You are a quantitative researcher. You will propose one feature per turn to predict which of {n} anonymous groups (G01 to G{n}) will have higher returns next month relative to the others. [...] You do not know what the groups, variables or time periods are. Do not guess them and do not use knowledge about any real industry, company or date.
> Starting emphasis: {emphasis}.
> Rules: return only JSON with keys name, hypothesis, falsified_if, expression; use only the allowed operations; state a hypothesis that the statistics could falsify. [...] Keep that entire report comfortably below 120 words, including headings, and check its word count before returning it."

**P4, red team** (`outputs/p4_request.json`)

> System: "You are an independent quantitative research auditor. Use only the supplied anonymous research results. Use no tools. Follow the requested numbered format."
>
> Prompt: "Give 10 distinct reasons these results could be spurious, ranked by likelihood.
> For each, name a test that can be run with this data and the result that would make us say "do not implement"."

Followed by the anonymous research tables in JSON.

## 3. When the Claude judge and the human disagreed

In the follow-up run, we hand-checked 17 report–proposal pairs. The Claude judge said "uses a claim" 10 times; the human said yes 3 times. All 7 disagreements (items 2, 3, 8, 12, 13, 16, 17) were a machine yes against a human no, and the judge never missed a true yes. Four are clear errors. In items 2, 3 and 13, the proposal cites a result ("submission 2's significant negative IC") that exists elsewhere in the study but not in the paired report. In item 12, the proposal cites "submission 4" from a report that only had two submissions. The judge seems to accept a proposal's own claim of building on earlier work, and to match on shared variables and regimes without checking that the cited result is in the report. The other three are judgment calls: item 8 reuses a methodological tip rather than a finding, and items 16 and 17 share a report's topic but contradict its result. Repeated proposals make the bias visible: the same proposal paired with two different reports (items 12 and 17) got a yes both times. The judge therefore over-attributes, and its 62% uptake rate overstates real communication between islands. With 17 dependent pairs, this is a small sample.

## 4. What Claude is good and bad at as a research assistant

**Good at:**

- **Fast, wide first-pass audits.** In one pass, P1 listed every place our industry mapping is approximate. It works as a checklist that a human then verifies.
- **Structured skepticism.** P4 read the research tables correctly and proposed the standard battery: multiple-testing correction, placebo, cost break-even, subsample stability.
- **Following a blind protocol.** 98 of 108 proposals passed a strict grammar, and the blinding audit of all 199 calls passed.

**Bad at:**

- **Calibration.** It labels design choices as "confirmed errors" and states results it never computed. 5 of 25 P1 findings were wrong.
- **Holding the rules fixed.** Left alone, it adds tests and thresholds after seeing results (4 of 10 P4 suggestions). Pre-registration exists to stop exactly that, so a human has to hold the line.
- **Counting and strict formats.** 10 of 18 migration reports ran over 120 words, even though the prompt told it to check its word count. 28 of 36 judge answers in the main run were not clean JSON.
- **Judging provenance.** As a judge, it matches on vocabulary and trusts a proposal's own claim about where an idea came from (7 false yes out of 17).
- **Seeing past the feedback it gets.** The agents optimized what we showed them. We showed IC split by T tercile, and both features the independent arm sent to A3 were gated on low T. Blinded, they could not know T would stay high after 2014, so those features were almost never active in the test.
- **Sharing did not help.** Islands did not search better than independent agents. The gap between arms was inside the seed range on all four process metrics, and islands had the lower best IC (0.05 vs 0.08).

**Bottom line.** Claude is a useful auditor and idea generator when a human checks every claim against the code and data, and when it cannot change the rules after seeing results. Every Claude output here needed a human check: 25 P1 dispositions, 10 P4 dispositions and 25 hand-labeled migration pairs.

---

**Notes for Romain**

- Sources: `outputs/follow_the_workers/` (Sonnet main study). The 7 disagreements are from the Opus follow-up: `outputs/follow_the_workers_opus55_xhigh/outputs/human_review_submission.md`.
- Post-mortem row: written from Piero's summary in the gc. `docs/FINDINGS_AND_PROPOSAL.md` is not in Alex's repo, so check that row's wording against it.
- Decoded from `blind_map.json`: the two independent-arm features are `regime(yoy(E),"low")` (wage growth) and `regime(spread(tsz(LDR,60),tsz(HIR,60)),"low")` (layoffs vs hires).

**My own critique line for the table (Sunday noon):** Showing agents IC split by T tercile pushed them toward regime-gated features. Both picks for A3 were switched off by a low-T gate for most of the test. Next time, keep regime splits out of agent feedback, or require a minimum share of active months in research.
