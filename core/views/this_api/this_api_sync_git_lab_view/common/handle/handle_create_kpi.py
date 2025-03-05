from core.models.person import Person
from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def handle_create_kpi(
        developer: Person | None = None,
        indicator_map: IndicatorMap | None = None,
        scrum_capacity_base: int | None = None,
        sprint: Sprint | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if developer is None or sprint is None:
        return indicator_map
    if not KeyPerformanceIndicatorSprint.objects.filter(
            person_developer=developer,
            sprint=sprint,
    ).exists():
        KeyPerformanceIndicatorSprint.objects.create(
            capacity_base=developer.scrum_capacity_base or scrum_capacity_base,
            sprint=sprint,
            person_developer=developer,
        )
    return indicator_map
