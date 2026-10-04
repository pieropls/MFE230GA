# Study 1 robustness (B..) and Study 2.3 (T..) claims. Executed by build_results_book.py with claim(), t(), rel(), P and the labels in scope.
# The result files of Studies 2.1 and 2.2 keep the codes V2a..V2d inside; W, SC, W+MOM, HQ12 are the same variants.
d11, d11h, fz = t('d11_study1_robustness'), t('d11_a3_horizon_profile'), t('d11_freeze_check')
r1v, r1o, r1b, r1c = t('s23_r1_variants'), t('s23_r1_overlap'), t('s23_r1_hq12_battery'), t('s23_r1_validation')
r2, r2d, r3 = t('s23_r2_risk_overlay'), t('s23_r2_distribution'), t('s23_r3_rank_weighted')
r4, r4p, r5, r5r, r6 = t('s23_r4_agents_by_seed'), t('s23_r4_permutation'), t('s23_r5_tokens'), t('s23_r5_tokens_ic'), t('s23_r6_breadth')
r7, r8, r9, r9c = t('s23_r7_capacity'), t('s23_r8_judge_summary'), t('s23_r9_ablation_summary'), t('s23_r9_input_check')
tp, ct = t('s23_time_patterns'), t('s23_costs_turnover')
A3H = 'A3 agent features (Study 1 primary)'

# --- Study 1 robustness
claim('B01', 'Study 1 freeze record: the SHA-256 of FREEZE.json equals the hash stored in evaluation_started.json, and the test was opened after the freeze (0.040 s later, 2 Oct 2026, 06:00:09 UTC).',
      ['True', 'True', '0.040 s later'],
      [f'{fz}::col=ok;check=SHA-256 of FREEZE.json equals evaluation_started.freeze_sha256', f'{fz}::col=ok;check=Test opened after the freeze', f'{fz}::col=value;check=Test opened after the freeze'], CONF)
claim('B02', 'Of the 525 files in the freeze inventory, 338 are in the repository and 337 match their frozen hash; the one that differs is the human migration review, written after the test.',
      [525, 338, 337, 'outputs/human_migration_review.md'],
      [f'{fz}::col=value;check=Files in the freeze inventory', f'{fz}::col=value;check=of which present in the repository',
       f'{fz}::col=value;check=present files whose hash matches the inventory', f'{fz}::col=value;check=present files that differ'], CONF)
claim('B03', 'Block-bootstrap 90% interval for the test Sharpe (12-month blocks, 5,000 draws): A3 [-0.99, -0.16], A0 [-0.91, +0.20].', ['[-0.99, -0.16]', '[-0.91, +0.20]'],
      [f'{d11}::col=A3;item=Block-bootstrap 90% interval, test Sharpe', f'{d11}::col=A0;item=Block-bootstrap 90% interval, test Sharpe'], POST)
claim('B04', 'The A3 score has no IC at any horizon in the test: -0.021 (t -1.08) at 1 month, -0.004 (t -0.09) at 6, -0.013 (t -0.22) at 12, -0.000 (t -0.00) at 24.',
      [-0.021, -1.08, -0.004, -0.09, -0.013, -0.22, -0.000, -0.00],
      [f'{d11h}::col={c};book={A3H};h={h}' for h in [1, 6, 12, 24] for c in ['ic', 't']], POST)
claim('B05', 'A3 test Sharpe with the gross cap at 2, at 3 and with no cap: -0.58, -0.61, -0.62; realised volatility 7.8%, 9.7%, 10.3%; the cap binds in 87% and 35% of months.',
      [-0.58, -0.61, -0.62], [f'{r2}::col=sharpe;book=A3;cap={c}' for c in ['2', '3', 'none']], POST)
claim('B05b', 'A3 realised volatility by cap: 7.8% (cap 2), 9.7% (cap 3), 10.3% (no cap); cap binding in 87% and 35% of test months.', [7.8, 9.7, 10.3, 87, 35],
      [f'{r2}::col=realised_vol;book=A3;cap={c}' for c in ['2', '3', 'none']] + [f'{r2}::col=cap_binds_share;book=A3;cap={c}' for c in ['2', '3']], POST, scale=100)
claim('B06', 'The rank-weighted A3 book earns a test Sharpe of -0.49 with a transfer coefficient of 0.83 (top 3 / bottom 3: -0.58, 0.80).', [-0.49, 0.83, -0.58, 0.80],
      [f'{r3}::col=sharpe;book=A3;weighting=rank-weighted', f'{r3}::col=tc;book=A3;weighting=rank-weighted', f'{r3}::col=sharpe;book=A3;weighting=top 3 / bottom 3', f'{r3}::col=tc;book=A3;weighting=top 3 / bottom 3'], POST)
claim('B07', 'A0 (fixed rule) test Sharpe by data version: -0.36 as known, -0.16 first release, -0.26 revised, -0.27 fixed lag.', ['-0.36', '-0.16', '-0.26', '-0.27'],
      [f'{d11}::col=A0;item=Test Sharpe, data {v}' for v in ['as known', 'first release', 'revised', 'fixed lag']], CONF)
claim('B08', 'A0 by window: first test half -0.55, second half -0.20, last 18 months -1.56; factor alpha -0.25% a month (t -0.92).', ['-0.55', '-0.20', '-1.56', '-0.25% (-0.92)'],
      [f'{d11}::col=A0;item=Sharpe, first test half', f'{d11}::col=A0;item=Sharpe, second test half', f'{d11}::col=A0;item=Sharpe, last 18 months', f'{d11}::col=A0;item=Factor alpha per month (t)'], CONF)
claim('B09', 'Dropping one group at a time, A3 test Sharpe ranges from -0.70 (without wholesale) to -0.24 (without durable manufacturing).', '-0.70 (Wholesale) to -0.24 (Durable mfg)',
      f'{d11}::col=A3;item=Drop one group, Sharpe range', CONF)
claim('B10', 'Study 1 research-period deflated Sharpe (41 nominal trials): A3 0.003, A0 0.000.', ['0.003', '0.000'],
      [f'{d11}::col=A3;item=Deflated Sharpe, research (41 trials)', f'{d11}::col=A0;item=Deflated Sharpe, research (41 trials)'], CONF)

# --- R1 as-known rerun
claim('T01', 'R1 validation: raw features rebuilt from the as-known panel equal Study 1 saved features exactly (maximum difference 0), and the as-known A0 score equals the saved one to 4e-16.', [0, 0, 0],
      [f'{r1c}::col=value;check=raw F1-F5 rebuilt from panel_asof vs features_asof.raw_value: max abs difference',
       f'{r1c}::col=value;check=rows without a counterpart or with a missing-value mismatch',
       f'{r1c}::col=value;check=A0 from features_asof vs saved ASOF_A0_scores.csv, test window: max abs difference'], POST, decimals=9)
claim('T02', 'As-known test Sharpe: W +0.13, SC +0.24, W+MOM +0.46, HQ12 +0.20 (fixed lag: +0.16, -0.15, +0.35, +0.29).', [0.13, 0.24, 0.46, 0.20, 0.16, -0.15, 0.35, 0.29],
      [f'{r1v}::col=sharpe_asknown;variant={v};window=test' for v in ['W', 'SC', 'W+MOM', 'HQ12']] + [f'{r1v}::col=sharpe_fixedlag;variant={v};window=test' for v in ['W', 'SC', 'W+MOM', 'HQ12']], POST)
claim('T03', 'HQ12 as known: 12-month test IC +0.085 (t 2.26) against +0.096 (t 2.43) with fixed lags; W one-month IC +0.041 (t 1.73) against +0.049 (t 2.04).', [0.085, 2.26, 0.096, 2.43, 0.041, 1.73],
      [f'{r1v}::col=ic_asknown;variant=HQ12;window=test', f'{r1v}::col=ic_t_asknown;variant=HQ12;window=test', f'{r1v}::col=ic_fixedlag;variant=HQ12;window=test', f'{r1v}::col=ic_t_fixedlag;variant=HQ12;window=test',
       f'{r1v}::col=ic_asknown;variant=W;window=test', f'{r1v}::col=ic_t_asknown;variant=W;window=test'], POST)
claim('T04', 'Share of test months in which the as-known and fixed-lag scores pick the same top three and the same bottom three groups: HQ12 39% and 51%, W 76% and 70%, W+MOM 84% and 74%, SC 0% and 0%.',
      [39, 51, 76, 70, 84, 74, 0, 0], [f'{r1o}::col={c};variant={v}' for v in ['HQ12', 'W', 'W+MOM', 'SC'] for c in ['same_top3', 'same_bottom3']], POST, scale=100)
claim('T05', 'HQ12 as known by window: research +0.54, test +0.20, full +0.31, post-2010 +0.23, last 18 months +0.14.', [0.54, 0.20, 0.31, 0.23, 0.14],
      [f'{r1v}::col=sharpe_asknown;variant=HQ12;window={w}' for w in ['research', 'test', 'full', 'post-2010', 'last 18m']], POST)
claim('T06', 'HQ12 battery as known: first test half -0.23, second +0.49; break-even cost 50 bp; drop-one test Sharpe between +0.05 and +0.36; hires only +0.19, quits only +0.17; holding 9 months +0.16, 18 months +0.11.',
      [-0.23, 0.49, 50, 0.05, 0.36, 0.19, 0.17, 0.16, 0.11],
      [f'{r1b}::col=as_known;check={c}' for c in ['First test half, Sharpe', 'Second test half, Sharpe', 'Break-even cost, test (bp)', 'Drop one group, minimum test Sharpe', 'Drop one group, maximum test Sharpe',
                                                'Component hires only, test Sharpe', 'Component quits only, test Sharpe', 'Holding 9 months, test Sharpe', 'Holding 18 months, test Sharpe']], POST)
claim('T07', 'HQ12 as known: bootstrap 90% interval [-0.14, +0.57] in the test and [+0.02, +0.60] over the full sample; alpha t 0.92 (test) and 1.81 (full sample, 12 HAC lags); deflated Sharpe 0.02 at 162 looks.',
      [-0.14, 0.57, 0.02, 0.60, 0.92, 1.81, 0.02],
      [f'{r1b}::col=as_known;check={c}' for c in ['Bootstrap 90% interval, test: low', 'Bootstrap 90% interval, test: high', 'Bootstrap 90% interval, full: low', 'Bootstrap 90% interval, full: high',
                                                'Alpha t, test, HAC 12', 'Alpha t, full, HAC 12']] + [f'{r1v}::col=dsr_162_asknown;variant=HQ12;window=test'], POST)
claim('T08', 'As known, the last 18 months: W -1.31, SC +1.38, W+MOM -0.94, HQ12 +0.14; W+MOM test alpha t 1.93, the largest of the four.', [-1.31, 1.38, -0.94, 0.14, 1.93],
      [f'{r1v}::col=sharpe_asknown;variant={v};window=last 18m' for v in ['W', 'SC', 'W+MOM', 'HQ12']] + [f'{r1v}::col=alpha_t_asknown;variant=W+MOM;window=test'], POST)
claim('T09', 'SC signs re-learned on as-known research data: negative for openings, hires, layoffs and hours, positive for quits and wages (with fixed lags only hours was negative).', [-1, -1, 1, -1, -1, 1],
      [f'{t("s23_r1_sc_signs")}::col=sign;signal={k}' for k in ['F1', 'F2', 'F3', 'F4', 'F5', 'W']], POST)

# --- R2 / R3 risk overlay and rank-weighted books
claim('T10', 'Median gross exposure needed to reach 10% ex-ante volatility in the test: 2.60 for A3 and 2.45 for HQ12 (5th to 95th percentile 1.85 to 4.19 and 1.79 to 4.24); median unit-book volatility 7.5% and 6.4%.',
      [2.60, 2.45, 1.85, 4.19, 1.79, 4.24],
      [f'{r2d}::col=gross_needed_p50;book=A3', f'{r2d}::col=gross_needed_p50;book=HQ12', f'{r2d}::col=gross_needed_p5;book=A3', f'{r2d}::col=gross_needed_p95;book=A3',
       f'{r2d}::col=gross_needed_p5;book=HQ12', f'{r2d}::col=gross_needed_p95;book=HQ12'], POST)
claim('T10b', 'Median ex-ante volatility of the unit book: 7.5% (A3) and 6.4% (HQ12).', [7.5, 6.4], [f'{r2d}::col=unit_vol_p50;book=A3', f'{r2d}::col=unit_vol_p50;book=HQ12'], POST, scale=100)
claim('T11', 'HQ12 test Sharpe with the cap at 2, 3 and none: +0.29, +0.24, +0.24; realised volatility 8.7%, 10.5%, 11.1%; the cap binds in 83% and 39% of months.', [0.29, 0.24, 0.24],
      [f'{r2}::col=sharpe;book=HQ12;cap={c}' for c in ['2', '3', 'none']], POST)
claim('T11b', 'HQ12 realised volatility by cap 8.7%, 10.5%, 11.1%; cap binding 83% and 39% of test months.', [8.7, 10.5, 11.1, 83, 39],
      [f'{r2}::col=realised_vol;book=HQ12;cap={c}' for c in ['2', '3', 'none']] + [f'{r2}::col=cap_binds_share;book=HQ12;cap={c}' for c in ['2', '3']], POST, scale=100)
claim('T12', 'Rank-weighted HQ12: test Sharpe +0.31, transfer coefficient 0.49, monthly turnover 0.37 (top 3 / bottom 3: +0.29, 0.48, 0.37); fundamental-law implied IR +0.17 for both.', [0.31, 0.49, 0.37, 0.29, 0.48, 0.17, 0.17],
      [f'{r3}::col=sharpe;book=HQ12;weighting=rank-weighted', f'{r3}::col=tc;book=HQ12;weighting=rank-weighted', f'{r3}::col=turnover;book=HQ12;weighting=rank-weighted',
       f'{r3}::col=sharpe;book=HQ12;weighting=top 3 / bottom 3', f'{r3}::col=tc;book=HQ12;weighting=top 3 / bottom 3',
       f'{r3}::col=implied_ir;book=HQ12;weighting=rank-weighted', f'{r3}::col=implied_ir;book=HQ12;weighting=top 3 / bottom 3'], POST)

# --- R4 / R5 agents
claim('T13', 'Islands minus independent, best research IC per seed: -0.034 in Study 1 (largest seed range 0.056, permutation p 0.30) and +0.076 in Study 1b (seed range 0.099, p 0.10); in both the gap is within the seed range.',
      [-0.034, 0.056, 0.30, 0.076, 0.099, 0.10, 'True', 'True'],
      [f'{r4p}::col={c};study={s};metric=best_ic' for s in ['Study 1 (Sonnet)', 'Study 1b (Opus)'] for c in ['islands_minus_independent', 'largest_seed_range_within_arm', 'perm_p_two_sided']]
      + [f'{r4p}::col=gap_within_seed_range;study={s};metric=best_ic' for s in ['Study 1 (Sonnet)', 'Study 1b (Opus)']], POST)
claim('T14', 'Share of valid independent-arm proposals with a regime gate in Study 1: 29%, 24% and 15% across the three seeds.', [29, 24, 15],
      [f'{r4}::col=regime_share;study=Study 1 (Sonnet);arm=independent;seed={s}' for s in [1, 2, 3]], POST, scale=100)
claim('T15', 'Tokens per proposal call: 2,239 (independent) and 2,485 (islands) in Study 1; 3,344 and 3,963 in Study 1b. Spearman correlation between a proposal\'s output tokens and its research IC: +0.13 (Study 1), +0.41 (Study 1b).',
      [2239, 2485, 3344, 3963, 0.13, 0.41],
      [f'{r5}::col=tokens_per_call;study={s};arm={a}' for s in ['Study 1 (Sonnet)', 'Study 1b (Opus)'] for a in ['independent', 'islands']]
      + [f'{r5r}::col=spearman_output_tokens_vs_ic;study={s}' for s in ['Study 1 (Sonnet)', 'Study 1b (Opus)']], POST)

# --- R6 / R7 breadth and capacity
claim('T16', 'Participation ratio of the 13-group correlation matrix: 2.0 for excess returns, 9.1 for relative returns, 7.4 for z(W) and 10.1 for the HQ12 score.', [2.0, 9.1, 7.4, 10.1],
      [f'{r6}::col=participation_ratio;matrix={m}' for m in ['13 group excess returns', '13 group relative returns (group minus equal-weight mean)', 'z(W) across groups', 'HQ12 score across groups']], POST, decimals=1)
claim('T17', 'Capacity with the proxy ETFs: the binding ETF is PEJ (average daily volume $3.2 million); monthly trading reaches 1% of it at $0.5 million of AUM for A3 and $1.2 million for HQ12, and 5% at $2.5 and $5.9 million; SPY trades $47 billion a day.',
      ['PEJ', 3.2, 0.5, 1.2, 2.5, 5.9, 47],
      [f'{r7}::col=binding_etf;book=HQ12', f'{r7}::col=binding_adv_usd_m;book=HQ12', f'{r7}::col=aum_at_1pct_adv_usd_m;book=A3', f'{r7}::col=aum_at_1pct_adv_usd_m;book=HQ12',
       f'{r7}::col=aum_at_5pct_adv_usd_m;book=A3', f'{r7}::col=aum_at_5pct_adv_usd_m;book=HQ12', f'{r7}::col=spy_adv_usd_bn;book=HQ12'], POST, decimals=1)

# --- R8 / R9 judge and feedback ablation
SJ, OJ = 'Study 1 (Sonnet)', 'Study 1b (Opus)'
claim('T18', 'Judge with a verbatim quote, Study 1 pairs (Sonnet): 8 of 8 answers usable (2 of 8 originally), agreement with the human 7 of 8, one false yes.', [8, 2, 7, 1],
      [f'{r8}::col=defined;study={SJ};judge=judge with verbatim quote', f'{r8}::col=defined;study={SJ};judge=original judge', f'{r8}::col=agree;study={SJ};judge=judge with verbatim quote',
       f'{r8}::col=false_yes;study={SJ};judge=judge with verbatim quote'], POST)
claim('T19', 'Judge with a verbatim quote, Study 1b pairs (Opus): 7 of 17 answers were JSON only; accepting fenced JSON, agreement with the human is 9 of 17 (10 of 17 originally) with 8 false yes (7 originally) and no missed yes.',
      [7, 9, 10, 8, 7, 0],
      [f'{r8}::col=defined;study={OJ};judge=judge with verbatim quote', f'{r8}::col=agree;study={OJ};judge=with quote, fenced JSON accepted (supplementary)', f'{r8}::col=agree;study={OJ};judge=original judge',
       f'{r8}::col=false_yes;study={OJ};judge=with quote, fenced JSON accepted (supplementary)', f'{r8}::col=false_yes;study={OJ};judge=original judge',
       f'{r8}::col=missed_yes;study={OJ};judge=with quote, fenced JSON accepted (supplementary)'], POST)
claim('T20', 'Feedback ablation (independent arm, research data, 3 seeds, 54 proposals per condition): with the tightness-tercile split 4 of 48 valid proposals used a regime gate (8%); without it 3 of 50 (6%).',
      [54, 48, 4, 8, 54, 50, 3, 6],
      [f'{r9}::col={c};condition=A_with_tercile_split' for c in ['proposals', 'valid', 'regime_proposals', 'regime_share']]
      + [f'{r9}::col={c};condition=B_without_tercile_split' for c in ['proposals', 'valid', 'regime_proposals', 'regime_share']], POST, scale=[1, 1, 1, 100, 1, 1, 1, 100])
claim('T21', 'The reconstructed research inputs of the ablation reproduce 94 of 98 saved Study 1 feedbacks exactly; the largest difference is 0.11.', [98, 94, 0.11],
      [f'{r9c}::col=saved_valid_candidates', f'{r9c}::col=feedback_reproduced_exactly', f'{r9c}::col=largest_abs_difference'], POST)

# --- report tables
claim('T22', 'Net Sharpe, full sample / post-2010 / last 18 months: A0 -0.48/-0.41/-1.56, A1 -0.52/-0.66/+0.73, A1-T -0.58/-0.73/-0.37, A3 -0.44/-0.62/+0.85, A4 -0.56/-0.74/+1.23 (Study 1); W +0.15/+0.12/-1.71, SC -0.11/-0.16/-1.34, W+MOM +0.32/+0.24/-0.78, HQ12 +0.35/+0.30/+0.29 (Study 2).',
      [-0.48, -0.41, -1.56, -0.52, -0.66, 0.73, -0.58, -0.73, -0.37, -0.44, -0.62, 0.85, -0.56, -0.74, 1.23, 0.15, 0.12, -1.71, -0.11, -0.16, -1.34, 0.32, 0.24, -0.78, 0.35, 0.30, 0.29],
      [f'{tp}::col={c};strategy={P.STRATEGY_NAMES[s]}' for s in ['A0', 'A1', 'A1-T', 'A3', 'A4', 'W', 'SC', 'W+MOM', 'HQ12'] for c in ['full', 'post_2010', 'last_18m']], f'{CONF} / {POST}')
claim('T23', 'Annual turnover, cost drag and break-even cost in the test: A3 11.0x, 1.11%, -32 bp; W 4.7x, 0.47%, +46 bp; SC 8.7x, 0.88%, -5 bp; W+MOM 5.8x, 0.59%, +62 bp; HQ12 4.4x, 0.44%, +68 bp.',
      [11.0, 1.11, -32, 4.7, 0.47, 46, 8.7, 0.88, -5, 5.8, 0.59, 62, 4.4, 0.44, 68],
      [f'{ct}::col={c};book={P.STRATEGY_NAMES[s]}' for s in ['A3', 'W', 'SC', 'W+MOM', 'HQ12'] for c in ['annual_turnover', 'cost_drag_pa', 'breakeven_bp']], f'{CONF} / {POST}',
      scale=[1, 100, 1] * 5)
claim('T24', 'Rank-weighted books: A3 turnover 10.3x a year, break-even -24 bp; HQ12 4.4x, +69 bp.', [10.3, -24, 4.4, 69],
      [f'{ct}::col=annual_turnover;book=A3 rank-weighted', f'{ct}::col=breakeven_bp;book=A3 rank-weighted', f'{ct}::col=annual_turnover;book=HQ12 rank-weighted', f'{ct}::col=breakeven_bp;book=HQ12 rank-weighted'], POST)
claim('T25', 'The Study 2.3 specification was hashed (068a3e03...) at 2026-10-04T09:18:39Z, before its first output; deflated Sharpe ratios in Study 2.3 use 162 looks.', '068a3e0396332514ee3b76677f31b9c1ff6bfea7362d9e91d69ecc013e791528',
      'analysis/specs/study2_3_robustness.sha256::line=1', POST)
