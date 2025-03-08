from io import BytesIO

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from openpyxl.styles import Font, Side, PatternFill, Border
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook

from core.models.sprint import Sprint
from core.views.generic.generic_500 import generic_500
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def kpi_sprint_export_view(request: HttpRequest, uuid: str) -> HttpResponse:
    sprint: Sprint | None = Sprint.from_uuid(uuid=uuid)
    if sprint is None:
        return generic_500(request=request)
    sprint_kpis: QuerySet[KeyPerformanceIndicatorSprint] = KeyPerformanceIndicatorSprint.from_sprint(sprint=sprint)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Sprint {sprint.name} KPIs"

    color_white: str = "FFFFFF"
    color_light_grey: str = "D3D3D3"
    color_blue: str = "4F81BD"
    thin_side = Side(style="thin")
    thick_side = Side(style="thick")
    header_font = Font(
        bold=True,
        color=color_white
    )
    group_header_fill = PatternFill(
        end_color=color_blue,
        fill_type="solid",
        start_color=color_blue,
    )
    subheader_fill = PatternFill(
        end_color=color_light_grey,
        fill_type="solid",
        start_color=color_light_grey,
    )
    thin_border = Border(
        bottom=thin_side,
        left=thin_side,
        right=thin_side,
        top=thin_side,
    )
    thick_border = Border(
        bottom=thick_side,
        left=thick_side,
        right=thick_side,
        top=thick_side,
    )

    group_headers: list[tuple[str, int, int]] = [
        ("Developer", 1, 1),
        ("Availability", 2, 5),
        ("Commitments", 6, 7),
        ("Code Review Activity", 8, 10),
        ("Development Output", 11, 13),
        ("Performance Metrics", 14, 15),
    ]

    sheet.append([""] * 15)
    sheet.append(
        [
            "Developer",
            "Base Capacity",
            "Holidays",
            "PTO Days",
            "Adjusted Capacity",
            "Committed",
            "Delivered",
            "Reviews",
            "Comments",
            "Threads",
            "Issues",
            "Code Changes",
            "Context Switching",
            "Velocity",
            "Accuracy",
        ]
    )

    for title, start_col, end_col in group_headers:
        cell = sheet.cell(row=1, column=start_col, value=title)
        cell.font = header_font
        cell.fill = group_header_fill
        cell.border = thick_border

        if start_col != end_col:
            sheet.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
            for col in range(start_col, end_col + 1):
                sheet.cell(row=1, column=col).border = thick_border

    for col in range(1, 16):
        cell = sheet.cell(row=2, column=col)
        cell.font = Font(bold=True)
        cell.fill = subheader_fill
        cell.border = thin_border
        sheet.column_dimensions[get_column_letter(col)].width = 15

    for kpi in sprint_kpis:
        code_changes = f"+{kpi.coerced_number_of_code_lines_added}/-{kpi.coerced_number_of_code_lines_removed} lines"
        person = kpi.person_developer
        sprint = kpi.sprint

        row = [
            person.gitlab_sync_username if person else "N/A",
            kpi.coerced_scrum_capacity_base,
            sprint.number_of_holidays_during_sprint if sprint else 0,
            kpi.coerced_number_of_paid_time_off_days,
            kpi.adjusted_capacity,
            kpi.coerced_number_of_story_points_committed_to,
            kpi.coerced_number_of_story_points_delivered,
            kpi.coerced_number_of_merge_requests_approved,
            kpi.coerced_number_of_comments_made,
            kpi.coerced_number_of_threads_made,
            kpi.coerced_number_of_issues_written,
            code_changes,
            kpi.coerced_number_of_context_switches,
            kpi.capacity_based_velocity,
            kpi.commitment_accuracy,
        ]

        sheet.append(row)

    for row in sheet.iter_rows(min_row=3):
        for cell in row:
            cell.border = thin_border
            if cell.column_letter in ["N", "O"]:
                cell.number_format = "0.00"

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        content=output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="sprint_{sprint.name}_kpis.xlsx"'
    return response

