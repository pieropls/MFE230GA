"""IC, Newey-West (HAC) inference, performance, factor regressions, placebo and deflated Sharpe.

The estimators follow the frozen study's stats.py so that numbers are comparable; run.ipynb
checks them against the frozen results.json (Gate 1).
"""
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, norm, skew

import params as P


def rank_ic(scores, target):
    """Monthly Spearman correlation between scores and target across groups (NaN if constant)."""
    scores, target = scores.align(target, join='inner')
    valid = scores.notna().all(axis=1) & target.notna().all(axis=1)
    rs, rt = scores.rank(axis=1), target.rank(axis=1)
    ok = valid & (rs.std(axis=1) > 0) & (rt.std(axis=1) > 0)
    out = pd.Series(np.nan, index=scores.index)
    out.loc[ok] = rs.loc[ok].corrwith(rt.loc[ok], axis=1)
    return out.rename('ic')


def hac(y, x=None, lags=P.HAC_LAGS):
    """OLS of y on a constant (and x) with Bartlett HAC errors on the calendar (gaps count as zero
    scores), small-sample factor n/(n-k). Returns dict with mean (=intercept), se, t, n, coefficients."""
    y = pd.Series(y).rename('y')
    design = pd.DataFrame({'intercept': 1.0}, index=y.index)
    if x is not None:
        design = design.join(x)
    joined = pd.concat([y, design], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    n, k = len(joined), design.shape[1]
    empty = {'n': n, 'mean': np.nan, 'se': np.nan, 't': np.nan, 'coef': {}, 'tstat': {}}
    if n <= max(k + 1, lags + 1):
        return empty
    a, b = joined[design.columns].to_numpy(), joined.y.to_numpy()
    bread = np.linalg.inv(a.T @ a)
    coef = bread @ a.T @ b
    score = pd.DataFrame(a * (b - a @ coef)[:, None], index=joined.index)
    score = score.reindex(pd.period_range(joined.index.min(), joined.index.max(), freq='M'), fill_value=0).to_numpy()
    meat = score.T @ score
    for lag in range(1, min(lags + 1, len(score))):
        cross = score[lag:].T @ score[:-lag]
        meat += (1 - lag / (lags + 1)) * (cross + cross.T)
    se = np.sqrt(np.maximum(0, np.diag(bread @ meat @ bread * n / (n - k))))
    t = np.divide(coef, se, out=np.full(k, np.nan), where=se > 1e-15)
    names = list(design.columns)
    return {'n': n, 'mean': float(coef[0]), 'se': float(se[0]), 't': float(t[0]),
            'coef': dict(zip(names, map(float, coef))), 'tstat': dict(zip(names, map(float, t))),
            'se_all': dict(zip(names, map(float, se)))}


def perf(ledger):
    """Frozen-study performance: annualised mean of net excess return, volatility, Sharpe,
    max drawdown of funded wealth (RF + net), hit rate, turnover, costs."""
    r = ledger.net.dropna()
    vol = r.std(ddof=1) * np.sqrt(12)
    wealth = (1 + ledger.total_net.dropna()).cumprod()
    drawdown = (wealth / wealth.cummax().clip(lower=1) - 1).min()
    return {'n': len(r), 'net_ann': 12 * r.mean(), 'vol': vol,
            'sharpe': 12 * r.mean() / vol if vol > 0 else np.nan,
            'max_dd': drawdown, 'hit': (r > 0).mean(), 'gross_ann': 12 * ledger.gross.mean(),
            'turnover': ledger.turnover.mean(), 'cost_ann': 12 * ledger.cost.mean()}


def group_momentum(total):
    """Top-3 minus bottom-3 groups on 11-month return m-12..m-2 (frozen attribution factor)."""
    signal = (1 + total).rolling(11, min_periods=11).apply(np.prod, raw=True).shift(2) - 1
    out = pd.Series(np.nan, index=total.index)
    for month, row in signal.iterrows():
        if row.notna().all() and total.loc[month].notna().all():
            rank = row.sort_index().sort_values(kind='stable')
            out.loc[month] = total.loc[month, rank.index[-3:]].mean() - total.loc[month, rank.index[:3]].mean()
    return out.rename('group_momentum')


def factor_attribution(net, returns, lags=P.HAC_LAGS):
    """Net returns on FF5 + Mom + group momentum, HAC (6 lags by default)."""
    factors = returns['factors'][['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'Mom']].join(group_momentum(returns['total']))
    return hac(net, factors, lags=lags)


def placebo(scores, target, months, min_shift=P.PLACEBO_MIN_SHIFT):
    """Circular time shift of the score panel against the target inside `months`.
    p = share of shifted mean ICs at or above the actual mean IC."""
    months = pd.PeriodIndex(months, freq='M')
    s, t = scores.reindex(months), target.reindex(months)
    actual = rank_ic(s, t).mean()
    shifted = []
    for k in range(min_shift, len(months) - min_shift + 1):
        rolled = pd.DataFrame(np.roll(s.to_numpy(), k, axis=0), index=months, columns=s.columns)
        shifted.append(rank_ic(rolled, t).mean())
    shifted = np.asarray(shifted)
    return {'actual_ic': float(actual), 'p': float(np.mean(shifted >= actual)), 'n_shifts': len(shifted)}


def deflated_sharpe(net, n_trials=P.N_TRIALS, trial_var=None):
    """Bailey & Lopez de Prado (2014). Benchmark = expected max monthly Sharpe of n_trials
    independent trials with variance trial_var (default 1/T, the null sampling variance)."""
    r = np.asarray(pd.Series(net).dropna(), dtype=float)
    T = len(r)
    sr = r.mean() / r.std(ddof=1)
    var = 1.0 / T if trial_var is None else trial_var
    g = np.euler_gamma
    sr0 = np.sqrt(var) * ((1 - g) * norm.ppf(1 - 1 / n_trials) + g * norm.ppf(1 - 1 / (n_trials * np.e)))
    denom = 1 - skew(r, bias=False) * sr + (kurtosis(r, fisher=False, bias=False) - 1) / 4 * sr ** 2
    dsr = float(norm.cdf((sr - sr0) * np.sqrt((T - 1) / denom))) if denom > 0 else np.nan
    return {'dsr': dsr, 'monthly_sharpe': float(sr), 'benchmark_monthly_sharpe': float(sr0),
            'benchmark_annual_sharpe': float(sr0 * np.sqrt(12)), 'T': T, 'n_trials': n_trials}


def window(frame, name):
    a, b = P.WINDOWS[name]
    return frame.loc[a:b]


def block_bootstrap_sharpe(net, block=12, draws=5000, seed=P.SEED, level=0.90):
    """Circular moving-block bootstrap of monthly returns; percentile interval for the annualised Sharpe."""
    r = np.asarray(pd.Series(net).dropna(), dtype=float)
    n = len(r)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(draws, n_blocks))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(draws, -1)[:, :n] % n
    samples = r[idx]
    sharpes = np.sqrt(12) * samples.mean(axis=1) / samples.std(axis=1, ddof=1)
    lo, hi = np.quantile(sharpes, [(1 - level) / 2, 1 - (1 - level) / 2])
    return {'sharpe': float(np.sqrt(12) * r.mean() / r.std(ddof=1)), 'low': float(lo), 'high': float(hi), 'n': n, 'block': block, 'draws': draws}
