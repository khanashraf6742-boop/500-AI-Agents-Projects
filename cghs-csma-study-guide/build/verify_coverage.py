#!/usr/bin/env python3
"""Coverage check: every text leaf / OM number / date / amount / rule ref of the SOURCE must appear
inside the study-guide body views (#v-about, #v-cghs, #v-csma) of the OUTPUT.

usage: python3 -I verify_coverage.py <source.html> <index.html> [report.md]
"""
import sys, re, json
from bs4 import BeautifulSoup

SRC, OUT = sys.argv[1], sys.argv[2]
REPORT = sys.argv[3] if len(sys.argv) > 3 else None

ws = lambda t: re.sub(r'\s+', ' ', t).strip()
alnum = lambda t: re.sub(r'[\W_]+', '', t.lower())

src = BeautifulSoup(open(SRC, encoding='utf8').read(), 'lxml')
for s in src.find_all('script'):
    s.decompose()
# generated TOC blocks are replaced by the sidebar -> exclude
for d in src.find_all('div'):
    if ws(d.get_text(' ', strip=True)).startswith('📑') and len(d.get_text()) < 2500:
        d.decompose()

out = BeautifulSoup(open(OUT, encoding='utf8').read(), 'lxml')
body_text = ''
for vid in ('v-about', 'v-cghs', 'v-csma'):
    v = out.find(id=vid)
    body_text += ' ' + v.get_text(' ', strip=True)
hay = alnum(body_text)
hay_raw = ws(body_text)

# 1. every leaf
leaves = []
for e in src.select('li,p,td,th,h1,h2,h3,.otag,.htag,.ttag,.gdtag,.ktag,.atag,.rule-tag,.rule-om,.qlabel,.alabel'):
    t = ws(e.get_text(' ', strip=True))
    if len(t) > 2:
        leaves.append(t)
leaves = sorted(set(leaves))
missing = [t for t in leaves if alnum(t) not in hay]

# 2. key facts
body = ws(src.body.get_text(' ', strip=True))
RS = r'(?:Rs\.?|₹)\s?[\d,]+(?:\.\d+)?'
facts = {
    'OM numbers': sorted(set(re.findall(r'OM\s+No\.?\s*[\w\.\-/\(\)]+', body))),
    'Dates (dd.mm.yyyy)': sorted(set(re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b', body))),
    'Rupee amounts': sorted(set(re.findall(RS, body))),
    'Rule references': sorted(set(re.findall(r'Rule\s+\d+(?:\(\w+\))*', body))),
    'GD items': sorted(set(re.findall(r'GD\(\d+\)', body))),
}
lines = ['# Coverage report', '', f'Source: `{SRC.split("/")[-1]}`  →  Output: `{OUT.split("/")[-1]}`', '']
ok_all = True
tot = len(leaves)
lines.append(f'- Text blocks checked: **{tot}**, present: **{tot-len(missing)}** ({100*(tot-len(missing))/tot:.2f}%)')
for k, items in facts.items():
    miss = [i for i in items if alnum(i) not in hay]
    lines.append(f'- {k}: **{len(items)-len(miss)}/{len(items)}** present' + (f' — missing: {miss[:20]}' if miss else ''))
    if miss:
        ok_all = False
if missing:
    ok_all = False
    lines += ['', '## Missing text blocks', ''] + [f'- {m[:200]}' for m in missing[:200]]
# counts
cnt = lambda doc, sel: len(doc.select(sel))
lines += ['', '## Structure counts (source → output)', '']
for lab, sel in [('rule-cards (+1 Q&A card)', '.rule-card'), ('official boxes', '.official-box'), ('Government-decision boxes', '.gd-box'), ('amendment boxes', '.amend-box'),
                 ('trap boxes', '.trap-box'), ('key boxes', '.key-box'), ('tables', 'table'), ('Hinglish paired units', '.paired-unit'), ('Hinglish blocks', '.hinglish, details.hing')]:
    a = cnt(src, sel)
    osel = 'details.card' if sel == '.rule-card' else sel
    b = sum(cnt(out.find(id=v), osel) for v in ('v-about', 'v-cghs', 'v-csma'))
    lines.append(f'- {lab}: {a} → {b}')
lines += ['', '**RESULT: ' + ('100% — all source content present' if ok_all else 'GAPS FOUND') + '**']
txt = '\n'.join(lines)
print(txt)
if REPORT:
    open(REPORT, 'w', encoding='utf8').write(txt + '\n')
sys.exit(0 if ok_all else 1)
