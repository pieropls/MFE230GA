"""Private grammar evaluation and resumable, blinded research-call protocol.

No subprocess, browser, shell, or general code evaluation is exposed to agents.
Experimental transport remains disabled until its isolation is documented.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import numpy as np
import pandas as pd

import params as P
import data as D
import stats as S


def blind_inputs(levels, tightness):
    names = list(P.AGENT['leaf_inputs'])
    rng = np.random.default_rng(P.SEED)
    mapping = dict(zip(names,[f'V{i:02}' for i in rng.permutation(np.arange(1,len(names)+1))]))
    groups = sorted(levels.group.unique())
    group_map = dict(zip(map(str,groups),[f'G{i:02}' for i in rng.permutation(np.arange(1,len(groups)+1))]))
    units = {'JOR':'rate in percent of employment','HIR':'rate in percent of employment',
             'QUR':'rate in percent of employment','LDR':'rate in percent of employment',
             'H':'hours','E':'dollars per hour'}
    values, dictionary = {}, []
    for name in names:
        frame = S.monthly(levels.loc[levels.variable==name].pivot(index='decision',columns='group',values='value'))
        frame.columns = [group_map[str(g)] for g in frame.columns]
        frame = frame.sort_index(axis=1)
        identifier = mapping[name]
        values[identifier] = frame
        research = frame.loc[P.RESEARCH_START:P.SELECTION_END]
        dictionary.append({'id':identifier,'type':units[name], 'stock_or_flow':'stock' if name=='JOR' else 'flow' if name in P.MEASURES else 'average',
                           'frequency':'monthly','availability_lag_months':2 if name in P.MEASURES else 1,
                           'coverage_share':round(float(research.notna().mean().mean()),2),'common':False})
    t = S.monthly(tightness['T'])
    dictionary.append({'id':'T','type':'index','stock_or_flow':'stock ratio','frequency':'monthly',
                       'availability_lag_months':2,'coverage_share':round(float(t.loc[P.RESEARCH_START:P.SELECTION_END].notna().mean()),2),'common':True})
    private = {'variables':mapping,'groups':group_map,'research_months':{str(m):i+1 for i,m in enumerate(pd.period_range(P.RESEARCH_START,P.SELECTION_END,freq='M'))}}
    path = P.OUT/'blind_map.json'
    if path.exists() and json.loads(path.read_text()) != private:
        raise ValueError('Existing blind map differs')
    if not path.exists():
        D.write_json(path,private,exclusive=True)
        path.chmod(0o600)
    dictionary.sort(key=lambda item:item['id'])
    D.write_json(P.OUT/'agents/dictionary.json',dictionary)
    return values,t,dictionary,private


def parse_expression(expression, variable_ids):
    if not isinstance(expression,str):
        raise ValueError('Expression must be a string')
    try:
        tree = ast.parse(expression,mode='eval').body
    except (SyntaxError,RecursionError):
        raise ValueError('Invalid expression syntax') from None
    variables,tokens = set(),set()
    unary = {'yoy','accel','csrank','withT'}
    binary = {'ratio','spread','mult'}
    scalar = {'lag','mavg','chg','lchg','persist','tsz','regime'}
    def visit(node,depth=0):
        if isinstance(node,ast.Name):
            if node.id not in set(variable_ids)|{'T'}:
                raise ValueError('Unknown variable')
            if node.id!='T':
                variables.add(node.id)
            tokens.add(node.id)
            return
        if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.keywords:
            raise ValueError('Only whitelisted function calls and variables are allowed')
        operation = node.func.id
        if operation not in unary|binary|scalar or depth>=P.AGENT['depth']:
            raise ValueError('Unknown operation or nesting limit exceeded')
        tokens.add(operation)
        expected = 1 if operation in unary else 2
        if len(node.args)!=expected:
            raise ValueError('Wrong number of arguments')
        visit(node.args[0],depth+1)
        if operation in binary:
            visit(node.args[1],depth+1)
        elif operation in scalar:
            argument = node.args[1]
            if not isinstance(argument,ast.Constant) or type(argument.value) not in (int,str):
                raise ValueError('A literal window or regime is required')
            choices = P.AGENT['window_choices'] if operation=='mavg' else P.AGENT['persist_choices'] if operation=='persist' else P.AGENT['tsz_choices'] if operation=='tsz' else ['low','high'] if operation=='regime' else P.AGENT['lag_choices']
            if argument.value not in choices:
                raise ValueError('Unregistered lag, window or regime')
    visit(tree)
    if len(variables)>P.AGENT['max_variables']:
        raise ValueError('Too many base variables')
    return tree,tokens


def validate_spec(spec, variables):
    if not isinstance(spec,dict) or set(spec)!={'name','hypothesis','falsified_if','expression'}:
        raise ValueError('Expected exactly four submission fields')
    if any(not isinstance(v,str) or not v.strip() for v in spec.values()):
        raise ValueError('Submission fields must be nonempty strings')
    for field,limit in [('hypothesis',P.AGENT['hypothesis_word_limit']),
                        ('falsified_if',P.AGENT['falsification_word_limit'])]:
        count = len(spec[field].split())
        if count>limit:
            raise ValueError(f'{field} has {count} words; maximum is {limit}')
    return parse_expression(spec['expression'],variables)


def evaluate_expression(expression, variables, tightness, standardized=True):
    tree,_ = parse_expression(expression,variables)
    template = next(iter(variables.values()))
    t = tightness.reindex(template.index)
    broadcast = pd.DataFrame(np.repeat(t.to_numpy()[:,None],len(template.columns),axis=1),index=template.index,columns=template.columns)
    def csz(x):
        return x.sub(x.mean(axis=1),axis=0).div(x.std(axis=1,ddof=1).replace(0,np.nan),axis=0)
    def evaluate(node):
        if isinstance(node,ast.Name):
            return broadcast if node.id=='T' else variables[node.id]
        operation = node.func.id
        x = evaluate(node.args[0])
        argument = node.args[1] if len(node.args)>1 else None
        k = argument.value if isinstance(argument,ast.Constant) else None
        if operation=='lag': return x.shift(k)
        if operation=='mavg': return x.rolling(k,min_periods=k).mean()
        if operation=='chg': return x-x.shift(k)
        if operation=='lchg': return np.log(x.where(x>0))-np.log(x.shift(k).where(x.shift(k)>0))
        if operation=='yoy': return x-x.shift(12)
        if operation=='accel': return x-2*x.shift(3)+x.shift(6)
        if operation=='persist':
            change = x-x.shift(1)
            return (change>0).astype(float).where(change.notna()).rolling(k,min_periods=k).mean()
        if operation=='tsz':
            window = x.expanding(min_periods=P.AGENT['tsz_exp_min']) if k=='exp' else x.rolling(k,min_periods=k)
            return (x-window.mean())/window.std(ddof=1).replace(0,np.nan)
        if operation=='csrank': return x.rank(axis=1,pct=True,method='average')
        if operation=='withT': return x.mul(t,axis=0)
        if operation=='regime':
            regimes = S.tightness_regimes(t)
            multiplier = regimes.eq(k).astype(float).where(regimes.notna())
            return x.mul(multiplier,axis=0)
        y = evaluate(argument)
        if operation=='ratio': return x/y.replace(0,np.nan)
        if operation=='spread': return csz(x)-csz(y)
        if operation=='mult': return x*y
        raise AssertionError('Unreachable grammar branch')
    raw = evaluate(tree).replace([np.inf,-np.inf],np.nan)
    return D.standardize(raw)[0] if standardized else raw


def leak_check(text):
    # These phrases describe statistics, not the industries with the same words.
    screened = re.sub(r'\binformation coefficients?\b','statistic',text,flags=re.I)
    screened = re.sub(r'\b(?:signal|feature|spread-based) construction\b','transformation',screened,flags=re.I)
    forbidden = [name for _,name,_,_,_,_ in P.GROUPS]
    forbidden += list(D.series_map().series_id.unique())
    forbidden += ['JOLTS','FRED','ALFRED','Revelio','LinkUp','Dewey','Ken French','Microsoft','Apple','Amazon',
                  'manufacturing','mining','logging','wholesale','retail','utilities','banking','insurance','real estate',
                  'health care','accommodation','transportation','construction']
    if any(re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',screened,re.I) for term in forbidden):
        raise ValueError('Blinded payload contains a forbidden name or identifier')
    if re.search(r'\b(?:19|20)\d{2}[-/]\d{1,2}(?:[-/]\d{1,2})?\b',text):
        raise ValueError('Blinded payload contains a calendar date')
    if re.search(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:19|20)\d{2}\b',text,re.I):
        raise ValueError('Blinded payload contains a calendar date')
    capital_tokens = set(re.findall(r'\b[A-Z]{2,5}\b',text))
    if capital_tokens-{'IC','JSON','SD','T','HAC','NW','AND','OR','NOT'}:
        raise ValueError('Blinded payload contains an unapproved capitalized identifier')
    if re.search(r'\b(?:first_half_ic|second_half_ic|half.sample.IC)\b',text,re.I):
        raise ValueError('Blinded payload contains selection-only feedback')
    return True


def safe_history_spec(spec):
    """Retain a rejected proposal only when its text remains safe to send back."""
    fields = ('name','hypothesis','falsified_if','expression')
    if not isinstance(spec,dict) or any(not isinstance(spec.get(k),str) for k in fields):
        return None
    result = {k:spec[k] for k in fields}
    try:
        leak_check(json.dumps(result))
    except ValueError:
        return None
    return result


def migration_has_formula(text):
    """Recognize expression syntax without treating prose punctuation as code."""
    if '```' in text or re.search(r'(?m)^\s*(?:import\s+|from\s+\w+\s+import\s+|def\s+\w+\s*\()',text):
        return True
    variable = r'(?:V\d{2}|T)\b'
    operand = r'(?:V\d{2}\b|T\b|\d+(?:\.\d+)?|\()'
    operator = r'(?:\*\*|[+*/×^=<>-])'
    if re.search(r'\b'+variable+r'\s*'+operator+r'\s*'+operand,text):
        return True
    if re.search(r'\b\d+(?:\.\d+)?\s*'+operator+r'\s*'+variable,text):
        return True
    operations = r'lag|mavg|chg|lchg|yoy|accel|persist|tsz|csrank|mult|ratio|spread|withT|regime'
    for match in re.finditer(r'\b(?:'+operations+r')\s*\(',text):
        depth = 1
        for end in range(match.end(),len(text)):
            depth += (text[end]=='(')-(text[end]==')')
            if depth==0:
                try:
                    node = ast.parse(text[match.start():end+1],mode='eval').body
                except (SyntaxError,RecursionError):
                    break
                if isinstance(node,ast.Call):
                    return True
                break
    return False


def validate_migration(text):
    """Return all admission failures; the lexical screen is not a semantic proof."""
    reasons = []
    try:
        leak_check(text)
    except ValueError as exc:
        reasons.append(str(exc))
    count = len(text.split())
    limit = P.AGENT['migration_word_limit']
    if count>limit:
        reasons.append(f'Migration report has {count} words; maximum is {limit}')
    if migration_has_formula(text):
        reasons.append('Migration report contains an expression or code')
    # Negated claims of failure do not establish an unsuccessful attempt.
    failure_text = re.sub(r'\b(?:no|without|zero)\s+failures?\b|\b(?:did not|didn.t|never)\s+fail\b','',text,flags=re.I)
    failure = re.search(r'\b(?:failed|failure|invalid|unsuccessful|underperformed)\b|'
                        r'\b(?:did not|didn.t|could not|couldn.t)\b|'
                        r'\b(?:nothing|none)\s+(?:improved|worked|helped)\b|'
                        r'\bno\s+(?:usable\s+)?(?:improvement|benefit)\b',failure_text,re.I)
    if not failure:
        reasons.append('Migration report needs an explicit unsuccessful attempt or finding')
    return reasons


def require_transport():
    if (P.OUT/'PAUSED.json').exists():
        raise PermissionError('Research is paused; explicit resumption is required')
    alignment_path = P.OUT/'protocol_alignment.json'
    alignment = json.loads(alignment_path.read_text()) if alignment_path.exists() else {}
    if alignment.get('ready_for_research') is not True or alignment.get('open_flags')!=[]:
        raise PermissionError('Project-guideline alignment must be resolved before research calls')
    for name in ['params.py','data.py','stats.py','agents.py','plots.py','run.ipynb']:
        if alignment.get('evidence_hashes',{}).get(name)!=D.sha256(P.ROOT/name):
            raise PermissionError('Project-guideline alignment evidence is stale')
    active_path = P.OUT/'active_run.json'
    active = json.loads(active_path.read_text()) if active_path.exists() else {}
    if active.get('run_id')!=P.AGENT['run_id'] or active.get('fresh_namespace_verified') is not True:
        raise PermissionError('Research requires the verified fresh run namespace')
    path = P.OUT/'agents/transport_attestation.json'
    if not path.exists():
        raise PermissionError('Tool-free transport has not been verified; use manual prompt export only')
    record = json.loads(path.read_text())
    required = ['approved_protocol','zero_tools_verified','no_project_context_verified','no_history_reuse_verified','exact_model_recorded']
    if any(record.get(key) is not True for key in required) or not record.get('evidence_files') or not record.get('actual_model'):
        raise PermissionError('Transport attestation is incomplete')
    for item in record['evidence_files']:
        if D.sha256(P.ROOT/item['file'])!=item['sha256']:
            raise PermissionError('Transport evidence changed')
    if P.AGENT.get('transport') == 'claude_subscription':
        D.stage0()
        for name in ['params.py','agents.py','outputs/prereg_amendments/001_claude_subscription.json']:
            if record.get('binding_hashes',{}).get(name) != D.sha256(P.ROOT/name):
                raise PermissionError('Claude transport binding changed')
        cli = Path(record.get('cli_path',''))
        if not cli.is_file() or D.sha256(cli) != record.get('cli_sha256'):
            raise PermissionError('Claude executable changed; repeat transport verification')
        if record['actual_model'] != P.AGENT['model'] or record.get('live_subscription_verified') is not True:
            raise PermissionError('Claude subscription/model verification is incomplete')
    return record


def claude_environment(request=None):
    """Reuse login through the CLI, never through copied tokens or inherited API keys."""
    env = {k:os.environ[k] for k in ('PATH','HOME','USER','LANG') if k in os.environ}
    env.update({'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC':'1',
                'CLAUDE_CODE_DISABLE_AUTO_MEMORY':'1','CLAUDE_CODE_DISABLE_ATTACHMENTS':'1',
                'DISABLE_UPDATES':'1','CLAUDE_CODE_MAX_RETRIES':'0'})
    if request is not None:
        # Documented body customization keeps the outgoing conversation controlled.
        env['CLAUDE_CODE_EXTRA_BODY'] = json.dumps({'messages':[{'role':'user','content':request['prompt']}]})
    return env


def claude_command(cli, request):
    return [str(cli),'-p','--safe-mode','--tools','','--strict-mcp-config',
            '--mcp-config','{"mcpServers":{}}','--disable-slash-commands','--no-chrome',
            '--no-session-persistence','--permission-prompts','none','--setting-sources','',
            '--settings','{"enabledPlugins":{"agents-md@builtin":false}}',
            '--system-prompt',request['system'],'--model',P.AGENT['model'],
            '--effort',P.AGENT['effort'],'--max-turns','1','--output-format','stream-json','--verbose']


def validate_claude_events(events):
    """Fail closed on model fallback, extra turns, tools, or missing result evidence."""
    init = [e for e in events if e.get('type')=='system' and e.get('subtype')=='init']
    replies = [e['message'] for e in events if e.get('type')=='assistant']
    results = [e for e in events if e.get('type')=='result']
    if len(init)!=1 or not replies or len(results)!=1:
        raise ValueError('Expected one initialization, assistant content and one result')
    head, result = init[0], results[0]
    if any(head.get(k)!=[] for k in ('tools','mcp_servers','skills','plugins')):
        raise ValueError('Claude exposed tools or customizations')
    if head.get('apiKeySource')!='none':
        raise ValueError('Claude reported an API key source')
    if head.get('model')!=P.AGENT['model'] or any(reply.get('model')!=P.AGENT['model'] for reply in replies):
        raise ValueError('Claude model changed')
    if result.get('subtype')!='success' or result.get('is_error') is not False or result.get('num_turns')!=1:
        raise ValueError('Claude did not complete exactly one successful turn')
    # The SDK emits one assistant event per completed content block, not per turn.
    content = [block for reply in replies for block in reply.get('content',[])]
    if any(block.get('type') not in ('text','thinking','redacted_thinking') for block in content):
        raise ValueError('Unexpected assistant content or tool invocation')
    response = ''.join(block['text'] for block in content if block.get('type')=='text')
    if not response or result.get('result')!=response:
        raise ValueError('Claude response/result mismatch')
    usage, models = result.get('usage',{}), result.get('modelUsage',{})
    if set(models)!={P.AGENT['model']} or not usage or any(usage.get('server_tool_use',{}).values()):
        raise ValueError('Unexpected model usage or server tools')
    model_usage = models[P.AGENT['model']]
    if model_usage.get('canonicalModel')!=P.AGENT['model'] or model_usage.get('provider')!='firstParty':
        raise ValueError('Claude canonical model/provider changed')
    return {'response':response,'model':P.AGENT['model'],'tokens':usage,
            'seed_honoured':False,'temperature_honoured':False,
            'transport':'claude_subscription','estimated_list_cost_usd':result.get('total_cost_usd'),
            'cost_note':'CLI list-price estimate, not evidence of a separate API charge',
            'runtime':{k:head[k] for k in ('model','tools','mcp_servers','skills','plugins','apiKeySource')}}


def safe_claude_events(events):
    """Retain protocol evidence without account/session identifiers or debug output."""
    saved = []
    for event in events:
        if event.get('type')=='system' and event.get('subtype')=='init':
            saved.append({k:event.get(k) for k in ('type','subtype','model','tools','mcp_servers','skills','plugins','apiKeySource')})
        elif event.get('type')=='assistant':
            message = event['message']
            content = [{'type':block.get('type'),**({'text':block['text']} if block.get('type')=='text' else {})}
                       for block in message.get('content',[])]
            saved.append({'type':'assistant','message':{'model':message.get('model'),
                         'content':content,'usage':message.get('usage')}})
        elif event.get('type')=='result':
            saved.append({k:event.get(k) for k in ('type','subtype','is_error','num_turns','result','usage','modelUsage','total_cost_usd')})
    return saved


def claude_subscription_call(request, cli, call_root):
    """One fresh process per logical call; a crash never triggers an automatic re-call."""
    if not re.fullmatch(r'[A-Za-z0-9_]+',request['call_id']):
        raise ValueError('Unsafe call identifier')
    if request.get('requested_model',P.AGENT['model']) != P.AGENT['model']:
        raise ValueError('Request model differs from registered Claude model')
    version = subprocess.run([str(cli),'--version'],env=claude_environment(),
                             text=True,capture_output=True,timeout=20)
    match = re.search(r'\b(\d+)\.(\d+)\.(\d+)\b',version.stdout)
    if version.returncode or not match or tuple(map(int,match.groups())) < (2,1,284):
        raise RuntimeError('Sonnet 5.5 requires Claude Code 2.1.284 or newer')
    digest = hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
    folder = Path(call_root)/request['call_id']
    env = claude_environment(request)
    env['TMPDIR'] = str(folder/'tmp')
    recorded_env = {k:v for k,v in env.items() if k not in ('HOME','PATH','USER','LANG')}
    if folder.exists():
        saved = json.loads((folder/'request.json').read_text())
        if saved['request_hash']!=digest:
            raise ValueError('Claude call ID reused with different inputs')
        result_path = folder/'response.json'
        if result_path.exists():
            controls = json.loads((folder/'controls.json').read_text())
            if (controls['command']!=claude_command(cli,request) or controls['cli_sha256']!=D.sha256(cli)
                    or controls.get('environment')!=recorded_env):
                raise ValueError('Cached Claude invocation used different controls or executable')
            recorded = json.loads((folder/'events.json').read_text())
            if recorded.get('exit_code')!=0:
                raise ValueError('Cached Claude invocation did not succeed')
            envelope = validate_claude_events(recorded['events'])
            envelope['request_hash'] = digest
            if json.loads(result_path.read_text())!=envelope:
                raise ValueError('Cached Claude response differs from its validated events')
            return envelope
        raise RuntimeError('Previous Claude call is incomplete; inspect it before any retry')
    folder.mkdir(parents=True,exist_ok=False)
    (folder/'empty').mkdir()
    (folder/'tmp').mkdir()
    D.write_json(folder/'request.json',{'request_hash':digest,'request':request},exclusive=True)
    # The CLI can authenticate normally, but cannot read study inputs or Codex context.
    profile = '\n'.join(['(version 1)','(allow default)',
        f'(deny file-read* (subpath {json.dumps(str(P.WORKSPACE))}))',
        f'(allow file-read* (subpath {json.dumps(str(folder))}))',
        f'(allow file-read* (literal {json.dumps(str(Path(cli).resolve()))}))',
        '(deny file-read* (subpath "/Users/alex/Downloads"))',
        '(deny file-read* (subpath "/Users/alex/.codex"))'])
    command = claude_command(cli,request)
    D.write_json(folder/'controls.json',{'command':command,'sandbox':profile,
                 'cli_sha256':D.sha256(cli),'environment':recorded_env},exclusive=True)
    try:
        auth = subprocess.run([str(cli),'auth','status'],env=env,cwd=folder/'empty',
                              text=True,capture_output=True,timeout=20)
        status = json.loads(auth.stdout)
        safe_auth = {k:status.get(k) for k in ('loggedIn','authMethod','apiProvider','subscriptionType')}
        D.write_json(folder/'auth_status.json',safe_auth,exclusive=True)
        if (auth.returncode or not status.get('loggedIn') or status.get('authMethod')!='claude.ai'
                or status.get('apiProvider')!='firstParty'):
            raise PermissionError('Claude subscription login unavailable; no inference attempted')
        process = subprocess.run(['/usr/bin/sandbox-exec','-p',profile,*command],input=request['prompt'],
                                 env=env,cwd=folder/'empty',text=True,capture_output=True,timeout=180)
        events = [json.loads(line) for line in process.stdout.splitlines() if line.startswith('{')]
        saved_events = safe_claude_events(events)
        D.write_json(folder/'events.json',{'exit_code':process.returncode,'events':saved_events,
                     'stderr_present':bool(process.stderr)},exclusive=True)
        if process.returncode:
            raise RuntimeError('Claude call failed; inspect saved status before resuming')
        envelope = validate_claude_events(saved_events)
        envelope['request_hash'] = digest
        D.write_json(folder/'response.json',envelope,exclusive=True)
        return envelope
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ''
        if isinstance(output,bytes):
            output = output.decode('utf-8',errors='replace')
        partial = []
        for line in output.splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item,dict):
                partial.append(item)
        D.write_json(folder/'partial_events.json',{'events':safe_claude_events(partial),
                     'requires_manual_recovery':True},exclusive=True)
        D.write_json(folder/'failure.json',{'utc':D.utc_now(),'error_type':'TimeoutExpired',
                     'automatic_retry':False},exclusive=True)
        raise RuntimeError('Claude timed out; partial events preserved, no automatic retry') from None
    except (ValueError,RuntimeError,OSError,KeyError,TypeError) as exc:
        D.write_json(folder/'failure.json',{'utc':D.utc_now(),'error_type':type(exc).__name__,
                     'automatic_retry':False},exclusive=True)
        raise RuntimeError('Claude call incomplete; no automatic retry or provider fallback') from None


def require_p1_audit():
    review_path = P.OUT/'p1_review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else {}
    if review.get('complete') is not True or review.get('open_flags')!=[] or not review.get('evidence'):
        raise PermissionError('Complete the documented P1 audit before research calls')
    for name in ['data.py','outputs/manifest.csv','outputs/crosswalk.csv']:
        if review.get('evidence_hashes',{}).get(name) != D.sha256(P.ROOT/name):
            raise PermissionError('P1 audit evidence is stale')
    return review


def research_call_root():
    run_id = P.AGENT['run_id']
    if not re.fullmatch(r'[A-Za-z0-9_]+',run_id):
        raise ValueError('Unsafe research run identifier')
    return P.WORKSPACE/'work/research_runs'/run_id/'calls'


def claude_transport(request):
    attestation = require_transport()
    require_p1_audit()
    return claude_subscription_call(request,Path(attestation['cli_path']),
                                   research_call_root())


def manual_transport(request):
    """File exchange only; exporting a prompt never certifies chat isolation."""
    digest = hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
    path = P.OUT/'agents/manual'/digest
    path.mkdir(parents=True,exist_ok=True)
    D.write_json(path/'request.json',request)
    response = path/'response.json'
    if not response.exists():
        raise FileNotFoundError(f'Pending manual response: {response}')
    envelope = json.loads(response.read_text())
    if envelope.get('request_sha256')!=digest or not isinstance(envelope.get('response'),str) or not envelope.get('model'):
        raise ValueError('Manual response needs matching request hash, text response and exact model')
    return envelope


def _call(request, transport):
    attestation = require_transport()
    payload = request['system']+'\n'+request['prompt']
    leak_check(payload)
    path = P.OUT/'agents/responses'/f"{request['call_id']}.json"
    digest = hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
    if path.exists():
        response = json.loads(path.read_text())
        if response['request_hash']!=digest:
            raise ValueError('Call ID was previously used with a different prompt')
        envelope = response['envelope']
        if transport is claude_transport:
            journal = research_call_root()/request['call_id']/'response.json'
            if not journal.exists():
                raise ValueError('Cached Claude response has no completed transport journal')
            if transport(request)!=envelope:
                raise ValueError('Cached response differs from its Claude transport journal')
    else:
        envelope = transport(request)
    if not isinstance(envelope.get('response'),str) or not envelope.get('model'):
        raise ValueError('Transport must record raw response and exact model ID')
    if envelope['model']!=attestation['actual_model']:
        raise ValueError('Response model differs from the registered actual model')
    if not path.exists():
        D.write_json(path,{'request_hash':digest,'envelope':envelope},exclusive=True)
    log = P.OUT/'agents/log.jsonl'
    logged = {json.loads(line)['call_id'] for line in log.read_text().splitlines()} if log.exists() else set()
    if request['call_id'] not in logged:
        D.append_event('agents/log.jsonl',{**request,'raw_response':envelope['response'],'model':envelope['model'],
                                    'tokens':envelope.get('tokens'),'seed_honoured':envelope.get('seed_honoured'),
                                    'temperature_honoured':envelope.get('temperature_honoured')})
    return envelope


def initial_prompts(dictionary):
    records = []
    for seed in P.AGENT['seeds']:
        for arm in P.AGENT['arms']:
            for emphasis in P.AGENT['emphases']:
                request = _request(arm,seed,emphasis,1,dictionary,[],[])
                leak_check(request['system']+'\n'+request['prompt'])
                D.write_json(P.OUT/'agents/manual'/f'{arm}_{seed}_{emphasis}_first.json',request)
                records.append(request)
    return records


def _request(arm,seed,emphasis,i,dictionary,history,reports):
    return {'call_id':f'{arm}_{seed}_{emphasis}_{i}','kind':'candidate','arm':arm,'seed':seed,
            'agent':emphasis,'submission':i,'requested_model':P.AGENT['model'],
            'requested_seed':P.SEED+seed,'requested_temperature':P.AGENT['temperature'],
            'system':P.SYSTEM_PROMPT.format(n=len(P.GROUPS),emphasis=emphasis,dictionary=json.dumps(dictionary),grammar=P.GRAMMAR),
            'prompt':P.TURN_PROMPT.format(i=i,history=json.dumps(history),migration_reports=json.dumps(reports) if reports else '')}


def run_experiment(variables,tightness,dictionary,target,base,transport=manual_transport):
    require_transport()
    specs,values,reports = [],{},[]
    for seed in P.AGENT['seeds']:
        for arm in P.AGENT['arms']:
            history = {name:[] for name in P.AGENT['emphases']}
            received = {name:[] for name in P.AGENT['emphases']}
            for i in range(1,P.AGENT['submissions']+1):
                for emphasis in P.AGENT['emphases']:
                    request = _request(arm,seed,emphasis,i,dictionary,history[emphasis],received[emphasis])
                    envelope = _call(request,transport)
                    spec,valid,feedback,error = None,False,None,None
                    for attempt in range(P.AGENT['syntax_retries']+1):
                        try:
                            spec = json.loads(envelope['response'])
                            break
                        except json.JSONDecodeError:
                            try:
                                leak_check(envelope['response'])
                            except ValueError:
                                error = 'Invalid JSON contains prohibited content; retry withheld to preserve blinding'
                                break
                            if attempt==P.AGENT['syntax_retries']:
                                error = 'Invalid JSON after syntax retry'
                                break
                            retry = {**request,'call_id':request['call_id']+'_syntax_retry',
                                     'prompt':request['prompt']+'\nYour response was not valid JSON. Return the same proposal as valid JSON only.\n'+envelope['response']}
                            envelope = _call(retry,transport)
                    cid = request['call_id']
                    if spec is not None:
                        try:
                            _,tokens = validate_spec(spec,variables)
                            leak_check(json.dumps(spec))
                            value = evaluate_expression(spec['expression'],variables,tightness)
                            feedback = S.candidate_feedback(value,target,base,tightness)
                            if feedback['mean_ic'] is None:
                                raise ValueError('Candidate has no defined research IC')
                            valid = True
                            values[cid] = value
                        except ValueError as exc:
                            error = str(exc)
                    if not valid:
                        feedback = {'validity':'invalid','reason':error}
                        tokens = set()
                    row = {'candidate_id':cid,'arm':arm,'seed':seed,'agent':emphasis,'submission':i,
                           'spec':spec,'valid':valid,'feedback':feedback,'tokens':sorted(tokens)}
                    row['research_mean_ic'] = float(S.rank_ic(value.loc[P.RESEARCH_START:P.SELECTION_END],target).mean()) if valid else None
                    specs.append(row)
                    log_path = P.OUT/'agents/log.jsonl'
                    known = {json.loads(line)['call_id'] for line in log_path.read_text().splitlines()}
                    evaluation_id = cid+'_evaluation'
                    if evaluation_id not in known:
                        D.append_event('agents/log.jsonl',{'call_id':evaluation_id,'kind':'evaluation',**row})
                    history[emphasis].append({'submission':i,'spec':safe_history_spec(spec),'feedback':feedback})
                    D.write_json(P.OUT/'agents/candidate_records.json',specs)
                # Barrier: all three have completed this submission before any migration.
                if arm=='islands' and i in P.AGENT['migration_after']:
                    new_reports = []
                    for emphasis in P.AGENT['emphases']:
                        request = _request(arm,seed,emphasis,i,dictionary,history[emphasis],received[emphasis])
                        request.update(call_id=request['call_id']+'_migration',kind='migration',
                                       prompt=json.dumps(history[emphasis])+'\n'+P.MIGRATION_PROMPT)
                        request['system'] = request['system'].replace('Rules: return only JSON with keys name, hypothesis, falsified_if, expression; use only the allowed operations; state a hypothesis that the statistics could falsify.',
                                                                    'Report findings only in prose, including a failure. No expressions, specifications or code.')
                        response = _call(request,transport)['response']
                        reasons = validate_migration(response)
                        valid = not reasons
                        report = {'report_id':request['call_id'],'seed':seed,'agent':emphasis,'after_submission':i,
                                  'text':response,'valid':valid,'word_count':len(response.split()),'rejection_reasons':reasons}
                        reports.append(report)
                        if valid:
                            new_reports.append(report)
                    for emphasis in P.AGENT['emphases']:
                        received[emphasis].extend(r['text'] for r in new_reports if r['agent']!=emphasis)
                    D.write_json(P.OUT/'agents/migrations.json',reports)
    pd.DataFrame([{**r,'spec':json.dumps(r['spec']),'feedback':json.dumps(r['feedback']),'tokens':json.dumps(r['tokens'])} for r in specs]).to_csv(P.OUT/'candidates.csv',index=False)
    return specs,values,reports


def trace_migrations(specs,reports,transport=manual_transport):
    judgments = []
    for report in reports:
        if not report['valid']:
            continue
        claims = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',report['text']) if s.strip()]
        for row in specs:
            if row['arm']!='islands' or row['seed']!=report['seed'] or row['agent']==report['agent'] or row['submission']<=report['after_submission']:
                continue
            spec = safe_history_spec(row['spec'])
            if spec is None:
                judgments.append({'report_id':report['report_id'],'candidate_id':row['candidate_id'],
                                  'uses_claim':None,'claim_ids':[],'avoids_failure':None,
                                  'judged':False,'reason':'Submission is unparseable or unsafe to disclose',
                                  'human_uses_claim':None,'human_avoids_failure':None})
                continue
            request = {'call_id':report['report_id']+'__'+row['candidate_id'],'kind':'judge',
                       'arm':'islands','seed':row['seed'],'agent':'judge','submission':row['submission'],
                       'system':'Assess whether the hypothesis or expression uses or tests numbered claims. Return JSON only: {"uses_claim": true|false, "claim_ids": []}.',
                       'prompt':json.dumps({'claims':{str(i+1):c for i,c in enumerate(claims)},
                                            'hypothesis':spec['hypothesis'],'expression':spec['expression']})}
            raw = _call(request,transport)['response']
            try:
                decision = json.loads(raw)
                if set(decision)!={'uses_claim','claim_ids'} or type(decision['uses_claim']) is not bool or not isinstance(decision['claim_ids'],list) or any(type(i) is not int or not 1<=i<=len(claims) for i in decision['claim_ids']) or decision['uses_claim']!=bool(decision['claim_ids']):
                    raise ValueError('Invalid judge response')
            except (ValueError,TypeError):
                decision = {'uses_claim':None,'claim_ids':[]}
            failure_request = {**request,'call_id':request['call_id']+'_failure',
                               'system':'Determine whether the proposed hypothesis or expression explicitly avoids a failure described in the report. Return JSON only: {"avoids_failure": true|false|null}. Use null when the evidence is unclear.',
                               'prompt':json.dumps({'report':report['text'],'hypothesis':spec['hypothesis'],'expression':spec['expression']})}
            failure_raw = _call(failure_request,transport)['response']
            try:
                failure = json.loads(failure_raw)
                if set(failure)!={'avoids_failure'} or type(failure['avoids_failure']) not in (bool,type(None)):
                    raise ValueError('Invalid failure judgment')
            except (ValueError,TypeError):
                failure = {'avoids_failure':None}
            judgments.append({'report_id':report['report_id'],'candidate_id':row['candidate_id'],**decision,**failure,'judged':True,
                              'human_uses_claim':None,'human_avoids_failure':None})
    judgeable = [i for i,row in enumerate(judgments) if row['judged']]
    review = np.random.default_rng(P.SEED).choice(judgeable,size=math_ceil(P.AGENT['judge_review_fraction']*len(judgeable)),replace=False) if judgeable else []
    for i,row in enumerate(judgments):
        row['human_review_required'] = i in review
    path = P.OUT/'agents/migration_judgments.json'
    if path.exists():
        previous = {(r['report_id'],r['candidate_id']):r for r in json.loads(path.read_text())}
        for row in judgments:
            old = previous.get((row['report_id'],row['candidate_id']),{})
            for field in ['human_uses_claim','human_avoids_failure']:
                row[field] = old.get(field)
    D.write_json(P.OUT/'agents/migration_judgments.json',judgments)
    return judgments


def math_ceil(number):
    return int(np.ceil(number))


def process_metrics(specs):
    rows = []
    for seed in P.AGENT['seeds']:
        for arm in P.AGENT['arms']:
            current = [r for r in specs if r['seed']==seed and r['arm']==arm]
            valid = [r for r in current if r['valid']]
            sets = [set(r['tokens']) for r in valid]
            similarities = [len(a&b)/len(a|b) for i,a in enumerate(sets) for b in sets[i+1:] if a|b]
            for i in range(1,7):
                scores = [r['research_mean_ic'] for r in valid if r['submission']<=i]
                rows.append({'arm':arm,'seed':seed,'submission':i,'best_so_far_ic':max(scores) if scores else np.nan,
                             'median_ic':np.median([r['research_mean_ic'] for r in valid]) if valid else np.nan,
                             'invalid_rate':1-len(valid)/len(current) if current else np.nan,
                             'diversity':1-np.mean(similarities) if similarities else np.nan})
    return pd.DataFrame(rows)


def summarize_search(specs):
    frame = process_metrics(specs)
    frame.to_csv(P.OUT/'agents/process_metrics.csv',index=False)
    final = frame.loc[frame.submission==P.AGENT['submissions']]
    result = {'unit':'three seeds per architecture; descriptive search variation, not additional sealed observations','metrics':{}}
    for metric in ['best_so_far_ic','median_ic','invalid_rate','diversity']:
        arms = {}
        for arm,rows in final.groupby('arm'):
            values = rows[metric].dropna()
            arms[arm] = {'mean':values.mean(),'minimum':values.min(),'maximum':values.max(),'seeds_with_defined_value':len(values)}
        independent,islands = arms['independent'],arms['islands']
        gap = islands['mean']-independent['mean']
        largest_range = max(a['maximum']-a['minimum'] for a in arms.values())
        result['metrics'][metric] = {**arms,'islands_minus_independent':gap,
                                    'largest_between_seed_range':largest_range,
                                    'absolute_gap_exceeds_seed_range':bool(abs(gap)>largest_range) if np.isfinite(gap) and np.isfinite(largest_range) else None,
                                    'higher_is_better':metric!='invalid_rate'}
    D.write_json(P.OUT/'agents/search_summary.json',S.clean_json(result))
    return S.clean_json(result)


def summarize_migrations(specs, reports, judgments):
    by_candidate = {r['candidate_id']:r for r in specs}
    by_report = {r['report_id']:r for r in reports}
    records = []
    for item in judgments:
        row = by_candidate[item['candidate_id']]
        report = by_report[item['report_id']]
        earlier = [r['research_mean_ic'] for r in specs if r['arm']=='islands' and r['seed']==row['seed']
                   and r['agent']==row['agent'] and r['submission']<=report['after_submission'] and r['valid']]
        records.append({**item,'seed':row['seed'],
                        'improvement':row['research_mean_ic']-max(earlier) if earlier and row['valid'] else np.nan})
    frame = pd.DataFrame(records)
    def group_summary(current):
        if current.empty:
            return {'uptake_rate':None,'improvement_with_uptake':None,'improvement_without_uptake':None,'n':0,'failure_avoidance_rate':None}
        defined = current.loc[current.uses_claim.notna()]
        avoided = current.avoids_failure.dropna()
        return S.clean_json({'n':len(current),'defined_judgments':len(defined),
                             'uptake_rate':defined.uses_claim.mean(),
                             'improvement_with_uptake':defined.loc[defined.uses_claim.eq(True),'improvement'].mean(),
                             'improvement_without_uptake':defined.loc[defined.uses_claim.eq(False),'improvement'].mean(),
                             'failure_avoidance_rate':avoided.mean() if len(avoided) else np.nan,
                             'failure_avoidance_n':len(avoided)})
    summary = group_summary(frame)
    admitted = sum(bool(r['valid']) for r in reports)
    summary['reports_total'] = len(reports)
    summary['reports_admitted'] = admitted
    summary['reports_rejected'] = len(reports)-admitted
    summary['communication_observed'] = admitted>0
    summary['interpretation'] = ('Only admitted reports were delivered; report rejection and undefined judgments separately.' if admitted
                                 else 'No report was admitted or delivered. This run cannot establish the benefit or absence of benefit from exchanging findings.')
    summary['unit'] = 'report–receiving-submission pair; uptake comparisons are associations, not causal effects'
    summary['by_seed'] = {str(seed):group_summary(frame.loc[frame.seed==seed] if len(frame) else frame) for seed in P.AGENT['seeds']}
    judged_count = int(frame.judged.sum()) if len(frame) else 0
    required = frame.loc[frame.human_review_required] if len(frame) else frame
    completed = required.loc[required.human_uses_claim.map(type).eq(bool)] if len(required) else required
    agreement = (completed.human_uses_claim==completed.uses_claim).mean() if len(completed) else np.nan
    review = {'complete':len(completed)==len(required), 'total_judgments':judged_count,'total_receiving_pairs':len(frame),
              'review_fraction':len(completed)/judged_count if judged_count else None,
              'review_required':len(required),'review_completed':len(completed),'agreement':agreement,
              'evidence_hashes':{'outputs/agents/migration_judgments.json':D.sha256(P.OUT/'agents/migration_judgments.json')}}
    D.write_json(P.OUT/'agents/migration_summary.json',S.clean_json(summary))
    D.write_json(P.OUT/'agents/migration_review.json',S.clean_json(review))
    return summary,review


def audit_agent_prompts():
    log = P.OUT/'agents/log.jsonl'
    records = [json.loads(line) for line in log.read_text().splitlines()]
    prompts = [r for r in records if 'prompt' in r]
    for row in prompts:
        leak_check(row['system']+'\n'+row['prompt'])
    calls = [r for r in prompts if r.get('kind')=='candidate' and not r['call_id'].endswith('_syntax_retry')]
    expected = len(P.AGENT['arms'])*len(P.AGENT['seeds'])*len(P.AGENT['emphases'])*P.AGENT['submissions']
    if len(calls)!=expected or len({r['call_id'] for r in prompts})!=len(prompts):
        raise ValueError('Call budget or uniqueness check failed')
    expected_ids = {f'{arm}_{seed}_{agent}_{i}' for arm in P.AGENT['arms'] for seed in P.AGENT['seeds']
                    for agent in P.AGENT['emphases'] for i in range(1,P.AGENT['submissions']+1)}
    if {r['call_id'] for r in calls}!=expected_ids:
        raise ValueError('Candidate schedule differs from the prescribed design')
    migrations = [r for r in prompts if r.get('kind')=='migration']
    expected_reports = {f'islands_{seed}_{agent}_{i}_migration' for seed in P.AGENT['seeds']
                        for agent in P.AGENT['emphases'] for i in P.AGENT['migration_after']} if 'islands' in P.AGENT['arms'] else set()
    if {r['call_id'] for r in migrations}!=expected_reports:
        raise ValueError('Migration schedule differs from the prescribed design')
    repairs = [r for r in prompts if r.get('kind')=='candidate' and r['call_id'].endswith('_syntax_retry')]
    if any(r['call_id'].removesuffix('_syntax_retry') not in expected_ids for r in repairs):
        raise ValueError('Syntax repair has no original proposal slot')
    result = {'passed':True,'candidate_calls':len(calls),'total_calls':len(prompts),'log_sha256':D.sha256(log),
              'migration_calls':len(migrations),'syntax_repairs':len(repairs),
              'evidence_hashes':{'outputs/agents/log.jsonl':D.sha256(log)},
              'limitation':'Automatic identifier/date screening does not prove absence of every possible real-world reference; inspect ambiguous text before freeze.'}
    D.write_json(P.OUT/'agents/blinding_audit.json',result)
    return result


def self_test():
    months = pd.period_range('2000-01',periods=80,freq='M')
    frame = pd.DataFrame(np.tile(np.arange(1.,81)[:,None],(1,13)),index=months)
    variables = {'V01':frame,'V02':frame*2,'V03':frame+5}
    t = pd.Series(np.linspace(-1,1,80),index=months)
    assert (evaluate_expression('chg(V01,1)',variables,t,False).iloc[1:]==1).all().all()
    assert (evaluate_expression('persist(V01,3)',variables,t,False).iloc[3:]==1).all().all()
    for bad in ['__import__("os")','V01+V02','lag(V01,-1)','V01.__class__','lag(V01,True)',
                'mult(mult(V01,V02),V03)','lag(lag(lag(lag(V01,1),1),1),1)','lag(V01,k=1)']:
        try:
            parse_expression(bad,variables)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsafe grammar accepted: '+bad)
    for bad in ['2014-10-31','JTU2300JOR','LinkUp','first_half_ic']:
        try:
            leak_check(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Blinding failure')
    later = {k:v.copy() for k,v in variables.items()}
    later['V01'].iloc[60:] *= 999
    first = evaluate_expression('tsz(V01,"exp")',variables,t,False)
    second = evaluate_expression('tsz(V01,"exp")',later,t,False)
    assert first.iloc[:60].equals(second.iloc[:60])
    return {'AST_rejection':'passed','grammar_semantics':'passed','blinding':'passed','causal_transforms':'passed'}
