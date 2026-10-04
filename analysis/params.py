"""Constants for Study 2 (the post-hoc iteration): paths, dates, lags, portfolio settings and variant definitions.

Nothing here reads data. The portfolio settings mirror the frozen study's params.py and are
checked against it in run.ipynb (Gate 1).
"""
import re
from pathlib import Path

# ---------- paths ----------
ROOT = Path(__file__).resolve().parent              # analysis/
PROJECT = ROOT.parent
FROZEN_REPO = PROJECT / 'study1_preregistered'     # Study 1 (Alex's preregistered study): read-only, never written
SONNET = FROZEN_REPO / 'outputs' / 'follow_the_workers'            # confirmatory study
OPUS = FROZEN_REPO / 'outputs' / 'follow_the_workers_opus55_xhigh'  # exploratory follow-up
SEALED = SONNET / 'outputs' / 'sealed' / 'initial'
# SHA-256 over (relative path, file hash) of every file in the frozen repo except .git, taken
# on 3 Oct 2026 before any v2 work. Gate 1 checks it is unchanged.
FROZEN_FINGERPRINT = ('eb109be969176412635ab80c03e0e37c6a006aedca740f671ed2908c371fbd9a', 3067)
DATA = ROOT / 'data'
FRENCH = DATA / 'french'
FRED = DATA / 'fred'                                 # current (revised) FRED, downloaded 3 Oct 2026
VINTAGE_DATE = '2026-09-29'                          # day before the 30 Sep 2026 decision
FRED_VINTAGE = DATA / f'alfred_{VINTAGE_DATE}'       # ALFRED as known on VINTAGE_DATE (forward book)
PACKAGE = DATA / 'alex_package'                      # Alex's data package (as-known panels, vintages); may be absent
SPECS = ROOT / 'specs'                               # every frozen (hashed) specification
OUT = ROOT / 'output'
OUT1, OUT2, FORWARD = OUT / 'study1', OUT / 'study2', OUT / 'forward'
TABLES1, TABLES2 = OUT1 / 'tables', OUT2 / 'tables'
REPORT = PROJECT / 'report'
FIGS = REPORT / 'figures'
TEX = REPORT / 'tables'

# ---------- dates (earning months: a decision at the end of month m-1 earns month m) ----------
WINDOWS = {
    'research': ('2004-05', '2014-09'),
    'test': ('2014-11', '2026-08'),
    'full': ('2004-05', '2026-08'),
    'post-2010': ('2010-01', '2026-08'),
    'last 18m': ('2025-03', '2026-08'),
}
SIGNAL_START = '2002-04'          # first DECISION month of signal history (frozen FEATURE_START)
FORWARD_DECISION = '2026-09'      # decision at end of Sep 2026 -> first earning month Oct 2026

# ---------- universe (same 13 groups, codes and French members as the frozen study) ----------
GROUPS = {
    1: ('Mining & logging', '110099', '10000000', 'Gold Mines Coal Oil'),
    2: ('Construction', '2300', '20000000', 'Cnstr'),
    3: ('Durable mfg', '3200', '31000000', 'Toys BldMt Steel FabPr Mach ElcEq Autos Aero Ships Guns Hardw Chips LabEq MedEq'),
    4: ('Nondurable mfg', '3400', '32000000', 'Food Soda Beer Smoke Hshld Clths Drugs Chems Rubbr Txtls Paper'),
    5: ('Wholesale', '4200', '41420000', 'Whlsl'),
    6: ('Retail', '4400', '42000000', 'Rtail'),
    7: ('Transport & utilities', '480099', '43000000', 'Trans Util'),
    8: ('Information', '5100', '50000000', 'Telcm'),
    9: ('Finance & insurance', '5200', '55000000', 'Banks Insur Fin'),
    10: ('Real estate', '5300', '55000000', 'RlEst'),
    11: ('Prof. & business svcs', '540099', '60000000', 'BusSv'),
    12: ('Health care', '6200', '65000000', 'Hlth'),
    13: ('Accommodation & food', '7200', '70000000', 'Meals'),
}
NAMES = {g: v[0] for g, v in GROUPS.items()}
JOLTS_MEASURES = ['JOR', 'HIR', 'QUR', 'LDR']        # F1 openings, F2 hires, F3 quits, F4 layoffs
CONSTRUCTION_EARNINGS = 'CES2000000008'              # SA exception, as in the frozen study

# ---------- signal construction (as in the frozen study) ----------
JOLTS_LAG = 2      # JOLTS month m-2 is the latest usable at the end of month m (fixed-lag rule)
CES_LAG = 1        # CES month m-1
STD_MIN_MONTHS = 24
WINSOR = 3.0
MIN_GROUPS = 11

# ---------- portfolio (must equal the frozen params.PORTFOLIO; asserted in Gate 1) ----------
PORTFOLIO = {'longs': 3, 'shorts': 3, 'holding': 3, 'risk_window': 60, 'risk_min_months': 36,
             'vol_target': 0.10, 'gross_cap': 2.0, 'cost_bps': 10, 'hedge_cost_bps': 2}
COST_GRID_BPS = [0, 10, 25]

# ---------- inference ----------
SEED = 230              # the frozen study's seed; used by the block bootstrap
HAC_LAGS = 6
PLACEBO_MIN_SHIFT = 24
N_TRIALS = 112          # ~108 diagnostic looks already taken + the 4 v2 variants
HORIZONS = [1, 3, 6, 12]

# ---------- labels and colours ----------
CONFIRMATORY, POSTHOC, FORWARD_TEST = 'CONFIRMATORY', 'POST-HOC', 'FORWARD TEST'
COLORS = {CONFIRMATORY: '#1F4E79', POSTHOC: '#B35C00', FORWARD_TEST: '#2E7D32',
          'grey': '#7F7F7F', 'lightgrey': '#BFBFBF', 'darkgrey': '#404040'}
FULL_WIDTH, HALF_WIDTH = 6.5, 3.2   # inches

# ---------- v2 variants (definitions are frozen in v2_spec.md; this is only the registry) ----------
VARIANTS = {
    'V2a': 'Cross-sectional rank of W (headline)',
    'V2b': 'Equal-weight composite of z(F1..F5, W), each signed by its research-period IC',
    'V2c': 'Equal-rank composite of W and industry momentum 12-1',
    'V2d': '-(z(F2)+z(F3))/2, held 12 months (12 tranches)',
}


# ---------- names (presentation layer; frozen result files keep the original codes inside) ----------
DISPLAY = {'V2a': 'W', 'V2b': 'SC', 'V2c': 'W+MOM', 'V2d': 'HQ12', 'islands (communicating)': 'communicating (treatment)', 'Islands': 'Communicating', 'islands': 'communicating',
           'island-arm': 'communicating-arm', 'island agents': 'communicating agents', 'Study 1 (Sonnet)': 'Study 1', 'Study 1b (Opus)': 'Study 1b', 'Sonnet': 'Study 1', 'Opus': 'Study 1b'}
STRATEGY_NAMES = {'A0': 'A0 fixed rule', 'A1': 'A1 ridge', 'A1-T': 'A1-T ridge x tightness',
                  'A3': 'A3 agent features, independent (primary)', 'A4': 'A4 agent features, communicating',
                  'W': 'W wage growth (declared headline)', 'SC': 'SC signed composite',
                  'W+MOM': 'W+MOM wage growth + momentum', 'HQ12': 'HQ12 hires + quits reversal, 12-month hold'}


def display(text):
    """Old variant codes -> new names, for figures, LaTeX fragments and new outputs."""
    for old, new in DISPLAY.items():
        text = text.replace(old, new)
    return text


def table_path(name):
    """CSV path of a result table: d1..d10 are Study 1 diagnostics, everything else is Study 2."""
    name = name[:-4] if name.endswith('.csv') else name
    return (TABLES1 if re.match(r'd\d', name) else TABLES2) / f'{name}.csv'
