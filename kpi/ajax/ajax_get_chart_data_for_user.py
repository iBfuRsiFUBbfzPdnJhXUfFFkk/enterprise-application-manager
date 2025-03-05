from django.db.models import QuerySet
from django.http import JsonResponse, HttpRequest, HttpResponse

from core.models.person import Person
from core.models.sprint import Sprint
from core.models.user import User
from core.views.generic.generic_500 import generic_500
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def ajax_get_chart_data_for_user(
        request: HttpRequest,
        uuid: str
) -> JsonResponse | HttpResponse:
    user: User | None = User.get_by_uuid(uuid=uuid)
    if user is None:
        return generic_500(request=request)
    person: Person | None = user.person_mapping
    if person is None:
        return generic_500(request=request)
    last_five_sprints: QuerySet[Sprint] = Sprint.last_five()
    velocity_data = []
    accuracy_data = []
    sprint_labels = []

    for sprint in last_five_sprints:
        sprint_kpi = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint, developer=person).first()

        if sprint_kpi:
            adjusted_capacity = sprint_kpi.capacity_base - sprint_kpi.number_of_paid_time_off_days
            velocity = round(sprint_kpi.number_of_story_points_delivered / adjusted_capacity, 2) if adjusted_capacity > 0 else 0
            accuracy = round(sprint_kpi.number_of_story_points_delivered / sprint_kpi.number_of_story_points_committed_to, 2) if sprint_kpi.number_of_story_points_committed_to > 0 else 0
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
    return JsonResponse(data=data)