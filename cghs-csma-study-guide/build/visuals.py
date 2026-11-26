"""Hand-authored visual aids (SVG flowcharts, timelines, comparison tables).
Every fact below is taken from the source guide (CGHS_CSMA_MASTER_GUIDE_ELABORATED.html).
Keys are card indexes (document order of .rule-card in the source)."""
from svg import *

def cmp(headers, rows, caption='', cls='cmp'):
    h = ''.join(f'<th scope="col">{x}</th>' for x in headers)
    r = ''.join('<tr>' + ''.join((f'<th scope="row">{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(row)) + '</tr>' for row in rows)
    cap = f'<caption>{caption}</caption>' if caption else ''
    return f'<div class="tblwrap"><table class="{cls}">{cap}<thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'

def fig(title, body, note=''):
    n = f'<p class="vnote">{note}</p>' if note else ''
    return f'<figure class="vis"><figcaption>{title}</figcaption>{body}{n}</figure>'

V = {}

# ---------- OVERVIEW: CGHS vs CS(MA) -----------
OVERVIEW = fig('CGHS vs CS(MA) Rules 1944 — side-by-side (figures as stated in the guide)', cmp(
    ['Point', 'CGHS', 'CS(MA) Rules, 1944'],
    [
     ['Claim deadline', '<b>3 months</b> of treatment / medicine purchase', '<b>6 months</b> (OPD: from treatment; IPD: from discharge); <b>1 month</b> from discharge if advance drawn (IPD)'],
     ['Who refers', 'Medical Officer of a CGHS Wellness Centre (specialist referral valid 3 months)', 'AMA (Authorised Medical Attendant) — Rule 5'],
     ['Consultation cap', 'Max <b>6 consultations</b>, max <b>3 specialists</b> per 3-month referral', '<b>4 consultations within 10 days</b> per spell of illness (AYUSH/Homoeopathy: up to 40 days)'],
     ['Where serving employees claim', 'Own Department/Ministry (not CGHS office); pensioners → AD, CGHS of city of registration', 'Controlling Authority (Rule 9); appeal within <b>45 days</b> to Central Government'],
     ['IPD advance', '90% of approved CGHS package rates', '90% (same framework); TB: 80% or Rs.36,000 whichever is less'],
     ['Financial powers to settle claims', 'Serving employees: HoD up to <b>Rs.10 lakh</b> without IFD (OM 16.02.2026). CGHS administration: AD Rs.15 lakh · Director Rs.25 lakh · AS&amp;DG Rs.50 lakh (OM 25.06.2026)', 'HoD up to <b>Rs.10 lakh</b> without IFD (OM 16.02.2026); above → Ministry with IFD; relaxation → MoHFW'],
     ['Family income test', 'Dependent: income &lt; Rs.9,000 + DA / month', 'Same (OM 08.11.2016 extends it to CS(MA))'],
     ['Parents / Parents-in-law', 'One-time irrevocable choice [OM 13.05.2026]', 'Extended to CS(MA) [OM 28.03.2024]; one-time choice [OM 13.05.2026]'],
     ['Legal basis', 'Executive scheme — no separate statute; governed by MoHFW guidelines, OMs, circulars (established 1954)', 'Statutory Rules (notified 1 Jan 1944) — legally enforceable rights'],
     ['Who is covered', 'Serving employees posted in a CGHS-covered area (mandatory); pensioners (if enrolled); serving employees outside such areas who exercised the one-time option (OM 17.09.2026)', 'Serving employees outside CGHS-covered areas who have NOT opted for CGHS; pensioners EXCLUDED'],
    ]), 'Take the exact wording of every cell from the section it points to — this table is a revision aid, not a substitute for the rule text.')

# ---------- PARA 3: family eligibility ----------
V[2] = fig('Family eligibility — decision flow (CGHS Para 3)', spine([
    dict(t='Is the person the SPOUSE?', k='d', side=('Covered automatically — no income test, no residence condition', 'g', 'Yes'), down_label='No'),
    dict(t='Son / unmarried daughter / dependent child?', k='d', side=('Son: till earning or age 25 (whichever earlier) · Daughter: till earning or marriage, any age · Permanently disabled son: any age — all need income < Rs.9,000+DA and normally residing', 'b', 'Yes')),
    dict(t='Divorced / separated / widowed daughter, widowed or unmarried sister, minor brother?', k='d', side=('Daughter & sister: any age · Minor brother: till 18 · Dependent income < Rs.9,000+DA', 'b', 'Yes')),
    dict(t='Transgender child / sibling (OM 16.09.2025)?', k='d', side=('Any age, financially dependent + certificate under Transgender Persons (Protection of Rights) Act, 2019', 'b', 'Yes')),
    dict(t='Parents OR Parents-in-law?', k='d', side=('ONE-TIME choice — either, not both [OM 26.07.2023 / 13.05.2026]; income < Rs.9,000+DA and normally residing; parents on FMA cannot be claimed', 'a', 'Yes')),
], 'Family eligibility decision flow', sw=300, side_w=480, bh=76), 'Dependency income test = income from all sources &lt; Rs.9,000 + DA per month (≈ Rs.14,670 at 63% DA from 01.07.2026 — recompute on date of consideration).')

# ---------- PARA 4: OM chronology timeline ----------
def _tl():
    w, h = 960, 250
    o = [svg_open(w, h, 'Parents vs Parents-in-law OM timeline')]
    o.append('<line x1="40" y1="60" x2="920" y2="60" class="ln"/>')
    items = [('03.03.1987', 'OM 4(1)-18/63-H', 'Only FEMALE employees may choose parents OR parents-in-law'),
             ('26.07.2023', 'OM H.11020/2/2023-EHS', 'MALE + FEMALE may choose either; supersedes earlier OMs'),
             ('28.03.2024', 'OM S.14025/15/2024-EHS', 'Extended to CS(MA) Rules beneficiaries'),
             ('13.05.2026', 'OM S.14025/15/2024-EHS(8270534)/I/3862000/2026', 'ONE-TIME irreversible option; no switching, even on demise')]
    for i, (d, om, t) in enumerate(items):
        x = 130 + i * 230
        o.append(f'<circle cx="{x}" cy="60" r="11" class="dot"/>')
        o.append(text(x, 30, d, 15, bold=True))
        o.append(box(x - 105, 85, 210, 150, om + '\n' + t, ['n', 'b', 'b', 'a'][i], 12, chars=26, bold_first=True))
    o.append(svg_close())
    return ''.join(o)
V[3] = fig('Parents / Parents-in-law — OM timeline', _tl())

# ---------- PARA 5: card colours, application, options, contributions ----------
def _cards():
    w, h = 900, 190
    o = [svg_open(w, h, 'CGHS card stripe colours')]
    data = [('#2563eb', 'BLUE', 'Serving Central Govt employees'), ('#16a34a', 'GREEN', 'Pensioners · Ex-MPs · Retired personnel · Freedom fighters · Family pensioners'),
            ('#dc2626', 'RED', 'Sitting Members of Parliament'), ('#eab308', 'YELLOW', 'PIB-accredited journalists · Employees of autonomous companies')]
    for i, (c, n, t) in enumerate(data):
        x = 12 + i * 222
        o.append(f'<rect x="{x}" y="10" width="206" height="160" rx="12" class="cardbody"/>')
        o.append(f'<rect x="{x}" y="10" width="206" height="36" rx="12" fill="{c}"/>')
        o.append(f'<rect x="{x}" y="30" width="206" height="16" fill="{c}"/>')
        o.append(text(x + 103, 36, n, 15, bold=True, cls='onclr'))
        for j, ln in enumerate(wrap(t, 24)):
            o.append(text(x + 103, 74 + j * 18, ln, 13))
    o.append(svg_close())
    return ''.join(o)
V[4] = (fig('CGHS card — stripe colour = category', _cards())
    + fig('Card application — 5 steps', vflow([
        ('Step 1 — Mandatory online application at cghs.nic.in → temporary reference number', 's'),
        ('Step 2 — Fill form online, take printout, affix photographs', 'n'),
        ('Step 3 — Submit hard copy to Department/Office (sponsoring HoO/HoD)', 'n'),
        ('Step 4 — Department submits to Additional Director (AD), CGHS of the city', 'n'),
        ('Step 5 — AD office issues CGHS card', 'g')], 'CGHS card application steps', bh=44, gap=22, bw=620))
    + fig('Pensioner options', cmp(['Option', 'Description', 'Facility'], [
        ['A', 'Full CGHS card — no FMA taken', 'OPD + IPD (cashless / reimbursement)'],
        ['B', 'CGHS “IPD Only” card — FMA taken for OPD', 'IPD cashless at empanelled hospitals; FMA for OPD'],
        ['C', 'FMA only — no CGHS card', 'Rs.3,000/month for OPD only'] ])))
V[5] = (fig('Monthly contribution by pay level (7th CPC)', hbar([
        ('Level 1–5', 250, 'Rs.250 /mo (Rs.3,000 /yr)'), ('Level 6', 450, 'Rs.450 /mo (Rs.5,400 /yr)'),
        ('Level 7–11', 650, 'Rs.650 /mo (Rs.7,800 /yr)'), ('Level 12+', 1000, 'Rs.1,000 /mo (Rs.12,000 /yr)')], 'Monthly contribution', w=900, label_w=120))
    + fig('Lifetime card = 120 × monthly rate', hbar([
        ('Level 1–5', 30000, 'Rs.30,000'), ('Level 6', 54000, 'Rs.54,000'), ('Level 7–11', 78000, 'Rs.78,000'), ('Level 12+', 120000, 'Rs.1,20,000')],
        'Lifetime contribution', w=900, label_w=120, color='a'))
    + fig('Ward entitlement in private empanelled hospitals (by basic pay)', cmp(['Basic pay / month', 'Ward'], [
        ['Up to Rs.36,500', 'General ward'], ['Rs.36,501 – Rs.50,500', 'Semi-private ward'], ['Rs.50,501 and above', 'Private ward']]), 'Ward is based on BASIC PAY drawn, not pension. It does not apply in Govt hospitals.'))

# ---------- PARA 8: referral flow ----------
V[7] = fig('CGHS referral — which route applies? (OM 28.06.2024 + SOP 02.09.2024)', spine([
    dict(t='Treatment at a GOVERNMENT hospital? (AIIMS, INIs, NE institutions, Tata Memorial, CG hospitals, CGHS WCs)', k='d', side=('NO referral / permission / endorsement — even for unlisted investigations & procedures [Clause A]', 'g', 'Yes'), down_label='No'),
    dict(t='Emergency at empanelled hospital?', k='d', side=('No referral or endorsement. Cashless on emergency certificate; claim via BCA portal. Unlisted: NHA portal — no AD approval [Clause D]', 'g', 'Yes')),
    dict(t='Beneficiary aged 70+ ?', k='d', side=('No referral for any specialist; listed procedures free of referral; UNLISTED need CGHS authority approval [Clause C]', 'b', 'Yes')),
    dict(t='Chronic: cardiac surgery / organ transplant / neurosurgery / ESRD / cancer / autoimmune / neurological (7)', k='d', side=('Consultations & investigations without time limit on primary referral; no repeat referral [Clause E]', 'b', 'Yes')),
    dict(t='Referral from CGHS WC Medical Officer — valid 3 months · max 3 specialists · max 6 consultations [B(i)]', k='a'),
], 'CGHS referral decision flow', sw=340, side_w=480, bh=74, gap=38), 'Follow-up must be at the SAME HCO [B(ii)]. CT/MRI always need separate CGHS endorsement [B(iii)]. Tests at a different diagnostic centre need WC endorsement [SOP OM 05.08.2024].')

# ---------- PARA 10: MRC ----------
V[9] = (fig('Medical reimbursement claim (CGHS) — process', vflow([
    ('Treatment / medicine purchase', 's'),
    ('Submit claim within 3 MONTHS on BCA portal (claims beyond 3 months not entertained)', 'a'),
    ('Serving employee → own Department / Ministry   |   Pensioner → AD, CGHS city of registration', 'n'),
    ('Processing — avg 21 days (60–120 days for non-empanelled hospital cases); SMS at every stage; track via myCGHS app', 'n'),
    ('Settlement', 'g')], 'CGHS MRC process', bh=54, gap=26, bw=700))
  + fig('Competent authority & monetary limit', cmp(['Scenario', 'Authority', 'Limit'], [
    ['Emergency (within prescribed rates) — serving', 'Head of Ministry/Dept/Office', 'No financial limit'],
    ['Emergency — pensioners', 'Head of CGHS covered city', 'No financial limit (as stated in the guide; not confirmed by OM 25.06.2026 — see Verify tab)'],
    ['General MRC — serving', 'Head of Ministry/Dept/Office', 'Up to Rs.10 lakh (OM 16.02.2026; earlier Rs.5L, Rs.2L)'],
    ['General MRC — pensioners / CGHS beneficiaries', 'Additional Director, CGHS city/zone (OM 25.06.2026)', 'Up to Rs.15 lakh; Director, CGHS Rs.25 lakh; AS&amp;DG, CGHS Rs.50 lakh; above Rs.50 lakh → MoHFW with IFD'],
    ['Per rate list but above Rs.10 lakh — serving employees (HoD route)', 'Ministry/Dept with IFD consultation', '&gt; Rs.10 lakh'],
    ['Rule relaxation · Air travel / ex-post facto', 'MoHFW', 'As needed'] ])))

# ---------- RULE 4: TA ----------
def _ta():
    w, h = 900, 260
    o = [svg_open(w, h, 'Rule 4 travelling allowance — 5 miles rule')]
    o.append(box(30, 100, 190, 70, 'AMA consulting room', 'b', 15))
    o.append(box(680, 100, 190, 70, 'Place where patient falls ill', 'n', 15))
    o.append('<line x1="220" y1="135" x2="680" y2="135" class="ln dash"/>')
    o.append(text(450, 122, 'more than 5 miles (≈ 8 km) — shortest route', 14, bold=True))
    o.append(poly([(660, 190), (250, 190)], 'Rule 4(1)(a): patient travels to AMA → PATIENT gets TA (to & fro)', 260, 212))
    o.append(poly([(250, 70), (660, 70)], '', 0, 0))
    o.append(text(455, 52, 'Rule 4(1)(b): patient too ill to travel → AMA gets TA (to & fro)', 13, bold=True))
    o.append(text(450, 245, 'Written AMA certificate is mandatory · distance measured by SHORTEST route · compounders / lab assistants get NO TA', 13))
    o.append(svg_close())
    return ''.join(o)
V[20] = fig('Rule 4 — who gets TA?', _ta())

# ---------- RULE 5 ----------
def _tenday():
    w, h = 900, 190
    o = [svg_open(w, h, '4 consultations in 10 days')]
    o.append(text(110, 40, 'Day 0 — treatment begins', 13, bold=True))
    o.append(text(790, 40, 'Day 10', 13, bold=True))
    o.append('<line x1="110" y1="60" x2="790" y2="60" class="ln"/>')
    o.append('<circle cx="110" cy="60" r="9" class="dot"/><circle cx="790" cy="60" r="9" class="dot"/>')
    o.append(box(110, 78, 680, 40, 'First FOUR consultations / visits — one continuous spell of illness, one particular disease', 'a', 14))
    o.append(box(110, 130, 680, 50, 'Beyond 4 → specialist refers patient to OPD of Govt / recognized hospital.  Indian System of Medicine & Homoeopathy: the 10 days can be extended up to 40 days by the AMA', 'g', 13))
    o.append(svg_close())
    return ''.join(o)
V[21] = (fig('Rule 5(1) — AMA referral to a specialist', spine([
        dict(t='AMA: case is serious / special — needs someone other than himself', k='s', down_label=''),
        dict(t='Specialist / MO at a Government hospital in the district?', k='d', side=('Rule 5(1)(a): refer there', 'g', 'Yes'), down_label='No'),
        dict(t='Any Govt hospital that can reasonably be reached?', k='d', side=('Rule 5(1)(b): refer there', 'g', 'Yes'), down_label='No'),
        dict(t='Refer to PRIVATE specialist — with AMA certificate that no Govt specialist is available [Rule 5(1)(c)]', k='a')],
        'Rule 5(1) referral flow', sw=360, side_w=360, bh=62, gap=34))
    + fig('4 consultations in 10 days', _tenday(), 'Fresh illness after cure of a particular illness = “fresh consultation”. Same doctor for superimposed disease = “fresh consultation”.')
    + fig('AMA consultation fees (OM 20.09.2023)', cmp(['Doctor', 'First', 'Subsequent'], [['Specialist / PG', 'Rs.350', 'Rs.350'], ['MBBS', 'Rs.200', 'Rs.200'], ['Injection IM/SC', 'Rs.25', '—'], ['Injection IV', 'Rs.50', '—']]), 'No separate day / night charges.'))

# ---------- RULE 6 ----------
V[22] = fig('Rule 6(1) — where is free hospital treatment available?', spine([
    dict(t='Govt servant falls ill — AMA opines hospital treatment needed', k='s'),
    dict(t='Govt hospital at / near the place can give necessary & suitable treatment?', k='d', side=('Rule 6(1)(a): free treatment there', 'g', 'Yes'), down_label='No'),
    dict(t='Non-Govt hospital at / near the place can give it?', k='d', side=('Rule 6(1)(b): recognized private hospital (CS(MA)/CGHS) — AMA opinion', 'g', 'Yes'), down_label='No'),
    dict(t='Ill away from headquarters and AMA opinion unobtainable', k='a', side=('Rule 6(1)(c): head of nearest Govt hospital decides the appropriate hospital', 'g', ''))],
    'Rule 6 hospital entitlement', sw=360, side_w=380, bh=62, gap=34), 'Amounts paid are reimbursed on AMA certificate; appeal within 45 days of rejection.')

# ---------- RULE 11 ----------
V[27] = fig('Rule 11 — treatment outside India', spine([
    dict(t='Govt servant / family member needs treatment abroad (condition listed in the Table to Rule 11(3))', k='s'),
    dict(t='Apply through own Ministry / Department to the Standing Committee (prescribed proforma)', k='n'),
    dict(t='Standing Committee examines (records, second opinion) and recommends — Rule 11(2)', k='n'),
    dict(t='Prior approval obtained?', k='d', side=('Rule 11(7) exception: if prior approval was not feasible (e.g. emergency abroad), Central Govt may still authorize reimbursement', 'a', 'No'), down_label='Yes'),
    dict(t='Ministry incurs expenditure on Standing Committee certificate — scale = Indian Foreign Service official of corresponding grade (AMA Scheme, MEA)', k='g')],
    'Rule 11 treatment abroad flow', sw=380, side_w=360, bh=66, gap=34), 'Rule 11(4): the Table can be revised by Central Govt (additions / deletions by Gazette notification).')

# ---------- CS(MA) advance + deadlines ----------
V[29] = (fig('Medical advance', cmp(['Treatment', 'Advance', 'Condition'], [
        ['Indoor (IPD) — all', '90% of approved CGHS package rates', 'Certificate from treating physician of Govt/recognized hospital'],
        ['OPD', '90% of total estimate', 'Only if estimate &gt; Rs.10,000'],
        ['TB (&gt; 3 months)', '80% of estimate OR Rs.36,000 — whichever is less', 'Treatment duration exceeds 3 months']]),
        'Sanctioned within 10 days · ordinarily one advance per illness · recovered from final claim.')
    + fig('Claim deadlines (CS(MA)) vs CGHS', hbar([
        ('IPD, advance drawn', 1, '1 month from discharge'), ('CGHS (all claims)', 3, '3 months'),
        ('CS(MA) OPD / IPD', 6, '6 months (from treatment / discharge)')], 'Claim deadline comparison', w=900, label_w=190, maxv=6, color='a'))
    + fig('HoD settlement ceiling — history', hbar([
        ('Original', 2, 'Rs.2 lakh'), ('OM 23.11.2016', 5, 'Rs.5 lakh'), ('OM 16.02.2026', 10, 'Rs.10 lakh (no IFD consultation)')], 'HoD ceiling history', w=900, label_w=150, maxv=10, color='g'),
        'Above Rs.10 lakh → Ministry/Dept with IFD consultation. Rule relaxation → MoHFW. Appeal against rejection: 45 days to Central Government.'))

# ---------- PARA 9: rate framework ----------
V[8] = (fig('CGHS rate framework — OM 03.10.2025 (effective 13.10.2025): base = 100', hbar([
        ('Non-NABH / non-NABL', 85, '15% lower than NABH'), ('NABH / NABL (base)', 100, 'Standard base rate'), ('Super-specialty (200+ beds)', 115, '15% higher than NABH'),
        ('Tier III (Z cities)', 80, '20% lower than Tier I'), ('Tier II (Y cities)', 90, '10% lower than Tier I'), ('Tier I (X cities)', 100, 'Standard base rate'),
        ('General ward', 95, '5% lower than semi-private'), ('Semi-private (reference)', 100, 'Base (reference) rate'), ('Private ward', 105, '5% higher than semi-private')],
        '4-dimension rate framework', w=900, label_w=230, maxv=115, row=34),
        'Dimension 1 = hospital accreditation · 2 = city tier (NE states + J&K + Ladakh = Tier II) · 3 = ward · 4 = consultations, investigations, radiotherapy, day-care and minor procedures are UNIFORM across wards.')
    + fig('Multiple procedures in the same session', cmp(['Procedure', 'Reimbursement'], [
        ['1st (primary) procedure', '100%'], ['2nd procedure (same session)', '50%'], ['3rd and subsequent (same session)', '25% each'], ['Bilateral / identical procedures (different sites)', '100% for one side + 50% for the second']]))
    + fig('2023 consultation & room-rent rates (OM 12.04.2023 — still applicable)', cmp(['Item', 'Previous', 'Revised'], [
        ['OPD consultation', 'Rs.150', 'Rs.350'], ['IPD consultation', 'Rs.300', 'Rs.350'], ['Super-specialty / psychiatry consultation', '—', 'Rs.700'],
        ['ICU (all wards, all-inclusive)', 'Rs.862 (NABH) + room rent', 'Rs.5,400 (Non-NABH: Rs.5,400 × 0.85 = Rs.4,590)'],
        ['General ward room rent', 'Rs.1,000', 'Rs.1,500'], ['Semi-private room rent', 'Rs.2,000', 'Rs.3,000'], ['Private ward room rent', 'Rs.3,000', 'Rs.4,500']])))

# ---------- RULE 1: who is covered ----------
V[17] = fig('Rule 1 — is the person covered by CS(MA) Rules?', spine([
    dict(t='Retired Govt servant (pensioner), defence personnel, All-India Service officer, or officer posted abroad?', k='d', side=('NOT covered — Notes 2(i), 2(iv), 2(vii), 2(ii)/(viii)  (pensioners → CGHS or FMA; AIS → AIS(MA) Rules 1954)', 'r', 'Yes'), down_label='No'),
    dict(t='Employee in a CGHS city (e.g. Delhi / New Delhi)?', k='d', side=('NOT covered — governed by CGHS [Note 2(vi)]', 'r', 'Yes')),
    dict(t='Railway service?', k='d', side=('Excluded under Rule 1(2)(i) — BUT railway employee on deputation to a Central Govt office IS covered [Note 1]', 'a', 'Yes')),
    dict(t='Serving CG employee in a non-CGHS area (also: probationer, leave preparatory to retirement, suspension, re-employed pensioner, State servant on deputation to CG)', k='g'),
], 'Rule 1 coverage decision flow', sw=360, side_w=440, bh=70, gap=34), 'Concessions extend to the employee’s family, subject to conditions in the rules.')

# ---------- RULE 3 ----------
V[19] = fig('Rule 3 — claim and appeal path', vflow([
    ('Free medical attendance by the AMA (consultation, prescriptions, AMA-ordered tests at Govt hospital, injections, dressings, scheduled medicines)', 's'),
    ('If paid by the employee → claim reimbursement with a WRITTEN AMA CERTIFICATE (attendance necessary and actually provided)', 'n'),
    ('Controlling Officer may reject claims that fail genuineness / other requirements — without consulting MoHFW (doubtful cases → MoHFW)', 'a'),
    ('Rejected? Appeal to Central Government within 45 days of receipt of the rejection order', 'g')],
    'Rule 3 claim and appeal', bh=62, gap=26, bw=700, size=13)) + fig('Duration limits for one continuous spell of illness', cmp(['System', 'Limit'], [
    ['Allopathic AMA + specialist (combined)', '10 days — specialist beyond 4 consultations → refer to OPD of Govt / recognized hospital'],
    ['Indian System of Medicine / Homoeopathy AMA', 'Up to 40 days — beyond that, referral to Govt hospital']]))

# ---------- RULE 7 ----------
V[23] = fig('Rule 7 — treatment at residence', spine([
    dict(t='AMA opines: (a) no suitable hospital nearby / remote, OR (b) illness too severe to move the patient', k='d', side=('EITHER condition is enough — treatment at residence permitted [Rule 7(1)]', 'g', 'Yes'), down_label=''),
    dict(t='Entitlement [Rule 7(2)]: sum equal to the cost of SIMILAR treatment in a hospital (not more)', k='n'),
    dict(t='Claim with AMA certificate stating (a) reasons for the opinion and (b) cost of similar hospital treatment [Rule 7(3)]', k='g')],
    'Rule 7 treatment at residence', sw=380, side_w=380, bh=62, gap=32), 'GD(1): treatment at the AMA’s own private clinic / nursing home is NOT covered by Rule 7.')

# ---------- AMA appointment ----------
V[28] = fig('AMA appointment — process (CS(MA))', vflow([
    ('Adequate Govt doctors not available within 5 km radius (8 km by some references) → private registered practitioner may be appointed', 's'),
    ('HoD verifies the duly filled proforma + character & antecedents through local police', 'n'),
    ('HoD issues appointment order — stations / areas, category of employees, validity', 'n'),
    ('Annual re-verification is mandatory (qualification & registration valid, still willing; 5-km basis still holds)', 'a')],
    'AMA appointment flow', bh=58, gap=26, bw=720, size=13))
