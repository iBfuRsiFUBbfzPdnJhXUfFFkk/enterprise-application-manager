from django.http import HttpRequest, HttpResponse

from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from kpi.utilities.calculate_average_metrics import calculate_average_metrics
from kpi.utilities.calculate_sprint_metrics import calculate_sprint_metrics


def kpi_dashboard_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    # Get current sprint
    current_sprint = Sprint.current_sprint()
    completed_sprints = Sprint.last_five()

    # Adjust data retrieval for developers vs. superusers
    if user.is_staff or user.is_superuser:
        current_metrics = (
            calculate_sprint_metrics(KeyPerformanceIndicatorSprint.objects.filter(sprint=current_sprint).exclude(
                person_developer__user__is_superuser=True)) if current_sprint else None
        )
        completed_metrics = [
            calculate_sprint_metrics(KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint).exclude(
                person_developer__user__is_superuser=True)) for
            sprint in completed_sprints
        ]
        developer = None  # Not a single developer
    else:
        developer = user.person_mapping
        current_metrics = calculate_sprint_metrics(
            KeyPerformanceIndicatorSprint.objects.filter(sprint=current_sprint,
                                                         person_developer=developer)) if current_sprint else None
        completed_metrics = [calculate_sprint_metrics(
            KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint, person_developer=developer)) for
                             sprint in completed_sprints]

    # Compute averages
    avg_metrics = calculate_average_metrics(completed_metrics)

    # Fetch all sprints for the user (if not admin)
    sprint_kpis = KeyPerformanceIndicatorSprint.objects.filter(person_developer=developer).order_by(
        "-sprint__date_end") if developer else []
    return base_render(
        context={
            "developer": developer,
            "current_sprint": current_sprint,
            "current_metrics": current_metrics,
            "completed_sprints": completed_sprints,
            "avg_metrics": avg_metrics,
            "sprint_kpis": sprint_kpis,
        },
        request=request,
        template_name="authenticated/kpi/kpi_dashboard_admin.html" if (
                    user.is_staff or user.is_superuser) else "authenticated/kpi/kpi_dashboard_person.html"
    )
