"""Monthly inference and causal models. All inputs are explicit, never downloaded."""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, norm, skew
from sklearn.linear_model import Ridge

import params as P
import data as D


def monthly(frame):
    result = frame.copy()
    if isinstance(result.index, pd.DatetimeIndex):
        result.index = result.index.to_period('M') + 1
    if not isinstance(result.index, pd.PeriodIndex) or result.index.has_duplicates:
        raise ValueError('Expected unique monthly periods (or decision dates)')
    if not result.index.is_monotonic_increasing:
        raise ValueError('Months must be sorted')
    return result


def feature_matrices(features):
    return {name: monthly(f.pivot(index='decision', columns='group', values='value'))
            for name, f in features.groupby('feature')}


def target_horizon(total, horizon=1):
    if horizon not in P.INFERENCE['horizons']:
        raise ValueError('Unregistered horizon')
    compounded = (1 + total).rolling(horizon, min_periods=horizon).apply(np.prod, raw=True).shift(1-horizon) - 1
    compounded.loc[compounded.isna().any(axis=1)] = np.nan
    return compounded.sub(compounded.mean(axis=1), axis=0)


def rank_ic(scores, target):
    scores, target = monthly(scores).align(monthly(target), join='inner')
    valid = scores.notna().all(axis=1) & target.notna().all(axis=1)
    ranked_score = scores.rank(axis=1)
    ranked_target = target.rank(axis=1)
    nonconstant = ranked_score.std(axis=1)>0
    nonconstant &= ranked_target.std(axis=1)>0
    result = pd.Series(np.nan,index=scores.index)
    result.loc[nonconstant] = ranked_score.loc[nonconstant].corrwith(ranked_target.loc[nonconstant],axis=1)
    return result.where(valid).rename('ic')


def hac_regression(y, x=None, lags=None):
    """Bartlett HAC on actual calendar lags, preserving gaps in window subsets."""
    lags = P.INFERENCE['hac_lags'] if lags is None else lags
    y = monthly(y).rename('y')
    design = pd.DataFrame({'intercept': 1.0}, index=y.index)
    if x is not None:
        design = design.join(monthly(x))
    joined = pd.concat([y, design], axis=1).replace([np.inf,-np.inf], np.nan).dropna()
    n, k = len(joined), design.shape[1]
    empty = {'n': n, 'lags': lags, 'mean': np.nan, 'se': np.nan, 't': np.nan,
             'coefficients': {}, 'standard_errors': {}, 't_statistics': {}}
    if n <= max(k+1, lags+1):
        return empty
    a, b = joined[design.columns].to_numpy(), joined.y.to_numpy()
    if np.linalg.matrix_rank(a) < k:
        return empty
    bread = np.linalg.inv(a.T @ a)
    coef = bread @ a.T @ b
    residual = b - a @ coef
    score = pd.DataFrame(a * residual[:,None], index=joined.index)
    score = score.reindex(pd.period_range(joined.index.min(), joined.index.max(), freq='M'), fill_value=0).to_numpy()
    meat = score.T @ score
    for lag in range(1, min(lags+1, len(score))):
        cross = score[lag:].T @ score[:-lag]
        meat += (1-lag/(lags+1)) * (cross+cross.T)
    covariance = bread @ meat @ bread * n/(n-k)
    se = np.sqrt(np.maximum(0, np.diag(covariance)))
    t = np.divide(coef, se, out=np.full(k,np.nan), where=se>1e-15)
    names = design.columns
    return {'n': n, 'lags': lags, 'mean': float(coef[0]), 'se': float(se[0]), 't': float(t[0]),
            'coefficients': dict(zip(names,coef)), 'standard_errors': dict(zip(names,se)),
            't_statistics': dict(zip(names,t))}


def _contiguous(frame):
    frame = monthly(frame).replace([np.inf,-np.inf],np.nan).dropna()
    if len(frame) and len(pd.period_range(frame.index.min(), frame.index.max(), freq='M')) != len(frame):
        raise ValueError('Bootstrap requires a contiguous complete monthly sample')
    return frame


def stationary_indices(n, draws=None, block=None, seed=P.SEED):
    draws = P.INFERENCE['bootstrap_draws'] if draws is None else draws
    block = P.INFERENCE['mean_block'] if block is None else block
    if n < 2 or draws < 1 or block < 1:
        raise ValueError('Invalid bootstrap dimensions')
    rng = np.random.default_rng(seed)
    result = np.empty((draws,n), dtype=int)
    result[:,0] = rng.integers(n,size=draws)
    for t in range(1,n):
        restart = rng.random(draws) < 1/block
        result[:,t] = np.where(restart, rng.integers(n,size=draws), (result[:,t-1]+1)%n)
    return result


def paired_bootstrap(a, b, draws=None):
    a,b = monthly(a),monthly(b)
    calendar = pd.period_range(max(a.index.min(),b.index.min()),min(a.index.max(),b.index.max()),freq='M')
    frame = pd.concat([a.rename('a'),b.rename('b')],axis=1).reindex(calendar).replace([np.inf,-np.inf],np.nan)
    mask = frame.notna().all(axis=1).to_numpy()
    n = int(mask.sum())
    result = {'n':n,'calendar_n':len(frame),'difference':np.nan,'p_one_sided':np.nan,'low':np.nan,'high':np.nan}
    if n < 2:
        return {**result,'reason':'Fewer than two jointly observed months'}
    difference = (frame.a-frame.b).fillna(0).to_numpy()
    indices = stationary_indices(len(frame),draws=draws)
    counts = mask[indices].sum(axis=1)
    if (counts==0).any():
        return {**result,'reason':'A bootstrap draw has no jointly observed months'}
    sampled = difference[indices].sum(axis=1)/counts
    observed = difference.sum()/n
    return {**result,'difference':observed,
            'p_one_sided':(1+np.sum(sampled-observed >= observed))/(len(sampled)+1),
            'low':np.quantile(sampled,.025), 'high':np.quantile(sampled,.975)}


def holm(p_values):
    values = pd.Series(p_values,dtype=float)
    if values.isna().any():
        return pd.Series(np.nan,index=values.index)
    if ((values<0)|(values>1)).any():
        raise ValueError('Invalid endpoint p-value')
    ordered = values.sort_values(kind='stable')
    adjusted = np.maximum.accumulate(ordered.to_numpy()*np.arange(len(ordered),0,-1)).clip(0,1)
    return pd.Series(adjusted,index=ordered.index).reindex(values.index)


def reality_check(ic_matrix, nominal_trials, draws=None):
    matrix = monthly(ic_matrix).replace([np.inf,-np.inf],np.nan)
    if not matrix.index.equals(pd.period_range(matrix.index.min(),matrix.index.max(),freq='M')):
        raise ValueError('Reality check requires the full calendar, including missing observations')
    counts = matrix.notna().sum()
    result = {'calendar_n':len(matrix),'nominal_trials':nominal_trials,
              'effective_n':counts.to_dict(),'p':np.nan,
              'caveat':'Research diagnostic; resamples joint IC and missingness. Warm-up and regime-dependent missingness weaken stationarity.'}
    if len(matrix)<2 or (counts==0).any() or len(matrix.columns)!=nominal_trials:
        return {**result,'reason':'Full family contains an invalid/all-missing trial or has fewer than two months'}
    mask = matrix.notna().to_numpy()
    means = matrix.mean().to_numpy()
    values = matrix.fillna(0).to_numpy()
    observed = means.max()
    indices = stationary_indices(len(values),draws=draws)
    centered = values-mask*means
    null = []
    for index in indices:
        sampled_n = mask[index].sum(axis=0)
        if (sampled_n==0).any():
            return {**result,'reason':'A bootstrap draw contains a trial with no observations'}
        null.append((centered[index].sum(axis=0)/sampled_n).max())
    return {**result,'best_mean_ic':observed,'p':(1+np.sum(np.asarray(null)>=observed))/(len(null)+1)}


def deflated_sharpe(returns, trial_monthly_sharpes, nominal_trials):
    r = np.asarray(pd.Series(returns).dropna(), dtype=float)
    trials = np.asarray(trial_monthly_sharpes, dtype=float)
    trials = trials[np.isfinite(trials)]
    if len(r)<3 or len(trials)<2 or np.std(r,ddof=1)==0 or nominal_trials<2:
        return {'dsr':np.nan, 'reason':'Insufficient nondegenerate trials'}
    sr = r.mean()/r.std(ddof=1)
    gamma = np.euler_gamma
    benchmark = trials.std(ddof=1)*((1-gamma)*norm.ppf(1-1/nominal_trials)+gamma*norm.ppf(1-1/(nominal_trials*np.e)))
    denominator = 1-skew(r,bias=False)*sr+(kurtosis(r,fisher=False,bias=False)-1)*sr*sr/4
    dsr = norm.cdf((sr-benchmark)*np.sqrt((len(r)-1)/denominator)) if denominator>0 else np.nan
    return {'dsr':dsr, 'monthly_sharpe':sr, 'benchmark':benchmark, 'n':len(r), 'nominal_trials':nominal_trials,
            'caveat':'Research diagnostic; dependence and adaptive model search are not fully corrected'}


def chronological_folds(months):
    months = pd.PeriodIndex(months,freq='M')
    if not months.equals(pd.period_range(months.min(),months.max(),freq='M')):
        raise ValueError('CV requires consecutive whole months')
    start = P.MODEL['min_train_months']+P.MODEL['purge_months']
    validation = np.array_split(months[start:],P.MODEL['folds'])
    if any(len(v)==0 for v in validation):
        raise ValueError('Not enough months for CV')
    return [(months[months < v[0]-P.MODEL['purge_months']], pd.PeriodIndex(v,freq='M')) for v in validation]


def _design(features, target):
    names = list(features)
    if not names:
        raise ValueError('No model features')
    months = target.index
    groups = target.columns
    arrays = [monthly(features[name]).reindex(index=months,columns=groups).to_numpy() for name in names]
    x = np.stack(arrays,axis=2)
    y = target.to_numpy()
    usable = np.isfinite(x).all(axis=(1,2)) & np.isfinite(y).all(axis=1)
    return x,y,usable


def choose_alpha(features, target):
    target = monthly(target).loc[P.RESEARCH_START:P.SELECTION_END]
    x,y,usable = _design(features,target)
    folds = chronological_folds(target.index)
    losses = []
    for alpha in P.MODEL['penalties']:
        errors = []
        for train,valid in folds:
            ti,vi = target.index.get_indexer(train),target.index.get_indexer(valid)
            if not usable[np.r_[ti,vi]].all():
                raise ValueError('CV feature/target month is incomplete; resolve before comparing models')
            model = Ridge(alpha=alpha).fit(x[ti].reshape(-1,x.shape[-1]),y[ti].ravel())
            prediction = model.predict(x[vi].reshape(-1,x.shape[-1])).reshape(len(vi),y.shape[1])
            errors.extend(np.mean((prediction-y[vi])**2,axis=1))
        losses.append({'alpha':alpha,'monthly_mse':float(np.mean(errors))})
    # Exact ties are broken toward stronger regularization.
    best = min(losses,key=lambda row:(row['monthly_mse'],-row['alpha']))
    return best['alpha'],losses


def predict_expanding(features, target, alpha, prediction_months, label=None):
    target = monthly(target)
    training_months = pd.period_range(P.RESEARCH_START, max(prediction_months),freq='M')
    target = target.reindex(training_months)
    x,y,usable = _design(features,target)
    result = pd.DataFrame(np.nan,index=pd.PeriodIndex(prediction_months,freq='M'),columns=target.columns)
    logs = []
    for month in result.index:
        pos = target.index.get_loc(month)
        train = (target.index <= month-2) & usable
        if train.sum()<P.MODEL['min_train_months'] or not np.isfinite(x[pos]).all():
            continue
        model = Ridge(alpha=alpha).fit(x[train].reshape(-1,x.shape[-1]),y[train].ravel())
        result.loc[month] = model.predict(x[pos])
        logs.append({'return_month':str(month),'train_last':str(target.index[train][-1]),
                     'train_months':int(train.sum()),'alpha':alpha,'coefficients':model.coef_.tolist(),
                     'intercept':float(model.intercept_)})
    if label:
        for row in logs:
            D.append_event('model_fits.jsonl',{'strategy':label,**row})
    return result


def tightness_regimes(tightness):
    t = monthly(tightness)
    low = t.expanding(min_periods=P.MODEL['standardization_min_months']).quantile(1/3)
    high = t.expanding(min_periods=P.MODEL['standardization_min_months']).quantile(2/3)
    result = pd.Series('middle',index=t.index)
    result.loc[t<=low] = 'low'
    result.loc[t>=high] = 'high'
    return result.where(t.notna()&low.notna())


def maximum_correlation(candidate, base):
    correlations = []
    for other in base.values():
        a,b = candidate.align(other,join='inner')
        pairs = pd.DataFrame({'a':a.to_numpy().ravel(),'b':b.to_numpy().ravel()}).dropna()
        value = pairs.a.corr(pairs.b) if len(pairs)>2 else np.nan
        if np.isfinite(value):
            correlations.append(abs(value))
    return max(correlations) if correlations else np.nan


def candidate_feedback(candidate, target, base, tightness):
    candidate = candidate.loc[P.RESEARCH_START:P.SELECTION_END]
    target = target.reindex(candidate.index)
    ic = rank_ic(candidate,target)
    hac = hac_regression(ic)
    regime = tightness_regimes(tightness).reindex(ic.index)
    rank = candidate.rank(axis=1)
    feedback = {'coverage':np.isfinite(candidate).mean().mean(), 'mean_ic':ic.mean(), 'hac_t':hac['t'],
                'low_T_ic':ic.loc[regime=='low'].mean(),'high_T_ic':ic.loc[regime=='high'].mean(),
                'max_base_correlation':maximum_correlation(candidate,base),
                'rank_autocorrelation':rank.corrwith(rank.shift(1),axis=1).mean(), 'validity':'valid'}
    return {k:round(float(v),2) if isinstance(v,(float,np.floating)) and np.isfinite(v)
            else None if isinstance(v,(float,np.floating)) else v for k,v in feedback.items()}


def select_candidates(specs, values, target, base):
    eligible,decisions = [],[]
    boundary = pd.Period(P.RESEARCH_START)+(len(pd.period_range(P.RESEARCH_START,P.SELECTION_END,freq='M'))//2)
    for row in specs:
        if row['seed']!=1:
            continue
        cid = row['candidate_id']
        if not row['valid']:
            decisions.append({'candidate_id':cid,'eligible':False,'reason':'invalid'})
            continue
        score = values[cid].loc[P.RESEARCH_START:P.SELECTION_END]
        ic = rank_ic(score,target)
        stat = hac_regression(ic)
        correlation = maximum_correlation(score,base)
        passes = bool(stat['t']>=P.MODEL['candidate_min_t'] and ic.loc[ic.index<boundary].mean()>0
                      and ic.loc[ic.index>=boundary].mean()>0 and correlation<P.MODEL['candidate_max_correlation'])
        decisions.append({'candidate_id':cid,'eligible':passes,'t':stat['t'],'base_correlation':correlation,
                          'first_half_ic':ic.loc[ic.index<boundary].mean(),'second_half_ic':ic.loc[ic.index>=boundary].mean()})
        if passes:
            eligible.append((cid,stat['t']))
    selected = []
    for cid,_ in sorted(eligible,key=lambda item:(-item[1],item[0])):
        if selected and not maximum_correlation(values[cid].loc[P.RESEARCH_START:P.SELECTION_END],{other:values[other].loc[P.RESEARCH_START:P.SELECTION_END] for other in selected})<P.MODEL['candidate_max_correlation']:
            continue
        selected.append(cid)
        if len(selected)==P.MODEL['candidate_max']:
            break
    return selected,decisions


def performance(ledger):
    r = ledger.net.dropna()
    volatility = r.std(ddof=1)*np.sqrt(12)
    wealth = (1+ledger.total_net.dropna()).cumprod()
    peak = wealth.cummax().clip(lower=1)
    contiguous = bool(len(ledger)) and ledger.index.equals(pd.period_range(ledger.index.min(),ledger.index.max(),freq='M'))
    result = {'n':len(r),'mean_net_annual':12*r.mean(),'volatility':volatility,
              'sharpe':12*r.mean()/volatility if volatility>0 else np.nan,
              'max_drawdown':(wealth/peak-1).min() if contiguous else np.nan,'hit_rate':(r>0).mean(),
              'drawdown_note':'Funded NAV' if contiguous else 'Unavailable for disconnected conditional months',
              'mean_gross_annual':12*ledger.gross.mean(),'turnover':ledger.turnover.mean(),
              'hedge_turnover':ledger.hedge_turnover.mean(),'cost':ledger.cost.mean(),
              'borrow_financing':ledger.borrow_financing.mean()}
    if 'active' in ledger:
        tracking = ledger.active.std(ddof=1)*np.sqrt(12)
        result.update(active_return=ledger.active.mean()*12,tracking_error=tracking,
                      information_ratio=ledger.active.mean()*12/tracking if tracking>0 else np.nan)
    return result


def group_momentum(total):
    # At the decision for return month m, the most recent full month is m-2.
    signal = (1+total).rolling(11,min_periods=11).apply(np.prod,raw=True).shift(2)-1
    result = pd.Series(np.nan,index=total.index)
    for month,row in signal.iterrows():
        if row.notna().all() and total.loc[month].notna().all():
            rank = row.sort_index().sort_values(kind='stable')
            result.loc[month] = total.loc[month,rank.index[-3:]].mean()-total.loc[month,rank.index[:3]].mean()
    return result.rename('group_momentum')


def factor_attribution(net, returns):
    factors = returns['factors'][['Mkt-RF','SMB','HML','RMW','CMA','Mom']].join(group_momentum(returns['total']))
    return hac_regression(net,factors)


def circular_placebo(features, evaluator, actual_ic, months):
    if not np.isfinite(actual_ic):
        raise ValueError('Observed placebo statistic must be finite')
    months = pd.PeriodIndex(months,freq='M')
    k = P.INFERENCE['placebo_min_shift']
    values = []
    for shift in range(k,len(months)-k+1):
        shifted = {}
        for name,frame in features.items():
            shifted[name] = frame.copy()
            shifted[name].loc[months] = np.roll(frame.loc[months].to_numpy(),shift,axis=0)
        values.append({'shift':shift,'mean_ic':float(evaluator(shifted,shift))})
    scores = np.array([v['mean_ic'] for v in values])
    if not len(scores) or not np.isfinite(scores).all():
        raise ValueError('Incomplete prespecified placebo shifts')
    return {'p':float(np.mean(scores>=actual_ic)), 'shifts':values}


def evaluation_windows(index, tightness):
    index = pd.PeriodIndex(index,freq='M')
    regimes = tightness_regimes(tightness).reindex(index)
    cut = len(index)//2
    return {'whole':index,'first_half':index[:cut],'second_half':index[cut:],
            'ex_pandemic':index[(index<pd.Period('2020-03'))|(index>pd.Period('2020-12'))],
            'last_18':index[-P.INFERENCE['last_window_months']:],
            **{f'T_{name}':index[regimes.eq(name)] for name in ['low','middle','high']},
            'VU_below_1':index[tightness.reindex(index)<0],
            'VU_above_1':index[tightness.reindex(index)>0]}


def gate(primary, ic, attribution, placebo_p, profit_share, costly_sharpe, audit, capacity_documented):
    halves = [ic.iloc[:len(ic)//2],ic.iloc[len(ic)//2:]]
    stat = hac_regression(ic)
    flags = {
        'G1':audit.get('variant')=='ASOF' and audit.get('open_flags')==[],
        'G2':np.isfinite(stat['mean']) and np.isfinite(stat['t']) and stat['mean']>0 and stat['t']>=P.INFERENCE['gate_min_t'],
        'G3':np.isfinite(attribution['mean']) and np.isfinite(attribution['t']) and attribution['mean']>0 and attribution['t']>=P.INFERENCE['gate_min_t'],
        'G4':all(x.mean()>0 for x in halves) and np.isfinite(placebo_p) and 0<=placebo_p<P.INFERENCE['gate_placebo_p'] and np.isfinite(profit_share) and 0<=profit_share<=P.INFERENCE['gate_max_profit_share'],
        'G5':np.isfinite(costly_sharpe) and costly_sharpe>0 and capacity_documented is True,
    }
    flags = {k:bool(v) for k,v in flags.items()}
    return {'primary':primary,'criteria':flags,'verdict':'Implement' if all(flags.values()) else 'Do not implement',
            'failed':[k for k,v in flags.items() if not v],
            'power':'142 sealed months require roughly 0.6 annualized Sharpe for IID t≈2; a null does not rule out a smaller effect.'}


def clean_json(value):
    if isinstance(value,dict):
        return {str(k):clean_json(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [clean_json(v) for v in value]
    if isinstance(value,np.generic):
        return clean_json(value.item())
    if isinstance(value,float) and not math.isfinite(value):
        return None
    return value


def construct_strategies(base, tightness, specs, candidates, target):
    """Deterministic selection; no engineer feature proposals or manual ranking."""
    selected,selection = {},{}
    for arm in P.AGENT['arms']:
        rows = [r for r in specs if r['arm']==arm]
        selected[arm],selection[arm] = select_candidates(rows,candidates,target,base)
    models = {'A1':dict(base),'A1-T':{**base,**{name+'*T':x.mul(tightness,axis=0) for name,x in base.items()}}}
    models['A3'] = {**base,**{cid:candidates[cid].fillna(0) for cid in selected['independent']}}
    models['A4'] = {**base,**{cid:candidates[cid].fillna(0) for cid in selected['islands']}}
    configuration = {'selected':selected,'decisions':selection,'models':{},'primary':None}
    for name,features in models.items():
        alpha,losses = choose_alpha(features,target)
        configuration['models'][name] = {'features':list(features),'alpha':alpha,'cv':losses}
    return models,configuration


def score_models(models, configuration, base, target, months, log_prefix=None):
    scores = {'A0':((base['F1']+base['F2']-base['F4']+base['F5'])/4).reindex(months)}
    for name,features in models.items():
        scores[name] = predict_expanding(features,target,configuration['models'][name]['alpha'],months,
                                        label=f'{log_prefix}:{name}' if log_prefix else None)
    return scores


def research_run(base, tightness, specs, candidates, returns):
    if returns['total'].index.max()>pd.Period(P.SELECTION_END):
        raise PermissionError('Research evaluator received sealed returns')
    expected = len(P.AGENT['arms'])*len(P.AGENT['seeds'])*len(P.AGENT['emphases'])*P.AGENT['submissions']
    if len(specs)!=expected or len({r['candidate_id'] for r in specs})!=expected:
        raise ValueError('Full fixed-budget agent library is required before selection')
    base = {k:v.loc[:P.SELECTION_END] for k,v in base.items()}
    candidates = {k:v.loc[:P.SELECTION_END] for k,v in candidates.items()}
    models,configuration = construct_strategies(base,tightness,specs,candidates,returns['relative'])
    months = pd.period_range(P.RESEARCH_START,P.SELECTION_END,freq='M')
    scores = score_models(models,configuration,base,returns['relative'],months,log_prefix='research')
    common = months.copy()
    for value in scores.values():
        common = common.intersection(value.index[value.notna().all(axis=1)])
    if len(common)<P.MODEL['min_train_months']:
        raise ValueError('Too few common research predictions')
    ledgers,ics,summary,trial_sr = {},{}, {},[]
    for name,value in scores.items():
        ledger,weights = D.backtest(value.loc[common],returns)
        ledgers[name] = ledger
        ics[name] = rank_ic(value.loc[common],returns['relative'])
        summary[name] = {**performance(ledger),'IC':hac_regression(ics[name])}
        ledger.to_csv(P.OUT/f'research_{name}_ledger.csv')
        weights.to_csv(P.OUT/f'research_{name}_weights.csv')
        trial_sr.append(ledger.net.mean()/ledger.net.std(ddof=1))
    seed_one = [r for r in specs if r['seed']==1]
    candidate_stats = []
    for row in seed_one:
        cid = row['candidate_id']
        if not row['valid']:
            candidate_stats.append({'candidate_id':cid,'valid':False})
            ics[cid] = pd.Series(np.nan,index=months)
            continue
        score = candidates[cid].loc[P.RESEARCH_START:P.SELECTION_END]
        ic = rank_ic(score,returns['relative'])
        ics[cid] = ic
        diagnostic_score = score.reindex(common)
        available = diagnostic_score.notna().all(axis=1)&diagnostic_score.std(axis=1).gt(0)
        ledger,_ = D.backtest(diagnostic_score,returns,signal_available=available)
        trial_sr.append(ledger.net.mean()/ledger.net.std(ddof=1) if ledger.net.std(ddof=1)>0 else np.nan)
        ledger.to_csv(P.OUT/f'research_candidate_{cid}_ledger.csv')
        candidate_stats.append({'candidate_id':cid,'valid':True,**hac_regression(ic)})
    nominal = len(seed_one)+len(scores)
    # Section 12 distinguishes the candidate-only reality check from the DSR family.
    candidate_ics = {row['candidate_id']:ics[row['candidate_id']] for row in seed_one}
    reality = reality_check(pd.DataFrame(candidate_ics).reindex(months),len(seed_one))
    reality['family'] = '36 seed-1 candidate slots; corrected-run diagnostic'
    for name,ledger in ledgers.items():
        summary[name]['deflated_sharpe'] = deflated_sharpe(ledger.net,trial_sr,nominal)
    eligible = [name for name in P.MODEL['primary_order'] if name in summary]
    if not all(np.isfinite(summary[name]['sharpe']) for name in eligible):
        raise ValueError('Undefined primary-strategy Sharpe')
    configuration['primary'] = max(eligible,key=lambda name:summary[name]['sharpe'])
    configuration['common_research_months'] = list(map(str,common))
    configuration['seed_one_specs'] = seed_one
    D.write_json(P.OUT/'selected_features.json',clean_json(configuration))
    D.write_json(P.OUT/'research_summary.json',clean_json({'strategies':summary,'candidates':candidate_stats,'reality_check':reality}))
    return configuration,summary


def readiness():
    """These review artifacts are evidence records, never auto-approved defaults."""
    problems = []
    checks = {
        'timing_approval.json':lambda x:x.get('selection_end')==P.SELECTION_END,
        'p1_review.json':lambda x:x.get('complete') is True and x.get('open_flags')==[] and bool(x.get('evidence')),
        'p4_review.json':lambda x:x.get('complete') is True and len(x.get('decisions',[]))==10 and all(r.get('reason') and (not r.get('accepted') or r.get('test_id') in P.INFERENCE['diagnostic_ids']) for r in x['decisions']),
        'synthetic_checks.json':lambda x:x.get('passed') is True,
        'integration_checks.json':lambda x:x.get('passed') is True and x.get('synthetic_only') is True,
        'selected_features.json':lambda x:x.get('primary') in P.MODEL['primary_order'],
        'agents/blinding_audit.json':lambda x:x.get('passed') is True,
        'agents/migration_review.json':lambda x:(x.get('total_judgments')==0 or (x.get('review_fraction') or 0)>=P.AGENT['judge_review_fraction']) and x.get('complete') is True,
        'panel_audit.json':lambda x:x.get('passed') is True and x.get('open_flags')==[],
        'capacity_review.json':lambda x:type(x.get('complete')) is bool and bool(x.get('reason')),
    }
    for file,check in checks.items():
        path = P.OUT/file
        if not path.exists():
            problems.append('Missing '+file)
        elif not check(json.loads(path.read_text())):
            problems.append('Incomplete '+file)
    evidence_requirements = {
        'p1_review.json':['data.py','outputs/manifest.csv','outputs/crosswalk.csv'],
        'p4_review.json':['stats.py','outputs/research_summary.json','outputs/selected_features.json'],
        'synthetic_checks.json':['params.py','data.py','stats.py','agents.py','plots.py'],
        'integration_checks.json':['params.py','data.py','stats.py','agents.py','plots.py'],
        'agents/blinding_audit.json':['outputs/agents/log.jsonl'],
        'agents/migration_review.json':['outputs/agents/migration_judgments.json'],
        'panel_audit.json':[f'outputs/{kind}_{variant.lower()}.parquet' for kind in ['panel','features','levels','tightness'] for variant in P.VARIANTS],
    }
    for artifact,required in evidence_requirements.items():
        path = P.OUT/artifact
        if not path.exists():
            continue
        hashes = json.loads(path.read_text()).get('evidence_hashes',{})
        for name in required:
            if not (P.ROOT/name).exists() or hashes.get(name)!=D.sha256(P.ROOT/name):
                problems.append(f'Stale or missing {artifact} evidence: {name}')
    import agents
    try:
        agents.require_transport()
    except (PermissionError,FileNotFoundError):
        problems.append('Experimental transport is unverified')
    return {'ready_to_freeze':not problems,'open_flags':problems,'variant':'ASOF'}


def freeze():
    if (P.OUT/'FREEZE.json').exists():
        return D.verify_freeze()
    status = readiness()
    D.write_json(P.OUT/'readiness.json',status)
    if not status['ready_to_freeze']:
        raise PermissionError('; '.join(status['open_flags']))
    D.stage0()
    required = ['params.py','data.py','stats.py','agents.py','plots.py']
    operational_logs = {'FREEZE.json','checkpoints.md','deviations.md','model_fits.jsonl','return_access.jsonl','figures.jsonl'}
    required += [str(path.relative_to(P.ROOT)) for path in P.OUT.rglob('*') if path.is_file() and path.name not in operational_logs and 'sealed' not in path.parts]
    required += [item['file'] for item in json.loads((P.OUT/'input_hashes.json').read_text())]
    hashes = {name:D.sha256(P.ROOT/name) for name in sorted(set(required))}
    record = {'utc':D.utc_now(),'hashes':hashes,'notebook_source_sha256':D.notebook_source_hash(),
              'selection_end':P.SELECTION_END,'first_sealed_decision':P.FIRST_SEALED_DECISION}
    D.write_json(P.OUT/'FREEZE.json',record,exclusive=True)
    return D.verify_freeze()


def frozen_models(base, tightness, candidates, configuration):
    all_features = {**base,**{k:v.fillna(0) for k,v in candidates.items()},
                    **{name+'*T':x.mul(tightness,axis=0) for name,x in base.items()}}
    return {name:{key:all_features[key] for key in settings['features']} for name,settings in configuration['models'].items()}


def drop_group_diagnostic(features, variables, tightness, blind, configuration, returns, months):
    """Recompute transforms, target ranks, fitted coefficients and risk; keep selection/alpha fixed."""
    import agents
    decoded = {v:int(k) for k,v in blind['groups'].items()}
    primary = configuration['primary']
    output = {}
    for removed in returns['total'].columns:
        groups = returns['total'].columns.drop(removed)
        base = {}
        for name,rows in features.groupby('feature'):
            raw = monthly(rows.pivot(index='decision',columns='group',values='raw_value')).loc[:,groups]
            base[name] = D.standardize(raw)[0]
        subset_variables = {name:value.drop(columns=blind['groups'][str(removed)]) for name,value in variables.items()}
        candidates = {r['candidate_id']:agents.evaluate_expression(r['spec']['expression'],subset_variables,tightness).rename(columns=decoded).sort_index(axis=1)
                      for r in configuration['seed_one_specs'] if r['valid']}
        reduced = {**returns,'total':returns['total'][groups],'excess':returns['excess'][groups]}
        reduced['relative'] = reduced['excess'].sub(reduced['excess'].mean(axis=1),axis=0)
        models = frozen_models(base,tightness,candidates,configuration)
        score = score_models({primary:models[primary]} if primary!='A0' else {},configuration,base,reduced['relative'],months,log_prefix=f'drop_{removed}')[primary]
        ledger,_ = D.backtest(score,reduced)
        output[str(removed)] = {**performance(ledger),'IC':hac_regression(rank_ic(score,reduced['relative'])),
                               'alpha':factor_attribution(ledger.net,reduced)}
    return output


def evaluate_frozen(returns, freeze_record, run_id):
    """Invoked only by data.final_evaluation after the durable opening marker."""
    import agents
    directory = P.OUT/'sealed'/run_id
    directory.mkdir(parents=True,exist_ok=False)
    configuration = json.loads((P.OUT/'selected_features.json').read_text())
    blind = json.loads((P.OUT/'blind_map.json').read_text())
    reversed_groups = {v:int(k) for k,v in blind['groups'].items()}
    months = pd.period_range(pd.Period(P.FIRST_SEALED_DECISION,freq='M')+1,P.LAST_RETURN,freq='M')
    variants,all_scores,all_ledgers = {},{},{}
    for variant in P.VARIANTS:
        suffix = variant.lower()
        base = feature_matrices(pd.read_parquet(P.OUT/f'features_{suffix}.parquet'))
        tightness = monthly(pd.read_parquet(P.OUT/f'tightness_{suffix}.parquet')['T'])
        levels = pd.read_parquet(P.OUT/f'levels_{suffix}.parquet')
        variables = {}
        for name,identifier in blind['variables'].items():
            value = monthly(levels.loc[levels.variable==name].pivot(index='decision',columns='group',values='value'))
            value.columns = [blind['groups'][str(g)] for g in value.columns]
            variables[identifier] = value.sort_index(axis=1)
        candidates = {r['candidate_id']:agents.evaluate_expression(r['spec']['expression'],variables,tightness).rename(columns=reversed_groups).sort_index(axis=1)
                      for r in configuration['seed_one_specs'] if r['valid']}
        models = frozen_models(base,tightness,candidates,configuration)
        scores = score_models(models,configuration,base,returns['relative'],months,log_prefix=f'{run_id}:{variant}')
        variant_summary,ledgers = {},{}
        for name,score in scores.items():
            ledger,weights = D.backtest(score,returns)
            ledgers[name] = ledger
            ledger.to_csv(directory/f'{variant}_{name}_ledger.csv')
            weights.to_csv(directory/f'{variant}_{name}_weights.csv')
            ic = {str(h):hac_regression(rank_ic(score,target_horizon(returns['total'],h)),lags=h+5) for h in P.INFERENCE['horizons']}
            rank_ic(score,returns['relative']).to_csv(directory/f'{variant}_{name}_ic.csv')
            score.to_csv(directory/f'{variant}_{name}_scores.csv')
            variant_summary[name] = {**performance(ledger),'IC':ic}
        variants[variant] = variant_summary
        all_scores[variant],all_ledgers[variant] = scores,ledgers
        if variant=='ASOF':
            primary_base,primary_t,primary_candidates,primary_models = base,tightness,candidates,models
            primary_variables = variables
    scores,ledgers = all_scores['ASOF'],all_ledgers['ASOF']
    comparisons = []
    for a,b,inferential in [('A1','A0',True),('A3','A1',True),('A4','A3',False),('A1-T','A1',False)]:
        for endpoint in ['IC','return']:
            first = rank_ic(scores[a],returns['relative']) if endpoint=='IC' else ledgers[a].net
            second = rank_ic(scores[b],returns['relative']) if endpoint=='IC' else ledgers[b].net
            comparisons.append({'comparison':a+' vs '+b,'endpoint':endpoint,'inferential':inferential,**paired_bootstrap(first,second)})
    family = {i:row['p_one_sided'] for i,row in enumerate(comparisons) if row['inferential']}
    corrected = holm(family)
    for i,value in corrected.items():
        comparisons[i]['holm_p'] = value
        if not np.isfinite(value):
            comparisons[i]['holm_status'] = 'Entire family unavailable because at least one registered endpoint is unavailable'
    primary = configuration['primary']
    primary_ic = rank_ic(scores[primary],returns['relative'])
    attribution = {name:factor_attribution(ledger.net,returns) for name,ledger in ledgers.items()}
    costly,costly_weights = D.backtest(scores[primary],returns,cost_bps=25)
    costly.to_csv(directory/'primary_cost25_ledger.csv')
    sensitivities = {}
    for holding in P.PORTFOLIO['holdings_sensitivity']:
        sensitivities['holding_'+str(holding)] = performance(D.backtest(scores[primary],returns,holding=holding)[0])
    for cost in P.PORTFOLIO['cost_sensitivity_bps']:
        sensitivities['cost_'+str(cost)] = performance(D.backtest(scores[primary],returns,cost_bps=cost)[0])
    sensitivities['borrow_25'] = performance(D.backtest(scores[primary],returns,borrow_bps=25)[0])
    def placebo_score(shifted,shift):
        if primary=='A0':
            prediction = (shifted['F1']+shifted['F2']-shifted['F4']+shifted['F5'])/4
        else:
            prediction = predict_expanding(shifted,returns['relative'],configuration['models'][primary]['alpha'],months,label=f'{run_id}:placebo:{shift}')
        return rank_ic(prediction.reindex(months),returns['relative']).mean()
    feature_set = primary_base if primary=='A0' else primary_models[primary]
    placebo = circular_placebo(feature_set,placebo_score,primary_ic.mean(),months)
    weights = pd.read_csv(directory/f'ASOF_{primary}_weights.csv',index_col=0)
    weights.index = pd.PeriodIndex(weights.index,freq='M')
    weights.columns = [int(c) if c!='market' else c for c in weights.columns]
    contributions = (weights[returns['excess'].columns]*returns['excess'].loc[months]).sum()
    total_profit = ledgers[primary].net.sum()
    profit_share = max(0,float(contributions.max()))/total_profit if total_profit>0 else np.inf
    windows = {name:{label:{**performance(ledger.reindex(index)),'IC':hac_regression(rank_ic(scores[name].reindex(index),returns['relative']))}
                     for label,index in evaluation_windows(months,primary_t).items()} for name,ledger in ledgers.items()}
    accounting = []
    decision_lookup = {row['candidate_id']:row for rows in configuration['decisions'].values() for row in rows}
    for row in configuration['seed_one_specs']:
        cid = row['candidate_id']
        if row['valid']:
            value = primary_candidates[cid]
            sealed_stat = hac_regression(rank_ic(value.reindex(months),returns['relative']))
            half = len(months)//2
            sealed_first = rank_ic(value.reindex(months[:half]),returns['relative']).mean()
            sealed_second = rank_ic(value.reindex(months[half:]),returns['relative']).mean()
            passed_research = bool(decision_lookup.get(cid,{}).get('eligible',False))
            passed_sealed = bool(sealed_stat['t']>=P.MODEL['candidate_min_t'] and sealed_first>0 and sealed_second>0)
            accounting.append({'candidate_id':cid,'research':hac_regression(rank_ic(value.loc[P.RESEARCH_START:P.SELECTION_END],returns['relative'])),
                               'sealed':sealed_stat,'passed_research_filter':passed_research,
                               'sealed_predictive_pass':passed_sealed,
                               'research_pass_sealed_failure':passed_research and not passed_sealed})
        else:
            accounting.append({'candidate_id':cid,'valid':False})
    # These mixed windows are descriptive: research uses coefficients/features selected in research.
    all_months = pd.period_range(P.RESEARCH_START,P.LAST_RETURN,freq='M')
    mixed_scores = score_models(primary_models,configuration,primary_base,returns['relative'],all_months,log_prefix=f'{run_id}:course')
    course = {}
    for name,score in mixed_scores.items():
        usable = score.notna().all(axis=1)
        ledger,_ = D.backtest(score.loc[usable],returns)
        ledger.to_csv(directory/f'course_{name}_ledger.csv')
        course[name] = {}
        for label,start in [('full',P.RESEARCH_START),('post_2010','2010-01')]:
            selected_ledger = ledger.loc[start:]
            course[name][label] = {**performance(selected_ledger),'IC':hac_regression(rank_ic(score.reindex(selected_ledger.index),returns['relative'])),
                                  'first_observed_return':str(selected_ledger.index.min()),'requested_start':start,
                                  'label':'Descriptive mixed pseudo-real-time research and ASOF sealed; unavailable burn-in excluded'}
    dropped = drop_group_diagnostic(pd.read_parquet(P.OUT/'features_asof.parquet'),primary_variables,primary_t,blind,configuration,returns,months)
    audit = json.loads((P.OUT/'readiness.json').read_text())
    capacity_file = P.OUT/'capacity_review.json'
    capacity = json.loads(capacity_file.read_text()).get('complete') is True if capacity_file.exists() else False
    verdict = gate(primary,primary_ic,attribution[primary],placebo['p'],profit_share,performance(costly)['sharpe'],audit,capacity)
    turnover_total = ledgers[primary].turnover.sum()
    breakeven = (ledgers[primary].gross.sum()-ledgers[primary].hedge_turnover.sum()*P.PORTFOLIO['hedge_cost_bps']/10000-ledgers[primary].borrow_financing.sum())/turnover_total*10000 if turnover_total>0 else np.nan
    result = clean_json({'variants':variants,'comparisons':comparisons,'attribution':attribution,'windows':windows,
                         'placebo':placebo,'sensitivities':sensitivities,'candidate_accounting':accounting,
                         'research_pass_sealed_failure_count':sum(r.get('research_pass_sealed_failure',False) for r in accounting),
                         'candidate_failure_definition':'Passed complete research eligibility filter; failed sealed t>=1.5 and positive IC in each half. No sealed reselection.',
                         'course_windows':course,'drop_one_group':dropped,
                         'group_profit_share':profit_share,'cost_breakeven_bps':breakeven,'gate':verdict})
    D.write_json(directory/'results.json',result,exclusive=True)
    return result


def self_test():
    months = pd.period_range('2004-05',periods=80,freq='M')
    rng = np.random.default_rng(P.SEED)
    x = pd.DataFrame(rng.normal(size=(80,13)),index=months)
    assert np.allclose(rank_ic(x,x),1)
    assert np.allclose(rank_ic(x,-x),-1)
    assert rank_ic(x*0,x).isna().all()
    for train,valid in chronological_folds(months):
        assert train[-1] <= valid[0]-2 and len(train)>=36
    y = x*.01
    pred = predict_expanding({'x':x},y,1,months)
    assert pred.iloc[:37].isna().all().all() and pred.iloc[37].notna().all()
    altered = y.copy()
    altered.iloc[55:] += rng.normal(0,100,size=altered.iloc[55:].shape)
    again = predict_expanding({'x':x},altered,1,months)
    assert np.allclose(pred.iloc[37:57],again.iloc[37:57])
    assert np.array_equal(stationary_indices(80,draws=10),stationary_indices(80,draws=10))
    assert np.allclose(holm([.01,.03,.20]),[.03,.06,.20])
    returns = pd.DataFrame([[.1,.2],[-.1,.1],[.2,-.1],[0,0]],index=months[:4])
    expected = np.prod(1+returns.iloc[:3],axis=0)-1
    assert np.allclose(target_horizon(returns,3).iloc[0],expected-expected.mean())
    s = pd.Series(rng.normal(size=80),index=months)
    full = hac_regression(s)
    assert full['n']==80 and np.isfinite(full['t'])
    assert hac_regression(s.iloc[::2])['n']==40
    gap = s.drop(s.index[40])
    paired = paired_bootstrap(gap,gap,draws=10)
    assert paired['calendar_n']==80 and paired['n']==79 and paired['p_one_sided']==1
    assert holm([.01,np.nan]).isna().all()
    unavailable = paired_bootstrap(s*0+np.nan,s,draws=10)
    assert unavailable['n']==0 and np.isnan(unavailable['p_one_sided'])
    verdict = gate('fixture',s,{'mean':.01,'t':3},.01,.2,np.inf,{'variant':'ASOF','open_flags':[]},True)
    assert verdict['criteria']['G5'] is False
    return {'known_IC':'passed','causal_training':'passed','whole_month_CV':'passed',
            'horizon_compounding':'passed','HAC_gaps':'passed','bootstrap':'passed','Holm':'passed'}
