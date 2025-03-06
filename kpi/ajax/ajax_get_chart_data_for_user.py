from django.db.models import QuerySet
from django.http import JsonResponse, HttpRequest, HttpResponse

from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.models.user import User
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration
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
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    parent_base_capacity: int = this_server_configuration.scrum_capacity_base or 15
    last_five_sprints: QuerySet[Sprint] = Sprint.last_five()
    velocity_data = []
    accuracy_data = []
    sprint_labels = []

    for sprint in last_five_sprints:
        sprint_kpi: KeyPerformanceIndicatorSprint | None = KeyPerformanceIndicatorSprint.objects.filter(
            person_developer=person,
            sprint=sprint,
        ).first()
        base_capacity: int = sprint_kpi.capacity_base or parent_base_capacity
        number_of_paid_time_off_days: int = sprint_kpi.number_of_paid_time_off_days or 0
        number_of_story_points_delivered: int = sprint_kpi.number_of_story_points_delivered or 0
        number_of_story_points_committed_to: int = sprint_kpi.number_of_story_points_committed_to or 0

        if sprint_kpi is not None:
            adjusted_capacity = base_capacity - number_of_paid_time_off_days
            velocity = round(number_of_story_points_delivered / adjusted_capacity, 2) if adjusted_capacity > 0 else 0
            accuracy = round(number_of_story_points_delivered / number_of_story_points_committed_to,
                             2) if number_of_story_points_committed_to > 0 else 0
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
