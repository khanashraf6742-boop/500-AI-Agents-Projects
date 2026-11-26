"""Memory sheet (key numbers + mnemonics) and order timeline. Numbers are from the guide / verified 2026 orders;
mnemonics are memory aids written for this guide and are labelled as such."""
from html import escape

# (group, item, value, rule-card ordinal)
NUMS = [
 ('CGHS basics', 'CGHS established', '1954 (replaced CHSS); no separate statute', 0),
 ('CGHS basics', 'Wellness Centre timing', 'Monday–Saturday 7:30 AM – 2:00 PM', 0),
 ('CGHS basics', 'Card colours', 'Blue serving · Green pensioners / ex-MPs · Red sitting MP · Yellow PIB journalists', 4),
 ('CGHS basics', 'Plastic card replacement / digital card', 'Rs.100 / free', 4),
 ('CGHS basics', 'Monthly contribution (7th CPC)', 'L1–5 Rs.250 · L6 Rs.450 · L7–11 Rs.650 · L12+ Rs.1,000', 5),
 ('CGHS basics', 'Lifetime card', '120 × monthly rate: Rs.30,000 / 54,000 / 78,000 / 1,20,000', 5),
 ('CGHS basics', 'FMA', 'Rs.3,000 per month w.e.f. 01.01.2022; mutually exclusive with CGHS OPD', 5),
 ('CGHS basics', 'Ward entitlement (basic pay)', 'Up to Rs.36,500 general · 36,501–50,500 semi-private · 50,501+ private', 5),
 ('Family', 'Dependency income limit', 'Below Rs.9,000 + DA per month (≈ Rs.14,670 at 63% DA from 01.07.2026)', 2),
 ('Family', 'Son / daughter / brother', 'Son till earning or 25 · Daughter till earning or marriage · Minor brother till 18', 2),
 ('Family', 'Parents / parents-in-law', 'One-time irrevocable choice (OM 13.05.2026)', 3),
 ('Family', 'Critical / terminal illness (sons, brothers)', 'Lifelong cover on Board / LTC assessment (OM 01.09.2026, 26.10.2026); card first for 1 year', 2),
 ('Coverage', 'CS(MA) vs CGHS', 'Mandatory CGHS within covered area (district HQ limits); one-time irrevocable option for others (OM 17.09.2026)', 16),
 ('Referral & approvals', 'Specialist referral', '3 months · max 3 specialists · max 6 consultations', 7),
 ('Referral & approvals', 'Government hospital (AIIMS, INIs, Tata Memorial…)', 'No referral at all, even for unlisted items', 7),
 ('Referral & approvals', 'Tests', 'Same hospital up to Rs.3,000 each; endorsement for CT / MRI / PET or above Rs.3,000 (relayed CGHS HQ text)', 7),
 ('Referral & approvals', 'STC-type cases (OM 01.09.2026)', 'AD CGHS + 3-member LTC · deficiencies in 3 working days · decision in 15 working days', 7),
 ('Money & time limits', 'Claim deadline', 'CGHS 3 months · CS(MA) 6 months (1 month from discharge if IPD advance drawn)', 29),
 ('Money & time limits', 'Advance', 'IPD 90% · OPD 90% only if estimate > Rs.10,000 · TB 80% or Rs.36,000 · sanction in 10 days', 29),
 ('Money & time limits', 'Appeal', '45 days to the Central Government', 19),
 ('Money & time limits', 'HoD ceiling (serving employees)', 'Rs.10 lakh without IFD (OM 16.02.2026); earlier Rs.2L → Rs.5L', 29),
 ('Money & time limits', 'CGHS authorities (OM 25.06.2026)', 'AD Rs.15L · Director Rs.25L · AS&DG Rs.50L · above → MoHFW + IFD', 9),
 ('Money & time limits', 'Unlisted items (OM 25.06.2026)', 'AD Rs.2L · Director Rs.5L · AS&DG Rs.10L', 9),
 ('CS(MA) Rules', 'Rule 4 distance', '5 miles (≈ 8 km) by the shortest route', 20),
 ('CS(MA) Rules', 'Rule 5 consultations', '4 within 10 days (Indian systems / Homoeopathy up to 40 days)', 21),
 ('CS(MA) Rules', 'AMA fees (OM 20.09.2023)', 'Specialist Rs.350 · MBBS Rs.200 · injection IM/SC Rs.25, IV Rs.50', 28),
 ('CS(MA) Rules', 'AMA for private practitioners', 'HoD appoints when no adequate Govt doctor within 5 km; annual re-verification', 18),
 ('Rates', 'October 2025 framework', 'Non-NABH −15% · Tier II −10% · Tier III −20% · general ward −5% · private +5%', 8),
 ('Rates', 'Consultations 2023', 'OPD Rs.350 · super-specialty Rs.700 · ICU Rs.5,400 all-inclusive', 8),
 ('Rates', 'Multiple procedures', '100% / 50% / 25%', 8),
 ('Devices', 'Cochlear implant (OM 09.11.2026)', 'Rs.7,00,000 pre-lingual · Rs.6,00,000 post-lingual (incl. GST)', 10),
 ('Devices', 'Hearing aids (OM 01.12.2020)', 'Digital BTE Rs.8,000 · Digital ITC/CIC Rs.9,000 per ear', 24),
]

# memory aids (written for this guide — not quotes from any order)
AIDS = [
 ('3-6-3', 'Referral: 3 months, 6 consultations, 3 specialists.'),
 ('3 vs 6', 'CGHS claims in 3 months; CS(MA) in 6 months (CS-six).'),
 ('90-80-36', 'IPD advance 90%, TB advance 80% or Rs.36,000.'),
 ('2 → 5 → 10', 'HoD ceiling: Rs.2 lakh, then 5, now 10 lakh.'),
 ('15 – 25 – 50', 'CGHS ladder: AD, Director, AS&DG (lakh).'),
 ('4 in 10, 40 for AYUSH', 'Four consultations in ten days; Indian systems up to forty.'),
 ('5 miles ≈ 8 km', 'Rule 4 travel allowance distance.'),
 ('B-G-R-Y', 'Card stripes: Blue serving, Green pensioner, Red MP, Yellow PIB.'),
 ('7 and 6', 'Cochlear ceilings now: seven lakh pre-lingual, six lakh post-lingual (older Rs.5,35,000 is obsolete).'),
]

# key orders for the timeline: (date, short label, rc-link)
TIMELINE = [
 ('01.12.2020', 'Hearing-aid rates revised (Digital BTE / ITC-CIC)', 24),
 ('12.04.2023', 'Consultation and room-rent rates revised', 8),
 ('26.07.2023', 'Parents OR parents-in-law choice for male and female employees', 3),
 ('20.09.2023', 'AMA consultation / injection fees revised (CS(MA))', 28),
 ('28.03.2024', 'Parents / parents-in-law option extended to CS(MA)', 3),
 ('28.06.2024', 'Revised referral guidelines (+ SOP 02.09.2024)', 7),
 ('03.10.2025', 'Revised CGHS package rates (effective 13.10.2025)', 8),
 ('16.09.2025', 'Dependent transgender children and siblings covered', 2),
 ('09.01.2026', 'DANICS / AGMUT pensioners’ option', 4),
 ('16.02.2026', 'HoD ceiling Rs.10 lakh without IFD', 29),
 ('13.05.2026', 'Parents / parents-in-law: one-time option clarified', 3),
 ('25.06.2026', 'Revised financial powers of CGHS authorities', 9),
 ('17.07.2026', 'Bhavishya portal for pensioner cards', 4),
 ('24.07.2026', 'Tirzepatide / Semaglutide guidelines', 6),
 ('01.09.2026', 'Decentralised STC approvals; critical-illness relaxation', 7),
 ('17.09.2026', '5 km rule removed; one-time CGHS option', 16),
 ('26.10.2026', 'Critical-illness cases via LTC; 42-disease list', 2),
 ('28.10.2026', 'Family pensioners: divorced / widowed daughters', 2),
 ('29.10.2026', 'DA 63% from 01.07.2026', 2),
 ('09.11.2026', 'Cochlear implant ceilings revised', 10),
]
TIMELINE.sort(key=lambda t: tuple(reversed(t[0].split('.'))))


def build(ref):
    groups = {}
    for g, item, val, rc in NUMS:
        groups.setdefault(g, []).append((item, val, rc))
    tabs = ''
    for g, rows in groups.items():
        tabs += (f'<div class="tblwrap"><table class="cmp"><caption>{escape(g)}</caption><thead><tr><th scope="col">Item</th><th scope="col">Value to remember</th><th scope="col">Section</th></tr></thead><tbody>'
                 + ''.join(f'<tr><th scope="row">{escape(i)}</th><td>{escape(v)}</td><td><a href="{ref(rc)}">open</a></td></tr>' for i, v, rc in rows) + '</tbody></table></div>')
    aids = ''.join(f'<div class="listitem"><span class="tag">{escape(a)}</span>{escape(b)}</div>' for a, b in AIDS)
    tl = '<ol class="tl">' + ''.join(f'<li><b>{d}</b> <a href="{ref(rc)}">{escape(t)}</a></li>' for d, t, rc in TIMELINE) + '</ol>'
    return (f'<p class="lead">Every figure below is taken from the guide or from the verified 2026 orders. Printable: use the 🖨️ button.</p>'
            f'<h3>Numbers that get tested</h3>{tabs}'
            f'<h3>Memory aids <span class="tag">written for this guide, not from any order</span></h3>{aids}'
            f'<h3>Order timeline</h3>{tl}')
