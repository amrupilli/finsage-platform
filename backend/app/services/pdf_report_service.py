from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.schemas.report import ReportResponse


def generate_report_pdf(report: ReportResponse) -> bytes:
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="FinSage Educational Investment Report",
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("FinSage Educational Investment Report", styles["Title"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("User", styles["Heading2"]))
    story.append(Paragraph(report.user_email, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Risk Profile", styles["Heading2"]))
    story.append(Paragraph(f"Profile: {report.risk_profile.profile}", styles["BodyText"]))
    story.append(Paragraph(report.risk_profile.summary, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Portfolio Scenario", styles["Heading2"]))
    story.append(Paragraph(report.portfolio.description, styles["BodyText"]))

    for category, percentage in report.portfolio.allocations.items():
        story.append(Paragraph(f"{category}: {percentage}%", styles["BodyText"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("Simulation Summary", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Expected final value: {report.simulation.expected_return}",
            styles["BodyText"],
        )
    )
    story.append(
        Paragraph(
            f"Probability of loss: {report.simulation.probability_of_loss}",
            styles["BodyText"],
        )
    )
    story.append(Paragraph(report.simulation.summary, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Warnings and Educational Guidance", styles["Heading2"]))

    if report.warnings:
        for warning in report.warnings:
            story.append(Paragraph(f"{warning.severity.upper()}: {warning.title}", styles["Heading3"]))
            story.append(Paragraph(warning.message, styles["BodyText"]))
            story.append(Paragraph(f"Recommended action: {warning.recommended_action}", styles["BodyText"]))
            story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("No warnings available for this report.", styles["BodyText"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("Disclaimer", styles["Heading2"]))
    story.append(Paragraph(report.disclaimer, styles["BodyText"]))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes