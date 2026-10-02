"""Figures and a report assembled only from saved results."""
import json
import html
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import params as P
import data as D


def save(fig, name, directory=None):
    directory = directory or P.OUT/'figures'
    directory.mkdir(parents=True,exist_ok=True)
    fig.tight_layout()
    for extension in ['png','pdf']:
        path = directory/f'{name}.{extension}'
        fig.savefig(path,dpi=160,bbox_inches='tight')
        D.append_event('figures.jsonl',{'file':str(path.relative_to(P.ROOT)),'sha256':D.sha256(path)})
    plt.close(fig)


def design_figures():
    fig,ax = plt.subplots(figsize=(10,2.5))
    labels = ['Pin inputs\nAudit timing','Build as-of\nfeatures','Blind research\nCompare searches','Freeze choices\nand code','Open sealed test\nReport all gates']
    for i,label in enumerate(labels):
        ax.text(i,.5,label,ha='center',va='center',bbox={'boxstyle':'round,pad=.5','facecolor':'#e8f0f8','edgecolor':'#3a607d'})
        if i<4: ax.annotate('',xy=(i+.69,.5),xytext=(i+.31,.5),arrowprops={'arrowstyle':'->'})
    ax.set(xlim=(-.5,4.5),ylim=(0,1),title='Follow the Workers: preregistered sequence')
    ax.axis('off')
    save(fig,'01_pipeline')
    fig,ax = plt.subplots(figsize=(10,2.8))
    start,end = pd.Timestamp('2004-05-01'),pd.Timestamp('2026-09-01')
    boundary = pd.Timestamp('2014-11-01')
    purge = pd.Timestamp('2014-10-01')
    ax.axvspan(start,purge,color='#acc9e1',label='Selection: 125 months')
    ax.axvspan(purge,boundary,color='#c79644',label='Boundary purge: October 2014')
    ax.axvspan(boundary,end,color='#aed8bd',label='Sealed: 142 months')
    ax.axvspan(pd.Timestamp('2025-03-01'),end,color='#559f72',label='Last 18 months')
    ax.set(xlim=(start,end),yticks=[],title='Return months; first sealed decision October 31, 2014')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.22),ncol=2,frameon=False)
    save(fig,'02_sample_split')


def result_figures(run_id='initial'):
    directory = P.OUT/'sealed'/run_id
    result = json.loads((directory/'results.json').read_text())
    figures = directory/'figures'
    def plotted(value):
        return np.nan if value is None else value
    names = list(result['variants']['ASOF'])
    ledgers = {name:pd.read_csv(directory/f'ASOF_{name}_ledger.csv',index_col=0) for name in names}
    fig,ax = plt.subplots(figsize=(9,4))
    for name,frame in ledgers.items(): ax.plot(pd.to_datetime(frame.index), (1+frame.net).cumprod()-1,label=name)
    ax.set(title='Compounded net excess returns',ylabel='Cumulative excess-return index minus one')
    ax.legend(ncol=3)
    save(fig,'03_cumulative_net',figures)
    fig,ax = plt.subplots(figsize=(8,4))
    for i,name in enumerate(names):
        rows = result['variants']['ASOF'][name]['IC']
        x = np.array(P.INFERENCE['horizons'])+(i-len(names)/2)*.06
        y = [rows[str(h)]['mean'] for h in P.INFERENCE['horizons']]
        error = [1.96*rows[str(h)]['se'] for h in P.INFERENCE['horizons']]
        ax.errorbar(x,y,yerr=error,marker='o',capsize=3,label=name)
    ax.axhline(0,color='grey',lw=.7)
    ax.set(xticks=P.INFERENCE['horizons'],xlabel='Horizon (months)',ylabel='Rank IC',title='IC with 95% HAC intervals')
    ax.legend()
    save(fig,'04_ic_horizons',figures)
    fig,ax = plt.subplots(figsize=(8,4))
    for name in names:
        ax.plot(['low','middle','high'],[result['windows'][name]['T_'+r]['IC']['mean'] for r in ['low','middle','high']],marker='o',label=name)
    ax.set(title='IC by expanding tightness tercile',ylabel='Mean monthly rank IC')
    ax.legend()
    save(fig,'05_ic_tightness',figures)
    fig,ax = plt.subplots(figsize=(8,4))
    gap = [result['variants']['ASOF'][n]['IC']['1']['mean']-result['variants']['REVISED'][n]['IC']['1']['mean'] for n in names]
    ax.bar(names,gap)
    ax.set(title='As-known minus revised IC',ylabel='Mean monthly rank IC difference')
    save(fig,'06_revision_gap',figures)
    fig,ax = plt.subplots(figsize=(8,4))
    ax.hist([x['mean_ic'] for x in result['placebo']['shifts']],bins=15,color='#3a607d')
    primary = result['gate']['primary']
    ax.axvline(result['variants']['ASOF'][primary]['IC']['1']['mean'],color='#b14a31',label='Observed')
    ax.set(title=f"Circular-shift placebo; p={result['placebo']['p']:.3f}",xlabel='Mean rank IC',ylabel='Shifts')
    ax.legend()
    save(fig,'07_placebo',figures)
    process = pd.read_csv(P.OUT/'agents/process_metrics.csv')
    fig,ax = plt.subplots(figsize=(8,4))
    for arm,frame in process.groupby('arm'):
        grouped = frame.groupby('submission').best_so_far_ic.agg(['mean','min','max'])
        ax.plot(grouped.index,grouped['mean'],label=arm)
        ax.fill_between(grouped.index,grouped['min'],grouped['max'],alpha=.2)
    ax.set(title='Search progress; mean and range across three runs',xlabel='Submission number',ylabel='Best-so-far research IC')
    ax.legend()
    save(fig,'08_search_progress',figures)
    migration = json.loads((P.OUT/'agents/migration_summary.json').read_text())
    fig,axes = plt.subplots(1,2,figsize=(9,4))
    axes[0].bar(['Claim uptake'],[plotted(migration['uptake_rate'])]); axes[0].set(ylim=(0,1),title='Migration claim uptake')
    axes[1].bar(['Uptake','No uptake'],[plotted(migration['improvement_with_uptake']),plotted(migration['improvement_without_uptake'])])
    if any(migration[k] is None for k in ['uptake_rate','improvement_with_uptake','improvement_without_uptake']):
        fig.text(.5,.02,'Missing bars: no defined observations in that category',ha='center',fontsize=9)
    axes[1].set(title='IC improvement over prior own best',ylabel='Research IC difference')
    save(fig,'09_migration',figures)
    fig,ax = plt.subplots(figsize=(6,5))
    valid = [r for r in result['candidate_accounting'] if 'sealed' in r]
    ax.scatter([r['research']['mean'] for r in valid],[r['sealed']['mean'] for r in valid])
    if not valid: ax.text(.5,.5,'No valid seed-1 candidates',transform=ax.transAxes,ha='center')
    ax.axhline(0,color='grey',lw=.7); ax.axvline(0,color='grey',lw=.7)
    ax.set(xlabel='Research mean IC',ylabel='Sealed mean IC',title='All valid seed-1 candidates')
    save(fig,'10_research_sealed',figures)
    fig,ax = plt.subplots(figsize=(9,4))
    attribution = result['attribution'][primary]
    labels = [key for key in attribution['coefficients'] if key!='intercept']
    ax.errorbar(labels,[attribution['coefficients'][k] for k in labels],yerr=[1.96*attribution['standard_errors'][k] for k in labels],fmt='o',capsize=3)
    ax.set(title=f'{primary}: factor loadings with HAC intervals',ylabel='Loading')
    save(fig,'11_factor_loadings',figures)
    fig,ax = plt.subplots(figsize=(9,4))
    for name,frame in ledgers.items():
        nav = (1+frame.total_net).cumprod()
        ax.plot(pd.to_datetime(frame.index),nav/nav.cummax().clip(lower=1)-1,label=name)
    ax.set(title='Funded account drawdowns',ylabel='Drawdown')
    ax.legend()
    save(fig,'12_drawdowns',figures)


def write_report(run_id='initial'):
    directory = P.OUT/'sealed'/run_id
    result = json.loads((directory/'results.json').read_text())
    research = json.loads((P.OUT/'research_summary.json').read_text())
    report = P.ROOT/'report'/run_id
    report.mkdir(parents=True,exist_ok=False)
    gate = result['gate']
    primary = gate['primary']
    selection = json.loads((P.OUT/'selected_features.json').read_text())
    blind = json.loads((P.OUT/'blind_map.json').read_text())
    def number(v): return 'unavailable' if v is None else f'{v:.3f}'
    text = f"# Follow the Workers\n\n## 1. Executive summary\n\n**{gate['verdict']}**. The prespecified primary is {primary}. Failed criteria: {', '.join(gate['failed']) or 'none'}. {gate['power']} This study separates public labor prediction, optional company data, and agent search behavior.\n\n"
    text += '## 2. What did you try\n\n### 2a. Ideas\n\nPredict next-month relative returns across 13 fixed industry groups using public labor changes. Compare independent and communicating agent searches with equal budgets; only seed 1 supplies strategy features.\n\n'
    text += '### 2b. Data\n\nFRED/ALFRED labor vintages and Ken French industry returns and factors, pinned by file hash. Research uses the October 30, 2014 snapshot with fixed publication lags. Sealed results use information available before each decision. Selection ends September 2014; October is purged. LinkUp and WARN failed timing/evidence gates and are excluded. F6 and A5 are omitted; Q2 cannot be answered with these inputs. See manifest.csv and deviations.md.\n\n'
    text += '### 2c. Implementation\n\nExpanding ridge fits require 36 fully available training months. Penalties are fixed using five chronological folds with a one-month purge. Portfolios rank the top and bottom three, average three monthly tranches, hedge lagged market beta, target 10% volatility and cap gross exposure at 2. Costs use drift-adjusted one-way turnover; industry trades cost 10 bp and market-hedge trades 2 bp. The registered volatility target and leverage cap also apply during startup.\n\n'
    text += '''The target is an industry's excess return less the equal-weight mean excess return of the fixed group universe. This focuses the prediction exercise on relative performance. National tightness is common to every group and cannot change a cross-sectional ranking on its own; it enters the interaction comparator, while the main public model answers the primary labor-information question. The fixed benchmark averages standardized openings, hires, negative layoffs and hours with signs specified before observing results.

Each industry return combines its assigned French portfolios using prior-month market capitalizations, computed as number of firms times average firm size. Missing required members or factors cause a validation failure rather than a smaller, changing universe. The French files are current historical research series. Their use does not establish point-in-time constituent availability or the tradability of an identical basket. Exact source bytes and observation endpoints are retained in the input inventory.

The labor pipeline distinguishes reference months from publication dates. A value observed for an earlier month is not usable merely because its reference month precedes the portfolio decision. ASOF uses the vintage interval in force by the previous calendar day. FIRST keeps the earliest archived vintage, which is not necessarily the original release for observations predating archive coverage. REVISED is a hindsight diagnostic and FIXEDLAG applies publication lags to revised values. Research history uses a single frozen snapshot with fixed lags, so it is explicitly pseudo-real-time. No later revision enters that research snapshot. National openings and unemployment use the latest jointly available reference month, with staleness recorded. Construction earnings use the prescribed seasonally adjusted exception, explicitly flagged in the manifest.

Public signals compare three-month averages with their year-earlier counterparts; hours use log growth. Each signal is divided by its own expanding historical standard deviation, then standardized across groups and winsorized. Insufficient current coverage does not become an apparently valid all-zero signal. Permitted missing groups are flagged before imputation. Shared series and broad supersector matches reduce the effective diversity of the information, even when the portfolio has distinct return columns.

Training labels obey the same timing rule as predictors. For a return earned in month m, the decision is at the previous month-end and the most recent fully available monthly return is m minus two. The October boundary return therefore cannot choose the first sealed portfolio's model, and the same restriction applies to its risk estimates. Cross-validation keeps entire months together and uses chronological training followed by purged validation blocks. Penalties and selected feature definitions remain fixed in the sealed test, while coefficients update using newly available historical labels.

Agent leaves are decision-time levels, evaluated privately; agents receive their anonymous dictionary, permitted operations and rounded development summaries. Temporal operators retain the information known at each previous decision rather than retrospectively revising the feature history. A whitelist parser rejects arbitrary code, arithmetic outside the grammar, negative lags and excess depth or variable counts. Constructed candidates receive the registered standardization. Missing candidate model inputs are zero-imputed with coverage reported separately; undefined candidate IC is never presented as zero.

Both search architectures receive equal submission budgets and starting emphases. Migration occurs only after all participating islands finish the designated submission, preventing an ordering advantage within a round. Invalid submissions consume their slots. Syntax repair is limited and is distinct from revising an invalid hypothesis. Only the first seed can contribute selected features; the remaining seeds characterize search variation. The engineer does not propose, manually edit or rank experimental candidates.

Portfolio membership stays fixed within each tranche. Each month's target combines the remaining tranches, estimates group market betas from prior returns, adds a market hedge and uses a joint covariance estimate for risk scaling. Both hedge exposure and industry exposure count toward the gross cap. Empty startup or abstention slots contribute zero tranches; the aggregate book is scaled to the registered volatility target subject to the leverage cap. If tranches cancel, the book can become flat and pays any required liquidation costs. Weight drift uses funded account returns, while performance Sharpe uses net excess returns.

Transaction charges are applied once to absolute changes from drifted pretrade weights. Industry and hedge rates are distinct, and borrow/financing sensitivities are reported separately. Candidate portfolio diagnostics use the common research comparison calendar; missing or constant signals create no new tranche while existing holdings age normally. The long-only comparator uses the same top-group membership against an equal-weight group benchmark. Its active return, tracking error and information ratio supplement the long–short results.

Monthly IC inference uses calendar-aware Newey–West errors. Overlapping horizons compound total returns before cross-sectional demeaning, with longer HAC lags. Paired comparisons resample the same calendar positions and center the null distribution; the prespecified inferential endpoints share a Holm adjustment. The reality-check diagnostic preserves the joint IC/missingness calendar, and unavailable full-family calculations are reported explicitly. Deflated Sharpe uses monthly units and the nominal search budget; neither diagnostic completely removes dependence or adaptive-search bias.

Before opening sealed returns, feature choices, code, inputs, review evidence and the implementation-capacity assessment are hashed. A start marker precedes the sealed read. Any later rerun needs a written reason and a separate output directory. Readiness rejects stale audit stamps whose underlying files changed. The notebook source is protected independently of execution outputs, while append-only operational logs remain available to document the run.

'''
    text += '## 3. What did you learn\n\n### 3a. Style and risk exposures\n\n| Strategy | Research Sharpe | Sealed Sharpe | Sealed IC | HAC t |\n|---|---:|---:|---:|---:|\n'
    for name,row in result['variants']['ASOF'].items():
        text += f"| {name} | {number(research['strategies'][name]['sharpe'])} | {number(row['sharpe'])} | {number(row['IC']['1']['mean'])} | {number(row['IC']['1']['t'])} |\n"
    text += f"\nPrimary factor alpha (monthly): {number(result['attribution'][primary]['mean'])}; HAC t: {number(result['attribution'][primary]['t'])}. See the saved factor table and figure.\n\n"
    text += '### 3b. Time patterns\n\nThe results file contains whole-period, half-period, pandemic-excluded, last-18-month and expanding-tightness-tercile results. Course-window series combine pseudo-real-time research and as-known sealed data and are descriptive.\n\n'
    text += '| Primary window | Months | Net Sharpe | Mean IC | HAC t |\n|---|---:|---:|---:|---:|\n'
    for label,row in result['windows'][primary].items():
        text += f"| {label} | {row['n']} | {number(row['sharpe'])} | {number(row['IC']['mean'])} | {number(row['IC']['t'])} |\n"
    text += '\nFunded drawdown is not computed for disconnected conditional months: concatenating isolated regimes would not describe a continuous account. The full and post-2010 windows state their actual first observation after model burn-in. Their research segment is descriptive because the same research sample supplied model choices. It is not additional sealed evidence.\n\n'
    text += '### 3c. Robustness and limits\n\nEffective cross-sectional width is approximately 8–9 because some groups share CES series or use approximate supersectors. Tightness interactions and A4 versus A3 are descriptive. Company-data exclusion limits the study to Q1 and Q3. Research bootstrap and DSR diagnostics cannot fully correct adaptive model search. French industry portfolios are research series, not directly tradable. NAICS-based CRSP stock baskets are the recommended follow-up. ETF proxies require verified mapping and capacity analysis before trading.\n\n'
    text += f"Primary placebo p: {number(result['placebo']['p'])}. Fixed-path industry-cost breakeven: {number(result['cost_breakeven_bps'])} bp. All prespecified sensitivity values, candidate failures, Holm-adjusted comparisons and exclusion reasons remain in the output files regardless of sign.\n\n"
    text += '| Primary sensitivity | Net Sharpe | Mean turnover |\n|---|---:|---:|\n'
    for label,row in result['sensitivities'].items():
        text += f"| {label} | {number(row['sharpe'])} | {number(row['turnover'])} |\n"
    text += f"\nCandidates that passed research eligibility but failed the sealed predictive criterion: {result['research_pass_sealed_failure_count']}. The saved definition requires the research t/correlation/half-sample filter and checks sealed t plus positive IC in each half; it does not reselect features on test outcomes. Every original seed-1 slot remains accounted for, including invalid proposals.\n\n"
    text += 'Circular-shift tests refit the frozen algorithm causally under every registered displacement. They do not merely shift already-fitted predictions. Drop-one-group diagnostics recompute cross-sectional transforms, target ranks, coefficients and portfolio risk while retaining the selected specifications and penalties. Revised-data comparisons measure the difference between available information and hindsight. These checks expose sensitivity; passing them does not prove an executable trading edge.\n\n'
    text += '### 3d. AI evaluation\n\nThe experimental researchers, migration judges and P1/P4 reviewers use Claude Sonnet 5.5 through a subscription. The user approved Claude for all agent usage before research began; the provider amendment and actual interaction evidence are retained. Run indices 1–3 label independent repetitions; the CLI does not honor requested model seeds or temperature. Only run 1 supplies strategy features. Agents saw tightness-tercile feedback but never half-sample IC. Study calls receive no calendar dates or project context; the verified transport removes the CLI’s injected environment reminders.\n\n'
    search = json.loads((P.OUT/'agents/search_summary.json').read_text())
    migration = json.loads((P.OUT/'agents/migration_summary.json').read_text())
    text += f"Migration reports admitted: {migration['reports_admitted']} of {migration['reports_total']}. {migration['interpretation']}\n\n"
    text += '| Search metric | Independent mean | Islands mean | Islands minus independent | Absolute gap exceeds seed range? |\n|---|---:|---:|---:|---|\n'
    for metric,row in search['metrics'].items():
        text += f"| {metric} | {number(row['independent']['mean'])} | {number(row['islands']['mean'])} | {number(row['islands_minus_independent'])} | {row['absolute_gap_exceeds_seed_range']} |\n"
    text += '\nThese comparisons describe the search process. Claim uptake is evaluated per report–receiving-submission pair; a later hypothesis can be associated with several earlier reports. Improvements over a receiving agent’s earlier best are therefore descriptive associations, not causal estimates of communication. Failure avoidance and the sampled human agreement are retained separately. Students must critically assess the proposals and audit findings rather than treating a syntactically valid response as economic evidence.\n\n## 4. Appendices\n\nAll reported results originate in saved research_summary.json, agent summary files or sealed results.json. Full code, input hashes, inference tables, frozen selections, call logs and figure hashes accompany this report. Team critique remains for the students.\n'
    decoded = {value:key for key,value in blind['variables'].items()}
    text += '\n### Selected feature interpretation, decoded after evaluation\n\n'
    by_id = {row['candidate_id']:row for row in selection['seed_one_specs']}
    for arm,ids in selection['selected'].items():
        if not ids:
            text += f'- {arm}: no candidate met the registered selection rule; strategy equals its base.\n'
        for identifier in ids:
            expression = by_id[identifier]['spec']['expression']
            expression = re.sub(r'\bV\d{2}\b',lambda match:decoded.get(match.group(),match.group()),expression)
            text += f'- {arm}, {html.escape(identifier)}: `{expression}`. {html.escape(by_id[identifier]["spec"]["hypothesis"])}\n'
    (report/'report.md').write_text(text)
    (report/'chatgpt_log.md').write_text('# Claude interaction log\n\nThe user approved Claude for all agent usage. This file retains the assignment-template filename; all P1–P4 interactions identify their actual Claude provider. Genuine transcripts, tested findings and student critique remain required.\n\n| Phase | Provider | Prompt source | Output summary | What was wrong | What changed | Team critique |\n|---|---|---|---|---|---|---|\n| P1 | Claude Sonnet 5.5, see audit evidence | p1_request.json | See p1_review.json | See tested claims | See fixes | |\n| P2 | Claude Sonnet 5.5 | agents/log.jsonl, run 1 first submissions | See candidates.csv | See invalid submissions | No engineer edits | |\n| P3 | Claude Sonnet 5.5 | agents/migrations.json | See migration_summary.json | See human spot checks | See tracing | |\n| P4 | Claude Sonnet 5.5, see audit evidence | p4_prompt.json | See p4_review.json | See decisions | Accepted registered diagnostics | |\n')
    return report/'report.md'
