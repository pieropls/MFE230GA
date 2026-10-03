from pathlib import Path
import numpy as np, pandas as pd
from french import load, NAMES
J={1:'110099',2:'2300',3:'3200',4:'3400',5:'4200',6:'4400',7:'480099',8:'5100',9:'5200',10:'5300',11:'540099',12:'6200',13:'7200'}
C={1:'10000000',2:'20000000',3:'31000000',4:'32000000',5:'41420000',6:'42000000',7:'43000000',8:'50000000',9:'55000000',10:'55000000',11:'60000000',12:'65000000',13:'70000000'}
def fred(s):
    f=pd.read_csv(Path(__file__).resolve().parent/'data'/'fred'/f'{s}.csv');f.columns=['d','v'];f['v']=pd.to_numeric(f.v,errors='coerce')
    return pd.Series(f.v.values,index=pd.PeriodIndex(pd.to_datetime(f.d),freq='M'))
def raw_panel():
    out={}
    for m in ['JOR','HIR','QUR','LDR']:
        out[m]=pd.DataFrame({g:fred(f'JTU{J[g]}{m}') for g in J})
    out['H']=pd.DataFrame({g:fred(f'CEU{C[g]}07') for g in C})
    out['E']=pd.DataFrame({g:fred('CES2000000008' if g==2 else f'CEU{C[g]}08') for g in C})
    t=np.log(fred('JTSJOL')/fred('UNEMPLOY')).dropna()
    return out,t
def avg3(x): return x.rolling(3,min_periods=3).mean()
def standardize(raw,minp=24,lim=3):
    sig=raw.expanding(min_periods=minp).std(ddof=1).replace(0,np.nan)
    s=raw/sig
    z=s.sub(s.mean(axis=1),axis=0).div(s.std(axis=1,ddof=1),axis=0).clip(-lim,lim)
    ready=np.isfinite(s).sum(axis=1)>=11
    z.loc[ready]=z.loc[ready].fillna(0);z.loc[~ready]=np.nan
    return z
def features(jlag=2,clag=1):
    """Returns dict of standardized features indexed by EARNING month (decision month + 1)."""
    raw,t=raw_panel()
    f={}
    for i,m in enumerate(['JOR','HIR','QUR','LDR'],1):
        x=avg3(raw[m]);f[f'F{i}']=(x-x.shift(12)).shift(jlag)   # value known at decision month d uses obs d-jlag
    h=avg3(raw['H']);f['F5']=np.log(h/h.shift(12)).shift(clag)
    e=avg3(raw['E']);f['W']=np.log(e/e.shift(12)).shift(clag)  # wage growth (not in A0)
    out={k:standardize(v.loc['2001-01':]) for k,v in f.items()}
    # index currently = decision month; convert to earning month
    out={k:v.set_axis(v.index+1) for k,v in out.items()}
    T=t.shift(2);T.index=T.index+1
    return out,T,raw
def rank_ic(score,target):
    s,t=score.align(target,join='inner')
    ok=s.notna().all(axis=1)&t.notna().all(axis=1)&(s.std(axis=1)>0)
    return s[ok].rank(axis=1).corrwith(t[ok].rank(axis=1),axis=1)
def nw_t(x,lags=6):
    x=x.dropna().values;n=len(x);m=x.mean();e=x-m
    v=e@e/n
    for l in range(1,lags+1): v+=2*(1-l/(lags+1))*(e[l:]@e[:-l])/n
    return m/np.sqrt(v/n),n
