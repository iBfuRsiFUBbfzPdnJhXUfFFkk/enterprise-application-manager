from typing import cast

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest, Project

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_request import \
    fetch_project_merge_request
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_change import GitLabApiChange


def fetch_project_merge_requests_changes(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
        project_merge_request: ProjectMergeRequest | None = None
) -> list[GitLabApiChange] | None:
    if project_merge_request is None:
        project_merge_request: ProjectMergeRequest | None = fetch_project_merge_request(
            git_lab_client=git_lab_client,
            git_lab_project=git_lab_project,
            merge_request_internal_identification_iid=merge_request_internal_identification_iid,
            project_id=project_id,
        )
    if project_merge_request is None:
        return None
    return cast(
        typ=list[GitLabApiChange],
        val=project_merge_request.changes(get_all=True, lazy=True)["changes"]
    )
