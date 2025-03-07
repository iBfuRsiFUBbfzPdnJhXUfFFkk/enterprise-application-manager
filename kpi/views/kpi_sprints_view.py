from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def kpi_sprints_view(request: HttpRequest) -> HttpResponse:
    current_sprint: Sprint | None = Sprint.current_sprint()
    completed_sprints: QuerySet[Sprint] | None = Sprint.last_five()
    current_metrics = _calculate_sprint_metrics(current_sprint) if current_sprint else None
    completed_metrics = [_calculate_sprint_metrics(sprint) for sprint in completed_sprints]
    avg_metrics = _calculate_average_metrics(completed_metrics)
    return base_render(
        context={
            "sprints": Sprint.objects.all(),
            "current_sprint": current_metrics,
            "avg_completed_metrics": avg_metrics,
            "completed_sprints_count": len(completed_sprints),
        },
        request=request,
        template_name="authenticated/kpi/kpi_sprints.html"
    )


def _calculate_sprint_metrics(sprint):
    """Calculate key metrics for a single sprint using model properties"""
    kpis = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint)

    # Calculate totals using model properties
    total_capacity = sum(kpi.adjusted_capacity for kpi in kpis)
    total_delivered = sum(kpi.coerced_number_of_story_points_delivered for kpi in kpis)
    total_committed = sum(kpi.coerced_number_of_story_points_committed_to for kpi in kpis)
    total_reviews = sum(kpi.coerced_number_of_merge_requests_approved  for kpi in kpis)

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
