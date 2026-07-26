from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "e:/AI_COMMAND_CENTER/sample_research_paper.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
story = []

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=10
)

h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#1e40af'),
    spaceBefore=10,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#334155'),
    spaceAfter=6
)

story.append(Paragraph("Comparative Synthesis: The Future of Open-Weight AI vs. Centralized Governance", title_style))
story.append(Paragraph("<b>Compiled Research Compendium</b> | Multiple Sources Included | Date: June 2026", body_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e40af'), spaceAfter=12))

# Source 1
story.append(Paragraph("Source 1: 'The Case for Frontier AI Licensing' — Dr. Aris Thorne (AI Safety Policy Institute)", h2_style))
story.append(Paragraph(
    "Dr. Thorne argues that frontier AI models exceeding 10^26 FLOPs pose unprecedented biosecurity and automated cyber-attack risks. "
    "To mitigate these dangers, governments must enforce a mandatory licensing regime for training runs above certain compute thresholds. "
    "Thorne contends that open-releasing raw model weights removes safety guardrails permanently, making malicious fine-tuning irreversible. "
    "He recommends establishing international oversight bodies similar to nuclear regulatory commissions to control hardware access.", body_style))

# Source 2
story.append(Paragraph("Source 2: 'Democratizing Innovation Through Open-Source AI' — Prof. Maya Lin (Open Science Alliance)", h2_style))
story.append(Paragraph(
    "Prof. Lin presents a contrasting viewpoint, asserting that mandatory licensing creates regulatory capture that favors incumbents and "
    "entrenches Big Tech monopolies. She argues that open-source AI democratizes access for independent researchers, enabling global oversight "
    "and rapid security vulnerability identification. Lin points out that open models allow smaller enterprises to run localized inference "
    "without data privacy leakage to cloud providers. She advocates for regulating downstream application misuse rather than upstream model math.", body_style))

# Source 3
story.append(Paragraph("Source 3: 'Empirical Benchmark & Compute Efficiency Analysis' — TechCorp AI Research (2026 Report)", h2_style))
story.append(Paragraph(
    "TechCorp's empirical analysis benchmarked open-weights models (e.g., Llama-3-70B) against proprietary frontier APIs (e.g., GPT-4o, Gemini 1.5 Pro). "
    "The data shows open models have closed the performance gap to within 2.5% on standard coding and reasoning benchmarks, while operating at "
    "up to 80% lower per-token inference cost. Crucially, TechCorp's study highlights that <b>both proponents and opponents agree</b> that "
    "energy consumption and GPU data center availability are the single bottleneck constraining future model scaling through 2028.", body_style))

story.append(Spacer(1, 8))

# Summary Comparison Table
data = [
    ["Dimension", "Source 1 (Dr. Thorne)", "Source 2 (Prof. Lin)", "Source 3 (TechCorp)"],
    ["Core Focus", "Risk Mitigation & Safety", "Democratization & Innovation", "Cost & Performance Data"],
    ["Governance Model", "Centralized Govt Licensing", "Open Access / Misuse Rules", "Market-Driven Hybrids"],
    ["Key Bottleneck", "Hardware Regulation", "Monopoly / Access Barriers", "Energy & GPU Availability"],
    ["Model Weight Stance", "Strictly Closed / Gated", "Fully Open / Transparent", "Empirically Competitive"]
]

t = Table(data, colWidths=[110, 130, 130, 130])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8.5),
    ('BOTTOMPADDING', (0,0), (-1,0), 5),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('FONTSIZE', (0,1), (-1,-1), 8),
]))
story.append(t)

doc.build(story)
print("Research PDF generated successfully at:", pdf_path)
