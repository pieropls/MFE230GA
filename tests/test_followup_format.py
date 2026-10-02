"""The follow-up clarifies formatting without relaxing validation."""
import ast
from pathlib import Path
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1] / 'outputs/follow_the_workers_opus55_xhigh'
sys.path.insert(0,str(PROJECT))
import agents as A
import params as P

class FollowupFormatTests(unittest.TestCase):
    def test_ranking_information_is_statistical_language(self):
        self.assertTrue(A.leak_check('The signal itself carried no ranking information.'))
        for text in ['The ranking information industry is weak.', 'The information sector', 'V01 identifies Information']:
            with self.subTest(text=text),self.assertRaises(ValueError):
                A.leak_check(text)

    def test_candidate_contract_is_explicit_and_limits_unchanged(self):
        request=A._request("independent",1,"Temporal",1,[{"id":"V01","type":"index"}],[],[])
        self.assertIn("bare JSON object without Markdown code fences",request["system"])
        self.assertEqual((P.AGENT["hypothesis_word_limit"],P.AGENT["falsification_word_limit"],P.AGENT["migration_word_limit"]),(40,30,120))
        self.assertEqual((P.AGENT["model"],P.AGENT["effort"]),("claude-opus-5-5","xhigh"))

    def test_judge_contract_matches_existing_validator(self):
        source=(PROJECT/"agents.py").read_text()
        fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=="trace_migrations")
        strings=[n.value for n in ast.walk(fn) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        claim=next(s for s in strings if s.startswith("Assess whether"))
        failure=next(s for s in strings if s.startswith("Determine whether"))
        self.assertIn("array of integer claim numbers, never quoted strings",claim)
        self.assertIn("JSON boolean or null, never a quoted string",failure)
        self.assertIn("type(i) is not int",source)
        self.assertNotIn("strip('\\`')",source)

if __name__=="__main__":unittest.main()
