# Exploratory diagnostics (post-hoc, not part of either preregistered study)

## 1. Group-return reconstruction vs saved sealed ledgers

| study | strategy | max_abs_error | gross_cap_binds_% | mean_ex_ante_vol | realized_vol | cost_%_per_yr |
|---|---|---|---|---|---|---|
| Sonnet (original) | A0 | 9.71e-17 | 80.3 | 0.0795 | 0.0966 | 1.01 |
| Sonnet (original) | A1 | 1.01e-16 | 88 | 0.0754 | 0.0786 | 1.11 |
| Sonnet (original) | A3 | 1.28e-16 | 86.6 | 0.0754 | 0.0785 | 1.11 |
| Sonnet (original) | A4 | 1.08e-16 | 90.8 | 0.073 | 0.0775 | 1.35 |
| Opus (follow-up) | A0 | 9.71e-17 | 80.3 | 0.0795 | 0.0966 | 1.01 |
| Opus (follow-up) | A1 | 1.01e-16 | 88 | 0.0754 | 0.0786 | 1.11 |
| Opus (follow-up) | A3 | 1.1e-16 | 91.5 | 0.0735 | 0.075 | 1.16 |
| Opus (follow-up) | A4 | 1.08e-16 | 93 | 0.0735 | 0.0837 | 1.14 |

## 2. Sealed-period gross P&L by industry (sum of monthly contributions)

| industry | A0 (Sonnet) | A0 (Sonnet) % months long | A1 (Sonnet) | A1 (Sonnet) % months long | A3 (Sonnet) | A3 (Sonnet) % months long | A4 (Opus) | A4 (Opus) % months long |
|---|---|---|---|---|---|---|---|---|
| Mining | -0.081 | 47 | +0.105 | 34 | +0.072 | 33 | -0.141 | 31 |
| Construction | +0.023 | 34 | -0.197 | 36 | -0.192 | 36 | -0.184 | 42 |
| Durable mfg | -0.140 | 27 | +0.008 | 33 | +0.018 | 31 | +0.273 | 64 |
| Nondurable mfg | +0.035 | 32 | +0.065 | 30 | +0.054 | 32 | -0.002 | 44 |
| Wholesale | +0.017 | 25 | +0.143 | 32 | +0.149 | 31 | +0.050 | 32 |
| Retail | +0.006 | 32 | -0.015 | 39 | +0.002 | 39 | +0.001 | 35 |
| Transport+Util | -0.058 | 27 | +0.031 | 48 | +0.014 | 47 | +0.063 | 42 |
| Information | +0.056 | 30 | -0.060 | 30 | -0.058 | 30 | +0.088 | 41 |
| Finance+Ins | -0.011 | 35 | -0.146 | 37 | -0.163 | 34 | -0.121 | 25 |
| Real estate | -0.084 | 37 | -0.072 | 23 | -0.016 | 24 | +0.135 | 23 |
| Prof+Bus svcs | +0.038 | 36 | -0.119 | 20 | -0.122 | 18 | -0.037 | 27 |
| Health care | -0.129 | 52 | -0.259 | 39 | -0.262 | 41 | -0.166 | 39 |
| Accom+Food | -0.014 | 29 | +0.086 | 44 | +0.045 | 46 | +0.080 | 45 |

## 3. Single-signal rank IC vs next-month relative return (revised data, fixed lags)

W = 12-month log growth of 3-month-average hourly earnings (the wage half of the dropped F6).
A0 = (F1 + F2 - F4 + F5)/4 as preregistered. IndMom = 12-month industry momentum.

| signal | research 2004-05..2014-09 | test 2014-11..2026-08 | full 2004-05..2026-08 |
|---|---|---|---|
| F1 | +0.001 (t +0.02) | -0.011 (t -0.44) | -0.005 (t -0.30) |
| F2 | +0.012 (t +0.48) | +0.013 (t +0.48) | +0.013 (t +0.71) |
| F3 | +0.014 (t +0.50) | +0.002 (t +0.12) | +0.009 (t +0.50) |
| F4 | +0.033 (t +1.07) | +0.026 (t +0.94) | +0.028 (t +1.38) |
| F5 | -0.015 (t -0.70) | -0.009 (t -0.43) | -0.012 (t -0.84) |
| W | +0.039 (t +1.80) | +0.041 (t +1.66) | +0.040 (t +2.37) |
| A0 | -0.018 (t -0.69) | -0.006 (t -0.25) | -0.011 (t -0.58) |
| IndMom 12-2 | +0.036 (t +1.26) | +0.003 (t +0.11) | +0.020 (t +0.99) |
| IndMom 12-1 | +0.050 (t +1.61) | +0.017 (t +0.65) | +0.034 (t +1.72) |

## 4. IC by horizon, full sample 2004-05..2026-08 (HAC lags = h+5)

| signal | h=1 | h=3 | h=6 | h=12 |
|---|---|---|---|---|
| F1 | -0.005 (t -0.3) | +0.007 (t +0.2) | -0.011 (t -0.3) | -0.039 (t -0.9) |
| F2 | +0.013 (t +0.7) | +0.002 (t +0.1) | +0.002 (t +0.1) | -0.062 (t -2.1) |
| F3 | +0.009 (t +0.5) | -0.013 (t -0.6) | -0.022 (t -0.8) | -0.065 (t -1.7) |
| F4 | +0.028 (t +1.4) | +0.005 (t +0.2) | +0.000 (t +0.0) | -0.036 (t -1.3) |
| F5 | -0.012 (t -0.8) | -0.026 (t -1.2) | -0.046 (t -1.6) | -0.051 (t -1.6) |
| W | +0.040 (t +2.4) | +0.041 (t +1.9) | +0.045 (t +1.6) | +0.028 (t +0.7) |
| A0 | -0.011 (t -0.6) | -0.002 (t -0.1) | -0.020 (t -0.6) | -0.049 (t -1.5) |
| IndMom 12-2 | +0.020 (t +1.0) | +0.025 (t +0.8) | +0.048 (t +1.2) | +0.029 (t +0.6) |

## 5. Tightness regime balance

| period | expanding low | expanding middle | expanding high | T rising (12m) | T falling (12m) | V/U > 1 | T min | T max |
|---|---|---|---|---|---|---|---|---|
| research | 55.0 | 29.0 | 41.0 | 93.0 | 32.0 | 0.0 | -1.88 | -0.3 |
| test | 3.0 | 6.0 | 132.0 | 88.0 | 53.0 | 75.0 | -1.61 | 0.71 |

## 6. Selected agent features: months with a defined IC, research vs sealed

| study | arm | candidate | expression | research IC | research t | research n | sealed IC | sealed n |
|---|---|---|---|---|---|---|---|---|
| Sonnet (original) | independent | independent_1_Temporal_3 | `regime(yoy(V05),"low")` | 0.065 | 1.636 | 48 |  | 3 |
| Sonnet (original) | independent | independent_1_Interactions_4 | `regime(spread(tsz(V04,60),tsz(V02,60)),"low")` | 0.070 | 1.531 | 43 |  | 3 |
| Sonnet (original) | islands | islands_1_Composition_5 | `spread(chg(V04,6),chg(V06,6))` | 0.052 | 1.895 | 120 | -0.004 | 142 |
| Sonnet (original) | islands | islands_1_Composition_2 | `spread(chg(V04,3),chg(V06,3))` | 0.037 | 1.575 | 123 | -0.023 | 142 |
| Opus (follow-up) | independent | independent_1_Interactions_6 | `mult(regime(tsz(V02,"exp"),"high"),csrank(tsz(V06,"exp")))` | 0.088 | 1.642 | 15 | -0.028 | 133 |
| Opus (follow-up) | islands | islands_1_Composition_4 | `regime(spread(chg(V03,3),chg(V02,3)),"low")` | 0.125 | 3.556 | 48 |  | 3 |
| Opus (follow-up) | islands | islands_1_Temporal_4 | `tsz(lchg(lag(V05,1),12),36)` | 0.064 | 2.158 | 78 | 0.022 | 142 |
| Opus (follow-up) | islands | islands_1_Temporal_6 | `tsz(lchg(lag(V01,1),12),36)` | 0.057 | 2.080 | 78 | 0.011 | 142 |

## 7. Ridge penalty selected by CV (grid 0.01..1000) and research-period net Sharpe

| study | strategy | alpha | research Sharpe | research IC | IC t | primary |
|---|---|---|---|---|---|---|
| Sonnet (original) | A0 | n/a (fixed rule) | -0.441 | 0.012 | 0.442 |  |
| Sonnet (original) | A1 | 1000.0 | -0.541 | -0.023 | -0.690 |  |
| Sonnet (original) | A1-T | 1000.0 | -0.548 | -0.030 | -0.951 |  |
| Sonnet (original) | A3 | 1000.0 | -0.132 | 0.014 | 0.416 | yes |
| Sonnet (original) | A4 | 1000.0 | -0.181 | 0.036 | 1.228 |  |
| Opus (follow-up) | A0 | n/a (fixed rule) | -0.441 | 0.012 | 0.442 |  |
| Opus (follow-up) | A1 | 1000.0 | -0.541 | -0.023 | -0.690 |  |
| Opus (follow-up) | A1-T | 1000.0 | -0.548 | -0.030 | -0.951 |  |
| Opus (follow-up) | A3 | 1000.0 | -0.482 | -0.028 | -0.945 |  |
| Opus (follow-up) | A4 | 1000.0 | -0.403 | 0.027 | 0.939 | yes |

