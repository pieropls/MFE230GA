    for month,score in scores.iterrows():
        tranche = pd.Series(0.,index=groups)
        if signal_available.loc[month]:
            rank = score.sort_index().sort_values(kind='stable')
            tranche.loc[rank.index[-P.PORTFOLIO['longs']:]] = 1/P.PORTFOLIO['longs']
            tranche.loc[rank.index[:P.PORTFOLIO['shorts']]] = -1/P.PORTFOLIO['shorts']
        tranches.append(tranche)
        book = sum(tranches[-holding:])/holding
        betas = pd.Series({g:np.cov(historical[g],market,ddof=1)[0,1]/variance for g in groups})
        raw = np.r_[book.to_numpy(),-float(book@betas)]
        covariance = LedoitWolf().fit(historical.to_numpy()).covariance_
        risk = np.sqrt(max(0,float(raw@covariance@raw))*12)
        if risk<=0 and np.abs(raw).sum()>1e-14:
            raise ValueError('Degenerate portfolio risk estimate')
        scale = min(P.PORTFOLIO['vol_target']/risk,P.PORTFOLIO['gross_cap']/np.abs(raw).sum()) if risk>0 else 0.
        weights = pd.Series(raw*scale,index=pretrade.index)
        assert abs(weights[groups]@betas+weights['market'])<1e-10
        assert weights.abs().sum()<=P.PORTFOLIO['gross_cap']+1e-10
        turnover = float((weights[groups]-pretrade[groups]).abs().sum())
        hedge_turnover = abs(weights['market']-pretrade['market'])
        transaction = turnover*cost_bps/10000+hedge_turnover*P.PORTFOLIO['hedge_cost_bps']/10000
        # Charge borrowed securities plus negative residual cash, at the stated annual rate.
        borrow_base = -weights.clip(upper=0).sum()
        finance_base = max(0,float(weights.sum()-1))
        financing = (borrow_base+finance_base)*borrow_bps/10000/12
        gross = float(weights[groups]@returns['excess'].loc[month,groups]+weights['market']*factors['Mkt-RF'])
        net = gross-transaction-financing
