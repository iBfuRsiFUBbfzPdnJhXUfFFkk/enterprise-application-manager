from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client


def fetch_project_merge_request(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> ProjectMergeRequest | None:
    if merge_request_internal_identification_iid is None or project_id is None:
        return None
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return None
    return cast(
        typ=ProjectMergeRequest,
        val=(
            git_lab_client.projects.get(project_id)
            .mergerequests.get(merge_request_internal_identification_iid)
        )
    )
