"""P1 regression checks using temporary labor-vintage fixtures, never returns."""
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

import pandas as pd

PROJECT = Path(__file__).resolve().parents[1] / 'outputs/follow_the_workers_opus55_xhigh'
sys.path.insert(0,str(PROJECT))
import data as D
import params as P


class P1FixTests(unittest.TestCase):
    def test_blank_date_columns_raise_clear_validation_error(self):
        for column in ['date','realtime_start','realtime_end']:
            with self.subTest(column=column),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);folder=root/'provided/4_alfred_vintages';folder.mkdir(parents=True)
                frame=pd.DataFrame({'date':['2010-01-01','2010-02-01'],
                    'realtime_start':['2010-02-01','2010-03-01'],
                    'realtime_end':['9999-12-31','9999-12-31'],'value':['1','2']})
                frame.loc[1,column]=''
                frame.to_csv(folder/'fixture.csv',index=False)
                with patch.object(P,'CACHE',root),self.assertRaisesRegex(ValueError,'ISO calendar dates'):
                    D.read_vintage('fixture')

    def test_manifest_flags_apply_to_the_actual_series(self):
        history=pd.DataFrame({'date':['2010-01-01'],'realtime_start':['2011-03-04']})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);cache=root/'cache';(cache/'french').mkdir(parents=True)
            # Keep this mapping check independent of omitted source archives.
            for name in P.PUBLIC_URLS:
                with zipfile.ZipFile(cache/'french'/(name+'.zip'),'w') as archive:
                    archive.writestr('fixture.csv','200405,DO_NOT_PARSE\n202608,DO_NOT_PARSE\n')
            definitions=cache/'provided/2_definitions';definitions.mkdir(parents=True)
            for name in ['Siccodes49.txt','1987_SIC_to_2002_NAICS.xls']:
                (definitions/name).write_text('fixture')
            with patch.object(P,'CACHE',cache),patch.object(P,'OUT',root),patch.object(D,'read_vintage',return_value=history):
                manifest=D.manifest().fillna('')
        construction=manifest.loc[manifest.id.eq('CES2000000008')]
        self.assertEqual(len(construction),1)
        self.assertIn('seasonally adjusted',construction.iloc[0]['flags'])
        shared=manifest.loc[manifest['flags'].eq('shared CES')]
        self.assertEqual(len(shared),4)
        self.assertEqual(set(shared.id),{'CEU5500000007','CEU5500000008'})
        self.assertTrue(manifest.loc[manifest.id.str.startswith('JTU'),'flags'].eq('').all())


if __name__=='__main__':
    unittest.main()
