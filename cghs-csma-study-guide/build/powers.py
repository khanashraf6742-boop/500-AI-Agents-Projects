"""'Who has the power?' view — appointing authority for AMA, authority matrix, delegation of powers, practice Q&A.

Every statement is taken from the source guide (section refs given with each row).
Nothing here is added from outside the guide; newer orders reported after the guide's cut-off are
listed separately in the Verify tab as UNVERIFIED.
"""
from svg import *
from visuals import cmp, fig


def build(ref):
    """ref(n) -> '#cNN' link target of rule-card number n (document order in the source)."""
    R = lambda n, label: f'<a href="{ref(n)}">{label}</a>'
    r2, r3, r5, r6, r8, r9, r11 = R(18, 'Rule 2'), R(19, 'Rule 3'), R(21, 'Rule 5'), R(22, 'Rule 6'), R(24, 'Rule 8'), R(25, 'Rule 9'), R(27, 'Rule 11')
    ama, adv, mrc, para8 = R(28, 'AMA guidelines'), R(29, 'Advance & MRC (CS(MA))'), R(9, 'MRC (CGHS)'), R(7, 'Referral (CGHS)')

    banner = ('<div class="notice-box"><h3>📅 Currency check</h3><p>This tab follows the guide’s own text, which states it is current to <b>21 July 2026</b>. '
              'Orders reported after that date, or not reproduced in the guide, are listed in the <a href="#verify">Verify tab</a> as <b>unverified</b> — '
              'check them on the MoHFW CS(MA) page and the CGHS site before quoting any figure in an exam answer. '
              'In particular, the HoD monetary limits below are as given in the guide (OM 16.02.2026).</p></div>')

    # ---- who appoints the AMA
    who = fig('Who appoints the AMA? — Rule 2(a)', spine([
        dict(t='Is he a Medical Officer appointed by an authority named in Rule 2(a)(A)?', k='d',
             side=('YES → he is the AMA: appointed by (i) Dept of Health, GoI · (ii) any other Dept of GoI · (iii) an authority declared Head of a Department by the President under SR 2(10) · (iv) Chairman, CG Employees Welfare Co-ordination Committee at the station', 'g', 'Yes'), down_label='No'),
        dict(t='Govt doctors (in the system of medicine needed) available within 5 km?', k='d',
             side=('YES → Rule 2(a)(B): Principal Medical Officer of the District, or Asst Surgeon Grade I / Grade II, according to the employee’s pay status', 'b', 'Yes'), down_label='No'),
        dict(t='Head of Department appoints a PRIVATE registered medical practitioner as AMA — after duly filled proforma + verification of antecedents through local police [GD(1), GD(2)]', k='a'),
    ], 'Who appoints the AMA', sw=360, side_w=470, bh=70, gap=36, size=13),
        'Annual re-verification of every appointed AMA is mandatory. Honorary medical officers outside hospital precincts are treated as private practitioners and are NOT AMAs (Note 5; Andhra States exception). The AMA is fixed by the PLACE where the patient falls ill (Note 4).')

    # ---- delegation ladder
    ladder = fig('Delegation of powers — who settles what (as given in the guide)', spine([
        dict(t='Emergency treatment, within prescribed rates', k='n',
             side=('Head of Ministry/Dept/Office (serving) · Head of CGHS-covered city (pensioners) — NO financial limit', 'g', 'Level 1')),
        dict(t='Ordinary claim per rate list, no relaxation of rules, up to Rs.10 lakh (permission cases and post-facto approvals included)', k='n',
             side=('HoD / Head of Ministry/Dept/Office; Head of CGHS city for pensioners — WITHOUT IFD consultation [OM 16.02.2026]', 'g', 'Level 2')),
        dict(t='Per rate list but ABOVE Rs.10 lakh', k='n',
             side=('Ministry/Department WITH Internal Finance Division (IFD) consultation', 'a', 'Level 3')),
        dict(t='Relaxation of rules · air travel for treatment / ex-post facto', k='n',
             side=('MoHFW', 'r', 'Level 4')),
    ], 'Delegation of financial powers ladder', sw=420, side_w=420, bh=70, gap=30, size=13),
        'Ceiling history: Rs.2 lakh (original) → Rs.5 lakh (OM 23.11.2016) → Rs.10 lakh (OM 16.02.2026, File No. S.11030/4/2026-EHS).')

    # ---- authority matrix
    rows = [
        ['Appoint a Government Medical Officer as AMA', 'Dept of Health, GoI / other Dept of GoI / authority declared Head of Department under SR 2(10) / Chairman of CGEWCC', 'Rule 2(a)(A)(i)–(iv)', r2],
        ['Appoint a <b>private</b> registered practitioner as AMA', '<b>Head of Department</b> — issues appointment order', 'Only when adequate Govt doctors are not available within 5 km radius (8 km by some references); duly filled proforma + police verification of antecedents', r2 + ' GD(1)–(2), ' + ama],
        ['Annual re-verification of an AMA', 'HoD or designated officer', 'Mandatory every year; qualification / registration valid, still willing, 5-km basis holds', r2 + ' GD(3), ' + ama],
        ['Revise AMA consultation / injection fees', 'MoHFW (OM 20.09.2023 with IFD concurrence)', 'Specialist Rs.350, MBBS Rs.200, injection IM/SC Rs.25 / IV Rs.50; no day-night difference', ama],
        ['Recognise / empanel private hospitals under CS(MA)', '<b>MoHFW</b>', 'Only private hospitals in NON-CGHS cities; separate guidelines for dental and eye hospitals', ama + ', ' + r6],
        ['Refer patient to a specialist (CS(MA))', 'The AMA (or first specialist for a second opinion)', '4 consultations within 10 days; AYUSH / Homoeopathy up to 40 days', r5],
        ['Decide the hospital when AMA opinion cannot be obtained (ill away from headquarters)', 'Head of the nearest Government hospital', 'Rule 6(1)(c)', r6],
        ['Permit indoor treatment at a recognised private hospital (employee already at a Govt hospital)', '<b>Head of Department</b>', 'On the basis of AMA’s medical prescription', r6 + ' GD(3)'],
        ['Decide “emergency” cases / post-facto approval', 'HoD (delegated); Head of Ministry/Dept/Office (serving), Head of CGHS city (pensioners)', 'No financial limit, within prescribed rates', r6 + ' GD(4), ' + adv],
        ['Settle ordinary reimbursement claims', 'HoD / Head of Ministry/Dept/Office; Head of CGHS city for pensioners', 'Up to Rs.10 lakh, no relaxation of rules, without IFD (OM 16.02.2026)', adv + ', ' + mrc],
        ['Claims above Rs.10 lakh', 'Ministry/Dept', 'With IFD consultation', adv],
        ['Relax rules · interpretation · air travel ex-post facto', 'MoHFW', 'Doubtful / relaxation cases are referred to MoHFW', r9 + ', ' + adv],
        ['Reject a claim that fails genuineness / other requirements', '<b>Controlling Officer</b>', 'Fully empowered — without consulting MoHFW', r3 + ' GD(3), ' + r9],
        ['Counter-sign AMA certificates and claims', 'Controlling Officer', 'Claim within 6 months of discharge / treatment (CS(MA))', r9],
        ['Hear an appeal against rejection', 'Central Government', 'Within 45 days of receipt of the rejection order', r3 + ' GD(4), ' + r6],
        ['Reimburse Ayah / nursing charges at home', 'Head of Office (delegated)', 'At prescribed ceiling or actual, whichever less; AMA / specialist prescription; claim within 6 months', r8],
        ['Reimburse artificial appliances', 'Head of Department', 'Per CS(MA) Rules and CGHS rules at the time of procurement', r8],
        ['Permit confinement at a private recognised hospital', 'Head of Department', 'Rule 8 — maternity', r8],
        ['Permit specific cancer-treatment procedures', 'HoD / Head of CGHS city', 'Treatment at any cancer hospital on the specified list; CGHS rates or actual, whichever less', r8],
        ['Recommend treatment outside India', '<b>Standing Committee</b> (application routed through own Ministry/Dept)', 'Prior approval mandatory; Table of conditions under Rule 11(3)', r11],
        ['Authorise treatment abroad without prior approval; amend the Rule 11(3) Table', '<b>Central Government</b>', '11(7): only where prior approval was not feasible (e.g. emergency abroad); 11(4): additions / deletions by Gazette notification', r11],
        ['Sponsor a CGHS card application', 'Head of Department / Head of Office', 'Card issued by the Additional Director (AD), CGHS of the city', R(4, 'Para 5')],
        ['Issue a CGHS specialist referral', 'Medical Officer of a CGHS Wellness Centre', 'Valid 3 months; ≤ 3 specialists; ≤ 6 consultations; no referral needed at Govt hospitals', para8],
        ['Settle a pensioner’s CGHS claim', 'AD (Additional Director), CGHS city of registration', 'Claim within 3 months of treatment', mrc],
    ]
    matrix = ('<div class="row"><input class="filterbox" data-filter="#powtab tbody tr" placeholder="Filter: e.g. HoD, MoHFW, appeal, Rs.10 lakh…" aria-label="Filter authority matrix"></div>'
              '<div class="tblwrap"><table id="powtab" class="cmp"><caption>Authority matrix — who decides what</caption><thead><tr><th scope="col">Decision / power</th><th scope="col">Authority</th><th scope="col">Condition / limit</th><th scope="col">Section</th></tr></thead><tbody>'
              + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows) + '</tbody></table></div>')

    # ---- delegation compare: CGHS vs CS(MA) claims
    deadlines = fig('Claims & appeals — time limits that decide “who can still approve”', cmp(['Item', 'CGHS', 'CS(MA)'], [
        ['Claim deadline', '3 months', '6 months (1 month from discharge if IPD advance drawn)'],
        ['Serving employee’s claim goes to', 'Own Department / Ministry', 'Controlling Officer (counter-signature, Rule 9)'],
        ['Pensioner’s claim goes to', 'AD, CGHS city of registration', 'Pensioners are excluded from CS(MA)'],
        ['Appeal against rejection', '—', '45 days to Central Government'],
        ['Advance sanction', 'Within 10 days of request', 'Within 10 days of request']]))

    # ---- practice questions
    qa = [
        ('Who has the power to authorise (appoint) private doctors as AMA?',
         'The <b>Head of Department</b> (HoD) — by issuing an appointment order — but only when adequate Government doctors are not available within a 5 km radius (8 km by some references) and after he has verified the duly filled prescribed proforma and the doctor’s character and antecedents through the local police [Rule 2(a) GD(1)–(2)]. The appointment is subject to <b>annual re-verification</b>. Note: Rule 2(a)(A) itself lists the authorities that appoint Medical Officers (Dept of Health, other Depts of GoI, authorities declared Head of Department under SR 2(10), Chairman of the CGEWCC). The guide gives no OM number for the HoD’s power — see Verify tab.', 18),
        ('Who appoints the AMA under Rule 2(a)(A)?',
         '(i) Department of Health, GoI (for persons in that Department) · (ii) any other Department of GoI (for its own persons) · (iii) any authority declared by the President under sub-rule (10) of Rule 2 of the Supplementary Rules to be the Head of a Department · (iv) the Chairman of the Central Government Employees Welfare Co-ordination Committee at stations where such Committees function.', 18),
        ('Can an honorary medical officer be an AMA?',
         'No. Honorary Medical Officers outside hospital precincts are like private practitioners and are not AMAs (Note 5). Exception: in Andhra States they have been declared AMAs.', 18),
        ('Who can empanel / recognise a private hospital under CS(MA)?',
         '<b>MoHFW</b>. Only private hospitals in non-CGHS-covered cities are considered; in CGHS cities the CGHS-empanelled hospitals serve the purpose. Separate guidelines exist for dental and eye hospitals.', 28),
        ('Who can permit an employee at a Government hospital to take indoor treatment in a private hospital?',
         'The Head of Department, on the basis of the AMA’s medical prescription, for a hospital recognised under CGHS / CS(MA) [Rule 6 GD(3)].', 22),
        ('Up to what amount can a HoD settle a medical-reimbursement claim?',
         'Up to <b>Rs.10 lakh</b> without IFD consultation, where no relaxation of rules is involved and entitlement is worked out strictly at prescribed CGHS / CS(MA) rates — OM File No. S.11030/4/2026-EHS dated 16.02.2026 (earlier Rs.5 lakh by OM 23.11.2016, originally Rs.2 lakh). It covers permission cases and post-facto approvals. Above Rs.10 lakh: Ministry/Department with IFD consultation.', 29),
        ('Who decides emergency cases, and is there a monetary limit?',
         'Head of Ministry/Dept/Office for serving employees and Head of the CGHS-covered city for pensioners — <b>no financial limit</b>, within prescribed rates. HoDs have been delegated the power to decide “emergency” cases [Rule 6 GD(4)].', 29),
        ('Who can reject a medical claim, and does he need MoHFW’s permission?',
         'The Controlling Officer in the Ministry/Department can reject any claim not meeting genuineness and other requirements, <b>without consulting MoHFW</b>. Cases needing clarification, interpretation or relaxation are referred to MoHFW [Rule 3 GD(3), Rule 9].', 19),
        ('Where is the appeal against rejection, and in what time?',
         'To the Central Government, within <b>45 days</b> of receipt of the rejection order [Rule 3 GD(4)]. Trap: it is not “appeal to MoHFW”.', 19),
        ('Who has the power to relax the rules?',
         'MoHFW — rule-relaxation cases are referred to it; HoDs can settle only cases where no relaxation is involved.', 29),
        ('Who recommends treatment abroad, and who can allow it without prior approval?',
         'The <b>Standing Committee</b> recommends (application through the employee’s Ministry/Department; prior approval mandatory). The <b>Central Government</b> may authorise reimbursement where prior approval was not feasible [Rule 11(7)] and may add or delete treatments in the Rule 11(3) Table by Gazette notification [Rule 11(4)].', 27),
        ('Who issues the CGHS card and who sponsors the application?',
         'The Additional Director (AD), CGHS of the city issues the card; the application is sponsored by the Head of Department / Head of Office of the employee.', 4),
        ('Who issues a CGHS specialist referral and for how long is it valid?',
         'Any Medical Officer of a CGHS Wellness Centre: valid 3 months, up to 3 specialists and 6 consultations. No referral is needed at Government hospitals (AIIMS, INIs, NE institutions, Tata Memorial, Central Govt hospitals, CGHS WCs).', 7),
        ('Who settles Ayah (nursing) charges, artificial appliances and confinement permissions?',
         'Ayah charges: Head of Office (delegated). Artificial appliances: Head of Department. Confinement at a private recognised hospital: HoD may permit [Rule 8].', 24),
    ]
    qa_html = ''.join(
        f'<details class="listitem"><summary><b>Q{i+1}. {q}</b></summary><div class="qa-answer"><p>{a}</p><p class="src">Section: <a href="{ref(n)}">open</a></p></div></details>'
        for i, (q, a, n) in enumerate(qa))

    return (banner + '<h3>1 · Who appoints the AMA — and who can authorise private doctors?</h3>' + who
            + '<h3>2 · Delegation of powers</h3>' + ladder + deadlines
            + '<h3>3 · Authority matrix</h3>' + matrix
            + '<h3>4 · Practice questions</h3><div class="toolbar"></div>' + qa_html)
