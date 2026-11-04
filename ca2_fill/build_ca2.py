from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BLACK = RGBColor(0x00, 0x00, 0x00)
GRAY = RGBColor(0x59, 0x59, 0x59)
HEADER_BLUE = RGBColor(0x5B, 0x9B, 0xD5)
ROW_LIGHT = RGBColor(0xD9, 0xE2, 0xF3)
ROW_LIGHTER = RGBColor(0xEA, 0xEF, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Calibri"
FONT_LIGHT = "Calibri Light"

SW, SH = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.78)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
blank = prs.slide_layouts[6]


def add_slide():
    s = prs.slides.add_slide(blank)
    bg = s.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = WHITE
    return s


def textbox(slide, left, top, width, height, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def para(tf, new, align=PP_ALIGN.LEFT, line_spacing=1.15, space_after=6, space_before=0):
    p = tf.paragraphs[0] if not new else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line_spacing
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    return p


def run(p, text, size=18, bold=False, italic=False, color=BLACK, font=FONT):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    r.font.color.rgb = color
    return r


def heading(slide, text, top=Inches(0.55)):
    tb, tf = textbox(slide, MARGIN, top, Inches(11.5), Inches(1.0))
    p = para(tf, new=False)
    run(p, text, size=40, bold=False, font=FONT_LIGHT, color=BLACK)


def bullet_block(slide, items, top, left=MARGIN, width=Inches(11.5), size=20,
                  gap_before_first=0.25, space_after=10, bold_lead=None):
    tb, tf = textbox(slide, left, top, width, Inches(5.0))
    for i, item in enumerate(items):
        p = para(tf, new=(i > 0), space_after=space_after, line_spacing=1.2)
        run(p, "• ", size=size, color=BLACK)
        if isinstance(item, tuple):
            lead, rest = item
            run(p, lead, size=size, bold=True, color=BLACK)
            if rest:
                run(p, rest, size=size, bold=False, color=BLACK)
        else:
            run(p, item, size=size, color=BLACK)
    return tb


def footnote(slide, text, top=Inches(7.05)):
    tb, tf = textbox(slide, MARGIN, top, Inches(11.8), Inches(0.35))
    p = para(tf, new=False)
    run(p, text, size=10.5, italic=True, color=GRAY)


# =====================================================================
# SLIDE 1 — TITLE
# =====================================================================
s = add_slide()
tb, tf = textbox(s, Inches(0), Inches(2.6), SW, Inches(1.4), anchor=MSO_ANCHOR.MIDDLE)
p = para(tf, new=False, align=PP_ALIGN.CENTER, space_after=4)
run(p, "VERDIKT", size=54, bold=False, font=FONT_LIGHT, color=BLACK)
p2 = para(tf, new=True, align=PP_ALIGN.CENTER, space_before=10)
run(p2, "Turning Business Decisions Into Measurable Learning", size=20, color=GRAY)

tb2, tf2 = textbox(s, Inches(0), Inches(4.55), SW, Inches(0.5), anchor=MSO_ANCHOR.TOP)
p3 = para(tf2, new=False, align=PP_ALIGN.CENTER)
run(p3, "B.Tech Artificial Intelligence & Machine Learning  ·  CA2 Capstone Project  ·  AY 2026–27", size=13, color=GRAY)

tb3, tf3 = textbox(s, Inches(0), Inches(5.3), SW, Inches(0.5), anchor=MSO_ANCHOR.TOP)
p4 = para(tf3, new=False, align=PP_ALIGN.CENTER)
run(p4, "Name: Utsav Tyagi    PRN: 26070126233    Branch: AI/ML    Division: C-3", size=12, color=GRAY)
p5 = para(tf3, new=True, align=PP_ALIGN.CENTER, space_before=4)
run(p5, "Symbiosis Institute of Technology, Pune", size=11, color=GRAY)

# =====================================================================
# SLIDE 2 — OBJECTIVE
# =====================================================================
s = add_slide()
heading(s, "OBJECTIVE")
bullet_block(s, [
    ("Specific problem statement: ",
     "Businesses make repeated, consequential decisions — retention discounts, pricing changes, feature launches — without recording a measurable assumption about the expected outcome, and without later checking whether that assumption held true."),
], top=Inches(1.9), size=19)

tb, tf = textbox(s, MARGIN, Inches(3.4), Inches(11.6), Inches(2.2))
p = para(tf, new=False, space_after=8)
run(p, "This creates ", size=18, color=BLACK)
run(p, "Decision Debt", size=18, bold=True, color=BLACK)
run(p, ": an accumulation of unresolved assumptions, overdue reviews, invalidated assumptions still driving active work, and repeated forecasting errors. Ordinary dashboards and project-management tools report what happened; none of them capture what a team believed would happen before it acted, so the belief can never be systematically checked.", size=18, color=BLACK)
p2 = para(tf, new=True, space_before=14)
run(p2, "Goal: ", size=18, bold=True, color=BLACK)
run(p2, "build a lightweight decision-to-outcome tracking workflow, Verdikt, that converts a business decision into a structured, measurable commitment and automatically evaluates it against reality.", size=18, color=BLACK)

# =====================================================================
# SLIDE 3 — LITERATURE REVIEW
# =====================================================================
s = add_slide()
heading(s, "LITERATURE REVIEW")
bullet_block(s, ["Discussing drawback of atleast 3 research papers (existing technology)"], top=Inches(1.75), size=19)

rows_data = [
    ("Scheibel & Rinderle-Ma\n(CAiSE 2023)",
     "An End-to-End Approach for\nOnline Decision Mining and\nDecision Drift Analysis",
     "Monitors decision rules at runtime (not just after the fact); detects “decision drift”; validated on 4 synthetic + 1 real-life log",
     "Tracks how an automated decision RULE changes — not whether a human's stated assumption about an outcome came true; needs existing event logs",
     "We track a human assumption vs. a measured outcome; they track automated rule drift inside a process log — adjacent problem, different object"),
    ("Goossens, De Smedt\n& Vanthienen (2024, KU Leuven)",
     "Extracting Process-Aware\nDecision Models from Object-\nCentric Process Data",
     "First object-centric decision-mining algorithm (IODDA); discovers decision structure + rules directly from logs; open benchmark released",
     "Purely retrospective — reconstructs a model from data that already exists; can't recover an assumption that was never logged; no deadline/validation concept",
     "We capture the assumption BEFORE the outcome is known (forward-looking); they mine structure AFTER the fact (backward-looking) — complementary, not a substitute"),
    ("Natarajan, Mathur, Sidheekh,\nStammer & Kersting (AAAI-25)",
     "Human-in-the-loop or AI-in-\nthe-loop? Automate or\nCollaborate?",
     "Directly tackles when to automate a decision vs. keep a human in control; argues evaluation over-weights the model, under-weights the human expert",
     "A conceptual/positional framework, not a deployable system; no mechanism to record or later validate the human's stated assumption",
     "We operationalise exactly this division of labour: the model scores risk, a human approves + states the assumption, the system checks the outcome later"),
    ("Gruetzemacher, Lee\n& Paradice (2024)",
     "Calibration Training for\nImproving Probabilistic\nJudgments Using an Interactive App",
     "Shows forecast calibration can be measurably improved with short, repeated feedback — supports asking for a stated confidence number",
     "Small exploratory study (153 students, a sports-forecasting tournament); trains general forecasting skill, not tied to any business decision or metric",
     "We don't train forecasting skill in the abstract — we capture a one-off, decision-specific forecast and check it against a real business metric"),
]

tbl_left, tbl_top = MARGIN, Inches(2.25)
col_w = [Inches(2.0), Inches(2.15), Inches(2.45), Inches(2.45), Inches(2.6)]
tbl_w = sum(col_w, Emu(0))
n_rows = len(rows_data) + 1
header_h = Inches(0.5)
data_h = Inches(1.08)
total_h = header_h + data_h * len(rows_data)
gtbl = s.shapes.add_table(n_rows, 5, tbl_left, tbl_top, tbl_w, total_h).table
for i, w in enumerate(col_w):
    gtbl.columns[i].width = w
gtbl.rows[0].height = header_h
for ri in range(1, n_rows):
    gtbl.rows[ri].height = data_h
headers = ["AUTHOR(S) & YEAR", "TITLE", "PROS", "CONS", "DIFFERENTIATION FROM VERDIKT"]
for c, h in enumerate(headers):
    cell = gtbl.cell(0, c)
    cell.fill.solid(); cell.fill.fore_color.rgb = HEADER_BLUE
    cell.margin_left = Pt(5); cell.margin_right = Pt(5); cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = h
    r.font.size = Pt(10.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE
for ri, row in enumerate(rows_data, start=1):
    fill = ROW_LIGHT if ri % 2 == 1 else ROW_LIGHTER
    for ci, val in enumerate(row):
        cell = gtbl.cell(ri, ci)
        cell.fill.solid(); cell.fill.fore_color.rgb = fill
        cell.margin_left = Pt(5); cell.margin_right = Pt(5); cell.margin_top = Pt(3); cell.margin_bottom = Pt(3)
        cell.vertical_anchor = MSO_ANCHOR.TOP
        tf = cell.text_frame; tf.word_wrap = True
        lines = val.split("\n")
        for li, line in enumerate(lines):
            p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.line_spacing = 1.0
            p.space_after = Pt(0)
            r = p.add_run(); r.text = line
            r.font.size = Pt(8.5); r.font.name = FONT; r.font.color.rgb = BLACK

footnote(s, "All four papers published 2023–2025 (peer-reviewed / top-tier preprint). Pros, Cons and Differentiation assessed against Verdikt's specific mechanism: an explicit, falsifiable assumption bound to a deadline-evaluated outcome. Full citations on the References slide.", top=Inches(6.95))

# =====================================================================
# SLIDE 4 — NOVELTY
# =====================================================================
s = add_slide()
heading(s, "NOVELTY")
bullet_block(s, [
    ("What new techniques used: ",
     "Combines a churn-risk classifier (Random Forest, trained on real customer-behaviour data) with a rule-based Decision Evaluation Engine that checks a stated forecast against the actual outcome at a deadline, assigning one of six honest validation states — Validated, Partially Validated, Invalidated, Inconclusive, Stale, or Not Measurable."),
    ("How your topic is different from existing one: ",
     "BI dashboards report outcomes only; Jira/Notion capture decisions without a bound forecast; corporate prediction markets (P0, Hypermind) forecast a question but aren't tied to a company's own decision log; enterprise decision-intelligence patents are heavyweight, org-wide systems. A deeper prior-art search also found small prediction-and-outcome journals (RationalGo, Reckon, Condelo) that do pieces of this. Verdikt's honest claim is narrower: no prior art found combines an explicit, falsifiable assumption with automatic outcome evaluation in a lightweight workflow sized for a single product or retention team, with a published six-state evaluation engine and a working prototype."),
], top=Inches(1.9), size=18.5, space_after=16)

# =====================================================================
# SLIDE 5 — DATASET USED
# =====================================================================
s = add_slide()
heading(s, "DATASET USED")
bullet_block(s, [
    ("Link: ", "Synthetic dataset generated for this project — no external public-repository link; file supplied directly as Customer_Transactions.csv."),
    ("Downloaded data set: ", "10,000 fictional customer-decision records · 14 fields — age, gender, country, annual income, spending score, number of purchases, average purchase value, membership years, website visits/month, cart-abandon rate, churned (target), feedback text, last purchase date."),
], top=Inches(1.9), size=19)

tb, tf = textbox(s, MARGIN, Inches(4.1), Inches(11.5), Inches(1.6))
p = para(tf, new=False)
run(p, "Note: ", size=16, bold=True, color=BLACK)
run(p, "clearly labelled synthetic / fictional data, used for prototype demonstration only — not drawn from any real company's customers.", size=16, italic=True, color=GRAY)

# =====================================================================
# SLIDE 6 — ML ALGORITHM
# =====================================================================
s = add_slide()
heading(s, "ML ALGORITHM")
bullet_block(s, ["Implementation of problem formulation using ML"], top=Inches(1.75), size=19)

tb, tf = textbox(s, MARGIN, Inches(2.6), Inches(11.6), Inches(4.0))
items = [
    ("Problem formulation: ", "binary classification — predict whether a customer churns within 30 days (churned = 1) or is retained (churned = 0)."),
    ("Features: ", "spending score, cart-abandon rate, website visits/month, number of purchases, average purchase value, membership years, annual income, age, gender, country."),
    ("Preprocessing: ", "StandardScaler on numeric features, One-Hot Encoding on categorical features (gender, country)."),
    ("Train/test split: ", "80% / 20%, stratified by class to preserve the churn ratio."),
    ("Algorithms compared: ", "Logistic Regression (baseline) vs. Random Forest Classifier, 300 trees, class_weight=\"balanced\" to correct for churn being only 10.9% of the data."),
]
for i, (lead, rest) in enumerate(items):
    p = para(tf, new=(i > 0), space_after=12, line_spacing=1.2)
    run(p, "• ", size=18, color=BLACK)
    run(p, lead, size=18, bold=True, color=BLACK)
    run(p, rest, size=18, color=BLACK)

# =====================================================================
# SLIDE 7 — IF IMPLEMENTED (RESULT)
# =====================================================================
s = add_slide()
heading(s, "IF IMPLEMENTED (RESULT)")
bullet_block(s, ["Which tools/language used to implement"], top=Inches(1.75), size=19)

tb, tf = textbox(s, MARGIN, Inches(2.5), Inches(11.5), Inches(0.6))
p = para(tf, new=False)
run(p, "Python 3 · Pandas · NumPy · Scikit-learn · Matplotlib", size=18, bold=True, color=BLACK)

tb2, tf2 = textbox(s, MARGIN, Inches(3.25), Inches(11.6), Inches(0.4))
p2 = para(tf2, new=False)
run(p2, "Result (Random Forest, held-out test set, n = 2,000) — real, computed values:", size=18, bold=True, color=BLACK)

metrics = [("Precision", "0.26"), ("Recall", "0.78"), ("F1-score", "0.39"), ("ROC-AUC", "0.84")]
mx = MARGIN
mw, mh, mgap = Inches(2.6), Inches(1.2), Inches(0.25)
for i, (lbl, val) in enumerate(metrics):
    x = Emu(int(mx + i * (mw + mgap)))
    box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(3.8), mw, mh)
    box.fill.solid(); box.fill.fore_color.rgb = ROW_LIGHTER
    box.line.color.rgb = HEADER_BLUE; box.line.width = Pt(1.25)
    try:
        box.shadow.inherit = False
    except Exception:
        pass
    tf3 = box.text_frame; tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
    p3 = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
    r = p3.add_run(); r.text = val
    r.font.size = Pt(26); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = BLACK
    p4 = tf3.add_paragraph(); p4.alignment = PP_ALIGN.CENTER
    r2 = p4.add_run(); r2.text = lbl
    r2.font.size = Pt(13); r2.font.name = FONT; r2.font.color.rgb = GRAY

tb3, tf4 = textbox(s, MARGIN, Inches(5.35), Inches(11.6), Inches(1.3))
p5 = para(tf4, new=False)
run(p5, "Interpretation: ", size=16, bold=True, color=BLACK)
run(p5, "optimised for recall over precision — catching 78% of true churners matters more than being right every time, since churn is only 10.9% of the data. The model flags risk; it does not prove any retention action caused a customer to stay — that requires a controlled comparison, which the Decision Evaluation Engine checks for.", size=16, color=BLACK)

# =====================================================================
# SLIDE 8 — CONCLUSION
# =====================================================================
s = add_slide()
heading(s, "CONCLUSION")
bullet_block(s, [
    "Decision Debt — the accumulation of decisions whose assumptions are never checked against reality — is a real, recurring gap that ordinary dashboards and project trackers do not close.",
    "Verdikt prototypes a lightweight workflow (Capture → Structure → Forecast → Measure → Evaluate → Learn) that binds a stated assumption to a measurable metric and a deadline.",
    "On a real, if synthetic, 10,000-row dataset, risk-based targeting is justified: a high-risk cohort churns at 37.2% versus 1.5% for a low-risk cohort, and a Random Forest classifier reaches 0.84 ROC-AUC predicting that risk.",
    "The model predicts risk; it does not prove causation — human review and a controlled comparison remain required before crediting any intervention.",
    "Verdikt does not replace human judgment. It makes the assumptions behind human decisions visible, measurable, and reviewable.",
], top=Inches(1.9), size=18, space_after=14)

# =====================================================================
# SLIDE 9 — APPLICATIONS
# =====================================================================
s = add_slide()
heading(s, "APPLICATIONS")
bullet_block(s, [
    "Customer-retention decisions — discounts, win-back offers, onboarding changes for at-risk customer segments",
    "Pricing and packaging decisions — testing a price change against a stated, measurable revenue/churn forecast",
    "Feature-launch decisions — tracking whether a shipped feature met its adoption or retention target",
    "Growth and marketing experiments — binding a campaign's expected lift to an explicit, checkable number",
    "Organisation-wide decision registries — a shared log of assumptions, forecasts and outcomes for audit and institutional learning",
], top=Inches(1.9), size=19, space_after=16)

# =====================================================================
# SLIDE 10 — REFERENCES
# =====================================================================
s = add_slide()
heading(s, "REFERENCES")
refs_a = [
    "Scheibel, B. & Rinderle-Ma, S. (2023). An End-to-End Approach for Online Decision Mining and Decision Drift Analysis in Process-Aware Information Systems. CAiSE 2023 Forum (LNBIP) / arXiv:2303.03961.",
    "Goossens, A., De Smedt, J. & Vanthienen, J. (2024). Extracting Process-Aware Decision Models from Object-Centric Process Data. arXiv:2401.14847 (KU Leuven).",
    "Natarajan, S., Mathur, S., Sidheekh, S., Stammer, W. & Kersting, K. (2025). Human-in-the-loop or AI-in-the-loop? Automate or Collaborate? Proc. AAAI-25, 39(27), 28594–28600.",
    "Gruetzemacher, R., Lee, K.B. & Paradice, D. (2024). Calibration Training for Improving Probabilistic Judgments Using an Interactive App. Futures & Foresight Science, 6(2), e177.",
]
refs_b = [
    "Organisational Memory and Decision Rationale — ScienceDirect",
    "Operational Decision Discovery from Data — Springer",
    "Improving Decisions with Market Information: Corporate Prediction Markets — Cambridge / Experimental Economics",
    "Incentive-Compatible Forecasting — INFORMS / Management Science",
    "P0 — Internal Prediction Markets (priorityzero.ai)",
    "Hypermind — Crowd Forecasting (hypermind.com)",
    "Vigil — Decision Tracking Use Cases (trustvigil.com)",
    "Patent EP1402435A4 — Google Patents",
    "Patent US20250217680A1 — Google Patents",
]

tb0, tf0 = textbox(s, MARGIN, Inches(1.65), Inches(11.6), Inches(0.3))
p0 = para(tf0, new=False)
run(p0, "Literature review (last 3 years)", size=13, bold=True, color=GRAY)

tb, tf = textbox(s, MARGIN, Inches(2.0), Inches(11.8), Inches(2.1))
for i, r_ in enumerate(refs_a):
    p = para(tf, new=(i > 0), space_after=6, line_spacing=1.08)
    run(p, f"{i+1}. ", size=11.5, bold=True, color=BLACK)
    run(p, r_, size=11.5, color=BLACK)

tb2, tf2 = textbox(s, MARGIN, Inches(4.25), Inches(11.6), Inches(0.3))
p2 = para(tf2, new=False)
run(p2, "Background & prior art", size=13, bold=True, color=GRAY)

tb3, tf3 = textbox(s, MARGIN, Inches(4.6), Inches(11.8), Inches(2.6))
for i, r_ in enumerate(refs_b):
    p = para(tf3, new=(i > 0), space_after=5, line_spacing=1.05)
    run(p, f"{i+1}. ", size=10.5, bold=True, color=BLACK)
    run(p, r_, size=10.5, color=BLACK)

OUT = "/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/ca2_fill/Verdikt_CA2_Format.pptx"
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
