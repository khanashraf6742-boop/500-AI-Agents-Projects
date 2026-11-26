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


TL_REASON = 'CGHS final-claim time limit is no longer 3 months: CGHS OM File No. 1-60/2017-CGHS/C&P/EHS (e-signed 01.06.2020) revised it to 6 months from completion of treatment / discharge; only bills submitted after 6 months need condonation of delay (power of condonation as in OM S.14025/8/99-MS dated 25.05.1999). No later revision was found.'
TIME_RULES = [
    (r'CGHS claim deadline = 3 months \(CS\(MA\) = 6 months\) — yeh difference sabse zyada poocha jaata hai\.', 'CGHS claim deadline = 6 months (OM 01.06.2020); CS(MA) = 6 months — purana 3-month rule obsolete hai.'),
    (r'CS\(MA\) claim = 6 months \(CGHS = 3 months\)', 'CS(MA) claim = 6 months (CGHS bhi 6 months — OM 01.06.2020)'),
    (r'CGHS claim deadline: ilaaj/dawai ke 3 months ke andar — uske baad claim entertain NAHI hota \(CS\(MA\) mein yeh 6 months hai — fark yaad rakho!\)', 'CGHS claim deadline: ilaaj/discharge ke 6 months ke andar (OM 01.06.2020) — uske baad sirf condonation se; CS(MA) mein bhi 6 months.'),
    (r'Ke andar 3 months of ilaaj/dawai purchase — claims \(daave\) beyond 3 months maana NAHI jaata \(entertain NAHI hota\) \(note \(tippani\): CS\(MA\) rules \(niyam\) has a 6-month period — different se CGHS\)', 'Ke andar 6 months of ilaaj/discharge (OM 01.06.2020) — uske baad claims ko condonation chahiye (note: CS(MA) mein bhi 6 months)'),
    (r'Claim deadline: CS\(MA\) mein 6 months \(CGHS ke 3 months se alag!\)', 'Claim deadline: CS(MA) mein 6 months (CGHS bhi 6 months — OM 01.06.2020)'),
    (r'CS\(MA\) = 6 months, CGHS = 3 months[^.]*\.', 'CS(MA) = 6 months aur CGHS bhi 6 months (OM 01.06.2020).'),
    (r'Exam trap: 6 months \(OPD/IPD\), advance case 1 month, appeal 45 days — aur CGHS se fark \(3 vs 6 months\)\.', 'Exam trap: 6 months (OPD/IPD), advance case 1 month, appeal 45 days — CGHS bhi ab 6 months (OM 01.06.2020).'),
    (r'mukhya note: Different se CGHS \(3 months\)!', 'mukhya note: CGHS jaisa hi 6 months (OM 01.06.2020)!'),
    (r'CS\(MA\) mein claim 6 mahine mein submit karo — CGHS ke 3 mahine se alag!', 'CS(MA) mein claim 6 mahine mein submit karo — CGHS bhi ab 6 mahine (OM 01.06.2020)!'),
    (r' — CGHS ka 3 months nahi! Bahut important distinction\.', ' — CGHS ka bhi ab 6 months hai (OM 01.06.2020).'),
    (r'Submit claim within 3 months of treatment date', 'Submit claim within 6 months of completion of treatment / discharge'),
    (r'; CGHS = 3 months', '; CGHS = 6 months (OM 01.06.2020)'),
    (r' \(CGHS = 3 months — different rules!\)', ' (CGHS is also 6 months since OM 01.06.2020)'),
    (r' \(CGHS = 3 months\)', ' (CGHS is also 6 months since OM 01.06.2020)'),
    (r'Within 3 months of treatment/medicine purchase', 'Within 6 months of completion of treatment / discharge (OM 01.06.2020; earlier 3 months)'),
    (r'claims beyond 3 months NOT entertained', 'only claims after 6 months need condonation of delay'),
    (r'\(Note: CS\(MA\) Rules has a 6-month period — different from CGHS\)', '(CS(MA) Rules also have a 6-month period)'),
    (r'claim within 3 months from your department', 'claim within 6 months from your department'),
    (r'claim reimbursement from your department within 3 months', 'claim reimbursement from your department within 6 months'),
    (r'Claim submitted within 3 months of treatment/purchase date', 'Claim submitted within 6 months of completion of treatment / discharge'),
    (r'within 3 months; CGHS rates applicable', 'within 6 months; CGHS rates applicable'),
    (r'Within 3 months: Submit claim within 3 months of treatment date', 'Within 6 months: Submit claim within 6 months of completion of treatment / discharge'),
    (r'"CGHS claim within 6 months"', '"CGHS claim must be within 3 months"'),
    (r'CGHS = 3 months \(CS\(MA\) = 6 months — different!\)', 'CGHS = 6 months (OM 01.06.2020; the old 3-month limit is obsolete)'),
    (r'CGHS = 3 months \(CS\(MA\) = 6 months\)', 'CGHS = 6 months (OM 01.06.2020); CS(MA) = 6 months'),
    (r'\(CS\(MA\) = 6 months — different!\)', '(CS(MA) = 6 months)'),
    (r'CS\(MA\) = 6 months — different!', 'CS(MA) = 6 months; CGHS is also 6 months since OM 01.06.2020'),
    (r'CS\(MA\) = 6 months \(CGHS = 3 months — different rules!\)', 'CS(MA) = 6 months (CGHS is also 6 months since OM 01.06.2020)'),
    (r'CS\(MA\) = 6 months ; CGHS = 3 months', 'CS(MA) = 6 months; CGHS = 6 months (OM 01.06.2020)'),
    (r'CS\(MA\) = 6 months \(CGHS = 3 months\)', 'CS(MA) = 6 months (CGHS is also 6 months since OM 01.06.2020)'),
    (r'CS\(MA\) = 6 months \(CGHS = 3 months — different rules!\)', 'CS(MA) = 6 months'),
    (r'CGHS claim: 3 months', 'CGHS claim: 6 months'),
    (r'\[Note: This is different from CGHS where limit is 3 months\]', '[CGHS limit is also 6 months since OM 01.06.2020]'),
    (r'Different from CGHS \(3 months\)!', 'Same 6-month limit as CGHS (OM 01.06.2020)!'),
    (r'CGHS = 3 months — alag hai!', 'CGHS bhi ab 6 months hai — OM 01.06.2020'),
    (r'CGHS ke 3 mahine se alag!', 'CGHS bhi ab 6 mahine hai (OM 01.06.2020)!'),
    (r'CGHS ka 3 months nahi!', 'CGHS ka bhi ab 6 months hai (OM 01.06.2020)!'),
]
for _rx, _rep in TIME_RULES:
    TEXT_RULES.append((_rx, _rep, TL_REASON))


# leaf-level rewrites for claim-deadline statements whose wording is split by bold markup
LEAF_REWRITES = [
    (r'^Within 3 months: Submit claim within 6 months', '<strong>Within 6 months:</strong> Submit claim within 6 months of completion of treatment / discharge (OM 01.06.2020)'),
    (r'^🔴 Critical — 6 Months \(CS\(MA\)\) vs 3 Months \(CGHS\)', '🔴 Critical — Claim time limit: 6 months for both CS(MA) and CGHS (CGHS since OM 01.06.2020)'),
    (r'^Within 3 months of treatment date$', 'Within <strong>6 months</strong> of completion of treatment / discharge (OM 01.06.2020)'),
    (r'^Within 3 months of treatment$', '<strong>6 months</strong> of completion of treatment / discharge (OM 01.06.2020)'),
    (r'^CGHS = 3 months \(CS\(MA\) = 6 months\)', 'CGHS = <strong>6 months</strong> (OM 01.06.2020); CS(MA) = 6 months'),
    (r'^CS\(MA\) = 6 months — critical difference!', 'CS(MA) = <strong>6 months</strong> (CGHS is also 6 months since OM 01.06.2020)'),
    (r'^CGHS claim deadline: Within 3 months', '<strong>CGHS claim deadline:</strong> within <strong>6 months</strong> of completion of treatment / discharge (OM 01.06.2020; earlier 3 months) — only claims after 6 months need condonation of delay (CS(MA) Rules also have a 6-month period)'),
    (r'^"CGHS claim must be within 3 months" — WRONG!', '"CGHS claim must be within 3 months" — <strong>WRONG!</strong> <strong>6 months</strong> since OM 01.06.2020 (CS(MA) is also 6 months)'),
    (r'^OPD reimbursement: Medicines issued from CGHS WC', '<strong>OPD reimbursement:</strong> Medicines issued from CGHS WC are FREE (no reimbursement needed — directly issued). If they buy OPD medicines from outside after CGHS reference — claim within <strong>6 months</strong> from your department'),
    (r'^Claim submitted within 3 months of treatment/purchase date', 'Claim submitted within <strong>6 months</strong> of completion of treatment / discharge'),
    (r'^Within 3 months: Submit claim within 3 months of treatment date', '<strong>Within 6 months:</strong> Submit claim within 6 months of completion of treatment / discharge'),
    (r'^CGHS claim: 3 months \| IPD advance', 'CGHS claim: <strong>6 months</strong> | IPD advance: 90% | Within: 10 days'),
    (r'^"CS\(MA\) claim within 3 months" — WRONG!', '"CS(MA) claim within 3 months" — <strong>WRONG!</strong> CS(MA) = <strong>6 months</strong> (CGHS is also 6 months since OM 01.06.2020)'),
    (r'^"CS\(MA\) claim = 3 months like CGHS" — WRONG!', '"CS(MA) claim = 3 months" — <strong>WRONG!</strong> CS(MA) = <strong>6 months</strong> (CGHS is also 6 months since OM 01.06.2020)'),
    (r'^"CS\(MA\) claim = 3 months like CGHS"$', '"CS(MA) claim = 3 months"'),
    (r'^"CS\(MA\) claims within 3 months" — ABSOLUTELY WRONG!', '"CS(MA) claims within 3 months" — <strong>ABSOLUTELY WRONG!</strong> CS(MA) = <strong>6 months</strong>; CGHS is also 6 months (OM 01.06.2020)'),
    (r'^CS\(MA\) claim deadline: 6 months \(CGHS = 3 months\)', 'CS(MA) claim deadline: <strong>6 months</strong> (CGHS is also 6 months since OM 01.06.2020)'),
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

    # ---- 1c. leaf rewrites (claim time limit)
    from bs4 import BeautifulSoup as _BS
    for el in body.find_all(['li', 'p', 'td', 'th']):
        if el.find(['li', 'p', 'td', 'th']):
            continue
        t = ws(el.get_text(' ', strip=True))
        for rx, new_html in LEAF_REWRITES:
            if re.search(rx, t):
                el.clear()
                frag = _BS('<x>' + new_html + '</x>', 'lxml').find('x')
                for ch in list(frag.children):
                    el.append(ch)
                log.append(dict(old=t, new=ws(el.get_text(' ', strip=True)), reason=TL_REASON, kind='leaf'))
                break

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
