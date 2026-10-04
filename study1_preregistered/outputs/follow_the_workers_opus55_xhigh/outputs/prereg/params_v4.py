"""Prespecified research constants; no data reads or model execution on import."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
OUT = ROOT / 'outputs'
CACHE = ROOT / 'data' / 'cache'
SOURCE_ARCHIVE = Path('/Users/alex/Downloads/230GA_Project_Data.zip')
SOURCE_SHA256 = 'ce3c625da9baf3319d45af617aac9dbea6bdef219c2be6f4c9fe51b0193756a3'
SEED = 230
RESEARCH_START = '2004-05'
RESEARCH_END = '2014-10'
SELECTION_END = '2014-09'
FIRST_SEALED_DECISION = '2014-10-31'
RESEARCH_SNAPSHOT = '2014-10-30'
LAST_RETURN = '2026-08'
FEATURE_START = '2002-04'
CORE_AVAILABILITY = '2011-03-04'
VINTAGE_ADMISSION = '2015-06-30'
BOUNDARY_APPROVAL_REQUIRED = True
VARIANTS = ('ASOF', 'FIRST', 'REVISED', 'FIXEDLAG')
FEATURES = ('F1', 'F2', 'F3', 'F4', 'F5')
MEASURES = ('JOR', 'HIR', 'QUR', 'LDR')
GROUPS = [
    (1, 'Mining and logging', '110099', 'Gold Mines Coal Oil', '10000000', 'exact'),
    (2, 'Construction', '2300', 'Cnstr', '20000000', 'exact'),
    (3, 'Durable manufacturing', '3200', 'Toys BldMt Steel FabPr Mach ElcEq Autos Aero Ships Guns Hardw Chips LabEq MedEq', '31000000', 'exact'),
    (4, 'Nondurable manufacturing', '3400', 'Food Soda Beer Smoke Hshld Clths Drugs Chems Rubbr Txtls Paper', '32000000', 'Hshld approximate'),
    (5, 'Wholesale trade', '4200', 'Whlsl', '41420000', 'exact'),
    (6, 'Retail trade', '4400', 'Rtail', '42000000', 'exact'),
    (7, 'Transportation, warehousing and utilities', '480099', 'Trans Util', '43000000', 'CES excludes utilities'),
    (8, 'Information', '5100', 'Telcm', '50000000', 'exact'),
    (9, 'Finance and insurance', '5200', 'Banks Insur Fin', '55000000', 'CES financial activities'),
    (10, 'Real estate and rental and leasing', '5300', 'RlEst', '55000000', 'shared CES with group 9'),
    (11, 'Professional and business services', '540099', 'BusSv', '60000000', 'exact'),
    (12, 'Health care and social assistance', '6200', 'Hlth', '65000000', 'CES includes private education'),
    (13, 'Accommodation and food services', '7200', 'Meals', '70000000', 'CES includes leisure'),
]
EXCLUDED_FRENCH = {'Agric': 'outside nonfarm JOLTS', **{s: 'ambiguous SIC/NAICS scope' for s in ('Other','Boxes','Books','Softw','Fun','PerSv')}}
PUBLIC_URLS = {
    'industry': 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip',
    'ff5': 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip',
    'momentum': 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip',
}
MODEL = {
    'min_train_months': 36, 'penalties': [10 ** (-2 + i / 2) for i in range(11)],
    'folds': 5, 'purge_months': 1, 'standardization_min_months': 24,
    'winsor_limit': 3.0, 'ddof': 1, 'alpha_tie': 'larger',
    'primary_order': ['A0','A1','A2','A3','A4'], 'candidate_max': 3,
    'candidate_min_t': 1.5, 'candidate_max_correlation': 0.8,
    'return_information_lag_months': 1,
    'candidate_missing_in_regression': 'zero with coverage reported; never impute candidate IC observations',
    'research_comparison': 'common complete prediction months across all reported strategies',
}
PORTFOLIO = {
    'longs': 3, 'shorts': 3, 'holding': 3, 'holdings_sensitivity': [1,6],
    'risk_window': 60, 'risk_min_months': 36, 'vol_target': 0.10,
    'gross_cap': 2.0, 'cost_bps': 10, 'cost_sensitivity_bps': [0,25],
    'hedge_cost_bps': 2, 'borrow_finance_base_bps_year': 0,
    'borrow_finance_sensitivity_bps_year': 25,
    'tranche_start': 'cash in unavailable slots; fixed 1/holding per slot',
    'startup_risk': 'registered volatility target and gross cap apply from the first nonzero book',
    'tranche_rebalance': 'monthly equal-weight templates with fixed membership',
    'tie_break': 'stable group ID',
    'profit_concentration': 'largest positive group excess-PnL contribution divided by positive total book excess PnL; nonpositive total fails',
    'cost_breakeven': 'annual mean gross less hedge costs and financing divided by industry turnover; fixed base-path diagnostic',
}
INFERENCE = {
    'hac_lags': 6, 'bootstrap_draws': 5000, 'mean_block': 6,
    'horizons': [1,3,6], 'placebo_min_shift': 24, 'last_window_months': 18,
    'excluded_pandemic_months': ['2020-03','2020-12'],
    'holm': 'all inferential comparison-endpoint pairs',
    'reality_check': 'Section 12: 36 seed-1 candidate slots; monthly IC against zero',
    'deflated_sharpe_family': '36 seed-1 candidate slots plus research strategies',
    'gate_min_t': 2.0, 'gate_placebo_p': 0.05, 'gate_max_profit_share': 0.50,
    'diagnostic_ids': ['horizons','pandemic','drop_group','cost_0','cost_25','borrow_25',
                       'holding_1','holding_6','variant_gap','placebo','tightness','halves','last_18','course_windows'],
}
AGENT = {
    'run_id': 'opus55_xhigh_followup',
    'model': 'claude-opus-5-5', 'temperature': 0.7, 'seeds': [1,2,3],
    'provider': 'Anthropic', 'effort': 'xhigh',
    'run_semantics': 'independent repetitions; model seed and temperature unsupported',
    'context_exception': 'none; injected calendar dates are excluded from study calls',
    'arms': ['independent','islands'], 'emphases': ['Temporal','Composition','Interactions'],
    'submissions': 6, 'migration_after': [2,4], 'migration_word_limit': 120,
    'hypothesis_word_limit': 40, 'falsification_word_limit': 30,
    'syntax_retries': 1, 'depth': 3, 'max_variables': 2,
    'lag_choices': [1,2,3,6,12], 'window_choices': [3,6,12],
    'persist_choices': [3,6], 'tsz_choices': [36,60,'exp'],
    'tsz_exp_min': 36, 'judge_review_fraction': 0.20,
    'transport': 'claude_subscription',
    'leaf_inputs': ['JOR','HIR','QUR','LDR','H','E'],
    'temporal_semantics': 'monthly decision-time levels; lags preserve the vintage known at each past decision',
    'candidate_transform': 'same expanding-sigma and cross-sectional standardization as public features',
}
OPTIONAL_ADMISSION = {
    'LinkUp_Tier1': {'admitted': False, 'reason': 'No collection-success/failure history; PIT mapping and cohort gates unverified'},
    'LinkUp_Tier2': {'admitted': False, 'reason': 'No dated historical snapshots/version history'},
    'WARN': {'admitted': False, 'reason': 'No amendment history or dated mapping; group coverage unverified'},
    'F6': {'admitted': False, 'reason': 'Completed 13-group search: two exact sector matches, below nine required; Information has partial scope. Bundled first vintages follow research snapshot. Coverage diagnostic only.'},
    'A5': {'admitted': False, 'reason': 'Optional LightGBM not installed; no extra dependency requested'},
}
GATE_CONSTANTS = {'minimum_groups_measure': 11, 'minimum_jolts_measures': 3,
                  'ppi_exact_groups': 9, 'company_groups': 10, 'company_count': 20,
                  'cohort_history_months': 24, 'warn_information_delay_days': 30,
                  'access_timebox_hours': 3, 'raw_size_limit_gb': 50, 'processing_hours': 6}
GRAMMAR = '''lag(x,k); mavg(x,w); chg(x,k); lchg(x,k); yoy(x); accel(x);
persist(x,k); tsz(x,w); csrank(x); ratio(x,y); spread(x,y); mult(x,y);
withT(x); regime(x,s). k=1,2,3,6,12 (persist:3,6); mavg w=3,6,12;
tsz w=36,60,"exp"; regime s="low","high". Depth<=3, <=2 variables plus T.
yoy=x-lag(x,12); chg=x-lag(x,k); lchg=log(x)-log(lag(x,k));
accel=chg(chg(x,3),3); persist=share(chg(x,1)>0) over full window;
tsz=(x-expanding_or_rolling_mean)/sample_sd, exp minimum 36;
csrank=average fractional rank across groups; spread=csz(x)-csz(y);
ratio requires nonzero denominator; logs require strictly positive values;
rolling windows require complete history. No arithmetic or operations beyond these.'''
SYSTEM_PROMPT = '''You are a quantitative researcher. You will propose one feature per turn to predict which of {n} anonymous groups (G01 to G{n}) will have higher returns next month relative to the others. You see only the variable dictionary below, the allowed operations, and summary statistics of your previous submissions. You do not know what the groups, variables or time periods are. Do not guess them and do not use knowledge about any real industry, company or date.
Starting emphasis: {emphasis}.
Rules: return only JSON with keys name, hypothesis, falsified_if, expression; use only the allowed operations; state a hypothesis that the statistics could falsify.
Variable dictionary: {dictionary}
Allowed operations: {grammar}
Submission format: return exactly the four named fields, each a nonempty string. The hypothesis has at most 40 words; falsified_if has at most 30 words. Words are counted by whitespace. Invalid submissions consume a slot; only invalid JSON syntax permits one repair.
The JSON submission rules apply when proposing a feature. When asked for a migration report, return prose following the migration instructions instead. Keep that entire report comfortably below 120 words, including headings, and check its word count before returning it.'''
TURN_PROMPT = 'Submission {i} of 6. Your previous submissions and their development statistics: {history}.\n{migration_reports}\nPropose your next feature.'
MIGRATION_PROMPT = 'In at most 120 words, report to the other researchers what you learned so far, including at least one thing that failed. Do not include formulas. The entire report, including headings, must contain at most 120 whitespace-separated words. Include a concrete unsuccessful attempt or finding. Use prose only, without expressions, specifications or code.'
P1_PROMPT = 'Find mapping errors, timestamp or look-ahead errors, and code bugs in the material below.\nFor each problem, give the exact line or row, why it is wrong, and a test that would confirm it.\nDo not report style issues.'
P4_PROMPT = 'Give 10 distinct reasons these results could be spurious, ranked by likelihood.\nFor each, name a test that can be run with this data and the result that would make us say "do not implement".'
PREREG_NOTES = [
    'V/U stays below 1 (T below 0) throughout the research period. Any feature × T interaction is therefore estimated outside the support observed in research and applied to a test period containing the 2021–23 tight regime. Q1 is judged on the main effect. The interaction model and the V/U above-versus-below-1 split are reported as descriptive, not as tests.',
    'Core vintage coverage begins March 4, 2011. The first sealed decision is deliberately October 31, 2014. Moving the boundary later to capture tight-regime variation costs sealed observations. The Sharpe values 0.58/0.72/0.84 for 142/92/68 months are IID t≈2 approximations, not formal power calculations.',
    'Each agent arm is run with three seeds. Seed 1 is the only strategy-producing run: only its candidates may supply features to A3 and A4. Seeds 2 and 3 measure search behaviour and never enter selection.',
    'The detailed Section 12 definition governs: the reality check uses the 36 candidate slots of seed 1; deflated Sharpe ratios use those slots plus strategies evaluated in research. Process-measurement seeds are excluded. These are within-run research diagnostics for the corrected experiment; the excluded technical run is disclosed separately and supplies no candidates, scores or agent history.',
    'Holm correction applies to A1 vs A0, A2 vs A1 (if admitted) and A3 vs its base. A4 vs A3 is reported with its interval, outside the family, as descriptive.',
    'Given about 142 sealed months and a five-part gate, "Do not implement" is the expected outcome. The report is built so that three things carry the contribution whatever the verdict: the research-versus-sealed performance gap, the number of candidates that pass in research and fail in the sealed test, and the comparison of the two search architectures.',
]
