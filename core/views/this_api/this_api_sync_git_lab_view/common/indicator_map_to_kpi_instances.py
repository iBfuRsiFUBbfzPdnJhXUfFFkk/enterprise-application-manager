from typing import TypedDict

from core.models.person import Person
from core.models.sprint import Sprint
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_to_kpi_instance import indicator_to_kpi_instance
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


class KpiInstanceStats(TypedDict):
    number_of_new_kpi_records_created: int
    number_of_updated_kpi_records: int


def indicator_map_to_kpi_instances(
        current_sprint: Sprint | None = None,
        indicator_map: IndicatorMap | None = None
) -> KpiInstanceStats:
    stats: KpiInstanceStats = {
        "number_of_new_kpi_records_created": 0,
        "number_of_updated_kpi_records": 0,
    }
    if indicator_map is None or current_sprint is None:
        return stats
    for git_lab_user_id, indicator in indicator_map.items():
        person_instance: Person | None = Person.objects.filter(gitlab_sync_id=git_lab_user_id).first()
        if person_instance is None:
            continue
        kpi_instance, did_create = KeyPerformanceIndicatorSprint.objects.get_or_create(
            person_developer=person_instance,
            sprint=current_sprint,
        )
        kpi_instance: KeyPerformanceIndicatorSprint | None = indicator_to_kpi_instance(
            indicator=indicator,
            kpi_instance=kpi_instance,
        )
        if kpi_instance is None:
            continue
        kpi_instance.save()
        if did_create:
            stats["number_of_new_kpi_records_created"] += 1
        else:
            stats["number_of_updated_kpi_records"] += 1
    return stats
