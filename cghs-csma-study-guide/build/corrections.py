"""Corrections applied to the SOURCE text at build time (obsolete / wrong statements).

Every rule cites the primary order that supersedes the source wording. Each change is logged
(old leaf text -> new leaf text) so the Corrections tab and the coverage report can show exactly
what was changed. Primary texts were read from the copies of the official OMs hosted on staffnews.in
(the MoHFW site itself returned HTTP 502 from this environment).
"""
import re

COCH_NEW = 'Rs.7,00,000 (pre-lingual) / Rs.6,00,000 (post-lingual), incl. GST [OM 09.11.2026]'

TEXT_RULES = [
    # (regex, replacement, reason)
    (r'Rs\.[\s\u00a0]*5,35,000(?:/-)?', COCH_NEW,
     'Cochlear implant ceiling Rs.5,35,000 is obsolete: OM 09.11.2026 (F. No. S-367/2026/CGHSHQ/R&H/EHS(8410942)) revised it to Rs.7,00,000 (pre-lingual) / Rs.6,00,000 (post-lingual) incl. GST and superseded earlier cochlear orders.'),
    (r'Rs\.[\s\u00a0]*5\.35 ?lakh', 'Rs.7 lakh (pre-lingual) / Rs.6 lakh (post-lingual) [OM 09.11.2026]',
     'Same cochlear ceiling correction (OM 09.11.2026).'),
    (r'Rs\.5\.35L', 'Rs.7L pre-lingual / Rs.6L post-lingual [OM 09.11.2026]',
     'Same cochlear ceiling correction (OM 09.11.2026).'),
    (r'confirmed by June-2026 CPI-IW; Cabinet approval & formal notification expected Sept–Oct 2026,? with arrears from 01\.07\.2026',
     'Department of Expenditure OM No. 1/2(i)/2026-E.II(B) dated 29.10.2026 raised DA from 60% to 63%',
     'DA 63% from 01.07.2026 is no longer “expected”: it was notified by DoE OM dated 29.10.2026.'),
]

PENS_REASON = ('The guide showed pensioners’ general MRC settled by “Head of CGHS covered city up to Rs.10 lakh”. The Rs.10 lakh HoD ceiling (OM 16.02.2026) is for Heads of Departments of Ministries/Departments. '
               'For CGHS pensioners and other eligible CGHS beneficiaries the financial powers are those in CGHS OM No. Z.15025/14/2/DIR/CGHS dated 25.06.2026: Additional Director, CGHS city/zone Rs.15 lakh; Director, CGHS Rs.25 lakh; '
               'Additional Secretary & DG, CGHS Rs.50 lakh; above Rs.50 lakh → MoHFW with IFD concurrence.')

PENS_AUTH = 'Additional Director, CGHS city/zone [OM 25.06.2026]'
PENS_LIMIT = 'Up to Rs.15 lakh (Director, CGHS: Rs.25 lakh; Additional Secretary & DG, CGHS: Rs.50 lakh; above Rs.50 lakh → MoHFW with IFD concurrence)'


def apply(soup, ws):
    """Mutate soup; return list of log dicts."""
    log = []
    body = soup.body

    def leaf_of(node):
        p = node.parent
        while p is not None and p.name not in ('li', 'p', 'td', 'th', 'div'):
            p = p.parent
        return p

    # ---- 1. regex rules on text nodes
    touched = {}
    for node in list(body.find_all(string=True)):
        old = str(node)
        new = old
        reasons = []
        for rx, rep, why in TEXT_RULES:
            n2 = re.sub(rx, rep, new)
            if n2 != new:
                reasons.append(why)
                new = n2
        if new != old:
            leaf = leaf_of(node)
            key = id(leaf)
            if key not in touched:
                touched[key] = dict(leaf=leaf, old=ws(leaf.get_text(' ', strip=True)), reasons=[])
            touched[key]['reasons'] += [r for r in reasons if r not in touched[key]['reasons']]
            node.replace_with(new)
    for t in touched.values():
        log.append(dict(old=t['old'], new=ws(t['leaf'].get_text(' ', strip=True)), reason=' '.join(t['reasons']), kind='text'))

    # ---- 1b. amount split from its 'Rs.' prefix by inline markup (<strong>5,35,000</strong>)
    for st in body.find_all(['strong', 'b']):
        if re.fullmatch(r'\s*5,35,000(?:/-)?\s*', st.get_text()):
            leaf = leaf_of(st)
            old = ws(leaf.get_text(' ', strip=True))
            st.clear(); st.append('7,00,000 (pre-lingual) / Rs.6,00,000 (post-lingual), incl. GST [OM 09.11.2026]')
            log.append(dict(old=old, new=ws(leaf.get_text(' ', strip=True)), reason=TEXT_RULES[0][2], kind='text'))

    # ---- 2. pensioner general-MRC row (table) and its Hinglish paired units
    for tr in body.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        if len(cells) == 3 and 'General MRC' in cells[0].get_text() and 'pensioners' in cells[0].get_text():
            old = ws(tr.get_text(' | ', strip=True))
            cells[1].clear(); cells[1].append(PENS_AUTH)
            cells[2].clear(); cells[2].append(PENS_LIMIT)
            new = ws(tr.get_text(' | ', strip=True))
            log.append(dict(old=old, new=new, reason=PENS_REASON, kind='row'))
    for el in body.select('.hinglish-mini, .original-mini'):
        t = el.get_text()
        if 'General MRC' in t and 'pensioners' in t and 'Head of CGHS covered' in t:
            old = ws(el.get_text(' ', strip=True))
            for node in list(el.find_all(string=True)):
                s = str(node)
                s2 = re.sub(r'Head of CGHS covered(?: \(shaamil\))? city', 'Additional Director, CGHS city/zone [OM 25.06.2026]', s)
                s2 = re.sub(r'(?:Tak|Up to)\s*Rs\.10 lakhs', 'Rs.15 lakh tak (Director Rs.25L; AS&DG Rs.50L; upar MoHFW+IFD)', s2)
                s2 = s2.replace('Rs.10 lakhs', 'Rs.15 lakh (Director Rs.25L; AS&DG Rs.50L)')
                if s2 != s:
                    node.replace_with(s2)
            new = ws(el.get_text(' ', strip=True))
            if new != old:
                log.append(dict(old=old, new=new, reason=PENS_REASON, kind='hinglish'))
    return log
