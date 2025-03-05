from typing import cast, TypedDict

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequestApprovalRule

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client


class GitLabApproval(TypedDict):
    id: str | None
    username: str | None


def fetch_project_merge_requests_approvals(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> list[GitLabApproval] | None:
    if merge_request_internal_identification_iid is None or project_id is None:
        return None
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return None
    approval_rules: list[ProjectMergeRequestApprovalRule] = cast(
        typ=list[ProjectMergeRequestApprovalRule],
        val=(
            git_lab_client.projects.get(project_id)
            .mergerequests.get(merge_request_internal_identification_iid)
            .approval_state.get().rules
        )
    )
    if len(approval_rules) == 0:
        return None
    return approval_rules[0]["approved_by"]
