from typing import Mapping

from requests import Response, get


def calculate_committed_issues(
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        connection_gitlab_hostname: str | None = None,
        decrypted_token: str | None = None,
        iteration_id: str | None = None,
) -> list[dict] | None:
    if (
            connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or connection_gitlab_hostname is None
            or decrypted_token is None
            or iteration_id is None
    ):
        return None
    all_issues: list[dict] = []
    params = {
        "iteration_id": iteration_id,
        "per_page": 100,
        "state": "all",
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
        issues = response.json()
        all_issues.extend(issues)
        url: str | None = response.links.get("next", {}).get("url")
    return all_issues