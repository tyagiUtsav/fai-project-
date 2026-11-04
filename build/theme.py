"""Shared theme + layout helpers for the Decision Debt OS deck."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
import copy

# ---------------- Palette (pastel) ----------------
# Soft ivory backdrop, white cards, dusty-muted accents (legible as both
# fills and text), warm charcoal-plum body text. Variable NAMES are kept
# identical to the original dark theme so every call site below (strips,
# text runs, borders, chart colors) keeps working unchanged.
NAVY      = RGBColor(0xFA, 0xF7, 0xF2)   # page background — soft ivory
PANEL     = RGBColor(0xFF, 0xFF, 0xFF)   # card fill — white
PANEL_2   = RGBColor(0xF2, 0xED, 0xFA)   # secondary card fill — soft lavender-white
STROKE    = RGBColor(0xE3, 0xDC, 0xEF)   # card border — soft lavender-gray
BLUE      = RGBColor(0x6C, 0x8E, 0xBF)   # dusty pastel blue
BLUE_DK   = RGBColor(0x4A, 0x6C, 0x94)   # deeper dusty blue
CYAN      = RGBColor(0x4F, 0xAE, 0x97)   # muted pastel teal/sage
AMBER     = RGBColor(0xD9, 0xA5, 0x4C)   # muted pastel gold
RED       = RGBColor(0xD9, 0x78, 0x78)   # muted pastel coral
WHITE     = RGBColor(0x3A, 0x35, 0x42)   # primary text — warm charcoal-plum
GRAY      = RGBColor(0x78, 0x6F, 0x85)   # secondary text — muted mauve-gray
GRAY_DK   = RGBColor(0x99, 0x92, 0xA3)   # tertiary text — lighter muted mauve-gray

FONT = "Calibri"
FONT_TITLE = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.6)


def new_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_slide(prs):
    layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(layout)
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    return slide


def _no_shadow(shape):
    try:
        shape.shadow.inherit = False
    except Exception:
        pass


def set_round_radius(shape, frac=0.08):
    try:
        shape.adjustments[0] = frac
    except Exception:
        pass


def add_rect(slide, left, top, width, height, fill=PANEL, line=None, line_w=Pt(1), radius=None, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    shp = slide.shapes.add_shape(shape_type, left, top, width, height)
    _no_shadow(shp)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w
    if radius is not None and shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        set_round_radius(shp, radius)
    return shp


def add_line(slide, left, top, width, height, color=BLUE, weight=Pt(2.25)):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    _no_shadow(shp)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp


def add_text(slide, left, top, width, height, text, size=14, color=WHITE, bold=False,
             italic=False, align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP,
             line_spacing=1.0, wrap=True, space_after=0, char_spacing=None):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
        r.font.color.rgb = color
        if char_spacing is not None:
            _set_char_spacing(r, char_spacing)
    return tb


def _set_char_spacing(run, pts):
    rPr = run._r.get_or_add_rPr()
    rPr.set('spc', str(int(pts * 100)))


def add_multirun_textbox(slide, left, top, width, height, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def add_para(tf, runs, align=PP_ALIGN.LEFT, line_spacing=1.1, space_after=4, space_before=0, bullet=False, new=True):
    """runs: list of (text, size, color, bold, italic, font)"""
    p = tf.paragraphs[0] if (new is False) else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line_spacing
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    for (text, size, color, bold, italic, font) in runs:
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font or FONT
        r.font.color.rgb = color
    return p


def eyebrow(slide, text, color=CYAN, top=Inches(0.42)):
    add_text(slide, MARGIN, top, Inches(11.5), Inches(0.35), text.upper(), size=12.5,
              color=color, bold=True, font=FONT, char_spacing=1.6)


def title(slide, text, top=Inches(0.78), size=30, width=Inches(12.1), color=WHITE):
    add_text(slide, MARGIN, top, width, Inches(1.0), text, size=size, color=color, bold=True, font=FONT_TITLE, line_spacing=1.03)


def accent_rule(slide, top=Inches(1.56), left=MARGIN, width=Inches(0.85), color=AMBER):
    add_line(slide, left, top, width, Pt(3.2), color=color)


def page_footer(slide, idx, total, section=""):
    add_text(slide, MARGIN, Inches(7.14), Inches(6), Inches(0.3), section, size=9.5, color=GRAY_DK, font=FONT)
    add_text(slide, Inches(11.4), Inches(7.14), Inches(1.4), Inches(0.3), f"{idx:02d} / {total:02d}", size=9.5,
              color=GRAY_DK, align=PP_ALIGN.RIGHT, font=FONT)
    add_text(slide, Inches(5.1), Inches(7.14), Inches(3.1), Inches(0.3), "VERDIKT", size=9, color=RGBColor(0xD8,0xD2,0xE2),
              align=PP_ALIGN.CENTER, font=FONT, char_spacing=1.2)


def set_notes(slide, text):
    notes = slide.notes_slide
    notes.notes_text_frame.text = text


def connector_arrow(slide, x1, y1, x2, y2, color=GRAY, weight=Pt(1.75)):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    conn.line.color.rgb = color
    conn.line.width = weight
    line_elem = conn.line._get_or_add_ln()
    tail = line_elem.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
    line_elem.append(tail)
    return conn


def pill(slide, left, top, width, height, text, fill=PANEL_2, line=STROKE, text_color=WHITE, size=11, bold=False):
    shp = add_rect(slide, left, top, width, height, fill=fill, line=line, line_w=Pt(1), radius=0.5, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = FONT
    r.font.color.rgb = text_color
    return shp


def dot(slide, left, top, size, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    _no_shadow(shp)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp
