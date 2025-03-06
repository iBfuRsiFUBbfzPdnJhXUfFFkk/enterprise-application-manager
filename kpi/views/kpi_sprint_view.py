from django.db.models import Sum
from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def kpi_sprint_view(request: HttpRequest, uuid: str) -> HttpResponse:
    sprint: Sprint | None = Sprint.get_by_uuid(uuid=uuid)
    sprint_kpis = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint)

    total_adjusted_capacity = sum(kpi.adjusted_capacity for kpi in sprint_kpis)
    total_delivered = sprint_kpis.aggregate(total=Sum("number_of_story_points_delivered"))["total"] or 0
    total_committed = sprint_kpis.aggregate(total=Sum("number_of_story_points_committed_to"))["total"] or 0

    # Calculate Capacity-Based Velocity
    velocity = round(total_delivered / total_adjusted_capacity, 2) if total_adjusted_capacity > 0 else 0

    # Calculate Commitment Accuracy
    commitment_accuracy = round(total_delivered / total_committed, 2) if total_committed > 0 else 0

    return base_render(
        context={
            "sprint": sprint,
            "sprint_kpis": sprint_kpis,
            "total_adjusted_capacity": total_adjusted_capacity,
            "total_delivered": total_delivered,
            "total_committed": total_committed,
            "velocity": velocity,  # Sprint-level Capacity-Based Velocity
            "commitment_accuracy": commitment_accuracy,  # Sprint-level Commitment Accuracy
            "sprint_start_date": sprint.date_start,
            "sprint_end_date": sprint.date_end,
        },
        request=request,
        template_name="authenticated/kpi/kpi_sprints.html"
    )


def _calculate_sprint_metrics(sprint):
    """Calculate key metrics for a single sprint using model properties"""
    kpis = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint)

    # Calculate totals using model properties
    total_capacity = sum(kpi.adjusted_capacity for kpi in kpis)
    total_delivered = sum((kpi.number_of_story_points_delivered or 0) for kpi in kpis)
    total_committed = sum((kpi.number_of_story_points_committed_to or 0) for kpi in kpis)
    total_reviews = sum((kpi.number_of_merge_requests_approved or 0) for kpi in kpis)

    return {
        "sprint": sprint,
        "capacity": total_capacity,
        "delivered": total_delivered,
        "committed": total_committed,
        "reviews": total_reviews,
        "velocity": _safe_divide(total_delivered, total_capacity),
        "accuracy": _safe_divide(total_delivered, total_committed),
    }


def _calculate_average_metrics(completed_metrics):
    """Calculate weighted averages considering capacity"""
    if not completed_metrics:
        return None

    # Calculate weighted averages for velocity
    total_capacity = sum(m["capacity"] for m in completed_metrics)
    total_delivered = sum(m["delivered"] for m in completed_metrics)
    weighted_velocity = _safe_divide(total_delivered, total_capacity)

    # Calculate simple averages for other metrics
    avg_accuracy = sum(m["accuracy"] for m in completed_metrics) / len(completed_metrics)
    avg_delivered = sum(m["delivered"] for m in completed_metrics) / len(completed_metrics)
    avg_reviews = sum(m["reviews"] for m in completed_metrics) / len(completed_metrics)

    return {
        "velocity": weighted_velocity,
        "accuracy": avg_accuracy,
        "delivered": avg_delivered,
        "reviews": avg_reviews,
    }


def _safe_divide(a, b):
    """Safe division helper with proper rounding"""
    return round(a / b, 2) if b and b > 0 else 0
