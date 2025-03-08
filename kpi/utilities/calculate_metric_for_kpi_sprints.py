from typing import TypedDict

from django.db.models import QuerySet

from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from kpi.utilities.safe_divide import safe_divide


class KpiSprintMetric(TypedDict):
    accuracy: float
    capacity: int
    committed: int
    delivered: int
    reviews: int
    velocity: float

def get_initial_kpi_sprint_metric() -> KpiSprintMetric:
    return {
        "accuracy": 0.0,
        "capacity": 0,
        "committed": 0,
        "delivered": 0,
        "reviews": 0,
        "velocity": 0.0,
    }


def calculate_metric_for_kpi_sprints(
        kpi_sprints: QuerySet[KeyPerformanceIndicatorSprint] | None = None,
) -> KpiSprintMetric:
    if kpi_sprints is None:
        return get_initial_kpi_sprint_metric()
    total_capacity: int = sum(
        kpi_sprint.adjusted_capacity
        for kpi_sprint
        in kpi_sprints
    )
    total_delivered: int = sum(
        kpi_sprint.coerced_number_of_story_points_delivered
        for kpi_sprint
        in kpi_sprints
    )
    total_committed: int = sum(
        kpi_sprint.coerced_number_of_story_points_committed_to
        for kpi_sprint
        in kpi_sprints
    )
    total_reviews: int = sum(
        kpi_sprint.coerced_number_of_merge_requests_approved
        for kpi_sprint
        in kpi_sprints
    )
    velocity: float = safe_divide(
        dividend=total_delivered,
        divisor=total_capacity,
    )
    accuracy: float = safe_divide(
        dividend=total_delivered,
        divisor=total_committed,
    )

    return {
        "accuracy": round(accuracy, 2),
        "capacity": total_capacity,
        "committed": total_committed,
        "delivered": total_delivered,
        "reviews": total_reviews,
        "velocity": round(velocity, 2),
    }
