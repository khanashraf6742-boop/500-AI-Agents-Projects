"""Latest orders (Jan–Nov 2026) read from the primary OM texts, plus update call-outs inserted into the relevant sections.

Source of each text: copies of the official Office Memoranda hosted on staffnews.in (PDF/HTML), read 25.11.2026.
The MoHFW / CGHS websites themselves could not be opened from this environment (HTTP 502), so nothing here
was cross-checked on mohfw.gov.in. Every figure below is quoted from the order text.
"""
from html import escape
from visuals import cmp, fig

SN = 'https://www.staffnews.in'
URL = {
    'deleg': SN + '/2026/06/revision-of-delegation-of-financial-powers-for-medical-reimbursement.html',
    'stc': SN + '/2026/09/decentralisation-of-approval-procedure-under-cghs.html',
    'relax': SN + '/2026/09/relaxation-in-age-and-marital-status-criteria-for-dependent-cghs-csma.html',
    'ext': SN + '/2026/11/cghs-facilities-to-dependent-sons-brothers-suffering-from-critical-terminal-illnesses.html',
    'fpd': SN + '/2026/10/cghs-cards-of-family-pensioners-inclusion-of-divorced-and-widowed-daughters.html',
    'coch': SN + '/2026/11/revised-ceiling-rates-and-guidelines-for-cochlear-implantation.html',
    'glp1': SN + '/2026/07/guidelines-for-prescription-of-injectable-glp-1-cghs-csma-rules.html',
    'bhav': SN + '/2026/07/integration-of-cghs-online-system-with-bhavishya-portal.html',
    'danics': SN + '/2026/02/extension-of-cghs-facilities-to-pensioners-of-danics-and-agmut-cadre.html',
    'hod': SN + '/2026/02/medical-reimbursement-under-cghs-or-csma-rules.html',
    'parents': SN + '/2026/05/option-to-avail-medical-facilities-either-for-their-parents-or-parents-in-law.html',
    'da': SN + '/2026/10/revision-of-rates-of-dearness-allowance-from-01-07-2026.html',
}


def a(key, label='source copy'):
    return f'<a href="{URL[key]}" rel="noopener">{label}</a>'


def box(title, body):
    return f'<div class="upd-box"><div class="utag">🆕 UPDATE — {title}</div>{body}</div>'


DELEG_TABLE_A = cmp(['Authority', 'Earlier power', 'Revised power'], [
    ['Additional Director, CGHS City/Zone', 'Rs.7 lakh', '<b>Rs.15 lakh</b>'],
    ['Director, CGHS', 'Rs.15 lakh', '<b>Rs.25 lakh</b>'],
    ['Additional Secretary & DG, CGHS', 'Rs.25 lakh', '<b>Rs.50 lakh</b>'],
], 'A. Medical reimbursement claims / hospital bills at approved rates — above Rs.50 lakh: MoHFW with IFD concurrence')

DELEG_TABLE_B = cmp(['Authority', 'Earlier power', 'Revised power'], [
    ['Additional Director, CGHS City/Zone', 'Up to Rs.1 lakh', '<b>Up to Rs.2 lakh</b>'],
    ['Director, CGHS', 'Up to Rs.3 lakh', '<b>Up to Rs.5 lakh</b>'],
    ['Additional Secretary & DG, CGHS', 'Up to Rs.5 lakh', '<b>Up to Rs.10 lakh</b>'],
], 'B. Unlisted investigations / procedures / implants (where no CGHS package or ceiling rate exists) — above Rs.10 lakh: Ministry with IFD concurrence')

DELEG_BODY = (
    '<p><b>CGHS OM No. Z.15025/14/2/DIR/CGHS dated 25.06.2026</b> (Director, CGHS; IFD concurrence Dy. No. 1029 dated 18.06.2026) — “Revision of delegation of financial powers for settlement of medical reimbursement claims and grant of permissions/ex-post facto approvals in respect of pensioner CGHS beneficiaries and other eligible beneficiaries, including serving CGHS employees”. '
    'It revises the powers under the earlier OM No. Z.15025/79/2/DIR/CGHS dated 05.10.2016.</p>'
    + DELEG_TABLE_A + DELEG_TABLE_B +
    '<p><b>C. Permissions / ex-post facto approvals</b></p><ul>'
    '<li>(i) Elective treatment / investigations in <b>non-empanelled</b> hospitals, diagnostic labs or imaging centres for pensioners / ex-MPs / freedom fighters / serving CGHS employees etc.: considered by the <b>Additional Director of the CGHS city/zone</b>, reimbursement restricted to CGHS package rates or actual expenditure, whichever is less.</li>'
    '<li>(ii) Cases of <b>procedural lapse</b> (elective treatment in empanelled hospitals without Govt Specialist/CMO recommendation and without prior permission): considered by the Additional Director, same restriction (CGHS rates or actual, whichever is less).</li></ul>'
    '<p><b>Conditions (para 3)</b></p><ul>'
    '<li>The delegation does <b>not</b> cover cases involving relaxation of rules, irrespective of amount.</li>'
    '<li>Cases above the limits go to MoHFW with IFD concurrence.</li>'
    '<li>Reimbursement restricted to CGHS package / ceiling rate, or actual expenditure, whichever is less. Where no package or ceiling rate exists (para 2(B)), actual expenditure may be considered subject to admissibility, reasonableness and the limits.</li>'
    '<li>All approvals subject to admissibility under CGHS rules, supporting records and bills, reasonableness of charges, budgetary provisions and audit requirements.</li>'
    '<li>Powers are exercised case by case and create no general entitlement or precedent.</li>'
    '<li>The revised delegations <b>supersede earlier instructions to the extent of the financial delegations now conveyed</b>.</li></ul>'
    f'<p class="vnote">Read from the {a("deleg", "published text of the OM")}.</p>')

DISEASES = [
    'Major organ / bone-marrow transplant (requiring, or post-transplant)', 'All malignant tumours (solid and haematological)', 'Congenital heart disease', 'Eisenmenger syndrome',
    'Post CIED (PCD/CRT-D) with heart failure (EF < 35%)', 'Symptomatic, haemodynamically significant valvular heart disease', 'Severe left ventricular dysfunction, EF < 35%', 'Cardiomyopathy',
    'Primary pulmonary artery hypertension', 'Aortic aneurysm / dissections (treated or untreated)', 'Demyelinating disease', 'Degenerative / progressive nervous-system disorders',
    'Wilson’s disease (congenital metabolic and storage disorders)', 'Refractory epilepsy syndromes', 'Myasthenia gravis', 'Autoimmune disorders', 'Immunodeficiency syndromes',
    'Chronic liver disease', 'Chronic pancreatitis', 'Chronic bleeding disorders', 'Congenital haemolytic anaemias', 'Thrombotic microangiopathy – haemolytic uraemic syndrome',
    'Budd-Chiari syndrome', 'Adrenal cancer / functioning adrenal tumours', 'Diabetes mellitus type 1', 'Endogenous Cushing’s syndrome', 'Panhypopituitarism',
    'Chronic primary adrenal insufficiency', 'Chronic respiratory failure', 'Obstructive sleep apnoea requiring CPAP', 'Severe bronchial asthma', 'Chronic kidney disease',
    'Autosomal dominant polycystic kidney disease', 'Congenital / hereditary progressive kidney disorders', 'Bladder dysfunction (congenital / acquired) requiring continued intervention',
    'Major congenital genitourinary abnormality with residual functional defects', 'Anatomic disorders of sexual dysfunction', 'Moderate to severe psoriasis, PASI > 10',
    'Severe atopic dermatitis', 'Severe pemphigus vulgaris', 'Severe chronic urticaria', 'Vitiligo > 10 to < 50% BSA',
]
assert len(DISEASES) == 42

RELAX_BODY = (
    '<p><b>OM F. No. S.11030/54/2023-EHS(8248513)/I/3893459/2026 dated 01.09.2026</b> — relaxation in age and marital-status criteria for dependent sons and brothers suffering from critical / terminal illnesses under CGHS / CS(MA) Rules, 1944 (immediate effect).</p>'
    '<ul><li><b>Existing norms recited:</b> unmarried dependent son — up to 25 years; permanently disabled unmarried son — for life; dependent brother — ordinarily up to 18 years, disabled dependent brother — no age limit; daughters and sisters (incl. divorced / abandoned / separated / widowed) already eligible.</li>'
    '<li><b>New:</b> CGHS / medical-attendance facilities may be extended <b>for life</b> to dependent sons and brothers suffering from critical / terminal illnesses, subject to the dependency conditions and assessment by the competent Medical Board.</li>'
    '<li><b>Illnesses (indicative):</b> chronic, severe, critical or terminal illnesses causing substantial and continuing functional impairment or inability to earn a livelihood / attain self-sufficiency — e.g. advanced malignancies, severe neurological disorders, end-stage organ disease, severe congenital / genetic disorders.</li>'
    '<li><b>Eligibility</b> is decided case by case (disease nature, functional impairment, ability to earn, continuing dependency); specialists assess multi-system conditions.</li>'
    '<li><b>CGHS beneficiaries:</b> assessed and recommended by decentralised Medical Boards at Additional-Director / Regional-HQ level; Appellate Medical Board at CGHS HQ for appeals. <b>CS(MA) beneficiaries:</b> assessed and recommended by the Directorate General of Health Services (DGHS).</li>'
    '<li><b>Marital status:</b> marriage is not a ground for cessation for a dependent son / brother covered on account of critical / terminal illness <i>or permanent disability</i>, provided dependency continues and the Board / authority recommends continuation. The relaxation does <b>not</b> expand “family” — it does not extend to his spouse or children.</li>'
    '<li>Medical criteria are a “living framework”, reviewable by the designated CGHS Board.</li></ul>'
    f'<p class="vnote">Read from the {a("relax", "published text of the OM")}.</p>')

EXT_BODY = (
    '<p><b>OM F. No. S.11030/54/2023-EHS(8248513)/I/3909989/2026 dated 26.10.2026</b> — consideration of cases for dependent sons / brothers with critical / terminal illnesses under the decentralised STC mechanism.</p>'
    '<ul><li>Cases beyond the permissible age limit may be considered under the decentralised STC mechanism of Dte. of CGHS OM No. 56-1/2026-27/CGHS/MSD dated 01.09.2026.</li>'
    '<li>As there is <b>no standing Medical Board in CGHS</b>, the advice / prescription of a <b>Government Specialist</b> of the concerned specialty is taken as the medical recommendation for examination by the <b>Local Technical Committee (LTC)</b> at the office of the Additional Director, CGHS; on its recommendation the card is issued / extended.</li>'
    '<li>The card under this relaxation is issued <b>initially for one year</b>; extension beyond a year needs fresh medical / treatment records showing the continuing illness.</li></ul>'
    '<p class="vnote">Exam note: the 01.09.2026 OM speaks of “decentralised Medical Boards”; the 26.10.2026 clarification says there is no standing Medical Board and the LTC procedure applies — the later OM governs the CGHS procedure.</p>'
    '<details class="listitem"><summary><b>Annexure-A — indicative list of 42 critical and terminal diseases</b></summary><ol class="dlist">'
    + ''.join(f'<li>{escape(d)}</li>' for d in DISEASES) + '</ol></details>'
    f'<p class="vnote">Read from the {a("ext", "published text of the OM")}.</p>')

FPD_BODY = (
    '<p><b>OM File No. S.11030/321/2026-EHS(8430063)/I/3910699/2026 dated 28.10.2026</b> — inclusion and reinstatement of eligible divorced and widowed daughters in CGHS cards of family pensioners.</p>'
    '<ul><li>OM No. 37-1-97-C&amp;P/CGHS/pt.III/CGHS(P) dated 26.05.1999 governs family-member eligibility; the guidelines had no provision to add or reinstate dependants in a family pensioner’s card after the primary cardholder’s death.</li>'
    '<li><b>Now permitted:</b> addition and reinstatement of eligible divorced or widowed daughters in the CGHS cards held by family pensioners, subject to verification of marital status, dependency, income and the other prescribed eligibility conditions. All other CGHS terms continue.</li></ul>'
    f'<p class="vnote">Read from the {a("fpd", "published text of the OM")}.</p>')

DA_BODY = (
    '<p>Department of Expenditure OM No. 1/2(i)/2026-E.II(B) dated 29.10.2026: DA enhanced from <b>60% to 63%</b> of basic pay w.e.f. <b>01.07.2026</b>. '
    'The CGHS dependency ceiling “Rs.9,000 + DA/DR” therefore works out to Rs.9,000 + 63% = <b>≈ Rs.14,670 per month</b> (recompute at each revision).</p>'
    f'<p class="vnote">Read from the {a("da", "published text of the OM")}.</p>')

STC_BODY = (
    '<p><b>CGHS OM F. No. 56-1/2026-27/CGHS/MSD (E-file 8392910) dated 01.09.2026</b> — decentralisation of approval procedure for selected STC-related cases.</p>'
    + cmp(['Category', 'Cases covered'], [
        ['1', 'All transplant cases having notified CGHS package rates or guidelines'],
        ['2', 'Listed procedures, devices and treatment items with notified CGHS rates/guidelines — incl. TAVI, DBS, IVL, cochlear implants, CPAP, BiPAP, oxygen concentrators, CSII pumps'],
        ['3', 'STC-restricted medicines in the list displayed on the CGHS website'],
        ['4', 'Unlisted procedures, investigations, implants, medicines, devices and other treatments'],
        ['5', 'Robotic surgery for cancer cases']], 'Five categories decided by the Additional Director, CGHS within delegated financial powers')
    + '<ul><li><b>No referral / permission / endorsement</b> where treatment is at AIIMS, Institutions of National Importance, Tata Memorial Hospital or <b>any other medical institution under the Central Government or a State Government</b> [para 3(a)].</li>'
    '<li>Approval (Categories 1–5) is accorded by the concerned <b>Additional Director, CGHS</b> within the delegated financial powers, if (i) supported by the recommendation / advice / prescription of <b>one Government Specialist</b> of the concerned specialty from such an institution, or (ii) failing that, by <b>two specialists of the concerned specialty from two different CGHS-empanelled hospitals</b>; (iii) every case is scrutinised by a <b>three-member Local Technical Committee</b> (headed by the AD with two GDMOs); (iv) for STC-restricted medicines the approved indication is verified against CDSCO approval / regulatory status.</li>'
    '<li>Annexure I: cases outside the categories or above the AD’s delegated powers go to the Directorate. Deficiencies are ordinarily communicated within <b>3 working days</b>; a complete case is ordinarily decided within <b>15 working days</b>. <b>Post-facto approval</b> may be considered in an emergency / unavoidable circumstances / reasons beyond the beneficiary’s control, with recorded reasons — not an automatic entitlement. Records are kept for audit; monthly reports to the Directorate; mechanism reviewed monthly.</li>'
    '<li>Para 5: <b>all existing OMs requiring Standing Technical Committee examination stand superseded and subsumed</b> by this OM from the date of issue.</li></ul>'
    f'<p class="vnote">Read from the {a("stc", "published text of the OM")}.</p>')

COCH_BODY = (
    '<p><b>OM F. No. S-367/2026/CGHSHQ/R&amp;H/EHS(8410942)/I/3913657/2026 dated 09.11.2026</b> (IFD concurrence CD No. 2680 dated 04.11.2026) — revised ceiling rates and guidelines for cochlear implantation and rehabilitation under CGHS and CS(MA) Rules, 1944. It refers to OM No. 6-469/2003-CGHS/R&amp;H dated 12 June 2009 and <b>supersedes earlier orders on cochlear implantation</b> (existing sanctions continue on their terms).</p>'
    + cmp(['Category', 'Package ceiling (incl. GST)'], [['Pre-lingual deafness', '<b>Rs.7,00,000</b>'], ['Post-lingual deafness', '<b>Rs.6,00,000</b>']], 'Unilateral implantation — package cost or actual admissible expenditure, whichever is lower')
    + '<ul><li><b>Eligibility — pre-lingual:</b> children 9 months to 7 years with severe-to-profound bilateral sensorineural hearing loss; hearing-aid trial of 3–6 months without appreciable benefit (urgent surgery may be considered in meningitis / cochlear ossification); no intellectual disability, active middle-ear disease, cochlear aplasia, cochlear nerve agenesis, retrocochlear lesion or central deafness; any tympanic perforation closed ≥ 3 months earlier; adequate family support. <b>Post-lingual:</b> severe-to-profound bilateral sensorineural loss, any age, with chronic ear disease treated and retrocochlear / central disorders excluded.</li>'
    '<li><b>Implant:</b> multichannel, CDSCO-approved, admissible for all ages; surgery at Government hospitals, AIIMS, INIs, autonomous Government hospitals or CGHS-empanelled / CS(MA)-recognised hospitals with implant facilities and rehabilitation arrangements.</li>'
    '<li><b>Advice:</b> one ENT specialist of a Government institution (AIIMS, INI, Tata Memorial, any Central/State Government institution); otherwise two ENT specialists of two different CGHS-empanelled hospitals (para 3(b) of OM 01.09.2026).</li>'
    '<li><b>Approval:</b> prior approval is mandatory; for serving and pensioners the Additional Directors (zone/city) permit it under the decentralised STC OM 01.09.2026, <b>Category 2</b>. Initially <b>unilateral</b>; the other side after <b>1 year</b> with justification and assessment. CGHS applications route through Wellness Centres to the AD; <b>CS(MA) beneficiaries through their Ministry/Department/Office to DGHS</b>.</li>'
    '<li><b>Replacement:</b> wear-and-tear upgradation of eligible wearable components after <b>3 years</b> (excluding cords and batteries), reimbursement limited to <b>50%</b> of package cost or actual, whichever is lower.</li></ul>'
    f'<p class="vnote">Read from the {a("coch", "published text of the OM")}.</p>')

GLP_BODY = (
    '<p><b>OM No. 1-360/18-19/CGHS/MSD (2740767/P)-Part (1611)/EHS(8354138) dated 24.07.2026</b> — Injection <b>Tirzepatide (Mounjaro)</b> included in the Online List of Restricted Drugs under CGHS; Injection Tirzepatide and Injection Semaglutide are to be prescribed under CGHS and CS(MA) Rules only per Annexure-I (immediate effect).</p>'
    '<ul><li><b>Eligibility:</b> BMI ≥ 35 kg/m², <i>or</i> BMI ≥ 32.5 kg/m² with one or more of: uncontrolled type-2 diabetes despite metformin + at least two other oral drugs; severe obstructive sleep apnoea; atherosclerotic cardiovascular disease; MASLD; chronic kidney disease.</li>'
    '<li><b>Contraindications:</b> history of pancreatitis; personal / family history of medullary thyroid carcinoma or MEN2; pregnancy or lactation; severe NPDR or PDR; severe GERD, gastroparesis, inflammatory bowel disease or prior metabolic / bariatric surgery.</li>'
    '<li><b>Prerequisites:</b> treating specialist certifies lifestyle modification, dietary counselling and a supervised activity programme complied with for at least <b>3 months</b>.</li>'
    '<li><b>Prescriber:</b> an Endocrinologist or Internal Medicine specialist of a <b>Government hospital</b>; every prescription endorsed by the concerned Head of Department; approval valid <b>6 months</b>, continuation needs a fresh recommendation and endorsement.</li>'
    '<li><b>Monitoring:</b> monthly for the first 3 months, then every 3 months.</li></ul>'
    f'<p class="vnote">Read from the {a("glp1", "published text of the OM")} (Annexure-I read up to the monitoring paragraph).</p>')

BHAV_BODY = (
    '<p><b>OM F. No. S.11012/1/2024-EHS(8283407)/I/3881628/2026 dated 17.07.2026</b> — CGHS web portal integrated with the Bhavishya portal for retiring employees (an <b>additional</b> mode; the existing online application on the CGHS portal continues).</p>'
    '<ul><li>Approved pension details on Bhavishya pre-fill the CGHS Pensioner Card application; <b>PAN</b> is the unique identifier for real-time validation.</li>'
    '<li>After the Head of Office verifies the pension forms, the PPO is generated and the prescribed CGHS contribution is paid online through BharatKosh, the Pensioner Card is generated and can be downloaded from the CGHS Portal and the Bhavishya Portal.</li></ul>'
    f'<p class="vnote">Read from the {a("bhav", "published text of the OM")}.</p>')

DANICS_BODY = (
    '<p><b>OM File No. S.11030/147/2025-EHS(8366647)/I/3830861/2026 dated 09.01.2026</b> — Central Civil Service pensioners under <b>DANICS</b> and similarly placed <b>AGMUT</b> cadre employees may opt for medical facilities either from the State Government from which they retired or under CGHS, at par with AIS pensioners (OM No. S.11011/1/87-CGHS D.I/CGHS(P) dated 01.02.1988), on the same terms.</p>'
    f'<p class="vnote">Read from the {a("danics", "published text of the OM")}.</p>')

HOD_BODY = (
    '<p>Text of <b>OM File No. S.11030/4/2026-EHS(8385264)/I/3840089/2026 dated 16.02.2026</b> verified: the ceiling for Heads of Departments of Ministries/Departments to settle medical-reimbursement cases (no relaxation of CGHS/CS(MA) Rules, entitlement strictly per prescribed rate lists) rises from Rs.5 lakh to <b>Rs.10 lakh without IFD consultation</b> (earlier Rs.2 lakh → Rs.5 lakh by OM No. 11011/20/2014-CGHS(P)/EHS dated 23.11.2016); IFD concurrence CD No. 3131 dated 29.01.2026. '
    'This is the limit for HoDs of Ministries/Departments (serving employees under CGHS or CS(MA)); the CGHS administration’s own powers for pensioners and other beneficiaries are in OM 25.06.2026.</p>'
    f'<p class="vnote">Read from the {a("hod", "published text of the OM")}.</p>')

PARENTS_BODY = (
    '<p>Text of <b>OM S.14025/15/2024-EHS(8270534)/I/3862000/2026 dated 13.05.2026</b> verified: a <b>male</b> Government employee has a one-time option between parents and parents-in-law as dependants under CGHS / CS(MA); once exercised for parents he cannot later opt for parents-in-law (also not on the parents’ demise) and vice-versa. It re-iterates OMs of 03.03.1987, 26.07.2023 and 28.03.2024 (CS(MA) extension).</p>'
    f'<p class="vnote">Read from the {a("parents", "published text of the OM")}.</p>')

# ---- call-outs keyed by rule-card ordinal (document order of the source rule-cards)
CALLOUTS = {
    2: [box('Family: critical / terminal illness (OM 01.09.2026)', RELAX_BODY),
        box('Beyond-age cases & LTC procedure (OM 26.10.2026)', EXT_BODY),
        box('Family pensioners: divorced / widowed daughters (OM 28.10.2026)', FPD_BODY),
        box('Dependency income limit — DA now 63% (DoE OM 29.10.2026)', DA_BODY)],
    3: [box('Parents / parents-in-law — OM 13.05.2026 verified', PARENTS_BODY)],
    4: [box('Pensioner card via Bhavishya portal (OM 17.07.2026)', BHAV_BODY),
        box('DANICS / AGMUT pensioners’ option (OM 09.01.2026)', DANICS_BODY)],
    6: [box('Restricted drugs: Tirzepatide & Semaglutide (OM 24.07.2026)', GLP_BODY)],
    7: [box('Decentralised approval of STC cases (OM 01.09.2026)', STC_BODY)],
    9: [box('Revised financial powers of CGHS authorities (OM 25.06.2026)', DELEG_BODY),
        box('HoD ceiling Rs.10 lakh — OM 16.02.2026 verified', HOD_BODY)],
    10: [box('Cochlear implants — revised ceilings (OM 09.11.2026)', COCH_BODY)],
    18: [box('Applies to CS(MA) too: critical / terminal illness relaxation', '<p>OM 01.09.2026 (see the Latest orders tab) extends to CS(MA) beneficiaries; for them eligibility is assessed and recommended by the <b>DGHS</b>. The family definition itself is not expanded.</p>')],
    24: [box('Cochlear implants under CS(MA) (OM 09.11.2026)', '<p>The revised ceilings (Rs.7,00,000 pre-lingual / Rs.6,00,000 post-lingual, incl. GST) apply to CS(MA) beneficiaries as well; applications are routed through the Ministry / Department / Office to <b>DGHS</b>. Earlier cochlear orders are superseded.</p>')],
    29: [box('HoD delegation — OM 16.02.2026 verified', HOD_BODY)],
    30: [box('CS(MA) family: critical / terminal illness (OM 01.09.2026) & DA 63%', '<p>Dependent sons / brothers with critical or terminal illness may be covered for life (assessment by <b>DGHS</b> for CS(MA)); marriage does not end coverage in those cases; “family” is not expanded to his spouse / children. DA is 63% from 01.07.2026, so Rs.9,000 + DA ≈ Rs.14,670.</p>')],
}

# ---- register of verified orders (Latest orders tab)
ORDERS = [
    ('09.01.2026', 'S.11030/147/2025-EHS(8366647)/I/3830861/2026', 'CGHS facilities option for DANICS / AGMUT pensioners at par with AIS pensioners', 'danics'),
    ('16.02.2026', 'S.11030/4/2026-EHS(8385264)/I/3840089/2026', 'HoD ceiling Rs.5 lakh → Rs.10 lakh without IFD (CGHS & CS(MA))', 'hod'),
    ('13.05.2026', 'S.14025/15/2024-EHS(8270534)/I/3862000/2026', 'Parents / parents-in-law: one-time option (male employee), CGHS & CS(MA)', 'parents'),
    ('25.06.2026', 'Z.15025/14/2/DIR/CGHS', 'Revised financial powers: AD CGHS Rs.15 lakh, Director Rs.25 lakh, AS&DG Rs.50 lakh; unlisted items Rs.2 / 5 / 10 lakh; permissions & ex-post facto', 'deleg'),
    ('17.07.2026', 'S.11012/1/2024-EHS(8283407)/I/3881628/2026', 'CGHS–Bhavishya portal integration for Pensioner Cards', 'bhav'),
    ('24.07.2026', '1-360/18-19/CGHS/MSD (2740767/P)-Part (1611)/EHS(8354138)', 'Tirzepatide & Semaglutide: restricted-drug guidelines', 'glp1'),
    ('01.09.2026', '56-1/2026-27/CGHS/MSD (E-file 8392910)', 'Decentralised approval of STC-related cases (5 categories, LTC); supersedes earlier STC OMs', 'stc'),
    ('01.09.2026', 'S.11030/54/2023-EHS(8248513)/I/3893459/2026', 'Critical / terminal illness: lifelong cover for dependent sons & brothers; marital-status relaxation', 'relax'),
    ('26.10.2026', 'S.11030/54/2023-EHS(8248513)/I/3909989/2026', 'Beyond-age cases via LTC; card annual; Annexure-A 42 diseases', 'ext'),
    ('28.10.2026', 'S.11030/321/2026-EHS(8430063)/I/3910699/2026', 'Family pensioners: add / reinstate eligible divorced & widowed daughters', 'fpd'),
    ('29.10.2026', 'No. 1/2(i)/2026-E.II(B) (DoE, Ministry of Finance)', 'DA 60% → 63% w.e.f. 01.07.2026', 'da'),
    ('09.11.2026', 'S-367/2026/CGHSHQ/R&H/EHS(8410942)/I/3913657/2026', 'Cochlear implants: Rs.7,00,000 pre-lingual / Rs.6,00,000 post-lingual; supersedes earlier orders', 'coch'),
]


def latest_view(corrections):
    rows = ''.join(f'<tr><td>{d}</td><td>{escape(f)}</td><td>{escape(s)}</td><td><a href="{URL[k]}" rel="noopener">read</a></td></tr>' for d, f, s, k in ORDERS)
    reg = ('<div class="tblwrap"><table class="cmp"><caption>Orders read in full from the primary text (2026)</caption><thead><tr><th>Date</th><th>File / OM no.</th><th>Subject</th><th>Text</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
    intro = ('<div class="notice-box"><h3>📅 How current is this?</h3><p>Orders up to <b>09.11.2026</b> found for CGHS / CS(MA) were read and incorporated (searched 25.11.2026). '
             'The texts were read from copies of the official OMs hosted on staffnews.in; the MoHFW / CGHS sites could not be opened from this environment (HTTP 502), so nothing was cross-checked there. '
             'Not found: any order on AMA appointment / re-verification, and the CS(MA) Rules PDF — those items stay on the <a href="#verify">Verify tab</a>.</p></div>')
    sections = (
        '<h3>Who can join CGHS — 5 km rule removed (OM 17.09.2026)</h3>' + ELIG_BODY +
        '<h3>CGHS final-claim time limit — 6 months (OM 01.06.2020)</h3>' + TL_BODY +
        '<h3>Financial powers — CGHS (OM 25.06.2026)</h3>' + DELEG_BODY +
        '<h3>HoD ceiling (OM 16.02.2026)</h3>' + HOD_BODY +
        '<h3>Decentralised STC approvals (OM 01.09.2026)</h3>' + STC_BODY +
        '<h3>Dependent sons / brothers with critical / terminal illness</h3>' + RELAX_BODY + EXT_BODY +
        '<h3>Family pensioners’ daughters (OM 28.10.2026)</h3>' + FPD_BODY +
        '<h3>Cochlear implants (OM 09.11.2026)</h3>' + COCH_BODY +
        '<h3>Restricted drugs — GLP-1 (OM 24.07.2026)</h3>' + GLP_BODY +
        '<h3>Pensioner card — Bhavishya integration (OM 17.07.2026)</h3>' + BHAV_BODY +
        '<h3>DANICS / AGMUT pensioners (OM 09.01.2026)</h3>' + DANICS_BODY +
        '<h3>DA 63% (DoE OM 29.10.2026)</h3>' + DA_BODY +
        '<h3>Parents / parents-in-law (OM 13.05.2026)</h3>' + PARENTS_BODY +
        '<h3>2025 rate clarifications and transition</h3>' + MRI_BODY +
        '<h3>Generic / branded medicines (OM 16.05.2025)</h3>' + GENERIC_BODY +
        '<h3>CS(MA) delegation to HoDs (OM 05.06.2014)</h3>' + HOD2014_BODY +
        '<h3>Medical advance without package rate (OM 22.09.2021)</h3>' + ADV_BODY +
        '<h3>Pensioners and CS(MA) (OM 12.09.2022)</h3>' + PEN_BODY)
    sec = ''
    corr = ''
    if corrections:
        groups = {}
        for c in corrections:
            groups.setdefault(c['reason'], []).append(c)
        items = []
        for reason, cs in groups.items():
            eng = [c for c in cs if c['kind'] != 'hinglish' and not c['old'].startswith('Hinglish')]
            ex = (eng or cs)[0]
            old, new = ex['old'], ex['new']
            # show a compact window around the first difference
            i = next((k for k, (x, y) in enumerate(zip(old, new)) if x != y), 0)
            lo = max(0, i - 70)
            items.append(f'<div class="listitem"><span class="tag">Replaced · {len(cs)} places</span><b>Why:</b> {escape(reason)}<br><del>…{escape(old[lo:i+120])}…</del><br><ins>…{escape(new[lo:i+170])}…</ins></div>')
        corr = ('<h3>Corrections made to the guide’s earlier text</h3><p class="lead">Obsolete or wrong statements in the source file were replaced everywhere they occurred (English and Hinglish); one example of the old and new wording is shown for each. The full list is in <code>build/corrections_log.json</code>.</p>' + ''.join(items))
    return intro + reg + corr + sections + sec


# ======================= additions (second research pass, 26.11.2026) =======================
URL.update({
    'elig': SN + '/2026/09/eligibility-for-availing-cghs-facilities-5-km-radius-limit-removed.html',
    'mri': SN + '/2026/03/cghs-rates-applicable-for-mri-without-contrast-and-super-specialist.html',
    'generic': SN + '/2025/06/revised-instructions-for-the-issue-of-generic-branded-medicines-at-cghs.html',
    'tms': SN + '/2025/10/transition-to-revised-cghs-rates-2025-and-tms-2-0.html',
})

ELIG_BODY = (
    '<p><b>OM F. No. Z.16025/227/2026/CGHS-III/EHS(8421134) dated 17.09.2026</b> — eligibility of serving Central Government employees for CGHS (immediate effect). '
    'It refers to OM No. C.14012/02/2018/CGHS-III/DIR dated 06.04.2018, under which CGHS coverage of serving employees was restricted to those residing / working within a <b>5 km radius</b> of a CGHS Wellness Centre.</p>'
    '<ul><li><b>The geographical (5 km) criterion is totally dispensed with.</b></li>'
    '<li><b>One-time option:</b> serving employees residing / posted outside the earlier geographical coverage or in a city not covered by CGHS, who are on CS(MA) Rules solely for that reason, may opt to become CGHS beneficiaries, subject to other eligibility conditions and payment of the prescribed CGHS contribution.</li>'
    '<li><b>Mandatory CGHS:</b> serving employees residing or posted within the CGHS-covered area, i.e. the limits of the district headquarters where a CGHS Wellness Centre is situated, are <b>mandatorily covered under CGHS</b> and cannot opt out in favour of CS(MA).</li>'
    '<li><b>Conditions of the option:</b> one-time, final and binding; applies to <b>all dependants</b> (no splitting between the two systems); the employee keeps paying the CGHS contribution irrespective of residence / posting; no simultaneous claims under CGHS and CS(MA); <b>no TA/DA</b> for treatment or medicine procurement under CGHS rules; an <b>undertaking</b> that benefits will not be availed under both systems (inadmissible benefits are recoverable).</li>'
    '<li>Employees who do not opt <b>continue under CS(MA) Rules, 1944</b>. False, incorrect or suppressed information attracts disciplinary action under the CCS (Conduct) Rules, 1964 and recovery.</li></ul>'
    '<p class="vnote"><b>Effect on the exam answer:</b> “CS(MA) applies where CGHS does not” is now only the default. A serving employee outside a CGHS area may choose CGHS once, irrevocably, for the whole family.</p>'
    f'<p class="vnote">Read from the {a("elig", "published text of the OM")}.</p>')

MRI_BODY = (
    '<p><b>CGHS Directorate OM F. No. 5-16/CGHS(HQ)/HEC/2024(Part I)/I/38850429/2026 dated 24.03.2026</b> — clarification, effective <i>ab initio</i>, forming part of OM 03.10.2025: code <b>RI134</b> reads “MRI Dorsal / Dorso-Lumbar Spine / Cervical / Cervico-Dorsal Spine – <b>Without Contrast</b>”; for code <b>CN003</b> (OPD consultation) “Super Specialist” means DM / MCh / DNB-SS or an equivalent qualification as per National Medical Commission norms.</p>'
    '<p><b>Transition to the 2025 rates — OM 12.10.2025</b> (F. No. 5-16/CGHS(HQ)/HEC/2024 Part I): Revised Rates apply from <b>00:00 hrs on 13.10.2025</b>; all new registrations only on <b>TMS 2.0</b> (none on TMS 1.0 after that time); surgical / radiotherapy packages booked before 13.10.2025 continue at <b>old rates</b> until completed; ongoing medical management started earlier continues in the same case with services from 13.10.2025 billed at revised rates; no beneficiary is to be sent back to CGHS only to obtain a new referral.</p>'
    f'<p class="vnote">Read from the {a("mri", "MRI clarification")} and the {a("tms", "TMS 2.0 transition OM")}.</p>')

GENERIC_BODY = (
    '<p><b>OM F. No. Z.15025/117/2017/DIR/CGHS/EHS(3132722) dated 16.05.2025</b> (continuing OM of 15.01.2018) — issue of generic / branded medicines at Wellness Centres: '
    '(1) medicines prescribed by specialists are supplied by the <b>available generic name</b>; (2) if available under an <b>alternative brand</b> of the same composition, that brand is supplied; (3) if available in neither form, it is <b>indented by the same brand name through the Authorised Local Chemist</b>. Subject to admissibility instructions issued from time to time.</p>'
    f'<p class="vnote">Read from the {a("generic", "published text of the OM")}.</p>')

CALLOUTS[0] = CALLOUTS.get(0, []) + [box('Who can join CGHS — 5 km rule removed (OM 17.09.2026)', ELIG_BODY)]
CALLOUTS[16] = CALLOUTS.get(16, []) + [box('CS(MA) vs CGHS — one-time option (OM 17.09.2026)', ELIG_BODY)]
CALLOUTS[17] = CALLOUTS.get(17, []) + [box('Rule 1 coverage — see OM 17.09.2026', '<p>A serving employee posted in a CGHS-covered area (district HQ limits where a Wellness Centre is situated) is mandatorily under CGHS and outside CS(MA); one outside such an area may opt once, irrevocably, for CGHS for the whole family; otherwise CS(MA) continues. Details: the update box in the CS(MA) preamble and the Latest orders tab.</p>')]
CALLOUTS[6] = CALLOUTS.get(6, []) + [box('Generic / branded medicines (OM 16.05.2025)', GENERIC_BODY)]
CALLOUTS[8] = CALLOUTS.get(8, []) + [box('2025 rate clarifications & transition (OM 24.03.2026 / 12.10.2025)', MRI_BODY)]

ORDERS += [
    ('16.05.2025', 'Z.15025/117/2017/DIR/CGHS/EHS(3132722)/I/3767573/2025', 'Generic / branded medicines at Wellness Centres (3-step rule)', 'generic'),
    ('12.10.2025', '5-16/CGHS(HQ)/HEC/2024(Part I)/I/3809236/2025', 'Transition to revised CGHS rates 2025 and TMS 2.0 (effective 13.10.2025)', 'tms'),
    ('24.03.2026', '5-16/CGHS(HQ)/HEC/2024(Part I)/I/38850429/2026', 'Clarification: code RI134 (MRI without contrast); super specialist = DM/MCh/DNB-SS', 'mri'),
    ('17.09.2026', 'Z.16025/227/2026/CGHS-III/EHS(8421134)', '5 km criterion removed; one-time option CS(MA) → CGHS; mandatory CGHS in covered area', 'elig'),
]
ORDERS.sort(key=lambda o: tuple(reversed(o[0].split('.'))))


# ======================= third research pass (26.11.2026): claim limits, CS(MA) delegation, advance, pensioners =======================
URL.update({
    'tl2020': SN + '/2020/06/revision-of-time-limit-for-submission-of-final-claims.html',
    'hod2014': SN + '/2021/12/delegation-of-powers-to-heads-of-departments-for-permission-and-approval-under-cs-ma-rules.html',
    'adv2021': SN + '/2021/10/grant-of-medical-advance-for-all-treatment-opd-and-ipd-under-cghs-csms-rules.html',
    'pen2022': SN + '/2022/09/reimbursement-of-medical-claims-to-pensioners-under-csma-rules-1944.html',
    'pen2016': SN + '/2020/07/reimbursement-of-medical-claims-to-pensioners-residing-in-non-cghs-areas.html',
})

TL_BODY = (
    '<p><b>CGHS OM File No. 1-60/2017-CGHS/C&amp;P/EHS (e-signed 01.06.2020)</b> — “Revision of time limit for submission of final claims for reimbursement of medical expenses under CGHS”.</p>'
    '<ul><li>Earlier CGHS guidelines: <b>3 months</b>. Revised to <b>6 months</b>.</li>'
    '<li>Only cases where bills are submitted <b>after 6 months</b> from the date of completion of treatment / discharge from hospital need to be taken up for <b>condonation</b>; the power of condonation and other terms are as in OM No. S.14025/8/99-MS dated 25.05.1999.</li></ul>'
    '<p class="vnote"><b>Correction made:</b> the guide’s “CGHS = 3 months; CS(MA) = 6 months — different!” is obsolete. Both CGHS and CS(MA) final claims are now 6 months (CS(MA): 6 months from discharge / treatment; 1 month from discharge where an IPD advance was drawn). No later revision was found; confirm on the CGHS site before quoting.</p>'
    f'<p class="vnote">Read from the {a("tl2020", "published text of the OM")}.</p>')

HOD2014_BODY = (
    '<p><b>MoHFW OM No. S.14025/01/2014-MS dated 05.06.2014</b> (IFD concurrence CD No. 335 dated 28.05.2014) — delegation to Heads of Departments for CS(MA) beneficiaries. '
    '<span class="tag">Read in a Department of Posts letter of 25.11.2021 that reproduces it</span></p>'
    '<ul><li>A serving employee covered under CS(MA) who is being treated at a Government hospital and wants treatment in a <b>private hospital recognised under CGHS / CS(MA)</b>: the <b>Head of Department may grant permission</b> for indoor treatment on the prescription of the concerned AMA.</li>'
    '<li>Heads of Departments may <b>decide reimbursement of emergency treatment</b> at a private hospital / nursing home / clinic, subject to <b>item-wise ceiling</b> as per CGHS / CS(MA) rates.</li>'
    '<li>Departments / Ministries settle all cases with <b>no relaxation of rules</b> where entitlement is worked out from the prescribed rate list: Heads up to <b>Rs.2,00,000</b>; above that (still per rate list) in consultation with the Internal Finance Division; only cases needing <b>relaxation of rules</b> go to MoHFW.</li></ul>'
    '<p class="vnote">The letter adds that MoHFW (ID No. S.14025/35/2021-EHS dated 29.10.2021) clarified that the 2014 OM remains valid for CS(MA) beneficiaries, and that the Rs.5 lakh enhancement of OM 23.11.2016 was noted as applying to CGHS beneficiary cases. '
    'OM 16.02.2026 now sets the HoD ceiling at <b>Rs.10 lakh</b> for settlement “under CGHS or CS(MA) Rules”.</p>'
    f'<p class="vnote">Read from the {a("hod2014", "Department of Posts letter reproducing the OM")} — relayed text.</p>')

ADV_BODY = (
    '<p><b>MoHFW OM No. Z.15025/8/2021/DIR/CGHS (signed 22.09.2021)</b> — medical advance where <b>no package rate</b> is prescribed (refers to OM No. 14025/18/2015-MS/EHSS dated 17.10.2016: 90% advance for all treatment, OPD and IPD):</p>'
    '<ul><li>Admissible amount is computed <b>item-wise at CGHS rates</b>; for items with no CGHS rate, <b>AIIMS rates</b>; if there is none, the <b>actual estimate</b>.</li>'
    '<li>The hospital seeking the advance must give an <b>item-wise break-up</b> of the estimate; <b>90%</b> of the admissible amount so arrived at is advanced.</li>'
    '<li>Other terms of the 17.10.2016 OM are unchanged.</li></ul>'
    f'<p class="vnote">Read from the {a("adv2021", "published text of the OM")}.</p>')

PEN_BODY = (
    '<p><b>MoHFW OM File No. S.14028/30/2022-EHS dated 12.09.2022</b> — reimbursement of medical claims to pensioners under CS(MA) Rules (as directed by CATs / courts):</p>'
    '<ul><li>Retired Government officials are <b>not covered</b> by the CS(MA) Rules (an earlier OM No. S.14025/23/2013-MS-EHSS dated 29.09.2016 said the same: the Rules “are not applicable to pensioners”).</li>'
    '<li>Pensioners residing in <b>non-CGHS areas</b> have three options: (1) <b>FMA</b> in lieu of OPD; (2) <b>CGHS (OPD &amp; IPD)</b> by registering at the nearest CGHS-covered city with the required subscription; (3) <b>FMA for OPD and CGHS for IPD</b> with subscription.</li>'
    '<li>Ministries / Departments are to defend CAT / court cases in this light and need not refer them to MoHFW; retiring employees are to be made aware of the position.</li></ul>'
    '<p class="vnote">This confirms the guide’s statement that pensioners are excluded from CS(MA) (the guide cites Rule 1 Note 2(iv); the OM calls it a note below Rule 2).</p>'
    f'<p class="vnote">Read from the {a("pen2022", "published text of the OM")} and the {a("pen2016", "DoT copy reproducing the 2016 OM")}.</p>')

CALLOUTS[9] = CALLOUTS.get(9, []) + [box('CGHS final-claim time limit is 6 months (OM 01.06.2020) — replaces the 3-month rule', TL_BODY), box('Medical advance where no package rate exists (OM 22.09.2021)', ADV_BODY)]
CALLOUTS[29] = CALLOUTS.get(29, []) + [box('CS(MA) delegation to HoDs — OM 05.06.2014 (permissions, emergencies, limit)', HOD2014_BODY), box('Medical advance where no package rate exists (OM 22.09.2021)', ADV_BODY)]
CALLOUTS[22] = CALLOUTS.get(22, []) + [box('HoD permission for private-hospital treatment & emergency reimbursement (OM 05.06.2014)', HOD2014_BODY)]
CALLOUTS[17] = CALLOUTS.get(17, []) + [box('Pensioners are outside CS(MA) — their three options (OM 12.09.2022)', PEN_BODY)]
CALLOUTS[25] = CALLOUTS.get(25, []) + [box('Claim time limit — CGHS and CS(MA) are both 6 months', '<p>CGHS final claims were also moved to 6 months by OM 01.06.2020 (see the update box in the CGHS reimbursement section). A delay beyond 6 months needs condonation.</p>')]

ORDERS += [
    ('05.06.2014', 'S.14025/01/2014-MS (relayed by DoP letter 25.11.2021)', 'CS(MA): HoD permission, emergency reimbursement; Rs.2 lakh limit, IFD above, relaxation → MoHFW', 'hod2014'),
    ('29.09.2016', 'S.14025/23/2013-MS-EHSS (as reproduced in a DoT letter)', 'CS(MA) Rules not applicable to pensioners; options for pensioners', 'pen2016'),
    ('01.06.2020', '1-60/2017-CGHS/C&P/EHS', 'CGHS final-claim time limit revised from 3 to 6 months; condonation only after 6 months', 'tl2020'),
    ('22.09.2021', 'Z.15025/8/2021/DIR/CGHS', 'Medical advance where no package rate: item-wise CGHS rate → AIIMS rate → actual estimate; 90%', 'adv2021'),
    ('12.09.2022', 'S.14028/30/2022-EHS', 'Pensioners not covered by CS(MA); FMA / CGHS / both options', 'pen2022'),
]
ORDERS.sort(key=lambda o: tuple(reversed(o[0].split('.'))))
