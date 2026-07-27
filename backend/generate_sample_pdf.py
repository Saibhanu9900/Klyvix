from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "e:/AI_COMMAND_CENTER/sample_test_document.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
story = []

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=10
)

h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#2563eb'),
    spaceBefore=12,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#334155'),
    spaceAfter=8
)

story.append(Paragraph("Quantum Dynamics Inc. — Annual Project & Financial Report (2026)", title_style))
story.append(Paragraph("<b>Document ID:</b> QD-2026-REPORT-V2 | <b>Date:</b> July 15, 2026 | <b>Author:</b> Dr. Elena Rostova", body_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=15))

# Section 1
story.append(Paragraph("1. Executive Summary", h2_style))
story.append(Paragraph(
    "Quantum Dynamics Inc. has successfully completed Phase 2 of the HexaMind platform integration. "
    "Overall system performance increased by 42% following the deployment of multi-provider routing (Gemini 2.5 Flash, "
    "Groq Llama 3.3, and Mistral Codestral). The total target revenue for Q3 2026 was projected at $4.5 Million, with an "
    "actual achieved revenue of $4.85 Million (an 8% overperformance).", body_style))

# Section 2
story.append(Paragraph("2. Financial Breakdown & Budget Allocation", h2_style))
story.append(Paragraph("The total operational budget allocated for FY 2026 is <b>$1,250,000</b>. Below is the detailed breakdown by department:", body_style))

data = [
    ["Department", "Budget Allocated", "Amount Spent", "Variance"],
    ["Cloud Infrastructure (AWS/GCP)", "$450,000", "$412,000", "+$38,000 (Under budget)"],
    ["LLM API Token Licensing", "$300,000", "$315,000", "-$15,000 (Over budget)"],
    ["Engineering & R&D", "$350,000", "$340,000", "+$10,000 (Under budget)"],
    ["Security & Compliance Audit", "$150,000", "$120,000", "+$30,000 (Under budget)"],
    ["TOTAL", "$1,250,000", "$1,187,000", "+$63,000 (Net Savings)"]
]

t = Table(data, colWidths=[180, 100, 100, 140])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8fafc')),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2e8f0')),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
]))
story.append(t)
story.append(Spacer(1, 10))

# Section 3
story.append(Paragraph("3. Key Risk Factors & Deadlines", h2_style))
story.append(Paragraph(
    "<b>Risk 1 - API Rate Limits:</b> Increased usage of Mistral Codestral may exceed initial tier thresholds. "
    "Mitigation: Groq fallback routing is enabled automatically.<br/>"
    "<b>Risk 2 - Security Audit Compliance:</b> ISO-27001 re-certification audit deadline is <b>September 30, 2026</b>.<br/>"
    "<b>Key Milestone:</b> Version 3.0 Production Launch scheduled for <b>October 15, 2026</b>.", body_style))

# Section 4
story.append(Paragraph("4. Recommended Next Steps", h2_style))
story.append(Paragraph(
    "1. Finalize AWS App Runner production container deployment by August 15, 2026.<br/>"
    "2. Configure AWS CloudWatch budget alerts at the $1,000 threshold to prevent unexpected billing spikes.<br/>"
    "3. Restrict backend CORS origins strictly to production domain endpoints prior to launch.", body_style))

doc.build(story)
print("PDF generated successfully at:", pdf_path)
