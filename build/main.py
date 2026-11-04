import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from theme import *
from components import *

CHARTS = "/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/charts"
TOTAL = 18
CONTENT_TOP = Inches(1.78)

prs = new_deck()

# =====================================================================
# SLIDE 1 — TITLE
# =====================================================================
s = add_slide(prs)
# faint corner accent lines
add_rect(s, Inches(-1.2), Inches(-1.2), Inches(4.0), Inches(4.0), fill=None, line=None,
          shape_type=MSO_SHAPE.OVAL)
accent = add_rect(s, SLIDE_W - Inches(5.6), SLIDE_H - Inches(5.6), Inches(9.0), Inches(9.0),
                    fill=PANEL, line=None, shape_type=MSO_SHAPE.OVAL)
accent.fill.fore_color.rgb = PANEL
add_line(s, MARGIN, Inches(0.7), Inches(0.85), Pt(3), color=AMBER)
add_text(s, MARGIN, Inches(0.84), Inches(10), Inches(0.35), "B.TECH ARTIFICIAL INTELLIGENCE & MACHINE LEARNING  ·  CA2 CAPSTONE PROJECT",
          size=12.5, color=CYAN, bold=True, char_spacing=1.4)
add_text(s, MARGIN, Inches(2.15), Inches(11.5), Inches(1.5), "Verdikt", size=58, color=WHITE, bold=True)
add_text(s, MARGIN, Inches(3.15), Inches(10.5), Inches(0.7), "Turning business decisions into measurable learning",
          size=20, color=GRAY, italic=False)

# mini flow diagram: Decision -> Assumption -> Outcome
flow_steps(s, ["Decision", "Assumption", "Forecast", "Outcome"], MARGIN, Inches(4.05), Inches(7.6), Inches(0.85),
            node_colors=[BLUE, CYAN, AMBER, CYAN], text_size=12.5)

# placeholder footer card
pc = card(s, MARGIN, Inches(6.15), Inches(12.13), Inches(0.95), fill=PANEL, line=STROKE, radius=0.1)
tf = pc.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.25)
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
runs = [
    ("Name: ", GRAY, True), ("Utsav Tyagi", WHITE, False), ("     PRN: ", GRAY, True), ("26070126233", WHITE, False),
    ("     Branch: ", GRAY, True), ("AI/ML", WHITE, False),
]
for i, (lbl, col, bold) in enumerate(runs):
    r = p.add_run(); r.text = lbl
    r.font.size = Pt(11.5); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = col
p2 = tf.add_paragraph()
p2.space_before = Pt(6)
runs2 = [
    ("Division: ", GRAY, True), ("C-3", WHITE, False), ("     Institution: ", GRAY, True), ("Symbiosis Institute of Technology, Pune", WHITE, False),
    ("     Academic Year: ", GRAY, True), ("2026-27", WHITE, False),
]
for lbl, col, bold in runs2:
    r = p2.add_run(); r.text = lbl
    r.font.size = Pt(11.5); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = col

set_notes(s, "Welcome. This project is Verdikt, a decision-to-outcome tracking platform. The core idea in one line: most"
    "teams track what happened, but almost nobody systematically records what they believed would happen before they"
    "acted, and then checks whether that belief turned out to be true. We'll walk through the problem, the workflow, the"
    "prototype built on a synthetic customer-retention dataset, the real machine-learning results from that dataset, the"
    "architecture, and an honest look at differentiation, risk, and what's next. Please fill in your name, PRN, branch,"
    "division, institution and academic year in the placeholder bar before presenting or submitting.")

# =====================================================================
# SLIDE 2 — THE PROBLEM
# =====================================================================
s = add_slide(prs)
eyebrow(s, "The Problem")
title(s, "Decisions get made. Assumptions get forgotten.")
accent_rule(s, color=AMBER)

broken_loop(s, ["Decision\nmade", "Assumption\nforgotten", "Outcome\nunclear", "Same mistake\nrepeated"],
             MARGIN, Inches(2.15), Inches(11.0), Inches(1.05))

note_card = card(s, MARGIN, Inches(4.55), Inches(11.1), Inches(1.9), fill=PANEL, line=STROKE)
tf = note_card.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.35); tf.margin_right = Inches(0.35)
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Dashboards and BI tools show what happened. Project trackers show what is scheduled. Neither one records "
r.font.size = Pt(15); r.font.name = FONT; r.font.color.rgb = WHITE
r2 = p.add_run()
r2.text = "what a team believed would happen"
r2.font.size = Pt(15); r2.font.bold = True; r2.font.name = FONT; r2.font.color.rgb = CYAN
r3 = p.add_run()
r3.text = " before they acted — so when the belief turns out to be wrong, nothing captures that it was ever tested, and the same unexamined assumption drives the next decision."
r3.font.size = Pt(15); r3.font.name = FONT; r3.font.color.rgb = WHITE

set_notes(s, "Teams make important, recurring decisions (pricing a discount, launching a feature, changing an onboarding flow)"
    "without ever writing down the measurable belief behind the decision. A dashboard will later show churn went up or"
    "down, but it won't show whether that matched what the team expected, by how much, or why. Because the original"
    "assumption was never captured in a structured, queryable way, nobody can systematically check it later, and the same"
    "flawed assumption quietly resurfaces in the next planning cycle. This is the gap Verdikt targets: not"
    "reporting on outcomes, but closing the loop between a stated belief and what actually happened.")

# =====================================================================
# SLIDE 2B — LITERATURE REVIEW (last 3 years)
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Literature Review — Last 3 Years")
title(s, "Four Recent Papers, Four Different Gaps", size=27)
accent_rule(s, color=BLUE)

lit_rows = [
    ("Scheibel & Rinderle-Ma\n(CAiSE 2023)",
     "An End-to-End Approach for\nOnline Decision Mining and\nDecision Drift Analysis",
     "Monitors decision rules at runtime, not just after the fact; detects “decision drift”; validated on 4 synthetic + 1 real-life log",
     "Tracks how an automated decision RULE changes — not whether a human's stated assumption about an outcome came true; needs existing event logs",
     "We track a human assumption vs. a measured outcome; they track automated rule drift inside a process log — adjacent problem, different object"),
    ("Goossens, De Smedt &\nVanthienen (2024, KU Leuven)",
     "Extracting Process-Aware\nDecision Models from Object-\nCentric Process Data",
     "First object-centric decision-mining algorithm (IODDA); discovers decision structure + rules directly from logs; open benchmark released",
     "Purely retrospective — reconstructs a model from data that already exists; can't recover an assumption that was never logged; no deadline/validation concept",
     "We capture the assumption BEFORE the outcome is known (forward-looking); they mine structure AFTER the fact (backward-looking) — complementary, not a substitute"),
    ("Natarajan, Mathur, Sidheekh,\nStammer & Kersting (AAAI-25)",
     "Human-in-the-loop or AI-in-\nthe-loop? Automate or\nCollaborate?",
     "Directly tackles when to automate a decision vs. keep a human in control; argues evaluation over-weights the model, under-weights the human expert",
     "A conceptual/positional framework, not a deployable system; no mechanism to record or later validate the human's stated assumption",
     "We operationalise exactly this division of labour: the model scores risk, a human approves + states the assumption, the system checks the outcome later"),
    ("Gruetzemacher, Lee &\nParadice (2024)",
     "Calibration Training for\nImproving Probabilistic\nJudgments Using an Interactive App",
     "Shows forecast calibration can be measurably improved with short, repeated feedback — supports asking for a stated confidence number",
     "Small exploratory study (153 students, a sports-forecasting tournament); trains general forecasting skill, not tied to any business decision or metric",
     "We don't train forecasting skill in the abstract — we capture a one-off, decision-specific forecast and check it against a real business metric"),
]

lcol_w = [Inches(1.95), Inches(2.1), Inches(2.3), Inches(2.3), Inches(2.5)]
lx0, ly0 = MARGIN, Inches(1.8)
lheader_h = Inches(0.4)
ldata_h = Inches(1.08)
ltbl_w = sum(lcol_w, Emu(0))
ltbl_h = lheader_h + ldata_h * len(lit_rows)
ltable = s.shapes.add_table(len(lit_rows) + 1, 5, lx0, ly0, ltbl_w, ltbl_h).table
for i, w in enumerate(lcol_w):
    ltable.columns[i].width = w
ltable.rows[0].height = lheader_h
for ri in range(1, len(lit_rows) + 1):
    ltable.rows[ri].height = ldata_h
lheaders = ["AUTHOR(S) & YEAR", "TITLE", "PROS", "CONS", "DIFFERENTIATION FROM DECISION DEBT OS"]
for c, h in enumerate(lheaders):
    cell = ltable.cell(0, c)
    cell.fill.solid(); cell.fill.fore_color.rgb = BLUE_DK
    cell.margin_left = Pt(5); cell.margin_right = Pt(5); cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = h
    r.font.size = Pt(9.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE
for ri, row in enumerate(lit_rows, start=1):
    fill = PANEL if ri % 2 == 1 else PANEL_2
    for ci, val in enumerate(row):
        cell = ltable.cell(ri, ci)
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
            r.font.size = Pt(8.5)
            r.font.name = FONT
            r.font.color.rgb = (CYAN if ci == 0 else WHITE) if ci < 2 else GRAY
            if ci == 0:
                r.font.bold = (li == 0)

add_text(s, MARGIN, Inches(6.72), Inches(12.13), Inches(0.35),
          "All four papers published 2023–2025 (peer-reviewed / top-tier preprint) — verified titles, authors and venues. See References for full citations.",
          size=9.5, italic=True, color=GRAY_DK)

set_notes(s, "Four recent, verified papers, each covering a different piece of the 'existing technology' this project sits beside."
    "Scheibel and Rinderle-Ma (CAiSE 2023) monitor automated decision rules at runtime and flag when they drift. That is"
    "close in spirit, but the object being tracked is a rule inside a process log, not a human's stated business"
    "assumption. Goossens, De Smedt and Vanthienen (2024, KU Leuven) mine decision structure from object-centric logs"
    "after the fact. That is valuable, but strictly backward-looking, so it can never recover an assumption nobody logged"
    "in the first place. Natarajan et al. (AAAI-25) argue for a clearer division between automated and human-controlled"
    "decisions, which is exactly the division Verdikt operationalises: the model scores risk, a human approves"
    "and states the assumption, the system checks the outcome later. Gruetzemacher, Lee and Paradice (2024) show forecast"
    "calibration can be trained, direct support for asking decision-makers to state a confidence number, though their"
    "intervention trains general forecasting skill in the abstract rather than tracking one specific, real business"
    "decision. Together these four papers cover runtime rule-monitoring, retrospective decision mining, human/AI decision"
    "authority, and forecast calibration, four adjacent pieces, none of which close the full assumption-to-outcome loop"
    "the way this project does.")

# =====================================================================
# SLIDE 3 — CORE INSIGHT
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Core Insight")
title(s, "A decision is not finished when it is made.")
accent_rule(s, color=CYAN)

qc = card(s, Inches(1.4), Inches(2.5), Inches(10.5), Inches(2.0), fill=PANEL_2, line=STROKE, radius=0.08)
add_rect(s, Inches(1.4), Inches(2.5), Pt(5), Inches(2.0), fill=CYAN, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
tf = qc.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.5); tf.margin_right = Inches(0.5)
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
r = p.add_run()
r.text = "“A business decision is incomplete until its original assumption is compared with the real-world outcome.”"
r.font.size = Pt(23); r.font.italic = True; r.font.name = FONT; r.font.color.rgb = WHITE

add_text(s, Inches(1.4), Inches(4.85), Inches(10.5), Inches(0.4), "This gap has a name:", size=14, color=GRAY)
dd = card(s, Inches(1.4), Inches(5.3), Inches(10.5), Inches(1.25), fill=PANEL, line=AMBER, radius=0.1)
tf = dd.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.4); tf.margin_right = Inches(0.4)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Decision Debt — "
r.font.size = Pt(19); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = AMBER
r2 = p.add_run(); r2.text = "the accumulation of decisions whose assumptions were never checked against reality."
r2.font.size = Pt(16); r2.font.name = FONT; r2.font.color.rgb = WHITE

set_notes(s, "This is the thesis of the whole project. Borrow the idea of technical debt: shortcuts in code that aren't fixed"
    "accumulate and quietly slow a team down. The same thing happens with decisions. Every decision made without a"
    "stated, checkable assumption, or whose assumption was stated but never verified, is a small piece of debt."
    "Individually each one looks harmless. It's just one discount campaign, one feature flag. Collected across a year, an"
    "organisation is running on dozens of untested beliefs it has forgotten it is relying on. Verdikt exists to"
    "make that debt visible, the same way a linter makes code debt visible.")

# =====================================================================
# SLIDE 4 — WHAT IS DECISION DEBT?
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Defining The Problem")
title(s, "What Is Decision Debt?")
accent_rule(s, color=AMBER)

defs = [
    ("Unresolved Assumptions", "A decision was made, but its underlying belief was never written down in a checkable form.", BLUE),
    ("Overdue Reviews", "A deadline for checking the outcome has passed, and no one has looked at the result.", CYAN),
    ("Invalidated Assumptions Still Driving Work", "The assumption was checked, found false, but the decision or policy it justified is still active.", AMBER),
    ("Repeated Forecasting Errors", "The same type of assumption keeps failing across different decisions, and no one notices the pattern.", RED),
]
cw, ch = Inches(5.45), Inches(2.05)
gx, gy = Inches(0.3), Inches(0.28)
for i, (h, body, col) in enumerate(defs):
    r, c = divmod(i, 2)
    x = Emu(int(MARGIN + c * (cw + gx)))
    y = Emu(int(Inches(2.2) + r * (ch + gy)))
    bx = card(s, x, y, cw, ch, fill=PANEL, line=STROKE, radius=0.1)
    add_rect(s, x, y, cw, Pt(4.5), fill=col, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
    tf = bx.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.28); tf.margin_right = Inches(0.28); tf.margin_top = Inches(0.22)
    p = tf.paragraphs[0]
    rn = p.add_run(); rn.text = h
    rn.font.size = Pt(15.5); rn.font.bold = True; rn.font.name = FONT; rn.font.color.rgb = WHITE
    p2 = tf.add_paragraph(); p2.space_before = Pt(8); p2.line_spacing = 1.15
    rn2 = p2.add_run(); rn2.text = body
    rn2.font.size = Pt(12); rn2.font.name = FONT; rn2.font.color.rgb = GRAY

set_notes(s, "Decision Debt has four recognisable forms, and this dashboard view is how the product would actually show them to a"
    "team. First, unresolved assumptions: decisions live in Slack or meeting notes with no structured, checkable belief"
    "attached. Second, overdue reviews: a review deadline passed and nobody looked. Third, and most dangerous, is"
    "invalidated assumptions still driving work. The team found out the belief was wrong, but the policy built on it is"
    "still running, costing money every day it continues. Fourth, repeated forecasting errors: the same kind of"
    "overconfident or miscalibrated forecast keeps showing up across unrelated decisions, which is a signal about the"
    "forecaster or the process, not just one bad call. None of these are visible in a normal project tracker, because"
    "none of them are about task status. They are about belief status.")

# =====================================================================
# SLIDE 5 — PROPOSED SOLUTION
# =====================================================================
s = add_slide(prs)
eyebrow(s, "The Solution")
title(s, "Capture → Structure → Forecast → Measure → Evaluate → Learn")
accent_rule(s, color=CYAN)

flow_steps(s, ["Capture", "Structure", "Forecast", "Measure", "Evaluate", "Learn"],
            MARGIN, Inches(2.15), Inches(12.13), Inches(1.05),
            node_colors=[BLUE, BLUE, CYAN, CYAN, AMBER, AMBER],
            sub=["Natural-language\ndecision note", "Fields extracted\n& validated",
                 "Confidence +\ntarget set", "Live metric\ntracked",
                 "State assigned\nat deadline", "Pattern fed back\nto next decision"],
            sub_size=9, text_size=13)

# before/after transformation
bx1 = card(s, MARGIN, Inches(4.0), Inches(5.55), Inches(2.5), fill=PANEL, line=STROKE, radius=0.1)
add_text(s, MARGIN + Inches(0.3), Inches(4.2), Inches(5.0), Inches(0.3), "UNSTRUCTURED INPUT", size=10.5, bold=True, color=GRAY, char_spacing=1.2)
tf = bx1.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.3); tf.margin_top = Inches(0.7)
p = tf.paragraphs[0]; r = p.add_run()
r.text = "“Let's offer the 10% discount to high-risk customers — I think it'll cut churn to around 18% within a month.”"
r.font.size = Pt(14); r.font.italic = True; r.font.name = FONT; r.font.color.rgb = WHITE

arr_x = Emu(int(MARGIN + Inches(5.55) + Inches(0.15)))
connector_arrow(s, arr_x, Emu(int(Inches(5.25))), Emu(int(arr_x + Inches(0.9))), Emu(int(Inches(5.25))), color=CYAN, weight=Pt(2.5))

bx2 = card(s, Emu(int(MARGIN + Inches(6.6))), Inches(4.0), Inches(5.53), Inches(2.5), fill=PANEL_2, line=CYAN, radius=0.1)
tf = bx2.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.3); tf.margin_top = Inches(0.22)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "STRUCTURED DECISION RECORD"
r.font.size = Pt(10.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = CYAN
for lbl, val in [("Intervention", "10% retention discount"), ("Target metric", "30-day churn, high-risk cohort"),
                   ("Forecast", "25% → 18%"), ("Confidence", "62%"), ("Deadline", "+30 days")]:
    field_row(tf, lbl, val, label_size=9.5, value_size=11, space_after=5)

set_notes(s, "This is the core product loop. A manager types a sentence the way they already talk, with no form-filling up front."
    "An LLM-assisted capture step extracts the structured fields: the intervention, the target metric, the forecast"
    "numbers, and a deadline. The system then asks for one more number that most teams never state out loud, a confidence"
    "level, because a forecast without a stated confidence can't later be checked for calibration. From that point the"
    "decision is a row in a database, not a sentence in a chat thread, so it can be measured, reviewed, and eventually"
    "marked validated or invalidated.")

# =====================================================================
# SLIDE 6 — EXAMPLE DECISION CONTRACT
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Worked Example")
title(s, "One Decision, Fully Specified")
accent_rule(s, color=CYAN)

qc = card(s, MARGIN, Inches(2.05), Inches(12.13), Inches(1.0), fill=PANEL_2, line=CYAN, radius=0.1)
tf = qc.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.35); tf.margin_right = Inches(0.35); tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run()
r.text = "“We believe a 10% retention discount will reduce 30-day churn among high-risk customers from 25% to 18%.”"
r.font.size = Pt(16.5); r.font.italic = True; r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE

fields = [
    ("Owner", "Retention Lead, Growth Team"), ("Confidence (forecast)", "62% self-reported probability"),
    ("Intervention", "10% discount, auto-applied at checkout"), ("Target metric", "30-day churn rate, high-risk cohort"),
    ("Deadline", "30 days from decision date"), ("Estimated cost", "~$4.80 / customer (10% of avg. order)"),
    ("Kill condition", "If interim churn > 25% at day 15, stop offer"), ("Actual result", "Pending — 30-day window not yet elapsed"),
]
cw2, ch2 = Inches(2.95), Inches(1.75)
gx2 = Inches(0.1)
for i, (lbl, val) in enumerate(fields):
    r_, c_ = divmod(i, 4)
    x = Emu(int(MARGIN + c_ * (cw2 + gx2)))
    y = Emu(int(Inches(3.3) + r_ * (ch2 + Inches(0.15))))
    bx = card(s, x, y, cw2, ch2, fill=PANEL, line=STROKE, radius=0.1)
    tf = bx.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2); tf.margin_right = Inches(0.18); tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    rn = p.add_run(); rn.text = lbl.upper()
    rn.font.size = Pt(10); rn.font.bold = True; rn.font.name = FONT; rn.font.color.rgb = (AMBER if lbl=="Actual result" else CYAN)
    p2 = tf.add_paragraph(); p2.space_before = Pt(6); p2.line_spacing = 1.1
    rn2 = p2.add_run(); rn2.text = val
    rn2.font.size = Pt(12.5); rn2.font.name = FONT; rn2.font.color.rgb = WHITE

add_text(s, MARGIN, Inches(6.78), Inches(12.1), Inches(0.3),
          "Baseline shown here (25%) is one risk-tier definition; the dataset's observed high-risk cohort baseline is 37% — see Slide 7.",
          size=9.5, color=GRAY_DK, italic=True)

set_notes(s, "This is what one row in the decision database actually looks like: every field a human filled in or confirmed before"
    "the decision went live. Note the 'kill condition': an explicit rule for when the team would abandon the intervention"
    "early, which most decisions never specify. And note 'Actual result' is honestly marked pending. In a live deployment"
    "this field only populates once the deadline passes and the metric pipeline has enough data; for this capstone demo"
    "it is the dataset's synthetic timestamp horizon that limits a fully closed example, which we show in the evaluation-"
    "engine slide instead using a simulated batch of decisions.")

# =====================================================================
# SLIDE 7 — DATASET AND DATA PIPELINE
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Dataset & Pipeline — Synthetic, For Demonstration Only")
title(s, "From Customer Record to Decision Evaluation")
accent_rule(s, color=BLUE)

flow_steps(s, ["Customer\nprofile", "Churn-risk\nprediction", "Retention\ndecision",
               "Treatment /\ncontrol group", "30-day\noutcome", "Decision\nevaluation"],
            MARGIN, Inches(2.1), Inches(12.13), Inches(0.95),
            node_colors=[BLUE, BLUE, CYAN, CYAN, AMBER, AMBER], text_size=12)

dsc = card(s, MARGIN, Inches(3.45), Inches(6.0), Inches(3.3), fill=PANEL, line=STROKE, radius=0.1)
tf = dsc.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.25); tf.margin_top = Inches(0.25)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "SYNTHETIC CUSTOMER-RETENTION DATASET"
r.font.size = Pt(11.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = CYAN
for lbl, val in [
    ("Records", "10,000 fictional customer rows"),
    ("Fields", "age, gender, country, income, spending score, purchases, avg. order value, membership years, site visits/mo, cart-abandon rate, churn flag, feedback text, last purchase date"),
    ("Status", "Clearly labelled synthetic data — used for demonstration only; not a real company's data"),
]:
    field_row(tf, lbl, val, label_size=9.5, value_size=11, space_after=8)

add_text(s, Emu(int(MARGIN + Inches(6.35))), Inches(3.45), Inches(5.78), Inches(0.35),
          "Real, observed churn rate by risk segment", size=12, bold=True, color=WHITE)
s.shapes.add_picture(f"{CHARTS}/churn_by_segment.png", Emu(int(MARGIN + Inches(6.55))), Inches(3.85),
                       width=Inches(5.05))

set_notes(s, "This is the one dataset used across the whole prototype, and it is explicitly synthetic and fictional, generated for"
    "demonstration, with no link to any real company or real customers. The pipeline shows how a raw customer row becomes"
    "a decision record: a churn-risk score is computed per customer, a retention decision is attached to the highest-risk"
    "customers, those customers are conceptually split into a treated group and a held-out comparison group, a 30-day"
    "outcome window is observed, and the decision-evaluation engine assigns a validation state. The chart on the right is"
    "real, not illustrative: computed directly from the uploaded dataset. Customers matching a high-risk profile (cart-"
    "abandonment at or above 70% and a spending score at or below 25) actually churn at 37.2% within this dataset,"
    "against 1.5% for a clearly low-risk profile and 10.9% overall. That gap is what makes risk-based targeting worth"
    "doing in the first place.")

# =====================================================================
# SLIDE 7B — DATASET PREVIEW (real rows + signed correlations)
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Dataset Preview")
title(s, "What the Raw Rows Actually Look Like")
accent_rule(s, color=BLUE)

LCOL_W = Inches(5.85)
RCOL_X = Emu(int(MARGIN + LCOL_W + Inches(0.43)))
RCOL_W = Inches(5.85)

add_text(s, MARGIN, Inches(1.95), LCOL_W, Inches(0.55),
          "First 8 rows of Customer_Transactions.csv\n(8 of 14 columns shown)", size=12, bold=True, color=WHITE, line_spacing=1.15)
ds_h = Emu(int(LCOL_W * 726 / 2026))
s.shapes.add_picture(f"{CHARTS}/dataset_preview.png", MARGIN, Inches(2.55), width=LCOL_W)

stats = card(s, MARGIN, Emu(int(Inches(2.55) + ds_h + Inches(0.3))), LCOL_W, Inches(1.65), fill=PANEL_2, line=STROKE, radius=0.12)
tf = stats.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.28); tf.margin_right = Inches(0.28)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "10,000 rows × 14 columns"
r.font.size = Pt(13); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = CYAN
p2 = tf.add_paragraph(); p2.space_before = Pt(6); p2.line_spacing = 1.2
r2 = p2.add_run(); r2.text = "Clearly labelled synthetic / fictional data, generated for this project — not drawn from any real company's customers. No column was dropped or reshaped for this preview; these are the literal supplied values."
r2.font.size = Pt(11); r2.font.name = FONT; r2.font.color.rgb = GRAY

add_text(s, RCOL_X, Inches(1.95), RCOL_W, Inches(0.55),
          "Which features actually move churn\n(real, signed correlations)", size=12, bold=True, color=WHITE, line_spacing=1.15)
CORR_W = Inches(4.85)
corr_h = Emu(int(CORR_W * 4.0 / 7.4))
s.shapes.add_picture(f"{CHARTS}/correlation_chart.png", RCOL_X, Inches(2.55), width=CORR_W)

note = card(s, RCOL_X, Emu(int(Inches(2.55) + corr_h + Inches(0.22))), RCOL_W, Inches(1.35), fill=PANEL_2, line=STROKE, radius=0.12)
tf = note.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.28); tf.margin_right = Inches(0.28)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Cart-abandon rate is the only feature that "
r.font.size = Pt(12); r.font.name = FONT; r.font.color.rgb = WHITE
r2 = p.add_run(); r2.text = "increases"
r2.font.size = Pt(12); r2.font.bold = True; r2.font.name = FONT; r2.font.color.rgb = RED
r3 = p.add_run(); r3.text = " churn risk among these eight — everything else (spending, purchase frequency, tenure) is protective. This matches the model's own feature-importance ranking one slide over."
r3.font.size = Pt(12); r3.font.name = FONT; r3.font.color.rgb = WHITE

set_notes(s, "Two real views of the same raw data. On top, the first eight rows of the actual CSV exactly as supplied. Nothing was"
    "synthesized for the slide, this is what training data for this project literally looks like, row by row. Below,"
    "correlation coefficients between each numeric feature and the churn flag, computed directly on the full 10,000-row"
    "dataset. Note this is correlation, not the model's feature importance. They're computed differently, but they agree"
    "here: spending score and purchase count are the strongest protective signals, cart-abandon rate is the strongest"
    "risk signal, and age and income barely matter. That agreement between two independent statistical views is a small"
    "but real piece of evidence that the model learned something real in the data, not noise.")

# =====================================================================
# SLIDE 8 — MACHINE LEARNING COMPONENT
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Machine Learning Component")
title(s, "Predicting Risk, Not Proving Causation")
accent_rule(s, color=BLUE)

lc = card(s, MARGIN, Inches(2.05), Inches(4.45), Inches(4.35), fill=PANEL, line=STROKE, radius=0.08)
tf = lc.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
tf.margin_left = Inches(0.26); tf.margin_right = Inches(0.22); tf.margin_top = Inches(0.24)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "HOW IT'S BUILT"
r.font.size = Pt(11); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = CYAN
ml_rows = [
    ("Task", "Binary classification — churned vs. retained"),
    ("Features", "Spending score, cart-abandon rate, site visits/mo, purchases, avg. order value, membership years, income, age, gender, country"),
    ("Preprocessing", "Standardization (numeric) + one-hot encoding (categorical)"),
    ("Split", "80 / 20 train-test, stratified by class"),
    ("Models compared", "Logistic Regression vs. Random Forest (300 trees)"),
]
for lbl, val in ml_rows:
    field_row(tf, lbl, val, label_size=9.5, value_size=11, space_after=9)

RX = Emu(int(MARGIN + Inches(4.75)))
RW = Inches(7.38)
tiles = [("0.28", "Precision"), ("0.67", "Recall"), ("0.40", "F1-score"), ("0.84", "ROC-AUC")]
tcols = [RED, CYAN, BLUE, AMBER]
tw = Inches(1.77); tgap = Inches(0.1)
for i, (val, lbl) in enumerate(tiles):
    x = Emu(int(RX + i * (tw + tgap)))
    metric_tile(s, x, Inches(2.05), tw, Inches(1.05), val, lbl, accent=tcols[i], value_size=26, label_size=10)
add_text(s, RX, Inches(3.2), RW, Inches(0.3), "Random Forest · held-out test set · n = 2,000 (live, reproducible — same numbers the running Verdikt prototype shows)",
          size=9.5, color=GRAY_DK, italic=True)

add_text(s, RX, Inches(3.58), Inches(4.7), Inches(0.3), "Top churn-risk drivers", size=12, bold=True, color=WHITE)
s.shapes.add_picture(f"{CHARTS}/feature_importance.png", RX, Inches(3.88), width=Inches(4.6))

cmx = Emu(int(RX + Inches(4.85)))
add_text(s, cmx, Inches(3.58), Inches(2.5), Inches(0.3), "Confusion matrix", size=12, bold=True, color=WHITE)
s.shapes.add_picture(f"{CHARTS}/confusion_matrix.png", cmx, Inches(3.88), width=Inches(2.5))

cb = card(s, MARGIN, Inches(6.58), Inches(12.13), Inches(0.38), fill=PANEL_2, line=AMBER, radius=0.18)
tf = cb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.3); tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = "A model that flags churn risk does not prove an intervention caused a customer to stay — prediction identifies candidates for a decision; it does not validate the decision's outcome."
r.font.size = Pt(10.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE

set_notes(s, "These are the real, calculated numbers from training on the uploaded dataset. Nothing here is a placeholder, and"
    "these are the exact numbers the live Verdikt prototype shows too, since both run the identical training script."
    "Churn is imbalanced at 10.9%, so we used class-weighted models and optimised for recall over precision: catching"
    "true churners matters more than being right every time we flag someone, because the cost of a missed at-risk"
    "customer is higher than the cost of one unnecessary discount. Random Forest reaches 0.67 recall and 0.84 ROC-AUC at"
    "0.28 precision. The confusion matrix on the left shows exactly where those errors land: a sizeable false-positive"
    "count, which is expected and acceptable because this score feeds a human-reviewed decision, never an automatic"
    "action. Spending score and cart-abandon rate dominate feature importance, matching the raw correlations in the data"
    "shown on the previous slide. The callout at the bottom is the single most important caveat in the whole deck: this"
    "model ranks risk, it does not and cannot show that any specific retention action caused a customer to stay. That"
    "requires a controlled comparison, which is what the evaluation engine is for.")

# =====================================================================
# SLIDE 9 — SYSTEM ARCHITECTURE
# =====================================================================
s = add_slide(prs)
eyebrow(s, "System Architecture")
title(s, "Seven Layers, One Feedback Loop")
accent_rule(s, color=CYAN)

layers = [
    ("User Interface", "Where a manager types a decision in plain language", BLUE),
    ("Decision Capture Layer", "Parses the note into a draft structured record", BLUE),
    ("Assumption & Metric Layer", "Binds the decision to one measurable target metric", CYAN),
    ("ML Risk-Prediction Layer", "Scores churn risk to prioritise which customers/decisions matter", CYAN),
    ("Data Integration Layer", "Pulls in product, billing and CRM data to track the metric live", CYAN),
    ("Outcome Evaluation Engine", "Checks deadline, sample size and target at review time", AMBER),
    ("Decision Debt Dashboard", "Shows every decision's state — and what's overdue or invalidated", AMBER),
]
bw, bh, bgap = Inches(4.2), Inches(0.5), Inches(0.135)
bx0 = MARGIN
by0 = Inches(2.05)
for i, (name, desc, col) in enumerate(layers):
    y = Emu(int(by0 + i * (bh + bgap)))
    box = card(s, bx0, y, bw, bh, fill=PANEL_2, line=STROKE, radius=0.18)
    add_rect(s, bx0, y, Pt(4.5), bh, fill=col, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
    tf = box.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.22)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = name
    r.font.size = Pt(12.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE
    add_text(s, Emu(int(bx0 + bw + Inches(0.3))), y, Inches(6.7), bh, desc, size=11, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(layers) - 1:
        cx = Emu(int(bx0 + bw / 2))
        connector_arrow(s, cx, Emu(int(y + bh)), cx, Emu(int(y + bh + bgap)), color=GRAY, weight=Pt(1.75))

stackrow_y = Inches(6.65)
pills_list = ["Python", "FastAPI", "SQLAlchemy", "Scikit-learn", "React + TypeScript"]
pw_list = [Inches(1.3), Inches(1.5), Inches(1.75), Inches(1.95), Inches(2.5)]
pgap = Inches(0.14)
add_text(s, MARGIN, Inches(6.38), Inches(3), Inches(0.25), "BUILT WITH (REAL, RUNNING PROTOTYPE)", size=9.5, bold=True, color=GRAY_DK, char_spacing=1.0)
_px = MARGIN
for name, pw in zip(pills_list, pw_list):
    pill(s, _px, stackrow_y, pw, Inches(0.42), name, size=11, bold=True)
    _px = Emu(int(_px + pw + pgap))

set_notes(s, "Seven layers, each with one job, connected top to bottom in one direction except for the feedback that flows back"
    "from the dashboard into future decisions. The UI captures intent in natural language; the capture layer turns it"
    "into a draft record; the assumption-and-metric layer forces a single, bound target metric rather than vague success"
    "criteria; the ML layer scores risk to help prioritise which customers or segments a decision applies to; the data-"
    "integration layer pulls in the live numbers needed to actually measure the metric over time from product, billing or"
    "CRM systems; the evaluation engine runs the four checks at review time; and the dashboard is where a team sees every"
    "open, overdue, or invalidated decision at a glance. This is not a hypothetical stack. It's what the actual working"
    "Verdikt prototype is built on, shown running on the next slide: FastAPI and SQLAlchemy for the backend and data"
    "layer, Scikit-learn for the risk model, React and TypeScript for the dashboard UI. Boring, well-understood"
    "technology on purpose. The value is in the workflow, not the tooling.")

# =====================================================================
# SLIDE 9B — WORKING PROTOTYPE (real screenshots)
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Working Prototype — Verdikt")
title(s, "Not a Mockup. A Running Application.", size=28)
accent_rule(s, color=CYAN)

SHOTS = f"{CHARTS}/screenshots"
shot_w = Inches(3.92)
shot_gap = Inches(0.2)
shot_top = Inches(2.05)
shot_items = [
    ("verdikt_dashboard.png", "Decision Dashboard", "7 seeded decisions, every validation state represented"),
    ("verdikt_capture.png", "Capture — Live Risk Preview", "Real segment scoring as the form is filled in"),
    ("verdikt_evaluated.png", "Decision Detail — Evaluated", "Real p-value, real state: Invalidated"),
]
pic_w = shot_w - Inches(0.16)
pic_h = Emu(int(pic_w * 1800 / 2880))
frame_h = Emu(int(pic_h + Inches(0.16)))
for i, (fname, cap, sub) in enumerate(shot_items):
    x = Emu(int(MARGIN + i * (shot_w + shot_gap)))
    frame = card(s, x, shot_top, shot_w, frame_h, fill=PANEL, line=CYAN, radius=0.05)
    s.shapes.add_picture(f"{SHOTS}/{fname}", Emu(int(x + Inches(0.08))), Emu(int(shot_top + Inches(0.08))), width=pic_w)
    cap_y = Emu(int(shot_top + frame_h + Inches(0.14)))
    add_text(s, x, cap_y, shot_w, Inches(0.28), cap, size=12.5, bold=True, color=WHITE)
    add_text(s, x, Emu(int(cap_y + Inches(0.3))), shot_w, Inches(0.55), sub, size=10, color=GRAY, wrap=True)

cb2 = card(s, MARGIN, Inches(6.55), Inches(12.13), Inches(0.42), fill=PANEL_2, line=STROKE, radius=0.18)
tf = cb2.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.3); tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = "All three screens captured from the actual running app (FastAPI backend + React frontend, real SQLite data) — not a design mockup."
r.font.size = Pt(10.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE

set_notes(s, "This is the single strongest piece of evidence in the whole deck: three real screenshots, captured from the actual"
    "running Verdikt prototype with a headless browser, not designed in Figma. Left: the dashboard loaded with seven"
    "seeded decisions, one for each of the six validation states plus a pending example, with color-coded status badges,"
    "filterable by state. Middle: the Capture screen mid-use, with the live risk-preview panel on the right actually"
    "calling the trained model as the form's segment filters change. That 68.3% mean churn risk and 724-customer segment"
    "size are real numbers from a real API call, not hardcoded. Right: a newly created decision after clicking 'fast-"
    "forward and evaluate'. The evaluation engine computed a real p-value of 0.0000 and assigned Invalidated, visibly"
    "labelled as a demo fast-forward rather than a real elapsed deadline. If asked in a viva: yes, this can be run live,"
    "right now, with two terminal commands documented in the project's README.")

# =====================================================================
# SLIDE 10 — DECISION EVALUATION
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Decision Evaluation Engine")
title(s, "Four Checks, Six Possible States")
accent_rule(s, color=AMBER)

checks = [
    "Was the target metric reached?",
    "Has the review deadline passed?",
    "Was the sample size large enough to trust the result?",
    "Is the result statistically conclusive, or still noisy?",
]
ccol = [CYAN, BLUE, AMBER, RED]
cw3, ch3 = Inches(5.5), Inches(0.82)
for i, q in enumerate(checks):
    y = Emu(int(Inches(2.1) + i * (ch3 + Inches(0.18))))
    bx = card(s, MARGIN, y, cw3, ch3, fill=PANEL, line=STROKE, radius=0.16)
    dot(s, Emu(int(MARGIN + Inches(0.24))), Emu(int(y + ch3/2 - Inches(0.08))), Inches(0.16), ccol[i])
    add_text(s, Emu(int(MARGIN + Inches(0.55))), y, Inches(4.75), ch3, q, size=13, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, wrap=True)

RX2 = Emu(int(MARGIN + cw3 + Inches(0.4)))
add_text(s, RX2, Inches(2.1), Inches(6.2), Inches(0.3), "Illustrative state mix — simulated for demonstration", size=11.5, bold=True, color=WHITE)
s.shapes.add_picture(f"{CHARTS}/decision_states_donut.png", RX2, Inches(2.42), width=Inches(5.95))

note = card(s, MARGIN, Inches(6.35), Inches(12.13), Inches(0.68), fill=PANEL_2, line=STROKE, radius=0.14)
tf = note.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.3); tf.margin_right = Inches(0.3)
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Validated / Invalidated = target clearly met or missed, with enough data. Partially Validated = directionally right, underpowered. Inconclusive = evidence too weak either way. Stale = deadline passed, never reviewed. Not Measurable = metric or data unavailable."
r.font.size = Pt(10.5); r.font.name = FONT; r.font.color.rgb = GRAY

set_notes(s, "The evaluation engine is rule-based, not another model. It runs four checks against each decision record at or after"
    "its deadline and assigns one of six states. This keeps the logic auditable: anyone can see exactly why a decision"
    "was marked Validated versus Inconclusive. The pie chart here is explicitly illustrative: a simulated mix of outcome"
    "states across a batch of synthetic decisions, built to demonstrate what the dashboard would show. It is not a"
    "measured result from real deployments, and the deck is careful to label it that way rather than imply it's"
    "empirical. The six states matter because the real failure mode this project targets is 'Stale' and 'Invalidated-but-"
    "still-active' decisions, the ones nobody goes back to check.")

# =====================================================================
# SLIDE 11 — DIFFERENTIATION AND COMPETITION
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Differentiation & Prior Art")
title(s, "Honest Positioning: The Pieces Exist. The Workflow Is New.", size=25)
accent_rule(s, color=BLUE)

cols = ["Captures\ndecisions", "Explicit\nassumption", "Forecasts\noutcome", "Closes loop w/\nmeasured outcome", "Built for product\n& retention teams"]
rows = [
    ("BI dashboards\n(Looker, Tableau, Power BI)", ["no","no","no","no","no"]),
    ("Jira / Linear / Notion", ["partial","no","no","no","partial"]),
    ("Corporate prediction markets\n(P0, Hypermind)", ["no","partial","yes","partial","no"]),
    ("Investment decision trackers", ["yes","partial","partial","partial","no"]),
    ("Enterprise decision intelligence\n(Vigil, org-memory patents)", ["yes","yes","partial","partial","no"]),
    ("Prediction/outcome journals\n(RationalGo, Reckon, Condelo)", ["yes","partial","yes","partial","no"]),
    ("Verdikt (this project)", ["yes","yes","yes","yes","yes"]),
]
label_w = Inches(3.15)
metric_w = Inches(1.78)
tx0 = MARGIN
ty0 = Inches(1.92)
rh = Inches(0.42)
# header
add_text(s, tx0, ty0, label_w, rh, "", size=1)
for i, c in enumerate(cols):
    x = Emu(int(tx0 + label_w + i * metric_w))
    add_text(s, x, ty0, metric_w, rh, c, size=9, bold=True, color=GRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, line_spacing=1.0)
for ri, (label, vals) in enumerate(rows):
    y = Emu(int(ty0 + Inches(0.55) + ri * rh))
    highlight = (ri == len(rows) - 1)
    rowfill = PANEL_2 if highlight else (PANEL if ri % 2 == 0 else NAVY)
    rowline = CYAN if highlight else None
    add_rect(s, tx0, y, label_w + metric_w * 5, rh, fill=rowfill, line=rowline, line_w=Pt(1.25), radius=0, shape_type=MSO_SHAPE.RECTANGLE)
    add_text(s, Emu(int(tx0 + Inches(0.15))), y, label_w - Inches(0.15), rh, label, size=10.5,
              bold=highlight, color=(CYAN if highlight else WHITE), anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.95)
    for ci, v in enumerate(vals):
        x = Emu(int(tx0 + label_w + ci * metric_w))
        checkmark(s, Emu(int(x + metric_w/2 - Inches(0.1))), Emu(int(y + rh/2 - Inches(0.1))), Inches(0.2), kind=v)

NOV_Y = Inches(5.58)
add_text(s, MARGIN, NOV_Y, Inches(2.6), Inches(0.28), "NOVELTY, SCORED HONESTLY", size=10, bold=True, color=GRAY, char_spacing=1.0)
nov_tiles = [("3/10", "Algorithmic & technical novelty"), ("8/10", "Workflow & combination novelty")]
nov_cols = [RED, CYAN]
ntw = Inches(2.85); ntgap = Inches(0.2)
for i, (val, lbl) in enumerate(nov_tiles):
    x = Emu(int(MARGIN + i * (ntw + ntgap)))
    metric_tile(s, x, Emu(int(NOV_Y + Inches(0.3))), ntw, Inches(0.72), val, lbl, accent=nov_cols[i], value_size=20, label_size=9)

stmt = card(s, Emu(int(MARGIN + 2*(ntw+ntgap))), Emu(int(NOV_Y + Inches(0.3))), Emu(int(Inches(12.13) - 2*(ntw+ntgap))), Inches(0.72), fill=PANEL_2, line=AMBER, radius=0.14)
tf = stmt.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Not a new machine-learning technique. "
r.font.size = Pt(11); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = AMBER
r2 = p.add_run(); r2.text = "The real argument is the workflow combination, and even that is close to at least three small existing tools."
r2.font.size = Pt(11); r2.font.name = FONT; r2.font.color.rgb = WHITE

set_notes(s, "Every individual capability in this table already exists somewhere. BI dashboards report outcomes. Jira, Linear and Notion "
    "capture decisions as tickets or docs but never bind them to a measurable forecast. Corporate prediction markets like P0 and "
    "Hypermind are excellent at forecasting a specific question but aren't built around a company's own decision log. Investment "
    "decision trackers and patents around organisational memory (EP1402435A4) and decision lifecycle management "
    "(US20250217680A1) capture decisions and sometimes rationale, but are generally heavyweight, enterprise-wide systems, not "
    "something a five-person growth team adopts in an afternoon. A deeper search also found prediction-and-outcome journals "
    "(RationalGo, Reckon, Condelo) that already combine a stated forecast, a confidence level, and a later outcome check, which is "
    "closer to this project's core loop than anything in the original literature review. The honest novelty score reflects that: "
    "3 out of 10 on the machine-learning and statistics, which are textbook methods, and 8 out of 10 on the specific workflow "
    "combination, which has not been found bundled together with a published six-state evaluation engine and a working prototype. "
    "The claim on this slide is deliberately narrow and should be defended that way, not inflated.")

# =====================================================================
# SLIDE 12 — TARGET CUSTOMER & BUSINESS MODEL
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Target Customer & Business Model")
title(s, "B2B SaaS, 20–150 Employees, Active Growth Teams")
accent_rule(s, color=CYAN)

bm = [
    ("Buyer", "VP Product or Head of Growth / Retention at a venture-backed B2B SaaS company", BLUE),
    ("Initial use case", "Churn-intervention decisions — discounts, win-back campaigns, onboarding changes", CYAN),
    ("Pilot price", "$499 / month per workspace", AMBER),
    ("Expansion path", "Retention decisions → pricing & packaging → feature launches → org-wide decision registry", BLUE),
    ("Business model", "B2B SaaS subscription, per-workspace, usage-based tiers above the pilot", CYAN),
]
cw4, ch4 = Inches(5.75), Inches(1.38)
gx4, gy4 = Inches(0.4), Inches(0.22)
ch4_last = Inches(1.62)
for i, (h, body, col) in enumerate(bm):
    r_, c_ = divmod(i, 2)
    x = Emu(int(MARGIN + c_ * (cw4 + gx4)))
    y = Emu(int(Inches(2.05) + r_ * (ch4 + gy4)))
    if i == 4:
        x = Emu(int(MARGIN))
        y = Emu(int(Inches(2.05) + 2 * (ch4 + gy4)))
        cw_use, ch_use = Inches(11.9), ch4_last
    else:
        cw_use, ch_use = cw4, ch4
    bx = card(s, x, y, cw_use, ch_use, fill=PANEL, line=STROKE, radius=0.1)
    add_rect(s, x, y, Pt(4.5), ch_use, fill=col, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
    tf = bx.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.28); tf.margin_right = Inches(0.28); tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    rn = p.add_run(); rn.text = h.upper()
    rn.font.size = Pt(10.5); rn.font.bold = True; rn.font.name = FONT; rn.font.color.rgb = col
    p2 = tf.add_paragraph(); p2.space_before = Pt(5); p2.line_spacing = 1.15
    rn2 = p2.add_run(); rn2.text = body
    rn2.font.size = Pt(13.5); rn2.font.name = FONT; rn2.font.color.rgb = WHITE
    if i == 4:
        p3 = tf.add_paragraph(); p3.space_before = Pt(7)
        rn3 = p3.add_run(); rn3.text = "Business hypothesis — not yet validated with paying customers or signed pilots."
        rn3.font.size = Pt(10.5); rn3.font.italic = True; rn3.font.name = FONT; rn3.font.color.rgb = AMBER

set_notes(s, "This is deliberately a hypothesis slide, not a validated market finding. The target buyer is a VP Product or Head of"
    "Growth/Retention inside a mid-sized SaaS company, large enough to have a dedicated retention motion and real"
    "decision volume, and small enough that a five-hundred-dollar-a-month tool is an easy yes without procurement"
    "friction. The initial wedge is narrow on purpose: churn-intervention decisions, because that's exactly what the"
    "prototype and dataset demonstrate. Expansion into pricing, feature-launch, and eventually an org-wide decision"
    "registry only makes sense after the narrow wedge proves the workflow is worth adopting. No pilot customers, signed"
    "contracts, or market-sizing research back this slide yet. That is the next validation step, not a claim already"
    "proven.")

# =====================================================================
# SLIDE 13 — RISKS AND LIMITATIONS
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Risks & Limitations")
title(s, "What Could Go Wrong — And the Mitigation", size=27)
accent_rule(s, color=RED)

add_text(s, MARGIN, Inches(1.98), Inches(5.6), Inches(0.25), "RISK", size=9.5, bold=True, color=GRAY_DK, char_spacing=1.4)
add_text(s, Emu(int(MARGIN + Inches(6.1))), Inches(1.98), Inches(6.0), Inches(0.25), "MITIGATION", size=9.5, bold=True, color=GRAY_DK, char_spacing=1.4)

risks = [
    ("Synthetic data cannot prove real-world value", "Pilot with design-partner companies' real (anonymised) data before any efficacy claim.", "red"),
    ("No guaranteed causal inference from churn prediction", "Treat scores as risk triage only; require a held-out comparison group before crediting any intervention.", "red"),
    ("Metric-binding errors — wrong metric tied to a decision", "Shared metric ontology plus reviewer sign-off before a decision record goes live.", "amber"),
    ("Poor data quality / integration gaps", "Data-quality checks at ingestion; low-confidence source feeds are flagged, not trusted silently.", "amber"),
    ("Forecast manipulation — gaming confidence scores", "Track forecaster calibration over time so gaming becomes visible, not just the raw score.", "amber"),
    ("Privacy — customer PII inside decision records", "Field-level encryption, role-based access, minimal PII in ML features.", "red"),
    ("False alerts / alert fatigue from risk scoring", "Tunable thresholds and a batched digest instead of per-customer pings.", "amber"),
    ("User resistance / adoption friction", "Natural-language capture to avoid new process overhead; start with one team, not the whole org.", "amber"),
    ("Prior-art & patent overlap (e.g., EP1402435A4, US20250217680A1)", "Freedom-to-operate review before commercial launch; keep claims to the workflow, not the method.", "red"),
]
ry0 = Inches(2.3)
rrh = Inches(0.465)
for i, (risk, mit, lvl) in enumerate(risks):
    y = Emu(int(ry0 + i * rrh))
    risk_dot_row(s, MARGIN, y, Inches(12.0), risk, mit, level=lvl, risk_w=Inches(5.3))

set_notes(s, "Nine concrete risks, each with a specific mitigation rather than a vague reassurance. The two most severe, marked in"
    "red, are foundational: the dataset is synthetic so it cannot by itself prove real-world value, and churn prediction"
    "cannot by itself prove causation. Both are addressed by requiring real pilot data and controlled comparisons before"
    "any efficacy claim is made externally. Privacy is flagged red because decision records can contain customer PII by"
    "nature of referencing specific customers, so field-level encryption and role-based access are non-negotiable before"
    "any production use. Prior-art overlap is also flagged red and deliberately tied to the two patents cited earlier. A"
    "freedom-to-operate legal review is listed as a precondition for commercial launch, not an afterthought.")

# =====================================================================
# SLIDE 14 — CONCLUSION AND ROADMAP
# =====================================================================
s = add_slide(prs)
eyebrow(s, "Conclusion & Roadmap")
title(s, "Verdikt Doesn't Replace Judgment. It Makes It Checkable.", size=25)
accent_rule(s, color=CYAN)

qc = card(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(1.35), fill=PANEL_2, line=STROKE, radius=0.1)
add_rect(s, Inches(0.9), Inches(2.0), Pt(5), Inches(1.35), fill=CYAN, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
tf = qc.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.4); tf.margin_right = Inches(0.4)
p = tf.paragraphs[0]
r = p.add_run()
r.text = "“Verdikt does not replace human judgment. It makes the assumptions behind human decisions visible, measurable and reviewable.”"
r.font.size = Pt(17); r.font.italic = True; r.font.name = FONT; r.font.color.rgb = WHITE

add_text(s, MARGIN, Inches(3.75), Inches(5), Inches(0.3), "ROADMAP", size=11, bold=True, color=GRAY, char_spacing=1.4)
flow_steps(s, ["CSV\nPrototype", "PostHog /\nSlack Integration", "Calibration\nAnalytics", "Metric\nOntology", "Enterprise\nGovernance"],
            MARGIN, Inches(4.1), Inches(12.13), Inches(1.0),
            node_colors=[CYAN, BLUE, BLUE, AMBER, AMBER], text_size=12.5)

cb = card(s, Inches(0.9), Inches(5.65), Inches(11.5), Inches(1.15), fill=PANEL, line=AMBER, radius=0.12)
tf = cb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
tf.margin_left = Inches(0.4); tf.margin_right = Inches(0.4)
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "“The goal is not to automate responsibility. The goal is to prevent important decisions from disappearing into memory.”"
r.font.size = Pt(16); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = AMBER

set_notes(s, "To close: this project does not claim to make decisions for anyone, and it does not claim to prove that any one"
    "intervention works. What it claims, modestly, is that making an assumption explicit and checking it later is better"
    "than letting it quietly disappear. The roadmap moves in deliberate stages, from this CSV-based prototype, to live"
    "integrations with tools teams already use like PostHog and Slack, to calibration analytics that track whether"
    "specific forecasters or teams are over- or under-confident over time, to a shared metric ontology that prevents"
    "metric-binding errors, and eventually to governance features for larger organisations. Every stage after the"
    "prototype requires real usage data to build responsibly, which is why none of it is overpromised here. Thank you."
    "Happy to take questions.")

# =====================================================================
# SLIDE 15 — REFERENCES
# =====================================================================
s = add_slide(prs)
eyebrow(s, "References")
title(s, "Related Work & Sources", size=28)
accent_rule(s, color=GRAY)

add_text(s, MARGIN, Inches(1.78), Inches(10), Inches(0.3), "LITERATURE REVIEW — LAST 3 YEARS", size=11.5, bold=True, color=CYAN, char_spacing=1.1)

lit_refs = [
    ("Scheibel, B. & Rinderle-Ma, S. (2023). An End-to-End Approach for Online Decision Mining and Decision Drift Analysis in Process-Aware Information Systems.", "CAiSE 2023 Forum / arXiv:2303.03961"),
    ("Goossens, A., De Smedt, J. & Vanthienen, J. (2024). Extracting Process-Aware Decision Models from Object-Centric Process Data.", "arXiv:2401.14847 (KU Leuven)"),
    ("Natarajan, S., Mathur, S., Sidheekh, S., Stammer, W. & Kersting, K. (2025). Human-in-the-loop or AI-in-the-loop? Automate or Collaborate?", "Proc. AAAI-25, 39(27), 28594–28600"),
    ("Gruetzemacher, R., Lee, K.B. & Paradice, D. (2024). Calibration Training for Improving Probabilistic Judgments Using an Interactive App.", "Futures & Foresight Science, 6(2), e177"),
]
ly = Inches(2.14)
lrh = Inches(0.52)
for i, (t, src) in enumerate(lit_refs):
    y = Emu(int(ly + i * lrh))
    add_text(s, MARGIN, y, Inches(0.35), Inches(0.3), f"{i+1}.", size=10.5, bold=True, color=GRAY_DK)
    tb, tf = add_multirun_textbox(s, Emu(int(MARGIN + Inches(0.35))), y, Inches(11.6), lrh, wrap=True)
    p = tf.paragraphs[0]; p.line_spacing = 1.02
    r = p.add_run(); r.text = t
    r.font.size = Pt(10); r.font.name = FONT; r.font.color.rgb = WHITE
    r2 = p.add_run(); r2.text = "  " + src
    r2.font.size = Pt(10); r2.font.italic = True; r2.font.name = FONT; r2.font.color.rgb = CYAN

by = Inches(4.35)
add_text(s, MARGIN, by, Inches(10), Inches(0.3), "BACKGROUND & PRIOR ART", size=11.5, bold=True, color=GRAY, char_spacing=1.1)

refs = [
    ("Organisational Memory and Decision Rationale", "ScienceDirect", "https://www.sciencedirect.com/science/article/pii/S0920410505000173"),
    ("Operational Decision Discovery from Data", "Springer", "https://link.springer.com/article/10.1007/s40622-024-00402-2"),
    ("Corporate Prediction Markets & Decisions", "Cambridge / Experimental Economics", "https://www.cambridge.org/core/journals/experimental-economics/article/abs/improving-decisions-with-market-information-an-experiment-on-corporate-prediction-markets/A37AD7E6552E892B97709D825715A9E8"),
    ("Incentive-Compatible Forecasting", "INFORMS / Management Science", "https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4410"),
    ("P0 — Internal Prediction Markets", "priorityzero.ai", "https://priorityzero.ai/"),
    ("Hypermind — Crowd Forecasting", "hypermind.com", "https://www.hypermind.com/products-services/crowd"),
    ("Vigil — Decision Tracking Use Cases", "trustvigil.com", "https://trustvigil.com/use-cases"),
    ("Patent EP1402435A4", "Google Patents", "https://patents.google.com/patent/EP1402435A4/en"),
    ("Patent US20250217680A1", "Google Patents", "https://patents.google.com/patent/US20250217680A1/en"),
]
col_w = Inches(5.95)
row_h = Inches(0.5)
r2y0 = Inches(4.72)
for i, (t, src, url) in enumerate(refs):
    r_, c_ = divmod(i, 2)
    x = Emu(int(MARGIN + c_ * (col_w + Inches(0.25))))
    y = Emu(int(r2y0 + r_ * row_h))
    tb, tf = add_multirun_textbox(s, x, y, col_w, row_h, wrap=True)
    p = tf.paragraphs[0]
    p.line_spacing = 1.0
    r = p.add_run(); r.text = f"{i+1}. {t} "
    r.font.size = Pt(9.5); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE
    r2 = p.add_run(); r2.text = "— " + src
    r2.font.size = Pt(9.5); r2.font.name = FONT; r2.font.color.rgb = GRAY
    r2.hyperlink.address = url

set_notes(s, "Thirteen sources in total. The top four are real, independently verified papers published 2023 to 2025. Full details"
    "are on the Literature Review slide (precision, F1/ROC-AUC style methodology notes aside, this is where novelty gets"
    "defended). The remaining nine are background and prior-art sources from the original project brief: two academic"
    "papers on organisational memory and operational decision discovery, two on corporate prediction markets and"
    "incentive-compatible forecasting, two commercial products (P0 and Hypermind) in the forecasting-market space, one"
    "decision-tracking product (Vigil), and two patents covering related decision-lifecycle and organisational-memory"
    "concepts. All thirteen should be read before claiming novelty in any written report that accompanies this deck.")

# =====================================================================
# FOOTERS — applied uniformly across slides 2..15 (title slide has its own bar)
# =====================================================================
SECTION_NAMES = [
    None, "The Problem", "Literature Review", "Core Insight", "Defining Decision Debt", "The Solution",
    "Worked Example", "Dataset & Pipeline", "Dataset Preview", "Machine Learning", "System Architecture",
    "Working Prototype", "Decision Evaluation", "Differentiation", "Target Customer & Model",
    "Risks & Limitations", "Conclusion & Roadmap", "References",
]
for idx, sl in enumerate(prs.slides, start=1):
    if idx == 1:
        continue
    page_footer(sl, idx, TOTAL, section=SECTION_NAMES[idx - 1])

prs.save("/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/build/Verdikt.pptx")
print("FINAL deck saved. total slides:", len(prs.slides._sldIdLst))
