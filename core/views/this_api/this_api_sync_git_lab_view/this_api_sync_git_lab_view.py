from time import time

from django.http import HttpRequest, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group

from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_group import fetch_git_lab_group
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_issues import handle_group_issues
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_members import handle_group_members
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_group_merge_requests import \
    handle_group_merge_requests
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, \
    create_initial_indicator_map
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map_to_kpi_instances import \
    indicator_map_to_kpi_instances, KpiInstanceStats


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
    indicator_map: IndicatorMap = handle_group_members(
        git_lab_client=git_lab_client,
        git_lab_group=git_lab_group,
        indicator_map=indicator_map,
    )
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
    stats: KpiInstanceStats = indicator_map_to_kpi_instances(
        current_sprint=current_sprint,
        indicator_map=indicator_map,
    )
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
                **stats
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
