import io
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape


def generate_medical_pdf(results):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "MedicalTitle",
        parent=styles["Title"],
        fontSize=19,
        leading=25,
        textColor=colors.HexColor("#174A75"),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "MedicalHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#174A75"),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "MedicalBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=16,
        spaceAfter=8
    )

    content = []

    content.append(
        Paragraph("MediVision AI", title_style)
    )

    content.append(
        Paragraph(
            "AI-Assisted Medical Analysis Report",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 12))

    date_text = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    content.append(
        Paragraph(
            "Generated: " + date_text,
            body_style
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#174A75")
        )
    )

    for heading, value in results.items():

        content.append(
            Paragraph(
                escape(str(heading)),
                heading_style
            )
        )

        safe_text = escape(str(value))
        safe_text = safe_text.replace("\n", "<br/>")

        content.append(
            Paragraph(safe_text, body_style)
        )

    content.append(Spacer(1, 20))

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "Disclaimer: This is an AI-assisted research "
            "prototype. Results are not a clinical diagnosis. "
            "Consult a qualified healthcare professional.",
            body_style
        )
    )

    document.build(content)

    buffer.seek(0)

    return buffer.getvalue()