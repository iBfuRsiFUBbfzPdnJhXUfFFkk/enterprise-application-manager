from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_approvals import \
    fetch_project_merge_requests_approvals
from core.views.this_api.this_api_sync_git_lab_view.common.handle.handle_project_merge_request_approval import \
    handle_project_merge_request_approval
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import ensure_indicator_map, IndicatorMap
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


def handle_project_merge_request_approvals(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: IndicatorMap | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    approvals: list[GitLabApiUser] | None = fetch_project_merge_requests_approvals(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request
    )
    if approvals is None:
        return indicator_map
    for approval in approvals:
        indicator_map: IndicatorMap = handle_project_merge_request_approval(
            approval=approval,
            indicator_map=indicator_map,
        )
    return indicator_map
