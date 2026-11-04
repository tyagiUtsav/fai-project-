"""Higher-level diagram components built on theme.py primitives."""
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from theme import (add_rect, add_text, add_line, connector_arrow, dot, pill,
                    NAVY, PANEL, PANEL_2, STROKE, BLUE, BLUE_DK, CYAN, AMBER, RED,
                    WHITE, GRAY, GRAY_DK, FONT, _no_shadow)


def flow_steps(slide, steps, left, top, width, height, node_colors=None, text_size=11.5,
               sub=None, sub_size=9.5, gap=Inches(0.28)):
    """Draw N boxes left-to-right connected by arrows. steps: list[str]."""
    n = len(steps)
    gap_emu = gap
    node_w = Emu(int((width - gap_emu * (n - 1)) / n))
    for i, label in enumerate(steps):
        x = Emu(int(left + i * (node_w + gap_emu)))
        color = (node_colors[i] if node_colors else PANEL_2)
        box = add_rect(slide, x, top, node_w, height, fill=PANEL_2, line=STROKE, line_w=Pt(1), radius=0.14)
        strip = add_rect(slide, x, top, node_w, Pt(4.5), fill=color, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Pt(6)
        label_lines = label.split("\n")
        for li, lline in enumerate(label_lines):
            p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            if li > 0:
                p.space_before = Pt(1)
            r = p.add_run()
            r.text = lline
            r.font.size = Pt(text_size)
            r.font.bold = True
            r.font.name = FONT
            r.font.color.rgb = WHITE
        if sub and sub[i]:
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(3)
            r2 = p2.add_run()
            r2.text = sub[i]
            r2.font.size = Pt(sub_size)
            r2.font.name = FONT
            r2.font.color.rgb = GRAY
        if i < n - 1:
            ax1 = Emu(int(x + node_w))
            ax2 = Emu(int(ax1 + gap_emu))
            ay = Emu(int(top + height / 2))
            connector_arrow(slide, ax1, ay, ax2, ay, color=GRAY, weight=Pt(2))


def broken_loop(slide, steps, left, top, width, height, loop_color=RED):
    """4-step flow where the last step loops back to the first (repeated-mistake cycle)."""
    flow_steps(slide, steps, left, top, width, height, node_colors=[BLUE, AMBER, RED, RED])
    # loop-back arrow under the row
    n = len(steps)
    node_w = Emu(int((width - Inches(0.28) * (n - 1)) / n))
    last_cx = Emu(int(left + (n - 1) * (node_w + Inches(0.28)) + node_w / 2))
    first_cx = Emu(int(left + node_w / 2))
    y_bottom = Emu(int(top + height + Inches(0.22)))
    y_top = Emu(int(top + height))
    connector_arrow(slide, last_cx, y_top, last_cx, y_bottom, color=loop_color, weight=Pt(1.75))
    connector_arrow(slide, last_cx, y_bottom, first_cx, y_bottom, color=loop_color, weight=Pt(1.75))
    connector_arrow(slide, first_cx, y_bottom, first_cx, y_top, color=loop_color, weight=Pt(1.75))
    add_text(slide, Emu(int(left + width/2 - Inches(1.1))), Emu(int(y_bottom + Inches(0.05))), Inches(2.2), Inches(0.3),
              "REPEATS", size=9.5, color=loop_color, bold=True, align=PP_ALIGN.CENTER, char_spacing=1.5)


def metric_tile(slide, left, top, width, height, value, label, accent=CYAN, value_size=30, label_size=10.5):
    box = add_rect(slide, left, top, width, height, fill=PANEL, line=STROKE, line_w=Pt(1), radius=0.12)
    add_rect(slide, left, top, Pt(4), height, fill=accent, line=None, radius=0, shape_type=MSO_SHAPE.RECTANGLE)
    tf = box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.22)
    tf.margin_right = Inches(0.12)
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = value
    r.font.size = Pt(value_size); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = WHITE
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    p2.space_before = Pt(2)
    r2 = p2.add_run(); r2.text = label
    r2.font.size = Pt(label_size); r2.font.name = FONT; r2.font.color.rgb = GRAY
    return box


def card(slide, left, top, width, height, fill=PANEL, line=STROKE, radius=0.08):
    return add_rect(slide, left, top, width, height, fill=fill, line=line, line_w=Pt(1), radius=radius)


def field_row(tf, label, value, label_color=GRAY, value_color=WHITE, label_size=10, value_size=12,
              new=True, space_after=7):
    p = tf.paragraphs[0] if not new else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.line_spacing = 1.05
    r1 = p.add_run(); r1.text = label.upper() + "   "
    r1.font.size = Pt(label_size); r1.font.bold = True; r1.font.name = FONT; r1.font.color.rgb = label_color
    r2 = p.add_run(); r2.text = value
    r2.font.size = Pt(value_size); r2.font.name = FONT; r2.font.color.rgb = value_color
    return p


def risk_dot_row(slide, left, top, width, risk_text, mitigation_text, level="amber", risk_w=Inches(5.4)):
    colors = {"red": RED, "amber": AMBER, "cyan": CYAN}
    c = colors.get(level, AMBER)
    d = dot(slide, left, Emu(int(top + Inches(0.07))), Inches(0.14), c)
    add_text(slide, Emu(int(left + Inches(0.3))), top, risk_w, Inches(0.5), risk_text, size=11.5, bold=True,
              color=WHITE, wrap=True, line_spacing=1.05)
    add_text(slide, Emu(int(left + Inches(0.3) + risk_w + Inches(0.25))), top, width - risk_w - Inches(0.55), Inches(0.5),
              mitigation_text, size=11, color=GRAY, wrap=True, line_spacing=1.05)


def checkmark(slide, left, top, size, kind="yes"):
    """kind: yes / no / partial"""
    if kind == "yes":
        t, c = "✓", CYAN
    elif kind == "no":
        t, c = "–", GRAY_DK
    else:
        t, c = "◐", AMBER
    add_text(slide, left, top, size, size, t, size=15, color=c, bold=True, align=PP_ALIGN.CENTER)
