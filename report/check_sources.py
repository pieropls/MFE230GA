"""Guard against a `% src:` comment swallowing LaTeX text on the same line, and list unsourced-looking numbers.

Run after editing main.tex:  python3 report/check_sources.py
Exit code 1 if a `% src:` comment is followed by LaTeX (a backslash, a math `$` or a brace) on the same line.
"""
import re
import sys
from pathlib import Path

tex = Path(__file__).with_name('main.tex').read_text().splitlines()
bad = []
for n, line in enumerate(tex, 1):
    m = re.search(r'%\s*src:(.*)$', line)
    if m and re.search(r'[\\${}]', m.group(1)):
        bad.append((n, line.strip()[:120]))
todos = sum(1 for l in tex if '\\todo{' in l and not l.lstrip().startswith('%'))
print(f'{len(tex)} lines, {todos} \\todo marks')
if bad:
    print('A % src comment swallows LaTeX on these lines (move the comment to the end of the line):')
    for n, l in bad:
        print(f'  {n}: {l}')
    sys.exit(1)
print('no swallowed text after % src comments')
