"""
Premium PDF Generator — The Manipulation Map
Lazy Scholar PH · Psychological Defense Series
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, CondPageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String
from reportlab.graphics import renderPDF
import os

# ─────────────────────────────────────────
# BRAND PALETTE
# ─────────────────────────────────────────
INK        = colors.HexColor('#1A1A2E')
MUTED      = colors.HexColor('#4A4A6A')
ACCENT     = colors.HexColor('#C9A84C')
ACCENT2    = colors.HexColor('#1B4F72')
LIGHT      = colors.HexColor('#F8F7F4')
WHITE      = colors.white
RULE       = colors.HexColor('#E0DDD5')
HIGHLIGHT  = colors.HexColor('#FFF8E7')
RED        = colors.HexColor('#8B2635')
DARK_TEAL  = colors.HexColor('#2C5F7A')
FOREST     = colors.HexColor('#3A7A5E')

W, H = A4  # 595.28 x 841.89 points
MARGIN_L = 50
MARGIN_R = 50
MARGIN_T = 50
MARGIN_B = 50
CONTENT_W = W - MARGIN_L - MARGIN_R

OUTPUT = '/home/user/Lazy-ScholarPH/ai-pipeline/pdfs/2026-06-02-premium.pdf'

# ─────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────
def make_styles():
    s = {}

    s['brand_label'] = ParagraphStyle('brand_label',
        fontName='Helvetica-Bold', fontSize=8, textColor=ACCENT,
        alignment=TA_CENTER, letterSpacing=3, leading=12,
        spaceAfter=8)

    s['series_tag'] = ParagraphStyle('series_tag',
        fontName='Helvetica', fontSize=7, textColor=colors.HexColor('#888899'),
        alignment=TA_CENTER, letterSpacing=2, leading=10, spaceAfter=36)

    s['title_eyebrow'] = ParagraphStyle('title_eyebrow',
        fontName='Helvetica-Bold', fontSize=8, textColor=ACCENT,
        alignment=TA_CENTER, letterSpacing=4, leading=12, spaceAfter=16)

    s['main_title'] = ParagraphStyle('main_title',
        fontName='Times-Bold', fontSize=46, textColor=WHITE,
        alignment=TA_CENTER, leading=52, spaceAfter=24)

    s['main_subtitle'] = ParagraphStyle('main_subtitle',
        fontName='Helvetica', fontSize=12, textColor=colors.HexColor('#BBBBCC'),
        alignment=TA_CENTER, leading=20, spaceAfter=40)

    s['title_meta'] = ParagraphStyle('title_meta',
        fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor('#555566'),
        alignment=TA_CENTER, letterSpacing=2, leading=10)

    # TOC
    s['toc_label'] = ParagraphStyle('toc_label',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=ACCENT,
        letterSpacing=3, leading=12, spaceAfter=16)

    s['toc_heading'] = ParagraphStyle('toc_heading',
        fontName='Times-Bold', fontSize=22, textColor=INK,
        leading=28, spaceAfter=24)

    s['toc_title'] = ParagraphStyle('toc_title',
        fontName='Helvetica-Bold', fontSize=10, textColor=INK,
        leading=14, spaceAfter=2)

    s['toc_sub'] = ParagraphStyle('toc_sub',
        fontName='Helvetica', fontSize=8.5, textColor=MUTED,
        leading=13, spaceAfter=8)

    # Chapter
    s['chapter_num'] = ParagraphStyle('chapter_num',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=ACCENT,
        letterSpacing=3, leading=12, spaceAfter=12)

    s['chapter_title'] = ParagraphStyle('chapter_title',
        fontName='Times-Bold', fontSize=28, textColor=INK,
        leading=34, spaceAfter=16)

    s['chapter_intro'] = ParagraphStyle('chapter_intro',
        fontName='Times-Italic', fontSize=11.5, textColor=MUTED,
        leading=19, spaceAfter=24)

    # Body
    s['body'] = ParagraphStyle('body',
        fontName='Times-Roman', fontSize=10.5, textColor=INK,
        leading=18, spaceAfter=10, alignment=TA_JUSTIFY)

    s['body_muted'] = ParagraphStyle('body_muted',
        fontName='Times-Roman', fontSize=10.5, textColor=MUTED,
        leading=18, spaceAfter=10, alignment=TA_JUSTIFY)

    s['h2'] = ParagraphStyle('h2',
        fontName='Times-Bold', fontSize=17, textColor=INK,
        leading=22, spaceBefore=24, spaceAfter=12)

    s['h3'] = ParagraphStyle('h3',
        fontName='Helvetica-Bold', fontSize=11.5, textColor=INK,
        leading=16, spaceBefore=18, spaceAfter=8)

    s['h4'] = ParagraphStyle('h4',
        fontName='Helvetica-Bold', fontSize=9.5, textColor=ACCENT2,
        leading=14, spaceBefore=14, spaceAfter=6, letterSpacing=0.5)

    s['pull_quote'] = ParagraphStyle('pull_quote',
        fontName='Times-Italic', fontSize=13.5, textColor=INK,
        leading=22, spaceAfter=6, alignment=TA_LEFT,
        leftIndent=0, rightIndent=0)

    s['pull_attr'] = ParagraphStyle('pull_attr',
        fontName='Helvetica', fontSize=8, textColor=MUTED,
        leading=12, letterSpacing=1)

    s['callout_label'] = ParagraphStyle('callout_label',
        fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
        letterSpacing=3, leading=12, spaceAfter=8)

    s['callout_body'] = ParagraphStyle('callout_body',
        fontName='Helvetica', fontSize=10.5, textColor=WHITE,
        leading=17, spaceAfter=0, alignment=TA_JUSTIFY)

    s['counter_label'] = ParagraphStyle('counter_label',
        fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
        letterSpacing=2, leading=11, spaceAfter=4)

    s['counter_body'] = ParagraphStyle('counter_body',
        fontName='Helvetica', fontSize=9.5, textColor=WHITE,
        leading=15, spaceAfter=0)

    s['arch_number'] = ParagraphStyle('arch_number',
        fontName='Helvetica-Bold', fontSize=26, textColor=ACCENT,
        leading=30, spaceAfter=0)

    s['arch_label'] = ParagraphStyle('arch_label',
        fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
        letterSpacing=2, leading=11, spaceAfter=2)

    s['arch_title'] = ParagraphStyle('arch_title',
        fontName='Helvetica-Bold', fontSize=14, textColor=INK,
        leading=18, spaceAfter=0)

    s['arch_body'] = ParagraphStyle('arch_body',
        fontName='Times-Roman', fontSize=10, textColor=INK,
        leading=16, spaceAfter=8)

    s['arch_example'] = ParagraphStyle('arch_example',
        fontName='Times-Italic', fontSize=9.5, textColor=MUTED,
        leading=15, spaceAfter=0)

    s['step_num'] = ParagraphStyle('step_num',
        fontName='Helvetica-Bold', fontSize=36, textColor=ACCENT,
        leading=40, spaceAfter=0)

    s['step_title'] = ParagraphStyle('step_title',
        fontName='Helvetica-Bold', fontSize=12.5, textColor=INK,
        leading=17, spaceAfter=8)

    s['step_body'] = ParagraphStyle('step_body',
        fontName='Times-Roman', fontSize=10.5, textColor=MUTED,
        leading=17, spaceAfter=8)

    s['step_phrase'] = ParagraphStyle('step_phrase',
        fontName='Times-Italic', fontSize=9.5, textColor=INK,
        leading=16, leftIndent=10)

    s['bias_num'] = ParagraphStyle('bias_num',
        fontName='Helvetica-Bold', fontSize=7, textColor=WHITE,
        leading=11, letterSpacing=1)

    s['bias_title'] = ParagraphStyle('bias_title',
        fontName='Helvetica-Bold', fontSize=12, textColor=INK,
        leading=17, spaceAfter=8)

    s['bias_body'] = ParagraphStyle('bias_body',
        fontName='Times-Roman', fontSize=10, textColor=INK,
        leading=16, spaceAfter=6)

    s['checklist_item'] = ParagraphStyle('checklist_item',
        fontName='Times-Roman', fontSize=10, textColor=INK,
        leading=16, leftIndent=18, spaceAfter=2)

    s['table_header'] = ParagraphStyle('table_header',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE,
        leading=13, letterSpacing=0.5)

    s['table_cell'] = ParagraphStyle('table_cell',
        fontName='Times-Roman', fontSize=9.5, textColor=INK,
        leading=15)

    s['table_cell_bold'] = ParagraphStyle('table_cell_bold',
        fontName='Helvetica-Bold', fontSize=9.5, textColor=INK,
        leading=15)

    s['closing_brand'] = ParagraphStyle('closing_brand',
        fontName='Helvetica-Bold', fontSize=9, textColor=ACCENT,
        alignment=TA_CENTER, letterSpacing=4, leading=14, spaceAfter=28)

    s['closing_quote'] = ParagraphStyle('closing_quote',
        fontName='Times-Italic', fontSize=15, textColor=WHITE,
        alignment=TA_CENTER, leading=24, spaceAfter=36)

    s['closing_tagline'] = ParagraphStyle('closing_tagline',
        fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#888899'),
        alignment=TA_CENTER, leading=17, spaceAfter=16)

    s['closing_series'] = ParagraphStyle('closing_series',
        fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#555566'),
        alignment=TA_CENTER, letterSpacing=2, leading=12, spaceAfter=0)

    s['rung_label'] = ParagraphStyle('rung_label',
        fontName='Helvetica', fontSize=7, textColor=WHITE,
        letterSpacing=2, leading=11, spaceAfter=2)

    s['rung_text'] = ParagraphStyle('rung_text',
        fontName='Helvetica-Bold', fontSize=11, textColor=WHITE,
        leading=15)

    s['seq_label'] = ParagraphStyle('seq_label',
        fontName='Helvetica-Bold', fontSize=7, textColor=ACCENT,
        letterSpacing=2, leading=11, alignment=TA_CENTER)

    s['seq_title'] = ParagraphStyle('seq_title',
        fontName='Helvetica-Bold', fontSize=11, textColor=INK,
        leading=15, alignment=TA_CENTER)

    s['seq_title_w'] = ParagraphStyle('seq_title_w',
        fontName='Helvetica-Bold', fontSize=11, textColor=WHITE,
        leading=15, alignment=TA_CENTER)

    s['compare_header'] = ParagraphStyle('compare_header',
        fontName='Helvetica-Bold', fontSize=11, textColor=WHITE,
        leading=15)

    s['compare_label'] = ParagraphStyle('compare_label',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=MUTED,
        leading=14, letterSpacing=0.5)

    s['compare_cell'] = ParagraphStyle('compare_cell',
        fontName='Times-Roman', fontSize=10, textColor=INK,
        leading=15)

    s['summary_h2'] = ParagraphStyle('summary_h2',
        fontName='Helvetica-Bold', fontSize=8, textColor=ACCENT,
        letterSpacing=3, leading=12, spaceAfter=14)

    s['summary_h3'] = ParagraphStyle('summary_h3',
        fontName='Times-Bold', fontSize=17, textColor=WHITE,
        leading=22, spaceAfter=16)

    s['summary_item'] = ParagraphStyle('summary_item',
        fontName='Times-Roman', fontSize=10.5, textColor=colors.HexColor('#DDDDEE'),
        leading=17, leftIndent=16, spaceAfter=4)

    return s


# ─────────────────────────────────────────
# CUSTOM FLOWABLES
# ─────────────────────────────────────────

class AccentBar(Flowable):
    """Top accent bar (gradient-like)."""
    def __init__(self, width=CONTENT_W, height=5):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        # Draw a two-tone bar simulating gradient
        self.canv.setFillColor(ACCENT)
        self.canv.rect(0, 0, self.width * 0.5, self.height, fill=1, stroke=0)
        self.canv.setFillColor(ACCENT2)
        self.canv.rect(self.width * 0.5, 0, self.width * 0.5, self.height, fill=1, stroke=0)


def draw_title_page(canvas, doc):
    """Draw the full title page background and content."""
    canvas.saveState()
    c = canvas
    cx = W / 2  # true page center

    # Background
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, H - 6, W * 0.5, 6, fill=1, stroke=0)
    c.setFillColor(ACCENT2)
    c.rect(W * 0.5, H - 6, W * 0.5, 6, fill=1, stroke=0)

    # Bottom accent bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, W * 0.5, 6, fill=1, stroke=0)
    c.setFillColor(ACCENT2)
    c.rect(W * 0.5, 0, W * 0.5, 6, fill=1, stroke=0)

    # Brand badge box
    badge_w, badge_h = 180, 26
    badge_x = cx - badge_w / 2
    badge_y = H - 150
    c.setStrokeColor(colors.HexColor('#6A5A2C'))
    c.setLineWidth(1)
    c.rect(badge_x, badge_y, badge_w, badge_h, fill=0, stroke=1)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(ACCENT)
    c.drawCentredString(cx, badge_y + 9, 'LAZY SCHOLAR PH')

    # Series tag
    c.setFont('Helvetica', 7)
    c.setFillColor(colors.HexColor('#666677'))
    c.drawCentredString(cx, badge_y - 22, 'PSYCHOLOGICAL DEFENSE SERIES  ·  VOLUME II')

    # Eyebrow
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(ACCENT)
    c.drawCentredString(cx, badge_y - 54, 'PREMIUM DIGITAL GUIDE')

    # Title
    c.setFont('Times-Bold', 48)
    c.setFillColor(WHITE)
    c.drawCentredString(cx, badge_y - 116, 'The Manipulation')
    c.drawCentredString(cx, badge_y - 168, 'Map')

    # Accent rule
    line_y = badge_y - 185
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(cx - 30, line_y, cx + 30, line_y)

    # Subtitle
    c.setFont('Helvetica', 11)
    c.setFillColor(colors.HexColor('#AAAACC'))
    c.drawCentredString(cx, line_y - 30, 'How to Recognize, Decode, and Neutralize')
    c.drawCentredString(cx, line_y - 47, 'Psychological Influence Before It Works on You')

    # Copyright
    c.setFont('Helvetica', 7.5)
    c.setFillColor(colors.HexColor('#444455'))
    c.drawCentredString(cx, 30, '© 2026 LAZY SCHOLAR PH  ·  ALL RIGHTS RESERVED')
    canvas.restoreState()


def draw_closing_page(canvas):
    """Draw the full closing page background and content."""
    canvas.saveState()
    c = canvas
    cx = W / 2

    # Background
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, H - 6, W * 0.5, 6, fill=1, stroke=0)
    c.setFillColor(ACCENT2)
    c.rect(W * 0.5, H - 6, W * 0.5, 6, fill=1, stroke=0)

    # Brand
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(ACCENT)
    c.drawCentredString(cx, H - 100, 'LAZY SCHOLAR PH')

    # Quote
    c.setFont('Times-Italic', 14)
    c.setFillColor(WHITE)
    c.drawCentredString(cx, H - 190, '"The first and most fundamental defense')
    c.drawCentredString(cx, H - 210, 'against manipulation is the refusal')
    c.drawCentredString(cx, H - 230, 'to be ashamed of your own judgment."')

    # Divider
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(cx - 20, H - 255, cx + 20, H - 255)

    # Tagline
    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#888899'))
    c.drawCentredString(cx, H - 285, 'Becoming manipulation-literate is not about becoming cynical.')
    c.drawCentredString(cx, H - 302, 'It is about ensuring your decisions are actually yours.')

    # Series
    c.setFont('Helvetica', 8.5)
    c.setFillColor(colors.HexColor('#555566'))
    c.drawCentredString(cx, H - 340, 'PSYCHOLOGICAL DEFENSE SERIES  ·  VOLUME II')

    # Copyright
    c.setFont('Helvetica', 7.5)
    c.setFillColor(colors.HexColor('#333344'))
    c.drawCentredString(cx, 30, '© 2026 Lazy Scholar PH  ·  All Rights Reserved  ·  Educational Use Only')
    canvas.restoreState()


class ChapterBar(Flowable):
    """Dark top border for chapter openers."""
    def __init__(self, width=CONTENT_W):
        Flowable.__init__(self)
        self.width = width
        self.height = 5

    def draw(self):
        self.canv.setFillColor(INK)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


class PullQuoteBlock(Flowable):
    def __init__(self, text, attr=None, width=CONTENT_W):
        Flowable.__init__(self)
        self.text = text
        self.attr = attr
        self.width = width
        self.height = 100  # estimated

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(HIGHLIGHT)
        c.rect(0, 0, self.width, self.height - 4, fill=1, stroke=0)
        # Left bar
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4, self.height - 4, fill=1, stroke=0)

        # Quote text
        from reportlab.platypus import Paragraph
        from io import StringIO
        c.setFont('Times-Italic', 13.5)
        c.setFillColor(INK)
        # Draw text with padding
        c.drawString(16, self.height - 30, '')  # placeholder — we handle via table


class SectionRule(Flowable):
    def __init__(self, width=CONTENT_W):
        Flowable.__init__(self)
        self.width = width
        self.height = 20

    def draw(self):
        c = self.canv
        y = self.height / 2
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(0, y, self.width * 0.45, y)
        c.line(self.width * 0.55, y, self.width, y)
        c.setFillColor(ACCENT)
        c.circle(self.width / 2, y, 4, fill=1, stroke=0)


class ClosingPageMarker(Flowable):
    """Zero-height marker that signals the on_page callback to draw the closing page."""
    _is_closing = [False]

    def __init__(self):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        ClosingPageMarker._is_closing[0] = True


# ─────────────────────────────────────────
# PAGE TEMPLATES / HEADER-FOOTER
# ─────────────────────────────────────────

_page_counter = [0]

def on_page(canvas, doc):
    _page_counter[0] += 1
    page = _page_counter[0]

    if page == 1:
        draw_title_page(canvas, doc)
        return

    if page == 2:
        # Light TOC background
        canvas.saveState()
        canvas.setFillColor(LIGHT)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()
        return

    # Check if this is the closing page
    if ClosingPageMarker._is_closing[0]:
        draw_closing_page(canvas)
        ClosingPageMarker._is_closing[0] = False
        return

    # Normal content pages
    canvas.saveState()

    # Header rule
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, H - MARGIN_T + 8, W - MARGIN_R, H - MARGIN_T + 8)

    # Header brand
    canvas.setFont('Helvetica-Bold', 7)
    canvas.setFillColor(ACCENT)
    canvas.drawString(MARGIN_L, H - MARGIN_T + 12, 'LAZY SCHOLAR PH')

    # Header series
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(W - MARGIN_R, H - MARGIN_T + 12, 'THE MANIPULATION MAP')

    # Footer rule
    canvas.setStrokeColor(RULE)
    canvas.line(MARGIN_L, MARGIN_B - 10, W - MARGIN_R, MARGIN_B - 10)

    # Footer page number
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(W / 2, MARGIN_B - 22, str(page - 2))

    canvas.restoreState()


# ─────────────────────────────────────────
# HELPER BUILDERS
# ─────────────────────────────────────────

S = make_styles()


def sp(n):
    return Spacer(1, n)


def rule(color=RULE, width=CONTENT_W, thickness=0.5):
    return HRFlowable(width=width, thickness=thickness, color=color, spaceAfter=0)


def pull_quote(text, attr=None):
    rows = [[Paragraph(text, S['pull_quote'])]]
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HIGHLIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LINEBEFORE', (0, 0), (0, -1), 4, ACCENT),
    ])
    elems = [Table(rows, colWidths=[CONTENT_W], style=ts), sp(4)]
    if attr:
        elems.append(Paragraph(attr, S['pull_attr']))
    elems.append(sp(12))
    return elems


def callout(label, text):
    rows = [
        [Paragraph(label, S['callout_label'])],
        [Paragraph(text, S['callout_body'])],
    ]
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT2),
        ('LEFTPADDING', (0, 0), (-1, -1), 24),
        ('RIGHTPADDING', (0, 0), (-1, -1), 24),
        ('TOPPADDING', (0, 0), (0, 0), 20),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        ('TOPPADDING', (0, 1), (0, 1), 0),
        ('BOTTOMPADDING', (0, 1), (0, 1), 20),
    ])
    return [Table(rows, colWidths=[CONTENT_W], style=ts), sp(12)]


def arch_card(num, title, mechanic, lever, examples, tell, counter):
    num_p = Paragraph(num, S['arch_number'])
    lbl_p = Paragraph('ARCHITECTURE', S['arch_label'])
    ttl_p = Paragraph(title, S['arch_title'])

    header_data = [[num_p, [lbl_p, ttl_p]]]
    header_ts = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    header_tbl = Table(header_data, colWidths=[50, CONTENT_W - 50 - 64 + 20], style=header_ts)

    body_items = [
        Paragraph(f'<b>The Mechanic:</b> {mechanic}', S['arch_body']),
        Paragraph(f'<b>The Lever:</b> {lever}', S['arch_body']),
    ]

    ex_data = [[Paragraph(examples, S['arch_example'])]]
    ex_ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])
    ex_tbl = Table(ex_data, colWidths=[CONTENT_W - 64], style=ex_ts)

    if tell:
        body_items.append(sp(4))
        body_items.append(ex_tbl)
        body_items.append(sp(6))
        body_items.append(Paragraph(f'<b>The Tell:</b> {tell}', S['arch_body']))

    ctr_data = [
        [Paragraph('YOUR COUNTER', S['counter_label'])],
        [Paragraph(counter, S['counter_body'])],
    ]
    ctr_ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), INK),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (0, 0), 12),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        ('TOPPADDING', (0, 1), (0, 1), 0),
        ('BOTTOMPADDING', (0, 1), (0, 1), 12),
    ])
    ctr_tbl = Table(ctr_data, colWidths=[CONTENT_W - 64], style=ctr_ts)

    body_items.append(sp(8))
    body_items.append(ctr_tbl)

    inner_data = [[header_tbl], [body_items]]
    inner_ts = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    inner = Table(inner_data, colWidths=[CONTENT_W - 64], style=inner_ts)

    outer_data = [[inner]]
    outer_ts = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, RULE),
        ('LINEBEFORE', (0, 0), (0, -1), 4, ACCENT2),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('BACKGROUND', (0, 0), (-1, -1), WHITE),
    ])
    outer = Table(outer_data, colWidths=[CONTENT_W], style=outer_ts)

    return [KeepTogether([outer]), sp(14)]


def bias_card(num_label, title, *paragraphs):
    badge = Table(
        [[Paragraph(num_label, S['bias_num'])]],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]),
        colWidths=[120]
    )

    content = [badge, sp(10), Paragraph(title, S['bias_title'])]
    for p in paragraphs:
        content.append(Paragraph(p, S['bias_body']))

    card = Table(
        [[content]],
        style=TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, RULE),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
            ('BACKGROUND', (0, 0), (-1, -1), WHITE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]),
        colWidths=[CONTENT_W]
    )
    return [KeepTogether([card]), sp(14)]


def checklist(items):
    rows = []
    for item in items:
        rows.append([
            Paragraph('☐', ParagraphStyle('cb', fontName='Helvetica', fontSize=12,
                                          textColor=ACCENT, leading=16)),
            Paragraph(item, S['checklist_item'])
        ])
    ts = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 8),
        ('LEFTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, RULE),
    ])
    return Table(rows, colWidths=[20, CONTENT_W - 20], style=ts)


def chapter_header(num, title, intro):
    return [
        ChapterBar(),
        sp(24),
        Paragraph(num, S['chapter_num']),
        Paragraph(title, S['chapter_title']),
        Paragraph(intro, S['chapter_intro']),
        rule(RULE),
        sp(20),
    ]


def data_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)

    header_row = [Paragraph(h, S['table_header']) for h in headers]
    body_rows = []
    for i, row in enumerate(rows):
        body_rows.append([Paragraph(str(cell), S['table_cell']) for cell in row])

    data = [header_row] + body_rows
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), INK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT]),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, RULE),
    ])
    return Table(data, colWidths=col_widths, style=ts)


def protocol_step(num, title, body, phrases=None):
    num_cell = Paragraph(num, S['step_num'])
    content = [Paragraph(title, S['step_title']), Paragraph(body, S['step_body'])]
    if phrases:
        phrase_data = [[Paragraph(ph, S['step_phrase'])] for ph in phrases]
        phrase_ts = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
            ('LINEBEFORE', (0, 0), (0, -1), 2, ACCENT),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])
        content.append(Table(phrase_data, colWidths=[CONTENT_W - 70], style=phrase_ts))

    row = [[num_cell, content]]
    ts = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 20),
        ('LEFTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, RULE),
    ])
    return [Table(row, colWidths=[50, CONTENT_W - 50], style=ts), sp(8)]


def sequence_diagram(steps):
    cells = []
    for i, (label, title, highlight) in enumerate(steps):
        lbl_s = S['seq_label'] if not highlight else ParagraphStyle(
            'sl_h', fontName='Helvetica-Bold', fontSize=7,
            textColor=ACCENT, letterSpacing=2, leading=11, alignment=TA_CENTER)
        ttl_s = S['seq_title_w'] if highlight else S['seq_title']
        cells.append(Paragraph(label, lbl_s))
        cells.append(Paragraph(title, ttl_s))
        if i < len(steps) - 1:
            cells.append(Paragraph('', S['seq_title']))  # spacer

    # Build as row of boxes
    col_w = (CONTENT_W - 30) / len(steps)  # minus arrows
    row_data = []
    ts_cmds = []

    for i, (label, title, highlight) in enumerate(steps):
        lbl_s = S['seq_label'] if not highlight else ParagraphStyle(
            'sl_h2', fontName='Helvetica-Bold', fontSize=7,
            textColor=ACCENT, letterSpacing=2, leading=11, alignment=TA_CENTER)
        ttl_s = S['seq_title_w'] if highlight else S['seq_title']
        row_data.append([[Paragraph(label, lbl_s), Paragraph(title, ttl_s)]])
        bg = INK if highlight else LIGHT
        ts_cmds.append(('BACKGROUND', (i * 2, 0), (i * 2, -1), bg))

    # Interleave arrows
    final_row = []
    for i in range(len(steps)):
        final_row.append([Paragraph(steps[i][1], S['seq_title_w'] if steps[i][2] else S['seq_title']),
                          Paragraph(steps[i][0], S['seq_label'])])
        if i < len(steps) - 1:
            final_row.append([Paragraph('→',
                ParagraphStyle('arr', fontName='Helvetica-Bold', fontSize=16,
                               textColor=ACCENT, leading=20, alignment=TA_CENTER))])

    # Simpler approach: just a flat table
    col_widths = []
    header_cells = []
    body_cells = []
    for i, (label, title, highlight) in enumerate(steps):
        col_widths.append(col_w)
        lbl_s = ParagraphStyle('seql', fontName='Helvetica-Bold', fontSize=6.5,
                               textColor=ACCENT if highlight else ACCENT,
                               letterSpacing=2, leading=10, alignment=TA_CENTER)
        ttl_s = S['seq_title_w'] if highlight else S['seq_title']
        header_cells.append(Paragraph(label, lbl_s))
        body_cells.append(Paragraph(title, ttl_s))
        if i < len(steps) - 1:
            col_widths.append(10)
            header_cells.append(Paragraph('', lbl_s))
            body_cells.append(Paragraph('→',
                ParagraphStyle('arr2', fontName='Helvetica-Bold', fontSize=14,
                               textColor=ACCENT, leading=18, alignment=TA_CENTER)))

    data = [header_cells, body_cells]
    ts = TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                     ('TOPPADDING', (0, 0), (-1, -1), 14),
                     ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
                     ('LEFTPADDING', (0, 0), (-1, -1), 6),
                     ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                     ('SPAN', (0, 0), (0, -1)),
                     ])

    # Use a simpler flat layout
    items = []
    for i, (label, title, highlight) in enumerate(steps):
        lbl_s = ParagraphStyle('seql2', fontName='Helvetica-Bold', fontSize=6.5,
                               textColor=ACCENT, letterSpacing=2, leading=10, alignment=TA_CENTER)
        ttl_s = S['seq_title_w'] if highlight else S['seq_title']
        items.append([Paragraph(label, lbl_s), Paragraph(title, ttl_s)])

    step_tables = []
    for i, (label, title, highlight) in enumerate(steps):
        lbl_s = ParagraphStyle('seql3', fontName='Helvetica-Bold', fontSize=6.5,
                               textColor=ACCENT, letterSpacing=2, leading=10, alignment=TA_CENTER)
        ttl_s = S['seq_title_w'] if highlight else S['seq_title']
        cell_ts = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), INK if highlight else LIGHT),
            ('TOPPADDING', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ])
        step_tables.append(Table(
            [[Paragraph(label, lbl_s)], [Paragraph(title, ttl_s)]],
            colWidths=[col_w], style=cell_ts
        ))

    # Build final row with arrows
    final_cells = []
    final_widths = []
    for i, st in enumerate(step_tables):
        final_cells.append(st)
        final_widths.append(col_w)
        if i < len(step_tables) - 1:
            final_cells.append(Paragraph('→',
                ParagraphStyle('farr', fontName='Helvetica-Bold', fontSize=14,
                               textColor=ACCENT, leading=18, alignment=TA_CENTER)))
            final_widths.append(12)

    row_ts = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])

    return [Table([final_cells], colWidths=final_widths, style=row_ts), sp(16)]


def compare_table(rows_data):
    header = [
        Paragraph('', S['compare_label']),
        Paragraph('Manipulation', ParagraphStyle('ch', fontName='Helvetica-Bold',
                  fontSize=11, textColor=WHITE, leading=15)),
        Paragraph('Ethical Influence', ParagraphStyle('ch2', fontName='Helvetica-Bold',
                  fontSize=11, textColor=WHITE, leading=15)),
    ]
    body = []
    for label, manip, ethical in rows_data:
        body.append([
            Paragraph(label, S['compare_label']),
            Paragraph(manip, S['compare_cell']),
            Paragraph(ethical, S['compare_cell']),
        ])

    ts = TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT),
        ('BACKGROUND', (1, 0), (1, 0), RED),
        ('BACKGROUND', (2, 0), (2, 0), ACCENT2),
        ('ROWBACKGROUNDS', (1, 1), (1, -1), [WHITE, LIGHT]),
        ('ROWBACKGROUNDS', (2, 1), (2, -1), [WHITE, LIGHT]),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, RULE),
    ])

    col1 = CONTENT_W * 0.22
    col23 = (CONTENT_W - col1) / 2
    return Table([header] + body, colWidths=[col1, col23, col23], style=ts)


def ladder_diagram():
    rungs = [
        ('4', 'RUNG FOUR', 'Confirm the Tactic', INK),
        ('3', 'RUNG THREE', 'Test the Pattern', ACCENT2),
        ('2', 'RUNG TWO', 'Notice the Emotional Signal', DARK_TEAL),
        ('1', 'RUNG ONE', 'Pause on the Feeling', FOREST),
    ]
    rows = []
    for num, lbl, text, bg in rungs:
        num_p = Paragraph(num, ParagraphStyle('ln', fontName='Helvetica-Bold',
                          fontSize=22, textColor=colors.Color(1,1,1,0.35), leading=26))
        lbl_p = Paragraph(lbl, ParagraphStyle('ll', fontName='Helvetica', fontSize=7,
                          textColor=colors.Color(1,1,1,0.6), letterSpacing=2, leading=11))
        txt_p = Paragraph(text, ParagraphStyle('lt', fontName='Helvetica-Bold',
                          fontSize=11, textColor=WHITE, leading=15))
        rows.append([num_p, [lbl_p, txt_p]])

    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), INK),
        ('BACKGROUND', (0, 1), (-1, 1), ACCENT2),
        ('BACKGROUND', (0, 2), (-1, 2), DARK_TEAL),
        ('BACKGROUND', (0, 3), (-1, 3), FOREST),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.Color(1,1,1,0.1)),
    ])
    return [Table(rows, colWidths=[44, CONTENT_W - 44], style=ts), sp(16)]


def summary_box(items):
    content = [
        Paragraph('MASTER FRAMEWORK', S['summary_h2']),
        Paragraph('Recognize → Decode → Neutralize', S['summary_h3']),
    ]
    for item in items:
        p = Paragraph(f'→  {item}', S['summary_item'])
        content.append(p)

    data = [[content]]
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), INK),
        ('LEFTPADDING', (0, 0), (-1, -1), 36),
        ('RIGHTPADDING', (0, 0), (-1, -1), 36),
        ('TOPPADDING', (0, 0), (-1, -1), 36),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 36),
    ])
    return [Table(data, colWidths=[CONTENT_W], style=ts), sp(16)]


def toc_row(num, title, subtitle):
    num_p = Paragraph(f'0{num}', ParagraphStyle('tn', fontName='Helvetica-Bold',
                      fontSize=8, textColor=ACCENT, letterSpacing=1, leading=14))
    title_p = Paragraph(title, S['toc_title'])
    sub_p = Paragraph(subtitle, S['toc_sub'])
    content = [title_p, sub_p]
    data = [[num_p, content]]
    ts = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 16),
        ('LEFTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, RULE),
    ])
    return Table(data, colWidths=[30, CONTENT_W - 30], style=ts)


# ─────────────────────────────────────────
# BUILD DOCUMENT
# ─────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title='The Manipulation Map',
        author='Lazy Scholar PH',
        subject='Psychological Defense — Recognize, Decode, Neutralize',
    )

    story = []

    # ── TITLE PAGE ──────────────────────────
    # All content drawn by on_page callback; just need a tiny placeholder
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # ── TOC PAGE ────────────────────────────
    story.append(Paragraph('CONTENTS', S['toc_label']))
    story.append(sp(4))
    story.append(Paragraph("What's Inside", S['toc_heading']))
    story.append(sp(8))

    toc_entries = [
        (1, "Why This Guide Exists", "The upstream problem — why awareness arrives too late"),
        (2, "The 7 Core Manipulation Architectures", "Scarcity · Obligation · Guilt · Intermittent Reward · Social Proof · Identity Hijack · Manufactured Urgency"),
        (3, "The Tactic Recognition Ladder", "A 4-rung system for identifying manipulation in under 30 seconds"),
        (4, "The Neutralization Protocol", "3-step response: Name it · Pause it · Redirect it"),
        (5, "The Workplace Manipulation Index", "The 6 most common tactics used by managers and institutions"),
        (6, "The Relationship Manipulation Decoder", "Patterns in personal relationships and how they sustain"),
        (7, "The Cognitive Bias Exploitation Map", "Anchoring · Sunk Cost · Reciprocity · Authority · Framing"),
        (8, "The Emotional Hook Anatomy", "Why manipulation always targets feeling before logic"),
        (9, "Manipulation vs. Influence", "The ethical line and your own communication audit"),
        (10, "Your Psychological Defense Stack", "Master summary · Daily checklist · Context-specific defenses"),
    ]
    for num, title, sub in toc_entries:
        story.append(toc_row(num, title, sub))

    story.append(PageBreak())

    # ── CHAPTER 1 ───────────────────────────
    story.extend(chapter_header('CHAPTER 01', 'Why This Guide Exists',
        'Most people believe they are immune to manipulation. Research says otherwise.'))

    story.extend(pull_quote(
        '"The moment you name what is being done to you,\nthe person doing it loses most of their power."'))

    story.append(Paragraph(
        'In a landmark study by Robert Cialdini, participants consistently underestimated how much '
        'social and environmental cues shaped their decisions — even when the cues were explicitly '
        'pointed out to them <i>after the fact</i>. The manipulation had already worked. '
        'The awareness came too late.', S['body']))

    story.append(Paragraph(
        'This is the core problem: <b>manipulation operates upstream of conscious thought.</b> '
        'By the time you feel something — urgency, guilt, obligation, fear — the cognitive hook '
        'is already set. You are responding to a script someone else wrote.', S['body']))

    story.append(Paragraph(
        'This guide gives you the vocabulary and the framework to intercept that script in real time.',
        S['body']))

    story.extend(callout(
        'WHAT THIS GUIDE IS',
        'A defensive intelligence resource — the equivalent of teaching someone to recognize a '
        'phishing email before they click the link. Knowing the mechanics of coercion makes you '
        'less vulnerable to it, not more dangerous.'))

    story.append(Paragraph('Who Needs This', S['h3']))
    story.append(sp(8))
    story.append(checklist([
        'Anyone who has felt pressured into decisions they later regretted',
        'Anyone in high-stakes professional environments with complex power dynamics',
        'Anyone in relationships where guilt, obligation, or fear drives more decisions than preference',
        'Anyone who wants to communicate with more clarity and less reactivity',
    ]))

    story.append(PageBreak())

    # ── CHAPTER 2 ───────────────────────────
    story.extend(chapter_header('CHAPTER 02', 'The 7 Core Manipulation Architectures',
        'Every manipulation tactic — no matter how sophisticated — is a variation of seven '
        'fundamental patterns. Learn these and you have a master key to decoding influence.'))

    story.extend(arch_card('01', 'Scarcity',
        'Creates perceived limited availability of time, resources, or access to trigger fear of missing out. The scarcity may be real or manufactured.',
        'Loss aversion. Humans are roughly twice as motivated to avoid loss as to pursue equivalent gain (Kahneman &amp; Tversky, 1979).',
        '"This offer expires in 24 hours"  ·  "Only 3 spots left"  ·  "I can\'t hold this much longer"',
        'Real scarcity is verifiable. Manufactured scarcity creates urgency but resists verification — the deadline is always vague or just out of reach.',
        'Ask: <i>"What happens if I wait a week?"</i> If the answer is punitive without a logical reason, the scarcity is a construct.'))

    story.extend(arch_card('02', 'Obligation',
        'Creates a felt sense of debt through unsolicited favors or gifts — then leverages the resulting discomfort.',
        'Reciprocity. The obligation to return favors is one of the most hardwired social responses in human psychology.',
        '"After everything I\'ve done for you..."  ·  Excessive helpfulness that later becomes leverage',
        'The favor is disproportionate to the relationship, arrives before a request, or is deployed after you resist.',
        'You are not obligated to repay what you did not ask for. Gratitude is appropriate; compliance is not.'))

    story.extend(arch_card('03', 'Guilt',
        'Frames your preferences, limits, or decisions as evidence of moral failure — selfishness, disloyalty, ingratitude, or cruelty.',
        'The pain of self-condemnation. Guilt is effective because it is internally produced — the target condemns themselves.',
        '"I guess I\'m just not important to you"  ·  "Fine, don\'t worry about me"  ·  "You\'re choosing that over me?"',
        'Guilt-tripping conflates your preference with a moral offense. It requires you to accept the premise that your preference is wrong.',
        'Ask: <i>"Have I actually done something wrong, or am I just not doing what this person wants?"</i> These are different things.'))

    story.extend(arch_card('04', 'Intermittent Reward',
        'Alternates between warmth/approval and coldness/criticism on an unpredictable schedule — creating an anxious attachment loop.',
        'Variable ratio reinforcement. The same mechanism that makes slot machines compelling — unpredictable reward makes pursuit more intense, not less.',
        'Hot and cold behavioral cycles  ·  Praise followed by sudden withdrawal  ·  "Walking on eggshells"',
        'You feel more focused on managing the other person\'s moods than pursuing your own goals.',
        'Name the pattern to yourself. Chart the cycle — warmth, coldness, pursuit, reward, warmth again. Seeing the cycle breaks the spell.'))

    story.extend(arch_card('05', 'Social Proof',
        'Uses real or implied group behavior to make a specific choice seem like the obvious, rational, or safe option.',
        'Conformity instinct. In conditions of uncertainty, humans default to what others are doing as a proxy for correctness.',
        '"Everyone in our industry is moving to this"  ·  "Most people just agree without making it complicated"',
        'The "everyone" claim is never specific. Ask who, exactly, agrees — and what their actual circumstances are.',
        'Popularity is not proof of quality. Ask: <i>"Does this make sense for my specific situation?"</i> — not <i>"Is this what most people do?"</i>'))

    story.extend(arch_card('06', 'Identity Hijack',
        'Frames a behavior as an expression of who you are — then uses your self-concept to compel compliance or block resistance.',
        'Identity consistency. People will do more to remain consistent with their self-image than to gain material rewards.',
        '"A real leader would make this call"  ·  "I thought you were the kind of person who..."',
        'The argument is about who you ARE, not about whether the decision is actually good.',
        'Ask: <i>"Is this actually consistent with my values — or is someone using my values against me?"</i>'))

    story.extend(arch_card('07', 'Manufactured Urgency',
        'Compresses the decision timeline artificially to prevent careful analysis and force compliance before the target can consult alternatives.',
        'Cognitive overload. Under time pressure, humans abandon deliberative thinking and rely on heuristics — making them far more susceptible to suggestion.',
        '"I need an answer by end of day"  ·  "If you don\'t decide now, I\'ll have to move on"',
        'Legitimate urgency has external, verifiable causes. Manufactured urgency is created by the other party and cannot be independently confirmed.',
        'Say: <i>"Let me take 24 hours."</i> Resistance to this pause is itself diagnostic.'))

    story.append(PageBreak())

    # ── CHAPTER 3 ───────────────────────────
    story.extend(chapter_header('CHAPTER 03', 'The Tactic Recognition Ladder',
        'A real-time 4-rung system for identifying manipulation during a conversation — before you\'ve already responded.'))

    story.extend(ladder_diagram())

    story.append(Paragraph('Rung 1: Pause on the Feeling', S['h3']))
    story.append(Paragraph(
        '<b>Signal:</b> An unexpected emotion — urgency, guilt, obligation, shame, or fear — '
        'in response to something someone said or did. <b>Action:</b> Pause. Name the feeling '
        'explicitly to yourself: <i>"I am feeling pressured / guilty / obligated right now."</i> '
        'Naming an emotion reduces its automatic pull on behavior.', S['body']))

    story.append(Paragraph('Rung 2: Notice the Emotional Signal', S['h3']))
    story.append(Paragraph(
        '<b>Questions:</b> Who benefits from me feeling this? Is this emotion coming from inside '
        '(my values, my genuine preferences) or outside (someone else\'s framing)? '
        'Would I feel this way if no one was watching or asking?', S['body']))

    story.append(Paragraph('Rung 3: Test the Pattern', S['h3']))
    story.append(sp(8))
    story.append(data_table(
        ['If you notice...', 'Likely Architecture'],
        [
            ['Artificial time pressure', 'Manufactured Urgency or Scarcity'],
            ['Felt debt or obligation', 'Obligation Architecture'],
            ['Being told you\'re a bad person', 'Guilt Architecture'],
            ['Your identity being invoked', 'Identity Hijack'],
            ['"Everyone else agrees" claims', 'Social Proof'],
        ],
        [CONTENT_W * 0.50, CONTENT_W * 0.50]
    ))

    story.append(sp(12))
    story.append(Paragraph('Rung 4: Confirm the Tactic', S['h3']))
    story.append(Paragraph(
        'The pattern fits. You know what you\'re dealing with. Move to the Neutralization Protocol. '
        'You are no longer operating on instinct — you are operating on information.', S['body']))

    story.extend(callout('KEY INSIGHT',
        'You do not need 100% certainty. A strong pattern match is enough to justify moving to '
        'Neutralization. Waiting for certainty is itself a manipulation trap.'))

    story.append(PageBreak())

    # ── CHAPTER 4 ───────────────────────────
    story.extend(chapter_header('CHAPTER 04', 'The Neutralization Protocol',
        'A 3-step response system that does not escalate, does not require accusation, '
        'and restores your autonomy without burning the relationship.'))

    story.extend(protocol_step('1', 'Name It — Internally',
        'Label the tactic explicitly in your own mind. Labeling activates prefrontal processing '
        '(deliberate thought) and reduces the automatic emotional response generated by the limbic '
        'system. You move from reactive to analytical. This step is private — you are not accusing '
        'anyone. You are orienting yourself.',
        ['"This is a guilt trip."',
         '"This is manufactured urgency."',
         '"This is an identity hijack."']))

    story.extend(protocol_step('2', 'Pause It — Externally',
        'Create time and space before you respond. Manufactured urgency depends on you not having '
        'time to think. Every extra minute reduces the tactic\'s effectiveness. '
        'If the person resists your request for time: that resistance is itself diagnostic.',
        ['"I need to think about this before I respond."',
         '"Let me come back to you on that."',
         '"I\'ll have an answer for you by [specific time]."']))

    story.extend(protocol_step('3', 'Redirect It — Externally',
        'Shift the conversation from the emotional pressure frame to a factual or logical frame. '
        'Manipulation operates in the emotional register. Redirecting to facts moves the conversation '
        'to ground where manipulation has less leverage.',
        ['"Help me understand the actual timeline — what changes if I respond tomorrow?"',
         '"I want to make a decision that works for both of us. What\'s the core concern?"',
         '"I\'m going to set the emotion aside and just look at what makes sense practically."']))

    story.append(sp(8))
    story.append(data_table(
        ['Step', 'Internal/External', 'Action', 'Purpose'],
        [
            ['1. Name It', 'Internal', 'Label the tactic', 'Activate deliberate thinking'],
            ['2. Pause It', 'External', 'Buy time', 'Break the urgency loop'],
            ['3. Redirect It', 'External', 'Shift to substance', 'Remove emotional leverage'],
        ],
        [CONTENT_W * 0.2, CONTENT_W * 0.22, CONTENT_W * 0.28, CONTENT_W * 0.30]
    ))

    story.append(PageBreak())

    # ── CHAPTER 5 ───────────────────────────
    story.extend(chapter_header('CHAPTER 05', 'The Workplace Manipulation Index',
        'Professional environments are among the most common contexts for manipulation — '
        'because power differentials and career stakes make resistance feel costly.'))

    story.extend(bias_card('TACTIC 01', 'Goalpost Shifting',
        '<b>What It Looks Like:</b> Standards or criteria change after you\'ve met the previous version. You achieve the target; the target moves.',
        '<b>The Hidden Message:</b> <i>"You can never fully satisfy the requirement — keeping you in a permanent state of striving and compliance."</i>',
        '<b>Counter:</b> Document agreements in writing. When goalposts shift, reference the original: <i>"My understanding was X. Has that changed?"</i>'))

    story.extend(bias_card('TACTIC 02', 'The Credit Absorb',
        '<b>What It Looks Like:</b> Your work, ideas, or contributions are claimed or downplayed by someone with more organizational power.',
        '<b>Counter:</b> Create a visible record of your contributions. Build lateral visibility with peers so your contribution is known through multiple channels.'))

    story.extend(bias_card('TACTIC 03', 'Selective Inclusion',
        '<b>What It Looks Like:</b> Information, opportunities, or meetings are shared selectively to create dependency — then used as leverage.',
        '<b>Counter:</b> Build information networks independent of the gatekeeper. Never allow a single person to be your only source of organizational context.'))

    story.extend(bias_card('TACTIC 04', 'The Double Bind',
        '<b>What It Looks Like:</b> Two options are presented, both resulting in negative outcomes for you — then you\'re blamed for whichever you choose.',
        '<b>Example:</b> <i>"If you take time off, you\'re not committed. If you don\'t, you\'ll burn out — and that\'s your fault."</i>',
        '<b>Counter:</b> Refuse the frame. Double binds only sustain when the target accepts both options as the only options. There is almost always a third.'))

    story.extend(bias_card('TACTIC 05', 'Weaponized Feedback',
        '<b>What It Looks Like:</b> Critical feedback delivered in front of others, timed to maximize discomfort, or embedded with personal attacks within professional critique.',
        '<b>Counter:</b> Separate substance from delivery. Extract what is actionable. Address the emotional attack separately, in private, when you can approach it without defensiveness.'))

    story.extend(bias_card('TACTIC 06', 'False Consensus Building',
        '<b>What It Looks Like:</b> Claims that "everyone agrees" or "leadership sees it this way" are used to preempt your objection without actual consultation.',
        '<b>Counter:</b> Verify directly. <i>"Who specifically was part of that decision?"</i> Unverified consensus claims almost always collapse under direct, calm inquiry.'))

    story.append(PageBreak())

    # ── CHAPTER 6 ───────────────────────────
    story.extend(chapter_header('CHAPTER 06', 'The Relationship Manipulation Decoder',
        'Personal relationships are where manipulation causes the most lasting damage — '
        'because love, loyalty, and connection make us most willing to override our own judgment.'))

    story.extend(bias_card('PATTERN 01', 'Gaslighting',
        'Your perception of events is repeatedly denied, minimized, or reframed until you doubt your own memory and judgment.',
        '<b>Recognition Signs:</b> You frequently doubt your own memory. You apologize for things you\'re fairly sure didn\'t happen. Disagreements always end with you questioning yourself, not the other person.',
        '<b>Counter:</b> Keep a private record. Write down what happened immediately — before the reframing begins. The record is for your own orientation, not confrontation.'))

    story.extend(bias_card('PATTERN 02', 'Love Bombing + Withdrawal Cycling',
        'Excessive early attention and idealization followed by withdrawal or criticism. The contrast creates a powerful emotional gradient the brain interprets as significance.',
        '<b>Recognition Signs:</b> The relationship felt "too good" unusually fast. Affection fluctuates dramatically. You expend energy trying to return to the early "high."',
        '<b>Counter:</b> Assess consistency over time, not intensity at a single moment. A stable, slightly less intense connection is worth more than a volatile, highly intense one.'))

    story.extend(bias_card('PATTERN 03', 'Triangulation',
        'A third party — real or implied — is used to induce jealousy or insecurity and make you work harder for validation.',
        '<b>Counter:</b> Your worth in a relationship should not be determined by comparison to unnamed others. When triangulation is used, redirect: <i>"What\'s the actual concern here?"</i>'))

    story.extend(bias_card('PATTERN 04', 'Manufactured Helplessness',
        'The other person consistently positions themselves as incapable without you — creating obligation through dependency framing.',
        '<b>Counter:</b> Compassion does not require unlimited availability. Their distress in response to your limits is information about them, not evidence of your wrongdoing.'))

    story.extend(bias_card('PATTERN 05', 'Norm Erosion',
        'Limits are tested incrementally — small transgressions followed by apology, then slightly larger ones — until your original standards feel like overreactions.',
        '<b>Counter:</b> Compare where you are now to where you <i>started</i> — not where you were last week. Ask: <i>"Would I have accepted this at the beginning of this relationship?"</i>'))

    story.append(PageBreak())

    # ── CHAPTER 7 ───────────────────────────
    story.extend(chapter_header('CHAPTER 07', 'The Cognitive Bias Exploitation Map',
        'Manipulators exploit predictable flaws in human reasoning. These are not personality weaknesses — '
        'they are features of how all human brains process information.'))

    story.extend(bias_card('BIAS 01', 'Anchoring',
        'The first number or framing presented becomes the reference point — even if the anchor is arbitrary. The "door in the face" technique uses an extreme initial ask to make a smaller follow-up seem reasonable.',
        '<b>Counter:</b> Before any negotiation, establish your own anchor independently. What is this worth to you, without any external reference?'))

    story.extend(bias_card('BIAS 02', 'Sunk Cost Exploitation',
        'The more you\'ve invested, the harder it becomes to walk away — even when walking away is clearly the better decision.',
        '<b>Counter:</b> Past investment is irrelevant to present decisions. The only relevant question: <i>"Given where I am now, what\'s the best next move?"</i>'))

    story.extend(bias_card('BIAS 03', 'Reciprocity Exploitation',
        'The social obligation to return favors is weaponized through unsolicited gifts or strategic generosity that creates felt debt.',
        '<b>Counter:</b> You are not obligated to repay what you did not request. Saying "thank you" is sufficient. You can accept a gift and still decline the implied obligation.'))

    story.extend(bias_card('BIAS 04', 'Authority Bias',
        'Credentials, titles, or signals of expertise are used to bypass critical evaluation — even in domains outside genuine expertise.',
        '<b>Counter:</b> Ask: <i>"Is this person actually expert in this specific claim?"</i> — not just <i>"Are they generally impressive?"</i>'))

    story.extend(bias_card('BIAS 05', 'Framing Effects',
        '"90% success rate" vs. "10% failure rate" — identical content, different emotional loading. Identical information in different frames produces different responses.',
        '<b>Counter:</b> Translate every framed statement into its neutral, factual equivalent. What is actually being said, stripped of emotional loading?'))

    story.append(PageBreak())

    # ── CHAPTER 8 ───────────────────────────
    story.extend(chapter_header('CHAPTER 08', 'The Emotional Hook Anatomy',
        'Every manipulation attempt operates through the same mechanism: '
        'emotion is activated before logic can engage. This is the master key.'))

    story.extend(sequence_diagram([
        ('STAGE 01', 'Trigger', False),
        ('STAGE 02', 'Emotion', False),
        ('INTERVENE HERE', 'Interpretation', True),
        ('STAGE 04', 'Behavior', False),
    ]))

    story.extend(callout('THE ONLY RELIABLE INTERVENTION POINT',
        'The only reliable intervention point is between Stage 2 and Stage 3. '
        'Once you feel something, you cannot un-feel it. But you can pause before interpreting — '
        'and that pause is where your autonomy lives.'))

    story.append(Paragraph('Emotional Hooks by Architecture', S['h3']))
    story.append(sp(8))
    story.append(data_table(
        ['Architecture', 'Primary Emotion', 'Secondary Emotion'],
        [
            ['Scarcity', 'Fear (of loss)', 'Anxiety'],
            ['Obligation', 'Shame', 'Discomfort'],
            ['Guilt', 'Self-condemnation', 'Fear of judgment'],
            ['Intermittent Reward', 'Anxiety', 'Hope'],
            ['Social Proof', 'Fear (of exclusion)', 'Shame'],
            ['Identity Hijack', 'Pride / Fear', 'Shame'],
            ['Manufactured Urgency', 'Fear', 'Panic'],
        ],
        [CONTENT_W * 0.34, CONTENT_W * 0.33, CONTENT_W * 0.33]
    ))

    story.append(sp(16))
    story.extend(pull_quote(
        'Tactic + Emotional Hook + Compressed Timeline = Compliance\n'
        'Remove any one element — and the formula fails.',
        'The Manipulation Formula'))

    story.append(PageBreak())

    # ── CHAPTER 9 ───────────────────────────
    story.extend(chapter_header('CHAPTER 09', 'Manipulation vs. Influence',
        'Where is the ethical line? This distinction matters for protecting yourself — '
        'and for auditing your own communication.'))

    story.append(compare_table([
        ('Transparency', 'Hides its mechanism', 'Open about its intent'),
        ('Consent', 'Bypasses it', 'Respects it'),
        ('Information', 'Distorts or withholds', 'Accurate and complete'),
        ('Autonomy', 'Overrides it', 'Enhances it'),
        ('Who Benefits', 'The influencer', 'Can benefit both parties'),
        ('How You Feel After', 'Coerced, regretful', 'Informed, empowered'),
    ]))

    story.append(sp(16))
    story.extend(pull_quote(
        '"If this person fully understood what I was doing and why,\nwould they still consider it fair?"',
        'The definitive test question for ethical influence'))

    story.append(Paragraph('Your Own Communication Audit', S['h3']))
    story.append(sp(8))
    story.append(checklist([
        '<b>Accuracy Check:</b> Is everything I\'m presenting factually true?',
        '<b>Completeness Check:</b> Am I withholding information that would change their decision?',
        '<b>Autonomy Check:</b> Am I enhancing their ability to decide freely, or restricting it?',
        '<b>Motive Check:</b> If this person knew my intent, would they consider it fair?',
    ]))

    story.append(PageBreak())

    # ── CHAPTER 10 ──────────────────────────
    story.extend(chapter_header('CHAPTER 10', 'Your Psychological Defense Stack',
        'Everything in this guide, compressed into a single reference framework '
        'you can use immediately.'))

    story.extend(summary_box([
        'Know the 7 Architectures: Scarcity · Obligation · Guilt · Intermittent Reward · Social Proof · Identity Hijack · Manufactured Urgency',
        'Use the 4-Rung Recognition Ladder: Pause · Notice · Test · Confirm',
        'Apply the 3-Step Neutralization Protocol: Name it · Pause it · Redirect it',
    ]))

    story.append(Paragraph('Daily Defense Checklist', S['h2']))

    story.append(Paragraph('Before High-Stakes Interactions', S['h3']))
    story.append(sp(8))
    story.append(checklist([
        'Identify the most likely tactic given the context',
        'Set your anchor / preferred outcome independently',
        'Decide in advance how you will create space if pressured',
    ]))

    story.append(sp(12))
    story.append(Paragraph('During Interactions', S['h3']))
    story.append(sp(8))
    story.append(checklist([
        'Notice unexpected emotions before acting on them',
        'Use pause phrases if you feel pressure',
        'Redirect from emotional to substantive framing',
    ]))

    story.append(sp(12))
    story.append(Paragraph('After Interactions', S['h3']))
    story.append(sp(8))
    story.append(checklist([
        'Audit: did I decide freely, or in response to pressure?',
        'Note which tactics were used — pattern recognition builds over time',
        'Recalibrate any agreements made under pressure',
    ]))

    story.append(sp(16))
    story.append(Paragraph('Context-Specific Defenses', S['h2']))
    story.append(sp(8))
    story.append(data_table(
        ['Context', 'Primary Defenses'],
        [
            ['Workplace', 'Document agreements · Build lateral visibility · Name double binds · Separate feedback substance from delivery'],
            ['Relationships', 'Chart consistency over time · Keep private records · Compare to starting point · Maintain defensible limits'],
            ['Cognitive Exploits', 'Set your own anchor first · Evaluate on future outcomes · Translate framed statements · Verify authority claims in their specific domain'],
        ],
        [CONTENT_W * 0.22, CONTENT_W * 0.78]
    ))

    # ── CLOSING PAGE ────────────────────────
    story.append(PageBreak())
    story.append(ClosingPageMarker())
    story.append(Spacer(1, 1))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'PDF generated: {OUTPUT}')


if __name__ == '__main__':
    build()
