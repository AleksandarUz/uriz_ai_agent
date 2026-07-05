import re
from html import escape
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def register_pdf_fonts() -> None:
    """
    Registruje fontove koji podržavaju srpska latinična slova.
    Prvo pokušava Windows Arial fontove.
    """

    regular_font_paths = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
    ]

    bold_font_paths = [
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
    ]

    regular_font = next(
        (path for path in regular_font_paths if path.exists()),
        None,
    )

    bold_font = next(
        (path for path in bold_font_paths if path.exists()),
        None,
    )

    if regular_font is None:
        raise FileNotFoundError(
            "Nije pronađen font za generisanje PDF-a."
        )

    if bold_font is None:
        bold_font = regular_font

    pdfmetrics.registerFont(
        TTFont("AppFont", str(regular_font))
    )

    pdfmetrics.registerFont(
        TTFont("AppFont-Bold", str(bold_font))
    )

    pdfmetrics.registerFontFamily(
        "AppFont",
        normal="AppFont",
        bold="AppFont-Bold",
        italic="AppFont",
        boldItalic="AppFont-Bold",
    )


def convert_inline_markdown(text: str) -> str:
    """
    Pretvara jednostavan Markdown bold format u ReportLab format.

    Primer:
    **US-3** -> <b>US-3</b>
    """

    safe_text = escape(text)

    safe_text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        safe_text,
    )

    return safe_text


def add_page_number(canvas, document) -> None:
    """
    Dodaje broj stranice u footer PDF dokumenta.
    """

    canvas.saveState()

    canvas.setFont("AppFont", 9)

    page_number = canvas.getPageNumber()

    page_text = f"Stranica {page_number}"

    canvas.drawCentredString(
        A4[0] / 2,
        12 * mm,
        page_text,
    )

    canvas.restoreState()


def generate_pdf(report_text: str, output_path: str) -> None:
    """
    Pretvara tekstualni Markdown-like izveštaj u PDF dokument.
    """

    register_pdf_fonts()

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="User Story Quality Analysis Report",
        author="Aleksandar Uzelac",
    )

    base_styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=base_styles["Title"],
        fontName="AppFont-Bold",
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    heading_1_style = ParagraphStyle(
        "Heading1Custom",
        parent=base_styles["Heading1"],
        fontName="AppFont-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=12,
        spaceAfter=8,
    )

    heading_2_style = ParagraphStyle(
        "Heading2Custom",
        parent=base_styles["Heading2"],
        fontName="AppFont-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=base_styles["BodyText"],
        fontName="AppFont",
        fontSize=10.5,
        leading=15,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=4,
    )

    numbered_style = ParagraphStyle(
        "NumberedCustom",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=4,
    )

    elements = []

    lines = report_text.splitlines()

    first_main_heading = True

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            elements.append(Spacer(1, 5))
            continue

        if line.startswith("# "):
            text = convert_inline_markdown(line[2:])

            if first_main_heading:
                elements.append(
                    Paragraph(text, title_style)
                )
                first_main_heading = False
            else:
                elements.append(
                    Paragraph(text, heading_1_style)
                )

        elif line.startswith("## "):
            text = convert_inline_markdown(line[3:])

            elements.append(
                Paragraph(text, heading_1_style)
            )

        elif line.startswith("### "):
            text = convert_inline_markdown(line[4:])

            elements.append(
                Paragraph(text, heading_2_style)
            )

        elif line.startswith("- "):
            text = convert_inline_markdown(line[2:])

            elements.append(
                Paragraph(
                    f"• {text}",
                    bullet_style,
                )
            )

        elif re.match(r"^\d+\.\s+", line):
            text = convert_inline_markdown(line)

            elements.append(
                Paragraph(
                    text,
                    numbered_style,
                )
            )

        else:
            text = convert_inline_markdown(line)

            elements.append(
                Paragraph(
                    text,
                    body_style,
                )
            )

    document.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )