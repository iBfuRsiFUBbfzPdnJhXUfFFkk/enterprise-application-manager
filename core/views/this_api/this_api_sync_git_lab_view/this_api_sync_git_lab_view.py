from time import time

from django.http import HttpRequest, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group

from core.models.person import Person
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_issues import handle_group_issues
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_merge_requests import \
    handle_group_merge_requests
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, \
    create_initial_indicator_map
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_to_kpi_instance import indicator_to_kpi_instance
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def this_api_sync_git_lab_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_group: Group | None = fetch_git_lab_group(git_lab_client=git_lab_client)
    if git_lab_group is None:
        return generic_500(request=request)
    current_sprint: Sprint | None = Sprint.current_sprint()
    indicator_map: IndicatorMap = create_initial_indicator_map()
    if current_sprint is None:
        return generic_500(request=request)
    indicator_map: IndicatorMap = handle_group_merge_requests(
        current_sprint=current_sprint,
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
        indicator_map=indicator_map,
    )
    indicator_map: IndicatorMap = handle_group_issues(
        current_sprint=current_sprint,
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
        indicator_map=indicator_map,
    )
    number_of_new_kpi_records_created: int = 0
    number_of_updated_kpi_records: int = 0
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
            number_of_new_kpi_records_created += 1
        else:
            number_of_updated_kpi_records += 1
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
                "number_of_new_kpi_records_created": number_of_new_kpi_records_created,
                "number_of_updated_kpi_records": number_of_updated_kpi_records,
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
