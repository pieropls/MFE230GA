def signals(folder=P.FRED, last_decision=None, groups=None):
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
    # T at decision d uses the latest month <= d-2 with both V and U observed (frozen rule); this
    # matters once: the Oct 2025 household survey (UNEMPLOY) was never collected.
    ratio = np.log(panel['V'] / panel['U']).ffill()
    t = to_decision(ratio, P.JOLTS_LAG).reindex(decisions)
    t.index = t.index + 1
    return features, t
