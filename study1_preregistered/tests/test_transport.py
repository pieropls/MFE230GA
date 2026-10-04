"""Offline regression tests. No real models, credentials, or return data."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1] / 'outputs/follow_the_workers_opus55_xhigh'
sys.path.insert(0,str(PROJECT))
import agents as A
import data as D
import params as P


def events():
    return [
        {'type':'system','subtype':'init','model':P.AGENT['model'],'tools':[],
         'mcp_servers':[],'skills':[],'plugins':[],'apiKeySource':'none'},
        {'type':'assistant','message':{'model':P.AGENT['model'],
         'content':[{'type':'text','text':'{"status":"ready"}'}]}},
        {'type':'result','subtype':'success','is_error':False,'num_turns':1,
         'result':'{"status":"ready"}','usage':{'input_tokens':100,'output_tokens':8},
         'modelUsage':{P.AGENT['model']:{'canonicalModel':P.AGENT['model'],'provider':'firstParty'}}}]


class TransportTests(unittest.TestCase):
    def test_accepts_one_empty_tools_subscription_response(self):
        envelope=A.validate_claude_events(events())
        self.assertEqual(envelope['model'],'claude-opus-5-5')
        self.assertFalse(envelope['seed_honoured'])
        self.assertFalse(envelope['temperature_honoured'])

    def test_rejects_context_tools_fallback_and_extra_calls(self):
        fixtures=[]
        for key in ('tools','skills','mcp_servers','plugins'):
            x=events(); x[0][key]=['unexpected']; fixtures.append(x)
        x=events(); x[0]['apiKeySource']='api_key'; fixtures.append(x)
        x=events(); x[1]['message']['model']='another-model'; fixtures.append(x)
        x=events(); x[1]['message']['content'].append({'type':'tool_use'}); fixtures.append(x)
        x=events(); x[2]['num_turns']=2; fixtures.append(x)
        x=events(); x[2]['usage']['server_tool_use']={'web_search_requests':1}; fixtures.append(x)
        x=events(); x[2]['modelUsage']['another-model']={}; fixtures.append(x)
        x=events(); x.append(deepcopy(x[1])); fixtures.append(x)
        x=events(); x[2]['result']='different'; fixtures.append(x)
        for fixture in fixtures:
            with self.subTest(fixture=fixture),self.assertRaises(ValueError):
                A.validate_claude_events(fixture)

    def test_environment_omits_inherited_credentials_and_config(self):
        with patch.dict(A.os.environ,{'ANTHROPIC_API_KEY':'dummy','ANTHROPIC_AUTH_TOKEN':'dummy',
                        'CLAUDE_CONFIG_DIR':'dummy','ANTHROPIC_BASE_URL':'dummy'}):
            env=A.claude_environment()
        self.assertFalse(set(env)&{'ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','CLAUDE_CONFIG_DIR','ANTHROPIC_BASE_URL'})
        self.assertEqual(env['CLAUDE_CODE_MAX_RETRIES'],'0')
        controlled=A.claude_environment({'prompt':'only this controlled input'})
        self.assertEqual(json.loads(controlled['CLAUDE_CODE_EXTRA_BODY']),
                         {'messages':[{'role':'user','content':'only this controlled input'}]})

    def test_split_content_blocks_are_one_turn_without_retaining_reasoning(self):
        x=events()
        x.insert(1,{'type':'assistant','message':{'model':P.AGENT['model'],
                    'content':[{'type':'thinking','thinking':'private reasoning','signature':'opaque'}]}})
        safe=A.safe_claude_events(x)
        self.assertEqual(safe[1]['message']['content'],[{'type':'thinking'}])
        self.assertEqual(A.validate_claude_events(safe)['response'],'{"status":"ready"}')
        x[1]['message']['model']='another-model'
        with self.assertRaisesRegex(ValueError,'model changed'): A.validate_claude_events(x)
        x[1]['message']['model']=P.AGENT['model']
        x[1]['message']['content']=[{'type':'tool_use'}]
        with self.assertRaisesRegex(ValueError,'tool invocation'): A.validate_claude_events(A.safe_claude_events(x))

    def test_split_text_must_match_single_turn_result(self):
        x=events(); x[1]['message']['content']=[{'type':'text','text':'{"status":'}]
        x.insert(2,{'type':'assistant','message':{'model':P.AGENT['model'],
                    'content':[{'type':'text','text':'"ready"}'}]}})
        self.assertEqual(A.validate_claude_events(x)['response'],'{"status":"ready"}')
        x[-1]['num_turns']=2
        with self.assertRaisesRegex(ValueError,'one successful turn'): A.validate_claude_events(x)

    def test_cache_and_failure_do_not_repeat_inference(self):
        for failed in (False,True):
            with self.subTest(failed=failed),tempfile.TemporaryDirectory() as temp:
                root=Path(temp); cli=root/'cli'; cli.write_text('fixture')
                calls=[]
                def run(command,**kwargs):
                    calls.append(command)
                    if command[-1]=='--version':
                        text='2.1.284 (Claude Code)'
                    elif command[-2:]==['auth','status']:
                        text=json.dumps({'loggedIn':True,'authMethod':'claude.ai','apiProvider':'firstParty'})
                    else:
                        if failed: raise subprocess.TimeoutExpired(command,180,output=json.dumps(events()[0]).encode())
                        text='\n'.join(map(json.dumps,events()))
                    return subprocess.CompletedProcess(command,0,text,'')
                request={'call_id':'fixture','system':'Return JSON','prompt':'Connection test'}
                with patch.object(A.subprocess,'run',side_effect=run):
                    if failed:
                        with self.assertRaises(RuntimeError): A.claude_subscription_call(request,cli,root/'calls')
                        with self.assertRaises(RuntimeError): A.claude_subscription_call(request,cli,root/'calls')
                        self.assertTrue((root/'calls/fixture/failure.json').exists())
                        self.assertEqual(len(json.loads((root/'calls/fixture/partial_events.json').read_text())['events']),1)
                    else:
                        one=A.claude_subscription_call(request,cli,root/'calls')
                        two=A.claude_subscription_call(request,cli,root/'calls')
                        self.assertEqual(one,two)
                        with self.assertRaises(ValueError):
                            A.claude_subscription_call({**request,'prompt':'changed'},cli,root/'calls')
                        cached=root/'calls/fixture/response.json'
                        tampered=json.loads(cached.read_text()); tampered['response']='changed'
                        cached.write_text(json.dumps(tampered))
                        with self.assertRaisesRegex(ValueError,'validated events'):
                            A.claude_subscription_call(request,cli,root/'calls')
                        cached.write_text(json.dumps(one))
                        recorded=root/'calls/fixture/events.json'
                        tampered=json.loads(recorded.read_text()); tampered['events'][0]['tools']=['Read']
                        recorded.write_text(json.dumps(tampered))
                        with self.assertRaisesRegex(ValueError,'tools'):
                            A.claude_subscription_call(request,cli,root/'calls')
                self.assertEqual(sum(c[0]=='/usr/bin/sandbox-exec' for c in calls),1)

    def test_old_cli_rejected_before_auth_or_inference(self):
        with patch.object(A.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'2.1.259','')) as run:
            with self.assertRaisesRegex(RuntimeError,'2.1.284'):
                A.claude_subscription_call({'call_id':'fixture'},Path('unused'),Path('unused'))
            self.assertEqual(run.call_count,1)

    def test_outer_cache_requires_completed_transport_journal(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            request={'call_id':'fixture','system':'Return JSON','prompt':'Connection test'}
            digest=A.hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
            D.write_json(root/'outputs/agents/responses/fixture.json',{'request_hash':digest,
                         'envelope':{'model':P.AGENT['model'],'response':'unverified'}})
            with patch.object(P,'OUT',root/'outputs'),patch.object(P,'WORKSPACE',root),patch.object(A,'require_transport',return_value={'actual_model':P.AGENT['model']}),patch.object(A.subprocess,'run') as run:
                with self.assertRaisesRegex(ValueError,'completed transport journal'):
                    A._call(request,A.claude_transport)
                run.assert_not_called()

    def test_amendment_chain_preserves_original_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); out=root/'outputs'; out.mkdir()
            archive=root/'source.zip'; archive.write_bytes(b'fixture')
            (root/'params.py').write_text('original')
            D.write_json(out/'timing_approval.json',{'selection_end':P.SELECTION_END})
            with patch.object(P,'ROOT',root),patch.object(P,'OUT',out),patch.object(P,'SOURCE_ARCHIVE',archive),patch.object(P,'SOURCE_SHA256',D.sha256(archive)):
                old=D.stage0(); original_bytes=(out/'prereg_v0.json').read_bytes()
                (out/'prereg').mkdir()
                (out/'prereg/params_v0.py').write_text('original')
                (root/'params.py').write_text('changed')
                with self.assertRaises(RuntimeError): D.stage0()
                snapshot=out/'params_v1.py'; snapshot.write_text('changed')
                record={'approved':True,'user_approval':'approved','previous_record_sha256':D.sha256(out/'prereg_v0.json'),
                        'previous_params_sha256':old['params_sha256'],'params_sha256':D.sha256(snapshot),
                        'params_snapshot':'outputs/params_v1.py'}
                amendment=out/'prereg_amendments/001.json'; D.write_json(amendment,record)
                D.stage0()
                self.assertEqual((out/'prereg_v0.json').read_bytes(),original_bytes)
                (out/'prereg/params_v0.py').write_text('tampered')
                with self.assertRaisesRegex(RuntimeError,'Original parameter snapshot'): D.stage0()
                (out/'prereg/params_v0.py').write_text('original')
                record['previous_record_sha256']='tampered'; D.write_json(amendment,record)
                with self.assertRaisesRegex(RuntimeError,'chain'): D.stage0()


if __name__=='__main__':
    unittest.main()
