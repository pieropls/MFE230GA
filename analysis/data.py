"""Loaders, group returns, labor signals and the (frozen) backtest.

Everything is indexed by EARNING month m: a decision at the end of month m-1 earns month m.
The portfolio construction is the frozen study's own `data.backtest`, imported read-only.
"""
import importlib.util
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


def signals(folder=P.FRED, last_decision=None, groups=None):
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
        value = value[list(groups)] if groups is not None else value   # drop-one-industry diagnostics
        z = standardize(value.reindex(decisions))
        z.index = z.index + 1                                         # earning month
        features[name] = z
    # T at decision d uses the latest month <= d-2 with both V and U observed (fixed-lag analogue of the frozen as-known rule); this
    # matters once: the Oct 2025 household survey (UNEMPLOY) was never collected.
    ratio = np.log(panel['V'] / panel['U']).ffill()
    t = to_decision(ratio, P.JOLTS_LAG).reindex(decisions)
    t.index = t.index + 1
    return features, t


def csrank(frame):
    return frame.rank(axis=1, pct=True, method='average')


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


def backtest_variant(scores, returns, holding=None, cost_bps=None, gross_cap=None, weighting='top3'):
    """Study 1's portfolio with two options (Study 2.3, R2 and R3): the gross cap (np.inf = none)
    and rank-weighted tranches. Also records the ex-ante volatility of the unit book and the gross
    exposure needed to reach the volatility target. With the defaults it reproduces `backtest`."""
    from sklearn.covariance import LedoitWolf
    pf = frozen()[0].PORTFOLIO
    holding = pf['holding'] if holding is None else holding
    cost_bps = pf['cost_bps'] if cost_bps is None else cost_bps
    cap = pf['gross_cap'] if gross_cap is None else gross_cap
    scores = scores.copy()
    scores.index = pd.PeriodIndex(scores.index, freq='M')
    available = scores.notna().all(axis=1) & scores.std(axis=1).gt(0)
    scores = scores.where(available, 0.0)
    groups = scores.columns
    tranches, rows, weight_rows = [], [], []
    pretrade = pd.Series(0., index=list(groups) + ['market'])
    for month, score in scores.iterrows():
        tranche = pd.Series(0., index=groups)
        if available.loc[month] and weighting == 'top3':
            rank = score.sort_index().sort_values(kind='stable')
            tranche.loc[rank.index[-pf['longs']:]] = 1 / pf['longs']
            tranche.loc[rank.index[:pf['shorts']]] = -1 / pf['shorts']
        elif available.loc[month]:                               # rank-weighted: longs sum to +1, shorts to -1
            demeaned = score.rank(method='average') - score.rank(method='average').mean()
            tranche = 2 * demeaned / demeaned.abs().sum()
        tranches.append(tranche)
        book = sum(tranches[-holding:]) / holding
        history = pd.period_range(month - pf['risk_window'] - 1, month - 2, freq='M')
        historical = returns['excess'].reindex(index=history, columns=groups).join(returns['factors']['Mkt-RF']).dropna()
        market = historical['Mkt-RF'].to_numpy()
        betas = pd.Series({g: np.cov(historical[g], market, ddof=1)[0, 1] / np.var(market, ddof=1) for g in groups})
        raw = np.r_[book.to_numpy(), -float(book @ betas)]
        covariance = LedoitWolf().fit(historical.to_numpy()).covariance_
        unit_vol = np.sqrt(max(0, float(raw @ covariance @ raw)) * 12)
        unit_gross = np.abs(raw).sum()
        scale_vol = pf['vol_target'] / unit_vol if unit_vol > 0 else 0.
        scale = min(scale_vol, cap / unit_gross) if unit_vol > 0 else 0.
        weights = pd.Series(raw * scale, index=pretrade.index)
        factors = returns['factors'].loc[month]
        current = returns['total'].loc[month, groups]
        turnover = float((weights[groups] - pretrade[groups]).abs().sum())
        hedge_turnover = abs(weights['market'] - pretrade['market'])
        cost = turnover * cost_bps / 1e4 + hedge_turnover * pf['hedge_cost_bps'] / 1e4
        financing = (-weights.clip(upper=0).sum() + max(0, float(weights.sum() - 1))) * pf['borrow_finance_base_bps_year'] / 1e4 / 12
        gross = float(weights[groups] @ returns['excess'].loc[month, groups] + weights['market'] * factors['Mkt-RF'])
        net = gross - cost - financing
        nav = 1 + factors.RF + net
        pretrade = weights * (1 + pd.concat([current, pd.Series({'market': factors['Mkt-RF'] + factors.RF})])) / nav
        rows.append({'month': month, 'gross': gross, 'net': net, 'turnover': turnover, 'hedge_turnover': hedge_turnover,
                     'total_net': net + factors.RF, 'cost': cost, 'borrow_financing': financing,
                     'ex_ante_vol': unit_vol * scale, 'gross_leverage': weights.abs().sum(),
                     'unit_vol': unit_vol, 'gross_needed': scale_vol * unit_gross,
                     'cap_binds': bool(unit_vol > 0 and cap / unit_gross < scale_vol)})
        weight_rows.append(weights.rename(month))
    return pd.DataFrame(rows).set_index('month'), pd.DataFrame(weight_rows)


# ---------------------------------------------------------------- as-known features (Alex's package)
def asknown_features(package=P.PACKAGE):
    """Raw F1..F5 and W as known at each month-end decision, rebuilt from Study 1's as-known panel
    with Study 1's transforms (reference month = latest month with >= 11 groups observed; 3-month
    averages; 12-month differences, log differences for hours and earnings). Long frame:
    decision (month), group, feature, raw."""
    panel = pd.read_parquet(package / 'studies/follow_the_workers/outputs/panel_asof.parquet',
                            columns=['decision', 'series_id', 'observation_month', 'value'])
    ids = {m: {g: f'JTU{v[1]}{m}' for g, v in P.GROUPS.items()} for m in P.JOLTS_MEASURES}
    ids['H'] = {g: f'CEU{v[2]}07' for g, v in P.GROUPS.items()}
    ids['E'] = {g: (P.CONSTRUCTION_EARNINGS if g == 2 else f'CEU{v[2]}08') for g, v in P.GROUPS.items()}
    avg3 = lambda wide, month: wide.reindex(pd.period_range(month - 2, month, freq='M')).mean(skipna=False)
    rows = []
    for decision, current in panel.groupby('decision', sort=True):
        wide = current.pivot(index='observation_month', columns='series_id', values='value')
        wide.index = pd.PeriodIndex(wide.index, freq='M')
        wide = wide.sort_index()
        by = {m: wide[list(ids[m].values())].set_axis(list(ids[m]), axis=1) for m in ids}       # measure -> month x group
        ok_j = pd.concat([by[m].notna().sum(axis=1) >= P.MIN_GROUPS for m in P.JOLTS_MEASURES], axis=1).all(axis=1)
        ok_c = by['H'].notna().sum(axis=1) >= P.MIN_GROUPS
        m_j = ok_j.index[ok_j].max() if ok_j.any() else None
        m_c = ok_c.index[ok_c].max() if ok_c.any() else None
        d = pd.Timestamp(decision).to_period('M')
        for i, m in enumerate(P.JOLTS_MEASURES, 1):
            value = avg3(by[m], m_j) - avg3(by[m], m_j - 12) if m_j is not None else pd.Series(np.nan, index=list(P.GROUPS))
            rows += [(d, g, f'F{i}', value[g]) for g in P.GROUPS]
        for name, key in [('F5', 'H'), ('W', 'E')]:
            if m_c is None:
                value = pd.Series(np.nan, index=list(P.GROUPS))
            else:
                a, b = avg3(by[key], m_c), avg3(by[key], m_c - 12)
                value = np.log((a / b).where((a > 0) & (b > 0)))
            rows += [(d, g, name, value[g]) for g in P.GROUPS]
    return pd.DataFrame(rows, columns=['decision', 'group', 'feature', 'raw'])
