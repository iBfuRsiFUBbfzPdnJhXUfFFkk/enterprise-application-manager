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

    # Add methodology explanation section
    document.add_heading('Estimation Methodology', level=2)

    # Overview paragraph
    overview = document.add_paragraph()
    overview.add_run('This estimation uses a sophisticated multi-factor approach to provide realistic project timelines. ').font.size = Pt(10)
    overview.add_run('The methodology accounts for developer experience levels, task uncertainty, and project-specific contingencies.').font.size = Pt(10)
    document.add_paragraph()

    # Developer level multipliers
    document.add_heading('Developer Level Multipliers', level=3)
    multipliers_para = document.add_paragraph()
    multipliers_para.add_run('Each developer level has a different uncertainty multiplier based on experience:').font.size = Pt(10)

    multipliers_list = [
        ('Junior Developer (6x):', 'Junior developers require significantly more time due to learning curves, troubleshooting, and the need for guidance. The 6x multiplier accounts for these factors.'),
        ('Mid-Level Developer (3x):', 'Mid-level developers have foundational skills but still encounter unforeseen challenges. The 3x multiplier provides reasonable padding for problem-solving.'),
        ('Senior Developer (1.5x):', 'Senior developers work efficiently with fewer blockers. The 1.5x multiplier accounts for architectural decisions and edge cases.'),
        ('Lead Developer (1x):', 'Lead developers provide the baseline estimate with no additional multiplier, representing expert-level execution.'),
    ]

    for label, description in multipliers_list:
        p = document.add_paragraph(style='List Bullet')
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(10)
        run2 = p.add_run(description)
        run2.font.size = Pt(10)

    document.add_paragraph()

    # Separated hours components
    document.add_heading('Hour Components', level=3)
    components_para = document.add_paragraph()
    components_para.add_run('Each estimation item separates work into distinct components, each with level-specific multipliers applied:').font.size = Pt(10)

    components_list = [
        ('Development Hours:', 'Core implementation time for writing features, fixing bugs, or building functionality.'),
        ('Code Review Hours:', 'Time for reviewing others\' code (typically 0.5x development time). Critical for maintaining code quality and catching issues early.'),
        ('Testing Hours:', 'Time for writing unit tests, integration tests, and manual QA (typically 1x development time). Essential for long-term maintainability.'),
        ('Code Reviewer Hours:', 'Dedicated time for lead developers to review all team code (no uncertainty multiplier). Shown separately as it represents additional team capacity needs.'),
    ]

    for label, description in components_list:
        p = document.add_paragraph(style='List Bullet')
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(10)
        run2 = p.add_run(description)
        run2.font.size = Pt(10)

    document.add_paragraph()

    # Contingency padding
    document.add_heading('Contingency Padding', level=3)
    contingency_para = document.add_paragraph()
    contingency_value = float(estimation.contingency_padding_percent or 0)
    contingency_para.add_run(f'This estimation includes a {contingency_value:.1f}% contingency buffer applied to all final totals. ').font.size = Pt(10)
    contingency_para.add_run('Contingency padding accounts for:').font.size = Pt(10)

    contingency_list = [
        'Scope creep and requirement changes',
        'Integration challenges with existing systems',
        'Unforeseen technical debt or refactoring needs',
        'Team coordination overhead and communication time',
        'Deployment, documentation, and release activities',
    ]

    for item in contingency_list:
        p = document.add_paragraph(style='List Bullet')
        run = p.add_run(item)
        run.font.size = Pt(10)

    document.add_paragraph()

    # Cone of Uncertainty
    document.add_heading('Cone of Uncertainty', level=3)
    cou_para = document.add_paragraph()
    cou_para.add_run('The "Cone of Uncertainty" field tracks project phase for reference purposes. ').font.size = Pt(10)
    cou_para.add_run('While displayed on items, it is informational only—actual uncertainty is handled through developer level multipliers:').font.size = Pt(10)

    cou_list = [
        ('Initial Concept (4x):', 'Early exploration phase with high uncertainty'),
        ('Approved Product (2x):', 'Product definition complete, requirements being refined'),
        ('Requirements Complete (1.5x):', 'Requirements documented, design in progress'),
        ('Design Complete (1.25x):', 'Technical design finished, implementation starting'),
        ('Implementation Complete (1.1x):', 'Code complete, final testing and refinement'),
    ]

    for label, description in cou_list:
        p = document.add_paragraph(style='List Bullet')
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(10)
        run2 = p.add_run(description)
        run2.font.size = Pt(10)

    document.add_paragraph()

    # How to use estimates
    document.add_heading('Interpreting the Estimates', level=3)
    interpret_para = document.add_paragraph()
    interpret_para.add_run('Each developer level represents an alternative staffing scenario, not additive totals. ').font.size = Pt(10)
    interpret_para.add_run('Choose the level that matches your team composition:').font.size = Pt(10)

    interpret_list = [
        'Junior developers require more calendar time but may be more cost-effective',
        'Lead developers complete work faster but represent higher labor costs',
        'Mixed teams should use weighted averages based on actual team composition',
        'Code reviewer hours are additive to developer hours and represent dedicated review capacity',
    ]

    for item in interpret_list:
        p = document.add_paragraph(style='List Bullet')
        run = p.add_run(item)
        run.font.size = Pt(10)

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

    # Add combined project estimate (if team composition is set)
    if estimation.get_total_team_size() > 0 or estimation.reviewer_count:
        document.add_heading('Combined Project Estimate', level=2)

        combined_para = document.add_paragraph()
        combined_para.add_run('Based on your team composition, this is the realistic project timeline assuming all developer levels work in parallel on their assigned tasks.').font.size = Pt(10)
        document.add_paragraph()

        # Create table for combined estimate
        combined_table = document.add_table(rows=4, cols=2)
        combined_table.style = 'Light Grid Accent 1'

        # Team size
        row = combined_table.rows[0]
        row.cells[0].text = 'Total Team Size'
        team_text = f"{estimation.get_total_team_size()} developer{'s' if estimation.get_total_team_size() != 1 else ''}"
        if estimation.reviewer_count:
            team_text += f" + {estimation.reviewer_count} reviewer{'s' if estimation.reviewer_count != 1 else ''}"
        row.cells[1].text = team_text

        # Project duration in weeks
        row = combined_table.rows[1]
        row.cells[0].text = 'Project Duration (Weeks)'
        weeks = estimation.get_combined_project_duration_weeks()
        row.cells[1].text = f"{float(weeks):.1f} weeks" if weeks else 'N/A'

        # Project duration in months
        row = combined_table.rows[2]
        row.cells[0].text = 'Project Duration (Months)'
        months = estimation.get_combined_project_duration_months()
        row.cells[1].text = f"{float(months):.1f} months" if months else 'N/A'

        # Bottleneck level
        row = combined_table.rows[3]
        row.cells[0].text = 'Bottleneck Level'
        bottleneck = estimation.get_bottleneck_level()
        if bottleneck:
            row.cells[1].text = f"{bottleneck[0]} ({float(bottleneck[1]):.1f} weeks - determines project duration)"
        else:
            row.cells[1].text = 'N/A'

        # Make all text in table smaller
        for row in combined_table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(10)

        document.add_paragraph()

        # Team composition breakdown
        document.add_heading('Team Composition', level=3)
        comp_table = document.add_table(rows=5, cols=2)
        comp_table.style = 'Light Grid Accent 1'

        comp_table.rows[0].cells[0].text = 'Junior Developers'
        comp_table.rows[0].cells[1].text = str(estimation.junior_developer_count or 0)

        comp_table.rows[1].cells[0].text = 'Mid-Level Developers'
        comp_table.rows[1].cells[1].text = str(estimation.mid_developer_count or 0)

        comp_table.rows[2].cells[0].text = 'Senior Developers'
        comp_table.rows[2].cells[1].text = str(estimation.senior_developer_count or 0)

        comp_table.rows[3].cells[0].text = 'Lead Developers'
        comp_table.rows[3].cells[1].text = str(estimation.lead_developer_count or 0)

        comp_table.rows[4].cells[0].text = 'Code Reviewers'
        comp_table.rows[4].cells[1].text = str(estimation.reviewer_count or 0)

        # Make all text in table smaller
        for row in comp_table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(10)

        document.add_paragraph()

    # Add estimation items section
    document.add_heading('Estimation Items', level=2)
    document.add_paragraph('Hours include development, code review, and testing with level-based uncertainty multipliers (Jr: 6x, Mid: 3x, Sr: 1.5x, Lead: 1x). Reviewer hours shown separately without uncertainty.')

    items = estimation.items.all().order_by('order', 'id')

    if items:
        # Create table for items (hours with uncertainty applied)
        table = document.add_table(rows=1, cols=10)
        table.style = 'Light Grid Accent 1'

        # Header row
        header_cells = table.rows[0].cells
        header_cells[0].text = 'Title'
        header_cells[1].text = 'Pts'
        header_cells[2].text = 'Cmplx'
        header_cells[3].text = 'Prior'
        header_cells[4].text = 'CoU'
        header_cells[5].text = 'Jr'
        header_cells[6].text = 'Mid'
        header_cells[7].text = 'Sr'
        header_cells[8].text = 'Lead'
        header_cells[9].text = 'Rev'

        # Make header bold and smaller font
        for cell in header_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)

        # Add items (showing hours with uncertainty applied)
        for item in items:
            row_cells = table.add_row().cells

            # Set text content
            contents = [
                item.title if item.title else '(No title)',
                f"{float(item.story_points or 0):.1f}",
                item.get_complexity_level_display() if item.complexity_level else 'N/A',
                item.get_priority_display() if item.priority else 'N/A',
                item.get_cone_of_uncertainty_display() if item.cone_of_uncertainty else 'N/A',
                f"{float(item.get_junior_hours_with_uncertainty()):.2f}",
                f"{float(item.get_mid_hours_with_uncertainty()):.2f}",
                f"{float(item.get_senior_hours_with_uncertainty()):.2f}",
                f"{float(item.get_lead_hours_with_uncertainty()):.2f}",
                f"{float(item.get_reviewer_hours()):.2f}"
            ]

            for idx, content in enumerate(contents):
                row_cells[idx].text = content
                # Set font size for the paragraph
                for paragraph in row_cells[idx].paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(9)

    else:
        document.add_paragraph('No estimation items added yet.')

    document.add_paragraph()

    # Add summary section
    document.add_heading('Estimation Summary', level=2)
    document.add_paragraph('Hours include level-based uncertainty multipliers (Jr: 6x, Mid: 3x, Sr: 1.5x, Lead: 1x). Each level represents alternative estimates, not additive totals.')

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
        ('CODE REVIEWER (LEAD DEV)', ''),
        ('  Total Hours', estimation.get_total_reviewer_hours()),
        (f'  Contingency ({float(estimation.contingency_padding_percent or 0):.2f}%)', estimation.get_contingency_hours_reviewer()),
        ('  Grand Total', estimation.get_grand_total_reviewer_hours()),
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
                        run.font.size = Pt(9)
        else:
            row.cells[1].text = f"{float(value):.2f} hours"

            # Make grand total rows bold
            if 'Grand Total' in label:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.bold = True
                            run.font.size = Pt(9)
            else:
                # Regular rows - make smaller
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(9)

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
