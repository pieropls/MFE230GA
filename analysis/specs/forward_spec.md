# Forward test specification: Q4 2026 book (frozen)

**Label: FORWARD TEST.**
- Written and hashed on Sat 3 Oct 2026, before the Q4 2026 book was computed. The hash is in `spec_frozen.sha256`.
- The holding period starts Thu 1 Oct 2026, so returns for 1 Oct and 2 Oct 2026 already existed when this file was frozen. We did not look at sector or ETF returns for those days. They are part of the holding period and are disclosed here.
- This is the only clean holdout left: the frozen study's test period, and every post-hoc variant (`analysis/v2_spec.md`), were evaluated on data that had already been seen.

## 1. Strategies

Both choices were fixed in `analysis/v2_spec.md` §8 before the v2 results existed.

| Role | Variant | Score at decision month d |
|---|---|---|
| Headline | V2a | csrank(z(W)), wage growth: 12-month log change in 3-month-average CES hourly earnings, standardised as in `analysis/data.py::signals` |
| Secondary | V2b | (1/6) Σ_k sign_k · z_k over k ∈ {F1, F2, F3, F4, F5, W}. Signs were learned on research months only (May 2004–Sep 2014, `analysis/output/tables/v2b_signs.csv`): F1 +, F2 +, F3 +, F4 +, F5 −, W +. |

Neither variant met the v2 reading rule. Both were reported as "not distinguishable from noise after the looks already taken" (`analysis/output/v2_results.md`). They are forward-tested because that was decided in advance, not because they passed.

## 2. Information set and decision

- **Decision date:** Wed 30 Sep 2026 (last trading day of September); information cutoff Tue 29 Sep 2026.
- **Labor data:** ALFRED values as published on 29 Sep 2026 (`analysis/data/alfred_2026-09-29/`, from alfredgraph.csv with `vintage_date=2026-09-29`), with the fixed-lag rule:
  - JOLTS rates through **July 2026**;
  - CES hours and earnings through **August 2026**;
  - tightness from July 2026.
  - The notebook stops if any series carries an observation later than these months.
- **Returns for risk estimates:** Ken French data through August 2026, the latest full month at the decision (frozen rule m−2 for earning month October 2026).

## 3. The Q4 2026 book

- **Tranche.** One tranche formed at the 30 Sep 2026 close: long the 3 groups with the highest score (+1/3 each) and short the 3 with the lowest (−1/3 each). Ties use the frozen backtest's stable group order. The industry weights sum to zero.
- **Holding.** Buy and hold from 1 Oct to 31 Dec 2026 (three months, the strategy's tranche life), with no rebalancing.
- **Market hedge.** A market position of −Σ_g w_g β_g. Each β_g is group g's beta to Mkt-RF over the 60 months ending August 2026 (frozen rule). Traded as SPY.
- **Scale.** Results are reported per unit of the ±1/3 tranche. For information, the notebook also reports the frozen rule's volatility scaling (10% target, Ledoit–Wolf covariance, gross cap 2); returns scale linearly with it.
- **Costs.** 10 bp per unit of traded industry weight at entry and at exit, and 2 bp on the hedge.

## 4. Instruments and tracking

- **ETF proxies.** One liquid ETF per group (`etf_proxies.csv`), taken from the issuer-verified list in the frozen study (`230ga-follow-the-workers/.../implementation_capacity.md`, checked 28 Sep 2026). SPY is the hedge.
  - The French industry portfolios are research series, not tradable.
  - Several proxies are poor matches; see the caveat column. In particular, Durable manufacturing is 60% semiconductors by market cap and Nondurable manufacturing is 60% pharmaceuticals.
  - When two book positions map to the same ETF, the ETF weights are netted.
- **Weekly tracker.** `tracker.csv` has one row per Friday close from 2 Oct to 31 Dec 2026, plus a 30 Sep 2026 baseline. Elouan fills it in.
- **Final evaluation**, reported whatever it shows:
  - (i) the ETF book's cumulative return after costs, from the 30 Sep 2026 close to the 31 Dec 2026 close;
  - (ii) the same book on Ken French group returns for October–December 2026, once French publishes them (expected around February 2027).

## 5. What the result can and cannot show

- **One quarter has almost no statistical power.** V2a's test-period volatility was about 10% a year (`v2_window_stats.csv`), so one quarter's return has a standard deviation of about 5%. A Q4 result anywhere between −10% and +10% is consistent with no skill.
- The forward test exists to keep an honest, pre-committed record. It is not a verdict.
- **Event risk.** The US midterm elections (Tue 3 Nov 2026) fall inside the holding period, and the model has no political variable.
