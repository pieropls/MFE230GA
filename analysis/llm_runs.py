"""Model calls of Study 2.3: R8 (judge with a verbatim quote) and R9 (feedback ablation).

Run once from the project root:  python3 -B analysis/llm_runs.py r8   |   python3 -B analysis/llm_runs.py r9
Each call is headless (`claude -p`, no tools, one turn), uses the original model ID and is logged in
analysis/output/study2/llm/. run.ipynb only reads the saved outputs. Study 1's code is imported read-only.
The CLI is `claude` on the PATH unless CLAUDE_CLI points to another binary (the Opus model needs version
2.1.280 or newer). A call that fails in transport (no model answer) is not a judgment; rerunning `r8`
repeats only those pairs.
"""
import concurrent.futures
import importlib.util
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import params as P
import data as D

LLM = P.OUT2 / 'llm'
CALL_TIMEOUT = 300            # seconds per call (spec: at most 5 minutes)
R9_BUDGET = 2 * 3600          # seconds (spec: at most 2 hours)
MODELS = {'Study 1 (Sonnet)': 'claude-sonnet-5-5', 'Study 1b (Opus)': 'claude-opus-5-5'}
JUDGE_SYSTEM = ('Assess whether the hypothesis or expression uses or tests numbered claims. Return JSON only: '
                '{"uses_claim": true|false, "quote": "<one claim sentence copied verbatim, or none>"}. '
                'Answer true only if you can copy the exact claim sentence that the hypothesis or expression uses or tests.')


def call(system, prompt, model, call_id, log_name, effort=None):
    """One headless call. Returns the response text ('' on failure) and appends the full record to the log."""
    env = {k: os.environ[k] for k in ('PATH', 'HOME', 'USER', 'LANG') if k in os.environ}
    env.update({'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1', 'DISABLE_UPDATES': '1'})
    command = [os.environ.get('CLAUDE_CLI', 'claude'), '-p', '--tools', '', '--no-session-persistence', '--setting-sources', '', '--system-prompt', system,
               '--model', model, '--max-turns', '1', '--output-format', 'json'] + (['--effort', effort] if effort else [])
    start, record = time.time(), {'utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'call_id': call_id,
                                  'requested_model': model, 'effort': effort, 'system': system, 'prompt': prompt}
    try:
        done = subprocess.run(command, input=prompt, capture_output=True, text=True, timeout=CALL_TIMEOUT, env=env, cwd=str(LLM))
        envelope = json.loads(done.stdout)
        record.update(response=envelope.get('result', ''), actual_models=sorted(envelope.get('modelUsage', {})), usage=envelope.get('usage'),
                      is_error=envelope.get('is_error'))
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        record.update(response='', error=f'{type(exc).__name__}: {str(exc)[:200]}')
    record['seconds'] = round(time.time() - start, 1)
    with open(LLM / log_name, 'a') as handle:
        handle.write(json.dumps(record) + '\n')
    return record['response'] if not record.get('is_error') and not record['response'].startswith('API Error') else None


# ---------------------------------------------------------------- R8 judge fix
def r8():
    norm = lambda text: ' '.join(str(text).lower().split())
    path = P.table_path('s23_r8_judge_pairs')
    done = {(r.study, r.item): r._asdict() for r in pd.read_csv(path).itertuples(index=False) if r.transport_ok} if path.exists() else {}
    rows = []
    for study, root in [('Study 1 (Sonnet)', P.SONNET), ('Study 1b (Opus)', P.OPUS)]:
        out = root / 'outputs'
        sample = json.loads((out / 'human_review_sample.json').read_text())['items']
        reports = {r['report_id']: r['text'] for r in json.loads((out / 'agents/migrations.json').read_text())}
        before = {(j['report_id'], j['candidate_id']): j['uses_claim'] for j in json.loads((out / 'agents/migration_judgments.json').read_text())}
        specs = pd.read_csv(out / 'candidates.csv').set_index('candidate_id').spec.map(json.loads)
        for item in sample:
            if (study, item['item']) in done:                       # already judged; only transport failures are repeated
                rows.append(done[(study, item['item'])])
                continue
            report, spec = reports[item['report_id']], specs[item['candidate_id']]
            import re
            claims = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', report) if s.strip()]          # Study 1's own claim split
            prompt = json.dumps({'claims': {str(i + 1): c for i, c in enumerate(claims)}, 'hypothesis': spec['hypothesis'], 'expression': spec['expression']})
            raw = call(JUDGE_SYSTEM, prompt, MODELS[study], f"r8_{study.split()[1]}_{item['item']}", 'r8_calls.jsonl', effort=os.environ.get('R8_EFFORT'))
            after, quote_found, said_yes = None, None, None
            try:
                answer = json.loads(raw) if raw is not None else None
                if isinstance(answer, dict) and isinstance(answer.get('uses_claim'), bool) and isinstance(answer.get('quote'), str):
                    said_yes = answer['uses_claim']
                    quote = norm(answer['quote'])
                    quote_found = bool(quote not in ('', 'none') and quote in norm(report))
                    after = bool(said_yes and quote_found)
            except (ValueError, TypeError):
                pass
            rows.append({'study': study, 'item': item['item'], 'report_id': item['report_id'], 'candidate_id': item['candidate_id'], 'human': item['human_uses_claim'],
                         'machine_before': before.get((item['report_id'], item['candidate_id'])), 'machine_after': after, 'said_yes': said_yes, 'quote_found': quote_found,
                         'model': MODELS[study], 'transport_ok': raw is not None})
            print(study, item['item'], 'human', item['human_uses_claim'], 'before', rows[-1]['machine_before'], 'after', after, flush=True)
    pd.DataFrame(rows).to_csv(path, index=False)


# ---------------------------------------------------------------- R9 feedback ablation
def study1_modules():
    """Study 1's params, data, stats and agents modules, imported read-only (nothing is written into its folder)."""
    sys.dont_write_bytecode = True
    saved = {k: sys.modules.get(k) for k in ('params', 'data', 'stats', 'agents')}
    modules = {}
    try:
        for name in ('params', 'data', 'stats', 'agents'):
            spec = importlib.util.spec_from_file_location('study1_' + name, P.SONNET / f'{name}.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            modules[name] = module
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return modules


def r9_inputs():
    """Blinded research inputs exactly as Study 1 built them, from Alex's package; checked against a saved feedback."""
    m = study1_modules()
    FP, FS, FA = m['params'], m['stats'], m['agents']
    out, pkg = P.SONNET / 'outputs', P.PACKAGE / 'studies/follow_the_workers/outputs'
    blind = json.loads((out / 'blind_map.json').read_text())
    dictionary = json.loads((out / 'agents/dictionary.json').read_text())
    groups = {int(k): v for k, v in blind['groups'].items()}
    levels = pd.read_parquet(pkg / 'levels_asof.parquet')
    variables = {}
    for name, identifier in blind['variables'].items():
        frame = FS.monthly(levels.loc[levels.variable == name].pivot(index='decision', columns='group', values='value'))
        variables[identifier] = frame.rename(columns=groups).sort_index(axis=1).loc[:FP.SELECTION_END]
    tightness = FS.monthly(pd.read_parquet(pkg / 'tightness_asof.parquet')['T']).loc[:FP.SELECTION_END]
    base = {k: v.rename(columns=groups).sort_index(axis=1).loc[:FP.SELECTION_END]
            for k, v in FS.feature_matrices(pd.read_parquet(pkg / 'features_asof.parquet')).items()}
    target = D.load_returns()['relative'].rename(columns=groups).sort_index(axis=1).loc[:FP.SELECTION_END]
    # self-check: reproduce the saved feedback of every valid seed-1 candidate of Study 1
    saved = pd.read_csv(out / 'candidates.csv')
    saved = saved[saved.valid]
    mismatches, worst = 0, 0.0
    for row in saved.itertuples():
        spec = json.loads(row.spec)
        new, old = FS.candidate_feedback(FA.evaluate_expression(spec['expression'], variables, tightness), target, base, tightness), json.loads(row.feedback)
        mismatches += new != old
        worst = max([worst] + [abs(new[k] - old[k]) for k in new if isinstance(new[k], float) and isinstance(old.get(k), float)])
    print(f'R9 input check: {len(saved) - mismatches} of {len(saved)} saved feedbacks reproduced exactly; largest difference {worst:.2f}', flush=True)
    pd.DataFrame([{'saved_valid_candidates': len(saved), 'feedback_reproduced_exactly': len(saved) - mismatches, 'largest_abs_difference': worst}]).to_csv(
        P.table_path('s23_r9_input_check'), index=False)
    if mismatches > 0.1 * len(saved) or worst > 0.15:       # rounding of near-ties is tolerated; anything larger is not
        raise SystemExit('R9 not run: the reconstructed research inputs do not reproduce Study 1 feedback')
    return FP, FS, FA, variables, tightness, base, target, dictionary


def r9_agent(condition, seed, emphasis, env):
    FP, FS, FA, variables, tightness, base, target, dictionary = env
    history, rows = [], []
    for i in range(1, FP.AGENT['submissions'] + 1):
        request = FA._request('independent', seed, emphasis, i, dictionary, history, [])
        cid = f'r9_{condition}_{seed}_{emphasis}_{i}'
        raw = call(request['system'], request['prompt'], FP.AGENT['model'], cid, 'r9_calls.jsonl') or ''
        spec, valid, feedback, error, value = None, False, None, None, None
        try:
            spec = json.loads(raw)
        except ValueError:
            raw = call(request['system'], request['prompt'] + '\nYour response was not valid JSON. Return the same proposal as valid JSON only.\n' + raw,
                       FP.AGENT['model'], cid + '_syntax_retry', 'r9_calls.jsonl') or ''
            try:
                spec = json.loads(raw)
            except ValueError:
                error = 'Invalid JSON after syntax retry'
        if spec is not None:
            try:
                FA.validate_spec(spec, variables)
                FA.leak_check(json.dumps(spec))
                value = FA.evaluate_expression(spec['expression'], variables, tightness)
                feedback = FS.candidate_feedback(value, target, base, tightness)
                if feedback['mean_ic'] is None:
                    raise ValueError('Candidate has no defined research IC')
                valid = True
            except (ValueError, KeyError, TypeError) as exc:
                error = str(exc)[:200]
        shown = {'validity': 'invalid', 'reason': error} if not valid else (
            feedback if condition == 'A_with_tercile_split' else {k: v for k, v in feedback.items() if k not in ('low_T_ic', 'high_T_ic')})
        history.append({'submission': i, 'spec': FA.safe_history_spec(spec), 'feedback': shown})
        research = value.loc[FP.RESEARCH_START:FP.SELECTION_END] if valid else None
        rows.append({'condition': condition, 'seed': seed, 'agent': emphasis, 'submission': i, 'valid': valid,
                     'expression': spec.get('expression') if isinstance(spec, dict) else None,
                     'uses_regime': bool(valid and 'regime(' in spec['expression']),
                     'active_share': float((np.isfinite(research).sum(axis=1) >= 11).mean()) if valid else np.nan,
                     'mean_ic': feedback['mean_ic'] if valid else np.nan, 'hac_t': feedback['hac_t'] if valid else np.nan, 'error': error})
        print(cid, 'valid' if valid else f'invalid ({error})', rows[-1]['expression'], flush=True)
    return rows


def r9():
    env = r9_inputs()
    FP = env[0]
    start, rows = time.time(), []
    for seed in FP.AGENT['seeds']:
        if time.time() - start > R9_BUDGET:
            print('R9 time budget reached before seed', seed, flush=True)
            break
        jobs = [(c, seed, e) for c in ['A_with_tercile_split', 'B_without_tercile_split'] for e in FP.AGENT['emphases']]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            for result in pool.map(lambda job: r9_agent(*job, env), jobs):
                rows += result
        pd.DataFrame(rows).to_csv(P.table_path('s23_r9_ablation_proposals'), index=False)      # saved after every seed
        print(f'seed {seed} done after {time.time() - start:.0f} s', flush=True)


def r9post():
    """No model call: add to each saved valid proposal the share of research months in which its
    cross-section is not constant (a regime gate returns a constant outside its regime)."""
    FP, FS, FA, variables, tightness, base, target, dictionary = r9_inputs()
    path = P.table_path('s23_r9_ablation_proposals')
    frame = pd.read_csv(path)
    shares = []
    for row in frame.itertuples():
        if not row.valid:
            shares.append(np.nan)
            continue
        value = FA.evaluate_expression(row.expression, variables, tightness).loc[FP.RESEARCH_START:FP.SELECTION_END]
        shares.append(float(((np.isfinite(value).sum(axis=1) >= 11) & (value.std(axis=1) > 0)).mean()))
    frame['informative_share'] = shares
    frame.to_csv(path, index=False)
    print(frame[frame.valid].groupby(['condition', 'uses_regime']).informative_share.describe()[['count', 'mean', 'min']])


if __name__ == '__main__':
    LLM.mkdir(parents=True, exist_ok=True)
    {'r8': r8, 'r9': r9, 'r9post': r9post}[sys.argv[1]]()
