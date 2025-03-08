from django.db.models import QuerySet
from math import floor

from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from core.utilities.safe_divide import safe_divide
from kpi.utilities.scoped_metrics.scoped_metric import ScopedMetric, get_initial_scoped_metric


def calculate_scoped_metric(
        kpi_sprints: QuerySet[KeyPerformanceIndicatorSprint] | None = None,
) -> ScopedMetric:
    scoped_metric: ScopedMetric = get_initial_scoped_metric()
    if kpi_sprints is None:
        return scoped_metric
    kpi_sprints_length: int = len(kpi_sprints)
    if kpi_sprints_length == 0:
        return scoped_metric
    scoped_metric["total_adjusted_capacity"] = floor(
        sum(
            kpi_sprint.adjusted_capacity
            for kpi_sprint
            in kpi_sprints
        ) / kpi_sprints_length
    )
    scoped_metric["total_story_points_delivered"] = floor(
        sum(
            kpi_sprint.coerced_number_of_story_points_delivered
            for kpi_sprint
            in kpi_sprints
        ) / kpi_sprints_length
    )
    scoped_metric["total_story_points_committed_to"] = floor(
        sum(
            kpi_sprint.coerced_number_of_story_points_committed_to
            for kpi_sprint
            in kpi_sprints
        ) / kpi_sprints_length
    )
    scoped_metric["total_merge_requests_approved"] = floor(
        sum(
            kpi_sprint.coerced_number_of_merge_requests_approved
            for kpi_sprint
            in kpi_sprints
        ) / kpi_sprints_length
    )
    scoped_metric["total_velocity_of_capacity"] = safe_divide(
        dividend=scoped_metric["total_story_points_delivered"],
        divisor=scoped_metric["total_adjusted_capacity"],
    ) / kpi_sprints_length
    scoped_metric["total_accuracy_on_committed_to_story_points"] = safe_divide(
        dividend=scoped_metric["total_story_points_delivered"],
        divisor=scoped_metric["total_story_points_committed_to"],
    ) / kpi_sprints_length
    return scoped_metric
