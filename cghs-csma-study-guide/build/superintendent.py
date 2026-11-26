"""Superintendent (NIT / IIT) exam map and claim-processing checklist.

Syllabus wording was read from the NIT Warangal 2025 examination syllabus, MANIT and SVNIT Superintendent syllabi and the IIT Bhubaneswar
2013 Junior Superintendent paper (NIT Raipur 2026 is quoted from a search summary only). The processing checklist is compiled ONLY from the
guide's official CGHS / CS(MA) rules and orders; no institute-level or departmental instructions are used.
"""
from visuals import cmp


def build(ref):
    R = lambda n, t: f'<a href="{ref(n)}">{t}</a>'
    syl = cmp(['Recruiting institute', 'What the syllabus says about these rules', 'Weight / note'], [
        ['NIT Warangal (Examination Syllabus, 2025)', '“… Purchase procedures, Tendering process, Contract Management, <b>CGHS/CS(MA) Rules</b>, General Accounting Procedures, PFMS …” in the 60-question domain-knowledge portion', 'Superintendent Stage-I: 100 objective questions, 200 marks (2 each), 0.5 marks deducted per wrong answer, 2 hours; 40 general + 60 domain; 6 × vacancies shortlisted. CGHS/CS(MA) is one of 30+ domain items (so expect only a few questions — my inference)'],
        ['MANIT Bhopal and SVNIT Surat (Superintendent syllabus)', '“… CCS (LTC) rules, <b>Medical Attendance rules</b>, RTI Act-2005, CCS Pension Rules 1972 …”', 'One item in a long list; no sub-topics named'],
        ['IIT Bhubaneswar (Junior Superintendent paper, 2013 — old)', '“GFR-2005, GPF, CPF, EPF, NPS, CCS (Pension) Rules 1972, <b>CGHS, CS (MA) Rules</b> [15 questions]”', 'Weight 15 shared with the pension / GPF topics; may have changed since'],
        ['NIT Raipur advertisement, 2026 (search summary only — document not opened)', 'Search summary lists CGHS/CS(MA) Rules in the indicative domain syllabus', 'Check the advertisement for your exam'],
    ], 'Syllabus wording found (sources: institute recruitment notifications)')
    note = ('<div class="notice-box"><h3>🎓 What this means for preparation</h3><p>No syllabus I could open names sub-topics: it says only “CGHS/CS(MA) Rules” or “Medical Attendance rules”. '
            'So expect questions at the level of <b>entitlement, definitions (AMA, family), who may authorise, time limits, advance, reimbursement rates and recent orders</b>, and — for a Superintendent — '
            '<b>checking a claim against the rules</b>. Everything in this guide is limited to official CGHS and CS(MA) rules and orders. Use the mock tests (case scenarios) and the Memory sheet, and confirm the topic list in <i>your</i> advertisement.</p></div>')
    check = cmp(['Check before putting up a claim', 'Rule it tests', 'Guide section'], [
        ['Claimant covered: CGHS card (CGHS beneficiary) or AMA (CS(MA)); employees in a CGHS-covered area are under CGHS (OM 17.09.2026)', 'Entitlement; Rule 2(a) AMA', R(18, 'Rule 2') + ', ' + R(16, 'CS(MA) preamble')],
        ['Patient is a “family” member: relationship, age limits, income below Rs.9,000 + DA, normally residing', 'Rule 2(c); CGHS family definition; 2026 relaxations', R(30, 'CS(MA) family') + ', ' + R(2, 'CGHS family')],
        ['Submitted within 6 months of discharge / treatment (1 month if an IPD advance was drawn); delay needs condonation', 'Time limits; OM 01.06.2020', R(29, 'Advance & MRC') + ', ' + R(9, 'MRC (CGHS)')],
        ['Hospital: Government, CGHS-empanelled / CS(MA)-recognised, or non-empanelled (then only emergency, at non-NABH rates or actual, whichever is less)', 'Rule 6; empanelment', R(22, 'Rule 6')],
        ['AMA certificate for the medical attendance; referral / prescription valid; 4 consultations in 10 days (40 for Indian systems)', 'Rules 3 and 5; CGHS referral rules', R(19, 'Rule 3') + ', ' + R(21, 'Rule 5') + ', ' + R(7, 'Referral')],
        ['Permission or ex-post-facto approval where required (private hospital, non-empanelled hospital, unlisted items)', 'HoD / AD powers', R(22, 'Rule 6 GD(3)') + ', <a href="#powers">Who has the power?</a>'],
        ['Emergency treatment supported by the emergency certificate of the treating hospital', 'CGHS referral OM 28.06.2024; Rule 6 GD(2)', R(7, 'Referral') + ', ' + R(22, 'Rule 6')],
        ['Reimbursement restricted to the prescribed CGHS / CS(MA) rate (or actual, whichever is less); inadmissible items excluded', 'Rates; non-admissible lists', R(10, 'Devices & rates') + ', ' + R(8, 'Rates') + ', ' + R(12, 'Non-admissible')],
        ['Advance already sanctioned? Net amount = admissible − advance (advance recovered from the final claim)', 'Advance 90% / TB 80% or Rs.36,000', R(29, 'Advance')],
        ['Amount within the competent authority’s limit; relaxation of rules → refer to MoHFW; Controlling Officer may reject non-genuine claims', 'Delegation; Rules 3 and 9', R(25, 'Rule 9') + ', <a href="#powers">Who has the power?</a>'],
    ], 'Claim-checking checklist — compiled only from the guide’s official CGHS / CS(MA) rules and orders')
    return note + '<h3>1 · What the syllabi say</h3>' + syl + '<h3>2 · Checking a claim against the rules</h3>' + check
