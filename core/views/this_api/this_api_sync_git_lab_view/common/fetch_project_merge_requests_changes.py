from typing import cast, TypedDict

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest, Project

from core.views.this_api.this_api_sync_git_lab_view.common.fetch_project_merge_request import \
    fetch_project_merge_request


class GitLabChange(TypedDict):
    diff: str | None


def fetch_project_merge_requests_changes(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
        project_merge_request: ProjectMergeRequest | None = None
) -> list[GitLabChange] | None:
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
        typ=list[GitLabChange],
        val=project_merge_request.changes(get_all=True)["changes"]
    )
