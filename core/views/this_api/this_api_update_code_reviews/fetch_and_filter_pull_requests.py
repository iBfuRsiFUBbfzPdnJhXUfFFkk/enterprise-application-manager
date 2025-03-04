from datetime import datetime
from typing import Mapping

from requests import get, Response

from core.views.this_api.this_api_update_code_churn_view.update_code_churn_typed_dicts import MergeRequest


def fetch_and_filter_pull_requests(
        closed_after: str | None = None,
        closed_before: str | None = None,
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        connection_gitlab_hostname: str | None = None,
        decrypted_token: str | None = None,
) -> list[MergeRequest] | None:
    if (
            closed_after is None
            or closed_before is None
            or connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or connection_gitlab_hostname is None
            or decrypted_token is None
    ):
        return None
    filtered_pull_requests: list[dict] = []
    params = {
        "per_page": 100,
        "state": "merged",
        "updated_after": closed_after,
        "updated_before": closed_before,
    }
    url: str = (
        f"https://{connection_gitlab_hostname}/"
        f"api/v{connection_gitlab_api_version}/"
        f"groups/{connection_gitlab_group_id}/"
        f"merge_requests"
    )
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    while url is not None:
        response: Response = get(
            headers=headers,
            params=params,
            url=url,
        )
        response.raise_for_status()
        pull_requests: list[MergeRequest] = response.json()
        for pull_request in pull_requests:
            if "merged_at" in pull_request:
                merged_at: str | None = pull_request["merged_at"]
                if merged_at is None:
                    continue
                try:
                    merged_at_dt = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    merged_at_dt = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
                if closed_after <= merged_at_dt.strftime("%Y-%m-%dT%H:%M:%SZ") <= closed_before:
                    filtered_pull_requests.append(pull_request)
        url: str | None = response.links.get("next", {}).get("url")
    return filtered_pull_requests
