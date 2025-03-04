from typing import Mapping, TypedDict

from requests import get, Response

from core.utilities.git_lab.get_git_lab_url_base_projects_merge_requests_changes import \
    get_git_lab_url_base_projects_merge_requests_changes
from core.views.this_api.this_api_update_code_churn_view.parse_diff import parse_diff
from core.views.this_api.this_api_update_code_churn_view.update_code_churn_typed_dicts import Changes, Change


class FetchPullRequestChangesReturn(TypedDict):
    added: int
    removed: int


def fetch_pull_request_changes(
        connection_gitlab_hostname: str | None = None,
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        decrypted_token: str | None = None,
        project_id: str | None = None,
        pull_request_iid: str | None = None,
) -> FetchPullRequestChangesReturn | None:
    if (
            connection_gitlab_hostname is None
            or connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or decrypted_token is None
            or project_id is None
            or pull_request_iid is None
    ):
        return None
    url: str | None = get_git_lab_url_base_projects_merge_requests_changes(
        merge_request_internal_identification_iid=pull_request_iid,
        project_id=project_id,
    )
    if url is None:
        return None
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    response: Response = get(
        headers=headers,
        url=url,
    )
    response.raise_for_status()
    changes_data: Changes = response.json()
    changes: list[Change] | None = changes_data.get("changes")
    if changes is None:
        return None
    total_added: int = 0
    total_removed: int = 0

    for change in changes:
        diff_text: str | None = change.get("diff")
        if diff_text is None:
            continue
        parse_diff_tuple: tuple[int, int] | None = parse_diff(diff_text=diff_text)
        if parse_diff_tuple is None:
            continue
        added, removed = parse_diff_tuple
        total_added += added
        total_removed += removed
    return {
        "added": total_added,
        "removed": total_removed
    }
