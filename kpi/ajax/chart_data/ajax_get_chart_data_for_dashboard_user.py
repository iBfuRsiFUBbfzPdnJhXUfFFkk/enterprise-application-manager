from django.http import HttpRequest, JsonResponse

from core.models.sprint import Sprint
from core.models.user import User
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def ajax_get_chart_data_for_dashboard_user(
        request: HttpRequest,
        uuid: str,
):
    user = User.get_by_uuid(uuid=uuid)
    developer = user.person_mapping

    # Get the last 5 completed sprints
    completed_sprints = Sprint.last_five()

    # Fetch metrics for the developer in each sprint
    velocity_data = []
    accuracy_data = []
    sprint_labels = []

    for sprint in completed_sprints:
        sprint_kpi = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint, person_developer=developer).first()

        if sprint_kpi:
            adjusted_capacity = sprint_kpi.coerced_base_capacity - sprint_kpi.number_of_paid_time_off_days
            velocity = round((sprint_kpi.number_of_story_points_delivered or 0) / adjusted_capacity, 2) if adjusted_capacity > 0 else 0
            accuracy = round((sprint_kpi.number_of_story_points_delivered or 0) / (sprint_kpi.number_of_story_points_committed_to or 0), 2) if (sprint_kpi.number_of_story_points_committed_to or 0) > 0 else 0
        else:
            velocity = 0
            accuracy = 0

        sprint_labels.append(sprint.name)
        velocity_data.append(velocity)
        accuracy_data.append(accuracy)

    # Prepare data for the charts
    data = {
        "labels": sprint_labels[::-1],  # Reverse order for chronological display
        "velocity": velocity_data[::-1],
        "accuracy": accuracy_data[::-1],
    }

    return JsonResponse(data)