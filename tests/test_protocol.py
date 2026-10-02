"""Offline protocol regressions; only synthetic inputs, no model or return-file access."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1] / 'outputs/follow_the_workers_opus55_xhigh'
sys.path.insert(0,str(PROJECT))
import params as P
import data as D
import agents as A


class ProtocolChecks(unittest.TestCase):
    def test_new_prompts_state_limits_without_old_run_context(self):
        request=A._request('independent',1,'Temporal',1,[{'id':'V01','type':'index'}],[],[])
        payload=request['system']+'\n'+request['prompt']
        self.assertIn('at most 40 words',payload)
        self.assertIn('at most 30 words',payload)
        self.assertIn('Words are counted by whitespace',payload)
        self.assertIn('including headings',P.MIGRATION_PROMPT)
        for forbidden in ['technical run','old run','restart','72 attempts']:
            self.assertNotIn(forbidden,payload.lower())
        self.assertTrue(A.leak_check(payload))

    def test_run_identity_separates_journals(self):
        with patch.dict(P.AGENT,{'run_id':'fixture_one'}):
            first=A.research_call_root()
        with patch.dict(P.AGENT,{'run_id':'fixture_two'}):
            second=A.research_call_root()
        self.assertNotEqual(first,second)
        self.assertNotIn('claude_research_calls',str(first))
        with patch.dict(P.AGENT,{'run_id':'../previous'}),self.assertRaises(ValueError):
            A.research_call_root()

    def test_crosswalk_discloses_scope_without_remapping_baskets(self):
        groups=[{'group':row[0],'assessment':'Approximate SIC portfolio proxy',
                 'outside_scope_rows':1,'correspondence_rows':2} for row in P.GROUPS]
        with tempfile.TemporaryDirectory() as directory,patch.object(P,'OUT',Path(directory)):
            D.write_json(P.OUT/'census_crosswalk_check.json',{'groups':groups})
            result=D.crosswalk()
            self.assertEqual(result.French_members.tolist(),[row[3] for row in P.GROUPS])
            self.assertTrue(result.verified_French_scope.eq('Approximate SIC portfolio proxy').all())
            self.assertIn('prescribed_match',result)
            self.assertNotIn('match',result)
            D.write_json(P.OUT/'census_crosswalk_check.json',{'groups':groups[:-1]})
            with self.assertRaisesRegex(ValueError,'does not cover'):
                D.crosswalk()

    def test_pause_and_alignment_are_hard_gates(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(P,'OUT',Path(directory)):
            with self.assertRaisesRegex(PermissionError,'alignment'):
                A.require_transport()
            D.write_json(P.OUT/'PAUSED.json',{'status':'paused'})
            with self.assertRaisesRegex(PermissionError,'paused'):
                A.require_transport()

    def test_statistical_language_is_not_an_identifier_leak(self):
        for text in ['HAC and NW statistics are weak.', 'The information coefficient was nonpositive.',
                     'Signal construction failed.', 'Feature construction failed.',
                     'Spread-based construction did not improve stability.', 'Coverage AND stability matter.']:
            with self.subTest(text=text):
                self.assertTrue(A.leak_check(text))

    def test_actual_identities_and_selection_feedback_remain_blocked(self):
        for text in ['Construction', 'The construction sector', 'The information industry', 'Microsoft',
                     'JTU2300JOR', 'LinkUp', 'FRED', '2014-10-31', 'October 2014', 'AAPL',
                     'first_half_ic', 'second_half_ic', 'half-sample IC',
                     'The information coefficient for construction is weak.']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                A.leak_check(text)

    def test_only_registered_submission_limits(self):
        spec={'name':'descriptive '*15, 'hypothesis':'word '*40, 'falsified_if':'word '*30,
              'expression':'lag('+' '*1100+'V01, 1)'}
        A.validate_spec(spec,{'V01'})
        for field,count in [('hypothesis',41),('falsified_if',31)]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError,field):
                A.validate_spec({**spec,field:'word '*count},{'V01'})

    def test_migration_prose_vs_formulas(self):
        valid=[
            '* One attempt failed to improve stability.',
            'The high-T regime (the upper group) did not improve stability.',
            'The ratio (V03 versus V04) failed to improve stability.',
            'V02-versus-V04 comparisons failed to improve stability.',
            'The information coefficient and HAC statistic were weak; the signal failed.',
            'Nothing improved stability.',
        ]
        for report in valid:
            with self.subTest(report=report):
                self.assertEqual(A.validate_migration(report),[])
        invalid=[
            'An attempt failed. Try lag(V01, 1).',
            'An attempt failed. Try V01 + V02.',
            'An attempt failed. Try V01*2.',
            'An attempt failed. Try 2 / V01.',
            'An attempt failed. Try V01 = 2.',
            'An attempt failed. ```python\nprint(1)\n```',
            'An attempt failed.\nimport os',
            'No failures occurred.',
            'Every attempt worked.',
        ]
        for report in invalid:
            with self.subTest(report=report):
                self.assertTrue(A.validate_migration(report))
        self.assertEqual(A.validate_migration('Failed. '+'word '*119),[])
        self.assertTrue(any('121' in reason for reason in A.validate_migration('Failed. '+'word '*120)))

    def test_full_schedule_migration_delivery_feedback_and_cache(self):
        months=pd.period_range('2001-01',periods=180,freq='M')
        rng=np.random.default_rng(230)
        values=pd.DataFrame(rng.uniform(1,5,(len(months),13)),index=months)
        target=pd.DataFrame(rng.normal(size=values.shape),index=months)
        tightness=pd.Series(np.sin(np.arange(len(months))/20),index=months)
        calls=[]
        def transport(request):
            calls.append(request)
            if request['kind']=='migration':
                response='* The information coefficient and HAC statistic were weak. Signal construction failed to improve stability.'
            else:
                hypothesis='word '*41 if request['submission']==1 else 'Changes predict relative rankings.'
                response=json.dumps({'name':'fixture','hypothesis':hypothesis,
                                     'falsified_if':'The HAC statistic is nonpositive.','expression':'yoy(V01)'})
            return {'response':response,'model':'synthetic-model'}
        with tempfile.TemporaryDirectory() as directory, patch.object(P,'OUT',Path(directory)), patch.object(A,'require_transport',return_value={'actual_model':'synthetic-model'}):
            dictionary=[{'id':'V01','type':'index','common':False}]
            specs,_,reports=A.run_experiment({'V01':values},tightness,dictionary,target,{'F1':values},transport)
            self.assertEqual(len(specs),108)
            self.assertEqual(sum(row['valid'] for row in specs),90)
            self.assertEqual(len(reports),18)
            self.assertTrue(all(row['valid'] for row in reports))
            self.assertEqual(len(calls),126)
            for request in calls:
                if request['kind']!='candidate':continue
                if request['submission']==2:
                    self.assertIn('41',request['prompt'])
                    self.assertIn('word word',request['prompt'])
                delivered='Signal construction failed' in request['prompt']
                self.assertEqual(delivered,request['arm']=='islands' and request['submission']>=3)
                self.assertNotIn('first_half_ic',request['prompt'])
            A.run_experiment({'V01':values},tightness,dictionary,target,{'F1':values},transport)
            self.assertEqual(len(calls),126)
            self.assertEqual(A.audit_agent_prompts()['candidate_calls'],108)
            # Cache identity includes every prompt: a changed prompt cannot replay the old call.
            request=calls[0].copy();request['prompt']+=' Different instructions.'
            with self.assertRaisesRegex(ValueError,'different prompt'):
                A._call(request,transport)

    def test_invalid_receiving_submissions_remain_in_tracing_population(self):
        report={'report_id':'r','valid':True,'seed':1,'agent':'Temporal','after_submission':2,
                'text':'An earlier contrast failed to improve stability.'}
        spec={'name':'test','hypothesis':'This contrast avoids the earlier failure.',
              'falsified_if':'No improvement.', 'expression':'V01+V02'}
        rows=[{'candidate_id':'parseable_invalid','arm':'islands','seed':1,'agent':'Composition',
               'submission':3,'valid':False,'spec':spec,'research_mean_ic':None},
              {'candidate_id':'unparseable','arm':'islands','seed':1,'agent':'Composition',
               'submission':4,'valid':False,'spec':None,'research_mean_ic':None},
              {'candidate_id':'unsafe','arm':'islands','seed':1,'agent':'Interactions',
               'submission':3,'valid':False,'spec':{**spec,'hypothesis':'Construction sector'},'research_mean_ic':None}]
        calls=[]
        def transport(request):
            calls.append(request)
            response={'avoids_failure':True} if request['call_id'].endswith('_failure') else {'uses_claim':True,'claim_ids':[1]}
            return {'response':json.dumps(response),'model':'synthetic-model'}
        with tempfile.TemporaryDirectory() as directory, patch.object(P,'OUT',Path(directory)), patch.object(A,'require_transport',return_value={'actual_model':'synthetic-model'}):
            judgments=A.trace_migrations(rows,[report],transport)
            self.assertEqual(len(judgments),3)
            self.assertEqual(len(calls),2)
            self.assertEqual(sum(row['uses_claim'] is None for row in judgments),2)
            for row in judgments:
                if row['human_review_required']:row['human_uses_claim']=row['uses_claim']
            D.write_json(P.OUT/'agents/migration_judgments.json',judgments)
            summary,review=A.summarize_migrations(rows,[report],judgments)
            self.assertEqual(summary['n'],3)
            self.assertEqual(summary['defined_judgments'],1)
            self.assertEqual(summary['uptake_rate'],1)
            self.assertIsNone(summary['improvement_with_uptake'])
            self.assertTrue(review['complete'])
            self.assertEqual(review['total_judgments'],1)

    def test_syntax_budget_replay_and_separate_run_caches(self):
        months=pd.period_range('2001-01',periods=180,freq='M')
        rng=np.random.default_rng(230)
        frame=pd.DataFrame(rng.uniform(1,5,(len(months),13)),index=months)
        t=pd.Series(-1.,index=months)
        calls=[]
        def transport(request):
            calls.append(request)
            # First proposal is repaired once; the second remains invalid after its repair.
            if request['submission']<=2:
                response='not valid' if request['submission']==2 or not request['call_id'].endswith('_syntax_retry') else json.dumps({'name':'fixture','hypothesis':'Changes predict ranks.','falsified_if':'Nonpositive IC.','expression':'yoy(V01)'})
            else:
                response=json.dumps({'name':'fixture','hypothesis':'Construction sector','falsified_if':'Nonpositive IC.','expression':'yoy(V01)'})
            return {'response':response,'model':'synthetic-model'}
        settings={**P.AGENT,'arms':['independent'],'seeds':[1],'emphases':['Temporal']}
        with tempfile.TemporaryDirectory() as directory, patch.object(P,'AGENT',settings), patch.object(A,'require_transport',return_value={'actual_model':'synthetic-model'}):
            for folder in ['first','second']:
                with patch.object(P,'OUT',Path(directory)/folder):
                    specs,_,_=A.run_experiment({'V01':frame},t,[],frame,{'F1':frame},transport)
                    self.assertEqual(len(specs),6)
                    self.assertEqual(sum(row['valid'] for row in specs),1)
                    before=len(calls)
                    A.run_experiment({'V01':frame},t,[],frame,{'F1':frame},transport)
                    self.assertEqual(len(calls),before)
            self.assertEqual(len(calls),16)
            self.assertTrue(all('Construction sector' not in request['prompt'] for request in calls))

    def test_startup_obeys_registered_risk_target(self):
        rng=np.random.default_rng(230)
        months=pd.period_range('2000-01',periods=100,freq='M')
        market=pd.Series(rng.normal(.004,.03,100),index=months)
        total=pd.DataFrame(rng.normal(.004,.03,(100,13))+market.to_numpy()[:,None],index=months)
        factors=pd.DataFrame({'Mkt-RF':market,'RF':.002},index=months)
        returns={'total':total,'excess':total.sub(factors.RF,axis=0),'factors':factors}
        scores=pd.DataFrame([np.arange(13)],index=months[-1:],columns=total.columns)
        one,one_weights=D.backtest(scores,returns,holding=1)
        three,three_weights=D.backtest(scores,returns,holding=3)
        np.testing.assert_allclose(one_weights,three_weights)
        self.assertTrue(np.isclose(three.ex_ante_vol.iloc[0],P.PORTFOLIO['vol_target']) or np.isclose(three.gross_leverage.iloc[0],P.PORTFOLIO['gross_cap']))

    def test_manifest_records_all_sources_without_parsing_sealed_values(self):
        history=pd.DataFrame({'date':['2010-01-01'],'realtime_start':['2011-03-04']})
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);cache=root/'cache';(cache/'french').mkdir(parents=True)
            for name in P.PUBLIC_URLS:
                with zipfile.ZipFile(cache/'french'/(name+'.zip'),'w') as archive:
                    archive.writestr('fixture.csv','200405,DO_NOT_PARSE\n202608,DO_NOT_PARSE\n')
            definitions=cache/'provided/2_definitions';definitions.mkdir(parents=True)
            for name in ['Siccodes49.txt','1987_SIC_to_2002_NAICS.xls']:(definitions/name).write_text('fixture')
            with patch.object(P,'CACHE',cache),patch.object(P,'OUT',root),patch.object(D,'read_vintage',return_value=history):
                manifest=D.manifest()
                self.assertTrue(set(P.PUBLIC_URLS).issubset(set(manifest.id)))
                self.assertTrue(set(P.EXCLUDED_FRENCH).issubset(set(manifest.id)))
                D.write_json(root/'live_vintage_confirmation.json',[])
                with self.assertRaisesRegex(ValueError,'exact core series'):D.manifest()

    def test_p1_required_before_panel_preparation(self):
        notebook=json.loads((PROJECT/'run.ipynb').read_text())
        cell=next(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code' and 'D.build_asof_panel(variant)' in ''.join(c['source']))
        self.assertTrue(cell.startswith('A.require_p1_audit()'))
        with tempfile.TemporaryDirectory() as directory,patch.object(P,'OUT',Path(directory)):
            with self.assertRaisesRegex(PermissionError,'P1 audit'):A.require_p1_audit()


if __name__=='__main__':
    unittest.main()
