from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_approvals import \
    fetch_project_merge_requests_approvals, GitLabApproval
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, create_initial_indicator_map


def handle_project_merge_request_approvals(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: dict[str, IndicatorMap] | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> dict[str, IndicatorMap]:
    if indicator_map is None:
        indicator_map: dict[str, IndicatorMap] = {}
    approvals: list[GitLabApproval] | None = fetch_project_merge_requests_approvals(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request
    )
    if approvals is None:
        return indicator_map
    for approval in approvals:
        approved_by_username: str | None = approval["username"]
        if approved_by_username is None:
            continue
        if approved_by_username not in indicator_map:
            indicator_map[approved_by_username] = create_initial_indicator_map()
        indicator_map[approved_by_username]["number_of_approvals"] += 1
    return indicator_map
