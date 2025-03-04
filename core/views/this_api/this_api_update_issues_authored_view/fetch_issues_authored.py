from typing import Mapping

from requests import get, Response

from core.views.this_api.this_api_update_code_churn_view.update_code_churn_typed_dicts import MergeRequest


def fetch_issues_authored(
        closed_after: str | None = None,
        closed_before: str | None = None,
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        connection_gitlab_hostname: str | None = None,
        decrypted_token: str | None = None,
) -> dict | None:
    if (
            closed_after is None
            or closed_before is None
            or connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or connection_gitlab_hostname is None
            or decrypted_token is None
    ):
        return None
    all_issues: list[dict] = []
    params = {
        "per_page": 100,
        "state": "merged",
        "updated_after": closed_after,
        "updated_before": closed_before,
    }
    url: str = (
        f"https://{connection_gitlab_hostname}/"
        f"api/{connection_gitlab_api_version}/"
        f"groups/{connection_gitlab_group_id}/"
        f"issues"
    )
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    while url is not None:
        response: Response = get(
            headers=headers,
            params=params,
            url=url,
        )
        response.raise_for_status()
        issues: list[MergeRequest] = response.json()
        all_issues.extend(issues)
        url: str | None = response.links.get("next", {}).get("url")
    author_counts = {}
    for issue in all_issues:
        author_username = issue.get("author", {}).get("username", "unknown_user")
        if author_username not in author_counts:
            author_counts[author_username] = 0
        author_counts[author_username] += 1
    return author_counts
