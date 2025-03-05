from typing import cast, TypedDict

from gitlab.v4.objects import ProjectMergeRequestApprovalRule, ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch_project_merge_request import \
    fetch_project_merge_request


class GitLabApproval(TypedDict):
    id: str | None
    username: str | None


def fetch_project_merge_requests_approvals(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> list[GitLabApproval] | None:
    project_merge_request: ProjectMergeRequest | None = fetch_project_merge_request(
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
    )
    if project_merge_request is None:
        return None
    approval_rules: list[ProjectMergeRequestApprovalRule] = cast(
        typ=list[ProjectMergeRequestApprovalRule],
        val=project_merge_request.approval_state.get().rules
    )
    if len(approval_rules) == 0:
        return None
    return approval_rules[0]["approved_by"]
