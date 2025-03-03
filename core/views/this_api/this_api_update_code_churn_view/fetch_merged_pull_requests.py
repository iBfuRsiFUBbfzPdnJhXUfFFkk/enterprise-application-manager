from typing import Any, Mapping

from requests import get, Response

from core.views.this_api.this_api_update_code_churn_view.update_code_churn_typed_dicts import MergeRequest


def fetch_merged_pull_requests(
        connection_gitlab_hostname: str | None = None,
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        decrypted_token: str | None = None,
        merged_after: str | None = None,
        merged_before: str | None = None,
) -> list[MergeRequest] | None:
    if (
            connection_gitlab_hostname is None
            or connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or decrypted_token is None
            or merged_after is None
            or merged_before is None
    ):
        return None
    url: str = f"https://{connection_gitlab_hostname}/api/{connection_gitlab_api_version}/groups/{connection_gitlab_group_id}/merge_requests"
    parameters: dict[str, Any] = {
        "state": "merged",
        "updated_after": merged_after,
        "updated_before": merged_before,
        "per_page": 100,
    }
    all_pull_requests: list[MergeRequest] = []
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    while url is not None:
        response: Response = get(
            headers=headers,
            params=parameters,
            url=url,
        )
        response.raise_for_status()
        all_pull_requests.extend(response.json())
        url: str | None = response.links.get("next", {}).get("url")
    return all_pull_requests
