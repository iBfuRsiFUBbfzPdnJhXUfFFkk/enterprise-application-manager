from gitlab import Gitlab
from gitlab.v4.objects import GroupMergeRequest, User, Project, \
    ProjectMergeRequest

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_request import \
    fetch_project_merge_request
from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_project import fetch_git_lab_project
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_approvals import \
    handle_project_merge_request_approvals
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_changes import \
    handle_project_merge_request_changes
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_discussions import \
    handle_project_merge_request_discussions
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, create_initial_indicator_map


def handle_group_merge_request(
        git_lab_client: Gitlab | None = None,
        group_merge_request: GroupMergeRequest | None = None,
        indicator_map: dict[str, IndicatorMap] | None = None,
) -> dict[str, IndicatorMap]:
    if indicator_map is None:
        indicator_map: dict[str, IndicatorMap] = {}
    if git_lab_client is None:
        git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return indicator_map
    project_id: int | None = group_merge_request.project_id
    merge_request_internal_identification_iid: int | None = group_merge_request.iid
    if project_id is None:
        return indicator_map
    git_lab_project: Project | None = fetch_git_lab_project(
        git_lab_client=git_lab_client,
        project_id=project_id,
    )
    if git_lab_project is None:
        return indicator_map
    project_merge_request: ProjectMergeRequest | None = fetch_project_merge_request(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
    )
    if project_merge_request is None:
        return indicator_map
    author: User | None = group_merge_request.author
    if author is None:
        return indicator_map
    merge_request_author_username: str | None = author["username"]
    if merge_request_author_username is None:
        return indicator_map
    if merge_request_author_username not in indicator_map:
        indicator_map[merge_request_author_username] = create_initial_indicator_map()
    indicator_map: dict[str, IndicatorMap] = handle_project_merge_request_changes(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        indicator_map=indicator_map,
        merge_request_author_username=merge_request_author_username,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request,
    )
    indicator_map: dict[str, IndicatorMap] = handle_project_merge_request_discussions(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        indicator_map=indicator_map,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request,
    )
    indicator_map: dict[str, IndicatorMap] = handle_project_merge_request_approvals(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        indicator_map=indicator_map,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request,
    )
    return indicator_map
