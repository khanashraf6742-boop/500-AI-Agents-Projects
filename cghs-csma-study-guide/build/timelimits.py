"""Time limits, validity periods and age limits — CGHS and CS(MA) in separate tables.
Every row is taken from the guide's text or from the verified 2026 orders; the section link shows where."""
from visuals import cmp

CGHS = [
 ('Final claim for reimbursement', '6 months from completion of treatment / discharge; only later bills need condonation (OM 01.06.2020; earlier 3 months)', 9),
 ('Claim processing', 'Average 21 days (60–120 days for non-empanelled hospital cases)', 9),
 ('Medical advance — sanction', 'Within 10 days of receipt of request; ordinarily one advance per illness; recovered from the final claim', 9),
 ('TB advance', '80% of estimate or Rs.36,000 (whichever is less) where treatment lasts more than 3 months', 9),
 ('Specialist referral', 'Valid 3 months; up to 3 specialists; up to 6 consultations', 7),
 ('Follow-up / routine tests', 'Same HCO within the 3-month validity; CT / MRI always need CGHS endorsement', 7),
 ('Seven chronic conditions (cardiac surgery, transplant, neurosurgery, ESRD, cancer, autoimmune, neurological)', 'Consultations and investigations without time limit on the primary referral', 7),
 ('Decentralised STC approval (OM 01.09.2026)', 'Deficiencies communicated within 3 working days; complete case ordinarily decided within 15 working days', 7),
 ('Chronic-disease medicines', 'Issued 3 months at a time against a valid specialist prescription', 6),
 ('Medicines for a beneficiary going abroad', 'Up to 6 months with the Additional Director’s permission', 6),
 ('Indented medicines', 'Must be collected within 15 days of the indent', 6),
 ('Card validity', 'Serving: till retirement; pensioner: lifetime if lifetime contribution (120 × monthly rate) paid; digital card = plastic card', 4),
 ('Pensioner card application', '6 months before retirement, with pension papers', 4),
 ('Annual health check-up', 'Annual, for pensioner primary cardholders aged 75+ at empanelled hospitals', 6),
 ('Home visit (80+)', 'Once a month by the Wellness Centre MO / CMO if the beneficiary cannot attend and lives within 5 km', 13),
 ('Cancer — post-operative follow-up', '6 months from discharge', 10),
 ('CPAP / device replacement', 'After 5 years with condemnation certificate', 10),
 ('Cochlear implant (OM 09.11.2026)', 'Unilateral first; other side after 1 year; wearable-component upgradation after 3 years at 50% of package cost', 10),
 ('Critical / terminal illness cover (OMs 01.09.2026, 26.10.2026)', 'Card issued first for 1 year; extension on fresh medical records', 2),
 ('GLP-1 drugs (OM 24.07.2026)', 'Approval valid 6 months; follow-up monthly for 3 months then every 3 months; 3 months’ lifestyle compliance before starting', 6),
 ('Eyesight testing', 'Employee only, once in 3 years', 12),
 ('Revised rates (OM 03.10.2025)', 'Effective 00:00 hrs on 13.10.2025; empanelled hospitals sign fresh MoAs within 90 days; TMS 2.0 for all new registrations from that time', 8),
 ('Parents / parents-in-law (OM 13.05.2026); CGHS option for outstation employees (OM 17.09.2026)', 'Both are one-time and irrevocable', 3),
]

CSMA = [
 ('Final claim for reimbursement', '6 months — OPD from treatment, IPD from discharge', 29),
 ('Final claim where an IPD advance was drawn', '1 month from discharge', 29),
 ('Appeal against rejection', '45 days from receipt of the rejection order, to the Central Government', 19),
 ('Medical advance — sanction', 'Within 10 days of receipt of request; ordinarily one advance per illness', 29),
 ('TB advance', '80% of estimate or Rs.36,000 (whichever is less) where treatment lasts more than 3 months', 29),
 ('Rule 5 — specialist consultations', 'First 4 consultations within 10 days (one continuous spell of one disease); Indian systems / Homoeopathy up to 40 days by the AMA', 21),
 ('Rule 3 — AMA + specialist together', 'Combined 10 days for one continuous spell of illness (allopathy); AYUSH AMA up to 40 days', 19),
 ('Prescription validity (Rule 3)', 'AMA / specialist prescription for specialist consultation or test: single use within 14 days; investigations prescribed by a specialist: 30 days; chronic illness: 6 months', 19),
 ('Rule 6 — mental illness (indoor)', 'Maximum 3 years', 22),
 ('Rule 5 GD(5) — male child in a women’s hospital', 'Till the age of 6 years', 21),
 ('AMA — private practitioner', 'Annual re-verification is mandatory; fresh police verification periodically (at least once in 5 years or as prescribed); appointment order states its validity', 28),
 ('Rule 8 — eyesight testing', 'Employee only, once in every 3 years on the AMA’s recommendation', 24),
 ('Rule 8 — annual medical examination', 'Annually, Group A officers aged 40+ (ceiling men Rs.2,000; women Rs.2,200)', 24),
 ('Rule 8 — cancer follow-up', '6 months from discharge', 24),
 ('Rule 8 — maternity / ayah / other claims', 'Claim within 6 months', 24),
 ('Rule 8 — devices (CPAP etc.)', 'Replacement after 5 years with condemnation certificate', 24),
 ('Critical / terminal illness cover (OM 01.09.2026)', 'Lifelong cover on DGHS assessment; marriage does not end it', 30),
 ('CGHS option for outstation serving employees (OM 17.09.2026)', 'One-time, final and binding for the whole family', 16),
 ('HoD delegation (OM 05.06.2014; OM 16.02.2026)', 'No time limit; monetary: Rs.2 lakh (2014) → Rs.10 lakh (16.02.2026) without IFD', 29),
]

AGES = [
 ('Son', 'Till earning or age 25, whichever is earlier; any age if permanently disabled; any age if critical / terminal illness (OM 01.09.2026)', 2),
 ('Daughter', 'Till earning or marriage, any age; divorced / separated / widowed daughters any age', 2),
 ('Brother', 'Minor brother till 18; disabled brother any age; critical / terminal illness cover (OM 01.09.2026)', 2),
 ('Transgender children / siblings', 'Any age, if financially dependent with a certificate under the 2019 Act (OM 16.09.2025)', 2),
 ('Referral-free OPD', '70 years and above (earlier 75; reduced by OM 28.06.2024)', 7),
 ('Annual health check-up', '75 years and above — pensioner primary cardholders', 6),
 ('IVF', 'Married woman Government servant aged 21–39 living with her husband (max 3 cycles)', 10),
 ('Male child in a women’s hospital (CS(MA))', 'Till 6 years', 21),
]


def build(ref):
    def tbl(title, rows, cols=('Matter', 'Time limit / period', 'Section')):
        body = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td><a href="{ref(r)}">open</a></td></tr>' for a, b, r in rows)
        return f'<div class="tblwrap"><table class="cmp"><caption>{title}</caption><thead><tr>' + ''.join(f'<th scope="col">{c}</th>' for c in cols) + f'</tr></thead><tbody>{body}</tbody></table></div>'
    same = cmp(['Point', 'CGHS', 'CS(MA) Rules, 1944'], [
        ['Final claim', '6 months from completion of treatment / discharge (OM 01.06.2020)', '6 months (OPD from treatment; IPD from discharge); 1 month from discharge if IPD advance drawn'],
        ['Advance sanction', 'Within 10 days', 'Within 10 days'],
        ['Appeal against rejection', '—', '45 days to the Central Government'],
        ['Consultation cap', 'Referral valid 3 months: ≤ 3 specialists, ≤ 6 consultations', '4 consultations within 10 days (Indian systems / Homoeopathy: 40 days)'],
        ['Prescription / medicines', 'Chronic medicines 3 months at a time; abroad up to 6 months', 'Prescription: 14 days (single use); investigations 30 days; chronic 6 months'],
        ['Eyesight testing', 'Employee only, once in 3 years', 'Employee only, once in 3 years'],
        ['Cancer follow-up', '6 months from discharge', '6 months from discharge'],
    ], 'The few points that look alike — and where they differ')
    return ('<p class="lead">Time limits, validity periods and age limits, <b>separately for CGHS and CS(MA)</b>. Taken from the guide and the verified 2026 orders; each row links to its section.</p>'
            + tbl('CGHS — time limits and periods', CGHS) + tbl('CS(MA) Rules, 1944 — time limits and periods', CSMA) + tbl('Age limits (both systems unless marked)', AGES, ('Who', 'Age limit', 'Section'))
            + '<h3>Side by side</h3>' + same)
