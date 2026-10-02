# Human migration spot-check

This is the fixed sample of 8 judgments selected by the registered random seed. Read each report and later proposal. Decide whether the proposal uses or tests at least one claim from the report. Similar vocabulary alone is insufficient.

Reply with `1 yes, 2 no, ...`. You may mark an item `unclear` for discussion. No answers have been filled in on your behalf.

The expression uses anonymous variables. lag shifts an input; chg measures a change; yoy is a year-over-year change; mavg averages; csrank ranks groups; tsz standardizes over time; spread compares standardized inputs; withT interacts with common tightness.

## Item 1

**Earlier report**

**Migration report**

Two submissions so far, and neither produced a usable signal.

The first used a standardized version of the V02 flow rate against its own expanding history. Its mean rank correlation was essentially zero, with a HAC t-statistic near zero. The regime split was unstable: slightly negative in low-T and clearly positive (0.12) in high-T. That suggests a regime-dependent sign, not the negative relation I hypothesized. This one failed.

The second used the share of positive monthly changes in V05, restricted to high-T. It was mildly negative (t of -0.7), with very high rank autocorrelation (0.77), so it is slow-moving. It also failed.

Next: test V02 interacted with T, and try faster-moving temporal features.

**Later proposal**

Groups whose V03 flow rate, smoothed over 6 months, is high relative to V04 flow rate (cross-sectionally standardized) have higher next-month returns, because a composition tilt toward V03 signals improving conditions. Expect positive IC in both T regimes.

Expression: `spread(mavg(V03,6),mavg(V04,6))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 2

**Earlier report**

**Migration report**

Two submissions so far, and neither produced a usable signal.

The first used a standardized version of the V02 flow rate against its own expanding history. Its mean rank correlation was essentially zero, with a HAC t-statistic near zero. The regime split was unstable: slightly negative in low-T and clearly positive (0.12) in high-T. That suggests a regime-dependent sign, not the negative relation I hypothesized. This one failed.

The second used the share of positive monthly changes in V05, restricted to high-T. It was mildly negative (t of -0.7), with very high rank autocorrelation (0.77), so it is slow-moving. It also failed.

Next: test V02 interacted with T, and try faster-moving temporal features.

**Later proposal**

Groups whose average hours V01 have risen faster than wage level V05 over 3 months, in cross-sectional standardized terms, earn higher next-month returns, and this effect is concentrated in high-T. Predicts positive rank IC.

Expression: `regime(spread(lchg(V01,3),lchg(V05,3)),"high")`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 3

**Earlier report**

**Migration report**

Two submissions so far, and neither produced a usable signal.

The first used a standardized version of the V02 flow rate against its own expanding history. Its mean rank correlation was essentially zero, with a HAC t-statistic near zero. The regime split was unstable: slightly negative in low-T and clearly positive (0.12) in high-T. That suggests a regime-dependent sign, not the negative relation I hypothesized. This one failed.

The second used the share of positive monthly changes in V05, restricted to high-T. It was mildly negative (t of -0.7), with very high rank autocorrelation (0.77), so it is slow-moving. It also failed.

Next: test V02 interacted with T, and try faster-moving temporal features.

**Later proposal**

Groups whose V04 flow rate rose more than their V06 stock rate over the last 6 months (standardized across groups) have higher next-month returns, extending the 3-month version that showed positive IC. Expect positive IC in both T regimes.

Expression: `spread(chg(V04,6),chg(V06,6))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 4

**Earlier report**

**Migration report**

**Failed:** My first feature, an interaction of two standardized stress-type variables (one flow rate, one stock rate), showed essentially no predictive power. Mean IC was slightly negative, the HAC t-stat was weak, and coverage was only about half, likely because of the long history requirement. My second submission was invalid because the hypothesis exceeded the word limit by two words, which wasted a slot.

**Learned:** The interaction's IC looked much stronger in the high-T regime than in the low-T regime, so the effect may be regime-dependent. Base correlation was low, so the feature is novel. Rank autocorrelation was moderate.

**Next:** Try a regime-conditioned pay-and-hours interaction, and count words carefully before submitting.

**Later proposal**

Groups whose V05 year-over-year change, smoothed over three months and standardized against its own expanding history, is high will have higher next-month returns, because smoothing reduces noise in the positive signal and raises rank stability.

Expression: `mavg(tsz(yoy(V05),"exp"),3)`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 5

**Earlier report**

**Migration report**

**Failed:** My first feature, an interaction of two standardized stress-type variables (one flow rate, one stock rate), showed essentially no predictive power. Mean IC was slightly negative, the HAC t-stat was weak, and coverage was only about half, likely because of the long history requirement. My second submission was invalid because the hypothesis exceeded the word limit by two words, which wasted a slot.

**Learned:** The interaction's IC looked much stronger in the high-T regime than in the low-T regime, so the effect may be regime-dependent. Base correlation was low, so the feature is novel. Rank autocorrelation was moderate.

**Next:** Try a regime-conditioned pay-and-hours interaction, and count words carefully before submitting.

**Later proposal**

Groups whose V03 flow rate is high relative to V04 flow rate, each standardized against its own 60-month history, earn higher next-month returns than other groups, with a positive mean IC.

Expression: `spread(tsz(V03,60),tsz(V04,60))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 6

**Earlier report**

**Migration Report**

**What worked (weakly):** The first attempt, a three-month change in the ratio of two turnover-type flow rates, ranked across groups, gave the only encouraging result. Mean IC was 0.03 and the HAC t-stat was 1.42. The signal was concentrated in low-T periods, and it was near zero in high-T periods. It is suggestive, not significant.

**What failed:** Regime-gating a spread between two flow rates (submission 2) covered only 58% of observations and had no high-T output. It gave a slightly negative IC. The stock-versus-flow standardized spread (submission 3) was negative, at -1.18 HAC t, and correlated 0.33 with base features. The pay-per-hours change was flat.

**Next:** Try changes in flow-rate ratios with longer smoothing, and avoid regime gating.

**Later proposal**

Groups with V03 high relative to V04, both standardized on a 60-month window and lightly smoothed over 3 months, will have higher next-month returns, extending the only significant positive result (submission 4) with modest noise reduction.

Expression: `spread(mavg(tsz(V03,60),3),mavg(tsz(V04,60),3))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 7

**Earlier report**

**Migration report**

**Failures:** The product of two long-history standardized measures (a flow rate and a stock rate) showed essentially zero predictive power (t-stat around -0.4), despite the stress-compounding rationale. The cross-sectional rank product of pay growth and hours change also produced nothing (mean IC zero), and was fairly redundant with existing features. One submission was invalid because the hypothesis exceeded the word limit, so count words carefully.

**Tentative finding:** A spread between two flow rates, each standardized against its own history, gave a positive IC, opposite to my predicted sign (t-stat about 1.9). It looked stronger in high-T periods. Coverage was limited, at about 54%, so it is suggestive only.

**Later proposal**

Groups whose V04 flow rate is high relative to V03 flow rate, each standardized against its own 60-month history, earn higher next-month returns, since the prior V03-minus-V04 spread had negative IC.

Expression: `spread(tsz(V04,60),tsz(V03,60))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear

## Item 8

**Earlier report**

**Migration report**

Four composition-style features were tried, all valid. None was statistically convincing.

The most promising was the smoothed cross-sectional contrast between average hours and hourly wage. Its mean IC was 0.03 (HAC t of 1.0), somewhat stronger in the high-T regime. That is suggestive but not significant.

The clearest failure was the high-T-only flow-rate contrast. It had an IC of -0.07 (t of -1.25), the opposite sign to my hypothesis, and coverage fell to 0.82.

The stock-versus-flow contrast and the wage-versus-turnover contrast both had ICs near zero.

Smoothed features have rank autocorrelation of 0.97 to 1.0, so their effective sample is small. Base correlations were low, at most 0.18.

**Later proposal**

Groups whose 3-month hours change ranks high relative to their separation-type rate V03 (cross-sectionally standardized, smoothed over 3 months) have healthier conditions, so this spread predicts higher next-month returns; sign is positive.

Expression: `spread(mavg(chg(V01,3),3),mavg(V03,3))`

**Does the proposal use or test a claim from the report?** Yes / No / Unclear
