from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest, Project

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_git_lab_project import fetch_git_lab_project


def fetch_project_merge_request(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> ProjectMergeRequest | None:
    if git_lab_project is None:
        git_lab_project: Project | None = fetch_git_lab_project(
            git_lab_client=git_lab_client,
            project_id=project_id,
        )
    if git_lab_project is None:
        return None
    if merge_request_internal_identification_iid is None:
        return None
    return cast(
        typ=ProjectMergeRequest,
        val=git_lab_project.mergerequests.get(id=merge_request_internal_identification_iid, lazy=True)
    )
