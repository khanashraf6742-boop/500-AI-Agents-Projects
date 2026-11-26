#!/usr/bin/env python3
"""Build the interactive study guide from the source HTML.

usage: python3 -I build.py <source.html> <output index.html>

Every text node of the source guide is carried into the output (see verify_coverage.py);
visuals (SVG / comparison tables) are additive and authored in visuals.py.
"""
import sys, os, re, json, html
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import visuals
import powers
import corrections
import latest
import quiz
import memory

SRC, OUT = sys.argv[1], sys.argv[2]
soup = BeautifulSoup(open(SRC, encoding='utf8').read(), 'lxml')
for sc in soup.find_all('script'):
    sc.decompose()

ws = lambda t: re.sub(r'\s+', ' ', t).strip()
txt = lambda e: ws(e.get_text(' ', strip=True))
esc = html.escape
new = lambda name, **kw: soup.new_tag(name, **kw)

# ---------------------------------------------------------------- 1. un-nest cards
LAST = {}
for c in list(soup.select('.rule-card')):
    p = c.parent
    while p is not None and 'rule-card' not in (p.get('class') or []):
        p = p.parent
    if p is not None:                      # card nested inside another card -> move after the outermost card
        top = p
        while top.parent is not None and 'rule-card' in (top.parent.get('class') or []):
            top = top.parent
        # keep insertion order: insert after the last already-moved sibling
        anchor = LAST.get(id(top), top)
        anchor.insert_after(c.extract())
        LAST[id(top)] = c

ALL_CARDS = soup.select('.rule-card')
CORR_LOG = corrections.apply(soup, ws)
json.dump(CORR_LOG, open(os.path.join(HERE, 'corrections_log.json'), 'w'), ensure_ascii=False, indent=1)
print('corrections applied:', len(CORR_LOG), file=sys.stderr)
print('cards:', len(ALL_CARDS), file=sys.stderr)

# ---------------------------------------------------------------- 2. cleaning helpers
def strip_attrs(el):
    for t in [el] + el.find_all(True):
        keep = {}
        for k, v in t.attrs.items():
            if k in ('class', 'colspan', 'rowspan', 'href'):
                keep[k] = v
        t.attrs = keep
    return el

LEAD = re.compile(r'^[^A-Za-z0-9(\[]*')
MARK = [
    (re.compile(r'^(key\s+)?provisos?\b|^proviso\b|^provided\b', re.I), 'proviso', 'Proviso'),
    (re.compile(r'^explanations?\b', re.I), 'expl', 'Explanation'),
    (re.compile(r'^exceptions?\b', re.I), 'exc', 'Exception'),
    (re.compile(r'^notes?\b', re.I), 'note', 'Note'),
]
def mark_semantics(root):
    for e in root.find_all(['li', 'p']):
        if e.find(['li', 'p']):
            continue
        if e.find_parent(class_=['hinglish', 'trap-box']):
            continue
        t = LEAD.sub('', txt(e))
        for rx, cls, label in MARK:
            if rx.match(t):
                e['class'] = e.get('class', []) + [cls]
                chip = new('span'); chip['class'] = ['chip']; chip.string = label
                e.insert(0, chip)
                e.insert(1, NavigableString(' '))
                break

def wrap_tables(root):
    for t in root.find_all('table'):
        if t.parent and 'tblwrap' in (t.parent.get('class') or []):
            continue
        w = new('div'); w['class'] = ['tblwrap']
        t.wrap(w)

def convert_hinglish(root):
    for h in root.select('.hinglish'):
        d = new('details'); d['class'] = ['hing']
        tag = h.select_one('.htag')
        title = ws(tag.get_text(' ', strip=True)) if tag else 'Hinglish'
        title = re.sub(r'^🗣️\s*', '', title)
        s = new('summary'); s.string = title
        body = new('div'); body['class'] = ['hing-body']
        for ch in list(h.children):
            body.append(ch.extract())
        d.append(s); d.append(body)
        h.replace_with(d)

# ---------------------------------------------------------------- 3. extract model
class Card:
    pass

def parse_card(c, i):
    k = Card()
    k.i = i
    k.id = f'c{i}'
    bar = c.select_one('.rule-bar')
    k.tag = txt(c.select_one('.rule-tag')) if c.select_one('.rule-tag') else ''
    k.title = txt(c.select_one('.rule-bar-info h2')) if c.select_one('.rule-bar-info h2') else ''
    k.om = txt(c.select_one('.rule-om')) if c.select_one('.rule-om') else ''
    k.color = next((x for x in (bar.get('class') or []) if x.startswith('bg-')), 'bg-blue') if bar else 'bg-blue'
    body = c.select_one('.rule-body')
    k.body = body
    k.extra = [ch for ch in c.find_all(recursive=False) if ch is not bar and ch is not body]
    return k

parts = []   # [{'key','name','secs':[('sec title', [card or qa or recap...])], 'intro':[...]}]

def collect(wrap, key, name):
    P = dict(key=key, name=name, items=[], intro=[])
    seen_card = False
    for ch in list(wrap.find_all(recursive=False)):
        cl = ch.get('class') or []
        if any(x.startswith('sec-div') for x in cl):
            P['items'].append(('sec', txt(ch)))
        elif 'rule-card' in cl:
            P['items'].append(('card', ch)); seen_card = True
        elif 'qa-card' in cl:
            P['items'].append(('qa', ch)); seen_card = True
        elif 'recap' in cl:
            P['items'].append(('recap', ch))
        else:
            if txt(ch).startswith('📑'):          # generated table of contents is replaced by the sidebar
                continue
            (P['items'] if seen_card else P['intro']).append(('misc', ch) if seen_card else ch)
    return P

m1 = soup.select_one('.m1'); m2 = soup.select_one('.m2')
topdiv = [c for c in soup.body.find_all(recursive=False)][0]
P1 = collect(m1.select_one('.wrap'), 'cghs', 'CGHS')
P2 = collect(m2.select_one('.wrap'), 'csma', 'CS(MA) Rules 1944')
# trailing blocks of m2 outside wrap
for ch in m2.find_all(recursive=False):
    if 'wrap' not in (ch.get('class') or []):
        P2['items'].append(('misc', ch))
about = [c for c in topdiv.find_all(recursive=False)]
# the master header is one level deeper
about_items = []
for ch in about:
    for sub in ch.find_all(recursive=False):
        if txt(sub).startswith('📑'):
            continue
        about_items.append(sub)
parts = [P1, P2]

# ---------------------------------------------------------------- 4. render
cid = 0
RC = 0
CARDS = []        # all Card objects in doc order
html_views = {}
extras = dict(traps=[], tables=[], flash=[], om=[], verify=[], changelog=[])

def leaf_texts(root):
    for e in root.find_all(['li', 'p', 'td']):
        if e.find(['li', 'p', 'td']):
            continue
        if e.find_parent(class_=['hinglish', 'hing-body']) or e.find_parent('details', class_='hing'):
            continue
        t = txt(e)
        if len(t) > 3:
            yield t

DATE = re.compile(r'\b(\d{2})\.(\d{2})\.(\d{4})\b')
OMKW = re.compile(r'\bOM\b|Order|Notification|File No|Circular|SOP|vide|Gazette', re.I)
VERIFY = [
    ('Dynamic / DA-linked figure', re.compile(r'dynamic|subject to change|currently\s*≈|DA/DR|approx', re.I)),
    ('Reference to website only — no order number given', re.compile(r'see mohfw|\[MoHFW OM\]|MoHFW OM —|—\s*see\s+MoHFW', re.I)),
    ('Source gives two values', re.compile(r'by some references', re.I)),
]
CHANGE = re.compile(r'supersed|🔧|CORRECTED|OBSOLETE|➕\s*Added|NEW\s*—|\bamend', re.I)

def render_card(k, src_card, extra_cls=''):
    body = k.body
    strip_attrs(body)
    convert_hinglish(body)
    mark_semantics(body)
    wrap_tables(body)
    # card pieces for extras
    for t in leaf_texts(body):
        for lab, rx in VERIFY:
            if rx.search(t):
                extras['verify'].append((k, lab, t))
        if CHANGE.search(t):
            extras['changelog'].append((k, t))
        if DATE.search(t) and OMKW.search(t):
            d = DATE.search(t)
            extras['om'].append((f'{d.group(3)}-{d.group(2)}-{d.group(1)}', d.group(0), t, k))
    for tb in body.select('.trap-box'):
        if tb.find_parent(class_='hinglish'):
            continue
        for li in tb.select('li'):
            extras['traps'].append((k, li))
            t = txt(li)
            m = re.match(r'^[“"\']?(.+?)[”"\']?\s*[—–-]+\s*(?:ABSOLUTELY\s+)?WRONG!?\s*(.*)$', t, re.S)
            if m:
                extras['flash'].append(dict(t='trap', q=esc(m.group(1).strip(' "“”')), a='<b>WRONG!</b> ' + esc(m.group(2)), s=esc(k.title[:60]), c=k.id))
            else:
                extras['flash'].append(dict(t='trap', q=esc(t[:140]), a=esc(t), s=esc(k.title[:60]), c=k.id))
    for tb in body.find_all('table'):
        if tb.find_parent(class_=['hinglish', 'hing-body']):
            continue
        rows = tb.find_all('tr')
        if len(rows) < 2:
            continue
        hdr = [txt(c) for c in rows[0].find_all(['th', 'td'])]
        cap = ''
        kb = tb.find_parent(class_='key-box')
        if kb and kb.select_one('.ktag'):
            cap = txt(kb.select_one('.ktag'))
        extras['tables'].append((k, cap, tb))
        if 2 <= len(hdr) <= 5:
            for r in rows[1:]:
                cells = [txt(c) for c in r.find_all(['th', 'td'])]
                if len(cells) == len(hdr) and cells[0] and len(cells[0]) < 120 and all(cells[1:]):
                    ans = '<br>'.join(f'<b>{esc(h)}:</b> {esc(c)}' for h, c in zip(hdr[1:], cells[1:]))
                    extras['flash'].append(dict(t='table', q=esc((cap or k.title)[:70]) + f'<br><b>{esc(cells[0])}</b>', a=ans, s=esc(k.title[:60]), c=k.id))
    # visual
    vis = visuals.V.get(k.rc)
    visual_html = ''
    if vis:
        visual_html = f'<details class="visual" open><summary>📊 Visual summary — diagrams &amp; comparison</summary>{vis}</details>'
    upd = ''.join(latest.CALLOUTS.get(k.rc, []))
    inner = ''.join(str(ch) for ch in body.children)
    inner += ''.join(clean_misc(x) for x in k.extra)
    return (f'<details class="card {extra_cls}" id="{k.id}" open>'
            f'<summary class="{k.color}"><span class="rtag">{esc(k.tag)}</span>'
            f'<div class="rinfo"><h2>{esc(k.title)}</h2><div class="rom">{esc(k.om)}</div>{"<span class=sbadge>🆕 updated with 2026 orders</span>" if k.rc in latest.CALLOUTS else ""}</div>'
            f'<span class="cardtools"><button class="bBm" aria-label="Bookmark">☆</button><button class="bStudy">Mark studied</button></span></summary>'
            f'<div class="cbody">{visual_html}{upd}{inner}<div class="notes"><label for="n-{k.id}">📝 My notes</label><textarea id="n-{k.id}" data-note="{k.id}" rows="3" placeholder="Your notes for this section (saved in this browser)…"></textarea></div></div></details>')

def render_qa(el, k):
    strip_attrs(el); convert_hinglish(el); mark_semantics(el); wrap_tables(el)
    t = txt(el.select_one('.qa-header h2')) if el.select_one('.qa-header h2') else 'Authoritative Q&A'
    k.title = t; k.tag = 'Q&A'; k.om = 'Verified by MoHFW, DoPPW, DoPT, DoE & GoI Orders'
    for tt in leaf_texts(el):
        if CHANGE.search(tt):
            extras['changelog'].append((k, tt))
        if DATE.search(tt) and OMKW.search(tt):
            d = DATE.search(tt); extras['om'].append((f'{d.group(3)}-{d.group(2)}-{d.group(1)}', d.group(0), tt, k))
    return (f'<details class="card" id="{k.id}" open><summary class="bg-indigo"><span class="rtag">Q&amp;A</span>'
            f'<div class="rinfo"><h2>{esc(t)}</h2><div class="rom">{esc(k.om)}</div></div>'
            f'<span class="cardtools"><button class="bBm">☆</button><button class="bStudy">Mark studied</button></span></summary>'
            f'<div class="cbody">{str(el)}</div></details>')

def clean_misc(el):
    strip_attrs(el); convert_hinglish(el); mark_semantics(el); wrap_tables(el)
    return str(el)

nav = {'cghs': [], 'csma': []}
for P in parts:
    out = []
    pend_sec = None
    for kind, val in P['items']:
        if kind == 'sec':
            out.append(f'<div class="secdiv">{esc(val)}</div>')
            nav[P['key']].append(('sec', val))
        elif kind in ('card', 'qa'):
            k = parse_card(val, cid) if kind == 'card' else Card()
            if kind == 'qa':
                k.i = cid; k.id = f'c{cid}'; k.rc = None
            else:
                k.rc = RC; RC += 1
            CARDS.append(k); cid += 1
            k.part = P['key']
            out.append(render_card(k, val) if kind == 'card' else render_qa(val, k))
            nav[P['key']].append(('card', k))
        elif kind == 'recap':
            out.append(clean_misc(val))
        else:
            out.append(clean_misc(val))
    intro = ''.join(clean_misc(x) for x in P['intro'])
    P['html'] = f'<div class="intro">{intro}</div>' + ''.join(out)

about_html = ('<div class="notice-box"><h3>🔔 Currency &amp; obsolete content — read this first</h3><ul>'
  '<li>The original guide’s text was current to <b>21 July 2026</b>. Orders to <b>09.11.2026</b> were read in full and incorporated — see <a href="#latest">Latest orders</a> (e.g. OMs of 25.06.2026, 01.09.2026, 26.10.2026, 09.11.2026) — and wrong / obsolete figures were corrected with the old wording kept on that tab.</li>'
  '<li>Superseded rates and orders are NOT presented as current in the rule text; where the guide itself records a correction (e.g. hearing-aid rates, HoD ceiling) it is listed in the <a href="#changelog">changelog</a>.</li>'
  '<li>Study tools: <a href="#quiz">mock tests</a> (275 questions, timer, weak-area report) · <a href="#plan">study plan</a> · <a href="#memory">memory sheet &amp; timeline</a> · <a href="#compare2">compare two sections</a> · <a href="#mystudy">notes &amp; progress export</a> · ⚡ Revision mode · spaced-repetition flashcards. Green “🆕 UPDATE” boxes mark content added from 2026 orders.</li><li>New: <a href="#powers">Who has the power?</a> — who appoints the AMA, delegation of powers, authority matrix and practice questions.</li></ul></div>') + ''.join(clean_misc(x) for x in about_items)

# ---------------------------------------------------------------- 5. derived views
def card_link(k):
    return f'<a href="#{k.id}">{esc(k.tag)} · {esc(k.title[:70])}</a>'

# quick reference: all tables
qr = ['<div class="row"><input class="filterbox" data-filter="#v-quick .qt" placeholder="Filter tables… (e.g. Rs.10,000, 3 months, ward)" aria-label="Filter tables"></div>']
for k, cap, tb in extras['tables']:
    tb2 = BeautifulSoup(str(tb), 'lxml').find('table')
    tb2.attrs = {}
    qr.append(f'<section class="qt"><h3>{esc(cap or k.title)}</h3><p class="src">From {card_link(k)}</p><div class="tblwrap">{tb2}</div></section>')
quick_html = ''.join(qr)

# visuals overview tab
comp_html = visuals.OVERVIEW

# traps
tr = ['<div class="row"><input class="filterbox" data-filter="#v-traps .listitem" placeholder="Filter traps…" aria-label="Filter traps"></div>',
      f'<p class="lead">{len(extras["traps"])} exam traps collected from every section of the guide (each “WRONG!” is followed by the correct position).</p>']
last = None
for k, li in extras['traps']:
    if last is not k:
        tr.append(f'<h3 class="trh">{esc(k.title)}</h3>'); last = k
    l2 = BeautifulSoup(str(li), 'lxml').find('li'); l2.attrs = {}
    tr.append(f'<div class="listitem">{l2.decode_contents()}<div class="src">{card_link(k)}</div></div>')
traps_html = ''.join(tr)

# OM register
seen = set(); rows = []
for iso, dtxt, t, k in sorted(extras['om'], key=lambda x: x[0]):
    key = (iso, t[:90])
    if key in seen:
        continue
    seen.add(key)
    st = 'Superseded / corrected in source' if re.search(r'supersed|CORRECTED|OBSOLETE', t, re.I) else ''
    rows.append(f'<tr><td data-k="{iso}">{dtxt}</td><td>{esc(t[:360])}</td><td>{card_link(k)}</td><td>{st}</td></tr>')
oms_html = ('<div class="row"><input class="filterbox" data-filter="#oms tbody tr" placeholder="Filter OMs / orders / dates…" aria-label="Filter OM register"></div>'
            f'<p class="lead">{len(rows)} dated orders, OMs, notifications and circulars found in the guide. Click a column header to sort. This register is extracted automatically — the rule text in each section is authoritative.</p>'
            '<div class="tblwrap"><table id="oms" class="sortable"><thead><tr><th>Date ⇅</th><th>Order / provision (as written in the guide)</th><th>Section</th><th>Note</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table></div>')

# changelog
cl_seen = set(); cl = []
for k, t in extras['changelog']:
    if t[:100] in cl_seen: continue
    cl_seen.add(t[:100])
    cl.append(f'<div class="listitem">{esc(t[:520])}<div class="src">{card_link(k)}</div></div>')
cl_new = ''.join(f'<div class="listitem"><span class="tag">New order</span><b>{d}</b> — {esc(subj)}<div class="src">{esc(fn)} · <a href="#latest">Latest orders tab</a></div></div>' for d, fn, subj, _k in latest.ORDERS)
_cg = {}
for c in CORR_LOG:
    _cg[c['reason']] = _cg.get(c['reason'], 0) + 1
cl_corr = ''.join(f'<div class="listitem"><span class="tag">Corrected · {n} places</span>{esc(r)}<div class="src"><a href="#latest">see old vs new</a></div></div>' for r, n in _cg.items())
changelog_html = ('<div class="row"><input class="filterbox" data-filter="#v-changelog .listitem" placeholder="Filter…" aria-label="Filter changelog"></div>'
    '<p class="lead">Every place the guide itself records an amendment, correction, supersession or obsolete item. Obsolete provisions are NOT presented as current in the body; they appear here as the source flags them.</p>' + '<h3>New orders incorporated (2026)</h3>' + cl_new + '<h3>Corrections to earlier text</h3>' + cl_corr + '<h3>Amendments recorded inside the original guide</h3>' + ''.join(cl))

# verify
MANUAL = [
    ('Rule 4 — fare concession', 'The Rule 4 body gives “Patient + Attendant: half of normal fare / Patient alone: one quarter” without naming the category, while the Rule 4 trap list says “TB patient + attendant: half fare”. Confirm the category against the primary text before relying on it.', 'Rule 4'),
    ('Rule 11 — cross-reference', 'Rule 11 GD(1) cites “[Rule 11(11) GD]” although the section describes sub-rules (1)–(7). Treat the cross-reference as unverified.', 'Rule 11'),
    ('Distance wording', 'Rule 4 uses “five miles (≈ 8 km)”. AMA-appointment GD(1) says “5 kms (8 km by some references)”. The two distance tests are different rules — do not mix them.', 'Rule 2(a) / Rule 4'),
    ('CS(MA) mix-ups', 'Several CS(MA) sections point to “see mohfw.gov.in/csma” with no OM number (AMA re-verification, NABH/NABL accreditation, AYAH/nursing ceiling). The guide does not give the order number — check before quoting in an answer.', 'Rule 2(a) GD, Rule 8'),
]
vr = ['<p class="lead">Items that need a second look before you rely on them in an exam answer. Nothing here changes the rule text — it only flags dynamic figures, internally inconsistent cross-references and statements that cite no order number.</p>',
      '<h3>Flagged by reading the guide</h3>']
for a, b, c in MANUAL:
    vr.append(f'<div class="listitem"><b>{esc(a)}</b><br>{esc(b)}<div class="src">{esc(c)}</div></div>')
vr.append('<h3>Flagged automatically</h3><div class="row"><input class="filterbox" data-filter="#v-verify .auto" placeholder="Filter…" aria-label="Filter verify items"></div>')
vseen = set()
for k, lab, t in extras['verify']:
    if (lab, t[:100]) in vseen: continue
    vseen.add((lab, t[:100]))
    vr.append(f'<div class="listitem auto"><span class="tag">{esc(lab)}</span>{esc(t[:480])}<div class="src">{card_link(k)}</div></div>')
vr.append('<h3>Still unverified</h3><p class="lead">Recent CGHS / CS(MA) orders (Jan–Nov 2026) were read in full — see the <a href="#latest">Latest orders</a> tab. What could not be confirmed:</p>')
for a_, b_ in [
    ('AMA appointment — OM number', 'The guide says the Head of Department appoints private practitioners as AMA (Rule 2(a) GD(2)) but cites no OM number. The CS(MA) Rules PDF and the MoHFW CS(MA) page (orders list, AMA re-verification OM, verification proforma) could not be opened from this environment (HTTP 502). A CSIR policy document found in search says Supplementary Rule 2(10) allows a private registered practitioner to be appointed AMA for a class of employees where adequate doctors are unavailable — consistent with the guide, but not read at the source.'),
    ('Pensioners’ emergency claims', 'The guide says emergency claims within prescribed rates for pensioners are settled by the Head of the CGHS-covered city with no financial limit. OM 25.06.2026 gives the Additional Director / Director / AS&DG financial powers for CGHS claims generally and does not mention an “emergency, no limit” category; treat the “no limit” statement for pensioners as unconfirmed.'),
    ('Pre-16.02.2026 statements', 'Statements in older sections that quote “Rs.5 lakh” for the HoD / IFD threshold have already been corrected in the guide; if you see one elsewhere, Rs.10 lakh (OM 16.02.2026) is the current HoD figure.'),
    ('Orders after 09.11.2026', 'The search for new orders was made on 25.11.2026. Anything issued later, or not published on the sites searched, is not included.'),
]:
    vr.append(f'<div class="listitem"><span class="tag">Unverified</span><b>{esc(a_)}</b><br>{esc(b_)}</div>')
vr.append('<h3>Where to check</h3><div class="listitem">MoHFW — Central Services (Medical Attendance) page: <a href="https://www.mohfw.gov.in/documents/csma" rel="noopener">mohfw.gov.in/documents/csma</a>. CGHS portal: <a href="https://cghs.gov.in" rel="noopener">cghs.gov.in</a>. Order texts are mirrored by <a href="https://www.staffnews.in" rel="noopener">staffnews.in</a> (used for the Latest orders tab).</div>')
verify_html = ''.join(vr)

# powers view
RCMAP = {k.rc: k.id for k in CARDS if getattr(k, 'rc', None) is not None}
powers_html = powers.build(lambda n: '#' + RCMAP[n])
latest_html = latest.latest_view(CORR_LOG)
RCPART = {k.rc: k.part for k in CARDS if getattr(k, 'rc', None) is not None}
RCTITLE = {k.rc: k.title for k in CARDS if getattr(k, 'rc', None) is not None}
QBANK = quiz.build(extras, RCMAP, RCPART, RCTITLE, esc)
for _q in QBANK:
    if _q.get('p') not in ('cghs', 'csma'):
        _q['p'] = 'cghs'
qdata = json.dumps(QBANK, ensure_ascii=False).replace('</', '<\\/')
memory_html = memory.build(lambda n: '#' + RCMAP[n])
quiz_html = '''<div id="qSetup"><p class="lead"><b id="qBank">0</b> questions: hand-written case and fact questions plus questions generated from the guide’s own tables and trap lists. Each question links back to its section.</p>
<div class="row"><label>Questions <select id="qCount"><option>10</option><option selected>20</option><option>30</option><option>50</option><option>100</option></select></label>
<label>Type <select id="qKind"><option value="all">All</option><option value="case">Case scenarios</option><option value="fact">Facts &amp; figures</option><option value="tf">True / false (traps)</option></select></label>
<label>Part <select id="qPart"><option value="all">Both</option><option value="cghs">CGHS</option><option value="csma">CS(MA)</option></select></label>
<label>Mode <select id="qMode"><option value="exam">Exam (feedback at the end)</option><option value="practice">Practice (instant feedback)</option></select></label>
<label>Timer <select id="qTime"><option value="0">None</option><option value="10">10 min</option><option value="20">20 min</option><option value="30">30 min</option><option value="45">45 min</option></select></label>
<button id="qStart" class="on">Start test</button></div><div id="qHist"></div></div>
<div id="qRun" class="hide"><div class="row"><b id="qProg"></b><span id="qTimer"></span><button id="qFinish">Finish</button></div>
<div class="qbox"><p id="qText" class="qtext"></p><div id="qOpts"></div><div id="qFeedback"></div></div>
<div class="row"><button id="qPrev">◀ Prev</button><button id="qNext">Next ▶</button></div></div>
<div id="qResult" class="hide"><div id="qResultBody"></div><div class="row"><button id="qRetryWrong">Retry only the wrong ones</button><button id="qAgain" class="on">New test</button></div></div>'''
plan_html = '''<p class="lead">Choose how many days you have. Sections are spread by length; the last day is for revision. Progress follows the “Mark studied” buttons.</p>
<div class="row"><label>Days <select id="planDays"><option value="7">7</option><option value="14" selected>14</option><option value="21">21</option><option value="30">30</option></select></label><button id="bPlan" class="on">Create plan</button></div><div id="planOut"></div>'''
mystudy_html = '''<p class="lead">Everything is stored in this browser only. Export a file to move your progress to another device or to keep a backup.</p>
<div class="row"><button id="bExport" class="on">⬇ Export progress</button><label class="btn">⬆ Import progress <input id="fImport" type="file" accept="application/json" hidden></label><button id="bReset">🗑 Reset everything</button></div>
<h3>My notes</h3><div id="notesList"></div>'''
compare_html = '''<p class="lead">Pick any two sections to read them side by side (Hinglish layers are left out here).</p>
<div class="row"><select id="cmpA" aria-label="First section"></select><select id="cmpB" aria-label="Second section"></select></div>
<div class="cmpgrid"><div id="cmpOutA"></div><div id="cmpOutB"></div></div>'''

# flashcards
fc_json = json.dumps(extras['flash'], ensure_ascii=False).replace('</', '<\\/')

# ---------------------------------------------------------------- 6. sidebar
def nav_html():
    o = ['<h4>Study guide</h4>']
    for v, label in [('about', '🏠 Overview & fact-check'), ('compare', '⚖️ CGHS vs CS(MA)'), ('latest', '🆕 Latest orders (2026) & corrections'), ('powers', '🏛️ Who has the power? (AMA, delegation)')]:
        o.append(f'<a class="view" data-view="{v}" href="#{v}">{label}</a>')
    for P, label in [(P1, '🏥 PART 1 — CGHS'), (P2, '⚖️ PART 2 — CS(MA) Rules 1944')]:
        o.append(f'<h4>{label}</h4><a class="view" data-view="{P["key"]}" href="#{P["key"]}">Open part</a>')
        for kind, v in nav[P['key']]:
            if kind == 'sec':
                o.append(f'<h4 style="margin-top:8px;text-transform:none;letter-spacing:0">{esc(v[:62])}</h4>')
            else:
                o.append(f'<a class="sub" data-card="{v.id}" href="#{v.id}"><b>{esc(v.tag)}</b> {esc(v.title[:60])}</a>')
    o.append('<h4>Study tools</h4>')
    for v, label in [('quiz', '📝 Mock tests & practice'), ('plan', '🗓️ Study plan'), ('memory', '🧠 Memory sheet & timeline'), ('compare2', '↔️ Compare two sections'), ('mystudy', '💾 My notes & progress')]:
        o.append(f'<a class="view" data-view="{v}" href="#{v}">{label}</a>')
    o.append('<h4>Revision tools</h4>')
    for v, label in [('quick', '📋 Quick reference tables'), ('oms', '📜 OM / order register'), ('traps', '⚠️ All exam traps'), ('flash', '🃏 Flashcards'), ('verify', '🔎 Verify list'), ('changelog', '🔄 Amendments & changelog')]:
        o.append(f'<a class="view" data-view="{v}" href="#{v}">{label}</a>')
    return ''.join(o)

# ---------------------------------------------------------------- 7. assemble
css = open(os.path.join(HERE, 'assets/style.css'), encoding='utf8').read()
js = open(os.path.join(HERE, 'assets/app.js'), encoding='utf8').read()
js2 = open(os.path.join(HERE, 'assets/tools.js'), encoding='utf8').read()

def view(vid, title, lead, content, tools=False):
    t = ('<div class="toolbar"><button data-act="expand">Expand all</button><button data-act="collapse">Collapse all</button></div>' if tools else '')
    return f'<section class="view" id="v-{vid}"><h2 class="vtitle">{title}</h2><p class="lead">{lead}</p>{t}{content}</section>'

ncards1 = sum(1 for kk, _ in P1['items'] if kk in ('card', 'qa'))
ncards2 = sum(1 for kk, _ in P2['items'] if kk in ('card', 'qa'))
page = f'''<!DOCTYPE html>
<html lang="en" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CGHS + CS(MA) Rules 1944 — Interactive Study Guide</title>
<style>{css}</style></head>
<body>
<header id="top">
  <button id="menu" aria-label="Open contents">☰</button>
  <h1>CGHS + CS(MA) 1944</h1>
  <div class="grow"><input id="q" type="search" placeholder="Search rule no., OM no., keyword, amount…  ( / )" aria-label="Search the guide" autocomplete="off"><div id="results" role="listbox"></div></div>
  <div id="prog" title="Sections studied"><i></i></div><span id="progt" style="font-size:12px"></span>
  <button id="bRev" title="Hide long text, keep boxes, tables, traps and diagrams">⚡ Revision</button><button id="bHing">🗣️ Hinglish</button><button id="bFm" aria-label="Smaller text">A−</button><button id="bFp" aria-label="Larger text">A+</button><button id="bTheme" aria-label="Toggle theme">🌙</button><button id="bPrint" aria-label="Print">🖨️</button>
</header>
<div id="scrim"></div>
<div id="layout">
<nav id="side" aria-label="Contents"><div class="row" style="padding:0 8px"><button id="bOnlyBm" style="background:#1e293b;color:#fff;border-color:#334155">★ Bookmarks only</button></div>{nav_html()}</nav>
<main>
{view('about', '🏠 Overview, fact-check & how to use', f'{len(CARDS)} sections in two parts. Press <b>/</b> to search, <b>j / k</b> to jump between sections.', '<div class="intro">'+about_html+'</div>')}
{view('compare', '⚖️ CGHS vs CS(MA) — at a glance', 'Comparison built only from figures stated in the guide.', comp_html)}
{view('latest', '🆕 Latest orders (2026), verified & incorporated', 'Primary-text summaries of the newest CGHS / CS(MA) orders, plus the corrections made to earlier text.', latest_html)}
{view('powers', '🏛️ Who has the power? — AMA appointment, delegation of powers, authority matrix', 'Appointing authorities, HoD / Controlling Officer / MoHFW / Central Government powers and money limits, with practice questions.', powers_html)}
{view('cghs', '🏥 PART 1 — CGHS', f'{ncards1} sections', P1['html'], True)}
{view('csma', '⚖️ PART 2 — CS(MA) Rules, 1944', f'{ncards2} sections (Rules 1–11, AMA, advance, family, non-admissible items)', P2['html'], True)}
{view('quiz', '📝 Mock tests & practice', '', quiz_html)}
{view('plan', '🗓️ Study plan', '', plan_html)}
{view('memory', '🧠 Memory sheet & timeline', '', memory_html)}
{view('compare2', '↔️ Compare two sections', '', compare_html)}
{view('mystudy', '💾 My notes & progress', '', mystudy_html)}
{view('quick', '📋 Quick reference — every table', f'{len(extras["tables"])} tables from the guide, filterable.', quick_html)}
{view('oms', '📜 OM / order register', 'All dated orders mentioned, sortable by date.', oms_html)}
{view('traps', '⚠️ Exam traps', '', traps_html)}
{view('flash', '🃏 Flashcards', f'{len(extras["flash"])} cards generated from traps and tables. Tap the card to reveal.', '''<div class="row"><select id="fkind" aria-label="Card type"><option value="all">All cards</option><option value="trap">Exam traps</option><option value="table">Table facts</option></select>
<select id="fonly" aria-label="Filter"><option value="all">All</option><option value="due">Due now (spaced repetition)</option><option value="mastered">Mastered</option></select>
<label><input type="checkbox" id="fshuf" checked> shuffle</label><span id="fcount"></span></div>
<div id="fcard" role="button" tabindex="0" aria-live="polite"></div>
<div class="row"><button id="fPrev">◀ Prev</button><button id="fNo">✗ Still learning</button><button id="fKnow">✓ Know it</button><button id="fNext">Next ▶</button><button id="fReset">Reset</button></div>''')}
{view('verify', '🔎 Verify list', '', verify_html)}
{view('changelog', '🔄 Amendments & changelog', '', changelog_html)}
</main></div>
<script id="fcdata" type="application/json">{fc_json}</script>
<script id="qdata" type="application/json">{qdata}</script>
<script>{js}</script>
<script>{js2}</script>
</body></html>'''

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, 'w', encoding='utf8').write(page)
print(f'wrote {OUT}: {len(page)//1024} KB, cards={len(CARDS)}, traps={len(extras["traps"])}, tables={len(extras["tables"])}, flash={len(extras["flash"])}, questions={len(QBANK)}, om={len(rows)}, verify={len(vseen)+len(MANUAL)}, changelog={len(cl)}', file=sys.stderr)
