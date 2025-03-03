from typing import Mapping

from requests import get, Response


def fetch_discussions_for_pull_requests(
        connection_gitlab_hostname: str | None = None,
        connection_gitlab_api_version: str | None = None,
        connection_gitlab_group_id: str | None = None,
        decrypted_token: str | None = None,
        project_id: str | None = None,
        pull_request_iid: str | None = None,
) -> list[dict] | None:
    if (
            connection_gitlab_hostname is None
            or connection_gitlab_api_version is None
            or connection_gitlab_group_id is None
            or decrypted_token is None
            or project_id is None
            or pull_request_iid is None
    ):
        return None
    url: str = f"https://{connection_gitlab_hostname}/api/{connection_gitlab_api_version}/projects/{project_id}/merge_requests/{pull_request_iid}/discussions"
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    discussions: list[dict] = []
    while url is not None:
        response: Response = get(
            headers=headers,
            url=url,
        )
        response.raise_for_status()
        discussions.extend(response.json())
        url: str | None = response.links.get("next", {}).get("url")
    return discussions
