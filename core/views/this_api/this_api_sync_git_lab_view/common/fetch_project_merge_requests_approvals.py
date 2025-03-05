from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequestApprovalState

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client


def fetch_project_merge_requests_approvals(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> list[ProjectMergeRequestApprovalState] | None:
    if merge_request_internal_identification_iid is None or project_id is None:
        return None
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return None
    return cast(
        typ=list[ProjectMergeRequestApprovalState],
        val=(
            git_lab_client.projects.get(project_id)
            .mergerequests.get(merge_request_internal_identification_iid)
            .approval_state.list()
        )
    )
