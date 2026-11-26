"""Superintendent (NIT / IIT) exam map and claim-processing guide.

Sources: syllabus wording read from the NIT Warangal 2025 examination syllabus, MANIT and SVNIT Superintendent syllabi and the
IIT Bhubaneswar 2013 Junior Superintendent paper (opened and read); NITRR 2026 is quoted from a search summary only (document not opened).
Processing checks come from two departmental examples (CBDT 28.10.2020, CDA Patna 08.10.2021) and the NIT Sikkim guideline —
they illustrate practice and are NOT Ministry rules. The guide's rule content is unchanged.
"""
from html import escape
from visuals import cmp, fig
from svg import vflow


def build(ref):
    R = lambda n, t: f'<a href="{ref(n)}">{t}</a>'
    syl = cmp(['Recruiting institute', 'What the syllabus says about these rules', 'Weight / note'], [
        ['NIT Warangal (Examination Syllabus, 2025)', '“… Purchase procedures, Tendering process, Contract Management, <b>CGHS/CS(MA) Rules</b>, General Accounting Procedures, PFMS …” in the 60-question domain-knowledge portion', 'Superintendent Stage-I: 100 objective questions, 200 marks (2 each), 0.5 marks deducted per wrong answer, 2 hours; 40 general + 60 domain; 6 × vacancies shortlisted. CGHS/CS(MA) is one of 30+ domain items (so expect only a few questions — my inference)'],
        ['MANIT Bhopal and SVNIT Surat (Superintendent syllabus)', '“… CCS (LTC) rules, <b>Medical Attendance rules</b>, RTI Act-2005, CCS Pension Rules 1972 …”', 'One item in a long list; no sub-topics named'],
        ['IIT Bhubaneswar (Junior Superintendent paper, 2013 — old)', '“GFR-2005, GPF, CPF, EPF, NPS, CCS (Pension) Rules 1972, <b>CGHS, CS (MA) Rules</b> [15 questions]”', 'Weight 15 shared with the pension / GPF topics; may have changed since'],
        ['NIT Raipur advertisement, 2026 (search summary only — document not opened)', 'Search summary lists CGHS/CS(MA) Rules in the indicative domain syllabus', 'Check the advertisement for your exam'],
    ], 'Syllabus wording found (sources: institute notifications)')
    note = ('<div class="notice-box"><h3>🎓 What this means for preparation</h3><p>No syllabus I could open names sub-topics: it says only “CGHS/CS(MA) Rules” or “Medical Attendance rules”. '
            'So expect questions at the level of <b>entitlement, definitions (AMA, family), who may authorise, time limits, advance, reimbursement rates and recent orders</b>, and — for a Superintendent — '
            '<b>how a claim is processed and checked</b>. The whole guide is written to that level; use the mock tests (case scenarios) and the Memory sheet. '
            'Always confirm the topic list in <i>your</i> advertisement.</p></div>')
    flow = fig('How an NIT (Sikkim) processes a medical claim — one institute’s practice', vflow([
        ('Employee submits the claim form with original bills and prescriptions to the Institute Medical Unit (timely intimation for indoor treatment; emergency within 3 days)', 's'),
        ('Medical Unit verifies medicine bills against prescriptions and tests against CGHS rates — any variance is noted and disallowed', 'n'),
        ('Verified and signed by the Institute visiting doctor; claimant takes it to the Accounts Office', 'n'),
        ('Accounts Section scrutinises (reimbursement restricted to CGHS rates) and puts up for payment', 'g'),
    ], 'NIT Sikkim claim processing flow', bh=62, gap=26, bw=760, size=13),
        'Source: NIT Sikkim “Guidelines for Medical Attendance, Treatment & Reimbursement Procedure”. This is an Institute document (Board of Governors decisions), not a Ministry order — your Institute’s own rules govern.')
    nit = cmp(['Point in the NIT Sikkim guideline', 'Detail'], [
        ['Beneficiaries', 'Regular employees and dependent family members “as per the CS(MA) Rules 1944”; entitlement and norms follow CS(MA) / CGHS rules'],
        ['Where treatment may be taken (BoG, 27th meeting, 09.04.2022)', 'Institute Medical Unit; Government hospitals; hospitals empanelled by the State; CGHS / CS(MA) empanelled hospitals'],
        ['Rate of reimbursement', 'Restricted to CGHS rates; package rates for indoor treatment; bed category must be permissible'],
        ['Medicines', 'Purchase within three days of the prescription at recognised hospitals; separate prescription ordinarily needed for each purchase'],
        ['Emergency', 'Private practitioner allowed only for a life-threatening emergency, very short spell; application, circumstances and treating doctor’s certificate; claim considered on competent authority’s recommendation; intimation within 3 days'],
        ['Not reimbursable', 'Unrecognised hospital / practitioner except in emergency; spectacles; items declared inadmissible by Government'],
        ['Time limit', '6 months from completion of treatment / discharge; separate claim for each spell of illness'],
        ['Disputes / false claims', 'Interpretation doubts → Board of Governors; false, tampered claims → rejection and action under CCS (Conduct) Rules, 1964'],
    ], 'What an NIT guideline typically adds on top of the Ministry rules (institute-level)')
    check = cmp(['Check before putting up a claim', 'Why / rule it tests', 'Guide section'], [
        ['Claimant covered: CGHS card (CGHS beneficiary) or AMA appointment order (CS(MA))', 'Entitlement; Rule 2(a) AMA; OM 17.09.2026 option', R(18, 'Rule 2') + ', ' + R(16, 'CS(MA) preamble')],
        ['Patient is a “family” member: relationship, age limits, income below Rs.9,000 + DA, normally residing', 'Rule 2(c); CGHS family definition; 2026 relaxations', R(30, 'CS(MA) family') + ', ' + R(2, 'CGHS family')],
        ['Claim form complete; submitted within 6 months of discharge / treatment (1 month if an IPD advance was drawn); delays need condonation', 'Time limits; OM 01.06.2020', R(29, 'Advance & MRC') + ', ' + R(9, 'MRC (CGHS)')],
        ['Hospital: Government, CGHS-empanelled / CS(MA)-recognised, or non-empanelled (then only emergency, at non-NABH rates or actual, whichever is less)', 'Rule 6; empanelment', R(22, 'Rule 6')],
        ['Referral / AMA prescription and its validity; 4 consultations in 10 days (40 for Indian systems); specialist referral correct', 'Rule 5; CGHS referral rules', R(21, 'Rule 5') + ', ' + R(7, 'Referral')],
        ['Permission or ex-post-facto approval on file where required (private hospital, unlisted items, credit)', 'HoD / AD powers', R(22, 'Rule 6 GD(3)') + ', <a href="#powers">Who has the power?</a>'],
        ['Original certified bills, item-wise break-up, prescriptions / day-to-day reports, discharge summary, emergency certificate (original) where applicable', 'Genuineness; Controlling Officer may reject', R(25, 'Rule 9')],
        ['Item-wise table: amount charged vs amount admissible at CGHS rate / CS(MA) Rules, authenticated by the HoD', 'Reimbursement only to prescribed rates', R(10, 'Devices & rates') + ', ' + R(8, 'Rates')],
        ['Advance already sanctioned? Net amount = admissible − advance', 'Advance 90% / TB 80% or Rs.36,000; recovery from final claim', R(29, 'Advance')],
        ['Amount within the competent authority’s limit; relaxation of rules → refer upward', 'Delegation', '<a href="#powers">Who has the power?</a>'],
    ], 'Claim-processing checklist for a Superintendent (compiled from the guide’s rules; departmental checklists of CBDT 28.10.2020 and CDA Patna 08.10.2021 follow the same pattern)')
    caution = ('<div class="notice-box"><h3>⚠️ NITs and IITs are autonomous institutes</h3><p>The Ministry delegation orders in this guide (for example the Rs.10 lakh limit of OM 16.02.2026) speak of Heads of Departments of Ministries / Departments. '
               'For an NIT or IIT the approving authority and limits are those set by the Institute’s Statutes and Board of Governors — as the NIT Sikkim example shows, the Board decides where treatment may be taken and who interprets the rules. '
               'For exam answers about Ministry rules, use the guide; for “what does your Institute do”, use your Institute’s own notification. I could not find a Ministry of Education order on this, so treat the point as unverified.</p></div>')
    return (note + '<h3>1 · What the syllabi say</h3>' + syl + '<h3>2 · The processor’s checklist</h3>' + check + '<h3>3 · One NIT’s procedure</h3>' + flow + nit + caution)
