from typing import Mapping, Optional, TypedDict, List

from requests import get, Response

class User(TypedDict):
    id: int
    username: str
    name: str
    state: str
    locked: bool
    avatar_url: str
    web_url: str

class ApprovedBy(TypedDict):
    user: User

class MergeRequest(TypedDict):
    id: Optional[int]
    iid: Optional[int]
    project_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    state: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    merge_status: Optional[str]
    approved: Optional[bool]
    approvals_required: Optional[int]
    approvals_left: Optional[int]
    require_password_to_approve: Optional[bool]
    approved_by: Optional[List[ApprovedBy]]
    suggested_approvers: Optional[List]
    approvers: Optional[List]
    approver_groups: Optional[List]
    user_has_approved: Optional[bool]
    user_can_approve: Optional[bool]
    approval_rules_left: Optional[List]
    has_approval_rules: Optional[bool]
    merge_request_approvers_available: Optional[bool]
    multiple_approval_rules_available: Optional[bool]
    invalid_approvers_rules: Optional[List]


def fetch_approvals_for_pull_requests(
        connection_gitlab_hostname: str | None = None,
        connection_gitlab_api_version: str | None = None,
        decrypted_token: str | None = None,
        project_id: str | None = None,
        pull_request_iid: str | None = None,
) -> MergeRequest | None:
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
        f"api/{connection_gitlab_api_version}/"
        f"projects/{project_id}/"
        f"merge_requests/{pull_request_iid}/"
        f"approvals"
    )
    headers: Mapping[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    response: Response = get(
        headers=headers,
        url=url,
    )
    response.raise_for_status()
    return response.json()
