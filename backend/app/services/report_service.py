import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.schemas.investigation import InvestigationDetail

def generate_pdf_report(inv: InvestigationDetail) -> bytes:
    """
    Generates a professional, print-ready PDF investigation report using ReportLab.
    Enforces clear typographic distinction between Observed Facts, Inferences, and Hypotheses.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom forensic report typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563EB')
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("DIGITAL FOSSIL", subtitle_style))
    story.append(Paragraph("Explainable Activity Reconstruction Report", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Investigation ID: <b>{inv.investigation_id}</b> | Session: <b>{inv.session_id}</b>", body_style))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | Platform: Digital Fossil v1.0", body_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=14))

    # 2. Executive Metadata Grid
    conf_color = colors.HexColor('#16A34A') if inv.confidence_label == "HIGH" else (colors.HexColor('#D97706') if inv.confidence_label == "MEDIUM" else colors.HexColor('#DC2626'))
    status_color = colors.HexColor('#16A34A') if inv.reviewer_verdict == "approved" else (colors.HexColor('#DC2626') if inv.reviewer_verdict == "flagged" else colors.HexColor('#64748B'))

    metadata_table_data = [
        [
            Paragraph("<b>Investigation Title:</b>", table_header),
            Paragraph(inv.title, table_cell),
            Paragraph("<b>Evidence Confidence:</b>", table_header),
            Paragraph(f"<font color='{conf_color.hexval()}'><b>{inv.confidence_label} ({int(inv.overall_confidence*100)}%)</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Session Duration:</b>", table_header),
            Paragraph(f"{inv.session_duration:.1f} seconds", table_cell),
            Paragraph("<b>Anomaly Status:</b>", table_header),
            Paragraph(f"<b>{'ANOMALOUS (Score: ' + str(inv.anomaly_score) + ')' if inv.is_anomaly else 'BASELINE CONFORMANT'}</b>", table_cell)
        ],
        [
            Paragraph("<b>Reviewer Verdict:</b>", table_header),
            Paragraph(f"<font color='{status_color.hexval()}'><b>{(inv.reviewer_verdict or 'PENDING REVIEW').upper()}</b></font>", table_cell),
            Paragraph("<b>Observed vs Inferred:</b>", table_header),
            Paragraph(f"{inv.observed_facts_count} Facts / {inv.inferences_count} Inferences", table_cell)
        ]
    ]

    meta_table = Table(metadata_table_data, colWidths=[110, 160, 110, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 3. Principle Banner: Facts vs Inference Distinction
    distinction_data = [[
        Paragraph(
            "<b>EPISTEMIC STANDARDS NOTICE:</b> This system strictly separates <b>OBSERVED FACTS</b> (directly verifiable from system telemetry) "
            "from <b>INFERENCES</b> (probabilistic correlations) and <b>HYPOTHESES</b> (plausible explanations). "
            "No unrecorded action is asserted as fact.",
            table_cell
        )
    ]]
    dist_table = Table(distinction_data, colWidths=[530])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3B82F6')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(dist_table)
    story.append(Spacer(1, 12))

    # 4. Section: Observed Facts
    story.append(Paragraph("1. OBSERVED FACTS (Verifiable Event Records)", section_heading))
    fact_table_data = [[
        Paragraph("<b>ID</b>", table_header),
        Paragraph("<b>Time (UTC)</b>", table_header),
        Paragraph("<b>Event Type</b>", table_header),
        Paragraph("<b>File / Target</b>", table_header),
        Paragraph("<b>Size</b>", table_header)
    ]]
    for f in inv.observed_facts[:12]:
        fact_table_data.append([
            Paragraph(f.id, table_cell),
            Paragraph(f.timestamp.strftime("%H:%M:%S"), table_cell),
            Paragraph(f.event_type.replace("FILE_", ""), table_cell),
            Paragraph(f.file_name, table_cell),
            Paragraph(f"{f.file_size:,} B" if f.file_size else "-", table_cell)
        ])
    
    fact_table = Table(fact_table_data, colWidths=[55, 65, 95, 235, 80])
    fact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fact_table)
    story.append(Spacer(1, 14))

    # 5. Section: Inferences & Correlated Relationships
    story.append(Paragraph("2. INFERENCES (Derived Multi-Event Correlations)", section_heading))
    if inv.inferences:
        inf_table_data = [[
            Paragraph("<b>ID</b>", table_header),
            Paragraph("<b>Inferred Relationship Statement</b>", table_header),
            Paragraph("<b>Score</b>", table_header),
            Paragraph("<b>Supporting Evidence</b>", table_header)
        ]]
        for inf in inv.inferences[:8]:
            inf_table_data.append([
                Paragraph(inf.id, table_cell),
                Paragraph(inf.statement, table_cell),
                Paragraph(f"{inf.correlation_score:.2f}", table_cell),
                Paragraph(", ".join(inf.supporting_evidence_ids[:2]), table_cell)
            ])
        inf_table = Table(inf_table_data, colWidths=[50, 310, 50, 120])
        inf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(inf_table)
    else:
        story.append(Paragraph("No multi-event correlations met the minimum relationship threshold.", body_style))
    story.append(Spacer(1, 14))

    # 6. Section: Primary Hypothesis and Explicit Uncertainty
    story.append(Paragraph("3. HYPOTHESES & UNCERTAINTY STATEMENTS", section_heading))
    for h in inv.hypotheses:
        hyp_box = [
            [Paragraph(f"<b>Hypothesis {h.id} (Confidence: {int(h.confidence*100)}% - {h.confidence_label}):</b>", table_header)],
            [Paragraph(h.hypothesis_text, body_style)],
            [Paragraph(f"<b>Reasoning:</b> {h.reasoning_summary}", body_style)],
            [Paragraph(f"<b>Explicit Uncertainty / Unproven Assumptions:</b> <font color='#B91C1C'><i>{h.uncertainty_statement}</i></font>", body_style)]
        ]
        t = Table(hyp_box, colWidths=[530])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAF5FF')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#A855F7')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

    # 7. Section: Missing / Conflicting Evidence
    if inv.missing_evidence or inv.conflicting_evidence:
        story.append(Paragraph("4. GAPS IN EVIDENCE & CONFLICTING ARTIFACTS", section_heading))
        gaps = []
        for m in inv.missing_evidence:
            gaps.append(f"• <b>[MISSING]:</b> {m.description} <i>({m.significance})</i>")
        for c in inv.conflicting_evidence:
            gaps.append(f"• <b>[CONFLICT]:</b> {c.description} <i>({c.impact_on_confidence})</i>")
        story.append(Paragraph("<br/>".join(gaps), body_style))
        story.append(Spacer(1, 14))

    # 8. Reviewer Verdict Sign-off Block
    story.append(Paragraph("5. REVIEWER VERDICT & ATTESTATION", section_heading))
    rev_data = [
        [
            Paragraph("<b>Verdict:</b>", table_header),
            Paragraph(f"<b>{(inv.reviewer_verdict or 'PENDING REVIEW').upper()}</b>", body_style),
            Paragraph("<b>Reviewed By:</b>", table_header),
            Paragraph(inv.reviewed_by or "Pending Assignment", body_style)
        ],
        [
            Paragraph("<b>Review Comments:</b>", table_header),
            Paragraph(inv.reviewer_comment or "No reviewer comments recorded to date.", body_style),
            Paragraph("<b>Review Date:</b>", table_header),
            Paragraph(inv.reviewed_at.strftime('%Y-%m-%d %H:%M UTC') if inv.reviewed_at else "N/A", body_style)
        ]
    ]
    rev_table = Table(rev_data, colWidths=[100, 180, 90, 160])
    rev_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(rev_table)

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
