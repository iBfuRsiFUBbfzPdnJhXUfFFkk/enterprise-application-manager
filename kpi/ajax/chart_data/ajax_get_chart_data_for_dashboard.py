from django.http import JsonResponse, HttpRequest, HttpResponse

from core.models.sprint import Sprint
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from kpi.utilities.calculate_sprint_metrics import calculate_sprint_metrics


def ajax_get_chart_data_for_dashboard(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    completed_sprints = Sprint.last_five()

    if request.user.is_staff or request.user.is_superuser:
        velocity_data = [sprint.velocity for sprint in completed_sprints]
        accuracy_data = [sprint.accuracy for sprint in completed_sprints]
    else:
        velocity_data = [
            calculate_sprint_metrics(KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint,
                                                                                  person_developer=request.user.person_mapping))[
                "velocity"] for
            sprint in completed_sprints
        ]
        accuracy_data = [
            calculate_sprint_metrics(KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint,
                                                                                  person_developer=request.user.person_mapping))[
                "accuracy"] for
            sprint in completed_sprints
        ]

    # Prepare data for the charts
    data = {
        "labels": [sprint.name for sprint in completed_sprints],
        "velocity": velocity_data,
        "accuracy": accuracy_data,
    }
    return JsonResponse(data=data)
