from django.db.models import QuerySet

from core.models.person import Person
from core.models.role import Role
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_create_kpi import handle_create_kpi
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map


def handle_create_kpis(
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    this_server_configuration: ThisServerConfiguration | None = ThisServerConfiguration.objects.last()
    if this_server_configuration is None:
        return indicator_map
    scrum_capacity_base: int | None = this_server_configuration.scrum_capacity_base
    type_developer_role: Role | None = this_server_configuration.type_developer_role
    if type_developer_role is None:
        return indicator_map
    type_developer_role_id: int = type_developer_role.id
    sprints: QuerySet = Sprint.objects.all()
    if not sprints.exists():
        return indicator_map
    developers: QuerySet = Person.objects.filter(roles__in=[type_developer_role_id])
    if not developers.exists():
        return indicator_map
    for sprint in sprints:
        for developer in developers:
            indicator_map: IndicatorMap = handle_create_kpi(
                developer=developer,
                indicator_map=indicator_map,
                scrum_capacity_base=scrum_capacity_base,
                sprint=sprint,
            )
    return indicator_map
