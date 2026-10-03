"""Loaders, group returns, labor signals and the (frozen) backtest.

Everything is indexed by EARNING month m: a decision at the end of month m-1 earns month m.
The portfolio construction is the frozen study's own `data.backtest`, imported read-only.
"""
import importlib.util
import json
import re
import sys
import time
import urllib.request
from functools import lru_cache

import numpy as np
import pandas as pd

import params as P


# ---------------------------------------------------------------- frozen study (read-only)
@lru_cache(maxsize=None)
def frozen():
    """Load the frozen study's params.py and data.py without writing anything into its folder."""
    sys.dont_write_bytecode = True
    saved = {k: sys.modules.get(k) for k in ('params', 'data')}
    modules = {}
    try:
        for name in ('params', 'data'):
            spec = importlib.util.spec_from_file_location('frozen_' + name, P.SONNET / f'{name}.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module          # frozen data.py does `import params as P`
            spec.loader.exec_module(module)
            modules[name] = module
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return modules['params'], modules['data']


def saved_csv(name, study=P.SONNET, folder='outputs/sealed/initial'):
    """Read a saved ledger / weights / scores / ic CSV from a frozen study."""
    frame = pd.read_csv(study / folder / name, index_col=0)
    frame.index = pd.PeriodIndex(frame.index, freq='M')
    frame.columns = [int(c) if str(c).isdigit() else c for c in frame.columns]
    return frame


def saved_json(name, study=P.SONNET):
    return json.loads((study / 'outputs' / name).read_text())


# ---------------------------------------------------------------- Ken French returns
def _french_sections(path):
    out, title, header, rows = {}, None, None, []

    def finish():
        nonlocal rows
        if title and header and rows and title not in out:
            frame = pd.DataFrame(rows, columns=['m'] + header)
            frame['m'] = pd.PeriodIndex([f'{x[:4]}-{x[4:]}' for x in frame.m], freq='M')
            out[title] = frame.set_index('m').replace([-99.99, -999.0], np.nan)
        rows = []

    for line in open(path, encoding='utf-8-sig'):
        line = line.strip()
        first = line.split(',')[0].strip()
        if re.fullmatch(r'\d{6}', first):
            if header:
                rows.append([first] + [float(c) for c in line.split(',')[1:]])
        elif first == '' and ',' in line:
            finish()
            header = [c.strip() for c in line.split(',')[1:]]
        elif line:
            finish()
            title, header = line, None
    finish()
    return out


@lru_cache(maxsize=None)
def load_returns():
    """13 group returns exactly as the frozen study builds them (value weights = prior-month caps)."""
    sections = _french_sections(P.FRENCH / '49_Industry_Portfolios.csv')
    pick = lambda text: [v for k, v in sections.items() if text in k][0]
    ret49 = pick('Average Value Weighted Returns -- Monthly') / 100
    cap49 = (pick('Number of Firms in Portfolios') * pick('Average Firm Size')).shift(1)
    total = {}
    for g, (_, _, _, members) in P.GROUPS.items():
        m = members.split()
        total[g] = (ret49[m] * cap49[m]).sum(axis=1, min_count=len(m)) / cap49[m].sum(axis=1)
    total = pd.DataFrame(total)
    ff = list(_french_sections(P.FRENCH / 'F-F_Research_Data_5_Factors_2x3.csv').values())[0] / 100
    mom = list(_french_sections(P.FRENCH / 'F-F_Momentum_Factor.csv').values())[0] / 100
    mom.columns = ['Mom']
    factors = ff.join(mom, how='inner')
    total = total.loc[factors.index.min():factors.index.max()]
    excess = total.sub(factors.RF, axis=0)
    return {'total': total, 'excess': excess, 'relative': excess.sub(excess.mean(axis=1), axis=0),
            'factors': factors, 'ret49': ret49, 'cap49': cap49}


def horizon_target(total, h):
    """h-month compounded total return from month m to m+h-1, demeaned across groups."""
    compounded = (1 + total).rolling(h, min_periods=h).apply(np.prod, raw=True).shift(1 - h) - 1
    compounded.loc[compounded.isna().any(axis=1)] = np.nan
    return compounded.sub(compounded.mean(axis=1), axis=0)


def industry_momentum(total):
    """Industry momentum 12-1: compounded return over months m-12..m-2 (skips m-1, as the frozen
    study's information rule and its group-momentum factor do)."""
    return (1 + total).rolling(11, min_periods=11).apply(np.prod, raw=True).shift(2) - 1


# ---------------------------------------------------------------- FRED labor data
def series_ids():
    ids = [f'JTU{v[1]}{m}' for v in P.GROUPS.values() for m in P.JOLTS_MEASURES]
    ids += [f'CEU{v[2]}07' for v in P.GROUPS.values()]
    ids += [P.CONSTRUCTION_EARNINGS if g == 2 else f'CEU{v[2]}08' for g, v in P.GROUPS.items()]
    return sorted(set(ids)) + ['JTSJOL', 'UNEMPLOY']


def read_fred(sid, folder=P.FRED):
    frame = pd.read_csv(folder / f'{sid}.csv')
    frame.columns = ['date', 'value']
    values = pd.to_numeric(frame.value, errors='coerce')
    return pd.Series(values.to_numpy(), index=pd.PeriodIndex(pd.to_datetime(frame.date), freq='M')).dropna()


def download_alfred(vintage_date=P.VINTAGE_DATE, folder=P.FRED_VINTAGE):
    """Values as published on `vintage_date` (ALFRED, no API key needed). Skips files already present."""
    folder.mkdir(parents=True, exist_ok=True)
    for sid in series_ids():
        path = folder / f'{sid}.csv'
        if path.exists() and path.stat().st_size > 200:
            continue
        url = f'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={sid}&vintage_date={vintage_date}'
        for attempt in range(3):
            try:
                urllib.request.urlretrieve(url, path)
                break
            except OSError:
                time.sleep(2)
        else:
            raise RuntimeError(f'ALFRED download failed for {sid}')
        time.sleep(0.3)
    return folder


def labor_panel(folder=P.FRED):
    """Raw monthly levels by observation month: JOR, HIR, QUR, LDR (rates), H (hours), E (earnings)."""
    panel = {m: pd.DataFrame({g: read_fred(f'JTU{v[1]}{m}', folder) for g, v in P.GROUPS.items()})
             for m in P.JOLTS_MEASURES}
    panel['H'] = pd.DataFrame({g: read_fred(f'CEU{v[2]}07', folder) for g, v in P.GROUPS.items()})
    panel['E'] = pd.DataFrame({g: read_fred(P.CONSTRUCTION_EARNINGS if g == 2 else f'CEU{v[2]}08', folder)
                               for g, v in P.GROUPS.items()})
    panel['V'] = read_fred('JTSJOL', folder)
    panel['U'] = read_fred('UNEMPLOY', folder)
    # consecutive monthly index, so that row shifts are month shifts
    return {k: v.reindex(pd.period_range(v.index.min(), v.index.max(), freq='M')) for k, v in panel.items()}


def standardize(raw):
    """Frozen-study transform: divide by own expanding s.d. (>=24 months), z-score across groups,
    winsorise at +-3, fill missing with 0 only when >=11 groups are observed."""
    sigma = raw.expanding(min_periods=P.STD_MIN_MONTHS).std(ddof=1).replace(0, np.nan)
    scaled = raw / sigma
    z = scaled.sub(scaled.mean(axis=1), axis=0).div(scaled.std(axis=1, ddof=1).replace(0, np.nan), axis=0)
    z = z.clip(-P.WINSOR, P.WINSOR)
    ready = np.isfinite(scaled).sum(axis=1) >= P.MIN_GROUPS
    z.loc[ready] = z.loc[ready].fillna(0)
    z.loc[~ready] = np.nan
    return z


def signals(folder=P.FRED, last_decision=None):
    """Standardised F1..F5 and W plus tightness T, indexed by earning month.

    F1..F4 = avg3(rate, m_J) - avg3(rate, m_J-12) with m_J = d - 2 (JOLTS)
    F5     = log avg3(hours, m_C) - log avg3(hours, m_C-12) with m_C = d - 1 (CES)
    W      = log avg3(earnings, m_C) - log avg3(earnings, m_C-12)
    T      = log(JTSJOL / UNEMPLOY) for month d - 2
    """
    panel = labor_panel(folder)
    avg3 = lambda x: x.rolling(3, min_periods=3).mean()
    raw = {}
    to_decision = lambda frame, lag: frame.set_axis(frame.index + lag)   # observation o -> decision o+lag
    for i, m in enumerate(P.JOLTS_MEASURES, 1):
        x = avg3(panel[m])
        raw[f'F{i}'] = to_decision(x - x.shift(12), P.JOLTS_LAG)
    h, e = avg3(panel['H']), avg3(panel['E'])
    raw['F5'] = to_decision(np.log(h / h.shift(12)), P.CES_LAG)
    raw['W'] = to_decision(np.log(e / e.shift(12)), P.CES_LAG)
    # last decision month at which every feature has its lagged observation
    end = last_decision or min(v.dropna(how='all').index.max() for v in raw.values())
    decisions = pd.period_range(P.SIGNAL_START, end, freq='M')
    features = {}
    for name, value in raw.items():
        z = standardize(value.reindex(decisions))
        z.index = z.index + 1                                         # earning month
        features[name] = z
    # T at decision d uses the latest month <= d-2 with both V and U observed (frozen rule); this
    # matters once: the Oct 2025 household survey (UNEMPLOY) was never collected.
    ratio = np.log(panel['V'] / panel['U']).ffill()
    t = to_decision(ratio, P.JOLTS_LAG).reindex(decisions)
    t.index = t.index + 1
    return features, t


def csrank(frame):
    return frame.rank(axis=1, pct=True, method='average')


def cszscore(frame):
    return frame.sub(frame.mean(axis=1), axis=0).div(frame.std(axis=1, ddof=1), axis=0)


# ---------------------------------------------------------------- portfolio
def backtest(scores, returns, holding=None, cost_bps=None):
    """Frozen-study portfolio: tranches, 60m beta hedge, 10% vol target, gross cap 2, costs.

    A month whose scores are missing or constant opens no new tranche (frozen convention)."""
    _, frozen_data = frozen()
    scores = scores.copy()
    scores.index = pd.PeriodIndex(scores.index, freq='M')
    available = scores.notna().all(axis=1) & scores.std(axis=1).gt(0)
    return frozen_data.backtest(scores.where(available, 0.0), returns, holding=holding,
                                cost_bps=cost_bps, signal_available=available)
