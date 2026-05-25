"""
Premium HTML Generator for Lazy Scholar PH
Converts markdown to a beautifully styled single-file HTML ebook.
"""
import re
import sys
from pathlib import Path


HTML_CSS = """
:root {
  --dark: #1A1A2E;
  --mid: #16213E;
  --accent: #E94560;
  --gold: #F0A500;
  --light: #F5F5F5;
  --subtle: #E8E8EE;
  --text: #1A1A2E;
  --muted: #6B7280;
  --white: #ffffff;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 17px;
  line-height: 1.75;
  color: var(--text);
  background: var(--white);
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px 80px;
}

/* ── Cover Page ─────────────────────────────────────────────────────── */
.cover {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(160deg, var(--dark) 0%, var(--mid) 100%);
  color: var(--white);
  padding: 60px 40px;
  margin: 0 -24px 60px;
  position: relative;
  overflow: hidden;
}

.cover::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 5px;
  background: linear-gradient(90deg, var(--accent), var(--gold));
}

.cover-brand {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 40px;
}

.cover-title {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: clamp(42px, 8vw, 72px);
  font-weight: 900;
  line-height: 1.05;
  color: var(--white);
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.cover-divider {
  width: 80px;
  height: 4px;
  background: var(--gold);
  border-radius: 2px;
  margin: 20px auto;
}

.cover-subtitle {
  font-size: 20px;
  font-style: italic;
  color: rgba(255,255,255,0.7);
  margin-bottom: 40px;
  max-width: 500px;
}

.cover-tagline {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  padding: 16px 32px;
  font-size: 15px;
  font-style: italic;
  color: rgba(255,255,255,0.9);
  margin-bottom: 50px;
}

.cover-pills {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.cover-pill {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 100px;
  padding: 6px 18px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: rgba(255,255,255,0.8);
}

.cover-footer {
  position: absolute;
  bottom: 24px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.35);
  letter-spacing: 1px;
}

/* ── Table of Contents ───────────────────────────────────────────────── */
.toc {
  background: var(--light);
  border-radius: 12px;
  padding: 40px 44px;
  margin: 60px 0;
}

.toc-title {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 24px;
}

.toc-item {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--subtle);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.toc-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--accent);
  text-transform: uppercase;
  min-width: 90px;
}

.toc-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--dark);
  flex: 1;
}

/* ── Typography ──────────────────────────────────────────────────────── */
h1 {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 36px;
  font-weight: 900;
  color: var(--dark);
  margin-top: 80px;
  margin-bottom: 8px;
  line-height: 1.15;
  letter-spacing: -0.5px;
  padding-top: 40px;
  border-top: 4px solid var(--accent);
}

h1 .section-label {
  display: block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 8px;
}

h2 {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 24px;
  font-weight: 800;
  color: var(--dark);
  margin-top: 52px;
  margin-bottom: 12px;
  line-height: 1.25;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--subtle);
}

h3 {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--accent);
  margin-top: 36px;
  margin-bottom: 10px;
}

h4 {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: var(--dark);
  margin-top: 28px;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

p {
  margin-bottom: 20px;
  color: var(--text);
}

strong { font-weight: 700; color: var(--dark); }
em { font-style: italic; }

/* ── Callout / Blockquote ────────────────────────────────────────────── */
blockquote {
  background: linear-gradient(135deg, #FFF1F3 0%, #FFF8F9 100%);
  border-left: 5px solid var(--accent);
  border-radius: 0 10px 10px 0;
  padding: 22px 28px 22px 32px;
  margin: 32px 0;
  position: relative;
}

blockquote::before {
  content: '"';
  position: absolute;
  top: 8px;
  left: 14px;
  font-size: 48px;
  font-family: Georgia, serif;
  color: var(--accent);
  opacity: 0.6;
  line-height: 1;
}

blockquote p {
  font-size: 17px;
  font-style: italic;
  font-weight: 600;
  color: var(--dark);
  margin: 0;
  padding-left: 16px;
}

/* ── Lists ───────────────────────────────────────────────────────────── */
ul, ol {
  margin: 16px 0 24px 0;
  padding-left: 28px;
}

li {
  margin-bottom: 10px;
  line-height: 1.65;
}

ul li::marker { color: var(--accent); font-size: 1.2em; }
ol li::marker { color: var(--accent); font-weight: 700; }

/* ── Checklist ───────────────────────────────────────────────────────── */
.checklist {
  list-style: none;
  padding-left: 0;
  background: var(--light);
  border-radius: 10px;
  padding: 20px 24px;
  margin: 24px 0;
}

.checklist li {
  padding-left: 32px;
  position: relative;
  margin-bottom: 12px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 15px;
}

.checklist li::before {
  content: '☐';
  position: absolute;
  left: 0;
  color: var(--accent);
  font-size: 17px;
  line-height: 1.4;
}

/* ── Tables ──────────────────────────────────────────────────────────── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 28px 0;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 14px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(26,26,46,0.08);
}

thead tr {
  background: var(--dark);
  color: var(--white);
}

thead th {
  padding: 14px 18px;
  text-align: left;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

tbody tr:nth-child(even) { background: var(--light); }
tbody tr:nth-child(odd) { background: var(--white); }

td {
  padding: 12px 18px;
  border-bottom: 1px solid var(--subtle);
  line-height: 1.55;
  vertical-align: top;
}

/* ── Section Divider ─────────────────────────────────────────────────── */
hr.section-rule {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), transparent);
  margin: 60px 0 40px;
}

hr {
  border: none;
  height: 1px;
  background: var(--subtle);
  margin: 40px 0;
}

/* ── Frameworks / Callout Cards ──────────────────────────────────────── */
.framework-card {
  background: var(--dark);
  color: var(--white);
  border-radius: 12px;
  padding: 28px 32px;
  margin: 32px 0;
}

.framework-card h4 {
  color: var(--gold);
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 14px;
  letter-spacing: 1px;
}

.framework-card p, .framework-card li {
  color: rgba(255,255,255,0.85);
  font-size: 15px;
}

/* ── Closing Page ────────────────────────────────────────────────────── */
.closing {
  background: linear-gradient(160deg, var(--dark), var(--mid));
  color: var(--white);
  padding: 60px 50px;
  border-radius: 16px;
  margin: 80px -24px 0;
  text-align: center;
}

.closing h2 {
  color: var(--white);
  border: none;
  font-size: 30px;
  margin-top: 0;
}

.closing p { color: rgba(255,255,255,0.8); font-size: 17px; }

.closing-brand {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--accent);
  text-transform: uppercase;
  margin-top: 40px;
}

/* ── Print / PDF Optimization ────────────────────────────────────────── */
@media print {
  body { max-width: 100%; padding: 0; font-size: 12pt; }
  h1 { page-break-before: always; }
  blockquote, .checklist, table { page-break-inside: avoid; }
  .cover { page-break-after: always; min-height: auto; padding: 120px 60px; }
}
"""


def md_inline(text):
    """Convert inline markdown to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def md_to_html(md_text):
    """Convert full markdown document to HTML body content."""
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    in_ul = False
    in_ol = False
    in_checklist = False
    in_table = False
    table_rows = []
    in_blockquote = False
    bq_lines = []

    section_num = 0
    section_labels = {
        0: "INTRODUCTION",
        1: "SECTION 1",
        2: "SECTION 2",
        3: "SECTION 3",
        4: "SECTION 4",
        5: "SECTION 5",
        6: "SECTION 6",
        7: "SECTION 7",
        8: "SUMMARY",
        9: "CLOSING",
    }

    def close_lists():
        nonlocal in_ul, in_ol, in_checklist
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False
        if in_checklist:
            html_parts.append("</ul>")
            in_checklist = False

    def flush_bq():
        nonlocal in_blockquote, bq_lines
        if in_blockquote:
            content = " ".join(bq_lines)
            html_parts.append(f'<blockquote><p>{md_inline(content)}</p></blockquote>')
            bq_lines = []
            in_blockquote = False

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        clean = [r for r in table_rows if not all(re.match(r'^[-:]+$', c.strip()) for c in r)]
        if not clean:
            table_rows = []
            in_table = False
            return
        html_parts.append('<table>')
        for ri, row in enumerate(clean):
            tag = 'thead' if ri == 0 else ('tbody' if ri == 1 else '')
            if ri == 0:
                html_parts.append('<thead><tr>')
                for cell in row:
                    html_parts.append(f'<th>{md_inline(cell.strip())}</th>')
                html_parts.append('</tr></thead><tbody>')
            else:
                html_parts.append('<tr>')
                for cell in row:
                    html_parts.append(f'<td>{md_inline(cell.strip())}</td>')
                html_parts.append('</tr>')
        html_parts.append('</tbody></table>')
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

        # Blockquote
        if line.startswith('> '):
            close_lists()
            flush_table()
            in_blockquote = True
            bq_lines.append(line[2:])
            i += 1
            continue
        elif in_blockquote:
            flush_bq()

        # Table
        if line.startswith('|'):
            close_lists()
            in_table = True
            cells = [c.strip() for c in line.strip('|').split('|')]
            table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            flush_table()

        # HR
        if line.strip() == '---':
            close_lists()
            html_parts.append('<hr class="section-rule">')
            i += 1
            continue

        # H1
        if re.match(r'^# [^#]', line):
            close_lists()
            flush_bq()
            title = line[2:].strip()
            label = section_labels.get(section_num, "")
            label_html = f'<span class="section-label">{label}</span>' if label else ''
            html_parts.append(f'<h1>{label_html}{md_inline(title)}</h1>')
            section_num += 1
            i += 1
            continue

        # H2
        if re.match(r'^## ', line):
            close_lists()
            flush_bq()
            html_parts.append(f'<h2>{md_inline(line[3:].strip())}</h2>')
            i += 1
            continue

        # H3
        if re.match(r'^### ', line):
            close_lists()
            flush_bq()
            html_parts.append(f'<h3>{md_inline(line[4:].strip())}</h3>')
            i += 1
            continue

        # H4
        if re.match(r'^#### ', line):
            close_lists()
            flush_bq()
            html_parts.append(f'<h4>{md_inline(line[5:].strip())}</h4>')
            i += 1
            continue

        # Checklist
        if re.match(r'^- \[[ x]\] ', line):
            if not in_checklist:
                close_lists()
                html_parts.append('<ul class="checklist">')
                in_checklist = True
            text = re.sub(r'^- \[[ x]\] ', '', line)
            html_parts.append(f'<li>{md_inline(text)}</li>')
            i += 1
            continue

        # Unordered list
        if re.match(r'^[-*] ', line) and not re.match(r'^- \[', line):
            if not in_ul:
                close_lists()
                html_parts.append('<ul>')
                in_ul = True
            text = re.sub(r'^[-*] ', '', line)
            html_parts.append(f'<li>{md_inline(text)}</li>')
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\. ', line):
            if not in_ol:
                close_lists()
                html_parts.append('<ol>')
                in_ol = True
            text = re.sub(r'^\d+\. ', '', line)
            html_parts.append(f'<li>{md_inline(text)}</li>')
            i += 1
            continue

        # Close lists on non-list lines
        if line.strip() and not re.match(r'^[-*\d]', line):
            close_lists()

        # Empty line
        if not line.strip():
            flush_bq()
            i += 1
            continue

        # Paragraph
        html_parts.append(f'<p>{md_inline(line.strip())}</p>')
        i += 1

    close_lists()
    flush_bq()
    flush_table()

    return '\n'.join(html_parts)


def build_cover_html():
    return """
<div class="cover">
  <div class="cover-brand">Lazy Scholar PH</div>
  <div class="cover-title">THE DISCIPLINE<br>ARCHITECTURE</div>
  <div class="cover-divider"></div>
  <div class="cover-subtitle">Build the System That Makes Consistency Automatic</div>
  <div class="cover-tagline">Stop relying on motivation. Start designing behavior.</div>
  <div class="cover-pills">
    <span class="cover-pill">Identity Systems</span>
    <span class="cover-pill">Environment Design</span>
    <span class="cover-pill">Friction Engineering</span>
    <span class="cover-pill">30-Day Build</span>
  </div>
  <div class="cover-footer">lazyscholarph.com · A Lazy Scholar PH Premium Resource</div>
</div>
"""


def build_toc_html():
    sections = [
        ("INTRODUCTION", "The Real Reason You Keep Restarting"),
        ("SECTION 1", "Why Willpower Always Fails"),
        ("SECTION 2", "Identity Architecture"),
        ("SECTION 3", "Environment Design for Automatic Behavior"),
        ("SECTION 4", "The Anti-Chaos Routine System"),
        ("SECTION 5", "Friction Engineering"),
        ("SECTION 6", "The Restart Protocol"),
        ("SECTION 7", "30-Day Discipline Architecture Build"),
        ("SUMMARY", "Your Discipline Architecture at a Glance"),
        ("CLOSING", "Final Words from Lazy Scholar PH"),
    ]
    rows = "\n".join(
        f'<div class="toc-item"><span class="toc-label">{lbl}</span><span class="toc-name">{name}</span></div>'
        for lbl, name in sections
    )
    return f"""
<div class="toc">
  <div class="toc-title">Table of Contents</div>
  {rows}
</div>
"""


def build_html_document(md_path: Path, html_path: Path):
    md_text = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text)
    cover = build_cover_html()
    toc = build_toc_html()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Discipline Architecture — Lazy Scholar PH</title>
  <meta name="description" content="Build the System That Makes Consistency Automatic. A premium guide by Lazy Scholar PH.">
  <style>
{HTML_CSS}
  </style>
</head>
<body>
{cover}
{toc}
{body_html}
</body>
</html>"""

    html_path.write_text(full_html, encoding="utf-8")
    print(f"HTML generated: {html_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_html.py <input.md> <output.html>")
        sys.exit(1)
    build_html_document(Path(sys.argv[1]), Path(sys.argv[2]))
