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
        # Create table for items (hours with uncertainty applied)
        table = document.add_table(rows=1, cols=8)
        table.style = 'Light Grid Accent 1'

        # Header row
        header_cells = table.rows[0].cells
        header_cells[0].text = 'Description'
        header_cells[1].text = 'Complexity'
        header_cells[2].text = 'Priority'
        header_cells[3].text = 'Cone of Uncertainty'
        header_cells[4].text = 'Junior Hrs'
        header_cells[5].text = 'Mid Hrs'
        header_cells[6].text = 'Senior Hrs'
        header_cells[7].text = 'Lead Hrs'

        # Make header bold
        for cell in header_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

        # Add items (showing hours with uncertainty applied)
        for item in items:
            row_cells = table.add_row().cells
            row_cells[0].text = item.description
            row_cells[1].text = item.get_complexity_level_display() if item.complexity_level else 'N/A'
            row_cells[2].text = item.get_priority_display() if item.priority else 'N/A'
            row_cells[3].text = item.get_cone_of_uncertainty_display() if item.cone_of_uncertainty else 'N/A'
            row_cells[4].text = f"{float(item.get_junior_hours_with_uncertainty()):.2f}"
            row_cells[5].text = f"{float(item.get_mid_hours_with_uncertainty()):.2f}"
            row_cells[6].text = f"{float(item.get_senior_hours_with_uncertainty()):.2f}"
            row_cells[7].text = f"{float(item.get_lead_hours_with_uncertainty()):.2f}"

    else:
        document.add_paragraph('No estimation items added yet.')

    document.add_paragraph()

    # Add summary section
    document.add_heading('Estimation Summary', level=2)
    document.add_paragraph('Hours shown include cone of uncertainty multipliers. Each level represents alternative estimates, not additive totals.')

    summary_table = document.add_table(rows=17, cols=2)
    summary_table.style = 'Light Grid Accent 1'

    # Calculate totals per level
    totals = [
        ('JUNIOR DEVELOPER', ''),
        ('  Base Hours', estimation.get_base_hours_junior()),
        ('  With Uncertainty', estimation.get_total_hours_junior_with_uncertainty()),
        (f'  Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours_junior()),
        ('  Grand Total', estimation.get_grand_total_hours_junior()),
        ('MID-LEVEL DEVELOPER', ''),
        ('  Base Hours', estimation.get_base_hours_mid()),
        ('  With Uncertainty', estimation.get_total_hours_mid_with_uncertainty()),
        (f'  Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours_mid()),
        ('  Grand Total', estimation.get_grand_total_hours_mid()),
        ('SENIOR DEVELOPER', ''),
        ('  Base Hours', estimation.get_base_hours_senior()),
        ('  With Uncertainty', estimation.get_total_hours_senior_with_uncertainty()),
        (f'  Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours_senior()),
        ('  Grand Total', estimation.get_grand_total_hours_senior()),
        ('LEAD DEVELOPER', ''),
        ('  Base Hours', estimation.get_base_hours_lead()),
        ('  With Uncertainty', estimation.get_total_hours_lead_with_uncertainty()),
        (f'  Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours_lead()),
        ('  Grand Total', estimation.get_grand_total_hours_lead()),
    ]

    # Adjust rows to match the number of totals
    while len(summary_table.rows) < len(totals):
        summary_table.add_row()

    for idx, (label, value) in enumerate(totals):
        row = summary_table.rows[idx]
        row.cells[0].text = label
        if value == '':
            # Section headers
            row.cells[1].text = ''
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
        else:
            row.cells[1].text = f"{float(value):.2f} hours"

            # Make grand total rows bold
            if 'Grand Total' in label:
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
