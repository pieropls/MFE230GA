# Forward-test spec, amendment 001

**Label: FORWARD TEST.** This amends `analysis/forward/spec_frozen.md`, which was frozen at 2026-10-03T09:03:56Z (sha256 `735a8ffa9c9c23fd710dfae778a535cad649685aa157dcded3ae0e9996dfb21f`, commit `45991d4`). The original file is not edited. This amendment is hashed in `spec_amendment_001.sha256` and committed before any Q4 2026 book is computed.

Decided by the team (Piero) on Sat 3 Oct 2026, after reading `analysis/output/STOP.md`. At that time:
- no Q4 2026 book had been computed;
- no Q4 2026 sector or ETF return had been looked at;
- the returns of Thu 1 Oct and Fri 2 Oct 2026 existed, as already disclosed in the original spec.

## 1. Information set: Option A of STOP.md

- **What happened.** The original spec (§2) fixed the 30 Sep 2026 information set as "JOLTS through July 2026, CES through August 2026" and said the notebook stops if any series *carries* a later observation. ALFRED's 29 Sep 2026 vintage carries August 2026 JOLTS, because August JOLTS was released on 29 Sep 2026, the cutoff day itself (see STOP.md). The notebook stopped.
- **What changes.** The forward book uses the same fixed-lag rule as every v2 backtest (`analysis/v2_spec.md` §1):
  - JOLTS month d−2 = **July 2026**, CES month d−1 = **August 2026**, tightness month d−2 = July 2026;
  - all values as published in the ALFRED vintage of **29 Sep 2026**. The July JOLTS values therefore include any revision published with the August release that day. That revision was public at the cutoff.
- **The new stop condition.** The notebook stops if any observation later than the fixed-lag month is **used**: JOLTS after July 2026, or CES after August 2026. A vintage that merely *carries* later months no longer stops the run.
- **How "not used" is verified.** The forward scores are recomputed from a copy of the vintage truncated at July 2026 (JOLTS, JTSJOL) and August 2026 (CES, UNEMPLOY). The two sets of scores must be identical.

## 2. Variants in the forward book: V2c and V2d added

- **Disclosure.** V2c and V2d join V2a (headline) and V2b (secondary). We added them **after seeing the historical v2 results** (`analysis/output/v2_results.md`, first run 2026-10-03T09:01:55Z), and **before any Q4 2026 return beyond those of 1–2 Oct 2026 was observed**.
- **Context.** In the historical results, V2c and V2d had the two highest test-period Sharpe ratios of the four (`v2_window_stats.csv`), and none of the four met the reading rule. Adding variants after seeing their historical results is a selection step, and it is disclosed as one. It does not bias the forward evaluation, because Q4 2026 returns are new data for all four.
- **Specifications.** Unchanged from `analysis/v2_spec.md` §2: V2c = (csrank(z(W)) + csrank(Mom 12-1)) / 2; V2d = −(z(F2) + z(F3)) / 2.
- **Momentum input for V2c.** Mom for October 2026 is the compounded group return over October 2025 to August 2026 (months m−12 to m−2), from Ken French data through August 2026.
- **V2d horizon.** V2d's design horizon is 12 months (12 tranches). Its Q4 2026 book is its 30 Sep 2026 tranche, evaluated over October–December 2026 like the others. The full 12-month holding of that tranche ends in September 2027 and may also be reported, labelled FORWARD TEST.
- **Roles.** V2a stays the headline and V2b the secondary. V2c and V2d are reported alongside them, whatever they show.

## 3. Unchanged

Everything else in `spec_frozen.md` still applies:
- decision date 30 Sep 2026;
- one tranche of ±1/3 per group, buy and hold to 31 Dec 2026;
- 60-month beta hedge in SPY;
- costs of 10 bp on industry legs and 2 bp on the hedge;
- ETF proxies with caveats;
- final evaluation on ETF and French returns;
- the statement that one quarter has almost no statistical power.

The weekly tracker (`tracker.csv`) is deferred by team decision and not built in this run.
