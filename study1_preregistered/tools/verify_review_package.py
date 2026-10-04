"""Read-only verification of exported evidence; no network or model dependencies."""
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parents[1]
STUDIES = ['follow_the_workers', 'follow_the_workers_opus55_xhigh']


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual, expected):
    if not math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12):
        raise AssertionError(f'Numeric mismatch: {actual} versus {expected}')


def check_ledger(path, expected):
    with path.open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected['n'] == 142
    date_key = next(iter(rows[0]))
    months = [row[date_key] for row in rows]
    assert months[0] == '2014-11' and months[-1] == '2026-08'
    assert len(set(months)) == 142 and months == sorted(months)
    net = []
    wealth = peak = 1.0
    drawdown = 0.0
    for raw in rows:
        row = {k:float(v) for k,v in raw.items() if k != date_key}
        assert all(math.isfinite(value) for value in row.values())
        close(row['cost'], (10 * row['turnover'] + 2 * row['hedge_turnover']) / 10000)
        close(row['net'], row['gross'] - row['cost'] - row['borrow_financing'])
        close(row['total_net'], row['net'] + row['risk_free'])
        assert row['gross_leverage'] <= 2 + 1e-12
        net.append(row['net'])
        wealth *= 1 + row['total_net']
        peak = max(peak, wealth)
        drawdown = min(drawdown, wealth / peak - 1)
    annual_mean = 12 * statistics.mean(net)
    volatility = math.sqrt(12) * statistics.stdev(net)
    close(annual_mean, expected['mean_net_annual'])
    close(volatility, expected['volatility'])
    close(annual_mean / volatility, expected['sharpe'])
    close(drawdown, expected['max_drawdown'])


def main():
    manifest = read(ROOT / 'package_manifest.json')
    exported = {row['file']:row for row in manifest['exported_files']}
    omitted = {row['file']:row for row in manifest['omitted_files']}
    for filename, row in exported.items():
        path = ROOT / filename
        assert path.is_file() and not path.is_symlink(), filename
        assert path.stat().st_size == row['bytes'], filename
        assert digest(path) == row['export_sha256'], filename
        if not row['changes']:
            assert row['source_sha256'] == row['export_sha256'], filename

    ledgers = 0
    for name in STUDIES:
        project = ROOT / 'outputs' / name
        out = project / 'outputs'
        for source in ['params.py', 'data.py', 'stats.py', 'agents.py', 'plots.py', 'run.ipynb']:
            row = exported[str((project / source).relative_to(ROOT))]
            assert not row['changes']
        for local, original_hash in read(out / 'FREEZE.json')['hashes'].items():
            relative = str((project / local).relative_to(ROOT))
            if relative in exported:
                assert exported[relative]['source_sha256'] == original_hash, relative
            else:
                assert relative in omitted and omitted[relative]['sha256'] == original_hash, relative
        result = read(out / 'sealed/initial/results.json')
        for variant, strategies in result['variants'].items():
            for strategy, expected in strategies.items():
                check_ledger(out / f'sealed/initial/{variant}_{strategy}_ledger.csv', expected)
                ledgers += 1
        access = [json.loads(line) for line in (out / 'return_access.jsonl').read_text().splitlines()]
        assert sum(row['scope'] == 'sealed' for row in access) == 1
        assert len(list(out.glob('evaluation_completed_*.json'))) == 1
        assert not (out / 'reruns.log').exists()
        assert result['gate']['verdict'] == 'Do not implement'
        primary = result['gate']['primary']
        stats = result['variants']['ASOF'][primary]
        print(f'{name}: primary {primary}, Sharpe {stats["sharpe"]:.6f}, annual net excess mean {stats["mean_net_annual"]:.6%}')

    follow = ROOT / 'outputs/follow_the_workers_opus55_xhigh/outputs'
    judgments = read(follow / 'agents/migration_judgments.json')
    prior = read(follow / 'agents/migration_judgments_before_human.json')
    sample = [row for row in judgments if row['human_review_required']]
    assert len(sample) == 17 and len(judgments) == len(prior) == 88
    assert [i for i,row in enumerate(sample,1) if row['human_uses_claim']] == [5,11,15]
    assert all(type(row['human_uses_claim']) is bool for row in sample)
    assert sum(row['human_uses_claim'] == row['uses_claim'] for row in sample) == 10
    for current, original in zip(judgments, prior):
        assert {k:v for k,v in current.items() if k != 'human_uses_claim'} == {
            k:v for k,v in original.items() if k != 'human_uses_claim'}

    links = 0
    documents = [ROOT / file for file in ['README.md', 'REPRODUCIBILITY.md', 'TEAM_REVIEW.md']]
    documents += [ROOT / 'outputs' / name / 'report' / file
                  for name in STUDIES for file in ['report.md', 'chatgpt_log.md']]
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if target.startswith(('https://','http://','#')):
                continue
            assert not target.startswith('/'), f'Nonportable link in {document.name}'
            assert (document.parent / target.split('#')[0]).exists(), (document.name, target)
            links += 1
    all_files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
    assert sum(p.stat().st_size for p in all_files) < 60 * 1024**2
    assert max(p.stat().st_size for p in all_files) < 10 * 1024**2
    print(f'PASS: {len(exported)} export hashes, both source inventories, {ledgers} ledgers, exact human review and {links} portable links.')


if __name__ == '__main__':
    main()
