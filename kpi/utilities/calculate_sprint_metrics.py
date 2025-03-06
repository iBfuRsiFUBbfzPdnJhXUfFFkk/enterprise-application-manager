from typing import TypedDict

from django.db.models import QuerySet
from django.db.models import Sum

from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


class SprintMetrics(TypedDict):
    accuracy: float
    capacity: int
    committed: int
    delivered: int
    reviews: int
    velocity: float


def calculate_sprint_metrics(
        kpi_sprints: QuerySet[KeyPerformanceIndicatorSprint] | None = None,
) -> SprintMetrics | None:
    if kpi_sprints is None:
        return None
    total_capacity: int = sum(kpi_sprint.adjusted_capacity for kpi_sprint in kpi_sprints)
    total_delivered: int = sum((kpi_sprint.number_of_story_points_delivered or 0) for kpi_sprint in kpi_sprints)
    total_committed: int = kpi_sprints.aggregate(Sum("number_of_story_points_committed_to"))[
                               "number_of_story_points_committed_to__sum"] or 0
    total_reviews: int = kpi_sprints.aggregate(Sum("number_of_merge_requests_approved"))[
                             "number_of_merge_requests_approved__sum"] or 0
    velocity: float = total_delivered / total_capacity if total_capacity else 0
    accuracy: float = total_delivered / total_committed if total_committed else 0

    return {
        "accuracy": round(accuracy, 2),
        "capacity": total_capacity,
        "committed": total_committed,
        "delivered": total_delivered,
        "reviews": total_reviews,
        "velocity": round(velocity, 2),
    }
