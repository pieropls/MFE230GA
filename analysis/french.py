import re, numpy as np, pandas as pd
from pathlib import Path
D=str(Path(__file__).resolve().parent/'data'/'french')+'/'
GROUPS={1:'Gold Mines Coal Oil',2:'Cnstr',3:'Toys BldMt Steel FabPr Mach ElcEq Autos Aero Ships Guns Hardw Chips LabEq MedEq',
4:'Food Soda Beer Smoke Hshld Clths Drugs Chems Rubbr Txtls Paper',5:'Whlsl',6:'Rtail',7:'Trans Util',8:'Telcm',9:'Banks Insur Fin',10:'RlEst',11:'BusSv',12:'Hlth',13:'Meals'}
NAMES={1:'Mining',2:'Construction',3:'Durable mfg',4:'Nondurable mfg',5:'Wholesale',6:'Retail',7:'Transport+Util',8:'Information',9:'Finance+Ins',10:'Real estate',11:'Prof+Bus svcs',12:'Health care',13:'Accom+Food'}
def sections(path):
    out={};title=None;header=None;rows=[]
    def fin():
        nonlocal rows
        if title and header and rows and title not in out:
            f=pd.DataFrame(rows,columns=['m']+header);f['m']=pd.PeriodIndex([f'{x[:4]}-{x[4:]}' for x in f.m],freq='M')
            out[title]=f.set_index('m').replace([-99.99,-999.0],np.nan)
        rows=[]
    for line in open(path,encoding='utf-8-sig'):
        line=line.strip();first=line.split(',')[0].strip()
        if re.fullmatch(r'\d{6}',first):
            if header: rows.append([first]+[float(c) for c in line.split(',')[1:]])
        elif first=='' and ',' in line:
            fin();header=[c.strip() for c in line.split(',')[1:]]
        elif line:
            fin();title=line;header=None
    fin();return out
def load():
    s=sections(D+'49_Industry_Portfolios.csv')
    pick=lambda t:[v for k,v in s.items() if t in k][0]
    ret=pick('Average Value Weighted Returns -- Monthly')/100
    cap=(pick('Number of Firms in Portfolios')*pick('Average Firm Size')).shift(1)
    g={}
    for k,m in GROUPS.items():
        m=m.split();g[k]=(ret[m]*cap[m]).sum(axis=1,min_count=len(m))/cap[m].sum(axis=1)
    total=pd.DataFrame(g)
    ff=list(sections(D+'F-F_Research_Data_5_Factors_2x3.csv').values())[0]/100
    mom=list(sections(D+'F-F_Momentum_Factor.csv').values())[0]/100;mom.columns=['Mom']
    f=ff.join(mom,how='inner')
    total=total.loc[f.index.min():]
    ex=total.sub(f.RF,axis=0)
    return {'total':total,'excess':ex,'relative':ex.sub(ex.mean(axis=1),axis=0),'factors':f,'ret49':ret,'cap49':cap}
