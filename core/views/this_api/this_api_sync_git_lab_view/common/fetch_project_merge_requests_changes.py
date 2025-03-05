from typing import cast

from gitlab.v4.objects import ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch_project_merge_request import \
    fetch_project_merge_request


def fetch_project_merge_requests_changes(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> list[dict] | None:
    project_merge_request: ProjectMergeRequest | None = fetch_project_merge_request(
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
    )
    if project_merge_request is None:
        return None
    return cast(
        typ=list[dict],
        val=project_merge_request.changes(get_all=True)["changes"]
    )
