from datetime import datetime, timezone

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

from core.models.recommendation import (
    RECOMMENDATION_PRIORITY_HIGH,
    RECOMMENDATION_PRIORITY_LOW,
    RECOMMENDATION_PRIORITY_MEDIUM,
    Recommendation,
)
from core.views.application.utilities.application_docx_helpers import (
    add_header_footer as _add_header_footer,
    add_toc_placeholder as _add_toc_placeholder,
    set_narrow_margins as _set_narrow_margins,
)


def set_narrow_margins(document: Document) -> None:
    """Reuse application helper for narrow margins."""
    _set_narrow_margins(document)


def add_header_footer(document: Document, title: str, person_name: str, date_str: str) -> None:
    """Add custom header with person (left), title (center), date (right) and footer with page numbers."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor, Inches
    from docx.table import _Cell

    section = document.sections[0]

    # Add header with a table for proper three-column layout
    header = section.header

    # Clear existing paragraphs
    for para in header.paragraphs:
        para.clear()

    # Create a 1-row, 3-column table in the header
    table = header.add_table(rows=1, cols=3, width=Inches(7.5))
    table.autofit = False

    # Set column widths
    table.columns[0].width = Inches(2.5)  # Left column (person)
    table.columns[1].width = Inches(2.5)  # Center column (title)
    table.columns[2].width = Inches(2.5)  # Right column (date)

    # Get cells
    cells = table.rows[0].cells

    # Left cell - Person name
    left_para = cells[0].paragraphs[0]
    left_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    left_run = left_para.add_run(person_name)
    left_run.font.size = Pt(9)
    left_run.font.color.rgb = RGBColor(100, 100, 100)

    # Center cell - Title
    center_para = cells[1].paragraphs[0]
    center_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    center_run = center_para.add_run(title)
    center_run.font.size = Pt(9)
    center_run.font.color.rgb = RGBColor(100, 100, 100)
    center_run.bold = True

    # Right cell - Date
    right_para = cells[2].paragraphs[0]
    right_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    right_run = right_para.add_run(date_str)
    right_run.font.size = Pt(9)
    right_run.font.color.rgb = RGBColor(100, 100, 100)

    # Remove table borders
    from docx.oxml.shared import OxmlElement, qn
    tbl = table._element
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    # Set borders to none
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        border.set(qn('w:sz'), '0')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'auto')
        tblBorders.append(border)
    tblPr.append(tblBorders)

    # Add footer with page numbers
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_para.add_run()
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(100, 100, 100)

    # Add field for page number
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def add_toc_placeholder(document: Document) -> None:
    """Reuse application helper for TOC placeholder."""
    _add_toc_placeholder(document)


def add_recommendation_intro(document: Document) -> None:
    """Add introductory paragraph about recommendations."""
    from docx.shared import Pt

    intro_para = document.add_paragraph()
    intro_run = intro_para.add_run(
        "This document contains a technical recommendation for improving systems, processes, or practices. "
        "Recommendations are tracked to ensure continuous improvement and documentation of best practices. "
        "Each recommendation includes detailed analysis of benefits, risks, and implementation considerations."
    )
    intro_run.font.size = Pt(10)
    intro_run.italic = True

    # Add spacing after intro
    document.add_paragraph()


def add_title_page(document: Document, username: str, total_count: int) -> None:
    """Add title page with metadata."""
    title = document.add_heading("Recommendations Export", level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadata table
    table = document.add_table(rows=3, cols=2)
    table.style = "Light Grid Accent 1"

    table.rows[0].cells[0].text = "Generated By"
    table.rows[0].cells[1].text = username

    table.rows[1].cells[0].text = "Generated Date"
    now = datetime.now(timezone.utc)
    table.rows[1].cells[1].text = now.strftime("%Y-%m-%d %I:%M %p UTC")

    table.rows[2].cells[0].text = "Total Recommendations"
    table.rows[2].cells[1].text = str(total_count)

    # Format table
    for row in table.rows:
        row.cells[0].paragraphs[0].runs[0].bold = True
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)

    document.add_page_break()


def add_recommendation_section(document: Document, recommendation: Recommendation) -> None:
    """Add a formatted recommendation section to the document."""
    from core.utilities.get_name_acronym import get_name_acronym

    # Metadata table - only show related entities
    table = document.add_table(rows=0, cols=2)
    table.style = "Light Grid Accent 1"

    # Related entities
    if recommendation.application:
        row = table.add_row()
        row.cells[0].text = "Related Application"
        row.cells[1].text = get_name_acronym(
            acronym=recommendation.application.acronym, name=recommendation.application.name
        )

    if recommendation.project:
        row = table.add_row()
        row.cells[0].text = "Related Project"
        row.cells[1].text = recommendation.project.name if hasattr(recommendation.project, "name") else str(recommendation.project)

    if recommendation.estimation:
        row = table.add_row()
        row.cells[0].text = "Related Estimation"
        row.cells[1].text = recommendation.estimation.name if hasattr(recommendation.estimation, "name") else str(recommendation.estimation)

    # Format table cells
    for row in table.rows:
        row.cells[0].paragraphs[0].runs[0].bold = True
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)

    # Add spacing
    document.add_paragraph()

    # Description section
    if recommendation.description:
        document.add_heading("Description", level=2)
        para = document.add_paragraph(recommendation.description)
        for run in para.runs:
            run.font.size = Pt(9)

    # Rationale section
    if recommendation.rationale:
        document.add_heading("Rationale", level=2)
        para = document.add_paragraph(recommendation.rationale)
        for run in para.runs:
            run.font.size = Pt(9)

    # Expected Benefits section
    if recommendation.benefits:
        document.add_heading("Expected Benefits", level=2)
        para = document.add_paragraph(recommendation.benefits)
        for run in para.runs:
            run.font.size = Pt(9)

    # Potential Risks section
    if recommendation.risks:
        document.add_heading("Potential Risks", level=2)
        para = document.add_paragraph(recommendation.risks)
        for run in para.runs:
            run.font.size = Pt(9)

    # Additional Notes section
    if recommendation.comment:
        document.add_heading("Notes", level=2)
        para = document.add_paragraph(recommendation.comment)
        for run in para.runs:
            run.font.size = Pt(9)
