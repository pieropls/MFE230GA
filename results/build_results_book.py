"""Build the Results Book: scoreboard, claims register, RESULTS_BOOK.md and results_book.tex.

Every number is read from a file. The claims register (claims.csv) states each number the report
may use together with a locator; verify() re-reads the locator and marks the claim verified only
if the stated number matches the file at the stated precision. Run from anywhere:

    python3 results/build_results_book.py
"""
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT / 'analysis'))
import params as P  # noqa: E402

FROZ = 'frozen'          # label shorthand used in the register
CONF, POST, FWD = 'CONF', 'POST-HOC', 'FWD'
CALL_COUNTS = [None, None]   # logged model calls (Sonnet, Opus), filled by register_claims from log.jsonl
SON = P.SONNET / 'outputs'
OPU = P.OPUS / 'outputs'
TAB = P.TABLES


def rel(path):
    return str(Path(path).resolve().relative_to(PROJECT))


# ---------------------------------------------------------------- locators
def _json_get(path, dotted):
    value = json.loads(Path(path).read_text())
    for key in dotted.split('.'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def _csv_get(path, spec):
    """spec: 'col=<name>[;<filter_col>=<value>;...]'. Index column is restored as a filter column."""
    frame = pd.read_csv(path)
    parts = dict(p.split('=', 1) for p in spec.split(';'))
    col = parts.pop('col')
    mask = pd.Series(True, index=frame.index)
    for k, v in parts.items():
        column = frame[k].astype(str)
        mask &= column == v
    rows = frame[mask]
    if len(rows) != 1:
        raise KeyError(f'{spec} matched {len(rows)} rows in {path}')
    return rows.iloc[0][col]


def _md_get(path, spec):
    """spec: 'table=<n>||row=<first cell>||col=<header>' over the n-th markdown table in the file."""
    parts = dict(p.split('=', 1) for p in spec.split('||'))
    text = Path(path).read_text().splitlines()
    tables, current = [], []
    for line in text + ['']:
        if line.startswith('|'):
            current.append([c.strip() for c in line.strip().strip('|').split('|')])
        elif current:
            tables.append(current)
            current = []
    table = tables[int(parts['table'])]
    header = table[0]
    for row in table[2:]:
        if row[0] == parts['row']:
            return row[header.index(parts['col'])]
    raise KeyError(spec)


def read_locator(locator):
    path, spec = locator.split('::', 1)
    full = PROJECT / path
    if path.endswith('.json'):
        return _json_get(full, spec)
    if path.endswith('.csv'):
        return _csv_get(full, spec)
    if path.endswith('.md'):
        return _md_get(full, spec)
    if path.endswith('.sha256'):
        return Path(full).read_text().splitlines()[int(spec.split('=')[1]) - 1].split()[0]
    raise ValueError(locator)


def to_float(value):
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace('−', '-').replace('%', '').replace('$', '').strip()
    match = re.match(r'[+-]?\d+(\.\d+)?', text)
    return float(match.group(0)) if match else float('nan')


def verify(stated, locator, scale=1.0, decimals=None):
    """stated matches the file value (times scale) at the displayed precision."""
    raw = read_locator(locator)
    try:
        value = to_float(raw) * scale
    except Exception:
        return str(raw) == str(stated), raw
    if isinstance(stated, str):
        return str(raw).strip() == stated, raw
    text = repr(stated)
    dec = decimals if decimals is not None else (len(text.split('.')[1]) if '.' in text else 0)
    return abs(value - stated) <= 0.5 * 10 ** (-dec) + 1e-12, value


# ---------------------------------------------------------------- claims
CLAIMS = []


def claim(cid, sentence, stated, locator, label, scale=1.0, decimals=None, note=''):
    """Register a claim; `stated` may be a number or a list of numbers (same locator list)."""
    stateds = stated if isinstance(stated, list) else [stated]
    locators = locator if isinstance(locator, list) else [locator]
    ok, found = True, []
    for s, loc in zip(stateds, locators):
        good, value = verify(s, loc, scale, decimals)
        ok &= bool(good)
        found.append(value)
    CLAIMS.append({'claim_id': cid, 'sentence': sentence, 'numbers': '; '.join(map(str, stateds)),
                   'source': ' | '.join(locators), 'label': label, 'verified': 'y' if ok else 'n',
                   'file_value': '; '.join(f'{v:.6g}' if isinstance(v, float) else str(v) for v in found), 'note': note})
    return ok


def register_claims():
    R = rel(SON / 'sealed/initial/results.json')
    RS = rel(SON / 'research_summary.json')
    RO = rel(OPU / 'sealed/initial/results.json')
    RSO = rel(OPU / 'research_summary.json')
    t = lambda name: rel(TAB / name)
    # --- confirmatory: sealed test of the preregistered strategies
    claim('C01', 'The preregistered primary A3 earned a test Sharpe of -0.58 over 142 months (Nov 2014-Aug 2026).', [-0.58, 142],
          [f'{R}::variants.ASOF.A3.sharpe', f'{R}::variants.ASOF.A3.n'], CONF)
    claim('C02', 'A3 lost 4.6% a year net of costs, with 7.8% volatility and a 41% maximum drawdown.', [-4.6, 7.8, -41],
          [f'{R}::variants.ASOF.A3.mean_net_annual', f'{R}::variants.ASOF.A3.volatility', f'{R}::variants.ASOF.A3.max_drawdown'], CONF, scale=100)
    claim('C03', 'A3 one-month rank IC in the test was -0.021 (Newey-West t = -1.08).', [-0.021, -1.08],
          [f'{R}::variants.ASOF.A3.IC.1.mean', f'{R}::variants.ASOF.A3.IC.1.t'], CONF)
    claim('C04', 'A3 factor alpha was -0.38% a month after FF5, momentum and industry momentum.', -0.38, f'{R}::attribution.A3.coefficients.intercept', CONF, scale=100)
    claim('C04b', 'The t-statistic of the A3 alpha was -1.86.', -1.86, f'{R}::attribution.A3.t_statistics.intercept', CONF)
    claim('C05', 'The circular-shift placebo p-value for A3 was 0.72.', 0.72, f'{R}::placebo.p', CONF)
    claim('C06', 'A3 break-even trading cost was -32 bp: it loses money even with free industry trading.', -32, f'{R}::cost_breakeven_bps', CONF)
    claim('C07', 'A3 passed gate G1 and failed G2, G3, G4 and G5.', ['True', 'False', 'False', 'False', 'False'],
          [f'{R}::gate.criteria.G{i}' for i in range(1, 6)], CONF)
    claim('C08', 'Test Sharpe ratios: A0 -0.36, A1 -0.51, A1-T -0.59, A3 -0.58, A4 -0.79.', [-0.36, -0.51, -0.59, -0.58, -0.79],
          [f'{R}::variants.ASOF.{s}.sharpe' for s in ['A0', 'A1', 'A1-T', 'A3', 'A4']], CONF)
    claim('C09', 'Research-period Sharpe ratios (88 common months): A0 -0.44, A1 -0.54, A1-T -0.55, A3 -0.13, A4 -0.18.', [88, -0.44, -0.54, -0.55, -0.13, -0.18],
          [f'{RS}::strategies.A3.n'] + [f'{RS}::strategies.{s}.sharpe' for s in ['A0', 'A1', 'A1-T', 'A3', 'A4']], CONF)
    claim('C10', 'A3 by window: first half -0.72, second half -0.49, excluding Mar-Dec 2020 -0.51, last 18 months +0.85.', [-0.72, -0.49, -0.51, 0.85],
          [f'{R}::windows.A3.{w}.sharpe' for w in ['first_half', 'second_half', 'ex_pandemic', 'last_18']], CONF)
    claim('C11', 'A3 descriptive course windows: full sample (from Jun 2007) -0.44, post-2010 -0.62.', [-0.44, -0.62],
          [f'{R}::course_windows.A3.full.sharpe', f'{R}::course_windows.A3.post_2010.sharpe'], CONF)
    claim('C12', 'A3 Sharpe at 25 bp industry costs was -0.79 and at zero industry costs -0.45.', [-0.79, -0.45],
          [f'{R}::sensitivities.cost_25.sharpe', f'{R}::sensitivities.cost_0.sharpe'], CONF)
    claim('C13', 'A3 loads on profitability (RMW +0.19, t = 2.2) and against value (HML -0.15, t = -2.0).', [0.19, 2.2, -0.15, -2.0],
          [f'{R}::attribution.A3.coefficients.RMW', f'{R}::attribution.A3.t_statistics.RMW', f'{R}::attribution.A3.coefficients.HML', f'{R}::attribution.A3.t_statistics.HML'], CONF)
    claim('C14', 'A0 loads +0.22 on industry momentum (t = 1.9).', [0.22, 1.9], [f'{R}::attribution.A0.coefficients.group_momentum', f'{R}::attribution.A0.t_statistics.group_momentum'], CONF)
    claim('C15', 'A3 ran at 1.1% a year of trading costs against a gross loss of 3.5% a year.', [1.11, -3.5],
          [f'{t("d4_test_performance.csv")}::col=cost_ann;strategy=A3 primary', f'{R}::variants.ASOF.A3.mean_gross_annual'], CONF, scale=100)
    claim('C16', 'All four Holm-adjusted comparisons in the Sonnet study had adjusted p = 1.0.', [1.0, 1.0, 1.0, 1.0],
          [f'{R}::comparisons.{i}.holm_p' for i in range(4)], CONF)
    claim('C17', 'Of the 142 test months, A3 was in the expanding-tercile "high" tightness bin in 133.', 133, f'{R}::windows.A3.T_high.n', CONF)
    claim('C18', 'The cross-validated ridge penalty was 1000, the top of the grid, for every learned model.', [1000, 1000, 1000, 1000],
          [f'{rel(SON / "selected_features.json")}::models.{m}.alpha' for m in ['A1', 'A1-T', 'A3', 'A4']], CONF)
    claim('C19', 'Of the agent features that passed research selection, 4 of 4 (Sonnet) and 6 of 7 (Opus) failed the frozen sealed criterion (t >= 1.5 and positive IC in both test halves); the one Opus feature that passed it was not selected.', [4, 4, 6, 7],
          [f'{R}::research_pass_sealed_failure_count', f'{t("d7_agent_summary.csv")}::col=Sonnet;item=passed research filter', f'{RO}::research_pass_sealed_failure_count', f'{t("d7_agent_summary.csv")}::col=Opus;item=passed research filter'], CONF)
    claim('C23', 'A1-T test: net return -4.9% a year, volatility 8.2%, maximum drawdown -36.3%.', [-4.9, 8.2, -36.3],
          [f'{R}::variants.ASOF.A1-T.mean_net_annual', f'{R}::variants.ASOF.A1-T.volatility', f'{R}::variants.ASOF.A1-T.max_drawdown'], CONF, scale=100)
    # A06: logged model calls per study, counted directly from log.jsonl (non-evaluation entries) and the responses folder
    counts = []
    for study in [SON, OPU]:
        rows_ = [json.loads(l) for l in (study / 'agents/log.jsonl').read_text().splitlines()]
        n_calls = sum(1 for r_ in rows_ if r_.get('kind') != 'evaluation')
        n_files = len(list((study / 'agents/responses').glob('*.json')))
        counts += [n_calls, n_files]
    CLAIMS.append({'claim_id': 'A06', 'sentence': 'Logged model calls: 199 in the confirmatory (Sonnet) study and 294 in the Opus follow-up (candidate, migration and judge calls; the evaluation entries in the log are not calls).',
                   'numbers': '199; 294', 'source': f'{rel(SON / "agents/log.jsonl")} | {rel(OPU / "agents/log.jsonl")} :: entries with kind != evaluation; equals the file count in agents/responses/',
                   'label': CONF, 'verified': 'y' if counts == [199, 199, 294, 294] else 'n', 'file_value': '; '.join(map(str, counts)),
                   'note': 'an earlier draft of CLAUDE.md stated 607 and 905; corrected to the logged counts on 3 Oct 2026'})
    CALL_COUNTS[:] = [counts[0], counts[2]]
    # A07-A10: facts behind the team's Claude evaluation (docs/team_inputs/al_claude_section.md), counted from the frozen files
    p1 = (SON / 'p1_review.md').read_text()
    p1_items = re.findall(r'^\d+\. \*\*(\w+):\*\*', p1, flags=re.M)
    p1_prompt_chars = len(json.loads((SON / 'p1_request.json').read_text())['prompt'])
    shared = json.loads((SON / 'p1_claim_checks.json').read_text())['shared_CES_equal_nonmissing_rows']
    a07 = [len(p1_items), p1_items.count('claim_not_supported'), p1_items.count('fixed_metadata'), shared['asof'], p1_prompt_chars]
    CLAIMS.append({'claim_id': 'A07', 'sentence': 'P1 audit: 25 numbered findings, 5 not supported by the files, 1 metadata fix, none a look-ahead error; the shared group-9/10 CES series had 584 nonmissing rows; the prompt body ran to 38,717 characters.',
                   'numbers': '25; 5; 1; 584; 38717', 'source': f'{rel(SON / "p1_review.md")} :: numbered items and their bold disposition tags | {rel(SON / "p1_claim_checks.json")}::shared_CES_equal_nonmissing_rows.asof | {rel(SON / "p1_request.json")}::len(prompt)',
                   'label': CONF, 'verified': 'y' if a07 == [25, 5, 1, 584, 38717] else 'n', 'file_value': '; '.join(map(str, a07)), 'note': 'dispositions: documented_design, documented_limitation, checked_no_error, checked_question, nonblocking_error_message, documented_diagnostic are not errors'})
    BA = rel(SON / 'agents/blinding_audit.json')
    claim('A08', 'The blinding audit of all 199 Sonnet calls passed (108 candidate calls, 18 migration calls, 1 syntax repair).', [199, 108, 18, 1, 'True'],
          [f'{BA}::total_calls', f'{BA}::candidate_calls', f'{BA}::migration_calls', f'{BA}::syntax_repairs', f'{BA}::passed'], CONF)
    migs = json.loads((SON / 'agents/migrations.json').read_text())
    invalid = [m for m in migs if not m.get('valid')]
    over = [m for m in invalid if any('words; maximum is 120' in str(r_) for r_ in m.get('reasons', []) or m.get('rejection_reasons', []) or [])]
    a09 = [len(migs), len(invalid), len(over)]
    CLAIMS.append({'claim_id': 'A09', 'sentence': 'Sonnet migration reports: 11 of 18 rejected, 10 of them for exceeding the 120-word cap (121 to 133 words).',
                   'numbers': '18; 11; 10', 'source': f'{rel(SON / "agents/migrations.json")} :: valid == False; reasons containing "maximum is 120"',
                   'label': CONF, 'verified': 'y' if a09 == [18, 11, 10] else 'n', 'file_value': '; '.join(map(str, a09)), 'note': ''})
    p4 = (SON / 'p4_review.md').read_text()
    a10 = [len(re.findall(r'^\d+\. \*\*Covered by', p4, flags=re.M)), len(re.findall(r'^\d+\. \*\*No additional test adopted', p4, flags=re.M))]
    CLAIMS.append({'claim_id': 'A10', 'sentence': 'P4 red team: 6 of 10 concerns were covered by registered diagnostics; for the other 4 no additional test was adopted.',
                   'numbers': '6; 4', 'source': f'{rel(SON / "p4_review.md")} :: items tagged "Covered by" vs "No additional test adopted"',
                   'label': CONF, 'verified': 'y' if a10 == [6, 4] else 'n', 'file_value': '; '.join(map(str, a10)), 'note': ''})
    # V13-V14: provenance and power statements added in the final report pass
    claim('V13', 'On the research years alone the V2d 12-month IC is +0.047 (t 0.90) and its horizon-matched placebo p is 0.26.', [0.047, 0.90, 0.26],
          [f'{t("v3_r2_horizon_profile.csv")}::col=ic;window=research;h=12', f'{t("v3_r2_horizon_profile.csv")}::col=t;window=research;h=12', f'{t("v2d_placebo_12m.csv")}::col=placebo_p_12m;window=research'], POST)
    claim('V14', 'The best post-hoc test Sharpe (V2c, +0.35) corresponds to t of about 1.2 over 142 months (Sharpe times sqrt(142/12)).', 1.2,
          f'{t("v2_window_stats.csv")}::col=sharpe;variant=V2c;window=test', POST, scale=(142 / 12) ** 0.5, decimals=1, note='IID approximation; the Sharpe is read from the file and scaled by sqrt(142/12) = 3.44')
    claim('F09', 'The Q4 2026 book was first built at 2026-10-03T09:17:55Z (independent evidence: commit 9f4a50f, 09:18:29Z, holds a byte-identical book_2026Q4.csv, SHA-256 857275...); book_first_build.sha256 records that first build and later notebook runs must reproduce it.', '2026-10-03T09:17:55+00:00',
          'analysis/forward/book_first_build.sha256::line=2', FWD, note='book_first_build.sha256 was written on 3 Oct from the gate3.md of commit 9f4a50f; verify with: git show 9f4a50f:analysis/forward/book_2026Q4.csv | shasum -a 256')
    # --- exploratory Opus follow-up
    claim('X01', 'Opus follow-up: primary A4 test Sharpe +0.01, research Sharpe -0.40, placebo p 0.56, Sharpe at 25 bp -0.19.', [0.01, -0.40, 0.56, -0.19],
          [f'{RO}::variants.ASOF.A4.sharpe', f'{RSO}::strategies.A4.sharpe', f'{RO}::placebo.p', f'{RO}::sensitivities.cost_25.sharpe'], CONF, note='exploratory; after the test was seen')
    claim('X02', 'Opus A4 one-month IC -0.002 (t = -0.10); alpha t 0.05; last 18 months Sharpe -1.41.', [-0.002, -0.10, 0.05, -1.41],
          [f'{RO}::variants.ASOF.A4.IC.1.mean', f'{RO}::variants.ASOF.A4.IC.1.t', f'{RO}::attribution.A4.t_statistics.intercept', f'{RO}::windows.A4.last_18.sharpe'], CONF)
    claim('X03', 'Opus A3 test Sharpe -0.46.', -0.46, f'{RO}::variants.ASOF.A3.sharpe', CONF)
    claim('X04', 'In the Opus A4 book, durable manufacturing alone contributed +0.27 of cumulative gross return in the test.', 0.273,
          f'{rel(P.OUT / "diagnostics.md")}::table=1||row=Durable mfg||col=A4 (Opus)', POST)
    # --- diagnostics D1-D9 (post-hoc) and D10 (confirmatory counts)
    d1 = t('d1_signal_ic.csv')
    claim('D01', 'Wage growth W: rank IC +0.029 in research (t 1.54), +0.049 in test (t 2.04), +0.039 full sample (t 2.50).', [0.029, 1.54, 0.049, 2.04, 0.039, 2.50],
          [f'{d1}::col={c};signal=W' for c in ['research_ic', 'research_t', 'test_ic', 'test_t', 'full_ic', 'full_t']], POST)
    claim('D02', 'Full-sample one-month ICs: openings -0.005, hires +0.013, quits +0.009, layoffs +0.028, hours -0.010, A0 composite -0.013, industry momentum +0.020.',
          [-0.005, 0.013, 0.009, 0.028, -0.010, -0.013, 0.020], [f'{d1}::col=full_ic;signal={s}' for s in ['F1', 'F2', 'F3', 'F4', 'F5', 'A0', 'IndMom']], POST)
    claim('D03', 'Layoffs (F4) carry a positive IC (+0.033 research, +0.026 test) although A0 gave them a negative sign; hours (F5) carry a negative IC (-0.012, -0.007) although A0 gave them a positive sign.',
          [0.033, 0.026, -0.012, -0.007], [f'{d1}::col=research_ic;signal=F4', f'{d1}::col=test_ic;signal=F4', f'{d1}::col=research_ic;signal=F5', f'{d1}::col=test_ic;signal=F5'], POST)
    d2 = t('d2_horizon_ic.csv')
    claim('D04', 'At a 12-month horizon hires have IC -0.062 (t -2.1) and quits -0.065 (t -1.7); at one month +0.013 and +0.009.', [-0.062, -2.1, -0.065, -1.7, 0.013, 0.009],
          [f'{d2}::col=ic_h12;signal=F2', f'{d2}::col=t_h12;signal=F2', f'{d2}::col=ic_h12;signal=F3', f'{d2}::col=t_h12;signal=F3', f'{d2}::col=ic_h1;signal=F2', f'{d2}::col=ic_h1;signal=F3'], POST)
    claim('D05', 'Wage growth IC by horizon: +0.039 at 1 month (t 2.5), +0.026 at 12 months.', [0.039, 2.5, 0.026],
          [f'{d2}::col=ic_h1;signal=W', f'{d2}::col=t_h1;signal=W', f'{d2}::col=ic_h12;signal=W'], POST)
    d3 = t('d3_regime_balance.csv')
    claim('D06', 'Expanding tightness terciles put 133 of 142 test months in the "high" bin (3 low, 6 middle); V/U exceeded 1 in 0 research months and 75 test months.', [133, 3, 6, 0, 75],
          [f'{d3}::col=expanding high;period=test', f'{d3}::col=expanding low;period=test', f'{d3}::col=expanding middle;period=test', f'{d3}::col=V/U > 1;period=research', f'{d3}::col=V/U > 1;period=test'], POST)
    claim('D07', 'A 12-month-change split is balanced: T rising in 93 research and 88 test months, falling in 32 and 54.', [93, 88, 32, 54],
          [f'{d3}::col=T rising (12m);period=research', f'{d3}::col=T rising (12m);period=test', f'{d3}::col=T falling (12m);period=research', f'{d3}::col=T falling (12m);period=test'], POST)
    claim('D08', 'Industry momentum 12-1 through the same backtest had a test Sharpe of +0.03.', 0.03, f'{t("d4_test_performance.csv")}::col=sharpe;strategy=Industry momentum 12-1', POST)
    d5 = t('d5_industry_pnl.csv')
    claim('D09', 'A3 test P&L by industry: health care -26.2 pp, construction -19.2, finance -16.3, professional services -12.2; wholesale +14.9; trading costs -13.1.', [-26.2, -19.2, -16.3, -12.2, 14.9, -13.1],
          [f'{d5}::col=contribution;component={c}' for c in ['Health care', 'Construction', 'Finance & insurance', 'Prof. & business svcs', 'Wholesale', 'Trading costs']], POST, scale=100)
    d7 = t('d7_agent_summary.csv')
    claim('D10', 'Selected agent features: 2 of 4 regime-gated in each study; test IC undefined for 4 Sonnet and 2 Opus candidates; 0 (Sonnet) and 2 (Opus) selected features had a positive test IC.', [2, 2, 4, 2, 0, 2],
          [f'{d7}::col=Sonnet;item=selected and regime-gated', f'{d7}::col=Opus;item=selected and regime-gated', f'{d7}::col=Sonnet;item=test IC undefined (<=3 active months)',
           f'{d7}::col=Opus;item=test IC undefined (<=3 active months)', f'{d7}::col=Sonnet;item=selected with positive test IC', f'{d7}::col=Opus;item=selected with positive test IC'], POST)
    claim('D11', 'Correlation between research and test IC across valid agent candidates: 0.22 (Sonnet), 0.37 (Opus).', [0.22, 0.37],
          [f'{d7}::col=Sonnet;item=corr(research IC, test IC)', f'{d7}::col=Opus;item=corr(research IC, test IC)'], POST)
    d7s = t('d7_selected_features.csv')
    claim('D12', "Sonnet's two independent-arm features were active in only 3 of 142 test months; the best Opus island feature (research t 3.56) also in 3.", [3, 3, 3.56, 3],
          [f'{d7s}::col=test_n;candidate=independent_1_Temporal_3', f'{d7s}::col=test_n;candidate=independent_1_Interactions_4',
           f'{t("d7_agent_candidates.csv")}::col=research_t;study=Opus;candidate=islands_1_Composition_4', f'{d7s}::col=test_n;candidate=islands_1_Composition_4'], POST)
    d9 = t('d9_risk_overlay.csv')
    claim('D13', 'The gross-exposure cap bound in 87% of A3 test months; ex-ante volatility averaged 7.5% against a 10% target (realised 7.8%).', [87, 7.5, 7.8],
          [f'{d9}::col=cap_binding_share;study=Sonnet;strategy=A3', f'{d9}::col=mean_ex_ante_vol;study=Sonnet;strategy=A3', f'{d9}::col=realised_vol;study=Sonnet;strategy=A3'], POST, scale=100)
    claim('D14', 'Across the preregistered books the cap bound in 80% to 93% of test months.', [80, 93],
          [f'{d9}::col=cap_binding_share;study=Sonnet;strategy=A0', f'{d9}::col=cap_binding_share;study=Opus;strategy=A4'], POST, scale=100)
    d10 = t('d10_agent_design.csv')
    claim('A01', 'Sonnet study: 98 of 108 proposals valid, 7 of 18 migration reports admitted, 8 of 36 judge labels usable, 8 pairs human-audited.',
          ['98 / 108', '7 / 18', '8 / 36', '8'], [f'{d10}::col=value;study=Sonnet;item={i}' for i in ['Valid proposals', 'Migration reports admitted', 'Defined LLM-judge uptake labels', 'Human-audited judge pairs']], CONF)
    claim('A02', 'Opus study: 106 of 108 proposals valid, 15 of 18 reports admitted, 84 of 88 judge labels usable, 17 pairs human-audited, human-judge agreement 10 of 17 (human yes 3, judge yes 10).',
          ['106 / 108', '15 / 18', '84 / 88', '17', '10 / 17 (human yes 3, judge yes 10)'],
          [f'{d10}::col=value;study=Opus;item={i}' for i in ['Valid proposals', 'Migration reports admitted', 'Defined LLM-judge uptake labels', 'Human-audited judge pairs', 'Human-judge agreement']], CONF)
    hr = rel(OPU / 'human_review_submission.json')
    claim('A03', 'All 7 human-judge disagreements were judge-yes / human-no (items 2, 3, 8, 12, 13, 16, 17).', [7, 0],
          [f'{hr}::machine_yes_human_no_items', f'{hr}::machine_no_human_yes_items'], CONF, note='list lengths checked below')
    ms, mo = rel(SON / 'agents/migration_summary.json'), rel(OPU / 'agents/migration_summary.json')
    claim('A04', 'Judge-labelled uptake of migrated ideas: 25% of usable Sonnet labels (2 of 8), 62% of Opus labels (52 of 84).', [0.25, 0.619], [f'{ms}::uptake_rate', f'{mo}::uptake_rate'], CONF)
    ss, sso = rel(SON / 'agents/search_summary.json'), rel(OPU / 'agents/search_summary.json')
    claim('A05', 'Best-so-far research IC, islands vs independent (mean over 3 runs): Sonnet 0.049 vs 0.083, Opus 0.136 vs 0.059; neither gap exceeds the seed-to-seed range.',
          [0.049, 0.083, 0.136, 0.059, 'False', 'False'],
          [f'{ss}::metrics.best_so_far_ic.islands.mean', f'{ss}::metrics.best_so_far_ic.independent.mean', f'{sso}::metrics.best_so_far_ic.islands.mean',
           f'{sso}::metrics.best_so_far_ic.independent.mean', f'{ss}::metrics.best_so_far_ic.absolute_gap_exceeds_seed_range', f'{sso}::metrics.best_so_far_ic.absolute_gap_exceeds_seed_range'], CONF)
    # --- v2 (post-hoc)
    v2 = t('v2_window_stats.csv')
    for v, vals in {'V2a': [0.09, 0.16, 0.15, 0.12, -1.71], 'V2b': [-0.06, -0.15, -0.11, -0.16, -1.34],
                    'V2c': [0.27, 0.35, 0.32, 0.24, -0.78], 'V2d': [0.50, 0.29, 0.35, 0.30, 0.29]}.items():
        claim(f'V_{v}_SR', f'{v} net Sharpe (10 bp): research {vals[0]:+.2f}, test {vals[1]:+.2f}, full {vals[2]:+.2f}, post-2010 {vals[3]:+.2f}, last 18 months {vals[4]:+.2f}.', vals,
              [f'{v2}::col=sharpe;variant={v};window={w}' for w in ['research', 'test', 'full', 'post-2010', 'last 18m']], POST)
    claim('V01', 'V2a test: one-month IC +0.049 (t 2.04), alpha t 0.29, placebo p 0.02, deflated Sharpe 0.02, Sharpe at 25 bp +0.10, turnover 0.39 per month.', [0.049, 2.04, 0.29, 0.02, 0.02, 0.10, 0.39],
          [f'{v2}::col={c};variant=V2a;window=test' for c in ['ic', 'ic_t', 'alpha_t', 'placebo_p', 'dsr', 'sharpe_25bp', 'turnover']], POST)
    claim('V02', 'V2d test: 12-month IC +0.096 (t 2.43), one-month IC -0.020 (t -0.87), alpha t 1.37, pre-declared placebo p 0.85, deflated Sharpe 0.06, Sharpe at 25 bp +0.22.', [0.096, 2.43, -0.020, -0.87, 1.37, 0.85, 0.06, 0.22],
          [f'{v2}::col={c};variant=V2d;window=test' for c in ['ic_hold', 'ic_hold_t', 'ic', 'ic_t', 'alpha_t', 'placebo_p', 'dsr', 'sharpe_25bp']], POST)
    claim('V03', 'V2d full sample: alpha t 1.96, 12-month IC +0.071 (t 2.06), deflated Sharpe 0.18, pre-declared placebo p 0.86.', [1.96, 0.071, 2.06, 0.18, 0.86],
          [f'{v2}::col={c};variant=V2d;window=full' for c in ['alpha_t', 'ic_hold', 'ic_hold_t', 'dsr', 'placebo_p']], POST)
    claim('V04', 'V2d test: net return +2.6% a year, volatility 8.7%, maximum drawdown -14.4%, hit rate 55%, turnover 0.37 per month.', [2.6, 8.7, -14.4, 55, 37],
          [f'{v2}::col={c};variant=V2d;window=test' for c in ['net_ann', 'vol', 'max_dd', 'hit', 'turnover']], POST, scale=100)
    claim('V05', 'V2c test: alpha t 1.36, placebo p 0.26, deflated Sharpe 0.09.', [1.36, 0.26, 0.09], [f'{v2}::col={c};variant=V2c;window=test' for c in ['alpha_t', 'placebo_p', 'dsr']], POST)
    claim('V06', 'V2b test: one-month IC +0.042 (t 1.65) but alpha t -0.84.', [0.042, 1.65, -0.84], [f'{v2}::col={c};variant=V2b;window=test' for c in ['ic', 'ic_t', 'alpha_t']], POST)
    rr = t('v2_reading_rule.csv')
    claim('V07', 'No v2 variant met the pre-declared reading rule.', ['not distinguishable from noise after the looks already taken'] * 4,
          [f'{rr}::col=reading;variant={v}' for v in ['V2a', 'V2b', 'V2c', 'V2d']], POST)
    claim('V08', 'The highest deflated Sharpe among all v2 variants and windows was 0.18 (V2d, full sample).', 0.18, f'{v2}::col=dsr;variant=V2d;window=full', POST)
    pl = t('v2d_placebo_12m.csv')
    claim('V09', 'Horizon-matched (12-month IC) placebo for V2d, added post-hoc: p 0.06 test, 0.04 full sample, 0.00 post-2010, 0.26 research.', [0.06, 0.04, 0.00, 0.26],
          [f'{pl}::col=placebo_p_12m;window={w}' for w in ['test', 'full', 'post-2010', 'research']], POST)
    vb = t('v2b_signs.csv')
    claim('V10', 'V2b signs learned on research data: + for openings, hires, quits, layoffs and wages; - for hours.', [1, 1, 1, 1, 1, -1],
          [f'{vb}::col=sign;signal={s}' for s in ['F1', 'F2', 'F3', 'F4', 'W', 'F5']], POST)
    la = t('v2a_factor_loadings_test.csv')
    claim('V11', 'V2a test loadings: HML -0.43 (t -4.4), momentum +0.22 (t 3.3), SMB +0.28 (t 2.3).', [-0.43, -4.4, 0.22, 3.3, 0.28, 2.3],
          [f'{la}::col=coef;factor=HML', f'{la}::col=t;factor=HML', f'{la}::col=coef;factor=Mom', f'{la}::col=t;factor=Mom', f'{la}::col=coef;factor=SMB', f'{la}::col=t;factor=SMB'], POST)
    # --- forward test
    bk = rel(P.FORWARD / 'book_2026Q4.csv')
    claim('F01', 'V2a Q4 2026 book: long construction, durable manufacturing and information; short mining, health care and accommodation & food.', [1 / 3, 1 / 3, 1 / 3, -1 / 3, -1 / 3, -1 / 3],
          [f'{bk}::col=v2a_weight;group={g}' for g in [2, 3, 8, 1, 12, 13]], FWD, decimals=3)
    claim('F02', 'V2d Q4 2026 book: long finance, real estate and accommodation & food; short mining, durable manufacturing and retail.', [1 / 3, 1 / 3, 1 / 3, -1 / 3, -1 / 3, -1 / 3],
          [f'{bk}::col=v2d_weight;group={g}' for g in [9, 10, 13, 1, 3, 6]], FWD, decimals=3)
    hb = rel(P.FORWARD / 'book_2026Q4_hedge.csv')
    claim('F03', 'SPY hedge per unit tranche: V2a -0.40, V2b -0.06, V2c -0.24, V2d -0.02.', [-0.40, -0.06, -0.24, -0.02],
          [f'{hb}::col=spy_hedge_weight_per_unit;variant={v}' for v in ['V2a', 'V2b', 'V2c', 'V2d']], FWD)
    eb = rel(P.FORWARD / 'book_2026Q4_etf.csv')
    claim('F04', "V2c's long durable manufacturing and short professional services both map to XLI and cancel, so its tradable book has four legs.", 0.0, f'{eb}::col=v2c_weight;etf=XLI', FWD, decimals=6)
    claim('F05', 'The forward spec was frozen at 2026-10-03T09:03:56Z and amendment 001 at 2026-10-03T09:16:11Z, before the book was built (gate3.md records the order).',
          ['True', 'True'], [f'{rel(P.OUT / "gate3.md")}::table=0||row=Forward spec frozen before the book was built||col=pass',
                             f'{rel(P.OUT / "gate3.md")}::table=0||row=Amendment 001 frozen after the v2 results and before the book||col=pass'], FWD)
    # --- data and design facts
    claim('S01', 'Our rebuilt A0 signal matches the frozen fixed-lag scores with pooled correlation 0.998.', 0.998, f'{rel(P.OUT / "data_vintage.md")}::table=0||row=FIXEDLAG||col=pooled_corr', POST)
    claim('S02', 'As-known (ASOF) scores pick the same top three groups as our revised-data signal in only 42% of test months.', 42, f'{rel(P.OUT / "data_vintage.md")}::table=0||row=ASOF||col=same_top3_share', POST, scale=100)
    claim('S03', 'Durable manufacturing is 60% semiconductors (Chips) by market cap in August 2026; nondurable manufacturing is 60% pharmaceuticals.', ['Chips 60%, Mach 9%, Autos 7%', 'Drugs 60%, Hshld 9%, Soda 7%'],
          [f'{rel(P.FORWARD / "etf_proxies.csv")}::col=group_composition_aug2026;group=3', f'{rel(P.FORWARD / "etf_proxies.csv")}::col=group_composition_aug2026;group=4'], POST)
    claim('S04', 'Gate 1: the 13 group returns match all 50 saved ledgers to 1.5e-16 and our estimators match results.json to 3.6e-15.', ['1.51e-16', '3.55e-15'],
          [f'{rel(P.OUT / "validation.md")}::table=0||row=13 group returns vs 50 saved ledgers (both studies, sealed + research)||col=value',
           f'{rel(P.OUT / "validation.md")}::table=0||row=Estimators vs results.json (IC, IC t, Sharpe, factor coefs and t; A0-A4)||col=value'], CONF)
    # fix A03 (list lengths) and A05 (means over seeds) with direct computation, keeping the locator text
    h = json.loads((PROJECT / hr).read_text())
    for c in CLAIMS:
        if c['claim_id'] == 'A03':
            ok = len(h['machine_yes_human_no_items']) == 7 and len(h['machine_no_human_yes_items']) == 0
            c['verified'], c['file_value'] = ('y' if ok else 'n'), f"{len(h['machine_yes_human_no_items'])}; {len(h['machine_no_human_yes_items'])}"
    # --- extras used by the report
    claim('C20', 'A3 under the four data variants: Sharpe -0.58 (as-known), -0.52 (first release), -0.56 (revised), -0.53 (fixed lag); IC -0.021, -0.040, -0.026, -0.021.',
          [-0.58, -0.52, -0.56, -0.53, -0.021, -0.040, -0.026, -0.021],
          [f'{R}::variants.{v}.A3.sharpe' for v in ['ASOF', 'FIRST', 'REVISED', 'FIXEDLAG']] + [f'{R}::variants.{v}.A3.IC.1.mean' for v in ['ASOF', 'FIRST', 'REVISED', 'FIXEDLAG']], CONF)
    claim('C21', 'A3 turned over 0.91 of its industry book a month in the test.', 0.91, f'{R}::variants.ASOF.A3.turnover', CONF)
    claim('C22', 'The frozen power statement: 142 sealed months require roughly 0.6 annualised Sharpe for IID t of about 2.',
          '142 sealed months require roughly 0.6 annualized Sharpe for IID t≈2; a null does not rule out a smaller effect.', f'{R}::gate.power', CONF)
    claim('S05', 'Windows: research 125 months, test 142, full sample 268, post-2010 200, last 18 months 18.', [125, 142, 268, 200, 18],
          [f'{v2}::col=months;variant=V2a;window={w}' for w in ['research', 'test', 'full', 'post-2010', 'last 18m']], POST)
    claim('F06', 'V2b Q4 2026 book: long durable manufacturing, retail and transport & utilities; short real estate, health care and accommodation & food.', [1 / 3, 1 / 3, 1 / 3, -1 / 3, -1 / 3, -1 / 3],
          [f'{bk}::col=v2b_weight;group={g}' for g in [3, 6, 7, 10, 12, 13]], FWD, decimals=3)
    claim('F07', 'V2c Q4 2026 book: long construction, durable manufacturing and finance; short retail, transport & utilities and professional services.', [1 / 3, 1 / 3, 1 / 3, -1 / 3, -1 / 3, -1 / 3],
          [f'{bk}::col=v2c_weight;group={g}' for g in [2, 3, 9, 6, 7, 11]], FWD, decimals=3)
    claim('F08', 'Hashes: v2 spec ca658234..., forward spec 735a8ffa..., amendment 001 c76cde86..., v3 spec 312aef1d... (first 8 hex digits).',
          ['ca6582347904489bdb6fac1496f895fd18c91eba47ca2bc8566e35cdf44a5832', '735a8ffa9c9c23fd710dfae778a535cad649685aa157dcded3ae0e9996dfb21f',
           'c76cde86a85ff703d317cfeb15dc02a42e342d81a299da2aab959adeb372b12b', '312aef1dd9551aa7044d37ccf8562a8e66cddfe741e0e1097c15cff18ed8bfde'],
          ['analysis/v2_spec.sha256::line=1', 'analysis/forward/spec_frozen.sha256::line=1', 'analysis/forward/spec_amendment_001.sha256::line=1', 'analysis/v3_spec.sha256::line=1'], FWD)
    claim('V12', 'V2a turnover 0.39 and V2d turnover 0.37 of the industry book per month in the test; A3 0.91.', [0.39, 0.37],
          [f'{v2}::col=turnover;variant=V2a;window=test', f'{v2}::col=turnover;variant=V2d;window=test'], POST)
    claim('X05', 'Opus study: 7 island-arm candidates passed the research filter against 4 in the Sonnet study.', [7, 4],
          [f'{d7}::col=Opus;item=passed research filter', f'{d7}::col=Sonnet;item=passed research filter'], POST)
    # v3 claims are appended by register_v3_claims() when Stage 2 outputs exist
    if (P.OUT / 'v3_results.md').exists():
        register_v3_claims()


def register_v3_claims():
    """Filled in at Stage 2 (robustness battery). Kept separate so Stage 1 runs without it."""
    v3 = HERE / 'v3_claims.py'
    if v3.exists():
        namespace = {'claim': claim, 't': lambda name: rel(TAB / name), 'rel': rel, 'P': P, 'POST': POST, 'CONF': CONF, 'FWD': FWD}
        exec(v3.read_text(), namespace)


# ---------------------------------------------------------------- scoreboard
def scoreboard():
    r = json.loads((SON / 'sealed/initial/results.json').read_text())
    rs = json.loads((SON / 'research_summary.json').read_text())
    ro = json.loads((OPU / 'sealed/initial/results.json').read_text())
    rso = json.loads((OPU / 'research_summary.json').read_text())
    rows = []

    def frozen_row(name, key, res, rsum, label, verdict, primary):
        v, a = res['variants']['ASOF'][key], res['attribution'][key]
        rows.append({'strategy': name, 'label': label, 'research_sharpe': rsum['strategies'][key]['sharpe'], 'test_sharpe': v['sharpe'],
                     'full_sharpe': res['course_windows'][key]['full']['sharpe'], 'last18_sharpe': res['windows'][key]['last_18']['sharpe'],
                     'ic': v['IC']['1']['mean'], 'ic_t': v['IC']['1']['t'], 'alpha_month': a['coefficients']['intercept'], 'alpha_t': a['t_statistics']['intercept'],
                     'placebo_p': res['placebo']['p'] if primary else float('nan'), 'dsr': rsum['strategies'][key]['deflated_sharpe']['dsr'],
                     'dsr_note': 'research DSR, 41 nominal trials', 'verdict': verdict})

    names = {'A0': 'A0 fixed rule', 'A1': 'A1 ridge', 'A1-T': 'A1-T tightness', 'A3': 'A3 primary', 'A4': 'A4 islands'}
    for k, n in names.items():
        frozen_row(n + ' (Sonnet)', k, r, rs, 'CONFIRMATORY', 'Do not implement' if k == 'A3' else 'not primary; negative', k == 'A3')
    frozen_row('A3 (Opus follow-up)', 'A3', ro, rso, 'EXPLORATORY', 'exploratory; negative', False)
    frozen_row('A4 primary (Opus follow-up)', 'A4', ro, rso, 'EXPLORATORY', 'exploratory; fails G2-G5', True)
    v2 = pd.read_csv(TAB / 'v2_window_stats.csv').set_index(['variant', 'window'])
    rr = pd.read_csv(TAB / 'v2_reading_rule.csv').set_index('variant')
    desc = {'V2a': 'V2a wage growth (headline)', 'V2b': 'V2b signed composite', 'V2c': 'V2c wage + momentum', 'V2d': 'V2d -(hires+quits), 12m'}
    for v in ['V2a', 'V2b', 'V2c', 'V2d']:
        te = v2.loc[(v, 'test')]
        rows.append({'strategy': desc[v], 'label': 'POST-HOC', 'research_sharpe': v2.loc[(v, 'research'), 'sharpe'], 'test_sharpe': te['sharpe'],
                     'full_sharpe': v2.loc[(v, 'full'), 'sharpe'], 'last18_sharpe': v2.loc[(v, 'last 18m'), 'sharpe'],
                     'ic': te['ic_hold'] if v == 'V2d' else te['ic'], 'ic_t': te['ic_hold_t'] if v == 'V2d' else te['ic_t'],
                     'alpha_month': te['alpha_month'], 'alpha_t': te['alpha_t'], 'placebo_p': te['placebo_p'], 'dsr': te['dsr'],
                     'dsr_note': 'test DSR, 112 trials' + ('; IC is 12-month' if v == 'V2d' else ''), 'verdict': rr.loc[v, 'reading']})
    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / 'scoreboard.csv', index=False)
    return frame


def tex_escape(s):
    out = str(s).replace('&', r'\&').replace('%', r'\%').replace('_', r'\_\allowbreak{}').replace('#', r'\#')
    out = out.replace('≈', r'$\approx$').replace('≤', r'$\leq$').replace('≥', r'$\geq$').replace('→', r'$\to$').replace('−', r'$-$')
    out = re.sub(r'([0-9a-f]{16})(?=[0-9a-f]{8,})', r'\1\\allowbreak{}', out)   # long hashes may break
    return out.replace('/', r'/\allowbreak{}')


def num(x, f='{:+.2f}'):
    return '' if pd.isna(x) else f.format(x).replace('-', '$-$')


def scoreboard_tex(frame):
    short = {'Do not implement': 'Do not implement', 'not primary; negative': 'negative, not primary', 'exploratory; negative': 'exploratory, negative',
             'exploratory; fails G2-G5': 'exploratory, fails G2--G5'}
    lines = [r'\setlength{\tabcolsep}{3pt}\begin{tabular}{@{}p{2.9cm} l r r r r r r r r p{2.3cm}@{}}', r'\toprule',
             r'Strategy & Label & Res. & Test & Full & 18m & IC ($t$) & $\alpha$/m ($t$) & Plac. & DSR & Verdict \\', r'\midrule']
    for _, x in frame.iterrows():
        verdict = short.get(x.verdict, 'noise after the looks taken' if 'noise' in x.verdict else x.verdict)
        lines.append(' & '.join([tex_escape(x.strategy), {'CONFIRMATORY': 'conf.', 'POST-HOC': 'post-hoc'}.get(x.label, 'expl.'),
                                 num(x.research_sharpe), num(x.test_sharpe), num(x.full_sharpe), num(x.last18_sharpe),
                                 f"{num(x.ic, '{:+.3f}')} ({num(x.ic_t)})", f"{num(100 * x.alpha_month)}\\% ({num(x.alpha_t)})",
                                 num(x.placebo_p, '{:.2f}'), num(x.dsr, '{:.2f}'), tex_escape(verdict)]) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}']
    (HERE / 'tables').mkdir(exist_ok=True)
    (HERE / 'tables' / 'scoreboard.tex').write_text('\n'.join(lines) + '\n')


# ---------------------------------------------------------------- content
FIGURES = [
    ('fig_timeline.pdf', 'POST-HOC', 'Tightness never exceeded V/U = 1 in the research period, so the tightness moderator could not be learned there.', 'analysis/data/fred (JTSJOL, UNEMPLOY)'),
    ('fig_ic_signals.pdf', 'POST-HOC', 'Only wage growth has an IC above 1.5 standard errors in both periods; layoffs and hours carry the opposite sign to the one A0 imposed.', 'analysis/output/tables/d1_signal_ic.csv'),
    ('fig_horizon.pdf', 'POST-HOC', 'Hires and quits turn negative at 12 months (t -2.1, -1.7): the investment/cost channel shows up slowly, not at one month.', 'analysis/output/tables/d2_horizon_ic.csv'),
    ('fig_tightness.pdf', 'POST-HOC', 'Split by whether T rose or fell over 12 months, hires and quits predict returns only while the market tightens; the split is balanced in both periods.', 'analysis/output/tables/d3_tightness_ic.csv'),
    ('fig_cumulative.pdf', 'CONFIRMATORY (A0-A4) / POST-HOC (momentum, V2a)', 'Every preregistered strategy lost money in the test; the post-hoc wage-growth book gained until 2024 and gave much of it back.', 'sealed/initial/ASOF_*_ledger.csv; analysis/output/tables/v2_monthly_net.csv'),
    ('fig_industry_pnl.pdf', 'POST-HOC', 'A3 lost most in health care, construction and finance; trading costs were a secondary drag.', 'analysis/output/tables/d5_industry_pnl.csv'),
    ('fig_loadings.pdf', 'CONFIRMATORY (A0, A1, A3) / POST-HOC (V2a)', 'The labor books are quality/growth tilts: A3 loads on RMW and against HML; V2a loads against HML and on momentum.', 'results.json attribution; analysis/output/tables/v2a_factor_loadings_test.csv'),
    ('fig_agents_scatter.pdf', 'POST-HOC', 'Research IC of agent features barely predicts their test IC; the selected regime-gated features were active in 3 test months.', 'analysis/output/tables/d7_agent_candidates.csv'),
    ('fig_agents.pdf', 'CONFIRMATORY', 'Two arms with equal budgets, a blinded evaluator, mechanical selection and a human-audited LLM judge.', 'frozen params.py AGENT'),
    ('fig_v2_windows.pdf', 'POST-HOC / CONFIRMATORY (A3 bars)', 'V2d is the only variant positive in every window; V2a and V2c lost heavily in the last 18 months.', 'analysis/output/tables/v2_window_stats.csv'),
]

TABLES = [
    ('d1_signal_ic', 'D1 single-signal rank IC', 'POST-HOC'), ('d2_horizon_ic', 'D2 IC by horizon', 'POST-HOC'),
    ('d3_regime_balance', 'D3a tightness regime balance', 'POST-HOC'), ('d3_tightness_ic', 'D3b IC when T rises vs falls', 'POST-HOC'),
    ('d4_test_performance', 'D4 test-period performance', 'CONFIRMATORY (A0-A4) / POST-HOC (momentum)'), ('d5_industry_pnl', 'D5 A3 P&L by industry', 'POST-HOC'),
    ('d6_factor_loadings', 'D6 factor loadings', 'CONFIRMATORY'), ('d7_agent_summary', 'D7a agent candidates', 'POST-HOC'),
    ('d7_selected_features', 'D7b selected agent features', 'POST-HOC'), ('d8_a3_windows', 'D8 A3 by window', 'CONFIRMATORY'),
    ('d9_risk_overlay', 'D9 risk overlay', 'POST-HOC'), ('d10_agent_design', 'D10 agent experiment design', 'CONFIRMATORY'),
    ('v2_results', 'v2 variants: Sharpe by window and test statistics', 'POST-HOC'),
]

AI_ROWS = [
    ('P1', 'Source and code audit before research', 'claude-sonnet-5-5 (medium); Opus study: claude-opus-5-5 (xhigh)',
     'outputs/follow_the_workers/outputs/p1_request.json', 'p1_response.md, p1_review.md',
     '25 numbered findings; found the shared CES series for groups 9/10 and several metadata inconsistencies.',
     'Several alleged timing errors were not supported (release filtering precedes the month bound); no numeric change resulted.',
     'Mapping metadata corrected (prescribed vs verified scope); construction SA exception flagged; no basket or feature change.'),
    ('P2', 'Blinded signal-search agents (two arms, 3 repetitions)', 'claude-sonnet-5-5 (medium); Opus study: claude-opus-5-5 (xhigh)',
     'params.py SYSTEM_PROMPT / TURN_PROMPT; outputs/agents/log.jsonl', 'candidates.csv, agents/candidate_records.json',
     'Rediscovered wage growth (V05) blind in both studies; produced valid grammar expressions (98/108 Sonnet, 106/108 Opus).',
     'Highest research t-statistics came from regime gates that were active in 3 test months; every selected feature failed the test.',
     'Mechanical selection only; no engineer edits. v2 restores wage growth as a public, ungated signal.'),
    ('P3', 'Migration reports and LLM judge of idea uptake', 'claude-sonnet-5-5 (medium); Opus study: claude-opus-5-5 (xhigh)',
     'outputs/agents/migrations.json; judge prompt in agents.py trace_migrations', 'agents/migration_judgments.json, human_review_submission.md',
     'Opus: 15/18 reports admitted and 84/88 usable labels; a human audit of 17 pairs was possible.',
     'Sonnet: 28/36 judge outputs were not bare JSON; judge over-attributes uptake (10 yes vs human 3; all 7 disagreements judge-yes).',
     'Judge output treated as an association, not evidence; human labels reported alongside.'),
    ('P4', 'Robustness red team on research tables', 'claude-sonnet-5-5 (medium); Opus study: claude-opus-5-5 (xhigh)',
     'outputs/follow_the_workers/outputs/p4_request.json', 'p4_response.md, p4_review.md',
     'Ten ranked concerns; called "do not implement" from research tables before the seal opened.',
     'Asserted uncomputed p-values and proposed unregistered thresholds; every suggestion was already covered by a registered diagnostic.',
     'No new test adopted (all dispositions "covered by" or "not adopted"); registered diagnostics retained.'),
    ('P5', 'Post-mortem review of the frozen study', 'claude-opus-5-5 (Claude Code, 3 Oct 2026)',
     'conversation request (Piero, 3 Oct 2026); docs/FINDINGS_AND_PROPOSAL.md', 'docs/FINDINGS_AND_PROPOSAL.md, analysis/output/diagnostics.md',
     'Found the wrong A0 signs, the dropped wage signal, the 12-month hiring sign, the 3-of-142-month agent features, the one-bin tightness split.',
     'Guessed the engineering assistant was OpenAI Codex (unverified); used a momentum definition that included month m-1; quoted W ICs with a non-frozen start date.',
     'Momentum redefined on m-12..m-2; W ICs recomputed with the frozen feature start; Codex guess withdrawn (to be confirmed by Alex).'),
    ('P6', 'This iteration: rebuild, diagnostics, frozen v2/v3 specs, forward test, report', 'claude-opus-5-5 (Parts 1-3); claude-fable-5-1 (overnight)',
     'docs/process/ITERATION_PROMPT.md, docs/process/OVERNIGHT_PROMPT.md, CLAUDE.md', 'analysis/run.ipynb, analysis/output/*.md, results/, report/main.tex',
     'Reproduced the sealed A0 returns to 1e-16; froze specs before running; reported all variants; stopped at a failed gate instead of working around it.',
     'The forward spec assumed August JOLTS would not be out by 29 Sep; it was released that day, so the pre-committed check stopped the run.',
     'Amendment 001 (fixed-lag rule, V2c/V2d added, disclosed); run log guarantees v2 outputs never changed.'),
]

KNOWN_ISSUES = [
    ("V2c's ETF legs cancel", 'Its long durable manufacturing and short professional services both map to XLI, so the tradable V2c book has four legs (book_2026Q4_etf.csv).',
     'Disclose in the forward-test section; track V2c on French group returns as the primary record.'),
    ('Revised vs as-known data', 'Every historical v2/v3 number uses revised FRED values with fixed lags (option c in data_vintage.md). The frozen study found the same A3 IC under both rules, but as-known data picks the same top-3 groups in only 42% of months.',
     'Label every v2/v3 number "revised data"; R10 (as-known rerun) is not run without a FRED key.'),
    ('Overlap in the 12-month placebo', 'The horizon-matched placebo for V2d uses overlapping 12-month returns; the circular shift preserves but does not correct the overlap, so its p-values are optimistic.',
     'Keep the pre-declared 1-month placebo (p = 0.85) in the reading rule; report the 12-month one as a post-hoc check only.'),
    ('Mapping dilution', 'Labor data cover all establishments in an industry; returns cover listed firms. Durable manufacturing is 60% semiconductors and nondurable manufacturing 60% pharmaceuticals by market cap.',
     'State as a limit; name NAICS-based CRSP baskets as the follow-up.'),
    ('Power', '142 test months detect an annualised Sharpe of about 0.6 at t = 2. None of the post-hoc Sharpe ratios (0.1-0.35) is distinguishable from zero after deflation.',
     'Say so in the limits; the forward test is a record, not a verdict.'),
]


def md_table(rows, header):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(str(c).replace('|', '/') for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def write_markdown(board, verdict_text, v3_text):
    L = ['# Follow the Workers: Results Book', '', 'Generated by `results/build_results_book.py`. Every number traces to the file named next to it; '
         'the claims register (`claims.csv`) is the only source the report may quote.', '']
    L += ['## 1. Verdict', '', verdict_text or '*VERDICT.md is written at Stage 3.*', '']
    L += ['## 2. Scoreboard', '', 'Source: `results/scoreboard.csv` (built from results.json, research_summary.json of both studies and analysis/output/tables/v2_*.csv). '
          'IC is one-month except V2d (12-month, its holding horizon). DSR: research-period value with 41 nominal trials for the frozen studies; test-window value with 112 trials for v2.', '']
    rows = [[x.strategy, x.label, f'{x.research_sharpe:+.2f}', f'{x.test_sharpe:+.2f}', f'{x.full_sharpe:+.2f}', f'{x.last18_sharpe:+.2f}', f'{x.ic:+.3f} ({x.ic_t:+.2f})',
             f'{100 * x.alpha_month:+.2f}% ({x.alpha_t:+.2f})', '' if pd.isna(x.placebo_p) else f'{x.placebo_p:.2f}', f'{x.dsr:.2f}', x.verdict] for _, x in board.iterrows()]
    L += [md_table(rows, ['Strategy', 'Label', 'Research', 'Test', 'Full', 'Last 18m', 'IC (t)', 'alpha/m (t)', 'Placebo p', 'DSR', 'Verdict']), '']
    L += ['## 3. Figures', '']
    for f, lab, take, src in FIGURES:
        L += [f'- **`report/figures/{f}`** [{lab}]: {take} Source: {src}.']
    L += ['', '## 4. Statistics', '', 'Each table is in `analysis/output/tables/<name>.csv` with a LaTeX fragment in `report/tables/<name>.tex`; the numbers are listed in `analysis/output/diagnostics_v2.md` and `analysis/output/v2_results.md`.', '']
    L += [f'- `{n}`: {title} [{lab}]' for n, title, lab in TABLES]
    if v3_text:
        L += ['', v3_text]
    L += ['', '## 5. The agent experiment', '', '']
    d10 = pd.read_csv(TAB / 'd10_agent_design.csv')
    L += [md_table(d10[['study', 'item', 'value', 'source']].values.tolist(), ['Study', 'Item', 'Value', 'Source']), '']
    d7 = pd.read_csv(TAB / 'd7_selected_features.csv')
    L += ['Selected features and their research -> test fate (`d7_selected_features.csv`):', '',
          md_table([[r.study, r.arm, r.decoded, f'{r.research_ic:+.3f} ({int(r.research_n)})', ('n/a' if pd.isna(r.test_ic) else f'{r.test_ic:+.3f}') + f' ({int(r.test_n)})', 'yes' if r.gated else 'no'] for r in d7.itertuples()],
                   ['Study', 'Arm', 'Feature (decoded)', 'Research IC (n)', 'Test IC (n)', 'Regime-gated']), '',
          'Human vs judge (Opus): 10/17 agreement; human yes 3, judge yes 10; all 7 disagreements judge-yes/human-no (`human_review_submission.json`). '
          f'Models from the logs: Sonnet 5.5 at medium effort for the confirmatory study ({CALL_COUNTS[0]} logged calls), Opus 5.5 at xhigh for the follow-up ({CALL_COUNTS[1]} calls); claim A06.', '']
    L += ['## 6. AI-interaction inventory', '', md_table([list(r) + [''] for r in AI_ROWS], ['ID', 'Purpose', 'Model', 'Prompt file', 'Output file', 'What was right', 'What was wrong', 'What changed', 'Team critique']), '']
    L += ['## 7. Claims register', '', f'`results/claims.csv`: {len(CLAIMS)} claims, {sum(c["verified"] == "y" for c in CLAIMS)} verified against their source files.', '',
          md_table([[c['claim_id'], c['label'], c['sentence'], c['numbers'], c['verified']] for c in CLAIMS], ['ID', 'Label', 'Claim', 'Numbers', 'Verified']), '']
    L += ['## 8. Known issues', '', md_table([list(k) for k in KNOWN_ISSUES], ['Issue', 'What it is', 'Fix or disclosure']), '']
    (HERE / 'RESULTS_BOOK.md').write_text('\n'.join(L))


def write_tex(board, v3_tex):
    def tfig(f, lab, take, src):
        return (f'\\begin{{figure}}[H]\\centering\\includegraphics[width=\\linewidth]{{../report/figures/{f}}}'
                f'\\caption{{{tex_escape(take)} \\textcolor{{mute}}{{\\footnotesize Source: {tex_escape(src)}.}} \\hfill {lab}}}\\end{{figure}}')

    pill = lambda lab: lab.replace('CONFIRMATORY', r'\tagc').replace('POST-HOC', r'\tagp').replace('FWD', r'\tagf').replace('FORWARD TEST', r'\tagf')
    L = [r'\input{../report/preamble}', r'\renewcommand{\ReportTitle}{Follow the Workers: Results Book}',
         r'\renewcommand{\ReportSubtitle}{Every result, figure, table and claim behind the report, with its source file}',
         r'\usepackage{longtable}', r'\begin{document}', r'\MakeCover', r'\tableofcontents', r'\clearpage']
    L += [r'\section{Verdict}', r'\IfFileExists{verdict.tex}{\input{verdict}}{\emph{VERDICT.md is written at Stage 3.}}']
    L += [r'\section{Scoreboard}', 'The A3 sealed ledger starts from an empty book in November 2014; the v2 test figures are the test slice of a continuous run that starts in May 2004 (pre-declared in v2\\_spec.md section 4). IC is one-month except V2d (12-month, its holding horizon). DSR is the research-period value with 41 nominal trials for the frozen studies and the test-window value with 112 trials for v2. Labels: conf.\\ = confirmatory, expl.\\ = exploratory follow-up. Source: \\path{results/scoreboard.csv}.',
          r'{\scriptsize\input{tables/scoreboard}}']
    L += [r'\section{Figures}']
    L += [tfig(f, pill(lab), take, src) for f, lab, take, src in FIGURES]
    L += [r'\clearpage\section{Statistics}', 'Each table lives in \\path{analysis/output/tables/<name>.csv}; the LaTeX fragment in \\path{report/tables/<name>.tex}.']
    for n, title, lab in TABLES:
        L += [f'\\subsection*{{{tex_escape(title)} \\hfill {pill(lab)}}}', f'{{\\footnotesize\\setlength{{\\tabcolsep}}{{4pt}}\\input{{../report/tables/{n}}}}}\\par', r'\medskip']
    if v3_tex:
        L += [v3_tex]
    L += [r'\clearpage\section{The agent experiment}', r'\noindent{\footnotesize\setlength{\tabcolsep}{4pt}\input{../report/tables/d10_agent_design}}\par', r'\medskip',
          r'Selected features and their research$\to$test fate:\par\noindent{\footnotesize\setlength{\tabcolsep}{4pt}\input{../report/tables/d7_selected_features}}\par', r'\medskip',
          'Human vs judge (Opus): 10/17 agreement; human yes 3, judge yes 10; all 7 disagreements judge-yes/human-no. Models from the logs: Sonnet 5.5 at medium effort for the confirmatory study (' + str(CALL_COUNTS[0]) + ' logged calls), Opus 5.5 at xhigh for the follow-up (' + str(CALL_COUNTS[1]) + ' calls); claim A06.']
    L += [r'\clearpage\section{AI-interaction inventory}', r'{\scriptsize\setlength{\tabcolsep}{3pt}\begin{longtable}{@{}p{0.5cm}p{2.0cm}p{1.8cm}p{2.1cm}p{2.2cm}p{2.2cm}p{2.2cm}p{1.4cm}@{}}',
          r'\toprule ID & Purpose & Model & Prompt file & What was right & What was wrong & What changed & Team critique \\ \midrule \endhead']
    for r in AI_ROWS:
        L.append(' & '.join(tex_escape(x) for x in [r[0], r[1], r[2], r[3], r[5], r[6], r[7], '']) + r' \\ \addlinespace')
    L += [r'\bottomrule\end{longtable}}', 'Output files: ' + '; '.join(tex_escape(f'{r[0]}: {r[4]}') for r in AI_ROWS) + '.']
    L += [r'\clearpage\section{Claims register}', f'{len(CLAIMS)} claims, {sum(c["verified"] == "y" for c in CLAIMS)} verified. Source: \\texttt{{results/claims.csv}}.',
          r'{\scriptsize\setlength{\tabcolsep}{3pt}\begin{longtable}{@{}p{1.0cm}p{1.3cm}p{8.2cm}p{3.5cm}p{0.7cm}@{}}', r'\toprule ID & Label & Claim & Numbers & Ver. \\ \midrule \endhead']
    for c in CLAIMS:
        L.append(' & '.join([tex_escape(c['claim_id']), pill(c['label']), tex_escape(c['sentence']), tex_escape(c['numbers']), c['verified']]) + r' \\')
    L += [r'\bottomrule\end{longtable}}']
    L += [r'\section{Known issues}', r'\begin{itemize}']
    L += [f'\\item \\emph{{{tex_escape(k[0])}.}} {tex_escape(k[1])} \\textcolor{{mute}}{{Fix or disclosure: {tex_escape(k[2])}}}' for k in KNOWN_ISSUES]
    L += [r'\end{itemize}', r'\end{document}']
    (HERE / 'results_book.tex').write_text('\n'.join(L) + '\n')


def main():
    register_claims()
    board = scoreboard()
    scoreboard_tex(board)
    with open(HERE / 'claims.csv', 'w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['claim_id', 'sentence', 'numbers', 'source', 'label', 'verified', 'file_value', 'note'])
        writer.writeheader()
        writer.writerows(CLAIMS)
    verdict_md = (HERE / 'VERDICT.md').read_text() if (HERE / 'VERDICT.md').exists() else ''
    v3_md = (HERE / 'v3_section.md').read_text() if (HERE / 'v3_section.md').exists() else ''
    v3_tex = (HERE / 'v3_section.tex').read_text() if (HERE / 'v3_section.tex').exists() else ''
    write_markdown(board, verdict_md, v3_md)
    write_tex(board, v3_tex)
    bad = [c['claim_id'] for c in CLAIMS if c['verified'] != 'y']
    print(f'{len(CLAIMS)} claims; unverified: {bad}')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
