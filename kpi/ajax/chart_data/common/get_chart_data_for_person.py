from django.db.models import QuerySet

from core.models.person import Person
from core.models.sprint import Sprint
from kpi.ajax.chart_data.common.chart_data_model import ChartDataModel
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def get_chart_data_for_person(
        person: Person | None = None
) -> ChartDataModel | None:
    last_five_sprints: QuerySet[Sprint] = Sprint.last_five()
    velocity_data: list[float] = []
    accuracy_data: list[float] = []
    sprint_labels: list[str] = []

    for sprint in last_five_sprints:
        sprint_kpi: KeyPerformanceIndicatorSprint | None = KeyPerformanceIndicatorSprint.objects.filter(
            person_developer=person,
            sprint=sprint,
        ).first()
        if sprint_kpi is not None:
            base_capacity: int = sprint_kpi.coerced_scrum_capacity_base
            number_of_paid_time_off_days: int = sprint_kpi.coerced_number_of_paid_time_off_days
            number_of_story_points_delivered: int = sprint_kpi.coerced_number_of_story_points_delivered
            number_of_story_points_committed_to: int = sprint_kpi.coerced_number_of_story_points_committed_to
            adjusted_capacity: int = base_capacity - number_of_paid_time_off_days
            if adjusted_capacity > 0:
                velocity: float = round(
                    ndigits=2,
                    number=number_of_story_points_delivered / adjusted_capacity,
                )
            else:
                velocity: float = 0
            if number_of_story_points_committed_to > 0:
                accuracy: float = round(
                    ndigits=2,
                    number=number_of_story_points_delivered / number_of_story_points_committed_to,
                )
            else:
                accuracy: float = 0
        else:
            velocity: float = 0
            accuracy: float = 0

        sprint_labels.append(sprint.name)
        velocity_data.append(velocity)
        accuracy_data.append(accuracy)

    for index in range(5 - len(last_five_sprints)):
        velocity_data.append(0)
        accuracy_data.append(0)
        sprint_labels.append("No Sprint Data")

    return {
        "accuracy": accuracy_data[::-1],
        "labels": sprint_labels[::-1],
        "velocity": velocity_data[::-1],
    }
