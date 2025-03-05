from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequestDiscussion, Project, \
    ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_discussions import \
    fetch_project_merge_requests_discussions
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_discussion import \
    handle_project_merge_request_discussion
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map


def handle_project_merge_request_discussions(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: IndicatorMap | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    discussions: list[ProjectMergeRequestDiscussion] | None = fetch_project_merge_requests_discussions(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request
    )
    if discussions is None:
        return indicator_map
    for discussion in discussions:
        indicator_map: IndicatorMap = handle_project_merge_request_discussion(
            discussion=discussion,
            indicator_map=indicator_map,
        )
    return indicator_map
