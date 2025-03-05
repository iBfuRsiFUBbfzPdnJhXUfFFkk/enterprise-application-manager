from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import Indicator
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def indicator_to_kpi_instance(
        indicator: Indicator | None = None,
        kpi_instance: KeyPerformanceIndicatorSprint | None = None,
) -> KeyPerformanceIndicatorSprint | None:
    if indicator is None:
        return None
    if kpi_instance is None:
        return None
    kpi_instance.number_of_code_lines_added = indicator["number_of_code_lines_added"]
    kpi_instance.number_of_code_lines_removed = indicator["number_of_code_lines_removed"]
    kpi_instance.number_of_comments_made = indicator["number_of_comments_made"]
    kpi_instance.number_of_context_switches = len(indicator["project_ids_worked_on"])
    kpi_instance.number_of_issues_written = indicator["number_of_issues_authored"]
    kpi_instance.number_of_merge_requests_approved = indicator["number_of_approvals"]
    kpi_instance.number_of_story_points_committed_to = indicator["number_of_issues_weights_committed_to"]
    kpi_instance.number_of_story_points_delivered = indicator["number_of_issues_weights_delivered_on"]
    kpi_instance.number_of_threads_made = indicator["number_of_threads_made"]
    return kpi_instance
