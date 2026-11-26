"""Question bank. Hand-written questions use only facts stated in the guide or in the verified 2026 orders
(each cites its section); the rest are generated from the guide's own tables and trap lists.
Format of every question: dict(k=kind, q=text, o=[options] (mcq: correct option FIRST, shuffled in the browser),
a=index for tf, why=explanation, c=card id, s=section label, p=part)
"""
import re, random, html

# (question, correct, [3 wrong], explanation, rule-card ordinal, kind)
HAND = [
 ('A serving employee’s medical claim is within prescribed rates, needs no relaxation of rules and totals Rs.9 lakh. Who can settle it without consulting the Internal Finance Division?',
  'The Head of Department (limit Rs.10 lakh)', ['Only MoHFW', 'The Head of Department only up to Rs.5 lakh', 'Only the Additional Director, CGHS'],
  'OM 16.02.2026 raised the HoD ceiling from Rs.5 lakh to Rs.10 lakh without IFD consultation (no relaxation of rules; entitlement strictly per prescribed rates).', 29, 'case'),
 ('Above which amount does a serving employee’s claim (per rate list) need IFD consultation by the Ministry/Department?',
  'Rs.10 lakh', ['Rs.2 lakh', 'Rs.5 lakh', 'Rs.15 lakh'], 'The earlier Rs.2 lakh and Rs.5 lakh ceilings (OM 23.11.2016) were replaced by Rs.10 lakh on 16.02.2026.', 29, 'fact'),
 ('Under CGHS OM 25.06.2026, up to what amount can the Additional Director, CGHS city/zone settle claims at approved rates?',
  'Rs.15 lakh', ['Rs.7 lakh', 'Rs.10 lakh', 'Rs.25 lakh'], 'Earlier Rs.7 lakh; revised to Rs.15 lakh. Director, CGHS: Rs.25 lakh; AS&DG: Rs.50 lakh.', 9, 'fact'),
 ('Under CGHS OM 25.06.2026, who can settle a claim of Rs.40 lakh at approved rates?',
  'Additional Secretary & DG, CGHS', ['Additional Director, CGHS city/zone', 'Director, CGHS', 'Only MoHFW with IFD'], 'Director CGHS goes up to Rs.25 lakh; AS&DG up to Rs.50 lakh; above Rs.50 lakh → MoHFW with IFD concurrence.', 9, 'case'),
 ('Unlisted investigation / procedure / implant with no CGHS rate: what is the Additional Director’s limit under OM 25.06.2026?',
  'Up to Rs.2 lakh', ['Up to Rs.1 lakh', 'Up to Rs.5 lakh', 'Up to Rs.10 lakh'], 'AD Rs.2 lakh, Director Rs.5 lakh, AS&DG Rs.10 lakh; above → Ministry with IFD.', 9, 'fact'),
 ('A pensioner wants elective treatment at a non-empanelled hospital. Who considers permission / ex-post facto approval?',
  'Additional Director of the concerned CGHS city/zone', ['The pensioner’s former Department', 'Head of the Wellness Centre', 'MoHFW only'], 'OM 25.06.2026 para 2C(i); reimbursement restricted to CGHS package rates or actual, whichever is less.', 9, 'case'),
 ('Who may appoint a private medical practitioner as AMA (per the Government Decision in the guide)?',
  'The Head of Department', ['The patient’s family', 'The CGHS Additional Director', 'The nearest hospital superintendent'], 'Rule 2(a) GD(2): HoD issues the appointment order after a duly filled proforma and police verification of antecedents.', 18, 'fact'),
 ('A private practitioner can be appointed AMA when:',
  'Adequate Government doctors are not available within a 5 km radius', ['The employee prefers a private doctor', 'The Government doctor is on leave', 'The employee is posted abroad'], 'Rule 2(a) GD(1) (8 km by some references).', 18, 'fact'),
 ('Which statement about honorary medical officers outside hospital precincts is correct?',
  'They are treated like private practitioners and are not AMAs', ['They are AMAs everywhere', 'They are AMAs only for Group A', 'They are AMAs only in Delhi'], 'Rule 2(a) Note 5; exception: Andhra States.', 18, 'fact'),
 ('Can the Controlling Officer reject a claim that fails genuineness without consulting MoHFW?',
  'Yes — he is fully empowered', ['No — MoHFW must always be consulted', 'Only for claims above Rs.10 lakh', 'Only with IFD concurrence'], 'Rule 3 GD(3) and Rule 9; doubtful / relaxation cases go to MoHFW.', 19, 'fact'),
 ('A claim is rejected by the Controlling Officer. The appeal lies to:',
  'The Central Government, within 45 days', ['MoHFW, within 30 days', 'The Controlling Officer, within 60 days', 'CGHS Director, within 45 days'], 'Rule 3 GD(4). Trap: “appeal to MoHFW within 45 days” is wrong.', 19, 'fact'),
 ('Claim deadline: CGHS versus CS(MA)?',
  'CGHS 3 months; CS(MA) 6 months', ['CGHS 6 months; CS(MA) 3 months', 'Both 3 months', 'Both 6 months'], 'CS(MA): 6 months (1 month from discharge if IPD advance drawn).', 29, 'fact'),
 ('IPD medical advance is:',
  '90% of approved CGHS package rates', ['80% of package rates', '100% of the estimate', '50% of the estimate'], 'TB advance (treatment > 3 months): 80% or Rs.36,000, whichever is less.', 29, 'fact'),
 ('An OPD advance is available only if the estimated expenditure exceeds:',
  'Rs.10,000', ['Rs.3,000', 'Rs.5,000', 'Rs.36,000'], 'Advance = 90% of the estimate; sanctioned within 10 days.', 29, 'fact'),
 ('Under Rule 5, the first four consultations should be completed within:',
  '10 days (up to 40 days for Indian systems / Homoeopathy by the AMA)', ['4 days', '30 days for all systems', '10 days for Indian systems and 40 for allopathy'], 'One continuous spell of illness, one particular disease.', 21, 'fact'),
 ('A patient falls ill more than five miles (about 8 km) by the shortest route from the AMA. Rule 4(1)(a) gives travelling allowance to:',
  'The patient, if he travels to the AMA', ['The AMA’s compounder', 'The AMA, always', 'Nobody'], 'If the patient is too ill to travel, the AMA gets the TA (Rule 4(1)(b)). Compounders and lab assistants get none.', 20, 'fact'),
 ('A CGHS specialist referral from a Wellness Centre MO is valid for:',
  '3 months, up to 3 specialists and 6 consultations', ['6 months, 3 specialists, 4 consultations', '3 months, 2 specialists, 10 consultations', '1 month, 1 specialist, 6 consultations'], 'Applies only to referrals issued by CGHS MOs.', 7, 'fact'),
 ('A CGHS beneficiary wants to consult a specialist at AIIMS. Is a Wellness Centre referral needed?',
  'No — no referral, permission or endorsement at Government hospitals', ['Yes, always', 'Yes, but only for unlisted procedures', 'Only for CT/MRI'], 'OM 28.06.2024 Clause A (even unlisted investigations / procedures).', 7, 'case'),
 ('The revised cochlear implant ceiling under OM 09.11.2026 for pre-lingual deafness is:',
  'Rs.7,00,000 incl. GST', ['Rs.5,35,000', 'Rs.6,00,000', 'Rs.3,00,000'], 'Post-lingual: Rs.6,00,000. The older Rs.5,35,000 figure is obsolete.', 10, 'fact'),
 ('After a first unilateral cochlear implant, permission for the other side is considered after:',
  '1 year, with justification and assessment', ['6 months', '3 years', 'Never'], 'OM 09.11.2026; wearable-component upgradation after 3 years at 50% of package cost.', 10, 'fact'),
 ('Under the decentralised STC procedure (OM 01.09.2026), who accords approval within delegated powers?',
  'The Additional Director, CGHS, after a three-member Local Technical Committee', ['The Standing Technical Committee at the Directorate', 'The Wellness Centre MO', 'MoHFW'], 'Earlier OMs requiring STC examination stand superseded and subsumed.', 7, 'fact'),
 ('Under OM 01.09.2026 a complete case is ordinarily decided within:',
  '15 working days (deficiencies communicated within 3 working days)', ['3 working days', '30 days', '7 days'], 'Annexure I, para 3.', 7, 'fact'),
 ('Injection Tirzepatide / Semaglutide under CGHS may be prescribed by:',
  'An Endocrinologist or Internal Medicine specialist of a Government hospital, endorsed by the HoD', ['Any CGHS Medical Officer', 'Any private specialist', 'Only the Wellness Centre pharmacist'], 'Approval valid 6 months (OM 24.07.2026); BMI ≥ 35, or ≥ 32.5 with listed comorbidity.', 6, 'fact'),
 ('Under OM 01.09.2026, CGHS / CS(MA) cover for a dependent son with a critical or terminal illness can be extended:',
  'For life, subject to dependency conditions and Board assessment', ['Up to age 30', 'Up to age 25 only', 'Only if unmarried'], 'Marriage does not end cover for such sons/brothers; “family” is not widened to his spouse/children.', 2, 'fact'),
 ('For CS(MA) beneficiaries, eligibility of such a dependent son / brother is assessed by:',
  'The Directorate General of Health Services (DGHS)', ['The CGHS Additional Director', 'The Controlling Officer', 'The AMA'], 'For CGHS: decentralised Boards at AD / regional HQ level (LTC procedure per OM 26.10.2026).', 2, 'fact'),
 ('A CGHS card issued under the critical-illness relaxation (OM 26.10.2026) is first issued for:',
  'One year; extension needs fresh medical records', ['Five years', 'Life', 'Six months'], 'There is no standing Medical Board in CGHS: a Government Specialist’s advice goes to the LTC at the AD’s office.', 2, 'fact'),
 ('Under OM 28.10.2026 family pensioners’ CGHS cards may now include:',
  'Eligible divorced and widowed daughters (added or reinstated)', ['Married sons', 'Parents-in-law', 'Any sibling'], 'Subject to verification of marital status, dependency and income.', 2, 'fact'),
 ('Under OM 13.05.2026 a male employee who opted for parents:',
  'Cannot later switch to parents-in-law, even on the parents’ demise', ['May switch once on retirement', 'May switch on the parents’ demise', 'May switch every five years'], 'One-time, irrevocable; applies to CGHS and CS(MA).', 3, 'fact'),
 ('DA from 01.07.2026 is 63%. The dependency limit Rs.9,000 + DA therefore works out to about:',
  'Rs.14,670 per month', ['Rs.9,000 per month', 'Rs.13,000 per month', 'Rs.16,000 per month'], 'DoE OM 29.10.2026; recompute at each DA revision.', 2, 'fact'),
 ('A serving employee posted at a district headquarters where a CGHS Wellness Centre exists (OM 17.09.2026) is:',
  'Mandatorily covered under CGHS and cannot opt out', ['Free to choose CS(MA)', 'Covered only if he pays extra', 'Covered only after 3 years'], 'The 5 km radius criterion has been dispensed with altogether.', 0, 'case'),
 ('A serving employee outside any CGHS-covered area, currently under CS(MA) only because of his posting, may:',
  'Opt once for CGHS — final, binding and applicable to all dependants', ['Opt every year', 'Opt for himself but keep family on CS(MA)', 'Not opt at all'], 'OM 17.09.2026: no simultaneous claims under both systems; no TA/DA; undertaking required.', 16, 'case'),
 ('A pensioner CGHS card colour is:',
  'Green (Blue = serving; Red = sitting MP; Yellow = PIB journalists)', ['Blue', 'Red', 'Yellow'], 'Para 5.', 4, 'fact'),
 ('The Fixed Medical Allowance is Rs.3,000 per month w.e.f.:',
  '01.01.2022', ['01.01.2016', '01.01.2020', '01.07.2024'], 'MoP OM 16.02.2022. FMA and CGHS OPD are mutually exclusive.', 5, 'fact'),
 ('Ward entitlement in a private empanelled hospital depends on:',
  'Basic pay drawn (up to Rs.36,500 general; Rs.36,501–50,500 semi-private; above that private)', ['Pension amount', 'Years of service', 'Card colour'], 'Para 6.', 5, 'fact'),
 ('Under the October 2025 framework, non-NABH hospital rates are:',
  '15% lower than NABH rates', ['10% lower', '20% lower', 'The same'], 'Tier II cities 10% lower, Tier III 20% lower than Tier I; general ward 5% lower, private ward 5% higher than semi-private.', 8, 'fact'),
 ('Multiple procedures in the same session are reimbursed at:',
  '100% for the first, 50% for the second, 25% for each later one', ['100% for all', '100%, 75%, 50%', '50% for all'], 'Bilateral identical procedures: 100% for one side and 50% for the second.', 8, 'fact'),
 ('Treatment abroad under Rule 11 requires:',
  'Prior approval of the Standing Committee (Central Government may relax it in genuine emergencies)', ['Only the AMA’s certificate', 'Approval of the Head of Department', 'No approval'], 'Application goes through the employee’s Ministry/Department; Rule 11(7) exception.', 27, 'fact'),
 ('Treatment at residence under Rule 7 is permitted when:',
  'Either no suitable hospital is available nearby or the illness is too severe to move the patient', ['Both conditions are met', 'The AMA runs a private clinic', 'The patient prefers home care'], 'Treatment at the AMA’s own clinic is not covered.', 23, 'fact'),
 ('Referral to a private specialist under Rule 5(1)(c) requires:',
  'An AMA certificate that no Government specialist is available', ['Nothing', 'Permission of MoHFW', 'IFD concurrence'], 'Rule 5(1)(a)/(b) come first: Government hospital specialists.', 21, 'fact'),
 ('Which of these is excluded from the CS(MA) Rules (Rule 1 Notes)?',
  'Retired Government officials', ['Probationers', 'Re-employed pensioners', 'Employees under suspension'], 'Pensioners are covered by CGHS (if enrolled) or FMA.', 17, 'fact'),
 ('AMA fees under OM 20.09.2023: Specialist / MBBS?',
  'Rs.350 / Rs.200, no separate night charge', ['Rs.200 / Rs.350', 'Rs.350 / Rs.350 plus night charge', 'Rs.500 / Rs.300'], 'Injection IM/SC Rs.25, IV Rs.50.', 28, 'fact'),
 ('Emergency treatment at a non-empanelled private hospital is reimbursed at:',
  'Non-NABH CGHS rates of the city, or actual, whichever is less', ['NABH rates, always', 'Actual expenditure, always', 'Nothing'], 'CS(MA) Rule 6 GD(2); CGHS OM 28.06.2024.', 22, 'fact'),
 ('A test costing Rs.2,500 is prescribed by a specialist at an empanelled hospital. Where must it be done without a fresh endorsement? (UPSC OM 11.08.2026 relaying CGHS HQ)',
  'At the same hospital where the primary consultation took place', ['Any diagnostic centre', 'Only at a Government laboratory', 'Only after IFD approval'], 'Endorsement is needed for CT / MRI / PET and any investigation above Rs.3,000.', 7, 'case'),
 ('Digital BTE hearing aids are reimbursable up to:',
  'Rs.8,000 per ear (Digital ITC/CIC Rs.9,000) — OM 01.12.2020', ['Rs.3,000', 'Rs.20,000', 'Rs.35,000'], 'Body-worn and analogue types are not reimbursable.', 24, 'fact'),
 ('The CGHS dependency income limit for family members (other than spouse) is:',
  'Below Rs.9,000 plus DA per month', ['Below Rs.5,000', 'Below Rs.25,000', 'No limit'], 'Spouse: no dependency condition. OM 08.11.2016 extends the limit to CS(MA).', 2, 'fact'),
 ('A pensioner’s CGHS card application for a retiring employee can also be started through:',
  'The Bhavishya portal (PAN as identifier) — OM 17.07.2026', ['Only a paper form', 'A Wellness Centre visit only', 'The Bank branch'], 'An additional mode; the existing CGHS portal route continues.', 4, 'fact'),
 ('DANICS and similarly placed AGMUT pensioners may opt for medical facilities from:',
  'Either the State Government they retired from or CGHS (OM 09.01.2026)', ['CGHS only', 'The State only', 'CS(MA)'], 'At par with AIS pensioners.', 4, 'fact'),
]


def build(extras, rcmap, rcpart, rctitle, esc):
    rnd = random.Random(7)
    bank = []
    # ---- hand-written
    for q, ok, wrong, why, rc, kind in HAND:
        cid = rcmap.get(rc)
        bank.append(dict(k=kind, q=q, o=[ok] + wrong, why=why, c=cid, s=rctitle.get(rc, '')[:60], p=rcpart.get(rc, 'cghs')))
    # ---- true/false from traps
    pat = re.compile(r'^[“"\']?(.+?)[”"\']?\s*[—–-]+\s*(?:ABSOLUTELY\s+)?WRONG!?\s*(.*)$', re.S)
    n = 0
    for k, li in extras['traps']:
        t = re.sub(r'\s+', ' ', li.get_text(' ', strip=True))
        m = pat.match(t)
        if not m or not m.group(2).strip():
            continue
        claim, fix = m.group(1).strip(' "“”'), m.group(2).strip()
        if len(claim) > 150 or len(fix) > 200:
            continue
        if n % 2 == 0:
            bank.append(dict(k='tf', q='True or false: “' + claim + '”', a=1, why='False — ' + fix, c=k.id, s=k.title[:60], p=getattr(k, 'part', 'cghs')))
        else:
            bank.append(dict(k='tf', q='True or false: it is a mistake to say “' + claim + '” — the correct position is: ' + fix, a=0, why='True — ' + fix, c=k.id, s=k.title[:60], p=getattr(k, 'part', 'cghs')))
        n += 1
    # ---- MCQs from tables (distractors must have the same "shape" as the answer)
    def clean(x):
        return re.sub(r'^[^\w\(\u201c"<>]+', '', x).strip()

    def sig(x):
        u = set()
        for key, rx in (('rs', r'Rs\.|₹'), ('pct', r'%'), ('day', r'\bdays?\b'), ('mon', r'\bmonths?\b'), ('yr', r'\byears?\b'), ('km', r'\bkm\b|miles?'),
                        ('lakh', r'lakh'), ('hrs', r'hrs?\b|AM|PM'), ('digit', r'\d')):
            if re.search(rx, x, re.I):
                u.add(key)
        if 'digit' in u and len(u) > 1:
            u.discard('digit')
        return frozenset(u) if u else frozenset(['text'])

    def stem(cap, title):
        t = cap or title
        t = re.split(r'\s[—–:]\s|: ', t)[0]
        return re.sub(r'^[^\w]+', '', t)[:60]

    cnt = 0
    for k, cap, tb in extras['tables']:
        if re.search(r'Master Reference|Trap', k.title):
            continue
        rows = tb.find_all('tr')
        if len(rows) < 4:
            continue
        hdr = [re.sub(r'\s+', ' ', c.get_text(' ', strip=True)) for c in rows[0].find_all(['th', 'td'])]
        if not (2 <= len(hdr) <= 4):
            continue
        body = []
        for r in rows[1:]:
            cells = [clean(re.sub(r'\s+', ' ', c.get_text(' ', strip=True))) for c in r.find_all(['th', 'td'])]
            if len(cells) == len(hdr) and all(cells) and len(cells[0]) < 70 and all(len(x) < 90 for x in cells[1:]) and not cells[0].isdigit() and not any('[OM' in x for x in cells):
                body.append(cells)
        if len(body) < 4:
            continue
        ci = 1
        for r in body:
            same = [x[ci] for x in body if x[ci] != r[ci] and sig(x[ci]) == sig(r[ci])]
            same = list(dict.fromkeys(same))
            if len(same) < 3:
                continue
            rnd.shuffle(same)
            bank.append(dict(k='fact', q=f'{stem(cap, k.title)} — “{r[0]}”: what is the {hdr[ci].lower()}?', o=[r[ci]] + same[:3],
                             why=f'{r[0]} → {r[ci]}', c=k.id, s=k.title[:60], p=getattr(k, 'part', 'cghs')))
            cnt += 1
            if cnt >= 120:
                break
        if cnt >= 120:
            break
    return bank
