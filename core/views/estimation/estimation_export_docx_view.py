from io import BytesIO

from django.http import HttpRequest, HttpResponse
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.models.estimation import Estimation
from core.views.generic.generic_500 import generic_500


def estimation_export_docx_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Export estimation to DOCX document.
    """
    try:
        estimation = Estimation.objects.get(id=model_id)
    except Estimation.DoesNotExist:
        return generic_500(request=request)

    # Create a new Document
    document = Document()

    # Set narrow margins (0.5 inches on all sides)
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Add title
    title = document.add_heading(estimation.name, level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add description if present
    if estimation.description:
        document.add_paragraph(estimation.description)
        document.add_paragraph()

    # Add metadata section
    document.add_heading('Project Information', level=2)
    table = document.add_table(rows=3, cols=2)
    table.style = 'Light Grid Accent 1'

    # Application
    row = table.rows[0]
    row.cells[0].text = 'Application'
    row.cells[1].text = str(estimation.application) if estimation.application else 'N/A'

    # Project
    row = table.rows[1]
    row.cells[0].text = 'Project'
    row.cells[1].text = str(estimation.project) if estimation.project else 'N/A'

    # Contingency Padding
    row = table.rows[2]
    row.cells[0].text = 'Contingency Padding'
    row.cells[1].text = f"{float(estimation.contingency_padding_percent or 0):.2f}%"

    document.add_paragraph()

    # Add estimation items section
    document.add_heading('Estimation Items', level=2)

    items = estimation.items.all().order_by('id')

    if items:
        # Create table for items
        table = document.add_table(rows=1, cols=6)
        table.style = 'Light Grid Accent 1'

        # Header row
        header_cells = table.rows[0].cells
        header_cells[0].text = 'Description'
        header_cells[1].text = 'Junior'
        header_cells[2].text = 'Mid'
        header_cells[3].text = 'Senior'
        header_cells[4].text = 'Lead'
        header_cells[5].text = 'Total'

        # Make header bold
        for cell in header_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

        # Add items
        for item in items:
            row_cells = table.add_row().cells
            row_cells[0].text = item.description
            row_cells[1].text = f"{float(item.hours_junior or 0):.2f}"
            row_cells[2].text = f"{float(item.hours_mid or 0):.2f}"
            row_cells[3].text = f"{float(item.hours_senior or 0):.2f}"
            row_cells[4].text = f"{float(item.hours_lead or 0):.2f}"
            row_cells[5].text = f"{float(item.get_total_hours()):.2f}"

    else:
        document.add_paragraph('No estimation items added yet.')

    document.add_paragraph()

    # Add summary section
    document.add_heading('Estimation Summary', level=2)

    summary_table = document.add_table(rows=7, cols=2)
    summary_table.style = 'Light Grid Accent 1'

    # Calculate totals
    totals = [
        ('Junior Developer Hours', estimation.get_total_hours_junior()),
        ('Mid-Level Developer Hours', estimation.get_total_hours_mid()),
        ('Senior Developer Hours', estimation.get_total_hours_senior()),
        ('Lead Developer Hours', estimation.get_total_hours_lead()),
        ('Subtotal (All Levels)', estimation.get_total_hours_all_levels()),
        (f'Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours()),
        ('GRAND TOTAL', estimation.get_grand_total_hours()),
    ]

    for idx, (label, value) in enumerate(totals):
        row = summary_table.rows[idx]
        row.cells[0].text = label
        row.cells[1].text = f"{float(value):.2f} hours"

        # Make grand total row bold
        if idx == 6:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True

    # Save document to BytesIO
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Create HTTP response
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="estimation_{estimation.id}_{estimation.name.replace(" ", "_")}.docx"'

    return response
