# v3 robustness-battery claims (POST-HOC). Executed by build_results_book.py with claim(), t(), rel(), P and labels in scope.
r1, r2, r3, r4 = t('v3_r1_components.csv'), t('v3_r2_horizon_profile.csv'), t('v3_r3_holding.csv'), t('v3_r4_subperiods.csv')
r5, r6, r7s, r7 = t('v3_r5_costs.csv'), t('v3_r6_alpha.csv'), t('v3_r7_dropone_summary.csv'), t('v3_r7_dropone.csv')
r8, r9, r11, dsr, rd = t('v3_r8_tightness.csv'), t('v3_r9_bootstrap.csv'), t('v3_r11_fundamental_law.csv'), t('v3_dsr132.csv'), t('v3_reading.csv')

claim('R1a', 'Held 12 months, hires alone earn a test Sharpe of +0.19 and quits alone +0.16; openings +0.42 and layoffs +0.16 (both with the same negative sign, for contrast).', [0.19, 0.16, 0.42, 0.16],
      [f'{r1}::col=sharpe;window=test;book={b}' for b in ['hires only', 'quits only', 'openings (contrast)', 'layoffs (contrast)']], POST)
claim('R1b', 'Hires alone have a test 12-month IC of +0.093 (t 2.90); quits alone +0.085 (t 1.75).', [0.093, 2.90, 0.085, 1.75],
      [f'{r1}::col=ic12;window=test;book=hires only', f'{r1}::col=ic12_t;window=test;book=hires only', f'{r1}::col=ic12;window=test;book=quits only', f'{r1}::col=ic12_t;window=test;book=quits only'], POST)
claim('R2a', 'Test-window IC of the V2d score by horizon: -0.020 at 1 month (t -0.87), +0.069 at 9 (t 1.98), +0.096 at 12 (t 2.43), +0.085 at 18 (t 2.00), +0.063 at 24 (t 1.86).',
      [-0.020, -0.87, 0.069, 1.98, 0.096, 2.43, 0.085, 2.00, 0.063, 1.86],
      [f'{r2}::col={c};window=test;h={h}' for h in [1, 9, 12, 18, 24] for c in ['ic', 't']], POST)
claim('R2b', 'The 12-month IC of the V2d score is +0.047 (t 0.90) in research and +0.071 (t 2.06) over the full sample.', [0.047, 0.90, 0.071, 2.06],
      [f'{r2}::col=ic;window=research;h=12', f'{r2}::col=t;window=research;h=12', f'{r2}::col=ic;window=full;h=12', f'{r2}::col=t;window=full;h=12'], POST)
claim('R3a', 'Test Sharpe by holding period: +0.05 at 6 months, +0.14 at 9, +0.29 at 12, +0.30 at 18.', [0.05, 0.14, 0.29, 0.30], [f'{r3}::col=test;holding={h}' for h in [6, 9, 12, 18]], POST)
claim('R3b', 'Research Sharpe by holding period: +0.31 at 6 months, +0.43 at 9, +0.50 at 12, +0.58 at 18.', [0.31, 0.43, 0.50, 0.58], [f'{r3}::col=research;holding={h}' for h in [6, 9, 12, 18]], POST)
claim('R4a', 'V2d test Sharpe was -0.21 in the first half (71 months) and +0.64 in the second half.', [-0.21, 71, 0.64],
      [f'{r4}::col=sharpe;Window=test: first half', f'{r4}::col=months;Window=test: first half', f'{r4}::col=sharpe;Window=test: second half'], POST)
claim('R4b', 'V2d test Sharpe excluding Mar 2020-Dec 2021: +0.37; pre-2020: +0.14; 2020 onward: +0.37. Full-sample halves: +0.33 and +0.38.', [0.37, 0.14, 0.37, 0.33, 0.38],
      [f'{r4}::col=sharpe;Window={s}' for s in ['test: excl. Mar 2020-Dec 2021', 'test: pre-2020', 'test: 2020 onward', 'full: first half', 'full: second half']], POST)
claim('R4c', 'The 12-month IC of V2d was positive in both test halves (+0.097 and +0.095) even though the first-half Sharpe was negative.', [0.097, 0.095],
      [f'{r4}::col=ic12;Window=test: first half', f'{r4}::col=ic12;Window=test: second half'], POST)
claim('R5a', 'V2d test Sharpe: +0.34 at 0 bp, +0.29 at 10, +0.22 at 25, +0.09 at 50 bp; break-even industry cost 68 bp (69 bp full sample).', [0.34, 0.29, 0.22, 0.09, 68, 69],
      [f'{r5}::col=sharpe_{c}bp;Window=test' for c in [0, 10, 25, 50]] + [f'{r5}::col=breakeven_bp;Window=test', f'{r5}::col=breakeven_bp;Window=full'], POST)
claim('R6a', 'With 12 HAC lags, V2d alpha is +0.26% a month in the test and +0.26% over the full sample.', [0.26, 0.26],
      [f'{r6}::col=coef;window=test;factor=intercept', f'{r6}::col=coef;window=full;factor=intercept'], POST, scale=100)
claim('R6a2', 'The t-statistics of the V2d alpha with 12 HAC lags are 1.48 (test) and 1.92 (full sample).', [1.48, 1.92],
      [f'{r6}::col=t;window=test;factor=intercept', f'{r6}::col=t;window=full;factor=intercept'], POST)
claim('R6b', 'V2d loads against profitability in the test: RMW -0.36 (t -4.45) and SMB -0.17 (t -2.24); market, momentum and industry-momentum loadings are small.', [-0.36, -4.45, -0.17, -2.24],
      [f'{r6}::col=coef;window=test;factor=RMW', f'{r6}::col=t;window=test;factor=RMW', f'{r6}::col=coef;window=test;factor=SMB', f'{r6}::col=t;window=test;factor=SMB'], POST)
claim('R7a', 'Dropping any one industry leaves the V2d test Sharpe between +0.18 (without health care) and +0.48 (without real estate), median +0.30.', [0.18, 0.30, 0.48, 'Health care', 'Real estate'],
      [f'{r7s}::col=test_sharpe;statistic=minimum', f'{r7s}::col=test_sharpe;statistic=median', f'{r7s}::col=test_sharpe;statistic=maximum',
       f'{r7s}::col=test_sharpe;statistic=industry whose removal lowers test Sharpe most', f'{r7s}::col=test_sharpe;statistic=industry whose removal raises test Sharpe most'], POST)
claim('R8a', 'V2d net Sharpe by regime at the decision (test): -0.00 when T rose over 12 months, +0.66 when it fell; +0.72 when V/U > 1, -0.14 when V/U < 1.', [-0.00, 0.66, 0.72, -0.14],
      [f'{r8}::col=sharpe;window=test;regime={g}' for g in ['T rising', 'T falling', 'V/U > 1', 'V/U < 1']], POST)
claim('R8b', 'The 12-month IC of V2d is highest when T is rising (+0.115, t 2.52) although the Sharpe in those months is zero.', [0.115, 2.52],
      [f'{r8}::col=ic12;window=test;regime=T rising', f'{r8}::col=ic12_t;window=test;regime=T rising'], POST)
claim('R9a', 'Block-bootstrap 90% interval for the V2d Sharpe: [-0.07, +0.65] in the test (includes zero) and [+0.05, +0.64] over the full sample (excludes zero).', [-0.07, 0.65, 0.05, 0.64],
      [f'{r9}::col=low;Window=test', f'{r9}::col=high;Window=test', f'{r9}::col=low;Window=full', f'{r9}::col=high;Window=full'], POST)
claim('R11a', 'Fundamental law, test window: A3 IC -0.021 x sqrt(156) x TC 0.80 implies IR -0.21 (realised -0.58); V2a IC +0.049 x sqrt(156) x TC 0.91 implies +0.56 (realised +0.16); V2d IC +0.096 x sqrt(13) x TC 0.48 implies +0.17, ceiling +0.35 (realised +0.29).',
      [-0.021, 0.80, -0.21, -0.58, 0.049, 0.91, 0.56, 0.16, 0.096, 0.48, 0.17, 0.35, 0.29],
      [f'{r11}::col={c};Book (test window)=A3 primary' for c in ['ic', 'tc', 'implied_ir', 'realised_sharpe']] + [f'{r11}::col={c};Book (test window)=V2a wage growth' for c in ['ic', 'tc', 'implied_ir', 'realised_sharpe']]
      + [f'{r11}::col={c};Book (test window)=V2d -(hires+quits) 12m' for c in ['ic', 'tc', 'implied_ir', 'ceiling_ir_tc1', 'realised_sharpe']], POST)
claim('R12', 'With N_trials raised to 132, the V2d deflated Sharpe is 0.05 in the test and 0.16 over the full sample; the benchmark Sharpe that 132 null trials would produce is 0.76 (test) and 0.56 (full).', [0.05, 0.16, 0.76, 0.56],
      [f'{dsr}::col=dsr_132;variant=V2d;window=test', f'{dsr}::col=dsr_132;variant=V2d;window=full', f'{dsr}::col=benchmark_annual_sharpe_132;variant=V2d;window=test', f'{dsr}::col=benchmark_annual_sharpe_132;variant=V2d;window=full'], POST)
claim('R13', 'Against the pre-declared battery rule, V2d fails only R4 (both test halves positive); R1, R2, R3, R5, R7 and R9 hold.', ['no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes'],
      [f'{rd}::col=holds;condition={c}' for c in ['R4 both test halves Sharpe > 0', 'R1 hires-only and quits-only test Sharpe > 0', 'R2 test 12m IC t >= 2 and 1m IC t < 2', 'R3 holding 9 and 18 months test Sharpe > 0',
                                                   'R5 test break-even cost > 25 bp', 'R7 minimum drop-one test Sharpe > 0', 'R9 90% interval excludes 0 (test or full)']], POST)
claim('R10', 'R10 (as-known ALFRED rerun) was not run: no FRED API key.', 'not run: no key', f'{t("v3_r10_asknown.csv")}::col=status;check=R10 as-known (ALFRED vintage) rerun of V2a-V2d', POST)
