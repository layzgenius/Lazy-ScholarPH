"""
Premium PDF Generator for Lazy Scholar PH
Converts markdown draft to a premium-styled PDF using ReportLab.
"""
import re
import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak,
    Table, TableStyle, ListFlowable, ListItem, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Brand Colors ───────────────────────────────────────────────────────────
BRAND_DARK    = colors.HexColor("#1A1A2E")   # Deep navy
BRAND_MID     = colors.HexColor("#16213E")   # Darker navy
BRAND_ACCENT  = colors.HexColor("#E94560")   # Vibrant rose
BRAND_GOLD    = colors.HexColor("#F0A500")   # Warm gold
BRAND_LIGHT   = colors.HexColor("#F5F5F5")   # Off-white
BRAND_SUBTLE  = colors.HexColor("#E8E8EE")   # Light grey
BRAND_TEXT    = colors.HexColor("#1A1A2E")   # Main text
BRAND_MUTED   = colors.HexColor("#6B7280")   # Secondary text
WHITE         = colors.white

PAGE_W, PAGE_H = A4
MARGIN_LEFT   = 2.2 * cm
MARGIN_RIGHT  = 2.2 * cm
MARGIN_TOP    = 2.0 * cm
MARGIN_BOTTOM = 2.0 * cm


class NumberedCanvas(canvas.Canvas):
    """Canvas that adds header/footer to every page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        page_num = self._pageNumber
        w, h = A4

        # Skip cover page decoration
        if page_num == 1:
            return

        # Header line
        self.setStrokeColor(BRAND_ACCENT)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, h - 14 * mm, w - MARGIN_RIGHT, h - 14 * mm)

        # Header brand name
        self.setFont("Helvetica", 7)
        self.setFillColor(BRAND_MUTED)
        self.drawString(MARGIN_LEFT, h - 12 * mm, "LAZY SCHOLAR PH")
        self.drawRightString(w - MARGIN_RIGHT, h - 12 * mm, "THE DISCIPLINE ARCHITECTURE")

        # Footer line
        self.setStrokeColor(BRAND_SUBTLE)
        self.line(MARGIN_LEFT, 12 * mm, w - MARGIN_RIGHT, 12 * mm)

        # Footer page number
        self.setFont("Helvetica", 8)
        self.setFillColor(BRAND_MUTED)
        page_text = f"{page_num - 1}"  # offset for cover
        self.drawCentredString(w / 2, 7 * mm, page_text)


class SectionDivider(Flowable):
    """A premium branded section divider."""

    def __init__(self, label="", width=None):
        super().__init__()
        self.label = label
        self.width = width or (PAGE_W - MARGIN_LEFT - MARGIN_RIGHT)
        self.height = 18 * mm

    def draw(self):
        c = self.canv
        w = self.width

        # Full-width accent bar
        c.setFillColor(BRAND_ACCENT)
        c.rect(0, self.height - 4 * mm, w, 1.2 * mm, stroke=0, fill=1)

        if self.label:
            # Label pill background
            label_w = len(self.label) * 5.5 + 16
            c.setFillColor(BRAND_DARK)
            c.roundRect(0, self.height - 10 * mm, label_w, 8 * mm, 2 * mm, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(8, self.height - 6 * mm, self.label)


class CalloutBox(Flowable):
    """A styled pull-quote / callout box."""

    def __init__(self, text, width=None, style="accent"):
        super().__init__()
        self.text = text
        self.width = width or (PAGE_W - MARGIN_LEFT - MARGIN_RIGHT)
        self.style = style  # "accent", "gold", "dark"
        self._calc_height()

    def _calc_height(self):
        chars_per_line = int(self.width / 4.8)
        lines = max(1, len(self.text) // chars_per_line + self.text.count('\n') + 1)
        self.height = (lines * 13 + 28) * 0.352778 * mm * 2.8

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height

        bg = BRAND_DARK if self.style == "dark" else (
            colors.HexColor("#FFF8E7") if self.style == "gold" else colors.HexColor("#FFF1F3")
        )
        accent = BRAND_GOLD if self.style == "gold" else BRAND_ACCENT

        # Background
        c.setFillColor(bg)
        c.roundRect(0, 0, w, h, 3 * mm, stroke=0, fill=1)

        # Left accent stripe
        c.setFillColor(accent)
        c.rect(0, 0, 3 * mm, h, stroke=0, fill=1)

        # Quote mark
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(accent)
        c.drawString(8 * mm, h - 10 * mm, "“")

        # Text
        text_color = WHITE if self.style == "dark" else BRAND_TEXT
        c.setFillColor(text_color)
        c.setFont("Helvetica-BoldOblique" if self.style == "accent" else "Helvetica-Bold", 10)
        text_x = 8 * mm
        text_y = h - 16 * mm
        line_h = 5.5 * mm
        max_w = w - 16 * mm

        words = self.text.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if c.stringWidth(test, "Helvetica-Bold", 10) < max_w:
                line = test
            else:
                if line:
                    c.drawString(text_x, text_y, line)
                    text_y -= line_h
                line = word
        if line:
            c.drawString(text_x, text_y, line)


def build_styles():
    """Build the full style sheet."""
    base = getSampleStyleSheet()

    styles = {}

    styles["h1"] = ParagraphStyle(
        "h1",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=BRAND_DARK,
        spaceAfter=8 * mm,
        spaceBefore=4 * mm,
        leading=34,
        alignment=TA_LEFT,
    )
    styles["h2"] = ParagraphStyle(
        "h2",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=BRAND_DARK,
        spaceAfter=5 * mm,
        spaceBefore=10 * mm,
        leading=26,
        alignment=TA_LEFT,
        borderPadding=(0, 0, 3, 0),
    )
    styles["h3"] = ParagraphStyle(
        "h3",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=BRAND_ACCENT,
        spaceAfter=3 * mm,
        spaceBefore=6 * mm,
        leading=18,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10.5,
        textColor=BRAND_TEXT,
        spaceAfter=3.5 * mm,
        spaceBefore=1 * mm,
        leading=17,
        alignment=TA_JUSTIFY,
    )
    styles["body_bold"] = ParagraphStyle(
        "body_bold",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        textColor=BRAND_TEXT,
        spaceAfter=3.5 * mm,
        spaceBefore=1 * mm,
        leading=17,
        alignment=TA_LEFT,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=10.5,
        textColor=BRAND_TEXT,
        spaceAfter=2 * mm,
        spaceBefore=0,
        leading=16,
        leftIndent=5 * mm,
        bulletIndent=0,
        alignment=TA_LEFT,
    )
    styles["numbered"] = ParagraphStyle(
        "numbered",
        fontName="Helvetica",
        fontSize=10.5,
        textColor=BRAND_TEXT,
        spaceAfter=2.5 * mm,
        spaceBefore=0,
        leading=16,
        leftIndent=8 * mm,
        firstLineIndent=-8 * mm,
    )
    styles["checklist"] = ParagraphStyle(
        "checklist",
        fontName="Helvetica",
        fontSize=10,
        textColor=BRAND_TEXT,
        spaceAfter=2 * mm,
        spaceBefore=0,
        leading=15,
        leftIndent=5 * mm,
    )
    styles["toc_h1"] = ParagraphStyle(
        "toc_h1",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=BRAND_DARK,
        spaceAfter=2 * mm,
        spaceBefore=3 * mm,
        leading=15,
    )
    styles["toc_body"] = ParagraphStyle(
        "toc_body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=BRAND_MUTED,
        spaceAfter=1 * mm,
        spaceBefore=0,
        leading=14,
        leftIndent=4 * mm,
    )
    styles["label"] = ParagraphStyle(
        "label",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=BRAND_ACCENT,
        spaceAfter=1 * mm,
        spaceBefore=4 * mm,
        leading=12,
        tracking=1,
    )
    styles["caption"] = ParagraphStyle(
        "caption",
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=BRAND_MUTED,
        spaceAfter=2 * mm,
        spaceBefore=1 * mm,
        leading=13,
        alignment=TA_CENTER,
    )

    return styles


def make_cover_page(styles):
    """Build the cover page elements."""
    elements = []

    # Top accent bar via spacer + will use SectionDivider approach inline
    elements.append(Spacer(1, 2 * cm))

    # BRAND LABEL
    elements.append(Paragraph(
        "<font color='#E94560'><b>LAZY SCHOLAR PH</b></font>",
        ParagraphStyle("brand", fontName="Helvetica-Bold", fontSize=9,
                       textColor=BRAND_ACCENT, alignment=TA_CENTER,
                       spaceAfter=6 * mm, tracking=3)
    ))

    # Main title
    elements.append(Paragraph(
        "THE DISCIPLINE<br/>ARCHITECTURE",
        ParagraphStyle("cover_title", fontName="Helvetica-Bold", fontSize=42,
                       textColor=BRAND_DARK, alignment=TA_CENTER,
                       spaceAfter=4 * mm, leading=50)
    ))

    # Gold accent line
    elements.append(HRFlowable(
        width="40%", thickness=3, color=BRAND_GOLD,
        spaceAfter=6 * mm, spaceBefore=2 * mm, hAlign="CENTER"
    ))

    # Subtitle
    elements.append(Paragraph(
        "Build the System That Makes Consistency Automatic",
        ParagraphStyle("cover_sub", fontName="Helvetica-BoldOblique", fontSize=15,
                       textColor=BRAND_MUTED, alignment=TA_CENTER,
                       spaceAfter=10 * mm, leading=22)
    ))

    # Tagline box
    tagline_data = [["Stop relying on motivation. Start designing behavior."]]
    tagline_table = Table(tagline_data, colWidths=[12 * cm])
    tagline_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-BoldOblique"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [5, 5, 5, 5]),
    ]))
    tagline_table.hAlign = "CENTER"
    elements.append(tagline_table)

    elements.append(Spacer(1, 10 * mm))

    # Feature pills
    features = ["Identity Systems", "Environment Design", "Friction Engineering", "30-Day Build"]
    feat_data = [[f"  {f}  " for f in features]]
    feat_table = Table(feat_data, colWidths=[3.8 * cm] * 4)
    feat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_SUBTLE),
        ("TEXTCOLOR", (0, 0), (-1, -1), BRAND_DARK),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, WHITE),
        ("BOX", (0, 0), (-1, -1), 0, WHITE),
    ]))
    feat_table.hAlign = "CENTER"
    elements.append(feat_table)

    elements.append(Spacer(1, 6 * cm))

    # Bottom brand line
    elements.append(HRFlowable(
        width="100%", thickness=0.5, color=BRAND_SUBTLE,
        spaceAfter=4 * mm, spaceBefore=4 * mm
    ))
    elements.append(Paragraph(
        "lazyscholarph.com  ·  A Lazy Scholar PH Premium Resource",
        ParagraphStyle("cover_footer", fontName="Helvetica", fontSize=8,
                       textColor=BRAND_MUTED, alignment=TA_CENTER)
    ))

    elements.append(PageBreak())
    return elements


def make_toc(styles):
    """Build a visual table of contents."""
    elements = []

    elements.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle(
        "toc_title", fontName="Helvetica-Bold", fontSize=22,
        textColor=BRAND_DARK, spaceAfter=8 * mm, spaceBefore=4 * mm
    )))

    elements.append(HRFlowable(width="100%", thickness=1.5, color=BRAND_ACCENT,
                                spaceAfter=6 * mm))

    sections = [
        ("INTRODUCTION", "The Real Reason You Keep Restarting", "3"),
        ("SECTION 1", "Why Willpower Always Fails", "5"),
        ("SECTION 2", "Identity Architecture", "8"),
        ("SECTION 3", "Environment Design for Automatic Behavior", "11"),
        ("SECTION 4", "The Anti-Chaos Routine System", "15"),
        ("SECTION 5", "Friction Engineering", "19"),
        ("SECTION 6", "The Restart Protocol", "22"),
        ("SECTION 7", "30-Day Discipline Architecture Build", "25"),
        ("SUMMARY", "Your Discipline Architecture at a Glance", "29"),
        ("CLOSING", "Final Words from Lazy Scholar PH", "31"),
    ]

    for label, title, page in sections:
        row_data = [[
            Paragraph(f"<font color='#E94560'><b>{label}</b></font>",
                      ParagraphStyle("toc_lbl", fontName="Helvetica-Bold", fontSize=8,
                                     textColor=BRAND_ACCENT, leading=12)),
            Paragraph(f"<b>{title}</b>",
                      ParagraphStyle("toc_t", fontName="Helvetica-Bold", fontSize=10.5,
                                     textColor=BRAND_DARK, leading=15)),
            Paragraph(f"<font color='#6B7280'>{page}</font>",
                      ParagraphStyle("toc_p", fontName="Helvetica", fontSize=10,
                                     textColor=BRAND_MUTED, alignment=TA_RIGHT, leading=15)),
        ]]
        toc_row = Table(row_data, colWidths=[3.2 * cm, 12 * cm, 1.5 * cm])
        toc_row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, BRAND_SUBTLE),
        ]))
        elements.append(toc_row)

    elements.append(PageBreak())
    return elements


def strip_md(text):
    """Strip markdown syntax for clean PDF text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    return text


def parse_markdown_to_elements(md_text, styles):
    """Parse markdown into ReportLab flowables."""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []
    in_checklist = False
    checklist_items = []
    in_numbered = False
    numbered_items = []
    in_bullets = False
    bullet_items = []

    def flush_list(elems):
        nonlocal in_bullets, bullet_items, in_numbered, numbered_items, in_checklist, checklist_items
        if in_bullets and bullet_items:
            for item in bullet_items:
                elems.append(Paragraph(f"<b>›</b>  {strip_md(item)}", styles["bullet"]))
            bullet_items = []
            in_bullets = False
        if in_numbered and numbered_items:
            for idx, item in enumerate(numbered_items, 1):
                elems.append(Paragraph(f"<b>{idx}.</b>  {strip_md(item)}", styles["numbered"]))
            numbered_items = []
            in_numbered = False
        if in_checklist and checklist_items:
            for item in checklist_items:
                elems.append(Paragraph(f"☐  {strip_md(item)}", styles["checklist"]))
            checklist_items = []
            in_checklist = False

    def flush_table(elems):
        nonlocal in_table, table_rows
        if not table_rows:
            return
        # Filter out separator rows
        clean_rows = [r for r in table_rows if not all(re.match(r'^[-:]+$', c.strip()) for c in r)]
        if not clean_rows:
            table_rows = []
            in_table = False
            return

        col_count = max(len(r) for r in clean_rows)
        col_w = (PAGE_W - MARGIN_LEFT - MARGIN_RIGHT - 1 * cm) / col_count

        formatted = []
        for ri, row in enumerate(clean_rows):
            fmt_row = []
            for ci, cell in enumerate(row):
                style_name = "body_bold" if ri == 0 else "body"
                p = Paragraph(strip_md(cell.strip()), styles[style_name])
                fmt_row.append(p)
            while len(fmt_row) < col_count:
                fmt_row.append(Paragraph("", styles["body"]))
            formatted.append(fmt_row)

        t = Table(formatted, colWidths=[col_w] * col_count, repeatRows=1)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("BACKGROUND", (0, 1), (-1, -1), BRAND_LIGHT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BRAND_LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.3, BRAND_SUBTLE),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
        t.setStyle(ts)
        elems.append(Spacer(1, 3 * mm))
        elems.append(t)
        elems.append(Spacer(1, 3 * mm))
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

        # Skip title page & TOC markers already handled
        if line.strip() in ("---",):
            flush_list(elements)
            flush_table(elements)
            elements.append(Spacer(1, 4 * mm))
            i += 1
            continue

        # Page break hint
        if line.strip() == "<!-- pagebreak -->":
            elements.append(PageBreak())
            i += 1
            continue

        # Heading 1 → section divider + h1
        if line.startswith("# ") and not line.startswith("## "):
            flush_list(elements)
            flush_table(elements)
            title = line[2:].strip()
            if title.upper() in ("TABLE OF CONTENTS", "TITLE PAGE"):
                i += 1
                continue
            elements.append(PageBreak())
            elements.append(SectionDivider(label=""))
            elements.append(Spacer(1, 4 * mm))
            elements.append(Paragraph(strip_md(title), styles["h1"]))
            i += 1
            continue

        # Heading 2
        if line.startswith("## "):
            flush_list(elements)
            flush_table(elements)
            title = line[3:].strip()
            elements.append(Spacer(1, 4 * mm))
            elements.append(Paragraph(strip_md(title), styles["h2"]))
            elements.append(HRFlowable(width="30%", thickness=2, color=BRAND_ACCENT,
                                       spaceAfter=3 * mm, hAlign="LEFT"))
            i += 1
            continue

        # Heading 3
        if line.startswith("### "):
            flush_list(elements)
            flush_table(elements)
            title = line[4:].strip()
            elements.append(Paragraph(strip_md(title), styles["h3"]))
            i += 1
            continue

        # Heading 4
        if line.startswith("#### "):
            flush_list(elements)
            flush_table(elements)
            title = line[5:].strip()
            elements.append(Paragraph(
                f"<b>{strip_md(title)}</b>",
                ParagraphStyle("h4", fontName="Helvetica-Bold", fontSize=11,
                               textColor=BRAND_DARK, spaceAfter=2 * mm,
                               spaceBefore=4 * mm, leading=16)
            ))
            i += 1
            continue

        # Blockquote → callout box
        if line.startswith("> "):
            flush_list(elements)
            flush_table(elements)
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = " ".join(quote_lines)
            elements.append(Spacer(1, 3 * mm))
            elements.append(CalloutBox(quote_text, style="accent"))
            elements.append(Spacer(1, 3 * mm))
            continue

        # Table
        if line.startswith("|"):
            flush_list(elements)
            in_table = True
            cells = [c.strip() for c in line.strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            flush_table(elements)
            continue

        # Checklist item
        if re.match(r'^- \[[ x]\] ', line):
            in_checklist = True
            text = re.sub(r'^- \[[ x]\] ', '', line)
            checklist_items.append(text)
            i += 1
            continue
        elif in_checklist and not line.strip().startswith("- ") and line.strip():
            flush_list(elements)

        # Numbered list
        if re.match(r'^\d+\. ', line):
            in_numbered = True
            text = re.sub(r'^\d+\. ', '', line)
            numbered_items.append(text)
            i += 1
            continue
        elif in_numbered and not re.match(r'^\d+\. ', line) and line.strip():
            flush_list(elements)

        # Bullet list
        if re.match(r'^[-*] ', line) and not re.match(r'^- \[', line):
            in_bullets = True
            text = re.sub(r'^[-*] ', '', line)
            bullet_items.append(text)
            i += 1
            continue
        elif in_bullets and not re.match(r'^[-*] ', line) and line.strip():
            flush_list(elements)

        # Blank line
        if not line.strip():
            flush_list(elements)
            flush_table(elements)
            elements.append(Spacer(1, 2 * mm))
            i += 1
            continue

        # Bold-only line (acts as label/emphasis)
        if re.match(r'^\*\*[^*]+\*\*$', line.strip()):
            flush_list(elements)
            flush_table(elements)
            elements.append(Paragraph(strip_md(line.strip()), styles["label"]))
            i += 1
            continue

        # Regular paragraph
        flush_table(elements)
        elements.append(Paragraph(strip_md(line.strip()), styles["body"]))
        i += 1

    flush_list(elements)
    flush_table(elements)
    return elements


def build_pdf(md_path: Path, pdf_path: Path):
    styles = build_styles()
    md_text = md_path.read_text(encoding="utf-8")

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP + 12 * mm,
        bottomMargin=MARGIN_BOTTOM + 10 * mm,
        title="The Discipline Architecture",
        author="Lazy Scholar PH",
        subject="Discipline, Habit Formation, Productivity",
        creator="Lazy Scholar PH",
    )

    story = []

    # Cover page
    story.extend(make_cover_page(styles))

    # Table of Contents
    story.extend(make_toc(styles))

    # Body content
    story.extend(parse_markdown_to_elements(md_text, styles))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated: {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    build_pdf(Path(sys.argv[1]), Path(sys.argv[2]))
