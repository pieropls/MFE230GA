"""Exploratory diagnostics behind FINDINGS_AND_PROPOSAL.md (3 Oct 2026).

Everything here is POST-HOC. It reads the frozen outputs of both completed
studies (read-only) plus public data downloaded on 3 Oct 2026:
  - Ken French 49 industries, FF5, momentum (data/french/, CRSP 202608 build)
  - FRED current (revised) JOLTS/CES/V/U series (data/fred/)
It never writes into the team repo and changes nothing in either study.
Labor signals here use REVISED data with fixed publication lags
(JOLTS d-2, CES d-1), i.e. the study's FIXEDLAG approximation, not ALFRED.

Run:  python3 diagnostics.py   -> writes output/diagnostics.md
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from french import load, NAMES
from signals import features, rank_ic, nw_t

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / '230ga-follow-the-workers' / 'outputs'
STUDIES = {'Sonnet (original)': REPO / 'follow_the_workers',
           'Opus (follow-up)': REPO / 'follow_the_workers_opus55_xhigh'}
OUT = HERE / 'output'
OUT.mkdir(exist_ok=True)
lines = []


def emit(text=''):
    lines.append(text)
    print(text)


def table(frame, floatfmt='{:.3f}'):
    frame = frame.copy()
    for c in frame.columns:
        if pd.api.types.is_float_dtype(frame[c]):
            frame[c] = frame[c].map(lambda v: '' if pd.isna(v) else floatfmt.format(v))
    head = '| ' + ' | '.join([frame.index.name or ''] + list(map(str, frame.columns))) + ' |'
    sep = '|' + '---|' * (len(frame.columns) + 1)
    body = ['| ' + ' | '.join([str(i)] + [str(v) for v in row]) + ' |' for i, row in frame.iterrows()]
    emit('\n'.join([head, sep, *body]))
    emit()


R = load()
emit('# Exploratory diagnostics (post-hoc, not part of either preregistered study)\n')

# 1. Reconstruction check: public French data reproduces the saved ledgers exactly.
emit('## 1. Group-return reconstruction vs saved sealed ledgers\n')
rows = []
for study, root in STUDIES.items():
    for strat in ['A0', 'A1', 'A3', 'A4']:
        p = root / 'outputs/sealed/initial'
        w = pd.read_csv(p / f'ASOF_{strat}_weights.csv', index_col=0)
        w.index = pd.PeriodIndex(w.index, freq='M')
        led = pd.read_csv(p / f'ASOF_{strat}_ledger.csv', index_col=0)
        led.index = pd.PeriodIndex(led.index, freq='M')
        g = [str(i) for i in range(1, 14)]
        ex = R['excess'].loc[w.index]
        ex.columns = [str(c) for c in ex.columns]
        recon = (w[g] * ex[g]).sum(axis=1) + w['market'] * R['factors'].loc[w.index, 'Mkt-RF']
        rows.append({'study': study, 'strategy': strat, 'max_abs_error': float((recon - led.gross).abs().max()),
                     'gross_cap_binds_%': 100 * float((led.gross_leverage > 1.999).mean()),
                     'mean_ex_ante_vol': float(led.ex_ante_vol.mean()),
                     'realized_vol': float(led.net.std() * 12 ** .5),
                     'cost_%_per_yr': 1200 * float(led.cost.mean())})
table(pd.DataFrame(rows).set_index('study'), '{:.3g}')

# 2. Sealed P&L by industry for each primary / key strategy.
emit('## 2. Sealed-period gross P&L by industry (sum of monthly contributions)\n')
pnl = {}
for study, strat in [('Sonnet (original)', 'A0'), ('Sonnet (original)', 'A1'), ('Sonnet (original)', 'A3'), ('Opus (follow-up)', 'A4')]:
    p = STUDIES[study] / 'outputs/sealed/initial'
    w = pd.read_csv(p / f'ASOF_{strat}_weights.csv', index_col=0)
    w.index = pd.PeriodIndex(w.index, freq='M')
    g = [str(i) for i in range(1, 14)]
    ex = R['excess'].loc[w.index]
    ex.columns = g
    key = f'{strat} ({study.split()[0]})'
    pnl[key] = (w[g] * ex[g]).sum()
    pnl[key + ' % months long'] = (100 * (w[g] > 1e-9).mean()).round().astype(int)
frame = pd.DataFrame(pnl)
frame.index = [NAMES[int(i)] for i in frame.index]
frame.index.name = 'industry'
table(frame, '{:+.3f}')

# 3. Single-signal rank ICs (revised data, fixed lags).
emit('## 3. Single-signal rank IC vs next-month relative return (revised data, fixed lags)\n')
emit('W = 12-month log growth of 3-month-average hourly earnings (the wage half of the dropped F6).')
emit('A0 = (F1 + F2 - F4 + F5)/4 as preregistered. IndMom = 12-month industry momentum.\n')
F, T, raw = features()
rel = R['relative']
mom_skip = (1 + R['total']).rolling(11, min_periods=11).apply(np.prod, raw=True).shift(2) - 1
mom_skip = mom_skip.sub(mom_skip.mean(axis=1), axis=0)
mom_noskip = (1 + R['total']).rolling(12, min_periods=12).apply(np.prod, raw=True).shift(1) - 1
F['A0'] = (F['F1'] + F['F2'] - F['F4'] + F['F5']) / 4
F['IndMom 12-2'] = mom_skip
F['IndMom 12-1'] = mom_noskip
windows = {'research 2004-05..2014-09': ('2004-05', '2014-09'), 'test 2014-11..2026-08': ('2014-11', '2026-08'),
           'full 2004-05..2026-08': ('2004-05', '2026-08')}
rows = {}
for name, value in F.items():
    ic = rank_ic(value, rel)
    row = {}
    for label, (a, b) in windows.items():
        x = ic.loc[a:b]
        t, n = nw_t(x)
        row[label] = f'{x.mean():+.3f} (t {t:+.2f})'
    rows[name] = row
frame = pd.DataFrame(rows).T
frame.index.name = 'signal'
table(frame)

emit('## 4. IC by horizon, full sample 2004-05..2026-08 (HAC lags = h+5)\n')
rows = {}
for name in ['F1', 'F2', 'F3', 'F4', 'F5', 'W', 'A0', 'IndMom 12-2']:
    row = {}
    for h in [1, 3, 6, 12]:
        comp = (1 + R['total']).rolling(h).apply(np.prod, raw=True).shift(1 - h) - 1
        target = comp.sub(comp.mean(axis=1), axis=0)
        ic = rank_ic(F[name], target).loc['2004-05':'2026-08']
        t, _ = nw_t(ic, lags=h + 5)
        row[f'h={h}'] = f'{ic.mean():+.3f} (t {t:+.1f})'
    rows[name] = row
frame = pd.DataFrame(rows).T
frame.index.name = 'signal'
table(frame)

# 5. Tightness regimes: expanding terciles vs change-based split.
emit('## 5. Tightness regime balance\n')
lo, hi = T.expanding(24).quantile(1 / 3), T.expanding(24).quantile(2 / 3)
reg = pd.Series('middle', index=T.index)
reg[T <= lo] = 'low'
reg[T >= hi] = 'high'
dT = T - T.shift(12)
rows = {}
for label, (a, b) in [('research', ('2004-05', '2014-09')), ('test', ('2014-11', '2026-08'))]:
    r = reg.loc[a:b].value_counts()
    d = dT.loc[a:b]
    rows[label] = {'expanding low': int(r.get('low', 0)), 'expanding middle': int(r.get('middle', 0)),
                   'expanding high': int(r.get('high', 0)), 'T rising (12m)': int((d > 0).sum()),
                   'T falling (12m)': int((d <= 0).sum()), 'V/U > 1': int((T.loc[a:b] > 0).sum()),
                   'T min': round(float(T.loc[a:b].min()), 2), 'T max': round(float(T.loc[a:b].max()), 2)}
frame = pd.DataFrame(rows).T.astype(object)
frame.index.name = 'period'
table(frame)

# 6. Selected agent features: research vs sealed coverage.
emit('## 6. Selected agent features: months with a defined IC, research vs sealed\n')
rows = []
for study, root in STUDIES.items():
    sel = json.loads((root / 'outputs/selected_features.json').read_text())
    res = json.loads((root / 'outputs/sealed/initial/results.json').read_text())
    acc = {a['candidate_id']: a for a in res['candidate_accounting']}
    specs = {r['candidate_id']: r['spec']['expression'] for r in sel['seed_one_specs'] if r['valid']}
    for arm, ids in sel['selected'].items():
        for cid in ids:
            a = acc[cid]
            rows.append({'study': study, 'arm': arm, 'candidate': cid, 'expression': '`' + specs[cid] + '`',
                         'research IC': a['research']['mean'], 'research t': a['research']['t'],
                         'research n': a['research']['n'],
                         'sealed IC': a['sealed']['mean'], 'sealed n': a['sealed']['n']})
table(pd.DataFrame(rows).set_index('study'))

# 7. Ridge penalty chosen and research Sharpe of every strategy.
emit('## 7. Ridge penalty selected by CV (grid 0.01..1000) and research-period net Sharpe\n')
rows = []
for study, root in STUDIES.items():
    sel = json.loads((root / 'outputs/selected_features.json').read_text())
    summ = json.loads((root / 'outputs/research_summary.json').read_text())['strategies']
    for name, s in summ.items():
        rows.append({'study': study, 'strategy': name,
                     'alpha': sel['models'].get(name, {}).get('alpha', 'n/a (fixed rule)'),
                     'research Sharpe': s['sharpe'], 'research IC': s['IC']['mean'], 'IC t': s['IC']['t'],
                     'primary': 'yes' if name == sel['primary'] else ''})
table(pd.DataFrame(rows).set_index('study'))

(OUT / 'diagnostics.md').write_text('\n'.join(lines) + '\n')
print('\nwrote', OUT / 'diagnostics.md')
