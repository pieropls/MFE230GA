# Did the researchers use each other's findings?

Your task is to answer 17 yes/no questions. This is the fixed sample selected by the registered random seed.

For each item, read the earlier report and then the later proposal. Answer **Yes** if the proposal uses or tests a specific claim from that report. Answer **No** if it does not. Sharing variables, statistical terms or operators is not enough.

You are judging whether a finding was used, not whether the proposed investment would work. A proposal can use a finding and still misunderstand it; note that separately if relevant.

Reply with `1 yes, 2 no, ...`. You may mark an item `unclear` for discussion. Automated answers are hidden, and no answers have been filled in on your behalf.

The expression uses anonymous variables. lag shifts an input; chg measures a change; yoy is a year-over-year change; mavg averages; csrank ranks groups; tsz standardizes over time; spread compares standardized inputs; withT interacts with common tightness.

## Variable key

| Code | Description available to researchers |
|---|---|
| T | index; stock ratio |
| V01 | hours; average |
| V02 | rate in percent of employment; flow |
| V03 | rate in percent of employment; flow |
| V04 | rate in percent of employment; flow |
| V05 | dollars per hour; average |
| V06 | rate in percent of employment; stock |

## Item 1

**Earlier report**

**Findings so far**

Two temporal signals failed. Ranking groups by acceleration in average hours, lagged one month, gave a mean information coefficient near 0.02 and a HAC t-statistic near 0.7, well below two. Its ranks also turned over quickly. Ranking groups by how persistently the stock rate variable rose over six lagged months did worse, with coefficient near 0.01 and t-statistic near 0.5, despite stable ranks. Both looked somewhat stronger when the common index was high. Conditioning on high-index regimes merits testing, though that split may be noise. Coverage was about 95 percent, and overlap with base factors stayed low.

**Later proposal**

Groups whose V03 flow rate rose more than their V02 flow rate over three months, relative to peers, earn higher next-month relative returns, with the effect strongest when the common index is low.

Expression: `spread(chg(V03,3),chg(V02,3))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 2

**Earlier report**

Findings so far

Both composition attempts among the flow-rate variables failed. A cross-sectional rank of the smoothed V02-to-V03 ratio showed essentially zero predictive power (mean IC 0.01, HAC t 0.38) in both low and high T regimes. It was highly persistent and distinct from base features, so novelty alone did not help. A peer-relative three-month shift in V02 versus V04 was weaker still (IC zero, t 0.05) and noisier month to month. Lesson: flow-mix levels and short-term mix shifts appear uninformative. Next, we suggest testing hours, wages or the stock rate, or conditioning composition on T.

**Later proposal**

Reversing an observed negative signal: groups whose V03 flow rate rose more than V02 over three months, respecting the two-month lag, earn higher next-month relative returns, especially when T is low.

Expression: `spread(chg(lag(V03,2),3),chg(lag(V02,2),3))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 3

**Earlier report**

Findings so far

Both composition attempts among the flow-rate variables failed. A cross-sectional rank of the smoothed V02-to-V03 ratio showed essentially zero predictive power (mean IC 0.01, HAC t 0.38) in both low and high T regimes. It was highly persistent and distinct from base features, so novelty alone did not help. A peer-relative three-month shift in V02 versus V04 was weaker still (IC zero, t 0.05) and noisier month to month. Lesson: flow-mix levels and short-term mix shifts appear uninformative. Next, we suggest testing hours, wages or the stock rate, or conditioning composition on T.

**Later proposal**

Submission 2's significant negative IC suggests a genuine reversal: groups where V03 rose more than V02, relative to peers, outperform. Testing at a six-month horizon, not the snooped three-month one, checks whether this is robust rather than noise.

Expression: `spread(chg(V03,6),chg(V02,6))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 4

**Earlier report**

**Findings so far**

The interaction of hours momentum and pay momentum failed. Their joint signal showed slightly negative, insignificant predictive power.

The flow rates V02 and V03 were the most informative. When V02 rose faster than V03 over three months, groups significantly underperformed, mostly in low-T periods. Reversing the direction at six months gave a modest positive signal, with t near two. It was consistent across T regimes and overlapped little with base factors. This reversal was chosen after seeing the earlier result, so treat it cautiously.

Contrasting pay growth with the stock rate's deviation from its long norm was weak. It covered only half the sample and flipped sign when T was high.

**Later proposal**

Testing whether submission four's own-history effect generalizes: groups whose twelve-month log growth in average hours (V01), lagged one month, is unusually high versus its own 36-month history outperform peers next month.

Expression: `tsz(lchg(lag(V01,1),12),36)`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 5

**Earlier report**

**Findings so far**

The interaction of hours momentum and pay momentum failed. Their joint signal showed slightly negative, insignificant predictive power.

The flow rates V02 and V03 were the most informative. When V02 rose faster than V03 over three months, groups significantly underperformed, mostly in low-T periods. Reversing the direction at six months gave a modest positive signal, with t near two. It was consistent across T regimes and overlapped little with base factors. This reversal was chosen after seeing the earlier result, so treat it cautiously.

Contrasting pay growth with the stock rate's deviation from its long norm was weak. It covered only half the sample and flipped sign when T was high.

**Later proposal**

Flow composition, not flow levels, carries the earlier signal: groups whose V03-to-V02 ratio rose most in log terms over three months earn higher next-month relative returns, without conditioning on T regimes.

Expression: `csrank(lchg(ratio(V03,V02),3))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 6

**Earlier report**

**Findings so far**

Our composition theme compares two employment-rate flow variables, V02 and V03. Failure: ranking groups by the three-month rise in V02's share relative to V03 gave a negative information coefficient near minus 0.04, with a t-statistic of about minus 1.4. It was weakest when the common index was low. Reversing the mix to favor V03, lengthening to six months and restricting to low-index periods gave a positive coefficient near 0.05, with a t-statistic of about 1.9. Caveats: coverage is only 58 percent, and there is no high-index evidence. Rank persistence is low, near 0.22, and overlap with base factors is small. Next, test robustness outside the low regime.

**Later proposal**

Unusually high twelve-month log hourly-pay growth versus each group's expanding history predicts higher next-month relative returns mainly when the common index T is high; restricting to high-T periods should strengthen the signal.

Expression: `regime(tsz(lchg(V05,12),"exp"),"high")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 7

**Earlier report**

**Findings so far**

Our composition theme compares two employment-rate flow variables, V02 and V03. Failure: ranking groups by the three-month rise in V02's share relative to V03 gave a negative information coefficient near minus 0.04, with a t-statistic of about minus 1.4. It was weakest when the common index was low. Reversing the mix to favor V03, lengthening to six months and restricting to low-index periods gave a positive coefficient near 0.05, with a t-statistic of about 1.9. Caveats: coverage is only 58 percent, and there is no high-index evidence. Rank persistence is low, near 0.22, and overlap with base factors is small. Next, test robustness outside the low regime.

**Later proposal**

Twelve-month log hourly-pay growth unusually high versus each group's trailing three-year history signals tightening demand not yet priced, predicting higher next-month relative returns; rolling baselines adapt to structural shifts better than expanding ones.

Expression: `csrank(tsz(lchg(V05,12),36))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 8

**Earlier report**

**Summary of findings**

Both interaction features failed. Combining three-month hourly pay growth with the three-month change in average hours gave a slightly negative, insignificant information coefficient (about minus 0.02, t near minus 1.1). It was identical in low and high T regimes, so this pairing looks uninformative.

Pairing V06's standardized stock level with rising V02 flows was also negative overall (about minus 0.05, t near minus 1.4). Its sixty-month window cut coverage to roughly half. However, its sign flipped by regime: negative when T was low and clearly positive when T was high.

Next steps: condition on T, use expanding windows to restore coverage, and test sign reversal.

**Later proposal**

Groups whose twelve-month log hourly-pay growth is unusually high versus their expanding own history face tightening demand not yet priced, earning higher relative returns next month; expanding windows should preserve the signal while raising coverage.

Expression: `csrank(tsz(lchg(V05,12),"exp"))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 9

**Earlier report**

**Summary of findings**

Both interaction features failed. Combining three-month hourly pay growth with the three-month change in average hours gave a slightly negative, insignificant information coefficient (about minus 0.02, t near minus 1.1). It was identical in low and high T regimes, so this pairing looks uninformative.

Pairing V06's standardized stock level with rising V02 flows was also negative overall (about minus 0.05, t near minus 1.4). Its sixty-month window cut coverage to roughly half. However, its sign flipped by regime: negative when T was low and clearly positive when T was high.

Next steps: condition on T, use expanding windows to restore coverage, and test sign reversal.

**Later proposal**

If V03 is the informative leg of the flow mix, a three-month shift toward V03 relative to V04 in low-T regimes also predicts higher next-month relative returns, generalizing the V03/V02 composition result.

Expression: `regime(chg(ratio(V03,V04),3),"low")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 10

**Earlier report**

**Summary of findings**

Both interaction features failed. Combining three-month hourly pay growth with the three-month change in average hours gave a slightly negative, insignificant information coefficient (about minus 0.02, t near minus 1.1). It was identical in low and high T regimes, so this pairing looks uninformative.

Pairing V06's standardized stock level with rising V02 flows was also negative overall (about minus 0.05, t near minus 1.4). Its sixty-month window cut coverage to roughly half. However, its sign flipped by regime: negative when T was low and clearly positive when T was high.

Next steps: condition on T, use expanding windows to restore coverage, and test sign reversal.

**Later proposal**

Both V03/V02 and V03/V04 shifts worked in low-T regimes, suggesting V03 drives the composition signal. Groups with larger three-month increases in V03 alone should earn higher next-month relative returns when T is low.

Expression: `regime(chg(V03,3),"low")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 11

**Earlier report**

**Findings**
Our first feature ranked groups by how persistently average hours rose over the prior six available months. It was valid, with 95% coverage, but weak: mean information coefficient about 0.05, HAC t-statistic near 1.35, not significant. It predicted only when the common index was high and turned slightly negative when the index was low. Overlap with base factors was low, and ranks were stable.

**Failure**
Our second submission was rejected as invalid because the blinded payload contained a forbidden name or identifier. It used up a slot. The exact trigger is unclear, so use neutral naming.

**Next**
Condition the hours signal on the high-index regime, respecting the index's two-month lag.

**Later proposal**

Groups whose average hours rose in a larger share of the past six months earn higher next-month relative returns, but only when the common index is in its high regime.

Expression: `regime(persist(V01,6),"high")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 12

**Earlier report**

**Findings**
Our first feature ranked groups by how persistently average hours rose over the prior six available months. It was valid, with 95% coverage, but weak: mean information coefficient about 0.05, HAC t-statistic near 1.35, not significant. It predicted only when the common index was high and turned slightly negative when the index was low. Overlap with base factors was low, and ranks were stable.

**Failure**
Our second submission was rejected as invalid because the blinded payload contained a forbidden name or identifier. It used up a slot. The exact trigger is unclear, so use neutral naming.

**Next**
Condition the hours signal on the high-index regime, respecting the index's two-month lag.

**Later proposal**

In high common-index periods, groups whose V06 stock is high relative to V04 flow versus a rolling 36-month baseline earn higher next-month relative returns; a rolling baseline should handle structural drift better than submission 4's expanding one.

Expression: `regime(tsz(ratio(V06, V04), 36), "high")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 13

**Earlier report**

**Progress report**

Two valid interaction features, each with about 98% coverage, found no signal.

The first failed attempt multiplied the cross-sectional ranks of three-month hourly-pay growth and three-month hours change. I expected joint strength to predict outperformance. Instead, mean rank correlation was slightly negative, about minus 0.02 with t near minus 1.1. It was identical in low and high common-index regimes.

The second attempt also failed. A standardized spread between three-month changes in two flow rates showed essentially zero predictive power (t near 0.05). Its sign flipped weakly across regimes.

Both features had low overlap with base signals (about 0.1) and moderate rank persistence (about 0.35).

Next I will try stock-rate levels, longer horizons, time-series standardization and explicit regime conditioning.

**Later proposal**

Composition reversal: groups whose V06 stock is unusually high relative to their smoothed V04 flow, versus own history, earn higher next-month relative returns, mainly in high common-index periods, mirroring submission 2's strongly negative high-index IC.

Expression: `tsz(ratio(V06, mavg(V04,3)), "exp")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 14

**Earlier report**

**Progress report**

Two valid interaction features, each with about 98% coverage, found no signal.

The first failed attempt multiplied the cross-sectional ranks of three-month hourly-pay growth and three-month hours change. I expected joint strength to predict outperformance. Instead, mean rank correlation was slightly negative, about minus 0.02 with t near minus 1.1. It was identical in low and high common-index regimes.

The second attempt also failed. A standardized spread between three-month changes in two flow rates showed essentially zero predictive power (t near 0.05). Its sign flipped weakly across regimes.

Both features had low overlap with base signals (about 0.1) and moderate rank persistence (about 0.35).

Next I will try stock-rate levels, longer horizons, time-series standardization and explicit regime conditioning.

**Later proposal**

Hours-rise persistence predicted returns positively when the common index was high (0.09) and negatively when low (-0.04). A continuous index interaction should use both regimes, keep full coverage and beat the regime-filtered t of 1.51.

Expression: `withT(persist(lag(V01,1),6))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 15

**Earlier report**

**Summary**

We tested four interaction-themed features, and none is convincing. One failure: multiplying cross-sectional ranks of three-month hourly-pay momentum and hours momentum gave a slightly negative, insignificant information coefficient. Contrasting three-month changes in two flow rates produced essentially zero signal. Persistence of rising hours, restricted to high common-index regimes, was slightly negative and had reduced coverage. The most informative feature was the stock rate standardized against its own expanding history, interacted with the common index. It was weakly positive overall but sharply regime-dependent: positive when the index was low and strongly negative when it was high. It also overlapped moderately with an existing base signal. A suggested next step is to isolate that stock-rate signal within low-index regimes.

**Later proposal**

Groups whose stock rate is unusually high versus their own expanding history should outperform next month, but only when the common index is low. Regime conditioning should remove the offsetting high-index periods.

Expression: `regime(tsz(lag(V06,2),"exp"),"low")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 16

**Earlier report**

**Summary**

We tested four interaction-themed features, and none is convincing. One failure: multiplying cross-sectional ranks of three-month hourly-pay momentum and hours momentum gave a slightly negative, insignificant information coefficient. Contrasting three-month changes in two flow rates produced essentially zero signal. Persistence of rising hours, restricted to high common-index regimes, was slightly negative and had reduced coverage. The most informative feature was the stock rate standardized against its own expanding history, interacted with the common index. It was weakly positive overall but sharply regime-dependent: positive when the index was low and strongly negative when it was high. It also overlapped moderately with an existing base signal. A suggested next step is to isolate that stock-rate signal within low-index regimes.

**Later proposal**

Hours-rise persistence predicted returns positively when the common index was high (0.09) and negatively when low (-0.04). A continuous index interaction should use both regimes, keep full coverage and beat the regime-filtered t of 1.51.

Expression: `withT(persist(lag(V01,1),6))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 17

**Earlier report**

**Summary**

We tested four interaction-themed features, and none is convincing. One failure: multiplying cross-sectional ranks of three-month hourly-pay momentum and hours momentum gave a slightly negative, insignificant information coefficient. Contrasting three-month changes in two flow rates produced essentially zero signal. Persistence of rising hours, restricted to high common-index regimes, was slightly negative and had reduced coverage. The most informative feature was the stock rate standardized against its own expanding history, interacted with the common index. It was weakly positive overall but sharply regime-dependent: positive when the index was low and strongly negative when it was high. It also overlapped moderately with an existing base signal. A suggested next step is to isolate that stock-rate signal within low-index regimes.

**Later proposal**

In high common-index periods, groups whose V06 stock is high relative to V04 flow versus a rolling 36-month baseline earn higher next-month relative returns; a rolling baseline should handle structural drift better than submission 4's expanding one.

Expression: `regime(tsz(ratio(V06, V04), 36), "high")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear
