from typing import Mapping, TypedDict, Optional, Dict, List

from requests import get, Response

class Author(TypedDict):
    id: int
    username: str
    name: str
    state: str
    locked: bool
    avatar_url: str
    web_url: str

class Note(TypedDict):
    id: Optional[int]
    type: Optional[str]
    body: Optional[str]
    attachment: Optional[str]
    author: Author
    created_at: Optional[str]
    updated_at: Optional[str]
    system: Optional[bool]
    noteable_id: Optional[int]
    noteable_type: Optional[str]
    project_id: Optional[int]
    resolvable: Optional[bool]
    confidential: Optional[bool]
    internal: Optional[bool]
    imported: Optional[bool]
    imported_from: Optional[str]
    noteable_iid: Optional[int]
    commands_changes: Optional[Dict]

class NoteEntry(TypedDict):
    id: Optional[str]
    individual_note: Optional[bool]
    notes: Optional[List[Note]]


def fetch_discussions_for_pull_requests(
        connection_gitlab_hostname: str | None = None,
        connection_gitlab_api_version: str | None = None,
        decrypted_token: str | None = None,
        project_id: str | None = None,
        pull_request_iid: str | None = None,
) -> list[NoteEntry] | None:
    if (
            connection_gitlab_hostname is None
            or connection_gitlab_api_version is None
            or decrypted_token is None
            or project_id is None
            or pull_request_iid is None
    ):
        return None
    url: str = (
        f"https://{connection_gitlab_hostname}/"
        f"api/v{connection_gitlab_api_version}/"
        f"projects/{project_id}/"
        f"merge_requests/{pull_request_iid}/"
        f"discussions"
    )
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    discussions: list[NoteEntry] = []
    while url is not None:
        response: Response = get(
            headers=headers,
            url=url,
        )
        response.raise_for_status()
        discussions.extend(response.json())
        url: str | None = response.links.get("next", {}).get("url")
    return discussions
