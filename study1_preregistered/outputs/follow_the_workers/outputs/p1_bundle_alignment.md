Find mapping errors, timestamp or look-ahead errors, and code bugs in the material below.
For each problem, give the exact line or row, why it is wrong, and a test that would confirm it.
Do not report style issues.

Manifest:
```csv
source,id,url,group,measure,frequency,observation_start,observation_end,first_vintage,admitted,reason,mapping_quality,flags
FRED/ALFRED provided archive,JTU110099JOR,https://fred.stlouisfed.org/series/JTU110099JOR,1.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU110099HIR,https://fred.stlouisfed.org/series/JTU110099HIR,1.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU110099QUR,https://fred.stlouisfed.org/series/JTU110099QUR,1.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU110099LDR,https://fred.stlouisfed.org/series/JTU110099LDR,1.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU1000000007,https://fred.stlouisfed.org/series/CEU1000000007,1.0,H,monthly,1947-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU1000000008,https://fred.stlouisfed.org/series/CEU1000000008,1.0,E,monthly,1947-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU2300JOR,https://fred.stlouisfed.org/series/JTU2300JOR,2.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU2300HIR,https://fred.stlouisfed.org/series/JTU2300HIR,2.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU2300QUR,https://fred.stlouisfed.org/series/JTU2300QUR,2.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU2300LDR,https://fred.stlouisfed.org/series/JTU2300LDR,2.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU2000000007,https://fred.stlouisfed.org/series/CEU2000000007,2.0,H,monthly,1947-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CES2000000008,https://fred.stlouisfed.org/series/CES2000000008,2.0,E,monthly,1947-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,seasonally adjusted construction earnings exception
FRED/ALFRED provided archive,JTU3200JOR,https://fred.stlouisfed.org/series/JTU3200JOR,3.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3200HIR,https://fred.stlouisfed.org/series/JTU3200HIR,3.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3200QUR,https://fred.stlouisfed.org/series/JTU3200QUR,3.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3200LDR,https://fred.stlouisfed.org/series/JTU3200LDR,3.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU3100000007,https://fred.stlouisfed.org/series/CEU3100000007,3.0,H,monthly,1939-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU3100000008,https://fred.stlouisfed.org/series/CEU3100000008,3.0,E,monthly,1939-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3400JOR,https://fred.stlouisfed.org/series/JTU3400JOR,4.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3400HIR,https://fred.stlouisfed.org/series/JTU3400HIR,4.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3400QUR,https://fred.stlouisfed.org/series/JTU3400QUR,4.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU3400LDR,https://fred.stlouisfed.org/series/JTU3400LDR,4.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU3200000007,https://fred.stlouisfed.org/series/CEU3200000007,4.0,H,monthly,1939-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,Hshld approximate,
FRED/ALFRED provided archive,CEU3200000008,https://fred.stlouisfed.org/series/CEU3200000008,4.0,E,monthly,1939-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,Hshld approximate,
FRED/ALFRED provided archive,JTU4200JOR,https://fred.stlouisfed.org/series/JTU4200JOR,5.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4200HIR,https://fred.stlouisfed.org/series/JTU4200HIR,5.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4200QUR,https://fred.stlouisfed.org/series/JTU4200QUR,5.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4200LDR,https://fred.stlouisfed.org/series/JTU4200LDR,5.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU4142000007,https://fred.stlouisfed.org/series/CEU4142000007,5.0,H,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU4142000008,https://fred.stlouisfed.org/series/CEU4142000008,5.0,E,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4400JOR,https://fred.stlouisfed.org/series/JTU4400JOR,6.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4400HIR,https://fred.stlouisfed.org/series/JTU4400HIR,6.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4400QUR,https://fred.stlouisfed.org/series/JTU4400QUR,6.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU4400LDR,https://fred.stlouisfed.org/series/JTU4400LDR,6.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU4200000007,https://fred.stlouisfed.org/series/CEU4200000007,6.0,H,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU4200000008,https://fred.stlouisfed.org/series/CEU4200000008,6.0,E,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU480099JOR,https://fred.stlouisfed.org/series/JTU480099JOR,7.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU480099HIR,https://fred.stlouisfed.org/series/JTU480099HIR,7.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU480099QUR,https://fred.stlouisfed.org/series/JTU480099QUR,7.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU480099LDR,https://fred.stlouisfed.org/series/JTU480099LDR,7.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU4300000007,https://fred.stlouisfed.org/series/CEU4300000007,7.0,H,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES excludes utilities,
FRED/ALFRED provided archive,CEU4300000008,https://fred.stlouisfed.org/series/CEU4300000008,7.0,E,monthly,1972-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES excludes utilities,
FRED/ALFRED provided archive,JTU5100JOR,https://fred.stlouisfed.org/series/JTU5100JOR,8.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5100HIR,https://fred.stlouisfed.org/series/JTU5100HIR,8.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5100QUR,https://fred.stlouisfed.org/series/JTU5100QUR,8.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5100LDR,https://fred.stlouisfed.org/series/JTU5100LDR,8.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU5000000007,https://fred.stlouisfed.org/series/CEU5000000007,8.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU5000000008,https://fred.stlouisfed.org/series/CEU5000000008,8.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5200JOR,https://fred.stlouisfed.org/series/JTU5200JOR,9.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5200HIR,https://fred.stlouisfed.org/series/JTU5200HIR,9.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5200QUR,https://fred.stlouisfed.org/series/JTU5200QUR,9.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5200LDR,https://fred.stlouisfed.org/series/JTU5200LDR,9.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU5500000007,https://fred.stlouisfed.org/series/CEU5500000007,9.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES financial activities,shared CES
FRED/ALFRED provided archive,CEU5500000008,https://fred.stlouisfed.org/series/CEU5500000008,9.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES financial activities,shared CES
FRED/ALFRED provided archive,JTU5300JOR,https://fred.stlouisfed.org/series/JTU5300JOR,10.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5300HIR,https://fred.stlouisfed.org/series/JTU5300HIR,10.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5300QUR,https://fred.stlouisfed.org/series/JTU5300QUR,10.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU5300LDR,https://fred.stlouisfed.org/series/JTU5300LDR,10.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU5500000007,https://fred.stlouisfed.org/series/CEU5500000007,10.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,shared CES with group 9,shared CES
FRED/ALFRED provided archive,CEU5500000008,https://fred.stlouisfed.org/series/CEU5500000008,10.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,shared CES with group 9,shared CES
FRED/ALFRED provided archive,JTU540099JOR,https://fred.stlouisfed.org/series/JTU540099JOR,11.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU540099HIR,https://fred.stlouisfed.org/series/JTU540099HIR,11.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU540099QUR,https://fred.stlouisfed.org/series/JTU540099QUR,11.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU540099LDR,https://fred.stlouisfed.org/series/JTU540099LDR,11.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU6000000007,https://fred.stlouisfed.org/series/CEU6000000007,11.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU6000000008,https://fred.stlouisfed.org/series/CEU6000000008,11.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU6200JOR,https://fred.stlouisfed.org/series/JTU6200JOR,12.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU6200HIR,https://fred.stlouisfed.org/series/JTU6200HIR,12.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU6200QUR,https://fred.stlouisfed.org/series/JTU6200QUR,12.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU6200LDR,https://fred.stlouisfed.org/series/JTU6200LDR,12.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU6500000007,https://fred.stlouisfed.org/series/CEU6500000007,12.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES includes private education,
FRED/ALFRED provided archive,CEU6500000008,https://fred.stlouisfed.org/series/CEU6500000008,12.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES includes private education,
FRED/ALFRED provided archive,JTU7200JOR,https://fred.stlouisfed.org/series/JTU7200JOR,13.0,JOR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU7200HIR,https://fred.stlouisfed.org/series/JTU7200HIR,13.0,HIR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU7200QUR,https://fred.stlouisfed.org/series/JTU7200QUR,13.0,QUR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,JTU7200LDR,https://fred.stlouisfed.org/series/JTU7200LDR,13.0,LDR,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,exact,
FRED/ALFRED provided archive,CEU7000000007,https://fred.stlouisfed.org/series/CEU7000000007,13.0,H,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES includes leisure,
FRED/ALFRED provided archive,CEU7000000008,https://fred.stlouisfed.org/series/CEU7000000008,13.0,E,monthly,1964-01-01,2026-08-01,2011-03-04,True,cached vintage audit; live metadata confirmation separately tracked,CES includes leisure,
FRED/ALFRED provided archive,JTSJOL,https://fred.stlouisfed.org/series/JTSJOL,0.0,JTSJOL,monthly,2000-12-01,2026-07-01,2010-08-11,True,cached vintage audit; live metadata confirmation separately tracked,national,
FRED/ALFRED provided archive,UNEMPLOY,https://fred.stlouisfed.org/series/UNEMPLOY,0.0,UNEMPLOY,monthly,1948-01-01,2026-08-01,1961-02-09,True,cached vintage audit; live metadata confirmation separately tracked,national,
LinkUp_Tier1,LinkUp_Tier1,,,,,,,,False,No collection-success/failure history; PIT mapping and cohort gates unverified,,
LinkUp_Tier2,LinkUp_Tier2,,,,,,,,False,No dated historical snapshots/version history,,
WARN,WARN,,,,,,,,False,No amendment history or dated mapping; group coverage unverified,,
F6,F6,,,,,,,,False,Only three bundled PPI candidates; first vintages after research snapshot; discovery incomplete,,
A5,A5,,,,,,,,False,Optional LightGBM not installed; no extra dependency requested,,
Ken French data library,industry,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,monthly,1926-07,2026-08,,True,Pinned official archive; date fields checked without parsing return values,fixed prescribed French membership,research portfolios are not directly tradable
Ken French data library,ff5,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip,,,monthly,1963-07,2026-08,,True,Pinned official archive; date fields checked without parsing return values,fixed prescribed French membership,research portfolios are not directly tradable
Ken French data library,momentum,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip,,,monthly,1927-01,2026-08,,True,Pinned official archive; date fields checked without parsing return values,fixed prescribed French membership,research portfolios are not directly tradable
Ken French excluded portfolio,Agric,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,outside nonfarm JOLTS,,
Ken French excluded portfolio,Other,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Ken French excluded portfolio,Boxes,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Ken French excluded portfolio,Books,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Ken French excluded portfolio,Softw,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Ken French excluded portfolio,Fun,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Ken French excluded portfolio,PerSv,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip,,,,,,,False,ambiguous SIC/NAICS scope,,
Provided crosswalk documentation,Siccodes49.txt,https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes49.zip,,,static,,,,True,Documentation only; pinned source archive,,Does not imply exact economic scope for approximate groups
Provided crosswalk documentation,1987_SIC_to_2002_NAICS.xls,https://www.census.gov/naics/concordances/1987_SIC_to_2002_NAICS.xls,,,static,,,,True,Documentation only; pinned source archive,,Does not imply exact economic scope for approximate groups
```
Crosswalk:
```csv
group,name,JOLTS_code,French_members,CES_code,match
1,Mining and logging,110099,Gold Mines Coal Oil,10000000,exact
2,Construction,2300,Cnstr,20000000,exact
3,Durable manufacturing,3200,Toys BldMt Steel FabPr Mach ElcEq Autos Aero Ships Guns Hardw Chips LabEq MedEq,31000000,exact
4,Nondurable manufacturing,3400,Food Soda Beer Smoke Hshld Clths Drugs Chems Rubbr Txtls Paper,32000000,Hshld approximate
5,Wholesale trade,4200,Whlsl,41420000,exact
6,Retail trade,4400,Rtail,42000000,exact
7,"Transportation, warehousing and utilities",480099,Trans Util,43000000,CES excludes utilities
8,Information,5100,Telcm,50000000,exact
9,Finance and insurance,5200,Banks Insur Fin,55000000,CES financial activities
10,Real estate and rental and leasing,5300,RlEst,55000000,shared CES with group 9
11,Professional and business services,540099,BusSv,60000000,exact
12,Health care and social assistance,6200,Hlth,65000000,CES includes private education
13,Accommodation and food services,7200,Meals,70000000,CES includes leisure
```
As-of code:
```python
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
```
