"""Auditable input preparation, point-in-time features and guarded return access."""
import csv
import hashlib
import io
import json
import os
import platform
import re
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.covariance import LedoitWolf
from pandas.tseries.holiday import GoodFriday, USMemorialDay

import params as P

_SEALED_CAPABILITY = object()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def notebook_source_hash():
    notebook = json.loads((P.ROOT/'run.ipynb').read_text())
    source = [{'cell_type':c['cell_type'],'source':c['source']} for c in notebook['cells']]
    return hashlib.sha256(json.dumps(source,sort_keys=True).encode()).hexdigest()


def write_json(path, value, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2, allow_nan=False, default=str) + '\n'
    if exclusive:
        with path.open('x') as stream:
            stream.write(text)
    else:
        temporary = path.with_suffix(path.suffix + '.tmp')
        temporary.write_text(text)
        temporary.replace(path)


def append_event(name, event):
    path = P.OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps({'timestamp': utc_now(), **event}, default=str, allow_nan=False) + '\n')


def stage0():
    """Record the design before numeric returns are parsed; never overwrite it."""
    approval = P.OUT / 'timing_approval.json'
    if P.BOUNDARY_APPROVAL_REQUIRED and (not approval.exists() or json.loads(approval.read_text()).get('selection_end') != P.SELECTION_END):
        raise RuntimeError('Boundary-month purge approval must be recorded before preregistration')
    path = P.OUT / 'prereg_v0.json'
    record = {'utc': utc_now(), 'params_sha256': sha256(P.ROOT / 'params.py'),
              'input_archive_sha256': sha256(P.SOURCE_ARCHIVE),
              'notes': P.PREREG_NOTES, 'python': platform.python_version(),
              'selection_end': P.SELECTION_END, 'first_sealed_decision': P.FIRST_SEALED_DECISION}
    if record['input_archive_sha256'] != P.SOURCE_SHA256:
        raise RuntimeError('Provided source archive changed')
    if path.exists():
        old = json.loads(path.read_text())
        previous_hash, parameter_hash = sha256(path), old['params_sha256']
        amendments = sorted((P.OUT/'prereg_amendments').glob('*.json'))
        if amendments:
            original_snapshot = P.OUT/'prereg/params_v0.py'
            if not original_snapshot.is_file() or sha256(original_snapshot)!=parameter_hash:
                raise RuntimeError('Original parameter snapshot differs from preregistration')
        for amendment_path in amendments:
            amendment = json.loads(amendment_path.read_text())
            snapshot = P.ROOT/amendment['params_snapshot']
            if (amendment.get('approved') is not True or not amendment.get('user_approval')
                    or amendment.get('previous_record_sha256') != previous_hash
                    or amendment.get('previous_params_sha256') != parameter_hash
                    or not snapshot.is_file() or sha256(snapshot) != amendment.get('params_sha256')):
                raise RuntimeError('Preregistration amendment chain is invalid')
            previous_hash, parameter_hash = sha256(amendment_path), amendment['params_sha256']
        if parameter_hash != record['params_sha256']:
            raise RuntimeError('Parameters differ from preregistration; record and review the deviation')
        return old
    write_json(path, record, exclusive=True)
    return record


def prepare_inputs(refresh_french=True):
    stage0()
    prefix = '230GA_Project_Data/'
    inventory = []
    with zipfile.ZipFile(P.SOURCE_ARCHIVE) as archive:
        for name in archive.namelist():
            relative = name.removeprefix(prefix)
            if name.endswith('/') or not name.startswith(prefix):
                continue
            if not (relative.startswith(('3_fred_latest/','4_alfred_vintages/','2_definitions/')) or relative in {'series_list.csv','vintage_audit.csv'}):
                continue
            dest = P.CACHE / 'provided' / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            payload = archive.read(name)
            digest = hashlib.sha256(payload).hexdigest()
            if dest.exists() and sha256(dest) != digest:
                raise RuntimeError('Cached source differs from provided archive')
            if not dest.exists():
                dest.write_bytes(payload)
            inventory.append({'file': str(dest.relative_to(P.ROOT)), 'sha256': digest, 'source': 'provided archive'})
    for name, url in P.PUBLIC_URLS.items():
        dest = P.CACHE / 'french' / (name + '.zip')
        if not dest.exists():
            if not refresh_french:
                raise FileNotFoundError(f'Missing pinned French input: {name}')
            response = requests.get(url, timeout=(15,90))
            response.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
                if archive.testzip() is not None:
                    raise ValueError('Corrupt French ZIP')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(response.content)
            append_event('downloads.jsonl', {'source': url, 'file': str(dest.relative_to(P.ROOT)), 'bytes': len(response.content), 'sha256': sha256(dest)})
        inventory.append({'file': str(dest.relative_to(P.ROOT)), 'sha256': sha256(dest), 'source': url})
    target = P.OUT / 'input_hashes.json'
    if target.exists() and json.loads(target.read_text()) != inventory:
        raise RuntimeError('Pinned input inventory differs; preserve both versions before proceeding')
    if not target.exists():
        write_json(target, inventory, exclusive=True)
    return inventory


def fred_metadata_audit(api_key=None):
    """Optional live first-vintage confirmation; key is never logged or cached."""
    key = api_key or os.environ.get('FRED_API_KEY')
    if not key:
        raise RuntimeError('FRED_API_KEY is not configured locally; cached audit remains separately labeled')
    records = []
    for sid in sorted(series_map().series_id.unique()):
        cache = P.CACHE / 'fred_metadata' / (sid + '.json')
        if not cache.exists():
            try:
                response = requests.get('https://api.stlouisfed.org/fred/series/vintagedates',
                                        params={'series_id': sid, 'api_key': key, 'file_type': 'json', 'sort_order': 'asc', 'limit': 1}, timeout=(15,60))
            except requests.RequestException:
                raise RuntimeError('FRED transport failure; credential-bearing request details withheld') from None
            if response.status_code != 200:
                raise RuntimeError(f'FRED request failed with HTTP {response.status_code}; request details withheld')
            try:
                payload = response.json()
            except ValueError:
                raise RuntimeError('FRED returned invalid JSON; request details withheld') from None
            if len(payload.get('vintage_dates',[])) != 1:
                raise RuntimeError('FRED returned no first-vintage date')
            write_json(cache, {'series_id': sid, 'vintage_dates': payload.get('vintage_dates',[]), 'retrieved_at': utc_now()})
            time.sleep(0.6)
        records.append(json.loads(cache.read_text()))
    write_json(P.OUT / 'live_vintage_confirmation.json', records)
    return records


def series_map():
    rows = []
    for group, name, jolts, members, ces, quality in P.GROUPS:
        for measure in P.MEASURES:
            rows.append({'group': group, 'series_id': f'JTU{jolts}{measure}', 'measure': measure, 'family': 'JOLTS', 'lag': 2, 'match': 'exact'})
        for suffix, measure in [('07','H'),('08','E')]:
            sid = f'CEU{ces}{suffix}'
            if group == 2 and measure == 'E':
                sid = 'CES2000000008'
            rows.append({'group': group, 'series_id': sid, 'measure': measure, 'family': 'CES', 'lag': 1, 'match': quality})
    for sid in ['JTSJOL','UNEMPLOY']:
        rows.append({'group': 0, 'series_id': sid, 'measure': sid, 'family': 'JOLTS' if sid == 'JTSJOL' else 'CPS', 'lag': 2 if sid == 'JTSJOL' else 1, 'match': 'national'})
    return pd.DataFrame(rows)


def read_vintage(sid):
    frame = pd.read_csv(P.CACHE / 'provided' / '4_alfred_vintages' / f'{sid}.csv', dtype=str)
    needed = {'date','realtime_start','realtime_end','value'}
    if set(frame) != needed or frame.duplicated(['date','realtime_start']).any():
        raise ValueError('Unexpected vintage schema or duplicate keys')
    frame = frame.assign(value=pd.to_numeric(frame.value.replace('.',np.nan), errors='raise'),
                         observation_month=pd.PeriodIndex(frame.date, freq='M'))
    dates = frame[['date','realtime_start','realtime_end']]
    for column in dates:
        if not dates[column].str.fullmatch(r'\d{4}-\d{2}-\d{2}',na=False).all():
            raise ValueError('Vintage dates must be ISO calendar dates')
        for value in dates[column].unique():
            datetime.strptime(value,'%Y-%m-%d')
    ordered = frame.sort_values(['observation_month','realtime_start'])
    next_start = ordered.groupby('observation_month').realtime_start.shift(-1)
    if (ordered.realtime_end<ordered.realtime_start).any() or (next_start.notna()&(ordered.realtime_end>=next_start)).any():
        raise ValueError('Reversed or overlapping vintage intervals')
    return frame.sort_values(['observation_month','realtime_start'])


def vintage_view(frame, cutoff, first=False):
    cutoff = pd.Timestamp(cutoff).strftime('%Y-%m-%d')
    if first:
        eligible = frame.drop_duplicates('observation_month',keep='first')
        eligible = eligible.loc[eligible.realtime_start <= cutoff]
    else:
        eligible = frame.loc[(frame.realtime_start <= cutoff) & (frame.realtime_end >= cutoff)]
    if eligible.duplicated('observation_month').any():
        raise ValueError('Overlapping vintage intervals')
    return eligible.set_index('observation_month')[['value','realtime_start']].sort_index()


def month_end_decisions(start, end):
    """NYSE month ends for this study, not a general daily exchange calendar.

    Only Good Friday and Memorial Day can displace a weekday month end in
    2002-2026. NYSE does not observe Saturday New Year on December 31.
    """
    months = pd.period_range(start,end,freq='M')
    if len(months) and (months[0].year < 2002 or months[-1].year > 2026):
        raise ValueError('Month-end calendar is verified only for 2002-2026')
    holidays = set(GoodFriday.dates('2002-01-01','2026-12-31')) | set(USMemorialDay.dates('2002-01-01','2026-12-31'))
    result = []
    for month in months:
        day = month.end_time.normalize()
        while day.weekday() >= 5 or day in holidays:
            day -= pd.Timedelta(days=1)
        result.append(day)
    return pd.DatetimeIndex(result, name='decision')


def build_asof_panel(variant='ASOF'):
    if variant not in P.VARIANTS:
        raise ValueError('Unknown variant')
    mapping = series_map().drop_duplicates('series_id')
    decisions = month_end_decisions(P.FEATURE_START, str(pd.Period(P.LAST_RETURN)-1))
    rows = []
    for item in mapping.itertuples():
        history = read_vintage(item.series_id)
        latest = history.drop_duplicates('observation_month',keep='last').set_index('observation_month')[['value','realtime_start']]
        snapshot = vintage_view(history,P.RESEARCH_SNAPSHOT)
        for decision in decisions:
            cutoff = decision - pd.Timedelta(days=1)
            research = decision < pd.Timestamp(P.FIRST_SEALED_DECISION)
            if research:
                view = snapshot
                bound = decision.to_period('M') - item.lag
                label = 'frozen_snapshot_fixed_lag'
            elif variant == 'REVISED':
                view = latest
                actual = vintage_view(history,cutoff).dropna(subset=['value'])
                bound = actual.index.max() if len(actual) else decision.to_period('M')-item.lag
                label = 'hindsight'
            elif variant == 'FIXEDLAG':
                view = latest
                bound = decision.to_period('M')-item.lag
                label = 'fixed_lag_revised'
            else:
                view = vintage_view(history,cutoff,first=variant=='FIRST')
                bound = decision.to_period('M')-1
                label = 'as_known' if variant=='ASOF' else 'first_release'
            view = view.loc[(view.index >= pd.Period('2000-12')) & (view.index <= bound)]
            for observation, value, release in view.reset_index().itertuples(index=False,name=None):
                rows.append((decision,item.series_id,str(observation),value,release,variant,label,str(cutoff.date())))
    result = pd.DataFrame(rows,columns=['decision','series_id','observation_month','value','release_date','variant','timing','cutoff'])
    known = result.timing.isin(['as_known','first_release'])
    assert (result.loc[known,'release_date'] <= result.loc[known,'cutoff']).all()
    research = result.timing.eq('frozen_snapshot_fixed_lag')
    assert (result.loc[research,'release_date'] <= P.RESEARCH_SNAPSHOT).all()
    path = P.OUT / f'panel_{variant.lower()}.parquet'
    path.parent.mkdir(parents=True,exist_ok=True)
    result.to_parquet(path,index=False)
    return result


def _avg3(series, month):
    values = series.reindex(pd.period_range(month-2,month,freq='M'))
    return float(values.mean()) if values.notna().all() else np.nan


def standardize(raw):
    sigma = raw.expanding(min_periods=P.MODEL['standardization_min_months']).std(ddof=P.MODEL['ddof']).replace(0,np.nan)
    scaled = raw / sigma
    row_sd = scaled.std(axis=1,ddof=1).replace(0,np.nan)
    result = scaled.sub(scaled.mean(axis=1),axis=0).div(row_sd,axis=0).clip(-P.MODEL['winsor_limit'],P.MODEL['winsor_limit'])
    # Do not turn early warm-up into a usable all-zero signal.
    ready = np.isfinite(scaled).sum(axis=1) >= min(len(raw.columns),P.GATE_CONSTANTS['minimum_groups_measure'])
    result.loc[ready] = result.loc[ready].fillna(0)
    result.loc[~ready] = np.nan
    return result, scaled.isna()


def build_features(panel):
    rows, tightness_rows, level_rows = [], [], []
    mapping = series_map()
    for decision, current in panel.groupby('decision',sort=True):
        source = {sid: pd.Series(f.value.to_numpy(),index=pd.PeriodIndex(f.observation_month,freq='M')).sort_index()
                  for sid,f in current.groupby('series_id')}
        by_group = {}
        for group, meta in mapping.loc[mapping.group>0].groupby('group'):
            by_group[group] = {r.measure: source[r.series_id] for r in meta.itertuples()}
        j = pd.concat([v[m] for v in by_group.values() for m in P.MEASURES],axis=1)
        counts = pd.DataFrame({measure:pd.concat([v[measure] for v in by_group.values()],axis=1).notna().sum(axis=1) for measure in P.MEASURES})
        available = (counts >= P.GATE_CONSTANTS['minimum_groups_measure']).all(axis=1)
        m_j = j.index[available].max() if available.any() else None
        h = pd.concat([v['H'] for v in by_group.values()],axis=1)
        available = h.notna().sum(axis=1) >= P.GATE_CONSTANTS['minimum_groups_measure']
        m_c = h.index[available].max() if available.any() else None
        for group, values in by_group.items():
            for measure in P.AGENT['leaf_inputs']:
                reference = m_j if measure in P.MEASURES else m_c
                level_rows.append((decision,group,measure,values[measure].get(reference,np.nan)))
            for idx, measure in enumerate(P.MEASURES,1):
                value = _avg3(values[measure],m_j)-_avg3(values[measure],m_j-12) if m_j is not None else np.nan
                rows.append((decision,group,f'F{idx}',value,str(m_j)))
            a,b = (_avg3(values['H'],m_c),_avg3(values['H'],m_c-12)) if m_c is not None else (np.nan,np.nan)
            rows.append((decision,group,'F5',np.log(a/b) if a>0 and b>0 else np.nan,str(m_c)))
        national = pd.concat([source['JTSJOL'],source['UNEMPLOY']],axis=1,keys=['v','u']).dropna()
        national = national.loc[(national.v>0)&(national.u>0)]
        if len(national):
            last = national.iloc[-1]
            tightness_rows.append((decision,np.log(last.v/last.u),str(national.index[-1])))
        else:
            tightness_rows.append((decision,np.nan,None))
    raw = pd.DataFrame(rows,columns=['decision','group','feature','raw_value','reference_month'])
    frames = []
    for name, values in raw.groupby('feature'):
        wide = values.pivot(index='decision',columns='group',values='raw_value')
        standardized, missing = standardize(wide)
        result = standardized.stack(future_stack=True).rename('value').reset_index()
        result = result.assign(feature=name,missing_before_imputation=missing.stack(future_stack=True).to_numpy())
        frames.append(result)
    features = pd.concat(frames).merge(raw,on=['decision','group','feature'],validate='one_to_one')
    features = features.assign(variant=panel.variant.iloc[0])
    features.to_parquet(P.OUT/f'features_{features.variant.iloc[0].lower()}.parquet',index=False)
    tightness = pd.DataFrame(tightness_rows,columns=['decision','T','reference_month']).set_index('decision')
    tightness = tightness.assign(staleness_months=[d.to_period('M').ordinal-pd.Period(m).ordinal if m else np.nan for d,m in zip(tightness.index,tightness.reference_month)])
    tightness.to_parquet(P.OUT/f'tightness_{panel.variant.iloc[0].lower()}.parquet')
    pd.DataFrame(level_rows,columns=['decision','group','variable','value']).to_parquet(P.OUT/f'levels_{panel.variant.iloc[0].lower()}.parquet',index=False)
    return features,tightness


def crosswalk():
    """Distinguish prescribed labels from verified SIC basket scope."""
    result = pd.DataFrame(P.GROUPS, columns=['group','name','JOLTS_code','French_members','CES_code','prescribed_match'])
    check = json.loads((P.OUT/'census_crosswalk_check.json').read_text())
    scopes = pd.DataFrame(check['groups'])[['group','assessment','outside_scope_rows','correspondence_rows']]
    if set(scopes.group)!=set(result.group) or scopes.group.duplicated().any():
        raise ValueError('Census scope audit does not cover the fixed group crosswalk')
    result = result.merge(scopes,on='group',validate='one_to_one')
    result = result.rename(columns={'assessment':'verified_French_scope'})
    result.to_csv(P.OUT/'crosswalk.csv',index=False)
    return result


def manifest():
    mapping = series_map()
    confirmation = P.OUT/'live_vintage_confirmation.json'
    live = {}
    if confirmation.exists():
        audit = json.loads(confirmation.read_text())
        live = {r['series_id']:r['vintage_dates'][0] for r in audit}
        if len(live)!=len(audit) or set(live)!=set(mapping.series_id):
            raise ValueError('Live vintage confirmation does not cover the exact core series')
    records = []
    for item in mapping.itertuples():
        history = read_vintage(item.series_id)
        first = history.realtime_start.min()
        if live and live[item.series_id]!=first:
            raise ValueError('Live first-vintage metadata differs from the pinned archive; resolve before proceeding')
        records.append({'source': 'FRED/ALFRED provided archive', 'id': item.series_id,
                        'url': f'https://fred.stlouisfed.org/series/{item.series_id}',
                        'group': item.group,'measure': item.measure,'frequency': 'monthly',
                        'observation_start': history.date.min(),'observation_end': history.date.max(),
                        'first_vintage': first,'admitted': first<=P.VINTAGE_ADMISSION,
                        'reason': 'cached vintage audit; live first-vintage date confirmed' if live else 'cached vintage audit; live metadata confirmation separately tracked',
                        'mapping_quality': item.match,
                        'flags': 'seasonally adjusted construction earnings exception' if item.series_id=='CES2000000008'
                                 else 'shared CES' if item.family=='CES' and item.group in [9,10] else ''})
    records.extend({'source':name,'id':name,'admitted':r['admitted'],'reason':r['reason']} for name,r in P.OPTIONAL_ADMISSION.items())
    for name,url in P.PUBLIC_URLS.items():
        months = []
        with zipfile.ZipFile(P.CACHE/'french'/(name+'.zip')) as archive:
            for member in archive.namelist():
                if member.lower().endswith(('.csv','.txt')):
                    with archive.open(member) as stream:
                        for line in stream:
                            # Inspect only the date field, never sealed numeric return cells.
                            date = line.split(b',',1)[0].strip()
                            if re.fullmatch(rb'\d{6}',date):
                                months.append(pd.Period(date.decode('ascii'),freq='M'))
        if not months or max(months)!=pd.Period(P.LAST_RETURN,freq='M'):
            raise ValueError('French manifest endpoint differs from the registered endpoint')
        records.append({'source':'Ken French data library','id':name,'url':url,'frequency':'monthly',
                        'observation_start':str(min(months)),'observation_end':str(max(months)),
                        'admitted':True,'reason':'Pinned official archive; date fields checked without parsing return values',
                        'mapping_quality':'fixed prescribed French membership','flags':'research portfolios are not directly tradable'})
    records.extend({'source':'Ken French excluded portfolio','id':name,'url':P.PUBLIC_URLS['industry'],
                    'admitted':False,'reason':reason} for name,reason in P.EXCLUDED_FRENCH.items())
    for name,url in [('Siccodes49.txt','https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes49.zip'),
                     ('1987_SIC_to_2002_NAICS.xls','https://www.census.gov/naics/concordances/1987_SIC_to_2002_NAICS.xls')]:
        path = P.CACHE/'provided/2_definitions'/name
        if not path.is_file():
            raise FileNotFoundError('Missing prescribed crosswalk documentation')
        records.append({'source':'Provided crosswalk documentation','id':name,'url':url,
                        'frequency':'static','admitted':True,'reason':'Documentation only; pinned source archive',
                        'flags':'Does not imply exact economic scope for approximate groups'})
    result = pd.DataFrame(records)
    result.to_csv(P.OUT/'manifest.csv',index=False)
    return result


def _french_tables(name, cap, capability=None):
    if not (P.OUT/'prereg_v0.json').exists():
        raise RuntimeError('Preregistration required before parsing returns')
    if cap > pd.Period(P.SELECTION_END) and capability is not _SEALED_CAPABILITY:
        raise PermissionError('Sealed numeric returns are only available inside final_evaluation')
    path = P.CACHE/'french'/f'{name}.zip'
    tables, title, header, rows = {}, '', None, []
    def finish():
        nonlocal rows
        if rows and header:
            key = title or 'monthly'
            if key not in tables:
                frame = pd.DataFrame(rows,columns=['month']+header)
                frame = frame.assign(month=pd.PeriodIndex(frame.month,freq='M'))
                tables[key] = frame.set_index('month').replace([-99.99,-999.0],np.nan)
        rows = []
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith('.csv')]
        if len(names)!=1:
            raise ValueError('Expected one French CSV')
        with archive.open(names[0]) as stream:
            for binary in stream:
                line = binary.decode('utf-8-sig').strip()
                first = line.partition(',')[0].strip()
                if re.fullmatch(r'\d{6}',first):
                    month = pd.Period(first[:4]+'-'+first[4:],freq='M')
                    # Skip before numeric parsing, including every sealed observation.
                    if month <= cap and header:
                        cells = next(csv.reader([line]))
                        if len(cells)-1 != len(header):
                            raise ValueError('French header/data width mismatch')
                        rows.append([str(month)]+[float(c.strip()) for c in cells[1:]])
                elif not line:
                    finish()
                elif first == '' and ',' in line:
                    finish()
                    header = [c.strip() for c in next(csv.reader([line]))[1:]]
                elif not re.fullmatch(r'\d{4}|\d{8}',first):
                    finish()
                    if line.startswith(('Average','Number of Firms')):
                        title = line
                    elif 'annual' in line.lower() or 'daily' in line.lower():
                        title,header = line,None
    finish()
    return tables


def read_returns(cap=None, capability=None):
    cap = pd.Period(cap or P.SELECTION_END,freq='M')
    if cap > pd.Period(P.SELECTION_END) and capability is not _SEALED_CAPABILITY:
        raise PermissionError('Sealed return access denied')
    stage0()
    append_event('return_access.jsonl',{'cap':str(cap),'scope':'sealed' if cap>pd.Period(P.SELECTION_END) else 'research'})
    tables = _french_tables('industry',cap,capability)
    def pick(text):
        matches = [v for k,v in tables.items() if text.lower() in k.lower()]
        if len(matches)!=1:
            raise ValueError(f'Expected exactly one French section: {text}')
        return matches[0]
    returns = pick('Average Value Weighted Returns -- Monthly')/100
    caps = pick('Number of Firms')*pick('Average Firm Size')
    weights = caps.shift(1)
    grouped = {}
    for group,_,_,members,_,_ in P.GROUPS:
        members = members.split()
        valid = returns[members].notna().all(axis=1)&weights[members].notna().all(axis=1)&(weights[members]>=0).all(axis=1)
        value = (returns[members]*weights[members]).sum(axis=1)/weights[members].sum(axis=1).replace(0,np.nan)
        grouped[group] = value.where(valid)
    total = pd.DataFrame(grouped)
    ff_tables = _french_tables('ff5',cap,capability)
    mom_tables = _french_tables('momentum',cap,capability)
    ff = next(iter(ff_tables.values()))/100
    mom = next(iter(mom_tables.values()))/100
    mom.columns = ['Mom' if c.lower().strip() in ['mom','mom   '] else c for c in mom.columns]
    factors = ff.join(mom,how='inner')
    common = pd.period_range(max(total.index.min(),factors.index.min()),cap,freq='M')
    total, factors = total.reindex(common),factors.reindex(common)
    if total.index.max() < cap:
        raise ValueError('Requested return endpoint is not present')
    required = pd.period_range(pd.Period(P.RESEARCH_START)-P.PORTFOLIO['risk_window']-2,cap,freq='M')
    required_factors = ['Mkt-RF','SMB','HML','RMW','CMA','RF','Mom']
    if not set(required_factors).issubset(factors) or not np.isfinite(factors.reindex(required)[required_factors]).all().all():
        raise ValueError('Missing required factor columns or months')
    if not np.isfinite(total.reindex(required)).all().all():
        raise ValueError('Missing group return or month; universe must remain complete')
    excess = total.sub(factors.RF,axis=0)
    return {'total':total,'excess':excess,'relative':excess.sub(excess.mean(axis=1),axis=0),'factors':factors}


def verify_freeze():
    path = P.OUT/'FREEZE.json'
    if not path.exists():
        raise PermissionError('No complete freeze exists')
    record = json.loads(path.read_text())
    mandatory = {'params.py','data.py','stats.py','agents.py','outputs/selected_features.json',
                 'outputs/input_hashes.json','outputs/prereg_v0.json','outputs/readiness.json',
                 'outputs/agents/transport_attestation.json','outputs/agents/log.jsonl','outputs/capacity_review.json'}
    mandatory |= {'outputs/blind_map.json','outputs/agents/dictionary.json','outputs/runtime.json'}
    if P.AGENT.get('transport') == 'claude_subscription':
        mandatory |= {'outputs/prereg_amendments/001_claude_subscription.json',
                      'outputs/prereg/params_v0.py','outputs/prereg/params_v1.py'}
    mandatory |= {f'outputs/{kind}_{variant.lower()}.parquet' for kind in ['panel','features','levels','tightness'] for variant in P.VARIANTS}
    if not mandatory.issubset(record.get('hashes',{})):
        raise PermissionError('Incomplete freeze: required artifact hashes missing')
    if record.get('notebook_source_sha256')!=notebook_source_hash():
        raise PermissionError('Notebook source changed after freeze')
    inventory = json.loads((P.OUT/'input_hashes.json').read_text())
    if any(record['hashes'].get(row['file'])!=row['sha256'] for row in inventory):
        raise PermissionError('Freeze does not pin every input')
    for relative,digest in record['hashes'].items():
        if sha256(P.ROOT/relative)!=digest:
            raise PermissionError('A frozen code/data artifact changed')
    return record


def audit_prepared_data():
    """Verify pinned bytes, schemas, publication bounds and the fixed group grid."""
    input_hashes = json.loads((P.OUT/'input_hashes.json').read_text())
    for row in input_hashes:
        if sha256(P.ROOT/row['file'])!=row['sha256']:
            raise ValueError('Pinned input changed')
    rows = []
    lag = series_map().drop_duplicates('series_id').set_index('series_id').lag
    expected = month_end_decisions(P.FEATURE_START,str(pd.Period(P.LAST_RETURN)-1))
    evidence = {}
    for variant in P.VARIANTS:
        name = variant.lower()
        panel = pd.read_parquet(P.OUT/f'panel_{name}.parquet')
        if panel.duplicated(['decision','series_id','observation_month']).any() or panel.series_id.nunique()!=len(lag):
            raise ValueError('Panel key or series coverage failure')
        if not pd.DatetimeIndex(sorted(panel.decision.unique())).equals(expected.rename(None)):
            raise ValueError('Panel decision grid differs')
        observation = pd.PeriodIndex(panel.observation_month,freq='M').asi8
        decision = pd.DatetimeIndex(panel.decision).to_period('M').asi8
        fixed = panel.timing.isin(['frozen_snapshot_fixed_lag','fixed_lag_revised']).to_numpy()
        allowed = decision-panel.series_id.map(lag).to_numpy()
        if not (observation[fixed]<=allowed[fixed]).all():
            raise ValueError('Fixed-lag observation bound violated')
        known = panel.timing.isin(['as_known','first_release']).to_numpy()
        if not (panel.loc[known,'release_date']<=panel.loc[known,'cutoff']).all() or not (observation[known]<=decision[known]-1).all():
            raise ValueError('Point-in-time cutoff violated')
        frozen = panel.timing.eq('frozen_snapshot_fixed_lag')
        if not (panel.loc[frozen,'release_date']<=P.RESEARCH_SNAPSHOT).all():
            raise ValueError('Research snapshot cutoff violated')
        features = pd.read_parquet(P.OUT/f'features_{name}.parquet')
        if features.duplicated(['decision','group','feature']).any() or len(features)!=len(expected)*len(P.GROUPS)*len(P.FEATURES):
            raise ValueError('Feature grid incomplete or duplicated')
        if not set(features.feature)==set(P.FEATURES) or not set(features.group)=={g[0] for g in P.GROUPS}:
            raise ValueError('Feature universe changed')
        used = features.loc[features.decision>=pd.Timestamp('2004-04-01')]
        if not np.isfinite(used.value).all():
            raise ValueError('Core features incomplete after required warm-up')
        rows.append({'variant':variant,'panel_rows':len(panel),'feature_rows':len(features),'decision_months':len(expected)})
        for kind in ['panel','features','levels','tightness']:
            relative = f'outputs/{kind}_{name}.parquet'
            evidence[relative] = sha256(P.ROOT/relative)
    result = {'passed':True,'utc':utc_now(),'variants':rows,'evidence_hashes':evidence,
              'open_flags':[],'scope':'Prepared public labor data, no return values'}
    write_json(P.OUT/'panel_audit.json',result)
    return result


def backtest(scores, returns, holding=None, cost_bps=None, borrow_bps=None, signal_available=None):
    """Trade fixed-membership tranches; estimate risk using full months <= m-2.

    Net is excess return. NAV used for drift earns RF plus net excess. Costs
    reduce NAV once. Industry legs and the funded market hedge use total
    returns for weight drift; the residual cash account earns RF.
    """
    holding = P.PORTFOLIO['holding'] if holding is None else holding
    cost_bps = P.PORTFOLIO['cost_bps'] if cost_bps is None else cost_bps
    borrow_bps = P.PORTFOLIO['borrow_finance_base_bps_year'] if borrow_bps is None else borrow_bps
    if not isinstance(scores.index,pd.PeriodIndex) or scores.index.has_duplicates:
        raise ValueError('Scores must use unique earning-month periods')
    if not scores.index.equals(pd.period_range(scores.index.min(),scores.index.max(),freq='M')):
        raise ValueError('Portfolio months must be consecutive')
    if signal_available is None:
        signal_available = pd.Series(True,index=scores.index)
    if not signal_available.index.equals(scores.index) or signal_available.isna().any():
        raise ValueError('Availability must cover the exact portfolio calendar')
    if not np.isfinite(scores.loc[signal_available]).all().all():
        raise ValueError('No missing scores permitted for an available signal')
    groups = scores.columns
    if len(groups)<6:
        raise ValueError('At least six groups required')
    tranches, ledger, weight_rows = [], [], []
    pretrade = pd.Series(0.,index=list(groups)+['market'])
    long_pretrade = pd.Series(0.,index=groups)
    long_tranches = []
    for month,score in scores.iterrows():
        tranche = pd.Series(0.,index=groups)
        if signal_available.loc[month]:
            rank = score.sort_index().sort_values(kind='stable')
            tranche.loc[rank.index[-P.PORTFOLIO['longs']:]] = 1/P.PORTFOLIO['longs']
            tranche.loc[rank.index[:P.PORTFOLIO['shorts']]] = -1/P.PORTFOLIO['shorts']
        tranches.append(tranche)
        book = sum(tranches[-holding:])/holding
        history_months = pd.period_range(month-P.PORTFOLIO['risk_window']-1,month-2,freq='M')
        historical = returns['excess'].reindex(index=history_months,columns=groups).join(returns['factors']['Mkt-RF']).dropna()
        if len(historical)<P.PORTFOLIO['risk_min_months']:
            raise ValueError('Insufficient prior risk history')
        market = historical['Mkt-RF'].to_numpy()
        variance = np.var(market,ddof=1)
        if variance<=0:
            raise ValueError('Degenerate market risk history')
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
        current = returns['total'].loc[month,groups]
        factors = returns['factors'].loc[month]
        if not np.isfinite(current).all() or not np.isfinite(factors).all():
            raise ValueError('Missing holding-period returns')
        turnover = float((weights[groups]-pretrade[groups]).abs().sum())
        hedge_turnover = abs(weights['market']-pretrade['market'])
        transaction = turnover*cost_bps/10000+hedge_turnover*P.PORTFOLIO['hedge_cost_bps']/10000
        # Charge borrowed securities plus negative residual cash, at the stated annual rate.
        borrow_base = -weights.clip(upper=0).sum()
        finance_base = max(0,float(weights.sum()-1))
        financing = (borrow_base+finance_base)*borrow_bps/10000/12
        gross = float(weights[groups]@returns['excess'].loc[month,groups]+weights['market']*factors['Mkt-RF'])
        net = gross-transaction-financing
        nav = 1+factors.RF+net
        if nav<=0:
            raise ValueError('Portfolio NAV is nonpositive')
        instrument_total = pd.concat([current,pd.Series({'market':factors['Mkt-RF']+factors.RF})])
        pretrade = weights*(1+instrument_total)/nav
        long_tranches.append(tranche.clip(lower=0))
        long_weights = sum(long_tranches[-holding:])/holding
        long_turnover = (long_weights-long_pretrade).abs().sum()
        long_excess = long_weights@returns['excess'].loc[month,groups]-long_turnover*cost_bps/10000
        long_nav = 1+factors.RF+long_excess
        if long_nav<=0:
            raise ValueError('Long-only NAV is nonpositive')
        long_pretrade = long_weights*(1+current)/long_nav
        ledger.append({'month':month,'gross':gross,'net':net,'turnover':turnover,'hedge_turnover':hedge_turnover,
                       'total_net':net+factors.RF,'risk_free':factors.RF,
                       'cost':transaction,'borrow_financing':financing,'borrow_base':borrow_base,'finance_base':finance_base,
                       'ex_ante_vol':risk*scale,'gross_leverage':weights.abs().sum(),'market_hedge':weights['market'],
                       'active':long_excess-returns['excess'].loc[month,groups].mean(), 'long_only_turnover':long_turnover})
        weight_rows.append(weights.rename(month))
    return pd.DataFrame(ledger).set_index('month'),pd.DataFrame(weight_rows)


def final_evaluation(evaluator, reason=None):
    """Only this boundary can load sealed numeric returns, once per frozen run."""
    record = verify_freeze()
    marker = P.OUT/'evaluation_started.json'
    if marker.exists():
        if not reason or not reason.strip():
            raise PermissionError('Sealed evaluation was already started; written rerun reason required')
        append_event('reruns.log',{'reason':reason,'previous_start':json.loads(marker.read_text())})
        run_id = 'rerun_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    else:
        write_json(marker,{'utc':utc_now(),'freeze_sha256':sha256(P.OUT/'FREEZE.json')},exclusive=True)
        run_id = 'initial'
    returns = read_returns(P.LAST_RETURN,capability=_SEALED_CAPABILITY)
    result = evaluator(returns,record,run_id)
    write_json(P.OUT/f'evaluation_completed_{run_id}.json',{'utc':utc_now(),'run_id':run_id})
    return result


def self_test():
    fixture = pd.DataFrame({'date':['2010-01-01']*2,'observation_month':pd.PeriodIndex(['2010-01']*2,freq='M'),
                            'realtime_start':['2010-02-01','2010-03-01'],'realtime_end':['2010-02-28','9999-12-31'],'value':[1.,9.]})
    assert vintage_view(fixture,'2010-02-28').value.iloc[0]==1
    assert vintage_view(fixture,'2010-03-01',first=True).value.iloc[0]==1
    assert vintage_view(fixture,'2010-03-01').value.iloc[0]==9
    assert str(month_end_decisions('2024-03','2024-03')[0].date())=='2024-03-28'
    assert str(month_end_decisions('2021-12','2021-12')[0].date())=='2021-12-31'
    assert str(month_end_decisions('2021-05','2021-05')[0].date())=='2021-05-28'
    assert len(month_end_decisions('2014-10','2026-07'))==142
    rng = np.random.default_rng(P.SEED)
    sample = pd.DataFrame(rng.normal(size=(40,13)))
    sample.iloc[-1] = np.nan
    assert standardize(sample)[0].iloc[-1].isna().all()
    months = pd.period_range('2000-01',periods=100,freq='M')
    market = pd.Series(rng.normal(.005,.04,100),index=months)
    total = pd.DataFrame(rng.normal(.005,.03,(100,6))+market.to_numpy()[:,None],index=months)
    factors = pd.DataFrame({'Mkt-RF':market,'RF':.002},index=months)
    returns = {'total':total,'excess':total.sub(factors.RF,axis=0),'factors':factors}
    scores = pd.DataFrame([np.arange(6),-np.arange(6)],index=months[-2:],columns=total.columns)
    ledger,weights = backtest(scores,returns,holding=2)
    assert np.allclose(weights.iloc[1],0) and ledger.turnover.iloc[1]>0 and ledger.net.iloc[1]<0
    assert ledger.gross_leverage.iloc[0]<=P.PORTFOLIO['gross_cap']+1e-12
    single = backtest(scores.iloc[:1],returns,holding=1)[1]
    assert np.allclose(single.iloc[0],weights.iloc[0])
    first_total = pd.concat([total.iloc[-2],pd.Series({'market':factors['Mkt-RF'].iloc[-2]+.002})])
    drift = weights.iloc[0]*(1+first_total)/(1+ledger.total_net.iloc[0])
    assert np.isclose(ledger.turnover.iloc[1],drift[total.columns].abs().sum())
    expected_cost = ledger.turnover.iloc[1]*P.PORTFOLIO['cost_bps']/10000+abs(drift['market'])*P.PORTFOLIO['hedge_cost_bps']/10000
    assert np.isclose(ledger.cost.iloc[1],expected_cost)
    perturbed = {k:v.copy() for k,v in returns.items()}
    perturbed['excess'].iloc[-3] += 100
    unchanged = backtest(scores.iloc[:1],perturbed,holding=2)[1]
    assert np.allclose(unchanged.iloc[0],weights.iloc[0])
    try:
        verify_freeze()
    except PermissionError:
        pass
    else:
        raise AssertionError('Synthetic readiness test expects the seal still closed')
    return {'vintage_cutoffs':'passed','month_end_calendar':'passed','sealed_month_count':142,'seal_closed':'passed',
            'missing_coverage':'passed','zero_book_liquidation':'passed','drift_costs':'passed','risk_information_cutoff':'passed'}
